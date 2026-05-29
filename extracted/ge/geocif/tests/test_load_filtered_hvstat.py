"""Regression tests for the DRY refactor of HvStat production-system
handling.

After the refactor:
  - ``geocif.ml.stats.STANDARD_PRODUCTION_SYSTEMS`` is the single
    whitelist used by both ``add_statistics`` and ``load_filtered_hvstat``.
  - ``geocif.ml.stats.aggregate_yield_across_ps`` is the single
    area-weighted aggregator used by both.
  - ``load_filtered_hvstat`` now drops non-whitelisted PS rows AND
    collapses multi-PS rows per (country, admin, crop, season, year)
    via the aggregator, then sets ``crop_production_system="aggregated"``
    as a single synthetic value.

Tests cover the helper in isolation and the loader end-to-end against
synthetic CSVs that mirror the HvStat Africa schema.
"""
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

from geocif.ml.stats import (
    STANDARD_PRODUCTION_SYSTEMS,
    aggregate_yield_across_ps,
)
from geocif.production_analysis._common import load_filtered_hvstat


_HVSTAT_COLUMNS = [
    "fnid", "country", "country_code", "admin_1", "admin_2",
    "product", "season_name",
    "planting_year", "planting_month", "harvest_year", "harvest_month",
    "crop_production_system", "qc_flag",
    "area", "production", "yield",
]


def _make_row(
    fnid="ZZ001",
    country="Testland",
    country_code="ZZ",
    admin_1="Region1",
    admin_2="none",
    product="Maize",
    season_name="Main",
    harvest_year=2020,
    crop_production_system="rainfed",
    qc_flag=0,
    area=1000.0,
    production=2000.0,
    yield_val=2.0,
):
    return {
        "fnid": fnid,
        "country": country,
        "country_code": country_code,
        "admin_1": admin_1,
        "admin_2": admin_2,
        "product": product,
        "season_name": season_name,
        "planting_year": harvest_year - 1,
        "planting_month": 5,
        "harvest_year": harvest_year,
        "harvest_month": 1,
        "crop_production_system": crop_production_system,
        "qc_flag": qc_flag,
        "area": area,
        "production": production,
        "yield": yield_val,
    }


def _write_csv(tmpdir: Path, rows):
    path = tmpdir / "hvstat_synthetic.csv"
    df = pd.DataFrame(rows, columns=_HVSTAT_COLUMNS)
    df.to_csv(path, index=False)
    return path


class StandardProductionSystemsTests(unittest.TestCase):

    def test_constant_is_iterable_of_strings(self):
        self.assertGreater(len(STANDARD_PRODUCTION_SYSTEMS), 0)
        for ps in STANDARD_PRODUCTION_SYSTEMS:
            self.assertIsInstance(ps, str)

    def test_contains_canonical_labels(self):
        """The 10 labels documented in stats.py should all be present."""
        for ps in (
            "none", "Small-scale (PS)", "Commercial (PS)", "Communal (PS)",
            "All (PS)", "irrigated", "rainfed", "Rainfed (PS)",
            "agro_pastoral", "riverine",
        ):
            self.assertIn(ps, STANDARD_PRODUCTION_SYSTEMS)


