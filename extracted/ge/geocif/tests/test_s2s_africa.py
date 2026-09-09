"""Tests for the Africa-wide pre-season S2S runner.

The calendar parser is the risky piece: EWCM encodes a season as 24
half-month bins (1=plant 2=grow 3=harvest 4=post) that wrap the calendar
year, and one real row (Central African Republic / Vakaga) is 23 bins of
-1 plus a stray 3 — a naive "any value > 0" test reads that as a December
planting. Each case below is checked against known agronomy.
"""
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

MONTHS = ["jan", "feb", "mar", "apr", "may", "jun",
          "jul", "aug", "sep", "oct", "nov", "dec"]
BINS = [f"{m}_{h}" for m in MONTHS for h in (1, 15)]


def bins(**kw):
    """24 zero bins with the named ones overridden, e.g. bins(nov_15=1)."""
    v = dict.fromkeys(BINS, 0)
    v.update(kw)
    return [v[b] for b in BINS]


class TestBinParsing(unittest.TestCase):
    def test_malawi_maize_plants_november_harvests_april(self):
        from geocif.experiments.s2s_africa import _bounds_from_bins

        # Malawi Central Region, EWCM maize_1: plant mid-Nov, harvest Apr,
        # post-harvest May. The planting run STARTS at nov_15 even though
        # jan_1 is also a 1 (it is the tail of the same wrapped run).
        v = bins(nov_15=1, dec_1=1, dec_15=1, jan_1=1,
                 jan_15=2, feb_1=2, feb_15=2, mar_1=2,
                 mar_15=3, apr_1=3, apr_15=3, may_1=4, may_15=4)
        plant, harvest, wraps = _bounds_from_bins(v)
        self.assertEqual(plant, 11)
        self.assertEqual(harvest, 4)
        self.assertTrue(wraps)

    def test_egypt_winter_wheat_plants_november_harvests_may(self):
        from geocif.experiments.s2s_africa import _bounds_from_bins

        v = bins(nov_1=1, nov_15=1,
                 dec_1=2, dec_15=2, jan_1=2, jan_15=2, feb_1=2, feb_15=2,
                 mar_1=2, mar_15=2, apr_1=2, apr_15=2,
                 may_1=3, may_15=3, jun_1=4, jun_15=4)
        plant, harvest, wraps = _bounds_from_bins(v)
        self.assertEqual((plant, harvest), (11, 5))
        self.assertTrue(wraps)

    def test_sudan_sorghum_within_year(self):
        from geocif.experiments.s2s_africa import _bounds_from_bins

        # plant Jun-Jul, grow Aug-Oct, harvest Nov-Dec -> no wrap
        v = bins(jun_1=1, jun_15=1, jul_1=1, jul_15=1,
                 aug_1=2, aug_15=2, sep_1=2, sep_15=2, oct_1=2, oct_15=2,
                 nov_1=3, nov_15=3, dec_1=3, dec_15=3)
        plant, harvest, wraps = _bounds_from_bins(v)
        self.assertEqual((plant, harvest), (6, 12))
        self.assertFalse(wraps)

    def test_car_vakaga_minus_one_anomaly_is_rejected(self):
        from geocif.experiments.s2s_africa import _bounds_from_bins

        v = [-1] * 24
        v[-1] = 3                      # the real stray harvest flag
        self.assertIsNone(_bounds_from_bins(v))

    def test_crop_not_grown_rows_rejected(self):
        from geocif.experiments.s2s_africa import _bounds_from_bins

        self.assertIsNone(_bounds_from_bins([-1] * 24))
        self.assertIsNone(_bounds_from_bins([0] * 24))
        self.assertIsNone(_bounds_from_bins([0] * 23))          # wrong length

    def test_no_planting_flag_rejected(self):
        from geocif.experiments.s2s_africa import _bounds_from_bins

        # growing + harvest but no 1 anywhere
        self.assertIsNone(_bounds_from_bins(bins(mar_1=2, apr_1=3)))


