import functools
import typing

import pytest

from downstream.dstream import tilted_algo as algo


def validate_tilted_time_lookup(fn: typing.Callable) -> typing.Callable:
    """Decorator to validate pre- and post-conditions on time lookup."""

    @functools.wraps(fn)
    def wrapper(S: int, T: int) -> typing.List[int]:
        assert S.bit_count() == 1  # Assert S is a power of two
        assert 0 <= T  # Assert T is non-negative
        res = fn(S, T)
        for v in res:
            assert v is None or 0 <= v < T  # Assert valid output
        return res

    return wrapper


time_lookup = validate_tilted_time_lookup(algo.lookup_ingest_times_eager)


@pytest.mark.parametrize("s", range(1, 12))
def test_tilted_time_lookup_eager_against_site_selection(s: int):
    S = 1 << s
    T_max = min(1 << 17 - s, 2**S - 1)
    expected = [None] * S
    for T in range(T_max):
        if T >= S:
            actual = time_lookup(S, T)
            assert all(x == y for x, y in zip(expected, actual))
        else:
            with pytest.raises(ValueError):
                time_lookup(S, T)

        site = algo.assign_storage_site(S, T)
        if site is not None:
            expected[site] = T
