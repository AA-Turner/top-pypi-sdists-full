"""
ReconTools.py

Unified reconstruction tools for AOT-BioMaps.
All operations (forward_projection, backward_projection, vector ops, potentials) implemented as standalone functions.
Works with any SMatrix type (CSR, SELL, DENSE) and any device (CPU, GPU).

For GPU: Uses CUDA kernels from AOT_biomaps_kernels.cu when available.
For CPU: Uses NumPy operations.
"""

import os
import numpy as np
from scipy.signal.windows import hann
import warnings
from tqdm import trange


# Optional cupy imports for GPU acceleration
try:
    import cupy as cp
    from cupyx.scipy.ndimage import map_coordinates
    CUPY_AVAILABLE = True
except ImportError:
    CUPY_AVAILABLE = False

from AOT_biomaps.AOT_Recon.ReconEnums import PotentialShapeType, PotentialType, PreconditionerType, StopCriterionType

# =============================================================================
# BASIC ARRAY OPERATIONS
# =============================================================================

def clamp_positive(SMatrix, x):
    """Clamp array values to be non-negative. Uses CUDA kernel when available."""   
    xp = get_array_module(SMatrix)
    return xp.maximum(x, 0.0)

# =============================================================================
# MATRIX-VECTOR OPERATIONS (delegated to SMatrix implementation)
# These use the CUDA kernels from SMatrix classes
# =============================================================================

def forward_projection(SMatrix, theta):
    """Forward projection: q = A * theta. Uses SMatrix.forward_projection() which calls CUDA kernels."""
    return SMatrix.forward_projection(theta)

def backward_projection(SMatrix, e):
    """Backprojection: c = A^T * e. Uses SMatrix.backward_projection() which calls CUDA kernels."""
    return SMatrix.backward_projection(e)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def mse(SMatrix, lambda_true, lambda_pred):
    """
    Calculate the Mean Squared Error (MSE) between two arrays.
    Equivalent to sklearn.metrics.mean_squared_error.
    """
    xp = get_array_module(SMatrix) if SMatrix is not None else np

    lambda_true = xp.asarray(lambda_true)
    lambda_pred = xp.asarray(lambda_pred)
    return xp.mean((lambda_true - lambda_pred) ** 2)



# =============================================================================
# ALGORITHM FUNCTIONS
# =============================================================================

def calculate_step_size_reg(SMatrix, gamma, num_subsets, num_iters, show_logs):
    """
    Calculate step sizes tau and sigma for PDHG when alpha or sigma is "auto" in the regularized case.
    Args:
        - SMatrix: The system matrix, used to estimate the Lipschitz constant.
        - gamma: Regularization parameter
        - num_subsets: Number of subsets used in the algorithm (affects the effective Lipschitz constant)
        - num_iters: Number of iterations to use for the power method estimation of the Lipschitz constant
        - show_logs: If True, prints the estimated Lipschitz constant and chosen step sizes
    """
    L_estimate = estimate_operator_norm(SMatrix, num_iters=num_iters)
    L_grad = 8.0  # L_grad = 8.0 is the exact squared operator norm of the 2D finite difference matrix
    L_total = (L_estimate**2) + L_grad
    # Calculate Chambolle-Pock step sizes
    tau_val = float(0.99 / (np.sqrt(L_total) * gamma))
    sigma_q_val = float((0.99 * gamma / np.sqrt(L_total)) * num_subsets)
    sigma_p_val = float(0.99 * gamma / np.sqrt(L_total))
    if show_logs:
        print(f"Estimated Lipschitz: {L_estimate:.2e} | tau: {tau_val:.2e} | sigma_q: {sigma_q_val:.2e} | sigma_p: {sigma_p_val:.2e}")
        
    return tau_val, sigma_q_val, sigma_p_val

def calculate_step_size(SMatrix, eta, num_iters, show_logs):
    """
    Calculate the step size for the optimization algorithm if alpha is "auto".
    Args :
        SMatrix: The system matrix, used to estimate the Lipschitz constant.
        eta: Parameter for the step size calculation when alpha is "auto". Must be > 1 for convergence and < 2 for optimal convergence.
        num_iters: Number of iterations to use for the power method estimation of the Lipschitz constant
        show_logs: If True, prints the estimated Lipschitz constant and chosen alpha.
    """
    if eta is None:
        print("Warning: eta not set. Defaulting to 1.9.")
        eta = 1.9
    if not (1.0 < eta < 2.0):
        print(f"Warning: eta={eta} is outside (1.0, 2.0). Convergence might be suboptimal.")
    L_estimate = estimate_operator_norm(SMatrix, num_iters=num_iters)
    alpha = eta / (L_estimate**2) if L_estimate > 0 else 1.0
    if show_logs:
        print(f"Estimated Lipschitz constant: {L_estimate:.2e}, using step size alpha: {alpha:.2e}")
    return alpha

