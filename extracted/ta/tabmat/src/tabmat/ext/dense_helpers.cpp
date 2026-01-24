// The dense_sandwich function below implement a BLIS/GotoBLAS-like sandwich
// product for computing A.T @ diag(d) @ A
// It works for both C-ordered and Fortran-ordered matrices.
// It is parallelized to be fast for both narrow and square matrices
//
// A good intro to thinking about matrix-multiply optimization is here:
// https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-172-performance-engineering-of-software-systems-fall-2018/lecture-slides/MIT6_172F18_lec1.pdf
//
// For more reading, it'd be good to dig into the GotoBLAS and BLIS implementation. 
// page 3 here has a good summary of the ordered of blocking/loops:
// http://www.cs.utexas.edu/users/flame/pubs/blis3_ipdps14.pdf
//
// The innermost simd loop is parallelized using xsimd and should
// use the largest vector instructions available on any given machine.
//
// There's a bit of added complexity here from the use of Mako templates.
// It looks scary, but it makes the loop unrolling and generalization across
// matrix orderings and parallelization schemes much simpler than it would be
// if implemented directly.

#include <xsimd/xsimd.hpp>
#include <iostream>
#include <omp.h>

#include "alloc.h"

#if XSIMD_VERSION_MAJOR >= 8
    #define XSIMD_BROADCAST broadcast
#else
    #define XSIMD_BROADCAST set_simd
#endif

#if XSIMD_VERSION_MAJOR >= 9
    #define XSIMD_REDUCE_ADD reduce_add
#else
    #define XSIMD_REDUCE_ADD hadd
#endif

namespace xs = xsimd;








template <typename Int, typename F>
void dense_baseTrue(F* R, F* L, F* d, F* out,
                Py_ssize_t out_m,
                Py_ssize_t imin2, Py_ssize_t imax2,
                Py_ssize_t jmin2, Py_ssize_t jmax2, 
                Py_ssize_t kmin, Py_ssize_t kmax, Int innerblock, Int kstep) 
{
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
    constexpr std::size_t simd_size = 1;
#else
    constexpr std::size_t simd_size = xsimd::simd_type<F>::size;
#endif
    for (Py_ssize_t imin = imin2; imin < imax2; imin+=innerblock) {
        Py_ssize_t imax = imin + innerblock; 
        if (imax > imax2) {
            imax = imax2; 
        }
        for (Py_ssize_t jmin = jmin2; jmin < jmax2; jmin+=innerblock) {
            Py_ssize_t jmax = jmin + innerblock; 
            if (jmax > jmax2) {
                jmax = jmax2; 
            }
            Py_ssize_t i = imin;
            {
                
    int imaxblock = imin + ((imax - imin) / 4) * 4;
    for (; i < imaxblock; i += 4) {
        int jmaxinner = jmax;
        if (jmaxinner > i + 4) {
            jmaxinner = i + 4;
        }
        int j = jmin;
        {
            
    int jmaxblock = jmin + ((jmaxinner - jmin) / 4) * 4;
    for (; j < jmaxblock; j += 4) {

        // setup simd accumulators
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_0 = (F)0.0;
#else
                auto accumsimd0_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_1 = (F)0.0;
#else
                auto accumsimd0_1 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_2 = (F)0.0;
#else
                auto accumsimd0_2 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_3 = (F)0.0;
#else
                auto accumsimd0_3 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd1_0 = (F)0.0;
#else
                auto accumsimd1_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd1_1 = (F)0.0;
#else
                auto accumsimd1_1 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd1_2 = (F)0.0;
#else
                auto accumsimd1_2 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd1_3 = (F)0.0;
#else
                auto accumsimd1_3 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd2_0 = (F)0.0;
#else
                auto accumsimd2_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd2_1 = (F)0.0;
#else
                auto accumsimd2_1 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd2_2 = (F)0.0;
#else
                auto accumsimd2_2 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd2_3 = (F)0.0;
#else
                auto accumsimd2_3 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd3_0 = (F)0.0;
#else
                auto accumsimd3_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd3_1 = (F)0.0;
#else
                auto accumsimd3_1 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd3_2 = (F)0.0;
#else
                auto accumsimd3_2 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd3_3 = (F)0.0;
#else
                auto accumsimd3_3 = xs::XSIMD_BROADCAST(((F)0.0));
#endif

            int basei0 = (i - imin2 + 0) * kstep;
            int basei1 = (i - imin2 + 1) * kstep;
            int basei2 = (i - imin2 + 2) * kstep;
            int basei3 = (i - imin2 + 3) * kstep;
            int basej0 = (j - jmin2 + 0) * kstep;
            int basej1 = (j - jmin2 + 1) * kstep;
            int basej2 = (j - jmin2 + 2) * kstep;
            int basej3 = (j - jmin2 + 3) * kstep;

        // main simd inner loop
            F* Lptr0 = &L[basei0];
            F* Lptr1 = &L[basei1];
            F* Lptr2 = &L[basei2];
            F* Lptr3 = &L[basei3];
            F* Rptr0 = &R[basej0];
            F* Rptr1 = &R[basej1];
            F* Rptr2 = &R[basej2];
            F* Rptr3 = &R[basej3];
        int kblocksize = ((kmax - kmin) / simd_size) * simd_size;
        F* Rptr0end = Rptr0 + kblocksize;
        for(; Rptr0 < Rptr0end; 
                Rptr0+=simd_size,
                Rptr1+=simd_size,
                Rptr2+=simd_size,
                Rptr3+=simd_size,
                    Lptr0 += simd_size,
                    Lptr1 += simd_size,
                    Lptr2 += simd_size,
                    Lptr3 += simd_size
            ) {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd0 = *Lptr0;
#else
                auto Xtd0 = xs::load_aligned(Lptr0);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd0_0 = xs::fma(Xtd0, Xsimd, accumsimd0_0);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr1;
#else
                    auto Xsimd = xs::load_aligned(Rptr1);
#endif
                    accumsimd0_1 = xs::fma(Xtd0, Xsimd, accumsimd0_1);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr2;
#else
                    auto Xsimd = xs::load_aligned(Rptr2);
#endif
                    accumsimd0_2 = xs::fma(Xtd0, Xsimd, accumsimd0_2);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr3;
#else
                    auto Xsimd = xs::load_aligned(Rptr3);
#endif
                    accumsimd0_3 = xs::fma(Xtd0, Xsimd, accumsimd0_3);
                }
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd1 = *Lptr1;
#else
                auto Xtd1 = xs::load_aligned(Lptr1);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd1_0 = xs::fma(Xtd1, Xsimd, accumsimd1_0);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr1;
#else
                    auto Xsimd = xs::load_aligned(Rptr1);
#endif
                    accumsimd1_1 = xs::fma(Xtd1, Xsimd, accumsimd1_1);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr2;
#else
                    auto Xsimd = xs::load_aligned(Rptr2);
#endif
                    accumsimd1_2 = xs::fma(Xtd1, Xsimd, accumsimd1_2);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr3;
#else
                    auto Xsimd = xs::load_aligned(Rptr3);
#endif
                    accumsimd1_3 = xs::fma(Xtd1, Xsimd, accumsimd1_3);
                }
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd2 = *Lptr2;
#else
                auto Xtd2 = xs::load_aligned(Lptr2);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd2_0 = xs::fma(Xtd2, Xsimd, accumsimd2_0);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr1;
#else
                    auto Xsimd = xs::load_aligned(Rptr1);
#endif
                    accumsimd2_1 = xs::fma(Xtd2, Xsimd, accumsimd2_1);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr2;
#else
                    auto Xsimd = xs::load_aligned(Rptr2);
#endif
                    accumsimd2_2 = xs::fma(Xtd2, Xsimd, accumsimd2_2);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr3;
#else
                    auto Xsimd = xs::load_aligned(Rptr3);
#endif
                    accumsimd2_3 = xs::fma(Xtd2, Xsimd, accumsimd2_3);
                }
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd3 = *Lptr3;
#else
                auto Xtd3 = xs::load_aligned(Lptr3);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd3_0 = xs::fma(Xtd3, Xsimd, accumsimd3_0);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr1;
#else
                    auto Xsimd = xs::load_aligned(Rptr1);
#endif
                    accumsimd3_1 = xs::fma(Xtd3, Xsimd, accumsimd3_1);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr2;
#else
                    auto Xsimd = xs::load_aligned(Rptr2);
#endif
                    accumsimd3_2 = xs::fma(Xtd3, Xsimd, accumsimd3_2);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr3;
#else
                    auto Xsimd = xs::load_aligned(Rptr3);
#endif
                    accumsimd3_3 = xs::fma(Xtd3, Xsimd, accumsimd3_3);
                }
        }

        // horizontal sum of the simd blocks
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_0 = accumsimd0_0;
#else
                F accum0_0 = xs::XSIMD_REDUCE_ADD(accumsimd0_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_1 = accumsimd0_1;
#else
                F accum0_1 = xs::XSIMD_REDUCE_ADD(accumsimd0_1);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_2 = accumsimd0_2;
#else
                F accum0_2 = xs::XSIMD_REDUCE_ADD(accumsimd0_2);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_3 = accumsimd0_3;
#else
                F accum0_3 = xs::XSIMD_REDUCE_ADD(accumsimd0_3);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum1_0 = accumsimd1_0;
#else
                F accum1_0 = xs::XSIMD_REDUCE_ADD(accumsimd1_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum1_1 = accumsimd1_1;
#else
                F accum1_1 = xs::XSIMD_REDUCE_ADD(accumsimd1_1);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum1_2 = accumsimd1_2;
#else
                F accum1_2 = xs::XSIMD_REDUCE_ADD(accumsimd1_2);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum1_3 = accumsimd1_3;
#else
                F accum1_3 = xs::XSIMD_REDUCE_ADD(accumsimd1_3);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum2_0 = accumsimd2_0;
#else
                F accum2_0 = xs::XSIMD_REDUCE_ADD(accumsimd2_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum2_1 = accumsimd2_1;
#else
                F accum2_1 = xs::XSIMD_REDUCE_ADD(accumsimd2_1);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum2_2 = accumsimd2_2;
#else
                F accum2_2 = xs::XSIMD_REDUCE_ADD(accumsimd2_2);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum2_3 = accumsimd2_3;
#else
                F accum2_3 = xs::XSIMD_REDUCE_ADD(accumsimd2_3);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum3_0 = accumsimd3_0;
#else
                F accum3_0 = xs::XSIMD_REDUCE_ADD(accumsimd3_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum3_1 = accumsimd3_1;
#else
                F accum3_1 = xs::XSIMD_REDUCE_ADD(accumsimd3_1);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum3_2 = accumsimd3_2;
#else
                F accum3_2 = xs::XSIMD_REDUCE_ADD(accumsimd3_2);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum3_3 = accumsimd3_3;
#else
                F accum3_3 = xs::XSIMD_REDUCE_ADD(accumsimd3_3);
#endif

        // remainder loop handling the entries that can't be handled in a
        // simd_size stride
        for (int k = kblocksize; k < kmax - kmin; k++) {
                F Xtd0 = L[basei0 + k];
                F Xtd1 = L[basei1 + k];
                F Xtd2 = L[basei2 + k];
                F Xtd3 = L[basei3 + k];
                F Xv0 = R[basej0 + k];
                F Xv1 = R[basej1 + k];
                F Xv2 = R[basej2 + k];
                F Xv3 = R[basej3 + k];
                    accum0_0 += Xtd0 * Xv0;
                    accum0_1 += Xtd0 * Xv1;
                    accum0_2 += Xtd0 * Xv2;
                    accum0_3 += Xtd0 * Xv3;
                    accum1_0 += Xtd1 * Xv0;
                    accum1_1 += Xtd1 * Xv1;
                    accum1_2 += Xtd1 * Xv2;
                    accum1_3 += Xtd1 * Xv3;
                    accum2_0 += Xtd2 * Xv0;
                    accum2_1 += Xtd2 * Xv1;
                    accum2_2 += Xtd2 * Xv2;
                    accum2_3 += Xtd2 * Xv3;
                    accum3_0 += Xtd3 * Xv0;
                    accum3_1 += Xtd3 * Xv1;
                    accum3_2 += Xtd3 * Xv2;
                    accum3_3 += Xtd3 * Xv3;
        }

        // add to the output array
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 0) * out_m + (j + 0)] += accum0_0;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 0) * out_m + (j + 1)] += accum0_1;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 0) * out_m + (j + 2)] += accum0_2;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 0) * out_m + (j + 3)] += accum0_3;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 1) * out_m + (j + 0)] += accum1_0;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 1) * out_m + (j + 1)] += accum1_1;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 1) * out_m + (j + 2)] += accum1_2;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 1) * out_m + (j + 3)] += accum1_3;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 2) * out_m + (j + 0)] += accum2_0;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 2) * out_m + (j + 1)] += accum2_1;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 2) * out_m + (j + 2)] += accum2_2;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 2) * out_m + (j + 3)] += accum2_3;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 3) * out_m + (j + 0)] += accum3_0;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 3) * out_m + (j + 1)] += accum3_1;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 3) * out_m + (j + 2)] += accum3_2;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 3) * out_m + (j + 3)] += accum3_3;
    }

        }
        {
            
    int jmaxblock = jmin + ((jmaxinner - jmin) / 2) * 2;
    for (; j < jmaxblock; j += 2) {

        // setup simd accumulators
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_0 = (F)0.0;
#else
                auto accumsimd0_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_1 = (F)0.0;
#else
                auto accumsimd0_1 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd1_0 = (F)0.0;
#else
                auto accumsimd1_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd1_1 = (F)0.0;
#else
                auto accumsimd1_1 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd2_0 = (F)0.0;
#else
                auto accumsimd2_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd2_1 = (F)0.0;
#else
                auto accumsimd2_1 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd3_0 = (F)0.0;
#else
                auto accumsimd3_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd3_1 = (F)0.0;
#else
                auto accumsimd3_1 = xs::XSIMD_BROADCAST(((F)0.0));
#endif

            int basei0 = (i - imin2 + 0) * kstep;
            int basei1 = (i - imin2 + 1) * kstep;
            int basei2 = (i - imin2 + 2) * kstep;
            int basei3 = (i - imin2 + 3) * kstep;
            int basej0 = (j - jmin2 + 0) * kstep;
            int basej1 = (j - jmin2 + 1) * kstep;

        // main simd inner loop
            F* Lptr0 = &L[basei0];
            F* Lptr1 = &L[basei1];
            F* Lptr2 = &L[basei2];
            F* Lptr3 = &L[basei3];
            F* Rptr0 = &R[basej0];
            F* Rptr1 = &R[basej1];
        int kblocksize = ((kmax - kmin) / simd_size) * simd_size;
        F* Rptr0end = Rptr0 + kblocksize;
        for(; Rptr0 < Rptr0end; 
                Rptr0+=simd_size,
                Rptr1+=simd_size,
                    Lptr0 += simd_size,
                    Lptr1 += simd_size,
                    Lptr2 += simd_size,
                    Lptr3 += simd_size
            ) {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd0 = *Lptr0;
#else
                auto Xtd0 = xs::load_aligned(Lptr0);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd0_0 = xs::fma(Xtd0, Xsimd, accumsimd0_0);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr1;
#else
                    auto Xsimd = xs::load_aligned(Rptr1);
#endif
                    accumsimd0_1 = xs::fma(Xtd0, Xsimd, accumsimd0_1);
                }
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd1 = *Lptr1;
#else
                auto Xtd1 = xs::load_aligned(Lptr1);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd1_0 = xs::fma(Xtd1, Xsimd, accumsimd1_0);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr1;
#else
                    auto Xsimd = xs::load_aligned(Rptr1);
#endif
                    accumsimd1_1 = xs::fma(Xtd1, Xsimd, accumsimd1_1);
                }
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd2 = *Lptr2;
#else
                auto Xtd2 = xs::load_aligned(Lptr2);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd2_0 = xs::fma(Xtd2, Xsimd, accumsimd2_0);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr1;
#else
                    auto Xsimd = xs::load_aligned(Rptr1);
#endif
                    accumsimd2_1 = xs::fma(Xtd2, Xsimd, accumsimd2_1);
                }
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd3 = *Lptr3;
#else
                auto Xtd3 = xs::load_aligned(Lptr3);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd3_0 = xs::fma(Xtd3, Xsimd, accumsimd3_0);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr1;
