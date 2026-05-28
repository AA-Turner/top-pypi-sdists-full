"""Regression tests for `geocif.threshold_optimizer`.

The full ThresholdOptimizer requires a BaseGeo config with all the [PATHS]
entries, so we test the pure functions and method bodies in isolation
using SimpleNamespace stubs + bound methods — same pattern as
tests/test_trend_baseline.py.

What's covered:
  * detect_var_column — happy + error cases, alternate variable names
  * aggregate_seasonal — max + mean across DOY, fallback_used propagation
  * _pearson_abs / _loocv_rmse — basic math sanity
  * compute_metric → rank_and_filter → compute_pooled — end-to-end on a
    synthetic 2-region sweep with a planted signal at (floor, 20),
    verifying the pooled best is correctly identified
  * trustworthiness filter — high-fallback rows excluded from rank
"""
import logging
import unittest
from types import MethodType, SimpleNamespace

import numpy as np
import pandas as pd

from geocif.threshold_optimizer import ThresholdOptimizer, _NON_VAR_COLS


def _stub(metric_name="pearson", agg_method="max", max_fallback_share=0.3):
    """Minimum attrs needed by the methods under test."""
    s = SimpleNamespace(
        metric_name=metric_name,
        agg_method=agg_method,
        max_fallback_share=max_fallback_share,
        logger=logging.getLogger("test_threshold_optimizer"),
    )
    s.aggregate_seasonal = MethodType(ThresholdOptimizer.aggregate_seasonal, s)
    s.compute_metric = MethodType(ThresholdOptimizer.compute_metric, s)
    s.rank_and_filter = MethodType(ThresholdOptimizer.rank_and_filter, s)
    s.compute_pooled = MethodType(ThresholdOptimizer.compute_pooled, s)
    return s


def _build_sweep_df(
    regions=("A", "B"),
    years=(2018, 2019, 2020, 2021, 2022),
    doys=(180, 200, 220),
    floor_thresholds=(0, 10, 20, 30, 40, 50),
    ceil_thresholds=(50, 70, 90),
    var_col="ndvi",
    a_signal_threshold=20,
    a_signal_direction="floor",
    a_yields_by_year=None,
    fallback_seed=None,
):
    """Build a synthetic sweep CSV-shaped DataFrame.

    Region A: variable at (a_signal_direction, a_signal_threshold) is
    strongly linearly correlated with the synthetic yield via the
    a_yields_by_year map; all OTHER (direction, threshold) combos for
    region A are uncorrelated noise.

    Region B: variable is flat noise everywhere.
    """
    if a_yields_by_year is None:
        a_yields_by_year = {y: 2.0 + 0.5 * (i + 1) for i, y in enumerate(years)}

    rng = np.random.default_rng(fallback_seed or 7)
    rows = []
    for region in regions:
        for year in years:
            for doy in doys:
                for direction, thresholds in (
                    ("floor", floor_thresholds),
                    ("ceiling", ceil_thresholds),
                ):
                    for t in thresholds:
                        # Construct the variable value.
                        if (
                            region == "A"
                            and direction == a_signal_direction
                            and t == a_signal_threshold
                        ):
                            # Strong linear signal: var = 1000 * yield + ε
                            val = 1000.0 * a_yields_by_year[year] + rng.normal(0, 0.5)
                        else:
                            val = float(rng.normal(5000, 50))
                        rows.append({
                            "country": "synthland",
                            "region": region,
                            "region_id": 1 if region == "A" else 2,
                            "lat": 0.0,
                            "lon": 0.0,
                            "year": year,
                            "doy": doy,
                            var_col: val,
                            "direction": direction,
                            "threshold": t,
                            "fallback_used": False,
                            "n_cells_used": 100 - t if direction == "floor" else 100,
                            "crop_fraction_mean": float(t + 50),
                        })
    return pd.DataFrame(rows)


def _build_yield_df(regions=("A", "B"), years=(2018, 2019, 2020, 2021, 2022),
                    a_yields_by_year=None):
    if a_yields_by_year is None:
        a_yields_by_year = {y: 2.0 + 0.5 * (i + 1) for i, y in enumerate(years)}
    rng = np.random.default_rng(11)
    rows = []
    for region in regions:
        for year in years:
            if region == "A":
                y = a_yields_by_year[year]
            else:
                y = float(rng.normal(3.0, 0.05))
            rows.append({
                "Region": region,
                "Harvest Year": year,
                "Yield (tn per ha)": y,
            })
    return pd.DataFrame(rows)


