#!/usr/bin/env python

'''
`curried_binary_search` tests for `interval_search` package.
'''

import interval_search as inch


def test_curried_binary_search_singleton():
    assert inch.curried_binary_search(lambda __: True)(10, 10) == 10


def test_curried_binary_search():
    assert inch.curried_binary_search(lambda x: x >= 5)(0, 100) == 5


def test_fruitless_curried_binary_search():
    assert inch.curried_binary_search(lambda x: False)(0, 100) is None


def test_empty_curried_binary_search():
    assert inch.curried_binary_search(lambda x: False)(100, 99) is None
    assert inch.curried_binary_search(lambda x: False)(100, 0) is None
    assert inch.curried_binary_search(lambda x: True)(100, 99) is None
    assert inch.curried_binary_search(lambda x: True)(100, 0) is None
