from __future__ import annotations

"""
FISTA.py

Fast Iterative Shrinkage-Thresholding Algorithm (Accelerated PGD).
Uses unified SMatrix interface and ReconTools functions.
Single unified function that works with any SMatrix type (CSR, SELL, DENSE) and any device (CPU, GPU).

=============================================================================
MATHEMATICAL FRAMEWORK & OPTIMIZATION THEORY:
=============================================================================

1. Objective Function (Regularized Least Squares):
   minimize   F(λ) = 0.5 * ||A * λ - y||_2^2 + β * U(λ)   subject to λ >= 0

2. Dimensionless β Calibration (HOMOGENEOUS REGULARIZATION):
   The user-supplied β (β_phys) is a DIMENSIONLESS relative prior strength:
   β_phys = 1 means the prior gradient has the same magnitude as the data
   gradient (relative scale-free calibration, repeatable across datasets,
   SMatrix normalizations and potential functions).

   Internally, the algorithm measures at runtime:
   - G_f = || P⁻¹ Aᴴ (A λ_w - y) ||   : data gradient scale (preconditioned)
   - G_U = || ∇U_β=1(λ_w) ||          : prior gradient scale at β=1
     both evaluated on a short warm-up reconstruction λ_w (few unregularized
     iterations), and sets:
       β_int = β_phys * G_f / G_U        (so that ||∇U|| ≈ β_phys * ||∇f||)
       δ_int = δ_phys * amp(λ_w)        (Huber threshold in image-amplitude units)

   This removes all dependence on normalization_factor, y_max and matrix
   scaling: β_phys ∈ [0.01, 1] is meaningful and reproducible everywhere.

3. Lipschitz Constant & Adaptive Step Size:
   L_total = L_data + L_prior,   α = 1 / L_total
   - L_data via power iteration (estimate_lipschitz_constant)
   - L_prior via Gershgorin bounds on the potential Hessian (8β etc.)

4. Nesterov Acceleration:
   t_{k+1} = (1 + sqrt(1 + 4 t_k²)) / 2,   λ_bar = λ + momentum * (λ - λ_prev)

5. Proximal / Projected Gradient Step:
   λ_{k+1} = max(0, λ_bar - α ∇F(λ_bar))
=============================================================================
"""
import numpy as np
from tqdm import trange
from typing import Optional, Union, Tuple

from AOT_biomaps.AOT_Recon.ReconTools import ensure_device, get_array_module, get_device_context, forward_projection, backward_projection, get_potential_function, check_stopping_criterion, estimate_lipschitz_constant
from AOT_biomaps.AOT_Recon.ReconEnums import PotentialType, PotentialShapeType, StopCriterionType
from AOT_biomaps.AOT_Recon.AOT_Preconditioner.PreconditionerEnums import PreconditionerType
from AOT_biomaps.AOT_Recon.AOT_Preconditioner.NoPreconditioner import NoPreconditioner
from AOT_biomaps.AOT_Recon.AOT_Preconditioner.DiagPreconditioner import DiagPreconditioner
from AOT_biomaps.AOT_Recon.AOT_SMatrix.SMatrix_SELL import SMatrix_SELL
from AOT_biomaps.AOT_Recon.AOT_SMatrix.SMatrix_CSR import SMatrix_CSR
from AOT_biomaps.AOT_Recon.AOT_SMatrix.SMatrix_DENSE import SMatrix_DENSE

# Check for CuPy availability
try:
    import cupy as cp
    CUPY_AVAILABLE = True
except ImportError:
    cp = None
    CUPY_AVAILABLE = False

# =====================================================================
# CuPy Kernels definition for fusion of operations (Zero-Allocation)
# =====================================================================
if CUPY_AVAILABLE:
    fista_update_kernel = cp.ElementwiseKernel(
        'float32 prev_lambda, float32 z_in, float32 grad, float32 alpha, float32 momentum',
        'float32 x_new, float32 z_out',
        '''
        // Gradient descent step: z_in - alpha * grad(F(z_in))
        double step = (double)z_in - (double)alpha * (double)grad;

        // Non-negativity projection: x_{k+1} = max(0, step)
        double x_val = step > 0.0 ? step : 0.0;
        x_new = (float)x_val;

        // Nesterov Extrapolation: z_{k+1} = x_{k+1} + momentum * (x_{k+1} - x_k)
        z_out = (float)(x_val + (double)momentum * (x_val - (double)prev_lambda));
        ''',
        'fista_update_kernel'
    )


