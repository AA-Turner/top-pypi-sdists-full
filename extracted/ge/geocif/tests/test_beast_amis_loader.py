"""Regression tests for `geocif.production_analysis._common.load_filtered_amis`.

Asserts the AMIS loader produces output that is a drop-in replacement
for ``load_filtered_hvstat`` — same column contract, same admin /
yield-filter semantics — so the rest of the beast_* pipeline doesn't
need to know which source was used.
"""
import configparser
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

from geocif.production_analysis import _common
from geocif.production_analysis.beast_runner import GROUP_KEYS


def _make_amis_xlsx(
    path: Path,
    countries=("Argentina", "Brazil"),
    admin_1_by_country=None,
    years=(2000, 2001, 2002, 2003, 2004, 2005),
    yield_value_fn=None,
    write_yield=True,
    write_area=True,
    write_production=True,
):
    """Write a synthetic per-crop AMIS XLSX with 3 indicator sheets.

    Sheet layout (confirmed via direct inspection of the real
    maize_1.xlsx): ADM0_NAME | ADM1_NAME | ADM2_NAME | Season |
    Data Source | num_ID | <year_1> | <year_2> | ...
    """
    if admin_1_by_country is None:
        admin_1_by_country = {
            "Argentina": ["Buenos Aires", "Cordoba"],
            "Brazil": ["Mato Grosso"],
        }
    if yield_value_fn is None:
        def yield_value_fn(country, admin1, year):
            base = 3.0 if country == "Argentina" else 4.0
            return base + 0.1 * (year - years[0])

    rows = []
    for c in countries:
        for a1 in admin_1_by_country[c]:
            row = {
                "ADM0_NAME": c,
                "ADM1_NAME": a1,
                "ADM2_NAME": np.nan,
                "Season": "Main",
                "Data Source": "TEST",
                "num_ID": 0,
            }
            for y in years:
                row[y] = yield_value_fn(c, a1, y)
            rows.append(row)
    df_yield = pd.DataFrame(rows)

    df_area = df_yield.copy()
    df_prod = df_yield.copy()
    for y in years:
        df_area[y] = 1000.0
        df_prod[y] = df_yield[y] * 1000.0

    with pd.ExcelWriter(path, engine="openpyxl") as xw:
        if write_yield:
            df_yield.to_excel(xw, sheet_name="Yield (tn per ha)", index=False)
        if write_area:
            df_area.to_excel(xw, sheet_name="Area (ha)", index=False)
        if write_production:
            df_prod.to_excel(xw, sheet_name="Production (tn)", index=False)


def _make_parser(countries=("argentina", "brazil"), crops=None, seasons=(1,)):
    """Build a minimal ConfigParser the loader can consume."""
    if crops is None:
        crops = ["maize"]
    parser = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation()
    )
    parser["DEFAULT"] = {"countries": repr(list(countries))}
    for c in countries:
        parser[c] = {
            "crops": repr(crops),
            "seasons": repr(list(seasons)),
        }
    return parser


