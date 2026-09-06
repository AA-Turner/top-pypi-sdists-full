"""Tests for the simple S2S pre-season model (experiments/s2s_simple_model).

Covers: (a) z-score construction against hand-computed values; (b) the LOYO
harness never trains on the held-out year; (c) a region-year with an
incomplete Aug init is excluded, not NaN-propagated.
"""
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd


def _write_s2s(root, region, init_year, months, base=3.0, fnid="ZA1"):
    """Write one per-region s2s CSV pair with Aug-init lead values."""
    for var in ("tprate", "t2m"):
        d = Path(root) / f"s2s_{var}"
        d.mkdir(parents=True, exist_ok=True)
        rows = []
        for m in months:
            row = {"country": "south_africa", "region": region,
                   "region_id": fnid, "year": init_year, "month": m}
            for lead in range(1, 7):
                # deterministic, identifiable: value = base + init_year%10 + lead/10
                row[f"s2s_{var}_lead{lead}"] = base + (init_year % 10) + lead / 10
            rows.append(row)
        pd.DataFrame(rows).to_csv(
            d / f"{fnid}_{region}_{init_year}_s2s_{var}_cr.csv", index=False)


class TestFeatureConstruction(unittest.TestCase):
    def test_z_scores_match_hand_computation(self):
        from geocif.experiments import s2s_simple_model as sm2

        root = tempfile.mkdtemp()
        # real-hindcast init years 1993..2016 (harvests 1994..2017) + 2026
        for iy in list(range(1993, 2017)) + [2026]:
            _write_s2s(root, "free_state", iy, months=[8])
        feats = sm2.build_features(root, ["free_state"], [2000, 2027])
        self.assertEqual(len(feats), 2)

        # hand-compute PRCPTOT z for harvest 2000 (init 1999):
        # value(iy) = mean over leads {3,4,5,6} of (3 + iy%10 + lead/10)
        def season_val(iy):
            return np.mean([3 + iy % 10 + l / 10 for l in (3, 4, 5, 6)])

        ref = np.array([season_val(iy) for iy in range(1993, 2017)])
        z_expect = (season_val(1999) - ref.mean()) / ref.std(ddof=1)
        got = float(feats[feats["year"] == 2000]["z_PRCPTOT"].iloc[0])
        self.assertAlmostEqual(got, z_expect, places=6)
        # interaction is the product of its parts
        r = feats[feats["year"] == 2000].iloc[0]
        self.assertAlmostEqual(r["DRYHEAT"], r["z_PRCPTOT"] * r["z_TMEAN"], places=9)

    def test_incomplete_init_is_excluded_not_nan(self):
        from geocif.experiments import s2s_simple_model as sm2

        root = tempfile.mkdtemp()
        for iy in range(1993, 2017):
            _write_s2s(root, "free_state", iy, months=[8])
        # 2026 init file exists but has no August row -> harvest 2027 excluded
        _write_s2s(root, "free_state", 2026, months=[5, 6, 7])
        feats = sm2.build_features(root, ["free_state"], [2000, 2027])
        self.assertEqual(sorted(feats["year"]), [2000])
        self.assertFalse(feats.isna().any().any())


class TestLoyoHarness(unittest.TestCase):
    def test_held_out_year_never_in_training(self):
        """Poison test: give the held-out year an absurd anomaly. If the fold
        trained on it, its own prediction would chase the poison; a clean
        LOYO prediction stays near the (zero-signal) training mean."""
        from geocif.experiments import s2s_simple_model as sm2

        rng = np.random.default_rng(7)
        rows = []
        for y in range(1995, 2017):
            for r in ("a", "b", "c", "d"):
                rows.append({
                    "region": r, "year": y, "trend": 5.0,
                    "z_PRCPTOT": rng.normal(), "z_TMEAN": rng.normal(),
                    "z_P_GF": rng.normal(),
                })
        d = pd.DataFrame(rows)
        d["DRYHEAT"] = d["z_PRCPTOT"] * d["z_TMEAN"]
        d["anom"] = rng.normal(0, 0.02, len(d))          # ~zero signal
        d.loc[d["year"] == 2005, "anom"] = 5.0           # poison the fold year
        d["obs"] = d["trend"] * (1 + d["anom"])

        lo = sm2.loyo(d, sm2.FEATURES, list(range(1995, 2017)))
        fold = lo[lo["year"] == 2005]
        self.assertEqual(len(fold), 4)
        # clean LOYO: prediction unaware of the +500% poison
        self.assertTrue((fold["ahat"].abs() < 0.5).all(),
                        f"fold leaked training data: {fold['ahat'].tolist()}")

    def test_perfect_signal_is_recovered(self):
        from geocif.experiments import s2s_simple_model as sm2

        rng = np.random.default_rng(3)
        rows = []
        for y in range(1995, 2017):
            for r in ("a", "b", "c", "d"):
                zp, zt = rng.normal(), rng.normal()
                rows.append({"region": r, "year": y, "trend": 5.0,
                             "z_PRCPTOT": zp, "z_TMEAN": zt,
                             "z_P_GF": rng.normal(),
                             "anom": 0.10 * zp - 0.05 * zt})
        d = pd.DataFrame(rows)
        d["DRYHEAT"] = d["z_PRCPTOT"] * d["z_TMEAN"]
        d["obs"] = d["trend"] * (1 + d["anom"])
        lo = sm2.loyo(d, sm2.FEATURES, list(range(1995, 2017)))
        s = sm2.score(lo)
        self.assertGreater(s["anom_r"], 0.95)


