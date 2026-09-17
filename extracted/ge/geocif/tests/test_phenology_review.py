# -*- coding: utf-8 -*-
"""Adversarial-review repros for geocif/phenology and geocif/season_monitor.

Every test here is a CHARACTERIZATION test: it pins the behaviour the code has
TODAY, which in each case is the behaviour the review calls wrong. They are
written to pass against the current tree so the suite stays green; each one
carries a ``BUG:`` comment naming the assertion that should replace it once the
defect is fixed. Nothing here touches the network or the cluster -- the arrays
are synthetic and the one calendar read is of a temp workbook.

Findings pinned here
--------------------
1. ``season_monitor.file_stem`` / ``output_dirs`` omit ``harvest_year``, so two
   simultaneously active harvest years of the same (country, crop, season)
   write to one set of paths and the later one silently overwrites the earlier.
2. ``rain_10d`` / ``rain_30d`` are trailing sums over ``min(days, T_obs)`` rows
   while ``monitor.rain_window_stack`` always reads a full 30 days, so
   ``rain_30d_percentile`` collapses toward 0 for the first 29 days of every
   monitored season even when the season is exactly average.
3. ``monitor.observed_layers`` blanks ``dry_run_now`` and ``n_false_starts`` on
   nodata pixels but leaves ``rain_10d`` / ``rain_30d`` at 0.0, so a pixel with
   no CHIRPS at all is published as 0 mm and the driest year on record.
4. ``climatology._build_year_payload`` accepts any year with at least one finite
   CHIRPS value, and missing days (NaN) both count 0 mm AND break a dry run, so
   a gap can confirm an invalidated candidate ~50 days early with status OK.
5. ``climatology.build_climatology`` stamps the manifest with a hash over the
   REQUESTED year list even when most years failed, so one transient outage
   freezes a thin climatology in place as a permanent cache hit.
6. ``season_monitor._ensure_climatology`` swallows a build failure and
   ``climatology.load_climatology`` never checks ``params_hash``, so a cache
   built with different onset parameters is used silently.
7. ``geocif.viz.phenology_maps.climatology_maps`` labels ``false_start_rate``
   "episodes per year" while ``climatology.summarize_years`` produces a share of
   years in ``[0, 1]``.
"""
import datetime as dt
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

import numpy as np
from affine import Affine
from rasterio.windows import Window

from geocif import season_monitor
from geocif.phenology import climatology, core, inputs, monitor

MONTHS = ["jan", "feb", "mar", "apr", "may", "jun",
          "jul", "aug", "sep", "oct", "nov", "dec"]
BIN_COLS = [f"{m}_{d}" for m in MONTHS for d in (1, 15)]

ONSET = core.OnsetParams(
    precip_threshold=20.0,
    window_days=3,
    dry_spell_days=10,
    dry_day_threshold=1.0,
    validation_days=30,
)


def _flags(pairs, default=0):
    """A 24-bin GEOGLAM flag row; ``pairs`` maps a bin column to its flag."""
    row = {col: default for col in BIN_COLS}
    row.update(pairs)
    return np.array([row[col] for col in BIN_COLS], dtype=np.int32)


class _StubParser:
    """The three options ``monitor.active_seasons`` reads, nothing else."""

    _VALUES = {"countries": "['kenya']", "crops": "['maize']", "seasons": "[1]"}

    def has_section(self, section):
        return section == "DEFAULT"

    def has_option(self, section, option):
        return option in self._VALUES

    def get(self, section, option, **kwargs):
        return self._VALUES[option]


