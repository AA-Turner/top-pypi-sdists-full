#!/usr/bin/env python

'''
`samplify` tests for `iterify` package.
'''

import random

import iterify as itfy

random.seed(1)


def test_empty():
    assert [*itfy.samplify()] == []


def test_one():
    for val in 'a', 0, [], None:
        it = itfy.cyclify(val)
        for __ in range(10):
            assert next(it) == val


def test_two():
    for val1 in 'a', 0, [], None:
        for val2 in 'b', 1, {}, None:
            it = itfy.samplify(val1, val2)
            for __ in range(10):
                assert next(it) in (val1, val2)
                while next(it) != val1:
                    pass
                while next(it) != val2:
                    pass
