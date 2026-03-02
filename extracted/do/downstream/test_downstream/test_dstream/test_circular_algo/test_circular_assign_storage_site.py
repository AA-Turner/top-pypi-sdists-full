import functools
import itertools as it
from random import randrange as rand
import typing

import pytest

from downstream.dstream import circular_algo as algo


def validate_circular_site_selection(
    fn: typing.Callable,
) -> typing.Callable:
    """Decorator to validate pre- and post-conditions on site selection."""

    @functools.wraps(fn)
    def wrapper(S: int, T: int) -> typing.Optional[int]:
        assert S > 0  # Assert S is positive
        assert 0 <= T  # Assert T is non-negative
        res = fn(S, T)
        assert res is None or 0 <= res < S  # Assert valid output
        return res

    return wrapper


site_selection = validate_circular_site_selection(algo.assign_storage_site)


def test_circular_site_selection3():
    # fmt: off
    actual = (site_selection(3, T) for T in it.count())
    expected = [
        0, 1, 2,  # T 0-2
        0, 1, 2,  # T 3-5
        0, 1, 2,  # T 6-8
        0, 1, 2,  # T 9-11
        0, 1, 2,  # T 12-14
        0, 1, 2,  # T 15-17
    ]
    assert all(x == y for x, y in zip(actual, expected))


def test_circular_site_selection5():
    # fmt: off
    actual = (site_selection(5, T) for T in it.count())
    expected = [
        0, 1, 2, 3, 4,  # T 0-4
        0, 1, 2, 3, 4,  # T 5-9
        0, 1, 2, 3, 4,  # T 10-14
        0, 1, 2, 3, 4,  # T 15-19
    ]
    assert all(x == y for x, y in zip(actual, expected))


def test_circular_site_selection6():
    # fmt: off
    actual = (site_selection(6, T) for T in it.count())
    expected = [
        0, 1, 2, 3, 4, 5,  # T 0-5
        0, 1, 2, 3, 4, 5,  # T 6-11
        0, 1, 2, 3, 4, 5,  # T 12-17
        0, 1, 2, 3, 4, 5,  # T 18-23
    ]
    assert all(x == y for x, y in zip(actual, expected))


def test_circular_site_selection8():
    # fmt: off
    actual = (site_selection(8, T) for T in it.count())
    expected = [
        0, 1, 2, 3, 4, 5, 6, 7,  # T 0-7
        0, 1, 2, 3, 4, 5, 6, 7,  # T 8-15
        0, 1, 2, 3, 4, 5, 6, 7,  # T 16-23
        0, 1, 2, 3, 4, 5, 6, 7,  # T 24-31
        0, 1, 2, 3, 4, 5, 6, 7, # T 32-39
        0, 1, 2, 3, 4, 5, 6, 7, # T 40-47
    ]
    assert all(x == y for x, y in zip(actual, expected))


def test_circular_site_selection16():
    # fmt: off
    actual = (site_selection(16, T) for T in it.count())
    expected = [
        0, 1, 2, 3, 4, 5, 6, 7,  # T 0-7
        8, 9, 10, 11, 12, 13, 14, 15,  # T 8-15
        0, 1, 2, 3, 4, 5, 6, 7,  # T 16-23
        8, 9, 10, 11, 12, 13, 14, 15,  # T 24-31
    ]
    assert all(x == y for x, y in zip(actual, expected))


def test_circular_site_selection_fuzz():
    testS = it.chain(
        (1 << s for s in range(1, 33)),
        range(1, 65),
    )
    testT = it.chain(range(10**5), (rand(2**128) for _ in range(10**5)))
    for S, T in it.product(testS, testT):
        site_selection(S, T)  # Validated via wrapper


@pytest.mark.parametrize(
    "S",
    [*(1 << s for s in range(1, 21)), 3, 5, 6, 7, 9, 10, 11, 13, 17, 100],
)
def test_circular_site_selection_epoch0(S: int):
    actual = {site_selection(S, T) for T in range(S)}
    expected = set(range(S))
    assert actual == expected


def test_circular_site_selection_exceeds_capacity():
    with pytest.raises(ValueError):
        algo.assign_storage_site(0, 0)
