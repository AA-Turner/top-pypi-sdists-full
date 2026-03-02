import typing


def sticky_lookup_ingest_times_eager(S: int, T: int) -> typing.List[int]:
    """Ingest time lookup algorithm for sticky curation.

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

    return [*range(S)]


# lazy loader workaround
lookup_ingest_times_eager = sticky_lookup_ingest_times_eager
