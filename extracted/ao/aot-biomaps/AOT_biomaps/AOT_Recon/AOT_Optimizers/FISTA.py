"""
FISTA.py

Fast Iterative Shrinkage-Thresholding Algorithm (Accelerated PGD).
The absolute State-of-the-Art for Regularized Least Squares (Gaussian noise) with positivity constraints.

Uses unified SMatrix interface and ReconTools functions.
Single unified function that works with any SMatrix type (CSR, SELL, DENSE) and any device (CPU, GPU).
"""

import numpy as np
from tqdm import trange
from typing import Optional, Union, Tuple

from AOT_biomaps.AOT_Recon.ReconTools import get_array_module, forward_projection, backward_projection, get_potential_function, check_stopping_criterion, calculate_step_size
from AOT_biomaps.AOT_Recon.ReconEnums import PotentialType, PotentialShapeType, StopCriterionType
from AOT_biomaps.AOT_Recon.AOT_SMatrix.SMatrix_SELL import SMatrix_SELL
from AOT_biomaps.AOT_Recon.AOT_SMatrix.SMatrix_CSR import SMatrix_CSR
from AOT_biomaps.AOT_Recon.AOT_SMatrix.SMatrix_DENSE import SMatrix_DENSE

# Check for CuPy availability
try:
    import cupy as cp
    CUPY_AVAILABLE = True

    # =====================================================================
    # HIGH-PRECISION FUSED KERNEL FOR FISTA (Zero-Allocation)
    # =====================================================================
    fista_update_kernel = cp.ElementwiseKernel(
        'float32 x_old, float32 z_in, float32 grad, float32 alpha, float32 momentum',
        'float32 x_new, float32 z_out',
        '''
        // 1. Standard PGD Step from the extrapolation point (z)
        double step = (double)z_in - (double)alpha * (double)grad;
        
        // 2. Proximal operator: Positivity constraint (Clamp)
        double x_val = step > 0.0 ? step : 0.0;
        x_new = (float)x_val;
        
        // 3. Nesterov Acceleration (Momentum)
        z_out = (float)(x_val + (double)momentum * (x_val - (double)x_old));
        ''',
        'fista_update_kernel'
    )
