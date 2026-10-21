from __future__ import annotations

"""
PDHG.py

Primal-Dual Hybrid Gradient (PDHG) algorithm for regularized reconstruction.
Strictly implemented via the mathematically stable Chambolle-Pock framework, supporting both 
deterministic and Stochastic updates (SPDHG / Subsets) for accelerated reconstruction.

Tailored for Acousto-Optic Tomography (AOT) matrix pipelines where N represents acoustic emissions
and T represents temporal propagation frames.
Note : Algorithm handles both real and complex data (4-phase quadrature representation) seamlessly, 
with dynamic kernel selection based on data type.

=============================================================================
MATHEMATICAL FRAMEWORK & OPTIMIZATION THEORY:
=============================================================================

1. Saddle-Point Optimization Problem (Chambolle-Pock Framework):
   We seek to solve a nonsmooth convex optimization problem involving a data fidelity term 
   and an isotropic Total Variation (TV) regularization prior subject to non-negativity:
   
       minimize_{λ >= 0}  { 0.5 * ||Ã * λ - y||_2^2 + β * ||∇λ||_{2,1} }

   where Ã = c * A is the column-equilibrated system matrix (c = 1 / median(|A|^T 1)).
   Using Fenchel-Rockafellar convex duality, this is cast as a saddle-point problem:
   
       min_{λ >= 0} max_{q, p}  { <Ã * λ, q> - 0.5 * ||q||_2^2 - <q, y> + <∇λ, p> - δ_{||p||_{2,∞} <= β}(p) }

   where:
   - Ã is the scaled forward system matrix (SMatrix).
   - q is the dual variable associated with the data fidelity term.
   - p = (p_x, p_z) is the dual variable associated with the spatial gradient operator (∇λ).
   - β scales the dual feasible set (point-wise L_2 ball of radius β for isotropic TV).

2. Dual Update Steps:
   - Data Fidelity Dual Variable (Proximal operator of the conjugate quadratic data term,
     restricted to the active subset mask S_k in SPDHG mode):
     
       q_{k+1}[S_k] = (q_k[S_k] + σ_q[S_k] * (Ã * bar{λ}_k - y)[S_k]) / (1 + σ_q[S_k])
     
   - Regularization Dual Variable (Gradient ascent followed by exact point-wise Euclidean 
     projection onto the L_2 ball of radius β):
     
       p_{k+1} = Proj_{||p||_2 <= β} (p_k + σ_p * ∇bar{λ}_k)

3. Primal Update & Extrapolation (Nesterov-like Overrelaxation):
   - Primal variable update via backward projection and divergence operator (-∇^T p = div p),
     combined with an orthogonal projection onto the non-negativity orthant R_+^{Z * X}:
     
       λ_{k+1} = max(0, λ_k - τ * (Ã^H q_{k+1} + div p_{k+1}))
     
   - Extrapolation step for the next iteration:
     
       bar{λ}_{k+1} = λ_{k+1} + θ * (λ_{k+1} - λ_k)

4. Preconditioned Step Size Rules & Primal-Dual Block Balancing:
   To ensure convergence and rapid TV ball saturation, vector-valued step sizes are computed 
   via Pock & Chambolle (2011, Lemma 2) and Ehrhardt et al. (2019, Theorem 2) with block 
   balancing weights (w_q, w_p):
   
       τ_j     = ρ / (w_q * col_sums_j(Ã) + (w_p / p_i) * |∇|^T 1_j)
       σ_{q,i} = (ρ * w_q) / row_sums_i(Ã)
       σ_p     = (ρ * w_p) / 2.0
=============================================================================
"""

import contextlib
import warnings
import numpy as np
from tqdm import trange
from typing import Optional, Union, Tuple

