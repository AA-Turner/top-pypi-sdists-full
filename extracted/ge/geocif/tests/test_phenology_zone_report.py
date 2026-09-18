# -*- coding: utf-8 -*-
"""Tests for geocif/phenology/zone_report.py.

The report answers, per GEOGLAM calendar zone: in the two months around the
calendar planting date, how often has the season started, when, and how does the
season now running compare?

Fixture geometry, used by every test that needs a grid: a 2x4 window whose
columns 0-1 are zone "west" and columns 2-3 are zone "east". Weights are 1 km2
per pixel unless a test says otherwise, so a weighted share is just a pixel
count over 4.

Onset values are DAYS FROM THE PIXEL'S PLANTING START, which is what the cached
``sos`` rasters hold, so the window filter is a plain range test and negative
values are normal.
"""
import datetime as dt
import unittest

import numpy as np
import pandas as pd

from geocif.phenology import zone_report as zr

ZONE_ID = np.array([[1, 1, 2, 2],
                    [1, 1, 2, 2]], dtype="int16")
ZONE_NAMES = ["west", "east"]
WEIGHTS = np.ones((2, 4), dtype="float64")


def _stack(*years):
    """Stack per-year (2, 4) onset arrays."""
    return np.stack([np.asarray(y, dtype="float64") for y in years])


class TestWeightedQuantile(unittest.TestCase):
    """Weighted quantile, lower interpolation."""

    def test_uniform_weights_match_a_plain_quantile(self):
        v = np.array([1.0, 2.0, 3.0, 4.0])
        w = np.ones(4)
        # cumulative weight 1,2,3,4 of total 4; q=0.5 -> first index where
        # cum >= 2.0 -> index 1 -> value 2.0
        self.assertEqual(zr._weighted_quantile(v, w, 0.5), 2.0)
        self.assertEqual(zr._weighted_quantile(v, w, 0.0), 1.0)
        self.assertEqual(zr._weighted_quantile(v, w, 1.0), 4.0)

    def test_weight_moves_the_quantile(self):
        v = np.array([1.0, 10.0])
        # 9 units of weight on the 1 -> the median sits on 1
        self.assertEqual(zr._weighted_quantile(v, np.array([9.0, 1.0]), 0.5), 1.0)
        # and the other way round
        self.assertEqual(zr._weighted_quantile(v, np.array([1.0, 9.0]), 0.5), 10.0)

    def test_empty_and_zero_weight_give_nan(self):
        self.assertTrue(np.isnan(zr._weighted_quantile(np.array([]), np.array([]), 0.5)))
        self.assertTrue(np.isnan(zr._weighted_quantile(np.array([1.0]), np.array([0.0]), 0.5)))

    def test_nan_values_are_skipped(self):
        v = np.array([np.nan, 5.0, np.nan])
        self.assertEqual(zr._weighted_quantile(v, np.ones(3), 0.5), 5.0)


class TestCensoringShare(unittest.TestCase):
    """Onsets pinned at the search boundary are a floor, not a measurement."""

    def test_counts_only_values_at_or_beyond_the_boundary(self):
        # search opened 30 days early; -30 is the boundary, -29 is inside
        onset = np.array([-30.0, -30.0, -29.0, 5.0])
        # 2 of 4 pixels WITH an onset sit on the boundary
        self.assertAlmostEqual(zr.censoring_share(onset, np.ones(4), 30), 0.5)

    def test_denominator_is_pixels_that_started(self):
        # one boundary pixel, one ordinary, two that never started
        onset = np.array([-30.0, 5.0, np.nan, np.nan])
        # 1 of the 2 that started -> 0.5, NOT 1 of 4
        self.assertAlmostEqual(zr.censoring_share(onset, np.ones(4), 30), 0.5)

    def test_no_onset_anywhere_gives_nan(self):
        self.assertTrue(np.isnan(zr.censoring_share(np.full(3, np.nan), np.ones(3), 30)))

    def test_a_wider_lead_uncensors(self):
        onset = np.array([-30.0, -30.0, 5.0, 5.0])
        self.assertAlmostEqual(zr.censoring_share(onset, np.ones(4), 30), 0.5)
        # with the search opening 60 days early, -30 is an ordinary value
        self.assertAlmostEqual(zr.censoring_share(onset, np.ones(4), 60), 0.0)


