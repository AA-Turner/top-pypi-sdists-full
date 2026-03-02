#!/usr/bin/env python

'''
`doubling_search` tests for `interval_search` package.
'''

import interval_search as inch


def test_binary_search_singleton():
    assert inch.interval_search(lambda __: True, 10, 10) == 10

def test_binary_search():
    assert inch.interval_search(lambda x: x >= 5, 0, 100) == 5

def test_fruitless_binary_search():
    assert inch.interval_search(lambda x: False, 0, 100) is None

def test_empty_binary_search():
    assert inch.interval_search(lambda x: False, 100, 99) is None
    assert inch.interval_search(lambda x: False, 100, 0) is None
    assert inch.interval_search(lambda x: True, 100, 99) is None
    assert inch.interval_search(lambda x: True, 100, 0) is None

def test_doubling_search_trivial():
    assert inch.interval_search(lambda __: True) == 0
    assert inch.interval_search(lambda __: True, 10) == 10

def test_doubling_search_nontrivial():
    assert inch.interval_search(lambda x: x >= 5) == 5
    assert inch.interval_search(lambda x: x >= 5, 10) == 10
    assert inch.interval_search(lambda x: x >= 422) == 422
    assert inch.interval_search(lambda x: x >= 422, 10) == 422
    assert inch.interval_search(lambda x: x >= 423) == 423
    assert inch.interval_search(lambda x: x >= 423, 10) == 423
