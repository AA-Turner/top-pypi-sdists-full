import functools
import typing

import numpy as np
import pytest

from downstream.dstream import tilted_algo as algo


def validate_tilted_time_lookup(fn: typing.Callable) -> typing.Callable:
    """Decorator to validate pre- and post-conditions on time lookup."""

    @functools.wraps(fn)
    def wrapper(S: int, T: int) -> typing.Iterable[typing.Optional[int]]:
        assert S.bit_count() == 1  # Assert S is a power of two
        assert 0 <= T  # Assert T is non-negative
        res = fn(S, T)
        for v in res:
            assert v is None or 0 <= v < T  # Assert valid output
            yield v

    return wrapper


time_lookup = validate_tilted_time_lookup(algo.lookup_ingest_times)


@pytest.mark.parametrize("s", range(1, 12))
def test_tilted_time_lookup_against_site_selection(s: int):
    S = 1 << s
    T_max = min(1 << 17 - s, 2**S - 1)
    expected = [None] * S
    for T in range(T_max):
        actual = time_lookup(S, T)
        assert all(x == y for x, y in zip(expected, actual))

        site = algo.assign_storage_site(S, T)
        if site is not None:
            expected[site] = T


@pytest.mark.parametrize("S", [2**s for s in range(1, 13)])
@pytest.mark.parametrize(
    "T", [*range(10**2), *np.random.randint(2**63, size=10**2)]
)
def test_tilted_time_lookup_fuzz(S: int, T: int):
    if not algo.has_ingest_capacity(S, T):
        T = S
    [*time_lookup(S, T)]
