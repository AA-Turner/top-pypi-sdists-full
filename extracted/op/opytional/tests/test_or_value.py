#!/usr/bin/env python

'''
`or_value` tests for `opytional` package.
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


def test_value_or_with_not_none():
    for value in value_battery_without_none:
        for fallback_value in value_battery_with_none:
            res = opyt.or_value(value, fallback_value)
            assert value == res or all(math.isnan(x) for x in [value, res])


def test_with_none():
    for fallback_value in value_battery_with_none:
        res = opyt.or_value(None, fallback_value)
        assert \
            fallback_value == res \
            or all(math.isnan(x) for x in [fallback_value, res])
