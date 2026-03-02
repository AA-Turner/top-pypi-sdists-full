import functools
import itertools as it
import typing

import numpy as np
import pytest

from downstream.dstream import tilted_algo as algo

_dtypes = [
    np.uint8,
    np.uint16,
    np.uint32,
    np.uint64,
    np.int8,
    np.int16,
    np.int32,
    np.int64,
]


def validate_tilted_site_selection(fn: typing.Callable) -> typing.Callable:
    """Decorator to validate pre- and post-conditions on site selection."""

    @functools.wraps(fn)
    def wrapper(S: int, T: int) -> typing.Optional[int]:
        assert np.array(np.bitwise_count(S) == 1).all()  # S is a power of two
        assert np.asarray(0 <= T).all()  # T is non-negative
        res = fn(S, T)
        assert (np.clip(res, 0, S) == res).all()  # Assert valid output
        return res

    return wrapper


site_selection = validate_tilted_site_selection(
    algo.assign_storage_site_batched,
)


def test_tilted_site_selection_batched8_scalar():
    # fmt: off
    actual = (site_selection(8, T) for T in it.count())
    expected = [
        0, 1, 5, 2, 4, 6, 7, 3,  # T 0-7
        0, 1, 5, 7, 0, 6, 5, 4,  # T 8-15
        0, 1, 0, 2, 0, 6, 0, 3,  # T 16-23
        0, 1, 0, 7, 0, 6, 0, 5,  # T 24-31
        0, 1, 0, 2, 0, 1, 0, 3 # T 32-39
    ]
    assert all(x.tolist() == [y] for x, y in zip(actual, expected))


def test_tilted_site_selection_batched16_scalar():
    # fmt: off
    actual = (site_selection(16, T) for T in it.count())
    expected = [
        0, 1, 9, 2, 6, 10, 13, 3,  # T 0-7 --- hv 0,1,0,2,0,1,0,3
        5, 7, 8, 11, 12, 14, 15, 4,  # T 8-15 --- hv 0,1,0,2,0,1,0,4
        0, 1, 9, 8, 6, 10, 13, 12,  # T 16-24 --- hv 0,1,0, ...
        0, 7, 9, 15, 6, 14, 13, 5,  # T 24-31
        0, 1, 9, 2, 0, 10, 9, 3 # T 32-39
    ]
    assert all(x.tolist() == [y] for x, y in zip(actual, expected))


def test_tilted_site_selection_batched8():
    # fmt: off
    T = np.arange(40)

    actual = site_selection(8, T)
    expected = [
        0, 1, 5, 2, 4, 6, 7, 3,  # T 0-7
        0, 1, 5, 7, 0, 6, 5, 4,  # T 8-15
        0, 1, 0, 2, 0, 6, 0, 3,  # T 16-23
        0, 1, 0, 7, 0, 6, 0, 5,  # T 24-31
        0, 1, 0, 2, 0, 1, 0, 3 # T 32-39
    ]
    assert all(x == y for x, y in zip(actual, expected))


def test_tilted_site_selection_batched16():
    # fmt: off
    T = np.arange(40)

    actual = site_selection(16, T)
    expected = [
        0, 1, 9, 2, 6, 10, 13, 3,  # T 0-7 --- hv 0,1,0,2,0,1,0,3
        5, 7, 8, 11, 12, 14, 15, 4,  # T 8-15 --- hv 0,1,0,2,0,1,0,4
        0, 1, 9, 8, 6, 10, 13, 12,  # T 16-24 --- hv 0,1,0, ...
        0, 7, 9, 15, 6, 14, 13, 5,  # T 24-31
        0, 1, 9, 2, 0, 10, 9, 3 # T 32-39
    ]
    assert all(x == y for x, y in zip(actual, expected))


def test_tilted_site_selection_batched_dualS():
    # fmt: off
    T = np.array([*range(40), *range(40)])
    S = np.array([8] * 40 + [16] * 40)

    actual = site_selection(S, T)
    expected = [
        0, 1, 5, 2, 4, 6, 7, 3,  # T 0-7
        0, 1, 5, 7, 0, 6, 5, 4,  # T 8-15
        0, 1, 0, 2, 0, 6, 0, 3,  # T 16-23
        0, 1, 0, 7, 0, 6, 0, 5,  # T 24-31
        0, 1, 0, 2, 0, 1, 0, 3 # T 32-39
    ] + [
        0, 1, 9, 2, 6, 10, 13, 3,  # T 0-7 --- hv 0,1,0,2,0,1,0,3
        5, 7, 8, 11, 12, 14, 15, 4,  # T 8-15 --- hv 0,1,0,2,0,1,0,4
        0, 1, 9, 8, 6, 10, 13, 12,  # T 16-24 --- hv 0,1,0, ...
        0, 7, 9, 15, 6, 14, 13, 5,  # T 24-31
        0, 1, 9, 2, 0, 10, 9, 3 # T 32-39
    ]
    assert all(x == y for x, y in zip(actual, expected))


@pytest.mark.parametrize("dtype1", _dtypes)
@pytest.mark.parametrize("dtype2", _dtypes)
def test_tilted_site_selection_batched_fuzz(
    dtype1: typing.Type,
    dtype2: typing.Type,
):
    Smax = min(np.iinfo(dtype1).max, 2**52)
    Tmax = min(np.iinfo(dtype2).max, 2**52)
    if Tmax < Smax:
        return
    testS = np.array(
        [2**s for s in range(1, 64) if 2**s <= Smax],
        dtype=dtype1,
    )
    testT = np.array(
        [
            *range(min(10**5, Tmax + 1)),
            *np.random.randint(Tmax, size=10**4),
            Tmax,
        ],
        dtype=dtype2,
    )

    batchS, batchT = map(np.array, zip(*it.product(testS, testT)))
    assert (np.bitwise_count(batchS) == 1).all()
    mask = ~algo.has_ingest_capacity_batched(batchS, batchT)
    batchT[mask] = batchS[mask]

    site_selection(batchS, batchT)


@pytest.mark.parametrize("S", [1 << s for s in range(1, 21)])
def test_tilted_site_selection_epoch0(S: int):
    actual = set(site_selection(S, np.arange(S)))
    expected = set(range(S))
    assert actual == expected
