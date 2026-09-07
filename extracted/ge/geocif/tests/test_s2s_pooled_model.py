"""Tests for the S2S eligibility scanner and the pooled model.

Critical properties: the eligibility window math (open / too_early /
in_season, usable-from month), the phenology-aligned init calendar, and the
pooled LOYO's YEAR-level exclusion across countries (ENSO years are shared —
per-country exclusion would leak the fold year through the neighbour).
"""
import unittest
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd


class TestEligibilityWindow(unittest.TestCase):
    def test_sa_maize_open_in_september(self):
        from geocif.experiments.s2s_eligibility import window_state

        st = window_state(planting=11, wraps=True, today=date(2026, 9, 6),
                          latest_init="2026-08")
        self.assertEqual(st["status"], "open")
        self.assertEqual(st["harvest_year"], 2027)
        self.assertEqual(st["usable_from"], "2026-07")
        self.assertTrue(st["usable_init_published"])

    def test_kenya_march_planting_too_early(self):
        from geocif.experiments.s2s_eligibility import window_state

        st = window_state(planting=3, wraps=False, today=date(2026, 9, 6),
                          latest_init="2026-08")
        self.assertEqual(st["status"], "too_early")
        self.assertEqual(st["harvest_year"], 2027)
        self.assertEqual(st["usable_from"], "2026-11")

    def test_recently_planted_season_rolls_to_next_year(self):
        """Aug-planted crop on Sep 6: the current season is already growing
        (in-season CIDs own it); the scanner reports the NEXT unstarted
        season, whose window opens Apr 2027."""
        from geocif.experiments.s2s_eligibility import window_state

        st = window_state(planting=8, wraps=False, today=date(2026, 9, 6),
                          latest_init="2026-08")
        self.assertEqual(st["status"], "too_early")
        self.assertEqual(st["usable_from"], "2027-04")
        self.assertEqual(st["harvest_year"], 2027)

    def test_in_season_during_planting_month(self):
        from geocif.experiments.s2s_eligibility import window_state

        st = window_state(planting=9, wraps=False, today=date(2026, 9, 6),
                          latest_init="2026-08")
        self.assertEqual(st["status"], "in_season")

    def test_open_but_init_not_published(self):
        from geocif.experiments.s2s_eligibility import window_state

        # window open since July, but S2S data only reaches June
        st = window_state(planting=11, wraps=True, today=date(2026, 9, 6),
                          latest_init="2026-06")
        self.assertEqual(st["status"], "open")
        self.assertFalse(st["usable_init_published"])


class TestInitCalendar(unittest.TestCase):
    def test_sa_aug_init(self):
        from geocif.experiments.s2s_pooled_model import init_calendar, lead_map

        # SA: planting Nov (wraps), harvest 2027, offset 3 -> Aug 2026
        self.assertEqual(init_calendar(11, 3, 2027, True), (2026, 8))
        self.assertEqual(lead_map(11, 3), {11: 3, 12: 4, 1: 5, 2: 6})

    def test_kenya_dec_init(self):
        from geocif.experiments.s2s_pooled_model import init_calendar, lead_map

        # Kenya: planting Mar (no wrap), harvest 2027, offset 3 -> Dec 2026
        self.assertEqual(init_calendar(3, 3, 2027, False), (2026, 12))
        self.assertEqual(lead_map(3, 3), {3: 3, 4: 4, 5: 5, 6: 6})

    def test_offset4_drops_last_month(self):
        from geocif.experiments.s2s_pooled_model import lead_map

        # offset 4: lead for planting+3 would be 7 -> excluded
        self.assertEqual(lead_map(11, 4), {11: 4, 12: 5, 1: 6})


class TestPooledLoyoLeakage(unittest.TestCase):
    def test_fold_year_excluded_across_countries(self):
        """Poison the fold year in the NEIGHBOUR country. If pooling excluded
        only the target's rows, the poison would drag the fit; year-level
        exclusion keeps the prediction sane."""
        from geocif.experiments.s2s_pooled_model import pooled_loyo
        from geocif.experiments.s2s_simple_model import FEATURES

        rng = np.random.default_rng(9)
        rows = []
        for ctry in ("aa", "bb"):
            for y in range(2000, 2016):
                for r in ("r1", "r2", "r3", "r4"):
                    rows.append({"country": ctry, "region": f"{ctry}_{r}",
                                 "year": y, "z_PRCPTOT": rng.normal(),
                                 "z_TMEAN": rng.normal(),
                                 "z_P_GF": rng.normal(),
                                 "anom": rng.normal(0, 0.02)})
        d = pd.DataFrame(rows)
        d["DRYHEAT"] = d["z_PRCPTOT"] * d["z_TMEAN"]
        # poison 2007 in country bb only
        d.loc[(d.country == "bb") & (d.year == 2007), "anom"] = 8.0

        lo = pooled_loyo(d, FEATURES, list(range(2001, 2015)), "aa",
                         ["aa", "bb"])
        fold = lo[lo.year == 2007]
        self.assertEqual(len(fold), 4)
        self.assertTrue((fold["ahat"].abs() < 0.5).all(),
                        f"neighbour-year leak: {fold['ahat'].tolist()}")


class TestPickS2sDir(unittest.TestCase):
    """A country may have S2S at several admin levels (Malawi has both after
    the per-country extraction fix). The level that JOINS the yields wins."""

    def _make(self, root, admin, regions):
        d = Path(root) / admin / "cr" / "s2s_tprate"
        d.mkdir(parents=True, exist_ok=True)
        for i, r in enumerate(regions):
            (d / f"MW{i:04d}_{r}_2005_s2s_tprate_cr.csv").write_text("x")

    def test_prefers_the_level_that_joins(self):
        import tempfile
        from geocif.experiments.s2s_pooled_model import pick_s2s_dir

        root = tempfile.mkdtemp()
        self._make(root, "admin_1", ["central", "northern", "southern"])
        self._make(root, "admin_2", ["balaka", "blantyre", "chikwawa", "dedza"])
        yields = {"balaka", "blantyre", "chikwawa", "dedza"}
        got = pick_s2s_dir(root, yields)
        self.assertIn("admin_2", got)

    def test_returns_none_when_nothing_joins(self):
        import tempfile
        from geocif.experiments.s2s_pooled_model import pick_s2s_dir

        root = tempfile.mkdtemp()
        self._make(root, "admin_1", ["central", "northern"])
        self.assertIsNone(pick_s2s_dir(root, {"balaka", "dedza"}))


class TestCausalTrend(unittest.TestCase):
    def test_trend_excludes_own_year(self):
        from geocif.experiments.s2s_pooled_model import causal_trend

        obs = pd.DataFrame({
            "region": ["x"] * 12, "year": list(range(2000, 2012)),
            "obs": [2.0 + 0.1 * i for i in range(12)],
        })
        # spike one year; its own trend must be fit WITHOUT the spike
        obs.loc[obs.year == 2005, "obs"] = 30.0
        d = causal_trend(obs)
        r = d[d.year == 2005].iloc[0]
        self.assertLess(abs(r["trend"] - 2.55), 0.15)  # ~ the line without the spike
        self.assertGreater(r["anom"], 5)


if __name__ == "__main__":
    unittest.main()
