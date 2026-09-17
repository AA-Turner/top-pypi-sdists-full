# -*- coding: utf-8 -*-
"""Tests for geocif/phenology/inputs.py (DESIGN.md sections 1 and 4).

Everything here is synthetic and lives in a temp directory: aligned 0.05 deg
GeoTIFF tiles on the global lattice, a three-sheet calendar workbook, zone
polygons deliberately written in EPSG:3857 so the reprojection is provable, and
a two-unit boundary file.

Grid arithmetic used throughout (global transform
``Affine(0.05, 0, -180, 0, -0.05, 90)``):

    col_off = (west + 180) / 0.05 ,  row_off = (90 - north) / 0.05

    country box (35.5, -0.5, 37.5, 1.5) -> col_off = 215.5/0.05 = 4310
                                           row_off =  88.5/0.05 = 1770
                                           40 x 40 cells
    inner  box (36.0,  0.0, 37.0, 1.0) -> col_off = 216.0/0.05 = 4320
                                           row_off =  89.0/0.05 = 1780
                                           20 x 20 cells, i.e. tile[10:30, 10:30]
"""
import configparser
import datetime as dt
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
import pandas as pd
import rasterio
from affine import Affine
from rasterio.windows import Window

from geocif.phenology import inputs

# --- the synthetic country window ------------------------------------------
TILE_WEST, TILE_SOUTH, TILE_EAST, TILE_NORTH = 35.5, -0.5, 37.5, 1.5
TILE_TRANSFORM = Affine(0.05, 0, TILE_WEST, 0, -0.05, TILE_NORTH)
TILE_SHAPE = (40, 40)  # (1.5 - -0.5) / 0.05 = 40 in each direction

COUNTRY_WINDOW = Window(4310, 1770, 40, 40)
INNER_WINDOW = Window(4320, 1780, 20, 20)

CHIRPS_NODATA = -2147483648

MONTHS = ["jan", "feb", "mar", "apr", "may", "jun",
          "jul", "aug", "sep", "oct", "nov", "dec"]
BIN_COLS = [f"{m}_{d}" for m in MONTHS for d in (1, 15)]


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


