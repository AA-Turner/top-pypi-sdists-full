/* pair_kernel.c - C kernels for the front-4 RECORD RUN (rigid TIP4P/2005 water, SPME).
   1. pair_forces: real-space LJ (O-O, energy-shifted) + erfc Coulomb (site cutoff r<rc on every charge pair of
      different molecules; molecule cell list on O with prelist O-O < rc+skin) + intramolecular exclusion
      correction for the reciprocal sum. erfc(ar)/r and its force factor are tabulated (linear interpolation,
      dr = 2e-5 nm; max relative error checked in validate.py) - the table is rebuilt when (alpha, rc) change.
   2. rattle_positions / rattle_velocities: SHAKE/RATTLE per molecule (3 distance constraints).
   3. pme_spread / pme_gather: order-4 cardinal B-spline charge spreading and force gathering (Essmann 1995).
   OpenMP on the pair loop when compiled with -fopenmp (OMP_NUM_THREADS).
   Units: nm, kJ/mol, e, amu, ps.  Build: gcc -O3 -march=native -fopenmp -shared -fPIC -o pair_kernel.so pair_kernel.c -lm */
#include <math.h>
#include <stdlib.h>
#include <string.h>
#ifdef _OPENMP
#include <omp.h>
#endif

static inline double wrap(double d, double L) { return d - L * rint(d / L); }

/* ---------------- erfc table ---------------- */
static double *tab_f = 0, *tab_g = 0; static double tab_dr = 2e-5, tab_alpha = -1, tab_rc = -1; static int tab_n = 0;
static void build_table(double alpha, double rc) {
    if (tab_f && tab_alpha == alpha && tab_rc == rc) return;
    free(tab_f); free(tab_g);
    tab_n = (int)(rc / tab_dr) + 3; tab_f = malloc(sizeof(double) * tab_n); tab_g = malloc(sizeof(double) * tab_n);
    double two_a_pi = 2.0 * alpha / sqrt(M_PI);
    for (int i = 0; i < tab_n; i++) {
        double r = i * tab_dr; if (r < 1e-6) r = 1e-6;   /* node i at r = i*dr; r=0 never queried (i>=1 for any physical pair) */
        double ar = alpha * r, ec = erfc(ar);
        tab_f[i] = ec / r;                                         /* energy factor: qq * f */
        tab_g[i] = (ec / r + two_a_pi * exp(-ar * ar)) / (r * r);  /* force factor: F = qq * g * dv */
    }
    tab_alpha = alpha; tab_rc = rc;
}
static inline void tab_lookup(double r, double *f, double *g) {
    double x = r / tab_dr; int i = (int)x; double t = x - i;
    *f = tab_f[i] + t * (tab_f[i + 1] - tab_f[i]);
    *g = tab_g[i] + t * (tab_g[i + 1] - tab_g[i]);
}
double table_check(double alpha, double rc, double rmin) {
    /* max relative error of the tabulated force factor vs exact, for r in [rmin, rc] */
    build_table(alpha, rc); double worst = 0, two_a_pi = 2.0 * alpha / sqrt(M_PI);
    for (double r = rmin; r < rc; r += 1.7e-5) {
        double f, g; tab_lookup(r, &f, &g); double ar = alpha * r, ec = erfc(ar);
        double ge = (ec / r + two_a_pi * exp(-ar * ar)) / (r * r), fe = ec / r;
        double e1 = fabs(g - ge) / ge, e2 = fabs(f - fe) / fe; if (e1 > worst) worst = e1; if (e2 > worst) worst = e2;
    }
    return worst;
}

