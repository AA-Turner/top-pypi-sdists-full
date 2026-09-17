# -*- coding: utf-8 -*-
"""Tests for geocif/phenology/monitor.py (DESIGN.md section 8).

Everything here is a hand-built array: a synthetic rain cube of six pixels that
between them exercise every :class:`~geocif.phenology.core.SeasonState`, a
synthetic onset climatology stack, and a synthetic zonal grid for the two table
builders. No file is read, so the arithmetic below is the whole contract.

The observed cube (``TestObservedLayers``)
-----------------------------------------
30 days from 2026-03-01 (index 0), onset parameters ``precip_threshold = 20``,
``window_days = 3``, ``dry_spell_days = 5``, ``dry_day_threshold = 1``,
``validation_days = 10``. ``planting_offset = 5`` everywhere, i.e. planting is
2026-03-06 and ``onset_days = onset_idx - 5``.

Pixel 0 CONFIRMED: 25 mm on index 8, then 5 mm/day on indices 9..24.
    W[8] = P[6] + P[7] + P[8] = 0 + 0 + 25 = 25 >= 20      -> trigger
    8 >= window_days - 1 = 2 and 8 + 10 = 18 <= 30          -> look-ahead observed
    days 9..24 are all wet, so no dry run reaches 5 inside [12, 17]
                                                            -> CONFIRMED at 8
    onset_days = 8 - 5 = 3, onset_date = 2026-03-01 + 8 = 2026-03-09
    rain_10d = indices 20..29 = 5 x 5 + 0 x 5 = 25 mm
    rain_30d = 25 + 5 x 16 = 105 mm
    dry_run_now = indices 25..29 dry = 5

Pixel 1 FALSE_START: 25 mm on index 4 and nothing else.
    triggers on 4, 5, 6 (the 3-day window still holds the 25 mm) = ONE episode
    dry from index 5 on, so r[9] = 5 = dry_spell_days -> a spell ENDS at 9,
    which is inside the look-ahead [8, 13] of the candidate at 4
                                                            -> invalidated
    n_false_starts = 1 (invalidated EPISODES, the core.onset_state meaning)
    dry_run_now = indices 5..29 = 25, rain_30d = 25 mm, rain_10d = 0 mm

Pixel 2 PROVISIONAL: 25 mm on index 25, 5 mm/day on 26..29.
    triggers on 25, 26, 27; 25 + 10 = 35 > 30, so none can be confirmed and no
    spell has ended inside their windows -> the latest trigger is pending
    days_to_confirm is not reported here (it is a core.onset_state key)
    rain_10d = rain_30d = 25 + 5 x 4 = 45 mm, dry_run_now = 0

Pixel 3 NOT_STARTED: no rain at all, search_start = 0 <= 29.
    dry_run_now = 30, rain_10d = rain_30d = 0 mm

Pixel 4 BEFORE_WINDOW: no rain and search_start = 40 > 29.

Pixel 5 nodata: rain all NaN -> state -1, counts NaN.

The climatology stack (``TestClimatologyLayers``)
-------------------------------------------------
Five years, three pixels, values in days since planting start:

    pixel 0 and 1: [0, 5, 10, 15, 20] -> median 10
    pixel 2:       all NaN            -> median NaN

    pixel 0 CONFIRMED at onset_days 15 -> anomaly = 15 - 10 = +5 (LATE)
                                       -> percentile = #(years <= 15)/5 = 4/5
                                       -> p_onset NaN (onset already happened)
                                       -> days_past_median NaN (not NOT_STARTED)
    pixel 1 NOT_STARTED at as_of_days 2
        days_past_median = 2 - 10 = -8
        p_14d: den = #(onset > 2 or NaN) = #{5,10,15,20} = 4,
               num = #(2 < onset <= 16)  = #{5,10,15}    = 3 -> 3/4 = 0.75
        p_28d: num = #(2 < onset <= 30)  = #{5,10,15,20} = 4 -> 4/4 = 1.00
    pixel 2 NOT_STARTED, no valid year
        den = #(onset > 2 or NaN) = 5 -> p = 0/5 = 0.0, percentile NaN
"""
import datetime as dt
import unittest

