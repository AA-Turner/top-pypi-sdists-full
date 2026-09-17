# -*- coding: utf-8 -*-
"""Tests for geocif/phenology/climatology.py (DESIGN.md sections 7 and 11.1).

Everything is synthetic and lives in a temp tree, on the REAL global 0.05 deg
lattice (transform ``Affine(0.05, 0, -180, 0, -0.05, 90)``), in the same style
as tests/test_phenology_inputs.py:

    country box (35.5, -0.5, 37.5, 1.5) -> col_off = 215.5/0.05 = 4310
                                           row_off =  88.5/0.05 = 1770
                                           40 x 40 cells
    calendar zone box (36.0, 0.0, 37.0, 1.0) -> rows 10..29, cols 10..29
                                           (everything else has NO calendar)

The synthetic season (calendar ``cal_a.xlsx``, sheet ``maize_1``):
``apr_1 = 1`` and ``apr_15 = 3`` -> planting Apr 1, harvest Apr 30.

With ``search_start_days_before_planting = 5`` and ``cessation_grace_days = 20``
the cube therefore runs Mar 27 -> May 20:

    index 0..4   = Mar 27..31      (5 days)
    index 5..34  = Apr 1..30       (30 days; index 5 IS the planting day)
    index 35..54 = May 1..20       (20 days)          -> n_time = 55

Rain, per harvest year: nothing at all, then 25 mm on the "start day" s and
5 mm/day for the next 15 days, then nothing. With ``window_days = 3`` the
3-day window sum is 25 mm on day s (>= the 20 mm threshold), so the onset is
day s; with ``validation_days = 10`` and ``dry_spell_days = 5`` the look-ahead
[s+4, s+9] is entirely wet, so it validates.

    2001: s = Apr  6 -> index 10 -> 10 - 5 =  5 days after planting
    2002: s = Apr 11 -> index 15 -> 15 - 5 = 10 days after planting
    2003: s = Apr 16 -> index 20 -> 20 - 5 = 15 days after planting

2002 also carries a FALSE START: 25 mm on index 5 (Apr 1) followed by nine dry
days. r reaches dry_spell_days = 5 at index 10, which is inside that
candidate's look-ahead window [9, 14], so the episode 5..7 is invalidated and
``n_false_starts`` is 1 there.

Cessation, WHC = 20 mm, PET = 4 mm/day, min_season_days = 10,
empty_persist_days = 2, initial storage 0, from the onset day s:

    t = s          S = min(max(0 + 25 - 4, 0), 20) = 20   (capped at the WHC)
    t = s+1..s+15  S = min(20 + 5 - 4, 20)         = 20   (rain 5 > PET 4)
    t = s+16..s+19 S = 16, 12, 8, 4                       (no rain, -4/day)
    t = s+20       S = 0                 -> empty_run = 1
    t = s+21       S = 0                 -> empty_run = 2 = empty_persist_days
                   and s+21 >= s + min_season_days, so
                   cessation = (s+21) - 2 + 1 = s + 20

so eos = s + 20 and lgs = 20 days in every year:

    2001: eos = index 30 -> 25 days after planting
    2002: eos = index 35 -> 30 days after planting
    2003: eos = index 40 -> 35 days after planting

Summary over the three years at any in-zone pixel:
    onset_median = median(5, 10, 15) = 10, p25 = 7.5, p75 = 12.5,
    onset_std (ddof=1) = sqrt(((5-10)^2 + 0 + (15-10)^2) / 2) = 5.0,
    onset_n_valid = 3, onset_frac_no_onset = 0, false_start_rate = 1/3,
    eos_median = median(25, 30, 35) = 30, lgs_median = 20,
    eos_frac_censored = 0, eos_frac_at_floor = 0.

The PET-calibration fixture is separate (years 2010-2011, days 1/11/21 of each
month) and writes ``etref = 1.6 x hargreaves`` so the recovered factor must be
1.6.
"""
import configparser
import datetime as dt
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

import numpy as np
import pandas as pd
import rasterio
from affine import Affine

from geocif.phenology import climatology, core, inputs

# --- the synthetic country window ------------------------------------------
TILE_WEST, TILE_SOUTH, TILE_EAST, TILE_NORTH = 35.5, -0.5, 37.5, 1.5
TILE_TRANSFORM = Affine(0.05, 0, TILE_WEST, 0, -0.05, TILE_NORTH)
TILE_SHAPE = (40, 40)

CHIRPS_NODATA = -2147483648
FLOAT_NODATA = -9999.0

IN_ZONE = (15, 15)      # inside the calendar zone (rows/cols 10..29)
OUT_OF_ZONE = (0, 0)    # no calendar covers this pixel

MONTHS = ["jan", "feb", "mar", "apr", "may", "jun",
          "jul", "aug", "sep", "oct", "nov", "dec"]
BIN_COLS = [f"{m}_{d}" for m in MONTHS for d in (1, 15)]

CUBE_START = dt.date(2001, 3, 27)   # only the month/day matter, per year
CUBE_END = dt.date(2001, 5, 20)
N_TIME = 55                          # Mar 27 -> May 20 inclusive

# onset day (index into the cube) per harvest year
ONSET_INDEX = {2001: 10, 2002: 15, 2003: 20}
PLANTING_INDEX = 5                   # Apr 1 is index 5 of the cube

# The three 2001 days whose etref file is deliberately absent (index 0, 1, 2),
# so the Hargreaves gap-fill has something to do. They sit before every onset.
ETREF_GAP_DAYS = [dt.date(2001, 3, 27), dt.date(2001, 3, 28), dt.date(2001, 3, 29)]

