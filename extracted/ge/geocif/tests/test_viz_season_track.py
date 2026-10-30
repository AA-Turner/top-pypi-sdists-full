# -*- coding: utf-8 -*-
"""Tests for the season track (geocif/viz/season_track.py) and the
``hindcasts.csv`` rows it reads (experiments/s2s_africa.hindcast_rows).

What must hold: each hindcast row names the init it was forecast from (also
for inits after planting and across the new year) and carries its unit's
area; both systems are area-weighted to the national value; S2S inits are
dated the 11th of the init month and outlook stages the first day after the
data cutoff, in the right calendar year of a season that crosses the new
year; inits after the planting month are left out by default; the year
ranking rewards beating the trend, not small errors in a year that landed on
trend, and skips years without an observation or without both systems; a
disagreement between the two observed series is reported.
"""
import sqlite3
import tempfile
import unittest
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

from geocif.experiments import s2s_africa
from geocif.viz import season_track as st
from geocif.viz._outlook_db import OBS, PRED

COUNTRY, CROP, TABLE = "Zimbabwe", "maize", "zimbabwe_maize"
PLANTING = 11
UNITS = {"ZW001": ("Alpha", 300.0), "ZW002": ("Beta", 100.0)}
YEARS = [2010, 2011, 2012, 2013, 2014]
LIVE = 2015
#: same observed yield in every unit, so national = this value
OBS_BY_YEAR = {2010: 1.0, 2011: 0.9, 2012: 0.5, 2013: 1.2, 2014: 0.85}
TREND = 1.0
OFFSETS = [4, 3, 2, 1, 0, -1]
STAGES = [  # (Stage Name, Stage Window Display): issued Dec 1 .. Mar 1
    ("Nov 1-Nov 30", "Nov 1-Nov 30"),
    ("Dec 1-Nov 30", "Nov 1-Dec 31"),
    ("Jan 1-Nov 30", "Nov 1-Jan 31"),
    ("Feb 1-Nov 30", "Nov 1-Feb 28"),
]


def s2s_ahat(fnid, year):
    """The S2S model calls 2012 (0.55 vs trend 1.0) and says trend
    otherwise; Beta's 2010 differs so the national weight is visible."""
    if year == 2012:
        return -0.45
    if year == 2010 and fnid == "ZW002":
        return -0.2
    return 0.0


def hindcasts(obs_shift=None):
    obs_shift = obs_shift or {}
    lo = pd.DataFrame([
        {"fnid": f, "year": y, "obs": OBS_BY_YEAR[y] * obs_shift.get(y, 1.0),
         "trend": TREND, "anom": OBS_BY_YEAR[y] / TREND - 1,
         "ahat": s2s_ahat(f, y), "z_PRCPTOT": 0.1}
        for f in UNITS for y in YEARS])
    areas = pd.DataFrame([{"fnid": f, "year": y, "area": a}
                          for f, (_, a) in UNITS.items() for y in YEARS])
    keys = {"country": COUNTRY, "crop": CROP, "season_name": "Main"}
    return pd.concat([s2s_africa.hindcast_rows(lo, areas, keys, PLANTING, True, off)
                      for off in OFFSETS], ignore_index=True)


def db_rows():
    rows = []
    for fnid, (region, area) in UNITS.items():
        for year in YEARS + [LIVE]:
            live = year == LIVE
            for stage, swd in STAGES:
                rows.append({
                    "Experiment Name": "outlook", "Model": "kumo",
                    "Country": "Zimbabwe", "Region": region,
                    "Harvest Year": str(year), "Season": 1,
                    "Stage Name": stage, "Stage Window Display": swd,
                    PRED: 0.7 if live else OBS_BY_YEAR[year] + 0.02,
                    OBS: np.nan if live else OBS_BY_YEAR[year],
                    "Area (ha)": np.nan if live else area,
                    "Date": "October_11_2026",
                    "Time": "October-11-2026 23:00:00"})
    return pd.DataFrame(rows)


class Fixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.db = root / "outlook_10_11_2026_23h00.db"
        con = sqlite3.connect(self.db)
        db_rows().to_sql(TABLE, con, index=False)
        con.close()
        self.run_dir = root / "s2s_run"
        self.run_dir.mkdir()
        self.h = hindcasts()
        self.h.to_csv(self.run_dir / "hindcasts.csv", index=False)
        self.out = root / "out"

    def tearDown(self):
        self.tmp.cleanup()

    def frames(self, h=None):
        pre = st.s2s_national(h if h is not None else self.h, COUNTRY)
        ins = st.outlook_national(self.db, TABLE, "kumo", COUNTRY)
        return pre, ins


class TestHindcastRows(Fixture):
    def test_each_row_names_its_init(self):
        h = self.h[(self.h.fnid == "ZW001") & (self.h.year == 2012)]
        got = {int(r.offset): (int(r.init_year), int(r.init_month))
               for r in h.itertuples()}
        # Nov planting of the 2011/12 season
        self.assertEqual(got[4], (2011, 7))
        self.assertEqual(got[0], (2011, 11))
        self.assertEqual(got[-1], (2011, 12))

    def test_init_after_the_new_year(self):
        lo = pd.DataFrame({"fnid": ["ZW001"], "year": [2012], "obs": [0.5],
                           "trend": [1.0], "anom": [-0.5], "ahat": [0.0]})
        areas = pd.DataFrame({"fnid": ["ZW001"], "year": [2012], "area": [1.0]})
        keys = {"country": COUNTRY, "crop": CROP, "season_name": "Main"}
        h = s2s_africa.hindcast_rows(lo, areas, keys, PLANTING, True, -2)
        self.assertEqual((h.init_year.iloc[0], h.init_month.iloc[0]), (2012, 1))

    def test_level_is_trend_times_anomaly_and_area_rides_along(self):
        r = self.h[(self.h.fnid == "ZW002") & (self.h.year == 2010)].iloc[0]
        self.assertAlmostEqual(r.yhat_tha, TREND * (1 - 0.2))
        self.assertEqual(r.area, 100.0)
        self.assertEqual(list(self.h.columns), s2s_africa.HINDCAST_COLUMNS)


class TestNational(Fixture):
    def test_s2s_is_area_weighted_and_dated_the_11th(self):
        pre, _ = self.frames()
        r = pre[(pre.year == 2010) & (pre.offset == 4)].iloc[0]
        self.assertAlmostEqual(r.value, (300 * 1.0 + 100 * 0.8) / 400)
        self.assertEqual(r.date_made, date(2009, 7, 11))
        self.assertEqual(r.label, "Jul init")
        self.assertEqual((r.plant_year, r.plant_month), (2009, 11))

    def test_inits_after_planting_are_left_out_by_default(self):
        pre, _ = self.frames()
        self.assertEqual(sorted(pre.offset.unique()), [0, 1, 2, 3, 4])
        wider = st.s2s_national(self.h, COUNTRY, min_offset=-1)
        self.assertIn(-1, set(wider.offset))

    def test_outlook_issue_dates_cross_the_new_year(self):
        _, ins = self.frames()
        got = sorted(ins[ins.year == 2012].date_made)
        self.assertEqual(got, [date(2011, 12, 1), date(2012, 1, 1),
                               date(2012, 2, 1), date(2012, 3, 1)])
        self.assertTrue(np.allclose(ins[ins.year == 2012].value, 0.52))