import numpy as np
import pandas as pd

from geocif.phenology import core, monitor

ONSET_PARAMS = core.OnsetParams(
    precip_threshold=20.0,
    window_days=3,
    dry_spell_days=5,
    dry_day_threshold=1.0,
    validation_days=10,
)

N_TIME = 30
START_DATE = dt.date(2026, 3, 1)
PLANTING_OFFSET = 5.0

MONTHS = ["jan", "feb", "mar", "apr", "may", "jun",
          "jul", "aug", "sep", "oct", "nov", "dec"]
BIN_COLS = [f"{m}_{d}" for m in MONTHS for d in (1, 15)]


def _flags(pairs, default=0):
    """24-bin flag row as an int array, ``pairs`` maps a bin column to its flag."""
    row = {col: default for col in BIN_COLS}
    row.update(pairs)
    return np.array([row[col] for col in BIN_COLS], dtype=np.int32)


def _build_cube():
    """The six-pixel rain cube of the module docstring, shape (30, 1, 6)."""
    pr = np.zeros((N_TIME, 1, 6), dtype=np.float32)
    # pixel 0: confirmed
    pr[8, 0, 0] = 25.0
    pr[9:25, 0, 0] = 5.0
    # pixel 1: one invalidated episode
    pr[4, 0, 1] = 25.0
    # pixel 2: provisional, trigger too late to validate
    pr[25, 0, 2] = 25.0
    pr[26:30, 0, 2] = 5.0
    # pixels 3 and 4 stay dry; pixel 5 is nodata
    pr[:, 0, 5] = np.nan
    return pr


