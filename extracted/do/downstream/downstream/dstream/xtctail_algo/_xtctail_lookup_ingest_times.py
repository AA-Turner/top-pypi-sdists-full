import itertools as it
import typing

from ..._auxlib._ctz import ctz
from ..._auxlib._indexable_range import indexable_range
from ..._auxlib._modpow2 import modpow2
from ..compressing_algo._compressing_lookup_ingest_times import (
    compressing_lookup_impl,
)


def xtctail_lookup_ingest_times(
    S: int, T: int
) -> typing.Iterable[typing.Optional[int]]:
    """Ingest time lookup algorithm for xtctail curation.

    Lazy implementation.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two.
    T : int
        Current logical time.

    Yields
    ------
    typing.Optional[int]
        Ingest time of stored item at buffer sites in index order.
    """
    assert T >= 0
    if T < S:  # Patch for before buffer is filled...
        return (v if v < T else None for v in xtctail_lookup_impl(S, S))
    else:  # ... assume buffer has been filled
        return xtctail_lookup_impl(S, T)


def xtctail_lookup_impl(S: int, T: int) -> typing.Iterable[int]:
    """Implementation detail for `xtctail_lookup_ingest_times`."""
    S, T = int(S), int(T)  # play nice with numpy types
    assert S > 1 and S.bit_count() == 1
    assert T >= S  # T < S handled by T = S via xtctail_lookup_ingest_times

    epoch = T.bit_length()
    for h in it.islice(
        compressing_lookup_impl(S, max(epoch, S)),
        epoch,
    ):
        T_ = T - 1
        h_offset = (1 << h) - 1
        h_cadence = 2 << h
        assert T_ >= h_offset
        h_remainder = modpow2(T_ - h_offset, h_cadence)
        res = T_ - h_remainder
        assert ctz(res + 1) == h
        assert res <= T_
        yield res

    for k in range(epoch, S):
        x = k - S.bit_length() + 1
        # see https://oeis.org/A057716
        ansatz = x + (x + x.bit_length()).bit_length() - 1
        assert ansatz < T
        ansatz_h = ctz(ansatz + 1)  # Current hanoi value
        ansatz_h_offset = (1 << ansatz_h) - 1
        ansatz_h_cadence = 2 << ansatz_h

        res = (
            2 * ansatz_h_offset
            + ((S - ansatz_h_offset - 1) >> (ansatz_h + 1)) * ansatz_h_cadence
            - ansatz
        )
        assert (
            res
            == reversed(indexable_range(ansatz_h_offset, S, ansatz_h_cadence))[
                indexable_range(ansatz_h_offset, S, ansatz_h_cadence).index(
                    ansatz,
                )
            ]
        )
        yield res


lookup_ingest_times = xtctail_lookup_ingest_times  # lazy loader workaround
