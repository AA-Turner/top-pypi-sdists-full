#!/usr/bin/env python

'''
`iterify` tests for `iterify` package.
'''

import iterify as itfy


def test_empty():
    assert [*itfy.iterify()] == []


def test_one():
    for val in 'a', 0, [], None:
        assert [*itfy.iterify(val)] == [val]


def test_two():
    for val1 in 'a', 0, [], None:
        for val2 in 'b', 1, {}, None:
            assert [*itfy.iterify(val1, val2)] == [val1, val2]