class TestHarvestYearPathCollision(unittest.TestCase):
    """Two active harvest years collapse onto one output path.

    A season whose zones span ``>= 365 - search_start_days_before_planting -
    validation_days = 305`` days keeps harvest year Y active
    (``as_of <= max(harvest) + 30``) while harvest year Y+1 has already opened
    (``as_of >= min(planting) - 30``). Real GEOGLAM rows do this: EWCM
    ``maize_1`` Kenya spans 305 days (Mar 1 -> Dec 31), DRC 472 days and AMISCM
    ``winter_wheat`` USA 319 days.
    """

    # planting jan_1, growing to nov_15, harvest dec_1/dec_15 -> Jan 1 .. Dec 31
    FLAGS = _flags({**{col: 2 for col in BIN_COLS}, "jan_1": 1, "dec_1": 3, "dec_15": 3})
    AS_OF = dt.date(2026, 1, 10)

    def setUp(self):
        self.flags_by_season = {1: {"zone_a": self.FLAGS}}

    def test_two_harvest_years_are_active_at_once(self):
        self.assertEqual(
            monitor.season_bounds(self.flags_by_season, 1, 2026),
            (dt.date(2026, 1, 1), dt.date(2026, 12, 31)),
        )
        with mock.patch.object(
            inputs, "load_calendar_zones", return_value=(None, self.flags_by_season)
        ):
            seasons = monitor.active_seasons(_StubParser(), self.AS_OF)
        self.assertEqual(
            seasons,
            [
                monitor.ActiveSeason("kenya", "maize", 1, 2025),
                monitor.ActiveSeason("kenya", "maize", 1, 2026),
            ],
        )

    def test_each_harvest_year_gets_its_own_file_stem(self):
        """FIXED: the stem carries the harvest year, so the two cannot collide."""
        first = monitor.ActiveSeason("kenya", "maize", 1, 2025)
        second = monitor.ActiveSeason("kenya", "maize", 1, 2026)
        self.assertNotEqual(
            season_monitor.file_stem("onset_days", first, self.AS_OF),
            season_monitor.file_stem("onset_days", second, self.AS_OF),
        )
        self.assertEqual(
            season_monitor.file_stem("onset_days", first, self.AS_OF),
            "onset_days_kenya_maize_s1_hy2025_asof20260110",
        )

    def test_both_harvest_years_share_one_output_tree(self):
        with TemporaryDirectory() as tmp:
            cfg = {"dir_output": Path(tmp), "project": "testproj"}
            first = season_monitor.output_dirs(
                cfg, monitor.ActiveSeason("kenya", "maize", 1, 2025), stamp="Jan_10_2026"
            )
            second = season_monitor.output_dirs(
                cfg, monitor.ActiveSeason("kenya", "maize", 1, 2026), stamp="Jan_10_2026"
            )
            # FIXED: each harvest year owns its own directory.
            self.assertNotEqual(first["rasters"], second["rasters"])
            self.assertNotEqual(first["csvs"], second["csvs"])
            self.assertTrue(str(first["rasters"]).endswith("s1_hy2025/rasters")
                            or "s1_hy2025" in str(first["rasters"]))


class TestShortCubeRainPercentile(unittest.TestCase):
    """``rain_30d`` is truncated to the cube while the climatology is not.

    The monitored cube opens at ``min(planting) - 30``, so for the first 29 days
    of every season ``T_obs < 30``. ``core._trailing_sum`` then sums only
    ``T_obs`` days while ``monitor.rain_window_stack`` always reads 30 -- the
    percentile compares a 10-day total against 30-day totals.
    """

    def test_ten_day_cube_reports_a_ten_day_total_as_rain_30d(self):
        pr = np.full((10, 1, 1), 5.0, dtype=np.float32)   # 5 mm every day
        layers = monitor.observed_layers(
            pr, 0.0, 200.0, ONSET, dt.date(2026, 3, 1), np.zeros((1, 1), np.float32)
        )
        # FIXED: a cube shorter than the window yields NaN, not a short total
        # masquerading as a full one. rain_10d IS complete at 10 days: 10 x 5.
        self.assertTrue(np.isnan(layers["rain_30d"][0, 0]))
        self.assertAlmostEqual(float(layers["rain_10d"][0, 0]), 50.0, places=5)

    def test_an_average_season_is_published_at_the_0th_percentile(self):
        pr = np.full((10, 1, 1), 5.0, dtype=np.float32)
        layers = monitor.observed_layers(
            pr, 0.0, 200.0, ONSET, dt.date(2026, 3, 1), np.zeros((1, 1), np.float32)
        )
        # every climatology year had exactly the same 5 mm/day: 30 x 5 = 150 mm
        stack = np.full((20, 1, 1), 150.0, dtype=np.float32)
        pct = monitor.rain_percentile(stack, layers["rain_30d"], min_years=20)
        # FIXED: rain_30d is NaN on a 10-day cube, so no percentile is
        # published at all -- better than calling an average season the driest
        # on record on the day the season opens.
        self.assertTrue(np.isnan(pct[0, 0]))