class PhenologyInputsFixture(unittest.TestCase):
    """Builds the whole synthetic config tree once per test."""

    def setUp(self):
        self._tmp = TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

        self.dir_intermed = self.root / "intermed"
        self.dir_masks = self.root / "crop_masks"
        self.dir_boundaries = self.root / "boundary_files"
        self.dir_calendars = self.root / "crop_calendars"
        for d in (self.dir_intermed, self.dir_masks, self.dir_boundaries, self.dir_calendars):
            d.mkdir(parents=True, exist_ok=True)

        self._write_boundaries()
        self._write_zones()
        self._write_calendar()
        self._write_mask()

        self.parser = configparser.ConfigParser(
            interpolation=configparser.ExtendedInterpolation(),
            inline_comment_prefixes=(";",),
        )
        self.parser.read_dict({
            "PATHS": {
                "dir_intermed": str(self.dir_intermed),
                "dir_crop_masks": str(self.dir_masks),
                "dir_boundary_files": str(self.dir_boundaries),
                "dir_crop_calendars": str(self.dir_calendars),
            },
            "CHIRPS": {"version": "v3"},
            # Section named after the boundary file stem so
            # geoprepare.georegion.get_boundary_col_mapping does NOT fall back
            # to its alias map (which would drop our already-standard columns).
            "test_adm": {
                "adm0_col": "ADM0_NAME",
                "adm1_col": "ADM1_NAME",
                "id_col": "ADM_ID",
            },
            "kenya": {
                "boundary_file": "test_adm.gpkg",
                "shp_region": "test_zones.gpkg",
                "calendar_file": "test_cal.xlsx",
                "use_cropland_mask": "False",
            },
            "maize": {"mask": "maize_mask.tif"},
        })

    # -- fixture writers ---------------------------------------------------
    def _write_boundaries(self):
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
        gdf.to_file(self.dir_boundaries / "test_adm.gpkg", driver="GPKG")

    def _write_zones(self):
        """Zone polygons written in EPSG:3857 on purpose (the shipped
        GlobalCM_Regions file is Web Mercator); load_calendar_zones must
        reproject before anything is rasterised."""
        import geopandas as gpd
        from shapely.geometry import box

        gdf = gpd.GeoDataFrame(
            {
                "ADM0_NAME": ["Kenya", "Kenya", "Kenya"],
                "Name": ["Zone A", "Zone B", "Zone C"],
            },
            geometry=[
                box(36.0, 0.5, 37.0, 1.0),    # rows 10-19 of the country window
                box(36.0, 0.0, 37.0, 0.5),    # rows 20-29
                box(36.0, -0.5, 37.0, 0.0),   # rows 30-39, the all -1 zone
            ],
            crs="EPSG:4326",
        ).to_crs(epsg=3857)
        gdf.to_file(self.dir_boundaries / "test_zones.gpkg", driver="GPKG")

    def _write_calendar(self):
        """Two crop sheets: maize_1 within-year, maize_2 cross-year.

        maize_1: apr_1 = 1, apr_15..jul_15 = 2, aug_1 = aug_15 = 3
                 -> planting Apr 1, harvest Aug 31 (aug_15 bin ends on the
                    last day of August).
        maize_2: oct_15..dec_15 = 1, jan_1/jan_15 = 2, feb_1 = 3
                 -> the jan/feb head merges with the oct-dec tail into one
                    wrapped block; planting Oct 15 of harvest_year - 1,
                    harvest Feb 14 of harvest_year.
        Zone C carries the all -1 "crop not grown" sentinel in both sheets.
        """
        grow_1 = {"apr_1": 1, "apr_15": 2, "may_1": 2, "may_15": 2, "jun_1": 2,
                  "jun_15": 2, "jul_1": 2, "jul_15": 2, "aug_1": 3, "aug_15": 3}
        grow_2 = {"oct_15": 1, "nov_1": 1, "nov_15": 1, "dec_1": 1, "dec_15": 1,
                  "jan_1": 2, "jan_15": 2, "feb_1": 3}
        not_grown = {col: -1 for col in BIN_COLS}

        def _sheet(pairs):
            rows = []
            for name, flags in (("Zone A", pairs), ("Zone B", pairs), ("Zone C", not_grown)):
                row = {"admin": name, "country": "Kenya", "Country2": "Kenya", "Admin2": ""}
                row.update(_bins(flags) if flags is not not_grown else flags)
                rows.append(row)
            return pd.DataFrame(rows, columns=["admin", "country", "Country2", "Admin2"] + BIN_COLS)

        path = self.dir_calendars / "test_cal.xlsx"
        with pd.ExcelWriter(path, engine="openpyxl") as writer:
            _sheet(grow_1).to_excel(writer, sheet_name="maize_1", index=False)
            _sheet(grow_2).to_excel(writer, sheet_name="maize_2", index=False)

    def _write_mask(self):
        """Crop mask: percent x 100. 5000 -> 0.5; nodata and -1 -> 0."""
        mask = np.full(TILE_SHAPE, 5000, dtype=np.int32)
        mask[0, 0] = -1          # negative -> 0
        mask[0, 1] = -9999       # the declared nodata -> 0
        mask[20, 20] = 10000     # full cropland -> 1.0
        _write_tile(self.dir_masks / "maize_mask.tif", mask, "int32", -9999)

    def _write_chirps(self, day, array):
        path = inputs.daily_path(self.parser, "chirps", day)
        return _write_tile(path, array, "int32", CHIRPS_NODATA)


