"""Tests for the geocif.agmet module."""

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Synthetic data factory
# ---------------------------------------------------------------------------

def _make_ccs_dataframe(regions=None, seasons=None, n_days=180):
    """Create a synthetic CCS-style DataFrame for testing.

    Mimics the structure produced by geoprepare extraction + agmet pipeline.
    Returns a DataFrame indexed by datetime with all columns expected by
    AgmetPlotter.
    """
    regions = regions or ["Region_A", "Region_B", "Region_C"]
    seasons = seasons or [2023, 2024, 2025]

    rows = []
    for region in regions:
        for season in seasons:
            base = pd.Timestamp(f"{season}-01-01")
            for i in range(n_days):
                dt = base + pd.Timedelta(days=i)
                if dt.month == 2 and dt.day == 29:
                    continue
                doy = dt.timetuple().tm_yday
                rows.append({
                    "region": region,
                    "calendar_region": "District_1" if region != "Region_C" else "District_2",
                    "country": "TestCountry",
                    "harvest_season": season,
                    "doy": doy,
                    "month": dt.month,
                    "day": dt.day,
                    "datetime": dt,
                    "crop_calendar": 1 if i < 30 else (2 if i < 120 else 3),
                    "ndvi": 0.3 + 0.4 * np.sin(np.pi * i / n_days) + np.random.normal(0, 0.02),
                    "gcvi": 1.0 + 0.5 * np.sin(np.pi * i / n_days) + np.random.normal(0, 0.02),
                    "cpc_tmax": 25 + 10 * np.sin(np.pi * i / n_days) + np.random.normal(0, 1),
                    "cpc_tmin": 10 + 5 * np.sin(np.pi * i / n_days) + np.random.normal(0, 1),
                    "chirps": max(0, np.random.exponential(3)),
                    "esi_4wk": 30 + np.random.normal(0, 5),
                    "soil_moisture_as1": 0.3 + np.random.normal(0, 0.05),
                    "soil_moisture_as2": 0.4 + np.random.normal(0, 0.05),
                    "yield": 2.5 + np.random.normal(0, 0.3) if season < max(seasons) else np.nan,
                    "production_share_pct": {
                        "Region_A": 45.0, "Region_B": 35.0, "Region_C": 20.0,
                    }.get(region, np.nan),
                })

    df = pd.DataFrame(rows)
    df.index = pd.to_datetime(df["datetime"])
    df.index.name = None
    return df


def _make_logo_files(tmpdir):
    """Create minimal PNG logo files for testing."""
    import struct
    import zlib

    def _minimal_png(path):
        """Write a 1x1 white PNG."""
        raw = b"\x00\xff\xff\xff"
        compressed = zlib.compress(raw)

        def chunk(ctype, data):
            c = ctype + data
            return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

        with open(path, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n")
            f.write(chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)))
            f.write(chunk(b"IDAT", compressed))
            f.write(chunk(b"IEND", b""))

    logo1 = Path(tmpdir) / "logo_harvest.png"
    logo2 = Path(tmpdir) / "logo_geoglam.png"
    _minimal_png(logo1)
    _minimal_png(logo2)
    return [logo1, logo2]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestAgmetPlotter(unittest.TestCase):
    """Tests for AgmetPlotter class."""

    @classmethod
    def setUpClass(cls):
        """Build shared synthetic data once for all tests."""
        np.random.seed(42)
        cls.df = _make_ccs_dataframe()
        cls.tmpdir = tempfile.mkdtemp()
        cls.logos = _make_logo_files(cls.tmpdir)

    def _make_plotter(self, **overrides):
        from geocif.agmet.plot import AgmetPlotter

        defaults = dict(
            df=self.df,
            names_cols=["ndvi", "cumulative_precip", "cpc_tmax", "daily_precip", "esi_4wk"],
            closest=[2023, 2024],
            dates_cal=[
                pd.Timestamp("2025-01-15"),
                pd.Timestamp("2025-02-15"),
                pd.Timestamp("2025-05-01"),
                pd.Timestamp("2025-06-01"),
            ],
            frcast_yr=2025,
            logos=self.logos,
            window=5,
            dir_out=Path(self.tmpdir) / "plots",
            sup_title="Test Region (District, Country)\nMaize 2025",
            fname="test_plot.png",
            production_pct=45.0,
        )
        defaults.update(overrides)
        return AgmetPlotter(**defaults)

    def test_plotter_creates_figure(self):
        """AgmetPlotter.plot() should produce a PNG file."""
        import matplotlib
        matplotlib.use("Agg")

        plotter = self._make_plotter()
        plotter.plot()

        out_path = Path(self.tmpdir) / "plots" / "test_plot.png"
        self.assertTrue(out_path.exists(), f"Expected output at {out_path}")
        self.assertGreater(out_path.stat().st_size, 0)

    def test_compute_historical_stats_shapes(self):
        """_compute_historical_stats should return arrays matching df_current length."""
        import matplotlib
        matplotlib.use("Agg")

        plotter = self._make_plotter()
        # Trigger df_previous computation (normally done in plot())
        plotter.df_previous = plotter.df[
            plotter.df["harvest_season"].isin(plotter.closest)
        ]

        result = plotter._compute_historical_stats("ndvi")
        self.assertEqual(len(result), 6)
        n = len(plotter.df_current)
        for arr in result[1:]:
            self.assertEqual(len(arr), n)

    def test_production_pct_none_no_error(self):
        """Plot should succeed when production_pct is None."""
        import matplotlib
        matplotlib.use("Agg")

        plotter = self._make_plotter(
            production_pct=None,
            fname="test_no_pct.png",
        )
        plotter.plot()

        out_path = Path(self.tmpdir) / "plots" / "test_no_pct.png"
        self.assertTrue(out_path.exists())

    def test_build_gefs_dataframe(self):
        """_build_gefs_dataframe should return a DataFrame with correct date range."""
        from geocif.agmet.plot import AgmetPlotter
        import datetime

        date1 = datetime.date(2025, 3, 1)
        date2 = datetime.date(2025, 3, 10)
        values = np.arange(10, dtype=float)

        result = AgmetPlotter._build_gefs_dataframe(date1, date2, values)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 10)
        self.assertIn("val", result.columns)

    def test_build_gefs_dataframe_mismatch(self):
        """_build_gefs_dataframe should return None on length mismatch."""
        from geocif.agmet.plot import AgmetPlotter
        import datetime

        date1 = datetime.date(2025, 3, 1)
        date2 = datetime.date(2025, 3, 10)
        values = np.arange(5, dtype=float)  # too short

        result = AgmetPlotter._build_gefs_dataframe(date1, date2, values)
        self.assertIsNone(result)


