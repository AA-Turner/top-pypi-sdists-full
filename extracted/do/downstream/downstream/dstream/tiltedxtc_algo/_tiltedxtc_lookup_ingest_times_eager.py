import typing

from ..tilted_algo._tilted_has_ingest_capacity import (
    tilted_has_ingest_capacity,
)
from ..tilted_algo._tilted_lookup_ingest_times_eager import (
    tilted_lookup_ingest_times_eager,
)
from ..xtctail_algo._xtctail_lookup_ingest_times_eager import (
    xtctail_lookup_ingest_times_eager,
)


def tiltedxtc_lookup_ingest_times_eager(S: int, T: int) -> typing.List[int]:
    """Ingest time lookup algorithm for tiltedxtc curation.

    Eager implementation.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two greater than 4.
    T : int
        Current logical time.

    Returns
    -------
    typing.List[int]
        Ingest time of stored item at buffer sites in index order.
    """
    if tilted_has_ingest_capacity(S, T):
        return tilted_lookup_ingest_times_eager(S, T)
    else:
        return xtctail_lookup_ingest_times_eager(S, T)


# lazy loader workaround
lookup_ingest_times_eager = tiltedxtc_lookup_ingest_times_eager
