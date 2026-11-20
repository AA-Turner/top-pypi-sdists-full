from __future__ import annotations

"""
AOT-biomaps acoustic tools.

Consolidated module:
- MAT / IO helpers
- pattern & file-name utilities
- SIMPLE_SIM helpers (piezo-to-grid mapping + Numba kernel)
- k-Wave generation pipeline (fused GPU pipeline, formerly in kwave_gpu.py)

Removed (obsolete with the fused pipeline and the new parameter schema):
- reshape_field_cpu / reshape_field_gpu
    -> replaced by resample_bandlimited (spectral, anti-aliased)
- calculate_envelope_squared_cpu/gpu, calculate_envelope_cpu/gpu and the old
  calculate_envelope_squared / calculate_envelope wrappers with signature
  (field, isGPU, GPUdevice) -> replaced by time-last-axis GPU versions.

Layout conventions of the k-Wave pipeline:
- k-Wave grid layout:  (Nx, Nz, Nt)  -- time on the LAST axis
- pipeline/storage layout: (Nt, Nz, Nx)  -- time on the FIRST axis (after to_pipeline_layout)

Orchestration order (fused pipeline):
  sensor_data_to_grid -> calculate_envelope_squared (time last, full rate)
  -> compute_target_sizes -> resample_field (time -> z -> x) -> to_pipeline_layout
"""
import os
import gc
import numpy as np
from scipy.io import loadmat as scipy_loadmat
from scipy.stats import linregress
from numba import njit, prange
from scipy.fft import next_fast_len

# Optional cupy import for GPU acceleration
try:
    import cupy as cp
    CUPY_AVAILABLE = True
except ImportError:
    cp = None
    CUPY_AVAILABLE = False


def _get_xp(xp=None):
    """Return the array namespace to use: explicit argument, cupy if available, else numpy."""
    if xp is not None:
        return xp
    return cp if CUPY_AVAILABLE else np

def _get_dynamic_chunk_size(field_shape, ortho_axis, xp, multiplier=10.0):
    """
    Compute the optimal chunk size along ortho_axis based on available VRAM.
    Flushes the cuFFT plan cache and CuPy memory pool prior to querying device memory so the budget reflects truly available VRAM. If the full array fits within 80% of free memory (accounting for FFT temporary buffers via multiplier), returns the full axis length for single-pass processing.

    Args:
        field_shape (tuple[int, ...]): Shape of the input array.
        ortho_axis (int): Axis along which the array will be chunked.
        xp (module): Array namespace (cupy or numpy).
        multiplier (float, optional): Peak-memory safety factor relative to a float32 chunk to accommodate complex FFT intermediates and cuFFT work areas. Defaults to 10.0.

    Returns:
        int: Number of slices along ortho_axis to process per chunk,
        clamped to [1, field_shape[ortho_axis]].
    """
    N_ortho = field_shape[ortho_axis]

    # On CPU (NumPy), system RAM is typically large enough for a single pass
    if xp.__name__ != 'cupy':
        return N_ortho

    # Flush both cuFFT plan cache and CuPy pool for an accurate free VRAM reading
    _clear_gpu_memory(xp)
    free_mem, _ = xp.cuda.Device().mem_info

    # Memory footprint of a single slice along ortho_axis (float32 = 4 bytes)
    elements_per_slice = int(np.prod(field_shape)) // N_ortho
    bytes_per_slice = elements_per_slice * 4

    # Reserve 20% headroom for OS, driver overhead, and cuFFT internal buffers
    safe_mem = free_mem * 0.8

    if bytes_per_slice * N_ortho * multiplier < safe_mem:
        return N_ortho

    optimal_chunk = int(safe_mem / (bytes_per_slice * multiplier))
    return max(1, min(optimal_chunk, N_ortho))