class AggregateYieldAcrossPsTests(unittest.TestCase):

    def test_two_ps_combined_via_total_prod_over_total_area(self):
        """rainfed (1000 ha, 1500 t) + irrigated (500 ha, 2000 t) →
        total_prod=3500 / total_area=1500 = 2.333... t/ha"""
        agg_y, total_a, total_p = aggregate_yield_across_ps(
            pd.Series([1.5, 4.0]),
            pd.Series([1000.0, 500.0]),
            pd.Series([1500.0, 2000.0]),
        )
        self.assertAlmostEqual(agg_y, 3500.0 / 1500.0, places=6)
        self.assertAlmostEqual(total_a, 1500.0)
        self.assertAlmostEqual(total_p, 3500.0)

    def test_single_row_passthrough(self):
        """1-row group should return that row's yield unchanged."""
        agg_y, total_a, total_p = aggregate_yield_across_ps(
            pd.Series([2.5]), pd.Series([800.0]), pd.Series([2000.0]),
        )
        self.assertAlmostEqual(agg_y, 2.5, places=6)
        self.assertAlmostEqual(total_a, 800.0)
        self.assertAlmostEqual(total_p, 2000.0)

    def test_zero_and_inf_replaced_by_nan(self):
        """0, inf, -inf in any input should be treated as NaN
        (matches the legacy add_statistics behaviour)."""
        agg_y, total_a, total_p = aggregate_yield_across_ps(
            pd.Series([2.0, np.inf]),
            pd.Series([1000.0, 0.0]),
            pd.Series([2000.0, -np.inf]),
        )
        # Only the first row contributes — second row's 0 area + inf prod
        # are NaN'd. Result is row-1: prod=2000 / area=1000 = 2.0.
        self.assertAlmostEqual(agg_y, 2.0, places=6)
        self.assertAlmostEqual(total_a, 1000.0)
        self.assertAlmostEqual(total_p, 2000.0)

    def test_all_nan_returns_nan(self):
        agg_y, total_a, total_p = aggregate_yield_across_ps(
            pd.Series([np.nan, np.nan]),
            pd.Series([np.nan, np.nan]),
            pd.Series([np.nan, np.nan]),
        )
        self.assertTrue(np.isnan(agg_y))
        self.assertEqual(total_a, 0)  # sum(skipna=True) of all-NaN = 0
        self.assertEqual(total_p, 0)

    def test_area_only_branch_uses_area_weighted_yield(self):
        """When prod is all-NaN but yield + area both have values,
        the helper falls through to area-weighted yield mean:
        (y1*a1 + y2*a2) / (a1 + a2)."""
        agg_y, total_a, total_p = aggregate_yield_across_ps(
            pd.Series([2.0, 3.0]),
            pd.Series([1000.0, 500.0]),
            pd.Series([np.nan, np.nan]),
        )
        expected = (2.0 * 1000.0 + 3.0 * 500.0) / 1500.0
        self.assertAlmostEqual(agg_y, expected, places=6)


