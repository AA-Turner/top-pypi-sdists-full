from AOT_biomaps.AOT_Recon.ReconTools import power_method, gradient, div, proj_l2, prox_G, prox_F_star, _call_axpby, _call_minus_axpy, compute_TV_cpu, power_method_estimate_L__SELL, calculate_memory_requirement, check_gpu_memory
from AOT_biomaps.Config import config
from AOT_biomaps.AOT_Recon.ReconEnums import NoiseType, SMatrixType
import torch
from tqdm import trange
import numpy as np
import pycuda.driver as drv

'''
This module implements Primal-Dual Hybrid Gradient (PDHG) methods for solving inverse problems in Acousto-Optic Tomography.
It includes Chambolle-Pock algorithms for Total Variation (TV) and Kullback-Leibler (KL) divergence regularization.
The methods can run on both CPU and GPU, with configurations set in the AOT_biomaps.Config module.
'''

def CP_TV(
    SMatrix, 
    y, 
    alpha=None,               # TV regularization parameter (if None, alpha is auto-scaled)
    beta=1e-4,              # Tikhonov regularization parameter     
    theta=1.0,
    numIterations=5000, 
    isSavingEachIteration=True,
    L=None, 
    withTumor=True,
    device=None,
    max_saves=5000,
    show_logs=True,
    smatrixType=SMatrixType.SELL,
    k_security=0.8,
    use_power_method=True,
    auto_alpha_gamma=0.05,    # gamma for auto alpha: alpha = gamma * data_term / tv_term
    apply_positivity_clamp=True,
    tikhonov_as_gradient=False,  # if True, apply -tau*2*beta*x instead of prox multiplicative
    use_laplacian=True,         # enable Laplacian (Hessian scalar) penalty
    laplacian_beta_scale=1.0 # multiply beta for laplacian term if you want separate scaling
):
    # try:
    tumor_str = "WITH" if withTumor else "WITHOUT"
    # Auto-select device and method
    if device is None:
        if torch.cuda.is_available() and check_gpu_memory(config.select_best_gpu(), calculate_memory_requirement(SMatrix, y), show_logs=show_logs):
            device = torch.device(f"cuda:{config.select_best_gpu()}")
            use_gpu = True
        else:
            device = torch.device("cpu")
            use_gpu = False
    else:
        use_gpu = device.type == "cuda"
    # Dispatch to the appropriate implementation
    if use_gpu:
            if smatrixType == SMatrixType.CSR:
                raise NotImplementedError("GPU Chambolle Pock (LS-TV) with CSR not implemented.")
            elif smatrixType == SMatrixType.SELL:
                return CP_TV_Tikhonov_sparseSELL_pycuda(SMatrix, y, alpha,beta, theta, numIterations, isSavingEachIteration, L, tumor_str, device, max_saves, show_logs, k_security, use_power_method, auto_alpha_gamma, apply_positivity_clamp, tikhonov_as_gradient, use_laplacian, laplacian_beta_scale)
            elif smatrixType == SMatrixType.DENSE:
                return CP_TV_dense(SMatrix, y, alpha, theta, numIterations, isSavingEachIteration, L, tumor_str, device, max_saves, show_logs)
            else:
                raise ValueError("Unsupported SMatrixType for GPU Chambolle Pock (LS-TV).")
    else:
        raise NotImplementedError("CPU Chambolle Pock (LS-TV) not implemented.")

def CP_KL(
    SMatrix, 
    y, 
    alpha=None,               # TV regularization parameter (if None, alpha is auto-scaled)
    beta=1e-4,              # Tikhonov regularization parameter     
    theta=1.0,
    numIterations=5000, 
    isSavingEachIteration=True,
    L=None, 
    withTumor=True,
    device=None,
    max_saves=5000,
    show_logs=True,
    smatrixType=SMatrixType.SELL,
    k_security=0.8,
    use_power_method=True,
    auto_alpha_gamma=0.05,    # gamma for auto alpha: alpha = gamma * data_term / tv_term
    apply_positivity_clamp=True,
    tikhonov_as_gradient=False,  # if True, apply -tau*2*beta*x instead of prox multiplicative
    use_laplacian=True,         # enable Laplacian (Hessian scalar) penalty
    laplacian_beta_scale=1.0 # multiply beta for laplacian term if you want separate scaling
):
    # try:
    tumor_str = "WITH" if withTumor else "WITHOUT"
    # Auto-select device and method
    if device is None:
        if torch.cuda.is_available() and check_gpu_memory(config.select_best_gpu(), calculate_memory_requirement(SMatrix, y), show_logs=show_logs):
            device = torch.device(f"cuda:{config.select_best_gpu()}")
            use_gpu = True
        else:
            device = torch.device("cpu")
            use_gpu = False
    else:
        use_gpu = device.type == "cuda"
    # Dispatch to the appropriate implementation
    if use_gpu:
            if smatrixType == SMatrixType.CSR:
                raise NotImplementedError("GPU Chambolle Pock (LS-KL) with CSR not implemented.")
            elif smatrixType == SMatrixType.SELL:
                raise NotImplementedError("GPU Chambolle Pock (LS-KL) with SELL not implemented.")
            elif smatrixType == SMatrixType.DENSE:
                return CP_KL(SMatrix, y, alpha, theta, numIterations, isSavingEachIteration, L, tumor_str, device, max_saves, show_logs)
            else:
                raise ValueError("Unsupported SMatrixType for GPU Chambolle Pock (LS-KL).")
    else:
        raise NotImplementedError("CPU Chambolle Pock (LS-KL) not implemented.")