class TestGridAndWindow(PhenologyInputsFixture):
    def test_global_grid_constants(self):
        self.assertEqual(inputs.GLOBAL_TRANSFORM, Affine(0.05, 0, -180, 0, -0.05, 90))
        self.assertEqual((inputs.GRID_HEIGHT, inputs.GRID_WIDTH), (3600, 7200))

    def test_snap_bbox_rounds_outward(self):
        # west 36.02 -> floor to 36.00, east 36.53 -> ceil to 36.55,
        # south -0.11 -> floor to -0.15, north 1.01 -> ceil to 1.05
        snapped = inputs.snap_bbox((36.02, -0.11, 36.53, 1.01))
        self.assertAlmostEqual(snapped[0], 36.00, places=6)
        self.assertAlmostEqual(snapped[1], -0.15, places=6)
        self.assertAlmostEqual(snapped[2], 36.55, places=6)
        self.assertAlmostEqual(snapped[3], 1.05, places=6)

    def test_snap_bbox_clips_to_the_chirps_latitude_band(self):
        snapped = inputs.snap_bbox((-190.0, -75.0, 190.0, 75.0))
        self.assertEqual(snapped, (-180.0, -60.0, 180.0, 60.0))

    def test_country_bbox_and_window(self):
        # total_bounds (36.0, 0.0, 37.0, 1.0) +/- 0.5 -> (35.5, -0.5, 37.5, 1.5),
        # already on the lattice, so snapping is a no-op.
        bbox = inputs.country_bbox(self.parser, "kenya", buffer_deg=0.5)
        self.assertEqual(bbox, (TILE_WEST, TILE_SOUTH, TILE_EAST, TILE_NORTH))

        window, transform, shape = inputs.window_for_bbox(bbox)
        self.assertEqual((window.col_off, window.row_off), (4310, 1770))
        self.assertEqual((window.width, window.height), (40, 40))
        self.assertEqual(shape, (40, 40))
        self.assertEqual(transform, TILE_TRANSFORM)

    def test_pixel_centres_and_area(self):
        _window, transform, shape = inputs.window_for_bbox(
            (TILE_WEST, TILE_SOUTH, TILE_EAST, TILE_NORTH)
        )
        lon, lat = inputs.pixel_centres(transform, shape)
        # first centre = west + 0.5 * 0.05 = 35.5 + 0.025 = 35.525
        self.assertAlmostEqual(lon[0], 35.525, places=9)
        # first row centre = north - 0.5 * 0.05 = 1.5 - 0.025 = 1.475
        self.assertAlmostEqual(lat[0], 1.475, places=9)
        self.assertEqual(len(lon), 40)
        self.assertEqual(len(lat), 40)

        # At the equator a 0.05 deg cell is essentially a square:
        # side = 0.05 * pi/180 * 6371.0087714 km = 5.5597 km -> 30.91 km^2.
        area = inputs.pixel_area_km2(np.array([0.0]))
        self.assertAlmostEqual(float(area[0]), 30.91, places=1)
        # Area shrinks toward the pole: 60 N is half the equatorial value
        # (cos 60 = 0.5) to within the sphere-segment correction.
        area60 = inputs.pixel_area_km2(np.array([60.0]))
        self.assertAlmostEqual(float(area60[0]) / float(area[0]), 0.5, places=3)


