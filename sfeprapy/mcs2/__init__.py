# -*- coding: utf-8 -*-
import pandas as pd

from sfeprapy.func.mcs_gen import dict_flatten


def __example_config_dict():
    return dict(n_threads=2, cwd='')


def __example_input_dict():
    y = {
        "Standard Case 1": dict(
            case_name="Standard Case 1",
            n_simulations=5000,
            fire_time_step=30,
            fire_time_duration=18000,
            fire_hrr_density=0.25,
            fire_load_density=dict(dist="gumbel_r_", lbound=10, ubound=1200, mean=420, sd=126),
            fire_spread_speed=dict(dist="uniform_", lbound=0.0035, ubound=0.0190),
            fire_nft_limit=dict(dist="norm_", lbound=623.15, ubound=2023.15, mean=1323.15, sd=93),
            fire_combustion_efficiency=1.0,
            window_open_fraction=1.0,
            phi_teq=dict(dist="constant_", ubound=1, lbound=1, mean=0, sd=0),
            beam_cross_section_area=0.017,
            beam_position_horizontal=-1,
            beam_position_vertical=3.2,
            beam_rho=7850,
            fire_mode=0,
            fire_gamma_fi_q=1,
            fire_t_alpha=300,
            fire_tlim=0.333,
            protection_c=1700,
            protection_k=0.2,
            protection_protected_perimeter=2.14,
            protection_rho=800,
            room_floor_area=500,
            room_breadth_depth_ratio=dict(dist="uniform_", lbound=0.512 - 0.2, ubound=0.512 + 0.2),
            room_height=3,
            room_wall_thermal_inertia=720,
            solver_temperature_goal=893.15,
            solver_max_iter=20,
            solver_thickness_lbound=0.0001,
            solver_thickness_ubound=0.0500,
            solver_tol=1.0,
            window_height=2.8,
            window_floor_ratio=dict(dist="uniform_", lbound=0.05, ubound=0.4),
            window_open_fraction_permanent=0,
            timber_exposed_area=0,
            timber_charring_rate=0.7,  # mm/min
            timber_hc=13.2,  # MJ/kg
            timber_density=400,  # [kg/m3]
            timber_solver_ilim=20,
            timber_solver_tol=1,
        ),
    }
    return y


def __example_input_csv(x: dict):
    y = {k: dict_flatten(v) for k, v in x.items()}
    y = pd.DataFrame.from_dict(y, orient="columns")
    y.index.name = "PARAMETERS"
    y = y.to_csv(index=True, line_terminator='\n')
    return y


def __example_input_df(x: dict) -> pd.DataFrame:
    y = {k: dict_flatten(v) for k, v in x.items()}
    y = pd.DataFrame.from_dict(y, orient="columns")
    y.index.name = "PARAMETERS"
    return y


EXAMPLE_CONFIG_DICT = __example_config_dict()
EXAMPLE_INPUT_DICT = __example_input_dict()
EXAMPLE_INPUT_CSV = __example_input_csv(__example_input_dict())
EXAMPLE_INPUT_DF = __example_input_df(__example_input_dict())

if __name__ == "__main__":
    print(EXAMPLE_CONFIG_DICT, "\n")
    print(EXAMPLE_INPUT_DICT, "\n")
    print(EXAMPLE_INPUT_CSV, "\n")
