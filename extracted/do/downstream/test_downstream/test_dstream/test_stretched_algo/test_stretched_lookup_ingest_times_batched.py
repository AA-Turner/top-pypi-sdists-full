import functools
import typing

import numpy as np
import pytest

from downstream.dstream import stretched_algo as algo
from downstream.dstream.stretched_algo._stretched_lookup_ingest_times_batched import (
    _stretched_lookup_ingest_times_batched_jit,
)

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


def validate_stretched_time_lookup(fn: typing.Callable) -> typing.Callable:
    """Decorator to validate pre- and post-conditions on site lookup."""

    @functools.wraps(fn)
    def wrapper(S: int, T: np.ndarray, *args, **kwargs) -> np.ndarray:
        assert np.array(np.bitwise_count(S) == 1).all()  # S is a power of two
        assert np.asarray(S <= T).all()  # T is non-negative
        res = fn(S, T, *args, **kwargs)
        assert (np.clip(res, 0, T[:, None] - 1) == res).all()
        return res

    return wrapper


@pytest.mark.parametrize("s", range(1, 12))
def test_stretched_time_lookup_batched_against_site_selection(s: int):
    S = 1 << s
    T_max = min(1 << 20 - s, 2**S - 1)
    expected = [None] * S

    expecteds = []
    for T in range(T_max):
        if T >= S:
            expecteds.extend(expected)

        site = algo.assign_storage_site(S, T)
        if site is not None:
            expected[site] = T

    actual = algo.lookup_ingest_times_batched(S, np.arange(S, T_max)).ravel()
    np.testing.assert_array_equal(expecteds, actual)


@pytest.mark.parametrize("s", range(1, 12))
def test_stretched_time_lookup_batched_empty(s: int):
    S = 1 << s

    res = algo.lookup_ingest_times_batched(S, np.array([], dtype=int))
    assert res.size == 0


@pytest.mark.parametrize("dtype1", _dtypes)
@pytest.mark.parametrize("dtype2", _dtypes)
@pytest.mark.parametrize("parallel", [True, False])
def test_stretched_time_lookup_batched_fuzz(
    dtype1: typing.Type,
    dtype2: typing.Type,
    parallel: bool,
):
    Smax = min(np.iinfo(dtype1).max, [2**12, 2**8][bool(parallel)])
    Tmax = min(np.iinfo(dtype2).max, 2**52)
    testS = np.array(
        [2**s for s in range(1, 64) if 2**s <= min(Smax, Tmax)],
        dtype=dtype1,
    )

    testT1 = np.array(
        [
            *range(min(10**3, Tmax + 1)),
            *np.random.randint(Tmax, size=10**3),
            Tmax,
        ],
        dtype=dtype2,
    )

    testT2 = np.array(
        [
            *range(min(10**3, Tmax + 1)),
            *np.random.randint(min(Tmax, 2**32 - 1), size=10**3),
            min(Tmax, 2**32 - 1),
        ],
        dtype=dtype2,
    )

    validate = validate_stretched_time_lookup(algo.lookup_ingest_times_batched)
    for S in testS:
        assert np.issubdtype(np.asarray(S).dtype, np.integer), S
        mask1 = np.logical_or(
            ~algo.has_ingest_capacity_batched(S, testT1),
            testT1 < S,
        )
        batchT1 = np.where(mask1, int(S), testT1)
        validate(S, batchT1, parallel=parallel)

        mask2 = np.logical_or(
            ~algo.has_ingest_capacity_batched(S, testT2),
            testT2 < S,
        )
        batchT2 = np.where(mask2, int(S), testT2)
        validate(S, batchT2, parallel=parallel)


def test_stretched_time_lookup_batched_fuzz_parallel():
    dtype1 = np.int64
    dtype2 = np.int64
    Smax = min(np.iinfo(dtype1).max, 2**17)
    Tmax = min(np.iinfo(dtype2).max, 2**52)
    testS = np.array(
        [2**s for s in range(1, 64) if 2**s <= min(Smax, Tmax)],
        dtype=dtype1,
    )

    testT2 = np.array(
        [
            *range(min(10**3, Tmax + 1)),
            *np.random.randint(min(Tmax, 2**32 - 1), size=10**3),
            min(Tmax, 2**32 - 1),
        ],
        dtype=dtype2,
    )

    validate = validate_stretched_time_lookup(
        _stretched_lookup_ingest_times_batched_jit,
    )
    for S in testS:
        mask2 = np.logical_or(
            ~algo.has_ingest_capacity_batched(S, testT2),
            testT2 < S,
        )
        batchT2 = np.where(mask2, int(S), testT2)
        validate(S, batchT2, chunk_size=32768)