/* ---------------- pair forces ---------------- */
/* pos: [N][4][3] (O,H1,H2,M); F: [N][4][3] zeroed here; returns total real-space energy. */
double pair_forces(int N, const double *pos, double *F, double L, double rc, double skin,
                   double alpha, double fcoul, const double *q, double sig, double eps,
                   double *E_lj_out, double *E_real_out, double *E_excl_out)
{
    build_table(alpha, rc);
    memset(F, 0, sizeof(double) * N * 12);
    double rl = rc + skin, rl2 = rl * rl, rc2 = rc * rc;
    int nc = (int)floor(L / rl); if (nc < 3) nc = 1;
    double cw = L / nc; int ncell = nc * nc * nc;
    int *head = malloc(sizeof(int) * ncell), *next = malloc(sizeof(int) * N);
    for (int c = 0; c < ncell; c++) head[c] = -1;
    for (int i = 0; i < N; i++) {
        const double *o = pos + i * 12;
        int cx = ((int)floor(o[0] / cw) % nc + nc) % nc, cy = ((int)floor(o[1] / cw) % nc + nc) % nc, cz = ((int)floor(o[2] / cw) % nc + nc) % nc;
        int c = (cx * nc + cy) * nc + cz; next[i] = head[c]; head[c] = i;
    }
    double sig2 = sig * sig, sig6 = sig2 * sig2 * sig2, sig12 = sig6 * sig6;
    double rc6 = rc2 * rc2 * rc2, eshift = 4 * eps * (sig12 / (rc6 * rc6) - sig6 / rc6);
    double E_lj = 0, E_real = 0, E_excl = 0;
    int brute = (nc == 1);
    int nthr = 1;
#ifdef _OPENMP
    nthr = omp_get_max_threads();
#endif
    double *Fb = calloc((size_t)nthr * N * 12, sizeof(double));
#pragma omp parallel reduction(+:E_lj,E_real)
    {
        int tid = 0;
#ifdef _OPENMP
        tid = omp_get_thread_num();
#endif
        double *Ft = Fb + (size_t)tid * N * 12;
#pragma omp for schedule(dynamic, 4)
        for (int c = 0; c < ncell; c++) {
            int cx = c / (nc * nc), cy = (c / nc) % nc, cz = c % nc;
            for (int dx = -1; dx <= 1; dx++) for (int dy = -1; dy <= 1; dy++) for (int dz = -1; dz <= 1; dz++) {
                if (brute) { if (dx || dy || dz) continue; }
                else if (dx < 0 || (dx == 0 && dy < 0) || (dx == 0 && dy == 0 && dz < 0)) continue;
                int c2 = (((cx + dx + nc) % nc) * nc + (cy + dy + nc) % nc) * nc + (cz + dz + nc) % nc;
                int same = (c2 == c);
                for (int i = head[c]; i >= 0; i = next[i]) {
                    const double *pi = pos + i * 12; double *fi = Ft + i * 12;
                    for (int j = (same ? next[i] : head[c2]); j >= 0; j = next[j]) {
                        const double *pj = pos + j * 12; double *fj = Ft + j * 12;
                        double dO[3] = { wrap(pi[0] - pj[0], L), wrap(pi[1] - pj[1], L), wrap(pi[2] - pj[2], L) };
                        double r2 = dO[0] * dO[0] + dO[1] * dO[1] + dO[2] * dO[2];
                        if (r2 >= rl2) continue;
                        double sh[3] = { dO[0] - (pi[0] - pj[0]), dO[1] - (pi[1] - pj[1]), dO[2] - (pi[2] - pj[2]) };
                        if (r2 < rc2) {
                            double inv2 = sig2 / r2, inv6 = inv2 * inv2 * inv2;
                            double fl = 24 * eps * (2 * inv6 * inv6 - inv6) / r2;
                            E_lj += 4 * eps * (inv6 * inv6 - inv6) - eshift;
                            for (int d = 0; d < 3; d++) { fi[d] += fl * dO[d]; fj[d] -= fl * dO[d]; }
                        }
                        for (int a = 1; a < 4; a++) for (int b = 1; b < 4; b++) {
                            double dv[3] = { pi[a * 3] - pj[b * 3] + sh[0], pi[a * 3 + 1] - pj[b * 3 + 1] + sh[1], pi[a * 3 + 2] - pj[b * 3 + 2] + sh[2] };
                            double s2 = dv[0] * dv[0] + dv[1] * dv[1] + dv[2] * dv[2];
                            if (s2 >= rc2) continue;
                            double r = sqrt(s2), qq = fcoul * q[a] * q[b], f, g;
                            tab_lookup(r, &f, &g);
                            E_real += qq * f; double fs = qq * g;
                            for (int d = 0; d < 3; d++) { fi[a * 3 + d] += fs * dv[d]; fj[b * 3 + d] -= fs * dv[d]; }
                        }
                    }
                }
            }
        }
    }
    for (int t = 0; t < nthr; t++) { double *Ft = Fb + (size_t)t * N * 12; for (size_t k = 0; k < (size_t)N * 12; k++) F[k] += Ft[k]; }
    free(Fb);
    /* intramolecular exclusion correction: pairs (1,2),(1,3),(2,3) - exact erf */
    double two_a_pi = 2.0 * alpha / sqrt(M_PI);
    for (int i = 0; i < N; i++) {
        const double *pi = pos + i * 12; double *fi = F + i * 12;
        for (int a = 1; a < 4; a++) for (int b = a + 1; b < 4; b++) {
            double dv[3] = { pi[a * 3] - pi[b * 3], pi[a * 3 + 1] - pi[b * 3 + 1], pi[a * 3 + 2] - pi[b * 3 + 2] };
            double s2 = dv[0] * dv[0] + dv[1] * dv[1] + dv[2] * dv[2], r = sqrt(s2);
            double qq = fcoul * q[a] * q[b], ar = alpha * r, ef = erf(ar);
            E_excl -= qq * ef / r;
            double fs = qq * (two_a_pi * exp(-ar * ar) / r - ef / s2) / r;
            for (int d = 0; d < 3; d++) { fi[a * 3 + d] += fs * dv[d]; fi[b * 3 + d] -= fs * dv[d]; }
        }
    }
    free(head); free(next);
    *E_lj_out = E_lj; *E_real_out = E_real; *E_excl_out = E_excl;
    return E_lj + E_real + E_excl;
}