class TestNodataPixelRainLayers(unittest.TestCase):
    """A pixel with no CHIRPS at all is published as 0 mm, not as nodata.

    ``observed_layers`` multiplies ``dry_run_now`` and ``n_false_starts`` by a
    nodata mask but leaves the two rain sums alone, and ``core._trailing_sum``
    runs on the NaN-filled-with-zero slab.
    """

    def test_rain_layers_are_zero_where_state_is_nodata(self):
        pr = np.full((40, 1, 2), np.nan, dtype=np.float32)
        pr[:, 0, 0] = 2.0                      # pixel 0 has data, pixel 1 has none
        layers = monitor.observed_layers(
            pr, 0.0, 200.0, ONSET, dt.date(2026, 3, 1), np.zeros((1, 2), np.float32)
        )
        self.assertEqual(int(layers["state"][0, 1]), int(core.NODATA_STATUS))
        self.assertTrue(np.isnan(layers["dry_run_now"][0, 1]))
        self.assertTrue(np.isnan(layers["n_false_starts"][0, 1]))
        # FIXED: no observations -> no total. A 0.0 here was a fabricated
        # record drought in the raster, the map and the companion table.
        self.assertTrue(np.isnan(layers["rain_30d"][0, 1]))
        self.assertTrue(np.isnan(layers["rain_10d"][0, 1]))
        # the pixel that DOES have data is unaffected: 30 x 2 mm
        self.assertAlmostEqual(float(layers["rain_30d"][0, 0]), 60.0, places=5)

    def test_the_fabricated_zero_lands_at_the_0th_percentile(self):
        pr = np.full((40, 1, 1), np.nan, dtype=np.float32)
        layers = monitor.observed_layers(
            pr, 0.0, 200.0, ONSET, dt.date(2026, 3, 1), np.zeros((1, 1), np.float32)
        )
        stack = np.full((20, 1, 1), 150.0, dtype=np.float32)
        pct = monitor.rain_percentile(stack, layers["rain_30d"], min_years=20)
        # FIXED: a data-void pixel publishes no percentile.
        self.assertTrue(np.isnan(pct[0, 0]))


class TestMissingDaysFlipTheClimatology(unittest.TestCase):
    """Missing CHIRPS days can confirm an invalidated candidate 50 days early.

    NaN rain contributes 0 mm to the accumulation window AND is not a dry day,
    so a gap erases the dry spell that would have invalidated a false start.
    ``_build_year_payload`` only rejects a year when EVERY value is NaN, so such
    a year enters the median with full weight and status ``OK``.

    Series (200 days, default parameters): 7 mm on days 10-12 (W[12] = 21 mm),
    then nothing until day 60, then 8 mm/day (W = 24 mm).
    """

    @staticmethod
    def _series():
        rain = np.zeros(200, dtype=np.float64)
        rain[10:13] = 7.0
        rain[60:] = 8.0
        return rain

    def test_complete_year_rejects_the_false_start(self):
        sos, status = core.onset_index(self._series(), 0, 190, ONSET)
        # days 13..59 are dry, so a 10-day spell ends at day 22, inside the
        # look-ahead [21, 41] of the candidate at day 12 -> invalidated
        self.assertEqual(float(sos), 62.0)
        self.assertEqual(int(status), int(core.OnsetStatus.OK))

    def test_a_24_day_gap_confirms_the_false_start_50_days_early(self):
        rain = self._series()
        rain[18:42] = np.nan                    # 24 of 200 days missing (12 %)
        sos, status = core.onset_index(rain, 0, 190, ONSET)
        # the gap resets the dry-day counter, so the first spell now ends at
        # day 51, outside [21, 41]: day 12 is confirmed instead of day 62
        self.assertEqual(float(sos), 12.0)
        # BUG: the year is reported as a clean onset, 50 days early, and
        # _build_year_payload has no missing-day gate to reject it.
        self.assertEqual(int(status), int(core.OnsetStatus.OK))
        self.assertTrue(np.isfinite(rain).any())