class TestSeasonIndex(unittest.TestCase):
    def test_primary_and_secondary(self):
        from geocif.experiments.s2s_africa import season_index

        for name in ("Main", "Long", "Gu", "Meher", "Season A", "Summer"):
            self.assertEqual(season_index(name), 1, name)
        for name in ("Short", "Deyr", "Season B", "Second", "Winter"):
            self.assertEqual(season_index(name), 2, name)

    def test_unknown_season_defaults_primary(self):
        from geocif.experiments.s2s_africa import season_index

        self.assertEqual(season_index("Rice season"), 1)
        self.assertEqual(season_index("Annual"), 1)


class TestHvstatCalendarFallback(unittest.TestCase):
    """Beans have no EWCM sheet for Africa, so HarvestStat's own months
    are the only source; the fallback must read them correctly."""

    def test_wrapping_season_from_planting_year(self):
        from geocif.experiments.s2s_africa import hvstat_calendar

        raw = pd.DataFrame({
            "fnid": ["A", "B", "A", "B"],
            "planting_month": [11, 11, 11, 12],
            "harvest_month": [4, 4, 4, 4],
            "planting_year": [2010, 2010, 2011, 2011],
            "harvest_year": [2011, 2011, 2012, 2012],
        })
        cal = hvstat_calendar(raw)
        self.assertEqual(cal["planting_month"], 11)
        self.assertEqual(cal["harvest_month"], 4)
        self.assertTrue(cal["wraps"])
        self.assertEqual(cal["calendar_source"], "hvstat")

    def test_within_year_season(self):
        from geocif.experiments.s2s_africa import hvstat_calendar

        raw = pd.DataFrame({
            "fnid": ["A", "B"], "planting_month": [3, 3],
            "harvest_month": [8, 8],
            "planting_year": [2010, 2010], "harvest_year": [2010, 2010],
        })
        cal = hvstat_calendar(raw)
        self.assertEqual((cal["planting_month"], cal["harvest_month"]), (3, 8))
        self.assertFalse(cal["wraps"])

    def test_missing_months_returns_none(self):
        from geocif.experiments.s2s_africa import hvstat_calendar

        raw = pd.DataFrame({"fnid": ["A"], "planting_month": [np.nan],
                            "harvest_month": [np.nan],
                            "planting_year": [2010], "harvest_year": [2010]})
        self.assertIsNone(hvstat_calendar(raw))


class TestS2sFnidLoading(unittest.TestCase):
    def test_duplicate_admin_levels_are_deduplicated(self):
        """The same polygon can be written under admin_1 AND admin_2 (the
        level only sets the label); the loader must not double-count it."""
        import tempfile
        from geocif.experiments.s2s_africa import load_s2s_fnid

        root = Path(tempfile.mkdtemp())
        row = {"country": "x", "region_id": "MW001", "year": 2005, "month": 8,
               "s2s_tprate_lead1": 1.0}
        for admin, label in (("admin_1", "central"), ("admin_2", "dedza")):
            d = root / admin / "cr" / "s2s_tprate"
            d.mkdir(parents=True)
            pd.DataFrame([{**row, "region": label}]).to_csv(
                d / f"MW001_{label}_2005_s2s_tprate_cr.csv", index=False)

        df = load_s2s_fnid(root, "tprate")
        self.assertEqual(len(df), 1)
        self.assertIn("fnid", df.columns)
        self.assertEqual(df.iloc[0]["fnid"], "MW001")

    def test_missing_dir_returns_empty(self):
        import tempfile
        from geocif.experiments.s2s_africa import load_s2s_fnid

        self.assertTrue(load_s2s_fnid(Path(tempfile.mkdtemp()), "tprate").empty)