class TestExpandEoPlot(unittest.TestCase):
    """Tests for AgmetGeo._expand_eo_plot static method."""

    def test_ndvi_expansion(self):
        from geocif.agmet.geoagmet import AgmetGeo
        result = AgmetGeo._expand_eo_plot(["ndvi"])
        self.assertIn("ndvi", result)
        self.assertIn("yearly_ndvi", result)

    def test_chirps_expansion(self):
        from geocif.agmet.geoagmet import AgmetGeo
        result = AgmetGeo._expand_eo_plot(["chirps"])
        self.assertIn("cumulative_precip", result)
        self.assertIn("daily_precip", result)

    def test_passthrough(self):
        from geocif.agmet.geoagmet import AgmetGeo
        result = AgmetGeo._expand_eo_plot(["esi_4wk"])
        self.assertIn("esi_4wk", result)

    def test_cpc_tmax_absorbs_tmin(self):
        from geocif.agmet.geoagmet import AgmetGeo
        result = AgmetGeo._expand_eo_plot(["cpc_tmax", "cpc_tmin"])
        self.assertIn("cpc_tmax", result)
        self.assertNotIn("cpc_tmin", result)


class TestProductionShareComputation(unittest.TestCase):
    """Test the production share percentage logic."""

    def test_shares_sum_to_100(self):
        """Production shares across all regions should sum to ~100%."""
        df = _make_ccs_dataframe()
        shares = df.groupby("region")["production_share_pct"].first()
        self.assertAlmostEqual(shares.sum(), 100.0, places=1)

    def test_region_a_share(self):
        df = _make_ccs_dataframe()
        share_a = df[df["region"] == "Region_A"]["production_share_pct"].iloc[0]
        self.assertAlmostEqual(share_a, 45.0)


class TestAgmetUtils(unittest.TestCase):
    """Tests for geocif.agmet.utils functions."""

    def test_get_crop_abbrev(self):
        from geocif.agmet.utils import get_crop_abbrev
        self.assertEqual(get_crop_abbrev("maize"), "mz")
        self.assertEqual(get_crop_abbrev("Maize"), "mz")
        self.assertEqual(get_crop_abbrev("unknown_crop"), "unknown_crop")

    def test_sliding_mean(self):
        from geocif.agmet.utils import sliding_mean
        data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        result = sliding_mean(data, window=3)
        self.assertEqual(len(result), len(data))
        self.assertFalse(np.all(np.isnan(result)))

    def test_dict_vars_keys(self):
        from geocif.agmet.utils import dict_vars
        for key in ["ndvi", "chirps", "cpc_tmax", "cpc_tmin", "esi_4wk"]:
            self.assertIn(key, dict_vars)
            self.assertGreaterEqual(len(dict_vars[key]), 2)


if __name__ == "__main__":
    unittest.main()