class TestObservedLayers(unittest.TestCase):
    """The state machine plus monitor.py's index -> date / days shifts."""

    def setUp(self):
        self.pr = _build_cube()
        self.search_start = np.array([[0.0, 0.0, 0.0, 0.0, 40.0, 0.0]], dtype=np.float32)
        self.season_end = np.array([[29.0, 29.0, 29.0, 29.0, 50.0, 29.0]], dtype=np.float32)
        self.offset = np.full((1, 6), PLANTING_OFFSET, dtype=np.float32)
        self.layers = monitor.observed_layers(
            self.pr,
            self.search_start,
            self.season_end,
            ONSET_PARAMS,
            START_DATE,
            self.offset,
        )

    def px(self, name, index):
        return self.layers[name][0, index]

    def test_states_cover_every_case(self):
        expected = [
            core.SeasonState.CONFIRMED,
            core.SeasonState.FALSE_START,
            core.SeasonState.PROVISIONAL,
            core.SeasonState.NOT_STARTED,
            core.SeasonState.BEFORE_WINDOW,
            core.NODATA_STATUS,
        ]
        self.assertEqual(
            [int(self.px("state", i)) for i in range(6)], [int(e) for e in expected]
        )

    def test_onset_index_days_and_date(self):
        # trigger on index 8; onset_days = 8 - planting_offset(5) = 3
        self.assertEqual(self.px("onset_idx", 0), 8.0)
        self.assertEqual(self.px("onset_days", 0), 3.0)
        # 2026-03-01 + 8 days = 2026-03-09, carried as days since 1970-01-01
        self.assertEqual(
            monitor.EPOCH + int(self.px("onset_date", 0)),
            np.datetime64("2026-03-09", "D"),
        )
        for i in (1, 2, 3, 4, 5):
            self.assertTrue(np.isnan(self.px("onset_idx", i)))
            self.assertTrue(np.isnan(self.px("onset_days", i)))
            self.assertTrue(np.isnan(self.px("onset_date", i)))

    def test_false_starts_count_invalidated_episodes_only(self):
        # pixel 1: one episode (indices 4, 5, 6), invalidated by the spell ending
        # at index 9. Pixel 0's confirmed episode is NOT a false start.
        self.assertEqual(self.px("n_false_starts", 1), 1.0)
        self.assertEqual(self.px("n_false_starts", 0), 0.0)
        self.assertEqual(self.px("n_false_starts", 2), 0.0)

    def test_trailing_rain_and_dry_run(self):
        # pixel 0: last 10 days = indices 20..24 at 5 mm + 25..29 at 0 mm = 25 mm
        self.assertAlmostEqual(float(self.px("rain_10d", 0)), 25.0, places=4)
        # 25 mm + 16 days x 5 mm = 105 mm over the whole 30-day cube
        self.assertAlmostEqual(float(self.px("rain_30d", 0)), 105.0, places=4)
        # dry from index 25 to 29 inclusive = 5 days
        self.assertEqual(self.px("dry_run_now", 0), 5.0)
        # pixel 3 never rained: 30 consecutive dry days
        self.assertEqual(self.px("dry_run_now", 3), 30.0)
        self.assertAlmostEqual(float(self.px("rain_30d", 1)), 25.0, places=4)
        self.assertAlmostEqual(float(self.px("rain_10d", 1)), 0.0, places=4)
        # pixel 2: 25 + 4 x 5 = 45 mm in both windows, and it is raining now
        self.assertAlmostEqual(float(self.px("rain_30d", 2)), 45.0, places=4)
        self.assertEqual(self.px("dry_run_now", 2), 0.0)

    def test_nodata_pixel_has_no_counts(self):
        self.assertTrue(np.isnan(self.px("dry_run_now", 5)))
        self.assertTrue(np.isnan(self.px("n_false_starts", 5)))

    def test_as_of_days_is_relative_to_planting(self):
        # last observed index 29, planting at index 5 -> 24 days into the season
        self.assertEqual(self.layers["as_of_days"][0, 0], 24.0)

    def test_forecast_trigger_is_days_from_the_as_of_day(self):
        # 8 forecast days for pixel 3 (dry so far). Forecast day i is cube
        # index T_obs + i = 30 + i, so 25 mm at fcst[2] triggers at index 32 and
        # the answer is 32 - 29 = 3 days from the as-of day.
        fcst = np.zeros((8, 1, 6), dtype=np.float32)
        fcst[2, 0, 3] = 25.0
        layers = monitor.observed_layers(
            self.pr,
            self.search_start,
            np.full((1, 6), 60.0, dtype=np.float32),
            ONSET_PARAMS,
            START_DATE,
            self.offset,
            pr_fcst=fcst,
        )
        self.assertEqual(layers["fcst_trigger_days"][0, 3], 3.0)
        self.assertTrue(np.isnan(layers["fcst_trigger_days"][0, 4]))

    def test_every_advertised_layer_is_present(self):
        for name in ("state", "onset_idx", "onset_date", "onset_days", "rain_10d",
                     "rain_30d", "dry_run_now", "n_false_starts", "fcst_trigger_days"):
            self.assertIn(name, self.layers)

    def test_empty_cube_is_rejected(self):
        with self.assertRaises(ValueError):
            monitor.observed_layers(
                np.zeros((0, 1, 6), dtype=np.float32),
                self.search_start,
                self.season_end,
                ONSET_PARAMS,
                START_DATE,
                self.offset,
            )


