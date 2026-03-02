import typing

from ._steady_lookup_ingest_times import steady_lookup_impl


def steady_lookup_ingest_times_eager(S: int, T: int) -> typing.List[int]:
    """Ingest time lookup algorithm for steady curation.

    Eager implementation.

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
    """
    if T < S:
        raise ValueError("T < S not supported for eager lookup")
    return list(steady_lookup_impl(S, T))


# lazy loader workaround
lookup_ingest_times_eager = steady_lookup_ingest_times_eager
