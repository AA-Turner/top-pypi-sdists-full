from AOT_biomaps.AOT_Recon.ReconTools import _forward_projection, _backward_projection, check_gpu_memory, calculate_memory_requirement
from AOT_biomaps.Config import config
from AOT_biomaps.AOT_Recon.AOT_SparseSMatrix.SparseSMatrix_SELL import SparseSMatrix_SELL
from AOT_biomaps.AOT_Recon.AOT_SparseSMatrix.SparseSMatrix_CSR import SparseSMatrix_CSR
from AOT_biomaps.AOT_Recon.ReconEnums import SMatrixType
import numba
import torch
import numpy as np
import os
from tqdm import trange
import cupy as cp
import cupyx.scipy.sparse as cpsparse
import gc
import pycuda.driver as drv


def MLEM(
    SMatrix,
    y,
    numIterations=100,
    isSavingEachIteration=True,
    withTumor=True,
    device=None,
    use_numba=False,
    denominator_threshold=1e-6,
    max_saves=5000,
    show_logs=True,
    smatrixType=SMatrixType.SELL,
):
    """
    Unified MLEM algorithm for Acousto-Optic Tomography.
    Works on CPU (basic, multithread, optimized) and GPU (single or multi-GPU).
    Args:
        SMatrix: System matrix (shape: T, Z, X, N)
        y: Measurement data (shape: T, N)
        numIterations: Number of iterations
        isSavingEachIteration: If True, saves intermediate results
        withTumor: Boolean for description only
        device: Torch device (auto-selected if None)
        use_multi_gpu: If True and GPU available, uses all GPUs
        use_numba: If True and on CPU, uses multithreaded Numba
        max_saves: Maximum number of intermediate saves (default: 5000)
    Returns:
        Reconstructed image(s) and iteration indices (if isSavingEachIteration)
    """
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
                return MLEM_sparseCSR_pycuda(SMatrix, y, numIterations, isSavingEachIteration, tumor_str, max_saves, denominator_threshold, show_logs)
            elif smatrixType == SMatrixType.SELL:
                return MLEM_sparseSELL_pycuda(SMatrix, y, numIterations, isSavingEachIteration, tumor_str, max_saves, denominator_threshold, show_logs)
            elif smatrixType == SMatrixType.DENSE:
                return _MLEM_single_GPU(SMatrix, y, numIterations, isSavingEachIteration, tumor_str, max_saves, denominator_threshold,show_logs)
            else:
                raise ValueError("Unsupported SMatrixType for GPU MLEM.")
    else:
        if use_numba:
            return _MLEM_CPU_numba(SMatrix, y, numIterations, isSavingEachIteration, tumor_str, max_saves, denominator_threshold, show_logs)
        else:
            return _MLEM_CPU_opti(SMatrix, y, numIterations, isSavingEachIteration, tumor_str, max_saves, denominator_threshold, show_logs)
    # except Exception as e:
    #     print(f"Error in MLEM: {type(e).__name__}: {e}")
    #     return None, None

def _MLEM_single_GPU(SMatrix, y, numIterations, isSavingEachIteration, tumor_str, device, max_saves, denominator_threshold, show_logs=True):
    try:
        eps = torch.finfo(torch.float32).eps
        T, Z, X, N = SMatrix.shape
        ZX = Z * X
        TN = T * N
        A_flat = (
            torch.from_numpy(SMatrix)
            .to(device=device, dtype=torch.float32)
            .permute(0, 3, 1, 2)
            .contiguous()
            .reshape(TN, ZX)
        )
        y_flat = torch.from_numpy(y).to(device=device, dtype=torch.float32).reshape(-1)
        theta_flat = torch.ones(ZX, dtype=torch.float32, device=device)
        norm_factor_flat = (
            torch.from_numpy(SMatrix)
            .to(device=device, dtype=torch.float32)
            .sum(dim=(0, 3))
            .reshape(-1)
        )
        description = f"AOT-BioMaps -- ML-EM ---- {tumor_str} TUMOR ---- GPU {torch.cuda.current_device()}"
        # Calculate save indices
        if numIterations <= max_saves:
            save_indices = list(range(numIterations))
        else:
            step = numIterations // max_saves
            save_indices = list(range(0, numIterations, step))
            if save_indices[-1] != numIterations - 1:
                save_indices.append(numIterations - 1)
        saved_theta = []
        saved_indices = []
        with torch.no_grad():
            # Utilise range si show_logs=False, sinon trange
            iterator = trange(numIterations, desc=description) if show_logs else range(numIterations)
            for it in iterator:
                q_flat = A_flat @ theta_flat
                # Appliquer le seuil : si q_flat < denominator_threshold, on met e_flat à 1 (comme dans le code C++)
                mask = q_flat >= denominator_threshold
                e_flat = torch.where(mask, y_flat / (q_flat + eps), torch.ones_like(q_flat))
                c_flat = A_flat.T @ e_flat
                theta_flat = (theta_flat / (norm_factor_flat + eps)) * c_flat
                if isSavingEachIteration and it in save_indices:
                    saved_theta.append(theta_flat.reshape(Z, X).clone())
                    saved_indices.append(it)
        # Free memory
        del A_flat, y_flat, norm_factor_flat
        torch.cuda.empty_cache()
        if isSavingEachIteration:
            return [t.cpu().numpy() for t in saved_theta], saved_indices
        else:
            return theta_flat.reshape(Z, X).cpu().numpy(), None
    except Exception as e:
        print(f"Error in single-GPU MLEM: {type(e).__name__}: {e}")
        torch.cuda.empty_cache()
        return None, None