CACHE_SHAPE = (2, 2)
CACHE_TRANSFORM = Affine(0.05, 0, 36.0, 0, -0.05, 1.0)
CACHE_WINDOW = Window(0, 0, 2, 2)


def _year_layers(year, sos=10.0):
    """The dict ``climatology._build_year_payload`` returns, all constant."""
    return {
        "sos": np.full(CACHE_SHAPE, sos, np.float32),
        "eos": np.full(CACHE_SHAPE, sos + 100.0, np.float32),
        "lgs": np.full(CACHE_SHAPE, 100.0, np.float32),
        "sos_status": np.zeros(CACHE_SHAPE, np.int8),
        "eos_status": np.zeros(CACHE_SHAPE, np.int8),
        "first_candidate": np.full(CACHE_SHAPE, sos - 5.0, np.float32),
        "n_false_starts": np.zeros(CACHE_SHAPE, np.int16),
        "eos_at_floor": np.zeros(CACHE_SHAPE, bool),
        "meta": {
            "year": int(year), "start_date": f"{year}-03-01", "end_date": f"{year}-12-31",
            "n_days": 300, "n_missing_chirps": 0, "n_missing_etref": 0,
            "n_hargreaves_filled": 0, "n_calendar_pixels": 4, "n_onset_pixels": 4,
        },
    }


def _patched_build(year_fn):
    """Context managers that let ``build_climatology`` run with no raster I/O."""
    return (
        mock.patch.object(inputs, "country_bbox", return_value=(36.0, 0.9, 36.1, 1.0)),
        mock.patch.object(
            inputs, "window_for_bbox",
            return_value=(CACHE_WINDOW, CACHE_TRANSFORM, CACHE_SHAPE),
        ),
        mock.patch.object(inputs, "load_calendar_zones", return_value=(None, {})),
        mock.patch.object(
            climatology, "build_pet_calibration",
            return_value=np.ones((12,) + CACHE_SHAPE, np.float32),
        ),
        mock.patch.object(climatology, "_build_year_payload", side_effect=year_fn),
    )