class TestDailyPathsAndCube(PhenologyInputsFixture):
    def test_daily_path_uses_the_chirps_version_option(self):
        day = dt.date(2025, 3, 1)  # 2025 is not a leap year -> DOY 60
        path = inputs.daily_path(self.parser, "chirps", day)
        self.assertEqual(path.name, "chirps_v3.0_2025060_global.tif")
        self.assertEqual(path.parent, self.dir_intermed / "chirps" / "v3" / "global" / "2025")

        self.parser.set("CHIRPS", "version", "v2")
        path_v2 = inputs.daily_path(self.parser, "chirps", day)
        self.assertEqual(path_v2.name, "chirps_v2.0_2025060_global.tif")
        self.assertIn("v2", str(path_v2.parent))

    def test_daily_path_other_variables(self):
        day = dt.date(2024, 12, 31)  # 2024 is a leap year -> DOY 366
        self.assertEqual(
            inputs.daily_path(self.parser, "etref", day).name, "etref_2024366_global.tif"
        )
        self.assertEqual(
            inputs.daily_path(self.parser, "chirts_era5_tmax", day).name,
            "chirts_era5_tmax_2024366_global.tif",
        )
        with self.assertRaises(ValueError):
            inputs.daily_path(self.parser, "not_a_variable", day)

    def test_read_cube_windows_scales_and_reports_missing(self):
        raw = np.full(TILE_SHAPE, 1234, dtype=np.int32)
        raw[10, 10] = -9999            # in-band sentinel     -> NaN
        raw[10, 11] = CHIRPS_NODATA    # declared nodata      -> NaN
        raw[10, 12] = 7777             # marker at inner[0,2] -> 77.77 mm
        raw[12, 13] = 5000             # inner[2,3]           -> 50.00 mm
        raw[9, 9] = 999999             # OUTSIDE the inner window

        days = [dt.date(2025, 6, 1), dt.date(2025, 6, 2), dt.date(2025, 6, 3)]
        self._write_chirps(days[0], raw)
        # days[1] is deliberately absent -> all-NaN slab, reported as missing
        self._write_chirps(days[2], np.full(TILE_SHAPE, 100, dtype=np.int32))

        cube, missing = inputs.read_cube(self.parser, "chirps", days, INNER_WINDOW, n_threads=3)

        self.assertEqual(cube.shape, (3, 20, 20))
        self.assertEqual(cube.dtype, np.float32)
        self.assertEqual(missing, [days[1]])

        # Scaling: 1234 / 100 = 12.34 mm
        self.assertAlmostEqual(float(cube[0, 5, 5]), 12.34, places=4)
        self.assertTrue(np.isnan(cube[0, 0, 0]))   # -9999
        self.assertTrue(np.isnan(cube[0, 0, 1]))   # nodata
        # Windowing: tile[10, 12] is inner[0, 2] -> 7777 / 100 = 77.77
        self.assertAlmostEqual(float(cube[0, 0, 2]), 77.77, places=4)
        # tile[12, 13] is inner[2, 3] -> 5000 / 100 = 50.00
        self.assertAlmostEqual(float(cube[0, 2, 3]), 50.00, places=4)
        # The out-of-window marker never appears anywhere in the slab.
        self.assertFalse(np.any(np.isclose(cube[0], 9999.99, atol=0.01)))

        self.assertTrue(np.all(np.isnan(cube[1])))               # missing day
        self.assertAlmostEqual(float(cube[2, 0, 0]), 1.00, places=4)  # 100 / 100

    def test_read_cube_never_raises_when_nothing_is_on_disk(self):
        days = [dt.date(2030, 1, 1), dt.date(2030, 1, 2)]
        cube, missing = inputs.read_cube(self.parser, "chirps", days, INNER_WINDOW)
        self.assertEqual(missing, days)
        self.assertTrue(np.all(np.isnan(cube)))

    def test_scale_var_rules(self):
        # chirps: x < 0 -> NaN, else / 100
        out = inputs.scale_var("chirps", np.array([[1234, -9999, 0]], dtype=np.int32), None)
        self.assertAlmostEqual(float(out[0, 0]), 12.34, places=4)
        self.assertTrue(np.isnan(out[0, 1]))
        self.assertEqual(float(out[0, 2]), 0.0)

        # chirts: x <= -9990 -> NaN, else / 100 -> degrees Celsius
        temp = inputs.scale_var(
            "chirts_era5_tmax", np.array([[2750, -9999, -500]], dtype=np.int32), -9999
        )
        self.assertAlmostEqual(float(temp[0, 0]), 27.50, places=4)
        self.assertTrue(np.isnan(temp[0, 1]))
        self.assertAlmostEqual(float(temp[0, 2]), -5.00, places=4)

        # etref: float32 mm/day, negatives (incl. -9999) -> NaN, no division
        et = inputs.scale_var("etref", np.array([[4.5, -9999.0]], dtype=np.float32), -9999.0)
        self.assertAlmostEqual(float(et[0, 0]), 4.5, places=5)
        self.assertTrue(np.isnan(et[0, 1]))


class TestForecastCube(PhenologyInputsFixture):
    def _write_issue(self, issue, targets):
        folder = (
            self.dir_intermed / "chirps_gefs" / str(issue.year) / "issued"
            / issue.strftime("%Y%m%d")
        )
        for i, target in enumerate(targets):
            _write_tile(
                folder / f"c3g_{target.strftime('%Y.%m.%d')}.tif",
                np.full(TILE_SHAPE, 100 * (i + 1), dtype=np.int32),
                "int32",
                CHIRPS_NODATA,
            )
        return folder

    def test_read_forecast_cube_reads_the_issued_folder(self):
        issue = dt.date(2025, 9, 10)
        targets = [issue + dt.timedelta(days=k) for k in range(3)]
        self._write_issue(issue, targets)

        result = inputs.read_forecast_cube(self.parser, issue, INNER_WINDOW)
        self.assertIsNotNone(result)
        cube, dates = result
        self.assertEqual(cube.shape, (3, 20, 20))
        self.assertEqual(dates, targets)
        # file k holds 100 * (k + 1) mm x 100 -> (k + 1) mm/day
        self.assertAlmostEqual(float(cube[0, 0, 0]), 1.0, places=4)
        self.assertAlmostEqual(float(cube[2, 0, 0]), 3.0, places=4)

    def test_read_forecast_cube_returns_none_without_a_folder(self):
        self.assertIsNone(
            inputs.read_forecast_cube(self.parser, dt.date(2025, 9, 10), INNER_WINDOW)
        )

    def test_latest_forecast_issue_picks_the_newest(self):
        self.assertIsNone(inputs.latest_forecast_issue(self.parser))

        for issue in (dt.date(2025, 9, 3), dt.date(2025, 9, 10)):
            self._write_issue(issue, [issue])

        self.assertEqual(inputs.latest_forecast_issue(self.parser), dt.date(2025, 9, 10))
        self.assertEqual(
            inputs.latest_forecast_issue(self.parser, not_before=dt.date(2025, 9, 1)),
            dt.date(2025, 9, 10),
        )
        self.assertIsNone(
            inputs.latest_forecast_issue(self.parser, not_before=dt.date(2025, 9, 11))
        )


