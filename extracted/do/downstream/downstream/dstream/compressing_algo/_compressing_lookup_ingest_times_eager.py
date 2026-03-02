import itertools as it
import typing

from ._compressing_assign_storage_site import compressing_assign_storage_site


def compressing_lookup_ingest_times_eager(S: int, T: int) -> typing.List[int]:
    """Ingest time lookup algorithm for compressing curation.

    Eager implementation.

    Parameters
    ----------
    S : int
        Buffer size. Must be a positive integer.
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

    if S % 2 == 0:  # even S: site 0 special, M = S-1
        si = ((T - 2) // (S - 1)).bit_length()
        si_ = 1 << si
        assert si_

        candidates = it.chain(
            (0,),
            range(1, T, si_),
            reversed(
                range(
                    1 + (si_ >> 1),
                    (S - 1) * (si_ >> 1),
                    si_,
                )
            ),
        )
    else:  # odd S: no special site, M = S
        si = ((T - 1) // S).bit_length()
        si_ = 1 << si
        assert si_

        candidates = it.chain(
            range(0, T, si_),
            reversed(range(si_ >> 1, S * (si_ >> 1), si_)),
        )

    res = [None] * S
    for Tbar in it.islice(candidates, S):
        assert Tbar < T
        k = compressing_assign_storage_site(S, Tbar)
        assert k is not None
        res[k] = Tbar

    return res


# lazy loader workaround
lookup_ingest_times_eager = compressing_lookup_ingest_times_eager
