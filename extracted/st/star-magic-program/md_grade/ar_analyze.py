"""ar_analyze.py - analysis of argon_record.py output: eta(k) per shell (Green-Kubo, blocks), Gaussian/Lorentzian fits,
measured k_c; longitudinal dispersion omega(k) from C_L(k,omega) peaks -> the model's own c_0 at low k; D from MSD; eta_0.
usage: python ar_analyze.py ar_<tag>.npz [tmax_ps=10]"""
import sys, json, math, numpy as np
from scipy.optimize import curve_fit
f = np.load(sys.argv[1]); tmax = float(sys.argv[2]) if len(sys.argv) > 2 else 10.0
lags = f['lags']; dts = float(f['dts']); t = lags * dts; L = float(f['L']); N = int(f['N']); n2 = f['n2']; nacc = f['nacc']; nb = nacc.shape[0]
M = float(f['mass']); T = float(f['Tacc'].mean()); rho = N * M / L ** 3; CONV = 1.66053907e-3; sel = t <= tmax
CT = f['CT']; CL = f['CL']
rows = []
for s in sorted(set(n2.tolist())):
    idx = np.where(n2 == s)[0]; k = math.sqrt(s) * 2 * math.pi / L
    etab = []
    for b in range(nb):
        c = CT[b][idx].sum((0, 1)).real / np.maximum(nacc[b], 1); c = c / c[0]; ib = np.trapezoid(c[sel], t[sel]); etab.append(rho / (k * k * ib) * CONV if ib > 0 else np.nan)
    call = CT[:, idx].sum((0, 1, 2)).real / np.maximum(nacc.sum(0), 1); c0 = call[0]; call = call / c0
    integ = np.trapezoid(call[sel], t[sel]); eta = rho / (k * k * integ) * CONV if integ > 0 else np.nan
    etab = np.array(etab); err = np.nanstd(etab) / math.sqrt(np.isfinite(etab).sum())
    cmin = call[sel].min(); imin = np.argmin(call[sel])
    # longitudinal spectrum: FFT of C_L(k,t) on the uniform fine lag grid (lags <= fine part)
    fine = np.arange(len(lags))[np.diff(np.concatenate([[0], lags])) == 1]     # indices of consecutive lags
    cl = CL[:, idx].sum((0, 1)).real / np.maximum(nacc.sum(0), 1); cl = cl / cl[0]; clf = cl[fine]
    w = np.hanning(2 * len(clf))[len(clf):]; spec = np.abs(np.fft.rfft(np.concatenate([clf * w, np.zeros(4 * len(clf))]))); freqs = np.fft.rfftfreq(5 * len(clf), dts) * 2 * math.pi
    ipk = int(np.argmax(spec[1:]) + 1); wpk = float(freqs[ipk])
    rows.append(dict(n2=int(s), k=k, nvec=len(idx), eta=eta, err=err, C0_over_NkTM=float(c0 / (2 * len(idx) * N * 0.0083144626 * T * M)), cmin=float(cmin), tmin=float(t[sel][imin]), omega_L=wpk, cL_over_k=wpk / k * 1e3))
