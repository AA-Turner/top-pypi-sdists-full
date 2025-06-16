#pragma once

#include <cmath>

#include "anyode/anyode_matrix.hpp"
#include "anyode/anyode_buffer.hpp"

#if ANYODE_NO_LAPACK == 1
#include "anyode/anyode_blasless.hpp"
#else
#include "anyode/anyode_blas_lapack.hpp"
#endif

namespace AnyODE {

    template<typename Real_t>
    struct DecompositionBase {
        virtual ~DecompositionBase() {};
        virtual int factorize() = 0;
        virtual int solve(const Real_t * const, Real_t * const) = 0;
    };

    template<typename Real_t = double>
    struct DenseLU : public DecompositionBase<Real_t> {
        // DenseLU_callbacks<Real_t> m_cbs;
        DenseMatrix<Real_t> * m_view;
        buffer_t<int> m_ipiv;

        DenseLU(DenseMatrix<Real_t> * view) :
            m_view(view),
            m_ipiv(buffer_factory<int>(view->m_nr))
        {}
        int factorize() override final {
            int info;
            constexpr getrf_callback<Real_t> getrf{};
            getrf(&(m_view->m_nr), &(m_view->m_nc), m_view->m_data, &(m_view->m_ld),
                          buffer_get_raw_ptr(m_ipiv), &info);
            return info;
        }
        int solve(const Real_t * const b, Real_t * const x) override final {
            char trans = 'N';
            int nrhs = 1;
            int info;
            std::copy(b, b + m_view->m_nr, x);
            constexpr getrs_callback<Real_t> getrs{};
            getrs(&trans, &(m_view->m_nr), &nrhs, m_view->m_data, &(m_view->m_ld),
                          buffer_get_raw_ptr(m_ipiv), x, &(m_view->m_nr), &info);
            return info;
        }
    };

    template<typename Real_t = double>
    struct DiagonalInv : public DecompositionBase<Real_t> {
        DiagonalMatrix<Real_t> * m_view;
        DiagonalInv(DiagonalMatrix<Real_t> * view) : m_view(view)
        {
        }
        int factorize() final {
            for (int i=0; i < m_view->m_nc; ++i)
                m_view->m_data[i] = 1/m_view->m_data[i];
            return 0;
        }
        int solve(const Real_t * const b, Real_t * const x) final {
            for (int i=0; i < m_view->m_nc; ++i)
                x[i] = m_view->m_data[i]*b[i];
            return 0;
        }
    };

}
