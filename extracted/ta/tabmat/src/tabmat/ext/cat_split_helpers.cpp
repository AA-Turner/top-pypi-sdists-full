#include <vector>
#include <omp.h>










template <typename Int, typename F>
void _sandwich_cat_denseC_fast(
    F* d,
    const Int* indices,
    Int* rows,
    Int len_rows,
    Int* j_cols,
    Int len_j_cols,
    F* res,
    Int res_size,
    F* mat_j,
    Int mat_j_nrow,
    Int mat_j_ncol
    )
{
    #pragma omp parallel
    {
        std::vector<F> restemp(res_size, 0.0);
        #pragma omp for
        for (Py_ssize_t k_idx = 0; k_idx < len_rows; k_idx++) {
            Py_ssize_t k = rows[k_idx];
            // MAYBE TODO: explore whether the column restriction slows things down a
            // lot, particularly if not restricting the columns allows using SIMD
            // instructions
            // MAYBE TODO: explore whether swapping the loop order for F-ordered mat_j
            // is useful.
                Py_ssize_t i = indices[k];
                for (Py_ssize_t j_idx = 0; j_idx < len_j_cols; j_idx++) {
                    Py_ssize_t j = j_cols[j_idx];
                        restemp[i * len_j_cols + j_idx] += d[k] * mat_j[k * mat_j_ncol + j];
                }
        }
        for (Py_ssize_t i = 0; i < res_size; i++) {
            #pragma omp atomic
            res[i] += restemp[i];
        }
    }
}


template <typename Int, typename F>
void _sandwich_cat_denseF_fast(
    F* d,
    const Int* indices,
    Int* rows,
    Int len_rows,
    Int* j_cols,
    Int len_j_cols,
    F* res,
    Int res_size,
    F* mat_j,
    Int mat_j_nrow,
    Int mat_j_ncol
    )
{
    #pragma omp parallel
    {
        std::vector<F> restemp(res_size, 0.0);
        #pragma omp for
        for (Py_ssize_t k_idx = 0; k_idx < len_rows; k_idx++) {
            Py_ssize_t k = rows[k_idx];
            // MAYBE TODO: explore whether the column restriction slows things down a
            // lot, particularly if not restricting the columns allows using SIMD
            // instructions
            // MAYBE TODO: explore whether swapping the loop order for F-ordered mat_j
            // is useful.
                Py_ssize_t i = indices[k];
                for (Py_ssize_t j_idx = 0; j_idx < len_j_cols; j_idx++) {
                    Py_ssize_t j = j_cols[j_idx];
                        restemp[i * len_j_cols + j_idx] += d[k] * mat_j[j * mat_j_nrow + k];
                }
        }
        for (Py_ssize_t i = 0; i < res_size; i++) {
            #pragma omp atomic
            res[i] += restemp[i];
        }
    }
}


template <typename Int, typename F>
void _sandwich_cat_denseC_complex(
    F* d,
    const Int* indices,
    Int* rows,
    Int len_rows,
    Int* j_cols,
    Int len_j_cols,
    F* res,
    Int res_size,
    F* mat_j,
    Int mat_j_nrow,
    Int mat_j_ncol
        , bool drop_first
    )
{
    #pragma omp parallel
    {
        std::vector<F> restemp(res_size, 0.0);
        #pragma omp for
        for (Py_ssize_t k_idx = 0; k_idx < len_rows; k_idx++) {
            Py_ssize_t k = rows[k_idx];
            // MAYBE TODO: explore whether the column restriction slows things down a
            // lot, particularly if not restricting the columns allows using SIMD
            // instructions
            // MAYBE TODO: explore whether swapping the loop order for F-ordered mat_j
            // is useful.
                Py_ssize_t i = indices[k] - drop_first;
                if (i >= 0) {
                for (Py_ssize_t j_idx = 0; j_idx < len_j_cols; j_idx++) {
                    Py_ssize_t j = j_cols[j_idx];
                        restemp[i * len_j_cols + j_idx] += d[k] * mat_j[k * mat_j_ncol + j];
                }
                }
        }
        for (Py_ssize_t i = 0; i < res_size; i++) {
            #pragma omp atomic
            res[i] += restemp[i];
        }
    }
}


