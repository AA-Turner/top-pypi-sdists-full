import functools
import typing

import numpy as np
import pytest

from downstream import dstream
from downstream.dstream import primed_algo as algo_class


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
    time_lookup = validate_lookup(algo.lookup_ingest_times)
    S = (1 << s) + lpad + rpad
    T_max = algo.get_ingest_capacity(S)
    if T_max is None:
        T_max = 2**10
    T_max = min(T_max, 2**17)

    expected = [None] * S
    for T in range(min(T_max, 2**14)):
        actual = time_lookup(S, T)
        assert [*actual] == expected

        site = algo.assign_storage_site(S, T)
        if site is not None:
            expected[site] = T


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
@pytest.mark.parametrize(
    "T", [*range(10**2), *np.random.randint(2**63, size=10**2)]
)
def test_lookup_fuzz(
    base_algo: typing.Any, lpad: int, rpad: int, s: int, T: int
):
    algo = algo_class(algo=base_algo, lpad=lpad, rpad=rpad)
    S = (1 << s) + lpad + rpad
    time_lookup = validate_lookup(algo.lookup_ingest_times)
    if not algo.has_ingest_capacity(S, T):
        T = S
    [*time_lookup(S, T)]
