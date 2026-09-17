# -*- coding: utf-8 -*-
"""End-to-end tests for geocif/season_monitor.py (DESIGN.md sections 8 and 8.1).

The whole run happens in a temp tree on the REAL global 0.05 deg lattice, in the
same style as tests/test_phenology_inputs.py and
tests/test_phenology_climatology.py (the fixture builders are copied rather than
imported so this file states its own arithmetic):

    country box (35.5, -0.5, 37.5, 1.5) -> col_off = 215.5/0.05 = 4310
                                           row_off =  88.5/0.05 = 1770
                                           40 x 40 cells
    calendar zone + admin box (36.0, 0.0, 37.0, 1.0) -> rows 10..29, cols 10..29
    admin unit 1 = cols 10..19 ("West Unit"), unit 2 = cols 20..29 ("East Unit")

Calendar ``test_cal.xlsx``:

* ``maize_1``: ``apr_1 = 1``, ``apr_15 = 3`` -> planting Apr 1, harvest Apr 30.
* ``maize_2``: ``oct_15 .. dec_15 = 1``, ``jan_1/jan_15 = 2``, ``feb_1 = 3``
  -> the Kenya short rains shape: planting Oct 15 of ``harvest_year - 1``,
  harvest Feb 14 of ``harvest_year``.

``[SEASON_MONITOR]`` uses ``search_start_days_before_planting = 5``,
``validation_days = 10``, ``dry_spell_days = 5``, ``window_days = 3``,
``precip_threshold = 20``, ``min_valid_years = 3``, climatology 2001-2003.

Rain per harvest year (same shape as the climatology fixture): nothing, then
25 mm on the "start day" s and 5 mm/day for the next 15 days.

    cube index 0 = Mar 27, index 5 = Apr 1 (planting), index 34 = Apr 30

    2001: s = index 10 -> onset  5 days after planting
    2002: s = index 15 -> onset 10 days after planting (plus a false start on
          index 5, invalidated by the nine dry days that follow)
    2003: s = index 20 -> onset 15 days after planting

    climatological median onset = median(5, 10, 15) = 10 days after planting

The monitored run is harvest year 2003 as of **Apr 30 2003** (cube index 34,
n_obs = 35). The onset at index 20 confirms because 20 + 10 = 30 <= 35 and the
look-ahead [24, 29] is wet, so:

    onset_days        = 20 - 5 = 15
    onset_anomaly_days = 15 - 10 = +5  (positive = LATE)
    days_past_median   = NaN (no NOT_STARTED pixel)
    rain_30d (indices 5..34) = 25 + 14 x 5 = 95 mm
        2001 same window = 25 + 15 x 5       = 100 mm
        2002 same window = 25 + 25 + 15 x 5  = 125 mm   (the false start counts)
        -> 1 of 3 years at or below 95 mm -> percentile = 100/3 = 33.33
"""
import configparser
import datetime as dt
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

import numpy as np
import pandas as pd
import rasterio
from affine import Affine

from geocif import season_monitor
from geocif.phenology import inputs, monitor
from geocif.viz import phenology_maps

TILE_WEST, TILE_SOUTH, TILE_EAST, TILE_NORTH = 35.5, -0.5, 37.5, 1.5
TILE_TRANSFORM = Affine(0.05, 0, TILE_WEST, 0, -0.05, TILE_NORTH)
TILE_SHAPE = (40, 40)

CHIRPS_NODATA = -2147483648
FLOAT_NODATA = -9999.0

IN_ZONE = (15, 15)       # inside the calendar zone and admin unit 1
OUT_OF_ZONE = (0, 0)     # no calendar, no admin unit

MONTHS = ["jan", "feb", "mar", "apr", "may", "jun",
          "jul", "aug", "sep", "oct", "nov", "dec"]
BIN_COLS = [f"{m}_{d}" for m in MONTHS for d in (1, 15)]

