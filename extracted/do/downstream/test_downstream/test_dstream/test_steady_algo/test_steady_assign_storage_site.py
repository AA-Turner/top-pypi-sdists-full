import functools
import itertools as it
from random import randrange as rand
import typing

import pytest

from downstream.dstream import steady_algo as algo


def validate_steady_site_selection(fn: typing.Callable) -> typing.Callable:
    """Decorator to validate pre- and post-conditions on site selection."""

    @functools.wraps(fn)
    def wrapper(S: int, T: int) -> typing.Optional[int]:
        assert S.bit_count() == 1  # Assert S is a power of two
        assert 0 <= T  # Assert T is non-negative
        res = fn(S, T)
        assert res is None or 0 <= res < S  # Assert valid output
        return res

    return wrapper


site_selection = validate_steady_site_selection(algo.assign_storage_site)


def test_steady_site_selection8():
    # fmt: off
    actual = (site_selection(8, T) for T in it.count())
    expected = [
        0, 1, 4, 2, 6, 5, 7, 3,  # T 0-7
        None, 6, None, 4, None, 7, None, 0,  # T 8-15
        None, None, None, 6, None, None, None, 5,  # T 16-23
        None, None, None, 7, None, None, None, 1,  # T 24-31
        None, None, None, None, None, None, None, 6 # T 32-39
    ]
    assert all(x == y for x, y in zip(actual, expected))


def test_steady_site_selection16():
    # fmt: off
    actual = (site_selection(16, T) for T in it.count())
    expected = [
        0, 1, 5, 2, 8, 6, 10, 3,  # T 0-7 --- hv 0,1,0,2,0,1,0,3
        12, 9, 13, 7, 14, 11, 15, 4,  # T 8-15 --- hv 0,1,0,2,0,1,0,4
        None, 12, None  # T 16-18 --- hv 0,1,0
    ]
    assert all(x == y for x, y in zip(actual, expected))


def test_steady_site_selection_fuzz():
    testS = (1 << s for s in range(1, 33))
    testT = it.chain(range(10**5), (rand(2**128) for _ in range(10**5)))
    for S, T in it.product(testS, testT):
        site_selection(S, T)  # Validated via wrapper


@pytest.mark.parametrize("S", [1 << s for s in range(1, 21)])
def test_steady_site_selection_epoch0(S: int):
    actual = {site_selection(S, T) for T in range(S)}
    expected = set(range(S))
    assert actual == expected


def test_steady_site_selection_exceeds_capacity():
    with pytest.raises(ValueError):
        algo.assign_storage_site(7, 7)