#else
                    auto Xsimd = xs::load_aligned(Rptr1);
#endif
                    accumsimd3_1 = xs::fma(Xtd3, Xsimd, accumsimd3_1);
                }
        }

        // horizontal sum of the simd blocks
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_0 = accumsimd0_0;
#else
                F accum0_0 = xs::XSIMD_REDUCE_ADD(accumsimd0_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_1 = accumsimd0_1;
#else
                F accum0_1 = xs::XSIMD_REDUCE_ADD(accumsimd0_1);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum1_0 = accumsimd1_0;
#else
                F accum1_0 = xs::XSIMD_REDUCE_ADD(accumsimd1_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum1_1 = accumsimd1_1;
#else
                F accum1_1 = xs::XSIMD_REDUCE_ADD(accumsimd1_1);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum2_0 = accumsimd2_0;
#else
                F accum2_0 = xs::XSIMD_REDUCE_ADD(accumsimd2_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum2_1 = accumsimd2_1;
#else
                F accum2_1 = xs::XSIMD_REDUCE_ADD(accumsimd2_1);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum3_0 = accumsimd3_0;
#else
                F accum3_0 = xs::XSIMD_REDUCE_ADD(accumsimd3_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum3_1 = accumsimd3_1;
#else
                F accum3_1 = xs::XSIMD_REDUCE_ADD(accumsimd3_1);
#endif

        // remainder loop handling the entries that can't be handled in a
        // simd_size stride
        for (int k = kblocksize; k < kmax - kmin; k++) {
                F Xtd0 = L[basei0 + k];
                F Xtd1 = L[basei1 + k];
                F Xtd2 = L[basei2 + k];
                F Xtd3 = L[basei3 + k];
                F Xv0 = R[basej0 + k];
                F Xv1 = R[basej1 + k];
                    accum0_0 += Xtd0 * Xv0;
                    accum0_1 += Xtd0 * Xv1;
                    accum1_0 += Xtd1 * Xv0;
                    accum1_1 += Xtd1 * Xv1;
                    accum2_0 += Xtd2 * Xv0;
                    accum2_1 += Xtd2 * Xv1;
                    accum3_0 += Xtd3 * Xv0;
                    accum3_1 += Xtd3 * Xv1;
        }

        // add to the output array
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 0) * out_m + (j + 0)] += accum0_0;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 0) * out_m + (j + 1)] += accum0_1;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 1) * out_m + (j + 0)] += accum1_0;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 1) * out_m + (j + 1)] += accum1_1;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 2) * out_m + (j + 0)] += accum2_0;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 2) * out_m + (j + 1)] += accum2_1;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 3) * out_m + (j + 0)] += accum3_0;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 3) * out_m + (j + 1)] += accum3_1;
    }

        }
        {
            
    int jmaxblock = jmin + ((jmaxinner - jmin) / 1) * 1;
    for (; j < jmaxblock; j += 1) {

        // setup simd accumulators
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_0 = (F)0.0;
#else
                auto accumsimd0_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd1_0 = (F)0.0;
#else
                auto accumsimd1_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd2_0 = (F)0.0;
#else
                auto accumsimd2_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd3_0 = (F)0.0;
#else
                auto accumsimd3_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif

            int basei0 = (i - imin2 + 0) * kstep;
            int basei1 = (i - imin2 + 1) * kstep;
            int basei2 = (i - imin2 + 2) * kstep;
            int basei3 = (i - imin2 + 3) * kstep;
            int basej0 = (j - jmin2 + 0) * kstep;

        // main simd inner loop
            F* Lptr0 = &L[basei0];
            F* Lptr1 = &L[basei1];
            F* Lptr2 = &L[basei2];
            F* Lptr3 = &L[basei3];
            F* Rptr0 = &R[basej0];
        int kblocksize = ((kmax - kmin) / simd_size) * simd_size;
        F* Rptr0end = Rptr0 + kblocksize;
        for(; Rptr0 < Rptr0end; 
                Rptr0+=simd_size,
                    Lptr0 += simd_size,
                    Lptr1 += simd_size,
                    Lptr2 += simd_size,
                    Lptr3 += simd_size
            ) {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd0 = *Lptr0;
#else
                auto Xtd0 = xs::load_aligned(Lptr0);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd0_0 = xs::fma(Xtd0, Xsimd, accumsimd0_0);
                }
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd1 = *Lptr1;
#else
                auto Xtd1 = xs::load_aligned(Lptr1);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd1_0 = xs::fma(Xtd1, Xsimd, accumsimd1_0);
                }
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd2 = *Lptr2;
#else
                auto Xtd2 = xs::load_aligned(Lptr2);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd2_0 = xs::fma(Xtd2, Xsimd, accumsimd2_0);
                }
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd3 = *Lptr3;
#else
                auto Xtd3 = xs::load_aligned(Lptr3);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd3_0 = xs::fma(Xtd3, Xsimd, accumsimd3_0);
                }
        }

        // horizontal sum of the simd blocks
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_0 = accumsimd0_0;
#else
                F accum0_0 = xs::XSIMD_REDUCE_ADD(accumsimd0_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum1_0 = accumsimd1_0;
#else
                F accum1_0 = xs::XSIMD_REDUCE_ADD(accumsimd1_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum2_0 = accumsimd2_0;
#else
                F accum2_0 = xs::XSIMD_REDUCE_ADD(accumsimd2_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum3_0 = accumsimd3_0;
#else
                F accum3_0 = xs::XSIMD_REDUCE_ADD(accumsimd3_0);
#endif

        // remainder loop handling the entries that can't be handled in a
        // simd_size stride
        for (int k = kblocksize; k < kmax - kmin; k++) {
                F Xtd0 = L[basei0 + k];
                F Xtd1 = L[basei1 + k];
                F Xtd2 = L[basei2 + k];
                F Xtd3 = L[basei3 + k];
                F Xv0 = R[basej0 + k];
                    accum0_0 += Xtd0 * Xv0;
                    accum1_0 += Xtd1 * Xv0;
                    accum2_0 += Xtd2 * Xv0;
                    accum3_0 += Xtd3 * Xv0;
        }

        // add to the output array
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 0) * out_m + (j + 0)] += accum0_0;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 1) * out_m + (j + 0)] += accum1_0;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 2) * out_m + (j + 0)] += accum2_0;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 3) * out_m + (j + 0)] += accum3_0;
    }

        }
    }

            }
            {
                
    int imaxblock = imin + ((imax - imin) / 2) * 2;
    for (; i < imaxblock; i += 2) {
        int jmaxinner = jmax;
        if (jmaxinner > i + 2) {
            jmaxinner = i + 2;
        }
        int j = jmin;
        {
            
    int jmaxblock = jmin + ((jmaxinner - jmin) / 4) * 4;
    for (; j < jmaxblock; j += 4) {

        // setup simd accumulators
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_0 = (F)0.0;
#else
                auto accumsimd0_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_1 = (F)0.0;
#else
                auto accumsimd0_1 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_2 = (F)0.0;
#else
                auto accumsimd0_2 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_3 = (F)0.0;
#else
                auto accumsimd0_3 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd1_0 = (F)0.0;
#else
                auto accumsimd1_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd1_1 = (F)0.0;
#else
                auto accumsimd1_1 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd1_2 = (F)0.0;
#else
                auto accumsimd1_2 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd1_3 = (F)0.0;
#else
                auto accumsimd1_3 = xs::XSIMD_BROADCAST(((F)0.0));
#endif

            int basei0 = (i - imin2 + 0) * kstep;
            int basei1 = (i - imin2 + 1) * kstep;
            int basej0 = (j - jmin2 + 0) * kstep;
            int basej1 = (j - jmin2 + 1) * kstep;
            int basej2 = (j - jmin2 + 2) * kstep;
            int basej3 = (j - jmin2 + 3) * kstep;

        // main simd inner loop
            F* Lptr0 = &L[basei0];
            F* Lptr1 = &L[basei1];
            F* Rptr0 = &R[basej0];
            F* Rptr1 = &R[basej1];
            F* Rptr2 = &R[basej2];
            F* Rptr3 = &R[basej3];
        int kblocksize = ((kmax - kmin) / simd_size) * simd_size;
        F* Rptr0end = Rptr0 + kblocksize;
        for(; Rptr0 < Rptr0end; 
                Rptr0+=simd_size,
                Rptr1+=simd_size,
                Rptr2+=simd_size,
                Rptr3+=simd_size,
                    Lptr0 += simd_size,
                    Lptr1 += simd_size
            ) {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd0 = *Lptr0;
#else
                auto Xtd0 = xs::load_aligned(Lptr0);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd0_0 = xs::fma(Xtd0, Xsimd, accumsimd0_0);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr1;
#else
                    auto Xsimd = xs::load_aligned(Rptr1);
#endif
                    accumsimd0_1 = xs::fma(Xtd0, Xsimd, accumsimd0_1);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr2;
#else
                    auto Xsimd = xs::load_aligned(Rptr2);
#endif
                    accumsimd0_2 = xs::fma(Xtd0, Xsimd, accumsimd0_2);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr3;
#else
                    auto Xsimd = xs::load_aligned(Rptr3);
#endif
                    accumsimd0_3 = xs::fma(Xtd0, Xsimd, accumsimd0_3);
                }
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd1 = *Lptr1;
#else
                auto Xtd1 = xs::load_aligned(Lptr1);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd1_0 = xs::fma(Xtd1, Xsimd, accumsimd1_0);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr1;
#else
                    auto Xsimd = xs::load_aligned(Rptr1);
#endif
                    accumsimd1_1 = xs::fma(Xtd1, Xsimd, accumsimd1_1);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr2;
#else
                    auto Xsimd = xs::load_aligned(Rptr2);
#endif
                    accumsimd1_2 = xs::fma(Xtd1, Xsimd, accumsimd1_2);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr3;
#else
                    auto Xsimd = xs::load_aligned(Rptr3);
#endif
                    accumsimd1_3 = xs::fma(Xtd1, Xsimd, accumsimd1_3);
                }
        }

        // horizontal sum of the simd blocks
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_0 = accumsimd0_0;
#else
                F accum0_0 = xs::XSIMD_REDUCE_ADD(accumsimd0_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_1 = accumsimd0_1;
#else
                F accum0_1 = xs::XSIMD_REDUCE_ADD(accumsimd0_1);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_2 = accumsimd0_2;
#else
                F accum0_2 = xs::XSIMD_REDUCE_ADD(accumsimd0_2);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_3 = accumsimd0_3;
#else
                F accum0_3 = xs::XSIMD_REDUCE_ADD(accumsimd0_3);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum1_0 = accumsimd1_0;
#else
                F accum1_0 = xs::XSIMD_REDUCE_ADD(accumsimd1_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum1_1 = accumsimd1_1;
#else
                F accum1_1 = xs::XSIMD_REDUCE_ADD(accumsimd1_1);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum1_2 = accumsimd1_2;
#else
                F accum1_2 = xs::XSIMD_REDUCE_ADD(accumsimd1_2);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum1_3 = accumsimd1_3;
#else
                F accum1_3 = xs::XSIMD_REDUCE_ADD(accumsimd1_3);
#endif

        // remainder loop handling the entries that can't be handled in a
        // simd_size stride
        for (int k = kblocksize; k < kmax - kmin; k++) {
                F Xtd0 = L[basei0 + k];
                F Xtd1 = L[basei1 + k];
                F Xv0 = R[basej0 + k];
                F Xv1 = R[basej1 + k];
                F Xv2 = R[basej2 + k];
                F Xv3 = R[basej3 + k];
                    accum0_0 += Xtd0 * Xv0;
                    accum0_1 += Xtd0 * Xv1;
                    accum0_2 += Xtd0 * Xv2;
                    accum0_3 += Xtd0 * Xv3;
                    accum1_0 += Xtd1 * Xv0;
                    accum1_1 += Xtd1 * Xv1;
                    accum1_2 += Xtd1 * Xv2;
                    accum1_3 += Xtd1 * Xv3;
        }

        // add to the output array
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 0) * out_m + (j + 0)] += accum0_0;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 0) * out_m + (j + 1)] += accum0_1;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 0) * out_m + (j + 2)] += accum0_2;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 0) * out_m + (j + 3)] += accum0_3;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 1) * out_m + (j + 0)] += accum1_0;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 1) * out_m + (j + 1)] += accum1_1;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 1) * out_m + (j + 2)] += accum1_2;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 1) * out_m + (j + 3)] += accum1_3;
    }

        }
        {
            
    int jmaxblock = jmin + ((jmaxinner - jmin) / 2) * 2;
    for (; j < jmaxblock; j += 2) {

        // setup simd accumulators
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_0 = (F)0.0;
#else
                auto accumsimd0_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_1 = (F)0.0;
#else
                auto accumsimd0_1 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd1_0 = (F)0.0;
#else
                auto accumsimd1_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd1_1 = (F)0.0;
#else
                auto accumsimd1_1 = xs::XSIMD_BROADCAST(((F)0.0));
#endif

            int basei0 = (i - imin2 + 0) * kstep;
            int basei1 = (i - imin2 + 1) * kstep;
            int basej0 = (j - jmin2 + 0) * kstep;
            int basej1 = (j - jmin2 + 1) * kstep;

        // main simd inner loop
            F* Lptr0 = &L[basei0];
            F* Lptr1 = &L[basei1];
            F* Rptr0 = &R[basej0];
            F* Rptr1 = &R[basej1];
        int kblocksize = ((kmax - kmin) / simd_size) * simd_size;
        F* Rptr0end = Rptr0 + kblocksize;
        for(; Rptr0 < Rptr0end; 
                Rptr0+=simd_size,
                Rptr1+=simd_size,
                    Lptr0 += simd_size,
                    Lptr1 += simd_size
            ) {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd0 = *Lptr0;
#else
                auto Xtd0 = xs::load_aligned(Lptr0);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd0_0 = xs::fma(Xtd0, Xsimd, accumsimd0_0);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr1;
#else
                    auto Xsimd = xs::load_aligned(Rptr1);
#endif
                    accumsimd0_1 = xs::fma(Xtd0, Xsimd, accumsimd0_1);
                }
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd1 = *Lptr1;
#else
                auto Xtd1 = xs::load_aligned(Lptr1);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd1_0 = xs::fma(Xtd1, Xsimd, accumsimd1_0);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr1;
#else
                    auto Xsimd = xs::load_aligned(Rptr1);
#endif
                    accumsimd1_1 = xs::fma(Xtd1, Xsimd, accumsimd1_1);
                }
        }

        // horizontal sum of the simd blocks
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_0 = accumsimd0_0;
#else
                F accum0_0 = xs::XSIMD_REDUCE_ADD(accumsimd0_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_1 = accumsimd0_1;
#else
                F accum0_1 = xs::XSIMD_REDUCE_ADD(accumsimd0_1);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum1_0 = accumsimd1_0;
#else
                F accum1_0 = xs::XSIMD_REDUCE_ADD(accumsimd1_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum1_1 = accumsimd1_1;
#else
                F accum1_1 = xs::XSIMD_REDUCE_ADD(accumsimd1_1);
#endif

        // remainder loop handling the entries that can't be handled in a
        // simd_size stride
        for (int k = kblocksize; k < kmax - kmin; k++) {
                F Xtd0 = L[basei0 + k];
                F Xtd1 = L[basei1 + k];
                F Xv0 = R[basej0 + k];
                F Xv1 = R[basej1 + k];
                    accum0_0 += Xtd0 * Xv0;
                    accum0_1 += Xtd0 * Xv1;
                    accum1_0 += Xtd1 * Xv0;
                    accum1_1 += Xtd1 * Xv1;
        }

        // add to the output array
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 0) * out_m + (j + 0)] += accum0_0;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 0) * out_m + (j + 1)] += accum0_1;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 1) * out_m + (j + 0)] += accum1_0;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 1) * out_m + (j + 1)] += accum1_1;
    }

        }
        {
            
    int jmaxblock = jmin + ((jmaxinner - jmin) / 1) * 1;
    for (; j < jmaxblock; j += 1) {

        // setup simd accumulators
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_0 = (F)0.0;
#else
                auto accumsimd0_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd1_0 = (F)0.0;
#else
                auto accumsimd1_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif

            int basei0 = (i - imin2 + 0) * kstep;
            int basei1 = (i - imin2 + 1) * kstep;
            int basej0 = (j - jmin2 + 0) * kstep;

        // main simd inner loop
            F* Lptr0 = &L[basei0];
            F* Lptr1 = &L[basei1];
            F* Rptr0 = &R[basej0];
        int kblocksize = ((kmax - kmin) / simd_size) * simd_size;
        F* Rptr0end = Rptr0 + kblocksize;
        for(; Rptr0 < Rptr0end; 
                Rptr0+=simd_size,
                    Lptr0 += simd_size,
                    Lptr1 += simd_size
            ) {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd0 = *Lptr0;
#else
                auto Xtd0 = xs::load_aligned(Lptr0);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd0_0 = xs::fma(Xtd0, Xsimd, accumsimd0_0);
                }
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd1 = *Lptr1;
#else
                auto Xtd1 = xs::load_aligned(Lptr1);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd1_0 = xs::fma(Xtd1, Xsimd, accumsimd1_0);
                }
        }

        // horizontal sum of the simd blocks
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_0 = accumsimd0_0;
#else
                F accum0_0 = xs::XSIMD_REDUCE_ADD(accumsimd0_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum1_0 = accumsimd1_0;
#else
                F accum1_0 = xs::XSIMD_REDUCE_ADD(accumsimd1_0);
#endif

        // remainder loop handling the entries that can't be handled in a
        // simd_size stride
        for (int k = kblocksize; k < kmax - kmin; k++) {
                F Xtd0 = L[basei0 + k];
                F Xtd1 = L[basei1 + k];
                F Xv0 = R[basej0 + k];
                    accum0_0 += Xtd0 * Xv0;
                    accum1_0 += Xtd1 * Xv0;
        }

        // add to the output array
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 0) * out_m + (j + 0)] += accum0_0;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 1) * out_m + (j + 0)] += accum1_0;
    }

        }
    }

            }
            {
                
    int imaxblock = imin + ((imax - imin) / 1) * 1;
    for (; i < imaxblock; i += 1) {
        int jmaxinner = jmax;
        if (jmaxinner > i + 1) {
            jmaxinner = i + 1;
        }
        int j = jmin;
        {
            
    int jmaxblock = jmin + ((jmaxinner - jmin) / 4) * 4;
    for (; j < jmaxblock; j += 4) {

        // setup simd accumulators
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_0 = (F)0.0;
#else
                auto accumsimd0_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_1 = (F)0.0;
#else
                auto accumsimd0_1 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_2 = (F)0.0;
#else
                auto accumsimd0_2 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_3 = (F)0.0;
#else
                auto accumsimd0_3 = xs::XSIMD_BROADCAST(((F)0.0));
#endif

            int basei0 = (i - imin2 + 0) * kstep;
            int basej0 = (j - jmin2 + 0) * kstep;
            int basej1 = (j - jmin2 + 1) * kstep;
            int basej2 = (j - jmin2 + 2) * kstep;
            int basej3 = (j - jmin2 + 3) * kstep;

        // main simd inner loop
            F* Lptr0 = &L[basei0];
            F* Rptr0 = &R[basej0];
            F* Rptr1 = &R[basej1];
            F* Rptr2 = &R[basej2];
            F* Rptr3 = &R[basej3];
        int kblocksize = ((kmax - kmin) / simd_size) * simd_size;
        F* Rptr0end = Rptr0 + kblocksize;
        for(; Rptr0 < Rptr0end; 
                Rptr0+=simd_size,
                Rptr1+=simd_size,
                Rptr2+=simd_size,
                Rptr3+=simd_size,
                    Lptr0 += simd_size
            ) {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd0 = *Lptr0;
#else
                auto Xtd0 = xs::load_aligned(Lptr0);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd0_0 = xs::fma(Xtd0, Xsimd, accumsimd0_0);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr1;
#else
                    auto Xsimd = xs::load_aligned(Rptr1);
#endif
                    accumsimd0_1 = xs::fma(Xtd0, Xsimd, accumsimd0_1);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr2;
#else
                    auto Xsimd = xs::load_aligned(Rptr2);
#endif
                    accumsimd0_2 = xs::fma(Xtd0, Xsimd, accumsimd0_2);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr3;
#else
                    auto Xsimd = xs::load_aligned(Rptr3);
#endif
                    accumsimd0_3 = xs::fma(Xtd0, Xsimd, accumsimd0_3);
                }
        }

        // horizontal sum of the simd blocks
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_0 = accumsimd0_0;
#else
                F accum0_0 = xs::XSIMD_REDUCE_ADD(accumsimd0_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_1 = accumsimd0_1;
#else
                F accum0_1 = xs::XSIMD_REDUCE_ADD(accumsimd0_1);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_2 = accumsimd0_2;
#else
                F accum0_2 = xs::XSIMD_REDUCE_ADD(accumsimd0_2);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_3 = accumsimd0_3;
#else
                F accum0_3 = xs::XSIMD_REDUCE_ADD(accumsimd0_3);
#endif

        // remainder loop handling the entries that can't be handled in a
        // simd_size stride
        for (int k = kblocksize; k < kmax - kmin; k++) {
                F Xtd0 = L[basei0 + k];
                F Xv0 = R[basej0 + k];
                F Xv1 = R[basej1 + k];
                F Xv2 = R[basej2 + k];
                F Xv3 = R[basej3 + k];
                    accum0_0 += Xtd0 * Xv0;
                    accum0_1 += Xtd0 * Xv1;
                    accum0_2 += Xtd0 * Xv2;
                    accum0_3 += Xtd0 * Xv3;
        }

        // add to the output array
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 0) * out_m + (j + 0)] += accum0_0;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 0) * out_m + (j + 1)] += accum0_1;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 0) * out_m + (j + 2)] += accum0_2;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 0) * out_m + (j + 3)] += accum0_3;
    }

        }
        {
            
    int jmaxblock = jmin + ((jmaxinner - jmin) / 2) * 2;
    for (; j < jmaxblock; j += 2) {

        // setup simd accumulators
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_0 = (F)0.0;
#else
                auto accumsimd0_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_1 = (F)0.0;
#else
                auto accumsimd0_1 = xs::XSIMD_BROADCAST(((F)0.0));
#endif

            int basei0 = (i - imin2 + 0) * kstep;
            int basej0 = (j - jmin2 + 0) * kstep;
            int basej1 = (j - jmin2 + 1) * kstep;

        // main simd inner loop
            F* Lptr0 = &L[basei0];
            F* Rptr0 = &R[basej0];
            F* Rptr1 = &R[basej1];
        int kblocksize = ((kmax - kmin) / simd_size) * simd_size;
        F* Rptr0end = Rptr0 + kblocksize;
        for(; Rptr0 < Rptr0end; 
                Rptr0+=simd_size,
                Rptr1+=simd_size,
                    Lptr0 += simd_size
            ) {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd0 = *Lptr0;
#else
                auto Xtd0 = xs::load_aligned(Lptr0);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd0_0 = xs::fma(Xtd0, Xsimd, accumsimd0_0);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr1;
#else
                    auto Xsimd = xs::load_aligned(Rptr1);
#endif
                    accumsimd0_1 = xs::fma(Xtd0, Xsimd, accumsimd0_1);
                }
        }

        // horizontal sum of the simd blocks
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_0 = accumsimd0_0;
#else
                F accum0_0 = xs::XSIMD_REDUCE_ADD(accumsimd0_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_1 = accumsimd0_1;
#else
                F accum0_1 = xs::XSIMD_REDUCE_ADD(accumsimd0_1);
#endif

        // remainder loop handling the entries that can't be handled in a
        // simd_size stride
        for (int k = kblocksize; k < kmax - kmin; k++) {
                F Xtd0 = L[basei0 + k];
                F Xv0 = R[basej0 + k];
                F Xv1 = R[basej1 + k];
                    accum0_0 += Xtd0 * Xv0;
                    accum0_1 += Xtd0 * Xv1;
        }

        // add to the output array
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 0) * out_m + (j + 0)] += accum0_0;
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 0) * out_m + (j + 1)] += accum0_1;
    }

        }
        {
            
    int jmaxblock = jmin + ((jmaxinner - jmin) / 1) * 1;
    for (; j < jmaxblock; j += 1) {

        // setup simd accumulators
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_0 = (F)0.0;
#else
                auto accumsimd0_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif

            int basei0 = (i - imin2 + 0) * kstep;
            int basej0 = (j - jmin2 + 0) * kstep;

        // main simd inner loop
            F* Lptr0 = &L[basei0];
            F* Rptr0 = &R[basej0];
        int kblocksize = ((kmax - kmin) / simd_size) * simd_size;
        F* Rptr0end = Rptr0 + kblocksize;
        for(; Rptr0 < Rptr0end; 
                Rptr0+=simd_size,
                    Lptr0 += simd_size
            ) {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd0 = *Lptr0;
#else
                auto Xtd0 = xs::load_aligned(Lptr0);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd0_0 = xs::fma(Xtd0, Xsimd, accumsimd0_0);
                }
        }

        // horizontal sum of the simd blocks
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_0 = accumsimd0_0;
#else
                F accum0_0 = xs::XSIMD_REDUCE_ADD(accumsimd0_0);
#endif

        // remainder loop handling the entries that can't be handled in a
        // simd_size stride
        for (int k = kblocksize; k < kmax - kmin; k++) {
                F Xtd0 = L[basei0 + k];
                F Xv0 = R[basej0 + k];
                    accum0_0 += Xtd0 * Xv0;
        }

        // add to the output array
                    // we only need to be careful about parallelism when we're
                    // parallelizing the k loop. if we're just parallelizing i
                    // and j, the sum here is safe
                    #pragma omp atomic
                out[(i + 0) * out_m + (j + 0)] += accum0_0;
    }

        }
    }

            }
        }
    }
}


