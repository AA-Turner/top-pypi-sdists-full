import typing


def circular_lookup_ingest_times(
    S: int, T: int
) -> typing.Iterable[typing.Optional[int]]:
    """Ingest time lookup algorithm for circular curation.

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
        return (v if v < T else None for v in circular_lookup_impl(S, S))
    else:  # ... assume buffer has been filled
        return circular_lookup_impl(S, T)


def circular_lookup_impl(S: int, T: int) -> typing.Iterable[int]:
    """Implementation detail for `circular_lookup_ingest_times`."""
    S, T = int(S), int(T)  # play nice with numpy types
    assert S > 0
    assert T >= S  # T < S redirected to T = S by circular_lookup_ingest_times

    assert T
    T -= 1

    for k in range(S):  # Iterate over buffer sites
        yield T - (T - k) % S


lookup_ingest_times = circular_lookup_ingest_times  # lazy loader workaround
