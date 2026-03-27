from AOT_biomaps.Config import config
from AOT_biomaps.AOT_Recon.ReconTools import calculate_memory_requirement, check_gpu_memory
from AOT_biomaps.AOT_Recon.ReconEnums import SMatrixType

import torch
import numpy as np
from tqdm import trange
import pycuda.driver as drv
import torch.cuda 
import gc 



def LS(
    SMatrix,
    y,
    numIterations=100,
    isSavingEachIteration=True,
    withTumor=True,
    device=None,
    max_saves=5000,
    show_logs=True,
    smatrixType=SMatrixType.SELL
):
    """
    Least Squares reconstruction using Projected Gradient Descent (PGD) with non-negativity constraint.
    Currently only implements the stable GPU version.
    """
    tumor_str = "WITH" if withTumor else "WITHOUT"
    # Auto-select device and method
    if device is None:
        if torch.cuda.is_available():
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
                return _LS_CG_sparseCSR_pycuda(SMatrix, y, numIterations, isSavingEachIteration, tumor_str, max_saves, show_logs)
            elif smatrixType == SMatrixType.SELL:
                return _LS_CG_sparseSELL_pycuda(SMatrix, y, numIterations, isSavingEachIteration, tumor_str, max_saves, show_logs)
            elif smatrixType == SMatrixType.DENSE:
                return _LS_GPU_stable(SMatrix, y, numIterations, isSavingEachIteration, tumor_str, device, max_saves,show_logs)
            else:
                raise ValueError("Unsupported SMatrixType for GPU LS.")
    else:
        raise NotImplementedError("Only GPU implementations are currently available for LS.")

def _LS_GPU_stable(SMatrix, y, numIterations, alpha, isSavingEachIteration, tumor_str, max_saves=5000, show_logs=True):
    """
    Stable GPU implementation of LS using projected gradient descent with diagonal preconditioner.
    """
    device = torch.device(f"cuda:{config.select_best_gpu()}")
    T, Z, X, N = SMatrix.shape
    ZX = Z * X
    TN = T * N
    # 1. Conversion et normalisation
    A_flat = torch.from_numpy(SMatrix).to(device=device, dtype=torch.float32).permute(0, 3, 1, 2).reshape(TN, ZX)
    y_flat = torch.from_numpy(y).to(device=device, dtype=torch.float32).reshape(TN)
    norm_A = A_flat.max()
    norm_y = y_flat.max()
    A_flat.div_(norm_A + 1e-8)
    y_flat.div_(norm_y + 1e-8)
    # 2. Initialisation
    lambda_k = torch.zeros(ZX, device=device)
    lambda_history = [] if isSavingEachIteration else None
    saved_indices = []  # Pour stocker les indices des itérations sauvegardées

    # Calculate save indices
    if numIterations <= max_saves:
        save_indices = list(range(numIterations))
    else:
        step = numIterations // max_saves
        save_indices = list(range(0, numIterations, step))
        if save_indices[-1] != numIterations - 1:
            save_indices.append(numIterations - 1)

    # Préconditionneur diagonal
    diag_AAT = torch.sum(A_flat ** 2, dim=0)
    M_inv = 1.0 / torch.clamp(diag_AAT, min=1e-6)
    # Pré-allocation des tenseurs
    r_k = torch.empty_like(y_flat)
    AT_r = torch.empty(ZX, device=device)
    description = f"AOT-BioMaps -- Stable LS Reconstruction ---- {tumor_str} TUMOR ---- GPU {torch.cuda.current_device()}"

    iterator = trange(numIterations, desc=description) if show_logs else range(numIterations)
    for it in iterator:
        # Calcul du résidu (inplace)
        torch.matmul(A_flat, lambda_k, out=r_k)
        r_k = y_flat - r_k
        if isSavingEachIteration and it in save_indices:
            lambda_history.append(lambda_k.clone().reshape(Z, X) * (norm_y / norm_A))
            saved_indices.append(it)

        # Gradient préconditionné (inplace)
        torch.matmul(A_flat.T, r_k, out=AT_r)
        AT_r *= M_inv
        # Mise à jour avec pas fixe et projection (inplace)
        lambda_k.add_(AT_r, alpha=alpha)
        lambda_k.clamp_(min=0)

    # 3. Dénormalisation
    lambda_final = lambda_k.reshape(Z, X) * (norm_y / norm_A)
    # Free memory
    del A_flat, y_flat, r_k, AT_r
    torch.cuda.empty_cache()
    if isSavingEachIteration:
        return [t.cpu().numpy() for t in lambda_history], saved_indices
    else:
        return lambda_final.cpu().numpy(), None

