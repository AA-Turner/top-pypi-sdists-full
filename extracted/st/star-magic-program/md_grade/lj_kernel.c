/* lj_kernel.c - Lennard-Jones atomic fluid forces with a cell list (B288, the Q-251 argon test).
   Energy-shifted 12-6 at rc. pos,F: [N][3]. Returns potential energy; virial (sum r.F) in *W.
   Build: gcc -O3 -march=native -fopenmp -shared -fPIC -o lj_kernel.so lj_kernel.c -lm */
#include <math.h>
#include <stdlib.h>
#include <string.h>
#ifdef _OPENMP
#include <omp.h>
#endif
static inline double wrap(double d, double L) { return d - L * rint(d / L); }
double lj_forces(int N, const double *pos, double *F, double L, double rc, double sig, double eps, double *W)
{
    memset(F, 0, sizeof(double) * N * 3);
    double rc2 = rc * rc; int nc = (int)floor(L / rc); if (nc < 3) nc = 1; double cw = L / nc; int ncell = nc * nc * nc;
    int *head = malloc(sizeof(int) * ncell), *next = malloc(sizeof(int) * N);
    for (int c = 0; c < ncell; c++) head[c] = -1;
    for (int i = 0; i < N; i++) { const double *r = pos + i * 3;
        int cx = ((int)floor(r[0] / cw) % nc + nc) % nc, cy = ((int)floor(r[1] / cw) % nc + nc) % nc, cz = ((int)floor(r[2] / cw) % nc + nc) % nc;
        int c = (cx * nc + cy) * nc + cz; next[i] = head[c]; head[c] = i; }
    double sig2 = sig * sig, sig6 = sig2 * sig2 * sig2, rc6 = rc2 * rc2 * rc2, eshift = 4 * eps * (sig6 * sig6 / (rc6 * rc6) - sig6 / rc6);
    double E = 0, vir = 0; int brute = (nc == 1); int nthr = 1;
#ifdef _OPENMP
    nthr = omp_get_max_threads();
#endif
    double *Fb = calloc((size_t)nthr * N * 3, sizeof(double));
#pragma omp parallel reduction(+:E,vir)
    { int tid = 0;
#ifdef _OPENMP
      tid = omp_get_thread_num();
#endif
      double *Ft = Fb + (size_t)tid * N * 3;
#pragma omp for schedule(dynamic, 4)
      for (int c = 0; c < ncell; c++) { int cx = c / (nc * nc), cy = (c / nc) % nc, cz = c % nc;
        for (int dx = -1; dx <= 1; dx++) for (int dy = -1; dy <= 1; dy++) for (int dz = -1; dz <= 1; dz++) {
          if (brute) { if (dx || dy || dz) continue; } else if (dx < 0 || (dx == 0 && dy < 0) || (dx == 0 && dy == 0 && dz < 0)) continue;
          int c2 = (((cx + dx + nc) % nc) * nc + (cy + dy + nc) % nc) * nc + (cz + dz + nc) % nc; int same = (c2 == c);
          for (int i = head[c]; i >= 0; i = next[i]) { const double *ri = pos + i * 3; double *fi = Ft + i * 3;
            for (int j = (same ? next[i] : head[c2]); j >= 0; j = next[j]) { const double *rj = pos + j * 3;
              double d[3] = { wrap(ri[0] - rj[0], L), wrap(ri[1] - rj[1], L), wrap(ri[2] - rj[2], L) };
              double r2 = d[0] * d[0] + d[1] * d[1] + d[2] * d[2]; if (r2 >= rc2) continue;
              double inv2 = sig2 / r2, inv6 = inv2 * inv2 * inv2, fl = 24 * eps * (2 * inv6 * inv6 - inv6) / r2;
              E += 4 * eps * (inv6 * inv6 - inv6) - eshift; vir += fl * r2;
              double *fj = Ft + j * 3; for (int k = 0; k < 3; k++) { fi[k] += fl * d[k]; fj[k] -= fl * d[k]; } } } } } }
    for (int t = 0; t < nthr; t++) { double *Ft = Fb + (size_t)t * N * 3; for (size_t k = 0; k < (size_t)N * 3; k++) F[k] += Ft[k]; }
    free(Fb); free(head); free(next); *W = vir; return E;
}
