"""
SMatrix_CSR.py

CSR (Compressed Sparse Row) sparse matrix construction and operations.
Supports both CPU (NumPy) and GPU (CuPy) implementations.
"""

import os
import warnings
import numpy as np
from tqdm import trange
from typing import Optional, Union

from AOT_biomaps.AOT_Recon.AOT_SMatrix._mainSMatrix import SMatrix
from AOT_biomaps.AOT_Recon.ReconEnums import SMatrixType
from AOT_biomaps.AOT_Recon.ReconTools import check_gpu_available

# Check for CuPy availability
try:
    import cupy as cp
    CUPY_AVAILABLE = True
except ImportError:
    cp = None
    CUPY_AVAILABLE = False


class SMatrix_CSR(SMatrix):
    """
    Construction of a CSR matrix from a `experiment` object.

    Supports both CPU and GPU implementations:
    - On GPU: Uses CuPy for memory management and custom CUDA kernels (compiled from source)
    - On CPU: Uses NumPy arrays and CPU implementations

    Usage:
        S = SMatrix_CSR(experiment, device='gpu')  # or 'cpu'
        S.allocate()

    After allocate(), the following attributes are available:
    - row_ptr: Row pointer array (host)
    - col_ind: Column indices array (host)
    - values: Non-zero values array (host)
    - norm_factor_inv: Normalization factor (host)
    - For GPU: row_ptr_gpu, col_ind_gpu, values_gpu, norm_factor_inv_gpu
    """

    def __init__(self, block_rows: int = 128, relative_threshold: float = 0.01,**kwargs):
        """
        Initialize CSR sparse matrix.
        Args:
            **kwargs: Arguments passed to base SMatrix class
                - experiment: Experiment object containing AcousticFields
                - device: 'cpu' or 'gpu:{gpu_id}' (optional, defaults to GPU if available)
            block_rows: Number of rows to process per block when building on GPU (default: 128)
            relative_threshold: Relative threshold for sparsity (default: 0.01)
        """
        super().__init__(**kwargs)
        self.matrix_type = SMatrixType.CSR
        
        self.block_rows = block_rows
        self.relative_threshold = relative_threshold
        
        self.row_ptr = None
        self.h_col_ind = None
        self.h_values = None
        self.total_nnz = 0

        self.row_ptr_gpu = None
        self.col_ind_gpu = None
        self.values_gpu = None

    def _allocate_gpu(self):
        """Allocate and fill the CSR matrix on GPU using 1-Pass PCIe strategy."""
        num_rows = self.N * self.T
        num_cols = self.Z * self.X
        br = self.block_rows

        # Initialize global row pointer
        self.row_ptr = np.zeros(num_rows + 1, dtype=np.int64)

        # Temporary lists to hold local blocks of sparse data
        col_ind_list = []
        values_list = []

        dense_block_host = np.empty((br, num_cols), dtype=np.float32)
        count_nnz_kernel = self.sparse_mod.get_function('count_nnz_rows_kernel')
        fill_csr_kernel = self.sparse_mod.get_function('fill_kernel__CSR')
        block_size = 256

        for b in trange(0, num_rows, br, desc='Building CSR (1-Pass GPU)'):
            current_rows = min(br, num_rows - b)
            
            # Extract dense block from CPU experiment
            for r in range(current_rows):
                global_row = b + r
                n_idx = global_row // self.T
                t_idx = global_row % self.T
                dense_block_host[r, :] = self.experiment.AcousticFields[n_idx].field[t_idx].flatten()

            # 1. Send dense data to GPU ONCE
            dense_block_gpu = cp.asarray(dense_block_host[:current_rows])
            row_nnz_gpu = cp.zeros(current_rows, dtype=np.int32)

            grid = ((current_rows + block_size - 1) // block_size, 1, 1)
            
            # 2. Count NNZ
            count_nnz_kernel(
                grid=grid, block=(block_size, 1, 1),
                args=[dense_block_gpu, row_nnz_gpu, np.int32(current_rows), np.int32(num_cols),
                      np.float32(self.relative_threshold)]
            )
            cp.cuda.Stream.null.synchronize()

            # 3. Compute local offsets
            row_nnz_host = cp.asnumpy(row_nnz_gpu)
            local_row_ptr = np.zeros(current_rows + 1, dtype=np.int64)
            local_row_ptr[1:] = np.cumsum(row_nnz_host)
            local_nnz = int(local_row_ptr[-1])

            # Accumulate into global row_ptr
            self.row_ptr[b + 1 : b + current_rows + 1] = self.row_ptr[b] + local_row_ptr[1:]

            if local_nnz > 0:
                # 4. Fill local CSR exactly where the data lives
                local_row_ptr_gpu = cp.asarray(local_row_ptr)
                local_col_ind_gpu = cp.empty(local_nnz, dtype=np.uint32)
                local_values_gpu = cp.empty(local_nnz, dtype=np.float32)

                fill_csr_kernel(
                    grid=grid, block=(block_size, 1, 1),
                    args=[dense_block_gpu, local_row_ptr_gpu, local_col_ind_gpu, local_values_gpu,
                          np.int32(current_rows), np.int32(num_cols),
                          np.float32(self.relative_threshold), np.int64(local_nnz)]
                )
                cp.cuda.Stream.null.synchronize()

                # 5. Bring compressed data back to CPU
                col_ind_list.append(cp.asnumpy(local_col_ind_gpu))
                values_list.append(cp.asnumpy(local_values_gpu))

        self.total_nnz = int(self.row_ptr[-1])

        # 6. Concatenate locally constructed CSR blocks
        if self.total_nnz > 0:
            self.h_col_ind = np.concatenate(col_ind_list)
            self.h_values = np.concatenate(values_list)
        else:
            self.h_col_ind = np.array([], dtype=np.uint32)
            self.h_values = np.array([], dtype=np.float32)

        # 7. Final unified GPU transfer for operations
        self.row_ptr_gpu = cp.asarray(self.row_ptr)
        self.col_ind_gpu = cp.asarray(self.h_col_ind)
        self.values_gpu = cp.asarray(self.h_values)

        self.compute_norm_factor()
        del self.h_col_ind
        del self.h_values
        self.h_col_ind = None
        self.h_values = None

    def _allocate_cpu(self):
        """Allocate and fill the CSR matrix on CPU."""
        num_rows = self.N * self.T
        num_cols = self.Z * self.X

        self.row_ptr = np.zeros(num_rows + 1, dtype=np.int64)

        for global_row in trange(num_rows, desc='Counting NNZ (CPU)'):
            n_idx = global_row // self.T
            t_idx = global_row % self.T
            row = self.experiment.AcousticFields[n_idx].field[t_idx].flatten()
            row_max = np.max(np.abs(row))
            thr = row_max * self.relative_threshold
            nnz = np.count_nonzero(np.abs(row) > thr)
            self.row_ptr[global_row + 1] = self.row_ptr[global_row] + nnz

        self.total_nnz = int(self.row_ptr[-1])
        self.h_col_ind = np.zeros(self.total_nnz, dtype=np.uint32)
        self.h_values = np.zeros(self.total_nnz, dtype=np.float32)

        ptr = 0
        for global_row in trange(num_rows, desc='Filling CSR (CPU)'):
            n_idx = global_row // self.T
            t_idx = global_row % self.T
            row = self.experiment.AcousticFields[n_idx].field[t_idx].flatten()
            row_max = np.max(np.abs(row))
            thr = row_max * self.relative_threshold

            for col in range(num_cols):
                if np.abs(row[col]) > thr:
                    self.h_col_ind[ptr] = col
                    self.h_values[ptr] = row[col]
                    ptr += 1

        self.compute_norm_factor()

    def compute_norm_factor(self):
        """Compute normalization factor from CSR matrix by summing absolute values."""
        ZX = self.Z * self.X

        if check_gpu_available(self):
            col_sum_gpu = cp.zeros(ZX, dtype=np.float32)
            acc_kernel = self.sparse_mod.get_function("accumulate_columns_atomic")
            threads = 256
            blocks = (self.total_nnz + threads - 1) // threads

            acc_kernel(
                grid=(blocks, 1), block=(threads, 1, 1),
                args=[self.values_gpu, self.col_ind_gpu, np.int64(self.total_nnz), col_sum_gpu]
            )
            cp.cuda.Stream.null.synchronize()
            norm = cp.asnumpy(col_sum_gpu)
        else:
            norm = np.zeros(ZX, dtype=np.float32)
            for i in range(self.total_nnz):
                col = int(self.h_col_ind[i])
                norm[col] += np.abs(self.h_values[i])

        norm = np.maximum(norm.astype(np.float64), 1e-6)
        self.norm_factor_inv = (1.0 / norm).astype(np.float32)

        if CUPY_AVAILABLE:
            self.norm_factor_inv_gpu = cp.asarray(self.norm_factor_inv)

    def forward_projection(self, theta: Union[np.ndarray, "cp.ndarray"]) -> Union[np.ndarray, "cp.ndarray"]:
        """Perform forward projection: q = A * theta"""
        if check_gpu_available(self):
            theta_gpu = cp.asarray(theta) if not isinstance(theta, cp.ndarray) else theta
            q_gpu = cp.zeros(self.N * self.T, dtype=np.float32)

            proj_kernel = self.sparse_mod.get_function('forward_projection_kernel__CSR')
            threads = 256
            blocks = (self.N * self.T + threads - 1) // threads

            proj_kernel(
                grid=(blocks, 1), block=(threads, 1, 1),
                args=[q_gpu.data.ptr, self.values_gpu, self.row_ptr_gpu, self.col_ind_gpu,
                      theta_gpu.data.ptr, np.int32(self.N * self.T)]
            )
            cp.cuda.Stream.null.synchronize()
            return q_gpu
        else:
            theta_cpu = np.asarray(theta) if not isinstance(theta, np.ndarray) else theta
            if isinstance(theta_cpu, cp.ndarray):
                theta_cpu = cp.asnumpy(theta_cpu)

            q = np.zeros(self.N * self.T, dtype=np.float32)
            for i in range(self.N * self.T):
                start = int(self.row_ptr[i])
                end = int(self.row_ptr[i + 1])
                q[i] = np.sum(self.h_values[start:end] * theta_cpu[self.h_col_ind[start:end]])
            return q

    def backward_projection(self, e: Union[np.ndarray, "cp.ndarray"]) -> Union[np.ndarray, "cp.ndarray"]:
        """Perform backward projection: c = A^T * e"""
        if check_gpu_available(self):
            e_gpu = cp.asarray(e) if not isinstance(e, cp.ndarray) else e
            c_gpu = cp.zeros(self.Z * self.X, dtype=np.float32)

            backproj_kernel = self.sparse_mod.get_function('backward_projection_kernel__CSR')
            threads = 256
            blocks = (self.N * self.T + threads - 1) // threads

            backproj_kernel(
                grid=(blocks, 1), block=(threads, 1, 1),
                args=[c_gpu.data.ptr, self.values_gpu, self.row_ptr_gpu, self.col_ind_gpu,
                      e_gpu.data.ptr, np.int32(self.N * self.T)]
            )
            cp.cuda.Stream.null.synchronize()
            return c_gpu
        else:
            e_cpu = np.asarray(e) if not isinstance(e, np.ndarray) else e
            if isinstance(e_cpu, cp.ndarray):
                e_cpu = cp.asnumpy(e_cpu)

            c = np.zeros(self.Z * self.X, dtype=np.float32)
            for i in range(self.N * self.T):
                start = int(self.row_ptr[i])
                end = int(self.row_ptr[i + 1])
                for j in range(start, end):
                    col = int(self.h_col_ind[j])
                    c[col] += self.h_values[j] * e_cpu[i]
            return c

    def apply_apodization(self, window_vector: Union[np.ndarray, 'cp.ndarray']):
        raise NotImplementedError("Apodization not implemented for CSR matrix.")

    def flip_probe(self):
        """Permute the columns of the CSR matrix corresponding to opposite angles."""
        if self.N % 2 != 0:
            raise ValueError("Number of angles must be even to permute opposite angles.")

        new_col_ind = self.h_col_ind.copy()
        ZX = self.Z * self.X
        angle_block_size = ZX // self.N

        for n in range(self.N // 2):
            n_opposite = n + self.N // 2
            block_n_start = n * angle_block_size
            block_n_end = (n + 1) * angle_block_size
            block_opposite_start = n_opposite * angle_block_size
            block_opposite_end = (n_opposite + 1) * angle_block_size

            mask_n = (self.h_col_ind >= block_n_start) & (self.h_col_ind < block_n_end)
            mask_opposite = (self.h_col_ind >= block_opposite_start) & (self.h_col_ind < block_opposite_end)

            new_col_ind[mask_n] = self.h_col_ind[mask_n] - block_n_start + block_opposite_start
            new_col_ind[mask_opposite] = self.h_col_ind[mask_opposite] - block_opposite_start + block_n_start

        self.h_col_ind = new_col_ind
        self.compute_norm_factor()

        if CUPY_AVAILABLE and self.col_ind_gpu is not None:
            self.col_ind_gpu = cp.asarray(self.h_col_ind)

    def compute_density(self) -> float:
        """
        Returns the actual density of the CSR matrix in percentage.
        """
        if self.row_ptr is None and self.row_ptr_gpu is None:
            raise RuntimeError("Sparse matrix not allocated yet.")
            
        num_rows = int(self.N * self.T)
        num_cols = int(self.Z * self.X)
        density_ratio = self.total_nnz / (num_rows * num_cols)
        
        return density_ratio * 100.0

    def get_matrix_size(self) -> dict:
        """Returns the total size of the CSR matrix in GB."""
        if self.row_ptr is None and self.row_ptr_gpu is None:
            return {"error": "Sparse matrix not allocated yet."}

        total_bytes = 0
        
        if self.row_ptr is not None: total_bytes += self.row_ptr.nbytes
        if self.h_col_ind is not None: total_bytes += self.h_col_ind.nbytes
        if self.h_values is not None: total_bytes += self.h_values.nbytes
        if self.norm_factor_inv is not None: total_bytes += self.norm_factor_inv.nbytes

        if self.row_ptr_gpu is not None: total_bytes += self.row_ptr_gpu.nbytes
        if self.col_ind_gpu is not None: total_bytes += self.col_ind_gpu.nbytes
        if self.values_gpu is not None: total_bytes += self.values_gpu.nbytes
        if self.norm_factor_inv_gpu is not None: total_bytes += self.norm_factor_inv_gpu.nbytes

        return {
            "total_bytes": total_bytes,
            "total_gb": total_bytes / (1024**3),
            "device": self.device
        }

    def _free_specific(self):
        """Free all GPU memory allocated by the CSR matrix."""
        try:
            for attr in ['col_ind_gpu', 'values_gpu', 'row_ptr_gpu', 'norm_factor_inv_gpu']:
                gpu_mem = getattr(self, attr, None)
                if gpu_mem is not None:
                    try:
                        if hasattr(gpu_mem, 'free'): gpu_mem.free()
                        else: del gpu_mem
                    except:
                        pass
                    setattr(self, attr, None)
        except Exception as e:
            warnings.warn(f"Error freeing GPU memory: {e}")