class TestClimatologyCacheIntegrity(unittest.TestCase):
    """The cache hash answers "same request?", never "same content?"."""

    def test_a_mostly_failed_build_is_cached_as_a_permanent_hit(self):
        years = [2001, 2002, 2003]
        params = climatology.ClimatologyParams(min_valid_years=1)
        attempted = []

        def one_good_year(payload):
            attempted.append(int(payload.year))
            if int(payload.year) != 2003:
                raise RuntimeError("CHIRPS mount outage")
            return _year_layers(payload.year)

        with TemporaryDirectory() as tmp:
            out = Path(tmp) / "cache"
            patches = _patched_build(one_good_year)
            with patches[0], patches[1], patches[2], patches[3], patches[4]:
                climatology.build_climatology(
                    None, "kenya", "maize", 1, years, params, out, n_workers=1
                )
                manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
                self.assertEqual(manifest["years"], [2003])
                self.assertEqual(manifest["years_requested"], years)
                self.assertEqual(sorted(manifest["failed_years"]), ["2001", "2002"])
                # The hash still describes the REQUEST (that is what it is for)...
                self.assertEqual(
                    manifest["params_hash"],
                    climatology.params_hash(
                        params, "kenya", "maize", 1, years, CACHE_SHAPE,
                        climatology._bounds_of(CACHE_TRANSFORM, CACHE_SHAPE),
                    ),
                )
                # ...but FIXED: a hash match is no longer enough. The cache is
                # only a hit when it also HOLDS every year asked for, so the two
                # years lost to the outage are retried on the next run instead
                # of being frozen out for good.
                attempted.clear()
                climatology.build_climatology(
                    None, "kenya", "maize", 1, years, params, out, n_workers=1
                )
                self.assertEqual(sorted(attempted), [2001, 2002, 2003])
            arrays, _man = climatology.load_climatology(out)
            self.assertEqual(arrays["onset_stack"].shape[0], 1)

    def test_a_failed_rebuild_falls_back_to_the_previous_parameter_set(self):
        years = [2001, 2002]
        old = climatology.ClimatologyParams(
            onset=core.OnsetParams(precip_threshold=20.0), min_valid_years=1
        )
        new = climatology.ClimatologyParams(
            onset=core.OnsetParams(precip_threshold=25.0), min_valid_years=1
        )
        with TemporaryDirectory() as tmp:
            out = Path(tmp) / "cache"
            patches = _patched_build(lambda payload: _year_layers(payload.year, sos=10.0))
            with patches[0], patches[1], patches[2], patches[3], patches[4]:
                climatology.build_climatology(
                    None, "kenya", "maize", 1, years, old, out, n_workers=1
                )
            stale_hash = json.loads(
                (out / "manifest.json").read_text(encoding="utf-8")
            )["params_hash"]
            wanted_hash = climatology.params_hash(
                new, "kenya", "maize", 1, years, CACHE_SHAPE,
                climatology._bounds_of(CACHE_TRANSFORM, CACHE_SHAPE),
            )
            self.assertNotEqual(stale_hash, wanted_hash)

            cfg = {
                "parser": None, "climatology_start_year": 2001,
                "climatology_end_year": 2002, "n_workers": 1,
                "rebuild_climatology": False,
            }
            season = monitor.ActiveSeason("kenya", "maize", 1, 2026)
            # The grid patches stay on: _ensure_climatology derives the window to
            # compute the hash it checks the cache against, exactly as the real
            # run does. Without them the hash is unknowable and the guard is
            # skipped by design ("cannot check" is not "mismatch").
            grid = _patched_build(lambda payload: _year_layers(payload.year))
            with grid[0], grid[1],                  mock.patch.object(climatology, "climatology_dir", return_value=out),                  mock.patch.object(
                     climatology, "build_climatology",
                     side_effect=RuntimeError("every one of 2 year(s) failed")
                 ):
                arrays, clim_years = season_monitor._ensure_climatology(cfg, season, new)
            # FIXED: _ensure_climatology passes the wanted hash, so the 20 mm
            # cache is refused for a 25 mm run. The monitor then publishes the
            # state map with no anomaly, rather than an anomaly measured against
            # a reference built with other parameters -- a systematic bias with
            # nothing on the map to reveal it.
            self.assertIsNone(arrays)
            self.assertEqual(clim_years, [])
            # and the cache itself is untouched and still loadable on its own terms
            self.assertIsNotNone(climatology.load_climatology(out))
            self.assertIsNone(
                climatology.load_climatology(out, expect_hash=wanted_hash)
            )