from AOT_biomaps.AOT_Recon.ReconTools import (
    ensure_device, get_array_module, get_device_context,
    forward_projection, backward_projection, check_stopping_criterion,
    estimate_lipschitz_constant, gradient_2d, divergence_2d,
    get_ground_truth
)
from AOT_biomaps.AOT_Recon.ReconEnums import StopCriterionType
from AOT_biomaps.AOT_Recon.AOT_Preconditioner.PreconditionerEnums import PreconditionerType
from AOT_biomaps.AOT_Recon.AOT_Preconditioner.NoPreconditioner import NoPreconditioner
from AOT_biomaps.AOT_Recon.AOT_SMatrix.SMatrix_SELL import SMatrix_SELL
from AOT_biomaps.AOT_Recon.AOT_SMatrix.SMatrix_CSR import SMatrix_CSR
from AOT_biomaps.AOT_Recon.AOT_SMatrix.SMatrix_DENSE import SMatrix_DENSE

try:
    import cupy as cp
    CUPY_AVAILABLE = True
except ImportError:
    cp = None
    CUPY_AVAILABLE = False

# =====================================================================
# CuPy Kernels definition for zero-allocation GPU updates
# =====================================================================
if CUPY_AVAILABLE:
    pdhg_gaussian_kernel__REAL = cp.ElementwiseKernel(
        'float32 q_in, float32 Alambda_bar, float32 y, float32 sigma, bool mask',
        'float32 q_out',
        '''
        if (mask) {
            q_out = (q_in + sigma * (Alambda_bar - y)) / (1.0f + sigma);
        } else {
            q_out = q_in;
        }
        ''',
        'pdhg_gaussian_kernel__REAL'
    )

    pdhg_gaussian_kernel__COMPLEX = cp.ElementwiseKernel(
        'complex64 q_in, complex64 Alambda_bar, complex64 y, float32 sigma, bool mask',
        'complex64 q_out',
        '''
        if (mask) {
            q_out = (q_in + sigma * (Alambda_bar - y)) / (1.0f + sigma);
        } else {
            q_out = q_in;
        }
        ''',
        'pdhg_gaussian_kernel__COMPLEX'
    )

    pdhg_tv_dual_kernel = cp.ElementwiseKernel(
        'float32 px_in, float32 pz_in, float32 gx, float32 gz, float32 sigma_p, float32 beta',
        'float32 px_out, float32 pz_out',
        '''
        if (beta <= 0.0f) {
            px_out = 0.0f;
            pz_out = 0.0f;
        } else {
            float rx = px_in + sigma_p * gx;
            float rz = pz_in + sigma_p * gz;
            float norm = hypotf(rx, rz);
            if (norm > beta) {
                float scale = beta / norm;
                px_out = rx * scale;
                pz_out = rz * scale;
            } else {
                px_out = rx;
                pz_out = rz;
            }
        }
        ''',
        'pdhg_tv_dual_kernel'
    )

    pdhg_primal_kernel = cp.ElementwiseKernel(
        'float32 lam_in, float32 backproj, float32 div, float32 tau, float32 theta',
        'float32 lam_out, float32 x_bar_out',
        '''
        float lam_new = lam_in - tau * backproj - tau * div;
        lam_new = lam_new > 0.0f ? lam_new : 0.0f; // Orthogonal projection onto R+
        lam_out = lam_new;
        x_bar_out = lam_new + theta * (lam_new - lam_in); // Overrelaxation / Extrapolation
        ''',
        'pdhg_primal_kernel'
    )