/* ---------------- RATTLE ---------------- */
/* pos,ref,vel: [N][3][3]; mass[3]; pairs (0,1,d01),(0,2,d02),(1,2,d12) given as d0[3] in that order.
   If ref != NULL: RATTLE stage 1 (constraint directions from ref, velocity corrected by corr/dt). Returns iterations. */
int rattle_positions(int N, double *pos, const double *ref, double *vel, const double *mass, const double *d0, double dt, double tol, int maxit)
{
    const int I[3] = {0, 0, 1}, J[3] = {1, 2, 2};
    int worst_it = 0;
#pragma omp parallel for reduction(max:worst_it)
    for (int n = 0; n < N; n++) {
        double *p = pos + n * 9; const double *rf = ref ? ref + n * 9 : 0; double *v = vel ? vel + n * 9 : 0;
        int it;
        for (it = 0; it < maxit; it++) {
            double maxdev = 0;
            for (int c = 0; c < 3; c++) {
                int i = I[c], j = J[c]; double rij[3], d2 = 0, dev, g, dot = 0, r0[3];
                for (int d = 0; d < 3; d++) { rij[d] = p[i * 3 + d] - p[j * 3 + d]; d2 += rij[d] * rij[d]; }
                dev = d0[c] * d0[c] - d2; if (fabs(dev) > maxdev) maxdev = fabs(dev);
                double im = 1.0 / mass[i] + 1.0 / mass[j];
                if (!rf) { g = dev / (2 * im * d2); for (int d = 0; d < 3; d++) r0[d] = rij[d]; }
                else { for (int d = 0; d < 3; d++) { r0[d] = rf[i * 3 + d] - rf[j * 3 + d]; dot += r0[d] * rij[d]; } g = dev / (2 * im * dot); }
                for (int d = 0; d < 3; d++) {
                    double corr = g * r0[d];
                    p[i * 3 + d] += corr / mass[i]; p[j * 3 + d] -= corr / mass[j];
                    if (rf && v) { v[i * 3 + d] += corr / mass[i] / dt; v[j * 3 + d] -= corr / mass[j] / dt; }
                }
            }
            if (maxdev < tol) break;
        }
        if (it > worst_it) worst_it = it;
    }
    return worst_it;
}

int rattle_velocities(int N, const double *pos, double *vel, const double *mass, const double *d0, double tol, int maxit)
{
    const int I[3] = {0, 0, 1}, J[3] = {1, 2, 2};
    int worst_it = 0;
#pragma omp parallel for reduction(max:worst_it)
    for (int n = 0; n < N; n++) {
        const double *p = pos + n * 9; double *v = vel + n * 9; int it;
        for (it = 0; it < maxit; it++) {
            double maxv = 0;
            for (int c = 0; c < 3; c++) {
                int i = I[c], j = J[c]; double rij[3], vij[3], dot = 0;
                for (int d = 0; d < 3; d++) { rij[d] = p[i * 3 + d] - p[j * 3 + d]; vij[d] = v[i * 3 + d] - v[j * 3 + d]; dot += rij[d] * vij[d]; }
                double k = dot / (d0[c] * d0[c] * (1.0 / mass[i] + 1.0 / mass[j])); if (fabs(k) > maxv) maxv = fabs(k);
                for (int d = 0; d < 3; d++) { v[i * 3 + d] -= k / mass[i] * rij[d]; v[j * 3 + d] += k / mass[j] * rij[d]; }
            }
            if (maxv < tol) break;
        }
        if (it > worst_it) worst_it = it;
    }
    return worst_it;
}

