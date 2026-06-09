"""
PDHG.py

Primal-Dual Hybrid Gradient (PDHG) algorithm for regularized reconstruction.
Strictly implemented via the mathematically stable Chambolle-Pock framework, supporting both 
deterministic and Stochastic updates (SPDHG / Subsets) for accelerated reconstruction.

Tailored for Acousto-Optic Tomography (AOT) matrix pipelines where N represents acoustic emissions
and T represents temporal propagation frames.
"""

import numpy as np
from tqdm import trange
from typing import Optional, Union, Tuple

from AOT_biomaps.AOT_Recon.ReconTools import get_array_module, forward_projection, backward_projection, clamp_positive, check_stopping_criterion, calculate_step_size_reg, gradient_2d, divergence_2d, proj_tv
from AOT_biomaps.AOT_Recon.ReconEnums import NoiseType, PreconditionerType, StopCriterionType
from AOT_biomaps.AOT_Recon.AOT_SMatrix.SMatrix_SELL import SMatrix_SELL
from AOT_biomaps.AOT_Recon.AOT_SMatrix.SMatrix_CSR import SMatrix_CSR
from AOT_biomaps.AOT_Recon.AOT_SMatrix.SMatrix_DENSE import SMatrix_DENSE

# Check for CuPy availability
try:
    import cupy as cp
    CUPY_AVAILABLE = True
except ImportError:
    CUPY_AVAILABLE = False

# =====================================================================
# CuPy Kernels definition for fusion of operations (Zero-Allocation)
# =====================================================================
if CUPY_AVAILABLE:
    # Kernel for the Poisson update of q in SPDHG
    pdhg_poisson_kernel = cp.ElementwiseKernel(
        'float32 q_in, float32 Ax_bar, float32 y, float32 sigma, bool mask',
        'float32 q_out',
        '''
        if (mask) {
            float q_hat = q_in + sigma * Ax_bar;
            float val = 1.0f - q_hat;
            float disc = val * val + 4.0f * sigma * y;
            q_out = 0.5f * (1.0f + q_hat - sqrt(disc > 0.0f ? disc : 0.0f));
        } else {
            q_out = q_in;
        }
        ''',
        'pdhg_poisson_kernel'
    )
    # Kernel for the Gaussian update of q in SPDHG
    pdhg_gaussian_kernel = cp.ElementwiseKernel(
        'float32 q_in, float32 Ax_bar, float32 y, float32 sigma, bool mask',
        'float32 q_out',
        '''
        if (mask) {
            q_out = (q_in + sigma * (Ax_bar - y)) / (1.0f + sigma);
        } else {
            q_out = q_in;
        }
        ''',
        'pdhg_gaussian_kernel'
    )

    # Kernel for the primal update + extrapolation
    pdhg_primal_kernel = cp.ElementwiseKernel(
        'float32 lam_in, float32 backproj, float32 div, float32 tau, float32 theta',
        'float32 lam_out, float32 x_bar_out',
        '''
        float lam_new = lam_in - tau * backproj - tau * div;
        lam_new = lam_new > 0.0f ? lam_new : 0.0f; // Projection sur R+

        lam_out = lam_new;
        x_bar_out = lam_new + theta * (lam_new - lam_in); // Extrapolation
        ''',
        'pdhg_primal_kernel'
    )


