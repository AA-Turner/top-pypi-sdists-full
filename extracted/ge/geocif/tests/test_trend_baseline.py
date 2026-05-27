"""Regression test for the `trend` vs `trend_all` baselines.

`trend`     : Theil-Sen on the trailing 12 past-only training years
              (Harvest Year < forecast_season). arxiv:2506.19046 sec 2.
`trend_all` : Theil-Sen on ALL training rows for the region (df_train
              already excludes the forecast year via LOOCV).

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

    def test_trend_uses_only_past_12_years(self):
        """`trend` restricts to Harvest Year < forecast_season AND .tail(12)."""
        stub = _build_stub(
            "trend", self.df_train_clean, "Yield (tn per ha)",
            self.forecast_season,
        )
        y_pred, _, _ = stub._predict_baseline(self.X_test, self.df_region)
        expected = -99.55 + 0.05 * float(self.forecast_season)
        self.assertTrue(np.allclose(y_pred, expected, atol=1e-9))
        self.assertEqual(y_pred.shape, (1,))

    def test_trend_all_uses_every_training_row(self):
        """`trend_all` uses the full df_train slice for the region."""
        stub = _build_stub(
            "trend_all", self.df_train_clean, "Yield (tn per ha)",
            self.forecast_season,
        )
        y_pred, _, _ = stub._predict_baseline(self.X_test, self.df_region)
        expected = -99.55 + 0.05 * float(self.forecast_season)
        self.assertTrue(np.allclose(y_pred, expected, atol=1e-9))

    def test_trend_vs_trend_all_disagree_when_recent_window_differs(self):
        """When early + late regimes have different slopes, trend (12 past
        rows) and trend_all (all 24 rows) give different predictions."""
        forecast_season = 2013
        early_years = list(range(2001, 2008))   # 7 pre-forecast, slope 0.02
        recent_years = list(range(2008, 2013))  # 5 pre-forecast, slope 0.20
        post_years = list(range(2014, 2026))    # 12 post-forecast, slope 0.20
        rows = []
        for y in early_years:
            rows.append(("A", 1, y, 0.5 + 0.02 * (y - 2000)))
        for y in recent_years + post_years:
            rows.append(("A", 1, y, 0.66 + 0.20 * (y - 2008)))
        df_train = pd.DataFrame(
            rows,
            columns=["Region", "Region_ID", "Harvest Year", "Yield (tn per ha)"],
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

        self.assertFalse(
            np.isclose(pred_trend[0], pred_trend_all[0], atol=1e-3),
            msg=(
                f"Expected trend ({pred_trend[0]}) and trend_all "
                f"({pred_trend_all[0]}) to disagree when early- vs late-"
                "period slopes differ."
            ),
        )

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

    def test_trend_falls_back_to_mean_under_three_rows(self):
        """`trend` with fewer than 3 past rows returns mean of available."""
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