template <typename Int, typename F>
void dense_baseFalse(F* R, F* L, F* d, F* out,
                Py_ssize_t out_m,
                Py_ssize_t imin2, Py_ssize_t imax2,
                Py_ssize_t jmin2, Py_ssize_t jmax2, 
                Py_ssize_t kmin, Py_ssize_t kmax, Int innerblock, Int kstep) 
{
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
    constexpr std::size_t simd_size = 1;
#else
    constexpr std::size_t simd_size = xsimd::simd_type<F>::size;
#endif
    for (Py_ssize_t imin = imin2; imin < imax2; imin+=innerblock) {
        Py_ssize_t imax = imin + innerblock; 
        if (imax > imax2) {
            imax = imax2; 
        }
        for (Py_ssize_t jmin = jmin2; jmin < jmax2; jmin+=innerblock) {
            Py_ssize_t jmax = jmin + innerblock; 
            if (jmax > jmax2) {
                jmax = jmax2; 
            }
            Py_ssize_t i = imin;
            {
                
    int imaxblock = imin + ((imax - imin) / 4) * 4;
    for (; i < imaxblock; i += 4) {
        int jmaxinner = jmax;
        if (jmaxinner > i + 4) {
            jmaxinner = i + 4;
        }
        int j = jmin;
        {
            
    int jmaxblock = jmin + ((jmaxinner - jmin) / 4) * 4;
    for (; j < jmaxblock; j += 4) {

        // setup simd accumulators
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_0 = (F)0.0;
#else
                auto accumsimd0_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_1 = (F)0.0;
#else
                auto accumsimd0_1 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_2 = (F)0.0;
#else
                auto accumsimd0_2 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_3 = (F)0.0;
#else
                auto accumsimd0_3 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd1_0 = (F)0.0;
#else
                auto accumsimd1_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd1_1 = (F)0.0;
#else
                auto accumsimd1_1 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd1_2 = (F)0.0;
#else
                auto accumsimd1_2 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd1_3 = (F)0.0;
#else
                auto accumsimd1_3 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd2_0 = (F)0.0;
#else
                auto accumsimd2_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd2_1 = (F)0.0;
#else
                auto accumsimd2_1 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd2_2 = (F)0.0;
#else
                auto accumsimd2_2 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd2_3 = (F)0.0;
#else
                auto accumsimd2_3 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd3_0 = (F)0.0;
#else
                auto accumsimd3_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd3_1 = (F)0.0;
#else
                auto accumsimd3_1 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd3_2 = (F)0.0;
#else
                auto accumsimd3_2 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd3_3 = (F)0.0;
#else
                auto accumsimd3_3 = xs::XSIMD_BROADCAST(((F)0.0));
#endif

            int basei0 = (i - imin2 + 0) * kstep;
            int basei1 = (i - imin2 + 1) * kstep;
            int basei2 = (i - imin2 + 2) * kstep;
            int basei3 = (i - imin2 + 3) * kstep;
            int basej0 = (j - jmin2 + 0) * kstep;
            int basej1 = (j - jmin2 + 1) * kstep;
            int basej2 = (j - jmin2 + 2) * kstep;
            int basej3 = (j - jmin2 + 3) * kstep;

        // main simd inner loop
            F* Lptr0 = &L[basei0];
            F* Lptr1 = &L[basei1];
            F* Lptr2 = &L[basei2];
            F* Lptr3 = &L[basei3];
            F* Rptr0 = &R[basej0];
            F* Rptr1 = &R[basej1];
            F* Rptr2 = &R[basej2];
            F* Rptr3 = &R[basej3];
        int kblocksize = ((kmax - kmin) / simd_size) * simd_size;
        F* Rptr0end = Rptr0 + kblocksize;
        for(; Rptr0 < Rptr0end; 
                Rptr0+=simd_size,
                Rptr1+=simd_size,
                Rptr2+=simd_size,
                Rptr3+=simd_size,
                    Lptr0 += simd_size,
                    Lptr1 += simd_size,
                    Lptr2 += simd_size,
                    Lptr3 += simd_size
            ) {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd0 = *Lptr0;
#else
                auto Xtd0 = xs::load_aligned(Lptr0);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd0_0 = xs::fma(Xtd0, Xsimd, accumsimd0_0);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr1;
#else
                    auto Xsimd = xs::load_aligned(Rptr1);
#endif
                    accumsimd0_1 = xs::fma(Xtd0, Xsimd, accumsimd0_1);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr2;
#else
                    auto Xsimd = xs::load_aligned(Rptr2);
#endif
                    accumsimd0_2 = xs::fma(Xtd0, Xsimd, accumsimd0_2);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr3;
#else
                    auto Xsimd = xs::load_aligned(Rptr3);
#endif
                    accumsimd0_3 = xs::fma(Xtd0, Xsimd, accumsimd0_3);
                }
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd1 = *Lptr1;
#else
                auto Xtd1 = xs::load_aligned(Lptr1);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd1_0 = xs::fma(Xtd1, Xsimd, accumsimd1_0);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr1;
#else
                    auto Xsimd = xs::load_aligned(Rptr1);
#endif
                    accumsimd1_1 = xs::fma(Xtd1, Xsimd, accumsimd1_1);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr2;
#else
                    auto Xsimd = xs::load_aligned(Rptr2);
#endif
                    accumsimd1_2 = xs::fma(Xtd1, Xsimd, accumsimd1_2);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr3;
#else
                    auto Xsimd = xs::load_aligned(Rptr3);
#endif
                    accumsimd1_3 = xs::fma(Xtd1, Xsimd, accumsimd1_3);
                }
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd2 = *Lptr2;
#else
                auto Xtd2 = xs::load_aligned(Lptr2);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd2_0 = xs::fma(Xtd2, Xsimd, accumsimd2_0);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr1;
#else
                    auto Xsimd = xs::load_aligned(Rptr1);
#endif
                    accumsimd2_1 = xs::fma(Xtd2, Xsimd, accumsimd2_1);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr2;
#else
                    auto Xsimd = xs::load_aligned(Rptr2);
#endif
                    accumsimd2_2 = xs::fma(Xtd2, Xsimd, accumsimd2_2);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr3;
#else
                    auto Xsimd = xs::load_aligned(Rptr3);
#endif
                    accumsimd2_3 = xs::fma(Xtd2, Xsimd, accumsimd2_3);
                }
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd3 = *Lptr3;
#else
                auto Xtd3 = xs::load_aligned(Lptr3);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd3_0 = xs::fma(Xtd3, Xsimd, accumsimd3_0);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr1;
#else
                    auto Xsimd = xs::load_aligned(Rptr1);
#endif
                    accumsimd3_1 = xs::fma(Xtd3, Xsimd, accumsimd3_1);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr2;
#else
                    auto Xsimd = xs::load_aligned(Rptr2);
#endif
                    accumsimd3_2 = xs::fma(Xtd3, Xsimd, accumsimd3_2);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr3;
#else
                    auto Xsimd = xs::load_aligned(Rptr3);
#endif
                    accumsimd3_3 = xs::fma(Xtd3, Xsimd, accumsimd3_3);
                }
        }

        // horizontal sum of the simd blocks
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_0 = accumsimd0_0;
#else
                F accum0_0 = xs::XSIMD_REDUCE_ADD(accumsimd0_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_1 = accumsimd0_1;
#else
                F accum0_1 = xs::XSIMD_REDUCE_ADD(accumsimd0_1);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_2 = accumsimd0_2;
#else
                F accum0_2 = xs::XSIMD_REDUCE_ADD(accumsimd0_2);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_3 = accumsimd0_3;
#else
                F accum0_3 = xs::XSIMD_REDUCE_ADD(accumsimd0_3);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum1_0 = accumsimd1_0;
#else
                F accum1_0 = xs::XSIMD_REDUCE_ADD(accumsimd1_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum1_1 = accumsimd1_1;
#else
                F accum1_1 = xs::XSIMD_REDUCE_ADD(accumsimd1_1);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum1_2 = accumsimd1_2;
#else
                F accum1_2 = xs::XSIMD_REDUCE_ADD(accumsimd1_2);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum1_3 = accumsimd1_3;
#else
                F accum1_3 = xs::XSIMD_REDUCE_ADD(accumsimd1_3);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum2_0 = accumsimd2_0;
#else
                F accum2_0 = xs::XSIMD_REDUCE_ADD(accumsimd2_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum2_1 = accumsimd2_1;
#else
                F accum2_1 = xs::XSIMD_REDUCE_ADD(accumsimd2_1);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum2_2 = accumsimd2_2;
#else
                F accum2_2 = xs::XSIMD_REDUCE_ADD(accumsimd2_2);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum2_3 = accumsimd2_3;
#else
                F accum2_3 = xs::XSIMD_REDUCE_ADD(accumsimd2_3);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum3_0 = accumsimd3_0;
#else
                F accum3_0 = xs::XSIMD_REDUCE_ADD(accumsimd3_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum3_1 = accumsimd3_1;
#else
                F accum3_1 = xs::XSIMD_REDUCE_ADD(accumsimd3_1);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum3_2 = accumsimd3_2;
#else
                F accum3_2 = xs::XSIMD_REDUCE_ADD(accumsimd3_2);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum3_3 = accumsimd3_3;
#else
                F accum3_3 = xs::XSIMD_REDUCE_ADD(accumsimd3_3);
#endif

        // remainder loop handling the entries that can't be handled in a
        // simd_size stride
        for (int k = kblocksize; k < kmax - kmin; k++) {
                F Xtd0 = L[basei0 + k];
                F Xtd1 = L[basei1 + k];
                F Xtd2 = L[basei2 + k];
                F Xtd3 = L[basei3 + k];
                F Xv0 = R[basej0 + k];
                F Xv1 = R[basej1 + k];
                F Xv2 = R[basej2 + k];
                F Xv3 = R[basej3 + k];
                    accum0_0 += Xtd0 * Xv0;
                    accum0_1 += Xtd0 * Xv1;
                    accum0_2 += Xtd0 * Xv2;
                    accum0_3 += Xtd0 * Xv3;
                    accum1_0 += Xtd1 * Xv0;
                    accum1_1 += Xtd1 * Xv1;
                    accum1_2 += Xtd1 * Xv2;
                    accum1_3 += Xtd1 * Xv3;
                    accum2_0 += Xtd2 * Xv0;
                    accum2_1 += Xtd2 * Xv1;
                    accum2_2 += Xtd2 * Xv2;
                    accum2_3 += Xtd2 * Xv3;
                    accum3_0 += Xtd3 * Xv0;
                    accum3_1 += Xtd3 * Xv1;
                    accum3_2 += Xtd3 * Xv2;
                    accum3_3 += Xtd3 * Xv3;
        }

        // add to the output array
                out[(i + 0) * out_m + (j + 0)] += accum0_0;
                out[(i + 0) * out_m + (j + 1)] += accum0_1;
                out[(i + 0) * out_m + (j + 2)] += accum0_2;
                out[(i + 0) * out_m + (j + 3)] += accum0_3;
                out[(i + 1) * out_m + (j + 0)] += accum1_0;
                out[(i + 1) * out_m + (j + 1)] += accum1_1;
                out[(i + 1) * out_m + (j + 2)] += accum1_2;
                out[(i + 1) * out_m + (j + 3)] += accum1_3;
                out[(i + 2) * out_m + (j + 0)] += accum2_0;
                out[(i + 2) * out_m + (j + 1)] += accum2_1;
                out[(i + 2) * out_m + (j + 2)] += accum2_2;
                out[(i + 2) * out_m + (j + 3)] += accum2_3;
                out[(i + 3) * out_m + (j + 0)] += accum3_0;
                out[(i + 3) * out_m + (j + 1)] += accum3_1;
                out[(i + 3) * out_m + (j + 2)] += accum3_2;
                out[(i + 3) * out_m + (j + 3)] += accum3_3;
    }

        }
        {
            
    int jmaxblock = jmin + ((jmaxinner - jmin) / 2) * 2;
    for (; j < jmaxblock; j += 2) {

        // setup simd accumulators
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_0 = (F)0.0;
#else
                auto accumsimd0_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_1 = (F)0.0;
#else
                auto accumsimd0_1 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd1_0 = (F)0.0;
#else
                auto accumsimd1_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd1_1 = (F)0.0;
#else
                auto accumsimd1_1 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd2_0 = (F)0.0;
#else
                auto accumsimd2_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd2_1 = (F)0.0;
#else
                auto accumsimd2_1 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd3_0 = (F)0.0;
#else
                auto accumsimd3_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd3_1 = (F)0.0;
#else
                auto accumsimd3_1 = xs::XSIMD_BROADCAST(((F)0.0));
#endif

            int basei0 = (i - imin2 + 0) * kstep;
            int basei1 = (i - imin2 + 1) * kstep;
            int basei2 = (i - imin2 + 2) * kstep;
            int basei3 = (i - imin2 + 3) * kstep;
            int basej0 = (j - jmin2 + 0) * kstep;
            int basej1 = (j - jmin2 + 1) * kstep;

        // main simd inner loop
            F* Lptr0 = &L[basei0];
            F* Lptr1 = &L[basei1];
            F* Lptr2 = &L[basei2];
            F* Lptr3 = &L[basei3];
            F* Rptr0 = &R[basej0];
            F* Rptr1 = &R[basej1];
        int kblocksize = ((kmax - kmin) / simd_size) * simd_size;
        F* Rptr0end = Rptr0 + kblocksize;
        for(; Rptr0 < Rptr0end; 
                Rptr0+=simd_size,
                Rptr1+=simd_size,
                    Lptr0 += simd_size,
                    Lptr1 += simd_size,
                    Lptr2 += simd_size,
                    Lptr3 += simd_size
            ) {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd0 = *Lptr0;
#else
                auto Xtd0 = xs::load_aligned(Lptr0);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd0_0 = xs::fma(Xtd0, Xsimd, accumsimd0_0);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr1;
#else
                    auto Xsimd = xs::load_aligned(Rptr1);
#endif
                    accumsimd0_1 = xs::fma(Xtd0, Xsimd, accumsimd0_1);
                }
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd1 = *Lptr1;
#else
                auto Xtd1 = xs::load_aligned(Lptr1);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd1_0 = xs::fma(Xtd1, Xsimd, accumsimd1_0);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr1;
#else
                    auto Xsimd = xs::load_aligned(Rptr1);
#endif
                    accumsimd1_1 = xs::fma(Xtd1, Xsimd, accumsimd1_1);
                }
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd2 = *Lptr2;
#else
                auto Xtd2 = xs::load_aligned(Lptr2);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd2_0 = xs::fma(Xtd2, Xsimd, accumsimd2_0);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr1;
#else
                    auto Xsimd = xs::load_aligned(Rptr1);
#endif
                    accumsimd2_1 = xs::fma(Xtd2, Xsimd, accumsimd2_1);
                }
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd3 = *Lptr3;
#else
                auto Xtd3 = xs::load_aligned(Lptr3);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd3_0 = xs::fma(Xtd3, Xsimd, accumsimd3_0);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr1;
#else
                    auto Xsimd = xs::load_aligned(Rptr1);
#endif
                    accumsimd3_1 = xs::fma(Xtd3, Xsimd, accumsimd3_1);
                }
        }

        // horizontal sum of the simd blocks
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_0 = accumsimd0_0;
#else
                F accum0_0 = xs::XSIMD_REDUCE_ADD(accumsimd0_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_1 = accumsimd0_1;
#else
                F accum0_1 = xs::XSIMD_REDUCE_ADD(accumsimd0_1);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum1_0 = accumsimd1_0;
#else
                F accum1_0 = xs::XSIMD_REDUCE_ADD(accumsimd1_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum1_1 = accumsimd1_1;
#else
                F accum1_1 = xs::XSIMD_REDUCE_ADD(accumsimd1_1);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum2_0 = accumsimd2_0;
#else
                F accum2_0 = xs::XSIMD_REDUCE_ADD(accumsimd2_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum2_1 = accumsimd2_1;
#else
                F accum2_1 = xs::XSIMD_REDUCE_ADD(accumsimd2_1);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum3_0 = accumsimd3_0;
#else
                F accum3_0 = xs::XSIMD_REDUCE_ADD(accumsimd3_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum3_1 = accumsimd3_1;
#else
                F accum3_1 = xs::XSIMD_REDUCE_ADD(accumsimd3_1);
#endif

        // remainder loop handling the entries that can't be handled in a
        // simd_size stride
        for (int k = kblocksize; k < kmax - kmin; k++) {
                F Xtd0 = L[basei0 + k];
                F Xtd1 = L[basei1 + k];
                F Xtd2 = L[basei2 + k];
                F Xtd3 = L[basei3 + k];
                F Xv0 = R[basej0 + k];
                F Xv1 = R[basej1 + k];
                    accum0_0 += Xtd0 * Xv0;
                    accum0_1 += Xtd0 * Xv1;
                    accum1_0 += Xtd1 * Xv0;
                    accum1_1 += Xtd1 * Xv1;
                    accum2_0 += Xtd2 * Xv0;
                    accum2_1 += Xtd2 * Xv1;
                    accum3_0 += Xtd3 * Xv0;
                    accum3_1 += Xtd3 * Xv1;
        }

        // add to the output array
                out[(i + 0) * out_m + (j + 0)] += accum0_0;
                out[(i + 0) * out_m + (j + 1)] += accum0_1;
                out[(i + 1) * out_m + (j + 0)] += accum1_0;
                out[(i + 1) * out_m + (j + 1)] += accum1_1;
                out[(i + 2) * out_m + (j + 0)] += accum2_0;
                out[(i + 2) * out_m + (j + 1)] += accum2_1;
                out[(i + 3) * out_m + (j + 0)] += accum3_0;
                out[(i + 3) * out_m + (j + 1)] += accum3_1;
    }

        }
        {
            
    int jmaxblock = jmin + ((jmaxinner - jmin) / 1) * 1;
    for (; j < jmaxblock; j += 1) {

        // setup simd accumulators
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_0 = (F)0.0;
#else
                auto accumsimd0_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd1_0 = (F)0.0;
#else
                auto accumsimd1_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd2_0 = (F)0.0;
#else
                auto accumsimd2_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd3_0 = (F)0.0;
#else
                auto accumsimd3_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif

            int basei0 = (i - imin2 + 0) * kstep;
            int basei1 = (i - imin2 + 1) * kstep;
            int basei2 = (i - imin2 + 2) * kstep;
            int basei3 = (i - imin2 + 3) * kstep;
            int basej0 = (j - jmin2 + 0) * kstep;

        // main simd inner loop
            F* Lptr0 = &L[basei0];
            F* Lptr1 = &L[basei1];
            F* Lptr2 = &L[basei2];
            F* Lptr3 = &L[basei3];
            F* Rptr0 = &R[basej0];
        int kblocksize = ((kmax - kmin) / simd_size) * simd_size;
        F* Rptr0end = Rptr0 + kblocksize;
        for(; Rptr0 < Rptr0end; 
                Rptr0+=simd_size,
                    Lptr0 += simd_size,
                    Lptr1 += simd_size,
                    Lptr2 += simd_size,
                    Lptr3 += simd_size
            ) {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd0 = *Lptr0;
#else
                auto Xtd0 = xs::load_aligned(Lptr0);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd0_0 = xs::fma(Xtd0, Xsimd, accumsimd0_0);
                }
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd1 = *Lptr1;
#else
                auto Xtd1 = xs::load_aligned(Lptr1);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd1_0 = xs::fma(Xtd1, Xsimd, accumsimd1_0);
                }
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd2 = *Lptr2;
#else
                auto Xtd2 = xs::load_aligned(Lptr2);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd2_0 = xs::fma(Xtd2, Xsimd, accumsimd2_0);
                }
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd3 = *Lptr3;
#else
                auto Xtd3 = xs::load_aligned(Lptr3);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd3_0 = xs::fma(Xtd3, Xsimd, accumsimd3_0);
                }
        }

        // horizontal sum of the simd blocks
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_0 = accumsimd0_0;
#else
                F accum0_0 = xs::XSIMD_REDUCE_ADD(accumsimd0_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum1_0 = accumsimd1_0;
#else
                F accum1_0 = xs::XSIMD_REDUCE_ADD(accumsimd1_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum2_0 = accumsimd2_0;
#else
                F accum2_0 = xs::XSIMD_REDUCE_ADD(accumsimd2_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum3_0 = accumsimd3_0;
#else
                F accum3_0 = xs::XSIMD_REDUCE_ADD(accumsimd3_0);
#endif

        // remainder loop handling the entries that can't be handled in a
        // simd_size stride
        for (int k = kblocksize; k < kmax - kmin; k++) {
                F Xtd0 = L[basei0 + k];
                F Xtd1 = L[basei1 + k];
                F Xtd2 = L[basei2 + k];
                F Xtd3 = L[basei3 + k];
                F Xv0 = R[basej0 + k];
                    accum0_0 += Xtd0 * Xv0;
                    accum1_0 += Xtd1 * Xv0;
                    accum2_0 += Xtd2 * Xv0;
                    accum3_0 += Xtd3 * Xv0;
        }

        // add to the output array
                out[(i + 0) * out_m + (j + 0)] += accum0_0;
                out[(i + 1) * out_m + (j + 0)] += accum1_0;
                out[(i + 2) * out_m + (j + 0)] += accum2_0;
                out[(i + 3) * out_m + (j + 0)] += accum3_0;
    }

        }
    }

            }
            {
                
    int imaxblock = imin + ((imax - imin) / 2) * 2;
    for (; i < imaxblock; i += 2) {
        int jmaxinner = jmax;
        if (jmaxinner > i + 2) {
            jmaxinner = i + 2;
        }
        int j = jmin;
        {
            
    int jmaxblock = jmin + ((jmaxinner - jmin) / 4) * 4;
    for (; j < jmaxblock; j += 4) {

        // setup simd accumulators
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_0 = (F)0.0;
#else
                auto accumsimd0_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_1 = (F)0.0;
#else
                auto accumsimd0_1 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_2 = (F)0.0;
#else
                auto accumsimd0_2 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_3 = (F)0.0;
#else
                auto accumsimd0_3 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd1_0 = (F)0.0;
#else
                auto accumsimd1_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd1_1 = (F)0.0;
#else
                auto accumsimd1_1 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd1_2 = (F)0.0;
#else
                auto accumsimd1_2 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd1_3 = (F)0.0;
#else
                auto accumsimd1_3 = xs::XSIMD_BROADCAST(((F)0.0));
#endif

            int basei0 = (i - imin2 + 0) * kstep;
            int basei1 = (i - imin2 + 1) * kstep;
            int basej0 = (j - jmin2 + 0) * kstep;
            int basej1 = (j - jmin2 + 1) * kstep;
            int basej2 = (j - jmin2 + 2) * kstep;
            int basej3 = (j - jmin2 + 3) * kstep;

        // main simd inner loop
            F* Lptr0 = &L[basei0];
            F* Lptr1 = &L[basei1];
            F* Rptr0 = &R[basej0];
            F* Rptr1 = &R[basej1];
            F* Rptr2 = &R[basej2];
            F* Rptr3 = &R[basej3];
        int kblocksize = ((kmax - kmin) / simd_size) * simd_size;
        F* Rptr0end = Rptr0 + kblocksize;
        for(; Rptr0 < Rptr0end; 
                Rptr0+=simd_size,
                Rptr1+=simd_size,
                Rptr2+=simd_size,
                Rptr3+=simd_size,
                    Lptr0 += simd_size,
                    Lptr1 += simd_size
            ) {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd0 = *Lptr0;
#else
                auto Xtd0 = xs::load_aligned(Lptr0);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd0_0 = xs::fma(Xtd0, Xsimd, accumsimd0_0);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr1;
#else
                    auto Xsimd = xs::load_aligned(Rptr1);
#endif
                    accumsimd0_1 = xs::fma(Xtd0, Xsimd, accumsimd0_1);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr2;
#else
                    auto Xsimd = xs::load_aligned(Rptr2);
#endif
                    accumsimd0_2 = xs::fma(Xtd0, Xsimd, accumsimd0_2);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr3;
#else
                    auto Xsimd = xs::load_aligned(Rptr3);
#endif
                    accumsimd0_3 = xs::fma(Xtd0, Xsimd, accumsimd0_3);
                }
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd1 = *Lptr1;
#else
                auto Xtd1 = xs::load_aligned(Lptr1);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd1_0 = xs::fma(Xtd1, Xsimd, accumsimd1_0);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr1;
#else
                    auto Xsimd = xs::load_aligned(Rptr1);
#endif
                    accumsimd1_1 = xs::fma(Xtd1, Xsimd, accumsimd1_1);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr2;
#else
                    auto Xsimd = xs::load_aligned(Rptr2);
#endif
                    accumsimd1_2 = xs::fma(Xtd1, Xsimd, accumsimd1_2);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr3;
#else
                    auto Xsimd = xs::load_aligned(Rptr3);
#endif
                    accumsimd1_3 = xs::fma(Xtd1, Xsimd, accumsimd1_3);
                }
        }

        // horizontal sum of the simd blocks
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_0 = accumsimd0_0;
#else
                F accum0_0 = xs::XSIMD_REDUCE_ADD(accumsimd0_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_1 = accumsimd0_1;
#else
                F accum0_1 = xs::XSIMD_REDUCE_ADD(accumsimd0_1);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_2 = accumsimd0_2;
#else
                F accum0_2 = xs::XSIMD_REDUCE_ADD(accumsimd0_2);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_3 = accumsimd0_3;
#else
                F accum0_3 = xs::XSIMD_REDUCE_ADD(accumsimd0_3);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum1_0 = accumsimd1_0;
#else
                F accum1_0 = xs::XSIMD_REDUCE_ADD(accumsimd1_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum1_1 = accumsimd1_1;
#else
                F accum1_1 = xs::XSIMD_REDUCE_ADD(accumsimd1_1);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum1_2 = accumsimd1_2;
#else
                F accum1_2 = xs::XSIMD_REDUCE_ADD(accumsimd1_2);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum1_3 = accumsimd1_3;
#else
                F accum1_3 = xs::XSIMD_REDUCE_ADD(accumsimd1_3);
#endif

        // remainder loop handling the entries that can't be handled in a
        // simd_size stride
        for (int k = kblocksize; k < kmax - kmin; k++) {
                F Xtd0 = L[basei0 + k];
                F Xtd1 = L[basei1 + k];
                F Xv0 = R[basej0 + k];
                F Xv1 = R[basej1 + k];
                F Xv2 = R[basej2 + k];
                F Xv3 = R[basej3 + k];
                    accum0_0 += Xtd0 * Xv0;
                    accum0_1 += Xtd0 * Xv1;
                    accum0_2 += Xtd0 * Xv2;
                    accum0_3 += Xtd0 * Xv3;
                    accum1_0 += Xtd1 * Xv0;
                    accum1_1 += Xtd1 * Xv1;
                    accum1_2 += Xtd1 * Xv2;
                    accum1_3 += Xtd1 * Xv3;
        }

        // add to the output array
                out[(i + 0) * out_m + (j + 0)] += accum0_0;
                out[(i + 0) * out_m + (j + 1)] += accum0_1;
                out[(i + 0) * out_m + (j + 2)] += accum0_2;
                out[(i + 0) * out_m + (j + 3)] += accum0_3;
                out[(i + 1) * out_m + (j + 0)] += accum1_0;
                out[(i + 1) * out_m + (j + 1)] += accum1_1;
                out[(i + 1) * out_m + (j + 2)] += accum1_2;
                out[(i + 1) * out_m + (j + 3)] += accum1_3;
    }

        }
        {
            
    int jmaxblock = jmin + ((jmaxinner - jmin) / 2) * 2;
    for (; j < jmaxblock; j += 2) {

        // setup simd accumulators
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_0 = (F)0.0;
#else
                auto accumsimd0_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_1 = (F)0.0;
#else
                auto accumsimd0_1 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd1_0 = (F)0.0;
#else
                auto accumsimd1_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd1_1 = (F)0.0;
#else
                auto accumsimd1_1 = xs::XSIMD_BROADCAST(((F)0.0));
#endif

            int basei0 = (i - imin2 + 0) * kstep;
            int basei1 = (i - imin2 + 1) * kstep;
            int basej0 = (j - jmin2 + 0) * kstep;
            int basej1 = (j - jmin2 + 1) * kstep;

        // main simd inner loop
            F* Lptr0 = &L[basei0];
            F* Lptr1 = &L[basei1];
            F* Rptr0 = &R[basej0];
            F* Rptr1 = &R[basej1];
        int kblocksize = ((kmax - kmin) / simd_size) * simd_size;
        F* Rptr0end = Rptr0 + kblocksize;
        for(; Rptr0 < Rptr0end; 
                Rptr0+=simd_size,
                Rptr1+=simd_size,
                    Lptr0 += simd_size,
                    Lptr1 += simd_size
            ) {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd0 = *Lptr0;
#else
                auto Xtd0 = xs::load_aligned(Lptr0);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd0_0 = xs::fma(Xtd0, Xsimd, accumsimd0_0);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr1;
#else
                    auto Xsimd = xs::load_aligned(Rptr1);
#endif
                    accumsimd0_1 = xs::fma(Xtd0, Xsimd, accumsimd0_1);
                }
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd1 = *Lptr1;
#else
                auto Xtd1 = xs::load_aligned(Lptr1);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd1_0 = xs::fma(Xtd1, Xsimd, accumsimd1_0);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr1;
#else
                    auto Xsimd = xs::load_aligned(Rptr1);
#endif
                    accumsimd1_1 = xs::fma(Xtd1, Xsimd, accumsimd1_1);
                }
        }

        // horizontal sum of the simd blocks
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_0 = accumsimd0_0;
#else
                F accum0_0 = xs::XSIMD_REDUCE_ADD(accumsimd0_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_1 = accumsimd0_1;
#else
                F accum0_1 = xs::XSIMD_REDUCE_ADD(accumsimd0_1);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum1_0 = accumsimd1_0;
#else
                F accum1_0 = xs::XSIMD_REDUCE_ADD(accumsimd1_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum1_1 = accumsimd1_1;
#else
                F accum1_1 = xs::XSIMD_REDUCE_ADD(accumsimd1_1);
#endif

        // remainder loop handling the entries that can't be handled in a
        // simd_size stride
        for (int k = kblocksize; k < kmax - kmin; k++) {
                F Xtd0 = L[basei0 + k];
                F Xtd1 = L[basei1 + k];
                F Xv0 = R[basej0 + k];
                F Xv1 = R[basej1 + k];
                    accum0_0 += Xtd0 * Xv0;
                    accum0_1 += Xtd0 * Xv1;
                    accum1_0 += Xtd1 * Xv0;
                    accum1_1 += Xtd1 * Xv1;
        }

        // add to the output array
                out[(i + 0) * out_m + (j + 0)] += accum0_0;
                out[(i + 0) * out_m + (j + 1)] += accum0_1;
                out[(i + 1) * out_m + (j + 0)] += accum1_0;
                out[(i + 1) * out_m + (j + 1)] += accum1_1;
    }

        }
        {
            
    int jmaxblock = jmin + ((jmaxinner - jmin) / 1) * 1;
    for (; j < jmaxblock; j += 1) {

        // setup simd accumulators
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_0 = (F)0.0;
#else
                auto accumsimd0_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd1_0 = (F)0.0;
#else
                auto accumsimd1_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif

            int basei0 = (i - imin2 + 0) * kstep;
            int basei1 = (i - imin2 + 1) * kstep;
            int basej0 = (j - jmin2 + 0) * kstep;

        // main simd inner loop
            F* Lptr0 = &L[basei0];
            F* Lptr1 = &L[basei1];
            F* Rptr0 = &R[basej0];
        int kblocksize = ((kmax - kmin) / simd_size) * simd_size;
        F* Rptr0end = Rptr0 + kblocksize;
        for(; Rptr0 < Rptr0end; 
                Rptr0+=simd_size,
                    Lptr0 += simd_size,
                    Lptr1 += simd_size
            ) {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd0 = *Lptr0;
#else
                auto Xtd0 = xs::load_aligned(Lptr0);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd0_0 = xs::fma(Xtd0, Xsimd, accumsimd0_0);
                }
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd1 = *Lptr1;
#else
                auto Xtd1 = xs::load_aligned(Lptr1);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd1_0 = xs::fma(Xtd1, Xsimd, accumsimd1_0);
                }
        }

        // horizontal sum of the simd blocks
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_0 = accumsimd0_0;
#else
                F accum0_0 = xs::XSIMD_REDUCE_ADD(accumsimd0_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum1_0 = accumsimd1_0;
#else
                F accum1_0 = xs::XSIMD_REDUCE_ADD(accumsimd1_0);
#endif

        // remainder loop handling the entries that can't be handled in a
        // simd_size stride
        for (int k = kblocksize; k < kmax - kmin; k++) {
                F Xtd0 = L[basei0 + k];
                F Xtd1 = L[basei1 + k];
                F Xv0 = R[basej0 + k];
                    accum0_0 += Xtd0 * Xv0;
                    accum1_0 += Xtd1 * Xv0;
        }

        // add to the output array
                out[(i + 0) * out_m + (j + 0)] += accum0_0;
                out[(i + 1) * out_m + (j + 0)] += accum1_0;
    }

        }
    }

            }
            {
                
    int imaxblock = imin + ((imax - imin) / 1) * 1;
    for (; i < imaxblock; i += 1) {
        int jmaxinner = jmax;
        if (jmaxinner > i + 1) {
            jmaxinner = i + 1;
        }
        int j = jmin;
        {
            
    int jmaxblock = jmin + ((jmaxinner - jmin) / 4) * 4;
    for (; j < jmaxblock; j += 4) {

        // setup simd accumulators
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_0 = (F)0.0;
#else
                auto accumsimd0_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_1 = (F)0.0;
#else
                auto accumsimd0_1 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_2 = (F)0.0;
#else
                auto accumsimd0_2 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_3 = (F)0.0;
#else
                auto accumsimd0_3 = xs::XSIMD_BROADCAST(((F)0.0));
#endif

            int basei0 = (i - imin2 + 0) * kstep;
            int basej0 = (j - jmin2 + 0) * kstep;
            int basej1 = (j - jmin2 + 1) * kstep;
            int basej2 = (j - jmin2 + 2) * kstep;
            int basej3 = (j - jmin2 + 3) * kstep;

        // main simd inner loop
            F* Lptr0 = &L[basei0];
            F* Rptr0 = &R[basej0];
            F* Rptr1 = &R[basej1];
            F* Rptr2 = &R[basej2];
            F* Rptr3 = &R[basej3];
        int kblocksize = ((kmax - kmin) / simd_size) * simd_size;
        F* Rptr0end = Rptr0 + kblocksize;
        for(; Rptr0 < Rptr0end; 
                Rptr0+=simd_size,
                Rptr1+=simd_size,
                Rptr2+=simd_size,
                Rptr3+=simd_size,
                    Lptr0 += simd_size
            ) {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd0 = *Lptr0;
#else
                auto Xtd0 = xs::load_aligned(Lptr0);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd0_0 = xs::fma(Xtd0, Xsimd, accumsimd0_0);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr1;
#else
                    auto Xsimd = xs::load_aligned(Rptr1);
#endif
                    accumsimd0_1 = xs::fma(Xtd0, Xsimd, accumsimd0_1);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr2;
#else
                    auto Xsimd = xs::load_aligned(Rptr2);
#endif
                    accumsimd0_2 = xs::fma(Xtd0, Xsimd, accumsimd0_2);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr3;
#else
                    auto Xsimd = xs::load_aligned(Rptr3);
#endif
                    accumsimd0_3 = xs::fma(Xtd0, Xsimd, accumsimd0_3);
                }
        }

        // horizontal sum of the simd blocks
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_0 = accumsimd0_0;
#else
                F accum0_0 = xs::XSIMD_REDUCE_ADD(accumsimd0_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_1 = accumsimd0_1;
#else
                F accum0_1 = xs::XSIMD_REDUCE_ADD(accumsimd0_1);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_2 = accumsimd0_2;
#else
                F accum0_2 = xs::XSIMD_REDUCE_ADD(accumsimd0_2);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_3 = accumsimd0_3;
#else
                F accum0_3 = xs::XSIMD_REDUCE_ADD(accumsimd0_3);
#endif

        // remainder loop handling the entries that can't be handled in a
        // simd_size stride
        for (int k = kblocksize; k < kmax - kmin; k++) {
                F Xtd0 = L[basei0 + k];
                F Xv0 = R[basej0 + k];
                F Xv1 = R[basej1 + k];
                F Xv2 = R[basej2 + k];
                F Xv3 = R[basej3 + k];
                    accum0_0 += Xtd0 * Xv0;
                    accum0_1 += Xtd0 * Xv1;
                    accum0_2 += Xtd0 * Xv2;
                    accum0_3 += Xtd0 * Xv3;
        }

        // add to the output array
                out[(i + 0) * out_m + (j + 0)] += accum0_0;
                out[(i + 0) * out_m + (j + 1)] += accum0_1;
                out[(i + 0) * out_m + (j + 2)] += accum0_2;
                out[(i + 0) * out_m + (j + 3)] += accum0_3;
    }

        }
        {
            
    int jmaxblock = jmin + ((jmaxinner - jmin) / 2) * 2;
    for (; j < jmaxblock; j += 2) {

        // setup simd accumulators
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_0 = (F)0.0;
#else
                auto accumsimd0_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_1 = (F)0.0;
#else
                auto accumsimd0_1 = xs::XSIMD_BROADCAST(((F)0.0));
#endif

            int basei0 = (i - imin2 + 0) * kstep;
            int basej0 = (j - jmin2 + 0) * kstep;
            int basej1 = (j - jmin2 + 1) * kstep;

        // main simd inner loop
            F* Lptr0 = &L[basei0];
            F* Rptr0 = &R[basej0];
            F* Rptr1 = &R[basej1];
        int kblocksize = ((kmax - kmin) / simd_size) * simd_size;
        F* Rptr0end = Rptr0 + kblocksize;
        for(; Rptr0 < Rptr0end; 
                Rptr0+=simd_size,
                Rptr1+=simd_size,
                    Lptr0 += simd_size
            ) {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd0 = *Lptr0;
#else
                auto Xtd0 = xs::load_aligned(Lptr0);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd0_0 = xs::fma(Xtd0, Xsimd, accumsimd0_0);
                }
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr1;
#else
                    auto Xsimd = xs::load_aligned(Rptr1);
#endif
                    accumsimd0_1 = xs::fma(Xtd0, Xsimd, accumsimd0_1);
                }
        }

        // horizontal sum of the simd blocks
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_0 = accumsimd0_0;
#else
                F accum0_0 = xs::XSIMD_REDUCE_ADD(accumsimd0_0);
#endif
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_1 = accumsimd0_1;
#else
                F accum0_1 = xs::XSIMD_REDUCE_ADD(accumsimd0_1);
#endif

        // remainder loop handling the entries that can't be handled in a
        // simd_size stride
        for (int k = kblocksize; k < kmax - kmin; k++) {
                F Xtd0 = L[basei0 + k];
                F Xv0 = R[basej0 + k];
                F Xv1 = R[basej1 + k];
                    accum0_0 += Xtd0 * Xv0;
                    accum0_1 += Xtd0 * Xv1;
        }

        // add to the output array
                out[(i + 0) * out_m + (j + 0)] += accum0_0;
                out[(i + 0) * out_m + (j + 1)] += accum0_1;
    }

        }
        {
            
    int jmaxblock = jmin + ((jmaxinner - jmin) / 1) * 1;
    for (; j < jmaxblock; j += 1) {

        // setup simd accumulators
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto accumsimd0_0 = (F)0.0;
#else
                auto accumsimd0_0 = xs::XSIMD_BROADCAST(((F)0.0));
#endif

            int basei0 = (i - imin2 + 0) * kstep;
            int basej0 = (j - jmin2 + 0) * kstep;

        // main simd inner loop
            F* Lptr0 = &L[basei0];
            F* Rptr0 = &R[basej0];
        int kblocksize = ((kmax - kmin) / simd_size) * simd_size;
        F* Rptr0end = Rptr0 + kblocksize;
        for(; Rptr0 < Rptr0end; 
                Rptr0+=simd_size,
                    Lptr0 += simd_size
            ) {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		auto Xtd0 = *Lptr0;
#else
                auto Xtd0 = xs::load_aligned(Lptr0);
#endif
                {
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		    auto Xsimd = *Rptr0;
#else
                    auto Xsimd = xs::load_aligned(Rptr0);
#endif
                    accumsimd0_0 = xs::fma(Xtd0, Xsimd, accumsimd0_0);
                }
        }

        // horizontal sum of the simd blocks
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
		F accum0_0 = accumsimd0_0;
#else
                F accum0_0 = xs::XSIMD_REDUCE_ADD(accumsimd0_0);
#endif

        // remainder loop handling the entries that can't be handled in a
        // simd_size stride
        for (int k = kblocksize; k < kmax - kmin; k++) {
                F Xtd0 = L[basei0 + k];
                F Xv0 = R[basej0 + k];
                    accum0_0 += Xtd0 * Xv0;
        }

        // add to the output array
                out[(i + 0) * out_m + (j + 0)] += accum0_0;
    }

        }
    }

            }
        }
    }
}








