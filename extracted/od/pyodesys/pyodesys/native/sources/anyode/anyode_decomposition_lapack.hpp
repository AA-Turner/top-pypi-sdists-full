#pragma once
#include <anyode/anyode_util.hpp>
#include <anyode/anyode_decomposition.hpp>

BEGIN_NAMESPACE(AnyODE)
template<typename Real_t = double>
struct BandedLU : public DecompositionBase<Real_t> { // operates inplace
    BandedMatrix<Real_t> * m_view;
    buffer_t<int> m_ipiv;
    BandedLU(BandedMatrix<Real_t> * view) :
        m_view(view),
        m_ipiv(buffer_factory<int>(view->m_nr))
    {}
    int factorize() override final {
        int info;
        constexpr gbtrf_callback<Real_t> gbtrf{};
        gbtrf(&(m_view->m_nr), &(m_view->m_nc), &(m_view->m_kl), &(m_view->m_ku), m_view->m_data,
              &(m_view->m_ld), buffer_get_raw_ptr(m_ipiv), &info);
        return info;
    }
    int solve(const Real_t * const b, Real_t * const x) override final {
        char trans = 'N';
        int nrhs = 1;
        int info;
        std::copy(b, b + m_view->m_nr, x);
        constexpr gbtrs_callback<Real_t> gbtrs{};
        gbtrs(&trans, &(m_view->m_nr), &(m_view->m_kl), &(m_view->m_ku), &nrhs, m_view->m_data,
              &(m_view->m_ld), buffer_get_raw_ptr(m_ipiv), x, &(m_view->m_nr), &info);
        return info;
    }
};

template<typename Real_t = double>
struct SVD : public DecompositionBase<Real_t> {
    // SVD_callbacks<Real_t> m_cbs;
    DenseMatrix<Real_t> * m_view;
    buffer_t<Real_t> m_s;
    int m_ldu;
    buffer_t<Real_t> m_u;
    int m_ldvt;
    buffer_t<Real_t> m_vt;
    buffer_t<Real_t> m_work;
    int m_lwork = -1; // Query
    Real_t m_condition_number = -1;

    SVD(DenseMatrix<Real_t> * view) :
        m_view(view), m_s(buffer_factory<Real_t>(std::min(view->m_nr, view->m_nc))),
        m_ldu(view->m_nr), m_u(buffer_factory<Real_t>(m_ldu*(view->m_nr))),
        m_ldvt(view->m_nc), m_vt(buffer_factory<Real_t>(m_ldvt*(view->m_nc)))
    {
        int info;
        Real_t optim_work_size;
        char mode = 'A';
        constexpr gesvd_callback<Real_t> gesvd{};
        gesvd(&mode, &mode, &(m_view->m_nr), &(m_view->m_nc), m_view->m_data, &(m_view->m_ld),
              buffer_get_raw_ptr(m_s), buffer_get_raw_ptr(m_u), &m_ldu,
              buffer_get_raw_ptr(m_vt), &m_ldvt, &optim_work_size, &m_lwork, &info);
        m_lwork = static_cast<int>(optim_work_size);
        m_work = buffer_factory<Real_t>(m_lwork);
    }
    int factorize() override final {
        int info;
        char mode = 'A';
        constexpr gesvd_callback<Real_t> gesvd{};
        gesvd(&mode, &mode, &(m_view->m_nr), &(m_view->m_nc), m_view->m_data, &(m_view->m_ld),
              buffer_get_raw_ptr(m_s), buffer_get_raw_ptr(m_u), &m_ldu,
              buffer_get_raw_ptr(m_vt), &m_ldvt, buffer_get_raw_ptr(m_work), &m_lwork, &info);
        m_condition_number = std::fabs(m_s[0]/m_s[std::min(m_view->m_nr, m_view->m_nc) - 1]);
        return info;
    }
    int solve(const Real_t* const b, Real_t * const x) override final {
        Real_t alpha=1, beta=0;
        int incx=1, incy=1;
        char trans = 'T';
        auto y1 = buffer_factory<Real_t>(m_view->m_nr);
        constexpr gemv_callback<Real_t> gemv{};
        gemv(&trans, &(m_view->m_nr), &(m_view->m_nr), &alpha, buffer_get_raw_ptr(m_u), &(m_ldu),
             const_cast<Real_t*>(b), &incx, &beta, buffer_get_raw_ptr(y1), &incy);
        for (int i=0; i < m_view->m_nr; ++i)
            y1[i] /= m_s[i];
        gemv(&trans, &(m_view->m_nc), &(m_view->m_nc), &alpha, buffer_get_raw_ptr(m_vt), &m_ldvt,
             buffer_get_raw_ptr(y1), &incx, &beta, x, &incy);
        return 0;
    }

};
END_NAMESPACE(AnyODE)
