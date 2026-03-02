import typing

from ..._auxlib._ctz import ctz
from ..._auxlib._modpow2 import modpow2
from ..compressing_algo._compressing_lookup_ingest_times_eager import (
    compressing_lookup_ingest_times_eager,
)


def xtctail_lookup_ingest_times_eager(S: int, T: int) -> typing.List[int]:
    """Ingest time lookup algorithm for xtctail curation.

    Eager implementation.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two greater than 4.
    T : int
        Current logical time.

    Returns
    -------
    typing.List[int]
        Ingest time of stored item at buffer sites in index order.

    References
    ----------
    John C. Gunther. 2014. Algorithm 938: Compressing circular buffers. ACM
    Trans. Math. Softw. 40, 2, Article 17 (February 2014), 12 pages.
    https://doi.org/10.1145/2559995
    """
    if T < S:
        raise ValueError("T < S not supported for eager lookup")

    epoch = T.bit_length()
    res = [
        T - modpow2(T - (1 << h), 2 << h) - 1
        for h in compressing_lookup_ingest_times_eager(S, max(S, epoch))
    ]

    for k in range(epoch, S):
        x = k - S.bit_length() + 1
        # see https://oeis.org/A057716
        ansatz = x + (x + x.bit_length()).bit_length() - 1
        assert ansatz < T
        ansatz_h = ctz(ansatz + 1)  # Current hanoi value
        ansatz_h_offset = (1 << ansatz_h) - 1
        ansatz_h_cadence = 2 << ansatz_h
        res[k] = (
            2 * ansatz_h_offset
            + ((S - ansatz_h_offset - 1) >> (ansatz_h + 1)) * ansatz_h_cadence
            - ansatz
        )

    return res


# lazy loader workaround
lookup_ingest_times_eager = xtctail_lookup_ingest_times_eager
