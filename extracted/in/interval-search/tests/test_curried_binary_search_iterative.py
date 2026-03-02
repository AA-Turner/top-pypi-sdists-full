#!/usr/bin/env python

"""
`curried_binary_search_iterative` tests for `interval_search` package.
"""

import interval_search as inch


def test_curried_binary_search_iterative_singleton():
    assert inch.curried_binary_search_iterative(lambda __: True)(10, 10) == 10


def test_curried_binary_search_iterative():
    assert inch.curried_binary_search_iterative(lambda x: x >= 5)(0, 100) == 5


def test_fruitless_curried_binary_search_iterative():
    assert inch.curried_binary_search_iterative(lambda x: False)(
        0, 100
    ) is None


def test_empty_curried_binary_search_iterative():
    assert inch.curried_binary_search_iterative(lambda x: False)(
        100, 99
    ) is None
    assert inch.curried_binary_search_iterative(lambda x: False)(
        100, 0
    ) is None
    assert inch.curried_binary_search_iterative(lambda x: True)(
        100, 99
    ) is None
    assert inch.curried_binary_search_iterative(lambda x: True)(100, 0) is None