def calibrate_prior_FISTA(
    SMatrix,
    y_flat,
    preconditioner,
    potential_type: PotentialType,
    potential_shape: PotentialShapeType,
    potential_radius: int,
    L_data: float,
    num_warmup: int = 10,
    show_logs: bool = False
):
    """
    Runtime measurement of the data/prior gradient scales, enabling a
    DIMENSIONLESS user-facing β (see module docstring).

    Procedure:
    1. Warm-up: `num_warmup` unregularized preconditioned gradient steps
       (step size 1/L_data) from λ=0 → produces a representative image λ_w.
    2. Measure:
       - G_f : L2 norm of the last preconditioned data gradient at λ_w
       - amp : mean amplitude of the positive part of λ_w (image scale)
       - G_U : L2 norm of ∇U at β=1, δ=amp, evaluated on λ_w

    Returns:
        tuple: (G_f, G_U, amp)  (amp falls back to 1.0 if the warm-up
        collapses to zero, e.g. empty data.)
    """
    xp = get_array_module(SMatrix)

    lambda_w = xp.zeros(SMatrix.Z * SMatrix.X, dtype=xp.float32)
    alpha_w = 1.0 / max(L_data, 1e-12)
    grad_f = None

    for _ in range(num_warmup):
        Ax = forward_projection(SMatrix, lambda_w)
        residual = Ax - y_flat
        grad_f = xp.ascontiguousarray(
            preconditioner.apply_inverse(xp.real(backward_projection(SMatrix, residual))),
            dtype=xp.float32
        )
        lambda_w = lambda_w - alpha_w * grad_f
        xp.maximum(lambda_w, 0.0, out=lambda_w)

    if grad_f is None:
        return 1.0, 1.0, 1.0

    G_f = float(xp.linalg.norm(grad_f))

    pos = lambda_w[lambda_w > 0]
    amp = float(xp.mean(pos)) if pos.size > 0 else 1.0

    # Prior gradient scale at beta=1 (delta scaled to image amplitude)
    grad_U1, _, _ = get_potential_function(
        potential_type, SMatrix, lambda_w,
        beta=1.0, delta=amp,
        shape=potential_shape, radius=potential_radius,
        compute_grad=True, compute_hess=False, compute_energy=False,
        use_surrogate_hessian=False
    )
    G_U = float(xp.linalg.norm(grad_U1))

    if G_U <= 0.0:
        if show_logs:
            print("[AOT-biomaps] Warning : prior gradient scale is zero on the warm-up image (uniform image?). beta will have no effect.")
        G_U = 1.0

    return G_f, G_U, amp

def calculate_step_size_FISTA(SMatrix, preconditioner, potential_type, beta, delta, num_iters, L_data, show_logs):
    """
    Compute the step size α = 1 / (L_data + L_prior).

    L_data = λ_max(P⁻¹ Aᴴ A) via power iteration.
    L_prior from Gershgorin bounds on the regularization Hessian,
    expressed with the INTERNAL (calibrated) beta.
    """
    if L_data is None:
      L_data = estimate_lipschitz_constant(SMatrix, preconditioner=preconditioner, num_iters=num_iters, show_logs=show_logs)

    if potential_type == PotentialType.QUADRATIC:
        L_prior = 8.0 * beta
    elif potential_type == PotentialType.HUBER:
        # Linear-region bound (8β). The quadratic tip (L = 8β/δ) is handled
        # conservatively below when δ_int is small relative to image steps.
        L_prior = 8.0 * beta
        # Guard against the quadratic-region Lipschitz blow-up:
        # L_tip = 8β/δ is an upper bound; take max but cap at a sane fraction of L_data
        if delta > 0:
            L_prior = max(L_prior, min(8.0 * beta / max(delta, 1e-30), 10.0 * L_data))
    elif potential_type == PotentialType.RELATIVE_DIFFERENCE:
        gamma = 0.05  # Must strictly match the 'gamma' defined in the RDP kernel
        L_prior = 8.0 * (2.0 * beta / gamma)
    else:
        L_prior = 0.0

    alpha = 1.0 / (L_data + L_prior)

    if show_logs:
        print(f"[AOT-biomaps] Using step size α = {alpha:.3e} (L_data={L_data:.2e}, L_prior={L_prior:.2e})")

    return alpha

