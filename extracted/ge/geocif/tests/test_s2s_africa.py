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


class TestDecomposedAuc(unittest.TestCase):
    """The pooled region-year AUC conflates two abilities that can point
    opposite ways — South Africa maize is anti-skilled nationally (0.330)
    and the best in Africa spatially (0.667). Both must be reported."""

    def _frame(self, national, spatial, seed=3):
        """Build LOYO output with a chosen national and spatial signal."""
        rng = np.random.default_rng(seed)
        units = [f"U{i}" for i in range(9)]
        rows = []
        for y in range(1995, 2017):
            yeff = float(rng.normal())              # the year's own anomaly
            for i, u in enumerate(units):
                ueff = float(rng.normal())          # this unit's departure
                anom = yeff + ueff
                # ahat tracks the year effect and/or the unit effect,
                # depending on which signal we asked for
                ahat = national * yeff + spatial * ueff + 0.05 * rng.normal()
                rows.append({"fnid": u, "year": y, "anom": anom,
                             "obs": 2.0 * (1 + anom), "trend": 2.0,
                             "ahat": ahat})
        lo = pd.DataFrame(rows)
        return lo, lo[["fnid", "year", "obs", "trend", "anom"]]

    def test_national_signal_lifts_only_the_national_auc(self):
        from geocif.experiments.s2s_africa import decomposed_auc, edge_table

        lo, anoms = self._frame(national=1.0, spatial=0.0)
        d = decomposed_auc(lo, anoms, edge_table(anoms))
        self.assertGreater(d["auc_national"], 0.75)
        self.assertLess(abs(d["auc_spatial"] - 0.5), 0.12)

    def test_spatial_signal_lifts_only_the_spatial_auc(self):
        from geocif.experiments.s2s_africa import decomposed_auc, edge_table

        lo, anoms = self._frame(national=0.0, spatial=1.0)
        d = decomposed_auc(lo, anoms, edge_table(anoms))
        self.assertGreater(d["auc_spatial"], 0.75)
        self.assertLess(abs(d["auc_national"] - 0.5), 0.25)

    def test_score_combo_carries_the_split(self):
        from geocif.experiments.s2s_africa import edge_table, score_combo

        lo, anoms = self._frame(national=1.0, spatial=0.3)
        s = score_combo(lo, anoms, edge_table(anoms))
        for k in ("auc", "auc_national", "auc_spatial", "n_years"):
            self.assertIn(k, s, k)
        self.assertEqual(s["n_years"], 22)

    def test_permutation_accepts_the_decomposed_dict(self):
        from geocif.experiments.s2s_africa import permutation_auc

        # a tiny synthetic training frame; the point is the return shape
        rng = np.random.default_rng(11)
        rows = []
        for u in [f"U{i}" for i in range(8)]:
            for y in range(1995, 2013):
                x = float(rng.normal())
                a = 0.8 * x + 0.2 * float(rng.normal())
                rows.append({"fnid": u, "year": y, "anom": a,
                             "obs": 2.0 * (1 + a), "trend": 2.0,
                             "z_PRCPTOT": x, "z_TMEAN": float(rng.normal())})
        train = pd.DataFrame(rows)
        train["DRYHEAT"] = train.z_PRCPTOT * train.z_TMEAN
        anoms = train[["fnid", "year", "obs", "trend", "anom"]]
        from geocif.experiments.s2s_africa import (
            decomposed_auc, edge_table, loyo)
        edges = edge_table(anoms)
        yrs = list(range(1995, 2013))
        obs = decomposed_auc(loyo(train, ["z_PRCPTOT"], yrs), anoms, edges)
        r = permutation_auc(train, ["z_PRCPTOT"], yrs, anoms, edges, obs,
                            n_perm=25)
        for k in ("null_auc", "perm_p", "null_auc_spatial", "perm_spatial_p"):
            self.assertIn(k, r, k)
        # a float still works, for callers that only want the pooled test
        r2 = permutation_auc(train, ["z_PRCPTOT"], yrs, anoms, edges,
                             obs["auc"], n_perm=10)
        self.assertIn("perm_p", r2)
        self.assertNotIn("perm_spatial_p", r2)


