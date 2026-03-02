import typing

import pytest

from downstream import dstream
from downstream.dstream import hybrid_algo as algo_class


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
@pytest.mark.parametrize("s", range(1, 5))
def test_lookup_against_site_selection(algo: typing.Any, s: int):
    time_lookup = algo.lookup_ingest_times_eager
    S = (1 << s) * algo._get_num_chunks()
    T_max = algo.get_ingest_capacity(S)
    if T_max is None:
        T_max = 2**10

    expected = [None] * S
    for T in range(T_max):
        if T >= S:
            actual = time_lookup(S, T)
            assert all(x == y for x, y in zip(expected, actual))

        site = algo.assign_storage_site(S, T)
        if site is not None:
            expected[site] = T


# RE https://github.com/mmore500/downstream/pull/91
@pytest.mark.parametrize(
    "algo",
    [algo_class(0, dstream.steady_algo, 1, dstream.tilted_algo, 2)],
)
@pytest.mark.parametrize("T", [191998, 191230, 191722])
def test_bounds_regression91(algo: typing.Any, T: int):
    S = 128
    res = algo.lookup_ingest_times_eager(S, T)
    assert all(Tbar < T for Tbar in res)
