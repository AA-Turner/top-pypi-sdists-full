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

from AOT_biomaps.AOT_Recon.ReconEnums import PotentialShapeType, PotentialType, StopCriterionType
from AOT_biomaps.AOT_Recon.AOT_Preconditioner.PreconditionerEnums import PreconditionerType
# Optional cupy imports for GPU acceleration
try:
    import cupy as cp
    from cupyx.scipy.ndimage import map_coordinates
    CUPY_AVAILABLE = True
except ImportError:
    CUPY_AVAILABLE = False


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

def estimate_lipschitz_constant(SMatrix, preconditioner, num_iters=20):
    """
    Estimate the Lipschitz constant (spectral radius) of the gradient operator
    using the Power Iteration method.
    
    Mathematical framework:
    Finds the dominant eigenvalue of the operator M = inv(P) * A^H * A.
    - Without preconditioner: L = lambda_max(A^H * A)
    - With preconditioner: L = lambda_max(inv(P) * A^H * A)

    Args:
        SMatrix: System matrix wrapper instance.
        preconditioner: Preconditioner instance.
        num_iters: Number of power iterations.

    Returns:
        float: Estimated Lipschitz constant (spectral radius).
    """
    xp = get_array_module(SMatrix)

    # Initialize a random vector v_0 on the unit sphere: ||v_0||_2 = 1
    v = xp.random.randn(SMatrix.Z * SMatrix.X).astype(xp.float32)
    v /= xp.linalg.norm(v)

    eps = 1e-12
    L_est = 0.0

    for i in range(num_iters):
        # Forward projection -> u = A * v_k
        Av = forward_projection(SMatrix, v)
        if float(xp.sum(xp.abs(Av))) < eps:
            raise RuntimeError("[AOT-biomaps] Forward projection returned all zeros.")
        
        # Backward projection -> w = Aᴴ * u = Aᴴ * A * v_k
        w = backward_projection(SMatrix, Av)
        
        # Map complex gradients to the real parameter space if necessary
        w = xp.real(w).astype(xp.float32) if SMatrix.isComplexSMatrix else w.astype(xp.float32)
        
        # Apply the preconditioner -> w = P⁻¹ * Aᴴ * A * v_k
        w = preconditioner.apply_inverse(w)
        
        # Extract the eigenvalue
        # At convergence, the vector aligns with the dominant eigenvector v_max.
        # Thus, w = M * v_max = λmax * v_max.
        # Since ||v_max||_2 = 1, taking the L2 norm yields the spectral radius directly:
        # ||w||_2 = ||λmax * v_max||_2 = λmax * ||v_max||_2 = λmax
        norm = float(xp.linalg.norm(w))
        
        if norm < eps:
            raise RuntimeError("[AOT-biomaps] Power iteration collapsed to zero.")

        # Normalize for the next iteration -> v_{k+1} = w / ||w||_2
        v = w / norm
        L_est = norm 

    return max(L_est, 0.0)


def calculate_step_size_LS(SMatrix, preconditioner, eta, num_iters, show_logs):
    """
    Compute the gradient descent step size in the LS algorithm.
    Args:
        - SMatrix : System matrix.
        - preconditioner : Preconditioner object implementing apply_inverse().
        - eta : Relaxation parameter (typically 1.8-1.99).
        - num_iters : Number of power iterations.
        - show_logs : Print information.
    """
    if eta is None:
        print("[AOT-biomaps] Warning: eta not set. Defaulting to 1.9.")
        eta = 1.9

    if not (1.0 < eta < 2.0):
        print(f"[AOT-biomaps] Warning: eta={eta} is outside (1,2).")

    L = estimate_lipschitz_constant(SMatrix, preconditioner=preconditioner, num_iters=num_iters)

    alpha = eta / L if L > 0 else 1.0

    if show_logs:
        print(f"[AOT-biomaps] Using step size alpha = {alpha:.3e}")

    return alpha

def calculate_step_size_PGC(SMatrix, preconditioner, eta, num_iters, show_logs):
    """
    Compute the gradient descent step size in the PGC algorithm.
    Args:
        - SMatrix : System matrix.
        - preconditioner : Preconditioner object implementing apply_inverse(). Need to be set to NoPreconditioner for PGC.
        - eta : Relaxation parameter (typically 1.8-1.99).
        - num_iters : Number of power iterations.
        - show_logs : Print information.
    """
    if eta is None:
        print("[AOT-biomaps] Warning: eta not set. Defaulting to 1.9.")
        eta = 1.9

    if not (1.0 < eta < 2.0):
        print(f"[AOT-biomaps] Warning: eta={eta} is outside (1,2).")
    
    L = estimate_lipschitz_constant(SMatrix, preconditioner=preconditioner, num_iters=num_iters)

    alpha = eta / L if L > 0 else 1.0

    if show_logs:
        print(f"[AOT-biomaps] Using step size alpha = {alpha:.3e}")

    return alpha