def estimate_operator_norm(SMatrix, num_iters: int = 15) -> float:
    """
    Estimate the spectral norm (largest singular value) of the forward operator A using power iteration.
     - SMatrix: The system matrix with forward_projection and backward_projection methods.
     - num_iters: Number of power iterations to perform (default 15).
    """
    xp = get_array_module(SMatrix)

    v = xp.random.rand(SMatrix.Z * SMatrix.X).astype(xp.float32)
    v /= xp.linalg.norm(v) + 1e-12

    eig = 0.0

    for _ in range(num_iters):
        Av = forward_projection(SMatrix, v)
        AtAv = backward_projection(SMatrix, Av)

        eig = float(xp.vdot(v, AtAv))

        norm = xp.linalg.norm(AtAv)
        if norm > 1e-12:
            v = AtAv / norm

    return float(xp.sqrt(eig))

# =============================================================================
# POTENTIAL FUNCTIONS
# =============================================================================

# =====================================================================
# GPU KERNELS (CuPy) - Zero Allocation & Gather Paradigm
# =====================================================================

if CUPY_AVAILABLE:
    mrf_potential_kernel = cp.ElementwiseKernel(
        'int32 Z, int32 X, raw float32 U, raw int32 dz, raw int32 dx, raw float32 w, int32 num_neighbors, float32 beta, float32 delta, bool is_huber, int32 hessian_mode',
        'float32 grad_out, float32 hess_out, float32 energy_out',
        '''
        int z = i / X;
        int x = i % X;
        float u_i = U[i];
        
        float g = 0.0f;
        float h = 0.0f;
        float e = 0.0f;
        
        for(int k = 0; k < num_neighbors; ++k) {
            int nz = z + dz[k];
            int nx = x + dx[k];
            
            if (nz >= 0 && nz < Z && nx >= 0 && nx < X) {
                float u_j = U[nz * X + nx];
                float diff = u_i - u_j;
                float abs_diff = abs(diff);
                float weight = w[k];
                
                if (is_huber) {
                    if (abs_diff <= delta) {
                        // Quadratic Region
                        g += beta * weight * diff;
                        h += beta * weight;
                        e += 0.5f * beta * weight * diff * diff;
                    } else {
                        // Linear Region (Edges)
                        g += beta * weight * delta * (diff > 0.0f ? 1.0f : -1.0f);
                        if (hessian_mode == 1) {
                            h += beta * weight * delta / abs_diff; // De Pierro Surrogate (phi'/t)
                        } else {
                            h += 0.0f; // Exact Hessian phi''(t)
                        }
                        e += beta * weight * delta * (abs_diff - 0.5f * delta);
                    }
                } else { 
                    // Strictly Quadratic
                    g += beta * weight * diff;
                    h += beta * weight;
                    e += 0.5f * beta * weight * diff * diff;
                }
            }
        }
        grad_out = g;
        hess_out = h;
        energy_out = e;
        ''',
        'fused_mrf_potential_kernel'
    )

    # Dedicated kernel for Relative Difference Prior (RDP)
    rdp_potential_kernel = cp.ElementwiseKernel(
        'int32 Z, int32 X, raw float32 U, raw int32 dz, raw int32 dx, raw float32 w, int32 num_neighbors, float32 beta, float32 delta, int32 hessian_mode',
        'float32 grad_out, float32 hess_out, float32 energy_out',
        '''
        int z = i / X;
        int x = i % X;
        float u_i = U[i];
        float eps = 1e-8f;
        
        float g = 0.0f;
        float h = 0.0f;
        float e = 0.0f;
        
        for(int k = 0; k < num_neighbors; ++k) {
            int nz = z + dz[k];
            int nx = x + dx[k];
            
            if (nz >= 0 && nz < Z && nx >= 0 && nx < X) {
                float u_j = U[nz * X + nx];
                float diff = u_i - u_j;
                float abs_diff = abs(diff);
                float sum_ij = u_i + u_j;
                float weight = w[k];
                
                float denom = sum_ij + delta * abs_diff + eps;
                float denom_sq = denom * denom;
                
                float sign_diff = diff > 0.0f ? 1.0f : (diff < 0.0f ? -1.0f : 0.0f);
                float d_denom = 1.0f + delta * sign_diff;
                
                g += beta * weight * (2.0f * diff * denom - (diff * diff) * d_denom) / denom_sq;
                
                // The exact Hessian of RDP is non-convex. We use the standard 
                // pragmatic approximation 2.0 / denom to guarantee stability.
                h += beta * weight * 2.0f / denom;
                
                e += beta * weight * (diff * diff) / denom;
            }
        }
        grad_out = g;
        hess_out = h;
        energy_out = e;
        ''',
        'fused_rdp_potential_kernel'
    )