class TestClimatologyLayers(unittest.TestCase):
    """Anomaly sign, the NOT_STARTED gate and the conditional probabilities."""

    def setUp(self):
        stack = np.full((5, 1, 3), np.nan, dtype=np.float32)
        stack[:, 0, 0] = [0.0, 5.0, 10.0, 15.0, 20.0]
        stack[:, 0, 1] = [0.0, 5.0, 10.0, 15.0, 20.0]
        self.stack = stack
        self.clim = {
            "onset_median": np.array([[10.0, 10.0, np.nan]], dtype=np.float32),
            "onset_stack": stack,
            "false_start_rate": np.array([[0.2, 0.4, 0.6]], dtype=np.float32),
        }
        self.state = np.array(
            [[int(core.SeasonState.CONFIRMED),
              int(core.SeasonState.NOT_STARTED),
              int(core.SeasonState.NOT_STARTED)]],
            dtype=np.int8,
        )
        self.onset_days = np.array([[15.0, np.nan, np.nan]], dtype=np.float32)
        self.as_of_days = np.array([[30.0, 2.0, 2.0]], dtype=np.float32)
        self.out = monitor.climatology_layers(
            self.state, self.onset_days, self.as_of_days, self.clim, min_years=3
        )

    def test_positive_anomaly_means_late(self):
        # onset 15 days after planting vs a median of 10 -> five days LATE
        self.assertAlmostEqual(float(self.out["onset_anomaly_days"][0, 0]), 5.0, places=5)
        self.assertTrue(np.isnan(self.out["onset_anomaly_days"][0, 1]))

    def test_days_past_median_only_for_not_started(self):
        self.assertTrue(np.isnan(self.out["days_past_median"][0, 0]))
        # 2 days into the season vs a median onset on day 10 -> -8
        self.assertAlmostEqual(float(self.out["days_past_median"][0, 1]), -8.0, places=5)
        # no median at all at pixel 2
        self.assertTrue(np.isnan(self.out["days_past_median"][0, 2]))

    def test_onset_percentile(self):
        # 4 of the 5 years onset on or before day 15
        self.assertAlmostEqual(float(self.out["onset_percentile"][0, 0]), 0.8, places=5)
        self.assertTrue(np.isnan(self.out["onset_percentile"][0, 1]))  # no onset yet
        self.assertTrue(np.isnan(self.out["onset_percentile"][0, 2]))  # no valid year

    def test_p_onset_values_and_range(self):
        # 3 of the 4 years that onset after day 2 did so within 14 days
        self.assertAlmostEqual(float(self.out["p_onset_14d"][0, 1]), 0.75, places=5)
        self.assertAlmostEqual(float(self.out["p_onset_28d"][0, 1]), 1.0, places=5)
        # onset already confirmed: the conditional says nothing about this pixel
        self.assertTrue(np.isnan(self.out["p_onset_14d"][0, 0]))
        # every year of pixel 2 is a no-onset year -> 0 of 5
        self.assertAlmostEqual(float(self.out["p_onset_14d"][0, 2]), 0.0, places=5)
        for key in ("p_onset_14d", "p_onset_28d"):
            values = self.out[key][np.isfinite(self.out[key])]
            self.assertTrue(np.all((values >= 0.0) & (values <= 1.0)))

    def test_false_start_rate_is_passed_through(self):
        np.testing.assert_allclose(
            self.out["false_start_rate"], self.clim["false_start_rate"]
        )

    def test_p_onset_is_nan_when_the_cache_has_too_few_years(self):
        # two years in the cache, min_years = 3 -> the denominator can never
        # reach the floor, so no probability is published anywhere.
        clim = dict(self.clim)
        clim["onset_stack"] = self.stack[:2]
        out = monitor.climatology_layers(
            self.state, self.onset_days, self.as_of_days, clim, min_years=3
        )
        self.assertTrue(np.all(np.isnan(out["p_onset_14d"])))
        self.assertTrue(np.all(np.isnan(out["p_onset_28d"])))

    def test_no_climatology_gives_all_nan_layers(self):
        out = monitor.climatology_layers(
            self.state, self.onset_days, self.as_of_days, None, min_years=3
        )
        for key in ("onset_anomaly_days", "onset_percentile", "days_past_median",
                    "p_onset_14d", "p_onset_28d", "false_start_rate"):
            self.assertTrue(np.all(np.isnan(out[key])), key)

    def test_grid_mismatch_is_dropped_not_broadcast(self):
        clim = dict(self.clim)
        clim["onset_median"] = np.full((1, 7), 10.0, dtype=np.float32)
        out = monitor.climatology_layers(
            self.state, self.onset_days, self.as_of_days, clim, min_years=3
        )
        self.assertEqual(out["onset_anomaly_days"].shape, (1, 3))
        self.assertTrue(np.all(np.isnan(out["onset_anomaly_days"])))