/* ---------------- SPME order-4 spreading / gathering ---------------- */
static inline void m4(double u, double *M, double *dM) {
    /* weights for grid points floor(u)-j, j=0..3: x = u - (floor(u)-j) = frac + j, in (0,4) */
    double x = u - floor(u);
    double x0 = x, x1 = x + 1, x2 = x + 2, x3 = x + 3;
    M[0] = x0 * x0 * x0 / 6.0;
    M[1] = (-3 * x1 * x1 * x1 + 12 * x1 * x1 - 12 * x1 + 4) / 6.0;
    M[2] = (3 * x2 * x2 * x2 - 24 * x2 * x2 + 60 * x2 - 44) / 6.0;
    M[3] = (4 - x3) * (4 - x3) * (4 - x3) / 6.0;
    /* dM4/dx = M3(x) - M3(x-1); M3(x): 0<x<1: x^2/2; 1<x<2: (-2x^2+6x-3)/2; 2<x<3: (3-x)^2/2 */
    #define M3(y) (((y) <= 0 || (y) >= 3) ? 0.0 : ((y) < 1 ? (y)*(y)/2 : ((y) < 2 ? (-2*(y)*(y)+6*(y)-3)/2 : (3-(y))*(3-(y))/2)))
    dM[0] = M3(x0) - M3(x0 - 1); dM[1] = M3(x1) - M3(x1 - 1); dM[2] = M3(x2) - M3(x2 - 1); dM[3] = M3(x3) - M3(x3 - 1);
}
void pme_spread(int Nq, const double *r, const double *q, double L, int K, double *Q)
{
    memset(Q, 0, sizeof(double) * (size_t)K * K * K);
    for (int n = 0; n < Nq; n++) {
        double Mx[4], My[4], Mz[4], dm[4]; int ix[4], iy[4], iz[4];
        for (int d = 0; d < 3; d++) {
            double u = r[n * 3 + d] / L * K; u -= K * floor(u / K); int m0 = (int)floor(u);
            double *M = d == 0 ? Mx : (d == 1 ? My : Mz); int *ii = d == 0 ? ix : (d == 1 ? iy : iz);
            m4(u, M, dm); for (int j = 0; j < 4; j++) ii[j] = ((m0 - j) % K + K) % K;
        }
        for (int a = 0; a < 4; a++) for (int b = 0; b < 4; b++) { double w = q[n] * Mx[a] * My[b]; size_t base = ((size_t)ix[a] * K + iy[b]) * K;
            for (int c = 0; c < 4; c++) Q[base + iz[c]] += w * Mz[c]; }
    }
}
void pme_gather(int Nq, const double *r, const double *q, double L, int K, const double *phi, double *F)
{
    double s = K / L;
    for (int n = 0; n < Nq; n++) {
        double Mx[4], My[4], Mz[4], dMx[4], dMy[4], dMz[4]; int ix[4], iy[4], iz[4];
        for (int d = 0; d < 3; d++) {
            double u = r[n * 3 + d] / L * K; u -= K * floor(u / K); int m0 = (int)floor(u);
            double *M = d == 0 ? Mx : (d == 1 ? My : Mz), *dM = d == 0 ? dMx : (d == 1 ? dMy : dMz); int *ii = d == 0 ? ix : (d == 1 ? iy : iz);
            m4(u, M, dM); for (int j = 0; j < 4; j++) ii[j] = ((m0 - j) % K + K) % K;
        }
        double gx = 0, gy = 0, gz = 0;
        for (int a = 0; a < 4; a++) for (int b = 0; b < 4; b++) { size_t base = ((size_t)ix[a] * K + iy[b]) * K;
            for (int c = 0; c < 4; c++) { double p = phi[base + iz[c]];
                gx += dMx[a] * My[b] * Mz[c] * p; gy += Mx[a] * dMy[b] * Mz[c] * p; gz += Mx[a] * My[b] * dMz[c] * p; } }
        F[n * 3] = -q[n] * s * gx; F[n * 3 + 1] = -q[n] * s * gy; F[n * 3 + 2] = -q[n] * s * gz;
    }
}

/* ---------------- transverse currents j_T(k) = sum_i m_i (v_i . e) exp(i k.r_i) ---------------- */
/* r,v: [Na][3]; m: [Na]; kvec,e1,e2: [K][3]; J: [K][2][2] (re,im for e1 then e2). */
void currents(int Na, const double *r, const double *v, const double *m, int K, const double *kvec, const double *e1, const double *e2, double *J)
{
#pragma omp parallel for schedule(static)
    for (int k = 0; k < K; k++) {
        const double *kk = kvec + k * 3, *a = e1 + k * 3, *b = e2 + k * 3;
        double s1r = 0, s1i = 0, s2r = 0, s2i = 0;
        for (int i = 0; i < Na; i++) {
            const double *ri = r + i * 3, *vi = v + i * 3;
            double ph = kk[0] * ri[0] + kk[1] * ri[1] + kk[2] * ri[2];
            double c = cos(ph), s = sin(ph);
            double w1 = m[i] * (a[0] * vi[0] + a[1] * vi[1] + a[2] * vi[2]);
            double w2 = m[i] * (b[0] * vi[0] + b[1] * vi[1] + b[2] * vi[2]);
            s1r += w1 * c; s1i += w1 * s; s2r += w2 * c; s2i += w2 * s;
        }
        J[k * 4] = s1r; J[k * 4 + 1] = s1i; J[k * 4 + 2] = s2r; J[k * 4 + 3] = s2i;
    }
}
