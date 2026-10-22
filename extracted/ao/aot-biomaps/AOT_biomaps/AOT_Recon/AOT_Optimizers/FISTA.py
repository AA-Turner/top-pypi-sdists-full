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
   β_phys = 1 means the prior gradient has the same magnitude as the data gradient (relative scale-free calibration, repeatable across datasets, SMatrix normalizations and potential functions).
   Internally, the algorithm measures at runtime:
   - G_f = || P⁻¹ Aᴴ (A λ_w - y) ||   : data gradient scale (preconditioned)
   - G_U = || ∇U_β=1(λ_w) ||          : prior gradient scale at β=1
     both evaluated on a short warm-up reconstruction λ_w (few unregularized iterations), and sets:
       β_int = β_phys * G_f / G_U        (so that ||∇U|| ≈ β_phys * ||∇f||)

   Potential-dependent δ calibration:
       HUBER:               δ_int = δ_phys * amp(λ_w)   (image-amplitude units)
       RELATIVE_DIFFERENCE: δ_int = δ_phys               (Nuyts 2002, dimensionless)
   For the EXACT Nuyts prior, ∇U ∝ 1/(δ·s) so ||∇U|| scales like 1/amp(λ):
   G_U is measured on λ_w rescaled to unit mean amplitude (working regime, y normalized by y_max -> converged image O(1)).

   This removes all dependence on normalization_factor, y_max and matrix scaling: β_phys ∈ [0.01, 1] is meaningful and reproducible everywhere.

3. Lipschitz Constant & Adaptive Step Size:
   - QUADRATIC / HUBER: fixed scalar step
       L_total = L_data + L_prior,   α = 1 / L_total
     (L_data via power iteration, L_prior via Gershgorin bounds)
   - RELATIVE_DIFFERENCE (EXACT Nuyts 2002): the prior curvature at d=0 is
     U''(0) = 2/ε, so the GLOBAL Lipschitz constant is INFINITE and no fixed
     step is valid. A variable-metric MM surrogate (De Pierro) is used
     instead: per-pixel curvature
       q_i(λ) = β Σ_j w_ij · 2 / (δ·max(|d_ij|, h)·s_ij + ε)
     recomputed at each iteration, and the update becomes:
       λ_{k+1} = max(0, λ_bar - ∇F(λ_bar) / (L_data + q_i(λ_bar)))
     h bounds ONLY the majorant curvature, never the prior or its
     gradient (the converged solution is the exact Nuyts minimizer).