class TestZoneMasks(unittest.TestCase):
    def test_zero_means_no_zone_and_ids_are_one_based(self):
        masks = zr.zone_masks(ZONE_ID, ZONE_NAMES)
        self.assertEqual(set(masks), {"west", "east"})
        self.assertEqual(int(masks["west"].sum()), 4)
        self.assertEqual(int(masks["east"].sum()), 4)
        zid = np.zeros((2, 2), dtype="int16")
        self.assertEqual(int(zr.zone_masks(zid, ["a"])["a"].sum()), 0)


class TestZoneHistory(unittest.TestCase):
    """Per (zone, year) shares and offsets, hand-computed."""

    @classmethod
    def setUpClass(cls):
        # year 2001: west all start at day 0 (in window); east all at +50 (after)
        y1 = [[0, 0, 50, 50], [0, 0, 50, 50]]
        # year 2002: west half start at -40 (before window), half never start;
        #            east all start at -10 (in window)
        y2 = [[-40, np.nan, -10, -10], [-40, np.nan, -10, -10]]
        cls.hist = zr.zone_history(
            _stack(y1, y2), [2001, 2002], ZONE_ID, ZONE_NAMES, WEIGHTS,
            window_days=30, search_lead_days=30,
        )

    def _row(self, zone, year):
        m = (self.hist.zone == zone) & (self.hist.harvest_year == year)
        return self.hist[m].iloc[0]

    def test_one_row_per_zone_year(self):
        self.assertEqual(len(self.hist), 4)

    def test_in_window_and_after_window(self):
        west = self._row("west", 2001)
        self.assertAlmostEqual(west.share_started, 1.0)
        self.assertAlmostEqual(west.share_in_window, 1.0)
        self.assertAlmostEqual(west.onset_median_days, 0.0)
        east = self._row("east", 2001)
        # +50 is past the +30 edge: started, but not in the window
        self.assertAlmostEqual(east.share_started, 1.0)
        self.assertAlmostEqual(east.share_in_window, 0.0)
        self.assertAlmostEqual(east.share_after_window, 1.0)
        self.assertTrue(np.isnan(east.onset_median_days))

    def test_before_window_and_never_started(self):
        west = self._row("west", 2002)
        # 2 of 4 pixels started, at -40 -> before the window; 2 never started
        self.assertAlmostEqual(west.share_started, 0.5)
        self.assertAlmostEqual(west.share_before_window, 0.5)
        self.assertAlmostEqual(west.share_in_window, 0.0)

    def test_median_is_over_in_window_pixels_only(self):
        east = self._row("east", 2002)
        self.assertAlmostEqual(east.share_in_window, 1.0)
        self.assertAlmostEqual(east.onset_median_days, -10.0)

    def test_dates_are_attached_when_planting_is_known(self):
        plant = {("west", 2001): dt.date(2001, 3, 1), ("east", 2001): dt.date(2001, 4, 1)}
        hist = zr.zone_history(
            _stack([[0, 0, 5, 5], [0, 0, 5, 5]]), [2001], ZONE_ID, ZONE_NAMES,
            WEIGHTS, window_days=30, planting_dates=plant,
        )
        west = hist[hist.zone == "west"].iloc[0]
        self.assertEqual(west.planting_date, "2001-03-01")
        self.assertEqual(west.onset_median_date, "2001-03-01")   # median offset 0
        east = hist[hist.zone == "east"].iloc[0]
        self.assertEqual(east.onset_median_date, "2001-04-06")   # 1 Apr + 5 d

    def test_mismatched_year_labels_raise(self):
        with self.assertRaises(ValueError):
            zr.zone_history(_stack([[0, 0, 0, 0], [0, 0, 0, 0]]), [2001, 2002],
                            ZONE_ID, ZONE_NAMES, WEIGHTS)

    def test_weights_drive_the_share(self):
        # give one west pixel 97 of the zone's 100 km2; it starts in window,
        # the other three do not -> share_in_window = 0.97, not 0.25
        w = WEIGHTS.copy()
        w[0, 0] = 97.0
        y = [[0, 50, 0, 0], [50, 50, 0, 0]]
        hist = zr.zone_history(_stack(y), [2001], ZONE_ID, ZONE_NAMES, w, window_days=30)
        west = hist[hist.zone == "west"].iloc[0]
        self.assertAlmostEqual(west.share_in_window, 97.0 / 100.0)