class TestDecomposedR2(unittest.TestCase):
    """Regression skill, split the same three ways as the classification.

    On the anomaly scale the trend baseline predicts 0, so R2 > 0 is very
    nearly "beats trend". Discrimination and magnitude come apart — Somalia
    ranks years well (national AUC 0.776) with national R2 ~ 0 — so both
    families have to be reported.
    """

    def _lo(self, national, spatial, seed=5):
        rng = np.random.default_rng(seed)
        rows = []
        for y in range(1995, 2017):
            yeff = float(rng.normal())
            for u in [f"U{i}" for i in range(9)]:
                ueff = float(rng.normal())
                anom = yeff + ueff
                rows.append({"fnid": u, "year": y, "trend": 2.0,
                             "obs": 2.0 * (1 + anom),
                             "ahat": national * yeff + spatial * ueff})
        return pd.DataFrame(rows)

    def test_national_signal_lifts_only_the_national_r2(self):
        from geocif.experiments.s2s_africa import decomposed_r2

        d = decomposed_r2(self._lo(national=1.0, spatial=0.0))
        self.assertGreater(d["r2_national"], 0.8)
        self.assertLess(d["r2_within"], 0.05)

    def test_spatial_signal_lands_mostly_in_the_within_r2(self):
        from geocif.experiments.s2s_africa import decomposed_r2

        d = decomposed_r2(self._lo(national=0.0, spatial=1.0))
        self.assertGreater(d["r2_within"], 0.8)
        self.assertGreater(d["r2_within"], 3 * d["r2_national"])

    def test_national_metric_is_noisier_not_biased_at_few_units(self):
        """A finite-sample property worth pinning, and it is VARIANCE not
        bias — the distinction matters for how South Africa is read.

        A purely spatial predictor scores a national R2 of ~0 on AVERAGE at
        every unit count; the SPREAD is what shrinks as units grow, because
        the year-mean of a spatial predictor is a sample mean. So a national
        score on 9 provinces deserves wider error bars than one on 71, and
        the per-combination permutation null is what supplies them.
        """
        from geocif.experiments.s2s_africa import decomposed_r2

        def spread(n_units):
            vals = []
            for seed in range(10):
                rng = np.random.default_rng(seed)
                rows = []
                for y in range(1995, 2017):
                    yeff = float(rng.normal())      # predictor cannot see it
                    for u in [f"U{i}" for i in range(n_units)]:
                        ueff = float(rng.normal())
                        rows.append({"fnid": u, "year": y, "trend": 2.0,
                                     "obs": 2.0 * (1 + yeff + ueff),
                                     "ahat": ueff})
                vals.append(decomposed_r2(pd.DataFrame(rows))["r2_national"])
            return float(np.mean(vals)), float(np.max(vals))

        mean_few, max_few = spread(5)
        mean_many, max_many = spread(90)
        # unbiased at both
        self.assertLess(abs(mean_few), 0.2)
        self.assertLess(abs(mean_many), 0.2)
        # but far noisier with few units
        self.assertGreater(max_few, max_many)
        self.assertLess(max_many, 0.15)

    def test_zero_signal_gives_non_positive_r2(self):
        """A model that predicts nothing must not score above the trend."""
        from geocif.experiments.s2s_africa import decomposed_r2

        d = decomposed_r2(self._lo(national=0.0, spatial=0.0))
        for k in ("r2", "r2_national", "r2_within"):
            self.assertLessEqual(d[k], 0.02, k)

    def test_score_combo_reports_r2_beside_rrmse(self):
        from geocif.experiments.s2s_africa import edge_table, score_combo

        lo = self._lo(national=1.0, spatial=0.3)
        lo["anom"] = lo["obs"] / lo["trend"] - 1
        anoms = lo[["fnid", "year", "obs", "trend", "anom"]]
        s = score_combo(lo, anoms, edge_table(anoms))
        for k in ("rrmse", "rrmse_trend", "r2", "r2_national", "r2_within"):
            self.assertIn(k, s, k)