out = dict(N=N, L=L, T=T, k_min=2 * math.pi / L, samples=int(nacc.sum(0)[0]), t_ps=float(nacc.sum(0)[0] * dts), tmax=tmax, nblock=nb, seed=int(f['seed']), rows=rows)
print('== argon eta(k) ==  (C_T(0)/(N kT M) per vector-component: %s)' % ', '.join('%.2f' % r['C0_over_NkTM'] for r in rows[:5]))
for r in rows: print('n2=%4d k=%6.3f nvec=%2d  eta=%.4f +- %.4f mPa s  C_min %+.3f at %.3f ps  omega_L %.2f ps^-1 -> omega/k %.0f m/s' % (r['n2'], r['k'], r['nvec'], r['eta'], r['err'], r['cmin'], r['tmin'], r['omega_L'], r['cL_over_k']))
ks = np.array([r['k'] for r in rows]); e = np.array([r['eta'] for r in rows]); ee = np.array([r['err'] for r in rows]); m = np.isfinite(e) & (e > 0)
w_ = np.where(np.isfinite(ee) & (ee > 0), ee, np.nanmedian(ee[m]))
gauss = lambda k, e0, b: e0 * np.exp(-b * k * k); lor = lambda k, e0, c: e0 / (1 + c * k * k)
(e0g, b), cg = curve_fit(gauss, ks[m], e[m], p0=[e[m][0], 0.003], sigma=w_[m], absolute_sigma=True, maxfev=20000)
(e0l, cc), cl_ = curve_fit(lor, ks[m], e[m], p0=[e[m][0], 0.01], sigma=w_[m], absolute_sigma=True, maxfev=20000)
chi_g = float(np.sum(((gauss(ks[m], e0g, b) - e[m]) / w_[m]) ** 2)); chi_l = float(np.sum(((lor(ks[m], e0l, cc) - e[m]) / w_[m]) ** 2))
kc = math.sqrt(0.343653 / b); kce = 0.5 * kc * math.sqrt(cg[1, 1]) / b
out['fit'] = dict(eta0_gauss=e0g, b=b, b_err=float(math.sqrt(cg[1, 1])), kc_measured=kc, kc_err=kce, k_1e=1 / math.sqrt(b), chi2_gauss=chi_g, eta0_lor=e0l, c=cc, chi2_lor=chi_l, ndata=int(m.sum()), better='gaussian' if chi_g < chi_l else 'lorentzian')
print('\nGaussian: eta0 %.4f mPa s, b %.5f +- %.5f nm^2 -> measured k_c %.2f +- %.2f (1/e at %.2f), chi2 %.1f | Lorentzian eta0 %.4f c %.5f chi2 %.1f -> %s (n=%d)' % (e0g, b, out['fit']['b_err'], kc, kce, 1 / math.sqrt(b), chi_g, e0l, cc, chi_l, out['fit']['better'], m.sum()))
# low-k plateau eta_0 and the model's c_0
lo = [r for r in rows if r['k'] < 3.0]; wl = np.array([1 / r['err'] ** 2 for r in lo]); e0p = sum(r['eta'] * x for r, x in zip(lo, wl)) / wl.sum(); out['eta0_plateau'] = dict(value=e0p, err=1 / math.sqrt(wl.sum()), nshell=len(lo))
c0s = [r['cL_over_k'] for r in rows[:3]]; out['c0_model_low_k'] = dict(shells=[r['k'] for r in rows[:3]], values=c0s)
print('low-k plateau eta_0 (k<3, %d shells): %.4f +- %.4f mPa s (NIST 85 K: 0.2795)' % (len(lo), e0p, 1 / math.sqrt(wl.sum())))
print('model c_0 from longitudinal dispersion at k = %s: %s m/s (NIST 854.35)' % (', '.join('%.2f' % k for k in out['c0_model_low_k']['shells']), ', '.join('%.0f' % c for c in c0s)))
ct = f['comtraj'].astype(np.float64); dtm = float(f['msd_every_ps'])
if ct.shape[0] > 20:
    nlag = ct.shape[0] // 4; msd = np.array([((ct[l:] - ct[:-l]) ** 2).sum(-1).mean() for l in range(1, nlag)]); tt = np.arange(1, nlag) * dtm
    s_ = (tt >= 5.0) & (tt <= min(40.0, tt[-1])); D = np.polyfit(tt[s_], msd[s_], 1)[0] / 6; out['D_cm2_s'] = D * 1e-2
    print('D (multi-origin MSD, lags %.0f-%.0f ps) = %.2e cm^2/s (LJ literature at this state ~1.6-1.8e-5)' % (tt[s_][0], tt[s_][-1], D * 1e-2))
print('T mean %.2f K  P mean %.0f bar  samples %d = %.0f ps' % (T, float(f['Pacc'].mean()), out['samples'], out['t_ps']))
# candidates
for name, kcp in (('P1 k_c = omega/c_0 (NIST 854.35)', 9.193), ('P2 = 1.5 x P1', 13.789)):
    print('%s: %.2f -> measured/predicted = %.3f' % (name, kcp, kc / kcp))
out['P1_ratio'] = kc / 9.193; out['P2_ratio'] = kc / 13.789
json.dump(out, open(sys.argv[1].replace('.npz', '_analysis.json'), 'w'), indent=1, default=float)