_OFFSET_CACHE = {}

def build_full_neighborhood_offsets(SMatrix, shape=PotentialShapeType.CROSS, radius=1):
    """Generates the FULL neighborhood (Gather) and caches it."""
    xp = get_array_module(SMatrix)
    if shape not in [PotentialShapeType.CROSS, PotentialShapeType.SQUARE, PotentialShapeType.CIRCLE]:
        raise ValueError(f"Unsupported neighborhood shape: {shape}")

    offsets_dz, offsets_dx, weights = [], [], []
    total_weight = 0.0
    
    for dz in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            if dz == 0 and dx == 0:
                continue
                
            dist_l2 = np.sqrt(dz**2 + dx**2)
            dist_l1 = abs(dz) + abs(dx)
            dist_linf = max(abs(dz), abs(dx))
            
            is_valid = False
            if shape == PotentialShapeType.CROSS: is_valid = (dist_l1 <= radius)
            elif shape == PotentialShapeType.SQUARE: is_valid = (dist_linf <= radius)
            elif shape == PotentialShapeType.CIRCLE: is_valid = (dist_l2 <= radius + 1e-5)

            if is_valid:
                weight = 1.0 / dist_l2
                offsets_dz.append(dz)
                offsets_dx.append(dx)
                weights.append(weight)
                total_weight += weight
                
    normalization_factor = 4.0 / (total_weight + 1e-10)
    weights = [w * normalization_factor for w in weights]
    
    return xp.array(offsets_dz, dtype=xp.int32), xp.array(offsets_dx, dtype=xp.int32), xp.array(weights, dtype=xp.float32)

