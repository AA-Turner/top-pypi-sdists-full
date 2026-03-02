import functools
import typing

import numpy as np
import pytest

from downstream.dstream import compressing_algo as algo


def validate_compressing_time_lookup(fn: typing.Callable) -> typing.Callable:
    """Decorator to validate pre- and post-conditions on time lookup."""

    @functools.wraps(fn)
    def wrapper(S: int, T: int) -> typing.Iterable[typing.Optional[int]]:
        assert S > 0  # Assert S is positive
        assert 0 <= T  # Assert T is non-negative
        res = fn(S, T)
        for v in res:
            assert v is None or 0 <= v < T  # Assert valid output
            yield v

    return wrapper


time_lookup = validate_compressing_time_lookup(algo.lookup_ingest_times)


@pytest.mark.parametrize("s", range(1, 12))
def test_compressing_time_lookup_against_site_selection(s: int):
    S = 1 << s
    T_max = 1 << 17 - s
    expected = [None] * S
    for T in range(T_max):
        actual = time_lookup(S, T)
        assert [*actual] == expected

        site = algo.assign_storage_site(S, T)
        if site is not None:
            expected[site] = T


@pytest.mark.parametrize("S", [3, 5, 6, 7, 9, 10, 11, 13, 17, 100])
def test_compressing_time_lookup_nonpow2(S: int):
    T_max = S * 100
    expected = [None] * S
    for T in range(T_max):
        actual = [*algo.lookup_ingest_times(S, T)]
        for v in actual:
            assert v is None or 0 <= v < T
        assert actual == expected

        site = algo.assign_storage_site(S, T)
        if site is not None:
            expected[site] = T


@pytest.mark.parametrize(
    "S",
    [*(2**s for s in range(1, 13)), 3, 5, 6, 7, 9, 10, 11, 13, 17],
)
@pytest.mark.parametrize(
    "T", [*range(10**2), *np.random.randint(2**63, size=10**2)]
)
def test_compressing_time_lookup_fuzz(S: int, T: int):
    if not algo.has_ingest_capacity(S, T):
        T = S
    [*time_lookup(S, T)]