class TestCropFraction(PhenologyInputsFixture):
    def test_mask_percent_times_100_becomes_a_fraction(self):
        frac = inputs.read_crop_fraction(self.parser, "kenya", "maize", COUNTRY_WINDOW)
        self.assertEqual(frac.shape, (40, 40))
        self.assertEqual(frac.dtype, np.float32)
        # 5000 / 10000 = 0.5
        self.assertAlmostEqual(float(frac[5, 5]), 0.5, places=6)
        # 10000 / 10000 = 1.0
        self.assertAlmostEqual(float(frac[20, 20]), 1.0, places=6)
        # negative and nodata both collapse to 0, never NaN
        self.assertEqual(float(frac[0, 0]), 0.0)
        self.assertEqual(float(frac[0, 1]), 0.0)
        self.assertFalse(np.any(np.isnan(frac)))

    def test_use_cropland_mask_switches_the_config_section(self):
        # With use_cropland_mask = True the mask comes from [kenya], not [maize].
        self.parser.set("kenya", "use_cropland_mask", "True")
        self.parser.set("kenya", "mask", "cropland.tif")
        _write_tile(
            self.dir_masks / "cropland.tif",
            np.full(TILE_SHAPE, 2500, dtype=np.int32),
            "int32",
            -9999,
        )
        frac = inputs.read_crop_fraction(self.parser, "kenya", "maize", COUNTRY_WINDOW)
        self.assertAlmostEqual(float(frac[5, 5]), 0.25, places=6)  # 2500 / 10000


