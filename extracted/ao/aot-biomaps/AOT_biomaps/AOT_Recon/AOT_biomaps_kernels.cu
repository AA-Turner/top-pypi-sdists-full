/**
 * AOT_biomaps_kernels.cu
 * 
 * Centralized CUDA kernels for sparse matrix operations on GPU.
 * All custom CUDA kernels are organized in this file with:
 * - Clear naming convention: module_operation_purpose
 * - English documentation
 * - Consistent error handling
 * - Optimized for performance
 */

extern "C"{
    // ============================================================================
    // SMATRIX KERNELS
    // ============================================================================

    /**
    * Kernel: fill_kernel__DENSE
    * Purpose: Fill dense matrix from acoustic fields on GPU
    * Used for: DENSE matrix construction
    */
    __global__ void fill_kernel__DENSE(
        float* __restrict__ dense_matrix,
        const float* __restrict__ field_data,
        int T,
        int N,
        int Z,
        int X,
        int n
    ) {
        int idx = blockIdx.x * blockDim.x + threadIdx.x;
        if (idx >= T * Z * X) return;

        int t = idx / (Z * X);
        int zx = idx % (Z * X);
        int z = zx / X;
        int x = zx % X;

        // Position in dense_matrix: [t, n, z, x]
        int dense_idx = t * (N * Z * X) + n * (Z * X) + z * X + x;

        // Position in field_data: [t, z, x] (1D array of size T * Z * X)
        int field_idx = t * (Z * X) + z * X + x;

        if (dense_idx < T * N * Z * X && field_idx < T * Z * X) {
            dense_matrix[dense_idx] = field_data[field_idx];
        }
    }

    /**
    * Kernel: fill_kernel__SELL
    * Purpose: Fill SELL-C-sigma format from dense matrix block
    * Used for: SELL-C-sigma sparse matrix construction
    */
    __global__ void fill_kernel__SELL(
        const float* __restrict__ dense,
        const int* __restrict__ row_nnz,
        const long long* __restrict__ slice_ptr,
        const int* __restrict__ slice_len,
        unsigned int* __restrict__ col_ind,
        float* __restrict__ values_out,
        int rows_in_block,
        int cols,
        int rows_global_offset,
        int slice_height,
        float thr_rel
    ) {
        int r_local = blockIdx.x * blockDim.x + threadIdx.x;
        if (r_local >= rows_in_block) return;
        int r_global = rows_global_offset + r_local;
        int slice_id = r_global / slice_height;
        int row_in_slice = r_global % slice_height;
        
        const float* row = dense + (long long)r_local * cols;
        float maxv = 0.0f;
        for (int c = 0; c < cols; ++c) {
            float v = fabsf(row[c]);
            if (v > maxv) maxv = v;
        }
        float cut = maxv * thr_rel;
        
        long long base = slice_ptr[slice_id];
        int len = slice_len[slice_id];
        long long out_base = base + (long long)row_in_slice;
        
        int k = 0;
        for (int c = 0; c < cols; ++c) {
            float v = row[c];
            if (fabsf(v) > cut) {
                long long pos = out_base + (long long)k * slice_height;
                values_out[pos] = v;
                col_ind[pos] = (unsigned int)c;
                ++k;
            }
        }
        for (; k < len; ++k) {
            long long pos = out_base + (long long)k * slice_height;
            values_out[pos] = 0.0f;
            col_ind[pos] = 0u;
        }
    }

    /**
    * Kernel: fill_kernel__CSR
    * Purpose: Fill CSR format from dense matrix block
    * Used for: CSR sparse matrix construction
    */
    __global__ void fill_kernel__CSR(
        const float* __restrict__ dense_block,
        const long long* __restrict__ row_ptr,
        unsigned int* __restrict__ col_ind,
        float* __restrict__ values,
        int block_start_row,
        int current_rows,
        int num_cols,
        float relative_threshold,
        long long total_nnz
    ) {
        int row = blockIdx.x * blockDim.x + threadIdx.x;
        if (row >= current_rows) return;
        int global_row = block_start_row + row;
        
        const float* row_ptr_local = dense_block + (long long)row * num_cols;
        
        float row_max = 0.f;
        for (int c = 0; c < num_cols; ++c) {
            float v = fabsf(row_ptr_local[c]);
            if (v > row_max) row_max = v;
        }
        float thr = row_max * relative_threshold;
        
        long long base = row_ptr[global_row];
        int nnz = 0;
        for (int c = 0; c < num_cols; ++c) {
            float v = row_ptr_local[c];
            if (fabsf(v) > thr) {
                long long pos = base + nnz;
                if (pos < total_nnz) {
                    col_ind[pos] = (unsigned int)c;
                    values[pos] = v;
                }
                nnz++;
            }
        }
    }

    /**
    * Kernel: forward_projection_kernel__DENSE
    * Purpose: Forward projection using DENSE format: q = A * theta
    * Layout expectation: row = n * T + t
    */
    __global__ void forward_projection_kernel__DENSE(
        float* __restrict__ q_out,
        const float* __restrict__ dense_matrix,
        const float* __restrict__ theta,
        int T,
        int N,
        int Z,
        int X
    ) {
        int row = blockIdx.x * blockDim.x + threadIdx.x;
        if (row >= N * T) return;

        int n = row / T;
        int t = row % T;

        float sum = 0.0f;
        for (int z = 0; z < Z; z++) {
            for (int x = 0; x < X; x++) {
                long long pos = (((long long)t * N + n) * Z + z) * X + x;
                long long theta_idx = (long long)z * X + x;
                
                sum += dense_matrix[pos] * theta[theta_idx];
            }
        }
        q_out[row] = sum;
    }

    /**
    * Kernel: forward_projection_kernel__SELL
    * Purpose: Forward projection using SELL format: q = A * theta
    */
    __global__ void forward_projection_kernel__SELL(
        float* __restrict__ q_out,
        const float* __restrict__ sell_values,
        const unsigned int* __restrict__ sell_colinds,
        const long long* __restrict__ slice_ptr,
        const int* __restrict__ slice_len,
        const float* __restrict__ theta,
        int num_rows,
        int slice_height
    ) {
        int row = blockIdx.x * blockDim.x + threadIdx.x;
        if (row >= num_rows) return;
        
        int slice_id = row / slice_height;
        int row_in_slice = row % slice_height;
        long long base = slice_ptr[slice_id];
        int len = slice_len[slice_id];
        
        float acc = 0.0f;
        long long pos = base + (long long)row_in_slice;
        for (int j = 0; j < len; ++j) {
            float v = sell_values[pos];
            if (v != 0.0f) {
                unsigned int col = sell_colinds[pos];
                float t = __ldg(&theta[col]);
                acc += v * t;
            }
            pos += (long long)slice_height;
        }
        q_out[row] = acc;
    }

    /**
    * Kernel: forward_projection_kernel__CSR
    * Purpose: Forward projection using CSR format: q = A * theta
    */
    __global__ void forward_projection_kernel__CSR(
        float* __restrict__ q_flat,
        const float* __restrict__ values,
        const long long* __restrict__ row_ptr,
        const unsigned int* __restrict__ col_ind,
        const float* __restrict__ theta_flat,
        int TN
    ) {
        int row = blockIdx.x * blockDim.x + threadIdx.x;
        if (row >= TN) return;
        
        long long start = row_ptr[row];
        long long end = row_ptr[row + 1];
        
        float sum = 0.f;
        for (long long i = start; i < end; ++i) {
            sum += values[i] * theta_flat[col_ind[i]];
        }
        q_flat[row] = sum;
    }

    /**
    * Kernel: backward_projection_kernel__DENSE
    * Purpose: Backward projection using DENSE format: c = A^T * e
    * Layout expectation: col = z * X + x
    */
    __global__ void backward_projection_kernel__DENSE(
        float* __restrict__ c_out,
        const float* __restrict__ dense_matrix,
        const float* __restrict__ e,
        int T,
        int N,
        int Z,
        int X
    ) {
        int col = blockIdx.x * blockDim.x + threadIdx.x;
        if (col >= Z * X) return;

        int z = col / X;
        int x = col % X;

        float sum = 0.0f;
        for (int n = 0; n < N; n++) {
            for (int t = 0; t < T; t++) {
                long long e_idx = (long long)n * T + t;
                long long pos = (((long long)t * N + n) * Z + z) * X + x;
                
                sum += dense_matrix[pos] * e[e_idx];
            }
        }
        c_out[col] = sum;
    }

    /**
    * Kernel: backward_projection_kernel__SELL
    * Purpose: backward projection using SELL format: c += A^T * e
    */
    __global__ void backward_projection_kernel__SELL(
        const float* __restrict__ sell_values,
        const unsigned int* __restrict__ sell_colinds,
        const long long* __restrict__ slice_ptr,
        const int* __restrict__ slice_len,
        const float* __restrict__ e_flat,
        float* __restrict__ c_flat,
        int num_rows,
        int slice_height
    ) {
        int row = blockIdx.x * blockDim.x + threadIdx.x;
        if (row >= num_rows) return;
        
        float e = e_flat[row];
        if (e == 0.0f) return;
        
        int slice_id = row / slice_height;
        int row_in_slice = row % slice_height;
        long long base = slice_ptr[slice_id];
        int len = slice_len[slice_id];
        
        long long pos = base + (long long)row_in_slice;
        for (int j = 0; j < len; ++j) {
            float v = sell_values[pos];
            if (v != 0.0f) {
                unsigned int col = sell_colinds[pos];
                float contrib = v * e;
                atomicAdd(&c_flat[col], contrib);
            }
            pos += (long long)slice_height;
        }
    }

    /**
    * Kernel: backward_projection_kernel__CSR
    * Purpose: backward projection using CSR format: c += A^T * e
    */
    __global__ void backward_projection_kernel__CSR(
        float* __restrict__ c_flat,
        const float* __restrict__ values,
        const long long* __restrict__ row_ptr,
        const unsigned int* __restrict__ col_ind,
        const float* __restrict__ e_flat,
        int TN
    ) {
        int row = blockIdx.x * blockDim.x + threadIdx.x;
        if (row >= TN) return;
        
        float e = e_flat[row];
        long long start = row_ptr[row];
        long long end = row_ptr[row + 1];
        
        for (long long i = start; i < end; ++i) {
            unsigned int col = col_ind[i];
            float contrib = values[i] * e;
            atomicAdd(&c_flat[col], contrib);
        }
    }

    /**
    * Kernel: apply_apodization_sell
    * Purpose: Apply apodization window to SELL matrix values
    * Used for: Acoustic field correction
    */
    __global__ void apply_apodization_kernel__SELL(
        float* sell_values,
        const unsigned int* sell_colinds,
        const float* window_vector,
        long long num_elements,
        unsigned int ZX
    ) {
        long long i = (long long)blockIdx.x * blockDim.x + threadIdx.x;
        if (i < num_elements) {
            unsigned int pixel_index = sell_colinds[i];
            if (pixel_index < ZX) {
                sell_values[i] *= window_vector[pixel_index];
            }
        }
    }

    /**
    * Kernel: compute_norm_factor_dense
    * Purpose: Compute normalization factor for dense matrix: 1 / (sum(|A|) + eps)
    * Used for: DENSE matrix normalization
    */
    __global__ void compute_norm_factor_dense_kernel(
        const float* __restrict__ dense_matrix,
        float* __restrict__ norm_factor_inv,
        int T,
        int N,
        int Z,
        int X
    ) {
        int idx = blockIdx.x * blockDim.x + threadIdx.x;
        if (idx >= Z * X) return;
        
        // Each thread computes sum of absolute values for one column
        float sum_abs = 0.0f;
        for (int t = 0; t < T; t++) {
            for (int n = 0; n < N; n++) {
                int pos = t * N * Z * X + n * Z * X + idx;
                sum_abs += fabsf(dense_matrix[pos]);
            }
        }
        
        // Store sum for this column
        float* sum_buffer = norm_factor_inv; // Reuse buffer for sum
        sum_buffer[idx] = sum_abs;
        
        __syncthreads();
        
        // Reduction in shared memory (simplified - actual reduction would need more work)
        // For now, we'll do this in Python after kernel execution
    }

    /**
    * Kernel: count_nnz_rows
    * Purpose: Count non-zero elements per row in a dense matrix block
    * Used for: CSR and SELL-C-sigma matrix construction
    */
    __global__ void count_nnz_rows_kernel(
        const float* __restrict__ dense,
        int* __restrict__ row_nnz,
        int rows_in_block,
        int cols,
        float thr_rel
    ) {
        int r = blockIdx.x * blockDim.x + threadIdx.x;
        if (r >= rows_in_block) return;
        
        const float* row = dense + (long long)r * cols;
        float maxv = 0.0f;
        for (int c = 0; c < cols; ++c) {
            float v = fabsf(row[c]);
            if (v > maxv) maxv = v;
        }
        float cut = maxv * thr_rel;
        int cnt = 0;
        for (int c = 0; c < cols; ++c) {
            if (fabsf(row[c]) > cut) ++cnt;
        }
        row_nnz[r] = cnt;
    }

    /**
    * Kernel: accumulate_columns_atomic
    * Purpose: Accumulate column sums from CSR matrix using atomic operations
    * Used for: Matrix analysis, normalization
    */
    __global__ void accumulate_columns_atomic(
        const float* __restrict__ values,
        const unsigned int* __restrict__ col_ind,
        long long total_nnz,
        float* __restrict__ col_sum
    ) {
        const unsigned full_mask = 0xffffffffu;
        long long gid = (long long)blockIdx.x * blockDim.x + threadIdx.x;
        long long stride = (long long)blockDim.x * gridDim.x;
        int lane = threadIdx.x & 31;
        
        for (long long idx = gid; idx < total_nnz; idx += stride) {
            unsigned int col = col_ind[idx];
            float v = values[idx];
            if (v == 0.0f) continue;
            
            float sum = v;
            for (int offset = 1; offset <= 16; offset <<= 1) {
                unsigned int col_down = __shfl_down_sync(full_mask, col, offset);
                float sum_down = __shfl_down_sync(full_mask, sum, offset);
                if (col_down == col) {
                    sum += sum_down;
                }
            }
            
            unsigned int col_up = __shfl_up_sync(full_mask, col, 1);
            bool is_head = (lane == 0) || (col_up != col);
            
            if (is_head) {
                atomicAdd(&col_sum[col], sum);
            }
        }
    }
}