import typing

from ._tilted_lookup_ingest_times import tilted_lookup_impl


def tilted_lookup_ingest_times_eager(S: int, T: int) -> typing.List[int]:
    """Ingest time lookup algorithm for tilted curation.

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
    return list(tilted_lookup_impl(S, T))


# lazy loader workaround
lookup_ingest_times_eager = tilted_lookup_ingest_times_eager
