#!/usr/bin/env python

'''
`apply_if_or_value` tests for `opyttional` package.
'''

import math

import opytional as opyt

value_battery_without_none = [
    0,
    1,
    0.0,
    1.0,
    float('inf'),
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
            res = opyt.apply_if_or_value(
                value,
                lambda x: x,
                fallback_value
            )
            assert value == res or all(math.isnan(x) for x in [value, res])

            res = opyt.apply_if_or_value(
                value,
                lambda x: [x],
                fallback_value
            )
            assert [value] == res or all(math.isnan(x) for x, in [value, res])

            assert opyt.apply_if_or_value(
                value,
                lambda x: None,
                fallback_value,
            ) is None


def test_with_none():
    for fallback_value in value_battery_with_none:
        res = opyt.apply_if_or_value(
            None,
            lambda x: x,
            fallback_value,
        )
        assert \
            fallback_value == res \
            or all(math.isnan(x) for x in [fallback_value, res])

        res = opyt.apply_if_or_value(
            None,
            lambda x: [x],
            fallback_value,
        )
        assert \
            fallback_value == res \
            or all(math.isnan(x) for x in [fallback_value, res])

        res = opyt.apply_if_or_value(
            None,
            lambda x: None,
            fallback_value,
        )
        assert \
            fallback_value == res \
            or all(math.isnan(x) for x in [fallback_value, res])
