"""rec_pool.py - pool several rec_<tag>_analysis.json (same box) : per-shell mean eta(k) over seeds with
seed-to-seed scatter as the error, Gaussian/Lorentzian fits, measured k_c with error, candidate readings.
usage: python rec_pool.py out.json rec_a_analysis.json rec_b_analysis.json ..."""
import sys, json, math, numpy as np
from scipy.optimize import curve_fit
outp = sys.argv[1]; J = [json.load(open(p)) for p in sys.argv[2:]]
res = dict(n_seeds=len(J), N=J[0]['N'], L=J[0]['L'], t_ps_each=[j['t_ps'] for j in J], T=[j['T'] for j in J], D=[j.get('D_cm2_s') for j in J])
gauss = lambda k, e0, b: e0 * np.exp(-b * k * k); lor = lambda k, e0, c: e0 / (1 + c * k * k)
for label in ('COM', 'atoms'):
    ks = np.array([r['k'] for r in J[0][label]['rows']]); E = np.array([[r['eta'] for r in j[label]['rows']] for j in J])
    BE = np.array([[r['err'] for r in j[label]['rows']] for j in J]); BE = np.where(np.isfinite(BE) & (BE > 0), BE, np.nanmedian(BE))
    wts = 1 / BE ** 2; m = (E * wts).sum(0) / wts.sum(0); err_w = 1 / np.sqrt(wts.sum(0))     # block-error-weighted mean over seeds
    scatter = E.std(0, ddof=1) / math.sqrt(len(J)) if len(J) > 1 else 0 * m
    err = np.sqrt(err_w ** 2 + scatter ** 2)                                                   # block error and seed scatter in quadrature
    (e0g, b), cg = curve_fit(gauss, ks, m, p0=[m[0], 0.005], sigma=err, absolute_sigma=True, maxfev=20000)
    (e0l, cc), cl = curve_fit(lor, ks, m, p0=[m[0], 0.01], sigma=err, absolute_sigma=True, maxfev=20000)
    chi_g = float(np.sum(((gauss(ks, e0g, b) - m) / err) ** 2)); chi_l = float(np.sum(((lor(ks, e0l, cc) - m) / err) ** 2))
    kc = math.sqrt(0.343653 / b); kce = 0.5 * kc * math.sqrt(cg[1, 1]) / b
    # per-seed k_c scatter
    kcs = [j[label]['fit']['kc_measured'] for j in J]
    r = dict(k=ks.tolist(), eta_mean=m.tolist(), eta_err=err.tolist(), eta0_gauss=e0g, b=b, b_err=float(math.sqrt(cg[1, 1])), kc_measured=kc, kc_err_fit=kce,
             kc_per_seed=kcs, kc_seed_scatter=float(np.std(kcs, ddof=1) / math.sqrt(len(kcs))) if len(kcs) > 1 else None, k_1e=1 / math.sqrt(b),
             chi2_gauss=chi_g, chi2_lor=chi_l, ndata=len(ks), better='gaussian' if chi_g < chi_l else 'lorentzian', eta0_lor=e0l, c_lor=cc,
             ratio_c0=kc / 5.3067, ratio_cinf=kc / 2.4544, implied_c_m_s=2 * math.pi * 1.25e12 / (kc * 1e9),
             eta_ratio_at_c0_kc_fit=float(math.exp(-b * 5.3067 ** 2)), eta_ratio_at_c0_kc_data=float(np.interp(5.3067, ks, m) / e0g), eta_ratio_at_cinf_kc_fit=float(math.exp(-b * 2.4544 ** 2)))
    res[label] = r
    print('[%s] %d seeds: eta0 %.3f  k_c %.2f +- %.2f (fit) +- %s (seed scatter)  1/e %.2f  Gaussian chi2 %.1f vs Lorentzian %.1f (n=%d) -> %s | x c_0 %.2f  x c_inf %.2f  implied c %.0f m/s | eta(k_c(c0))/eta0 = %.3f from the fit, %.3f from the data (prediction e^-0.344 = 0.709)' %
          (label, len(J), e0g, kc, kce, ('%.2f' % r['kc_seed_scatter']) if r['kc_seed_scatter'] else 'n/a', r['k_1e'], chi_g, chi_l, len(ks), r['better'], r['ratio_c0'], r['ratio_cinf'], r['implied_c_m_s'], r['eta_ratio_at_c0_kc_fit'], r['eta_ratio_at_c0_kc_data']))
json.dump(res, open(outp, 'w'), indent=1, default=float)