class TestZoneClimatology(unittest.TestCase):
    def test_collapses_years_and_counts_them(self):
        hist = pd.DataFrame({
            "zone": ["a"] * 4,
            "harvest_year": [2001, 2002, 2003, 2004],
            "share_in_window": [1.0, 0.5, 0.0, 1.0],
            "share_started": [1.0, 1.0, 1.0, 1.0],
            "share_censored": [0.0, 0.0, 0.0, 0.0],
            "onset_median_days": [0.0, 10.0, np.nan, 20.0],
        })
        clim = zr.zone_climatology(hist, min_years=3)
        row = clim.iloc[0]
        self.assertEqual(row.n_years, 4)
        self.assertEqual(row.n_years_with_onset, 3)      # one NaN
        self.assertAlmostEqual(row.share_in_window_mean, 0.625)   # (1+.5+0+1)/4
        self.assertAlmostEqual(row.onset_median_days, 10.0)       # median(0,10,20)

    def test_too_few_years_blanks_the_statistics_but_keeps_the_count(self):
        hist = pd.DataFrame({
            "zone": ["a", "a"],
            "harvest_year": [2001, 2002],
            "share_in_window": [1.0, 1.0],
            "share_started": [1.0, 1.0],
            "share_censored": [0.0, 0.0],
            "onset_median_days": [0.0, 10.0],
        })
        row = zr.zone_climatology(hist, min_years=20).iloc[0]
        self.assertEqual(row.n_years_with_onset, 2)
        self.assertTrue(np.isnan(row.onset_median_days))
        self.assertAlmostEqual(row.share_in_window_mean, 1.0)

    def test_empty_history(self):
        self.assertTrue(zr.zone_climatology(pd.DataFrame()).empty)


class TestWindowStatus(unittest.TestCase):
    """A partial window must never be read as a complete one."""

    PLANT = dt.date(2026, 10, 15)

    def test_not_open(self):
        # window opens 15 Sep; 5 Sep is before it
        s, obs, tot = zr.window_status(dt.date(2026, 9, 5), self.PLANT, 30)
        self.assertIs(s, zr.WindowStatus.NOT_OPEN)
        self.assertEqual((obs, tot), (0, 61))

    def test_partial_counts_days_from_the_opening(self):
        # 20 Sep is the 6th day of a window that opened on 15 Sep
        s, obs, tot = zr.window_status(dt.date(2026, 9, 20), self.PLANT, 30)
        self.assertIs(s, zr.WindowStatus.PARTIAL)
        self.assertEqual((obs, tot), (6, 61))

    def test_complete_on_and_after_the_closing_day(self):
        for day in (dt.date(2026, 11, 14), dt.date(2027, 1, 1)):
            s, obs, tot = zr.window_status(day, self.PLANT, 30)
            self.assertIs(s, zr.WindowStatus.COMPLETE, day)
            self.assertEqual((obs, tot), (61, 61))

    def test_the_opening_day_itself_is_partial_day_one(self):
        s, obs, _ = zr.window_status(dt.date(2026, 9, 15), self.PLANT, 30)
        self.assertIs(s, zr.WindowStatus.PARTIAL)
        self.assertEqual(obs, 1)


