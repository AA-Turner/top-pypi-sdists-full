#!/usr/bin/env python

'''
`apply_if` tests for `opytional` package.
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
        res = opyt.apply_if(value, lambda x: x)
        assert value == res or all(math.isnan(x) for x in [value, res])

        res = opyt.apply_if(value, lambda x: [x])
        assert [value] == res or all(math.isnan(x) for x, in [value, res])

        assert opyt.apply_if(value, lambda x: None) is None


def test_with_none():
    assert opyt.apply_if(None, lambda x: x) is None
    assert opyt.apply_if(None, lambda x: [x]) is None
    assert opyt.apply_if(None, lambda x: None) is None
