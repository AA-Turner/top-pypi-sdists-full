#!/usr/bin/env python

"""
`binary_search_iterative` tests for `interval_search` package.
"""

import interval_search as inch


def test_binary_search_iterative_singleton():
    assert inch.binary_search_iterative(lambda __: True, 10, 10) == 10


def test_binary_search_iterative():
    assert inch.binary_search_iterative(lambda x: x >= 5, 0, 100) == 5


def test_fruitless_binary_search_iterative():
    assert inch.binary_search_iterative(lambda x: False, 0, 100) is None


def test_empty_binary_search_iterative():
    assert inch.binary_search_iterative(lambda x: False, 100, 99) is None
    assert inch.binary_search_iterative(lambda x: False, 100, 0) is None
    assert inch.binary_search_iterative(lambda x: True, 100, 99) is None
    assert inch.binary_search_iterative(lambda x: True, 100, 0) is None
