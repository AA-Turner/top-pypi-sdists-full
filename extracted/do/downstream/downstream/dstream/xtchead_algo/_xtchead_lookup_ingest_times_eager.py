import typing

from ..compressing_algo._compressing_lookup_ingest_times_eager import (
    compressing_lookup_ingest_times_eager,
)


def xtchead_lookup_ingest_times_eager(S: int, T: int) -> typing.List[int]:
    """Ingest time lookup algorithm for xtchead curation.

    Eager implementaiton.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two.
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
        (1 << x) - 1
        for x in compressing_lookup_ingest_times_eager(S, max(S, epoch))
    ]

    for k in range(epoch, S):
        # see https://oeis.org/A057716
        x = k - S.bit_length() + 1
        res[k] = x + (x + x.bit_length()).bit_length() - 1

    return res


# lazy loader workaround
lookup_ingest_times_eager = xtchead_lookup_ingest_times_eager