def PDHG(
    SMatrix: Union['SMatrix_DENSE', 'SMatrix_CSR', 'SMatrix_SELL'],
    y: Union[np.ndarray, 'cp.ndarray'],
    numIterations: int = 100,
    beta: float = 1.0,         
    gamma: float = 1.0,     
    eta = 0.9,   
    theta: float = 1.0,        
    tau: Union[float, str] = "auto",
    sigma: Union[float, str] = "auto",
    numIterations_stepCalculation: int = 20,
    num_subsets: int = 1,     
    reshuffle_period: int = 10,
    noise_type: NoiseType = NoiseType.GAUSSIAN,
    preconditioner_type: PreconditionerType = PreconditionerType.NONE,
    use_adaptive_steps: bool = False,
    stop_criterion: StopCriterionType = StopCriterionType.MAX_ITERATIONS,
    stop_threshold: float = 100.0,
    stop_window_size: int = 5,
    isSavingEachIteration: bool = True,
    isCostFunction: bool = False,
    withTumor: bool = True,
    max_saves=5000,
    show_logs=True,
    show_criterion: bool = True,
) -> Tuple[Union[np.ndarray, list], Optional[list], Optional[list]]:
    """
    Primal-Dual Hybrid Gradient (PDHG) function - Implemented via Chambolle-Pock Algorithm.
    
    Uses ReconTools functions for all matrix operations, making it compatible with
    any SMatrix type (CSR, SELL, DENSE) and device (CPU, GPU).
    Supports both deterministic and stochastic updates (SPDHG) for accelerated convergence.
    
    Supports potential functions:
        - NONE: No regularization
        - TOTAL_VARIATION: β*||∇u||_1 (Isotropic Total Variation regularization (implemented via dual variable projection))

    Supports stopping criteria:
        - MAX_ITERATIONS: Stop after a fixed number of iterations
        - RELATIVE_CHANGE: Stop when relative change in lambda is below threshold
        - COST_FUNCTION: Stop when cost function value changes by less than threshold
        - MSE: Stop when mean squared error with respect to ground truth is below threshold (requires ground truth) ONLY FOR SIMULATED DATA 
        - GRADIENT_NORM: Stop when norm of the update step is below threshold
    
    Supports preconditioning:
        - DIAGONAL: Diagonal preconditioning using A^T * 1
        - NONE: No preconditioning (equivalent to standard gradient descent, but may not converge for ill-conditioned problems)

    Args:
        SMatrix: SMatrix instance (already allocated)
        y: Measurement data
        numIterations: Number of iterations
        beta: TV regularization weight parameter (lambda)
        delta: Kept for backward compatibility with main call signatures
        gamma: Balancing step-size parameter (scales tau down and sigma up)
        eta : Step size adaptation factor (used if use_adaptive_steps is True)
        theta: Extrapolation parameter for primal variable (relaxation step)
        tau: Step size parameter for primal update ('auto' for operator norm adaptation)
        sigma: Step size parameter for dual update ('auto' for operator norm adaptation)
        num_subsets: Number of subsets for stochastic updates (SPDHG). If 1, runs deterministic PDHG.
        reshuffle_period: Number of iterations after which subsets are reshuffled
        noise_type: Type of noise (POISSON or GAUSSIAN)
        potential_type: Kept for signature compatibility, operates strictly as TOTAL_VARIATION
        preconditioner_type: Type of preconditioner to use (default: NONE)
        use_adaptive_steps: If True, adaptively adjusts step sizes based on gradient norms
        stop_criterion: Criterion for stopping the iterations (StopCriterionType enum)
        stop_threshold: Threshold value for the stopping criterion (for MAX_iterations, this is ignored)
        stop_window_size: Window size (used to avoid early stop due to oscillations)
        isSavingEachIteration: If True, saves intermediate results
        isCostFunction: If True, computes and saves cost function history
        withTumor: Boolean for description only
        max_saves: Maximum number of intermediate saves
        show_logs: If True, shows progress bar
        show_criterion: If True, shows stopping criterion evolution in progress bar
  
    Returns:
        tuple: (reconstructed_image, saved_indices, cost_history)
        - reconstructed_image: Final or list of images (Z, X)
        - saved_indices: List of saved iteration indices (None if not saving)
        - cost_history: List of cost function values (None if not requested)
    """
    xp = get_array_module(SMatrix)
    is_gpu = (xp.__name__ == 'cupy')
    Z = SMatrix.Z
    X = SMatrix.X
    ZX = Z * X
    NT = SMatrix.N * SMatrix.T

    if SMatrix.T != y.shape[0] or SMatrix.N != y.shape[1]:
        raise ValueError(f"Shape mismatch: y {y.shape} vs SMatrix (T={SMatrix.T}, N={SMatrix.N})")

    y_flat = xp.asarray(y.T.flatten().astype(xp.float32))
    if noise_type == NoiseType.POISSON:
        y_flat = xp.maximum(y_flat, 0.0)

    q = xp.zeros(NT, dtype=xp.float32)
    p_x = xp.zeros(ZX, dtype=xp.float32)
    p_z = xp.zeros(ZX, dtype=xp.float32)
    lambda_flat = xp.zeros(ZX, dtype=xp.float32)
    x_bar = xp.zeros(ZX, dtype=xp.float32)
    y_data = y_flat.copy()
    subset_mask = xp.ones(NT, dtype=xp.bool_)

    emission_indices = np.random.permutation(SMatrix.N)
    subset_slices = np.array_split(emission_indices, num_subsets)
    p_i = 1.0 / num_subsets

    if tau == "auto" or sigma == "auto":
        if preconditioner_type != PreconditionerType.NONE:
            sens_fwd = forward_projection(SMatrix, xp.ones(ZX, dtype=xp.float32))
            xp.maximum(sens_fwd, 1e-10, out=sens_fwd)
            sigma_q = gamma * 0.99 / sens_fwd
            sigma_p = gamma * 0.99 / 2.0

            sens_bwd = backward_projection(SMatrix, xp.ones(NT, dtype=xp.float32))
            xp.maximum(sens_bwd, 1e-10, out=sens_bwd)
            tau_vec = (0.99 * p_i / gamma) / (sens_bwd + 4.0)
        else:
            tau, sigma_q, sigma_p = calculate_step_size_reg(SMatrix, gamma, num_subsets, numIterations_stepCalculation, show_logs)
            sigma_q = xp.full(NT, sigma_q)
            sigma_p = sigma_p
            tau_vec = xp.full(ZX, tau)
    else:
        sigma_q = xp.full(NT, sigma, dtype=xp.float32)
        sigma_p = sigma
        tau_vec = xp.full(ZX, tau, dtype=xp.float32)

    if use_adaptive_steps:
        grad_norm_history = []
        max_grad_norm = 1.0

    # Préparation des sauvegardes
    save_indices = np.unique(
        np.append(np.arange(0, numIterations, max(1, numIterations // max_saves)), numIterations - 1)
    ).tolist()
    saved_lambda = []
    saved_indices_list = []
    cost_history = [] if isCostFunction else None
    window_history = []

    # Configuration de la barre de progression
    algo_name = f"SPDHG (Chambolle-Pock) ({num_subsets} subsets)" if num_subsets > 1 else "PDHG (Chambolle-Pock)"
    prec_str = "Diagonal Preconditioner" if preconditioner_type != PreconditionerType.NONE else "No Preconditioner"
    description = f"AOT-BioMaps --- {algo_name} --- {prec_str} --- {'WITH' if withTumor else 'WITHOUT'} TUMOR --- {SMatrix.device.upper()}"
    iterator = trange(numIterations, desc=description) if show_logs else range(numIterations)

    for it in iterator:
        prev_lambda = lambda_flat.copy()

        Ax_bar = xp.maximum(forward_projection(SMatrix, x_bar), 1e-8) if noise_type == NoiseType.POISSON else forward_projection(SMatrix, x_bar)

        if num_subsets > 1:
            if it % reshuffle_period == 0:
                subset_slices = np.array_split(np.random.permutation(SMatrix.N), num_subsets)

            subset_mask.fill(False)
            for emis in subset_slices[it % num_subsets]:
                subset_mask[emis * SMatrix.T : (emis + 1) * SMatrix.T] = True

        if is_gpu:
            if noise_type == NoiseType.POISSON:
                pdhg_poisson_kernel(q, Ax_bar, y_data, sigma_q, subset_mask, q)
            else:
                pdhg_gaussian_kernel(q, Ax_bar, y_data, sigma_q, subset_mask, q)
        else:
            if noise_type == NoiseType.POISSON:
                q_hat = q[subset_mask] + sigma_q[subset_mask] * Ax_bar[subset_mask]
                disc = np.maximum((1.0 - q_hat)**2 + 4.0 * sigma_q[subset_mask] * y_data[subset_mask], 0.0)
                q[subset_mask] = 0.5 * (1.0 + q_hat - np.sqrt(disc))
            else:
                q[subset_mask] = (q[subset_mask] + sigma_q[subset_mask] * (Ax_bar[subset_mask] - y_data[subset_mask])) / (1.0 + sigma_q[subset_mask])

        grad_x, grad_z = gradient_2d(SMatrix, x_bar)
        p_x += sigma_p * grad_x
        p_z += sigma_p * grad_z

        p_projected = proj_tv(SMatrix, xp.concatenate([p_x, p_z]), radius=beta)
        p_x, p_z = p_projected[:ZX], p_projected[ZX:]

        backproj_q = backward_projection(SMatrix, q)
        div_p = divergence_2d(SMatrix, p_x, p_z)

        if is_gpu:
            pdhg_primal_kernel(
                lambda_flat.astype(xp.float32, copy=False),
                backproj_q.astype(xp.float32, copy=False),
                div_p.astype(xp.float32, copy=False),
                tau_vec.astype(xp.float32, copy=False),
                float(theta),
                lambda_flat,
                x_bar
            )
        else:
            lambda_flat = lambda_flat - tau_vec * backproj_q - tau_vec * div_p
            np.maximum(lambda_flat, 0.0, out=lambda_flat)  # Projection sur R+
            x_bar = lambda_flat + theta * (lambda_flat - prev_lambda)  # Extrapolation

        # dynamic step size adaptation based on gradient norm (every 5 iterations)
        if use_adaptive_steps and  it % 5 == 0:
            grad_norm = float(xp.linalg.norm(backproj_q + div_p))
            grad_norm_history.append(grad_norm)
            if len(grad_norm_history) > 5:
                max_grad_norm = max(grad_norm_history[-5:])
                # step size adaptation rules (simple heuristic)
                if max_grad_norm > 1e2:
                    tau_vec *= eta
                    sigma_q /= eta
                    sigma_p /= eta
                elif max_grad_norm < 1e-2:
                    tau_vec *= eta
                    sigma_q /= eta
                    sigma_p /= eta

        if isCostFunction:
            Ax = forward_projection(SMatrix, lambda_flat)
            gx_eval, gz_eval = gradient_2d(SMatrix, lambda_flat)
            tv_penalty = beta * float(xp.sum(xp.sqrt(gx_eval**2 + gz_eval**2 + 1e-12)))

            if noise_type == NoiseType.POISSON:
                xp.maximum(Ax, 1e-10, out=Ax)
                fidelity = float(-(xp.sum(y_data * xp.log(Ax) - Ax)))
            else:
                fidelity = 0.5 * float(xp.vdot(Ax - y_data, Ax - y_data))
            cost_history.append(fidelity + tv_penalty)

        if stop_criterion != StopCriterionType.MAX_ITERATIONS:
            ground_truth = SMatrix.experiment.OpticImage.phantom if withTumor else SMatrix.experiment.OpticImage.laser.intensity
            gradient = backward_projection(SMatrix, q) + divergence_2d(SMatrix, p_x, p_z) if stop_criterion == StopCriterionType.GRADIENT_NORM else None
            isStop, val = check_stopping_criterion(SMatrix, lambda_flat, prev_lambda, stop_criterion, stop_threshold, window_size=stop_window_size, history=cost_history, ground_truth=ground_truth, gradient=gradient, window_history=window_history)
            if show_logs and show_criterion:
                iterator.set_postfix_str(f"{stop_criterion.name}: {val:.2e}")
            if isStop:
                if show_logs: print(f"\n[Stopping] Criterion {stop_criterion.name} reached at iteration {it}.")
                cost_history.pop() if isCostFunction else None
                break

        if isSavingEachIteration and it in save_indices:
            saved_lambda.append(lambda_flat.reshape(Z, X).get() if is_gpu else lambda_flat.reshape(Z, X).copy()
            )
            saved_indices_list.append(it)

    final_result = lambda_flat.reshape(Z, X).get() if is_gpu else lambda_flat.reshape(Z, X)
    return (saved_lambda, saved_indices_list, cost_history) if isSavingEachIteration else (final_result, None, cost_history)