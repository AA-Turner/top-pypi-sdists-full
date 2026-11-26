"""Utility functions for AOT-biomaps acoustic-field generation.

The module groups reusable helpers for:
- MAT files and acquisition naming;
- probe-pattern decoding and steering-angle calculations;
- SIMPLE_SIM piezo-to-grid mapping;
- GPU/CPU array layout conversion;
- Hilbert-envelope calculation and anti-aliased resampling;
- dynamic GPU-memory budgeting and asynchronous pinned-memory staging.

Array layout conventions
------------------------
The k-Wave simulation grid uses ``(Nx, Nz, Nt)`` with time on the last axis.
The reconstruction pipeline stores fields as ``(Nt, Nz, Nx)`` with time on
the first axis.

GPU memory policy
-----------------
Large arrays are not proactively freed inside processing loops. CuPy's memory
pool is allowed to reuse temporary allocations, and FFT plans remain cached.
The explicit :func:`clear_gpu_memory` helper is available for callers that
really need to return unused cached memory to the CUDA driver.
"""

from __future__ import annotations

import gc
import os
import numpy as np
from scipy.io import loadmat as scipy_loadmat
from scipy.stats import linregress
from scipy.fft import next_fast_len
from scipy import fft as scipy_fft
from numba import njit, prange

try:
    import cupy as cp
    CUPY_AVAILABLE = True
except ImportError:  # pragma: no cover - depends on the runtime
    cp = None
    CUPY_AVAILABLE = False

_IQ_ENVELOPE_KERNEL = None