CUBE_START = dt.date(2001, 3, 27)
CUBE_END = dt.date(2001, 5, 20)
ONSET_INDEX = {2001: 10, 2002: 15, 2003: 20}
PLANTING_INDEX = 5
CLIM_YEARS = (2001, 2002, 2003)

AS_OF = dt.date(2003, 4, 30)
SEASON = monitor.ActiveSeason("kenya", "maize", 1, 2003)


def _write_tile(path, array, dtype, nodata):
    """Write a 40x40 GeoTIFF aligned to the global 0.05 deg lattice."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    profile = {
        "driver": "GTiff", "dtype": dtype, "width": TILE_SHAPE[1],
        "height": TILE_SHAPE[0], "count": 1, "crs": "EPSG:4326",
        "transform": TILE_TRANSFORM, "nodata": nodata,
    }
    with rasterio.open(path, "w", **profile) as dst:
        dst.write(np.asarray(array).astype(dtype), 1)
    return path


def _bins(pairs, default=0):
    """Build a 24-bin flag row; ``pairs`` maps a bin column name to its flag."""
    row = {col: default for col in BIN_COLS}
    row.update(pairs)
    return row


def _stub_raster_map(grid_da, *, out_path, **kwargs):
    """Stand-in for the one pygmt call site: write a placeholder PNG."""
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(b"\x89PNG\r\n\x1a\n")
    return out


class SeasonMonitorFixture(unittest.TestCase):
    """Synthetic config file + raster tree, built once for the whole class."""

    @classmethod
    def setUpClass(cls):
        cls._tmp = TemporaryDirectory()
        cls.addClassCleanup(cls._tmp.cleanup)
        cls.root = Path(cls._tmp.name)

        cls.dir_intermed = cls.root / "intermed"
        cls.dir_masks = cls.root / "crop_masks"
        cls.dir_boundaries = cls.root / "boundary_files"
        cls.dir_calendars = cls.root / "crop_calendars"
        cls.dir_output = cls.root / "output"
        for directory in (cls.dir_intermed, cls.dir_masks, cls.dir_boundaries,
                          cls.dir_calendars, cls.dir_output):
            directory.mkdir(parents=True, exist_ok=True)

        cls._write_boundaries()
        cls._write_zones()
        cls._write_calendar()
        cls._write_mask()
        cls.config_file = cls._write_config()
        cls.parser = cls._read_parser()
        cls._write_rasters()

    # -- config ------------------------------------------------------------
    @classmethod
    def _write_config(cls):
        """One config file carrying every section the runner reads."""
        text = f"""
[DEFAULT]
project_name = testproj
countries = ['kenya']

[PATHS]
dir_intermed = {cls.dir_intermed.as_posix()}
dir_crop_masks = {cls.dir_masks.as_posix()}
dir_boundary_files = {cls.dir_boundaries.as_posix()}
dir_crop_calendars = {cls.dir_calendars.as_posix()}
dir_output = {cls.dir_output.as_posix()}

[CHIRPS]
version = v3

; Section named after the boundary file stem so
; geoprepare.georegion.get_boundary_col_mapping keeps our columns.
[test_adm]
adm0_col = ADM0_NAME
adm1_col = ADM1_NAME
id_col = ADM_ID

[kenya]
boundary_file = test_adm.gpkg
shp_region = test_zones.gpkg
calendar_file = test_cal.xlsx
use_cropland_mask = False
crops = ['maize']
seasons = [1, 2]

[maize]
mask = maize_mask.tif

