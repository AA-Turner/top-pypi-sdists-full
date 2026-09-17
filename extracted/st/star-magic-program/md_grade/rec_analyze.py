"""rec_analyze.py - analysis of a front4_record.py output (rec_<tag>.npz or the checkpoint).
eta(k) = rho / (k^2 int_0^tmax C_T(k,t)/C_T(k,0) dt) per k-SHELL (all vectors and both transverse
components averaged), on the ATOMIC current (A) and the CENTRE-OF-MASS current (C); errors from the
run's blocks; Gaussian and Lorentzian fits of eta(k)/eta_0 -> measured k_c; shear-wave onset k_T
(first shell whose normalized C_T(k,t) dips below -0.02); D from the multi-origin COM MSD.
usage: python rec_analyze.py rec_<tag>.npz [tmax_ps=8]"""
import sys, json, math, numpy as np
from scipy.optimize import curve_fit
f = np.load(sys.argv[1]); tmax = float(sys.argv[2]) if len(sys.argv) > 2 else 8.0
lags = f['lags']; dts = float(f['dts']); t = lags * dts; L = float(f['L']); N = int(f['N']); n2 = f['n2']; kvec = f['kvec']
nacc = f['nacc']; nb = nacc.shape[0]; T = float(f['Tacc'].mean()) if len(f['Tacc']) else float(f['T'])
rho = N * 18.0154 / L ** 3; CONV = 1.66053907e-3
sel = t <= tmax
def shell_eta(C):
    """C: (nb, K, 2, nlag) raw sums. Returns per-shell dict."""
    out = []
    for s in sorted(set(n2.tolist())):
        idx = np.where(n2 == s)[0]; k = math.sqrt(s) * 2 * math.pi / L
        cb = []; etab = []
        for b in range(nb):
            c = C[b][idx].sum((0, 1)).real / np.maximum(nacc[b], 1)     # shell-summed over vectors & comps
            c = c / c[0]; cb.append(c)
            integ = np.trapezoid(c[sel], t[sel]); etab.append(rho / (k * k * integ) * CONV if integ > 0 else np.nan)
        call = (C[:, idx].sum((0, 1, 2)).real / np.maximum(nacc.sum(0), 1)); c0 = call[0]; call = call / c0
        integ = np.trapezoid(call[sel], t[sel]); eta = rho / (k * k * integ) * CONV if integ > 0 else np.nan
        etab = np.array(etab); err = np.nanstd(etab) / math.sqrt(np.isfinite(etab).sum()) if np.isfinite(etab).sum() > 1 else np.nan
        cmin = call[sel].min(); imin = np.argmin(call[sel]); tmin = t[sel][imin]
        cb = np.array(cb); csig = float(cb[:, sel][:, imin].std() / math.sqrt(nb)) if nb > 1 else np.nan   # block error of C at its minimum
        out.append(dict(n2=int(s), k=k, nvec=len(idx), eta=eta, err=err, C0=c0 / (2 * len(idx)), cmin=float(cmin), cmin_sig=csig, tmin=float(tmin), c=call[sel].tolist(), tau_e=float(np.interp(1 / math.e, call[sel][::-1], t[sel][::-1])) if call[sel].min() < 1 / math.e else np.nan))
    return out
