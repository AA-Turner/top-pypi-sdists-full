#!/usr/bin/env python

'''
`curried_doubling_search` tests for `interval_search` package.
'''

import interval_search as inch


def test_curried_doubling_search_trivial():
    assert inch.curried_doubling_search(lambda __: True)() == 0
    assert inch.curried_doubling_search(lambda __: True)(10) == 10


def test_curried_doubling_search_nontrivial():
    assert inch.curried_doubling_search(lambda x: x >= 5)() == 5
    assert inch.curried_doubling_search(lambda x: x >= 5)(10) == 10
    assert inch.curried_doubling_search(lambda x: x >= 422)() == 422
    assert inch.curried_doubling_search(lambda x: x >= 422)(10) == 422
    assert inch.curried_doubling_search(lambda x: x >= 423)() == 423
    assert inch.curried_doubling_search(lambda x: x >= 423)(10) == 423