[SEASON_MONITOR]
precip_threshold = 20.0
window_days = 3
dry_spell_days = 5
dry_day_threshold = 1.0
validation_days = 10
search_start_days_before_planting = 5
soil_whc = 20.0
min_season_days = 30
min_season_days_maize = 10
empty_persist_days = 2
cessation_grace_days = 20
forecast_days = 16
use_forecast = False
refresh_datasets = ['CHIRPS']
bbox_buffer = 0.5
mask_to_cropland = True
climatology_start_year = 2001
climatology_end_year = 2003
min_valid_years = 3
rebuild_climatology = False
n_workers = 1
"""
        path = cls.root / "test_config.txt"
        path.write_text(text, encoding="utf-8")
        return path

    @classmethod
    def _read_parser(cls):
        parser = configparser.ConfigParser(
            interpolation=configparser.ExtendedInterpolation(),
            inline_comment_prefixes=(";",),
        )
        parser.read([str(cls.config_file)])
        return parser

    # -- fixture writers ---------------------------------------------------
    @classmethod
    def _write_boundaries(cls):
        import geopandas as gpd
        from shapely.geometry import box

        gdf = gpd.GeoDataFrame(
            {
                "ADM0_NAME": ["Kenya", "Kenya"],
                "ADM1_NAME": ["West Unit", "East Unit"],
                "ADM_ID": [101, 102],
            },
            geometry=[box(36.0, 0.0, 36.5, 1.0), box(36.5, 0.0, 37.0, 1.0)],
            crs="EPSG:4326",
        )
        gdf.to_file(cls.dir_boundaries / "test_adm.gpkg", driver="GPKG")

    @classmethod
    def _write_zones(cls):
        """One calendar zone over rows/cols 10..29, written in EPSG:3857."""
        import geopandas as gpd
        from shapely.geometry import box

        gdf = gpd.GeoDataFrame(
            {"ADM0_NAME": ["Kenya"], "Name": ["Zone A"]},
            geometry=[box(36.0, 0.0, 37.0, 1.0)],
            crs="EPSG:4326",
        ).to_crs(epsg=3857)
        gdf.to_file(cls.dir_boundaries / "test_zones.gpkg", driver="GPKG")

    @classmethod
    def _write_calendar(cls):
        """maize_1 within-year (Apr 1 - Apr 30), maize_2 the short-rains shape."""
        season_1 = {"apr_1": 1, "apr_15": 3}
        season_2 = {"oct_15": 1, "nov_1": 1, "nov_15": 1, "dec_1": 1, "dec_15": 1,
                    "jan_1": 2, "jan_15": 2, "feb_1": 3}

        def _sheet(pairs):
            row = {"admin": "Zone A", "country": "Kenya", "Country2": "Kenya", "Admin2": ""}
            row.update(_bins(pairs))
            return pd.DataFrame(
                [row], columns=["admin", "country", "Country2", "Admin2"] + BIN_COLS
            )

        with pd.ExcelWriter(cls.dir_calendars / "test_cal.xlsx", engine="openpyxl") as writer:
            _sheet(season_1).to_excel(writer, sheet_name="maize_1", index=False)
            _sheet(season_2).to_excel(writer, sheet_name="maize_2", index=False)

    @classmethod
    def _write_mask(cls):
        """Crop mask: percent x 100, 5000 -> 0.5 cropland fraction everywhere."""
        _write_tile(
            cls.dir_masks / "maize_mask.tif",
            np.full(TILE_SHAPE, 5000, dtype=np.int32),
            "int32",
            -9999,
        )

    @classmethod
    def _cube_dates(cls, year):
        start = dt.date(year, CUBE_START.month, CUBE_START.day)
        end = dt.date(year, CUBE_END.month, CUBE_END.day)
        return [start + dt.timedelta(days=i) for i in range((end - start).days + 1)]

    @classmethod
    def _write_rasters(cls):
        """CHIRPS and etref for every cube day of 2001-2003."""
        for year, onset_idx in ONSET_INDEX.items():
            dates = cls._cube_dates(year)
            rain_mm = np.zeros(len(dates), dtype=np.float64)
            rain_mm[onset_idx] = 25.0
            rain_mm[onset_idx + 1: onset_idx + 16] = 5.0
            if year == 2002:
                rain_mm[PLANTING_INDEX] = 25.0   # false start, invalidated
            for i, day in enumerate(dates):
                _write_tile(
                    inputs.daily_path(cls.parser, "chirps", day),
                    np.full(TILE_SHAPE, int(round(rain_mm[i] * 100)), dtype=np.int32),
                    "int32", CHIRPS_NODATA,
                )
                _write_tile(
                    inputs.daily_path(cls.parser, "etref", day),
                    np.full(TILE_SHAPE, 4.0, dtype=np.float32),
                    "float32", FLOAT_NODATA,
                )

    # -- helpers -----------------------------------------------------------
    def read_layer(self, dir_rasters, layer):
        path = Path(dir_rasters) / f"{season_monitor.file_stem(layer, SEASON, AS_OF)}.tif"
        self.assertTrue(path.is_file(), f"missing raster {path.name}")
        with rasterio.open(path) as src:
            data = src.read(1)
            nodata = src.nodata
            tags = src.tags()
        out = data.astype(np.float64)
        if nodata is not None and np.isfinite(nodata):
            out[data == nodata] = np.nan
        return out, tags


class TestActiveSeasons(SeasonMonitorFixture):
    """Kenya short rains: in season in October, out of season in July."""

    def test_short_rains_active_in_october(self):
        # harvest year 2026 is planted Oct 15 2025; the search opens 5 days
        # earlier (Oct 10 2025) and the window closes Feb 14 + 10 = Feb 24 2026.
        seasons = monitor.active_seasons(
            self.parser,
            dt.date(2025, 10, 20),
            search_start_days_before_planting=5,
            validation_days=10,
        )
        self.assertIn(("kenya", "maize", 2, 2026), seasons)

    def test_short_rains_not_active_in_july(self):
        # Jul 15 2025 is after the 2025 short rains closed (Feb 24 2025) and
        # before the 2026 one opens (Oct 10 2025); maize_1 2025 closed May 10.
        seasons = monitor.active_seasons(
            self.parser,
            dt.date(2025, 7, 15),
            search_start_days_before_planting=5,
            validation_days=10,
        )
        self.assertNotIn(("kenya", "maize", 2, 2026), seasons)
        self.assertNotIn(("kenya", "maize", 2, 2025), seasons)
        self.assertEqual(seasons, [])

    def test_long_season_active_mid_april(self):
        seasons = monitor.active_seasons(
            self.parser,
            dt.date(2025, 4, 15),
            search_start_days_before_planting=5,
            validation_days=10,
        )
        self.assertEqual(seasons, [("kenya", "maize", 1, 2025)])

    def test_only_the_long_season_is_active_on_the_run_date(self):
        seasons = monitor.active_seasons(
            self.parser, AS_OF, search_start_days_before_planting=5, validation_days=10
        )
        self.assertEqual(seasons, [tuple(SEASON)])


class TestSeasonOverride(SeasonMonitorFixture):
    """``[SEASON_MONITOR] seasons_<country>`` overrides ``[country] seasons``.

    The shared key is read by the CID / extract / merge pipelines, which need a
    merged CSV per season; this product reads rasters and the calendar directly.
    Kenya's short rains motivated it: they are monitorable without the merged
    CSV that ``[kenya] seasons = [1, 2]`` would otherwise imply exists.
    """

    def test_override_narrows_the_season_list(self):
        # the fixture config has [kenya] seasons = [1, 2]
        self.assertEqual(monitor.seasons_for(self.parser, "kenya"), [1, 2])
        self.assertEqual(monitor.seasons_for(self.parser, "kenya", [2]), [2])

    def test_override_is_used_by_active_seasons(self):
        # Apr 15 2025 is inside the long season only, so restricting to
        # season 2 must leave nothing active on that date.
        common = dict(search_start_days_before_planting=5, validation_days=10)
        self.assertEqual(
            monitor.active_seasons(self.parser, dt.date(2025, 4, 15), **common),
            [("kenya", "maize", 1, 2025)],
        )
        self.assertEqual(
            monitor.active_seasons(
                self.parser,
                dt.date(2025, 4, 15),
                seasons_by_country={"kenya": [2]},
                **common,
            ),
            [],
        )

    def test_absent_override_falls_back_to_the_country_key(self):
        common = dict(search_start_days_before_planting=5, validation_days=10)
        expected = monitor.active_seasons(self.parser, dt.date(2025, 10, 20), **common)
        for override in ({}, {"zimbabwe": [1]}, None):
            self.assertEqual(
                monitor.active_seasons(
                    self.parser,
                    dt.date(2025, 10, 20),
                    seasons_by_country=override,
                    **common,
                ),
                expected,
                override,
            )

    def test_read_config_parses_the_key(self):
        cfg_file = self.root / "with_override.txt"
        cfg_file.write_text(
            Path(self.config_file).read_text(encoding="utf-8")
            + "\nseasons_kenya = [2]\nseasons_zimbabwe = 1\n",
            encoding="utf-8",
        )
        cfg = season_monitor.read_config([cfg_file])
        # a bare scalar is accepted and wrapped, a list is taken as written
        self.assertEqual(cfg["country_seasons"], {"kenya": [2], "zimbabwe": [1]})

    def test_unparseable_override_is_ignored_not_fatal(self):
        cfg_file = self.root / "bad_override.txt"
        cfg_file.write_text(
            Path(self.config_file).read_text(encoding="utf-8")
            + "\nseasons_kenya = not-a-list\n",
            encoding="utf-8",
        )
        cfg = season_monitor.read_config([cfg_file])
        self.assertEqual(cfg["country_seasons"], {})


class TestReadConfig(SeasonMonitorFixture):
    """[SEASON_MONITOR] parsing, defaults, per-crop overrides, kwargs."""

    def test_every_key_is_read(self):
        cfg = season_monitor.read_config([self.config_file])
        self.assertEqual(cfg["precip_threshold"], 20.0)
        self.assertEqual(cfg["validation_days"], 10)
        self.assertEqual(cfg["search_start_days_before_planting"], 5)
        self.assertFalse(cfg["use_forecast"])
        self.assertTrue(cfg["mask_to_cropland"])
        self.assertEqual(cfg["refresh_datasets"], ["CHIRPS"])
        self.assertEqual(cfg["countries"], ["kenya"])
        self.assertEqual(cfg["climatology_start_year"], 2001)
        self.assertEqual(cfg["project"], "testproj")

    def test_missing_section_falls_back_to_the_documented_defaults(self):
        bare = self.root / "bare_config.txt"
        bare.write_text(
            f"[PATHS]\ndir_output = {self.dir_output.as_posix()}\n"
            f"dir_intermed = {self.dir_intermed.as_posix()}\n",
            encoding="utf-8",
        )
        cfg = season_monitor.read_config([bare])
        for key, default in season_monitor.DEFAULTS.items():
            self.assertEqual(cfg[key], default, key)

    def test_per_crop_min_season_days_override(self):
        cfg = season_monitor.read_config([self.config_file])
        self.assertEqual(cfg["crop_min_season_days"], {"maize": 10})
        self.assertEqual(season_monitor.climatology_params(cfg, "maize").cessation.min_season_days, 10)
        # a crop without an override keeps the section-wide value
        self.assertEqual(
            season_monitor.climatology_params(cfg, "sorghum").cessation.min_season_days, 30
        )

    def test_keyword_overrides_win(self):
        cfg = season_monitor.read_config(
            [self.config_file], min_valid_years=7, as_of="2003-04-30"
        )
        self.assertEqual(cfg["min_valid_years"], 7)
        self.assertEqual(cfg["as_of"], AS_OF)

    def test_unknown_override_is_rejected(self):
        with self.assertRaises(TypeError):
            season_monitor.read_config([self.config_file], not_a_key=1)


class TestRunEndToEnd(SeasonMonitorFixture):
    """One full run: refresh -> climatology -> monitor -> rasters/maps/tables."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.refresh_calls = []

        def _fake_refresh(cfg_list, datasets=(), years=None, logger=None):
            cls.refresh_calls.append(tuple(datasets))
            return {name: {"ok": True, "seconds": 0.0, "error": None} for name in datasets}

        with mock.patch.object(season_monitor, "refresh_inputs", _fake_refresh), \
                mock.patch.object(phenology_maps, "raster_map", _stub_raster_map):
            cls.summary = season_monitor.run([cls.config_file], as_of=AS_OF)
        cls.dirs = season_monitor.output_dirs(
            season_monitor.read_config([cls.config_file]), SEASON, cls.summary["stamp"]
        )

    def test_run_summary(self):
        self.assertEqual(self.summary["as_of"], AS_OF)
        self.assertEqual(self.summary["n_failed"], 0)
        self.assertEqual(self.summary["n_ok"], 1)
        record = self.summary["results"][0]
        self.assertTrue(record["ok"], record.get("error"))
        self.assertEqual(record["harvest_year"], 2003)
        self.assertEqual(record["climatology_years"], 3)
        self.assertEqual(record["data_through"], "2003-04-30")

    def test_refresh_stage_ran(self):
        self.assertEqual(self.refresh_calls, [("CHIRPS",)])

    def test_output_tree(self):
        root = self.dirs["root"]
        self.assertEqual(root.parent.parent.parent.name, season_monitor.PRODUCT)
        # the harvest year is in the directory AND the file names: two harvest
        # years of one season can be active on the same as-of date, and without
        # it the second run silently overwrote the first
        self.assertEqual(root.name, f"s1_hy{SEASON.harvest_year}")
        self.assertEqual(root.parent.name, "maize")
        self.assertEqual(root.parent.parent.name, "kenya")
        for key in ("rasters", "maps", "csvs"):
            self.assertTrue(self.dirs[key].is_dir(), key)

    def test_two_harvest_years_do_not_share_a_path(self):
        """The overwrite this naming exists to prevent."""
        other = monitor.ActiveSeason(
            SEASON.country, SEASON.crop, SEASON.season, SEASON.harvest_year + 1
        )
        cfg = season_monitor.read_config([self.config_file])
        self.assertNotEqual(
            season_monitor.output_dirs(cfg, SEASON, self.summary["stamp"])["rasters"],
            season_monitor.output_dirs(cfg, other, self.summary["stamp"])["rasters"],
        )
        self.assertNotEqual(
            season_monitor.file_stem("onset_days", SEASON, AS_OF),
            season_monitor.file_stem("onset_days", other, AS_OF),
        )
        # and the maps, which build their own stem, must agree with the rasters
        ctx = phenology_maps.MapContext(
            lon=np.zeros(1), lat=np.zeros(1), dir_plots=".", dir_csvs=".",
            country=SEASON.country, crop=SEASON.crop, season=SEASON.season,
            harvest_year=SEASON.harvest_year, asof=AS_OF,
        )
        other_ctx = phenology_maps.MapContext(
            lon=np.zeros(1), lat=np.zeros(1), dir_plots=".", dir_csvs=".",
            country=SEASON.country, crop=SEASON.crop, season=SEASON.season,
            harvest_year=other.harvest_year, asof=AS_OF,
        )
        self.assertNotEqual(
            phenology_maps.map_stem("season_state", ctx),
            phenology_maps.map_stem("season_state", other_ctx),
        )
        self.assertEqual(
            phenology_maps.map_stem("onset_days", ctx),
            season_monitor.file_stem("onset_days", SEASON, AS_OF),
        )

    def test_every_layer_has_a_raster(self):
        for layer in monitor.MONITOR_LAYERS:
            stem = season_monitor.file_stem(layer, SEASON, AS_OF)
            self.assertTrue((self.dirs["rasters"] / f"{stem}.tif").is_file(), layer)

    def test_onset_anomaly_is_five_days_late(self):
        # onset index 20 -> 15 days after planting; climatological median 10.
        values, tags = self.read_layer(self.dirs["rasters"], "onset_anomaly_days")
        self.assertAlmostEqual(float(values[IN_ZONE]), 5.0, places=4)
        self.assertTrue(np.isnan(values[OUT_OF_ZONE]))
        self.assertEqual(tags["data_through"], "2003-04-30")
        self.assertEqual(tags["units"], monitor.MONITOR_LAYERS["onset_anomaly_days"][2])

    def test_state_and_onset_date(self):
        from geocif.phenology import core

        state, _ = self.read_layer(self.dirs["rasters"], "state")
        self.assertEqual(int(state[IN_ZONE]), int(core.SeasonState.CONFIRMED))
        self.assertTrue(np.isnan(state[OUT_OF_ZONE]))
        onset_date, _ = self.read_layer(self.dirs["rasters"], "onset_date")
        # cube index 20 counted from Mar 27 2003 = Apr 16 2003
        self.assertEqual(
            monitor.EPOCH + int(onset_date[IN_ZONE]), np.datetime64("2003-04-16", "D")
        )

    def test_days_past_median_is_empty_when_nothing_is_waiting(self):
        values, _ = self.read_layer(self.dirs["rasters"], "days_past_median")
        self.assertTrue(np.all(np.isnan(values)))

    def test_rain_and_its_percentile(self):
        rain, _ = self.read_layer(self.dirs["rasters"], "rain_30d")
        # indices 5..34 = 25 mm on index 20 plus 14 days at 5 mm
        self.assertAlmostEqual(float(rain[IN_ZONE]), 95.0, places=3)
        pct, _ = self.read_layer(self.dirs["rasters"], "rain_30d_percentile")
        # 1 of the 3 years (2003 itself) was at or below 95 mm -> 100/3
        self.assertAlmostEqual(float(pct[IN_ZONE]), 100.0 / 3.0, places=3)

    def test_false_start_rate_comes_from_the_cache(self):
        rate, _ = self.read_layer(self.dirs["rasters"], "false_start_rate")
        # only 2002 carried an invalidated episode -> 1 of 3 years
        self.assertAlmostEqual(float(rate[IN_ZONE]), 1.0 / 3.0, places=4)

    def test_status_area_table(self):
        path = self.dirs["csvs"] / f"{season_monitor.file_stem('status_area', SEASON, AS_OF)}.csv"
        self.assertTrue(path.is_file())
        table = pd.read_csv(path)
        self.assertEqual(sorted(table["ADM1_NAME"]), ["East Unit", "West Unit"])
        # every cropland pixel of both units confirmed onset
        self.assertTrue(np.allclose(table["share_confirmed"].to_numpy(), 1.0))
        self.assertEqual(list(table["data_through"].unique()), ["2003-04-30"])

    def test_onset_summary_table(self):
        path = self.dirs["csvs"] / f"{season_monitor.file_stem('onset_summary', SEASON, AS_OF)}.csv"
        self.assertTrue(path.is_file())
        table = pd.read_csv(path)
        self.assertEqual(sorted(table["zone_type"].unique()), ["admin_1", "calendar_zone"])
        admin = table[table["zone_type"] == "admin_1"]
        self.assertTrue(
            np.allclose(admin["onset_anomaly_days_weighted_median"].to_numpy(), 5.0)
        )
        zones = table[table["zone_type"] == "calendar_zone"]
        self.assertEqual(list(zones["unit_name"]), ["zone_a"])

    def test_lookup_manifest_lists_only_files_that_exist(self):
        for folder in ("maps", "csvs"):
            manifest = self.dirs[folder] / "lookup_plots_csvs.csv"
            self.assertTrue(manifest.is_file(), folder)
        rows = pd.read_csv(self.dirs["maps"] / "lookup_plots_csvs.csv")
        self.assertEqual(list(rows.columns), ["plot_file", "csv_file", "description"])
        self.assertGreaterEqual(len(rows), 5)
        for _, row in rows.iterrows():
            self.assertTrue(
                (self.dirs["maps"] / row["plot_file"]).is_file(), row["plot_file"]
            )
            self.assertTrue(
                (self.dirs["csvs"] / row["csv_file"]).is_file(), row["csv_file"]
            )
            self.assertIn("2003", str(row["description"]) + str(row["plot_file"]))

    def test_the_expected_maps_were_drawn(self):
        names = {p.name for p in self.dirs["maps"].glob("*.png")}
        for layer in ("season_state", "onset_anomaly_days", "days_past_median",
                      "p_onset_28d", "rain_30d_percentile"):
            self.assertIn(
                f"{season_monitor.file_stem(layer, SEASON, AS_OF)}.png", names, layer
            )
        # no forecast on disk -> no forecast map rather than an empty one
        self.assertNotIn(
            f"{season_monitor.file_stem('fcst_trigger_days', SEASON, AS_OF)}.png", names
        )

    def test_climatology_cache_was_written(self):
        cache = self.dir_output / "testproj" / "phenology" / "climatology" / "kenya" / "maize" / "s1"
        self.assertTrue((cache / "manifest.json").is_file())
        self.assertTrue((cache / "onset_median.tif").is_file())

    def test_zone_report_ran_and_wrote_its_own_subtree(self):
        """The per-zone window report is a stage of the run, not an add-on.

        Guards against it silently skipping: a missing cache, a grid mismatch or
        a zone that misses the cropland mask all return [] rather than raising,
        so only an assertion on real output proves the stage did its work.
        """
        record = self.summary["results"][0]
        self.assertGreater(record["n_zone_report_files"], 0)
        plots, csvs = self.dirs["zone_plots"], self.dirs["zone_csvs"]
        self.assertTrue(plots.is_dir())
        self.assertEqual(plots.parent.name, "zones")
        self.assertTrue(any(plots.glob("onset_window_*.png")), sorted(p.name for p in plots.iterdir()))
        for name in ("zone_history", "zone_climatology", "zone_current"):
            self.assertTrue(any(csvs.glob(f"{name}_*.csv")), name)
        # the three frames must agree on the zone set
        hist = pd.read_csv(next(csvs.glob("zone_history_*.csv")))
        cur = pd.read_csv(next(csvs.glob("zone_current_*.csv")))
        self.assertEqual(set(hist.zone.unique()), set(cur.zone.unique()))
        # every current row states a window status, and the fixture's as-of is
        # well past its April window, so it has closed
        self.assertTrue(cur.window_status.isin(["complete", "partial", "not_open"]).all())

    def test_climatology_maps_go_to_their_own_subtree(self):
        """The reference set must not share a directory with the monitor set.

        ``phenology_maps`` writes ``lookup_plots_csvs.csv`` into whichever
        directory it is handed, so two map sets in one directory would leave the
        second manifest overwriting the first.
        """
        self.assertGreater(self.summary["results"][0]["n_climatology_maps"], 0)
        clim_maps = self.dirs["clim_maps"]
        self.assertTrue(clim_maps.is_dir())
        self.assertEqual(clim_maps.parent.name, "climatology")
        self.assertEqual(clim_maps.parent.parent, self.dirs["root"])
        drawn = {p.name for p in clim_maps.glob("*.png")}
        self.assertTrue(drawn, "no climatology maps rendered")
        # onset_median is the date-labelled one and must always be present
        self.assertTrue(
            any("onset_median" in name for name in drawn),
            f"onset_median missing from {sorted(drawn)}",
        )

    def test_both_manifests_survive(self):
        """Each map set keeps its own manifest, and every row resolves."""
        for dir_plots, dir_csvs in (
            (self.dirs["maps"], self.dirs["csvs"]),
            (self.dirs["clim_maps"], self.dirs["clim_csvs"]),
        ):
            manifest = dir_plots / "lookup_plots_csvs.csv"
            self.assertTrue(manifest.is_file(), f"no manifest in {dir_plots}")
            rows = pd.read_csv(manifest)
            self.assertGreater(len(rows), 0, f"empty manifest in {dir_plots}")
            for _, row in rows.iterrows():
                self.assertTrue(
                    (dir_plots / str(row["plot_file"])).is_file(), row["plot_file"]
                )
                self.assertTrue(
                    (dir_csvs / str(row["csv_file"])).is_file(), row["csv_file"]
                )


if __name__ == "__main__":
    unittest.main()
