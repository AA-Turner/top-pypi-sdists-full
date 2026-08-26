"""Regression tests for the `null`, `trend`, and `trend_all` baselines.

`null`      : per-unit leave-one-out mean — mean of the unit's yields over
              ALL training years (df_train already excludes the held-out
              forecast year via LOOCV). Computed within each unit, never
              pooled across units.
`trend`     : per-unit Theil-Sen fit on ALL training years, extrapolated to
              the forecast season. Falls back to the unit mean below 10
              training years.
`trend_all` : same all-years Theil-Sen fit, but with a >= 3-year floor; kept
              as a feature source (use_trend_all_as_feature).

These tests exercise the dispatch branch in
``geocif.geocif.Geocif._predict_baseline`` via a bound-method stub so we
don't have to spin up the full Geocif class + config + DB.
"""
import logging
import unittest
from types import MethodType, SimpleNamespace

import numpy as np
import pandas as pd

from geocif.geocif import Geocif


def _build_stub(model_name, df_train, target, forecast_season):
    """Minimum surface needed by the ``trend`` / ``trend_all`` branch."""
    stub = SimpleNamespace(
        model_name=model_name,
        df_train=df_train,
        target=target,
        forecast_season=forecast_season,
        logger=logging.getLogger("test_trend_baseline"),
    )
    stub._predict_baseline = MethodType(Geocif._predict_baseline, stub)
    return stub


def _make_monotonic_df(region, years, slope, intercept):
    """One region, one row per year, yield = intercept + slope*year."""
    return pd.DataFrame({
        "Region": region,
        "Region_ID": 1,
        "Harvest Year": years,
        "Yield (tn per ha)": intercept + slope * np.asarray(years, dtype=float),
    })