def _MLEM_CPU_numba(SMatrix, y, numIterations, isSavingEachIteration, tumor_str, max_saves, denominator_threshold, show_logs=True):
    try:
        numba.set_num_threads(os.cpu_count())
        q_p = np.zeros((SMatrix.shape[0], SMatrix.shape[3]), dtype=np.float32)
        c_p = np.zeros((SMatrix.shape[1], SMatrix.shape[2]), dtype=np.float32)
        theta_p_0 = np.ones((SMatrix.shape[1], SMatrix.shape[2]), dtype=np.float32)
        matrix_theta = [theta_p_0]
        saved_indices = [0]
        normalization_factor = np.sum(SMatrix, axis=(0, 3)).astype(np.float32)

        # Calculate save indices
        if numIterations <= max_saves:
            save_indices = list(range(numIterations))
        else:
            step = numIterations // max_saves
            save_indices = list(range(0, numIterations, step))
            if save_indices[-1] != numIterations - 1:
                save_indices.append(numIterations - 1)

        description = f"AOT-BioMaps -- ML-EM ---- {tumor_str} TUMOR ---- processing on multithread CPU ({numba.config.NUMBA_DEFAULT_NUM_THREADS} threads) ----"
        iterator = trange(numIterations, desc=description) if show_logs else range(numIterations)

        for it in iterator:
            theta_p = matrix_theta[-1]
            _forward_projection(SMatrix, theta_p, q_p)

            # Appliquer le seuil : si q_p < denominator_threshold, on met e_p à 1
            mask = q_p >= denominator_threshold
            e_p = np.where(mask, y / (q_p + 1e-8), 1.0)

            _backward_projection(SMatrix, e_p, c_p)
            theta_p_plus_1 = theta_p / (normalization_factor + 1e-8) * c_p

            if isSavingEachIteration and (it + 1) in save_indices:
                matrix_theta.append(theta_p_plus_1)
                saved_indices.append(it + 1)
            else:
                matrix_theta[-1] = theta_p_plus_1

        if not isSavingEachIteration:
            return matrix_theta[-1], None
        else:
            return matrix_theta, saved_indices
    except Exception as e:
        print(f"Error in Numba CPU MLEM: {type(e).__name__}: {e}")
        return None, None

def _MLEM_CPU_opti(SMatrix, y, numIterations, isSavingEachIteration, tumor_str, max_saves, denominator_threshold, show_logs=True):
    try:
        T, Z, X, N = SMatrix.shape
        A_flat = SMatrix.astype(np.float32).transpose(0, 3, 1, 2).reshape(T * N, Z * X)
        y_flat = y.astype(np.float32).reshape(-1)
        theta_0 = np.ones((Z, X), dtype=np.float32)
        matrix_theta = [theta_0]
        saved_indices = [0]
        normalization_factor = np.sum(SMatrix, axis=(0, 3)).astype(np.float32)
        normalization_factor_flat = normalization_factor.reshape(-1)

        # Calculate save indices
        if numIterations <= max_saves:
            save_indices = list(range(numIterations))
        else:
            step = numIterations // max_saves
            save_indices = list(range(0, numIterations, step))
            if save_indices[-1] != numIterations - 1:
                save_indices.append(numIterations - 1)

        description = f"AOT-BioMaps -- ML-EM ---- {tumor_str} TUMOR ---- processing on single CPU (optimized) ----"
        iterator = trange(numIterations, desc=description) if show_logs else range(numIterations)

        for it in iterator:
            theta_p = matrix_theta[-1]
            theta_p_flat = theta_p.reshape(-1)
            q_flat = A_flat @ theta_p_flat

            # Appliquer le seuil : si q_flat < denominator_threshold, on met e_flat à 1
            mask = q_flat >= denominator_threshold
            e_flat = np.where(mask, y_flat / (q_flat + np.finfo(np.float32).tiny), 1.0)

            c_flat = A_flat.T @ e_flat
            theta_p_plus_1_flat = theta_p_flat / (normalization_factor_flat + np.finfo(np.float32).tiny) * c_flat
            theta_p_plus_1 = theta_p_plus_1_flat.reshape(Z, X)

            if isSavingEachIteration and (it + 1) in save_indices:
                matrix_theta.append(theta_p_plus_1)
                saved_indices.append(it + 1)
            else:
                matrix_theta[-1] = theta_p_plus_1

        if not isSavingEachIteration:
            return matrix_theta[-1], None
        else:
            return matrix_theta, saved_indices
    except Exception as e:
        print(f"Error in optimized CPU MLEM: {type(e).__name__}: {e}")
        return None, None
    
