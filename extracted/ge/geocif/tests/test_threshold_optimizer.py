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


class SweepCsvPathTests(unittest.TestCase):
    """Regression: sweep_csv_path must hit the project-SUFFIXED dir_output,
    same path geoprepare.extract_sweep writes to. An earlier version of
    this method stripped the project_name segment based on a wrong
    assumption and produced silent "sweep CSV not found" warnings for
    every (country, crop, season) on the cluster (verified against
    Z:\\cmongp1\\GEO\\outputs\\geocif\\threshold_sweep\\... layout).
    """

    def test_path_includes_project_name_segment(self):
        from pathlib import Path
        stub = SimpleNamespace(
            dir_output=Path("/dir_output_root/geocif"),
            project_name="geocif",
        )
        stub.sweep_csv_path = MethodType(
            ThresholdOptimizer.sweep_csv_path, stub,
        )
        path = stub.sweep_csv_path("somalia", "maize", 1)
        expected = Path(
            "/dir_output_root/geocif/threshold_sweep/somalia/maize/"
            "somalia_maize_s1_sweep.csv"
        )
        self.assertEqual(str(path), str(expected))

    def test_path_does_not_strip_project_name(self):
        """Specifically guard against the prior bug: if dir_output ends
        with project_name, do NOT walk up to the parent."""
        from pathlib import Path
        stub = SimpleNamespace(
            dir_output=Path("/some/root/geocif"),
            project_name="geocif",
        )
        stub.sweep_csv_path = MethodType(
            ThresholdOptimizer.sweep_csv_path, stub,
        )
        path = stub.sweep_csv_path("kenya", "rice", 2)
        # Project name segment must be in the path.
        self.assertIn("/geocif/threshold_sweep/", str(path).replace("\\", "/"))
        # And the parent shortcut should NOT have been applied.
        self.assertNotEqual(
            str(path).replace("\\", "/"),
            "/some/root/threshold_sweep/kenya/rice/kenya_rice_s2_sweep.csv",
        )


class EmptyDfGuardTests(unittest.TestCase):
    """Regression: an empty aggregated DF (sweep CSV with 0 rows for
    some country/crop/season) used to crash add_GEOGLAM_statistics on
    df.loc[:, stat] = np.nan. The fix guards at two layers:

      - geocif.threshold_optimizer.join_yield short-circuits if df_agg
        is empty (returns df + NaN Yield column).
      - geocif.ml.stats.add_GEOGLAM_statistics guards df.empty at top
        as defense-in-depth for any other caller.
    """

    def test_add_GEOGLAM_statistics_handles_empty_df(self):
        """Passing an empty DF should return cleanly, not raise."""
        from geocif.ml.stats import add_GEOGLAM_statistics
        empty_df = pd.DataFrame(columns=["Region", "Harvest Year", "Season"])
        try:
            out = add_GEOGLAM_statistics(
                dir_stats="/nonexistent",  # never touched on empty input
                df=empty_df,
                stats=["Yield (tn per ha)"],
                method="",
                admin_zone="admin_1",
                crop="maize",
                country="testland",
            )
        except Exception as exc:  # noqa: BLE001
            self.fail(f"add_GEOGLAM_statistics raised on empty df: {exc}")
        self.assertTrue(out.empty)
        self.assertIn("Yield (tn per ha)", out.columns)

    def test_join_yield_short_circuits_on_empty_df_agg(self):
        """join_yield must not call add_statistics when the aggregated
        DF is empty — that path crashes downstream and was the bug."""
        from pathlib import Path
        empty_agg = pd.DataFrame(
            columns=["region", "region_id", "year", "direction", "threshold",
                     "fallback_used", "n_cells_used", "crop_fraction_mean",
                     "ndvi"],
        )
        stub = SimpleNamespace(
            dir_production_statistics=Path("/nonexistent"),
            parser=None,
            logger=logging.getLogger("test_threshold_optimizer"),
        )
        stub.join_yield = MethodType(ThresholdOptimizer.join_yield, stub)
        try:
            out = stub.join_yield(empty_agg, country="testland",
                                  crop="maize", admin_zone="admin_1", season=1)
        except Exception as exc:  # noqa: BLE001
            self.fail(f"join_yield raised on empty df_agg: {exc}")
        self.assertTrue(out.empty)
        self.assertIn("Yield (tn per ha)", out.columns)


