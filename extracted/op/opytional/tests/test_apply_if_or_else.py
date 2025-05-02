#!/usr/bin/env python

'''
`apply_if_or_else` tests for `opyttional` package.
'''

import math

import opytional as opyt

value_battery_without_none = [
    0,
    1,
    0.0,
    1.0,
    float('inf'),
    # requires np.testing.assert_equal because nan != nan otherwise
    float('nan'),
    False,
    True,
    '',
    'None',
    'hello',
    [],
    [None],
    ['greetings'],
    [[]],
]

value_battery_with_none = value_battery_without_none + [None]


def test_with_value():
    for value in value_battery_without_none:
        for fallback_value in value_battery_with_none:
            res = opyt.apply_if_or_else(
                value,
                lambda x: x,
                lambda: fallback_value
            )
            assert value == res or all(math.isnan(x) for x in [value, res])

            res = opyt.apply_if_or_else(
                value,
                lambda x: [x],
                lambda: fallback_value
            )
            assert [value] == res or all(math.isnan(x) for x, in [value, res])

            assert opyt.apply_if_or_else(
                value,
                lambda x: None,
                lambda: fallback_value,
            ) is None


def test_with_none():
    for fallback_value in value_battery_with_none:
        res = opyt.apply_if_or_else(
            None,
            lambda x: x,
            lambda: fallback_value,
        )
        assert \
            fallback_value == res \
            or all(math.isnan(x) for x in [fallback_value, res])

        res = opyt.apply_if_or_else(
            None,
            lambda x: [x],
            lambda: fallback_value,
        )
        assert \
            fallback_value == res \
            or all(math.isnan(x) for x in [fallback_value, res])

        res = opyt.apply_if_or_else(
            None,
            lambda x: None,
            lambda: fallback_value,
        )
        assert \
            fallback_value == res \
            or all(math.isnan(x) for x in [fallback_value, res])