class TestAlternativeLearners(unittest.TestCase):
    def _toy(self, n_years=10):
        rng = np.random.default_rng(5)
        rows = []
        for y in range(2000, 2000 + n_years):
            for r in ("a", "b", "c", "d"):
                zp, zt = rng.normal(), rng.normal()
                rows.append({"region": r, "year": y, "trend": 5.0,
                             "z_PRCPTOT": zp, "z_TMEAN": zt,
                             "z_P_GF": rng.normal(),
                             "anom": 0.08 * zp - 0.04 * zt + rng.normal(0, 0.01)})
        d = pd.DataFrame(rows)
        d["DRYHEAT"] = d["z_PRCPTOT"] * d["z_TMEAN"]
        d["obs"] = d["trend"] * (1 + d["anom"])
        return d

    def test_gam_learner_recovers_signal(self):
        from geocif.experiments import s2s_simple_model as sm2

        d = self._toy(12)
        lo = sm2.loyo(d, sm2.FEATURES, list(range(2002, 2010)), learner="gam")
        self.assertEqual(len(lo), 8 * 4)
        self.assertTrue(np.isfinite(lo["ahat"]).all())
        s = sm2.score(lo)
        self.assertGreater(s["anom_r"], 0.7)

    def test_gam_te_learner_runs(self):
        from geocif.experiments import s2s_simple_model as sm2

        d = self._toy(12)
        lo = sm2.loyo(d, sm2.FEATURES, [2005], learner="gam_te")
        self.assertEqual(len(lo), 4)
        self.assertTrue(np.isfinite(lo["ahat"]).all())

    def test_bass_learner_runs(self):
        try:
            import pyBASS  # noqa: F401
        except ImportError:
            self.skipTest("pyBASS not installed")
        from geocif.experiments import s2s_simple_model as sm2

        d = self._toy(10)
        lo = sm2.loyo(d, sm2.FEATURES, [2004], learner="bass")
        self.assertEqual(len(lo), 4)
        self.assertTrue(np.isfinite(lo["ahat"]).all())


class TestClassificationLabelModes(unittest.TestCase):
    def test_anom_labels_remove_trend_contamination(self):
        """With a rising trend and zero anomaly signal, raw-yield terciles
        make early years 'low' by construction; detrended terciles must not."""
        from geocif.experiments import s2s_simple_model as sm2

        rng = np.random.default_rng(11)
        rows = []
        for y in range(1995, 2017):
            for r in ("a", "b", "c", "d"):
                trend = 3.0 + 0.15 * (y - 1995)         # strong upward trend
                anom = rng.normal(0, 0.03)              # no real signal
                rows.append({"region": r, "year": y, "trend": trend,
                             "obs": trend * (1 + anom),
                             "z_PRCPTOT": rng.normal(), "z_TMEAN": rng.normal(),
                             "z_P_GF": rng.normal()})
        d = pd.DataFrame(rows)
        d["DRYHEAT"] = d["z_PRCPTOT"] * d["z_TMEAN"]
        d["anom"] = d["obs"] / d["trend"] - 1

        # a "trend follower" prediction source: yhat == trend
        pf = d[["region", "year", "trend"]].rename(columns={"trend": "yhat"})
        years = list(range(1996, 2016))

        raw = sm2.classification_eval(d, {"tf": pf}, years, native=False,
                                      label_mode="tercile_raw")
        anm = sm2.classification_eval(d, {"tf": pf}, years, native=False,
                                      label_mode="tercile_anom")
        acc_raw = float(raw[raw.model == "tf"].acc.iloc[0])
        acc_anm = float(anm[anm.model == "tf"].acc.iloc[0])
        # raw labels reward pure trend-following far above chance;
        # detrended labels must strip that advantage back toward chance
        self.assertGreater(acc_raw, 0.55)
        self.assertLess(acc_anm, 0.45)


if __name__ == "__main__":
    unittest.main()
