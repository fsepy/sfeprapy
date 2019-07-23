import os
import time
import json
import warnings
import pandas as pd
from typing import Union
from tkinter import filedialog, Tk, StringVar

from tqdm import tqdm


class MCS:
    DEFAULT_TEMP_FOLDER_NAME = 'temp'
    DEFAULT_CONFIG_FILE_NAME = 'config.json'
    DEFAULT_CONFIG = dict(n_threads=1, output_fires=0)

    def __init__(self):
        self._path_wd = None

        self._dict_master_input = None
        self._dict_config = None

        self._func_mcs_gen = None
        self._func_mcs_calc = None
        self._func_mcs_calc_mp = None

        self._df_mcs_out = None

    @property
    def path_wd(self):
        return self._path_wd

    @property
    def input(self) -> dict:
        return self._dict_master_input

    @property
    def config(self):
        return self._dict_config

    @property
    def func_mcs_gen(self):
        return self._func_mcs_gen

    @property
    def func_mcs_calc_mp(self):
        return self._func_mcs_calc_mp

    @property
    def func_mcs_calc(self):
        return self._func_mcs_calc

    @property
    def mcs_out(self) -> pd.DataFrame:
        return self._df_mcs_out

    @path_wd.setter
    def path_wd(self, p_):
        assert os.path.isdir(p_)
        self._path_wd = p_

    @input.setter
    def input(self, dict_: dict):
        self._dict_master_input = dict_

    @config.setter
    def config(self, dict_config: dict):
        self._dict_config = dict_config

    @func_mcs_gen.setter
    def func_mcs_gen(self, func_mcs_gen):
        self._func_mcs_gen = func_mcs_gen

    @func_mcs_calc.setter
    def func_mcs_calc(self, func_mcs_calc):
        self._func_mcs_calc = func_mcs_calc

    @func_mcs_calc_mp.setter
    def func_mcs_calc_mp(self, func_mcs_calc_mp):
        self._func_mcs_calc_mp = func_mcs_calc_mp

    @mcs_out.setter
    def mcs_out(self, df_out: pd.DataFrame):
        self._df_mcs_out = df_out

    def define_problem(self, data: Union[str, pd.DataFrame, dict] = None, config: dict = None, path_wd: str = None):

        # to get problem definition: try to parse from csv/xls/xlsx

        if data is None:
            fp = os.path.realpath(self._get_file_path_gui())
            self.path_wd = os.path.dirname(fp)
            if fp.endswith('.xlsx') or fp.endswith('.xls'):
                self.input = pd.read_excel(fp).set_index('PARAMETERS').to_dict()
            elif fp.endswith('.csv'):
                self.input = pd.read_csv(fp).set_index('PARAMETERS').to_dict()
            else:
                raise ValueError('Unknown input file format.')
        elif isinstance(data, str):
            fp = data
            self.path_wd = os.path.dirname(fp)
            if fp.endswith('.xlsx') or fp.endswith('.xls'):
                self.input = pd.read_excel(fp).set_index('PARAMETERS').to_dict()
            elif fp.endswith('.csv'):
                self.input = pd.read_csv(fp).set_index('PARAMETERS').to_dict()
            else:
                raise ValueError('Unknown input file format.')
        elif isinstance(data, pd.DataFrame):
            self.input = data.to_dict()
        elif isinstance(data, dict):
            self.input = data
        else:
            raise TypeError("Unknown input data type.")

        # to get configuration: try to parse from cwd if there is any, otherwise chose default values

        if self.path_wd is None:
            self.config = self.DEFAULT_CONFIG
        elif os.path.isfile(os.path.join(self.path_wd, self.DEFAULT_CONFIG_FILE_NAME)):
            with open(os.path.join(self.path_wd, self.DEFAULT_CONFIG_FILE_NAME), 'r') as f:
                self.config = json.load(f)
        else:
            self.config = self.DEFAULT_CONFIG

    def define_stochastic_parameter_generator(self, func):
        self.func_mcs_gen = func

    def define_calculation_routine(self, func, func_mp=None):
        self.func_mcs_calc = func
        self.func_mcs_calc_mp = func_mp

    def run_mcs(self):
        # Check whether required parameters are defined
        err_msg = list()
        if self._dict_master_input is None:
            err_msg.append('Problem definition is not defined.')
        if self._func_mcs_calc is None:
            err_msg.append('Monte Carlo Simulation calculation routine is not defined.')
        if self._func_mcs_gen is None:
            err_msg.append('Monte Carlo Simulation stochastic parameter generator is not defined.')
        if len(err_msg) > 0:
            raise ValueError(r'\n'.join(err_msg))

        # Prepare mcs parameter inputs
        x1 = self.input
        for case_name in list(x1.keys()):
            for param_name in list(x1[case_name].keys()):

                if ':' in param_name:
                    param_name_parent, param_name_sibling = param_name.split(':')
                    if param_name_parent not in x1[case_name]:
                        x1[case_name][param_name_parent] = dict()
                    x1[case_name][param_name_parent][param_name_sibling] = x1[case_name].pop(param_name)
        # to convert all "string numbers" to float data type
        for case_name in x1.keys():
            for i, v in x1[case_name].items():
                if isinstance(v, dict):
                    for ii, vv in v.items():
                        try:
                            x1[case_name][i][ii] = float(vv)
                        except:
                            pass
                else:
                    try:
                        x1[case_name][i] = float(v)
                    except:
                        pass

        # Generate mcs parameter samples
        x2 = {k: self.func_mcs_gen(v, int(v['n_simulations'])) for k, v in x1.items()}

        # Run mcs simulation
        x3 = dict()
        for k, v in x2.items():
            x3[k] = self._mcs_mp(self.func_mcs_calc, self.func_mcs_calc_mp, x=v, n_threads=self.config['n_threads'])
            if self.path_wd:
                x3[k].to_csv(os.path.join(self.path_wd, self.DEFAULT_TEMP_FOLDER_NAME, f'{k}.csv'))

        self.mcs_out = pd.concat([v for v in x3.values()])

        if self.path_wd:
            self.mcs_out.to_csv(os.path.join(self.path_wd, 'mcs_out.csv'), index=False)

    @staticmethod
    def _mcs_mp(func, func_mp, x: pd.DataFrame, n_threads: int):
        list_mcs_in = x.to_dict(orient='records')

        print('{:<24.24}: {}'.format("CASE", list_mcs_in[0]['case_name']))
        print('{:<24.24}: {}'.format("NO. OF THREADS", n_threads))
        print('{:<24.24}: {}'.format("NO. OF SIMULATIONS", len(x.index)))

        if n_threads == 1:
            mcs_out = list()
            for i in tqdm(list_mcs_in, ncols=60):
                mcs_out.append(func(**i))
        else:
            import multiprocessing as mp
            m, p = mp.Manager(), mp.Pool(n_threads, maxtasksperchild=1000)
            q = m.Queue()
            jobs = p.map_async(func_mp, [(dict_, q) for dict_ in list_mcs_in])
            n_simulations = len(list_mcs_in)
            with tqdm(total=n_simulations, ncols=60) as pbar:
                while True:
                    if jobs.ready():
                        if n_simulations > pbar.n:
                            pbar.update(n_simulations - pbar.n)
                        break
                    else:
                        if q.qsize() - pbar.n > 0:
                            pbar.update(q.qsize() - pbar.n)
                        time.sleep(1)
                p.close()
                p.join()
                mcs_out = jobs.get()

        df_mcs_out = pd.DataFrame(mcs_out)

        try:
            df_mcs_out.drop('fire_temperature', inplace=True, axis=1)
        except KeyError:
            pass

        df_mcs_out.sort_values('solver_time_equivalence_solved', inplace=True)  # sort base on time equivalence

        return df_mcs_out

    @staticmethod
    def _get_file_path_gui():
        # get a list of dict()s representing different scenarios
        root = Tk()
        root.withdraw()
        folder_path = StringVar()

        path_input_file_csv = filedialog.askopenfile(title='Select Input File', filetypes=[('csv', ['.csv'])])
        folder_path.set(path_input_file_csv)
        root.update()

        try:
            path_input_file_csv = os.path.realpath(path_input_file_csv.name)
            return path_input_file_csv
        except AttributeError:
            raise FileNotFoundError('file not found.')


def test():

    # test gui version
    def test_gui():
        from sfeprapy.mcs0.mcs0_calc import teq_main as calc
        from sfeprapy.mcs0.mcs0_calc import teq_main_wrapper as calc_mp
        from sfeprapy.func.mcs_gen import main as gen
        mcs = MCS()
        mcs.define_problem()
        mcs.define_stochastic_parameter_generator(gen)
        mcs.define_calculation_routine(calc, calc_mp)
        mcs.run_mcs()

    # test non-gui version
    def test_arg_dict():
        import sfeprapy.mcs0 as mcs0
        from sfeprapy.mcs0.mcs0_calc import teq_main as calc
        from sfeprapy.mcs0.mcs0_calc import teq_main_wrapper as calc_mp
        from sfeprapy.func.mcs_gen import main as gen
        mcs = MCS()
        mcs.define_problem(data=mcs0.EXAMPLE_INPUT_DICT, config=mcs0.EXAMPLE_CONFIG_DICT)
        mcs.define_stochastic_parameter_generator(gen)
        mcs.define_calculation_routine(calc, calc_mp)
        mcs.run_mcs()

    test_gui()
    test_arg_dict()

if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    test()