class TestCausalTrendFnid(unittest.TestCase):
    def test_trend_never_sees_its_own_year(self):
        from geocif.experiments.s2s_africa import causal_trend_fnid

        obs = pd.DataFrame({"fnid": ["A"] * 12,
                            "year": list(range(2000, 2012)),
                            "obs": [2.0 + 0.1 * i for i in range(12)]})
        obs.loc[obs.year == 2005, "obs"] = 30.0        # spike
        d = causal_trend_fnid(obs)
        r = d[d.year == 2005].iloc[0]
        self.assertLess(abs(r["trend"] - 2.55), 0.2)   # line without the spike
        self.assertGreater(r["anom"], 5)


class TestFeatureListPerOffset(unittest.TestCase):
    def test_offset4_drops_grainfill_feature(self):
        from geocif.experiments.s2s_africa import features_for_offset

        self.assertIn("z_P_GF", features_for_offset(3))
        self.assertNotIn("z_P_GF", features_for_offset(4))


class TestClassProbabilities(unittest.TestCase):
    def test_probabilities_sum_to_one_and_shift_with_anomaly(self):
        from geocif.experiments.s2s_africa import class_probabilities

        hist = pd.Series(np.linspace(-0.3, 0.3, 20))
        resid = np.random.default_rng(0).normal(0, 0.05, 200)
        dry = class_probabilities(-0.30, hist, resid)
        wet = class_probabilities(+0.30, hist, resid)
        for p in (dry, wet):
            self.assertAlmostEqual(p["P_low"] + p["P_mid"] + p["P_high"], 1.0,
                                   places=2)
        self.assertGreater(dry["P_low"], wet["P_low"])
        self.assertGreater(dry["P_below_trend"], wet["P_below_trend"])

    def test_too_little_history_returns_none(self):
        from geocif.experiments.s2s_africa import class_probabilities

        self.assertIsNone(class_probabilities(0.0, pd.Series([0.1, 0.2]),
                                              np.zeros(50)))


class TestExtendedTermOnly(unittest.TestCase):
    def test_in_season_is_not_forecastable(self):
        """Extended-term only: once planting has passed the combination
        belongs to the in-season system."""
        from datetime import date
        from geocif.experiments.s2s_eligibility import window_state

        st = window_state(planting=9, wraps=False, today=date(2026, 9, 20),
                          latest_init="2026-08")
        self.assertEqual(st["status"], "in_season")
        st_open = window_state(planting=11, wraps=True, today=date(2026, 9, 20),
                               latest_init="2026-08")
        self.assertEqual(st_open["status"], "open")


class TestHistoryGateSurvivesTheJoin(unittest.TestCase):
    """MIN_YEARS is checked on the raw HarvestStat record, but the S2S join
    can cut the usable span hard and the row-count gate does not notice
    because units multiply.

    Kenya Short reached the forecast on 189 unit-years spanning only 8
    calendar years — too few even to form a leave-one-out national tercile.
    Since the effective sample size of a pooled AUC is YEARS, not unit-years,
    the gate has to be re-applied after the join.
    """

    def test_gate_is_reapplied_on_the_joined_frame(self):
        import inspect
        from geocif.experiments import s2s_africa as sa

        src = inspect.getsource(sa.run)
        i_join = src.find("train = anoms.merge(fx_h")
        i_gate = src.find("n_train_years = int(train.year.nunique())")
        self.assertGreater(i_gate, i_join, "gate must follow the join")
        self.assertIn("if n_train_years < MIN_YEARS:", src)
        # and it must reject, not merely record
        tail = src[i_gate:i_gate + 900]
        self.assertIn('status="too_short"', tail)
        self.assertIn("excluded.append(rec)", tail)

    def test_row_count_gate_alone_would_have_passed_kenya(self):
        """The pre-existing gate cannot catch this: 189 rows over 8 years
        clears `len(train) < 40` by a factor of four."""
        rows, years, units = 189, 8, 40
        self.assertGreater(rows, 40)          # old gate passes
        self.assertLess(years, 12)            # new gate rejects
        self.assertAlmostEqual(rows / units, 4.7, places=1)