def get_potential_function(
    potential_type: PotentialType, 
    SMatrix, 
    U, 
    beta: float, 
    shape: PotentialShapeType, 
    radius: int, 
    delta: float = 1.0, 
    compute_grad: bool = True, 
    compute_hess: bool = True, 
    compute_energy: bool = True,
    use_surrogate_hessian: bool = False
):
    """
    Compute the potential function value, gradient, and Hessian for a given image U based on the specified potential type and neighborhood.
    Supports GPU acceleration with zero allocations using custom CUDA kernels when available, and falls back to CPU implementation when not.
    
    Args:
    - potential_type: Type of potential function to compute (e.g., QUADRATIC, HUBER, RELATIVE_DIFFERENCE).
    - SMatrix: The system matrix, used to determine the array module (NumPy or CuPy) and dimensions.
    - U: The input image (flattened) for which to compute the potential, gradient and Hessian.
    - beta: Regularization strength parameter.
    - shape: The shape of the neighborhood (CROSS, SQUARE, CIRCLE). 
    - radius: The radius of the neighborhood.
    - delta: The threshold parameter for Huber and Relative Difference potentials.
    - compute_grad: Whether to compute and return the gradient.
    - compute_hess: Whether to compute and return the Hessian.
    - compute_energy: Whether to compute and return the potential energy value.
    - use_surrogate_hessian: For Huber potential, whether to use the De Pierro surrogate (phi'/t) for the Hessian in the linear region instead of the exact phi''(t). This can improve convergence speed at the cost of not being the true Hessian.
    """
    
    xp = get_array_module(SMatrix)
    
    if potential_type == PotentialType.NONE:
        return (xp.zeros_like(U) if compute_grad else None, xp.zeros_like(U) if compute_hess else None, 0.0 if compute_energy else None)
    
    Z, X = SMatrix.Z, SMatrix.X
    is_gpu = (xp.__name__ == 'cupy')
    hessian_mode = 1 if use_surrogate_hessian else 0
    
    # Offset Cache Management
    cache_key = (shape, radius, xp.__name__)
    if cache_key not in _OFFSET_CACHE:
        _OFFSET_CACHE[cache_key] = build_full_neighborhood_offsets(SMatrix, shape, radius)
    dz_arr, dx_arr, w_arr = _OFFSET_CACHE[cache_key]

    # GPU Execution (Zero Allocation)
    if is_gpu:
        grad_out = xp.empty_like(U, dtype=xp.float32)
        hess_out = xp.empty_like(U, dtype=xp.float32)
        energy_out = xp.empty_like(U, dtype=xp.float32) if compute_energy else grad_out # Dummy buffer if false
        
        if potential_type in [PotentialType.QUADRATIC, PotentialType.HUBER]:
            mrf_potential_kernel(
                Z, X, U, dz_arr, dx_arr, w_arr, len(dz_arr), 
                beta, delta, potential_type == PotentialType.HUBER, hessian_mode,
                grad_out, hess_out, energy_out
            )
        elif potential_type == PotentialType.RELATIVE_DIFFERENCE:
            rdp_potential_kernel(
                Z, X, U, dz_arr, dx_arr, w_arr, len(dz_arr), 
                beta, delta, hessian_mode,
                grad_out, hess_out, energy_out
            )
        else:
            raise ValueError(f"Unsupported potential: {potential_type}")

        # The loop traverses the full neighborhood, each edge is counted twice (A->B and B->A)
        U_value = float(xp.sum(energy_out) / 2.0) if compute_energy else 0.0
        
        return (
            grad_out if compute_grad else None,
            hess_out if compute_hess else None,
            U_value
        )
    
    # CPU Fallback (Numpy)
    else:
        # For CPU, we loop over the full neighborhood.
        # This is not optimized for RAM, but it guarantees strictly identical results.
        U_img = U.reshape(Z, X)
        grad_img = xp.zeros_like(U_img, dtype=xp.float32) if compute_grad else None
        grad_img = xp.zeros_like(U_img) if compute_grad else None
        hess_img = xp.zeros_like(U_img) if compute_hess else None
        U_value = 0.0
        
        for k in range(len(dz_arr)):
            dz, dx, w = int(dz_arr[k]), int(dx_arr[k]), float(w_arr[k])
            
            slice_c_z = slice(max(0, -dz), min(Z, Z - dz))
            slice_n_z = slice(max(0, dz), min(Z, Z + dz))
            slice_c_x = slice(max(0, -dx), min(X, X - dx))
            slice_n_x = slice(max(0, dx), min(X, X + dx))
            
            u_i = U_img[slice_c_z, slice_c_x]
            u_j = U_img[slice_n_z, slice_n_x]
            diff = u_i - u_j
            
            if potential_type == PotentialType.QUADRATIC:
                g = beta * w * diff
                h = beta * w
                e = 0.5 * beta * w * diff**2
                
            elif potential_type == PotentialType.HUBER:
                abs_diff = xp.abs(diff)
                mask_quad = abs_diff <= delta
                mask_lin = ~mask_quad
                
                g = xp.zeros_like(diff)
                g[mask_quad] = beta * w * diff[mask_quad]
                g[mask_lin] = beta * w * delta * xp.sign(diff[mask_lin])
                
                h = xp.zeros_like(diff)
                h[mask_quad] = beta * w
                if hessian_mode == 1:
                    h[mask_lin] = beta * w * delta / (abs_diff[mask_lin] + 1e-8)
                    
                e = xp.zeros_like(diff)
                e[mask_quad] = 0.5 * beta * w * diff[mask_quad]**2
                e[mask_lin] = beta * w * delta * (abs_diff[mask_lin] - 0.5 * delta)
                
            elif potential_type == PotentialType.RELATIVE_DIFFERENCE:
                denom = u_i + u_j + delta * xp.abs(diff) + 1e-8
                d_denom = 1.0 + delta * xp.sign(diff)
                g = beta * w * (2.0 * diff * denom - (diff**2) * d_denom) / (denom**2)
                h = beta * w * 2.0 / denom
                e = beta * w * (diff**2) / denom

            if compute_grad: grad_img[slice_c_z, slice_c_x] += g
            if compute_hess: hess_img[slice_c_z, slice_c_x] += h
            if compute_energy: U_value += float(xp.sum(e))

        if compute_energy: U_value /= 2.0
        return (grad_img.flatten() if compute_grad else None, 
                hess_img.flatten() if compute_hess else None, 
                U_value)
    
# =============================================================================
# STOPPING CRITERIA
# =============================================================================