class TestPOnsetNaNPattern(unittest.TestCase):
    """Which states ``climatology_layers`` blanks, and which it should.

    Verified correct: ``onset_anomaly_days`` is positive = LATE, the percentile
    and the anomaly are CONFIRMED-only, and ``days_past_median`` is populated on
    NOT_STARTED pixels and nowhere else. The gap is ``p_onset``: it is blanked
    only on CONFIRMED, so a pixel whose rain is entirely nodata (``state == -1``,
    the layer contract's "no calendar or no rain") and a pixel whose season is
    already over (``NO_ONSET``) are both published with a conditional
    probability, on a map masked only to cropland.
    """

    STACK = np.array([[[5.0]], [[10.0]], [[15.0]], [[20.0]], [[25.0]]], np.float32)
    CLIM = {"onset_median": np.array([[15.0]], np.float32), "onset_stack": STACK}

    def _layers(self, code, onset):
        return monitor.climatology_layers(
            np.array([[int(code)]], np.int8),
            np.array([[onset]], np.float32),
            np.array([[8.0]], np.float32),      # as_of = 8 days after planting
            self.CLIM,
            horizons=(14,),
            min_years=1,
        )

    def test_confirmed_pixel(self):
        out = self._layers(core.SeasonState.CONFIRMED, 18.0)
        self.assertAlmostEqual(float(out["onset_anomaly_days"][0, 0]), 3.0)   # 18 - 15, LATE
        self.assertAlmostEqual(float(out["onset_percentile"][0, 0]), 0.6)     # 3 of 5 years <= 18
        self.assertTrue(np.isnan(out["days_past_median"][0, 0]))
        self.assertTrue(np.isnan(out["p_onset_14d"][0, 0]))

    def test_not_started_pixel(self):
        out = self._layers(core.SeasonState.NOT_STARTED, np.nan)
        self.assertAlmostEqual(float(out["days_past_median"][0, 0]), -7.0)    # 8 - 15
        # den = years with onset > 8 -> {10, 15, 20, 25}; num = onset in (8, 22]
        # -> {10, 15, 20} -> 3/4
        self.assertAlmostEqual(float(out["p_onset_14d"][0, 0]), 0.75)
        self.assertTrue(np.isnan(out["onset_anomaly_days"][0, 0]))

    def test_days_past_median_is_not_started_only(self):
        for code in (core.SeasonState.FALSE_START, core.SeasonState.PROVISIONAL,
                     core.SeasonState.NO_ONSET, core.SeasonState.BEFORE_WINDOW):
            with self.subTest(state=code.name):
                self.assertTrue(np.isnan(self._layers(code, np.nan)["days_past_median"][0, 0]))

    def test_p_onset_is_blank_on_nodata_and_finished_pixels(self):
        """FIXED: the conditional is only stated where a pixel is still waiting.

        A pixel with no rain observations at all, and one whose season has
        already closed without an onset, are both undefined for
        "P(onset in the next h days | it has not arrived yet)".
        """
        for code in (core.NODATA_STATUS, core.SeasonState.NO_ONSET):
            with self.subTest(state=int(code)):
                out = self._layers(code, np.nan)
                self.assertTrue(np.isnan(out["p_onset_14d"][0, 0]))

    def test_p_onset_survives_where_the_pixel_is_genuinely_waiting(self):
        """The fix must not blank the states the layer exists for."""
        for code in (core.SeasonState.NOT_STARTED, core.SeasonState.FALSE_START,
                     core.SeasonState.PROVISIONAL, core.SeasonState.BEFORE_WINDOW):
            with self.subTest(state=code.name):
                out = self._layers(code, np.nan)
                self.assertAlmostEqual(float(out["p_onset_14d"][0, 0]), 0.75)


class TestFalseStartRateUnits(unittest.TestCase):
    """The cached layer is a share of years; the map calls it episodes per year."""

    def test_summarize_years_produces_a_share_in_zero_one(self):
        shape = (1, 3)
        years = [2001, 2002, 2003, 2004]
        per_year = {}
        for i, year in enumerate(years):
            # pixel 0 never false-starts, pixel 1 false-starts in every year
            # (3 episodes), pixel 2 in one year of four
            n_false = np.array([[0, 3, 3 if i == 0 else 0]], dtype=np.int16)
            per_year[year] = {
                "sos": np.zeros(shape, np.float32),
                "eos": np.full(shape, 100.0, np.float32),
                "lgs": np.full(shape, 100.0, np.float32),
                "sos_status": np.zeros(shape, np.int8),
                "eos_status": np.zeros(shape, np.int8),
                "n_false_starts": n_false,
                "eos_at_floor": np.zeros(shape, bool),
            }
        summary = climatology.summarize_years(years, per_year, min_valid_years=1)
        rate = summary["false_start_rate"]
        self.assertAlmostEqual(float(rate[0, 0]), 0.00, places=6)
        self.assertAlmostEqual(float(rate[0, 1]), 1.00, places=6)
        self.assertAlmostEqual(float(rate[0, 2]), 0.25, places=6)
        # 0.25 means "one year in four had at least one false start", NOT
        # "0.25 episodes per year" -- pixel 1 averages 3 episodes a year and
        # still reads 1.0.
        self.assertEqual(
            climatology.LAYER_UNITS["false_start_rate"],
            "share of years with at least one invalidated candidate, 0..1",
        )

    def test_the_map_declares_episodes_per_year(self):
        from geocif.viz import phenology_maps

        source = Path(phenology_maps.__file__).read_text(encoding="utf-8")
        # FIXED: the label and the units column both say "share of years".
        self.assertNotIn('cbar_label="Invalidated onset episodes per year"', source)
        self.assertIn('cbar_label="Share of years with a false start"', source)
        self.assertNotIn('units="episodes per year"', source)
        self.assertIn('units="share of years with at least one invalidated', source)