template <typename Int, typename F>
void _denseC_sandwich(Int* rows, Int* cols, F* X, F* d, F* out,
        Int in_n, Int out_m, Int m, Int n, Int thresh1d, Int kratio, Int innerblock) 
{
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
    constexpr std::size_t simd_size = 1;
#else
    constexpr std::size_t simd_size = xsimd::simd_type<F>::size;
#endif
    constexpr auto alignment = simd_size * sizeof(F);

    bool kparallel = (in_n / (kratio*thresh1d)) > (out_m / thresh1d);
    Py_ssize_t Rsize = thresh1d*thresh1d*kratio*kratio;
    if (kparallel) {
        Rsize *= omp_get_max_threads();
    }

    auto Rglobal = make_aligned_unique<F>(Rsize, alignment);
    auto Lglobal = make_aligned_unique<F>(
        omp_get_max_threads() * thresh1d * thresh1d * kratio, 
        alignment
    );
    for (Py_ssize_t Cj = 0; Cj < out_m; Cj+=kratio*thresh1d) {
        Py_ssize_t Cjmax2 = Cj + kratio*thresh1d; 
        if (Cjmax2 > out_m) {
            Cjmax2 = out_m; 
        }
        if (kparallel) {
            
    #pragma omp parallel for
    for (Py_ssize_t Rk = 0; Rk < in_n; Rk+=kratio*thresh1d) {
    int Rkmax2 = Rk + kratio * thresh1d; 
    if (Rkmax2 > in_n) {
        Rkmax2 = in_n; 
    }

    F* R = Rglobal.get();
    R += omp_get_thread_num()*thresh1d*thresh1d*kratio*kratio;
    for (Py_ssize_t Cjj = Cj; Cjj < Cjmax2; Cjj++) {
        {
            Int jj = cols[Cjj];
                for (Py_ssize_t Rkk=Rk; Rkk<Rkmax2; Rkk++) {
                    Int kk = rows[Rkk];
                    R[(Cjj-Cj) * kratio * thresh1d + (Rkk-Rk)] = d[kk] * X[(Py_ssize_t) kk * m + jj];
                }
        }
    }

        for (Py_ssize_t Ci = Cj; Ci < out_m; Ci+=thresh1d) {
        Py_ssize_t Cimax2 = Ci + thresh1d; 
        if (Cimax2 > out_m) {
            Cimax2 = out_m; 
        }
        F* L = &Lglobal.get()[omp_get_thread_num()*thresh1d*thresh1d*kratio];
        for (Py_ssize_t Cii = Ci; Cii < Cimax2; Cii++) {
            Int ii = cols[Cii];
                for (Py_ssize_t Rkk=Rk; Rkk<Rkmax2; Rkk++) {
                    Int kk = rows[Rkk];
                    L[(Py_ssize_t) (Cii-Ci) * kratio * thresh1d + (Rkk-Rk)] = X[(Py_ssize_t) kk * m + ii];
                }
        }
        dense_baseTrue(R, L, d, out, out_m, Ci, Cimax2, Cj, Cjmax2, Rk, Rkmax2, innerblock, kratio*thresh1d);
    }
}

        } else {
            
    for (Py_ssize_t Rk = 0; Rk < in_n; Rk+=kratio*thresh1d) {
    int Rkmax2 = Rk + kratio * thresh1d; 
    if (Rkmax2 > in_n) {
        Rkmax2 = in_n; 
    }

    F* R = Rglobal.get();
    #pragma omp parallel for
    for (Py_ssize_t Cjj = Cj; Cjj < Cjmax2; Cjj++) {
        {
            Int jj = cols[Cjj];
                for (Py_ssize_t Rkk=Rk; Rkk<Rkmax2; Rkk++) {
                    Int kk = rows[Rkk];
                    R[(Cjj-Cj) * kratio * thresh1d + (Rkk-Rk)] = d[kk] * X[(Py_ssize_t) kk * m + jj];
                }
        }
    }

        #pragma omp parallel for
        for (Py_ssize_t Ci = Cj; Ci < out_m; Ci+=thresh1d) {
        Py_ssize_t Cimax2 = Ci + thresh1d; 
        if (Cimax2 > out_m) {
            Cimax2 = out_m; 
        }
        F* L = &Lglobal.get()[omp_get_thread_num()*thresh1d*thresh1d*kratio];
        for (Py_ssize_t Cii = Ci; Cii < Cimax2; Cii++) {
            Int ii = cols[Cii];
                for (Py_ssize_t Rkk=Rk; Rkk<Rkmax2; Rkk++) {
                    Int kk = rows[Rkk];
                    L[(Py_ssize_t) (Cii-Ci) * kratio * thresh1d + (Rkk-Rk)] = X[(Py_ssize_t) kk * m + ii];
                }
        }
        dense_baseFalse(R, L, d, out, out_m, Ci, Cimax2, Cj, Cjmax2, Rk, Rkmax2, innerblock, kratio*thresh1d);
    }
}

        }
    }

    #pragma omp parallel for if(out_m > 100)
    for (Py_ssize_t Ci = 0; Ci < out_m; Ci++) {
        for (Py_ssize_t Cj = 0; Cj <= Ci; Cj++) {
            out[Cj * out_m + Ci] = out[Ci * out_m + Cj];
        }
    }
}


