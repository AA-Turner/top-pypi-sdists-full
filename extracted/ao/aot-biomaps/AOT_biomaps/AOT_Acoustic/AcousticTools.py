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
    Calculates the optimal chunk size based on available GPU VRAM.
    If the GPU has enough memory, it returns the full dimension (processes all at once).

    Args:
        field_shape (tuple): Shape of the input field.
        ortho_axis (int): The axis along which the field will be chunked.
        xp (module): Array namespace (cupy or numpy).
        multiplier (float): Safety factor for peak memory usage during FFT operations.

    Returns:
        int: The optimal chunk size.
    """
    N_ortho = field_shape[ortho_axis]
    
    # If using CPU (numpy), RAM is usually large enough, process everything at once
    if xp.__name__ != 'cupy':
        return N_ortho

    # Clear cached memory to get an accurate reading of available VRAM
    mempool = xp.get_default_memory_pool()
    mempool.free_all_blocks()

    # Get free and total memory in bytes
    free_mem, total_mem = xp.cuda.Device().mem_info
    
    # Calculate how many bytes a single slice along the ortho_axis requires (float32 = 4 bytes)
    elements_per_slice = np.prod(field_shape) / N_ortho
    bytes_per_slice = elements_per_slice * 4 

    # We use 80% of free memory to leave a safe margin for OS and other background tasks
    safe_mem = free_mem * 0.8
    
    # If the entire array fits safely, do it in one single pass
    if bytes_per_slice * N_ortho * multiplier < safe_mem:
        return N_ortho

    # Otherwise, calculate how many slices can fit in the safe VRAM budget
    optimal_chunk = int(safe_mem / (bytes_per_slice * multiplier))
    
    # Ensure chunk is at least 1, and at most the full size
    return max(1, min(optimal_chunk, N_ortho))

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

def hilbert_analytic(field, xp=None):

    xp = _get_xp(xp)
    Nt = field.shape[-1]
    
    h = xp.zeros((1, 1, Nt), dtype=xp.float32)
    h[..., 0] = 1.0
    if Nt % 2 == 0:
        h[..., Nt // 2] = 1.0
        h[..., 1:Nt // 2] = 2.0
    else:
        h[..., 1:(Nt + 1) // 2] = 2.0
        
    f_fft = xp.fft.fft(field, axis=-1)
    f_fft *= h
    del h
    
    analytic = xp.fft.ifft(f_fft, axis=-1)
    del f_fft
    return analytic

def calculate_envelope_squared(field, xp=None, chunk_size=None):
    """
    Computes the squared envelope. Dynamically adapts to VRAM.
    """
    xp = _get_xp(xp)
    mempool = xp.get_default_memory_pool() if xp.__name__ == 'cupy' else None
    
    Nx = field.shape[0]
    
    # Dynamically determine the best chunk size based on available VRAM
    if chunk_size is None:
        chunk_size = _get_dynamic_chunk_size(field.shape, ortho_axis=0, xp=xp, multiplier=10.0)
    
    out_env_sq = xp.empty_like(field, dtype=xp.float32)
    
    for i in range(0, Nx, chunk_size):
        end = min(i + chunk_size, Nx)
        field_chunk = field[i:end, ...]
        
        analytic_chunk = hilbert_analytic(field_chunk, xp)
        out_env_sq[i:end, ...] = (analytic_chunk.real ** 2 + analytic_chunk.imag ** 2).astype(xp.float32)
        
        del field_chunk, analytic_chunk
        if mempool:
            mempool.free_all_blocks()
            
    del field
    if mempool:
        mempool.free_all_blocks()
            
    return out_env_sq

def calculate_envelope(field, xp=None, chunk_size=None):
    xp = _get_xp(xp)
    mempool = xp.get_default_memory_pool() if xp.__name__ == 'cupy' else None
    
    env_sq = calculate_envelope_squared(field, xp, chunk_size=chunk_size)
    env = xp.sqrt(env_sq)
    
    del env_sq
    if mempool:
        mempool.free_all_blocks()
        
    return env

def resample_bandlimited(field, axis, M, xp=None, chunk_size=None):
    """
    Band-limited resampling. Dynamically adapts to VRAM to process in one pass 
    if memory allows, or falls back to chunks if tight on memory.
    """
    xp = _get_xp(xp)
    mempool = xp.get_default_memory_pool() if xp.__name__ == 'cupy' else None
    
    N = field.shape[axis]
    if M == N:
        return field
        
    shape_out = list(field.shape)
    shape_out[axis] = M
    out = xp.empty(tuple(shape_out), dtype=xp.float32)
    
    ortho_axis = 1 if axis == 0 else 0
    N_ortho = field.shape[ortho_axis]
    
    # Calculate optimal chunk size (Needs a slightly higher multiplier for resample)
    if chunk_size is None:
        chunk_size = _get_dynamic_chunk_size(field.shape, ortho_axis, xp=xp, multiplier=12.0)
    
    Mk = M // 2 + 1                   
    cut = min(N // 2 + 1, Mk)                  
    kc = min(N, M) / 2.0              

    kb = xp.arange(cut, dtype=xp.float32)
    w = xp.where(kb <= 0.70 * kc, 1.0,
                 xp.where(kb <= kc,
                          0.5 * (1 + xp.cos(xp.pi * (kb - 0.70 * kc) / (0.30 * kc))),
                          0.0))
    w_shape = [cut if ax == axis else 1 for ax in range(field.ndim)]
    w = w.reshape(w_shape)
    del kb

    for i in range(0, N_ortho, chunk_size):
        end = min(i + chunk_size, N_ortho)
        
        sl_in = [slice(None)] * field.ndim
        sl_in[ortho_axis] = slice(i, end)
        
        chunk = field[tuple(sl_in)]
        
        E_chunk = xp.fft.rfft(chunk, axis=axis)
        del chunk
        
        E2_shape = list(E_chunk.shape)
        E2_shape[axis] = Mk
        E2_chunk = xp.zeros(tuple(E2_shape), dtype=E_chunk.dtype)
        
        sl_cut = [slice(None)] * E_chunk.ndim
        sl_cut[axis] = slice(0, cut)
        E2_chunk[tuple(sl_cut)] = E_chunk[tuple(sl_cut)] * w
        del E_chunk
        
        out_chunk = xp.fft.irfft(E2_chunk, n=M, axis=axis)
        del E2_chunk
        
        out_chunk *= xp.float32(M / N)
        
        out[tuple(sl_in)] = out_chunk
        del out_chunk
        
        if mempool:
            mempool.free_all_blocks()

    del w
    del field
    if mempool:
        mempool.free_all_blocks()
        
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