def CP_TV_dense(
    SMatrix,
    y,
    alpha=1e-1,
    theta=1.0,
    numIterations=5000,
    isSavingEachIteration=True,
    L=None,
    withTumor=True,
    device=None,
    max_saves=5000,
    show_logs=True,
):
    """
    Chambolle-Pock algorithm for Total Variation (TV) regularization.
    Works on both CPU and GPU.
    Args:
        SMatrix: System matrix (shape: T, Z, X, N)
        y: Measurement data (shape: T, N)
        alpha: Regularization parameter for TV
        theta: Relaxation parameter (1.0 for standard Chambolle-Pock)
        numIterations: Number of iterations
        isSavingEachIteration: If True, returns selected intermediate reconstructions
        L: Lipschitz constant (estimated if None)
        withTumor: Boolean for description only
        device: Torch device (auto-selected if None)
        max_saves: Maximum number of intermediate saves (default: 5000)
    """
    # Auto-select device if not provided
    if device is None:
        device = torch.device(f"cuda:{config.select_best_gpu()}" if torch.cuda.is_available() else "cpu")
    else:
        device = torch.device(device)

    # Convert data to tensors and move to device
    A = torch.tensor(SMatrix, dtype=torch.float32, device=device)
    y = torch.tensor(y, dtype=torch.float32, device=device)
    T, Z, X, N = SMatrix.shape
    A_flat = A.permute(0, 3, 1, 2).reshape(T * N, Z * X)
    y_flat = y.reshape(-1)

    # Robust normalization
    norm_A = A_flat.abs().max().clamp(min=1e-8)
    norm_y = y_flat.abs().max().clamp(min=1e-8)
    A_flat = A_flat / norm_A
    y_flat = y_flat / norm_y

    # Define forward/backward operators
    P = lambda x: torch.matmul(A_flat, x)
    PT = lambda y: torch.matmul(A_flat.T, y)

    # Estimate Lipschitz constant if needed
    if L is None:
        try:
            L = power_method(P, PT, y_flat, Z, X)
            L = max(L, 1e-3)
        except:
            L = 1.0

    sigma = 1.0 / L
    tau = 1.0 / L

    # Initialize variables
    x = torch.zeros(Z * X, device=device)
    p = torch.zeros((2, Z, X), device=device)
    q = torch.zeros_like(y_flat)
    x_tilde = x.clone()

    # Calculate save indices
    if numIterations <= max_saves:
        save_indices = list(range(numIterations))
    else:
        step = numIterations // max_saves
        save_indices = list(range(0, numIterations, step))
        if save_indices[-1] != numIterations - 1:
            save_indices.append(numIterations - 1)

    I_reconMatrix = []
    saved_indices = []

    # Description for progress bar
    tumor_str = "WITH TUMOR" if withTumor else "WITHOUT TUMOR"
    device_str = f"GPU no.{torch.cuda.current_device()}" if device.type == "cuda" else "CPU"
    description = f"AOT-BioMaps -- Primal/Dual Reconstruction (LS-TV) α:{alpha:.4f} L:{L:.4f} -- {tumor_str} -- {device_str}"

    iterator = trange(numIterations, desc=description) if show_logs else range(numIterations)
    for it in iterator:
        # Update p (TV proximal step)
        grad_x = gradient(x_tilde.reshape(Z, X))
        p = proj_l2(p + sigma * grad_x, alpha)

        # Update q (data fidelity)
        q = (q + sigma * (P(x_tilde) - y_flat)) / (1 + sigma)

        # Update x
        x_old = x.clone()
        div_p = div(p).ravel()  # Divergence calculation
        ATq = PT(q)
        x = (x - tau * (ATq - div_p)) / (1 + tau * 1e-6)  # Light L2 regularization

        # Update x_tilde
        x_tilde = x + theta * (x - x_old)

        # Save intermediate result if needed
        if isSavingEachIteration and it in save_indices:
            I_reconMatrix.append(x.reshape(Z, X).clone() * (norm_y / norm_A))
            saved_indices.append(it)

    # Return results
    if isSavingEachIteration:
        return [tensor.cpu().numpy() for tensor in I_reconMatrix], saved_indices
    else:
        return (x.reshape(Z, X) * (norm_y / norm_A)).cpu().numpy(), None

