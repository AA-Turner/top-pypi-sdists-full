import itertools as it
import typing


def circular_lookup_ingest_times_eager(S: int, T: int) -> typing.List[int]:
    """Ingest time lookup algorithm for circular curation.

    Eager implementation.

    Parameters
    ----------
    S : int
        Buffer size. Must be positive.
    T : int
        Current logical time.

    Returns
    -------
    typing.List[int]
        Ingest time of stored item at buffer sites in index order.
    """
    if T < S:
        raise ValueError("T < S not supported for eager lookup")

    assert T
    T -= 1

    res = [None] * S
    res[0] = T - T % S
    for k_, k in it.pairwise(range(S)):
        res[k] = res[k_] + 1
        res[k] -= S * (res[k] == T + 1)
        assert res[k] >= 0

    return res


# lazy loader workaround
lookup_ingest_times_eager = circular_lookup_ingest_times_eager