class DetectVarColumnTests(unittest.TestCase):

    def test_detects_ndvi(self):
        df = pd.DataFrame(columns=list(_NON_VAR_COLS) + ["ndvi"])
        self.assertEqual(ThresholdOptimizer.detect_var_column(df), "ndvi")

    def test_detects_chirps(self):
        df = pd.DataFrame(columns=list(_NON_VAR_COLS) + ["chirps"])
        self.assertEqual(ThresholdOptimizer.detect_var_column(df), "chirps")

    def test_raises_on_zero_candidates(self):
        df = pd.DataFrame(columns=list(_NON_VAR_COLS))
        with self.assertRaisesRegex(ValueError, "Expected exactly 1"):
            ThresholdOptimizer.detect_var_column(df)

    def test_raises_on_multiple_candidates(self):
        df = pd.DataFrame(columns=list(_NON_VAR_COLS) + ["ndvi", "chirps"])
        with self.assertRaisesRegex(ValueError, "Expected exactly 1"):
            ThresholdOptimizer.detect_var_column(df)


class AggregateSeasonalTests(unittest.TestCase):

    def test_max_collapses_doy(self):
        df = pd.DataFrame({
            "region": ["A", "A", "A", "A"],
            "region_id": [1, 1, 1, 1],
            "year": [2020, 2020, 2020, 2020],
            "doy": [180, 200, 220, 240],
            "direction": ["floor", "floor", "floor", "floor"],
            "threshold": [20, 20, 20, 20],
            "fallback_used": [False, False, True, False],
            "n_cells_used": [50, 60, 5, 50],
            "crop_fraction_mean": [40, 40, 40, 40],
            "ndvi": [1.0, 2.0, 3.0, 1.5],
        })
        s = _stub(agg_method="max")
        out = s.aggregate_seasonal(df, var_col="ndvi")
        self.assertEqual(len(out), 1)
        row = out.iloc[0]
        self.assertEqual(row["ndvi"], 3.0)  # max of 1, 2, 3, 1.5
        self.assertTrue(row["fallback_used"])  # any() True
        self.assertAlmostEqual(row["n_cells_used"], (50 + 60 + 5 + 50) / 4)

    def test_mean_collapses_doy(self):
        df = pd.DataFrame({
            "region": ["A", "A"],
            "region_id": [1, 1],
            "year": [2020, 2020],
            "doy": [180, 200],
            "direction": ["floor", "floor"],
            "threshold": [20, 20],
            "fallback_used": [False, False],
            "n_cells_used": [50, 60],
            "crop_fraction_mean": [40, 40],
            "ndvi": [1.0, 3.0],
        })
        s = _stub(agg_method="mean")
        out = s.aggregate_seasonal(df, var_col="ndvi")
        self.assertEqual(out.iloc[0]["ndvi"], 2.0)


class MetricFunctionTests(unittest.TestCase):

    def test_pearson_perfect_correlation(self):
        x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y = 2.0 * x + 1.0
        self.assertAlmostEqual(ThresholdOptimizer._pearson_abs(x, y), 1.0, places=9)

    def test_pearson_zero_variance_returns_nan(self):
        x = np.array([1.0, 1.0, 1.0, 1.0])
        y = np.array([1.0, 2.0, 3.0, 4.0])
        self.assertTrue(np.isnan(ThresholdOptimizer._pearson_abs(x, y)))

    def test_pearson_too_few_finite_returns_nan(self):
        x = np.array([1.0, np.nan])
        y = np.array([2.0, np.nan])
        self.assertTrue(np.isnan(ThresholdOptimizer._pearson_abs(x, y)))

    def test_loocv_rmse_perfect_line_near_zero(self):
        x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y = 2.0 * x + 1.0
        rmse = ThresholdOptimizer._loocv_rmse(x, y)
        self.assertAlmostEqual(rmse, 0.0, places=6)

    def test_loocv_rmse_too_few_years_returns_nan(self):
        x = np.array([1.0, 2.0, 3.0])
        y = np.array([1.0, 4.0, 9.0])
        self.assertTrue(np.isnan(ThresholdOptimizer._loocv_rmse(x, y, min_years=5)))