class TestRainPercentile(unittest.TestCase):
    def test_share_of_years_at_or_below_times_100(self):
        stack = np.array([[[10.0]], [[20.0]], [[30.0]], [[40.0]]], dtype=np.float32)
        current = np.array([[25.0]], dtype=np.float32)
        # 2 of 4 years were at or below 25 mm -> 50th percentile
        out = monitor.rain_percentile(stack, current, min_years=1)
        self.assertAlmostEqual(float(out[0, 0]), 50.0, places=5)

    def test_empty_stack_is_nan(self):
        out = monitor.rain_percentile(
            np.zeros((0, 1, 1), dtype=np.float32), np.array([[5.0]], dtype=np.float32)
        )
        self.assertTrue(np.all(np.isnan(out)))


class TestSeasonBounds(unittest.TestCase):
    """Zone-level planting/harvest extremes, including the cross-year case."""

    def test_within_year_season(self):
        flags_by_season = {
            1: {
                "zone_a": _flags({"apr_1": 1, "apr_15": 2, "may_1": 3}),
                "zone_b": _flags({"may_1": 1, "may_15": 2, "jun_1": 3}),
            }
        }
        planting, harvest = monitor.season_bounds(flags_by_season, 1, 2026)
        # earliest planting = Apr 1 (zone a), latest harvest = Jun 14 (zone b,
        # the jun_1 bin covers days 1-14)
        self.assertEqual(planting, dt.date(2026, 4, 1))
        self.assertEqual(harvest, dt.date(2026, 6, 14))

    def test_cross_year_season_is_planted_the_year_before(self):
        flags_by_season = {
            # the block must be CONTIGUOUS across the year boundary: every bin
            # from oct_15 to feb_1 carries a flag, so the jan/feb head merges
            # with the oct-dec tail into one wrapped block.
            2: {"zone_a": _flags({"oct_15": 1, "nov_1": 1, "nov_15": 1,
                                  "dec_1": 1, "dec_15": 1, "jan_1": 2,
                                  "jan_15": 2, "feb_1": 3})}
        }
        planting, harvest = monitor.season_bounds(flags_by_season, 2, 2026)
        self.assertEqual(planting, dt.date(2025, 10, 15))
        self.assertEqual(harvest, dt.date(2026, 2, 14))

    def test_crop_not_grown_sentinel_gives_none(self):
        flags_by_season = {1: {"zone_a": _flags({}, default=-1)}}
        self.assertIsNone(monitor.season_bounds(flags_by_season, 1, 2026))


class TestShiftYear(unittest.TestCase):
    def test_leap_day_falls_back_to_the_28th(self):
        self.assertEqual(monitor._shift_year(dt.date(2024, 2, 29), -1), dt.date(2023, 2, 28))
        self.assertEqual(monitor._shift_year(dt.date(2026, 11, 3), -5), dt.date(2021, 11, 3))


