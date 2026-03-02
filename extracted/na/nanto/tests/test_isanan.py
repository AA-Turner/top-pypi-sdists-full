#!/usr/bin/env python

'''
`apply_if_or_else` tests for `opyttional` package.
'''

from nanto import isanan

value_battery_without_nan = [
    0,
    1,
    0.0,
    1.0,
    float('inf'),
    None,
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


def test_with_value():
    for value in value_battery_without_nan:
        assert not isanan(value)


def test_with_nan():
    assert isanan(float('nan'))
