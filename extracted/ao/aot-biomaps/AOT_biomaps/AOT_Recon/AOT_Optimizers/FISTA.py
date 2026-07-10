"""
FISTA.py

Fast Iterative Shrinkage-Thresholding Algorithm (Accelerated PGD).
Uses unified SMatrix interface and ReconTools functions.
Single unified function that works with any SMatrix type (CSR, SELL, DENSE) and any device (CPU, GPU).

Supports potential functions: QUADRATIC, HUBER, RELATIVE_DIFFERENCE
"""

import numpy as np
from tqdm import trange
from typing import Optional, Union, Tuple

from AOT_biomaps.AOT_Recon.ReconTools import get_array_module, forward_projection, backward_projection, get_potential_function, check_stopping_criterion, calculate_step_size, build_preconditioner
from AOT_biomaps.AOT_Recon.ReconEnums import PotentialType, PotentialShapeType, StopCriterionType, PreconditionerType
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
    fista_update_kernel = cp.ElementwiseKernel(
        'float32 x_old, float32 z_in, float32 grad, float32 alpha, float32 momentum',
        'float32 x_new, float32 z_out',
        '''
        double step = (double)z_in - (double)alpha * (double)grad;
        
        double x_val = step > 0.0 ? step : 0.0;
        x_new = (float)x_val;
        
        z_out = (float)(x_val + (double)momentum * (x_val - (double)x_old));
        ''',
        'fista_update_kernel'
    )

