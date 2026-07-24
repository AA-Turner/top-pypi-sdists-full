"""Regression tests for the yield-outlook per-region metric maps.

Covers two things shipped together:

1. The title-case country-filter bug. ``_generate_diagnostics_for_stage``
   builds ``countries_display`` with ``str.title()`` — "united_states_of_america"
   becomes "United States Of America" (capital "Of"). The boundary shapefile
   stores the natural-English "United States of America" (lowercase "of").
   The original ``dg[dg["ADM0_NAME"].isin(countries_display)]`` was
   case-SENSITIVE, matched zero rows, and produced a blank choropleth
   (country outline + colorbar only, no filled regions). The fix lower-cases
   both sides.

2. ``diagnostics.metric_choropleth`` (RMSE / R² maps) and
   ``yield_outlook._plot_national_progression`` (national-only progression
   with a gray ±1 std band) exist with the expected shapes.
"""
import inspect
import sys
import types
import unittest

import pandas as pd

# ``geocif.yield_outlook`` imports ``geocif.viz.plot`` at module top, which
# imports ``pygeoutil.rgeo`` (a heavy geospatial extent helper present on the
# cluster but not required for these source-inspection tests). Stub it only if
# it is genuinely unavailable so the tests run in any environment.
try:  # pragma: no cover - environment dependent
    import pygeoutil  # noqa: F401
except ModuleNotFoundError:  # pragma: no cover
    _pg = types.ModuleType("pygeoutil")
    _rgeo = types.ModuleType("pygeoutil.rgeo")
    _rgeo.get_country_lat_lon_extent = lambda *a, **k: [-180, 180, -90, 90]
    _pg.rgeo = _rgeo
    sys.modules["pygeoutil"] = _pg
    sys.modules["pygeoutil.rgeo"] = _rgeo


class TestTitleCaseCountryFilter(unittest.TestCase):
    """The country name in the shapefile uses a lowercase connector word."""

    def setUp(self):
        # Mimic the boundary GeoDataFrame's ADM0_NAME column.
        self.dg = pd.DataFrame(
            {"ADM0_NAME": ["United States of America"] * 3 + ["Canada"]}
        )
        country = "united_states_of_america"
        # Exactly how _generate_diagnostics_for_stage builds it.
        self.countries_display = [country.title().replace("_", " ")]

    def test_titlecase_differs_from_shapefile_form(self):
        # Guards the premise: title() capitalises "of" -> "Of".
        self.assertEqual(self.countries_display, ["United States Of America"])
        self.assertNotIn("United States Of America", set(self.dg["ADM0_NAME"]))

    def test_buggy_case_sensitive_filter_is_empty(self):
        dg_sub = self.dg[self.dg["ADM0_NAME"].isin(self.countries_display)]
        self.assertEqual(len(dg_sub), 0)  # the original bug

    def test_fixed_case_insensitive_filter_matches(self):
        cd_lower = {c.lower() for c in self.countries_display}
        dg_sub = self.dg[self.dg["ADM0_NAME"].str.lower().isin(cd_lower)]
        self.assertEqual(len(dg_sub), 3)  # all three USA rows, Canada excluded

    def test_source_uses_case_insensitive_filter(self):
        from geocif import yield_outlook
        src = inspect.getsource(yield_outlook._generate_diagnostics_for_stage)
        self.assertIn('dg["ADM0_NAME"].str.lower().isin', src)
        # The exact buggy expression must be gone.
        self.assertNotIn('dg[dg["ADM0_NAME"].isin(countries_display)]', src)


class TestMetricMapAndProgressionExist(unittest.TestCase):
    def test_metric_choropleth_signature(self):
        from geocif.viz import diagnostics
        self.assertTrue(hasattr(diagnostics, "metric_choropleth"))
        params = inspect.signature(diagnostics.metric_choropleth).parameters
        for expected in ("col", "label", "vmin", "vmax", "higher_is_better"):
            self.assertIn(expected, params)

    def test_generate_diagnostics_renders_rmse_and_r2(self):
        from geocif import yield_outlook
        src = inspect.getsource(yield_outlook._generate_diagnostics_for_stage)
        self.assertIn("rmse_map_", src)
        self.assertIn("r2_map_", src)
        self.assertIn("metric_choropleth", src)

    def test_national_progression_exists_and_is_wired(self):
        from geocif import yield_outlook
        self.assertTrue(hasattr(yield_outlook, "_plot_national_progression"))
        allsrc = inspect.getsource(yield_outlook._plot_all_progressions)
        # One national-only call per metric.
        self.assertEqual(allsrc.count("_plot_national_progression("), 4)

    def test_national_progression_band_and_legend(self):
        from geocif import yield_outlook
        src = inspect.getsource(yield_outlook._plot_national_progression)
        self.assertIn("fill_between", src)          # gray std band
        self.assertIn('label="National"', src)      # no "area-weighted"
        self.assertNotIn("area-weighted", src)


if __name__ == "__main__":
    unittest.main()