def FISTA(
    SMatrix: Union['SMatrix_DENSE', 'SMatrix_CSR', 'SMatrix_SELL'],
    y: Union[np.ndarray, 'cp.ndarray'],
    numIterations: int = 100,
    alpha: Union[float, str] = "auto",
    beta: float = 0.1,
    delta: float = 0.01,
    numIterations_stepCalculation: int = 20,
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
) -> Tuple[Union[np.ndarray, list], Optional[list], Optional[list]]:
    """
    Fast Iterative Shrinkage-Thresholding Algorithm (FISTA).

    β IS DIMENSIONLESS (relative prior strength):
        β ≈ ||∇U|| / ||∇f||  is enforced by runtime calibration, so
        β ∈ [0.01, 1] has the SAME meaning for any dataset, SMatrix
        normalization, data amplitude or potential function.
        β=0 → no regularization, β~0.1-0.3 → mild smoothing (typical
        optimum), β>1 → strong smoothing.

    δ is a RELATIVE Huber threshold (fraction of the image amplitude,
    measured on a warm-up reconstruction): δ=0.01 means the transition
    quadratic→linear occurs at 1% of typical image amplitude.

    Other args: see previous docstring (unchanged).
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

        # Normalize data y
        y_max = float(np.max(np.abs(y))) if SMatrix.isComplexSMatrix else float(np.max(y))
        if y_max > 0:
            y_norm = y / y_max

        y_flat = xp.asarray(y_norm.T.flatten().astype(data_dtype))

        # Preconditioner Initialization
        if preconditioner_type == PreconditionerType.DIAGONAL:
            preconditioner = DiagPreconditioner(SMatrix=SMatrix)
            preconditioner.build()
        else:
            preconditioner = NoPreconditioner(SMatrix=SMatrix)

        # ==========================================================
        # DIMENSIONLESS β CALIBRATION (replaces ad-hoc normalization)
        # ==========================================================
        beta_phys = float(beta)
        delta_phys = float(delta)

        L_data = estimate_lipschitz_constant(SMatrix, preconditioner=preconditioner, num_iters=numIterations_stepCalculation, show_logs=show_logs)

        if potential_type == PotentialType.NONE or beta_phys == 0.0:
            beta_int = 0.0
            delta_int = 0.0
            G_f = G_U = 1.0
        else:
            G_f, G_U, amp = calibrate_prior_FISTA(
                SMatrix, y_flat, preconditioner,
                potential_type, potential_shape, potential_radius,
                L_data, num_warmup=10, show_logs=show_logs
            )
            # Enforce  ||∇U|| ≈ β_phys * ||∇f||  at the working point:
            beta_int = beta_phys * G_f / G_U
            # δ in internal image-amplitude units:
            delta_int = delta_phys * amp

        prior_ratio = beta_phys  # by construction: ||∇U||/||∇f|| ≈ β_phys
        if show_logs:
            print(f"[AOT-biomaps] β (dimensionless) = {beta_phys:.3e} | β_int = {beta_int:.3e} "
                  f"(G_f={G_f:.2e}, G_U={G_U:.2e}) | δ_int = {delta_int:.3e}")

        # Step size (uses the CALIBRATED internal beta)
        alpha_val = calculate_step_size_FISTA(SMatrix, preconditioner, potential_type, beta_int, delta_int, numIterations_stepCalculation, L_data=L_data, show_logs=show_logs) if alpha == "auto" else alpha
        alpha_vec = xp.full(ZX, alpha_val, dtype=xp.float32)

        # Variables initialization
        lambda_flat = xp.zeros(ZX, dtype=xp.float32)
        lambda_bar = xp.zeros(ZX, dtype=xp.float32)
        t = 1.0

        residual_buffer = xp.empty_like(y_flat)

        save_indices = np.unique(np.append(np.arange(0, numIterations, max(1, numIterations // max_saves)), numIterations - 1)).tolist()
        saved_lambda = []
        saved_indices_list = []
        cost_history = [] if isCostFunction else None
        window_history = []

        prec_str = preconditioner.get_name()
        cplx_str = "COMPLEX (4-phases quadrature) " if SMatrix.isComplexSMatrix else "REAL "
        delta_str = f" / δ_rel={delta_phys:.2e}" if potential_type == PotentialType.HUBER else ""
        description = f"[AOT-biomaps] {cplx_str}FISTA --- {prec_str} ({SMatrix.matrix_type.name}) with {potential_type.name} β={beta_phys:.2e} (ratio≈{prior_ratio:.1e}){delta_str} --- {'WITH' if withTumor else 'WITHOUT'} TUMOR --- DEVICE: {SMatrix.device.upper()}"

        iterator = trange(numIterations, desc=description) if show_logs else range(numIterations)

        # ==========================================================
        # MAIN OPTIMIZATION LOOP
        # ==========================================================
        for it in iterator:
            prev_lambda = lambda_flat.copy()

            Alambda_bar = forward_projection(SMatrix, lambda_bar)
            xp.subtract(Alambda_bar, y_flat, out=residual_buffer)

            # --- PRIOR GRADIENT --- ∇U(λ_bar)
            grad_U, _, _ = get_potential_function(potential_type, SMatrix, lambda_bar, beta=beta_int, delta=delta_int, shape=potential_shape, radius=potential_radius, compute_grad=True, compute_hess=False, compute_energy=isCostFunction, use_surrogate_hessian=False)

            # --- DATA FIDELITY GRADIENT WITH PRECONDITIONING ---
            grad_fidelity_prec = xp.ascontiguousarray(preconditioner.apply_inverse(xp.real(backward_projection(SMatrix, residual_buffer))), dtype=xp.float32)

            # --- TOTAL GRADIENT ---
            total_grad = grad_fidelity_prec + grad_U

            # --- NESTEROV MOMENTUM ---
            t_next = (1.0 + np.sqrt(1.0 + 4.0 * t * t)) / 2.0
            momentum = (t - 1.0) / t_next

            # --- FISTA UPDATE ---
            if is_gpu:
                fista_update_kernel(prev_lambda, lambda_bar, total_grad.astype(xp.float32, copy=False), alpha_vec, float(momentum), lambda_flat, lambda_bar)
            else:
                lambda_flat = lambda_bar - alpha_vec * total_grad
                np.maximum(lambda_flat, 0.0, out=lambda_flat)
                lambda_bar = lambda_flat + float(momentum) * (lambda_flat - prev_lambda)

            t = t_next

            if isCostFunction:
                Ax = forward_projection(SMatrix, lambda_flat)
                _, _, U_x = get_potential_function(potential_type, SMatrix, lambda_flat, beta=beta_int, delta=delta_int, shape=potential_shape, radius=potential_radius, compute_grad=False, compute_hess=False, compute_energy=True, use_surrogate_hessian=False)
                fidelity = 0.5 * float(xp.vdot(Ax - y_flat, Ax - y_flat).real)
                cost_history.append(fidelity + U_x)

            if stop_criterion != StopCriterionType.MAX_ITERATIONS:
                if SMatrix.experiment.OpticImage is None:
                    ground_truth = None
                else:
                    ground_truth = SMatrix.experiment.OpticImage.phantom if withTumor else SMatrix.experiment.OpticImage.laser.intensity
                gradient_for_stop = total_grad if stop_criterion == StopCriterionType.GRADIENT_NORM else None
                isStop, val = check_stopping_criterion(SMatrix, lambda_flat, prev_lambda, stop_criterion, stop_threshold, window_size=stop_window_size, history=cost_history, ground_truth=ground_truth, gradient=gradient_for_stop, window_history=window_history)
                if show_logs and show_criterion:
                    iterator.set_postfix_str(f"{stop_criterion.name}: {val:.2e}")
                if isStop:
                    if show_logs: print(f"\n[AOT-biomaps] Stopping Criterion {stop_criterion.name} reached at iteration {it}.")
                    cost_history.pop() if isCostFunction else None
                    break

            if isSavingEachIteration and it in save_indices:
                lambda_snapshot = lambda_flat.reshape(Z, X).get() if is_gpu else lambda_flat.reshape(Z, X).copy()
                saved_lambda.append(lambda_snapshot * y_max / SMatrix.normalization_factor)
                saved_indices_list.append(it)

        final_result = lambda_flat.reshape(Z, X).get() if is_gpu else lambda_flat.reshape(Z, X)
        final_result *= y_max / SMatrix.normalization_factor

        return (saved_lambda, saved_indices_list, cost_history) if isSavingEachIteration else ([final_result], [it + 1], cost_history)