# Harvest year 2004: the rasters stop on the harvest date (Apr 30 = index 34),
# so the cube is 35 days long and the one rain event cannot be validated.
TRUNCATED_N_TIME = 35
TRUNCATED_TRIGGER_INDEX = 30

PET_YEARS = (2010, 2011)
PET_FACTOR = 1.6
PET_TMIN_C = 18.0
PET_TMAX_C = 32.0


def _test_params(**overrides):
    """The parameter set the docstring arithmetic is based on."""
    kwargs = dict(
        onset=core.OnsetParams(
            precip_threshold=20.0,
            window_days=3,
            dry_spell_days=5,
            dry_day_threshold=1.0,
            validation_days=10,
        ),
        cessation=core.CessationParams(
            soil_whc=20.0,
            min_season_days=10,
            empty_persist_days=2,
            initial_storage=0.0,
        ),
        search_start_days_before_planting=5,
        cessation_grace_days=20,
        min_valid_years=3,
        pet_calibration_years=(2001,),
    )
    kwargs.update(overrides)
    return climatology.ClimatologyParams(**kwargs)


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


def _tile_hargreaves(day):
    """Reference Hargreaves PET (mm/day) over the whole tile for one date."""
    lat = inputs.pixel_centres(TILE_TRANSFORM, TILE_SHAPE)[1]
    tmin = np.full((1,) + TILE_SHAPE, PET_TMIN_C, dtype=np.float64)
    tmax = np.full((1,) + TILE_SHAPE, PET_TMAX_C, dtype=np.float64)
    doy = np.array([day.timetuple().tm_yday], dtype=np.float64)
    return core.hargreaves_pet(tmin, tmax, doy, lat)[0]