class TestCalendar(PhenologyInputsFixture):
    def setUp(self):
        super().setUp()
        self.zones, self.flags = inputs.load_calendar_zones(self.parser, "kenya", "maize")
        _window, self.transform, self.shape = inputs.window_for_bbox(
            (TILE_WEST, TILE_SOUTH, TILE_EAST, TILE_NORTH)
        )

    def test_zones_are_reprojected_to_4326(self):
        self.assertEqual(self.zones.crs.to_epsg(), 4326)
        self.assertEqual(
            sorted(self.zones["calendar_region"].tolist()), ["zone_a", "zone_b", "zone_c"]
        )
        # The polygons were written in EPSG:3857; after reprojection they must
        # land back on the 36-37 E / -0.5-1.0 N box they were defined on.
        west, south, east, north = self.zones.total_bounds
        self.assertAlmostEqual(west, 36.0, places=6)
        self.assertAlmostEqual(east, 37.0, places=6)
        self.assertAlmostEqual(south, -0.5, places=5)
        self.assertAlmostEqual(north, 1.0, places=5)

    def test_both_crop_sheets_are_loaded(self):
        self.assertEqual(sorted(self.flags), [1, 2])
        self.assertEqual(sorted(self.flags[1]), ["zone_a", "zone_b", "zone_c"])
        self.assertTrue(np.all(self.flags[1]["zone_c"] == -1))

    def test_within_year_season_dates(self):
        cal = inputs.rasterize_calendar(
            self.zones, self.flags, season=1, harvest_year=2025,
            transform=self.transform, shape=self.shape,
        )
        # Zone A occupies rows 10-19 (lat 0.5-1.0), cols 10-29 (lon 36-37).
        self.assertEqual(int(cal.zone_id[15, 15]), 1)
        self.assertEqual(int(cal.zone_id[25, 15]), 2)   # Zone B, rows 20-29
        self.assertEqual(int(cal.zone_id[35, 15]), 3)   # Zone C, rows 30-39
        self.assertEqual(int(cal.zone_id[5, 5]), 0)     # outside every zone
        self.assertEqual(cal.zone_id.dtype, np.int16)

        # apr_1 is bin 6 -> first day of the bin = Apr 1.
        # aug_15 is bin 15, the last bin flagged 3 -> last day of August = Aug 31.
        self.assertEqual(cal.planting[15, 15], np.datetime64("2025-04-01"))
        self.assertEqual(cal.harvest[15, 15], np.datetime64("2025-08-31"))
        self.assertEqual(cal.planting[25, 15], np.datetime64("2025-04-01"))

        # next_planting = earliest planting of ANY season after Aug 31 2025.
        # season 1 plants Apr 1 (2026-04-01), season 2 plants Oct 15
        # (2025-10-15) -> the October date wins.
        self.assertEqual(cal.next_planting[15, 15], np.datetime64("2025-10-15"))

    def test_cross_year_season_dates(self):
        cal = inputs.rasterize_calendar(
            self.zones, self.flags, season=2, harvest_year=2026,
            transform=self.transform, shape=self.shape,
        )
        # oct_15 is bin 19 -> planting Oct 15 of harvest_year - 1 = 2025.
        # feb_1 is bin 2, the last bin flagged 3, and 2 < 19 so the block wraps
        # -> harvest on the last day of that bin = Feb 14 2026.
        self.assertEqual(cal.planting[15, 15], np.datetime64("2025-10-15"))
        self.assertEqual(cal.harvest[15, 15], np.datetime64("2026-02-14"))
        # After Feb 14 2026 the next planting of any season is season 1's Apr 1.
        self.assertEqual(cal.next_planting[15, 15], np.datetime64("2026-04-01"))

    def test_all_minus_one_zone_is_nat_not_zero(self):
        cal = inputs.rasterize_calendar(
            self.zones, self.flags, season=1, harvest_year=2025,
            transform=self.transform, shape=self.shape,
        )
        self.assertEqual(int(cal.zone_id[35, 15]), 3)  # the zone IS burned...
        self.assertTrue(np.isnat(cal.planting[35, 15]))  # ...but has no dates
        self.assertTrue(np.isnat(cal.harvest[35, 15]))
        self.assertTrue(np.isnat(cal.next_planting[35, 15]))
        # Pixels with no zone at all are NaT too.
        self.assertTrue(np.isnat(cal.planting[5, 5]))

    def test_calendar_array_dtypes(self):
        cal = inputs.rasterize_calendar(
            self.zones, self.flags, season=1, harvest_year=2025,
            transform=self.transform, shape=self.shape,
        )
        self.assertEqual(cal.planting.dtype, np.dtype("datetime64[D]"))
        self.assertEqual(cal.harvest.dtype, np.dtype("datetime64[D]"))
        self.assertEqual(cal.next_planting.dtype, np.dtype("datetime64[D]"))
        self.assertEqual(cal.planting.shape, (40, 40))
        self.assertEqual(cal.zone_names, ["zone_a", "zone_b", "zone_c"])


class TestRasterizeAdmin(PhenologyInputsFixture):
    def test_admin_ids_and_lookup(self):
        _window, transform, shape = inputs.window_for_bbox(
            (TILE_WEST, TILE_SOUTH, TILE_EAST, TILE_NORTH)
        )
        id_grid, lookup = inputs.rasterize_admin(self.parser, "kenya", transform, shape)

        self.assertEqual(id_grid.shape, (40, 40))
        # West Unit: lon 36.0-36.5 -> cols 10-19; lat 0.0-1.0 -> rows 10-29.
        self.assertEqual(int(id_grid[15, 15]), 1)
        # East Unit: lon 36.5-37.0 -> cols 20-29.
        self.assertEqual(int(id_grid[15, 25]), 2)
        self.assertEqual(int(id_grid[35, 5]), 0)

        self.assertEqual(list(lookup["id"]), [1, 2])
        self.assertEqual(list(lookup["ADM_ID"]), [101, 102])
        self.assertEqual(list(lookup["ADM1_NAME"]), ["West Unit", "East Unit"])


if __name__ == "__main__":
    unittest.main()