def FISTA(
    SMatrix: Union['SMatrix_DENSE', 'SMatrix_CSR', 'SMatrix_SELL'],
    y: Union[np.ndarray, 'cp.ndarray'],
    numIterations: int = 100,
    alpha: Union[float, str] = "auto",     
    beta: float = 1.0,      
    delta: float = 0.01,     
    eta: Optional[float] = None, 
    numIterations_stepCalculation: int = 20,
    potential_type: PotentialType = PotentialType.QUADRATIC,
    potential_shape: PotentialShapeType = PotentialShapeType.CROSS,
    potential_radius: int = 2,
    preconditioner_type: PreconditionerType = PreconditionerType.DIAGONAL,
    stop_criterion: StopCriterionType = StopCriterionType.MAX_ITERATIONS,
    stop_threshold: float = 100.0,
    stop_window_size: int = 5,
    isSavingEachIteration: bool = True,
    isCostFunction: bool = False,
    withTumor: bool = True,
    max_saves: int = 5000,
    show_logs: bool = True,
    show_criterion: bool = True,
) -> Tuple[Union[np.ndarray, list], Optional[list], Optional[list]]:
    """
    Fast Iterative Shrinkage-Thresholding Algorithm (FISTA) for least squares reconstruction with potential regularization.
    
    Uses ReconTools functions for all matrix operations, so it works with
    any SMatrix type (CSR, SELL, DENSE) and any device (CPU, GPU).

    Supports potential functions:
        - NONE: No regularization
        - QUADRATIC: 0.5 * β * (u-v)^2
        - HUBER: β * (0.5 * (u-v)^2 if |u-v| <= δ else δ * (|u-v| - 0.5 * δ))
        - RELATIVE_DIFFERENCE: β * (u-v)^2 / (v + ε)

    Supports stopping criteria:
        - MAX_ITERATIONS: Stop after a fixed number of iterations
        - RELATIVE_CHANGE: Stop when relative change in lambda is below threshold
        - COST_FUNCTION: Stop when cost function value changes by less than threshold
        - MSE: Stop when mean squared error with respect to ground truth is below threshold (requires ground truth) ONLY FOR SIMULATED DATA 
        - GRADIENT_NORM: Stop when norm of the update step is below threshold
    
    Supports preconditioning:
        - DIAGONAL: Diagonal preconditioning using A^T * 1 (RECOMMENDED FOR FISTA)
        - NONE: No preconditioning (may lead to slower convergence)
    
    Args:
        SMatrix: SMatrix instance (already allocated)
        y: Measurement data (shape: (T, N))
        numIterations: Number of iterations
        alpha: Step size for gradient update (float or "auto" for backtracking line search)
        beta: Regularization parameter (weight for potential)
        delta: Huber threshold (only used if potential_type is HUBER)
        eta: Parameter for automatic step size calculation (only used if alpha is "auto")
        numIterations_stepCalculation: Number of iterations for step size calculation (only used if alpha is "auto")
        potential_type: Type of potential function to use
        potential_shape: Neighborhood shape (PotentialShapeType enum)
        potential_radius: Neighborhood radius in pixels
        preconditioner_type: Type of preconditioner to use (PreconditionerType enum)  
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
    Z, X = SMatrix.Z, SMatrix.X
    ZX = Z * X

    if SMatrix.T != y.shape[0] or SMatrix.N != y.shape[1]:
        raise ValueError(f"[AOT-biomaps] Shape mismatch: y={y.shape}, SMatrix T={SMatrix.T}, N={SMatrix.N}.")

    y_flat = xp.asarray(y.T.flatten(), dtype=xp.float32)
    
    # FISTA specific variables
    x_flat = xp.full(ZX, 0.1, dtype=xp.float32) # The actual image
    z_flat = xp.full(ZX, 0.1, dtype=xp.float32) # The extrapolation point
    t = 1.0 # Momentum tracker
    
    residual_buffer = xp.empty_like(y_flat)

    if alpha == "auto":
        eta_val = eta if eta is not None else 1.0
        alpha_data = calculate_step_size(SMatrix, eta_val, numIterations_stepCalculation, show_logs=False)
        L_A = eta_val / alpha_data
        L_prior = 8.0 * beta * (potential_radius ** 2) if potential_type != PotentialType.NONE else 0.0
        alpha_val = eta_val / (L_A + L_prior)
    else:
        alpha_val = alpha

    if preconditioner_type != PreconditionerType.NONE:
        if show_logs: print(f"[AOT-biomaps] preconditionning calculation : {preconditioner_type.name}...")
        preconditioner = build_preconditioner(SMatrix, preconditioner_type)
        preconditioner /= xp.max(preconditioner)
        alpha_vec = alpha_val / (preconditioner + 1e-8)
        alpha_vec = alpha_vec.astype(xp.float32)
    else:
        alpha_vec = xp.full(ZX, alpha_val, dtype=xp.float32)

    save_indices = np.unique(np.append(np.arange(0, numIterations, max(1, numIterations // max_saves)), numIterations - 1)).tolist()

    saved_lambda = []
    saved_indices_list = []
    cost_history = [] if isCostFunction else None
    window_history = []

    prec_str = "Precond" if preconditioner_type != PreconditionerType.NONE else "NoPrecond"
    description = f"[AOT-biomaps] FISTA-{prec_str} ({SMatrix.matrix_type.name}) with {potential_type.name} β={beta} ---- {'WITH' if withTumor else 'WITHOUT'} TUMOR"
    iterator = trange(numIterations, desc=description) if show_logs else range(numIterations)

    for it in iterator:
        x_old = x_flat.copy() if stop_criterion != StopCriterionType.MAX_ITERATIONS or is_gpu else x_flat.copy()
        q_flat = forward_projection(SMatrix, z_flat)
        xp.subtract(q_flat, y_flat, out=residual_buffer)

        grad_U, _, _ = get_potential_function(potential_type, SMatrix, z_flat, beta=beta, delta=delta, shape=potential_shape, radius=potential_radius, compute_grad=True, compute_hess=False, compute_energy=isCostFunction, use_surrogate_hessian=False)
  
        grad_fidelity = backward_projection(SMatrix, residual_buffer)
        total_grad = grad_fidelity + grad_U

        # Momentum Update (Nesterov)
        t_next = (1.0 + np.sqrt(1.0 + 4.0 * t * t)) / 2.0
        momentum = (t - 1.0) / t_next

        # FISTA Update (Gradient step + Clamp + Extrapolation)
        if is_gpu:
            fista_update_kernel(x_old, z_flat, total_grad.astype(xp.float32, copy=False), alpha_vec, float(momentum), x_flat, z_flat)
        else:
            x_flat = z_flat - alpha_vec * total_grad
            np.maximum(x_flat, 0.0, out=x_flat)
            z_flat = x_flat + float(momentum) * (x_flat - x_old)
            
        t = t_next

        if isCostFunction:
            Ax = forward_projection(SMatrix, x_flat)
            _, _, U_x = get_potential_function(potential_type, SMatrix, x_flat, beta=beta, delta=delta, shape=potential_shape, radius=potential_radius, compute_grad=False, compute_hess=False, compute_energy=True, use_surrogate_hessian=False)
            ls_cost = 0.5 * float(xp.vdot(Ax - y_flat, Ax - y_flat))
            cost_history.append(ls_cost + U_x)

        if stop_criterion != StopCriterionType.MAX_ITERATIONS:
            ground_truth = SMatrix.experiment.OpticImage.phantom if withTumor else SMatrix.experiment.OpticImage.laser.intensity
            gradient_for_stop = total_grad if stop_criterion == StopCriterionType.GRADIENT_NORM else None
            isStop, val = check_stopping_criterion(SMatrix, x_flat, x_old, stop_criterion, stop_threshold, window_size=stop_window_size, history=cost_history, ground_truth=ground_truth, gradient=gradient_for_stop, window_history=window_history)
            if show_logs and show_criterion:
                iterator.set_postfix_str(f"{stop_criterion.name}: {val:.2e}")
            if isStop:
                if show_logs: print(f"\n[AOT-biomaps] Stopping Criterion {stop_criterion.name} reached at iteration {it}.")
                cost_history.pop() if isCostFunction else None
                break
            
        if isSavingEachIteration and it in save_indices:
            saved_lambda.append(x_flat.reshape(Z, X).get() if is_gpu else x_flat.reshape(Z, X).copy())
            saved_indices_list.append(it)

    final_result = x_flat.reshape(Z, X).get() if is_gpu else x_flat.reshape(Z, X)
    return (saved_lambda, saved_indices_list, cost_history) if isSavingEachIteration else (final_result, None, cost_history)