def check_stopping_criterion(SMatrix, current_lambda, prev_lambda, criterion_type, threshold, window_size, history=None, ground_truth=None, gradient=None, window_history=None):
    """
    Evaluates stopping criteria by calculating the average relative variation (stagnation) 
    of the chosen metric over a sliding window. The returned value strictly converges to 0.
    """
    xp = get_array_module(SMatrix)

    # Initialize window_history if not provided
    if window_history is None:
        window_history = []

    if criterion_type == StopCriterionType.MAX_ITERATIONS:
        return False, 0.0

    raw_metric = 0.0

    # 1. Extract raw metric (Cast to standard float to avoid polluting RAM with GPU pointers)
    if criterion_type == StopCriterionType.RELATIVE_CHANGE:
        # RELATIVE_CHANGE is by definition an image variation
        raw_metric = float(xp.linalg.norm(current_lambda - prev_lambda) / (xp.linalg.norm(current_lambda) + 1e-10))
        
    elif criterion_type == StopCriterionType.COST_FUNCTION:
        if not history: return False, 0.0
        raw_metric = float(history[-1])
        
    elif criterion_type == StopCriterionType.MSE:
        if ground_truth is None:
            raise ValueError("Ground truth image required for MSE stopping criterion.")
        # Assuming mse() returns a scalar
        raw_metric = float(mse(SMatrix, ground_truth, current_lambda))
        
    elif criterion_type == StopCriterionType.GRADIENT_NORM:
        if gradient is None:
            raise ValueError("Gradient stop criterion is not supported with this optimizer.")
        raw_metric = float(xp.linalg.norm(gradient))
        
    else:
        raise ValueError(f"Unsupported stopping criterion type: {criterion_type}")

    # 2. Sliding window management
    window_history.append(raw_metric)
    
    # Keep 'window_size + 1' elements to compute 'window_size' consecutive differences
    if len(window_history) > window_size + 1:
        window_history.pop(0)

    # If there is not enough history to compute a difference
    if len(window_history) < 2:
        return False, 0.0

    # 3. Compute Average Stagnation (which will converge to 0)
    if criterion_type in [StopCriterionType.RELATIVE_CHANGE, StopCriterionType.GRADIENT_NORM]:
        # These metrics ALREADY evaluate a quantity tending to 0 by mathematical nature
        avg_diff = sum(window_history[1:]) / window_size
    else:
        # For COST_FUNCTION and MSE, compute the average relative variation between iterations
        diffs = [
            abs(window_history[i] - window_history[i-1]) / (abs(window_history[i-1]) + 1e-10) 
            for i in range(1, len(window_history))
        ]
        avg_diff = sum(diffs) / len(diffs)

    return bool(avg_diff < threshold), avg_diff    

# =============================================================================
# GRADIENT AND DIVERGENCE OPERATIONS (for TV regularization)
# =============================================================================

def gradient_2d(SMatrix, x):
    """
    Compute the 2D spatial forward gradient of a flattened image vector.
    Gradients are calculated using forward differences.
    
    Args:
        SMatrix: SMatrix instance (for dimension and device abstraction)
        x: Flattened 1D image array of shape (Z*X,)
        
    Returns:
        tuple: (grad_x, grad_z) where each component is a flattened 1D array of shape (Z*X,)
    """
    xp = get_array_module(SMatrix)
    Z = SMatrix.Z
    X = SMatrix.X
    
    # Reshape into standard 2D space to apply spatial stencils safely
    x_img = x.reshape(Z, X)
    
    # FORCED FLOAT32: Prevent silent float64 upcasting from external scalar math
    grad_x_img = xp.zeros_like(x_img, dtype=xp.float32)
    grad_z_img = xp.zeros_like(x_img, dtype=xp.float32)
    
    # Forward differences: ∂x / ∂x and ∂x / ∂z
    grad_x_img[:, :-1] = x_img[:, 1:] - x_img[:, :-1]
    grad_z_img[:-1, :] = x_img[1:, :] - x_img[:-1, :]
    
    return grad_x_img.flatten(), grad_z_img.flatten()

def divergence_2d(SMatrix, p_x, p_z):
    """
    Compute the 2D spatial divergence of a flattened dual vector field (p_x, p_z).
    Divergence is calculated using backward differences (Adjoint of forward gradient).
    
    Args:
        SMatrix: SMatrix instance
        p_x: Flattened 1D x-component array of shape (Z*X,)
        p_z: Flattened 1D z-component array of shape (Z*X,)
        
    Returns:
        div_p: Flattened 1D divergence array of shape (Z*X,)
    """
    xp = get_array_module(SMatrix)
    Z = SMatrix.Z
    X = SMatrix.X
    
    # Reshape dual vector fields back into their 2D layout
    p_x_img = p_x.reshape(Z, X)
    p_z_img = p_z.reshape(Z, X)
    
    # FORCED FLOAT32: Prevent silent float64 upcasting
    div_x = xp.zeros_like(p_x_img, dtype=xp.float32)
    div_z = xp.zeros_like(p_z_img, dtype=xp.float32)
    
    div_x[:, 0] = -p_x_img[:, 0]
    div_x[:, 1:-1] = p_x_img[:, :-2] - p_x_img[:, 1:-1]
    div_x[:, -1] = p_x_img[:, -2]
    
    div_z[0, :] = -p_z_img[0, :]
    div_z[1:-1, :] = p_z_img[:-2, :] - p_z_img[1:-1, :]
    div_z[-1, :] = p_z_img[-2, :]
    
    return (div_x + div_z).flatten()