template <typename Int, typename F>
void _denseF_sandwich(Int* rows, Int* cols, F* X, F* d, F* out,
        Int in_n, Int out_m, Int m, Int n, Int thresh1d, Int kratio, Int innerblock) 
{
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
    constexpr std::size_t simd_size = 1;
#else
    constexpr std::size_t simd_size = xsimd::simd_type<F>::size;
#endif
    constexpr auto alignment = simd_size * sizeof(F);

    bool kparallel = (in_n / (kratio*thresh1d)) > (out_m / thresh1d);
    Py_ssize_t Rsize = thresh1d*thresh1d*kratio*kratio;
    if (kparallel) {
        Rsize *= omp_get_max_threads();
    }

    auto Rglobal = make_aligned_unique<F>(Rsize, alignment);
    auto Lglobal = make_aligned_unique<F>(
        omp_get_max_threads() * thresh1d * thresh1d * kratio, 
        alignment
    );
    for (Py_ssize_t Cj = 0; Cj < out_m; Cj+=kratio*thresh1d) {
        Py_ssize_t Cjmax2 = Cj + kratio*thresh1d; 
        if (Cjmax2 > out_m) {
            Cjmax2 = out_m; 
        }
        if (kparallel) {
            
    #pragma omp parallel for
    for (Py_ssize_t Rk = 0; Rk < in_n; Rk+=kratio*thresh1d) {
    int Rkmax2 = Rk + kratio * thresh1d; 
    if (Rkmax2 > in_n) {
        Rkmax2 = in_n; 
    }

    F* R = Rglobal.get();
    R += omp_get_thread_num()*thresh1d*thresh1d*kratio*kratio;
    for (Py_ssize_t Cjj = Cj; Cjj < Cjmax2; Cjj++) {
        {
            Int jj = cols[Cjj];
                //TODO: this could use some pointer logic for the R assignment?
                for (Py_ssize_t Rkk=Rk; Rkk<Rkmax2; Rkk++) {
                    Int kk = rows[Rkk];
                    R[(Cjj-Cj) * kratio * thresh1d + (Rkk-Rk)] = d[kk] * X[(Py_ssize_t) jj * n + kk];
                }
        }
    }

        for (Py_ssize_t Ci = Cj; Ci < out_m; Ci+=thresh1d) {
        Py_ssize_t Cimax2 = Ci + thresh1d; 
        if (Cimax2 > out_m) {
            Cimax2 = out_m; 
        }
        F* L = &Lglobal.get()[omp_get_thread_num()*thresh1d*thresh1d*kratio];
        for (Py_ssize_t Cii = Ci; Cii < Cimax2; Cii++) {
            Int ii = cols[Cii];
                for (Py_ssize_t Rkk=Rk; Rkk<Rkmax2; Rkk++) {
                    Int kk = rows[Rkk];
                    L[(Py_ssize_t) (Cii-Ci) * kratio * thresh1d + (Rkk-Rk)] = X[(Py_ssize_t) ii * n + kk];
                }
        }
        dense_baseTrue(R, L, d, out, out_m, Ci, Cimax2, Cj, Cjmax2, Rk, Rkmax2, innerblock, kratio*thresh1d);
    }
}

        } else {
            
    for (Py_ssize_t Rk = 0; Rk < in_n; Rk+=kratio*thresh1d) {
    int Rkmax2 = Rk + kratio * thresh1d; 
    if (Rkmax2 > in_n) {
        Rkmax2 = in_n; 
    }

    F* R = Rglobal.get();
    #pragma omp parallel for
    for (Py_ssize_t Cjj = Cj; Cjj < Cjmax2; Cjj++) {
        {
            Int jj = cols[Cjj];
                //TODO: this could use some pointer logic for the R assignment?
                for (Py_ssize_t Rkk=Rk; Rkk<Rkmax2; Rkk++) {
                    Int kk = rows[Rkk];
                    R[(Cjj-Cj) * kratio * thresh1d + (Rkk-Rk)] = d[kk] * X[(Py_ssize_t) jj * n + kk];
                }
        }
    }

        #pragma omp parallel for
        for (Py_ssize_t Ci = Cj; Ci < out_m; Ci+=thresh1d) {
        Py_ssize_t Cimax2 = Ci + thresh1d; 
        if (Cimax2 > out_m) {
            Cimax2 = out_m; 
        }
        F* L = &Lglobal.get()[omp_get_thread_num()*thresh1d*thresh1d*kratio];
        for (Py_ssize_t Cii = Ci; Cii < Cimax2; Cii++) {
            Int ii = cols[Cii];
                for (Py_ssize_t Rkk=Rk; Rkk<Rkmax2; Rkk++) {
                    Int kk = rows[Rkk];
                    L[(Py_ssize_t) (Cii-Ci) * kratio * thresh1d + (Rkk-Rk)] = X[(Py_ssize_t) ii * n + kk];
                }
        }
        dense_baseFalse(R, L, d, out, out_m, Ci, Cimax2, Cj, Cjmax2, Rk, Rkmax2, innerblock, kratio*thresh1d);
    }
}

        }
    }

    #pragma omp parallel for if(out_m > 100)
    for (Py_ssize_t Ci = 0; Ci < out_m; Ci++) {
        for (Py_ssize_t Cj = 0; Cj <= Ci; Cj++) {
            out[Cj * out_m + Ci] = out[Ci * out_m + Cj];
        }
    }
}





