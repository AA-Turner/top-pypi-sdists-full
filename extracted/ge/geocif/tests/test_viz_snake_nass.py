# -*- coding: utf-8 -*-
"""Tests for the snake chart's USDA rows (viz/nass.py condition fetch and
snake_data.build_cci_track / build_usda_yield_track).

What must hold: the repo's 0-100 crop condition index (and the 100-500 plan
variant as an affine rescale), the Quick Stats CONDITION query without a
short_desc filter and the geoprepare 99-101 share rule, CSV-first loading
with the API only for missing years and an injected session, the latest
report on or before the issue date, a baseline from the same date in the
other years with the target excluded, the observation date taken from the
report, roles from the run's config, and the USDA yield forecast measured
on the GEOCIF yield baseline.
"""
import json
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

from geocif.viz import nass, snake_data as sd
from tests.test_viz_snake_data import (COUNTRY, CROP, LIVE, REGIONS, STAGES, YEARS, area,
                                       write_db)


class _Resp:
    def __init__(self, status, data=None):
        self.status_code = status
        self._data = data or []

    def raise_for_status(self):
        if self.status_code >= 400:
            raise ValueError(f"HTTP {self.status_code}")

    def json(self):
        return {"data": self._data}


class _Session:
    """Fake requests session answering CONDITION queries from a table."""

    def __init__(self, rows_by_year, fail=False):
        self.rows_by_year = rows_by_year
        self.fail = fail
        self.calls = []

    def get(self, url, timeout=None, params=None):
        self.calls.append(params)
        if self.fail:
            import requests

            raise requests.ConnectionError("no network")
        rows = self.rows_by_year.get(int(params["year"]))
        return _Resp(400) if rows is None else _Resp(200, rows)


def raw_condition_rows(state, fips, year, weeks, shares):
    """Quick Stats-like rows: one per category per week."""
    rows = []
    for wk, sh in zip(weeks, shares):
        for cat, val in zip(("PCT VERY POOR", "PCT POOR", "PCT FAIR", "PCT GOOD", "PCT EXCELLENT"), sh):
            rows.append({"state_name": state, "state_alpha": state[:2].upper(),
                         "state_fips_code": fips, "year": str(year), "week_ending": wk,
                         "unit_desc": cat, "Value": str(val), "class_desc": "ALL CLASSES",
                         "commodity_desc": "CORN"})
    return rows


class TestIndex(unittest.TestCase):
    def test_cci_scales(self):
        self.assertAlmostEqual(nass.cci_index(1, 4, 20, 55, 20), 72.25)
        self.assertAlmostEqual(nass.cci_index(1, 4, 20, 55, 20, scale="plan"), 100 + 4 * 72.25)
        self.assertAlmostEqual(nass.cci_index(0, 0, 0, 0, 100), 100.0)
        with self.assertRaises(ValueError):
            nass.cci_index(0, 0, 0, 0, 100, scale="other")

    def test_tidy_drops_incomplete_weeks_and_pseudo_states(self):
        rows = raw_condition_rows("IOWA", "19", 2026, ["2026-06-07", "2026-06-14"],
                                  [(1, 4, 20, 55, 20), (0, 5, 25, 50, 10)])   # second sums to 90
        rows += raw_condition_rows("OTHER STATES", "98", 2026, ["2026-06-07"], [(1, 4, 20, 55, 20)])
        out = nass._tidy_condition(rows, "maize")
        self.assertEqual(len(out), 1)
        self.assertEqual(out["region"].iloc[0], "iowa")
        self.assertAlmostEqual(out["cci"].iloc[0], 72.25)
        self.assertAlmostEqual(out["cci_ge"].iloc[0], 75.0)
        self.assertEqual(out["week_ending"].iloc[0], pd.Timestamp("2026-06-07"))
        self.assertEqual(list(out.columns), nass.CONDITION_COLUMNS)


