import typing


def sticky_lookup_ingest_times(
    S: int, T: int
) -> typing.Iterable[typing.Optional[int]]:
    """Ingest time lookup algorithm for sticky curation.

    Lazy implementation.

    Parameters
    ----------
    S : int
        Buffer size. Must be positive.
    T : int
        Current logical time.

    Yields
    ------
    typing.Optional[int]
        Ingest time of stored item at buffer sites in index order.
    """
    assert T >= 0
    if T < S:  # Patch for before buffer is filled...
        return (v if v < T else None for v in sticky_lookup_impl(S, S))
    else:  # ... assume buffer has been filled
        return sticky_lookup_impl(S, T)


def sticky_lookup_impl(S: int, T: int) -> typing.Iterable[int]:
    """Implementation detail for `sticky_lookup_ingest_times`."""
    S, T = int(S), int(T)  # play nice with numpy types
    assert T >= S  # T < S redirected to T = S by sticky_lookup_ingest_times

    yield from range(S)


lookup_ingest_times = sticky_lookup_ingest_times  # lazy loader workaround