template <typename Int, typename F>
void _denseC_rmatvec(Int* rows, Int* cols, F* X, F* v, F* out,
        Int n_rows, Int n_cols, Int m, Int n) 
{
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
    constexpr std::size_t simd_size = 1;
#else
    constexpr std::size_t simd_size = xsimd::simd_type<F>::size;
#endif
    constexpr std::size_t alignment = simd_size * sizeof(F);

    auto outglobal = make_aligned_unique<F>(omp_get_max_threads()*n_cols, alignment);

    constexpr int rowblocksize = 256;
    constexpr int colblocksize = 4;

    #pragma omp parallel for
    for (Py_ssize_t Ci = 0; Ci < n_rows; Ci += rowblocksize) {
        Py_ssize_t Cimax = Ci + rowblocksize;
        if (Cimax > n_rows) {
            Cimax = n_rows;
        }

        F* outlocal = &outglobal.get()[omp_get_thread_num()*n_cols];

        for (Py_ssize_t Cj = 0; Cj < n_cols; Cj += colblocksize) {
            Py_ssize_t Cjmax = Cj + colblocksize;
            if (Cjmax > n_cols) {
                Cjmax = n_cols;
            }

                for (Py_ssize_t Cjj = Cj; Cjj < Cjmax; Cjj++) {
                    outlocal[Cjj] = 0.0;
                }
                for (Py_ssize_t Cii = Ci; Cii < Cimax; Cii++) {
                    Int i = rows[Cii];
                    F vv = v[i];
                    for (Py_ssize_t Cjj = Cj; Cjj < Cjmax; Cjj++) {
                        Int j = cols[Cjj];
                        F Xv = X[(Py_ssize_t) i * m + j];
                        outlocal[Cjj] += Xv * vv;
                    }
                }
        }

        for (Py_ssize_t Cj = 0; Cj < n_cols; Cj++) {
            #pragma omp atomic
            out[Cj] += outlocal[Cj];
        }
    }
}


