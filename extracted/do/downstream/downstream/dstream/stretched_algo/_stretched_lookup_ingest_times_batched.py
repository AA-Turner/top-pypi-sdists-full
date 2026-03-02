import warnings

import numpy as np

from ..._auxlib._bit_floor32 import bit_floor32
from ..._auxlib._bit_floor32_batched import bit_floor32_batched
from ..._auxlib._bitlen32 import bitlen32
from ..._auxlib._bitlen32_batched import bitlen32_batched
from ..._auxlib._bitlen32_scalar import bitlen32_scalar
from ..._auxlib._bitwise_count64_batched import bitwise_count64_batched
from ..._auxlib._ctz32 import ctz32
from ..._auxlib._ctz32_batched import ctz32_batched
from ..._auxlib._jit import jit
from ..._auxlib._jit_prange import jit_prange
from ..._auxlib._pick_batched_chunk_size import pick_batched_chunk_size


def stretched_lookup_ingest_times_batched(
    S: int,
    T: np.ndarray,
    parallel: bool = True,
) -> np.ndarray:
    """Ingest time lookup algorithm for stretched curation.

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

    if parallel and T.size and T.max() >= 2**32:
        warnings.warn(
            "T too large; due to numba limitations in handling overflows, "
            "falling back to serial processing."
        )
        parallel = False

    return [
        _stretched_lookup_ingest_times_batched_serial,
        _stretched_lookup_ingest_times_batched_jit,
    ][bool(parallel)](np.int64(S), T.astype(np.int64))


def _stretched_lookup_ingest_times_batched_serial(
    S: int,
    T: np.ndarray,
) -> np.ndarray:
    """Implementation detail for stretched_lookup_ingest_times_batched."""
    assert np.logical_and(
        np.asarray(S) > 1,
        bitwise_count64_batched(np.atleast_1d(np.asarray(S)).astype(np.uint64))
        == 1,
    ).all(), S
    # restriction <= 2 ** 52 (bitlen32 precision) might be overly conservative
    assert (np.maximum(S, T) <= 2**52).all()

    S = T.dtype.type(S)
    s = bitlen32(S) - 1
    t = bitlen32(T) - s  # Current epoch

    blt = bitlen32(t)  # Bit length of t
    epsilon_tau = bit_floor32(t.astype(np.uint64) << 1) > t + blt
    # ^^^ Correction factor
    tau0 = blt - epsilon_tau  # Current meta-epoch
    tau1 = tau0 + 1  # Next meta-epoch

    M = np.maximum((S >> tau1), 1)  # Num invading segments at current epoch
    w0 = (1 << tau0) - 1  # Smallest segment size at current epoch start
    w1 = (1 << tau1) - 1  # Smallest segment size at next epoch start

    h_ = np.zeros_like(T, dtype=T.dtype)
    # ^^^ Assigned hanoi value of 0th site
    m_p = np.zeros_like(T, dtype=T.dtype)
    # ^^^ Calc left-to-right index of 0th segment (physical segment idx)

    res = np.empty((T.size, S), dtype=np.uint64)
    for k in range(S):  # For each site in buffer...
        b_l = ctz32(M + m_p)  # Logical bunch index...
        # ... REVERSE fill order (decreasing nestedness/increasing init size r)

        epsilon_w = m_p == 0  # Correction factor for segment size
        w = w1 + b_l + epsilon_w  # Number of sites in current segment

        # Determine correction factors for not-yet-seen data items, Tbar_ >= T
        i_ = (M + m_p) >> (b_l + 1)  # Guess h.v. incidence (i.e., num seen)
        Tbar_k_ = np.maximum(  # Guess ingest time
            ((2 * i_ + 1).astype(np.uint64) << h_.astype(np.uint64)) - 1,
            (np.uint64(1) << h_.astype(np.uint64)) - 1,  # catch overflow
        )
        epsilon_h = (Tbar_k_ >= T) * (w - w0)  # Correction factor, h
        epsilon_i = (Tbar_k_ >= T) * (m_p + M - i_)  # Correction factor, i

        # Decode ingest time for ith instance of assigned h.v.
        h = h_ - epsilon_h  # True hanoi value
        i = i_ + epsilon_i  # True h.v. incidence
        res[:, k] = ((2 * i + 1) << h) - 1  # True ingest time, Tbar_k

        # Update state for next site...
        h_ += 1  # Assigned h.v. increases within each segment
        # Bump to next segment if current is filled
        m_p += (h_ == w).astype(T.dtype)
        h_ *= (h_ != w).astype(T.dtype)  # Reset h.v. if segment is filled

    return res


@jit("uint64[:,:](int64, int64[:])", nogil=True, nopython=True)
def _stretched_lookup_ingest_times_batched_jit_serial(
    S: int,
    T: np.ndarray,
) -> np.ndarray:
    """Implementation detail for stretched_lookup_ingest_times_batched."""
    assert np.logical_and(
        np.asarray(S) > 1,
        bitwise_count64_batched(np.atleast_1d(np.asarray(S)).astype(np.uint64))
        == 1,
    ).all(), S
    assert (np.maximum(S, T) <= 2**32).all()

    S, T = np.int64(S), T.astype(np.int64)  # patch for numba type limitations
    s = T.dtype.type(bitlen32_scalar(S)) - 1
    t = bitlen32_batched(T).astype(T.dtype) - s  # Current epoch

    blt = bitlen32_batched(t).astype(T.dtype)  # Bit length of t
    epsilon_tau = (
        bit_floor32_batched(t << 1).astype(T.dtype) > t + blt
    )  # Correction factor
    tau0 = blt - epsilon_tau  # Current meta-epoch
    tau1 = tau0 + 1  # Next meta-epoch

    M = np.maximum((S >> tau1), 1)  # Num invading segments at current epoch
    w0 = (1 << tau0) - 1  # Smallest segment size at current epoch start
    w1 = (1 << tau1) - 1  # Smallest segment size at next epoch start

    h_ = np.zeros_like(T, dtype=T.dtype)
    # ^^^ Assigned hanoi value of 0th site
    m_p = np.zeros_like(T, dtype=T.dtype)
    # ^^^ Calc left-to-right index of 0th segment (physical segment idx)

    res = np.zeros((T.size, S), dtype=np.uint64)
    for k in range(S):  # For each site in buffer...
        b_l = ctz32_batched(M + m_p).astype(T.dtype)  # Logical bunch index...
        # ... REVERSE fill order (decreasing nestedness/increasing init size r)

        epsilon_w = m_p == 0  # Correction factor for segment size
        w = w1 + b_l + epsilon_w  # Number of sites in current segment

        # Determine correction factors for not-yet-seen data items, Tbar_ >= T
        i_ = (M + m_p) >> (b_l + 1)  # Guess h.v. incidence (i.e., num seen)
        Tbar_k_ = ((2 * i_ + 1) << h_) - 1  # Guess ingest time
        assert (Tbar_k_ >= (np.uint64(1) << h_.astype(np.uint64)) - 1).all()
        # ^^^ catch overflow
        epsilon_h = (Tbar_k_ >= T) * (w - w0)  # Correction factor, h
        epsilon_i = (Tbar_k_ >= T) * (m_p + M - i_)  # Correction factor, i

        # Decode ingest time for ith instance of assigned h.v.
        h = h_ - epsilon_h  # True hanoi value
        i = i_ + epsilon_i  # True h.v. incidence
        res[:, k] = ((2 * i + 1) << h) - 1  # True ingest time, Tbar_k

        # Update state for next site...
        h_ += 1  # Assigned h.v. increases within each segment
        # Bump to next segment if current is filled
        m_p += (h_ == w).astype(T.dtype)
        h_ *= (h_ != w).astype(T.dtype)  # Reset h.v. if segment is filled

    return res


@jit(cache=True, nogil=True, nopython=True, parallel=True)
def _stretched_lookup_ingest_times_batched_jit(
    S: int, T: np.ndarray, chunk_size: int = pick_batched_chunk_size()
):
    """Implementation detail for stretched_lookup_ingest_times_batched."""
    num_rows = T.shape[0]
    num_chunks = (num_rows + chunk_size - 1) // chunk_size

    result = np.empty((num_rows, S), dtype=np.uint64)
    for chunk in jit_prange(num_chunks):
        chunk_slice = slice(
            chunk * chunk_size,  # begin
            min((chunk + 1) * chunk_size, num_rows),  # end
        )

        chunk_T = T[chunk_slice]
        chunk_result = _stretched_lookup_ingest_times_batched_jit_serial(
            S, chunk_T
        )
        result[chunk_slice, :] = chunk_result

    return result


# lazy loader workaround
lookup_ingest_times_batched = stretched_lookup_ingest_times_batched