def proj_tv(SMatrix, p, radius=1.0):
    """
    Project a concatenated 1D dual vector field p = (p_x, p_z) onto the L∞ ball.
    The projection clip magnitudes to radius lambda_tv (default 1.0 for Chambolle-Pock).
    
    Args:
        SMatrix: SMatrix instance
        p: Flattened concatenated array of shape (2 * Z * X,)
        radius: Bound constraint radius of the L∞ ball (corresponds to weighted TV regularization strength)
        
    Returns:
        p_projected: Flattened projected array of shape (2 * Z * X,)
    ```"""
    xp = get_array_module(SMatrix)
    ZX = SMatrix.Z * SMatrix.X
    
    # Separate the stacked dual vector components cleanly
    p_x = p[:ZX]
    p_z = p[ZX:]
    
    # Compute conjoint spatial magnitude per pixel
    norm_p = xp.sqrt(p_x**2 + p_z**2 + 1e-12)
    mask = norm_p > radius
    
    # Apply threshold truncation mapping vector-wise
    p_x_proj = xp.where(mask, p_x * radius / norm_p, p_x)
    p_z_proj = xp.where(mask, p_z * radius / norm_p, p_z)
    
    return xp.concatenate([p_x_proj, p_z_proj])

# =============================================================================
# FILE I/O
# =============================================================================

def load_recon(hdr_path):
    """
    Load an Interfile (.hdr) and its binary file (.img) to reconstruct an image as Vinci does.

    Parameters:
    -----------
    - hdr_path : full path to the .hdr file

    Returns:
    --------
    - image : NumPy array containing the image
    - header : dictionary containing metadata from the .hdr file
    """
    header = {}
    with open(hdr_path, 'r') as f:
        for line in f:
            if ':=' in line:
                key, value = line.split(':=', 1)
                key = key.strip().lower().replace('!', '')
                value = value.strip()
                header[key] = value

    data_file = header.get('name of data file')
    if data_file is None:
        raise ValueError(f"Cannot find data file associated with header file {hdr_path}")

    img_path = os.path.join(os.path.dirname(hdr_path), data_file)

    shape = [int(header[f'matrix size [{i}]']) for i in range(1, 4) if f'matrix size [{i}]' in header]
    if shape and shape[-1] == 1:
        shape = shape[:-1]

    if not shape:
        raise ValueError("Cannot determine image shape from metadata.")

    data_type = header.get('number format', 'short float').lower()
    dtype_map = {
        'short float': np.float32,
        'float': np.float32,
        'int16': np.int16,
        'int32': np.int32,
        'uint16': np.uint16,
        'uint8': np.uint8
    }
    dtype = dtype_map.get(data_type)
    if dtype is None:
        raise ValueError(f"Unsupported data type: {data_type}")

    byte_order = header.get('imagedata byte order', 'LITTLEENDIAN').lower()
    endianess = '<' if 'little' in byte_order else '>'

    img_size = os.path.getsize(img_path)
    expected_size = np.prod(shape) * np.dtype(dtype).itemsize

    if img_size != expected_size:
        raise ValueError(f"Image file size ({img_size} bytes) does not match expected size ({expected_size} bytes).")

    with open(img_path, 'rb') as f:
        data = np.fromfile(f, dtype=endianess + np.dtype(dtype).char)

    image = data.reshape(shape[::-1])

    rescale_slope = float(header.get('data rescale slope', 1))
    rescale_offset = float(header.get('data rescale offset', 0))
    image = image * rescale_slope + rescale_offset

    return image

# =============================================================================
# MEMORY UTILITIES
# =============================================================================

def calculate_memory_requirement(SMatrix, y):
    """
    Calculate the memory required (in GB) for SMatrix and y.
    
    Args:
        SMatrix: Matrix object (SMatrix, SMatrix_CSR, SMatrix_SELL, SMatrix_DENSE, np.ndarray, cp.ndarray)
        y: Vector (float32)
    """
    total_bytes = 0

    try:
        matrix_size_gb = SMatrix.get_matrix_size()
        if isinstance(matrix_size_gb, dict) and 'error' in matrix_size_gb:
            raise ValueError(f"SMatrix allocation error: {matrix_size_gb['error']}")
        
        size_SMatrix = matrix_size_gb * (1024 ** 3)
        total_bytes += size_SMatrix
        print(f"SMatrix size: {matrix_size_gb:.3f} GB")
    except AttributeError:
        raise AttributeError("SMatrix must implement the get_matrix_size() method.")
    
    # Vector y
    if hasattr(y, 'nbytes'):
        size_y = y.nbytes
        total_bytes += size_y
        print(f"Vector y size: {size_y / (1024 ** 3):.3f} GB")
    else:
        raise ValueError("Vector y must be an array type exposing the .nbytes attribute.")
    
    return total_bytes / (1024 ** 3)

def check_gpu_memory(device_index, required_memory, show_logs=True):
    """Check if enough memory is available on the specified GPU."""
    if not CUPY_AVAILABLE:
        raise RuntimeError("CuPy not available. Cannot check GPU memory.")
    
    free_memory = cp.cuda.runtime.memoryGetInfo()[0]
    free_memory_gb = free_memory / 1024**3
    
    if show_logs:
        print(f"Free memory on GPU {device_index}: {free_memory_gb:.2f} GB, Required memory: {required_memory:.2f} GB")
    
    return free_memory_gb >= required_memory

