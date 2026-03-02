import functools
import typing

import pytest

from downstream.dstream import compressing_algo as algo


def validate_compressing_time_lookup(fn: typing.Callable) -> typing.Callable:
    """Decorator to validate pre- and post-conditions on time lookup."""

    @functools.wraps(fn)
    def wrapper(S: int, T: int) -> typing.Iterable[int]:
        assert S > 0  # Assert S is positive
        assert 0 <= T  # Assert T is non-negative
        res = fn(S, T)
        assert len(res) == S  # Assert output length matches buffer size
        for v in res:
            assert v is None or 0 <= v < T  # Assert valid output
        return res

    return wrapper


time_lookup = validate_compressing_time_lookup(
    algo.lookup_ingest_times_eager,
)


@pytest.mark.parametrize("s", range(1, 12))
def test_compressing_time_lookup_eager_against_site_selection(s: int):
    S = 1 << s
    T_max = 1 << 17 - s
    expected = [None] * S
    for T in range(T_max):
        if T >= S:
            actual = time_lookup(S, T)
            assert expected == actual
        else:
            with pytest.raises(ValueError):
                time_lookup(S, T)

        site = algo.assign_storage_site(S, T)
        if site is not None:
            expected[site] = T


@pytest.mark.parametrize("S", [3, 5, 6, 7, 9, 10, 11, 13, 17, 100])
def test_compressing_time_lookup_eager_nonpow2(S: int):
    T_max = S * 100
    expected = [None] * S
    for T in range(T_max):
        if T >= S:
            actual = algo.lookup_ingest_times_eager(S, T)
            assert len(actual) == S
            for v in actual:
                assert v is None or 0 <= v < T
            assert expected == actual

        site = algo.assign_storage_site(S, T)
        if site is not None:
            expected[site] = T