4. Nesterov Acceleration:
   t_{k+1} = (1 + sqrt(1 + 4 t_k²)) / 2,   λ_bar = λ + momentum * (λ - λ_prev)
   For RELATIVE_DIFFERENCE, an adaptive restart (O'Donoghue & Candès 2015)
   is applied: t -> 1 whenever  ∇Fᵀ (λ_k - λ_{k-1}) > 0.

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
    delta_phys: float = 1.0,
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
       - G_U : L2 norm of ∇U at β=1 evaluated on λ_w:
           * HUBER:               δ_cal = δ_phys * amp  (image-amplitude units)
           * RELATIVE_DIFFERENCE: δ_cal = δ_phys        (Nuyts 2002, dimensionless)
             measured on λ_w rescaled to unit mean amplitude (∇U ∝ 1/s, so a
             dim warm-up overestimates G_U by ~1/amp).

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

    # Prior gradient scale at beta=1
    if potential_type == PotentialType.RELATIVE_DIFFERENCE:
        # Nuyts 2002: δ dimensionless + G_U measured at the WORKING scale
        lambda_cal = lambda_w / amp if amp > 0 else lambda_w
        grad_U1, _, _ = get_potential_function(
            potential_type, SMatrix, lambda_cal,
            beta=1.0, delta=delta_phys,
            shape=potential_shape, radius=potential_radius,
            compute_grad=True, compute_hess=False, compute_energy=False,
            use_surrogate_hessian=False
        )
    else:
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
    Compute the FIXED scalar step size α = 1 / (L_data + L_prior).
    Valid for QUADRATIC and HUBER only.

    L_data = λ_max(P⁻¹ Aᴴ A) via power iteration.
    L_prior from Gershgorin bounds on the regularization Hessian,
    expressed with the INTERNAL (calibrated) beta.

    For RELATIVE_DIFFERENCE (EXACT Nuyts 2002), the global Lipschitz
    constant is INFINITE (prior curvature 2/ε at d=0): no fixed step is
    valid. Returns None; the caller then uses the per-pixel variable-metric
    MM step 1/(L_data + q_i) computed in the main loop.
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
        # EXACT Nuyts 2002: L_prior = INFINITE (curvature 2/ε at d=0).
        # No fixed scalar step is valid -> variable-metric MM step in the loop.
        return None
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
    h: float = 1e-3,
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
        β ≈ ||∇U|| / ||∇f|| is enforced by runtime calibration, so
        β ∈ [0.01, 1] has the SAME meaning for any dataset, SMatrix
        normalization, data amplitude or potential function.
        β=0 → no regularization, β~0.1-0.3 → mild smoothing (typical
        optimum), β>1 → strong smoothing.

    δ IS POTENTIAL-DEPENDENT (hyperparameter internal to U):

        * HUBER — RELATIVE threshold, in fraction of the image amplitude
          (measured on a warm-up reconstruction λ_w):
              δ_int = δ_phys * amp(λ_w)
          U_ij = βw·(d²/2δ if |d|≤δ else |d| - δ/2)
          δ=0.01 means the quadratic→linear transition occurs at 1% of
          the typical image amplitude.

        * RELATIVE_DIFFERENCE — dimensionless edge-preservation parameter
          of the EXACT Nuyts (2002) prior:
              U_ij = βw·d² / (d² + δ·|d|·s + ε),  s = u_i + u_j
          δ_int = δ_phys (NO amplitude calibration: δ is already relative
          to the local image scale u_i+u_j).
          The prior is linear (TV-like, weighted by 1/(δ·s)) near d=0 and
          bounded (βw) at true edges. Its curvature at d=0 is 2/ε, so no
          fixed step exists: this branch uses a variable-metric MM update
          (per-pixel step 1/(L_data + q_i), De Pierro majorant) with
          Nesterov momentum + adaptive restart (O'Donoghue & Candès 2015).
          δ small → TV-like sharp edges, δ large → weak regularization.
          The 'alpha' argument is ignored for this potential.

        * QUADRATIC — δ unused.

    Args:
        SMatrix: SMatrix instance (SMatrix_DENSE, SMatrix_CSR or SMatrix_SELL).
            Must implement forward_projection(), backward_projection(), and expose .Z, .X, .T, .N, .device, .matrix_type, .isComplexSMatrix, .normalization_factor, .experiment.OpticImage.
        y: measured data, shape (T, N). Complex if SMatrix.isComplexSMatrix (4-phase quadrature), else real. Normalized internally by y_max; the output is rescaled back via y_max/normalization_factor.
        numIterations: number of main-loop iterations (default 100).
        alpha: step size. "auto" -> α = 1/(L_data + L_prior) with L_data from power iteration and L_prior from Gershgorin bounds (QUADRATIC / HUBER). A float overrides it. Ignored for RELATIVE_DIFFERENCE (variable-metric MM step).
        beta: dimensionless prior strength β_phys (default 0.1).
            Calibrated at runtime: β_int = β_phys * G_f / G_U.
        delta: potential hyperparameter δ_phys (default 0.01). Meaning depends on potential_type (see δ section above).
        h: numerical floor on the MM majorant curvature for RELATIVE_DIFFERENCE only (default 1e-3). NOT a regularization hyperparameter: 
            it bounds ONLY the De Pierro majorant curvature q_i = βΣw·2/(δ·max(|d|,h)·s+ε), never the prior U or its gradient — the converged solution is the EXACT Nuyts minimizer for any h>0. Controls the per-pixel step on flat zones:
            h smaller -> smaller steps, slower convergence; h too large ->
            looser majorant, possible oscillations. Ignored for QUADRATIC
            and HUBER.
        numIterations_stepCalculation: power-iteration iterations for
            L_data estimation (default 20).
        potential_type: PotentialType.QUADRATIC (default), .HUBER,
            .RELATIVE_DIFFERENCE or .NONE.
        potential_shape: neighborhood shape, PotentialShapeType.CROSS
            (default), .SQUARE or .CIRCLE.
        potential_radius: neighborhood radius in pixels (default 2).
        preconditioner_type: PreconditionerType.NONE (default) or .DIAGONAL.
        stop_criterion: StopCriterionType.MAX_ITERATIONS (default),
            .RELATIVE_CHANGE, .COST_FUNCTION, .MSE or .GRADIENT_NORM.
        stop_threshold: stopping threshold on the averaged windowed
            criterion (default 100.0, i.e. effectively disabled).
        stop_window_size: averaging window size for the criterion (default 5).
        device: None (keep current), 'cpu', 'gpu' or 'gpu:<index>'.
            Transfers the SMatrix if needed (see ensure_device).
        isSavingEachIteration: if True (default), returns the list of saved
            snapshots; if False, returns only the final image.
        isCostFunction: if True, records the cost history
            0.5·||Aλ−y||² + U(λ) at each iteration (requires one extra
            forward projection and potential evaluation per iteration).
        withTumor: selects the ground-truth reference (phantom if True,
            laser intensity if False) used by the MSE stopping criterion.
        max_saves: maximum number of saved snapshots (default 5000);
            iterations are subsampled uniformly if numIterations > max_saves.
        show_logs: if True (default), prints calibration, step size and
            stopping messages.
        show_criterion: if True (default), displays the live criterion value
            in the tqdm postfix (requires show_logs).

    Returns:
        If isSavingEachIteration:
            (saved_lambda, saved_indices_list, cost_history)
        else:
            ([final_result], [it + 1], cost_history)
        where images are numpy arrays of shape (Z, X), rescaled to physical
        units by y_max / SMatrix.normalization_factor.
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
        else:
            y_norm = y

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

        # EXACT Nuyts RD: variable-metric MM branch (no fixed step exists)
        is_nuyts_rd = (potential_type == PotentialType.RELATIVE_DIFFERENCE) and beta_phys > 0.0

        L_data = estimate_lipschitz_constant(SMatrix, preconditioner=preconditioner, num_iters=numIterations_stepCalculation, show_logs=show_logs)

        if potential_type == PotentialType.NONE or beta_phys == 0.0:
            beta_int = 0.0
            delta_int = 0.0
            G_f = G_U = 1.0
            amp = 1.0
        else:
            G_f, G_U, amp = calibrate_prior_FISTA(
                SMatrix, y_flat, preconditioner,
                potential_type, potential_shape, potential_radius,
                L_data, delta_phys=delta_phys, num_warmup=10, show_logs=show_logs
            )
            # Enforce  ||∇U|| ≈ β_phys * ||∇f||  at the working point:
            beta_int = beta_phys * G_f / G_U
            # δ in internal units:
            if potential_type == PotentialType.HUBER:
                # Huber threshold in image-amplitude units
                delta_int = delta_phys * amp
            elif potential_type == PotentialType.RELATIVE_DIFFERENCE:
                # Nuyts 2002: δ relative to (u_i+u_j) -> already dimensionless
                delta_int = delta_phys
            else:
                delta_int = 0.0

        prior_ratio = beta_phys  # by construction: ||∇U||/||∇f|| ≈ β_phys
        if show_logs:
            print(f"[AOT-biomaps] β (dimensionless) = {beta_phys:.3e} | β_int = {beta_int:.3e} "
                  f"(G_f={G_f:.2e}, G_U={G_U:.2e}) | δ_int = {delta_int:.3e}")

        # h_floor: numerical floor on the MM MAJORANT curvature (RD only).
        # Bounds ONLY the majorant (never the prior or its gradient: the converged solution is the EXACT Nuyts minimizer).
        # Working regime: y normalized by y_max -> converged image O(1).
        # Do NOT scale by the dim warm-up amp (h*amp ≈ 1e-6 freezes the step).
        h_floor = float(h)

        # Step size (uses the CALIBRATED internal beta). RD: variable-metric.
        if is_nuyts_rd:
            if show_logs:
                print(f"[AOT-biomaps] RELATIVE_DIFFERENCE (Nuyts 2002): variable-metric MM step "
                      f"1/(L_data + q_i), h_floor={h_floor:.1e} (no fixed α).")
            alpha_vec = None  # unused in the RD branch
        else:
            alpha_val = calculate_step_size_FISTA(SMatrix, preconditioner, potential_type, beta_int, delta_int, numIterations_stepCalculation, L_data=L_data, show_logs=show_logs) if alpha == "auto" else alpha
            alpha_vec = xp.full(ZX, alpha_val, dtype=xp.float32)

        # Variables initialization
        lambda_flat = xp.zeros(ZX, dtype=xp.float32)
        lambda_bar = xp.zeros(ZX, dtype=xp.float32)
        t = 1.0

        # Start at 0 so forward projections are initially 0
        Ax = xp.zeros_like(y_flat)
        Alambda_bar = xp.zeros_like(y_flat)

        residual_buffer = xp.empty_like(y_flat)
        q_buffer = xp.empty(ZX, dtype=xp.float32)

        save_indices = np.unique(np.append(np.arange(0, numIterations, max(1, numIterations // max_saves)), numIterations - 1)).tolist()
        saved_lambda = []
        saved_indices_list = []
        cost_history = [] if isCostFunction else None
        window_history = []

        prec_str = preconditioner.get_name()
        cplx_str = "COMPLEX (4-phases quadrature) " if SMatrix.isComplexSMatrix else "REAL "
        delta_str = f" / δ_rel={delta_phys:.2e}" if potential_type in [PotentialType.HUBER, PotentialType.RELATIVE_DIFFERENCE] else ""
        description = f"[AOT-biomaps] {cplx_str}FISTA --- {prec_str} ({SMatrix.matrix_type.name}) with {potential_type.name} β={beta_phys:.2e} (ratio≈{prior_ratio:.1e}){delta_str} --- {'WITH' if withTumor else 'WITHOUT'} TUMOR --- DEVICE: {SMatrix.device.upper()}"

        iterator = trange(numIterations, desc=description) if show_logs else range(numIterations)

        # ==========================================================
        # MAIN OPTIMIZATION LOOP
        # ==========================================================
        for it in iterator:
            prev_lambda = lambda_flat.copy()
            prev_Ax = Ax

            # Alambda_bar is already correctly extrapolated from the previous iteration
            xp.subtract(Alambda_bar, y_flat, out=residual_buffer)

            # --- PRIOR GRADIENT --- ∇U(λ_bar)  (+ MM curvature q_i for RD)
            if is_nuyts_rd:
                grad_U, q_i, _ = get_potential_function(potential_type, SMatrix, lambda_bar, beta=beta_int, delta=delta_int, shape=potential_shape, radius=potential_radius, h_floor=h_floor, compute_grad=True, compute_hess=True, compute_energy=False, use_surrogate_hessian=False)
            else:
                grad_U, _, _ = get_potential_function(potential_type, SMatrix, lambda_bar, beta=beta_int, delta=delta_int, shape=potential_shape, radius=potential_radius, compute_grad=True, compute_hess=False, compute_energy=isCostFunction, use_surrogate_hessian=False)

            # --- DATA FIDELITY GRADIENT WITH PRECONDITIONING ---
            grad_fidelity_prec = xp.ascontiguousarray(preconditioner.apply_inverse(xp.real(backward_projection(SMatrix, residual_buffer))), dtype=xp.float32)

            # --- TOTAL GRADIENT ---
            total_grad = grad_fidelity_prec + grad_U

            # --- ADAPTIVE RESTART (O'Donoghue & Candès 2015) -- RD only ---
            # Restart Nesterov momentum when the gradient fights the
            # momentum direction: ∇Fᵀ (λ_k - λ_{k-1}) > 0  ->  t = 1
            if is_nuyts_rd and it > 0:
                dir_dot = float(xp.vdot(total_grad, lambda_flat - prev_lambda).real) if xp.iscomplexobj(total_grad) \
                    else float(xp.dot(total_grad, lambda_flat - prev_lambda))
                if dir_dot > 0.0:
                    t = 1.0

            # --- NESTEROV MOMENTUM ---
            t_next = (1.0 + np.sqrt(1.0 + 4.0 * t * t)) / 2.0
            momentum = (t - 1.0) / t_next

            # --- UPDATE ---
            if is_nuyts_rd:
                # Variable-metric MM step (De Pierro majorant, per-pixel):
                # λ_{k+1} = max(0, λ_bar - ∇F(λ_bar) / (L_data + q_i(λ_bar)))
                xp.maximum(L_data + q_i, 1e-12, out=q_buffer)
                lambda_flat = xp.maximum(lambda_bar - total_grad / q_buffer, 0.0)
                lambda_bar = lambda_flat + float(momentum) * (lambda_flat - prev_lambda)
            elif is_gpu:
                fista_update_kernel(prev_lambda, lambda_bar, total_grad.astype(xp.float32, copy=False), alpha_vec, float(momentum), lambda_flat, lambda_bar)
            else:
                lambda_flat = lambda_bar - alpha_vec * total_grad
                np.maximum(lambda_flat, 0.0, out=lambda_flat)
                lambda_bar = lambda_flat + float(momentum) * (lambda_flat - prev_lambda)

            t = t_next

            # --- UNIQUE FORWARD PROJECTION & LINEAR EXTRAPOLATION ---
            # Linearity trick: A(x + m·dx) = Ax + m·(Ax - prev_Ax)
            Ax = forward_projection(SMatrix, lambda_flat)
            Alambda_bar = Ax + float(momentum) * (Ax - prev_Ax)

            if isCostFunction or stop_criterion == StopCriterionType.COST_FUNCTION:
                _, _, U_x = get_potential_function(potential_type, SMatrix, lambda_flat, beta=beta_int, delta=delta_int, shape=potential_shape, radius=potential_radius, h_floor=h_floor, compute_grad=False, compute_hess=False, compute_energy=True, use_surrogate_hessian=False)
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
                    if not isCostFunction and stop_criterion == StopCriterionType.COST_FUNCTION:
                        cost_history.pop() if cost_history else None
                    break

            if isSavingEachIteration and it in save_indices:
                lambda_snapshot = lambda_flat.reshape(Z, X).get() if is_gpu else lambda_flat.reshape(Z, X).copy()
                saved_lambda.append(lambda_snapshot * y_max / SMatrix.normalization_factor)
                saved_indices_list.append(it)

        final_result = lambda_flat.reshape(Z, X).get() if is_gpu else lambda_flat.reshape(Z, X)
        final_result *= y_max / SMatrix.normalization_factor

        return (saved_lambda, saved_indices_list, cost_history) if isSavingEachIteration else ([final_result], [it + 1], cost_history)