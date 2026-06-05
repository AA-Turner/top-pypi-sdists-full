"""
LS.py

Least Squares reconstruction algorithms.
Uses ReconTools functions for all matrix operations.
Single unified function that works with any SMatrix type (CSR, SELL, DENSE) and any device (CPU, GPU).

Supports preconditioning:
- NONE: No preconditioning
- DIAGONAL: Diagonal preconditioning using A^T * 1
"""
import numpy as np
from tqdm import trange
from typing import Optional, Union, Tuple

from AOT_biomaps.AOT_Recon.ReconTools import get_array_module, forward_projection, backward_projection, clamp_positive, check_stopping_criterion, calculate_step_size, build_preconditioner, apply_preconditioner
from AOT_biomaps.AOT_Recon.ReconEnums import PreconditionerType, StopCriterionType
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
    # Fused Kernel : Update PGD + Clamp (Zero-Allocation)
    pgd_update_kernel = cp.ElementwiseKernel(
        'float32 lam_in, float32 g, float32 alpha',
        'float32 lam_out',
        '''
        float new_val = lam_in + alpha * g;
        lam_out = new_val > 0.0f ? new_val : 0.0f;
        ''',
        'pgd_update_kernel'
    )


def LS(
    SMatrix : Union[SMatrix_DENSE, SMatrix_CSR, SMatrix_SELL],
    y: Union[np.ndarray, 'cp.ndarray'],
    numIterations: int = 100,
    alpha: Union[str, float] = "auto",
    eta: float = 1.9, 
    numIterations_stepCalculation: int = 20,
    preconditioner_type: PreconditionerType = PreconditionerType.NONE,
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
    Least Squares reconstruction using Projected Gradient Descent (PGD).
    
    Uses ReconTools functions for all matrix operations, so it works with
    any SMatrix type (CSR, SELL, DENSE) and any device (CPU, GPU).
    
    Supports potential functions:
        - NONE: No regularization

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
        alpha: Step size parameter (float or 'auto' for power method estimation of Lipschitz constant)
        eta: Parameter for the Lipschitz constant estimation (must be < 2 for convergence and > 1 for faster convergence). Useless if alpha is a float.
        numIterations_stepCalculation: Number of iterations for power method when alpha is "auto"
        preconditioner_type: Type of preconditioner to use (default: NONE)
        stop_criterion: Criterion for stopping the iterations
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

    if SMatrix.T != y.shape[0] or SMatrix.N != y.shape[1]:
        raise ValueError(f"Shape of y {y.shape} does not match SMatrix dimensions (T={SMatrix.T}, N={SMatrix.N}).")

    y_flat = xp.asarray(y.T.flatten().astype(xp.float32))
    lambda_flat = xp.full(ZX, 0.1, dtype=xp.float32)
    residual_buffer = xp.empty_like(y_flat)

    preconditioner = build_preconditioner(SMatrix, preconditioner_type) if preconditioner_type != PreconditionerType.NONE else None

    # Setup save indices
    save_indices = np.unique(np.append(np.arange(0, numIterations, max(1, numIterations // max_saves)), numIterations - 1)).tolist()

    saved_lambda = []
    saved_indices_list = []
    cost_history = [] if isCostFunction else None
    window_history = []


    alpha = calculate_step_size(SMatrix, eta, numIterations_stepCalculation, show_logs) if alpha == "auto" else alpha

    description = f"AOT-BioMaps -- LS ({SMatrix.matrix_type.name}) ---- {'WITH' if withTumor else 'WITHOUT'} TUMOR ---- {SMatrix.device.upper()}"
    iterator = trange(numIterations, desc=description) if show_logs else range(numIterations)

    for it in iterator:
        prev_lambda = lambda_flat.copy()
        q_flat = forward_projection(SMatrix, lambda_flat)
        xp.subtract(y_flat, q_flat, out=residual_buffer)
 
        if isCostFunction:
            cost_history.append(0.5 * float(xp.vdot(residual_buffer, residual_buffer)))

        # Apply preconditioner to gradient (if asked): g = M^-1 * g with g = A^T * (y - A * λ) 
        g_flat = apply_preconditioner(backward_projection(SMatrix, y_flat - q_flat), preconditioner, SMatrix) if preconditioner is not None else backward_projection(SMatrix, y_flat - q_flat)

        # Update: λ = λ + α * (M^-1 * g)
        if is_gpu:
            pgd_update_kernel(lambda_flat, g_flat, float(alpha), lambda_flat)
        else:
            # Fallback CPU in-place
            g_flat *= float(alpha)
            lambda_flat += g_flat
            np.maximum(lambda_flat, 0.0, out=lambda_flat)

        # Stopping Criterion
        if stop_criterion != StopCriterionType.MAX_ITERATIONS:
            ground_truth = SMatrix.experiment.OpticImage.phantom if withTumor else SMatrix.experiment.OpticImage.laser.intensity
            gradient_for_stop = g_flat if stop_criterion == StopCriterionType.GRADIENT_NORM else None
            isStop, val = check_stopping_criterion(SMatrix, lambda_flat, prev_lambda, stop_criterion, stop_threshold, window_size=stop_window_size, history=cost_history, ground_truth=ground_truth, gradient=gradient_for_stop, window_history=window_history)
            if show_logs and show_criterion:
                iterator.set_postfix_str(f"{stop_criterion.name}: {val:.2e}")
            if isStop:
                if show_logs: print(f"\n[Stopping] Criterion {stop_criterion.name} reached at iteration {it}.")
                break

        if isSavingEachIteration and it in save_indices:
            saved_lambda.append(lambda_flat.reshape(Z, X).get() if hasattr(lambda_flat, 'get') else lambda_flat.reshape(Z, X).copy())
            saved_indices_list.append(it)

    final_result = lambda_flat.reshape(Z, X).get() if hasattr(lambda_flat, 'get') else lambda_flat.reshape(Z, X)
    return (saved_lambda, saved_indices_list, cost_history) if isSavingEachIteration else (final_result, None, cost_history)