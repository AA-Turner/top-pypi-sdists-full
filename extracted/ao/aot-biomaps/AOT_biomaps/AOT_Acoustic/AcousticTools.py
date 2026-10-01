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
import numpy as np
from scipy.io import loadmat as scipy_loadmat
from scipy.stats import linregress
from numba import njit, prange

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

def sensor_data_to_grid(sensor_data, Nt, Nz, Nx, xp=None):
    """
    Normalize k-Wave sensor output to the grid layout (Nx, Nz, Nt), time last.

    The pure-Python k-Wave backend returns 'p' shaped (Nt, Nz, Nx), while the
    compiled C++/CUDA binaries apply an internal transpose and return
    (Nx, Nz, Nt). This function detects the layout from the reference sizes
    and always returns (Nx, Nz, Nt), C-contiguous.

    Args:
        sensor_data: dict with key 'p', or raw array from k-Wave.
        Nt, Nz, Nx: reference sizes (from medium.kgrid).
        xp: array namespace (cupy or numpy). Defaults to cupy if available.

    Returns:
        array (Nx, Nz, Nt) in namespace xp.
    """
    xp = _get_xp(xp)
    if isinstance(sensor_data, dict):
        sensor_data = sensor_data['p']
    arr = xp.asarray(sensor_data)
    if arr.ndim != 3:
        raise ValueError(f"[AOT-biomaps] Expected 3D sensor data, got ndim={arr.ndim}.")

    if (Nt, Nz, Nx) == (Nx, Nz, Nt):
        # Ambiguous (Nx == Nt): assume the backend already returned grid layout.
        return xp.ascontiguousarray(arr)

    if arr.shape == (Nt, Nz, Nx):
        # Python backend layout -> transpose to grid layout
        arr = arr.transpose(2, 1, 0)
    elif arr.shape != (Nx, Nz, Nt):
        raise ValueError(
            f"[AOT-biomaps] Sensor data shape {arr.shape} matches neither "
            f"(Nt, Nz, Nx)=({Nt}, {Nz}, {Nx}) nor (Nx, Nz, Nt)=({Nx}, {Nz}, {Nt})."
        )
    return xp.ascontiguousarray(arr)

def to_pipeline_layout(grid_field, xp=None):
    """
    Convert a grid-layout field (Nx, Nz, Nt) to the pipeline/storage layout
    (Nt, Nz, Nx), C-contiguous.

    Args:
        grid_field: array (Nx, Nz, Nt), time last.
        xp: array namespace (cupy or numpy). Defaults to cupy if available.

    Returns:
        array (Nt, Nz, Nx), C-contiguous.
    """
    xp = _get_xp(xp)
    return xp.ascontiguousarray(grid_field.transpose(2, 1, 0))

