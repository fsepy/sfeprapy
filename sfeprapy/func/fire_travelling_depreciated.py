# -*- coding: utf-8 -*-
import copy
from typing import Union

import numpy as np


def fire(
        t: np.array,
        fire_load_density_MJm2: float,
        fire_hrr_density_MWm2: float,
        room_length_m: float,
        room_width_m: float,
        fire_spread_rate_ms: float,
        beam_location_height_m: float,
        beam_location_length_m: Union[float, list, np.ndarray],
        fire_nft_limit_c: float,
        opening_fraction: float = 0,
        opening_width_m: float = 0,
        opening_height_m: float = 0,
):
    """
    This function calculates and returns a temperature array representing travelling fire. This function is NOT in SI.
    :param t: in s, is the time array
    :param fire_load_density_MJm2: in MJ/m2, is the fuel density on the floor
    :param fire_hrr_density_MWm2: in MW/m2, is the heat release rate density
    :param room_length_m: in m, is the room length
    :param room_width_m: in m, is the room width
    :param fire_spread_rate_ms: in m/s, is fire spread speed
    :param beam_location_height_m: in m, is the beam lateral distance to fire origin
    :param beam_location_length_m: in m, is the beam height above the floor
    :param fire_nft_limit_c: in deg.C, is the maximum near field temperature
    :param opening_fraction: in -, is the ventilation opening proportion between 0 to 1
    :param opening_width_m: in m, is ventilation opening width
    :param opening_height_m: in m, is ventilation opening height
    :return T_g: in deg.C, is calculated gas temperature
    """

    # re-assign variable names for equation readability
    q_fd = fire_load_density_MJm2
    HRRPUA = fire_hrr_density_MWm2
    l = max([room_length_m, room_width_m])
    w = min([room_length_m, room_width_m])
    s = fire_spread_rate_ms
    h_s = beam_location_height_m
    l_s = beam_location_length_m

    # work out ventilation conditions

    # a_v = opening_height_m * opening_width_m * opening_fraction
    # Qv = 1.75 * a_v * np.sqrt(opening_height_m)

    # workout burning time etc.
    t_burn = max([q_fd / HRRPUA, 900.])
    t_decay = max([t_burn, l / s])
    t_lim = min([t_burn, l / s])

    # reduce resolution to fit time step for t_burn, t_decay, t_lim
    time_interval_s = t[1] - t[0]
    t_decay_ = round(t_decay / time_interval_s, 0) * time_interval_s
    t_lim_ = round(t_lim / time_interval_s, 0) * time_interval_s
    if t_decay_ == t_lim_: t_lim_ -= time_interval_s

    # workout the heat release rate ARRAY (corrected with time)
    Q_growth = (HRRPUA * w * s * t) * (t < t_lim_)
    Q_peak = min([HRRPUA * w * s * t_burn, HRRPUA * w * l]) * (t >= t_lim_) * (t <= t_decay_)
    Q_decay = (max(Q_peak) - (t - t_decay_) * w * s * HRRPUA) * (t > t_decay_)
    Q_decay[Q_decay < 0] = 0
    Q = (Q_growth + Q_peak + Q_decay) * 1000.

    # workout the distance between fire median to the structural element r
    l_fire_front = s * t
    l_fire_front[l_fire_front < 0] = 0
    l_fire_front[l_fire_front > l] = l
    l_fire_end = s * (t - t_lim)
    l_fire_end[l_fire_end < 0] = 0.
    l_fire_end[l_fire_end > l] = l
    l_fire_median = (l_fire_front + l_fire_end) / 2.

    # workout the far field temperature of gas T_g
    if isinstance(l_s, float) or isinstance(l_s, int):
        r = np.absolute(l_s - l_fire_median)
        T_g = np.where((r / h_s) > 0.8, (5.38 * np.power(Q / r, 2 / 3) / h_s) + 20., 0)
        T_g = np.where((r / h_s) <= 0.8, (16.9 * np.power(Q, 2 / 3) / np.power(h_s, 5 / 3)) + 20., T_g)
        T_g[T_g >= fire_nft_limit_c] = fire_nft_limit_c
        return T_g
    elif isinstance(l_s, np.ndarray) or isinstance(l_s, list):
        l_s_list = copy.copy(l_s)
        T_g_list = list()
        for l_s in l_s_list:
            r = np.absolute(l_s - l_fire_median)
            T_g = np.where((r / h_s) > 0.8, (5.38 * np.power(Q / r, 2 / 3) / h_s) + 20., 0)
            T_g = np.where((r / h_s) <= 0.8, (16.9 * np.power(Q, 2 / 3) / np.power(h_s, 5 / 3)) + 20., T_g)
            T_g[T_g >= fire_nft_limit_c] = fire_nft_limit_c
            T_g_list.append(T_g)
        return T_g_list
    else:
        raise TypeError('Unknown type of parameter "l_s": {}'.format(type(l_s)))


def check_fire():
    time = np.arange(0, 210 * 60, 30)
    list_l = [25, 50, 100, 150]

    import matplotlib.pyplot as plt
    plt.style.use('seaborn-paper')
    fig, ax = plt.subplots(figsize=(3.94, 2.76))
    ax.set_xlabel('Time [minute]')
    ax.set_ylabel('Temperature [$^{\circ}C$]')

    for length in list_l:
        temperature = fire(
            t=time,
            fire_load_density_MJm2=600,
            fire_hrr_density_MWm2=0.25,
            room_length_m=length,
            room_width_m=16,
            fire_spread_rate_ms=0.012,
            beam_location_height_m=3,
            beam_location_length_m=length / 2,
            fire_nft_limit_c=1050,
        )

        ax.plot(time / 60, temperature, label="Room length {:4.0f} m".format(length))

    ax.legend(loc=4).set_visible(True)
    ax.set_xlim((-10, 190))
    ax.grid(color='k', linestyle='--')
    plt.tight_layout()
    plt.show()


def check_fire_multiple_beam_location():
    time = np.arange(0, 210 * 60, 30)
    length = 100

    import matplotlib.pyplot as plt
    plt.style.use('seaborn-paper')
    fig, ax = plt.subplots(figsize=(3.94, 2.76))
    ax.set_xlabel('Time [minute]')
    ax.set_ylabel('Temperature [$^{\circ}C$]')

    temperature_list = fire(
        t=time,
        fire_load_density_MJm2=600,
        fire_hrr_density_MWm2=0.25,
        room_length_m=length,
        room_width_m=16,
        fire_spread_rate_ms=0.012,
        beam_location_height_m=3,
        beam_location_length_m=np.linspace(0, length, 12)[1:-1],
        fire_nft_limit_c=1050,
    )

    for temperature in temperature_list:
        ax.plot(time / 60, temperature, label="Room length {:4.0f} m".format(length))

    ax.legend(loc=4).set_visible(True)
    ax.set_xlim((-10, 190))
    ax.grid(color='k', linestyle='--')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    check_fire_multiple_beam_location()
    check_fire()