class TestCurrentVsHistory(unittest.TestCase):
    """Ranking the running season, and refusing to rank when it is too early."""

    @classmethod
    def setUpClass(cls):
        # history: west starts in window every year but one; east never does
        rows = []
        for y in range(2001, 2011):
            rows.append({"zone": "west", "harvest_year": y,
                         "share_in_window": 1.0 if y != 2005 else 0.0,
                         "share_started": 1.0, "share_censored": 0.0,
                         "onset_median_days": float(y - 2001)})
            rows.append({"zone": "east", "harvest_year": y,
                         "share_in_window": 0.0, "share_started": 1.0,
                         "share_censored": 0.0, "onset_median_days": np.nan})
        cls.history = pd.DataFrame(rows)
        cls.plant = {("west", 2026): dt.date(2026, 3, 1), ("east", 2026): dt.date(2026, 3, 1)}

    def test_complete_window_is_ranked(self):
        current = np.array([[0, 0, 50, 50], [0, 0, 50, 50]], dtype="float64")
        out = zr.current_vs_history(
            current, self.history, ZONE_ID, ZONE_NAMES, WEIGHTS,
            as_of=dt.date(2026, 6, 1), planting_dates=self.plant,
            harvest_year=2026, window_days=30,
        )
        west = out[out.zone == "west"].iloc[0]
        self.assertEqual(west.window_status, "complete")
        self.assertAlmostEqual(west.share_in_window, 1.0)
        # 10 past years, all share_in_window <= 1.0 -> 100th percentile
        self.assertAlmostEqual(west.share_percentile_vs_history, 100.0)
        self.assertEqual(west.n_history_years, 10)

    def test_partial_window_is_not_ranked(self):
        current = np.array([[0, np.nan, np.nan, np.nan],
                            [np.nan, np.nan, np.nan, np.nan]], dtype="float64")
        out = zr.current_vs_history(
            current, self.history, ZONE_ID, ZONE_NAMES, WEIGHTS,
            as_of=dt.date(2026, 2, 20), planting_dates=self.plant,
            harvest_year=2026, window_days=30,
        )
        west = out[out.zone == "west"].iloc[0]
        self.assertEqual(west.window_status, "partial")
        # the share is reported (it is a floor) but never ranked
        self.assertAlmostEqual(west.share_in_window, 0.25)
        self.assertTrue(np.isnan(west.share_percentile_vs_history))

    def test_unopened_window_reports_nothing_measurable(self):
        current = np.full((2, 4), np.nan)
        plant = {("west", 2027): dt.date(2027, 3, 1), ("east", 2027): dt.date(2027, 3, 1)}
        out = zr.current_vs_history(
            current, self.history, ZONE_ID, ZONE_NAMES, WEIGHTS,
            as_of=dt.date(2026, 9, 5), planting_dates=plant,
            harvest_year=2027, window_days=30,
        )
        west = out[out.zone == "west"].iloc[0]
        self.assertEqual(west.window_status, "not_open")
        self.assertEqual(west.window_days_observed, 0)
        for column in ("share_in_window", "share_started", "onset_median_days"):
            self.assertTrue(np.isnan(west[column]), column)
        self.assertEqual(west.window_opens, "2027-01-30")

    def test_which_side_of_the_window_is_reported(self):
        """A low in-window share is unreadable without the side it fell on.

        Kenya West 2026: 100 % of cropland started BEFORE the window, a median
        57 days ahead of the calendar date. Its 0 % in-window share and 6.7th
        percentile read as a failed season unless the split is published.
        """
        # west starts 40 d early (outside), east 40 d late (outside)
        current = np.array([[-40, -40, 40, 40], [-40, -40, 40, 40]], dtype="float64")
        out = zr.current_vs_history(
            current, self.history, ZONE_ID, ZONE_NAMES, WEIGHTS,
            as_of=dt.date(2026, 6, 1), planting_dates=self.plant,
            harvest_year=2026, window_days=30,
        )
        west = out[out.zone == "west"].iloc[0]
        east = out[out.zone == "east"].iloc[0]
        self.assertAlmostEqual(west.share_in_window, 0.0)
        self.assertAlmostEqual(west.share_before_window, 1.0)   # early, not absent
        self.assertAlmostEqual(west.share_after_window, 0.0)
        self.assertAlmostEqual(east.share_before_window, 0.0)
        self.assertAlmostEqual(east.share_after_window, 1.0)    # late
        # both started; only the timing differs
        self.assertAlmostEqual(west.share_started, 1.0)
        self.assertAlmostEqual(east.share_started, 1.0)

    def test_the_three_shares_account_for_everything_that_started(self):
        rng = np.random.default_rng(3)
        current = rng.normal(0, 40, size=(2, 4))
        out = zr.current_vs_history(
            current, self.history, ZONE_ID, ZONE_NAMES, WEIGHTS,
            as_of=dt.date(2026, 6, 1), planting_dates=self.plant,
            harvest_year=2026, window_days=30,
        )
        for _, row in out.iterrows():
            total = (row.share_before_window + row.share_in_window
                     + row.share_after_window)
            self.assertAlmostEqual(total, row.share_started, places=9, msg=row.zone)

    def test_a_missing_planting_date_is_not_open_not_a_crash(self):
        out = zr.current_vs_history(
            np.zeros((2, 4)), self.history, ZONE_ID, ZONE_NAMES, WEIGHTS,
            as_of=dt.date(2026, 6, 1), planting_dates={},
            harvest_year=2026, window_days=30,
        )
        self.assertTrue((out.window_status == "not_open").all())

    def test_the_running_year_is_excluded_from_its_own_history(self):
        history = pd.concat([
            self.history,
            pd.DataFrame([{"zone": "west", "harvest_year": 2026,
                           "share_in_window": 0.0, "share_started": 1.0,
                           "share_censored": 0.0, "onset_median_days": 99.0}]),
        ], ignore_index=True)
        out = zr.current_vs_history(
            np.zeros((2, 4)), history, ZONE_ID, ZONE_NAMES, WEIGHTS,
            as_of=dt.date(2026, 6, 1), planting_dates=self.plant,
            harvest_year=2026, window_days=30,
        )
        west = out[out.zone == "west"].iloc[0]
        self.assertEqual(west.n_history_years, 10)   # 2026 row dropped


class TestWindowIsAFilterNotARecomputation(unittest.TestCase):
    """The premise the whole module rests on.

    Onset is stored as days from each pixel's own planting start, so narrowing
    the reporting window can only reclassify values, never change them. A
    narrower window must be a subset of a wider one.
    """

    def test_narrowing_the_window_only_moves_pixels_out(self):
        rng = np.random.default_rng(0)
        cube = rng.normal(0, 25, size=(8, 2, 4))
        wide = zr.zone_history(cube, list(range(2001, 2009)), ZONE_ID, ZONE_NAMES,
                               WEIGHTS, window_days=45)
        narrow = zr.zone_history(cube, list(range(2001, 2009)), ZONE_ID, ZONE_NAMES,
                                 WEIGHTS, window_days=15)
        merged = wide.merge(narrow, on=["zone", "harvest_year"], suffixes=("_wide", "_narrow"))
        self.assertTrue((merged.share_in_window_narrow <= merged.share_in_window_wide + 1e-12).all())
        # and "started at all" is untouched by the window
        np.testing.assert_allclose(merged.share_started_wide, merged.share_started_narrow)
