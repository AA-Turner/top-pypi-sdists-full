"""
PGC.py

Penalized Gauss-Newton Conjugate Gradient (PGC) reconstruction algorithm.
Uses unified SMatrix interface and ReconTools functions.
Single unified function that works with any SMatrix type (CSR, SELL, DENSE) and any device (CPU, GPU).

Supports potential functions: QUADRATIC, HUBER, RELATIVE_DIFFERENCE
"""

import numpy as np
from tqdm import trange
from typing import Optional, Union, Tuple

from AOT_biomaps.AOT_Recon.ReconTools import (
    check_gpu_available, forward_projection, backward_projection, 
    clamp_positive, get_potential_function, cost_function, _get_array_module, estimate_operator_norm
)
from AOT_biomaps.AOT_Recon.ReconEnums import OptimizerType, PotentialType
from AOT_biomaps.AOT_Recon.AOT_SMatrix.SMatrix_SELL import SMatrix_SELL
from AOT_biomaps.AOT_Recon.AOT_SMatrix.SMatrix_CSR import SMatrix_CSR
from AOT_biomaps.AOT_Recon.AOT_SMatrix.SMatrix_DENSE import SMatrix_DENSE

# Check for CuPy availability
try:
    import cupy as cp
    CUPY_AVAILABLE = True
except ImportError:
    CUPY_AVAILABLE = False


def PGC(
    SMatrix: Union['SMatrix_DENSE', 'SMatrix_CSR', 'SMatrix_SELL'],
    y: Union[np.ndarray, 'cp.ndarray'],
    numIterations: int = 100,
    alpha: float = 0.05,     # Step size (learning rate)
    beta: float = 1.0,       # Regularization weight
    delta: float = 0.01,     # Parameter for potential function
    eta: Optional[float] = None, # Parameter for the Lipschitz constant estimation (must be < 2 for convergence and > 1 for faster convergence). Useless if alpha is a float.
    potential_type: PotentialType = PotentialType.QUADRATIC,
    isSavingEachIteration: bool = True,
    isCostFunction: bool = False,
    withTumor: bool = True,
    max_saves: int = 5000,
    show_logs: bool = True,
) -> Tuple[Union[np.ndarray, list], Optional[list], Optional[list]]:
    """
    Penalized Gauss-Newton Conjugate Gradient (PGC) reconstruction algorithm.
    Uses the Polak-Ribière conjugate direction method to accelerate convergence.
    
    Args:
        SMatrix: System matrix object.
        y: Measurement data vector.
        numIterations: Total number of iterations.
        alpha: Step size (learning rate). If set to "auto" 
        beta: Regularization weight parameter.
        delta: Threshold for non-quadratic potentials.
        eta: Parameter for the Lipschitz constant estimation (must be < 2 for convergence and > 1 for faster convergence). Useless if alpha is a float.
        potential_type: Type of potential function to use.
        isSavingEachIteration: If True, stores intermediate reconstructions.
        isCostFunction: If True, tracks the cost function history.
        withTumor: Flag for description.
        max_saves: Limit on stored iterations.
        show_logs: Displays tqdm progress bar.
    """
    tumor_str = "WITH" if withTumor else "WITHOUT"
    device = SMatrix.device
    matrix_type = SMatrix.matrix_type.name
    xp = _get_array_module(SMatrix)
    Z, X = SMatrix.Z, SMatrix.X
    ZX = Z * X

    if SMatrix.T != y.shape[0] or SMatrix.N != y.shape[1]:
        raise ValueError(f"Shape mismatch: y={y.shape}, SMatrix T={SMatrix.T}, N={SMatrix.N}.")

    y_flat = xp.asarray(y.T.flatten().astype(xp.float32))
    lambda_flat = xp.full(ZX, 0.1, dtype=xp.float32)

    # Conjugate Gradient vectors: r (residual), d (direction)
    r = xp.zeros_like(lambda_flat)
    d = xp.zeros_like(lambda_flat)
    prev_r_dot = 0.0

    if alpha == "auto":
        if eta is None:
            print("Warning: eta is not set for power method estimation of step size. Using default value of 1.9.")
            eta = 1.9
        if eta >= 2.0 or eta <= 1.0:
            print(f"Warning: For power method estimation of step size, eta should be in (1.0, 2.0) for convergence and faster convergence. Current value: {eta}. Proceeding with the given value, but consider adjusting it for better performance.")
        # Estimate Lipschitz constant using power method
        L_estimate = estimate_operator_norm(SMatrix, num_iters=20)
        alpha = eta / L_estimate if L_estimate > 0 else 1.0
        print(f"Estimated Lipschitz constant: {L_estimate:.4f}, using step size alpha: {alpha:.5f}")


    save_indices = list(range(0, numIterations, max(1, numIterations // max_saves)))
    if save_indices[-1] != numIterations - 1:
        save_indices.append(numIterations - 1)

    saved_lambda = []
    saved_indices_list = []
    cost_history = [] if isCostFunction else None

    description = f"AOT-BioMaps -- PGC ({matrix_type}) ---- {tumor_str} TUMOR ---- {device.upper()}"
    iterator = trange(numIterations, desc=description) if show_logs else range(numIterations)

    for it in iterator:
        # 1. Forward model
        q_flat = forward_projection(SMatrix, lambda_flat)
        
        # 2. Compute potential gradient
        _, grad_U, U_value = get_potential_function(potential_type, SMatrix, lambda_flat, beta=beta, delta=delta)
        if grad_U is None: 
            grad_U = xp.zeros_like(lambda_flat)
            U_value = 0.0

        if isCostFunction:
            q_safe = xp.maximum(q_flat, 1e-10)
            cost_history.append(float(xp.sum(q_safe - y_flat * xp.log(q_safe)) + U_value))

        # 3. Compute Gauss-Newton gradient: A^T * (Ax - y) + grad_U
        residual = q_flat - y_flat
        grad_f = backward_projection(SMatrix, residual) + grad_U
        
        # 4. Conjugate Gradient Update (Polak-Ribière)
        r = -grad_f
        r_dot = xp.sum(r * r)
        
        if it == 0:
            d = r
        else:
            # Conjugacy factor (beta_cg)
            beta_cg = xp.maximum(0, r_dot / (prev_r_dot + 1e-10))
            d = r + beta_cg * d
        
        # 5. Search step
        lambda_flat = lambda_flat + alpha * d
        lambda_flat = clamp_positive(SMatrix, lambda_flat)
        
        prev_r_dot = r_dot

        if isSavingEachIteration and it in save_indices:
            saved_lambda.append(lambda_flat.reshape(Z, X).get() if hasattr(lambda_flat, 'get') else lambda_flat.reshape(Z, X).copy())
            saved_indices_list.append(it)

    final_result = lambda_flat.reshape(Z, X).get() if hasattr(lambda_flat, 'get') else lambda_flat.reshape(Z, X)

    return (saved_lambda, saved_indices_list, cost_history) if isSavingEachIteration else (final_result, None, cost_history)