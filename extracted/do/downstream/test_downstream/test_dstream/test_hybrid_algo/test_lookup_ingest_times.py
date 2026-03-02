import functools
import typing

import numpy as np
import pytest

from downstream import dstream
from downstream.dstream import hybrid_algo as algo_class


def validate_lookup(fn: typing.Callable) -> typing.Callable:
    """Decorator to validate pre- and post-conditions on time lookup."""

    @functools.wraps(fn)
    def wrapper(S: int, T: int) -> typing.Iterable[typing.Optional[int]]:
        assert 0 <= T  # Assert T is non-negative
        res = fn(S, T)
        for v in res:
            assert v is None or 0 <= v < T  # Assert valid output
            yield v

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
    time_lookup = validate_lookup(algo.lookup_ingest_times)
    S = (1 << s) * algo._get_num_chunks()
    T_max = algo.get_ingest_capacity(S)
    if T_max is None:
        T_max = 2**14

    expected = [None] * S
    for T in range(min(T_max, 2**14)):
        actual = time_lookup(S, T)
        assert [*actual] == expected

        site = algo.assign_storage_site(S, T)
        if site is not None:
            expected[site] = T


@pytest.mark.parametrize(
    "algo",
    [
        algo_class(0, dstream.steady_algo, 1),
        algo_class(0, dstream.steady_algo, 1, dstream.stretched_algo, 2),
        algo_class(0, dstream.tilted_algo, 1, dstream.tilted_algo, 2),
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
@pytest.mark.parametrize("s", range(1, 8))
@pytest.mark.parametrize(
    "T", [*range(10**2), *np.random.randint(2**63, size=10**2)]
)
def test_lookup_fuzz(algo: typing.Any, s: int, T: int):
    S = (1 << s) * algo._get_num_chunks()
    time_lookup = validate_lookup(algo.lookup_ingest_times)
    if not algo.has_ingest_capacity(S, T):
        T = S
    [*time_lookup(S, T)]


# RE https://github.com/mmore500/downstream/pull/91
@pytest.mark.parametrize(
    "algo",
    [algo_class(0, dstream.steady_algo, 1, dstream.tilted_algo, 2)],
)
@pytest.mark.parametrize(
    "T",
    [191998, 191230, 191722],
)
def test_bounds_regression91(algo: typing.Any, T: int):
    S = 128
    res = algo.lookup_ingest_times(S, T)
    assert all(Tbar < T for Tbar in res)