def calculate_step_size_PDHG(
    SMatrix: Union['SMatrix_DENSE', 'SMatrix_CSR', 'SMatrix_SELL'],
    preconditioner_type: PreconditionerType,
    num_subsets: int,
    num_iters: int,
    show_logs: bool,
    col_scale: float = 1.0,
    beta: float = 0.5,
    raw_row_sums: Optional[Union[np.ndarray, 'cp.ndarray']] = None,
    raw_col_sums: Optional[Union[np.ndarray, 'cp.ndarray']] = None,
) -> Tuple[Union[float, np.ndarray, 'cp.ndarray'], Union[float, np.ndarray, 'cp.ndarray'], Union[float, np.ndarray, 'cp.ndarray']]:
    """
    Compute primal and dual step sizes for the PDHG / SPDHG algorithm.
    
    Mathematical framework:
    - Standard PDHG (NONE): Scalar steps based on the operator spectral radius:
      ||Ã||_2^2 = c^2 * lambda_max(A^H A), ||∇||_2^2 <= 8.
    - Diagonal Preconditioner (DIAGONAL): Vector-valued steps based on Pock & Chambolle (2011, Lemma 2)
      and Ehrhardt et al. (2019, Theorem 2) with primal-dual block balancing weights (w_q, w_p):
      * w_q = median(row_sums(Ã)) / ρ centers median(σ_q) at 1.0 to avoid damping in (1 + σ_q)^(-1).
      * w_p = η(β) * w_q calibrates σ_p so the TV dual variable saturates ||p||_2 <= β rapidly.
      * For SPDHG with uniform sampling probability p_i = 1 / num_subsets, the subset column sum
        satisfies col_sums_j(Ã_i) ≈ p_i * col_sums_j(Ã), which cancels p_i in the data block:
        τ_j     = ρ / (w_q * col_sums_j(Ã) + (w_p / p_i) * grad_col_sum_j)
        σ_{q,i} = (ρ * w_q) / row_sums_i(Ã)
        σ_p     = (ρ * w_p) / 2.0   (since each finite difference row has L1 norm = 2)

    Args:
        SMatrix: System matrix wrapper instance.
        preconditioner_type: PreconditionerType.NONE or PreconditionerType.DIAGONAL.
        num_subsets: Number of subsets for stochastic updates (SPDHG).
        num_iters: Number of power iterations for spectral radius estimation.
        show_logs: If True, prints diagnostic information.
        col_scale: Normalization factor c applied to A (Ã = c * A).
        beta: Total Variation regularization parameter.
        raw_row_sums: Precomputed |A| 1 (optional, avoids redundant GPU pass).
        raw_col_sums: Precomputed |A|^T 1 (optional, avoids redundant GPU pass).

    Returns:
        tuple: (tau_vec, sigma_q_vec, sigma_p_vec)
    """
    xp = get_array_module(SMatrix)
    rho = 0.99  # Safety convergence factor strictly less than 1

    with get_device_context(SMatrix):
        # ==========================================================
        # 1. STANDARD PDHG (Scalar Steps)
        # ==========================================================
        if preconditioner_type == PreconditionerType.NONE:
            L_data = estimate_lipschitz_constant(
                SMatrix, preconditioner=NoPreconditioner(SMatrix=SMatrix),
                num_iters=num_iters, show_logs=show_logs
            )
            L_data_sq = float(L_data) * (col_scale ** 2)  # ||c * A||_2^2 = c^2 * ||A||_2^2
            L_grad_sq = 8.0                               # ||∇||_2^2 <= 8 in 2D
            L_total = L_data_sq + num_subsets * L_grad_sq

            tau = float(rho / np.sqrt(L_total))
            sigma_q = float(rho / np.sqrt(L_total))
            sigma_p = float(rho / np.sqrt(L_total))

            if show_logs:
                print(f"[AOT-biomaps] L_data_sq={L_data_sq:.3e} | L_total={L_total:.3e} | tau={tau:.3e} | sigma_q={sigma_q:.3e}")

            return xp.asarray(tau, dtype=xp.float32), xp.asarray(sigma_q, dtype=xp.float32), xp.asarray(sigma_p, dtype=xp.float32)

        # ==========================================================
        # 2. DIAGONAL PRECONDITIONER (Pock-Chambolle / Ehrhardt)
        # ==========================================================
        if show_logs:
            print("[AOT-biomaps] Computing preconditioned diagonal step sizes...")

        if raw_row_sums is None or raw_col_sums is None:
            raw_row_sums, raw_col_sums = SMatrix.compute_absolute_row_col_sums()

        # NOTE: Solving with scaled matrix Ã = c * A => sums scale exactly by c
        row_sums = xp.asarray(raw_row_sums, dtype=xp.float32) * col_scale
        col_sums = xp.asarray(raw_col_sums, dtype=xp.float32) * col_scale

        row_med = float(xp.median(row_sums))
        col_med = float(xp.median(col_sums))

        # Robust stabilization clipping
        eps_row = max(row_med * 1e-6, 1e-12)
        eps_col = max(col_med * 1e-6, 1e-12)

        row_sums = xp.maximum(row_sums, eps_row)
        col_sums = xp.maximum(col_sums, eps_col)

        # Spatial gradient column sum contribution: |∇|^T 1
        # Stencil weights for 2D forward differences: corners=2, edges=3, interior=4
        grad_col_sum = xp.full((SMatrix.Z, SMatrix.X), 4.0, dtype=xp.float32)
        grad_col_sum[0, :] -= 1.0
        grad_col_sum[-1, :] -= 1.0
        grad_col_sum[:, 0] -= 1.0
        grad_col_sum[:, -1] -= 1.0
        grad_col_sum = grad_col_sum.ravel()

        # Block balancing weights (Pock & Chambolle 2011, Lemma 2):
        # 1. w_q centers median(sigma_q) at 1.0
        w_q = row_med / rho if row_med > 0 else 1.0

        # 2. w_p calibrates sigma_p so the TV dual ball ||p||_2 <= beta saturates within ~10 iterations
        if beta <= 0.0:
            eta = 0.0
        else:
            eta_target = (20.0 * beta) / max(w_q * rho, 1e-12)
            eta = float(np.clip(eta_target, 1e-4, 1.5))

        w_p = eta * w_q

        # For SPDHG: p_i = 1 / num_subsets. Since subset col_sums_i ≈ p_i * col_sums,
        # p_i cancels on the data term and only weights the deterministic TV operator.
        p_i = 1.0 / max(1, num_subsets)
        tau_vec = rho / (w_q * col_sums + (w_p / p_i) * grad_col_sum)
        sigma_q_vec = (rho * w_q) / row_sums

        # Row sum of |∇| is exactly 2.0 (each forward difference u_{i+1} - u_i has two nonzeros: +1 and -1)
        sigma_p_val = (rho * w_p) / 2.0 if w_p > 0.0 else 0.0
        sigma_p_vec = xp.full(SMatrix.Z * SMatrix.X, sigma_p_val, dtype=xp.float32)

        if show_logs:
            print(
                f"[AOT-biomaps] tau median={float(xp.median(tau_vec)):.3e} | "
                f"sigma_q median={float(xp.median(sigma_q_vec)):.3e} | "
                f"sigma_p={sigma_p_val:.3e}"
            )

        return tau_vec, sigma_q_vec, sigma_p_vec