template <typename Int, typename F>
void _sandwich_cat_denseF_complex(
    F* d,
    const Int* indices,
    Int* rows,
    Int len_rows,
    Int* j_cols,
    Int len_j_cols,
    F* res,
    Int res_size,
    F* mat_j,
    Int mat_j_nrow,
    Int mat_j_ncol
        , bool drop_first
    )
{
    #pragma omp parallel
    {
        std::vector<F> restemp(res_size, 0.0);
        #pragma omp for
        for (Py_ssize_t k_idx = 0; k_idx < len_rows; k_idx++) {
            Py_ssize_t k = rows[k_idx];
            // MAYBE TODO: explore whether the column restriction slows things down a
            // lot, particularly if not restricting the columns allows using SIMD
            // instructions
            // MAYBE TODO: explore whether swapping the loop order for F-ordered mat_j
            // is useful.
                Py_ssize_t i = indices[k] - drop_first;
                if (i >= 0) {
                for (Py_ssize_t j_idx = 0; j_idx < len_j_cols; j_idx++) {
                    Py_ssize_t j = j_cols[j_idx];
                        restemp[i * len_j_cols + j_idx] += d[k] * mat_j[j * mat_j_nrow + k];
                }
                }
        }
        for (Py_ssize_t i = 0; i < res_size; i++) {
            #pragma omp atomic
            res[i] += restemp[i];
        }
    }
}


template <typename Int, typename F>
void _sandwich_cat_cat_fast(
    F* d,
    const Int* i_indices,
    const Int* j_indices,
    Int* rows,
    Int len_rows,
    F* res,
    Int res_n_col,
    Int res_size
)
{
    #pragma omp parallel
    {
        std::vector<F> restemp(res_size, 0.0);
        # pragma omp for
        for (Py_ssize_t k_idx = 0; k_idx < len_rows; k_idx++) {
            Int k = rows[k_idx];

                Int i = i_indices[k];

                Int j = j_indices[k];

            restemp[(Py_ssize_t) i * res_n_col + j] += d[k];
        }
        for (Py_ssize_t i = 0; i < res_size; i++) {
            # pragma omp atomic
            res[i] += restemp[i];
        }
    }
}


template <typename Int, typename F>
void _sandwich_cat_cat_complex(
    F* d,
    const Int* i_indices,
    const Int* j_indices,
    Int* rows,
    Int len_rows,
    F* res,
    Int res_n_col,
    Int res_size
        , bool i_drop_first
        , bool j_drop_first
)
{
    #pragma omp parallel
    {
        std::vector<F> restemp(res_size, 0.0);
        # pragma omp for
        for (Py_ssize_t k_idx = 0; k_idx < len_rows; k_idx++) {
            Int k = rows[k_idx];

                Int i = i_indices[k] - i_drop_first;
                if (i < 0) {
                    continue;
                }

                Int j = j_indices[k] - j_drop_first;
                if (j < 0) {
                    continue;
                }

            restemp[(Py_ssize_t) i * res_n_col + j] += d[k];
        }
        for (Py_ssize_t i = 0; i < res_size; i++) {
            # pragma omp atomic
            res[i] += restemp[i];
        }
    }
}


template <typename Int, typename F>
void _transpose_matvec_all_rows_fast(
    Int n_rows,
    const Int* indices,
    F* other,
    F* res,
    Int res_size
) {
    int num_threads = omp_get_max_threads();
    std::vector<F> all_res(num_threads * res_size, 0.0);
    #pragma omp parallel shared(all_res)
    {
	int tid = omp_get_thread_num();
	F* res_slice = &all_res[tid * res_size];
	#pragma omp for
        for (Py_ssize_t i = 0; i < n_rows; i++) {
  	        res_slice[indices[i]] += other[i];
        }
	#pragma omp for
	for (Py_ssize_t i = 0; i < res_size; ++i) {
	    for (int tid = 0; tid < num_threads; ++tid) {
	        res[i] += all_res[tid * res_size + i];
	    }
	}
    }
}


template <typename Int, typename F>
void _transpose_matvec_all_rows_complex(
    Int n_rows,
    const Int* indices,
    F* other,
    F* res,
    Int res_size
        , bool drop_first
) {
    int num_threads = omp_get_max_threads();
    std::vector<F> all_res(num_threads * res_size, 0.0);
    #pragma omp parallel shared(all_res)
    {
	int tid = omp_get_thread_num();
	F* res_slice = &all_res[tid * res_size];
	#pragma omp for
        for (Py_ssize_t i = 0; i < n_rows; i++) {
                Py_ssize_t col_idx = indices[i] - drop_first;
                if (col_idx >= 0) {
                    res_slice[col_idx] += other[i];
                }
        }
	#pragma omp for
	for (Py_ssize_t i = 0; i < res_size; ++i) {
	    for (int tid = 0; tid < num_threads; ++tid) {
	        res[i] += all_res[tid * res_size + i];
	    }
	}
    }
}

