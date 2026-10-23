from __future__ import annotations

"""
LBFGS.py

Limited-Memory BFGS (L-BFGS) reconstruction for AOT-BioMaps.

This implementation uses a Two-Metric Projected L-BFGS directly in the image 
space to enforce non-negativity (lambda >= 0). This approach preserves the 
problem's convexity and Hessian conditioning while requiring only ONE forward 
projection per iteration via a feasible-direction exact quadratic line search.

All docstrings and comments are provided in English for consistency.
"""

import numpy as np
from tqdm import trange
from typing import Optional, Union, Tuple

from AOT_biomaps.AOT_Recon.ReconTools import (
    ensure_device, get_array_module, get_device_context,
    forward_projection, backward_projection, get_potential_function,
    check_stopping_criterion, estimate_lipschitz_constant
)
from AOT_biomaps.AOT_Recon.ReconEnums import PotentialType, PotentialShapeType, StopCriterionType
from AOT_biomaps.AOT_Recon.AOT_Preconditioner.PreconditionerEnums import PreconditionerType
from AOT_biomaps.AOT_Recon.AOT_Preconditioner.NoPreconditioner import NoPreconditioner
from AOT_biomaps.AOT_Recon.AOT_Preconditioner.DiagPreconditioner import DiagPreconditioner
from AOT_biomaps.AOT_Recon.AOT_SMatrix.SMatrix_SELL import SMatrix_SELL
from AOT_biomaps.AOT_Recon.AOT_SMatrix.SMatrix_CSR import SMatrix_CSR
from AOT_biomaps.AOT_Recon.AOT_SMatrix.SMatrix_DENSE import SMatrix_DENSE

try:
    import cupy as cp
    CUPY_AVAILABLE = True
except ImportError:
    cp = None
    CUPY_AVAILABLE = False


def _calibrate_prior_LBFGS(
    SMatrix,
    y_flat,
    potential_type: PotentialType,
    potential_shape: PotentialShapeType,
    potential_radius: int,
    delta_phys: float = 2.0,
    num_warmup: int = 10,
    show_logs: bool = False
):
    """
    Performs a warm-up reconstruction to measure the data gradient scale (G_f),
    the prior gradient scale on flat regions (G_U), and the typical image amplitude (amp).
    
    This allows dimensionless scaling of the regularization parameter (beta) across
    different datasets and geometries.
    """
    xp = get_array_module(SMatrix)
    ZX = SMatrix.Z * SMatrix.X

    lambda_w = xp.zeros(ZX, dtype=xp.float32)
    grad_f = None

    # 10 steps of non-negative Cauchy steepest descent to reach the working image scale
    for _ in range(num_warmup):
        Ax = forward_projection(SMatrix, lambda_w)
        res = Ax - y_flat
        grad_f = xp.ascontiguousarray(xp.real(backward_projection(SMatrix, res)), dtype=xp.float32)
        Ag = forward_projection(SMatrix, grad_f)
        g_norm2 = float(xp.vdot(grad_f, grad_f).real)
        Ag_norm2 = float(xp.vdot(Ag, Ag).real)
        alpha_c = g_norm2 / max(Ag_norm2, 1e-20)
        lambda_w = xp.maximum(lambda_w - np.float32(alpha_c) * grad_f, 0.0)

    if grad_f is None:
        return 1.0, 1.0, 1.0, 1e-6

    G_f = float(xp.linalg.norm(grad_f))
    pos = lambda_w[lambda_w > 0]
    amp = float(xp.mean(pos)) if pos.size > 0 else 1.0
    eps_rel_auto = max(1e-4 / max(amp, 1e-6), 1e-6)
    eps_rd = eps_rel_auto * 2.0 * amp

    if potential_type == PotentialType.RELATIVE_DIFFERENCE:
        # CRITICAL NUYTS 2002 PROPERTY:
        # Calibrate G_U at gamma = 0.0 (pure quadratic relative difference d^2 / s).
        # This locks the smoothing strength on flat/noisy regions (|d| << s) to `beta`,
        # so that varying `delta` (gamma) ONLY controls edge preservation without
        # rescaling beta_int by gamma!
        grad_U1, _, _ = get_potential_function(
            potential_type, SMatrix, lambda_w,
            beta=1.0, delta=0.0, eps_rd=eps_rd,
            shape=potential_shape, radius=potential_radius,
            compute_grad=True, compute_hess=False, compute_energy=False
        )
    else:
        delta_cal = delta_phys * amp if potential_type == PotentialType.HUBER else delta_phys
        grad_U1, _, _ = get_potential_function(
            potential_type, SMatrix, lambda_w,
            beta=1.0, delta=delta_cal, eps_rd=eps_rd,
            shape=potential_shape, radius=potential_radius,
            compute_grad=True, compute_hess=False, compute_energy=False
        )

    G_U = float(xp.linalg.norm(grad_U1))
    if G_U <= 0.0:
        if show_logs:
            print("[AOT-biomaps] Warning: prior gradient scale is zero on warm-up image.")
        G_U = 1.0

    return G_f, G_U, amp, eps_rd