template <typename Int, typename F>
void _denseF_rmatvec(Int* rows, Int* cols, F* X, F* v, F* out,
        Int n_rows, Int n_cols, Int m, Int n) 
{
#ifdef XSIMD_NO_SUPPORTED_ARCHITECTURE
    constexpr std::size_t simd_size = 1;
#else
    constexpr std::size_t simd_size = xsimd::simd_type<F>::size;
#endif
    constexpr std::size_t alignment = simd_size * sizeof(F);

    auto outglobal = make_aligned_unique<F>(omp_get_max_threads()*n_cols, alignment);

    constexpr int rowblocksize = 256;
    constexpr int colblocksize = 4;

    #pragma omp parallel for
    for (Py_ssize_t Ci = 0; Ci < n_rows; Ci += rowblocksize) {
        Py_ssize_t Cimax = Ci + rowblocksize;
        if (Cimax > n_rows) {
            Cimax = n_rows;
        }

        F* outlocal = &outglobal.get()[omp_get_thread_num()*n_cols];

        for (Py_ssize_t Cj = 0; Cj < n_cols; Cj += colblocksize) {
            Py_ssize_t Cjmax = Cj + colblocksize;
            if (Cjmax > n_cols) {
                Cjmax = n_cols;
            }

                for (Py_ssize_t Cjj = Cj; Cjj < Cjmax; Cjj++) {
                    Int j = cols[Cjj];
                    F out_entry = 0.0;
                    for (Py_ssize_t Cii = Ci; Cii < Cimax; Cii++) {
                        Int i = rows[Cii];
                        F Xv = X[(Py_ssize_t) j * n + i];
                        F vv = v[i];
                        out_entry += Xv * vv;
                    }

                    outlocal[Cjj] = out_entry;
                }
        }

        for (Py_ssize_t Cj = 0; Cj < n_cols; Cj++) {
            #pragma omp atomic
            out[Cj] += outlocal[Cj];
        }
    }
}