def calculate_step_size_FISTA(SMatrix, preconditioner, eta, potential_type, beta, potential_radius, num_iters, show_logs):
    """
    Compute the gradient descent step size in the FISTA algorithm.
    Args:
        - SMatrix : System matrix.
        - preconditioner : Preconditioner object implementing apply_inverse().
        - eta : Relaxation parameter (typically 1.8-1.99).
        - potential_type : Type of potential for regularization.
        - beta : Regularization parameter for the potential.
        - potential_radius : Neighborhood radius for the potential.
        - num_iters : Number of power iterations.
        - show_logs : Print information.
    """
    if eta is None:
        print("[AOT-biomaps] Warning: eta not set. Defaulting to 1.9.")
        eta = 1.9

    # λmax(AᴴA) or λmax(P⁻¹AᴴA)    
    L = estimate_lipschitz_constant(SMatrix, preconditioner=preconditioner, num_iters=num_iters)

    L_data = eta / L
    L_prior = 8.0 * beta * (potential_radius ** 2) if potential_type != PotentialType.NONE else 0.0
    alpha = eta / (L_data + L_prior)

    if show_logs:
        print(f"[AOT-biomaps] Using step size alpha = {alpha:.3e}")
    
    return alpha

def calculate_step_size_PDHG(SMatrix, preconditioner, num_subsets, num_iters, show_logs):
    """
    Calculate the PDHG step sizes (tau, sigma_q, sigma_p).
    If a preconditioner is passed, computes the diagonal vector step sizes 
    according to Ehrhardt et al. 2019, Theorem 2.
    """
    xp = get_array_module(SMatrix)
    rho = 0.99 # Safety factor strictly less than 1 
    
    # ---------------------------------------------------------
    # SCALAR STEPS (Standard PDHG without preconditioning)
    # ---------------------------------------------------------
    if preconditioner.precondType == PreconditionerType.NONE:
        # Force NoPreconditioner to evaluate the true Lipschitz constant L = λmax(AᴴA)
        L_data = estimate_lipschitz_constant(SMatrix, preconditioner=preconditioner, num_iters=num_iters)
        L_grad = 8.0 # ||∇||² = 8.0 for 2D finite differences
        L_total = (num_subsets * L_data) + L_grad

        tau_val = float(rho / np.sqrt(L_total))
        sigma_q_val = float(rho *  num_subsets / np.sqrt(L_total))
        sigma_p_val = float(rho / np.sqrt(L_total))

        if show_logs:
            print(f"[AOT-biomaps] L_data: {L_data:.2e} | L_total: {L_total:.2e} | scalar tau: {tau_val:.2e} | scalar sigma_q: {sigma_q_val:.2e}")
            
        return tau_val, sigma_q_val, sigma_p_val

    # ---------------------------------------------------------
    # DIAGONAL PRECONDITIONED STEPS (Theorem 2, Ehrhardt et al. 2019)
    # ---------------------------------------------------------
    elif preconditioner.precondType == PreconditionerType.DIAGONAL:
        if show_logs:
            print("[AOT-biomaps] Computing diagonal preconditioned step sizes (Ehrhardt 2019)...")
            
        # 1. Compute column sums: A^T * 1
        ones_dual = xp.ones(SMatrix.N * SMatrix.T, dtype=xp.float32)
        col_sums_raw = backward_projection(SMatrix, ones_dual)
        col_sums = xp.real(col_sums_raw) if SMatrix.isComplexSMatrix else col_sums_raw
        
        # 2. Compute row sums: A * 1
        ones_primal = xp.ones(SMatrix.Z * SMatrix.X, dtype=xp.float32)
        row_sums_raw = forward_projection(SMatrix, ones_primal)
        row_sums = xp.real(row_sums_raw) if SMatrix.isComplexSMatrix else row_sums_raw
        
        # 3. Add regularization norm to primal sensitivity (||∇||^2 bounded by 8)
        # In preconditioned PDHG, the primal norm must account for the spatial gradient
        col_sums += 8.0 

        # 4. Compute vector step sizes
        # p_i = 1/num_subsets (probability of selecting a subset)
        p_i = 1.0 / num_subsets 
        
        eps = 1e-12
        tau_vec = rho * p_i / (col_sums + eps)
        sigma_q_vec = rho / (row_sums + eps)
        
        # Regularization dual step remains scalar as gradient operator is uniform
        sigma_p_val = float(rho / 8.0) 

        if show_logs:
            print(f"[AOT-biomaps] Preconditioned steps computed. Median tau: {float(xp.median(tau_vec)):.2e}, Median sigma_q: {float(xp.median(sigma_q_vec)):.2e}")

        return tau_vec, sigma_q_vec, sigma_p_val
    else:
        raise ValueError(f"[AOT-biomaps] Unsupported preconditioner type: {preconditioner.precondType}, for PDHG step size calculation, need NoPreconditioner or DiagPreconditioner (Ehrhardt 2019).")
    
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
                        // Normalized Quadratic Region (divided by delta)
                        g += beta * weight * diff / delta;
                        h += beta * weight / delta;
                        e += 0.5f * beta * weight * diff * diff / delta;
                    } else {
                        // Normalized Linear Region (Edges)
                        g += beta * weight * (diff > 0.0f ? 1.0f : -1.0f);
                        if (hessian_mode == 1) {
                            h += beta * weight / abs_diff; // De Pierro Surrogate
                        } else {
                            h += 0.0f; // Exact Hessian
                        }
                        e += beta * weight * (abs_diff - 0.5f * delta);
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
    """
    Generates the FULL neighborhood (Gather) and caches it.
    """
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
                # Weights are inversely proportional to Euclidean distance: w = 1 / d
                weight = 1.0 / dist_l2
                offsets_dz.append(dz)
                offsets_dx.append(dx)
                weights.append(weight)
                total_weight += weight
                
    # Normalize weights so that Σ w_ij = 4.0 (ensures stable Lipschitz constant)
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
            raise ValueError(f"[AOT-biomaps] Unsupported potential: {potential_type}")

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
        hess_img = xp.zeros_like(U_img, dtype=xp.float32) if compute_hess else None
        U_value = 0.0
        
        for k in range(len(dz_arr)):
            dz, dx, w = int(dz_arr[k]), int(dx_arr[k]), float(w_arr[k])
            
            slice_c_z = slice(max(0, -dz), min(Z, Z - dz))
            slice_n_z = slice(max(0, dz), min(Z, Z + dz))
            slice_c_x = slice(max(0, -dx), min(X, X - dx))
            slice_n_x = slice(max(0, dx), min(X, X + dx))
            
            u_i = U_img[slice_c_z, slice_c_x]
            u_j = U_img[slice_n_z, slice_n_x]
            
            # Spatial gradient: Δu = u_i - u_j
            diff = u_i - u_j
            
            if potential_type == PotentialType.QUADRATIC:
                # Quadratic: U(Δu) = 0.5 * β * w * (Δu)²
                # ∇U = β * w * Δu  |  ∇²U = β * w
                g = beta * w * diff
                h = beta * w
                e = 0.5 * beta * w * diff**2
                
            elif potential_type == PotentialType.HUBER:
                abs_diff = xp.abs(diff)
                mask_quad = abs_diff <= delta
                mask_lin = ~mask_quad
                
                g = xp.zeros_like(diff)
                # Quadratic regime (|Δu| ≤ δ) : Normalized by δ
                # ∇U = β * w * Δu / δ
                g[mask_quad] = beta * w * diff[mask_quad] / delta
                
                # Linear regime (|Δu| > δ) : Acts like TV L1 penalty
                # ∇U = β * w * sign(Δu)
                g[mask_lin] = beta * w * xp.sign(diff[mask_lin])
                
                h = xp.zeros_like(diff)
                # ∇²U = β * w / δ
                h[mask_quad] = beta * w / delta
                if hessian_mode == 1:
                    # De Pierro Surrogate Hessian: H = ∇U / Δu
                    h[mask_lin] = beta * w / (abs_diff[mask_lin] + 1e-8)
                    
                # Energy computation
                e = xp.zeros_like(diff)
                e[mask_quad] = 0.5 * beta * w * (diff[mask_quad]**2) / delta
                e[mask_lin] = beta * w * (abs_diff[mask_lin] - 0.5 * delta)
                
            elif potential_type == PotentialType.RELATIVE_DIFFERENCE:
                # RDP: U(Δu) = β * w * (Δu)² / (u_i + u_j + δ|Δu|)
                denom = u_i + u_j + delta * xp.abs(diff) + 1e-8
                d_denom = 1.0 + delta * xp.sign(diff)
                
                # Quotient rule derivative: (u/v)' = (u'v - uv')/v²
                g = beta * w * (2.0 * diff * denom - (diff**2) * d_denom) / (denom**2)
                
                # Pragmatic strictly convex approximation for Hessian: ∇²U ≈ 2 * β * w / denom
                h = beta * w * 2.0 / denom
                e = beta * w * (diff**2) / denom

            if compute_grad: grad_img[slice_c_z, slice_c_x] += g
            if compute_hess: hess_img[slice_c_z, slice_c_x] += h
            if compute_energy: U_value += float(xp.sum(e))

        # Each edge is counted twice (A->B and B->A), so we divide total energy by 2
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
            raise ValueError(f"[AOT-biomaps] Ground truth image required for MSE stopping criterion.")
        # Assuming mse() returns a scalar
        raw_metric = float(mse(SMatrix, ground_truth, current_lambda))
        
    elif criterion_type == StopCriterionType.GRADIENT_NORM:
        if gradient is None:
            raise ValueError(f"[AOT-biomaps] Gradient stop criterion is not supported with this optimizer.")
        raw_metric = float(xp.linalg.norm(gradient))
        
    else:
        raise ValueError(f"[AOT-biomaps] Unsupported stopping criterion type: {criterion_type}")

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
        raise ValueError(f"[AOT-biomaps] Cannot find data file associated with header file {hdr_path}")

    img_path = os.path.join(os.path.dirname(hdr_path), data_file)

    shape = [int(header[f'matrix size [{i}]']) for i in range(1, 4) if f'matrix size [{i}]' in header]
    if shape and shape[-1] == 1:
        shape = shape[:-1]

    if not shape:
        raise ValueError(f"[AOT-biomaps] Cannot determine image shape from metadata.")
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
        raise ValueError(f"[AOT-biomaps] Unsupported data type: {data_type}")

    byte_order = header.get('imagedata byte order', 'LITTLEENDIAN').lower()
    endianess = '<' if 'little' in byte_order else '>'

    img_size = os.path.getsize(img_path)
    expected_size = np.prod(shape) * np.dtype(dtype).itemsize

    if img_size != expected_size:
        raise ValueError(f"[AOT-biomaps] Image file size ({img_size} bytes) does not match expected size ({expected_size} bytes).")

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
            raise ValueError(f"[AOT-biomaps] SMatrix allocation error: {matrix_size_gb['error']}")
        
        size_SMatrix = matrix_size_gb * (1024 ** 3)
        total_bytes += size_SMatrix
        print(f"[AOT-biomaps] SMatrix size: {matrix_size_gb:.3f} GB")
    except AttributeError:
        raise AttributeError(f"[AOT-biomaps] SMatrix must implement the get_matrix_size() method.")
    
    # Vector y
    if hasattr(y, 'nbytes'):
        size_y = y.nbytes
        total_bytes += size_y
        print(f"[AOT-biomaps] Vector y size: {size_y / (1024 ** 3):.3f} GB")
    else:
        raise ValueError(f"[AOT-biomaps] Vector y must be an array type exposing the .nbytes attribute.")

    return total_bytes / (1024 ** 3)

def check_gpu_memory(device_index, required_memory, show_logs=True):
    """Check if enough memory is available on the specified GPU."""
    if not CUPY_AVAILABLE:
        raise RuntimeError("CuPy not available. Cannot check GPU memory.")
    
    free_memory = cp.cuda.runtime.memoryGetInfo()[0]
    free_memory_gb = free_memory / 1024**3
    
    if show_logs:
        print(f"[AOT-biomaps] Free memory on GPU {device_index}: {free_memory_gb:.2f} GB, Required memory: {required_memory:.2f} GB")
    
    return free_memory_gb >= required_memory

def check_gpu_available(SMatrix) -> bool:
    """Check if GPU operations are available."""
    if not isinstance(SMatrix.device, str) or "gpu" not in SMatrix.device:
        return False
    if not hasattr(SMatrix, 'sparse_mod'):
        return False
    if not CUPY_AVAILABLE:
        print("[AOT-biomaps] Warning: CuPy is not available. Falling back to CPU.")
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
        raise ValueError(f"[AOT-biomaps] Unknown filter type: {filter_type}")

    FILTER[np.abs(f) > Fc] = 0
    FILTER = FILTER * np.exp(-2 * (np.abs(f) / Fc)**10)

    return FILTER