def check_gpu_available(SMatrix) -> bool:
    """Check if GPU operations are available."""
    if not isinstance(SMatrix.device, str) or "gpu" not in SMatrix.device:
        return False
    if not hasattr(SMatrix, 'sparse_mod'):
        return False
    if not CUPY_AVAILABLE:
        warnings.warn("CuPy not available. Falling back to CPU.")
        SMatrix.device = 'cpu'
        return False
    return True

def get_array_module(SMatrix):
    """Get the appropriate array module based on device."""
    if check_gpu_available(SMatrix):
        return cp
    else:
        return np

# =============================================================================
# OLD CUDA/GPU FUNCTIONS (kept for backward compatibility with AnalyticRecon)
# These are CuPy-only functions used by analytic reconstruction methods
# =============================================================================

def fourierz_gpu(z, X):
    """Forward Fourier transform along z-axis (GPU)."""
    if CUPY_AVAILABLE:
        dz = float(z[1] - z[0])
        Nz = X.shape[0]
        return cp.fft.fftshift(
            cp.fft.fft(
                cp.fft.ifftshift(X, axes=0),
                axis=0
            ),
            axes=0
        ) * (Nz * dz)

def ifourierz_gpu(z, X):
    """Inverse Fourier transform along z-axis (GPU)."""
    if CUPY_AVAILABLE:
        dz = float(z[1] - z[0])
        Nz = X.shape[0]
        return cp.fft.ifftshift(
            cp.fft.ifft(
                cp.fft.fftshift(X, axes=0),
                axis=0
            ),
            axes=0
        ) * (1 / dz)

def ifourierx_gpu(F_fx_z, dx):
    """Inverse Fourier along X (axis=1), Matlab-compatible (GPU)."""
    if CUPY_AVAILABLE:
        return (
            cp.fft.ifftshift(
                cp.fft.ifft(
                    cp.fft.fftshift(F_fx_z, axes=1),
                    axis=1
                ),
                axes=1
            ) * (1.0 / dx)
        )

def EvalDelayLawOS_center(X_m, theta, DelayLAWS, ActiveLIST, c):
    """
    Return the rotation center C for each angle.
    """
    Nangle = DelayLAWS.shape[1]
    C = np.zeros((Nangle, 2))
    ct = DelayLAWS * c
    
    for i in range(Nangle):
        active_idx = np.where(ActiveLIST[:, i] == 1)[0]
        if len(active_idx) == 0:
            continue
        angle_i = np.round(theta[i], 5)
        u = np.array([np.sin(angle_i), np.cos(angle_i)])
        X0 = X_m - u[0] * ct[:, i]
        Z0 = 0 - u[1] * ct[:, i]
        if Z0[-1] - Z0[0] != 0:
            C[i, 0] = (Z0[-1]*X0[0] - Z0[0]*X0[-1]) / (Z0[-1] - Z0[0])
            C[i, 1] = 0
    return C

def rotate_theta_gpu(X, Z, Iin, theta, C):
    """GPU equivalent of RotateTheta.m"""
    if CUPY_AVAILABLE:
        X_rel = X - C[0]
        Z_rel = Z - C[1]
        c = cp.cos(theta)
        s = cp.sin(theta)
        Xout = c * X_rel + s * Z_rel
        Zout = -s * X_rel + c * Z_rel
        Xout += C[0]
        Zout += C[1]
        dx = X[0, 1] - X[0, 0]
        dz = Z[1, 0] - Z[0, 0]
        x0 = X[0, 0]
        z0 = Z[0, 0]
        ix = (Xout - x0) / dx
        iz = (Zout - z0) / dz
        coords = cp.stack([iz.ravel(), ix.ravel()])
        Iout = map_coordinates(
            Iin, coords, order=1, mode='constant', cval=0.0
        )
        return Iout.reshape(Iin.shape)

def filter_radon_gpu(fz, Fc):
    """Filter for filtered backprojection (GPU)."""
    if CUPY_AVAILABLE:
        FILTER = cp.abs(fz)
        FILTER = cp.where(cp.abs(fz) > Fc, 0, FILTER)
        FILTER *= cp.exp(-2 * cp.abs(fz / Fc)**10)
        return FILTER