class TestTrendExtrapolation(unittest.TestCase):
    """A t/ha number needs a trend LEVEL for the pending season, and these
    records end from 2010 to 2024. Measuring the extrapolation is what makes
    publishing anomalies a stated choice rather than an omission."""

    def _obs(self, last_year, slope=0.05, n=25):
        rows = []
        for u in ("A", "B", "C"):
            for i, y in enumerate(range(last_year - n + 1, last_year + 1)):
                rows.append({"fnid": u, "year": y,
                             "obs": 2.0 + slope * i})
        return pd.DataFrame(rows)

    def test_reports_the_horizon_actually_required(self):
        from geocif.experiments.s2s_africa import trend_extrapolation

        # Madagascar's real case: record ends 2010, forecast 2027
        r = trend_extrapolation(self._obs(2010), 2027)
        self.assertEqual(r["extrap_years"], 17)
        r = trend_extrapolation(self._obs(2024), 2027)
        self.assertEqual(r["extrap_years"], 3)

    def test_a_clean_linear_record_extrapolates_almost_exactly(self):
        """Sanity floor: on a noiseless straight line the backtest error
        must be ~0, so a large reported error means the record, not the
        method."""
        from geocif.experiments.s2s_africa import trend_extrapolation

        r = trend_extrapolation(self._obs(2020, slope=0.05), 2027)
        self.assertLess(r["trend_extrap_err_pct"], 1.0)
        self.assertGreater(r["extrap_units"], 0)

    def test_short_records_are_skipped_not_guessed(self):
        from geocif.experiments.s2s_africa import trend_extrapolation

        r = trend_extrapolation(self._obs(2020, n=6), 2027)
        self.assertEqual(r["extrap_units"], 0)
        self.assertNotIn("trend_extrap_err_pct", r)


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
        # and it must reject, not merely record
        tail = src[i_gate:i_gate + 1200]
        self.assertIn('status="too_short"', tail)
        self.assertIn("excluded.append(rec)", tail)

    def test_gate_counts_SCORABLE_years_not_training_years(self):
        """Gating on the training frame is not enough, and 0.4.1002 got this
        wrong: Kenya Short has enough TRAINING years but only 8 inside the
        1995-2016 evaluation span, so no amount of training data makes its
        skill measurable — its national AUC is undefined. The gate has to
        count the joined years that actually produce LOYO folds."""
        import inspect
        from geocif.experiments import s2s_africa as sa

        src = inspect.getsource(sa.run)
        self.assertIn("scorable = sorted(set(train.year) & set(eval_years))",
                      src)
        self.assertIn("min(n_train_years, len(scorable)) < MIN_YEARS", src)

    def test_scorable_year_count_is_the_intersection(self):
        """The quantity the gate rests on, computed directly."""
        eval_years = list(range(1995, 2017))
        # Kenya: record reaches 2024, but the S2S join leaves these years
        joined = [1996, 1999, 2003, 2008, 2012, 2015, 2019, 2021, 2022, 2024]
        scorable = sorted(set(joined) & set(eval_years))
        self.assertEqual(len(scorable), 6)          # only 6 produce folds
        self.assertEqual(len(joined), 10)           # training looks healthier
        self.assertLess(len(scorable), 12)          # gate rejects
        # and the national tercile needs >= 9 to exist at all
        self.assertLess(len(scorable), 9)

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
        i_has = src.find("has_skill = _gate(")
        self.assertGreater(i_has, i_sk)

    def test_skill_gate_prefers_the_permutation_test_over_a_threshold(self):
        """0.5 is never the benchmark: the LOYO null sits near 0.445. When a
        permutation p-value exists the gate uses it; with n_perm=0 it falls
        back to Anderson et al.'s ROC > 0.6, not to 0.5.

        The ROC bar is the weaker test — on a 22-year record with ~7 low
        years a PURE NOISE region clears 0.6 about 22% of the time (the AUC
        sampling sd is 0.135) — so it must never take precedence when a
        p-value is available.
        """
        import inspect
        from geocif.experiments import s2s_africa as sa

        src = inspect.getsource(sa.run)
        self.assertIn("sk[p_key] < PERM_ALPHA", src)
        self.assertIn("SKILL_ROC_THRESHOLD", src)
        self.assertNotIn('sk["auc"] > 0.5', src)
        self.assertLessEqual(sa.PERM_ALPHA, 0.05)
        self.assertEqual(sa.SKILL_ROC_THRESHOLD, 0.6)
        # the p-value branch must come first inside _gate
        gate = src[src.find("def _gate("):]
        self.assertLess(gate.find("PERM_ALPHA"), gate.find("SKILL_ROC_THRESHOLD"))


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