class EmptyDfJoinedPipelineTests(unittest.TestCase):
    """Regression: when df_joined arrives at compute_metric with zero
    rows (e.g. yield join produced no matched years for a country not
    in HvStat), the downstream chain (compute_metric → rank_and_filter
    → compute_pooled) must survive intact. The user's cluster run hit
    KeyError: 'n_years' in rank_and_filter when Vietnam rice produced
    an empty df_joined — compute_metric returned a 0×0 DataFrame, so
    df["n_years"] threw."""

    def test_compute_metric_returns_stable_schema_on_empty_input(self):
        """Empty df_joined → empty df with the documented column set,
        not a 0×0 frame."""
        empty_joined = pd.DataFrame(columns=[
            "region", "direction", "threshold", "ndvi",
            "Yield (tn per ha)", "fallback_used",
        ])
        s = _stub(metric_name="pearson")
        out = s.compute_metric(empty_joined, var_col="ndvi")
        self.assertTrue(out.empty)
        for col in ("region", "direction", "threshold", "n_years",
                    "n_fallback_years", "metric_name", "metric_value"):
            self.assertIn(col, out.columns)

    def test_rank_and_filter_handles_empty_df_metric(self):
        """Even with the empty schema arriving from compute_metric,
        rank_and_filter must add trustworthy + rank_within_region
        columns instead of throwing on df["n_years"]."""
        empty_metric = pd.DataFrame(columns=[
            "region", "direction", "threshold",
            "n_years", "n_fallback_years",
            "metric_name", "metric_value",
        ])
        s = _stub(metric_name="pearson")
        out = s.rank_and_filter(empty_metric)
        self.assertTrue(out.empty)
        self.assertIn("trustworthy", out.columns)
        self.assertIn("rank_within_region", out.columns)

    def test_full_pipeline_chain_on_empty_input(self):
        """compute_metric → rank_and_filter → compute_pooled must NOT
        raise on a 0-row df_joined. Mirrors the Vietnam-rice crash
        from the cluster run."""
        empty_joined = pd.DataFrame(columns=[
            "region", "direction", "threshold", "ndvi",
            "Yield (tn per ha)", "fallback_used",
        ])
        s = _stub(metric_name="pearson")
        df_metric = s.compute_metric(empty_joined, var_col="ndvi")
        df_ranked = s.rank_and_filter(df_metric)
        df_pooled = s.compute_pooled(df_ranked)
        self.assertTrue(df_metric.empty)
        self.assertTrue(df_ranked.empty)
        self.assertTrue(df_pooled.empty)
        # All three must still carry the columns downstream code reads.
        self.assertIn("trustworthy", df_ranked.columns)
        self.assertIn("pooled_metric", df_pooled.columns)

    def test_compute_metric_missing_yield_column_returns_empty(self):
        """Regression: Sudan winter_wheat hit
        KeyError: 'Yield (tn per ha)' because add_statistics' hvstat
        path only adds the Yield column to groups that found a FEWSNET
        match — when zero match, the column never appears. compute_metric
        must short-circuit instead of accessing a missing column.
        """
        df_joined_no_yield = pd.DataFrame({
            "region": ["A"], "direction": ["floor"], "threshold": [20],
            "ndvi": [0.5], "fallback_used": [False],
            # NOTE: no "Yield (tn per ha)" column.
        })
        s = _stub(metric_name="pearson")
        out = s.compute_metric(df_joined_no_yield, var_col="ndvi")
        self.assertTrue(out.empty)
        for col in ("region", "direction", "threshold", "n_years",
                    "n_fallback_years", "metric_name", "metric_value"):
            self.assertIn(col, out.columns)