class TestTables(unittest.TestCase):
    """The two published tables, on a hand-built 2x2 result.

    weight (crop km^2)  = [[1, 1], [2, 2]]
    admin id_grid       = [[1, 1], [2, 2]]     zone id_grid = [[1, 2], [1, 2]]
    state               = [[CONFIRMED, CONFIRMED], [NOT_STARTED, NOT_STARTED]]
    onset_anomaly_days  = [[2, 4], [nan, nan]]
    days_past_median    = [[nan, nan], [10, 20]]
    """

    def setUp(self):
        nan = np.nan
        layers = {
            "state": np.array(
                [[int(core.SeasonState.CONFIRMED), int(core.SeasonState.CONFIRMED)],
                 [int(core.SeasonState.NOT_STARTED), int(core.SeasonState.NOT_STARTED)]],
                dtype=np.int8,
            ),
            "onset_anomaly_days": np.array([[2.0, 4.0], [nan, nan]], dtype=np.float32),
            "days_past_median": np.array([[nan, nan], [10.0, 20.0]], dtype=np.float32),
            "p_onset_14d": np.array([[nan, nan], [0.25, 0.75]], dtype=np.float32),
            "p_onset_28d": np.array([[nan, nan], [0.5, 1.0]], dtype=np.float32),
        }
        self.result = {
            "layers": layers,
            "weight": np.array([[1.0, 1.0], [2.0, 2.0]], dtype=np.float32),
            "id_grid": np.array([[1, 1], [2, 2]], dtype=np.int32),
            "lookup": pd.DataFrame(
                {"id": [1, 2], "ADM_ID": [10, 20],
                 "ADM1_NAME": ["west unit", "east unit"]}
            ),
            "zone_id": np.array([[1, 2], [1, 2]], dtype=np.int32),
            "zone_lookup": pd.DataFrame({"id": [1, 2], "ADM1_NAME": ["zone_a", "zone_b"]}),
            "meta": {
                "country": "kenya",
                "crop": "maize",
                "season": 1,
                "harvest_year": 2026,
                "data_through": "2026-03-30",
            },
        }

    def test_status_area_shares_are_of_crop_area(self):
        table = monitor.status_area_frame(self.result)
        west = table[table["ADM1_NAME"] == "west unit"].iloc[0]
        east = table[table["ADM1_NAME"] == "east unit"].iloc[0]
        self.assertAlmostEqual(float(west["share_confirmed"]), 1.0, places=6)
        self.assertAlmostEqual(float(east["share_not_started"]), 1.0, places=6)
        # row 1 weighs 1 km2 per pixel, row 2 weighs 2 -> 2 and 4 km2 per unit
        self.assertAlmostEqual(float(west["total_weight_km2"]), 2.0, places=6)
        self.assertAlmostEqual(float(east["total_weight_km2"]), 4.0, places=6)
        self.assertEqual(list(table["data_through"].unique()), ["2026-03-30"])

    def test_onset_summary_covers_both_zone_types(self):
        table = monitor.onset_summary_frame(self.result)
        self.assertEqual(
            sorted(table["zone_type"].unique()), ["admin_1", "calendar_zone"]
        )
        admin = table[table["zone_type"] == "admin_1"].set_index("unit_name")
        # west unit holds anomalies 2 and 4 with equal weight:
        #   weighted mean   = (1*2 + 1*4) / 2 = 3
        #   weighted median = lower median of [2, 4] = 2
        self.assertAlmostEqual(
            float(admin.loc["west unit", "onset_anomaly_days_weighted_mean"]), 3.0, places=5
        )
        self.assertAlmostEqual(
            float(admin.loc["west unit", "onset_anomaly_days_weighted_median"]), 2.0, places=5
        )
        # east unit has no confirmed onset at all -> nothing valid to average
        self.assertAlmostEqual(
            float(admin.loc["east unit", "onset_anomaly_days_valid_weight_share"]),
            0.0, places=6,
        )
        # days past median: (2*10 + 2*20) / 4 = 15
        self.assertAlmostEqual(
            float(admin.loc["east unit", "days_past_median_weighted_mean"]), 15.0, places=5
        )
        zones = table[table["zone_type"] == "calendar_zone"].set_index("unit_name")
        # zone_a is the left column: anomaly 2 (row 0) only, p_onset_28d 0.5 (row 1)
        self.assertAlmostEqual(
            float(zones.loc["zone_a", "onset_anomaly_days_weighted_mean"]), 2.0, places=5
        )
        self.assertAlmostEqual(
            float(zones.loc["zone_b", "p_onset_28d_weighted_mean"]), 1.0, places=5
        )

    def test_tables_carry_the_identity_columns(self):
        for table in (monitor.status_area_frame(self.result),
                      monitor.onset_summary_frame(self.result)):
            for col in ("country", "crop", "season", "harvest_year", "data_through"):
                self.assertIn(col, table.columns)


if __name__ == "__main__":
    unittest.main()