class TestTrack(Fixture):
    def test_positions_on_the_season_axis(self):
        track, info = st.build_track(*self.frames())
        g = track[track.year == 2012].set_index("label")["x"]
        self.assertAlmostEqual(g["Jul init"], -4 + 10 / 31)
        self.assertAlmostEqual(g["Nov init"], 10 / 30)
        self.assertAlmostEqual(g["Dec 1"], 1.0)
        self.assertAlmostEqual(g["Mar 1"], 4.0)

    def test_live_year_without_s2s_borrows_the_planting_date(self):
        track, info = st.build_track(*self.frames())
        p = info.set_index("year")
        self.assertEqual((p.at[LIVE, "plant_year"], p.at[LIVE, "plant_month"]),
                         (2014, 11))
        self.assertTrue(np.isnan(p.at[LIVE, "obs"]))
        self.assertAlmostEqual(
            track[(track.year == LIVE) & (track.label == "Dec 1")].x.iloc[0], 1.0)

    def test_ranking_rewards_beating_the_trend(self):
        track, info = st.build_track(*self.frames())
        rank = st.rank_years(track, info)
        self.assertEqual(rank.year.tolist(), [2012, 2013, 2014, 2011, 2010])
        # 2010 landed on trend: tiny errors, yet nothing beaten
        r = rank.set_index("year")
        self.assertTrue(np.isnan(r.at[2010, "skill"]))
        self.assertLess(r.at[2010, "gain"], 0)
        self.assertNotIn(LIVE, set(rank.year))

    def test_a_big_trend_miss_alone_does_not_win(self):
        # A: trend missed by 0.5, forecasts by 0.25 (gain 0.25, skill 0.5);
        # B: trend missed by 0.2, forecasts by 0.02 (gain 0.18, skill 0.9)
        info = pd.DataFrame({"year": [1, 2], "obs": [0.5, 0.6],
                             "trend": [1.0, 0.8]})
        track = pd.DataFrame({
            "year": [1, 1, 2, 2], "system": [st.PRE, st.INS] * 2,
            "value": [0.75, 0.75, 0.62, 0.62]})
        rank = st.rank_years(track, info)
        self.assertEqual(rank.year.tolist(), [2, 1])
        self.assertGreater(rank.set_index("year").at[1, "gain"],
                           rank.set_index("year").at[2, "gain"])

    def test_observed_disagreement_is_reported(self):
        h = hindcasts(obs_shift={2013: 1.05})
        with self.assertLogs("geocif.viz.season_track", level="WARNING") as cm:
            st.build_track(*self.frames(h))
        self.assertIn("2013", "\n".join(cm.output))

    def test_lead_skill_counts_years(self):
        track, info = st.build_track(*self.frames())
        sk = st.lead_skill(track, info)
        self.assertTrue((sk.n == len(YEARS)).all())
        self.assertEqual(sk.label.tolist()[:5],
                         ["Jul init", "Aug init", "Sep init", "Oct init",
                          "Nov init"])


class TestRun(Fixture):
    def test_writes_the_figure_notes_and_csvs_for_the_best_years(self):
        res = st.run(db=self.db, table=TABLE, model="kumo",
                     s2s_run=self.run_dir, country=COUNTRY, crop=CROP,
                     out=self.out)
        self.assertEqual(res["years"], [2012, 2013])
        for k in ("png", "txt", "csv", "ranking_csv"):
            self.assertTrue(Path(res[k]).exists(), k)
        self.assertTrue((self.out / "plots" / "lookup_plots_csvs.csv").exists())
        text = Path(res["txt"]).read_text(encoding="utf-8")
        self.assertIn("2012: observed 0.500 t/ha", text)
        self.assertIn("N= 5", text)

    def test_explicit_years_and_a_missing_one(self):
        res = st.run(db=self.db, table=TABLE, model="kumo",
                     s2s_run=self.run_dir, country=COUNTRY, crop=CROP,
                     out=self.out, years=[2014, 2010])
        self.assertEqual(res["years"], [2014, 2010])
        with self.assertRaises(ValueError):
            st.run(db=self.db, table=TABLE, model="kumo", s2s_run=self.run_dir,
                   country=COUNTRY, crop=CROP, out=self.out, years=[1999])

    def test_a_run_without_hindcasts_csv_says_so(self):
        (self.run_dir / "hindcasts.csv").unlink()
        with self.assertRaises(FileNotFoundError):
            st.load_s2s(self.run_dir, COUNTRY, CROP)


if __name__ == "__main__":
    unittest.main()