def hilbert_analytic(field, axis=-1, xp=None):
    """
    FFT-based Hilbert transform (analytic signal) along `axis`.

    Args:
        field: real input array.
        axis: axis of the time dimension (default: last axis).
        xp: array namespace (cupy or numpy). Defaults to cupy if available.

    Returns:
        complex analytic signal, same shape as input.
    """
    xp = _get_xp(xp)
    n = field.shape[axis]
    h = xp.zeros(n, dtype=xp.float32)
    if n % 2 == 0:
        h[0] = 1.0
        h[n // 2] = 1.0
        h[1:n // 2] = 2.0
    else:
        h[0] = 1.0
        h[1:(n + 1) // 2] = 2.0

    shape = [1] * field.ndim
    shape[axis] = n

    F = xp.fft.fft(xp.asarray(field, dtype=xp.float32), axis=axis)
    analytic = xp.fft.ifft(F * h.reshape(shape), axis=axis)
    return analytic

def calculate_envelope_squared(field, xp=None):
    """
    Squared envelope |s_a(t)|^2 of a grid-layout field (..., Nt), time last.

    New fused-pipeline signature: (field, xp=None). This replaces the old
    (field, isGPU, GPUdevice, chunk_size) time-first API.

    Args:
        field: array with time on the LAST axis (grid layout (Nx, Nz, Nt)).
        xp: array namespace (cupy or numpy). Defaults to cupy if available.

    Returns:
        float32 array, same shape as input.
    """
    xp = _get_xp(xp)
    analytic = hilbert_analytic(field, axis=-1, xp=xp)
    return (xp.abs(analytic) ** 2).astype(xp.float32)

def calculate_envelope(field, xp=None):
    """
    Envelope |s_a(t)| of a grid-layout field (..., Nt), time last.

    New fused-pipeline signature: (field, xp=None). This replaces the old
    (field, isGPU, GPUdevice, chunk_size) time-first API.

    Args:
        field: array with time on the LAST axis (grid layout (Nx, Nz, Nt)).
        xp: array namespace (cupy or numpy). Defaults to cupy if available.

    Returns:
        float32 array, same shape as input.
    """
    xp = _get_xp(xp)
    analytic = hilbert_analytic(field, axis=-1, xp=xp)
    return xp.abs(analytic).astype(xp.float32)

def resample_bandlimited(field, M, axis=-1, xp=None):
    """
    Band-limited resampling of `field` along `axis` from N to M samples.

    Pipeline: rfft -> raised-cosine anti-alias window rolling off between
    0.7*kc and kc (kc = new Nyquist bin) -> irfft(n=M) -> in-place amplitude
    correction `*= float32(M/N)`.

    The amplitude correction is essential: irfft(n=M) normalizes by M while
    the rfft bins were normalized by N, so without it a decimation M < N
    would inflate the amplitudes by N/M (this was the old bug).

    Args:
        field: input array (real, time/space on `axis`).
        M: target number of samples on `axis` (M < N decimates, M > N upsamples).
        axis: axis to resample (default: last axis = time in grid layout).
        xp: array namespace (cupy or numpy). Defaults to cupy if available.

    Returns:
        array with `axis` resampled to M samples.
    """
    xp = _get_xp(xp)
    N = field.shape[axis]
    if M == N:
        return field
    if M < 1:
        raise ValueError(f"[AOT-biomaps] Target size M must be >= 1, got {M}.")

    F = xp.fft.rfft(field, axis=axis)

    if M < N:
        # Raised-cosine anti-alias window: passband up to 0.7*kc,
        # cosine rolloff from 0.7*kc down to 0 at kc (new Nyquist bin).
        kc = M // 2
        k = xp.arange(F.shape[axis], dtype=xp.float32)
        f1 = 0.7 * kc
        f2 = float(kc)
        ramp = (k - f1) / max(f2 - f1, 1e-12)
        w = 0.5 * (1.0 + xp.cos(xp.pi * xp.clip(ramp, 0.0, 1.0)))

        shape = [1] * field.ndim
        shape[axis] = F.shape[axis]
        F = F * w.reshape(shape)

    # irfft(n=M) truncates (M < N) or zero-pads (M > N) the spectrum.
    out = xp.fft.irfft(F, n=M, axis=axis)

    # In-place amplitude correction: irfft(n=M) divides by M, the rfft bins
    # carry the N normalization -> multiply by M/N to restore true amplitudes.
    out *= xp.float32(M / N)
    return out

def resample_field(field, target_sizes, xp=None):
    """
    Band-limited resampling of a grid-layout field (Nx, Nz, Nt) to the save
    grid. Decimation order: time (axis 2) -> z (axis 1) -> x (axis 0).

    Time is resampled via the anti-aliased spectral path, which is why the
    envelope must be computed BEFORE this call (full-rate Hilbert).

    Args:
        field: grid-layout array (Nx, Nz, Nt), time last.
        target_sizes: (M_t, M_z, M_x). None on an axis = keep it unchanged.
        xp: array namespace (cupy or numpy). Defaults to cupy if available.

    Returns:
        array (M_x, M_z, M_t) grid layout, resampled.
    """
    xp = _get_xp(xp)
    M_t, M_z, M_x = target_sizes
    if M_t is not None:
        field = resample_bandlimited(field, int(M_t), axis=2, xp=xp)
    if M_z is not None:
        field = resample_bandlimited(field, int(M_z), axis=1, xp=xp)
    if M_x is not None:
        field = resample_bandlimited(field, int(M_x), axis=0, xp=xp)
    return field

def compute_target_sizes(shape, targets):
    """
    Compute effective output sizes for the resampling pipeline.

    Args:
        shape: current per-axis sizes (axis order is free, as long as it is
               consistent between shape and targets).
        targets: desired per-axis sizes. None on an axis = no decimation on
                 that axis (the axis is kept at its current size).

    Returns:
        tuple: effective sizes, each clamped to [1, N] per axis.
    """
    result = []
    for N, M in zip(shape, targets):
        if M is None:
            result.append(int(N))
        else:
            result.append(int(min(max(int(M), 1), int(N))))
    return tuple(result)