class TestPerRegionSkill(unittest.TestCase):
    """The map hatches per polygon, so each region needs its OWN verdict.

    A country-level flag paints every region with one brush: South Africa
    was stamped "no skill" wholesale while four Highveld provinces carried
    the signal (North West 0.857, Free State 0.752, Gauteng 0.717).
    """

    def _lo(self, good_units, seed=3):
        """Units in `good_units` get a real signal, the rest get noise."""
        rng = np.random.default_rng(seed)
        rows = []
        for u in [f"U{i}" for i in range(6)]:
            for y in range(1995, 2017):
                a = float(rng.normal())
                ah = (0.9 * a if u in good_units else float(rng.normal()))
                rows.append({"fnid": u, "year": y, "anom": a,
                             "obs": 2.0 * (1 + a), "trend": 2.0, "ahat": ah})
        return pd.DataFrame(rows)

    def test_only_the_informed_regions_are_marked_skilful(self):
        from geocif.experiments.s2s_africa import edge_table, per_region_skill

        lo = self._lo({"U0", "U1"})
        anoms = lo[["fnid", "year", "obs", "trend", "anom"]]
        r = per_region_skill(lo, anoms, edge_table(anoms))
        # informed regions must be found
        self.assertEqual(r["U0"]["region_skill"], "skill")
        self.assertEqual(r["U1"]["region_skill"], "skill")
        self.assertGreater(r["U0"]["region_auc"], 0.6)
        # Noise regions are NOT asserted individually: with ~22 years and
        # ~7 low-tercile events a pure-noise region clears ROC > 0.6 about
        # 22% of the time (sd of the AUC is 0.135), so a bare threshold
        # mislabels roughly one noise region in five. Assert the informed
        # ones score higher than the noise ones instead.
        good = np.mean([r[u]["region_auc"] for u in ("U0", "U1")])
        noise = np.mean([r[u]["region_auc"] for u in ("U2", "U3", "U4", "U5")])
        self.assertGreater(good, noise + 0.2)

    def test_unjudgeable_regions_are_insufficient_not_no_skill(self):
        """Marking a region we cannot score as "no skill" claims more than
        the record supports, so it gets its own state.

        The trigger is a short record or a degenerate event count (0 makes
        the AUC undefined, 1 gives sd 0.30) — NOT a "too few events" cut,
        which the noise simulation showed has no cliff to justify it.
        """
        from geocif.experiments.s2s_africa import (
            MIN_LOW_YEARS, MIN_YEARS, edge_table, per_region_skill)

        lo = self._lo(set())
        anoms = lo[["fnid", "year", "obs", "trend", "anom"]]
        r = per_region_skill(lo, anoms, edge_table(anoms))
        for u, rec in r.items():
            unjudgeable = (rec["region_n_years"] < MIN_YEARS
                           or rec["region_n_low"] < MIN_LOW_YEARS
                           or rec.get("region_auc") is None)
            self.assertEqual(rec["region_skill"] == "insufficient",
                             unjudgeable, u)

    def test_forecast_rows_carry_the_region_verdict(self):
        import inspect
        from geocif.experiments import s2s_africa as sa

        src = inspect.getsource(sa.run)
        self.assertIn("reg_skill = per_region_skill(", src)
        self.assertIn("reg_skill.get(r.fnid", src)