class EndToEndPearsonTests(unittest.TestCase):
    """The point of the optimizer: identify the planted (direction, threshold)
    as the per-region best AND the pooled best."""

    def setUp(self):
        years = (2018, 2019, 2020, 2021, 2022)
        self.a_yields_by_year = {y: 2.0 + 0.5 * (i + 1) for i, y in enumerate(years)}
        self.sweep = _build_sweep_df(
            years=years,
            a_signal_threshold=20,
            a_signal_direction="floor",
            a_yields_by_year=self.a_yields_by_year,
        )
        self.yield_df = _build_yield_df(
            years=years, a_yields_by_year=self.a_yields_by_year,
        )

    def _join_to_yield(self, df_agg):
        """Stand-in for join_yield since the real one hits add_statistics
        which needs a real HarvestStat file. Pure pandas merge."""
        return df_agg.merge(
            self.yield_df, left_on=["region", "year"],
            right_on=["Region", "Harvest Year"], how="left",
        )

    def test_region_A_best_is_floor_20(self):
        s = _stub(metric_name="pearson")
        df_agg = s.aggregate_seasonal(self.sweep, var_col="ndvi")
        df_joined = self._join_to_yield(df_agg)
        df_metric = s.compute_metric(df_joined, var_col="ndvi")
        df_ranked = s.rank_and_filter(df_metric)

        region_a = df_ranked[df_ranked["region"] == "A"]
        best_a = region_a[region_a["rank_within_region"] == 1.0].iloc[0]
        self.assertEqual(best_a["direction"], "floor")
        self.assertEqual(int(best_a["threshold"]), 20)
        self.assertGreater(best_a["metric_value"], 0.99)

    def test_pooled_best_is_floor_20(self):
        s = _stub(metric_name="pearson")
        df_agg = s.aggregate_seasonal(self.sweep, var_col="ndvi")
        df_joined = self._join_to_yield(df_agg)
        df_metric = s.compute_metric(df_joined, var_col="ndvi")
        df_ranked = s.rank_and_filter(df_metric)
        df_pooled = s.compute_pooled(df_ranked)

        best = df_pooled.iloc[0]
        self.assertEqual(best["direction"], "floor")
        self.assertEqual(int(best["threshold"]), 20)

    def test_high_fallback_share_drops_trustworthy(self):
        # Flip fallback_used to True for >max_fallback_share of years
        # within ONE (region, direction, threshold) combo. That row
        # should be marked trustworthy=False even if its metric is good.
        sweep = self.sweep.copy()
        mask = (
            (sweep["region"] == "A")
            & (sweep["direction"] == "floor")
            & (sweep["threshold"] == 20)
            & (sweep["year"].isin([2018, 2019, 2020, 2021]))  # 4/5 = 80% > 30%
        )
        sweep.loc[mask, "fallback_used"] = True

        s = _stub(metric_name="pearson", max_fallback_share=0.3)
        df_agg = s.aggregate_seasonal(sweep, var_col="ndvi")
        df_joined = self._join_to_yield(df_agg)
        df_metric = s.compute_metric(df_joined, var_col="ndvi")
        df_ranked = s.rank_and_filter(df_metric)

        flagged_row = df_ranked[
            (df_ranked["region"] == "A")
            & (df_ranked["direction"] == "floor")
            & (df_ranked["threshold"] == 20)
        ].iloc[0]
        self.assertFalse(bool(flagged_row["trustworthy"]))
        # And it should not have a rank.
        self.assertTrue(pd.isna(flagged_row["rank_within_region"]))


class LOOCVMetricTests(unittest.TestCase):
    """Metric-flag plumbing — LOOCV path produces ascending ranks (smaller
    RMSE = better)."""

    def test_loocv_rmse_pooled_smaller_is_better(self):
        # Identical sweep, but use LOOCV metric.
        years = (2018, 2019, 2020, 2021, 2022)
        sweep = _build_sweep_df(
            years=years, a_signal_threshold=20, a_signal_direction="floor",
        )
        yield_df = _build_yield_df(years=years)
        s = _stub(metric_name="loocv_rmse")
        df_agg = s.aggregate_seasonal(sweep, var_col="ndvi")
        df_joined = df_agg.merge(
            yield_df, left_on=["region", "year"],
            right_on=["Region", "Harvest Year"], how="left",
        )
        df_metric = s.compute_metric(df_joined, var_col="ndvi")
        df_ranked = s.rank_and_filter(df_metric)
        df_pooled = s.compute_pooled(df_ranked)
        self.assertFalse(df_pooled.empty)
        # rank 1 = smallest pooled_metric (best RMSE).
        best = df_pooled.iloc[0]
        rest = df_pooled.iloc[1:]
        self.assertTrue((rest["pooled_metric"] >= best["pooled_metric"]).all())


if __name__ == "__main__":
    unittest.main()
