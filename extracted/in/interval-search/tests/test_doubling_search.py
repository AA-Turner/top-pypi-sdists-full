#!/usr/bin/env python

'''
`doubling_search` tests for `interval_search` package.
'''

import interval_search as inch


def test_doubling_search_trivial():
    assert inch.doubling_search(lambda __: True) == 0
    assert inch.doubling_search(lambda __: True, 10) == 10


def test_doubling_search_nontrivial():
    assert inch.doubling_search(lambda x: x >= 5) == 5
    assert inch.doubling_search(lambda x: x >= 5, 10) == 10
    assert inch.doubling_search(lambda x: x >= 422) == 422
    assert inch.doubling_search(lambda x: x >= 422, 10) == 422
    assert inch.doubling_search(lambda x: x >= 423) == 423
    assert inch.doubling_search(lambda x: x >= 423, 10) == 423

def test_doubling_search_nontrivial_satisfaction_bound():
    assert inch.doubling_search(lambda x: x >= 5, satisfaction_bound = 3) == 3
    assert inch.doubling_search(lambda x: x >= 5, satisfaction_bound = 5) == 5
    assert inch.doubling_search(lambda x: x >= 5, satisfaction_bound = 6) == 5
    assert inch.doubling_search(lambda x: x >= 5, 10, 0) == 10
    assert inch.doubling_search(lambda x: x >= 50, 10, 0) == 10
    assert inch.doubling_search(lambda x: x >= 422, 10, 10) == 10
    assert inch.doubling_search(lambda x: x >= 422, 10, 422) == 422
    assert inch.doubling_search(lambda x: x >= 422, 10, 430) == 422