template <typename Int, typename F>
void _denseC_matvec(Int* rows, Int* cols, F* X, F* v, F* out,
        Int n_rows, Int n_cols, Int m, Int n) 
{
    constexpr int rowblocksize = 256;

    #pragma omp parallel for
    for (Py_ssize_t Ci = 0; Ci < n_rows; Ci += rowblocksize) {
        Int Cimax = Ci + rowblocksize;
        if (Cimax > n_rows) {
            Cimax = n_rows;
        }
        for (Py_ssize_t Cii = Ci; Cii < Cimax; Cii++) {
            F out_entry = 0.0;
            Int i = rows[Cii];
            for (Py_ssize_t Cjj = 0; Cjj < n_cols; Cjj++) {
                Int j = cols[Cjj];
                F vv = v[j];
                    F Xv = X[(Py_ssize_t) i * m + j];
                out_entry += Xv * vv;
            }
            out[Cii] = out_entry;
        }
    }
}


template <typename Int, typename F>
void _denseF_matvec(Int* rows, Int* cols, F* X, F* v, F* out,
        Int n_rows, Int n_cols, Int m, Int n) 
{
    constexpr int rowblocksize = 256;

    #pragma omp parallel for
    for (Py_ssize_t Ci = 0; Ci < n_rows; Ci += rowblocksize) {
        Int Cimax = Ci + rowblocksize;
        if (Cimax > n_rows) {
            Cimax = n_rows;
        }
        for (Py_ssize_t Cii = Ci; Cii < Cimax; Cii++) {
            F out_entry = 0.0;
            Int i = rows[Cii];
            for (Py_ssize_t Cjj = 0; Cjj < n_cols; Cjj++) {
                Int j = cols[Cjj];
                F vv = v[j];
                    F Xv = X[(Py_ssize_t) j * n + i];
                out_entry += Xv * vv;
            }
            out[Cii] = out_entry;
        }
    }
}