def MLEM_sparseCSR_pycuda(
    SMatrix,
    y,
    numIterations,
    isSavingEachIteration,
    tumor_str,
    max_saves,
    denominator_threshold,
    show_logs=True,
):
    """
    Robust MLEM implementation for CSR SMatrix using PyCUDA kernels.
    Expects SMatrix to be SparseSMatrix_CSR with attributes:
      - values_gpu, col_ind_gpu, row_ptr_gpu (device pointers)
      - norm_factor_inv_gpu (device pointer)
      - sparse_mod (loaded module with kernels)
      - ctx (PyCUDA context)
    Returns (saved_theta_list, saved_indices) if isSavingEachIteration else (final_theta, None)
    """
    final_result = None

    # Local holders to free in finally
    y_gpu = q_flat_gpu = e_flat_gpu = c_flat_gpu = theta_flat_gpu = None

    try:
        if not isinstance(SMatrix, SparseSMatrix_CSR):
            raise TypeError("SMatrix must be a SparseSMatrix_CSR object")

        # push context (if provided)
        popped_ctx = False
        if getattr(SMatrix, "ctx", None):
            SMatrix.ctx.push()
            popped_ctx = True

        dtype = np.float32
        TN = int(SMatrix.N * SMatrix.T)
        ZX = int(SMatrix.Z * SMatrix.X)
        Z = int(SMatrix.Z)
        X = int(SMatrix.X)

        # Make sure required GPU pointers exist
        if getattr(SMatrix, "values_gpu", None) is None or getattr(SMatrix, "col_ind_gpu", None) is None or getattr(SMatrix, "row_ptr_gpu", None) is None:
            raise RuntimeError("SMatrix is missing GPU buffers (values_gpu / col_ind_gpu / row_ptr_gpu)")

        if getattr(SMatrix, "norm_factor_inv_gpu", None) is None:
            raise RuntimeError("SMatrix.norm_factor_inv_gpu not available on GPU")

        # stream for async operations
        stream = drv.Stream()

        # prepare device buffers
        y_arr = np.ascontiguousarray(y.T.flatten().astype(np.float32))
        y_gpu = drv.mem_alloc(y_arr.nbytes)
        drv.memcpy_htod_async(y_gpu, y_arr, stream)

        theta_flat_gpu = drv.mem_alloc(ZX * np.dtype(dtype).itemsize)
        initial_theta = np.full(ZX, 0.1, dtype=dtype)
        drv.memcpy_htod_async(theta_flat_gpu, initial_theta, stream)

        norm_factor_inv_gpu = SMatrix.norm_factor_inv_gpu

        q_flat_gpu = drv.mem_alloc(TN * np.dtype(dtype).itemsize)
        e_flat_gpu = drv.mem_alloc(TN * np.dtype(dtype).itemsize)
        c_flat_gpu = drv.mem_alloc(ZX * np.dtype(dtype).itemsize)

        # Ensure kernels exist
        projection_kernel = SMatrix.sparse_mod.get_function("projection_kernel__CSR")
        backprojection_kernel = SMatrix.sparse_mod.get_function("backprojection_kernel__CSR")
        ratio_kernel = SMatrix.sparse_mod.get_function("ratio_kernel")
        update_kernel = SMatrix.sparse_mod.get_function("update_theta_kernel")
        block_size = 256

        # prepare save indices once
        if numIterations <= max_saves:
            save_indices = list(range(numIterations))
        else:
            step = max(1, numIterations // max_saves)
            save_indices = list(range(0, numIterations, step))
            if save_indices[-1] != numIterations - 1:
                save_indices.append(numIterations - 1)

        saved_theta = []
        saved_indices = []

        description = f"AOT-BioMaps -- ML-EM (CSR-sparse SMatrix) ---- {tumor_str} TUMOR ---- GPU {torch.cuda.current_device()}"
        iterator = trange(numIterations, desc=description) if show_logs else range(numIterations)

        # grid sizes
        grid_rows = ((TN + block_size - 1) // block_size, 1, 1)
        grid_cols = ((ZX + block_size - 1) // block_size, 1, 1)

        for it in iterator:
            # projection: q = A * theta
            projection_kernel(
                q_flat_gpu,
                SMatrix.values_gpu,
                SMatrix.row_ptr_gpu,
                SMatrix.col_ind_gpu,
                theta_flat_gpu,
                np.int32(TN),
                block=(block_size, 1, 1),
                grid=grid_rows,
                stream=stream,
            )

            # ratio: e = y / max(q, threshold)
            ratio_kernel(
                e_flat_gpu,
                y_gpu,
                q_flat_gpu,
                np.float32(denominator_threshold),
                np.int32(TN),
                block=(block_size, 1, 1),
                grid=grid_rows,
                stream=stream,
            )

            # backprojection: c = A^T * e  (zero c first)
            drv.memset_d32_async(c_flat_gpu, 0, ZX, stream)
            backprojection_kernel(
                c_flat_gpu,
                SMatrix.values_gpu,
                SMatrix.row_ptr_gpu,
                SMatrix.col_ind_gpu,
                e_flat_gpu,
                np.int32(TN),
                block=(block_size, 1, 1),
                grid=grid_rows,
                stream=stream,
            )

            # update: theta *= norm_factor_inv * c
            update_kernel(
                theta_flat_gpu,
                c_flat_gpu,
                norm_factor_inv_gpu,
                np.int32(ZX),
                block=(block_size, 1, 1),
                grid=grid_cols,
                stream=stream,
            )

            # periodic synchronization for stability / logging
            if show_logs and (it % 10 == 0 or it == numIterations - 1):
                stream.synchronize()

            # save snapshot if required
            if isSavingEachIteration and it in save_indices:
                # ensure kernels finished
                stream.synchronize()
                theta_host = np.empty(ZX, dtype=dtype)
                drv.memcpy_dtoh(theta_host, theta_flat_gpu)
                saved_theta.append(theta_host.reshape(Z, X))
                saved_indices.append(int(it))

        # make sure everything finished
        stream.synchronize()
        final_theta_host = np.empty(ZX, dtype=dtype)
        drv.memcpy_dtoh(final_theta_host, theta_flat_gpu)
        final_result = final_theta_host.reshape(Z, X)

        # free local allocations (will also be freed in finally if exception)
        try:
            y_gpu.free()
            q_flat_gpu.free()
            e_flat_gpu.free()
            c_flat_gpu.free()
            theta_flat_gpu.free()
        except Exception:
            pass

        return (saved_theta, saved_indices) if isSavingEachIteration else (final_result, None)

    except Exception as e:
        print(f"Error in MLEM_sparseCSR_pycuda: {type(e).__name__}: {e}")
        gc.collect()
        return None, None

    finally:
        # free buffers if still allocated
        for buf in ("y_gpu", "q_flat_gpu", "e_flat_gpu", "c_flat_gpu", "theta_flat_gpu"):
            try:
                val = locals().get(buf, None)
                if val is not None:
                    val.free()
            except Exception:
                pass
        # pop context safely
        try:
            if SMatrix and hasattr(SMatrix, "ctx") and SMatrix.ctx and popped_ctx:
                SMatrix.ctx.pop()
        except Exception:
            pass

def MLEM_sparseSELL_pycuda(
    SMatrix,
    y,
    numIterations,
    isSavingEachIteration,
    tumor_str,
    max_saves,
    denominator_threshold,
    show_logs=True,
):
    """
    MLEM using SELL-C-σ kernels already present on device.
    y must be float32 length TN.

    Version propre : diagnostics retirés.
    """
    final_result = None

    try:
        if not isinstance(SMatrix, SparseSMatrix_SELL):
            raise TypeError("SMatrix must be a SparseSMatrix_SELL object")
        if SMatrix.sell_values_gpu is None:
            raise RuntimeError("SELL not built. Call allocate_sell_c_sigma_direct() first.")

        # Context
        if SMatrix.ctx:
            SMatrix.ctx.push()

        TN = int(SMatrix.N * SMatrix.T)
        ZX = int(SMatrix.Z * SMatrix.X)
        dtype = np.float32
        block_size = 256

        proj = SMatrix.sparse_mod.get_function("projection_kernel__SELL")
        backproj = SMatrix.sparse_mod.get_function("backprojection_kernel__SELL")
        ratio = SMatrix.sparse_mod.get_function("ratio_kernel")
        update = SMatrix.sparse_mod.get_function("update_theta_kernel")

        stream = drv.Stream()

        # Device buffers
        y = y.T.flatten().astype(np.float32)
        y_gpu = drv.mem_alloc(y.nbytes)
        drv.memcpy_htod_async(y_gpu, y.astype(dtype), stream)

        theta_gpu = drv.mem_alloc(ZX * np.dtype(dtype).itemsize)
        drv.memcpy_htod_async(theta_gpu, np.full(ZX, 0.1, dtype=dtype), stream)

        q_gpu = drv.mem_alloc(TN * np.dtype(dtype).itemsize)
        e_gpu = drv.mem_alloc(TN * np.dtype(dtype).itemsize)
        c_gpu = drv.mem_alloc(ZX * np.dtype(dtype).itemsize)

        slice_ptr_gpu = SMatrix.slice_ptr_gpu
        slice_len_gpu = SMatrix.slice_len_gpu
        slice_height = np.int32(SMatrix.slice_height)

        grid_rows = ((TN + block_size - 1) // block_size, 1, 1)
        grid_cols = ((ZX + block_size - 1) // block_size, 1, 1)

        # Prepare save indices
        saved_theta, saved_indices = [], []
        if numIterations <= max_saves:
            save_indices = list(range(numIterations))
        else:
            save_indices = list(range(0, numIterations, max(1, numIterations // max_saves)))
            if save_indices[-1] != numIterations - 1:
                save_indices.append(numIterations - 1)

        description = f"AOT-BioMaps -- ML-EM (SELL-c-σ-sparse SMatrix) ---- {tumor_str} TUMOR ---- GPU {torch.cuda.current_device()}"
        iterator = trange(numIterations, desc=description) if show_logs else range(numIterations)

        # --- MLEM Loop ---
        for it in iterator:

            proj(q_gpu, SMatrix.sell_values_gpu, SMatrix.sell_colinds_gpu,
                 slice_ptr_gpu, slice_len_gpu,
                 theta_gpu, np.int32(TN), slice_height,
                 block=(block_size,1,1), grid=grid_rows, stream=stream)

            ratio(e_gpu, y_gpu, q_gpu, np.float32(denominator_threshold), np.int32(TN),
                  block=(block_size,1,1), grid=grid_rows, stream=stream)

            drv.memset_d32_async(c_gpu, 0, ZX, stream)

            backproj(SMatrix.sell_values_gpu, SMatrix.sell_colinds_gpu,
                     slice_ptr_gpu, slice_len_gpu,
                     e_gpu, c_gpu, np.int32(TN), slice_height,
                     block=(block_size,1,1), grid=grid_rows, stream=stream)

            update(theta_gpu, c_gpu, SMatrix.norm_factor_inv_gpu, np.int32(ZX),
                   block=(block_size,1,1), grid=grid_cols, stream=stream)

            if isSavingEachIteration and it in save_indices:
                out = np.empty(ZX, dtype=np.float32)
                drv.memcpy_dtoh(out, theta_gpu)
                saved_theta.append(out.reshape((SMatrix.Z, SMatrix.X)))
                saved_indices.append(it)

        stream.synchronize()
        res = np.empty(ZX, dtype=np.float32)
        drv.memcpy_dtoh(res, theta_gpu)

        # free
        try:
            y_gpu.free()
            q_gpu.free()
            e_gpu.free()
            c_gpu.free()
            theta_gpu.free()
        except Exception:
            pass

        final_result = res.reshape((SMatrix.Z, SMatrix.X))
        return (saved_theta, saved_indices) if isSavingEachIteration else (final_result, None)

    except Exception as e:
        print(f"Error in MLEM_sparseSELL_pycuda: {type(e).__name__}: {e}")
        gc.collect()
        return None, None

    finally:
        if SMatrix and hasattr(SMatrix, 'ctx') and SMatrix.ctx:
            try:
                SMatrix.ctx.pop()
            except Exception:
                pass
            