def _LS_GPU_opti(*args, **kwargs):
    raise NotImplementedError("Only _LS_GPU_stable is implemented for now.")

def _LS_GPU_multi(*args, **kwargs):
    raise NotImplementedError("Only _LS_GPU_stable is implemented for now.")

def _LS_CPU_opti(*args, **kwargs):
    raise NotImplementedError("Only _LS_GPU_stable is implemented for now.")

def _LS_CPU_basic(*args, **kwargs):
    raise NotImplementedError("Only _LS_GPU_stable is implemented for now.")

def _LS_CG_sparseCSR_pycuda(SMatrix, y, numIterations, isSavingEachIteration, tumor_str, max_saves, show_logs=True):
    """
    Reconstruction par Moindres Carrés (LS) via Gradient Conjugué (CG) sur format CSR.
    Utilise les mêmes arguments que la fonction MLEM, sans sous-fonctions Python.
    
    SMatrix: instance de SparseSMatrix_CSR (déjà allouée)
    y: données mesurées (1D np.float32 de taille TN)
    """
    final_result = None
    
    # Paramètres non utilisés dans CG mais conservés pour la signature: denominator_threshold, device

    # --- Logique de Produit Scalaire (Intégrée) ---
    def _dot_product_gpu(mod, a_ptr, b_ptr, N_int, stream):
        block_size = 256
        grid_size = (N_int + block_size - 1) // block_size
        
        reduction_host = np.empty(grid_size, dtype=np.float32)
        reduction_buffer = drv.mem_alloc(reduction_host.nbytes)
        
        dot_kernel = mod.get_function("dot_product_reduction_kernel") 

        dot_kernel(reduction_buffer, a_ptr, b_ptr, np.int32(N_int), 
                   block=(block_size, 1, 1), grid=(grid_size, 1, 1), stream=stream)
        
        drv.memcpy_dtoh(reduction_host, reduction_buffer)
        total_dot = np.sum(reduction_host)
        
        reduction_buffer.free()
        return total_dot
    # -----------------------------------------------

    try:
        if not isinstance(SMatrix, SMatrix.__class__):
            raise TypeError("SMatrix must be a SparseSMatrix_CSR object")

        if SMatrix.ctx:
            SMatrix.ctx.push()

        dtype = np.float32
        TN = SMatrix.N * SMatrix.T
        ZX = SMatrix.Z * SMatrix.X
        Z = SMatrix.Z 
        X = SMatrix.X
        block_size = 256
        tolerance = 1e-12 

        if show_logs:
            print(f"Executing on GPU device index: {SMatrix.device.primary_context.device.name()}")
            print(f"Dim X: {X}, Dim Z: {Z}, TN: {TN}, ZX: {ZX}")

        stream = drv.Stream()
        
        # Récupération des Kernels
        projection_kernel = SMatrix.sparse_mod.get_function('projection_kernel__CSR')
        backprojection_kernel = SMatrix.sparse_mod.get_function('backprojection_kernel__CSR')
        axpby_kernel = SMatrix.sparse_mod.get_function("vector_axpby_kernel")
        minus_axpy_kernel = SMatrix.sparse_mod.get_function("vector_minus_axpy_kernel")
        
        # --- Allocation des buffers (Pointeurs Bruts) ---
        y = y.T.flatten().astype(dtype)
        y_gpu = drv.mem_alloc(y.nbytes)
        drv.memcpy_htod_async(y_gpu, y.astype(dtype), stream)

        theta_flat_gpu = drv.mem_alloc(ZX * np.dtype(dtype).itemsize) # lambda
        drv.memcpy_htod_async(theta_flat_gpu, np.full(ZX, 0.1, dtype=dtype), stream)

        q_flat_gpu = drv.mem_alloc(TN * np.dtype(dtype).itemsize)      # q = A*p
        r_flat_gpu = drv.mem_alloc(ZX * np.dtype(dtype).itemsize)      # r (residue)
        p_flat_gpu = drv.mem_alloc(ZX * np.dtype(dtype).itemsize)      # p (direction)
        z_flat_gpu = drv.mem_alloc(ZX * np.dtype(dtype).itemsize)      # z = A^T A p
        ATy_flat_gpu = drv.mem_alloc(ZX * np.dtype(dtype).itemsize)    # A^T y (constant)

        # --- Initialisation CG ---
        
        # 1. ATy = A^T * y 
        drv.memset_d32_async(ATy_flat_gpu, 0, ZX, stream)
        backprojection_kernel(ATy_flat_gpu, SMatrix.values_gpu, SMatrix.row_ptr_gpu, SMatrix.col_ind_gpu,
                              y_gpu, np.int32(TN),
                              block=(block_size, 1, 1), grid=((TN + block_size - 1) // block_size, 1, 1), stream=stream)
        
        # 2. q = A * theta_0
        projection_kernel(q_flat_gpu, SMatrix.values_gpu, SMatrix.row_ptr_gpu, SMatrix.col_ind_gpu,
                          theta_flat_gpu, np.int32(TN),
                          block=(block_size, 1, 1), grid=((TN + block_size - 1) // block_size, 1, 1), stream=stream)

        # 3. r_temp = A^T * q = A^T A theta_0
        drv.memset_d32_async(r_flat_gpu, 0, ZX, stream)
        backprojection_kernel(r_flat_gpu, SMatrix.values_gpu, SMatrix.row_ptr_gpu, SMatrix.col_ind_gpu,
                              q_flat_gpu, np.int32(TN),
                              block=(block_size, 1, 1), grid=((TN + block_size - 1) // block_size, 1, 1), stream=stream)

        # 4. r_0 = ATy - r_temp (r = ATy + (-1)*r_temp)
        axpby_kernel(r_flat_gpu, ATy_flat_gpu, r_flat_gpu, 
                     np.float32(1.0), np.float32(-1.0), np.int32(ZX), 
                     block=(block_size, 1, 1), grid=((ZX + block_size - 1) // block_size, 1, 1), stream=stream)
        
        # 5. p_0 = r_0
        drv.memcpy_dtod(p_flat_gpu, r_flat_gpu, ZX * np.dtype(dtype).itemsize)
        
        # 6. rho_prev = ||r_0||^2
        rho_prev = _dot_product_gpu(SMatrix.sparse_mod, r_flat_gpu, r_flat_gpu, ZX, stream)

        # --- Boucle itérative ---
        saved_theta, saved_indices = [], []
        if numIterations <= max_saves:
            save_indices = list(range(numIterations))
        else:
            save_indices = list(range(0, numIterations, max(1, numIterations // max_saves)))
            if save_indices[-1] != numIterations - 1:
                save_indices.append(numIterations - 1)

        description = f"AOT-BioMaps -- LS-CG (CSR-sparse SMatrix) ---- {tumor_str} TUMOR ---- GPU {torch.cuda.current_device()}"
        iterator = trange(numIterations, desc=description) if show_logs else range(numIterations)

        for it in iterator:
            # a. q = A * p
            projection_kernel(q_flat_gpu, SMatrix.values_gpu, SMatrix.row_ptr_gpu, SMatrix.col_ind_gpu,
                              p_flat_gpu, np.int32(TN),
                              block=(block_size, 1, 1), grid=((TN + block_size - 1) // block_size, 1, 1), stream=stream)

            # b. z = A^T * q = A^T A p
            drv.memset_d32_async(z_flat_gpu, 0, ZX, stream)
            backprojection_kernel(z_flat_gpu, SMatrix.values_gpu, SMatrix.row_ptr_gpu, SMatrix.col_ind_gpu,
                                  q_flat_gpu, np.int32(TN),
                                  block=(block_size, 1, 1), grid=((TN + block_size - 1) // block_size, 1, 1), stream=stream)

            # c. alpha = rho_prev / <p, z>
            pAp = _dot_product_gpu(SMatrix.sparse_mod, p_flat_gpu, z_flat_gpu, ZX, stream)
            
            if abs(pAp) < 1e-15: break
            alpha = rho_prev / pAp
            
            # d. theta = theta + alpha * p
            axpby_kernel(theta_flat_gpu, theta_flat_gpu, p_flat_gpu, 
                         np.float32(1.0), alpha, np.int32(ZX), 
                         block=(block_size, 1, 1), grid=((ZX + block_size - 1) // block_size, 1, 1), stream=stream)

            # e. r = r - alpha * z
            minus_axpy_kernel(r_flat_gpu, z_flat_gpu, alpha, np.int32(ZX),
                              block=(block_size, 1, 1), grid=((ZX + block_size - 1) // block_size, 1, 1), stream=stream)
            
            # f. rho_curr = ||r||^2
            rho_curr = _dot_product_gpu(SMatrix.sparse_mod, r_flat_gpu, r_flat_gpu, ZX, stream)
            
            if rho_curr < tolerance: break

            # g. beta = rho_curr / rho_prev
            beta = rho_curr / rho_prev
            
            # h. p = r + beta * p
            axpby_kernel(p_flat_gpu, r_flat_gpu, p_flat_gpu, 
                         np.float32(1.0), beta, np.int32(ZX), 
                         block=(block_size, 1, 1), grid=((ZX + block_size - 1) // block_size, 1, 1), stream=stream)
            
            rho_prev = rho_curr

            if show_logs and (it % 10 == 0 or it == numIterations - 1):
                drv.Context.synchronize()

            if isSavingEachIteration and it in save_indices:
                theta_host = np.empty(ZX, dtype=dtype)
                drv.memcpy_dtoh(theta_host, theta_flat_gpu)
                saved_theta.append(theta_host.reshape(Z, X))
                saved_indices.append(it)

        drv.Context.synchronize()

        final_result = np.empty(ZX, dtype=dtype)
        drv.memcpy_dtoh(final_result, theta_flat_gpu)
        final_result = final_result.reshape(Z, X)

        # Libération
        y_gpu.free(); q_flat_gpu.free(); r_flat_gpu.free(); p_flat_gpu.free(); z_flat_gpu.free(); theta_flat_gpu.free(); ATy_flat_gpu.free()

        return (saved_theta, saved_indices) if isSavingEachIteration else (final_result, None)

    except Exception as e:
        print(f"Error in LS_CG_sparseCSR_pycuda: {type(e).__name__}: {e}")
        gc.collect()
        return None, None
        
    finally:
        if SMatrix and hasattr(SMatrix, 'ctx') and SMatrix.ctx:
            SMatrix.ctx.pop()

def _LS_CG_sparseSELL_pycuda(SMatrix, y, numIterations, isSavingEachIteration, tumor_str, max_saves, show_logs=True):
    """
    Reconstruction par Moindres Carrés (LS) via Gradient Conjugué (CG) sur format SELL-C-sigma.
    Utilise les mêmes arguments que la fonction MLEM, sans sous-fonctions Python.

    SMatrix: instance de SparseSMatrix_SELL (déjà allouée)
    y: données mesurées (1D np.float32 de taille TN)
    """
    final_result = None

    # --- Logique de Produit Scalaire (Intégrée) ---
    def _dot_product_gpu(mod, a_ptr, b_ptr, N_int, stream):
        block_size = 256
        grid_size = (N_int + block_size - 1) // block_size
        
        reduction_host = np.empty(grid_size, dtype=np.float32)
        reduction_buffer = drv.mem_alloc(reduction_host.nbytes)
        
        dot_kernel = mod.get_function("dot_product_reduction_kernel") 

        dot_kernel(reduction_buffer, a_ptr, b_ptr, np.int32(N_int), 
                   block=(block_size, 1, 1), grid=(grid_size, 1, 1), stream=stream)
        
        drv.memcpy_dtoh(reduction_host, reduction_buffer)
        total_dot = np.sum(reduction_host)
        
        reduction_buffer.free()
        return total_dot
    # -----------------------------------------------

    try:
        if not isinstance(SMatrix, SMatrix.__class__):
            raise TypeError("SMatrix must be a SparseSMatrix_SELL object")
        if SMatrix.sell_values_gpu is None:
            raise RuntimeError("SELL not built. Call allocate_sell_c_sigma_direct() first.")
            
        if SMatrix.ctx:
            SMatrix.ctx.push()

        dtype = np.float32
        TN = int(SMatrix.N * SMatrix.T)
        ZX = int(SMatrix.Z * SMatrix.X)
        Z = SMatrix.Z 
        X = SMatrix.X
        block_size = 256
        tolerance = 1e-12 

        # Accès aux paramètres SELL
        projection_kernel = SMatrix.sparse_mod.get_function("projection_kernel__SELL")
        backprojection_kernel = SMatrix.sparse_mod.get_function("backprojection_kernel__SELL")
        axpby_kernel = SMatrix.sparse_mod.get_function("vector_axpby_kernel")
        minus_axpy_kernel = SMatrix.sparse_mod.get_function("vector_minus_axpy_kernel")
        slice_height = np.int32(SMatrix.slice_height)
        grid_rows = ((TN + block_size - 1) // block_size, 1, 1)

        stream = drv.Stream()

        # Allocation des buffers
        y = y.T.flatten().astype(dtype)
        y_gpu = drv.mem_alloc(y.nbytes)
        drv.memcpy_htod_async(y_gpu, y.astype(dtype), stream)

        theta_flat_gpu = drv.mem_alloc(ZX * np.dtype(dtype).itemsize)
        drv.memcpy_htod_async(theta_flat_gpu, np.full(ZX, 0.1, dtype=dtype), stream)

        q_flat_gpu = drv.mem_alloc(TN * np.dtype(dtype).itemsize)
        r_flat_gpu = drv.mem_alloc(ZX * np.dtype(dtype).itemsize)
        p_flat_gpu = drv.mem_alloc(ZX * np.dtype(dtype).itemsize)
        z_flat_gpu = drv.mem_alloc(ZX * np.dtype(dtype).itemsize)
        ATy_flat_gpu = drv.mem_alloc(ZX * np.dtype(dtype).itemsize) 

        # --- Initialisation CG ---
        
        # 1. ATy = A^T * y 
        drv.memset_d32_async(ATy_flat_gpu, 0, ZX, stream)
        backprojection_kernel(SMatrix.sell_values_gpu, SMatrix.sell_colinds_gpu, SMatrix.slice_ptr_gpu, SMatrix.slice_len_gpu,
                              y_gpu, ATy_flat_gpu, np.int32(TN), slice_height,
                              block=(block_size, 1, 1), grid=grid_rows, stream=stream)
        
        # 2. q = A * theta_0
        projection_kernel(q_flat_gpu, SMatrix.sell_values_gpu, SMatrix.sell_colinds_gpu, SMatrix.slice_ptr_gpu, SMatrix.slice_len_gpu,
                          theta_flat_gpu, np.int32(TN), slice_height,
                          block=(block_size, 1, 1), grid=grid_rows, stream=stream)

        # 3. r_temp = A^T * q = A^T A theta_0
        drv.memset_d32_async(r_flat_gpu, 0, ZX, stream)
        backprojection_kernel(SMatrix.sell_values_gpu, SMatrix.sell_colinds_gpu, SMatrix.slice_ptr_gpu, SMatrix.slice_len_gpu,
                              q_flat_gpu, r_flat_gpu, np.int32(TN), slice_height,
                              block=(block_size, 1, 1), grid=grid_rows, stream=stream)

        # 4. r_0 = ATy - r_temp
        axpby_kernel(r_flat_gpu, ATy_flat_gpu, r_flat_gpu, 
                     np.float32(1.0), np.float32(-1.0), np.int32(ZX), 
                     block=(block_size, 1, 1), grid=((ZX + block_size - 1) // block_size, 1, 1), stream=stream)
        
        # 5. p_0 = r_0
        drv.memcpy_dtod(p_flat_gpu, r_flat_gpu, ZX * np.dtype(dtype).itemsize)
        
        # 6. rho_prev = ||r_0||^2
        rho_prev = _dot_product_gpu(SMatrix.sparse_mod, r_flat_gpu, r_flat_gpu, ZX, stream)

        # --- Boucle itérative ---
        saved_theta, saved_indices = [], []
        if numIterations <= max_saves:
            save_indices = list(range(numIterations))
        else:
            save_indices = list(range(0, numIterations, max(1, numIterations // max_saves)))
            if save_indices[-1] != numIterations - 1:
                save_indices.append(numIterations - 1)

        description = f"AOT-BioMaps -- LS-CG (SELL-c-σ-sparse SMatrix) ---- {tumor_str} TUMOR ---- GPU {torch.cuda.current_device()}"
        iterator = trange(numIterations, desc=description) if show_logs else range(numIterations)

        for it in iterator:
            # a. q = A * p
            projection_kernel(q_flat_gpu, SMatrix.sell_values_gpu, SMatrix.sell_colinds_gpu, SMatrix.slice_ptr_gpu, SMatrix.slice_len_gpu,
                              p_flat_gpu, np.int32(TN), slice_height,
                              block=(block_size, 1, 1), grid=grid_rows, stream=stream)

            # b. z = A^T * q = A^T A p
            drv.memset_d32_async(z_flat_gpu, 0, ZX, stream)
            backprojection_kernel(SMatrix.sell_values_gpu, SMatrix.sell_colinds_gpu, SMatrix.slice_ptr_gpu, SMatrix.slice_len_gpu,
                                  q_flat_gpu, z_flat_gpu, np.int32(TN), slice_height,
                                  block=(block_size, 1, 1), grid=grid_rows, stream=stream)

            # c. alpha = rho_prev / <p, z>
            pAp = _dot_product_gpu(SMatrix.sparse_mod, p_flat_gpu, z_flat_gpu, ZX, stream)
            
            if abs(pAp) < 1e-15: break
            alpha = rho_prev / pAp
            
            # d. theta = theta + alpha * p
            axpby_kernel(theta_flat_gpu, theta_flat_gpu, p_flat_gpu, 
                         np.float32(1.0), alpha, np.int32(ZX), 
                         block=(block_size, 1, 1), grid=((ZX + block_size - 1) // block_size, 1, 1), stream=stream)

            # e. r = r - alpha * z
            minus_axpy_kernel(r_flat_gpu, z_flat_gpu, alpha, np.int32(ZX),
                              block=(block_size, 1, 1), grid=((ZX + block_size - 1) // block_size, 1, 1), stream=stream)
            
            # f. rho_curr = ||r||^2
            rho_curr = _dot_product_gpu(SMatrix.sparse_mod, r_flat_gpu, r_flat_gpu, ZX, stream)
            
            if rho_curr < tolerance: break

            # g. beta = rho_curr / rho_prev
            beta = rho_curr / rho_prev
            
            # h. p = r + beta * p
            axpby_kernel(p_flat_gpu, r_flat_gpu, p_flat_gpu, 
                         np.float32(1.0), beta, np.int32(ZX), 
                         block=(block_size, 1, 1), grid=((ZX + block_size - 1) // block_size, 1, 1), stream=stream)
            
            rho_prev = rho_curr

            stream.synchronize()
            if isSavingEachIteration and it in save_indices:
                out = np.empty(ZX, dtype=dtype)
                drv.memcpy_dtoh(out, theta_flat_gpu)
                saved_theta.append(out.reshape((Z, X)))
                saved_indices.append(it)

        # final copy
        res = np.empty(ZX, dtype=np.float32)
        drv.memcpy_dtoh(res, theta_flat_gpu)
        final_result = res.reshape((Z, X))

        # free temporaries
        y_gpu.free(); q_flat_gpu.free(); r_flat_gpu.free(); p_flat_gpu.free(); z_flat_gpu.free(); theta_flat_gpu.free(); ATy_flat_gpu.free()
        
        return (saved_theta, saved_indices) if isSavingEachIteration else (final_result, None)
        
    except Exception as e:
        print(f"Error in LS_CG_sparseSELL_pycuda: {type(e).__name__}: {e}")
        gc.collect()
        return None, None
        
    finally:
        if SMatrix and hasattr(SMatrix, 'ctx') and SMatrix.ctx:
            SMatrix.ctx.pop()
            