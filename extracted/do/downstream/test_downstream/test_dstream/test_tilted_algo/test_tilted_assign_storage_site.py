import functools
import itertools as it
import typing

import pytest

from downstream.dstream import tilted_algo as algo


def validate_tilted_site_selection(fn: typing.Callable) -> typing.Callable:
    """Decorator to validate pre- and post-conditions on site selection."""

    @functools.wraps(fn)
    def wrapper(S: int, T: int) -> typing.Optional[int]:
        assert S.bit_count() == 1  # Assert S is a power of two
        assert S >= 8  # Assert S is at least 8
        assert 0 <= T  # Assert T is non-negative
        res = fn(S, T)
        assert 0 <= res < S  # Assert valid output
        return res

    return wrapper


site_selection = validate_tilted_site_selection(algo.assign_storage_site)


def test_tilted_site_selection8():
    # fmt: off
    actual = (site_selection(8, T) for T in it.count())
    expected = [
        0, 1, 5, 2, 4, 6, 7, 3,  # T 0-7
        0, 1, 5, 7, 0, 6, 5, 4,  # T 8-15
        0, 1, 0, 2, 0, 6, 0, 3,  # T 16-23
        0, 1, 0, 7, 0, 6, 0, 5,  # T 24-31
        0, 1, 0, 2, 0, 1, 0, 3 # T 32-39
    ]
    assert all(x == y for x, y in zip(actual, expected))


def test_tilted_site_selection16():
    # fmt: off
    actual = (site_selection(16, T) for T in it.count())
    expected = [
        0, 1, 9, 2, 6, 10, 13, 3,  # T 0-7 --- hv 0,1,0,2,0,1,0,3
        5, 7, 8, 11, 12, 14, 15, 4,  # T 8-15 --- hv 0,1,0,2,0,1,0,4
        0, 1, 9, 8, 6, 10, 13, 12,  # T 16-24 --- hv 0,1,0, ...
        0, 7, 9, 15, 6, 14, 13, 5,  # T 24-31
        0, 1, 9, 2, 0, 10, 9, 3 # T 32-39
    ]
    assert all(x == y for x, y in zip(actual, expected))


def test_tilted_site_selection_fuzz():
    for S in (1 << s for s in range(3, 17)):
        for T in range(S - 1):
            site_selection(S, T)  # Validated via wrapper


@pytest.mark.parametrize("S", [1 << s for s in range(3, 17)])
def test_tilted_site_selection_epoch0(S: int):
    actual = {site_selection(S, T) for T in range(S)}
    expected = set(range(S))
    assert actual == expected


def test_tilted_site_selection_exceeds_capacity():
    with pytest.raises(ValueError):
        algo.assign_storage_site(7, 7)
