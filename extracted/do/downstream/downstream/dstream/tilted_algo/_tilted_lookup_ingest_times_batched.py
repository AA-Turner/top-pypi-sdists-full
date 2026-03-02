import numpy as np

from ..._auxlib._bit_floor32_batched import bit_floor32_batched
from ..._auxlib._bitlen32_batched import bitlen32_batched
from ..._auxlib._bitlen32_scalar import bitlen32_scalar
from ..._auxlib._bitwise_count64_batched import bitwise_count64_batched
from ..._auxlib._ctz32_batched import ctz32_batched
from ..._auxlib._jit import jit
from ..._auxlib._jit_prange import jit_prange
from ..._auxlib._modpow2_batched import modpow2_batched
from ..._auxlib._pick_batched_chunk_size import pick_batched_chunk_size

_lor = np.logical_or
_land = np.logical_and


def tilted_lookup_ingest_times_batched(
    S: int,
    T: np.ndarray,
    parallel: bool = True,
) -> np.ndarray:
    """Ingest time lookup algorithm for tilted curation.

    Vectorized implementation for bulk calculations.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two.
    T : np.ndarray
        One-dimensional array of current logical times.
    parallel : bool, default True
        Should numba be applied to parallelize operations?

    Returns
    -------
    np.ndarray
        Ingest time of stored items at buffer sites in index order.

        Two-dimensional array. Each row corresponds to an entry in T. Contains
        S columns, each corresponding to buffer sites.
    """
    assert np.issubdtype(np.asarray(S).dtype, np.integer), S
    assert np.issubdtype(T.dtype, np.integer), T

    if (T < S).any():
        raise ValueError("T < S not supported for batched lookup")

    return [
        _tilted_lookup_ingest_times_batched,
        _tilted_lookup_ingest_times_batched_jit,
    ][bool(parallel)](np.int64(S), T.astype(np.int64))


def _tilted_lookup_ingest_times_batched(S: int, T: np.ndarray) -> np.ndarray:
    """Implementation detail for tilted_lookup_ingest_times_batched."""
    assert np.logical_and(
        np.asarray(S) > 1,
        bitwise_count64_batched(np.atleast_1d(np.asarray(S)).astype(np.uint64))
        == 1,
    ).all(), S
    # restriction <= 2 ** 52 (bitlen32 precision) might be overly conservative
    assert (np.maximum(S, T) <= 2**52).all()

    S, T = np.int64(S), T.astype(np.int64)  # Prevent overflow

    s = bitlen32_scalar(S) - 1
    t = bitlen32_batched(T).astype(T.dtype) - s  # Current epoch

    blt = bitlen32_batched(t).astype(T.dtype)  # Bit length of t
    # ^^^ why is this dtype cast necessary?
    epsilon_tau = bit_floor32_batched(t << 1) > t + blt  # Correction factor
    tau0 = blt - epsilon_tau  # Current meta-epoch
    tau1 = tau0 + 1  # Next meta-epoch
    t0 = (1 << tau0) - tau0  # Opening epoch of current meta-epoch
    T0 = 1 << (t + s - 1)  # Opening time of current epoch

    M_ = np.maximum(S >> tau1, 1)
    # ^^^ Number of invading segments present at current epoch
    w0 = (1 << tau0) - 1  # Smallest segment size at current epoch start
    w1 = (1 << tau1) - 1  # Smallest segment size at next epoch start

    h_ = np.zeros_like(T, dtype=T.dtype)
    # ^^^ Assigned hanoi value of 0th site
    m_p = np.zeros_like(T, dtype=T.dtype)
    # ^^^ Calc left-to-right index of 0th segment (physical segment idx)

    res = np.empty((T.size, S), dtype=np.uint64)
    for k in range(S):  # For each site in buffer...
        b_l = ctz32_batched(  # Reverse fill order (logical) bunch index
            M_ + m_p,
        ).astype(T.dtype)
        epsilon_w = m_p == 0  # Correction factor for segment size
        w = w1 + b_l + epsilon_w  # Number of sites in current segment
        m_l_ = (M_ + m_p) >> (b_l + 1)  # Logical (fill order) segment index

        # Detect scenario...
        # Scenario A: site in invaded segment, h.v. ring buffer intact
        X_A = h_ - (t - t0) > w - w0  # To be invaded in future epoch t in tau?
        T_i = ((2 * m_l_ + 1) << h_) - 1  # When overwritten by invader?
        X_A_ = _land(h_ - (t - t0) == w - w0, T_i >= T)
        # ^^^ Invaded at this epoch?

        # Scenario B site in invading segment, h.v. ring buffer intact
        Ss = np.uint64(S) - np.uint64(s)
        X_B = _land(t - t0 < h_, _land(h_ < w0, t < Ss))
        # ^^^ At future epoch t in tau?
        T_r = T0 + T_i  # When is site refilled after ring buffer halves?
        X_B_ = _land(h_ == t - t0, _land(t < Ss, T_r >= T))
        # ^^^ At this epoch?

        assert (np.asarray(X_A + X_A_ + X_B + X_B_) <= 1).all()
        # ^^^ scenarios are mutually exclusive

        # Calculate corrected values...
        epsilon_G = _lor(X_A, _lor(X_A_, _lor(X_B, X_B_))) * M_
        epsilon_h = _lor(X_A, X_A_) * (w - w0)
        epsilon_T = _lor(X_A_, X_B_) * (T - T0)
        # ^^^ Snap back to start of epoch

        M = M_ + epsilon_G
        h = h_ - epsilon_h
        Tc = T - epsilon_T  # Corrected time
        m_l = np.where(
            _lor(X_A, X_A_),
            (M_ + m_p),
            m_l_,
        )

        # Decode what h.v. instance fell on site k...
        j = ((Tc + (1 << h)) >> (h + 1)) - 1  # Num seen, less one
        i = j - modpow2_batched(j - m_l + M, M)
        # ^^^ H.v. incidence resident at site k
        # ... then decode ingest time for that ith h.v. instance
        res[:, k] = ((2 * i + 1) << h) - 1  # True ingest time, Tbar_k

        # Update state for next site...
        h_ += 1
        # ^^^ Assigned h.v. increases within each segment
        m_p += (h_ == w).astype(T.dtype)
        # ^^^ Bump to next segment if current is filled
        h_ *= (h_ != w).astype(T.dtype)  # Reset h.v. if segment is filled

    return res


# implementation detail for _tilted_lookup_ingest_times_batched_jit
_tilted_lookup_ingest_times_batched_jit_serial = jit(
    "uint64[:,:](int64, int64[:])", nogil=True, nopython=True
)(_tilted_lookup_ingest_times_batched)


@jit(cache=True, nogil=True, nopython=True, parallel=True)
def _tilted_lookup_ingest_times_batched_jit(
    S: int, T: np.ndarray, chunk_size: int = pick_batched_chunk_size()
):
    """Implementation detail for tilted_lookup_ingest_times_batched."""
    num_rows = T.shape[0]
    num_chunks = (num_rows + chunk_size - 1) // chunk_size

    result = np.empty((num_rows, S), dtype=np.uint64)
    for chunk in jit_prange(num_chunks):
        chunk_slice = slice(
            chunk * chunk_size,  # begin
            min((chunk + 1) * chunk_size, num_rows),  # end
        )

        chunk_T = T[chunk_slice]
        chunk_result = _tilted_lookup_ingest_times_batched_jit_serial(
            S, chunk_T
        )
        result[chunk_slice, :] = chunk_result

    return result


# lazy loader workaround
lookup_ingest_times_batched = tilted_lookup_ingest_times_batched
