#!/usr/bin/env python

'''
`shufflify` tests for `iterify` package.
'''

import random

import iterify as itfy

random.seed(1)


def test_empty():
    assert [*itfy.shufflify()] == []


def test_one():
    for val in 'a', 0, [], None:
        assert [*itfy.shufflify(val)] == [val]


def test_two():
    for v1 in 'a', 0, [], None:
        for v2 in 'b', 1, {}, None:
            assert [*itfy.shufflify(v1, v2)] in ([v1, v2], [v2, v1])

            while True:
                print('a')
                if [*itfy.shufflify(v1, v2)] == [v1, v2]:
                    break
            while True:
                print('b')
                if [*itfy.shufflify(v1, v2)] == [v2, v1]:
                    break
