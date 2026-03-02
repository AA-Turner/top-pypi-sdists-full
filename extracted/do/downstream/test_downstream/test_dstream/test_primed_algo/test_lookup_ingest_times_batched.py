import functools
import typing

import numpy as np
import pytest

from downstream import dstream
from downstream.dstream import primed_algo as algo_class


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
    "base_algo",
    [
        dstream.circular_algo,
        dstream.compressing_algo,
        dstream.sticky_algo,
        dstream.hybrid_0_steady_1_stretched_2_algo,
        dstream.hybrid_0_steady_1_stretchedxtc_2_algo,
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
@pytest.mark.parametrize("s", range(3, 7))
def test_lookup_against_site_selection(
    base_algo: typing.Any, lpad: int, rpad: int, s: int
):
    algo = algo_class(algo=base_algo, lpad=lpad, rpad=rpad)
    time_lookup = validate_lookup(algo.lookup_ingest_times_batched)
    S = (1 << s) + lpad + rpad
    T_max = min(
        1 << (17 - s), algo.get_ingest_capacity(S) or (1 << (s + 1)) - 1
    )
    expected = [None] * S

    expecteds = []
    for T in range(T_max):
        if T >= S:
            expecteds.extend(expected)

        site = algo.assign_storage_site(S, T)
        if site is not None:
            expected[site] = T

    actual = time_lookup(S, np.arange(S, T_max)).ravel()
    np.testing.assert_array_equal(expecteds, actual)
