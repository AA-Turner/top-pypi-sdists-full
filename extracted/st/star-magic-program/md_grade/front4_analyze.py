"""front4_analyze.py - TCAF -> eta(k) -> Gaussian/Lorentzian fits -> measured k_c.
usage: python front4_analyze.py f4_main.npz [tmax_ps]
"""
import sys, math, json, numpy as np
from scipy.optimize import least_squares, curve_fit

f = np.load(sys.argv[1]); tmax = float(sys.argv[2]) if len(sys.argv) > 2 else 8.0
J = f['J']; kvec = f['kvec']; n2 = f['n2']; L = float(f['L']); N = int(f['N']); dt = float(f['dt'])
nsamp = J.shape[0]; rho = N * 18.015 / L ** 3          # amu nm^-3
AMU_NM_PS_TO_MPAS = 1.66053907e-3
nlag = min(nsamp // 3, int(tmax / dt))
t = np.arange(nlag) * dt

def acf(x, nlag):
    n = len(x); m = 1 << (2 * n - 1).bit_length()
    X = np.fft.fft(x, m); c = np.fft.ifft(X * np.conj(X))[:nlag].real
    return c / (n - np.arange(nlag))

def gmx_form(t, tau, eta, k):
    v = -t / (2 * tau); W2 = 1 - 4 * tau * eta * k * k / rho
    if W2 >= 0:
        W = math.sqrt(W2); return np.exp(v) * (np.cosh(W * v) + np.sinh(W * v) / W)
    W = math.sqrt(-W2); return np.exp(v) * (np.cos(W * v) + np.sin(W * v) / W)

rows = []
for s in sorted(set(n2.tolist())):
    idx = np.where(n2 == s)[0]; k = math.sqrt(s) * 2 * math.pi / L
    c = np.zeros(nlag)
    for i in idx:
        for comp in (0, 1):
            c += acf(J[:, i, comp].astype(np.complex128), nlag)
    c /= c[0]
    # integral estimator (Green-Kubo generalized hydrodynamics): eta(k) = rho / (k^2 int_0^tmax C(t)/C(0) dt)
    integ = np.trapezoid(c, t)
    eta_int = rho / (k * k * integ) if integ > 0 else float('nan')
    # block errors: 4 blocks of the run
    nb = 4; blk = []
    bl = nsamp // nb; nl = min(bl // 3, nlag)
    for bi in range(nb):
        cb = np.zeros(nl)
        for i in idx:
            for comp in (0, 1):
                cb += acf(J[bi * bl:(bi + 1) * bl, i, comp].astype(np.complex128), nl)
        cb /= cb[0]; ib = np.trapezoid(cb, t[:nl])
        if ib > 0: blk.append(rho / (k * k * ib) * AMU_NM_PS_TO_MPAS)
    eta_int_err = float(np.std(blk) / math.sqrt(len(blk))) if len(blk) > 1 else float('nan')
    # gmx form fit
    def res(p): return gmx_form(t, p[0], p[1], k) - c
    best = None
    for tau0 in (0.05, 0.2, 1.0):
        for eta0 in (0.3 * rho, 0.9 * rho, 2.0 * rho):
            try:
                r = least_squares(res, [tau0, eta0], bounds=([1e-4, 1e-3], [50, 1e7]))
                if best is None or r.cost < best.cost: best = r
            except Exception: pass
    tau, eta_fit = best.x
    rows.append(dict(n2=s, k=k, nvec=len(idx), eta_fit=eta_fit * AMU_NM_PS_TO_MPAS, eta_int=eta_int * AMU_NM_PS_TO_MPAS,
                     tau=tau, chi=float(np.sqrt(np.mean(best.fun ** 2))), c1ps=float(np.interp(1.0, t, c)), eta_int_err=eta_int_err, c_at=c[:min(nlag, 60)].tolist()))
    print('n2=%2d k=%6.3f nvec=%2d  eta_int=%.4f +- %.4f  eta_fit=%.4f mPa s  tau=%.3f ps  C(1ps)=%.3f' % (s, k, len(idx), rows[-1]['eta_int'], eta_int_err, rows[-1]['eta_fit'], tau, rows[-1]['c1ps']))

ks = np.array([r['k'] for r in rows]); ef = np.array([r['eta_fit'] for r in rows]); ei = np.array([r['eta_int'] for r in rows])
w = np.sqrt(np.array([r['nvec'] for r in rows], float))
def gauss(k, e0, b): return e0 * np.exp(-b * k * k)
def lor(k, e0, c): return e0 / (1 + c * k * k)
out = {'N': N, 'L': L, 'k_min': ks.min(), 'nsamp': nsamp, 'dt': dt, 'T': float(f['T']), 'rows': [{k2: v for k2, v in r.items() if k2 != 'c_at'} for r in rows]}
ee = np.array([r['eta_int_err'] for r in rows])
for name, e in (('int', ei), ('fit', ef)):
    m = np.isfinite(e) & (e > 0)
    if name == 'int' and np.all(np.isfinite(ee[m])) and np.all(ee[m] > 0): w = 1.0 / ee
    else: w = np.sqrt(np.array([r['nvec'] for r in rows], float))
    try:
        (e0g, b), cg = curve_fit(gauss, ks[m], e[m], p0=[e[m][0], 0.01], sigma=1 / w[m], maxfev=20000)
        (e0l, cc), cl = curve_fit(lor, ks[m], e[m], p0=[e[m][0], 0.01], sigma=1 / w[m], maxfev=20000)
        rg = np.sqrt(np.mean((gauss(ks[m], e0g, b) - e[m]) ** 2)); rl = np.sqrt(np.mean((lor(ks[m], e0l, cc) - e[m]) ** 2))
        kc_meas = math.sqrt(0.3437 / b) if b > 0 else float('nan')
        out[name] = dict(eta0_gauss=e0g, b=b, kc_measured=kc_meas, k_1e=1 / math.sqrt(b) if b > 0 else None, rms_gauss=rg,
                         eta0_lor=e0l, c=cc, rms_lor=rl, better='gaussian' if rg < rl else 'lorentzian')
        print('\n[%s] Gaussian: eta0 %.4f mPa s, b %.5f nm^2 -> measured k_c %.2f nm^-1 (1/e at %.2f); rms %.4f' % (name, e0g, b, kc_meas, 1 / math.sqrt(b), rg))
        print('[%s] Lorentzian: eta0 %.4f, c %.5f; rms %.4f  ->  better: %s' % (name, e0l, cc, rl, out[name]['better']))
        print('    candidates: c_0 k_c 5.307 (b 0.0122) | c_inf k_c 2.454 (b 0.0570)')
    except Exception as ex:
        print(name, 'fit failed', ex)
# diffusion from COM MSD
mt = np.array(f['msd_t']); ms = np.array(f['msd'])
if len(mt) > 10:
    sl = np.polyfit(mt[len(mt) // 3:], ms[len(mt) // 3:], 1)[0]; D = sl / 6
    out['D_cm2_s'] = D * 1e-2
    print('\nD = %.2e cm^2/s (TIP4P/2005 ~2.1-2.3e-5; small-box finite-size lowers it)' % (D * 1e-2))
print('T = %.1f K' % out['T'])
json.dump(out, open(sys.argv[1].replace('.npz', '_analysis.json'), 'w'), indent=1)