def filter_radon(f, N, filter_type, Fc):
    """
    Implement filters for filtered backprojection (iRadon).
    Inspired by MATLAB FilterRadon function from Mamouna Bocoum.

    Parameters:
    -----------
    f : np.ndarray
        Frequency vector (e.g., f_t or f_z).
    N : int
        Filter size (length of f).
    filter_type : str
        Filter type: 'ram-lak', 'shepp-logan', 'cosine', 'hamming', 'hann'.
    Fc : float
        Cutoff frequency.

    Returns:
    -----------
    FILTER : np.ndarray
        Filter applied to frequencies.
    """
    FILTER = np.abs(f)

    if filter_type == 'ram-lak':
        pass
    elif filter_type == 'shepp-logan':
        with np.errstate(divide='ignore', invalid='ignore'):
            FILTER = FILTER * (np.sinc(2 * f / (2 * Fc)))
        FILTER[np.isnan(FILTER)] = 1.0
    elif filter_type == 'cosine':
        FILTER = FILTER * np.cos(2 * np.pi * f / (4 * Fc))
    elif filter_type == 'hamming':
        FILTER = FILTER * (0.54 + 0.46 * np.cos(2 * np.pi * f / Fc))
    elif filter_type == 'hann':
        FILTER = FILTER * (1 + np.cos(2 * np.pi * f / (4 * Fc))) / 2
    else:
        raise ValueError(f"Unknown filter type: {filter_type}")

    FILTER[np.abs(f) > Fc] = 0
    FILTER = FILTER * np.exp(-2 * (np.abs(f) / Fc)**10)

    return FILTER

# =============================================================================
# PRECONDITIONERS
# =============================================================================

def _compute_diagonal_preconditioner(SMatrix):
    """
    Compute diagonal preconditioner: M = diag(A^T * 1)
    
    The diagonal preconditioner is computed as the sum of absolute values of each column
    of the system matrix A, which equals A^T * 1.
    
    This is commonly used in iterative reconstruction to normalize the sensitivity.
    
    Args:
        SMatrix: SMatrix instance (DENSE, CSR, or SELL) - must be allocated
        
    Returns:
        preconditioner: Diagonal vector (Z*X,) with A^T * 1 values, clamped to avoid zeros
        
    Compatible with: All SMatrix types (DENSE, CSR, SELL) and all devices (CPU, GPU)
    """
    xp = get_array_module(SMatrix)
    
    # Compute A^T * 1 (column sums)
    ones = xp.ones(SMatrix.N * SMatrix.T, dtype=xp.float32)
    
    if check_gpu_available(SMatrix):
        # Use GPU backprojection
        if hasattr(SMatrix, 'backward_projection'):
            preconditioner = SMatrix.backward_projection(ones)
        else:
            # Fallback: use CPU and convert
            preconditioner_cpu = SMatrix.backward_projection(cp.asnumpy(ones))
            preconditioner = cp.asarray(preconditioner_cpu)
    else:
        # Use CPU backprojection
        preconditioner = SMatrix.backward_projection(ones)
    
    # Ensure preconditioner is on correct device
    if check_gpu_available(SMatrix):
        preconditioner = cp.asarray(preconditioner)
    else:
        preconditioner = np.asarray(preconditioner)
    
    # Clamp to avoid division by zero
    preconditioner = xp.maximum(preconditioner, 1e-10)

    return preconditioner

def _apply_diagonal_preconditioner(U, preconditioner, SMatrix):
    """
    Apply diagonal preconditioner to a vector: U -> M^-1 * U
    
    Args:
        U: Vector to precondition (Z*X,)
        preconditioner: Diagonal preconditioner (Z*X,)
        SMatrix: SMatrix instance (for device information)
        
    Returns:
        Preconditioned vector on the same device as input
        
    Compatible with: All SMatrix types and all devices (CPU, GPU)
    """
    xp = get_array_module(SMatrix)
    
    # Ensure arrays are on the same device
    U = xp.asarray(U)
    preconditioner = xp.asarray(preconditioner)
    
    # Apply diagonal preconditioning: element-wise multiplication
    return U / preconditioner

def build_preconditioner(SMatrix, preconditioner_type):
    """
    Build preconditioner based on type.
    
    Args:
        SMatrix: SMatrix instance (must be allocated)
        preconditioner_type: PreconditionerType enum value
        
    Returns:
        preconditioner or None if NONE
        
    Compatible with: All SMatrix types and all devices (CPU, GPU)
    """    
    if preconditioner_type == PreconditionerType.NONE:
        return None
    elif preconditioner_type == PreconditionerType.DIAGONAL:
        return _compute_diagonal_preconditioner(SMatrix)
    else:
        raise ValueError(f"Unknown preconditioner type: {preconditioner_type}")

def apply_preconditioner(U, preconditioner, SMatrix):
    """
    Apply the specified preconditioner to vector U.
    
    Args:
        U: Vector to precondition (Z*X,)
        preconditioner: The preconditioner (Z*X,) or None if no preconditioning
        SMatrix: SMatrix instance (for device information)
        
    Returns:
        Preconditioned vector on the same device as input
    """
    if preconditioner is None:
        return U
    else:
        return _apply_diagonal_preconditioner(U, preconditioner, SMatrix)