class LoadFilteredHvstatTests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.tmpdir = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)

    def test_qc_flag_zero_filter(self):
        path = _write_csv(self.tmpdir, [
            _make_row(harvest_year=2020, qc_flag=0, yield_val=2.0),
            _make_row(harvest_year=2021, qc_flag=1, yield_val=2.5),
        ])
        df = load_filtered_hvstat(path)
        self.assertEqual(len(df), 1)
        self.assertEqual(int(df.iloc[0]["harvest_year"]), 2020)

    def test_yield_positive_filter(self):
        path = _write_csv(self.tmpdir, [
            _make_row(harvest_year=2020, yield_val=2.0),
            _make_row(harvest_year=2021, yield_val=0.0),
            _make_row(harvest_year=2022, yield_val=-1.5),
            _make_row(harvest_year=2023, yield_val=float("nan"),
                      production=float("nan"), area=float("nan")),
        ])
        df = load_filtered_hvstat(path)
        self.assertEqual(len(df), 1)
        self.assertEqual(int(df.iloc[0]["harvest_year"]), 2020)

    def test_non_whitelisted_ps_dropped(self):
        """LSCF (PS) and dam irrigation are not in the whitelist and
        should disappear; rainfed survives."""
        path = _write_csv(self.tmpdir, [
            _make_row(harvest_year=2020, crop_production_system="rainfed"),
            _make_row(harvest_year=2021, crop_production_system="LSCF (PS)"),
            _make_row(harvest_year=2022, crop_production_system="dam irrigation"),
            _make_row(harvest_year=2023, crop_production_system="A1 (PS)"),
        ])
        df = load_filtered_hvstat(path)
        self.assertEqual(len(df), 1)
        self.assertEqual(int(df.iloc[0]["harvest_year"]), 2020)
        # After aggregation, PS column is synthetic.
        self.assertEqual(df.iloc[0]["crop_production_system"], "aggregated")

    def test_multi_ps_aggregated_within_series_year(self):
        """Same (country, admin, crop, season, year) with rainfed + irrigated
        → ONE row in the output, yield = total_prod / total_area."""
        rows = [
            _make_row(
                harvest_year=2020, crop_production_system="rainfed",
                area=1000.0, production=1500.0, yield_val=1.5,
            ),
            _make_row(
                harvest_year=2020, crop_production_system="irrigated",
                area=500.0, production=2000.0, yield_val=4.0,
            ),
        ]
        path = _write_csv(self.tmpdir, rows)
        df = load_filtered_hvstat(path)
        self.assertEqual(len(df), 1)
        self.assertAlmostEqual(
            df.iloc[0]["yield"], 3500.0 / 1500.0, places=6,
        )
        self.assertAlmostEqual(df.iloc[0]["area"], 1500.0)
        self.assertAlmostEqual(df.iloc[0]["production"], 3500.0)
        self.assertEqual(df.iloc[0]["crop_production_system"], "aggregated")

    def test_different_years_kept_separate(self):
        """Aggregation is PER (key, year) — different years must not collapse."""
        rows = [
            _make_row(harvest_year=2018, yield_val=1.0, area=1000.0, production=1000.0),
            _make_row(harvest_year=2019, yield_val=2.0, area=1000.0, production=2000.0),
            _make_row(harvest_year=2020, yield_val=3.0, area=1000.0, production=3000.0),
        ]
        path = _write_csv(self.tmpdir, rows)
        df = load_filtered_hvstat(path)
        self.assertEqual(len(df), 3)
        years_yields = dict(zip(df["harvest_year"].astype(int), df["yield"]))
        self.assertAlmostEqual(years_yields[2018], 1.0, places=6)
        self.assertAlmostEqual(years_yields[2019], 2.0, places=6)
        self.assertAlmostEqual(years_yields[2020], 3.0, places=6)

    def test_admin_column_picks_admin_2_when_present(self):
        rows = [
            _make_row(harvest_year=2020, admin_2="none", admin_1="Region1"),
            _make_row(fnid="ZZ002", admin_1="Region2", admin_2="District2A",
                      harvest_year=2020),
        ]
        path = _write_csv(self.tmpdir, rows)
        df = load_filtered_hvstat(path)
        self.assertEqual(len(df), 2)
        by_fnid = {r["fnid"]: r["admin"] for _, r in df.iterrows()}
        self.assertEqual(by_fnid["ZZ001"], "Region1")
        self.assertEqual(by_fnid["ZZ002"], "District2A")

    def test_output_schema_drop_in_for_beast(self):
        """Output must carry every column beast_runner.run reads, so the
        existing pipeline doesn't break post-refactor."""
        from geocif.production_analysis.beast_runner import GROUP_KEYS
        path = _write_csv(self.tmpdir, [_make_row(harvest_year=2020)])
        df = load_filtered_hvstat(path)
        # GROUP_KEYS minus admin_level (beast_runner adds that after load).
        # admin_level is NOT added by load_filtered_hvstat for the hvstat
        # path (matches pre-refactor behaviour; runner sets it via
        # np.where on df["admin_2"]).
        for col in GROUP_KEYS:
            if col == "admin_level":
                continue  # added by beast_runner.run, not the loader
            self.assertIn(col, df.columns, f"missing column: {col}")
        for col in ("yield", "harvest_year", "qc_flag", "admin_1",
                    "admin_2", "admin", "area", "production"):
            self.assertIn(col, df.columns, f"missing column: {col}")

    def test_empty_after_filter_returns_empty_frame(self):
        """All rows have non-whitelisted PS → empty output, no crash."""
        path = _write_csv(self.tmpdir, [
            _make_row(harvest_year=2020, crop_production_system="A1 (PS)"),
            _make_row(harvest_year=2021, crop_production_system="LSCF (PS)"),
        ])
        df = load_filtered_hvstat(path)
        self.assertTrue(df.empty)


if __name__ == "__main__":
    unittest.main()