class CumulativeOutputsTests(unittest.TestCase):
    """Cross-country cumulative outputs read per-country *_pooled.csv
    files written by write_summary() and produce one plot + one table
    image (with companion CSVs) PER (crop, season) combo, plus a
    top-level lookup CSV mapping plots/tables to their data CSVs.

    Mocks the BaseGeo-dependent attributes (dir_output, today_tag,
    metric_name, do_plot, logger) via SimpleNamespace, writes synthetic
    pooled CSVs under a tempdir laid out like the real summary tree,
    then calls write_cumulative_outputs via bound method.
    """

    def setUp(self):
        import tempfile
        from pathlib import Path
        self.tmp = tempfile.TemporaryDirectory()
        self.tmproot = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)

    def _write_pooled(self, country, crop, season, rows):
        """rows: list of (direction, threshold, pooled_metric, n_regions_trusted)."""
        d = (
            self.tmproot / "ml" / "analysis" / "test_today"
            / "threshold_sweep_summary" / country / crop
        )
        d.mkdir(parents=True, exist_ok=True)
        df = pd.DataFrame(
            rows,
            columns=["direction", "threshold", "pooled_metric",
                     "n_regions_trusted"],
        )
        df["metric_name"] = "pearson"
        df["rank_pooled"] = df["pooled_metric"].rank(
            method="min", ascending=False,
        )
        df["country"] = country
        path = d / f"{country}_{crop}_s{season}_pooled.csv"
        df.to_csv(path, index=False)
        return path

    def _stub(self):
        s = SimpleNamespace(
            dir_output=self.tmproot,
            today_tag="test_today",
            metric_name="pearson",
            do_plot=True,
            logger=logging.getLogger("test_threshold_optimizer"),
        )
        s.cumulative_root = MethodType(
            ThresholdOptimizer.cumulative_root, s,
        )
        s._read_all_pooled_csvs = MethodType(
            ThresholdOptimizer._read_all_pooled_csvs, s,
        )
        s._write_one_cumulative_plot = MethodType(
            ThresholdOptimizer._write_one_cumulative_plot, s,
        )
        s._write_one_cumulative_table = MethodType(
            ThresholdOptimizer._write_one_cumulative_table, s,
        )
        s.write_cumulative_outputs = MethodType(
            ThresholdOptimizer.write_cumulative_outputs, s,
        )
        return s

    def test_writes_per_combo_plots_and_tables_plus_lookup(self):
        """Happy path: 3 series across 2 countries × 2 (crop, season)
        combos produces:
          - cumulative_maize_s1.{png,_plot_data.csv,_table.png,_table.csv}
          - cumulative_rice_s2.{png,_plot_data.csv,_table.png,_table.csv}
          - lookup_cumulative.csv mapping all 4 images to their CSVs.
        """
        self._write_pooled("togo", "maize", 1, [
            ("floor", 0, 0.30, 5), ("floor", 20, 0.45, 5), ("floor", 40, 0.35, 5),
            ("ceiling", 10, 0.20, 5), ("ceiling", 30, 0.25, 5),
        ])
        self._write_pooled("kenya", "maize", 1, [
            ("floor", 0, 0.15, 4), ("floor", 20, 0.25, 4),
            ("ceiling", 10, 0.10, 4),
        ])
        self._write_pooled("togo", "rice", 2, [
            ("floor", 0, 0.50, 6), ("floor", 20, 0.60, 6), ("floor", 40, 0.55, 6),
        ])
        stub = self._stub()
        stub.write_cumulative_outputs()

        cum_root = self.tmproot / "ml" / "analysis" / "test_today" / "threshold_sweep_summary"

        # Per-(crop, season) plot + table.
        for crop, season in [("maize", 1), ("rice", 2)]:
            self.assertTrue(
                (cum_root / f"cumulative_{crop}_s{season}.png").is_file(),
                f"missing plot PNG for {crop} s{season}",
            )
            self.assertTrue(
                (cum_root / f"cumulative_{crop}_s{season}_plot_data.csv").is_file(),
                f"missing plot data CSV for {crop} s{season}",
            )
            self.assertTrue(
                (cum_root / f"cumulative_{crop}_s{season}_table.png").is_file(),
                f"missing table PNG for {crop} s{season}",
            )
            self.assertTrue(
                (cum_root / f"cumulative_{crop}_s{season}_table.csv").is_file(),
                f"missing table CSV for {crop} s{season}",
            )

        # Old single-file path should NOT exist (we replaced it).
        self.assertFalse(
            (cum_root / "cumulative_all_countries.png").is_file(),
            "old single-PNG path should be gone",
        )

        # Lookup CSV present and has expected shape.
        lookup_path = cum_root / "lookup_cumulative.csv"
        self.assertTrue(lookup_path.is_file())
        lookup = pd.read_csv(lookup_path)
        for col in ("crop", "season", "kind", "image", "data_csv"):
            self.assertIn(col, lookup.columns)
        # 2 combos × (plot + table) = 4 rows.
        self.assertEqual(len(lookup), 4)
        self.assertEqual(set(lookup["kind"]), {"plot", "table"})

        # Per-(crop, season) plot CSV schema.
        df_plot = pd.read_csv(cum_root / "cumulative_maize_s1_plot_data.csv")
        for col in ("country", "crop", "season", "direction", "threshold",
                    "pooled_metric", "n_regions_trusted", "metric_name",
                    "is_best"):
            self.assertIn(col, df_plot.columns)
        # All rows are for maize/s1 (filter shouldn't leak rice rows).
        self.assertTrue((df_plot["crop"] == "maize").all())
        self.assertTrue((df_plot["season"] == 1).all())

        # Per-(crop, season) table CSV schema.
        df_table = pd.read_csv(cum_root / "cumulative_maize_s1_table.csv")
        for col in ("country", "floor_T", "floor_metric", "ceil_T",
                    "ceil_metric", "pick", "apply"):
            self.assertIn(col, df_table.columns)
        # Maize-s1 has togo + kenya only.
        self.assertEqual(set(df_table["country"]), {"togo", "kenya"})
        # Apply column should contain the paste-ready string for floor
        # picks; togo maize floor-best is at T=20 with r=0.45 (better
        # than its ceiling 0.25), so togo's pick is "floor".
        togo_row = df_table[df_table["country"] == "togo"].iloc[0]
        self.assertEqual(togo_row["pick"], "floor")
        self.assertEqual(togo_row["apply"], "floor = 20")

    def test_skips_when_no_pooled_csvs_found(self):
        """No pooled CSVs anywhere → warn + return, no outputs written."""
        stub = self._stub()
        try:
            stub.write_cumulative_outputs()
        except Exception as exc:  # noqa: BLE001
            self.fail(f"write_cumulative_outputs raised when no CSVs: {exc}")
        cum_root = self.tmproot / "ml" / "analysis" / "test_today" / "threshold_sweep_summary"
        # No PNGs, no lookup.
        self.assertFalse((cum_root / "lookup_cumulative.csv").exists())

    def test_skips_when_do_plot_is_false(self):
        """do_plot=False → no images, no CSVs, no errors."""
        self._write_pooled("togo", "maize", 1, [
            ("floor", 0, 0.30, 5), ("floor", 20, 0.45, 5),
        ])
        stub = self._stub()
        stub.do_plot = False
        stub.write_cumulative_outputs()
        cum_root = self.tmproot / "ml" / "analysis" / "test_today" / "threshold_sweep_summary"
        self.assertFalse((cum_root / "cumulative_maize_s1.png").is_file())
        self.assertFalse((cum_root / "cumulative_maize_s1_table.png").is_file())
        self.assertFalse((cum_root / "lookup_cumulative.csv").is_file())


class LoggerErrorSignatureTest(unittest.TestCase):
    """Regression: main() used to call self.logger.exception(...) which
    geocif.logger.Logger doesn't implement → AttributeError swallows the
    real per-combo crash. Make sure main() uses .error() now."""

    def test_main_uses_logger_error_not_exception(self):
        import inspect
        src = inspect.getsource(ThresholdOptimizer.main)
        # Match the call pattern with receiver, so the explanatory
        # comment mentioning `.exception()` in backticks doesn't trip
        # the check.
        self.assertNotIn(
            "self.logger.exception(", src,
            "main() must not use logger.exception — geocif's Logger has no such method",
        )
        self.assertIn(
            "self.logger.error(", src,
            "main() should log per-combo failures via self.logger.error()",
        )


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