def fits(rows, label):
    ks = np.array([r['k'] for r in rows]); e = np.array([r['eta'] for r in rows]); ee = np.array([r['err'] for r in rows])
    m = np.isfinite(e) & (e > 0); w = np.where(np.isfinite(ee) & (ee > 0), ee, np.nanmedian(ee[m]) if np.isfinite(ee[m]).any() else 1.0)
    gauss = lambda k, e0, b: e0 * np.exp(-b * k * k); lor = lambda k, e0, c: e0 / (1 + c * k * k)
    res = {}
    try:
        (e0g, b), cg = curve_fit(gauss, ks[m], e[m], p0=[e[m][0], 0.005], sigma=w[m], absolute_sigma=True, maxfev=20000)
        (e0l, cc), cl = curve_fit(lor, ks[m], e[m], p0=[e[m][0], 0.01], sigma=w[m], absolute_sigma=True, maxfev=20000)
        chi_g = float(np.sum(((gauss(ks[m], e0g, b) - e[m]) / w[m]) ** 2)); chi_l = float(np.sum(((lor(ks[m], e0l, cc) - e[m]) / w[m]) ** 2))
        res = dict(eta0_gauss=e0g, b=b, b_err=float(np.sqrt(cg[1, 1])), kc_measured=math.sqrt(0.343653 / b), kc_err=0.5 * math.sqrt(0.343653 / b) * math.sqrt(cg[1, 1]) / b,
                   k_1e=1 / math.sqrt(b), chi2_gauss=chi_g, eta0_lor=e0l, c=cc, chi2_lor=chi_l, ndata=int(m.sum()), better='gaussian' if chi_g < chi_l else 'lorentzian')
        print('[%s] Gaussian: eta0 %.4f, b %.5f +- %.5f nm^2 -> k_c %.2f +- %.2f (1/e at %.2f), chi2 %.1f | Lorentzian: eta0 %.4f, c %.5f, chi2 %.1f -> %s (n=%d)' %
              (label, e0g, b, res['b_err'], res['kc_measured'], res['kc_err'], res['k_1e'], chi_g, e0l, cc, chi_l, res['better'], m.sum()))
    except Exception as ex:
        print(label, 'fit failed', ex)
    return res
out = dict(N=N, L=L, T=T, k_min=2 * math.pi / L, samples=int(nacc.sum(0)[0]), t_ps=float(nacc.sum(0)[0] * dts), tmax=tmax, nblock=nb, seed=int(f['seed']) if 'seed' in f.files else None)
for key, label in (('CC', 'COM'), ('CA', 'atoms')):
    rows = shell_eta(f[key]); out[label] = dict(rows=[{k2: v for k2, v in r.items() if k2 != 'c'} for r in rows])
    print('\n== %s current ==  C(0)/(N kT M) shells: %s' % (label, ', '.join('%.3f' % (r['C0'] / (N * 18.0154 * 0.0083144626 * T)) for r in rows[:6]) if label == 'COM' else ''))
    for r in rows:
        print('n2=%3d k=%6.3f nvec=%2d  eta=%.4f +- %.4f mPa s   C_min %+.3f +- %.3f at %.3f ps  tau_1/e %.3f ps' % (r['n2'], r['k'], r['nvec'], r['eta'], r['err'], r['cmin'], r['cmin_sig'], r['tmin'], r['tau_e']))
    out[label]['fit'] = fits(rows, label)
    onset = [r['k'] for r in rows if r['cmin'] < -0.02 and r['cmin'] < -3 * r['cmin_sig']]
    out[label]['k_T_onset'] = min(onset) if onset else None
    print('shear-wave onset k_T (first shell with C_min < -0.02 and < -3 sigma): %s' % (('%.2f nm^-1' % min(onset)) if onset else 'none in range'))
# diffusion, multi-origin
ct = f['comtraj'].astype(np.float64); dtm = float(f['msd_every_ps']) if 'msd_every_ps' in f.files else 0.5
if ct.shape[0] > 20:
    nlag = ct.shape[0] // 4; msd = np.array([((ct[l:] - ct[:-l]) ** 2).sum(-1).mean() for l in range(1, nlag)]); tt = np.arange(1, nlag) * dtm
    s_ = (tt >= 5.0) & (tt <= min(40.0, tt[-1])); D = np.polyfit(tt[s_], msd[s_], 1)[0] / 6; out['D_cm2_s'] = D * 1e-2; out['D_fit_ps'] = [float(tt[s_][0]), float(tt[s_][-1])]
    print('\nD (multi-origin COM MSD, %d molecules, lags %.0f-%.0f ps of a %.0f ps trajectory) = %.2e cm^2/s (TIP4P/2005 298 K: 2.1-2.3e-5 uncorrected; finite-size adds ~kT/(6 pi eta L))' % (ct.shape[1], tt[s_][0], tt[s_][-1], ct.shape[0] * dtm, D * 1e-2))
print('T mean %.1f K   samples %d = %.1f ps   rho %.2f amu/nm^3' % (T, out['samples'], out['t_ps'], rho))
json.dump(out, open(sys.argv[1].replace('.npz', '_analysis.json'), 'w'), indent=1, default=float)
