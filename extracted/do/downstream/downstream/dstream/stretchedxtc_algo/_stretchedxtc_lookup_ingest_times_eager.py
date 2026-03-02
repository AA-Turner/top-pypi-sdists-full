import typing

from ..stretched_algo._stretched_has_ingest_capacity import (
    stretched_has_ingest_capacity,
)
from ..stretched_algo._stretched_lookup_ingest_times_eager import (
    stretched_lookup_ingest_times_eager,
)
from ..xtchead_algo._xtchead_lookup_ingest_times_eager import (
    xtchead_lookup_ingest_times_eager,
)


def stretchedxtc_lookup_ingest_times_eager(S: int, T: int) -> typing.List[int]:
    """Ingest time lookup algorithm for stretchedxtc curation.

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
    if stretched_has_ingest_capacity(S, T):
        return stretched_lookup_ingest_times_eager(S, T)
    else:
        return xtchead_lookup_ingest_times_eager(S, T)


# lazy loader workaround
lookup_ingest_times_eager = stretchedxtc_lookup_ingest_times_eager