def _resample_axis(arr, n_new, axis, xp):
    """Resample one axis using integer decimation or linear interpolation.

    Integer decimation returns a view whenever possible.
    Linear interpolation uses two indexed arrays and performs the
    arithmetic in-place to limit temporary allocations.
    """
    n_old = int(arr.shape[axis])

    if n_new is None or int(n_new) == n_old:
        return arr

    n_new = int(n_new)

    if n_new <= 0:
        raise ValueError(f"Invalid output size on axis {axis}: {n_new}")

    if axis < 0:
        axis += arr.ndim

    if axis < 0 or axis >= arr.ndim:
        raise ValueError(f"Invalid axis: {axis}")

    # Return a strided view for exact integer decimation.
    if n_old % n_new == 0 and n_old // n_new > 1:
        slices = [slice(None)] * arr.ndim
        slices[axis] = slice(None, None, n_old // n_new)
        return arr[tuple(slices)]

    # Build interpolation coordinates.
    positions = xp.linspace(
        0.0,
        n_old - 1.0,
        n_new,
        dtype=xp.float64,
    )

    index0 = xp.floor(positions).astype(xp.int64)
    index1 = xp.minimum(index0 + 1, n_old - 1)

    weights = (positions - index0).astype(xp.float32)
    weights = weights.reshape(
        (n_new,) + (1,) * (arr.ndim - 1))

    # Move the resampled axis to the leading dimension.
    moved = xp.moveaxis(arr, axis, 0)

    # Advanced indexing creates independent arrays.
    lower = moved[index0]
    upper = moved[index1]

    # In-place interpolation:
    # upper <- lower + weights * (upper - lower)
    xp.subtract(upper, lower, out=upper)
    xp.multiply(upper, weights, out=upper)
    xp.add(upper, lower, out=upper)

    return xp.moveaxis(upper, 0, axis)


def _get_xp(xp=None):
    """Return the requested array namespace, defaulting to CuPy when present."""
    if xp is not None:
        return xp
    return cp if CUPY_AVAILABLE else np


def _get_dynamic_chunk_size(field_shape, ortho_axis, xp, multiplier=10.0):
    """Estimate a safe chunk size from currently available device memory.

    ``multiplier`` approximates FFT input, spectrum, output, and workspace
    overhead relative to one float32 input chunk. It is deliberately a
    workspace estimate, not a hard byte limit.
    """
    n_ortho = int(field_shape[ortho_axis])
    if n_ortho <= 0:
        raise ValueError("The chunked axis must have a positive length.")
    if getattr(xp, "__name__", "numpy") != "cupy":
        return n_ortho

    free_bytes, _ = xp.cuda.runtime.memGetInfo()
    pool = xp.get_default_memory_pool()
    allocatable_bytes = int(free_bytes) + int(pool.free_bytes())
    elements_per_slice = int(np.prod(field_shape)) // n_ortho
    bytes_per_slice = elements_per_slice * np.dtype(np.float32).itemsize
    safe_bytes = int(allocatable_bytes * 0.8)

    if bytes_per_slice <= 0:
        return n_ortho
    return max(1, min(n_ortho, int(safe_bytes / (bytes_per_slice * multiplier))))


def clear_gpu_memory(xp=None, clear_fft_plans=False):
    xp = _get_xp(xp)
    if getattr(xp, "__name__", "numpy") != "cupy":
        return
    if clear_fft_plans:
        try:
            import cupy.fft._cache as _fft_cache        # CuPy >= 13/14
            _fft_cache.get_plan_cache().clear()
        except ImportError:
            try:
                xp.fft.config.get_plan_cache().clear()   
            except Exception:
                pass
    xp.get_default_memory_pool().free_all_blocks()


def _clear_gpu_memory(xp):
    """Backward-compatible alias for :func:`clear_gpu_memory`."""
    clear_gpu_memory(xp=xp, clear_fft_plans=True)


def get_gpu_memory_info(xp=None):
    """Return physical and CuPy-pool memory information for the active device.

    ``allocatable_bytes`` includes both CUDA-driver free memory and unused
    blocks already owned by CuPy's default memory pool.
    """
    xp = _get_xp(xp)
    if getattr(xp, "__name__", "numpy") != "cupy":
        return {
            "free_bytes": None,
            "total_bytes": None,
            "pool_free_bytes": 0,
            "pool_used_bytes": 0,
            "allocatable_bytes": None,
        }

    free_bytes, total_bytes = xp.cuda.runtime.memGetInfo()
    pool = xp.get_default_memory_pool()
    pool_free = int(pool.free_bytes())
    pool_used = int(pool.used_bytes())
    return {
        "free_bytes": int(free_bytes),
        "total_bytes": int(total_bytes),
        "pool_free_bytes": pool_free,
        "pool_used_bytes": pool_used,
        "allocatable_bytes": int(free_bytes) + pool_free,
    }


def get_gpu_output_budget_bytes(xp=None, fraction=0.95, cap_bytes=None):
    """Compute a dynamic byte budget for a large GPU output buffer.

    The budget is based on memory available *at call time*. ``fraction`` leaves
    proportional headroom for allocator fragmentation and transient workspaces;
    no fixed GiB reserve is imposed. ``cap_bytes`` is an optional caller-defined
    ceiling and defaults to ``None``.
    """
    if not (0.0 < float(fraction) <= 1.0):
        raise ValueError("fraction must be in the interval (0, 1].")
    info = get_gpu_memory_info(xp)
    if info["allocatable_bytes"] is None:
        return 0
    budget = int(info["allocatable_bytes"] * float(fraction))
    if cap_bytes is not None:
        if int(cap_bytes) < 0:
            raise ValueError("cap_bytes must be non-negative or None.")
        budget = min(budget, int(cap_bytes))
    return budget


def get_available_host_memory_bytes():
    """Return currently available system RAM in bytes when it can be queried."""
    try:
        import psutil  # Optional dependency; used only for host-memory sizing.
        return int(psutil.virtual_memory().available)
    except ImportError:
        pass
    except Exception:
        pass

    if hasattr(os, "sysconf"):
        try:
            return int(os.sysconf("SC_AVPHYS_PAGES") * os.sysconf("SC_PAGE_SIZE"))
        except (ValueError, OSError, AttributeError):
            pass
    return None


def get_transfer_chunk_frames(ring_frames, frame_bytes, host_staging_fraction=1.0 / 16.0):
    """Choose a transfer chunk from ring capacity and available host RAM.

    Two pinned staging buffers are used. Their combined target size is limited
    to a fraction of currently available host RAM, not to a fixed byte count.
    The chunk is also kept below half the GPU ring so computation and transfer
    can overlap.
    """
    ring_frames = int(ring_frames)
    frame_bytes = int(frame_bytes)
    if ring_frames <= 0 or frame_bytes <= 0:
        raise ValueError("ring_frames and frame_bytes must be positive.")
    if not (0.0 < float(host_staging_fraction) <= 1.0):
        raise ValueError("host_staging_fraction must be in (0, 1].")

    available_host = get_available_host_memory_bytes()
    if available_host is None:
        host_budget = ring_frames * frame_bytes // 4
    else:
        host_budget = int(available_host * float(host_staging_fraction))

    # Each of the two staging buffers has half of the aggregate pinned budget.
    max_frames_per_stage = max(1, host_budget // (2 * frame_bytes))
    overlap_limit = max(1, ring_frames // 2)
    return max(1, min(overlap_limit, max_frames_per_stage))


def allocate_pinned_staging_buffers(frame_shape, requested_frames, n_buffers=2, dtype=np.float32):
    """Allocate pinned host staging arrays, shrinking the frame count on OOM.

    Returns
    -------
    pinned_allocations : list
        CuPy pinned-memory owner objects. Keep them alive while arrays are used.
    host_arrays : list[numpy.ndarray]
        NumPy views backed by the pinned allocations.
    allocated_frames : int
        Actual number of frames in each staging buffer.
    """
    if not CUPY_AVAILABLE:
        raise RuntimeError("Pinned staging buffers require CuPy.")
    requested_frames = int(requested_frames)
    n_buffers = int(n_buffers)
    if requested_frames <= 0 or n_buffers <= 0:
        raise ValueError("requested_frames and n_buffers must be positive.")

    frame_shape = tuple(int(v) for v in frame_shape)
    if not frame_shape or any(v <= 0 for v in frame_shape):
        raise ValueError("frame_shape must contain positive dimensions.")
    frame_elements = int(np.prod(frame_shape))
    dtype = np.dtype(dtype)
    frames = requested_frames

    while frames >= 1:
        owners = []
        arrays = []
        try:
            nbytes = frames * frame_elements * dtype.itemsize
            for _ in range(n_buffers):
                owner = cp.cuda.alloc_pinned_memory(nbytes)
                array = np.frombuffer(owner, dtype=dtype, count=frames * frame_elements)
                arrays.append(array.reshape((frames,) + frame_shape))
                owners.append(owner)
            return owners, arrays, frames
        except Exception:
            del arrays, owners
            gc.collect()
            if frames == 1:
                raise
            frames = max(1, frames // 2)

    raise MemoryError("Unable to allocate pinned host staging buffers.")


def get_iq_envelope_kernel():
    """Return the lazily compiled CUDA kernel for streaming I/Q demodulation.

    Each thread processes one spatial voxel. Filter states persist between
    time steps, and the squared envelope is written directly into the caller's
    output/ring buffer. No per-frame device-side output image is allocated.
    """
    global _IQ_ENVELOPE_KERNEL
    if not CUPY_AVAILABLE:
        raise RuntimeError("The I/Q CUDA kernel requires CuPy.")
    if _IQ_ENVELOPE_KERNEL is None:
        _IQ_ENVELOPE_KERNEL = cp.RawKernel(
            r"""
extern "C" __global__ void iq_envelope_step(
    const float* __restrict__ p,
    const int Nx, const int NzPad, const int PmlX, const int PmlZ,
    double* __restrict__ i_state1, double* __restrict__ i_state2,
    double* __restrict__ q_state1, double* __restrict__ q_state2,
    float* __restrict__ output,
    float* __restrict__ debug_pressure, float* __restrict__ debug_env2,
    const int debug_index, const int time_index,
    const long long output_slot, const int global_output_index,
    const int K, const double c_phase, const double s_phase,
    const double alpha, const int write_output,
    const int debug_enabled, const int output_sqrt)
{
    const int k = blockDim.x * blockIdx.x + threadIdx.x;
    if (k >= K) return;

    const int x = k % Nx;
    const int z = k / Nx;
    const int p_index = (x + PmlX) * NzPad + (z + PmlZ);
    const double pv = (double)p[p_index];

    if (debug_enabled && k == debug_index) {
        debug_pressure[time_index] = (float)pv;
    }

    const double beta = 1.0 - alpha;
    const double xI =  2.0 * pv * c_phase;
    const double xQ = -2.0 * pv * s_phase;

    const double i1 = alpha * xI + beta * i_state1[k];
    const double i2 = alpha * i1 + beta * i_state2[k];
    const double q1 = alpha * xQ + beta * q_state1[k];
    const double q2 = alpha * q1 + beta * q_state2[k];

    i_state1[k] = i1;
    i_state2[k] = i2;
    q_state1[k] = q1;
    q_state2[k] = q2;

    if (write_output) {
        const float e2 = (float)(i2 * i2 + q2 * q2);
        const float value = output_sqrt ? sqrtf(e2) : e2;
        const unsigned long long offset =
            (unsigned long long)output_slot * (unsigned long long)K + (unsigned long long)k;
        output[offset] = value;
        if (debug_enabled && k == debug_index) {
            debug_env2[global_output_index] = e2;
        }
    }
}
""",
            "iq_envelope_step",
        )
    return _IQ_ENVELOPE_KERNEL

# ---------------------------------------------------------------------------
# MAT / IO helpers
# ---------------------------------------------------------------------------

def loadmat(param_path_mat):
    """
    Load a .mat file (MATLAB format).

    Args:
        param_path_mat: Path to the .mat file.

    Returns:
        Dictionary containing the variables from the file.
    """
    try:
        return scipy_loadmat(param_path_mat)
    except Exception:
        raise ValueError(f"[AOT-biomaps] Could not load {param_path_mat}. Consider using scipy.io.loadmat or h5py for HDF5 files.")

# ---------------------------------------------------------------------------
# Pattern & file-name utilities
# ---------------------------------------------------------------------------

def get_pattern(pathFile):
    """
    Extract the pattern from a file path.

    Args:
        pathFile (str): Path to the file containing the pattern.

    Returns:
        str: The pattern string.
    """
    try:
        # Pattern between first _ and last _
        pattern = os.path.basename(pathFile).split('_')[1:-1]
        pattern_str = ''.join(pattern)
        return pattern_str
    except Exception as e:
        print(f"[AOT-biomaps] Error reading pattern from file: {e}")
        return None

def detect_space_0_and_space_1(hex_string):
    """
    Detect the longest sequences of 0s and 1s in a hex string.

    Args:
        hex_string: Hexadecimal string.

    Returns:
        tuple: (space_0, space_1) where space_0 is the length of the longest 0 sequence,
               and space_1 is the length of the longest 1 sequence.
    """
    binary_string = bin(int(hex_string, 16))[2:].zfill(len(hex_string) * 4)

    # Find longest sequence of consecutive 0s
    zeros_groups = [len(s) for s in binary_string.split('1')]
    space_0 = max(zeros_groups) if zeros_groups else 0

    # Find longest sequence of consecutive 1s
    ones_groups = [len(s) for s in binary_string.split('0')]
    space_1 = max(ones_groups) if ones_groups else 0

    return space_0, space_1

def get_angle(pathFile):
    """
    Extract the angle from a file path.

    Args:
        pathFile (str): Path to the file containing the angle.

    Returns:
        int: The angle in degrees.
    """
    try:
        # Angle between last _ and .
        angle_str = os.path.basename(pathFile).split('_')[-1].replace('.', '')
        if angle_str.startswith('0'):
            angle_str = angle_str[1:]
        elif angle_str.startswith('1'):
            angle_str = '-' + angle_str[1:]
        else:
            raise ValueError(f"[AOT-biomaps] Invalid angle format in file name: {pathFile}")
        return int(angle_str)
    except Exception as e:
        print(f"[AOT-biomaps] Error reading angle from file: {e}")
        return None

def get_frequency(fileName, num_elements, dx):
    """Return the dominant spatial-frequency bin of an activation pattern.

    The helper accepts the filename conventions used throughout AOT-biomaps:
    ``<hex>_<angle>``, ``field_<hex>_<angle>.hdr``, ``<hex>`` and paths to
    any of those forms. The angle and file extension do not affect the result.

    Parameters
    ----------
    fileName : str or os.PathLike
        Pattern identifier or acoustic-field filename.
    num_elements : int
        Number of transducer elements represented by the pattern.
    dx : float
        Element pitch in metres. It is validated for API compatibility; the
        returned integer is a normalized FFT-bin index, so ``dx`` cancels
        from the normalization.

    Returns
    -------
    int
        Dominant positive-frequency FFT bin. An all-active pattern returns 0.

    Notes
    -----
    This is equivalent to computing ``f_peak / (1 / (N * dx))`` from the
    original implementation, but returns the integer FFT bin directly and
    avoids fragile fixed-position filename slicing.
    """
    import os

    n_elements = int(num_elements)
    dx = float(dx)
    if n_elements < 4:
        raise ValueError("num_elements must be at least 4.")
    if not np.isfinite(dx) or dx <= 0.0:
        raise ValueError("dx must be a finite positive value in metres.")

    name = os.path.basename(os.fspath(fileName)).strip()
    stem, _ = os.path.splitext(name)
    if stem.startswith("field_"):
        stem = stem[len("field_"):]

    # Pattern IDs are stored as '<hex>_<encoded angle>'; a bare hex string is
    # also accepted by experimental-import and pattern-generation routines.
    pattern_hex = stem.split("_")[0].strip().replace(" ", "")
    if not pattern_hex:
        raise ValueError(f"Cannot extract a hexadecimal pattern from {fileName!r}.")
    try:
        int(pattern_hex, 16)
    except ValueError as exc:
        raise ValueError(
            f"Invalid hexadecimal activation pattern {pattern_hex!r} in {fileName!r}."
        ) from exc

    profile = hex_to_binary_profile(pattern_hex, n_elements)
    if pattern_hex and all(character.lower() == "f" for character in pattern_hex):
        return 0

    # rFFT includes the Nyquist bin for even-length patterns. That bin is a
    # valid alternating-element activation (period of two elements).
    spectrum = np.fft.rfft(profile)
    positive_spectrum = np.abs(spectrum[1:])
    if positive_spectrum.size == 0 or not np.any(positive_spectrum):
        return 0
    return int(np.argmax(positive_spectrum) + 1)

def format_angle(a):
    """
    Format an angle as a string for file naming.

    Args:
        a: Angle in degrees.

    Returns:
        str: Formatted angle string (e.g., "045" or "145" for -45).
    """
    return f"{'1' if a < 0 else '0'}{abs(int(a)):02d}"

def next_power_of_2(n):
    """Return the smallest power of two greater than or equal to ``n``."""
    n = int(n)
    if n <= 0:
        raise ValueError("n must be a positive integer.")
    return 1 << (n - 1).bit_length()

def hex_to_binary_profile(hex_string, n_piezos=192):
    """
    Convert a hex string to a binary profile array.

    Args:
        hex_string: Hexadecimal string representing the pattern.
        n_piezos: Number of piezos in the probe (default: 192).

    Returns:
        numpy.ndarray: Binary profile as an array of 0s and 1s.
    """
    hex_string = hex_string.strip().replace(" ", "").replace("\n", "")
    if set(hex_string.lower()) == {'f'}:
        return np.ones(n_piezos, dtype=int)

    try:
        n_char = len(hex_string)
        n_bits = n_char * 4
        binary_str = bin(int(hex_string, 16))[2:].zfill(n_bits)
        if len(binary_str) < n_piezos:
            # Pad or truncate to match the actual probe size
            binary_str = binary_str.ljust(n_piezos, '0')
        elif len(binary_str) > n_piezos:
            binary_str = binary_str[:n_piezos]
        return np.array([int(b) for b in binary_str])
    except ValueError:
        return np.zeros(n_piezos, dtype=int)

def calculate_angle_from_delays(delays, num_elements=192, pitch=0.2e-3, c=1540):
    """
    Calculate the angle of incidence theta (in degrees) from an array of delays.
    Uses linear regression to estimate the slope of the delays.

    Args:
        delays: Array of per-element delays (in seconds).
        num_elements: Number of elements in the probe (default: 192).
        pitch: Element spacing in meters (default: 0.2 mm).
        c: Speed of sound (m/s).

    Returns:
        theta: Angle in degrees (positive to the right, negative to the left).
    """
    x = np.linspace(-(num_elements - 1) / 2 * pitch, (num_elements - 1) / 2 * pitch, num_elements)

    # Linear regression to estimate the slope (sin(theta) / c)
    slope, _, _, _, _ = linregress(x, delays)

    # Calculate the angle (in degrees)
    theta = np.rad2deg(np.arcsin(slope * c))

    # Determine the sign based on the position of the maximum delay
    max_index = int(np.argmax(delays))
    if max_index < num_elements // 2:  # Left
        theta = -abs(theta)
    elif max_index > num_elements // 2:  # Right
        theta = abs(theta)
    else:  # Center (theta ~ 0)
        theta = 0.0

    return int(np.round(theta, 0))

# ---------------------------------------------------------------------------
# SIMPLE_SIM helpers
# ---------------------------------------------------------------------------

def get_piezo_to_grid_mapping(Nx, dx, num_elements, element_width, pitch, probe_start_x, active_list):
    """Map piezo elements to grid pixels with exact fractional coverage."""
    mappings = []

    for i in range(num_elements):
        if active_list[i] == 0:
            continue

        el_start_x = probe_start_x + i * pitch
        el_end_x = el_start_x + element_width

        start_idx = int(np.floor(el_start_x / dx))
        end_idx = int(np.floor(el_end_x / dx))

        # Single pixel coverage
        if start_idx == end_idx:
            if 0 <= start_idx < Nx:
                mappings.append((i, start_idx, element_width / dx))

        # Multi-pixel coverage
        else:
            if 0 <= start_idx < Nx:
                fraction_start = ((start_idx + 1) * dx - el_start_x) / dx
                mappings.append((i, start_idx, fraction_start))

            for j in range(start_idx + 1, end_idx):
                if 0 <= j < Nx:
                    mappings.append((i, j, 1.0))

            if 0 <= end_idx < Nx and (el_end_x - end_idx * dx) > 1e-9:
                fraction_end = (el_end_x - end_idx * dx) / dx
                mappings.append((i, end_idx, fraction_end))

    return mappings

@njit(parallel=True, fastmath=True)
def compute_field_numba(field, t, active_indices, apod_window, weight_base,
                        x_start_probe_fine, x_pivot_px_fine, dx_fine, c0, angle_rad,
                        n_t_burst, enveloppe_t, el_width_px_fine, cos_a, sin_a,
                        factor, Nt, Nz, Nx, Nx_fine, Nz_fine):
    """
    Kernel Numba (C) for the SIMPLE_SIM propagation loop.
    """
    for idx in prange(len(active_indices)):
        i = active_indices[idx]
        val_i = weight_base * apod_window[i]

        x_i_px_fine = x_start_probe_fine + (i * el_width_px_fine)
        dist_to_pivot = (x_i_px_fine - x_pivot_px_fine) * dx_fine
        delay_i = (abs(dist_to_pivot) * np.sin(abs(angle_rad))) / c0

        for t_idx in range(Nt):
            t_eff = t[t_idx] - delay_i
            if t_eff <= 0 or t_eff >= t[-1]:
                continue

            dist_travelled = c0 * t_eff
            z_px_fine = int((dist_travelled * cos_a) / dx_fine)
            x_px_fine_base = int((x_i_px_fine * dx_fine + dist_travelled * sin_a) / dx_fine)

            for b_shift in range(n_t_burst):
                st = t_idx + b_shift
                if st >= Nt:
                    continue

                val_final = enveloppe_t[b_shift] * val_i

                for offset_x in range(el_width_px_fine):
                    curr_x = x_px_fine_base + offset_x

                    if 0 <= z_px_fine < Nz_fine and 0 <= curr_x < Nx_fine:
                        zf = z_px_fine // factor
                        xf = curr_x // factor

                        field[st, zf, xf] += val_final

# ---------------------------------------------------------------------------
# k-Wave generation pipeline (fused GPU pipeline)
# ---------------------------------------------------------------------------
# Convention: k-Wave grid layout is (Nx, Nz, Nt) with time on the LAST axis,
# so that Hilbert/envelope and time resampling operate along the
# memory-contiguous last axis (fastest for rfft on both CPU and GPU).
# The final storage layout (Nt, Nz, Nx) is produced by to_pipeline_layout.
# ---------------------------------------------------------------------------

def sensor_data_to_grid(data, Nx, Nz, backend="python", xp=None):
    xp = _get_xp(xp)
    
    Ns = Nx * Nz
    if data.ndim == 2 and data.shape[1] == Ns and data.shape[0] != Ns:
        data = data.T
        
    data_array = xp.asarray(data, dtype=xp.float32)
    del data
    
    if backend in ["cpp", "cuda"]:
        out = data_array.reshape((Nz, Nx, -1)).transpose(1, 0, 2)
    else:
        out = data_array.reshape((Nx, Nz, -1))
        
    out = xp.ascontiguousarray(out)
    del data_array
    return out

def to_pipeline_layout(field, xp=None):
    """
    Convert a grid-layout field (Nx, Nz, Nt) to the pipeline/storage layout
    (Nt, Nz, Nx), C-contiguous.

    Args:
        field: array (Nx, Nz, Nt), time last.
        xp: array namespace (cupy or numpy). Defaults to cupy if available.

    Returns:
        array (Nt, Nz, Nx), C-contiguous.
    """
    xp = _get_xp(xp)
    return xp.ascontiguousarray(field.transpose(2, 1, 0))

def hilbert_transform(field, xp=None, show_log=False):
    """Compute the real Hilbert quadrature using one-sided FFTs.

    Parameters
    ----------
    field : array_like
        Real-valued input with time on the last axis.
    xp : module, optional
        NumPy or CuPy namespace.
    show_log : bool, optional
        Print FFT dimensions and temporary memory use.

    Returns
    -------
    ndarray
        Real-valued Hilbert transform, with the same shape as ``field``.

    Notes
    -----
    This implementation avoids constructing a full complex analytic spectrum.
    It modifies the one-sided FFT in place, then uses ``irfft`` to obtain the
    real quadrature component. This reduces peak memory compared with building
    a full complex spectrum and calling ``ifft``.
    """
    xp = _get_xp(xp)
    if field.ndim < 1:
        raise ValueError("field must have at least one dimension.")
    n_time = int(field.shape[-1])
    if n_time < 2:
        raise ValueError("Hilbert transform requires at least two time samples.")

    n_fft = next_fast_len(n_time, real=False)
    if show_log:
        print(
            f"[AOT-biomaps] Hilbert quadrature: shape={field.shape}, "
            f"Nt={n_time}, Nfft={n_fft}"
        )

    fft_module = scipy_fft if getattr(xp, "__name__", "numpy") == "numpy" else xp.fft
    spectrum = fft_module.rfft(field, n=n_fft, axis=-1)
    spectrum[..., 0] = 0
    if n_fft % 2 == 0:
        if spectrum.shape[-1] > 1:
            spectrum[..., 1:-1] *= -1j
        spectrum[..., -1] = 0
    else:
        spectrum[..., 1:] *= -1j

    quadrature = fft_module.irfft(spectrum, n=n_fft, axis=-1)
    del spectrum
    return quadrature[..., :n_time]


def hilbert_analytic(field, xp=None, show_log=False):
    """Return the analytic signal ``field + 1j * hilbert_transform(field)``.

    The input is not modified. The output precision follows the input precision:
    float32 inputs produce complex64, while float64 inputs produce complex128.
    """
    xp = _get_xp(xp)
    quadrature = hilbert_transform(field, xp=xp, show_log=show_log)
    complex_dtype = xp.complex64 if field.dtype.itemsize <= 4 else xp.complex128
    analytic = xp.empty(field.shape, dtype=complex_dtype)
    analytic.real = field
    analytic.imag = quadrature
    del quadrature
    return analytic


def calculate_envelope_squared(field, xp=None, chunk_size=None, in_place=True, show_log=False):
    """Compute the squared analytic envelope in spatial chunks.

    The time axis must be last. When ``in_place`` is true and the input is
    float32, the output overwrites the input. Chunk size is estimated from the
    currently available VRAM after the output storage has been selected.
    CuPy's memory pool and FFT plan cache are retained between chunks so that
    temporary allocations can be reused rather than repeatedly reallocated.

    Parameters
    ----------
    field : ndarray
        Real-valued array shaped ``(Nx, Nz, Nt)``.
    xp : module, optional
        NumPy or CuPy namespace.
    chunk_size : int, optional
        Number of x-slices per chunk. If omitted, estimated from available VRAM.
    in_place : bool, optional
        Overwrite a float32 input when true.
    show_log : bool, optional
        Print chunk and memory diagnostics.

    Returns
    -------
    ndarray
        Float32 squared envelope with the same shape as ``field``.
    """
    xp = _get_xp(xp)
    if field.ndim != 3:
        raise ValueError("field must have shape (Nx, Nz, Nt).")
    nx = int(field.shape[0])
    if nx <= 0:
        raise ValueError("The spatial x dimension must be non-empty.")

    use_in_place = bool(in_place and field.dtype == xp.float32)
    output = field if use_in_place else xp.empty(field.shape, dtype=xp.float32)

    if chunk_size is None:
        chunk_size = _get_dynamic_chunk_size(field.shape, ortho_axis=0, xp=xp, multiplier=8.0)
    chunk_size = max(1, min(int(chunk_size), nx))

    if show_log:
        n_chunks = (nx + chunk_size - 1) // chunk_size
        mode = "in-place" if use_in_place else "out-of-place"
        print(
            f"[AOT-biomaps] Squared envelope: shape={field.shape}, "
            f"{field.nbytes / 1e9:.3f} GB, {mode}, "
            f"{n_chunks} chunk(s) of {chunk_size} x-slices"
        )

    for start in range(0, nx, chunk_size):
        stop = min(start + chunk_size, nx)
        source_chunk = field[start:stop, ...]
        target_chunk = output[start:stop, ...]

        # Compute the quadrature before overwriting the input in in-place mode.
        quadrature = hilbert_transform(source_chunk, xp=xp, show_log=False)
        xp.multiply(source_chunk, source_chunk, out=target_chunk)
        xp.square(quadrature, out=quadrature)
        xp.add(target_chunk, quadrature, out=target_chunk)
        del quadrature

        if show_log and getattr(xp, "__name__", "numpy") == "cupy":
            info = get_gpu_memory_info(xp)
            print(
                f"[AOT-biomaps] Envelope chunk x[{start}:{stop}/{nx}] "
                f"| CUDA free={info['free_bytes'] / 1e9:.2f} GB "
                f"| pool used={info['pool_used_bytes'] / 1e9:.2f} GB"
            )

    return output


def calculate_envelope(field, xp=None, chunk_size=None, in_place=True, show_log=False):
    """Compute the analytic-signal envelope in place when possible."""
    xp = _get_xp(xp)
    envelope_squared = calculate_envelope_squared(
        field,
        xp=xp,
        chunk_size=chunk_size,
        in_place=in_place,
        show_log=show_log,
    )
    xp.sqrt(envelope_squared, out=envelope_squared)
    return envelope_squared


def resample_bandlimited(field, axis, M, xp=None, chunk_size=None):
    """
    Perform anti-aliased spectral resampling along one axis using rFFT.
    The one-sided spectrum is truncated or zero-padded to the target size and
    tapered near the cutoff to suppress Gibbs ringing. Processing is chunked
    along an orthogonal axis when required by available GPU memory.

    Args:
        field (ndarray): Real-valued array to resample (typically float32).
        axis (int): Axis along which to resample.
        M (int): Target length along axis. If M == field.shape[axis], field is returned unchanged.
        xp (module, optional): Array namespace (cupy or numpy). Defaults to CuPy if available, else NumPy.
        chunk_size (int, optional): Number of slices along the orthogonal chunking axis per iteration. If None, determined dynamically from available VRAM.

    Returns:
        ndarray: Resampled float32 array with shape[axis] == M.
    """
    xp = _get_xp(xp)
    N = field.shape[axis]
    if M == N:
        return field

    # Allocate output before estimating the temporary FFT chunk size.
    shape_out = list(field.shape)
    shape_out[axis] = M
    out = xp.empty(tuple(shape_out), dtype=xp.float32)

    ortho_axis = 1 if axis == 0 else 0
    N_ortho = field.shape[ortho_axis]

    # Both the input and output FFT plans may be active during resampling.
    if chunk_size is None:
        chunk_size = _get_dynamic_chunk_size(field.shape, ortho_axis, xp=xp, multiplier=16.0)
    chunk_size = max(1, min(chunk_size, N_ortho))

    # Build anti-aliasing raised-cosine taper along the frequency axis
    Mk = M // 2 + 1
    cut = min(N // 2 + 1, Mk)
    kc = min(N, M) / 2.0

    kb = xp.arange(cut, dtype=xp.float32)
    w = xp.where(kb <= 0.70 * kc, 1.0, xp.where(kb <= kc, 0.5 * (1.0 + xp.cos(xp.pi * (kb - 0.70 * kc) / (0.30 * kc))), 0.0))
    w = w.reshape([cut if ax == axis else 1 for ax in range(field.ndim)])
    del kb

    scale = xp.float32(M / N)

    fft_module = scipy_fft if getattr(xp, "__name__", "numpy") == "numpy" else xp.fft

    for i in range(0, N_ortho, chunk_size):
        end = min(i + chunk_size, N_ortho)

        sl_in = [slice(None)] * field.ndim
        sl_in[ortho_axis] = slice(i, end)

        E_chunk = fft_module.rfft(field[tuple(sl_in)], axis=axis)

        E2_shape = list(E_chunk.shape)
        E2_shape[axis] = Mk
        E2_chunk = xp.zeros(tuple(E2_shape), dtype=E_chunk.dtype)

        sl_cut = [slice(None)] * E_chunk.ndim
        sl_cut[axis] = slice(0, cut)
        E2_chunk[tuple(sl_cut)] = E_chunk[tuple(sl_cut)] * w
        del E_chunk

        out_chunk = fft_module.irfft(E2_chunk, n=M, axis=axis)
        del E2_chunk

        out_chunk *= scale
        out[tuple(sl_in)] = out_chunk
        del out_chunk

    del w
    return out

def resample_field(field, target_sizes, xp=None):
    """Resample an ``(Nx, Nz, Nt)`` field to target ``(Nt, Nz, Nx)`` sizes.

    The field is resampled in time, z, then x. The input grid layout remains
    ``(Nx, Nz, Nt)`` until :func:`to_pipeline_layout` is called.
    """
    xp = _get_xp(xp)
    if len(target_sizes) != 3:
        raise ValueError("target_sizes must be (Nt_target, Nz_target, Nx_target).")
    nt_target, nz_target, nx_target = (int(v) for v in target_sizes)
    field = resample_bandlimited(field, 2, nt_target, xp)
    field = resample_bandlimited(field, 1, nz_target, xp)
    field = resample_bandlimited(field, 0, nx_target, xp)
    return field

def compute_target_sizes(Nx, Nz, Nt, dx, dz, dt, target_dt, target_dx, target_dz):
    """Compute output dimensions and their effective sample spacings.

    Returns dimensions in pipeline order ``(Nt, Nz, Nx)`` and spacings in the
    matching order ``(dt, dz, dx)``.
    """
    if min(int(Nx), int(Nz), int(Nt)) <= 0:
        raise ValueError("Input grid dimensions must be positive.")
    if min(float(dx), float(dz), float(dt), float(target_dt), float(target_dx), float(target_dz)) <= 0:
        raise ValueError("All spatial and temporal sample spacings must be positive.")

    nt_target = max(2, int(np.floor(Nt * dt / target_dt + 1e-9)))
    nz_target = max(2, int(np.floor(Nz * dz / target_dz + 1e-9)))
    nx_target = max(2, int(np.floor(Nx * dx / target_dx + 1e-9)))
    dt_effective = (Nt * dt) / nt_target
    dz_effective = (Nz * dz) / nz_target
    dx_effective = (Nx * dx) / nx_target
    return (nt_target, nz_target, nx_target), (dt_effective, dz_effective, dx_effective)


def tukey_window(N, alpha=0.5):
    """
    Generate a Tukey window.
    Parameters:
        N (int): Number of points in the window.
        alpha (float): Shape parameter of the Tukey window. 0 <= alpha <= 1.
    Returns:
        numpy.ndarray: The Tukey window.
    """
    if N <= 1:
        return np.ones(N)
    if alpha <= 0:
        return np.ones(N)
    if alpha >= 1:
        return np.hanning(N)
    e = alpha * (N - 1) / 2.0
    n = np.arange(N)
    w = np.ones(N)
    left = n < e
    right = n > (N - 1 - e)
    if e > 0:
        w[left] = 0.5 * (1 + np.cos(np.pi * (e - n[left]) / e))
        w[right] = 0.5 * (1 + np.cos(np.pi * (n[right] - (N - 1 - e)) / e))
    return w