def LBFGS(
    SMatrix: Union['SMatrix_DENSE', 'SMatrix_CSR', 'SMatrix_SELL'],
    y: Union[np.ndarray, 'cp.ndarray'],
    numIterations: int = 100,
    beta: float = 0.1,
    delta: float = 2.0,
    potential_type: PotentialType = PotentialType.QUADRATIC,
    potential_shape: PotentialShapeType = PotentialShapeType.CROSS,
    potential_radius: int = 2,
    preconditioner_type: PreconditionerType = PreconditionerType.NONE,
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
    numIterations_stepCalculation: int = 15,
) -> Tuple[Union[np.ndarray, list], Optional[list], Optional[list]]:
    """
    Projected L-BFGS Optimizer with exact float64 polynomial line search.

    Args:
        beta (float): Regularization strength (dimensionless, typically [0.01, 1.0]).
        delta (float): Edge-preservation parameter:
            - HUBER: relative threshold as a fraction of image amplitude (e.g., 0.05).
            - RELATIVE_DIFFERENCE: dimensionless gamma parameter of Nuyts 2002 (typ. [1.0, 20.0]).
        numIterations_stepCalculation (int): Used here to define the L-BFGS memory 
            history size (commonly denoted as 'm'). Renamed to align with the 
            naming convention of other algorithms in the suite (default 15).
        ... (other standard parameters mirror the overarching framework).
    """
    ensure_device(SMatrix, device, show_logs=show_logs)
    xp = get_array_module(SMatrix)
    is_gpu = (xp.__name__ == 'cupy')

    with get_device_context(SMatrix):
        Z, X = SMatrix.Z, SMatrix.X
        ZX = Z * X

        if SMatrix.T != y.shape[0] or SMatrix.N != y.shape[1]:
            raise ValueError(f"[AOT-biomaps] Shape mismatch: y={y.shape}, SMatrix T={SMatrix.T}, N={SMatrix.N}.")

        data_dtype = xp.complex64 if SMatrix.isComplexSMatrix else xp.float32

        # 1. Data normalization (similar to FISTA)
        y_max = float(np.max(np.abs(y))) if SMatrix.isComplexSMatrix else float(np.max(y))
        y_norm = y / y_max if y_max > 0 else y
        y_flat = xp.asarray(y_norm.T.flatten().astype(data_dtype))

        # 2. Optional diagonal preconditioner (acts as the initial metric H_0)
        if preconditioner_type == PreconditionerType.DIAGONAL:
            preconditioner = DiagPreconditioner(SMatrix=SMatrix)
            preconditioner.build()
        else:
            preconditioner = NoPreconditioner(SMatrix=SMatrix)

        # 3. Dimensionless calibration of beta and image scale
        beta_phys = float(beta)
        delta_phys = float(delta)

        if potential_type == PotentialType.NONE or beta_phys == 0.0:
            beta_int = 0.0
            delta_int = 0.0
            G_f, G_U, amp, eps_rd = 1.0, 1.0, 1.0, 1e-6
        else:
            G_f, G_U, amp, eps_rd = _calibrate_prior_LBFGS(
                SMatrix, y_flat, potential_type, potential_shape, potential_radius,
                delta_phys=delta_phys, num_warmup=5, show_logs=show_logs
            )
            beta_int = beta_phys * G_f / G_U
            delta_int = delta_phys * amp if potential_type == PotentialType.HUBER else delta_phys

        if show_logs:
            print(f"[AOT-biomaps] L-BFGS (PROJECTED) | β_phys={beta_phys:.2e} -> β_int={beta_int:.3e} "
                  f"(G_f={G_f:.2e}, G_U={G_U:.2e}, amp={amp:.2e}) | γ/δ_int={delta_int:.2e} | ε_rd={eps_rd:.2e}")

        # 4. Initialization at the estimated physical scale
        lambda_flat = xp.zeros(ZX, dtype=xp.float32)

        # L-BFGS Memory buffers
        s_history = []
        y_history = []
        rho_history = []

        save_indices = np.unique(
            np.append(np.arange(0, numIterations, max(1, numIterations // max_saves)), numIterations - 1)
        ).tolist()
        saved_lambda = []
        saved_indices_list = []
        track_cost = isCostFunction or stop_criterion == StopCriterionType.COST_FUNCTION
        cost_history = [] if track_cost else None
        window_history = []

        # --- Initial evaluation (iteration 0) ---
        Ax = forward_projection(SMatrix, lambda_flat)
        residual = Ax - y_flat
        grad_f_lam = xp.ascontiguousarray(xp.real(backward_projection(SMatrix, residual)), dtype=xp.float32)

        grad_U_lam, _, U_val = get_potential_function(
            potential_type, SMatrix, lambda_flat,
            beta=beta_int, delta=delta_int, eps_rd=eps_rd,
            shape=potential_shape, radius=potential_radius,
            compute_grad=True, compute_hess=False, compute_energy=True
        )
        grad_lam = grad_f_lam + grad_U_lam
        fidelity_cost = 0.5 * float(xp.vdot(residual, residual).real)
        current_cost = fidelity_cost + (float(U_val) if U_val is not None else 0.0)

        iterator = trange(numIterations, desc=f"[AOT-biomaps] L-BFGS (Projected)", disable=not show_logs)

        # ==========================================================
        # MAIN L-BFGS LOOP
        # ==========================================================
        for it in iterator:
            prev_lambda = lambda_flat.copy()
            if cost_history is not None:
                cost_history.append(current_cost)

            # ------------------------------------------------------
            # 1. EFFECTIVE GRADIENT & ACTIVE CONSTRAINTS
            # ------------------------------------------------------
            # Active set: pixels stuck at 0 with a gradient pushing them negative
            active_mask = (lambda_flat <= 1e-12) & (grad_lam > 0.0)
            g_eff = xp.where(active_mask, 0.0, grad_lam)

            g_eff_norm = float(xp.linalg.norm(g_eff))
            if g_eff_norm < 1e-12:
                if show_logs:
                    print(f"\n[AOT-biomaps] Optimality reached at it={it} (||g_eff||₂ = {g_eff_norm:.2e}).")
                break

            # ------------------------------------------------------
            # 2. TWO-LOOP L-BFGS RECURSION
            # ------------------------------------------------------
            q = g_eff.copy()
            alphas = []

            for s_i, y_i, rho_i in zip(reversed(s_history), reversed(y_history), reversed(rho_history)):
                alpha_i = rho_i * float(xp.vdot(s_i, q).real)
                alphas.append(alpha_i)
                q -= np.float32(alpha_i) * y_i

            alphas.reverse()

            # Initial scaling H_0 = gamma_k * P^-1
            if len(s_history) > 0:
                sy = float(xp.vdot(s_history[-1], y_history[-1]).real)
                yy = float(xp.vdot(y_history[-1], y_history[-1]).real)
                gamma_k = sy / max(yy, 1e-20)
            else:
                # Exact Cauchy step scaling at iteration 0 (avoids arbitrary step sizes)
                Ag0 = forward_projection(SMatrix, g_eff)
                gamma_k = (g_eff_norm ** 2) / max(float(xp.vdot(Ag0, Ag0).real), 1e-20)

            d = np.float32(gamma_k) * preconditioner.apply_inverse(q)

            for s_i, y_i, rho_i, alpha_i in zip(s_history, y_history, rho_history, alphas):
                beta_i = rho_i * float(xp.vdot(y_i, d).real)
                d += s_i * np.float32(alpha_i - beta_i)

            d = -d

            # Two-metric Bertsekas projection onto the tangent cone
            # 1) Pixels in the active set remain locked
            d = xp.where(active_mask, 0.0, d)
            # 2) If a pixel is at 0 and its gradient is negative (needs to increase), 
            #    but the L-BFGS coupling gave d <= 0, we override it with the projected gradient direction
            blocked_unactive = (lambda_flat <= 1e-12) & (grad_lam < 0.0) & (d <= 0.0)
            d = xp.where(blocked_unactive, -np.float32(gamma_k) * grad_lam, d)

            # Check angle between -g_eff and d
            d_norm = float(xp.linalg.norm(d))
            dir_deriv = float(xp.vdot(g_eff, d).real)
            cos_gd = -dir_deriv / max(g_eff_norm * d_norm, 1e-20)

            # If d is not a strict descent direction (cos < 1e-5), reset H_k memory
            if dir_deriv >= 0.0 or cos_gd < 1e-5:
                s_history.clear()
                y_history.clear()
                rho_history.clear()
                d = -np.float32(gamma_k) * g_eff
                d_norm = float(xp.linalg.norm(d))
                dir_deriv = float(xp.vdot(g_eff, d).real)

            # ------------------------------------------------------
            # 3. EXACT FLOAT64 POLYNOMIAL ARMIJO LINE SEARCH
            # ------------------------------------------------------
            c1_armijo = 1e-4
            step = 1.0
            max_ls_iter = 25
            ls_accepted = False

            # Projected feasible direction: Delta_lambda = max(0, lambda + alpha_0 * d) - lambda
            # If alpha_0 = 1.0 crushes the direction too much (directional derivative >= 0),
            # we back-track alpha_0 in the image space directly (requires 0 forward projections!)
            alpha_0 = 1.0
            for _ in range(10):
                delta_lam = xp.maximum(lambda_flat + np.float32(alpha_0) * d, 0.0) - lambda_flat
                dir_deriv_proj = float(xp.vdot(grad_lam, delta_lam).real)
                if dir_deriv_proj < 0.0:
                    break
                alpha_0 *= 0.5
            else:
                delta_lam = xp.maximum(lambda_flat - np.float32(gamma_k) * g_eff, 0.0) - lambda_flat
                dir_deriv_proj = float(xp.vdot(grad_lam, delta_lam).real)

            # ONLY ONE forward projection is needed for the entire Line Search routine!
            q1 = forward_projection(SMatrix, delta_lam)

            # Exact float64 coefficients for the quadratic polynomial ΔJ_data(step) = c1*step + c2*step^2
            c1_poly = float(xp.vdot(residual, q1).real)
            c2_poly = 0.5 * float(xp.vdot(q1, q1).real)

            for ls_it in range(max_ls_iter):
                lam_probe = xp.maximum(lambda_flat + np.float32(step) * delta_lam, 0.0)
                _, _, U_probe = get_potential_function(
                    potential_type, SMatrix, lam_probe,
                    beta=beta_int, delta=delta_int, eps_rd=eps_rd,
                    shape=potential_shape, radius=potential_radius,
                    compute_grad=False, compute_hess=False, compute_energy=True
                )
                delta_data_cost = c1_poly * step + c2_poly * (step * step)
                delta_prior_cost = (float(U_probe) if U_probe is not None else 0.0) - (float(U_val) if U_val is not None else 0.0)
                delta_total_cost = delta_data_cost + delta_prior_cost

                if delta_total_cost <= c1_armijo * step * dir_deriv_proj + 1e-12 * abs(current_cost):
                    lambda_new = lam_probe
                    res_new = residual + np.float32(step) * q1
                    U_val_new = U_probe
                    new_cost = current_cost + delta_total_cost
                    ls_accepted = True
                    break
                step *= 0.5

            # If the line search fails despite float64 precision:
            # Clear L-BFGS memory and attempt a Cauchy step before giving up
            if not ls_accepted:
                if len(s_history) > 0:
                    s_history.clear()
                    y_history.clear()
                    rho_history.clear()
                    continue
                else:
                    if show_logs:
                        print(f"\n[AOT-biomaps] Line search hit precision floor at iteration {it}. Stopping.")
                    break

            # ------------------------------------------------------
            # 4. GRADIENT UPDATES & CAUTIOUS L-BFGS MEMORY
            # ------------------------------------------------------
            grad_f_new = xp.ascontiguousarray(xp.real(backward_projection(SMatrix, res_new)), dtype=xp.float32)
            grad_U_new, _, _ = get_potential_function(
                potential_type, SMatrix, lambda_new,
                beta=beta_int, delta=delta_int, eps_rd=eps_rd,
                shape=potential_shape, radius=potential_radius,
                compute_grad=True, compute_hess=False, compute_energy=False
            )
            grad_lam_new = grad_f_new + grad_U_new

            s_k = lambda_new - lambda_flat
            
            # Difference of gradients restricted to the free subspace
            free_mask = ~((lambda_new <= 1e-12) & (lambda_flat <= 1e-12))
            y_k = xp.where(free_mask, grad_lam_new - grad_lam, 0.0)

            curvature = float(xp.vdot(s_k, y_k).real)
            s_norm = float(xp.linalg.norm(s_k))
            y_norm_vec = float(xp.linalg.norm(y_k))
            cos_sy = curvature / max(s_norm * y_norm_vec, 1e-20)

            # Cautious update (Li & Fukushima 2001): Retain existing history if the pair is degenerate
            if cos_sy > 1e-6 and curvature > 1e-20:
                if len(s_history) >= numIterations_stepCalculation:
                    s_history.pop(0)
                    y_history.pop(0)
                    rho_history.pop(0)
                s_history.append(s_k)
                y_history.append(y_k)
                rho_history.append(1.0 / curvature)

            # State transition
            lambda_flat = lambda_new
            grad_lam = grad_lam_new
            residual = res_new
            U_val = U_val_new
            current_cost = new_cost

            # ------------------------------------------------------
            # 5. STOPPING CRITERION
            # ------------------------------------------------------
            if stop_criterion != StopCriterionType.MAX_ITERATIONS:
                if SMatrix.experiment.OpticImage is None:
                    ground_truth = None
                else:
                    ground_truth = (
                        SMatrix.experiment.OpticImage.phantom
                        if withTumor else SMatrix.experiment.OpticImage.laser.intensity
                    )
                gradient_for_stop = g_eff if stop_criterion == StopCriterionType.GRADIENT_NORM else None
                isStop, val = check_stopping_criterion(
                    SMatrix, lambda_flat, prev_lambda, stop_criterion, stop_threshold,
                    window_size=stop_window_size, history=cost_history,
                    ground_truth=ground_truth, gradient=gradient_for_stop,
                    window_history=window_history
                )
                if show_logs and show_criterion:
                    iterator.set_postfix_str(f"{stop_criterion.name}: {val:.2e}")
                if isStop:
                    if show_logs:
                        print(f"\n[AOT-biomaps] Stopping Criterion {stop_criterion.name} reached at iteration {it} (val={val:.2e}).")
                    break

            if isSavingEachIteration and it in save_indices:
                snap = lambda_flat.reshape(Z, X).get() if is_gpu else lambda_flat.reshape(Z, X).copy()
                saved_lambda.append(snap * y_max / SMatrix.normalization_factor)
                saved_indices_list.append(it)

        final_result = lambda_flat.reshape(Z, X).get() if is_gpu else lambda_flat.reshape(Z, X)
        final_result *= y_max / SMatrix.normalization_factor

        return (
            (saved_lambda, saved_indices_list, cost_history if isCostFunction else None)
            if isSavingEachIteration
            else ([final_result], [it + 1], cost_history if isCostFunction else None)
        )