class TrendBaselineTests(unittest.TestCase):
    """Regression tests for trend vs trend_all dispatch."""

    def setUp(self):
        # 25 yearly rows for region 'A', forecast year 2013 held out.
        # df_train spans 2001-2012 + 2014-2025 (24 rows) -- what
        # _prepare_train_test_split produces in real LOOCV. Yield is a
        # clean linear ramp y = 0.05*year - 99.55 so Theil-Sen recovers
        # slope=0.05 exactly on any monotonic subset.
        self.forecast_season = 2013
        years_train = [y for y in range(2001, 2026) if y != self.forecast_season]
        self.df_train_clean = _make_monotonic_df(
            region="A", years=years_train, slope=0.05, intercept=-99.55,
        )
        self.df_region = pd.DataFrame({
            "Region": ["A"], "Region_ID": [1],
            "Harvest Year": [self.forecast_season],
        })
        self.X_test = pd.DataFrame({"_dummy": [0.0]})

    def test_trend_fits_all_training_years(self):
        """`trend` fits Theil-Sen on ALL training years (pre- AND post-
        forecast), not a past-only / recent-12 window. On a two-regime series
        this makes `trend` agree exactly with `trend_all` and with a direct
        Theil-Sen fit over every training row."""
        from scipy.stats import theilslopes
        forecast_season = 2013
        rows = []
        for y in range(2001, 2013):        # 12 pre-forecast, gentle slope
            rows.append(("A", 1, y, 0.50 + 0.02 * (y - 2000)))
        for y in range(2014, 2026):        # 12 post-forecast, steep slope
            rows.append(("A", 1, y, 0.74 + 0.20 * (y - 2013)))
        df_train = pd.DataFrame(
            rows,
            columns=["Region", "Region_ID", "Harvest Year", "Yield (tn per ha)"],
        )
        df_region = pd.DataFrame({
            "Region": ["A"], "Region_ID": [1], "Harvest Year": [forecast_season],
        })
        X_test = pd.DataFrame({"_dummy": [0.0]})

        past = df_train.sort_values("Harvest Year")
        slope, intercept, _, _ = theilslopes(
            past["Yield (tn per ha)"].values,
            past["Harvest Year"].astype(float).values,
        )
        expected = intercept + slope * float(forecast_season)

        pred_trend, _, _ = _build_stub(
            "trend", df_train, "Yield (tn per ha)", forecast_season,
        )._predict_baseline(X_test, df_region)
        pred_trend_all, _, _ = _build_stub(
            "trend_all", df_train, "Yield (tn per ha)", forecast_season,
        )._predict_baseline(X_test, df_region)

        self.assertTrue(np.isclose(pred_trend[0], expected, atol=1e-9))
        self.assertTrue(np.isclose(pred_trend[0], pred_trend_all[0], atol=1e-9))
        self.assertEqual(pred_trend.shape, (1,))
        # A past-only fit (pre-forecast years alone) gives a different
        # extrapolation — proving `trend` no longer restricts to that window.
        pre = past[past["Harvest Year"] < forecast_season]
        ps_slope, ps_intercept, _, _ = theilslopes(
            pre["Yield (tn per ha)"].values,
            pre["Harvest Year"].astype(float).values,
        )
        past_only_pred = ps_intercept + ps_slope * float(forecast_season)
        self.assertFalse(np.isclose(pred_trend[0], past_only_pred, atol=1e-3))

    def test_trend_all_uses_every_training_row(self):
        """`trend_all` uses the full df_train slice for the region."""
        stub = _build_stub(
            "trend_all", self.df_train_clean, "Yield (tn per ha)",
            self.forecast_season,
        )
        y_pred, _, _ = stub._predict_baseline(self.X_test, self.df_region)
        expected = -99.55 + 0.05 * float(self.forecast_season)
        self.assertTrue(np.allclose(y_pred, expected, atol=1e-9))

    def test_trend_and_trend_all_agree_with_enough_years(self):
        """With >= 10 training years, `trend` and `trend_all` fit the SAME
        rows (all training years) and therefore agree — the old past-only vs
        all-rows split is gone."""
        pred_t, _, _ = _build_stub(
            "trend", self.df_train_clean, "Yield (tn per ha)",
            self.forecast_season,
        )._predict_baseline(self.X_test, self.df_region)
        pred_ta, _, _ = _build_stub(
            "trend_all", self.df_train_clean, "Yield (tn per ha)",
            self.forecast_season,
        )._predict_baseline(self.X_test, self.df_region)
        self.assertTrue(np.isclose(pred_t[0], pred_ta[0], atol=1e-9))

    def test_trend_and_trend_all_share_min_years_guard(self):
        """`trend` and `trend_all` share one minimum training length: >= 5
        years, else the per-unit mean. Below the bar BOTH fall back; at or
        above it both fit a Theil-Sen slope.

        History: `trend` required 10 and `trend_all` 3 until 0.4.943. At ~10
        observed years per region the 10-year bar silently degraded `trend`
        into `null` on smallholder panels (Kenya admin_2: only 162/2845 rows
        differed from the mean), while 3 points made `trend_all`'s slope
        mostly noise."""
        forecast_season = 2013
        years = list(range(2005, 2009))  # 4 years -> below the shared bar
        df_train = _make_monotonic_df(
            "A", years, slope=0.05, intercept=-99.55,
        )
        df_region = pd.DataFrame({
            "Region": ["A"], "Region_ID": [1], "Harvest Year": [forecast_season],
        })
        X_test = pd.DataFrame({"_dummy": [0.0]})

        pred_trend, _, _ = _build_stub(
            "trend", df_train, "Yield (tn per ha)", forecast_season,
        )._predict_baseline(X_test, df_region)
        pred_trend_all, _, _ = _build_stub(
            "trend_all", df_train, "Yield (tn per ha)", forecast_season,
        )._predict_baseline(X_test, df_region)

        mean_expected = float(df_train["Yield (tn per ha)"].mean())
        # 4 training years is below the shared bar -> BOTH return the mean
        self.assertAlmostEqual(pred_trend[0], mean_expected, places=6)
        self.assertAlmostEqual(pred_trend_all[0], mean_expected, places=6)
        self.assertTrue(np.isclose(pred_trend[0], pred_trend_all[0]))

        # ... and at 5 years both fit the slope instead
        years5 = list(range(2005, 2010))  # 5 years
        df5 = _make_monotonic_df("A", years5, slope=0.05, intercept=-99.55)
        slope_expected = -99.55 + 0.05 * float(forecast_season)
        for name in ("trend", "trend_all"):
            pred, _, _ = _build_stub(
                name, df5, "Yield (tn per ha)", forecast_season,
            )._predict_baseline(X_test, df_region)
            self.assertAlmostEqual(pred[0], slope_expected, places=6, msg=name)

    def test_null_filters_by_region_not_region_id(self):
        """`null` must compute per-region mean using the admin name, NOT
        Region_ID — under cluster_strategy=single, Region_ID collapses to
        1 for every admin, which would yield a country-wide mean instead
        of a per-region one. Build df_train with two regions sharing
        Region_ID=1 (single-cluster scenario) but different admin names,
        and confirm null returns each region's OWN mean."""
        forecast_season = 2013
        df_train = pd.DataFrame({
            "Region": ["A"] * 5 + ["B"] * 5,
            "Region_ID": [1] * 10,  # single-cluster collapse
            "Harvest Year": list(range(2001, 2006)) * 2,
            "Yield (tn per ha)": [1.0, 1.0, 1.0, 1.0, 1.0,  # mean 1.0
                                  3.0, 3.0, 3.0, 3.0, 3.0],  # mean 3.0
        })
        X_test = pd.DataFrame({"_dummy": [0.0]})

        df_region_a = pd.DataFrame({
            "Region": ["A"], "Region_ID": [1], "Harvest Year": [forecast_season],
        })
        df_region_b = pd.DataFrame({
            "Region": ["B"], "Region_ID": [1], "Harvest Year": [forecast_season],
        })

        pred_a, _, _ = _build_stub(
            "null", df_train, "Yield (tn per ha)", forecast_season,
        )._predict_baseline(X_test, df_region_a)
        pred_b, _, _ = _build_stub(
            "null", df_train, "Yield (tn per ha)", forecast_season,
        )._predict_baseline(X_test, df_region_b)

        self.assertTrue(np.allclose(pred_a, 1.0))
        self.assertTrue(np.allclose(pred_b, 3.0))
        # If null had filtered by Region_ID, both would equal the
        # combined mean of 2.0 — guard against regression.
        self.assertFalse(np.allclose(pred_a, 2.0))
        self.assertFalse(np.allclose(pred_b, 2.0))

    def test_cluster_df_region_gets_per_admin_predictions(self):
        """Reproduces the togo soybean year-banding bug.

        Under cluster_strategy=auto_detect (or single), df_region arrives
        with rows for MULTIPLE admins sharing the same Region_ID.  The
        baseline dispatch used to grab df_region["Region"].iloc[0] and
        broadcast that single admin's fit to every row in the cluster,
        producing identical predictions for all admins in the same year
        (the visible year-banding stripes in the cid_vs_yield diagnostic).

        Each admin's prediction must be computed from its OWN training
        rows.  Build a two-admin df_region (cluster) and assert the
        predictions for each row come from the correct admin's data."""
        forecast_season = 2013
        # Two admins, different yield levels & trends.
        years_train = [y for y in range(2001, 2026) if y != forecast_season]
        df_train = pd.concat([
            _make_monotonic_df("A", years_train, slope=0.05, intercept=-99.55),
            _make_monotonic_df("B", years_train, slope=0.10, intercept=-200.0),
        ], ignore_index=True)
        # Cluster df_region: both admins, same Region_ID, single forecast year.
        df_region = pd.DataFrame({
            "Region": ["A", "B"],
            "Region_ID": [1, 1],
            "Harvest Year": [forecast_season, forecast_season],
        })
        # df_region positional indexing matters — assert 0..n-1 index.
        self.assertTrue((df_region.index == [0, 1]).all())
        X_test = pd.DataFrame({"_dummy": [0.0, 0.0]})

        expected_A = -99.55 + 0.05 * float(forecast_season)
        expected_B = -200.0 + 0.10 * float(forecast_season)

        for model_name in ("trend", "trend_all", "null"):
            with self.subTest(model_name=model_name):
                stub = _build_stub(
                    model_name, df_train, "Yield (tn per ha)", forecast_season,
                )
                y_pred, _, _ = stub._predict_baseline(X_test, df_region)
                if model_name == "null":
                    # null uses arithmetic mean of all training years
                    mean_A = -99.55 + 0.05 * np.mean(years_train)
                    mean_B = -200.0 + 0.10 * np.mean(years_train)
                    self.assertAlmostEqual(y_pred[0], mean_A, places=6)
                    self.assertAlmostEqual(y_pred[1], mean_B, places=6)
                    self.assertFalse(
                        np.isclose(y_pred[0], y_pred[1]),
                        msg="null collapsed both admins to the same value — "
                            "cluster-broadcast regression has returned.",
                    )
                else:
                    self.assertAlmostEqual(y_pred[0], expected_A, places=6)
                    self.assertAlmostEqual(y_pred[1], expected_B, places=6)
                    self.assertFalse(
                        np.isclose(y_pred[0], y_pred[1]),
                        msg=f"{model_name} collapsed both admins to the same "
                            "value — cluster-broadcast regression has returned.",
                    )

    def test_trend_all_feature_per_admin_column(self):
        """`_compute_trend_all_feature` writes a per-admin Theil-Sen slope
        evaluated at each row's Harvest Year into df_train/df_test["Trend All"].

        Two admins with DIFFERENT slopes must produce different values in the
        same forecast year — proving the feature isn't broadcasting a single
        admin's fit across all admins (the same cluster-broadcast bug pattern
        that hit the trend baseline)."""
        forecast_season = 2013
        years_train = [y for y in range(2001, 2026) if y != forecast_season]
        df_train = pd.concat([
            _make_monotonic_df("A", years_train, slope=0.05, intercept=-99.55),
            _make_monotonic_df("B", years_train, slope=0.10, intercept=-200.0),
        ], ignore_index=True)
        df_test = pd.DataFrame({
            "Region": ["A", "B"],
            "Region_ID": [1, 1],
            "Harvest Year": [forecast_season, forecast_season],
            "Yield (tn per ha)": [np.nan, np.nan],
        })
        stub = SimpleNamespace(
            use_trend_all_as_feature=True,
            check_yield_trend=False,
            df_train=df_train.copy(),
            df_test=df_test.copy(),
            target="Yield (tn per ha)",
            logger=logging.getLogger("test_trend_baseline"),
        )
        stub._compute_trend_all_feature = MethodType(
            Geocif._compute_trend_all_feature, stub,
        )
        stub._compute_trend_all_feature()

        self.assertIn("Trend All", stub.df_train.columns)
        self.assertIn("Trend All", stub.df_test.columns)

        a_pred = stub.df_test.loc[stub.df_test["Region"] == "A", "Trend All"].iloc[0]
        b_pred = stub.df_test.loc[stub.df_test["Region"] == "B", "Trend All"].iloc[0]
        self.assertAlmostEqual(a_pred, -99.55 + 0.05 * forecast_season, places=6)
        self.assertAlmostEqual(b_pred, -200.0 + 0.10 * forecast_season, places=6)
        self.assertFalse(
            np.isclose(a_pred, b_pred),
            msg="Trend All feature collapsed two admins to the same value.",
        )

    def test_trend_all_feature_disabled_by_flag(self):
        """No-op when ``use_trend_all_as_feature = False``."""
        stub = SimpleNamespace(
            use_trend_all_as_feature=False,
            check_yield_trend=False,
            df_train=pd.DataFrame({"Region": ["A"], "Yield (tn per ha)": [1.0]}),
            df_test=pd.DataFrame({"Region": ["A"]}),
            target="Yield (tn per ha)",
            logger=logging.getLogger("test_trend_baseline"),
        )
        stub._compute_trend_all_feature = MethodType(
            Geocif._compute_trend_all_feature, stub,
        )
        stub._compute_trend_all_feature()
        self.assertNotIn("Trend All", stub.df_train.columns)
        self.assertNotIn("Trend All", stub.df_test.columns)

    def test_trend_all_feature_skipped_when_check_yield_trend(self):
        """Skipped with warning when ``check_yield_trend = True``."""
        stub = SimpleNamespace(
            use_trend_all_as_feature=True,
            check_yield_trend=True,
            df_train=pd.DataFrame({"Region": ["A"], "Yield (tn per ha)": [1.0]}),
            df_test=pd.DataFrame({"Region": ["A"]}),
            target="Yield (tn per ha)",
            logger=logging.getLogger("test_trend_baseline"),
        )
        stub._compute_trend_all_feature = MethodType(
            Geocif._compute_trend_all_feature, stub,
        )
        stub._compute_trend_all_feature()
        self.assertNotIn("Trend All", stub.df_train.columns)

    def test_trend_falls_back_to_mean_below_min_years(self):
        """`trend` with fewer than 5 training years returns the mean of the
        available years rather than a fitted slope."""
        forecast_season = 2003
        df_train = pd.DataFrame({
            "Region": ["A", "A"],
            "Region_ID": [1, 1],
            "Harvest Year": [2001, 2002],
            "Yield (tn per ha)": [1.0, 3.0],
        })
        df_region = pd.DataFrame({
            "Region": ["A"], "Region_ID": [1], "Harvest Year": [forecast_season],
        })
        X_test = pd.DataFrame({"_dummy": [0.0]})
        stub = _build_stub(
            "trend", df_train, "Yield (tn per ha)", forecast_season,
        )
        y_pred, _, _ = stub._predict_baseline(X_test, df_region)
        self.assertTrue(np.allclose(y_pred, 2.0))


if __name__ == "__main__":
    unittest.main()