class TestClipToSupport(unittest.TestCase):
    """Clipping must be measured, not silent.

    NOAA's S2S real-time stream runs ~1.3 C warmer than its 1993-2016
    hindcast members, so z_TMEAN lands at +3.5..+5.7 sd in every African
    country and DRYHEAT inherits it. Clipping then pins the forecast to the
    training boundary and the output looks like a confident call. These
    tests pin the reporting that makes it visible.
    """

    def _train(self):
        return pd.DataFrame({
            "z_PRCPTOT": [-1.0, 0.0, 1.0, -0.5, 0.5],
            "z_TMEAN": [-1.0, 0.0, 1.0, -0.5, 0.5],
            "DRYHEAT": [1.0, 0.0, 1.0, 0.25, 0.25],
        })

    def test_in_support_reports_zero_exceedance(self):
        from geocif.experiments.s2s_africa import clip_to_support

        fx = pd.DataFrame({"z_PRCPTOT": [0.5], "z_TMEAN": [0.5]})
        out, rep = clip_to_support(fx, self._train(), ["z_PRCPTOT", "z_TMEAN"])
        self.assertEqual(int(rep["n_clipped"].iloc[0]), 0)
        self.assertEqual(float(rep["oos_max_sigma"].iloc[0]), 0.0)
        self.assertEqual(rep["oos_feature"].iloc[0], "")
        self.assertAlmostEqual(float(out["z_TMEAN"].iloc[0]), 0.5)

    def test_out_of_support_is_clipped_and_named(self):
        from geocif.experiments.s2s_africa import clip_to_support

        # the real Kenya/South Africa case: temperature far outside the range
        fx = pd.DataFrame({"z_PRCPTOT": [1.7], "z_TMEAN": [3.7]})
        out, rep = clip_to_support(fx, self._train(), ["z_PRCPTOT", "z_TMEAN"])
        self.assertEqual(float(out["z_TMEAN"].iloc[0]), 1.0)      # pinned
        self.assertEqual(float(out["z_PRCPTOT"].iloc[0]), 1.0)
        self.assertEqual(int(rep["n_clipped"].iloc[0]), 2)
        self.assertEqual(rep["oos_feature"].iloc[0], "z_TMEAN")
        self.assertGreater(float(rep["oos_max_sigma"].iloc[0]), 3.0)

    def test_dryheat_is_rebuilt_from_the_raw_product(self):
        """DRYHEAT must be formed from the UNCLIPPED z terms, then clipped —
        clipping the terms first would hide the interaction's exceedance."""
        from geocif.experiments.s2s_africa import clip_to_support

        fx = pd.DataFrame({"z_PRCPTOT": [1.7], "z_TMEAN": [3.7]})
        out, rep = clip_to_support(fx, self._train(),
                                   ["z_PRCPTOT", "z_TMEAN", "DRYHEAT"])
        self.assertEqual(float(out["DRYHEAT"].iloc[0]), 1.0)      # train max
        self.assertGreater(float(rep["oos_max_sigma"].iloc[0]), 3.0)
        self.assertEqual(int(rep["n_clipped"].iloc[0]), 3)

    def test_forecast_rows_carry_the_support_columns(self):
        import inspect
        from geocif.experiments import s2s_africa as sa

        src = inspect.getsource(sa.run)
        for col in ('"n_clipped"', '"oos_max_sigma"', '"oos_feature"',
                    '"in_support"'):
            self.assertIn(col, src, col)
        self.assertIn("OOS_TOLERANCE", src)


if __name__ == "__main__":
    unittest.main()


