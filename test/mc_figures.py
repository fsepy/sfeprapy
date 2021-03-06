# -*- coding: utf-8 -*-
import numpy as np
from fsetools.lib.fse_bs_en_1991_1_2_parametric_fire import temperature as _fire_param
from fsetools.lib.fse_bs_en_1993_1_2_heat_transfer_c import temperature as _steel_heat_transfer
from fsetools.lib.fse_travelling_fire import temperature_si as _fire_travelling
from matplotlib import pyplot as plt

from sfeprapy.func.fire_iso834 import fire as _fire_iso


def fire_param(ax, label=None):
    x = np.arange(0, 60 * 180, 1, dtype=float)

    # PARAMETRIC FIRE
    inputs = {
        "t": x,
        "A_t": (10 * 40 + 40 * 2 + 2 * 10) * 2,
        "A_f": 10 * 40,
        "A_v": 5 * 5,
        "h_eq": 5,
        "q_fd": 420e6,
        "lambda_": 1,
        "rho": 1,
        "c": 2250000,
        "t_lim": 20 * 60,
        "temperature_initial": 273.15
    }
    y = _fire_param(**inputs)

    ax.plot(x / 60., y - 273.15, label=label)


def fire_travel(ax, label=None):
    x = np.arange(0, 60 * 180, 1, dtype=float)

    inputs = {
        "t": x,
        "T_0": 273.15,
        "q_fd": 420e6,
        "hrrpua": 0.15e6,
        "l": 40,
        "w": 10,
        "s": 0.01,
        "e_h": 4.5,
        "e_l": 25,
    }
    y = _fire_travelling(**inputs)

    ax.plot(x / 60., y - 273.15, label=label)


def heat_transfer_param(ax, label=None):
    x = np.arange(0, 60 * 180, 1, dtype=float)

    # PARAMETRIC FIRE
    inputs_parametric_fire = {
        "t": x,
        "A_t": 360,
        "A_f": 100,
        "A_v": 21.6,
        "h_eq": 1,
        "q_fd": 600e6,
        "lambda_": 1,
        "rho": 1,
        "c": 2250000,
        "t_lim": 20 * 60,
        "temperature_initial": 273.15
    }
    y_ = _fire_param(**inputs_parametric_fire)

    y = _steel_heat_transfer(
        fire_time=x,
        fire_temperature=y_,
        beam_rho=7850,
        beam_cross_section_area=0.017,
        protection_k=0.2,
        protection_rho=800,
        protection_c=1700,
        protection_thickness=0.00938,
        protection_protected_perimeter=2.14,
    )

    ax.plot(x / 60., y - 273.15, label=label)


def heat_transfer_travel(ax, label=None):
    x = np.arange(0, 60 * 180, 1, dtype=float)

    inputs = {
        "t": x,
        "T_0": 273.15,
        "q_fd": 420e6,
        "hrrpua": 0.15e6,
        "l": 40,
        "w": 10,
        "s": 0.01,
        "e_h": 4.5,
        "e_l": 25,
    }
    y_ = _fire_travelling(**inputs)

    y = _steel_heat_transfer(
        fire_time=x,
        fire_temperature=y_,
        beam_rho=7850,
        beam_cross_section_area=0.017,
        protection_k=0.2,
        protection_rho=800,
        protection_c=1700,
        protection_thickness=0.00938,
        protection_protected_perimeter=2.14,
    )

    ax.plot(x / 60., y - 273.15, label=label)


def fire_iso834(ax, label=None):
    x = np.arange(0, 60 * 180, 1)
    y = _fire_iso(x, 20 + 273.15)

    ax.plot(x / 60., y - 273.15, label=label)


def plot_examples(list_func, list_linelabel, figname, xlabel, ylabel):
    plt.style.use('seaborn-paper')

    fig, ax = plt.subplots(figsize=(3.94 * 1.5, 2.76 * 1.5))  # (3.94, 2.76) for large and (2.5, 2) for small figure size
    for i, func in enumerate(list_func):
        func(ax, label=list_linelabel[i])
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim((0, 120))
    ax.set_ylim((0, 1400))
    try:
        if isinstance(list_linelabel[0], str):
            ax.legend().set_visible(True)
    except KeyError:
        pass
    fig.tight_layout()
    fig.savefig(figname, dpi=300, transparent=True, bbox_inches='tight')


if __name__ == '__main__':
    plt.style.use('seaborn-paper')

    plot_examples(
        [fire_travel, heat_transfer_travel], ["Gas temperature", "Steel temperature"],
        'heat_transfer_travel.png', 'Time [minute]', 'Temperature [$^{\circ}C$]'
    )

    plot_examples(
        [fire_param], [None],
        'fire_param.png', 'Time [minute]', 'Temperature [$^{\circ}C$]'
    )

    plot_examples(
        [fire_param, heat_transfer_param], ["Gas temperature", "Steel temperature"],
        'heat_transfer_param.png', 'Time [minute]', 'Temperature [$^{\circ}C$]'
    )

    plot_examples(
        [fire_travel, fire_param], ["Gas temperature - Parametric fire", "Gas temperature - Travelling fire"],
        'fire_travel_param.png', 'Time [minute]', 'Temperature [$^{\circ}C$]'
    )

    plot_examples(
        [fire_iso834], [None],
        'fire_iso.png', 'Time [minute]', 'Temperature [$^{\circ}C$]'
    )