class TestFetch(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.rows = {2026: raw_condition_rows("IOWA", "19", 2026, ["2026-06-07"], [(1, 4, 20, 55, 20)])}

    def test_condition_query_and_cache(self):
        sess = _Session(self.rows)
        cache = self.tmp / "cond.csv"
        out = nass.fetch_condition("KEY", [2025, 2026], crops=("maize",), cache=cache, session=sess)
        self.assertEqual(len(out), 1)
        params = sess.calls[0]
        self.assertEqual(params["statisticcat_desc"], "CONDITION")
        self.assertEqual(params["agg_level_desc"], "STATE")
        self.assertEqual(params["commodity_desc"], "CORN")
        self.assertNotIn("short_desc", params)
        self.assertEqual({p["year"] for p in sess.calls}, {"2025", "2026"})   # 2025 answered 400
        self.assertTrue(cache.exists())
        offline = nass.fetch_condition(None, [2026], crops=("maize",), cache=cache, offline=True)
        self.assertAlmostEqual(offline["cci"].iloc[0], 72.25)
        self.assertEqual(offline["week_ending"].dtype.kind, "M")

    def test_network_failure_falls_back_to_cache_or_raises(self):
        cache = self.tmp / "cond.csv"
        nass.fetch_condition("KEY", [2026], crops=("maize",), cache=cache, session=_Session(self.rows))
        out = nass.fetch_condition("KEY", [2026], crops=("maize",), cache=cache,
                                   session=_Session(self.rows, fail=True))
        self.assertEqual(len(out), 1)
        with self.assertRaises(Exception):
            nass.fetch_condition("KEY", [2026], crops=("maize",), cache=self.tmp / "none.csv",
                                 session=_Session(self.rows, fail=True))
        with self.assertRaises(ValueError):
            nass.fetch_condition(None, [2026], crops=("maize",), session=_Session(self.rows))

    def test_csv_first_then_api_for_missing_years(self):
        csv = self.tmp / "quickstats_corn_soy_condition_state.csv"
        pd.DataFrame([{"crop": "maize", "region": "iowa", "state_alpha": "IA", "year": 2025,
                       "woy": 23, "week_ending": "2025-06-08", "cci": 70.0, "very_poor": 1,
                       "poor": 4, "fair": 25, "good": 55, "excellent": 15},
                      {"crop": "soybean", "region": "iowa", "state_alpha": "IA", "year": 2025,
                       "woy": 23, "week_ending": "2025-06-08", "cci": 60.0, "very_poor": 1,
                       "poor": 9, "fair": 30, "good": 50, "excellent": 10}]).to_csv(csv, index=False)
        sess = _Session(self.rows)
        out = nass.load_nass_crop_condition("maize", "Iowa", [2025, 2026], csv_path=csv,
                                            api_key="KEY", session=sess)
        self.assertEqual(sorted(out["year"].unique()), [2025, 2026])
        self.assertEqual({p["year"] for p in sess.calls}, {"2026"})           # only the missing year
        self.assertTrue((out["crop"] == "maize").all())
        self.assertAlmostEqual(float(out.loc[out["year"] == 2025, "cci_ge"].iloc[0]), 70.0)
        # no key, no fetch: the CSV years are returned and the gap is noted
        out2 = nass.load_nass_crop_condition("maize", None, [2025, 2026], csv_path=csv, api_key=None)
        self.assertEqual(sorted(out2["year"].unique()), [2025])
        self.assertIsNone(nass.nass_api_key(""))
        self.assertEqual(nass.nass_api_key(" abc "), "abc")


def weekly_condition(years, target_value=60.0, base_value=70.0, last_week="09-01"):
    """Weekly CCI for both test regions, Apr to the week ending ``last_week``,
    flat within a year: ``base_value`` plus a year-to-year wobble in baseline
    years, ``target_value`` in the live one."""
    rows = []
    for region in REGIONS:
        r = 1.0 if region == "Baringo" else 1.05
        for y in years:
            v = (target_value if y == LIVE else base_value + 3.0 * np.sin(y)) * r
            d = pd.Timestamp(f"{y}-04-05")
            end = pd.Timestamp(f"{y}-{last_week}")
            while d <= end:
                rows.append({"crop": CROP, "region": sd.norm_region(region), "state_alpha": "XX",
                             "year": y, "woy": d.isocalendar()[1], "week_ending": d, "cci": v,
                             "cci_ge": v + 5, "very_poor": 1, "poor": 4, "fair": 20,
                             "good": 55, "excellent": 20})
                d += pd.Timedelta(days=7)
    return pd.DataFrame(rows)


class TestCciTrack(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.db = write_db(self.tmp)
        self.fc = sd.load_forecasts(self.db, f"{COUNTRY}_{CROP}", model="tabpfn", season=1)
        self.cfg = sd.run_config(self.db, COUNTRY)
        self.sel = sd.selected_by_stage(self.db, f"{COUNTRY}_{CROP}", "tabpfn")

    def test_latest_report_before_the_issue_and_the_same_date_baseline(self):
        weekly = weekly_condition(YEARS)
        track = sd.build_cci_track(weekly, self.fc, country=COUNTRY, target_year=LIVE,
                                   selected=self.sel, candidates=sd.candidate_families(self.cfg),
                                   training_year_start=2017)
        self.assertEqual(len(track), len(STAGES))
        sep = track[track["issue_date"] == date(2026, 9, 1)].iloc[0]
        # the report used is the last one on or before Sep 1 2026 (Aug 30, a Sunday)
        self.assertLessEqual(sep["obs_date"], date(2026, 9, 1))
        self.assertEqual(sep["obs_date_kind"], "observed")
        self.assertEqual(sep["obs_date"], max(d for d in weekly["week_ending"].dt.date
                                              if d <= date(2026, 9, 1) and d.year == 2026))
        # baseline = the same date in 2017-2025 (flat 70 * weights), target 60 * weights -> z < 0
        self.assertLess(sep["value_std"], 0)
        self.assertEqual(sep["baseline_n"], 9)
        self.assertTrue(np.isfinite(sep["value_std"]))
        # by hand: national = area-weighted mean of the two states at the same date
        a, b = (np.mean([area(r, y) for y in (2023, 2024, 2025)]) for r in ("Baringo", "Bomet"))
        self.assertAlmostEqual(sep["value_raw"], (60.0 * a + 60.0 * 1.05 * b) / (a + b), places=6)
        self.assertEqual(sep["role"], "input")                  # cci_file is set in the run config
        self.assertTrue(sep["selected"])                        # MEAN_CCI selected at the Aug stage
        self.assertEqual(track["source"].iloc[0], "USDA NASS crop condition")

    def test_report_after_the_issue_is_not_used_and_stale_reports_are_skipped(self):
        weekly = weekly_condition(YEARS, last_week="05-20")     # reports stop in late May
        track = sd.build_cci_track(weekly, self.fc, country=COUNTRY, target_year=LIVE,
                                   training_year_start=2017)
        # the May and June issues have a report within 21 days; later issues do not
        self.assertEqual(sorted(track["issue_date"]), [date(2026, 5, 1), date(2026, 6, 1)])
        self.assertTrue((track["obs_date"] <= track["issue_date"]).all())

    def test_role_independent_when_the_run_did_not_use_cci(self):
        weekly = weekly_condition(YEARS)
        cands = sd.candidate_families({"use_cids": "['NDVI']", "cci_file": ""})
        track = sd.build_cci_track(weekly, self.fc, country=COUNTRY, target_year=LIVE,
                                   selected={}, candidates=cands, training_year_start=2017)
        self.assertEqual(set(track["role"]), {"independent"})

    def test_plan_scale_only_changes_the_raw_value(self):
        weekly = weekly_condition(YEARS)
        repo = sd.build_cci_track(weekly, self.fc, country=COUNTRY, target_year=LIVE,
                                  training_year_start=2017)
        plan = sd.build_cci_track(weekly, self.fc, country=COUNTRY, target_year=LIVE,
                                  training_year_start=2017, cci_scale="plan")
        np.testing.assert_allclose(repo["value_std"].values, plan["value_std"].values)
        np.testing.assert_allclose(plan["value_raw"].values, 100 + 4 * repo["value_raw"].values)

    def test_region_scope_and_ge_metric(self):
        weekly = weekly_condition(YEARS)
        track = sd.build_cci_track(weekly, self.fc, country=COUNTRY, target_year=LIVE,
                                   metric="cci_ge", region="Bomet", training_year_start=2017)
        self.assertEqual(set(track["scope"]), {"Bomet"})
        self.assertEqual(track["row"].iloc[0], sd.INDICATOR_META["cci_ge"].label)
        self.assertAlmostEqual(track["value_raw"].iloc[0], 60 * 1.05 + 5)


class TestUsdaYieldTrack(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.db = write_db(self.tmp)
        self.fc = sd.load_forecasts(self.db, f"{COUNTRY}_{CROP}", model="tabpfn", season=1)
        obs = sd.observed_series(self.fc)
        nat = sd.to_national(obs.assign(stage="obs"), COUNTRY, value_col=sd.OBS, obs_col=None, by=("year",))
        self.base = sd.loyo_baseline(nat["year"], nat["value"], LIVE, training_year_start=2017)

    def _nass(self, months=(7, 8), regions=REGIONS):
        from geocif.viz.cone import BU_PER_TNHA

        rows = []
        for m in months:
            for region in regions:
                tnha = (1.5 if region == "Baringo" else 2.0) + 0.04 * 11 + 0.1 * (m - 7)
                rows.append({"crop": CROP, "year": LIVE, "Region": region, "state_fips": "00",
                             "period": f"YEAR - {['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG'][m-1]} FORECAST",
                             "ref_month": m, "is_final": False,
                             "yield_bu_ac": tnha * BU_PER_TNHA["maize"],
                             "load_time": pd.Timestamp(f"{LIVE}-{m:02d}-12 12:00:00")})
        return pd.DataFrame(rows)

    def test_forecast_months_map_to_issues_and_share_the_yield_baseline(self):
        track = sd.build_usda_yield_track(self._nass(), self.fc, self.base, country=COUNTRY,
                                          crop="maize", target_year=LIVE,
                                          display=("bu/ac", 15.9318))
        # July and August reports serve the August and September issues only
        self.assertEqual(sorted(track["issue_date"]), [date(2026, 8, 1), date(2026, 9, 1)])
        sep = track[track["issue_date"] == date(2026, 9, 1)].iloc[0]
        self.assertEqual(sep["obs_date"], date(2026, 8, 12))
        self.assertEqual(sep["role"], "independent")
        self.assertEqual(sep["unit"], "bu/ac")
        # national = area-weighted t/ha, z on the GEOCIF LOYO baseline
        a, b = (np.mean([area(r, y) for y in (2023, 2024, 2025)]) for r in ("Baringo", "Bomet"))
        va, vb = 1.5 + 0.04 * 11 + 0.1, 2.0 + 0.04 * 11 + 0.1
        nat = (va * a + vb * b) / (a + b)
        self.assertAlmostEqual(sep["value_tnha"], nat, places=6)
        self.assertAlmostEqual(sep["value_std"], self.base.z(nat), places=6)
        self.assertAlmostEqual(sep["value_raw"], nat * 15.9318, places=4)

    def test_partial_pool_is_skipped(self):
        track = sd.build_usda_yield_track(self._nass(regions=["Baringo"]), self.fc, self.base,
                                          country=COUNTRY, crop="maize", target_year=LIVE)
        self.assertTrue(track.empty)

    def test_extra_tracks_join_build_tracks_and_count_toward_the_cap(self):
        from tests.test_viz_snake_data import write_cid

        root = write_cid(self.tmp)
        cid = sd.load_cid_years(root, "monthly_r", "admin_1", COUNTRY, CROP, 1, YEARS,
                                indices=["MEAN_NDVI", "PRCPTOT", "SU"])
        cfg = sd.run_config(self.db, COUNTRY)
        usda = sd.build_usda_yield_track(self._nass(), self.fc, self.base, country=COUNTRY,
                                         crop="maize", target_year=LIVE, display=("bu/ac", 15.9318))
        cci = sd.build_cci_track(weekly_condition(YEARS), self.fc, country=COUNTRY, target_year=LIVE,
                                 training_year_start=2017)
        tracks, meta = sd.build_tracks(self.fc, cid, [sd.INDICATOR_META[k] for k in ("ndvi", "rain")],
                                       country=COUNTRY, crop=CROP, target_year=LIVE, cfg=cfg,
                                       extra_tracks=(usda, cci))
        self.assertEqual(tracks["row"].nunique(), 5)
        self.assertIn("USDA yield forecast", set(tracks["row"]))
        self.assertIn("USDA NASS yield forecast", meta["sources"])
        self.assertTrue(any("Missing issues" in n for n in meta["notes"]))     # USDA lacks May-Jul
        with self.assertRaises(ValueError):
            sd.build_tracks(self.fc, cid, [sd.INDICATOR_META[k] for k in ("ndvi", "rain", "heat")],
                            country=COUNTRY, crop=CROP, target_year=LIVE, cfg=cfg,
                            extra_tracks=(usda, cci))


if __name__ == "__main__":
    unittest.main()