class AmisLoaderTests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.tmpdir = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        # Standard 2-country × 1-crop × 1-season fixture.
        _make_amis_xlsx(self.tmpdir / "maize_1.xlsx")
        self.parser = _make_parser()

    def test_schema_is_drop_in_replacement_for_hvstat(self):
        """Output must carry every column beast_runner.GROUP_KEYS expects
        + the yield/admin/year columns the per-series loop reads."""
        df = _common.load_filtered_amis(self.tmpdir, self.parser)
        self.assertFalse(df.empty, "loader returned empty frame on valid fixture")
        for col in GROUP_KEYS:
            self.assertIn(col, df.columns, f"missing GROUP_KEYS column: {col}")
        for col in ("yield", "harvest_year", "qc_flag", "admin_1", "admin_2",
                    "admin", "area", "production"):
            self.assertIn(col, df.columns, f"missing pipeline column: {col}")

    def test_yield_positive_filter_applied(self):
        """yield > 0 + notna filter must drop NaN / non-positive yield rows."""
        def yfn(country, admin1, year):
            if country == "Argentina" and admin1 == "Buenos Aires" and year == 2002:
                return np.nan
            if country == "Argentina" and admin1 == "Cordoba" and year == 2003:
                return -1.0
            return 3.0 + 0.1 * (year - 2000)
        _make_amis_xlsx(self.tmpdir / "maize_1.xlsx", yield_value_fn=yfn)
        df = _common.load_filtered_amis(self.tmpdir, self.parser)
        mask_bad = (
            ((df["country"] == "argentina") & (df["admin_1"] == "Buenos Aires")
             & (df["harvest_year"] == 2002))
            | ((df["country"] == "argentina") & (df["admin_1"] == "Cordoba")
               & (df["harvest_year"] == 2003))
        )
        self.assertEqual(mask_bad.sum(), 0,
                         "yield > 0 filter did not drop NaN/-1 rows")
        # qc_flag should be 0 everywhere — matches hvstat post-filter state.
        self.assertTrue((df["qc_flag"] == 0).all())

    def test_admin_column_collapses_admin_2_or_admin_1(self):
        """admin = admin_2 when present (!= 'none'), admin_1 otherwise.
        Match hvstat's _common.py:22 expression bit-for-bit."""
        # Default fixture has admin_2 NaN → should become "none" → admin_1 used.
        df = _common.load_filtered_amis(self.tmpdir, self.parser)
        self.assertTrue((df["admin_2"] == "none").all())
        self.assertTrue((df["admin"] == df["admin_1"]).all())

    def test_country_lowercase_normalized(self):
        """ADM0_NAME 'Argentina' → country 'argentina' so per-country
        boundary_file lookups in beast_spatial.py match."""
        df = _common.load_filtered_amis(self.tmpdir, self.parser)
        self.assertTrue(df["country"].isin({"argentina", "brazil"}).all())

    def test_synthetic_value_roundtrips(self):
        """Pull one (country, admin1, year) row and confirm the yield
        matches what we wrote into the synthetic XLSX."""
        df = _common.load_filtered_amis(self.tmpdir, self.parser)
        sub = df[
            (df["country"] == "argentina")
            & (df["admin_1"] == "Buenos Aires")
            & (df["harvest_year"] == 2003)
        ]
        self.assertEqual(len(sub), 1)
        # Synthetic value at year 2003 for Argentina: base 3.0 + 0.1 * (2003-2000) = 3.3
        self.assertAlmostEqual(float(sub.iloc[0]["yield"]), 3.3, places=6)

    def test_fnid_is_unique_per_series(self):
        """fnid must be unique per (country, admin_1, admin_2, season,
        product) — beast_runner uses it as a groupby key (with the rest
        of GROUP_KEYS), so duplicates would silently merge series."""
        df = _common.load_filtered_amis(self.tmpdir, self.parser)
        series_keys = df.groupby(GROUP_KEYS, observed=True).size().reset_index()
        # All series should be distinct rows.
        self.assertEqual(len(series_keys), 3)  # 2 admins in AR + 1 in BR

    def test_unique_xlsx_loaded_once_per_crop_season(self):
        """Two countries sharing crop=maize, season=1 should both pull
        from the same maize_1.xlsx — no FileNotFoundError or duplicate
        rows from double-reading."""
        df = _common.load_filtered_amis(self.tmpdir, self.parser)
        # 2 AR admins + 1 BR admin × 6 years = 18 rows
        self.assertEqual(len(df), 18)

    def test_missing_xlsx_returns_empty_with_warning(self):
        """Don't crash when a configured crop has no XLSX file present."""
        parser = _make_parser(crops=["nonexistent_crop"])
        df = _common.load_filtered_amis(self.tmpdir, parser)
        self.assertTrue(df.empty)

    def test_no_countries_in_parser_returns_empty(self):
        """Empty configuration → empty frame, no exception."""
        parser = configparser.ConfigParser(
            interpolation=configparser.ExtendedInterpolation()
        )
        df = _common.load_filtered_amis(self.tmpdir, parser)
        self.assertTrue(df.empty)

    def test_country_in_xlsx_but_not_in_config_dropped(self):
        """If the XLSX has Argentina + Brazil but config only requests
        Argentina, Brazil rows are dropped — keeps the loader output
        scoped to the analyst's intent."""
        parser = _make_parser(countries=("argentina",))
        df = _common.load_filtered_amis(self.tmpdir, parser)
        self.assertTrue((df["country"] == "argentina").all())
        self.assertEqual(df["country"].nunique(), 1)


if __name__ == "__main__":
    unittest.main()