class TestSkillGateFallsBackToRocThreshold(unittest.TestCase):
    """With the permutation test switched off (n_perm=0) the gate becomes
    Anderson et al.'s ROC > 0.6 rather than silently passing everything."""

    def test_gate_uses_the_threshold_when_no_p_value(self):
        import inspect
        from geocif.experiments import s2s_africa as sa

        src = inspect.getsource(sa.run)
        self.assertIn("def _gate(", src)
        self.assertIn("SKILL_ROC_THRESHOLD", src)
        self.assertEqual(sa.SKILL_ROC_THRESHOLD, 0.6)


class TestDegenerateTercileEdges(unittest.TestCase):
    """pd.qcut(duplicates="drop") collapses bins when anomalies tie, and
    nothing raises — the labels just stop being terciles. With constant
    yields EVERY year comes back "low". Those folds must be excluded, not
    scored against a boundary that no longer means what it says."""

    def _anoms(self, vals):
        return pd.DataFrame({
            "fnid": ["A"] * len(vals),
            "year": list(range(2000, 2000 + len(vals))),
            "obs": [2.0 * (1 + v) for v in vals],
            "trend": [2.0] * len(vals),
            "anom": vals,
        })

    def test_constant_yields_produce_no_labels_at_all(self):
        from geocif.experiments.s2s_africa import edge_table

        tab = edge_table(self._anoms([0.0] * 20))
        self.assertEqual(len(tab), 0, "constant series must yield no labels")

    def test_heavily_tied_series_is_excluded(self):
        from geocif.experiments.s2s_africa import edge_table

        rng = np.random.default_rng(0)
        vals = [0.0] * 14 + list(rng.normal(size=6))
        tab = edge_table(self._anoms(vals))
        # a single inner edge is a median split, not a tercile
        for e, _ in tab.values():
            self.assertGreaterEqual(len(e), 2)

    def test_distinct_series_labels_about_a_third_low(self):
        from geocif.experiments.s2s_africa import edge_table

        rng = np.random.default_rng(1)
        tab = edge_table(self._anoms(list(rng.normal(size=24))))
        self.assertEqual(len(tab), 24)
        share = np.mean([ev for _, ev in tab.values()])
        self.assertGreater(share, 0.2)
        self.assertLess(share, 0.5)


class TestRegionGateIsRecordLength(unittest.TestCase):
    """The limit on a per-region AUC is record LENGTH, not event count.

    Measured on pure noise the AUC sd falls smoothly with events — 0.304
    (1), 0.220 (2), 0.185 (3), 0.166 (4), 0.152 (5), 0.139 (7) — with no
    cliff, so a low-event threshold is an arbitrary proxy. Regions it
    flagged had an ordinary low-year share (median 0.300) and merely short
    records (median 12 years vs 19).
    """

    def test_gate_is_on_years_with_only_a_degenerate_event_guard(self):
        import inspect
        from geocif.experiments import s2s_africa as sa

        src = inspect.getsource(sa.per_region_skill)
        self.assertIn('rec["region_n_years"] < MIN_YEARS', src)
        self.assertIn('rec["region_n_low"] < MIN_LOW_YEARS', src)
        # the event guard now covers only n_low of 0 (AUC undefined) and 1
        self.assertEqual(sa.MIN_LOW_YEARS, 2)
        self.assertGreaterEqual(sa.MIN_YEARS, 12)

    def test_short_record_is_insufficient_even_with_enough_events(self):
        from geocif.experiments.s2s_africa import edge_table, per_region_skill

        rng = np.random.default_rng(4)
        rows = []
        for u, n in (("SHORT", 11), ("LONG", 22)):
            for i in range(n):
                a = float(rng.normal())
                rows.append({"fnid": u, "year": 2000 + i, "anom": a,
                             "obs": 2.0 * (1 + a), "trend": 2.0,
                             "ahat": float(rng.normal())})
        lo = pd.DataFrame(rows)
        anoms = lo[["fnid", "year", "obs", "trend", "anom"]]
        r = per_region_skill(lo, anoms, edge_table(anoms))
        self.assertEqual(r["SHORT"]["region_skill"], "insufficient")
        self.assertNotEqual(r["LONG"]["region_skill"], "insufficient")
        # and the short one was excluded for LENGTH, not for lack of events
        self.assertGreaterEqual(r["SHORT"]["region_n_low"], 2)
