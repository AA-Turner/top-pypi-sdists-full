import functools
import itertools as it
import typing

import numpy as np
import pytest

from downstream import dstream
from downstream.dstream import hybrid_algo as algo_class


def validate_lookup(fn: typing.Callable) -> typing.Callable:
    """Decorator to validate pre- and post-conditions on site lookup."""

    @functools.wraps(fn)
    def wrapper(S: int, T: np.ndarray, *args, **kwargs) -> np.ndarray:
        assert np.asarray(S <= T).all()  # T is non-negative
        res = fn(S, T, *args, **kwargs)
        assert (np.clip(res, 0, T[:, None] - 1) == res).all()
        return res

    return wrapper


@pytest.mark.parametrize(
    "algo",
    [
        algo_class(0, dstream.steady_algo, 1),
        algo_class(0, dstream.steady_algo, 1, dstream.stretched_algo, 2),
        algo_class(0, dstream.tilted_algo, 1, dstream.tilted_algo, 2),
        algo_class(
            0,
            dstream.tilted_algo,
            1,
            dstream.tilted_algo,
            2,
            dstream.steady_algo,
            3,
        ),
        algo_class(
            0,
            dstream.steady_algo,
            2,
            dstream.stretched_algo,
            3,
            dstream.steady_algo,
            4,
        ),
        algo_class(
            0,
            dstream.steady_algo,
            1,
            dstream.stretched_algo,
            3,
            dstream.tilted_algo,
            4,
        ),
    ],
)
@pytest.mark.parametrize("s", range(1, 7))
def test_lookup_against_site_selection(algo: typing.Any, s: int):
    time_lookup = validate_lookup(algo.lookup_ingest_times_batched)
    S = (1 << s) * algo._get_num_chunks()
    T_max = min(1 << (20 - s), algo.get_ingest_capacity(S) or 2**S - 1)
    expected = [None] * S

    expecteds = []
    for T in range(T_max):
        if T >= S:
            expecteds.extend(expected)

        site = algo.assign_storage_site(S, T)
        if site is not None:
            expected[site] = T

    for dtype1, dtype2 in it.product([int, np.int32, np.uint32], repeat=2):
        T_max_ = min(T_max, 1024)
        actual = time_lookup(
            dtype1(S), np.arange(S, T_max_, dtype=dtype2)
        ).ravel()
        np.testing.assert_array_equal(expecteds[: len(actual)], actual)

    for dtype in np.int32, np.uint32:
        actual = time_lookup(S, np.arange(S, T_max, dtype=dtype)).ravel()
        np.testing.assert_array_equal(expecteds, actual)


# RE https://github.com/mmore500/downstream/pull/91
def test_bounds_regression91():
    algo = algo_class(0, dstream.steady_algo, 1, dstream.tilted_algo, 2)
    S = 128
    T = np.array([191998, 191230, 191722], dtype=np.uint32)
    T_ = np.array([191998, 191230, 191722], dtype=np.int64)
    assert algo_class

    for i in 0, 1:
        np.testing.assert_array_equal(
            algo._get_adj_T(T, i), algo._get_adj_T(T_, i), f"{i=}"
        )

    res = algo.lookup_ingest_times_batched(S, T)
    res_ = algo.lookup_ingest_times_batched(S, T_)
    np.testing.assert_array_equal(res, res_)

    assert (res < T[:, None]).ravel().all()
