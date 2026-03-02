import typing

from ..stretched_algo._stretched_has_ingest_capacity import (
    stretched_has_ingest_capacity,
)
from ..stretched_algo._stretched_lookup_ingest_times import (
    stretched_lookup_ingest_times,
)
from ..xtchead_algo._xtchead_lookup_ingest_times import (
    xtchead_lookup_ingest_times,
)


def stretchedxtc_lookup_ingest_times(
    S: int, T: int
) -> typing.Iterable[typing.Optional[int]]:
    """Ingest time lookup algorithm for stretchedxtc curation.

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
    if stretched_has_ingest_capacity(S, T):
        return stretched_lookup_ingest_times(S, T)
    else:
        return xtchead_lookup_ingest_times(S, T)


# lazy loader workaround
lookup_ingest_times = stretchedxtc_lookup_ingest_times
