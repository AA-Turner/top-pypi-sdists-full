import typing

from ..._auxlib._bit_floor import bit_floor
from ..._auxlib._ctz import ctz
from ..._auxlib._modpow2 import modpow2


def tilted_lookup_ingest_times(
    S: int, T: int
) -> typing.Iterable[typing.Optional[int]]:
    """Ingest time lookup algorithm for tilted curation.

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
        Ingest time of stored item, if any, at buffer sites in index order.
    """
    assert T >= 0
    if T < S:  # Patch for before buffer is filled...
        return (v if v < T else None for v in tilted_lookup_impl(S, S))
    else:  # ... assume buffer has been filled
        return tilted_lookup_impl(S, T)


def tilted_lookup_impl(S: int, T: int) -> typing.Iterable[int]:
    """Implementation detail for `tilted_lookup_ingest_times`."""
    S, T = int(S), int(T)  # play nice with numpy types
    assert S > 1 and S.bit_count() == 1
    # T < S redirected to T = S by tilted_lookup_ingest_times
    assert T >= S  # T < S redirected to T = S by tilted_lookup_ingest_times

    s = S.bit_length() - 1
    t = (T).bit_length() - s  # Current epoch

    blt = t.bit_length()  # Bit length of t
    epsilon_tau = bit_floor(t << 1) > t + blt  # Correction factor
    tau0 = blt - epsilon_tau  # Current meta-epoch
    tau1 = tau0 + 1  # Next meta-epoch
    t0 = (1 << tau0) - tau0  # Opening epoch of current meta-epoch
    T0 = 1 << (t + s - 1)  # Opening time of current epoch

    M_ = S >> tau1 or 1  # Number of invading segments present at current epoch
    w0 = (1 << tau0) - 1  # Smallest segment size at current epoch start
    w1 = (1 << tau1) - 1  # Smallest segment size at next epoch start

    h_ = 0  # Assigned hanoi value of 0th site
    m_p = 0  # Left-to-right (physical) segment index
    for k in range(S):  # For each site in buffer...
        b_l = ctz(M_ + m_p)  # Reverse fill order (logical) bunch index
        epsilon_w = m_p == 0  # Correction factor for segment size
        w = w1 + b_l + epsilon_w  # Number of sites in current segment
        m_l_ = (M_ + m_p) >> (b_l + 1)  # Logical (fill order) segment index

        # Detect scenario...
        # Scenario A: site in invaded segment, h.v. ring buffer intact
        X_A = h_ - (t - t0) > w - w0  # To be invaded in future epoch t in tau?
        T_i = ((2 * m_l_ + 1) << h_) - 1  # When overwritten by invader?
        X_A_ = h_ - (t - t0) == w - w0 and T_i >= T  # Invaded at this epoch?

        # Scenario B site in invading segment, h.v. ring buffer intact
        X_B = (t - t0 < h_ < w0) and (t < S - s)  # At future epoch t in tau?
        T_r = T0 + T_i  # When is site refilled after ring buffer halves?
        X_B_ = (h_ == t - t0) and (t < S - s) and (T_r >= T)  # At this epoch?

        assert X_A + X_A_ + X_B + X_B_ <= 1  # scenarios are mutually exclusive

        # Calculate corrected values...
        epsilon_G = (X_A or X_A_ or X_B or X_B_) * M_
        epsilon_h = (X_A or X_A_) * (w - w0)
        epsilon_T = (X_A_ or X_B_) * (T - T0)  # Snap back to start of epoch

        M = M_ + epsilon_G
        h = h_ - epsilon_h
        Tc = T - epsilon_T  # Corrected time
        m_l = (X_A or X_A_) * (M_ + m_p) or m_l_

        # Decode what h.v. instance fell on site k...
        j = ((Tc + (1 << h)) >> (h + 1)) - 1  # Num seen, less one
        i = j - modpow2(j - m_l + M, M)  # H.v. incidence resident at site k
        # ... then decode ingest time for that ith h.v. instance
        yield ((2 * i + 1) << h) - 1  # True ingest time, Tbar_k

        # Update state for next site...
        h_ += 1  # Assigned h.v. increases within each segment
        m_p += h_ == w  # Bump to next segment if current is filled
        h_ *= h_ != w  # Reset h.v. if segment is filled


lookup_ingest_times = tilted_lookup_ingest_times  # lazy loader workaround