except ImportError:
    CUPY_AVAILABLE = False


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
    
    xp = get_array_module(SMatrix)
    is_gpu = (xp.__name__ == 'cupy')
    Z, X = SMatrix.Z, SMatrix.X
    ZX = Z * X

    if SMatrix.T != y.shape[0] or SMatrix.N != y.shape[1]:
        raise ValueError(f"Shape mismatch: y={y.shape}, SMatrix T={SMatrix.T}, N={SMatrix.N}.")

    y_flat = xp.asarray(y.T.flatten(), dtype=xp.float32)
    
    # FISTA specific variables
    x_flat = xp.full(ZX, 0.1, dtype=xp.float32) # The actual image
    z_flat = xp.full(ZX, 0.1, dtype=xp.float32) # The extrapolation point
    t = 1.0 # Momentum tracker
    
    residual_buffer = xp.empty_like(y_flat)

    # For FISTA (Least Squares), alpha is strictly 1/L. 
    # The power method (calculate_step_size) is perfect here.
    if alpha == "auto":
        eta_val = eta if eta is not None else 1.0
        
        # 1. On calcule le pas "de base" lié uniquement à la matrice système A
        alpha_data = calculate_step_size(SMatrix, eta_val, numIterations_stepCalculation, show_logs=False)
        
        # 2. On retrouve la constante de Lipschitz de la fidélité des données (L_A)
        L_A = eta_val / alpha_data
        
        # 3. On calcule la constante de Lipschitz de la régularisation spatiale
        # Pour le gradient discret en 2D (voisinage en croix), L = 8. 
        # On ajoute le rayon pour garantir la stabilité sur les grands voisinages.
        L_prior = 8.0 * beta * (potential_radius ** 2) if potential_type != PotentialType.NONE else 0.0
        
        # 4. On calcule le pas global strict pour empêcher l'explosion
        alpha_val = eta_val / (L_A + L_prior)
        
        if show_logs:
            print(f"[FISTA Step Size] L_A: {L_A:.2e} | L_prior: {L_prior:.2e} | Alpha sécurisé: {alpha_val:.5e}")
    else:
        alpha_val = alpha

    save_indices = np.unique(np.append(np.arange(0, numIterations, max(1, numIterations // max_saves)), numIterations - 1)).tolist()

    saved_lambda = []
    saved_indices_list = []
    cost_history = [] if isCostFunction else None
    window_history = []

    description = f"AOT-BioMaps -- FISTA ({SMatrix.matrix_type.name}) with {potential_type.name} β={beta} ---- {'WITH' if withTumor else 'WITHOUT'} TUMOR"
    iterator = trange(numIterations, desc=description) if show_logs else range(numIterations)

    for it in iterator:
        x_old = x_flat.copy() if stop_criterion != StopCriterionType.MAX_ITERATIONS or is_gpu else x_flat.copy()
        
        # 1. Forward Projection from the extrapolated point Z
        q_flat = forward_projection(SMatrix, z_flat)
        
        # 2. Least Squares Residual (Az - y)
        if is_gpu:
            cp.subtract(q_flat, y_flat, out=residual_buffer)
        else:
            np.subtract(q_flat, y_flat, out=residual_buffer)

        # 3. Dynamic Potential Gradient evaluated at Z
        grad_U, _, U_value = get_potential_function(
            potential_type, SMatrix, z_flat, beta=beta, delta=delta, 
            shape=potential_shape, radius=potential_radius, 
            compute_grad=True, compute_hess=False, compute_energy=isCostFunction,
            use_surrogate_hessian=False
        )
  
        # 4. Global Gradient of Least Squares Fidelity
        grad_fidelity = backward_projection(SMatrix, residual_buffer)
        total_grad = grad_fidelity + grad_U

        # 5. Momentum Update (Nesterov)
        t_next = (1.0 + np.sqrt(1.0 + 4.0 * t * t)) / 2.0
        momentum = (t - 1.0) / t_next

        # 6. FISTA Update (Gradient step + Clamp + Extrapolation)
        if is_gpu:
            # Shielded outputs to prevent TypeMismatch
            fista_update_kernel(
                x_old, 
                z_flat, 
                total_grad.astype(xp.float32, copy=False), 
                float(alpha_val), 
                float(momentum), 
                x_flat, 
                z_flat
            )
        else:
            # Fallback CPU
            x_flat = z_flat - float(alpha_val) * total_grad
            np.maximum(x_flat, 0.0, out=x_flat)
            z_flat = x_flat + float(momentum) * (x_flat - x_old)
            
        t = t_next


        if isCostFunction:
            # On calcule le coût exact sur l'image réelle x_flat à chaque itération
            Ax = forward_projection(SMatrix, x_flat)
            _, _, U_x = get_potential_function(
                potential_type, SMatrix, x_flat, beta=beta, delta=delta, 
                shape=potential_shape, radius=potential_radius, 
                compute_grad=False, compute_hess=False, compute_energy=True, use_surrogate_hessian=False
            )
            ls_cost = 0.5 * float(xp.vdot(Ax - y_flat, Ax - y_flat))
            cost_history.append(ls_cost + U_x)

        # 8. Stopping Criterion
        if stop_criterion != StopCriterionType.MAX_ITERATIONS:
            ground_truth = SMatrix.experiment.OpticImage.phantom if withTumor else SMatrix.experiment.OpticImage.laser.intensity
            gradient_for_stop = total_grad if stop_criterion == StopCriterionType.GRADIENT_NORM else None
            isStop, val = check_stopping_criterion(
                SMatrix, x_flat, x_old, stop_criterion, stop_threshold, 
                window_size=stop_window_size, history=cost_history, 
                ground_truth=ground_truth, gradient=gradient_for_stop, window_history=window_history
            )
            if show_logs and show_criterion:
                iterator.set_postfix_str(f"{stop_criterion.name}: {val:.2e}")
            if isStop:
                if show_logs: print(f"\n[Stopping] Criterion {stop_criterion.name} reached at iteration {it}.")
                break
            
        if isSavingEachIteration and it in save_indices:
            saved_lambda.append(x_flat.reshape(Z, X).get() if is_gpu else x_flat.reshape(Z, X).copy())
            saved_indices_list.append(it)

    final_result = x_flat.reshape(Z, X).get() if is_gpu else x_flat.reshape(Z, X)
    return (saved_lambda, saved_indices_list, cost_history) if isSavingEachIteration else (final_result, None, cost_history)