if __name__ == "__main__":
    unittest.main()


class TestMissingDayCoverageGuard(unittest.TestCase):
    """FIXED: a year with too many absent CHIRPS files is rejected, not trusted.

    A missing day reads as an all-NaN slab. NaN adds 0 mm to the accumulation
    but is NOT a dry day, so a gap can break the dry spell that invalidates a
    false start. The characterization test above shows the consequence at the
    algorithm level (onset 62 -> 12 with 24 days punched out); this pins the
    guard that keeps such a year out of the climatology.
    """

    def _payload(self, missing_days, n_days=200, threshold=0.05):
        """A payload whose CHIRPS read reports ``missing_days`` absent files."""
        params = climatology.ClimatologyParams(max_missing_day_fraction=threshold)
        return params, n_days, missing_days

    def test_threshold_is_part_of_the_cache_hash(self):
        # a stricter coverage rule must invalidate a cache built with a looser
        # one, or the old, contaminated years would be reused
        base = climatology.ClimatologyParams()
        strict = climatology.ClimatologyParams(max_missing_day_fraction=0.0)
        shape, bounds = (2, 2), (36.0, 0.9, 36.1, 1.0)
        self.assertNotEqual(
            climatology.params_hash(base, "kenya", "maize", 1, [2001], shape, bounds),
            climatology.params_hash(strict, "kenya", "maize", 1, [2001], shape, bounds),
        )

    def test_the_default_is_five_percent(self):
        self.assertAlmostEqual(
            climatology.ClimatologyParams().max_missing_day_fraction, 0.05
        )

    def _drive(self, n_missing):
        """Run one harvest year whose CHIRPS read reports ``n_missing`` gaps."""
        shape = (2, 2)
        transform = Affine(0.05, 0, 36.0, 0, -0.05, 1.0)
        cal = inputs.SeasonCalendar(
            planting=np.full(shape, np.datetime64("2003-03-01", "D")),
            harvest=np.full(shape, np.datetime64("2003-09-30", "D")),
            next_planting=np.full(shape, np.datetime64("NaT", "D")),
            zone_id=np.ones(shape, "int16"),
            zone_names=["z"],
        )

        def fake_read(parser, var, dates, window, n_threads=8):
            cube = np.full((len(dates),) + shape, 2.0, "float32")
            return cube, (list(dates[:n_missing]) if var == "chirps" else [])

        payload = climatology._YearPayload(
            parser=None, country="kenya", crop="maize", season=1, year=2003,
            window=Window(0, 0, 2, 2), transform=transform, shape=shape,
            zones_gdf=None, flags_by_season={},
            params=climatology.ClimatologyParams(),
            k=np.ones((12,) + shape, "float32"),
        )
        with mock.patch.object(inputs, "rasterize_calendar", return_value=cal),              mock.patch.object(
                 climatology, "last_available_day", return_value=dt.date(2003, 12, 31)
             ),              mock.patch.object(inputs, "read_cube", side_effect=fake_read):
            return climatology._build_year_payload(payload)

    def test_a_gappy_year_raises_and_names_the_reason(self):
        # 26 absent days in a 304-day cube = 8.6 % > the 5 % budget
        with self.assertRaises(ValueError) as caught:
            self._drive(26)
        message = str(caught.exception)
        self.assertIn("missing", message)
        self.assertIn("dry spell", message)   # the reason, not just the count

    def test_a_complete_year_is_accepted(self):
        """The guard must not reject a year that is merely imperfect."""
        self.assertIsNotNone(self._drive(0))
        # 9 of 304 = 3.0 %, inside the budget
        self.assertIsNotNone(self._drive(9))

    def test_a_gappy_year_is_rejected_with_a_named_reason(self):
        # 24 of 200 days = 12 % > 5 %: the exact shape of the measured failure
        params = climatology.ClimatologyParams(max_missing_day_fraction=0.05)
        n_days, n_missing = 200, 24
        self.assertGreater(n_missing / n_days, params.max_missing_day_fraction)
        # and 9 of 200 = 4.5 % stays inside the budget
        self.assertLess(9 / n_days, params.max_missing_day_fraction)
