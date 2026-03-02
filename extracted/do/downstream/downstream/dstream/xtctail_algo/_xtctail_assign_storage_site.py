import typing

from ..._auxlib._ctz import ctz
from ..._auxlib._indexable_range import indexable_range
from ..._auxlib._modpow2 import modpow2
from ..compressing_algo._compressing_assign_storage_site import (
    compressing_assign_storage_site,
)
from ._xtctail_has_ingest_capacity import xtctail_has_ingest_capacity


def xtctail_assign_storage_site(S: int, T: int) -> typing.Optional[int]:
    """Site selection algorithm for xtctail curation.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two greater than 4.
    T : int
        Current logical time.

    Returns
    -------
    typing.Optional[int]
        Selected site, if any.

    Raises
    ------
    ValueError
        If insufficient ingest capacity is available.

        See `xtctail_algo.has_ingest_capacity` for details.

    References
    ----------
    John C. Gunther. 2014. Algorithm 938: Compressing circular buffers. ACM
    Trans. Math. Softw. 40, 2, Article 17 (February 2014), 12 pages.
    https://doi.org/10.1145/2559995
    """
    if not xtctail_has_ingest_capacity(S, T):
        raise ValueError(f"Insufficient ingest capacity for {S=}, {T=}")

    S, T = int(S), int(T)
    h = ctz(T + 1)  # Current hanoi value

    if T < S:  # handle initial fill
        hv_offset = (1 << h) - 1
        hv_cadence = 2 << h
        T_ = 2 * hv_offset + ((S - hv_offset - 1) >> (h + 1)) * hv_cadence - T
        assert (
            T_
            == reversed(indexable_range(hv_offset, S, hv_cadence))[
                indexable_range(hv_offset, S, hv_cadence).index(T)
            ]
        )
        if (T_ + 1).bit_count() <= 1:
            return h
        else:
            # see https://oeis.org/A057716
            return S.bit_length() + T_ - T_.bit_length()

    if h <= 1:  # optimization --- not strictly necessary
        return h  # sites -0 and 1 always store hv's 0 and 1

    epoch = (T + 1).bit_length()  # Current epoch
    si = ((epoch - 2) // (S - 1)).bit_length()  # Current sampling interval
    si_ = 1 << si
    assert si_
    prev_si_ = si_ >> 1

    if modpow2(h, max(prev_si_, 1)):  # is not in either sampling interval
        return None
    elif modpow2(h - bool(h), si_) == 0:  # is in current sampling interval
        return compressing_assign_storage_site(S, h)

    num_cur_si = (epoch + si_ - 2) >> si
    assert len(range(1, epoch, si_)) == num_cur_si

    ub = (S - 1) * prev_si_
    lb = ub - (S - 1 - num_cur_si) * si_ + 1
    if lb <= h < ub:  # is among remaining entries from previous si
        return compressing_assign_storage_site(S, h)
    else:  # is among discarded entries from previous si
        return None


assign_storage_site = xtctail_assign_storage_site  # lazy loader workaround
