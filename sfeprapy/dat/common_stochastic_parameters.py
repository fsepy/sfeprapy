import numpy as np

occ2hrrpua = dict(
    dwelling=dict(
        dist='uniform_',
        ubound=0.57,
        lbound=0.32,
        reference='',
    ),
    office=dict(
        dist='uniform_',
        ubound=0.15,
        lbound=0.65,
        reference='',
    ),
    retail=dict(
        dist='uniform_',
        ubound=0.27,
        lbound=1.,
        reference='',
    ),
    car_park=dict(
        dist='uniform_',
        ubound=0.09,
        lbound=0.62,
        reference='',
    ),
    refuse_store=dict(
        dist='uniform_',
        ubound=0.09,
        lbound=0.62,
        reference='',
    ),
    cycle_store=dict(
        dist='uniform_',
        ubound=0.,
        lbound=0.,
        reference='',
    ),
    shopping_centre=dict(
        dist='uniform_',
        ubound=0.,
        lbound=0.,
        reference='',
    ),
    storage_high_fuel_load=dict(
        dist='uniform_',
        ubound=0.,
        lbound=0.,
        reference='',
    ),
    storage_low_fuel_load=dict(
        dist='uniform_',
        ubound=0.,
        lbound=0.,
        reference='',
    ),
    school=dict(
        dist='uniform_',
        ubound=0.,
        lbound=0.,
        reference='',
    ),
    kitchen=dict(
        dist='uniform_',
        ubound=0.,
        lbound=0.,
        reference='',
    ),
    restaurant=dict(
        dist='uniform_',
        ubound=0.,
        lbound=0.,
        reference='',
    ),
    gym=dict(
        dist='uniform_',
        ubound=0.,
        lbound=0.,
        reference='',
    ),
)

occ2qfd = dict(
    dwelling=dict(
        dist='gumbel_r_',
        ubound=0.57,
        lbound=0.32,
        mean=0,
        sd=0,
        reference='',
    ),
    office=dict(
        dist='gumbel_r_',
        ubound=0.15,
        lbound=0.65,
        mean=0,
        sd=0,
        reference='',
    ),
    retail=dict(
        dist='gumbel_r_',
        ubound=0.27,
        lbound=1.,
        mean=0,
        sd=0,
        reference='',
    ),
    car_park=dict(
        dist='gumbel_r_',
        ubound=0.09,
        lbound=0.62,
        mean=0,
        sd=0,
        reference='',
    ),
    refuse_store=dict(
        dist='gumbel_r_',
        ubound=0.09,
        lbound=0.62,
        mean=0,
        sd=0,
        reference='',
    ),
    cycle_store=dict(
        dist='gumbel_r_',
        ubound=0.,
        lbound=0.,
        mean=0,
        sd=0,
        reference='',
    ),
    shopping_centre=dict(
        dist='gumbel_r_',
        ubound=0.,
        lbound=0.,
        mean=0,
        sd=0,
        reference='',
    ),
    storage_high_fuel_load=dict(
        dist='gumbel_r_',
        ubound=0.,
        lbound=0.,
        mean=0,
        sd=0,
        reference='',
    ),
    storage_low_fuel_load=dict(
        dist='gumbel_r_',
        ubound=0.,
        lbound=0.,
        mean=0,
        sd=0,
        reference='',
    ),
    school=dict(
        dist='gumbel_r_',
        ubound=0.,
        lbound=0.,
        mean=0,
        sd=0,
        reference='',
    ),
    kitchen=dict(
        dist='gumbel_r_',
        ubound=0.,
        lbound=0.,
        mean=0,
        sd=0,
        reference='',
    ),
    restaurant=dict(
        dist='gumbel_r_',
        ubound=0.,
        lbound=0.,
        mean=0,
        sd=0,
        reference='',
    ),
    gym=dict(
        dist='gumbel_r_',
        ubound=0.,
        lbound=0.,
        mean=0,
        sd=0,
        reference='',
    ),
)


def _test_keys_consistency():
    """To ensure `occ2hrrpua` and `occ2qfd`"""

    assert len(occ2qfd) == len(occ2hrrpua)

    assert all(i in occ2hrrpua.keys() for i in occ2qfd.keys())


if __name__ == '__main__':
    _test_keys_consistency()
