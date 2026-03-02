#!/usr/bin/env python

'''
`cyclify` tests for `iterify` package.
'''

import iterify as itfy


def test_empty():
    assert [*itfy.cyclify()] == []


def test_one():
    for val in 'a', 0, [], None:
        it = itfy.cyclify(val)
        for __ in range(10):
            assert next(it) == val


def test_two():
    for val1 in 'a', 0, [], None:
        for val2 in 'b', 1, {}, None:
            it = itfy.cyclify(val1, val2)
            for __ in range(10):
                assert next(it) == val1
                assert next(it) == val2