def _clear_gpu_memory(xp):
    """
    Release cached cuFFT plans and free unused blocks in the CuPy memory pool.
    cuFFT plan work areas are allocated through CuPy's memory pool and remain pinned until the plan cache is cleared. Clearing the cache before calling free_all_blocks() ensures those blocks are actually returned to the device. No-op when xp is NumPy.

    Args:
        xp (module): Array namespace (cupy or numpy).
    """
    if xp.__name__ == 'cupy':
        xp.fft.config.get_plan_cache().clear()
        xp.get_default_memory_pool().free_all_blocks()

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
    """
    Compute the spatial-frequency bin index of a pattern from its file name.

    Args:
        fileName: File name containing the pattern (e.g. "field_<hex>_<angle>.hdr").
        num_elements: Number of elements in the probe.
        dx: Pixel size of the SIMULATION grid, in meters
            (params.acoustic['dx_sim'] with the new parameter schema).

    Returns:
        int: Spatial-frequency bin index (dimensionless, in units of 1/(N*dx)).
    """
    profile = hex_to_binary_profile(fileName[6:-4], num_elements)

    if set(fileName[6:-4].lower().replace(" ", "")) == {'f'}:
        fs_key = 0.0  # all-elements pattern -> zero spatial frequency
    else:
        ft_prof = np.fft.fft(profile)
        idx_max = np.argmax(np.abs(ft_prof[1:len(profile)//2])) + 1
        freqs = np.fft.fftfreq(len(profile), d=dx)

        # freqs is in m^-1 because dx is in meters
        fs_m_inv = abs(freqs[idx_max])

        fs_key = fs_m_inv  # Spatial frequency in m^-1
    return int(fs_key / (1/(len(profile)*dx)))

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
    """
    Calculate the next power of 2 greater than or equal to n.

    Args:
        n: Input integer.

    Returns:
        int: Next power of 2 >= n.
    """
    return int(2 ** np.ceil(np.log2(n)))

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
    mempool = xp.get_default_memory_pool() if xp.__name__ == 'cupy' else None
    
    Ns = Nx * Nz
    if data.ndim == 2 and data.shape[1] == Ns and data.shape[0] != Ns:
        data = data.T
        
    data_array = xp.asarray(data, dtype=xp.float32)
    del data
    gc.collect()
    
    if backend in ["cpp", "cuda"]:
        out = data_array.reshape((Nz, Nx, -1)).transpose(1, 0, 2)
    else:
        out = data_array.reshape((Nx, Nz, -1))
        
    out = xp.ascontiguousarray(out)
    del data_array
    if mempool:
        mempool.free_all_blocks()
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

def hilbert_analytic(field, xp=None, show_log=False):
    """
    Compute the analytic signal along the last axis (time) via Hilbert transform. Uses a real-to-complex forward FFT (rfft) padded to a 5-smooth length (next_fast_len(Nt, real=False)) followed by a complex inverse FFT (ifft).
    Mathematical definition:
        For a real signal :x[n], the analytic signal is defined in the frequency domain by keeping DC and Nyquist (if N_fft is even) unchanged, doubling strictly positive frequencies, and strictly zeroing all negative frequencies:

    Memory & performance notes:
        - Padding to next_fast_len(Nt, real=False) guarantees prime factors in {2, 3, 5}, preventing cuFFT from falling back to Bluestein's algorithm (which allocates large internal workspaces for prime factors > 7).
        - The returned slice analytic[..., :Nt] is a view into the padded buffer to avoid an extra copy; callers should consume and drop it promptly.
        - The input field is never modified or freed here.

    Args:
        field (ndarray): Real-valued array of shape (..., Nt) with time on the last axis.
        xp (module, optional): Array namespace (cupy or numpy). Defaults to CuPy if available, else NumPy.
        show_log (bool, optional): If True, log input/buffer shapes, FFT length, and memory footprint. Defaults to False.

    Returns:
        ndarray: Complex analytic signal of shape (..., Nt) (complex64 for float32 input on GPU; note that NumPy may promote to complex128 on CPU).
    """
    xp = _get_xp(xp)
    Nt = field.shape[-1]

    # real=False restricts prime factors to {2, 3, 5}, which are natively
    # accelerated by cuFFT without triggering Bluestein's workspace allocation
    N_fft = next_fast_len(Nt, real=False)

    if show_log:
        print(f"[Hilbert] input {field.shape} ({field.nbytes / 1e9:.3f} GB) | Nt={Nt} -> N_fft={N_fft}")

    # 1. Forward real FFT: computes only non-negative frequency bins (half memory)
    X_pos = xp.fft.rfft(field, n=N_fft, axis=-1)
    if show_log:
        print(f"[Hilbert] rfft done ({X_pos.nbytes / 1e9:.3f} GB, dtype={X_pos.dtype})")

    # Double strictly positive frequencies; leave DC (0) and Nyquist (-1 if even) at 1x
    if N_fft % 2 == 0:
        X_pos[..., 1:-1] *= 2.0
    else:
        X_pos[..., 1:] *= 2.0

    # 2. Build full analytic spectrum with negative frequencies strictly zeroed
    X_full = xp.zeros(field.shape[:-1] + (N_fft,), dtype=X_pos.dtype)
    X_full[..., :X_pos.shape[-1]] = X_pos
    del X_pos

    # 3. Inverse complex FFT and truncate back to original length Nt (view, no copy)
    analytic = xp.fft.ifft(X_full, axis=-1)
    if show_log:
        print(f"[Hilbert] ifft done ({analytic.nbytes / 1e9:.3f} GB)")
    del X_full

    if show_log and xp.__name__ != 'cupy' and field.dtype == np.float32:
        print("[Hilbert] WARNING (CPU): NumPy may promote float32 -> complex128, using 2x memory compared to the CuPy complex64 path.")

    return analytic[..., :Nt]

def calculate_envelope_squared(field, xp=None, chunk_size=None, in_place=True, show_log=False):
    """
    Compute the squared envelope :math: |x_a(t)|^2 via Hilbert transform, chunked along axis 0 (Nx).

    Memory management:
        - When in_place=True and field is float32, the squared envelope overwrites field chunk by chunk, avoiding a second full-size GPU allocation.
        - chunk_size is computed *after* any output allocation so VRAM estimation accounts for the output buffer.
        - CuPy pool blocks are freed after every chunk. If the final tail chunk has a different size from chunk_size, the cuFFT plan cache is flushed *before* that chunk so two differently sized plans never coexist in VRAM.
        - The cuFFT plan cache and memory pool are fully flushed upon return.

    Args:
        field (ndarray): Real-valued acoustic field of shape (Nx, Nz, Nt) with time on the last axis (typically float32).
        xp (module, optional): Array namespace (cupy or numpy). Defaults to CuPy if available, else NumPy.
        chunk_size (int, optional): Number of Nx slices per chunk. If None, determined dynamically from available VRAM.
        in_place (bool, optional): If True and field.dtype == float32, overwrite field in place to halve peak output VRAM. Defaults to True.
        show_log (bool, optional): If True, print chunk progress and GPU memory diagnostics. Defaults to False.

    Returns:
        ndarray: Squared envelope of shape (Nx, Nz, Nt), float32.
        Identical to field when in_place=True and input is float32.
    """
    xp = _get_xp(xp)
    is_gpu = (xp.__name__ == 'cupy')
    mempool = xp.get_default_memory_pool() if is_gpu else None

    Nx, _, _ = field.shape
    bytes_full = field.nbytes

    # Flush stale plans/blocks before output allocation and VRAM estimation
    _clear_gpu_memory(xp)

    # Allocate output before computing chunk_size so free VRAM reflects reality
    if in_place and field.dtype == xp.float32:
        out_env_sq = field
    else:
        out_env_sq = xp.empty_like(field, dtype=xp.float32)

    if chunk_size is None:
        chunk_size = _get_dynamic_chunk_size(field.shape, ortho_axis=0, xp=xp, multiplier=8.0)
    chunk_size = max(1, min(chunk_size, Nx))

    if show_log:
        n_chunks = (Nx + chunk_size - 1) // chunk_size
        mode = "in-place" if out_env_sq is field else "out-of-place"
        print(f"[Envelope^2] field {field.shape} ({bytes_full / 1e9:.2f} GB, {mode}) | {n_chunks} chunk(s) of {chunk_size} x-slices")

    for i in range(0, Nx, chunk_size):
        end = min(i + chunk_size, Nx)

        # Flush cached cuFFT plans before a smaller tail chunk so the main-chunk
        # plan and tail-chunk plan never coexist in VRAM
        if (end - i) != chunk_size:
            _clear_gpu_memory(xp)

        # Safe even when in_place=True: rfft reads field[i:end] into a new buffer
        # before out_env_sq[i:end] is written below
        analytic_chunk = hilbert_analytic(field[i:end, ...], xp, show_log=show_log)

        # Compute |x_a|^2 = Re(x_a)^2 + Im(x_a)^2 using a single float32 temporary
        env_sq = analytic_chunk.real ** 2
        env_sq += analytic_chunk.imag ** 2
        out_env_sq[i:end, ...] = env_sq
        del env_sq, analytic_chunk

        if mempool is not None:
            mempool.free_all_blocks()

        if show_log:
            msg = f"[Envelope^2] chunk x[{i}:{end}/{Nx}] done"
            if mempool is not None:
                device_free = xp.cuda.Device().mem_info[0]
                msg += (f" | pool used {mempool.used_bytes() / 1e9:.2f} GB / total {mempool.total_bytes() / 1e9:.2f} GB | device free {device_free / 1e9:.2f} GB")
            print(msg)

    # Final cleanup: drop all cuFFT plans first, then release pooled VRAM
    _clear_gpu_memory(xp)
    return out_env_sq


def calculate_envelope(
    field, xp=None, chunk_size=None, in_place=True, show_log=False
):
    """
    Compute the envelope :math:`|x_a(t)|` via Hilbert transform, chunked along axis 0 (Nx).
    Delegates to :func:`calculate_envelope_squared` and applies an in-place square root to avoid allocating an extra full-size buffer.

    Args:
        field (ndarray): Real-valued acoustic field of shape (Nx, Nz, Nt), float32.
        xp (module, optional): Array namespace (cupy or numpy). Defaults to CuPy if available, else NumPy.
        chunk_size (int, optional): Number of Nx slices per chunk. If None, determined dynamically from available VRAM.
        in_place (bool, optional): If True and field.dtype == float32, overwrite field in place. Defaults to True.
        show_log (bool, optional): If True, print progress and VRAM usage. Defaults to False.

    Returns:
        ndarray: Envelope of shape (Nx, Nz, Nt), float32.
    """
    xp = _get_xp(xp)
    env_sq = calculate_envelope_squared(field, xp=xp, chunk_size=chunk_size, in_place=in_place, show_log=show_log)
    xp.sqrt(env_sq, out=env_sq)
    _clear_gpu_memory(xp)
    return env_sq


def resample_bandlimited(field, axis, M, xp=None, chunk_size=None):
    """
    Perform anti-aliased spectral resampling along a single axis using rFFT.
    Truncates or zero-pads the one-sided spectrum to target size M with a raised-cosine taper over [0.70 * kc, kc] (where kc = min(N, M) / 2) to suppress Gibbs ringing. Processing is dynamically chunked along an orthogonal axis to fit within available GPU VRAM, and all cuFFT plans are cleared upon completion.

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
    is_gpu = (xp.__name__ == 'cupy')
    mempool = xp.get_default_memory_pool() if is_gpu else None

    N = field.shape[axis]
    if M == N:
        return field

    _clear_gpu_memory(xp)

    # Allocate output buffer before querying free VRAM for chunk sizing
    shape_out = list(field.shape)
    shape_out[axis] = M
    out = xp.empty(tuple(shape_out), dtype=xp.float32)

    ortho_axis = 1 if axis == 0 else 0
    N_ortho = field.shape[ortho_axis]

    # Higher multiplier than Hilbert because both N-point rfft and M-point irfft
    # plans coexist (and may require Bluestein workspaces if N or M is not smooth)
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

    for i in range(0, N_ortho, chunk_size):
        end = min(i + chunk_size, N_ortho)

        # Avoid keeping main-chunk and tail-chunk cuFFT plans alive simultaneously
        if (end - i) != chunk_size:
            _clear_gpu_memory(xp)

        sl_in = [slice(None)] * field.ndim
        sl_in[ortho_axis] = slice(i, end)

        E_chunk = xp.fft.rfft(field[tuple(sl_in)], axis=axis)

        E2_shape = list(E_chunk.shape)
        E2_shape[axis] = Mk
        E2_chunk = xp.zeros(tuple(E2_shape), dtype=E_chunk.dtype)

        sl_cut = [slice(None)] * E_chunk.ndim
        sl_cut[axis] = slice(0, cut)
        E2_chunk[tuple(sl_cut)] = E_chunk[tuple(sl_cut)] * w
        del E_chunk

        out_chunk = xp.fft.irfft(E2_chunk, n=M, axis=axis)
        del E2_chunk

        out_chunk *= scale
        out[tuple(sl_in)] = out_chunk
        del out_chunk

        if mempool is not None:
            mempool.free_all_blocks()

    del w
    _clear_gpu_memory(xp)
    return out

def resample_field(field, target_sizes, xp=None):
    xp = _get_xp(xp)
    
    Nt_t, Nz_t, Nx_t = target_sizes
    
    field = resample_bandlimited(field, 2, Nt_t, xp)
    field = resample_bandlimited(field, 1, Nz_t, xp)
    field = resample_bandlimited(field, 0, Nx_t, xp)
        
    return field

def compute_target_sizes(Nx, Nz, Nt, dx, dz, dt, target_dt, target_dx, target_dz):
    Nt_t = max(2, int(np.floor(Nt * dt / target_dt + 1e-9)))
    Nz_t = max(2, int(np.floor(Nz * dz / target_dz + 1e-9)))
    Nx_t = max(2, int(np.floor(Nx * dx / target_dx + 1e-9)))
    dt_p = (Nt * dt) / Nt_t
    dz_p = (Nz * dz) / Nz_t
    dx_p = (Nx * dx) / Nx_t
    return (Nt_t, Nz_t, Nx_t), (dt_p, dz_p, dx_p)

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