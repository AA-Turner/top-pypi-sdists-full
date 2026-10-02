#!/usr/bin/env python
"""Check pikobs.stats.pitman_morgan_confidence before any module uses it.

1. The worked example of the stats page (8 pairs, rho 0.999): 57.1 %.
2. Against scipy on raw data: Pitman-Morgan is the Pearson test of
   corr(x + y, y - x); both must agree to 1e-6 on random samples.
3. Identical runs (the iasi case): confidence 0, not NaN, not 100.
4. Independent runs (rho ~ 0): close to the F-test.
5. Correlated runs with a small sigma change (the sw case): the F-test
   misses it, Pitman-Morgan does not.
6. n < 3: NaN.  7. sigma_confidence picks the right test.

    python test_pitman_morgan.py        -> "all checks passed" or the first failure
"""
import numpy as np
from scipy import stats as sps

from pikobs.stats import (ftest_confidence, pitman_morgan_confidence,
                          sample_std, sigma_confidence)


def pop(x, y):
    """Population moments, as the modules derive them from their sums."""
    return x.var(), y.var(), np.mean((x - x.mean()) * (y - y.mean()))


def pm_scipy(x, y):
    r, p = sps.pearsonr(x + y, y - x)
    return (1 - p) * 100


def check(name, cond, detail=""):
    print(f"{'ok  ' if cond else 'FAIL'}  {name}  {detail}")
    if not cond:
        raise SystemExit(1)


# 1. the page's example, from its five sums
N, Sx, Sxx, Sy, Syy, Sxy = 8, 2.4, 2.7018, 1.96, 2.4028, 2.5381
vx, vy = Sxx / N - (Sx / N) ** 2, Syy / N - (Sy / N) ** 2
c = Sxy / N - (Sx / N) * (Sy / N)
got = float(pitman_morgan_confidence(vx, vy, c, N))
check("stats page example", abs(got - 57.1) < 0.1, f"{got:.1f} % (expected 57.1)")

# 2. against scipy on raw samples
rng = np.random.default_rng(1)
for rho, n in ((0.0, 30), (0.5, 200), (0.99, 1000), (0.9999, 50000)):
    base = rng.normal(size=n)
    x = base * 2.5 + rng.normal(size=n) * 2.5 * np.sqrt(1 - rho ** 2)
    y = base * 2.5 * 1.002 + rng.normal(size=n) * 2.5 * np.sqrt(1 - rho ** 2)
    ours = float(pitman_morgan_confidence(*pop(x, y), n))
    ref = pm_scipy(x, y)
    check(f"scipy rho={rho} n={n}", abs(ours - ref) < 1e-6,
          f"{ours:.6f} vs {ref:.6f}")

# 3. identical runs
x = rng.normal(size=1000)
got = float(pitman_morgan_confidence(*pop(x, x.copy()), 1000))
check("identical runs -> 0", got == 0.0, f"{got}")
got = float(pitman_morgan_confidence(*pop(x, x + 0.3), 1000))
check("same up to a constant -> 0", got == 0.0, f"{got}")

# 4. independent runs: close to the F-test
x, y = rng.normal(size=5000), rng.normal(size=5000) * 1.03
pm = float(pitman_morgan_confidence(*pop(x, y), 5000))
ft = float(ftest_confidence(sample_std(x.std(), 5000), 5000,
                            sample_std(y.std(), 5000), 5000))
check("independent: PM ~ F", abs(pm - ft) < 10, f"PM {pm:.1f} %, F {ft:.1f} %")

# 5. the sw case: rho 0.9999, sigma 2.5 -> 2.5 * 1.003, n = 20000
n = 20000
base = rng.normal(size=n) * 2.5
x = base + rng.normal(size=n) * 0.035
y = base * 1.003 + rng.normal(size=n) * 0.035
pm = float(pitman_morgan_confidence(*pop(x, y), n))
ft = float(ftest_confidence(sample_std(x.std(), n), n,
                            sample_std(y.std(), n), n))
check("correlated, sigma +0.3 %: PM sees it", pm > 95 and ft < 95,
      f"PM {pm:.1f} %, F {ft:.1f} %")

# 6. too few pairs
check("n < 3 -> NaN", np.isnan(pitman_morgan_confidence(1.0, 1.1, 0.9, 2)))

# 7. the picker
vx_, vy_, c_ = pop(x, y)
check("sigma_confidence with cov = PM",
      float(sigma_confidence(vx_, vy_, n, cov=c_)) == pm)
check("sigma_confidence without cov = F",
      abs(float(sigma_confidence(vx_, vy_, n)) - ft) < 1e-9)

# vectorised, as the modules call it
v = pitman_morgan_confidence([vx, vx_], [vy, vy_], [c, c_], [N, n])
check("vectorised", v.shape == (2,) and abs(v[0] - 57.1) < 0.1)

print("all checks passed")
