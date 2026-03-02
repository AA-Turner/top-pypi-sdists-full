import typing

import pytest

from downstream import dstream
from downstream.dstream import primed_algo as algo_class


@pytest.mark.parametrize(
    "base_algo",
    [
        dstream.circular_algo,
        dstream.compressing_algo,
        dstream.sticky_algo,
        dstream.hybrid_0_steady_1_tilted_2_algo,
        dstream.hybrid_0_steady_1_tiltedxtc_2_algo,
        dstream.stretched_algo,
        dstream.stretchedxtc_algo,
        dstream.tilted_algo,
        dstream.tiltedxtc_algo,
    ],
)
@pytest.mark.parametrize("lpad", [0, 4, 8])
@pytest.mark.parametrize("rpad", [0, 4, 8])
@pytest.mark.parametrize("s", range(3, 5))
def test_lookup_against_site_selection(
    base_algo: typing.Any, lpad: int, rpad: int, s: int
):
    algo = algo_class(algo=base_algo, lpad=lpad, rpad=rpad)
    time_lookup = algo.lookup_ingest_times_eager
    S = (1 << s) + lpad + rpad
    T_max = algo.get_ingest_capacity(S)
    if T_max is None:
        T_max = 2**10
    T_max = min(T_max, 2**17)

    expected = [None] * S
    for T in range(T_max):
        if T >= S:
            actual = time_lookup(S, T)
            assert all(x == y for x, y in zip(expected, actual))

        site = algo.assign_storage_site(S, T)
        if site is not None:
            expected[site] = T