def CP_TV_Tikhonov_sparseSELL_pycuda(
    SMatrix,
    y,
    alpha=None,               # TV regularization parameter (if None, alpha is auto-scaled)
    beta=1e-4,              # Tikhonov regularization parameter     
    theta=1.0,
    numIterations=2000,
    isSavingEachIteration=True,
    L=None,
    tumor_str="",
    device=None,
    max_saves=2000,
    show_logs=True,
    k_security=0.8,
    use_power_method=True,
    auto_alpha_gamma=0.05,    # gamma for auto alpha: alpha = gamma * data_term / tv_term
    apply_positivity_clamp=True,
    tikhonov_as_gradient=False,  # if True, apply -tau*2*beta*x instead of prox multiplicative
    use_laplacian=True,         # enable Laplacian (Hessian scalar) penalty
    laplacian_beta_scale=1.0    # multiply beta for laplacian term if you want separate scaling
):
    
    """
    CP-TV + Tikhonov + Laplacian (Hessian scalar) penalty integrated.
    Returns (I_reconMatrix, saved_indices) if isSavingEachIteration else (x_final, None).
    """
        # ----- begin main -----
    if SMatrix.ctx:
        SMatrix.ctx.push()

    # prepare variables
    dtype = np.float32
    TN = int(SMatrix.N * SMatrix.T)
    ZX = int(SMatrix.Z * SMatrix.X)
    Z, X = SMatrix.Z, SMatrix.X
    block_size = 256

    # existing kernels
    projection_kernel = SMatrix.sparse_mod.get_function("projection_kernel__SELL")
    backprojection_kernel = SMatrix.sparse_mod.get_function("backprojection_kernel__SELL")
    axpby_kernel = SMatrix.sparse_mod.get_function("vector_axpby_kernel")
    minus_axpy_kernel = SMatrix.sparse_mod.get_function("vector_minus_axpy_kernel")
    gradient_kernel = SMatrix.sparse_mod.get_function("gradient_kernel")
    divergence_kernel = SMatrix.sparse_mod.get_function("divergence_kernel")
    proj_tv_kernel = SMatrix.sparse_mod.get_function("proj_tv_kernel")

    # optional kernels (laplacian & clamp)
    has_laplacian = False
    has_clamp_kernel = False
    try:
        laplacian_kernel = SMatrix.sparse_mod.get_function("laplacian_kernel")
        laplacian_adj_kernel = SMatrix.sparse_mod.get_function("laplacian_adj_kernel")
        has_laplacian = True
    except Exception:
        has_laplacian = False

    try:
        clamp_positive_kernel = SMatrix.sparse_mod.get_function("clamp_positive_kernel")
        has_clamp_kernel = True
    except Exception:
        has_clamp_kernel = False

    stream = drv.Stream()

    # estimate L operator norm if needed
    if use_power_method or L is None:
        L_LS_sq = power_method_estimate_L__SELL(SMatrix, stream, n_it=20, block_size=block_size)
        L_nabla_sq = 8.0
        L_op_norm = np.sqrt(L_LS_sq + L_nabla_sq)
        if L_op_norm < 1e-6:
            L_op_norm = 1.0
    else:
        L_op_norm = L

    tau = np.float32(k_security / L_op_norm)
    sigma = np.float32(k_security / L_op_norm)

    # prepare y and normalization
    y = y.T.astype(dtype).reshape(-1)
    maxy = float(np.max(np.abs(y))) if y.size > 0 else 0.0
    if maxy > 0:
        y_normed = (y / maxy).copy()
    else:
        y_normed = y.copy()

    # GPU allocations
    bufs = []
    y_gpu = drv.mem_alloc(y_normed.nbytes); bufs.append(y_gpu)
    drv.memcpy_htod_async(y_gpu, y_normed.T.flatten(), stream)

    x_gpu = drv.mem_alloc(ZX * np.dtype(dtype).itemsize); bufs.append(x_gpu)
    drv.memset_d32_async(x_gpu, 0, ZX, stream)
    x_old_gpu = drv.mem_alloc(ZX * np.dtype(dtype).itemsize); bufs.append(x_old_gpu)
    x_tilde_gpu = drv.mem_alloc(ZX * np.dtype(dtype).itemsize); bufs.append(x_tilde_gpu)
    drv.memcpy_dtod_async(x_tilde_gpu, x_gpu, ZX * np.dtype(dtype).itemsize, stream)

    p_gpu = drv.mem_alloc(2 * ZX * np.dtype(dtype).itemsize); bufs.append(p_gpu)
    q_gpu = drv.mem_alloc(TN * np.dtype(dtype).itemsize); bufs.append(q_gpu)
    drv.memset_d32_async(p_gpu, 0, 2 * ZX, stream)
    drv.memset_d32_async(q_gpu, 0, TN, stream)

    grad_gpu = drv.mem_alloc(2 * ZX * np.dtype(dtype).itemsize); bufs.append(grad_gpu)
    div_gpu = drv.mem_alloc(ZX * np.dtype(dtype).itemsize); bufs.append(div_gpu)
    Ax_gpu = drv.mem_alloc(TN * np.dtype(dtype).itemsize); bufs.append(Ax_gpu)
    ATq_gpu = drv.mem_alloc(ZX * np.dtype(dtype).itemsize); bufs.append(ATq_gpu)
    zero_gpu = drv.mem_alloc(ZX * np.dtype(dtype).itemsize); bufs.append(zero_gpu)
    drv.memset_d32_async(zero_gpu, 0, ZX, stream)

    # Laplacian buffers (if enabled and kernel available)
    use_lap = use_laplacian and has_laplacian and (beta > 0)
    if use_lap:
        lap_gpu = drv.mem_alloc(ZX * np.dtype(dtype).itemsize); bufs.append(lap_gpu)
        r_gpu = drv.mem_alloc(ZX * np.dtype(dtype).itemsize); bufs.append(r_gpu)
        drv.memset_d32_async(r_gpu, 0, ZX, stream)
        # scalar beta for laplacian (allow separate scale)
        beta_lap = float(beta) * float(laplacian_beta_scale)
        inv_1_plus_sigma_beta = np.float32(1.0 / (1.0 + float(sigma) * beta_lap))

    # host buffers for logs
    x_host = np.empty(ZX, dtype=dtype)
    Ax_host = np.empty(TN, dtype=dtype)
    q_host = np.empty(TN, dtype=dtype)
    p_host = np.empty(2 * ZX, dtype=dtype)
    ATq_host = np.empty(ZX, dtype=dtype)

    # compute initial backprojection for auto-alpha
    drv.memset_d32_async(ATq_gpu, 0, ZX, stream)
    backprojection_kernel(SMatrix.sell_values_gpu, SMatrix.sell_colinds_gpu, SMatrix.slice_ptr_gpu, SMatrix.slice_len_gpu,
                        y_gpu, ATq_gpu, np.int32(TN), np.int32(SMatrix.slice_height),
                        block=(block_size, 1, 1), grid=((TN + block_size - 1) // block_size, 1, 1), stream=stream)
    stream.synchronize()
    drv.memcpy_dtoh(x_host, ATq_gpu)

    # auto alpha if requested
    if alpha is None:
        drv.memcpy_htod_async(x_gpu, x_host, stream)
        projection_kernel(Ax_gpu, SMatrix.sell_values_gpu, SMatrix.sell_colinds_gpu, SMatrix.slice_ptr_gpu, SMatrix.slice_len_gpu,
                        x_gpu, np.int32(TN), np.int32(SMatrix.slice_height),
                        block=(block_size, 1, 1), grid=((TN + block_size - 1) // block_size, 1, 1), stream=stream)
        stream.synchronize()
        drv.memcpy_dtoh(Ax_host, Ax_gpu)
        resid = Ax_host - y_normed[:TN]
        data_term = 0.5 * float(np.dot(resid, resid))
        tv_term = float(compute_TV_cpu(x_host, Z, X)) + 1e-12
        alpha = float(auto_alpha_gamma * data_term / tv_term)
        if show_logs:
            print(f"[auto-alpha] data_term={data_term:.6e}, tv_term={tv_term:.6e}, alpha_set={alpha:.6e}")

    # tikhonov prox multiplicative scale
    if tikhonov_as_gradient:
        tikh_scale = None
    else:
        tikh_scale = np.float32(1.0 / (1.0 + 2.0 * tau * beta)) if beta > 0 else np.float32(1.0)

    # saving policy
    if numIterations <= max_saves:
        save_indices_all = list(range(0, numIterations + 1))
    else:
        step = max(1, numIterations // max_saves)
        save_indices_all = list(range(0, numIterations + 1, step))

    device_str = f"GPU no.{torch.cuda.current_device()}" if device.type == "cuda" else "CPU"
    if show_logs:
        if (alpha is None or alpha == 0) and (beta is None or beta == 0):
            print(f"Parameters: L={L_op_norm:.6e} tau={tau:.3e} sigma={sigma:.3e} lap_enabled={use_lap}")
            description = f"AOT-BioMaps -- Primal/Dual Reconstruction (LS) -- {tumor_str} -- {device_str}"
        if alpha is None or alpha == 0:
            print(f"Parameters: L={L_op_norm:.6e} tau={tau:.3e} sigma={sigma:.3e} beta={beta:.4e} lap_enabled={use_lap}")
            description = f"AOT-BioMaps -- Primal/Dual Reconstruction (LS-Tikhonov) -- {tumor_str} -- {device_str}"
        elif beta is None or beta == 0:
            print(f"Parameters: L={L_op_norm:.6e} tau={tau:.3e} sigma={sigma:.3e} alpha={alpha:.4e} beta={beta:.4e} lap_enabled={use_lap}")
            description = f"AOT-BioMaps -- Primal/Dual Reconstruction (LS-TV) -- {tumor_str} -- {device_str}"
        else:
            print(f"Parameters: L={L_op_norm:.6e} tau={tau:.3e} sigma={sigma:.3e} alpha={alpha:.4e} beta={beta:.4e} lap_enabled={use_lap}")
            description = f"AOT-BioMaps -- Primal/Dual Reconstruction (LS-TV-Tikhonov) -- {tumor_str} -- {device_str}"

    I_reconMatrix = []
    saved_indices = []
    if isSavingEachIteration and 0 in save_indices_all:
        drv.memcpy_dtoh(x_host, x_gpu)
        x0 = x_host.reshape((Z, X)).copy()
        if maxy > 0:
            x0 *= maxy
        I_reconMatrix.append(x0)
        saved_indices.append(0)

    # main loop
    try:
        iterator = trange(numIterations, desc=description) if show_logs else range(numIterations)
        for it in iterator:
            # 1) dual p update (TV)
            gradient_kernel(grad_gpu, x_tilde_gpu, np.int32(Z), np.int32(X), np.int32(ZX),
                            block=(block_size, 1, 1),
                            grid=((X + block_size - 1) // block_size, (Z + block_size - 1) // block_size, 1),
                            stream=stream)
            _call_axpby(axpby_kernel, p_gpu, p_gpu, grad_gpu, 1.0, sigma, 2 * ZX, stream, block_size)
            proj_tv_kernel(p_gpu, np.float32(alpha), np.int32(ZX),
                            block=(block_size, 1, 1),
                            grid=((ZX + block_size - 1) // block_size, 1, 1),
                            stream=stream)

            # 2) dual q update (data fidelity)
            projection_kernel(Ax_gpu, SMatrix.sell_values_gpu, SMatrix.sell_colinds_gpu, SMatrix.slice_ptr_gpu, SMatrix.slice_len_gpu,
                            x_tilde_gpu, np.int32(TN), np.int32(SMatrix.slice_height),
                            block=(block_size, 1, 1), grid=((TN + block_size - 1) // block_size, 1, 1), stream=stream)
            _call_axpby(axpby_kernel, Ax_gpu, Ax_gpu, y_gpu, 1.0, -1.0, TN, stream, block_size)
            _call_axpby(axpby_kernel, q_gpu, q_gpu, Ax_gpu, 1.0 / (1.0 + sigma), sigma / (1.0 + sigma), TN, stream, block_size)

            # optional Laplacian dual update
            if use_lap:
                # compute Laplacian of x_tilde -> lap_gpu
                laplacian_kernel(lap_gpu, x_tilde_gpu, np.int32(Z), np.int32(X), np.int32(ZX),
                                block=(block_size, 1, 1),
                                grid=((X + block_size - 1) // block_size, (Z + block_size - 1) // block_size, 1),
                                stream=stream)
                # r = r + sigma * lap
                _call_axpby(axpby_kernel, r_gpu, r_gpu, lap_gpu, 1.0, sigma, ZX, stream, block_size)
                # r = r / (1 + sigma * beta_lap)
                _call_axpby(axpby_kernel, r_gpu, r_gpu, zero_gpu, inv_1_plus_sigma_beta, 0.0, ZX, stream, block_size)

            # 3) primal x update
            drv.memcpy_dtod_async(x_old_gpu, x_gpu, ZX * np.dtype(dtype).itemsize, stream)
            divergence_kernel(div_gpu, p_gpu, np.int32(Z), np.int32(X), np.int32(ZX),
                            block=(block_size, 1, 1),
                            grid=((X + block_size - 1) // block_size, (Z + block_size - 1) // block_size, 1),
                            stream=stream)
            drv.memset_d32_async(ATq_gpu, 0, ZX, stream)
            backprojection_kernel(SMatrix.sell_values_gpu, SMatrix.sell_colinds_gpu, SMatrix.slice_ptr_gpu, SMatrix.slice_len_gpu,
                                q_gpu, ATq_gpu, np.int32(TN), np.int32(SMatrix.slice_height),
                                block=(block_size, 1, 1), grid=((TN + block_size - 1) // block_size, 1, 1), stream=stream)
            # ATq - div
            _call_minus_axpy(minus_axpy_kernel, ATq_gpu, div_gpu, 1.0, ZX, stream, block_size)

            # if laplacian is used, add H^T r into ATq
            if use_lap:
                # compute laplacian_adj_kernel(temp, r)
                # reuse grad_gpu as temporary if safe (its content used earlier, but not reused until later)
                laplacian_adj_kernel(grad_gpu, r_gpu, np.int32(Z), np.int32(X), np.int32(ZX),
                                    block=(block_size, 1, 1),
                                    grid=((X + block_size - 1) // block_size, (Z + block_size - 1) // block_size, 1),
                                    stream=stream)
                # ATq_gpu += temp (grad_gpu)
                _call_axpby(axpby_kernel, ATq_gpu, ATq_gpu, grad_gpu, 1.0, 1.0, ZX, stream, block_size)

            # x = x_old - tau * ATq_buffer
            _call_minus_axpy(minus_axpy_kernel, x_gpu, ATq_gpu, tau, ZX, stream, block_size)

            # Tikhonov
            if beta > 0:
                if tikhonov_as_gradient:
                    mul = 1.0 - 2.0 * float(tau) * float(beta)
                    if mul <= 0.0:
                        # fallback to prox multiplicative stable
                        fallback_scale = np.float32(1.0 / (1.0 + 2.0 * float(tau) * float(beta)))
                        _call_axpby(axpby_kernel, x_gpu, x_gpu, zero_gpu, fallback_scale, 0.0, ZX, stream, block_size)
                    else:
                        # x *= mul  => implemented as axpby: out = 1* x + (mul-1)*x
                        _call_axpby(axpby_kernel, x_gpu, x_gpu, x_gpu, 1.0, np.float32(mul - 1.0), ZX, stream, block_size)
                else:
                    _call_axpby(axpby_kernel, x_gpu, x_gpu, zero_gpu, tikh_scale, np.float32(0.0), ZX, stream, block_size)

            # positivity clamp (prefer GPU kernel if available)
            if apply_positivity_clamp:
                if has_clamp_kernel:
                    # in-place clamp on GPU
                    clamp_positive_kernel(x_gpu, np.int32(ZX),
                                        block=(block_size, 1, 1),
                                        grid=((ZX + block_size - 1) // block_size, 1, 1),
                                        stream=stream)
                else:
                    # fallback CPU roundtrip (slower)
                    stream.synchronize()
                    drv.memcpy_dtoh(x_host, x_gpu)
                    np.maximum(x_host, 0.0, out=x_host)
                    drv.memcpy_htod_async(x_gpu, x_host, stream)

            # extrapolation
            _call_axpby(axpby_kernel, x_tilde_gpu, x_gpu, x_old_gpu, np.float32(1.0 + theta), np.float32(-theta), ZX, stream, block_size)

            # saves
            if isSavingEachIteration and (it + 1) in save_indices_all:
                stream.synchronize()
                drv.memcpy_dtoh(x_host, x_gpu)
                x_saved = x_host.reshape((Z, X)).copy()
                if maxy > 0:
                    x_saved *= maxy
                I_reconMatrix.append(x_saved)
                saved_indices.append(it + 1)

        stream.synchronize()
        drv.memcpy_dtoh(x_host, x_gpu)
        x_final = x_host.reshape((Z, X)).copy()
        if maxy > 0:
            x_final *= maxy
            if isSavingEachIteration and len(I_reconMatrix):
                for i in range(len(I_reconMatrix)):
                    I_reconMatrix[i] *= maxy

        # free buffers
        for buff in bufs:
            try:
                buff.free()
            except:
                pass

        if SMatrix.ctx:
            SMatrix.ctx.pop()

        if isSavingEachIteration:
            return I_reconMatrix, saved_indices
        else:
            return x_final, None

    except Exception as e:
        # cleanup robustly
        print("Error in CP_TV_Tikhonov+Lap (robust):", e)
        try:
            for buff in bufs:
                try:
                    buff.free()
                except:
                    pass
        except:
            pass
        try:
            if SMatrix and hasattr(SMatrix, 'ctx') and SMatrix.ctx:
                SMatrix.ctx.pop()
        except:
            pass
        raise

def CP_KL(
    SMatrix,
    y,
    alpha=1e-9,
    theta=1.0,
    numIterations=5000,
    isSavingEachIteration=True,
    L=None,
    tumor_str="",
    device=None,
    max_saves=5000,
    show_logs=True,
):
    """
    Chambolle-Pock algorithm for Kullback-Leibler (KL) divergence regularization.
    Works on both CPU and GPU.
    Args:
        SMatrix: System matrix (shape: T, Z, X, N)
        y: Measurement data (shape: T, X, N)
        alpha: Regularization parameter
        theta: Relaxation parameter (1.0 for standard Chambolle-Pock)
        numIterations: Number of iterations
        isSavingEachIteration: If True, returns selected intermediate reconstructions
        L: Lipschitz constant (estimated if None)
        withTumor: Boolean for description only
        device: Torch device (auto-selected if None)
        max_saves: Maximum number of intermediate saves (default: 5000)
    """
    # Auto-select device if not provided
    if device is None:
        device = torch.device(f"cuda:{config.select_best_gpu()}" if torch.cuda.is_available() else "cpu")
    else:
        device = torch.device(device)

    # Convert data to tensors and move to device
    A = torch.tensor(SMatrix, dtype=torch.float32, device=device)
    y = torch.tensor(y, dtype=torch.float32, device=device)
    T, Z, X, N = SMatrix.shape
    A_flat = A.permute(0, 3, 1, 2).reshape(T * N, Z * X)
    y_flat = y.reshape(-1)

    # Define forward/backward operators
    P = lambda x: torch.matmul(A_flat, x.ravel())
    PT = lambda y: torch.matmul(A_flat.T, y)

    # Estimate Lipschitz constant if needed
    if L is None:
        L = power_method(P, PT, y_flat, Z, X)

    sigma = 1.0 / L
    tau = 1.0 / L

    # Initialize variables
    x = torch.zeros(Z * X, device=device)
    q = torch.zeros_like(y_flat)
    x_tilde = x.clone()

    # Calculate save indices
    if numIterations <= max_saves:
        save_indices = list(range(numIterations))
    else:
        step = numIterations // max_saves
        save_indices = list(range(0, numIterations, step))
        if save_indices[-1] != numIterations - 1:
            save_indices.append(numIterations - 1)

    I_reconMatrix = [x.reshape(Z, X).cpu().numpy()]
    saved_indices = [0]

    # Description for progress bar
    device_str = f"GPU no.{torch.cuda.current_device()}" if device.type == "cuda" else "CPU"
    description = f"AOT-BioMaps -- Primal/Dual Reconstruction (KL) α:{alpha:.4f} L:{L:.4f} -- {tumor_str} -- {device_str}"

    iterator = trange(numIterations, desc=description) if show_logs else range(numIterations)
    for iteration in iterator:
        # Update q (proximal step for F*)
        q = prox_F_star(q + sigma * P(x_tilde) - sigma * y_flat, sigma, y_flat)

        # Update x (proximal step for G)
        x_old = x.clone()
        x = prox_G(x - tau * PT(q), tau, PT(torch.ones_like(y_flat)))

        # Update x_tilde
        x_tilde = x + theta * (x - x_old)

        # Save intermediate result if needed
        if isSavingEachIteration and iteration in save_indices:
            I_reconMatrix.append(x.reshape(Z, X).cpu().numpy())
            saved_indices.append(iteration)

    # Return results
    if isSavingEachIteration:
        return I_reconMatrix, saved_indices
    else:
        return I_reconMatrix[-1], None
    
def CP_TV_Tikhonov_Preconditioned_SELL_pycuda(
    SMatrix,
    y,
    alpha=None,             # TV param
    beta=1e-4,              # Tikhonov param
    numIterations=2000,
    isSavingEachIteration=True,
    tumor_str="",
    device=None,
    max_saves=2000,
    show_logs=True,
    k_security=1.0,         # Pock condition: tau*sigma * ||A||^2 < 1. Avec precond, souvent k=1.0 suffit.
    apply_positivity_clamp=True
):
    
    if SMatrix.ctx:
        SMatrix.ctx.push()

    dtype = np.float32
    TN = int(SMatrix.N * SMatrix.T)
    ZX = int(SMatrix.Z * SMatrix.X)
    Z, X = SMatrix.Z, SMatrix.X
    block_size = 256

    # --- Récupération des Kernels (Existants + Nouveaux) ---
    projection_kernel = SMatrix.sparse_mod.get_function("projection_kernel__SELL")
    backprojection_kernel = SMatrix.sparse_mod.get_function("backprojection_kernel__SELL")
    axpby_kernel = SMatrix.sparse_mod.get_function("vector_axpby_kernel")
    minus_axpy_kernel = SMatrix.sparse_mod.get_function("vector_minus_axpy_kernel")
    gradient_kernel = SMatrix.sparse_mod.get_function("gradient_kernel")
    divergence_kernel = SMatrix.sparse_mod.get_function("divergence_kernel")
    proj_tv_kernel = SMatrix.sparse_mod.get_function("proj_tv_kernel")
    
    # Nouveaux kernels pour le préconditionnement
    try:
        update_dual_data_precond = SMatrix.sparse_mod.get_function("update_dual_data_precond_kernel")
        update_primal_precond = SMatrix.sparse_mod.get_function("update_primal_precond_kernel")
        invert_vector_kernel = SMatrix.sparse_mod.get_function("invert_vector_kernel")
        clamp_positive_kernel = SMatrix.sparse_mod.get_function("clamp_positive_kernel")
    except Exception as e:
        print("Erreur: Il manque les kernels C++ de préconditionnement (update_dual_data_precond_kernel, etc).")
        raise e

    stream = drv.Stream()

    # --- 1. SETUP PRECONDITIONERS (tau_vec, sigma_vec) ---
    # Au lieu de calculer L, on calcule les sommes lignes/colonnes
    
    # Allocations vecteurs de pas
    sigma_vec_gpu = drv.mem_alloc(TN * np.dtype(dtype).itemsize)
    tau_vec_gpu = drv.mem_alloc(ZX * np.dtype(dtype).itemsize)
    
    # Buffer temporaire de 1 pour les sommes
    ones_TN_gpu = drv.mem_alloc(TN * np.dtype(dtype).itemsize)
    ones_ZX_gpu = drv.mem_alloc(ZX * np.dtype(dtype).itemsize)
    
    # Remplir de 1.0
    # On utilise une astuce : axpby(out, out, out, 0, 0) pour clear puis ajout de 1 ? Non, memset n'écrit pas des float 1.0.
    # On va transférer un array de 1 depuis le host (rapide au setup)
    drv.memcpy_htod_async(ones_TN_gpu, np.ones(TN, dtype=dtype), stream)
    drv.memcpy_htod_async(ones_ZX_gpu, np.ones(ZX, dtype=dtype), stream)
    
    # A) Calcul de Sigma (Inverse des Row Sums) : A * 1_ZX
    # On utilise ton kernel de projection existant : q = A * theta (avec theta=1)
    projection_kernel(sigma_vec_gpu, SMatrix.sell_values_gpu, SMatrix.sell_colinds_gpu, SMatrix.slice_ptr_gpu, SMatrix.slice_len_gpu,
                      ones_ZX_gpu, np.int32(TN), np.int32(SMatrix.slice_height),
                      block=(block_size, 1, 1), grid=((TN + block_size - 1) // block_size, 1, 1), stream=stream)
    
    # Inversion : sigma_vec = 1 / (sum + eps)
    # Note : sigma_vec doit être divisé par k_security ? Dans Pock precond, tau_i = 1/sum. On garde k_security global si besoin.
    invert_vector_kernel(sigma_vec_gpu, sigma_vec_gpu, np.float32(1e-6), np.int32(TN),
                         block=(block_size, 1, 1), grid=((TN + block_size - 1) // block_size, 1, 1), stream=stream)

    # B) Calcul de Tau (Inverse des Col Sums - Carte Sensibilité) : A^T * 1_TN
    # On utilise ton kernel de backprojection : c += A^T * e (avec e=1)
    # Important : backproj fait un atomicAdd, il faut mettre à 0 avant
    drv.memset_d32_async(tau_vec_gpu, 0, ZX, stream)
    backprojection_kernel(SMatrix.sell_values_gpu, SMatrix.sell_colinds_gpu, SMatrix.slice_ptr_gpu, SMatrix.slice_len_gpu,
                          ones_TN_gpu, tau_vec_gpu, np.int32(TN), np.int32(SMatrix.slice_height),
                          block=(block_size, 1, 1), grid=((TN + block_size - 1) // block_size, 1, 1), stream=stream)
    
    invert_vector_kernel(tau_vec_gpu, tau_vec_gpu, np.float32(1e-6), np.int32(ZX),
                         block=(block_size, 1, 1), grid=((ZX + block_size - 1) // block_size, 1, 1), stream=stream)

    # Nettoyage temp
    ones_TN_gpu.free()
    ones_ZX_gpu.free()

    # --- 2. PREPARE DATA ---
    y = y.T.astype(dtype).reshape(-1)
    maxy = float(np.max(np.abs(y))) if y.size > 0 else 0.0
    y_normed = (y / maxy).copy() if maxy > 0 else y.copy()

    # Allocations Variables Principales
    bufs = []
    y_gpu = drv.mem_alloc(y_normed.nbytes); bufs.append(y_gpu)
    drv.memcpy_htod_async(y_gpu, y_normed, stream)

    x_gpu = drv.mem_alloc(ZX * np.dtype(dtype).itemsize); bufs.append(x_gpu)
    drv.memset_d32_async(x_gpu, 0, ZX, stream)
    
    x_old_gpu = drv.mem_alloc(ZX * np.dtype(dtype).itemsize); bufs.append(x_old_gpu)
    x_tilde_gpu = drv.mem_alloc(ZX * np.dtype(dtype).itemsize); bufs.append(x_tilde_gpu)
    drv.memset_d32_async(x_tilde_gpu, 0, ZX, stream) # Important: x_tilde init à 0

    # Dual Variables
    p_gpu = drv.mem_alloc(2 * ZX * np.dtype(dtype).itemsize); bufs.append(p_gpu) # Gradient
    q_gpu = drv.mem_alloc(TN * np.dtype(dtype).itemsize); bufs.append(q_gpu)     # Data term
    drv.memset_d32_async(p_gpu, 0, 2 * ZX, stream)
    drv.memset_d32_async(q_gpu, 0, TN, stream)

    # Buffers intermédiaires
    grad_gpu = drv.mem_alloc(2 * ZX * np.dtype(dtype).itemsize); bufs.append(grad_gpu)
    div_gpu = drv.mem_alloc(ZX * np.dtype(dtype).itemsize); bufs.append(div_gpu)
    Ax_gpu = drv.mem_alloc(TN * np.dtype(dtype).itemsize); bufs.append(Ax_gpu)
    ATq_gpu = drv.mem_alloc(ZX * np.dtype(dtype).itemsize); bufs.append(ATq_gpu)

    # --- PARAMETRES & LOGS ---
    # Pour le TV, on a besoin d'un sigma scalaire pour le dual update du gradient.
    # Dans le preconditionning diagonal complet, c'est complexe.
    # Approximation robuste : on utilise sigma_tv fixe.
    # Cependant, alpha (le poids TV) joue le rôle de seuil.
    sigma_tv = np.float32(1.0) # Le scaling est absorbé par alpha et tau_vec

    if alpha is None:
        # Auto-alpha simplifié (ou tu gardes ta logique précédente)
        alpha = 0.01 # Valeur par défaut si non spécifié
        print(f"Warning: Alpha not set, using default {alpha}")

    # Description
    desc = f"Pock-Precond | {tumor_str} | Alpha={alpha} | Beta={beta}"
    
    # Saving setup
    x_host = np.empty(ZX, dtype=dtype)
    save_indices_all = list(range(0, numIterations + 1, max(1, numIterations // max_saves)))
    I_reconMatrix = []
    saved_indices = []

    try:
        iterator = trange(numIterations, desc=desc) if show_logs else range(numIterations)
        
        for it in iterator:
            
            # =======================
            # 1. UPDATE DUAL (P - TV)
            # =======================
            # Gradient de x_bar (x_tilde)
            gradient_kernel(grad_gpu, x_tilde_gpu, np.int32(Z), np.int32(X), np.int32(ZX),
                            block=(block_size, 1, 1), grid=((X + block_size - 1) // block_size, (Z + block_size - 1) // block_size, 1), stream=stream)
            
            # p = p + sigma_tv * grad
            axpby_kernel(p_gpu, p_gpu, grad_gpu, np.float32(1.0), sigma_tv, np.int32(2 * ZX),
                         block=(block_size, 1, 1), grid=((2*ZX + block_size - 1) // block_size, 1, 1), stream=stream)
            
            # Prox TV (Projection boule unité)
            # Attention : ici le pas "alpha" doit être adapté car on utilise un tau vectoriel ailleurs.
            # On passe alpha brut.
            proj_tv_kernel(p_gpu, np.float32(alpha), np.int32(ZX),
                           block=(block_size, 1, 1), grid=((ZX + block_size - 1) // block_size, 1, 1), stream=stream)

            # ==========================
            # 2. UPDATE DUAL (Q - DATA)
            # ==========================
            # Calcul Ax_bar
            projection_kernel(Ax_gpu, SMatrix.sell_values_gpu, SMatrix.sell_colinds_gpu, SMatrix.slice_ptr_gpu, SMatrix.slice_len_gpu,
                              x_tilde_gpu, np.int32(TN), np.int32(SMatrix.slice_height),
                              block=(block_size, 1, 1), grid=((TN + block_size - 1) // block_size, 1, 1), stream=stream)
            
            # Update q avec sigma vectoriel
            # q = (q + sigma_vec * (Ax - y)) / (1 + sigma_vec)
            update_dual_data_precond(q_gpu, Ax_gpu, y_gpu, sigma_vec_gpu, np.int32(TN),
                                     block=(block_size, 1, 1), grid=((TN + block_size - 1) // block_size, 1, 1), stream=stream)

            # ==========================
            # 3. UPDATE PRIMAL (X)
            # ==========================
            # Sauvegarde x_old
            drv.memcpy_dtod_async(x_old_gpu, x_gpu, ZX * np.dtype(dtype).itemsize, stream)
            
            # Calcul ATq (Backprojection)
            drv.memset_d32_async(ATq_gpu, 0, ZX, stream)
            backprojection_kernel(SMatrix.sell_values_gpu, SMatrix.sell_colinds_gpu, SMatrix.slice_ptr_gpu, SMatrix.slice_len_gpu,
                                  q_gpu, ATq_gpu, np.int32(TN), np.int32(SMatrix.slice_height),
                                  block=(block_size, 1, 1), grid=((TN + block_size - 1) // block_size, 1, 1), stream=stream)
            
            # Calcul Div p
            divergence_kernel(div_gpu, p_gpu, np.int32(Z), np.int32(X), np.int32(ZX),
                              block=(block_size, 1, 1), grid=((X + block_size - 1) // block_size, (Z + block_size - 1) // block_size, 1), stream=stream)
            
            # Combiner les gradients : ATq - Div p
            minus_axpy_kernel(ATq_gpu, div_gpu, np.float32(1.0), np.int32(ZX),
                             block=(block_size, 1, 1), grid=((ZX + block_size - 1) // block_size, 1, 1), stream=stream)

            # Update X avec tau vectoriel
            # x = x - tau_vec * (ATq - Div p)
            # Note: ATq_gpu contient maintenant le gradient total
            update_primal_precond(x_gpu, ATq_gpu, tau_vec_gpu, np.int32(ZX),
                                  block=(block_size, 1, 1), grid=((ZX + block_size - 1) // block_size, 1, 1), stream=stream)

            # Positivity
            if apply_positivity_clamp:
                clamp_positive_kernel(x_gpu, np.int32(ZX),
                                      block=(block_size, 1, 1), grid=((ZX + block_size - 1) // block_size, 1, 1), stream=stream)

            # Tikhonov (simplifié : decay)
            if beta > 0:
                # x = x / (1 + beta * tau_vec) ? 
                # Approx rapide : x *= (1 - beta * mean_tau) ou juste x *= (1-beta)
                # Utilisons axpby simple pour un petit decay
                axpby_kernel(x_gpu, x_gpu, x_gpu, np.float32(1.0 - beta), np.float32(0.0), np.int32(ZX),
                             block=(block_size, 1, 1), grid=((ZX + block_size - 1) // block_size, 1, 1), stream=stream)

            # ==========================
            # 4. EXTRAPOLATION
            # ==========================
            # x_tilde = x + theta * (x - x_old)
            axpby_kernel(x_tilde_gpu, x_gpu, x_old_gpu, np.float32(2.0), np.float32(-1.0), np.int32(ZX),
                         block=(block_size, 1, 1), grid=((ZX + block_size - 1) // block_size, 1, 1), stream=stream)

            # Save
            if isSavingEachIteration and (it + 1) in save_indices_all:
                stream.synchronize()
                drv.memcpy_dtoh(x_host, x_gpu)
                x_saved = x_host.reshape((Z, X)).copy()
                if maxy > 0: x_saved *= maxy
                I_reconMatrix.append(x_saved)
                saved_indices.append(it + 1)

        # Fin boucle
        stream.synchronize()
        # Cleanup (buffers)
        for b in bufs: b.free()
        sigma_vec_gpu.free()
        tau_vec_gpu.free()
        if SMatrix.ctx: SMatrix.ctx.pop()

        return I_reconMatrix, saved_indices

    except Exception as e:
        print(f"Error: {e}")
        if SMatrix.ctx: SMatrix.ctx.pop()
        return None, None
    