class PhenologyClimatologyFixture(unittest.TestCase):
    """Synthetic config tree + daily rasters, built once per test class."""

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
        cls._write_calendars()
        cls.parser = cls._build_parser("cal_a.xlsx")
        cls.parser_next_season = cls._build_parser("cal_b.xlsx")
        cls._write_season_rasters()
        cls._write_pet_rasters()

    # -- config ------------------------------------------------------------
    @classmethod
    def _build_parser(cls, calendar_file):
        parser = configparser.ConfigParser(
            interpolation=configparser.ExtendedInterpolation(),
            inline_comment_prefixes=(";",),
        )
        parser.read_dict({
            "PATHS": {
                "dir_intermed": str(cls.dir_intermed),
                "dir_crop_masks": str(cls.dir_masks),
                "dir_boundary_files": str(cls.dir_boundaries),
                "dir_crop_calendars": str(cls.dir_calendars),
                "dir_output": str(cls.dir_output),
            },
            "CHIRPS": {"version": "v3"},
            # Section named after the boundary file stem so
            # geoprepare.georegion.get_boundary_col_mapping keeps our columns.
            "test_adm": {
                "adm0_col": "ADM0_NAME",
                "adm1_col": "ADM1_NAME",
                "id_col": "ADM_ID",
            },
            "kenya": {
                "boundary_file": "test_adm.gpkg",
                "shp_region": "test_zones.gpkg",
                "calendar_file": calendar_file,
                "use_cropland_mask": "False",
            },
            "maize": {"mask": "maize_mask.tif"},
        })
        parser.set("DEFAULT", "project_name", "testproj")
        return parser

    # -- fixture writers ---------------------------------------------------
    @classmethod
    def _write_boundaries(cls):
        import geopandas as gpd
        from shapely.geometry import box

        gdf = gpd.GeoDataFrame(
            {
                "ADM0_NAME": ["Kenya"],
                "ADM1_NAME": ["Only Unit"],
                "ADM_ID": [101],
            },
            geometry=[box(36.0, 0.0, 37.0, 1.0)],
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
    def _write_calendars(cls):
        """cal_a: maize_1 only. cal_b: maize_1 plus a maize_2 planted May 1.

        maize_1: apr_1 = 1, apr_15 = 3 -> planting Apr 1, harvest Apr 30.
        maize_2: may_1 = 1, may_15 = 2, jun_1 = 3 -> planting May 1, so
        ``next_planting`` for maize_1 becomes May 1 and the cessation search
        end is capped at Apr 30 (index 34) instead of running to index 54.
        """
        season_1 = {"apr_1": 1, "apr_15": 3}
        season_2 = {"may_1": 1, "may_15": 2, "jun_1": 3}

        def _sheet(pairs):
            row = {"admin": "Zone A", "country": "Kenya", "Country2": "Kenya", "Admin2": ""}
            row.update(_bins(pairs))
            return pd.DataFrame(
                [row], columns=["admin", "country", "Country2", "Admin2"] + BIN_COLS
            )

        with pd.ExcelWriter(cls.dir_calendars / "cal_a.xlsx", engine="openpyxl") as writer:
            _sheet(season_1).to_excel(writer, sheet_name="maize_1", index=False)
        with pd.ExcelWriter(cls.dir_calendars / "cal_b.xlsx", engine="openpyxl") as writer:
            _sheet(season_1).to_excel(writer, sheet_name="maize_1", index=False)
            _sheet(season_2).to_excel(writer, sheet_name="maize_2", index=False)

    @classmethod
    def _cube_dates(cls, year):
        start = dt.date(year, CUBE_START.month, CUBE_START.day)
        end = dt.date(year, CUBE_END.month, CUBE_END.day)
        return [start + dt.timedelta(days=i) for i in range((end - start).days + 1)]

    @classmethod
    def _write_season_rasters(cls):
        """CHIRPS for every cube day of 2001-2003, etref (with a 3-day gap) and
        CHIRTS only where that gap needs filling."""
        for year, onset_idx in ONSET_INDEX.items():
            dates = cls._cube_dates(year)
            rain_mm = np.zeros(len(dates), dtype=np.float64)
            rain_mm[onset_idx] = 25.0
            rain_mm[onset_idx + 1: onset_idx + 16] = 5.0
            if year == 2002:
                rain_mm[PLANTING_INDEX] = 25.0   # the false start, invalidated
            for i, day in enumerate(dates):
                _write_tile(
                    inputs.daily_path(cls.parser, "chirps", day),
                    np.full(TILE_SHAPE, int(round(rain_mm[i] * 100)), dtype=np.int32),
                    "int32",
                    CHIRPS_NODATA,
                )
                if day in ETREF_GAP_DAYS:
                    for var, degc in (("chirts_era5_tmin", PET_TMIN_C),
                                      ("chirts_era5_tmax", PET_TMAX_C)):
                        _write_tile(
                            inputs.daily_path(cls.parser, var, day),
                            np.full(TILE_SHAPE, int(degc * 100), dtype=np.int32),
                            "int32", -9999,
                        )
                    continue
                _write_tile(
                    inputs.daily_path(cls.parser, "etref", day),
                    np.full(TILE_SHAPE, 4.0, dtype=np.float32),
                    "float32",
                    FLOAT_NODATA,
                )
        cls._write_truncated_year()

    @classmethod
    def _write_truncated_year(cls):
        """Harvest year 2004: the data stops on the harvest date itself.

        Only Mar 27 .. Apr 30 exist on disk, so the cube is clipped to 35 days
        (indices 0..34) instead of the usual 55. The single 25 mm day sits at
        index 30 (Apr 26): the 3-day window makes indices 30..32 trigger days,
        but ``30 + validation_days (10) > 35`` so none of them can be validated
        and none is invalidated either. That separates the two meanings of
        ``n_false_starts``: ``core.season_phenology`` would count this episode
        (1), the INVALIDATED-episode meaning this package reports counts 0.
        """
        start = dt.date(2004, 3, 27)
        dates = [start + dt.timedelta(days=i) for i in range(TRUNCATED_N_TIME)]
        for i, day in enumerate(dates):
            rain_mm = 25.0 if i == TRUNCATED_TRIGGER_INDEX else 0.0
            _write_tile(
                inputs.daily_path(cls.parser, "chirps", day),
                np.full(TILE_SHAPE, int(round(rain_mm * 100)), dtype=np.int32),
                "int32", CHIRPS_NODATA,
            )
            _write_tile(
                inputs.daily_path(cls.parser, "etref", day),
                np.full(TILE_SHAPE, 4.0, dtype=np.float32),
                "float32", FLOAT_NODATA,
            )

    @classmethod
    def _write_pet_rasters(cls):
        """etref = 1.6 x Hargreaves on days 1/11/21 of every month of 2010-2011.

        Two pixels break the pattern so the clip is exercised, and a third has
        no etref at all so the median fallback is exercised:
            (0, 0) etref = 5.0 x hargreaves -> k clipped to 2.0
            (0, 1) etref = 0.1 x hargreaves -> k clipped to 0.5
            (0, 2) etref = nodata           -> k = window median = 1.6
        """
        for year in PET_YEARS:
            for month in range(1, 13):
                for day_of_month in (1, 11, 21):
                    day = dt.date(year, month, day_of_month)
                    hg = _tile_hargreaves(day)
                    etref = (PET_FACTOR * hg).astype(np.float32)
                    etref[0, 0] = np.float32(5.0 * hg[0, 0])
                    etref[0, 1] = np.float32(0.1 * hg[0, 1])
                    etref[0, 2] = np.float32(FLOAT_NODATA)
                    _write_tile(
                        inputs.daily_path(cls.parser, "etref", day),
                        etref, "float32", FLOAT_NODATA,
                    )
                    for var, degc in (("chirts_era5_tmin", PET_TMIN_C),
                                      ("chirts_era5_tmax", PET_TMAX_C)):
                        _write_tile(
                            inputs.daily_path(cls.parser, var, day),
                            np.full(TILE_SHAPE, int(degc * 100), dtype=np.int32),
                            "int32", -9999,
                        )

    # -- helpers -----------------------------------------------------------
    def out_dir(self, name):
        path = self.dir_output / "cases" / name
        path.mkdir(parents=True, exist_ok=True)
        return path

    def read_band(self, path, to_float=True):
        with rasterio.open(Path(path)) as src:
            data = src.read(1)
            nodata = src.nodata
            dtype = src.dtypes[0]
        if to_float:
            out = data.astype(np.float64)
            if nodata is not None and np.isfinite(nodata):
                out[data == nodata] = np.nan
            return out, dtype, nodata
        return data, dtype, nodata


# ---------------------------------------------------------------------------
# Pure-function tests (no fixture needed)
# ---------------------------------------------------------------------------
class _FakeCalendar:
    """Minimal stand-in for inputs.SeasonCalendar (only the date arrays matter)."""

    def __init__(self, planting, harvest, next_planting):
        self.planting = np.array(planting, dtype="datetime64[D]")
        self.harvest = np.array(harvest, dtype="datetime64[D]")
        self.next_planting = np.array(next_planting, dtype="datetime64[D]")


class TestSeasonIndices(unittest.TestCase):
    def test_search_end_is_capped_by_the_next_planting(self):
        # start_date 2001-03-27 (index 0). Pixel 0: planting Apr 1 (index 5),
        # harvest Apr 30 (index 34), next planting May 1 (index 35).
        #   grace cap    = 34 + 20 = 54
        #   next-season  = 35 - 1  = 34   <- binds
        #   cube cap     = 55 - 1  = 54
        # Pixel 1 has no next season: min(54, 54) = 54.
        # Pixel 2 has no calendar at all -> NaN everywhere.
        cal = _FakeCalendar(
            planting=["2001-04-01", "2001-04-01", "NaT"],
            harvest=["2001-04-30", "2001-04-30", "NaT"],
            next_planting=["2001-05-01", "NaT", "NaT"],
        )
        params = _test_params()
        start, end, search_end = climatology.season_indices(
            cal, dt.date(2001, 3, 27), N_TIME, params
        )
        self.assertEqual(list(start[:2]), [0.0, 0.0])      # 5 - 5 = 0
        self.assertEqual(list(end[:2]), [34.0, 34.0])
        self.assertEqual(float(search_end[0]), 34.0)       # next-planting cap
        self.assertEqual(float(search_end[1]), 54.0)       # cube cap
        for arr in (start, end, search_end):
            self.assertTrue(np.isnan(arr[2]))
            self.assertEqual(arr.dtype, np.float32)

    def test_search_start_is_floored_at_zero_and_grace_can_bind(self):
        # planting index 5, search opens 30 days early -> -25, floored to 0.
        # harvest index 34 + grace 3 = 37, which is below both other caps.
        cal = _FakeCalendar(
            planting=["2001-04-01"], harvest=["2001-04-30"], next_planting=["NaT"]
        )
        params = _test_params(search_start_days_before_planting=30, cessation_grace_days=3)
        start, end, search_end = climatology.season_indices(
            cal, dt.date(2001, 3, 27), N_TIME, params
        )
        self.assertEqual(float(start[0]), 0.0)
        self.assertEqual(float(end[0]), 34.0)
        self.assertEqual(float(search_end[0]), 37.0)

    def test_planting_offset(self):
        cal = _FakeCalendar(
            planting=["2001-04-01", "NaT"], harvest=["2001-04-30", "NaT"],
            next_planting=["NaT", "NaT"],
        )
        offset = climatology.planting_offset(cal, dt.date(2001, 3, 27))
        self.assertEqual(float(offset[0]), 5.0)   # Mar 27 -> Apr 1 is 5 days
        self.assertTrue(np.isnan(offset[1]))


class TestCalibratedPet(unittest.TestCase):
    def test_etref_wins_and_gaps_use_the_calibrated_hargreaves(self):
        dates = [dt.date(2021, 1, 10), dt.date(2021, 6, 10)]
        lat = np.array([0.0, 10.0])
        tmin = np.full((2, 2, 1), 18.0)
        tmax = np.full((2, 2, 1), 32.0)
        etref = np.full((2, 2, 1), 4.0)
        etref[0, 0, 0] = np.nan   # January, row 0 -> filled with k[0] * hg
        etref[1, 1, 0] = np.nan   # June, row 1    -> filled with k[5] * hg

        k = np.ones((12, 2, 1), dtype=np.float32)
        k[0] = 2.0
        k[5] = 0.5

        pet, n_filled = climatology.calibrated_pet(etref, tmin, tmax, dates, lat, k)
        hg = core.hargreaves_pet(
            tmin, tmax, np.array([10.0, 161.0]), lat
        )  # Jan 10 = DOY 10, Jun 10 = DOY 161 (2021 is not a leap year)

        self.assertEqual(n_filled, 2)
        self.assertEqual(pet.dtype, np.float32)
        self.assertAlmostEqual(float(pet[0, 0, 0]), 2.0 * float(hg[0, 0, 0]), places=4)
        self.assertAlmostEqual(float(pet[1, 1, 0]), 0.5 * float(hg[1, 1, 0]), places=4)
        # every other cell is untouched etref
        self.assertAlmostEqual(float(pet[0, 1, 0]), 4.0, places=6)
        self.assertAlmostEqual(float(pet[1, 0, 0]), 4.0, places=6)

    def test_no_chirts_means_no_fill(self):
        dates = [dt.date(2021, 1, 10)]
        etref = np.array([[[np.nan, 3.0]]])
        pet, n_filled = climatology.calibrated_pet(
            etref, None, None, dates, np.array([0.0]), None
        )
        self.assertEqual(n_filled, 0)
        self.assertTrue(np.isnan(pet[0, 0, 0]))
        self.assertAlmostEqual(float(pet[0, 0, 1]), 3.0, places=6)


# ---------------------------------------------------------------------------
# PET calibration on synthetic rasters (DESIGN 11.1)
# ---------------------------------------------------------------------------
class TestPetCalibration(PhenologyClimatologyFixture):
    def _build(self, **kwargs):
        window, transform, shape = inputs.window_for_bbox(
            (TILE_WEST, TILE_SOUTH, TILE_EAST, TILE_NORTH)
        )
        options = dict(
            years=PET_YEARS,
            min_years=1,
            day_stride=10,          # days 1, 11, 21 (and 31, which is absent)
            min_days_per_month=3,
        )
        options.update(kwargs)
        return climatology.build_pet_calibration(
            self.parser, "kenya", window, transform, shape, **options
        )

    def test_recovers_the_injected_factor_with_clip_and_median_fallback(self):
        k = self._build()
        self.assertEqual(k.shape, (12,) + TILE_SHAPE)
        self.assertEqual(k.dtype, np.float32)
        self.assertTrue(np.isfinite(k).all())

        for month in range(12):
            # mean(etref) / mean(hargreaves) = 1.6 x hg / hg = 1.6 exactly
            self.assertAlmostEqual(float(k[month, 20, 20]), PET_FACTOR, places=3)
            # 5.0 -> clipped to the 2.0 ceiling, 0.1 -> clipped to the 0.5 floor
            self.assertAlmostEqual(float(k[month, 0, 0]), climatology.PET_K_MAX, places=6)
            self.assertAlmostEqual(float(k[month, 0, 1]), climatology.PET_K_MIN, places=6)
            # no etref at all -> the window median of the fitted values
            self.assertAlmostEqual(float(k[month, 0, 2]), PET_FACTOR, places=3)

    def test_min_years_gate_falls_back_to_one(self):
        # Only two years exist; requiring three leaves every pixel-month
        # undefined, and a month with nothing fitted falls back to 1.0.
        k = self._build(min_years=3)
        self.assertTrue(np.allclose(k, climatology.PET_K_FALLBACK))

    def test_cache_is_written_and_reused(self):
        cache = self.out_dir("pet_cache") / climatology.PET_CALIBRATION_FILE
        first = self._build(cache_path=cache)
        self.assertTrue(cache.is_file())
        with rasterio.open(cache) as src:
            self.assertEqual(src.count, 12)
            self.assertEqual(src.dtypes[0], "float32")

        # The second call must come from the cache, not from the rasters.
        with mock.patch.object(inputs, "read_cube", side_effect=AssertionError("re-read")):
            second = self._build(cache_path=cache)
        np.testing.assert_allclose(first, second)

        loaded = climatology.load_pet_calibration(cache)
        self.assertIsNotNone(loaded)
        np.testing.assert_allclose(loaded, first)
        self.assertIsNone(climatology.load_pet_calibration(cache.parent / "missing.tif"))


# ---------------------------------------------------------------------------
# The build
# ---------------------------------------------------------------------------
class TestBuildClimatology(PhenologyClimatologyFixture):
    """One three-year build, shared by every assertion in this class."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.params = _test_params()
        cls.case_dir = cls.dir_output / "cases" / "main"
        cls.paths = climatology.build_climatology(
            cls.parser, "kenya", "maize", 1, [2001, 2002, 2003],
            cls.params, cls.case_dir, n_workers=1,
        )
        cls.manifest = json.loads(
            (cls.case_dir / climatology.MANIFEST_FILE).read_text(encoding="utf-8")
        )

    def test_every_yearly_layer_exists_with_the_right_dtype_and_nodata(self):
        for year in (2001, 2002, 2003):
            for layer, (dtype, nodata) in climatology.YEAR_LAYERS.items():
                path = self.case_dir / climatology.YEAR_SUBDIR / f"{layer}_{year}.tif"
                self.assertTrue(path.is_file(), f"missing {path.name}")
                self.assertEqual(self.paths[f"{layer}_{year}"], path)
                _data, actual_dtype, actual_nodata = self.read_band(path)
                self.assertEqual(actual_dtype, dtype, f"{layer}_{year} dtype")
                self.assertEqual(actual_nodata, nodata, f"{layer}_{year} nodata")

    def test_every_summary_layer_exists_with_the_right_dtype_and_nodata(self):
        for layer, (dtype, nodata) in climatology.SUMMARY_LAYERS.items():
            path = self.case_dir / f"{layer}.tif"
            self.assertTrue(path.is_file(), f"missing {path.name}")
            self.assertEqual(self.paths[layer], path)
            _data, actual_dtype, actual_nodata = self.read_band(path)
            self.assertEqual(actual_dtype, dtype, f"{layer} dtype")
            if np.isnan(nodata):
                self.assertTrue(np.isnan(actual_nodata), f"{layer} nodata")
            else:
                self.assertEqual(actual_nodata, nodata, f"{layer} nodata")

    def test_days_since_planting_matches_the_hand_built_rain_series(self):
        row, col = IN_ZONE
        for year, expected_sos in ((2001, 5), (2002, 10), (2003, 15)):
            sos, _dtype, _nd = self.read_band(
                self.case_dir / climatology.YEAR_SUBDIR / f"sos_{year}.tif"
            )
            eos, _dtype, _nd = self.read_band(
                self.case_dir / climatology.YEAR_SUBDIR / f"eos_{year}.tif"
            )
            lgs, _dtype, _nd = self.read_band(
                self.case_dir / climatology.YEAR_SUBDIR / f"lgs_{year}.tif"
            )
            self.assertEqual(float(sos[row, col]), float(expected_sos), f"sos {year}")
            # cessation is 20 days after onset in every year (see the docstring)
            self.assertEqual(float(eos[row, col]), float(expected_sos + 20), f"eos {year}")
            self.assertEqual(float(lgs[row, col]), 20.0, f"lgs {year}")

    def test_statuses_and_false_starts(self):
        row, col = IN_ZONE
        for year in (2001, 2002, 2003):
            sos_status, _d, _n = self.read_band(
                self.case_dir / climatology.YEAR_SUBDIR / f"sos_status_{year}.tif",
                to_float=False,
            )
            eos_status, _d, _n = self.read_band(
                self.case_dir / climatology.YEAR_SUBDIR / f"eos_status_{year}.tif",
                to_float=False,
            )
            self.assertEqual(int(sos_status[row, col]), int(core.OnsetStatus.OK))
            self.assertEqual(int(eos_status[row, col]), int(core.CessationStatus.OK))
            # no calendar -> the -1 sentinel, never a core status code
            self.assertEqual(int(sos_status[OUT_OF_ZONE]), climatology.STATUS_NODATA)
            self.assertEqual(int(eos_status[OUT_OF_ZONE]), climatology.STATUS_NODATA)

        # 2002 alone carries an invalidated candidate episode (index 5..7).
        expected_false = {2001: 0, 2002: 1, 2003: 0}
        for year, expected in expected_false.items():
            n_false, _d, _n = self.read_band(
                self.case_dir / climatology.YEAR_SUBDIR / f"n_false_starts_{year}.tif",
                to_float=False,
            )
            self.assertEqual(int(n_false[row, col]), expected, f"n_false_starts {year}")
            self.assertEqual(int(n_false[OUT_OF_ZONE]), climatology.INT16_NODATA)

        # first_candidate: 2002 triggers on the planting day itself (offset 0)
        first, _d, _n = self.read_band(
            self.case_dir / climatology.YEAR_SUBDIR / "first_candidate_2002.tif"
        )
        self.assertEqual(float(first[row, col]), 0.0)

    def test_pixels_without_a_calendar_are_nodata(self):
        sos, _dtype, _nd = self.read_band(
            self.case_dir / climatology.YEAR_SUBDIR / "sos_2001.tif"
        )
        self.assertTrue(np.isnan(sos[OUT_OF_ZONE]))
        median, _dtype, _nd = self.read_band(self.case_dir / "onset_median.tif")
        self.assertTrue(np.isnan(median[OUT_OF_ZONE]))
        self.assertEqual(float(median[IN_ZONE]), 10.0)

    def test_summary_statistics(self):
        expected = {
            "onset_median": 10.0,    # median(5, 10, 15)
            "onset_p25": 7.5,        # linear interpolation between 5 and 10
            "onset_p75": 12.5,
            "onset_std": 5.0,        # sqrt((25 + 0 + 25) / 2)
            "onset_n_valid": 3.0,
            "onset_frac_no_onset": 0.0,
            "false_start_rate": 1.0 / 3.0,   # 2002 only
            "eos_median": 30.0,      # median(25, 30, 35)
            "lgs_median": 20.0,
            "eos_frac_censored": 0.0,
            "eos_frac_at_floor": 0.0,
        }
        for layer, value in expected.items():
            data, _dtype, _nd = self.read_band(self.case_dir / f"{layer}.tif")
            self.assertAlmostEqual(float(data[IN_ZONE]), value, places=4, msg=layer)

    def test_manifest_contents(self):
        self.assertEqual(self.manifest["years"], [2001, 2002, 2003])
        self.assertEqual(self.manifest["years_requested"], [2001, 2002, 2003])
        self.assertEqual(self.manifest["failed_years"], {})
        self.assertEqual(self.manifest["country"], "kenya")
        self.assertEqual(self.manifest["crop"], "maize")
        self.assertEqual(self.manifest["season"], 1)
        self.assertEqual(self.manifest["shape"], [40, 40])
        self.assertEqual(
            [round(v, 6) for v in self.manifest["bounds"]],
            [TILE_WEST, TILE_SOUTH, TILE_EAST, TILE_NORTH],
        )
        self.assertEqual(self.manifest["data_through"], "2003-05-20")
        self.assertEqual(self.manifest["summary_layers"], list(climatology.SUMMARY_LAYERS))
        self.assertNotEqual(self.manifest["geocif_version"], "")
        self.assertEqual(
            self.manifest["params_hash"],
            climatology.params_hash(
                self.params, "kenya", "maize", 1, [2001, 2002, 2003], (40, 40),
                (TILE_WEST, TILE_SOUTH, TILE_EAST, TILE_NORTH),
            ),
        )
        # the cube is the 55 days of the docstring, and 2001 needed the
        # Hargreaves gap-fill on three days x 1600 pixels
        meta_2001 = self.manifest["year_meta"]["2001"]
        self.assertEqual(meta_2001["n_days"], N_TIME)
        self.assertEqual(meta_2001["start_date"], "2001-03-27")
        self.assertEqual(meta_2001["end_date"], "2001-05-20")
        self.assertEqual(meta_2001["n_missing_etref"], len(ETREF_GAP_DAYS))
        self.assertEqual(meta_2001["n_hargreaves_filled"], len(ETREF_GAP_DAYS) * 40 * 40)
        self.assertEqual(self.manifest["year_meta"]["2002"]["n_hargreaves_filled"], 0)

    def test_pet_calibration_is_written_beside_the_climatology(self):
        path = self.case_dir / climatology.PET_CALIBRATION_FILE
        self.assertTrue(path.is_file())
        self.assertEqual(self.paths["pet_calibration"], path)
        k = climatology.load_pet_calibration(path)
        self.assertEqual(k.shape, (12,) + TILE_SHAPE)
        # 2001 has no day with BOTH etref and CHIRTS, so nothing is fitted and
        # every month falls back to 1.0.
        np.testing.assert_allclose(k, climatology.PET_K_FALLBACK)

    def test_load_climatology_round_trip(self):
        loaded = climatology.load_climatology(self.case_dir)
        self.assertIsNotNone(loaded)
        arrays, manifest = loaded
        self.assertEqual(manifest["years"], [2001, 2002, 2003])
        for layer in climatology.SUMMARY_LAYERS:
            self.assertIn(layer, arrays)
            self.assertEqual(arrays[layer].shape, TILE_SHAPE)
        self.assertEqual(arrays["onset_n_valid"].dtype, np.int16)
        self.assertEqual(arrays["onset_median"].dtype, np.float32)
        self.assertAlmostEqual(float(arrays["onset_median"][IN_ZONE]), 10.0, places=4)
        self.assertTrue(np.isnan(arrays["onset_median"][OUT_OF_ZONE]))

        self.assertEqual(arrays["onset_stack"].shape, (3,) + TILE_SHAPE)
        np.testing.assert_allclose(
            arrays["onset_stack"][:, IN_ZONE[0], IN_ZONE[1]], [5.0, 10.0, 15.0]
        )
        self.assertTrue(np.isnan(arrays["onset_stack"][0][OUT_OF_ZONE]))
        self.assertEqual(arrays["pet_calibration"].shape, (12,) + TILE_SHAPE)

        self.assertIsNone(climatology.load_climatology(self.case_dir / "nope"))

    def test_climatology_dir_layout(self):
        path = climatology.climatology_dir(self.parser, "kenya", "maize", 1)
        self.assertEqual(
            path,
            self.dir_output / "testproj" / "phenology" / "climatology" / "kenya" / "maize" / "s1",
        )


class TestSearchEndCap(PhenologyClimatologyFixture):
    def test_next_planting_cap_censors_the_cessation(self):
        """Same year, same rain: only the second season's planting date differs.

        2003 onset is index 20 and the bucket empties at index 40. With no next
        season the search runs to index 54 and cessation is found (35 days after
        planting). Adding a maize_2 planted May 1 caps the search at index 34,
        so the same pixel comes back RIGHT_CENSORED with no eos at all.
        """
        params = _test_params(min_valid_years=1)
        uncapped = climatology.build_climatology(
            self.parser, "kenya", "maize", 1, [2003], params,
            self.out_dir("uncapped"), n_workers=1,
        )
        capped = climatology.build_climatology(
            self.parser_next_season, "kenya", "maize", 1, [2003], params,
            self.out_dir("capped"), n_workers=1,
        )

        eos_free, _d, _n = self.read_band(uncapped["eos_2003"])
        status_free, _d, _n = self.read_band(uncapped["eos_status_2003"], to_float=False)
        self.assertEqual(float(eos_free[IN_ZONE]), 35.0)
        self.assertEqual(int(status_free[IN_ZONE]), int(core.CessationStatus.OK))

        eos_capped, _d, _n = self.read_band(capped["eos_2003"])
        status_capped, _d, _n = self.read_band(capped["eos_status_2003"], to_float=False)
        self.assertTrue(np.isnan(eos_capped[IN_ZONE]))
        self.assertEqual(
            int(status_capped[IN_ZONE]), int(core.CessationStatus.RIGHT_CENSORED)
        )
        # onset is unaffected by the cessation cap
        sos_capped, _d, _n = self.read_band(capped["sos_2003"])
        self.assertEqual(float(sos_capped[IN_ZONE]), 15.0)


class TestCacheAndRebuild(PhenologyClimatologyFixture):
    def test_params_hash_drives_the_rebuild(self):
        params = _test_params(min_valid_years=1)
        out_dir = self.out_dir("rebuild")
        first = climatology.build_climatology(
            self.parser, "kenya", "maize", 1, [2001], params, out_dir, n_workers=1
        )
        stamp = Path(first["sos_2001"]).stat().st_mtime_ns

        # 1. same params -> cache hit, nothing is rewritten
        again = climatology.build_climatology(
            self.parser, "kenya", "maize", 1, [2001], params, out_dir, n_workers=1
        )
        self.assertEqual(Path(again["sos_2001"]).stat().st_mtime_ns, stamp)
        self.assertEqual(set(again), set(first))

        # 2. a different parameter -> different hash -> rebuild
        other = _test_params(
            min_valid_years=1,
            onset=core.OnsetParams(
                precip_threshold=21.0, window_days=3, dry_spell_days=5,
                dry_day_threshold=1.0, validation_days=10,
            ),
        )
        self.assertNotEqual(
            climatology.params_hash(params, "kenya", "maize", 1, [2001], (40, 40),
                                    (TILE_WEST, TILE_SOUTH, TILE_EAST, TILE_NORTH)),
            climatology.params_hash(other, "kenya", "maize", 1, [2001], (40, 40),
                                    (TILE_WEST, TILE_SOUTH, TILE_EAST, TILE_NORTH)),
        )
        changed = climatology.build_climatology(
            self.parser, "kenya", "maize", 1, [2001], other, out_dir, n_workers=1
        )
        stamp_changed = Path(changed["sos_2001"]).stat().st_mtime_ns
        self.assertNotEqual(stamp_changed, stamp)

        # 3. rebuild=True rewrites even when the hash matches
        forced = climatology.build_climatology(
            self.parser, "kenya", "maize", 1, [2001], other, out_dir,
            n_workers=1, rebuild=True,
        )
        self.assertNotEqual(Path(forced["sos_2001"]).stat().st_mtime_ns, stamp_changed)

        # a changed year list also changes the hash
        self.assertNotEqual(
            climatology.params_hash(params, "kenya", "maize", 1, [2001], (40, 40),
                                    (TILE_WEST, TILE_SOUTH, TILE_EAST, TILE_NORTH)),
            climatology.params_hash(params, "kenya", "maize", 1, [2001, 2002], (40, 40),
                                    (TILE_WEST, TILE_SOUTH, TILE_EAST, TILE_NORTH)),
        )


class TestFailingYearIsSkipped(PhenologyClimatologyFixture):
    def test_one_bad_year_does_not_abort_the_build(self):
        real = climatology._build_year_payload

        def _boom(payload):
            if int(payload.year) == 2002:
                raise RuntimeError("synthetic failure for 2002")
            return real(payload)

        params = _test_params(min_valid_years=1)
        out_dir = self.out_dir("failing_year")
        with mock.patch.object(climatology, "_build_year_payload", _boom):
            paths = climatology.build_climatology(
                self.parser, "kenya", "maize", 1, [2001, 2002, 2003],
                params, out_dir, n_workers=1,
            )

        self.assertIn("sos_2001", paths)
        self.assertIn("sos_2003", paths)
        self.assertNotIn("sos_2002", paths)
        self.assertFalse(
            (out_dir / climatology.YEAR_SUBDIR / "sos_2002.tif").is_file()
        )

        manifest = json.loads(
            (out_dir / climatology.MANIFEST_FILE).read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["years"], [2001, 2003])
        self.assertEqual(manifest["years_requested"], [2001, 2002, 2003])
        self.assertIn("2002", manifest["failed_years"])
        self.assertIn("synthetic failure", manifest["failed_years"]["2002"])

        # the summary is built from the surviving years only: median(5, 15) = 10
        n_valid, _d, _n = self.read_band(out_dir / "onset_n_valid.tif", to_float=False)
        median, _d, _n = self.read_band(out_dir / "onset_median.tif")
        self.assertEqual(int(n_valid[IN_ZONE]), 2)
        self.assertEqual(float(median[IN_ZONE]), 10.0)

    def test_every_year_failing_raises(self):
        def _boom(payload):
            raise RuntimeError("synthetic failure")

        with mock.patch.object(climatology, "_build_year_payload", _boom):
            with self.assertRaises(RuntimeError):
                climatology.build_climatology(
                    self.parser, "kenya", "maize", 1, [2001], _test_params(min_valid_years=1),
                    self.out_dir("all_failing"), n_workers=1,
                )


class TestTruncatedYear(PhenologyClimatologyFixture):
    """The cube is clipped at the last day on disk, and false starts are the
    INVALIDATED episodes only."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.case_dir = cls.dir_output / "cases" / "truncated"
        cls.paths = climatology.build_climatology(
            cls.parser, "kenya", "maize", 1, [2004], _test_params(min_valid_years=1),
            cls.case_dir, n_workers=1,
        )
        cls.manifest = json.loads(
            (cls.case_dir / climatology.MANIFEST_FILE).read_text(encoding="utf-8")
        )

    def test_cube_is_clipped_to_the_last_available_day(self):
        meta = self.manifest["year_meta"]["2004"]
        # wanted end = Apr 30 + 20 grace = May 20, but CHIRPS stops on Apr 30
        self.assertEqual(meta["start_date"], "2004-03-27")
        self.assertEqual(meta["end_date"], "2004-04-30")
        self.assertEqual(meta["n_days"], TRUNCATED_N_TIME)
        self.assertEqual(meta["n_missing_chirps"], 0)
        self.assertEqual(self.manifest["data_through"], "2004-04-30")

    def test_unvalidatable_candidate_is_not_a_false_start(self):
        sos, _d, _n = self.read_band(self.paths["sos_2004"])
        sos_status, _d, _n = self.read_band(self.paths["sos_status_2004"], to_float=False)
        eos_status, _d, _n = self.read_band(self.paths["eos_status_2004"], to_float=False)
        n_false, _d, _n = self.read_band(self.paths["n_false_starts_2004"], to_float=False)
        first, _d, _n = self.read_band(self.paths["first_candidate_2004"])

        self.assertTrue(np.isnan(sos[IN_ZONE]))
        self.assertEqual(int(sos_status[IN_ZONE]), int(core.OnsetStatus.INSUFFICIENT_DATA))
        self.assertEqual(int(eos_status[IN_ZONE]), int(core.CessationStatus.NO_ONSET))
        # index 30 minus the planting index 5 = 25 days after planting
        self.assertEqual(float(first[IN_ZONE]), float(TRUNCATED_TRIGGER_INDEX - PLANTING_INDEX))
        # core.season_phenology would report 1 candidate episode here; the
        # INVALIDATED-episode meaning this package reports is 0.
        self.assertEqual(int(n_false[IN_ZONE]), 0)

    def test_summary_of_a_year_without_onset(self):
        n_valid, _d, _n = self.read_band(self.paths["onset_n_valid"], to_float=False)
        frac, _d, _n = self.read_band(self.paths["onset_frac_no_onset"])
        rate, _d, _n = self.read_band(self.paths["false_start_rate"])
        median, _d, _n = self.read_band(self.paths["onset_median"])
        censored, _d, _n = self.read_band(self.paths["eos_frac_censored"])
        self.assertEqual(int(n_valid[IN_ZONE]), 0)
        self.assertEqual(float(frac[IN_ZONE]), 1.0)
        self.assertEqual(float(rate[IN_ZONE]), 0.0)
        self.assertTrue(np.isnan(median[IN_ZONE]))
        # no year had an onset, so the censored share has no denominator
        self.assertTrue(np.isnan(censored[IN_ZONE]))


class TestPetCalibrationIsWiredIntoTheBuild(PhenologyClimatologyFixture):
    def test_the_fitted_factors_reach_calibrated_pet(self):
        """The (12, rows, cols) factor array must be handed to every year."""
        k = np.full((12,) + TILE_SHAPE, 2.0, dtype=np.float32)
        seen = {}
        real = climatology.calibrated_pet

        def _spy(etref, tmin, tmax, dates, lat, factors):
            seen["k"] = factors
            seen["n_dates"] = len(dates)
            return real(etref, tmin, tmax, dates, lat, factors)

        with mock.patch.object(climatology, "build_pet_calibration", return_value=k), \
                mock.patch.object(climatology, "calibrated_pet", side_effect=_spy):
            climatology.build_climatology(
                self.parser, "kenya", "maize", 1, [2001], _test_params(min_valid_years=1),
                self.out_dir("pet_wiring"), n_workers=1,
            )

        self.assertIsNotNone(seen.get("k"))
        self.assertEqual(seen["k"].shape, (12,) + TILE_SHAPE)
        np.testing.assert_allclose(seen["k"], 2.0)
        self.assertEqual(seen["n_dates"], N_TIME)


class TestProcessPool(PhenologyClimatologyFixture):
    def test_years_run_in_a_process_pool(self):
        params = _test_params(min_valid_years=1)
        paths = climatology.build_climatology(
            self.parser, "kenya", "maize", 1, [2001, 2003], params,
            self.out_dir("pool"), n_workers=2,
        )
        sos_2001, _d, _n = self.read_band(paths["sos_2001"])
        sos_2003, _d, _n = self.read_band(paths["sos_2003"])
        self.assertEqual(float(sos_2001[IN_ZONE]), 5.0)
        self.assertEqual(float(sos_2003[IN_ZONE]), 15.0)


if __name__ == "__main__":
    unittest.main()