def PDHG(
    SMatrix: Union['SMatrix_DENSE', 'SMatrix_CSR', 'SMatrix_SELL'],
    y: Union[np.ndarray, 'cp.ndarray'],
    numIterations: int = 100,
    beta: float = 0.5,
    theta: float = 1.0,
    tau: Union[float, str] = "auto",
    sigma: Union[float, str] = "auto",
    numIterations_stepCalculation: int = 20,
    num_subsets: int = 1,
    reshuffle_period: int = 10,
    preconditioner_type: PreconditionerType = PreconditionerType.DIAGONAL,
    stop_criterion: StopCriterionType = StopCriterionType.MAX_ITERATIONS,
    stop_threshold: float = 100.0,
    stop_window_size: int = 5,
    device: Optional[str] = None,
    isSavingEachIteration: bool = True,
    isCostFunction: bool = False,
    withTumor: bool = True,
    max_saves: int = 5000,
    show_logs: bool = True,
    show_criterion: bool = True,
) -> Tuple[Union[np.ndarray, list], Optional[list], Optional[list]]:
    """
    Primal-Dual Hybrid Gradient (PDHG) function - Implemented via Chambolle-Pock Algorithm.
    
    Uses ReconTools functions for all matrix operations, making it compatible with
    any SMatrix type (CSR, SELL, DENSE) and device (CPU, GPU).
    Supports both deterministic (num_subsets=1) and stochastic updates (SPDHG, num_subsets>1).
    
    Supports regularization:
        - beta = 0.0 : Unregularized least-squares with non-negativity constraint.
        - beta > 0.0 : β * ||∇λ||_{2,1} (Isotropic Total Variation regularization).

    Supports stopping criteria:
        - MAX_ITERATIONS  : Stop after a fixed number of iterations.
        - RELATIVE_CHANGE : Stop when relative change in lambda is below threshold.
        - COST_FUNCTION   : Stop when relative change in cost function is below threshold.
        - MSE             : Stop when mean squared error with respect to ground truth stabilizes.
        - GRADIENT_NORM   : Stop when norm of the primal update step is below threshold.
    
    Supports preconditioning:
        - DIAGONAL : Block-balanced Pock-Chambolle / Ehrhardt diagonal preconditioning.
        - NONE     : Scalar step sizes using spectral radius estimation.
    """
    ensure_device(SMatrix, device, show_logs=show_logs)
    xp = get_array_module(SMatrix)
    is_gpu = (xp.__name__ == 'cupy')
    device_context = cp.cuda.Device(SMatrix.gpu_index) if is_gpu else contextlib.nullcontext()

    with device_context:
        Z, X = SMatrix.Z, SMatrix.X
        ZX = Z * X
        NT = SMatrix.N * SMatrix.T

        if SMatrix.T != y.shape[0] or SMatrix.N != y.shape[1]:
            raise ValueError(f"[AOT-biomaps] Shape mismatch: y {y.shape} vs SMatrix (T={SMatrix.T}, N={SMatrix.N})")

        # Adapt data dtype based on whether the matrix is complex (4-phase quadrature) or real
        data_dtype = xp.complex64 if SMatrix.isComplexSMatrix else xp.float32
        norm_factor = float(getattr(SMatrix, 'normalization_factor', 1.0))

        # Normalize data y to O(1)
        y_max = float(np.max(np.abs(y))) if SMatrix.isComplexSMatrix else float(np.max(y))
        y_norm = (y / y_max) if y_max > 0 else y
        y_flat = xp.asarray(y_norm.T.flatten().astype(data_dtype))

        # ==========================================================
        # SCALE CORRECTION (Always Active):
        # Solves min_x 0.5 * || Ã * x - y_norm ||_2^2 + beta * TV(x)
        # where Ã = c * A, and c = 1 / median(|A|^T 1).
        # Physical scale recovery: lambda_phys = x * (c * y_max / norm_factor)
        # ==========================================================
        raw_row_sums, raw_col_sums = SMatrix.compute_absolute_row_col_sums()
        raw_col_med = float(xp.median(raw_col_sums))
        c = (1.0 / raw_col_med) if raw_col_med > 0 else 1.0
        phys_scale = (c * y_max) / norm_factor

        if show_logs:
            print(f"[AOT-biomaps] col_scale c={c:.3e} | phys_scale={phys_scale:.3e} | beta={beta:.3e}")

        # --- Scaled projections: Ã * theta = c * (A * theta), Ã^H * e = c * (A^H * e) ---
        def fwd(theta_in):
            return c * forward_projection(SMatrix, theta_in)

        def bwd(e_in):
            return c * backward_projection(SMatrix, e_in)

        # Primal and dual variables initialization
        lambda_flat = xp.zeros(ZX, dtype=xp.float32)
        lambda_bar = xp.zeros(ZX, dtype=xp.float32)
        q = xp.zeros(NT, dtype=data_dtype)
        p_x = xp.zeros(ZX, dtype=xp.float32)
        p_z = xp.zeros(ZX, dtype=xp.float32)

        # Subset partitioning for SPDHG
        subset_mask = xp.ones(NT, dtype=xp.bool_)
        emission_indices = np.random.permutation(SMatrix.N)
        subset_slices = np.array_split(emission_indices, max(1, num_subsets))

        # Step sizes configuration
        if tau == "auto" or sigma == "auto":
            tau_res, sigma_q_res, sigma_p_res = calculate_step_size_PDHG(
                SMatrix, preconditioner_type, num_subsets,
                numIterations_stepCalculation, show_logs,
                col_scale=c, beta=beta,
                raw_row_sums=raw_row_sums, raw_col_sums=raw_col_sums
            )
            ArrayType = (np.ndarray, cp.ndarray) if CUPY_AVAILABLE else (np.ndarray,)
            tau_vec = xp.asarray(tau_res, dtype=xp.float32) if isinstance(tau_res, ArrayType) and tau_res.ndim > 0 else xp.full(ZX, float(tau_res), dtype=xp.float32)
            sigma_q = xp.asarray(sigma_q_res, dtype=xp.float32) if isinstance(sigma_q_res, ArrayType) and sigma_q_res.ndim > 0 else xp.full(NT, float(sigma_q_res), dtype=xp.float32)
            sigma_p_vec = xp.asarray(sigma_p_res, dtype=xp.float32) if isinstance(sigma_p_res, ArrayType) and sigma_p_res.ndim > 0 else xp.full(ZX, float(sigma_p_res), dtype=xp.float32)
        else:
            sigma_q = xp.full(NT, sigma, dtype=xp.float32)
            sigma_p_vec = xp.full(ZX, sigma, dtype=xp.float32)
            tau_vec = xp.full(ZX, tau, dtype=xp.float32)

        save_indices = np.unique(np.append(np.arange(0, numIterations, max(1, numIterations // max_saves)), numIterations - 1)).tolist()
        saved_lambda, saved_indices_list = [], []
        cost_history, window_history = [], []

        ground_truth = get_ground_truth(SMatrix, withTumor=withTumor)

        algo_name = f"SPDHG (Chambolle-Pock) ({num_subsets} subsets)" if num_subsets > 1 else "PDHG (Chambolle-Pock)"
        prec_str = preconditioner_type.name.replace("_", " ")
        cplx_str = "COMPLEX (4-phases quadrature) " if SMatrix.isComplexSMatrix else "REAL "
        desc = f"[AOT-biomaps] {cplx_str}{algo_name} --- ({SMatrix.matrix_type.name}) --- {prec_str} | Beta={beta:.3e} | c={c:.2e} | {'WITH' if withTumor else 'WITHOUT'} TUMOR --- DEVICE: {SMatrix.device.upper()}"

        iterator = trange(numIterations, desc=desc) if show_logs else range(numIterations)

        Ax = xp.zeros(NT, dtype=data_dtype)
        Alambda_bar = xp.zeros(NT, dtype=data_dtype)

        # ==========================================================
        # MAIN OPTIMIZATION LOOP
        # ==========================================================
        for it in iterator:
            prev_lambda = lambda_flat.copy()
            prev_Ax = Ax

            # --- DUAL UPDATE (Data Fidelity Proximal Operator) ---
            if is_gpu:
                if SMatrix.isComplexSMatrix:
                    pdhg_gaussian_kernel__COMPLEX(q, Alambda_bar, y_flat, sigma_q, subset_mask, q)
                else:
                    pdhg_gaussian_kernel__REAL(q, Alambda_bar, y_flat, sigma_q, subset_mask, q)
            else:
                q[subset_mask] = (q[subset_mask] + sigma_q[subset_mask] * (Alambda_bar[subset_mask] - y_flat[subset_mask])) / (1.0 + sigma_q[subset_mask])

            # --- DUAL UPDATE (Total Variation) ---
            grad_x, grad_z = gradient_2d(SMatrix, lambda_bar)

            if is_gpu:
                pdhg_tv_dual_kernel(p_x, p_z, grad_x, grad_z, sigma_p_vec, float(beta), p_x, p_z)
            else:
                if beta > 0.0:
                    p_x_raw = p_x + sigma_p_vec * grad_x
                    p_z_raw = p_z + sigma_p_vec * grad_z
                    norm_p = np.hypot(p_x_raw, p_z_raw)
                    scale = np.where(norm_p > beta, beta / np.maximum(norm_p, 1e-30), 1.0)
                    p_x = p_x_raw * scale
                    p_z = p_z_raw * scale
                else:
                    p_x.fill(0.0)
                    p_z.fill(0.0)

            # --- PRIMAL UPDATE & EXTRAPOLATION ---
            backproj_raw = bwd(q)
            backproj_q = (
                xp.ascontiguousarray(xp.real(backproj_raw), dtype=xp.float32)
                if SMatrix.isComplexSMatrix
                else xp.ascontiguousarray(backproj_raw, dtype=xp.float32)
            )

            div_p = divergence_2d(SMatrix, p_x, p_z)

            if is_gpu:
                pdhg_primal_kernel(
                    lambda_flat.astype(xp.float32, copy=False),
                    backproj_q.astype(xp.float32, copy=False),
                    div_p.astype(xp.float32, copy=False),
                    tau_vec.astype(xp.float32, copy=False),
                    float(theta),
                    lambda_flat,
                    lambda_bar
                )
            else:
                lambda_flat = lambda_flat - tau_vec * backproj_q - tau_vec * div_p
                np.maximum(lambda_flat, 0.0, out=lambda_flat)
                lambda_bar = lambda_flat + theta * (lambda_flat - prev_lambda)

            Ax = fwd(lambda_flat)
            Alambda_bar = Ax + float(theta) * (Ax - prev_Ax)

            # --- METRICS & COST ---
            if isCostFunction or stop_criterion == StopCriterionType.COST_FUNCTION:
                gx_eval, gz_eval = gradient_2d(SMatrix, lambda_flat)
                tv_val = beta * float(xp.sum(xp.hypot(gx_eval, gz_eval)))
                fid_val = 0.5 * float(xp.vdot(Ax - y_flat, Ax - y_flat).real)
                total_cost = fid_val + tv_val
                if isCostFunction:
                    cost_history.append(total_cost)

            # --- STOPPING CRITERION ---
            isStop = False
            stop_val = 0.0

            if stop_criterion != StopCriterionType.MAX_ITERATIONS:
                gradient_for_stop = backproj_q + div_p if stop_criterion == StopCriterionType.GRADIENT_NORM else None

                # Check for stopping using the physically scaled lambda for valid MSE logic
                lambda_phys_scaled = lambda_flat * phys_scale
                prev_lambda_phys_scaled = prev_lambda * phys_scale

                isStop, stop_val = check_stopping_criterion(
                    SMatrix, lambda_phys_scaled, prev_lambda_phys_scaled, stop_criterion, stop_threshold,
                    window_size=stop_window_size, history=cost_history,
                    ground_truth=ground_truth, gradient=gradient_for_stop,
                    window_history=window_history
                )

            will_break = isStop and (it >= max(15, stop_window_size))

            if show_logs and show_criterion and stop_criterion != StopCriterionType.MAX_ITERATIONS:
                iterator.set_postfix_str(f"{stop_criterion.name}: {stop_val:.2e}")

            if isSavingEachIteration and (it in save_indices or will_break):
                lambda_snapshot = lambda_flat.reshape(Z, X).get() if is_gpu else lambda_flat.reshape(Z, X).copy()
                # Recover physical scale: lambda_phys = lambda_tilde * (c * y_max / norm_factor)
                saved_lambda.append(lambda_snapshot * phys_scale)
                saved_indices_list.append(it)

            if will_break:
                if show_logs:
                    print(f"\n[AOT-biomaps] Stopping criterion {stop_criterion.name} reached at iteration {it}.")
                break

        final_result = lambda_flat.reshape(Z, X).get() if is_gpu else lambda_flat.reshape(Z, X)
        # Recover physical scale for final output
        final_result *= phys_scale

        return (saved_lambda, saved_indices_list, cost_history) if isSavingEachIteration else ([final_result], [it + 1], cost_history)