class TestSkillReportedIsTheIssuedLead(unittest.TestCase):
    """forecasts.csv must quote the skill of the init the forecast was
    ISSUED from, not the best-scoring init.

    Kenya Short is issued at offset 2 (AUC 0.31, worse than chance) while
    its best offset scores 0.49; reporting the latter beside the forecast
    overstated it and would have hidden that the call sits on an
    anti-skilled lead.
    """

    def test_source_uses_issued_offset_not_best(self):
        import inspect
        from geocif.experiments import s2s_africa as sa

        src = inspect.getsource(sa.run)
        # the skill dict handed to the forecast rows is keyed on off_used
        self.assertIn("skill_by_offset.get(off_used)", src)
        # and the best-offset figures are kept in separate columns
        self.assertIn('"best_offset"', src)
        self.assertIn('"best_auc"', src)
        # has_skill is derived from the issued lead, not the best one
        i_sk = src.find("skill_by_offset.get(off_used)")
        i_has = src.find("has_skill = bool(")
        self.assertGreater(i_has, i_sk)

    def test_skill_gate_is_the_permutation_test_not_a_half_threshold(self):
        """0.5 is the wrong benchmark for LOYO AUC — the null sits at 0.445
        across the 17 African combinations, so the gate is the permutation
        p-value."""
        import inspect
        from geocif.experiments import s2s_africa as sa

        src = inspect.getsource(sa.run)
        self.assertIn('sk["perm_p"] < PERM_ALPHA', src)
        self.assertNotIn('sk["auc"] > 0.5', src)
        self.assertLessEqual(sa.PERM_ALPHA, 0.05)


class TestPermutationNull(unittest.TestCase):
    """The year-block permutation must destroy the predictor-yield year
    correspondence while leaving the spatial and serial structure alone."""

    def _frame(self, signal):
        rng = np.random.default_rng(7)
        rows = []
        for fnid in [f"U{i}" for i in range(12)]:
            for y in range(1995, 2017):
                x = float(rng.normal())
                a = signal * x + 0.2 * float(rng.normal())
                rows.append({"fnid": fnid, "year": y, "anom": a,
                             "obs": 2.0 * (1 + a), "trend": 2.0,
                             "z_PRCPTOT": x, "z_TMEAN": float(rng.normal())})
        d = pd.DataFrame(rows)
        d["DRYHEAT"] = d.z_PRCPTOT * d.z_TMEAN
        return d

    def test_null_is_flat_and_signal_is_detected(self):
        from geocif.experiments.s2s_africa import (
            edge_table, loyo, permutation_auc, score_combo)

        feats = ["z_PRCPTOT"]
        yrs = list(range(1995, 2017))
        for signal, expect_significant in ((1.0, True), (0.0, False)):
            d = self._frame(signal)
            anoms = d[["fnid", "year", "obs", "trend", "anom"]]
            edges = edge_table(anoms)
            auc = score_combo(loyo(d, feats, yrs), anoms, edges)["auc"]
            r = permutation_auc(d, feats, yrs, anoms, edges, auc, n_perm=40)
            self.assertEqual(r["n_perm"], 40)
            self.assertEqual(r["perm_p"] < 0.05, expect_significant)

    def test_edge_table_matches_row_by_row_scoring(self):
        """The cached edges must reproduce the original per-row computation
        exactly — the cache is a speed-up, not a change of definition."""
        from geocif.experiments.s2s_africa import (
            _fold_bins, _to_class, edge_table)

        d = self._frame(0.5)
        anoms = d[["fnid", "year", "obs", "trend", "anom"]]
        tab = edge_table(anoms)
        a = anoms.dropna(subset=["anom"])
        for (fnid, y), (e, ev) in list(tab.items())[:25]:
            tr = a[(a.fnid == fnid) & (a.year != y)]["anom"]
            te = a[(a.fnid == fnid) & (a.year == y)]["anom"]
            np.testing.assert_allclose(e, _fold_bins(tr))
            self.assertEqual(ev, int(_to_class(te.iloc[0], e) == 0))
