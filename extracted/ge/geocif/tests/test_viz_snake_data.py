# -*- coding: utf-8 -*-
"""Tests for the snake chart data layer (geocif/viz/snake_data.py).

What must hold: leave-one-year-out baselines (the target year never enters
its own trend, spread or indicator baseline; ``training_year_start`` floors
them), stage names mapped to Stage_ID chains and to observation / issue
dates (also across the new year), Season-aware reads that keep the newest
write, a causal area fill for the live year, area-weighted national
indicators read at the stage's window from the per-year CID tables, roles
resolved from the run's config and ``Selected Features``, the causality
guard on real observation dates, and the four-indicator cap.
"""
import sqlite3
import tempfile
import unittest
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

from geocif.viz import snake_data as sd
from geocif.viz._outlook_db import OBS, PRED

COUNTRY, CROP, SEASON = "kenya", "maize", 1
REGIONS = {"Baringo": 300.0, "Bomet": 200.0}
YEARS = list(range(2015, 2027))          # 2026 is the live year
LIVE = 2026
STAGES = [  # (Stage Name, Stage Window Display, Stage_ID)
    ("Apr 1-Apr 30", "Apr 1-Apr 30", "4"),
    ("May 1-Apr 30", "Apr 1-May 31", "5_4"),
    ("Jun 1-Apr 30", "Apr 1-Jun 30", "6_5_4"),
    ("Jul 1-Apr 30", "Apr 1-Jul 31", "7_6_5_4"),
    ("Aug 1-Apr 30", "Apr 1-Aug 31", "8_7_6_5_4"),
]
LIVE_PATH = [1.00, 1.08, 0.96, 0.90, 0.86]   # multiplier of the trend, per stage


def obs_yield(region, year):
    base = 1.5 if region == "Baringo" else 2.0
    return base + 0.04 * (year - 2015) + 0.08 * np.sin(year * 1.7)


def area(region, year):
    return REGIONS[region] + 5.0 * (year - 2015)


def selected(stage):
    feats = [f"PRCPTOT {stage}", f"SU {stage}"]
    if stage.startswith(("Jul", "Aug")):
        feats.append(f"MEAN_NDVI {stage}")
    if stage.startswith("Aug"):
        feats.append("MEAN_CCI Aug 1-Aug 31")
    return str(feats)


def db_rows(model="tabpfn", with_season2=True, with_dup=True):
    rows = []
    for region in REGIONS:
        for year in YEARS:
            for k, (stage, swd, sid) in enumerate(STAGES):
                live = year == LIVE
                trend = 1.5 + 0.04 * (year - 2015) if region == "Baringo" else 2.0 + 0.04 * (year - 2015)
                pred = trend * LIVE_PATH[k] if live else obs_yield(region, year) + 0.05 * (k - 2)
                rows.append({
                    "Experiment Name": "outlook", "Model": model, "Country": "Kenya",
                    "Region": region, "Harvest Year": str(year), "Season": 1,
                    "Stage Name": stage, "Stage Window Display": swd, "Stage_ID": sid,
                    "Selected Features": selected(stage),
                    PRED: pred, OBS: np.nan if live else obs_yield(region, year),
                    "Area (ha)": np.nan if live else area(region, year),
                    "Date": "September_17_2026", "Time": "September-17-2026 14:18:00",
                })
    if with_season2:   # a second season sharing Region and Stage Name
        for region in REGIONS:
            rows.append({**rows[0], "Region": region, "Harvest Year": str(LIVE), "Season": 2,
                         "Stage Name": STAGES[-1][0], "Stage Window Display": STAGES[-1][1],
                         "Stage_ID": STAGES[-1][2], PRED: 99.0, OBS: np.nan, "Area (ha)": np.nan})
    if with_dup:       # a stale duplicate of one live row, written earlier
        dup = dict(rows[len(STAGES) - 1 + (len(YEARS) - 1) * len(STAGES)])
        assert dup["Harvest Year"] == str(LIVE) and dup["Stage Name"] == STAGES[-1][0]
        dup.update({PRED: 5.55, "Date": "September_10_2026", "Time": "September-10-2026 12:00:00"})
        rows.append(dup)
    return pd.DataFrame(rows)


CONFIG_ROWS = [
    ("ML", "method", "monthly_r"), ("ML", "run_time_steps", "all"),
    ("ML", "detrend_method", "gaussian"), ("ML", "use_cids", "['all']"),
    ("ML", "models", "['tabpfn', 'trend']"), ("DEFAULT", "training_year_start", "2010"),
    ("kenya", "training_year_start", "2017"),
    ("DEFAULT", "cci_file", "/meta/crop_condition/quickstats.csv"),
    ("DEFAULT", "admin_zone", "admin_1"),
    ("zambia", "only_in_zambia", "x"),
]


def write_db(tmp, cfg_rows=CONFIG_ROWS, **kw):
    db = Path(tmp) / "outlook_09_17_2026_14h18.db"
    con = sqlite3.connect(db)
    db_rows(**kw).to_sql(f"{COUNTRY}_{CROP}", con, index=False)
    if cfg_rows is not None:
        pd.DataFrame(cfg_rows, columns=["Section", "Option", "Value"]).assign(Now="x") \
            .to_sql("config_September_17_2026", con, index=False)
    con.close()
    return db


def cid_value(index, region, year, tok):
    months = [int(t) for t in tok.split("_")]
    n = len(months)
    r = 1.0 if region == "Baringo" else 1.2
    if index == "MEAN_NDVI":
        return r * (0.5 + 0.01 * (year - 2015) + 0.02 * n + 0.03 * np.cos(year))
    if index == "PRCPTOT":
        return r * (60.0 * n + 5.0 * np.sin(year) + (20.0 if year == LIVE else 0.0))
    if index == "SU":
        return r * (10.0 * n + 2.0 * np.cos(year * 0.9) + (6.0 if year == LIVE else 0.0))
    raise KeyError(index)


def write_cid(tmp, years=YEARS):
    root = Path(tmp)
    d = sd.cid_dir(root, "monthly_r", "admin_1", COUNTRY, CROP)
    d.mkdir(parents=True, exist_ok=True)
    toks = sorted({t for _, _, s in STAGES for t in (s, s.split("_")[0])})
    for year in years:
        rows = []
        for region in REGIONS:
            for tok in toks:
                for index, typ in (("MEAN_NDVI", "VI"), ("PRCPTOT", "Rain"), ("SU", "Heat")):
                    rows.append({"Description": index, "CID": cid_value(index, region, year, tok),
                                 "Country": "Kenya", "Region": region, "Area": np.nan,
                                 "Crop": "Maize", "Season": 1, "Method": "monthly_r",
                                 "Stage": tok, "Harvest Year": year, "Index": index, "Type": typ})
        pd.DataFrame(rows).to_csv(d / f"{COUNTRY}_{CROP}_s{SEASON}_{year}.csv", index=False)
    return root


class TestStagesAndDates(unittest.TestCase):
    def test_stage_id_from_name(self):
        self.assertEqual(sd.stage_id_from_name("Aug 1-Apr 30", "Apr 1-Aug 31"), "8_7_6_5_4")
        self.assertEqual(sd.stage_id_from_name("Apr 1-Apr 30", "Apr 1-Apr 30"), "4")
        self.assertEqual(sd.stage_id_from_name("Jan 1-Oct 31", "Oct 1-Jan 31"), "1_12_11_10")
        self.assertIsNone(sd.stage_id_from_name("Pre-Season (init Feb)", "Pre-Season (init Feb)"))

    def test_dates_within_one_year(self):
        order = {4: 4, 5: 5, 8: 8}
        obs, issue = sd.stage_dates(8, order, 2026)
        self.assertEqual((obs, issue), (date(2026, 8, 31), date(2026, 9, 1)))

    def test_dates_across_the_new_year(self):
        from geocif.viz.leadtime import _season_order

        order = _season_order([10, 11, 12, 1, 2])
        self.assertEqual(sd.stage_dates(10, order, 2027), (date(2026, 10, 31), date(2026, 11, 1)))
        self.assertEqual(sd.stage_dates(12, order, 2027), (date(2026, 12, 31), date(2027, 1, 1)))
        self.assertEqual(sd.stage_dates(2, order, 2027), (date(2027, 2, 28), date(2027, 3, 1)))

    def test_window_tokens(self):
        self.assertEqual(sd.window_stage_id("8_7_6_5_4", "stage"), "8_7_6_5_4")
        self.assertEqual(sd.window_stage_id("8_7_6_5_4", "month"), "8")
        with self.assertRaises(ValueError):
            sd.window_stage_id("8", "week")

    def test_lookup_by_key_or_cid_name(self):
        self.assertIs(sd.lookup_indicator("rain"), sd.INDICATOR_META["rain"])
        self.assertEqual(sd.lookup_indicator("PRCPTOT").key, "rain")
        self.assertEqual(sd.lookup_indicator("dd").key, "dry_days")
        self.assertTrue(sd.lookup_indicator("DD").invert)
        self.assertEqual(sd.lookup_indicator("AUC_NDVI").key, "ndvi_auc")
        self.assertFalse(sd.lookup_indicator("AUC_NDVI").invert)
        with self.assertRaises(KeyError):
            sd.lookup_indicator("NOPE")
        self.assertEqual(sd.last_years(2026, 5), [2021, 2022, 2023, 2024, 2025])

    def test_any_cid_from_the_definitions(self):
        r10 = sd.lookup_indicator("R10mm")
        self.assertEqual((r10.cid, r10.label, r10.invert, r10.variable), ("R10mm", "R10mm", False, "chirps"))
        self.assertTrue(sd.lookup_indicator("TXx").invert)          # Heat
        self.assertTrue(sd.lookup_indicator("MAX_ETREF").invert)    # ETREF
        self.assertFalse(sd.lookup_indicator("MIN_ESI4WK").invert)  # ESI: higher is wetter
        self.assertEqual(sd.lookup_indicator("MIN_ESI4WK").variable, "esi_4wk")
        self.assertEqual(sd.lookup_indicator("AUC_GCVI").variable, "gcvi")
        self.assertFalse(sd.lookup_indicator("R10mm", invert=False).invert)
        self.assertTrue(sd.lookup_indicator("R10mm", invert=True).invert)
        self.assertEqual(sd.lookup_indicator("PRCPTOT", label="Rain").label, "Rain")
        self.assertFalse(sd.lookup_indicator("DD", invert=False).invert)  # registry entry overridden
        with self.assertRaises(KeyError):
            sd.lookup_indicator("NOT_A_CID")

    def test_feature_family(self):
        self.assertEqual(sd.feature_family("MEAN_NDVI Aug 1-Apr 30"), "NDVI")
        self.assertEqual(sd.feature_family("AUC_ESI4WK Jul 1-Jul 31"), "ESI4WK")
        self.assertEqual(sd.feature_family("PRCPTOT May 1-May 31"), "PRCPTOT")
        self.assertEqual(sd.feature_family("DELTA_MEAN_CCI Sep"), "CCI")
        self.assertEqual(sd.INDICATOR_META["ndvi"].family, "NDVI")
        self.assertEqual(sd.INDICATOR_META["rain"].family, "PRCPTOT")


class TestForecasts(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.db = write_db(self.tmp)

    def test_season_filter_dedup_and_dates(self):
        fc = sd.load_forecasts(self.db, f"{COUNTRY}_{CROP}", model="tabpfn", season=1)
        self.assertFalse((fc["Season"] == 2).any())
        live_aug = fc[(fc["year"] == LIVE) & (fc["stage"] == "Aug 1-Apr 30")
                      & (fc["Region"] == "Baringo")]
        self.assertEqual(len(live_aug), 1)                       # the stale duplicate is gone
        self.assertAlmostEqual(float(live_aug[PRED].iloc[0]), (1.5 + 0.04 * 11) * LIVE_PATH[-1])
        self.assertEqual(live_aug["obs_date"].iloc[0], date(2026, 8, 31))
        self.assertEqual(live_aug["issue_date"].iloc[0], date(2026, 9, 1))
        self.assertEqual(live_aug["stage_id"].iloc[0], "8_7_6_5_4")
        self.assertEqual(live_aug["run_date"].iloc[0], date(2026, 9, 17))

    def test_two_seasons_need_a_choice(self):
        with self.assertRaises(ValueError):
            sd.load_forecasts(self.db, f"{COUNTRY}_{CROP}", model="tabpfn")

    def test_causal_area_fill(self):
        fc = sd.load_forecasts(self.db, f"{COUNTRY}_{CROP}", model="tabpfn", season=1)
        live = fc[(fc["year"] == LIVE) & (fc["Region"] == "Baringo")]
        expect = np.mean([area("Baringo", y) for y in (2023, 2024, 2025)])
        self.assertTrue(live["area_filled"].all())
        self.assertTrue(np.allclose(live[sd.AREA], expect))
        hind = fc[(fc["year"] == 2020) & (fc["Region"] == "Baringo")]
        self.assertFalse(hind["area_filled"].any())

    def test_causal_area_uses_earliest_when_nothing_precedes(self):
        df = pd.DataFrame({"Region": ["A"] * 4, "year": [2010, 2011, 2012, 2013],
                           sd.AREA: [np.nan, 10.0, 20.0, 30.0]})
        out = sd.causal_area(df)
        self.assertAlmostEqual(float(out.loc[out["year"] == 2010, sd.AREA].iloc[0]), 20.0)

    def test_stage_id_falls_back_to_the_name(self):
        con = sqlite3.connect(self.db)
        con.execute(f'UPDATE "{COUNTRY}_{CROP}" SET "Stage_ID" = NULL')
        con.commit()
        con.close()
        fc = sd.load_forecasts(self.db, f"{COUNTRY}_{CROP}", model="tabpfn", season=1)
        self.assertEqual(set(fc["stage_id"]), {s for _, _, s in STAGES})

    def test_run_config_prefers_the_country_section(self):
        cfg = sd.run_config(self.db, country=COUNTRY)
        self.assertEqual(cfg["training_year_start"], "2017")
        self.assertEqual(cfg["detrend_method"], "gaussian")
        self.assertEqual(sd.literal(cfg["use_cids"]), ["all"])
        self.assertEqual(sd.run_config(self.db)["training_year_start"], "2010")
        # another country's section never leaks in
        self.assertNotIn("only_in_zambia", cfg)
        self.assertEqual(sd.run_config(self.db, country="ethiopia")["training_year_start"], "2010")

    def test_flat_rows(self):
        t = pd.DataFrame({"row": ["Y", "Heat", "Heat", "Rain"], "role": ["target", "input", "input", "input"],
                          "issue_date": [date(2026, 9, 1), date(2026, 8, 1), date(2026, 9, 1), date(2026, 9, 1)],
                          "baseline_mean": [np.nan, 150.0, 153.0, 800.0],
                          "baseline_sd": [np.nan, 0.6, 0.6, 110.0]})
        self.assertEqual(sd.flat_rows(t), ["Heat"])


class TestBaselines(unittest.TestCase):
    def _series(self):
        years = np.arange(2008, 2026)
        rng = np.random.RandomState(0)
        y = 2.0 + 0.05 * (years - 2008) + rng.normal(0, 0.1, len(years))
        return years, y

    def test_target_year_never_enters_its_own_baseline(self):
        years, y = self._series()
        b1 = sd.loyo_baseline(years, y, 2020)
        y2 = y.copy()
        y2[list(years).index(2020)] += 5.0          # a wild target-year value
        b2 = sd.loyo_baseline(years, y2, 2020)
        self.assertAlmostEqual(b1.trend, b2.trend)
        self.assertAlmostEqual(b1.sd, b2.sd)
        self.assertNotIn(2020, b1.years)

    def test_row_order_does_not_matter(self):
        years, y = self._series()
        perm = np.random.RandomState(1).permutation(len(years))
        b1 = sd.loyo_baseline(years, y, 2026)
        b2 = sd.loyo_baseline(years[perm], y[perm], 2026)
        self.assertAlmostEqual(b1.trend, b2.trend)
        self.assertAlmostEqual(b1.sd, b2.sd)

    def test_training_year_start_floor(self):
        years, y = self._series()
        b = sd.loyo_baseline(years, y, 2026, training_year_start=2015)
        self.assertEqual(b.years[0], 2015)
        self.assertEqual(b.n, 11)

    def test_gaussian_space_and_linear_by_hand(self):
        years = np.arange(2010, 2020)
        e = np.array([0.05, -0.05] * 5)
        y = 1.0 + 0.1 * (years - 2010) + e
        g = sd.loyo_baseline(years, y, 2020, model_type="gaussian", min_years=5)
        self.assertEqual(g.space, "percent")
        self.assertGreater(g.trend, 1.5)
        lin = sd.loyo_baseline(years, y, 2020, model_type="linear", min_years=5)
        self.assertEqual(lin.space, "absolute")
        slope, intercept = np.polyfit(years, y, 1)
        self.assertAlmostEqual(lin.trend, slope * 2020 + intercept, places=6)
        resid = y - (slope * years + intercept)
        self.assertAlmostEqual(lin.sd, float(np.std(resid, ddof=1)), places=6)
        self.assertAlmostEqual(lin.z(lin.trend + lin.sd), 1.0)
        self.assertAlmostEqual(g.z(g.trend * 1.10), 10.0 / g.sd)

    def test_degenerate_cases_raise(self):
        years = np.arange(2010, 2020)
        with self.assertRaises(ValueError):
            sd.loyo_baseline(years, 1.0 + 0.1 * (years - 2010), 2020, model_type="linear")
        with self.assertRaises(ValueError):
            sd.loyo_baseline(years[:3], [1, 2, 3], 2020)
        with self.assertRaises(ValueError):
            sd.loyo_baseline(years, years * 0.1, 2020, model_type="difference")

    def test_standardize_is_loyo(self):
        s = pd.Series([1.0, 1.2, 0.8, 1.1, 0.9, 1.05, 3.0], index=range(2019, 2026))
        z, mean, sdv, n = sd.standardize(s, 2025)
        base = s.drop(2025)
        self.assertAlmostEqual(mean, base.mean())
        self.assertAlmostEqual(sdv, base.std(ddof=1))
        self.assertAlmostEqual(z, (3.0 - mean) / sdv)
        self.assertEqual(n, 6)
        s2 = s.copy()
        s2[2025] = -4.0
        self.assertAlmostEqual(sd.standardize(s2, 2025)[1], mean)
        z3, _, _, n3 = sd.standardize(s, 2025, baseline_years=(2020, 2024))
        self.assertEqual(n3, 5)
        self.assertTrue(np.isnan(sd.standardize(s.drop(2025), 2025)[0]))
        with self.assertRaises(ValueError):
            sd.standardize(pd.Series([1.0] * 6, index=range(2019, 2025)), 2024)
        with self.assertRaises(ValueError):
            sd.standardize(s, 2025, min_years=10)


class TestIndicators(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.db = write_db(self.tmp)
        self.root = write_cid(self.tmp)
        self.fc = sd.load_forecasts(self.db, f"{COUNTRY}_{CROP}", model="tabpfn", season=1)
        self.cid = sd.load_cid_years(self.root, "monthly_r", "admin_1", COUNTRY, CROP, SEASON,
                                     YEARS, indices=["MEAN_NDVI", "PRCPTOT", "SU"])

    def test_cid_tables_load_and_windows_read(self):
        self.assertEqual(set(self.cid["Index"]), {"MEAN_NDVI", "PRCPTOT", "SU"})
        v = sd.indicator_by_year(self.cid, "PRCPTOT", "8_7_6_5_4", window="stage")
        self.assertEqual(len(v), len(REGIONS) * len(YEARS))
        row = v[(v["Region"] == "Baringo") & (v["year"] == 2020)]
        self.assertAlmostEqual(float(row["value"].iloc[0]), cid_value("PRCPTOT", "Baringo", 2020, "8_7_6_5_4"))
        m = sd.indicator_by_year(self.cid, "PRCPTOT", "8_7_6_5_4", window="month")
        row = m[(m["Region"] == "Baringo") & (m["year"] == 2020)]
        self.assertAlmostEqual(float(row["value"].iloc[0]), cid_value("PRCPTOT", "Baringo", 2020, "8"))

    def test_each_region_reads_its_own_cumulative_chain(self):
        rows = []
        for year in (2024, 2025):
            for stage, v in (("8_7_6_5_4_3", 300.0), ("8_7_6_5_4", 250.0), ("8", 90.0)):
                rows.append({"Region": "Missouri", "year": year, "Stage": stage,
                             "Index": "PRCPTOT", "CID": v + year - 2024})
            for stage, v in (("8_7_6_5_4", 200.0), ("8_7_6_5", 150.0), ("8", 80.0)):
                rows.append({"Region": "Iowa", "year": year, "Stage": stage,
                             "Index": "PRCPTOT", "CID": v + year - 2024})
            rows.append({"Region": "South Dakota", "year": year, "Stage": "8_7_6_5",
                         "Index": "PRCPTOT", "CID": 120.0})
        cid = pd.DataFrame(rows)
        got = sd.indicator_by_year(cid, "PRCPTOT", "8_7_6_5_4_3").set_index(["Region", "year"])
        self.assertEqual(got.loc[("Missouri", 2025), "stage_used"], "8_7_6_5_4_3")
        self.assertEqual(got.loc[("Iowa", 2025), "stage_used"], "8_7_6_5_4")
        self.assertEqual(got.loc[("South Dakota", 2025), "stage_used"], "8_7_6_5")
        self.assertEqual(got.loc[("Iowa", 2025), "value"], 201.0)
        month = sd.indicator_by_year(cid, "PRCPTOT", "8_7_6_5_4_3", window="month")
        self.assertEqual(set(month["stage_used"]), {"8"})
        self.assertEqual(len(month), 4)                      # South Dakota has no "8" row

    def test_national_indicator_is_area_weighted(self):
        v = sd.indicator_by_year(self.cid, "PRCPTOT", "8_7_6_5_4")
        nat = sd.national_indicator(v, self.fc[["Region", "year", sd.AREA]], COUNTRY)
        a, b = area("Baringo", 2020), area("Bomet", 2020)
        va, vb = (cid_value("PRCPTOT", r, 2020, "8_7_6_5_4") for r in ("Baringo", "Bomet"))
        self.assertAlmostEqual(nat.loc[2020], (va * a + vb * b) / (a + b))
        self.assertIn(LIVE, nat.index)     # the live year uses the causal area fill

    def test_roles(self):
        sel = sd.selected_by_stage(self.db, f"{COUNTRY}_{CROP}", "tabpfn")
        cfg = sd.run_config(self.db, COUNTRY)
        cands = sd.candidate_families(cfg)
        self.assertTrue(cands["all"] and cands["cci"])
        ndvi = sd.INDICATOR_META["ndvi"]
        self.assertEqual(sd.resolve_role(ndvi, "Aug 1-Apr 30", sel, cands), ("input", True))
        self.assertEqual(sd.resolve_role(ndvi, "May 1-Apr 30", sel, cands), ("input", False))
        cci = sd.INDICATOR_META["cci"]
        self.assertEqual(sd.resolve_role(cci, "Aug 1-Apr 30", sel, cands), ("input", True))
        self.assertEqual(sd.resolve_role(cci, "Jul 1-Apr 30", sel, cands), ("input", False))
        no_cci = sd.candidate_families({"use_cids": "['NDVI', 'PRCPTOT']", "cci_file": ""})
        self.assertEqual(sd.resolve_role(cci, "Aug 1-Apr 30", sel, no_cci), ("independent", True))
        self.assertEqual(sd.resolve_role(sd.INDICATOR_META["heat"], "Aug 1-Apr 30", sel, no_cci),
                         ("input", True))          # SU was selected, so it is an input anyway
        self.assertEqual(sd.resolve_role(sd.INDICATOR_META["esi"], "Aug 1-Apr 30", sel, no_cci),
                         ("independent", False))
        self.assertEqual(sd.resolve_role(sd.INDICATOR_META["usda_yield"], "Aug 1-Apr 30", sel, cands),
                         ("independent", False))

    def test_build_tracks_end_to_end(self):
        cfg = sd.run_config(self.db, COUNTRY)
        sel = sd.selected_by_stage(self.db, f"{COUNTRY}_{CROP}", "tabpfn")
        metas = [sd.INDICATOR_META[k] for k in ("ndvi", "rain", "heat")]
        tracks, meta = sd.build_tracks(self.fc, self.cid, metas, country=COUNTRY, crop=CROP,
                                       target_year=LIVE, cfg=cfg, selected=sel)
        self.assertEqual(tracks["row"].nunique(), 4)
        self.assertEqual(set(tracks["role"]), {"target", "input"})
        yld = tracks[tracks["role"] == "target"].sort_values("issue_date")
        self.assertEqual(len(yld), len(STAGES))
        self.assertEqual(list(yld["issue_date"])[-1], date(2026, 9, 1))
        # the live path rises then falls: the first step is up, the last down
        self.assertGreater(yld["value_std"].iloc[1], yld["value_std"].iloc[0])
        self.assertLess(yld["value_std"].iloc[-1], yld["value_std"].iloc[-2])
        self.assertEqual(meta["baseline"], (2017, 2025))          # training_year_start floor
        self.assertEqual(yld["baseline_space"].iloc[0], "percent")
        heat = tracks[tracks["row"] == sd.INDICATOR_META["heat"].label]
        self.assertTrue(heat["invert"].all())
        self.assertTrue((heat["value_std"] < 0).all())            # hot 2026, flipped to unfavorable
        rain = tracks[tracks["row"] == sd.INDICATOR_META["rain"].label]
        self.assertTrue((rain["value_std"] > 0).all())            # wet 2026 reads favorable
        self.assertTrue((tracks["obs_date"] <= tracks["issue_date"]).all())
        self.assertIn("re-forecasts", meta["notes"][0])

    def test_more_than_four_indicators_raise(self):
        cfg = sd.run_config(self.db, COUNTRY)
        metas = [sd.INDICATOR_META[k] for k in ("ndvi", "ndvi_max", "rain", "heat", "kdd")]
        with self.assertRaises(ValueError):
            sd.build_tracks(self.fc, self.cid, metas, country=COUNTRY, crop=CROP,
                            target_year=LIVE, cfg=cfg)

    def test_region_scope(self):
        cfg = sd.run_config(self.db, COUNTRY)
        tracks, _ = sd.build_tracks(self.fc, self.cid, [sd.INDICATOR_META["rain"]],
                                    country=COUNTRY, crop=CROP, target_year=LIVE, cfg=cfg,
                                    region="Bomet")
        self.assertEqual(set(tracks["scope"]), {"Bomet"})
        yld = tracks[tracks["role"] == "target"].sort_values("issue_date")
        self.assertAlmostEqual(float(yld["value_tnha"].iloc[-1]), (2.0 + 0.04 * 11) * LIVE_PATH[-1])

    def test_region_key_and_dates_by_region(self):
        self.assertEqual(sd.region_key("Homa Bay"), sd.region_key("homa_bay"))
        self.assertEqual(sd.region_key("Elgeyo-Marakwet"), "elgeyo-marakwet")
        p = Path(self.tmp) / "daily.csv"
        pd.DataFrame({"datetime": ["2026-08-01", "2026-08-02", "2026-08-03"],
                      "region": ["baringo", "baringo", "bomet"],
                      "ndvi": [0.5, np.nan, 0.6]}).to_csv(p, index=False)
        by = sd.observed_dates_by_region(p, ["ndvi"], 2026)
        self.assertEqual(list(by["baringo"]["ndvi"]), [date(2026, 8, 1)])
        self.assertEqual(list(by["bomet"]["ndvi"]), [date(2026, 8, 3)])
        self.assertEqual(list(by["*"]["ndvi"]), [date(2026, 8, 1), date(2026, 8, 3)])

    def test_observed_dates_and_the_causality_guard(self):
        p = Path(self.tmp) / "kenya_maize_s1.csv"
        days = pd.date_range("2026-04-01", "2026-09-05", freq="D")
        rows = []
        for region in REGIONS:
            for d in days:
                rows.append({"datetime": d.strftime("%Y-%m-%d"), "region": region.lower(),
                             "ndvi": 0.5 if d <= pd.Timestamp("2026-08-20") else np.nan,
                             "chirps": 1.0,
                             "chirts_era5_tmax": 30.0 if d >= pd.Timestamp("2026-09-02") else np.nan})
        pd.DataFrame(rows).to_csv(p, index=False)
        obs = sd.observed_dates(p, ["ndvi", "chirps", "chirts_era5_tmax", "missing_var"], LIVE)
        self.assertEqual(set(obs), {"ndvi", "chirps", "chirts_era5_tmax"})
        self.assertEqual(sd.last_observed(obs["ndvi"], date(2026, 8, 31)), date(2026, 8, 20))
        self.assertEqual(sd.last_observed(obs["chirps"], date(2026, 8, 31)), date(2026, 8, 31))
        self.assertIsNone(sd.last_observed(obs["chirts_era5_tmax"], date(2026, 8, 31)))
        cfg = sd.run_config(self.db, COUNTRY)
        tracks, _ = sd.build_tracks(self.fc, self.cid, [sd.INDICATOR_META["ndvi"]],
                                    country=COUNTRY, crop=CROP, target_year=LIVE, cfg=cfg,
                                    obs_dates=obs)
        ndvi = tracks[tracks["row"] == "NDVI"].sort_values("issue_date")
        self.assertEqual(ndvi["obs_date"].iloc[-1], date(2026, 8, 20))
        self.assertEqual(ndvi["obs_date_kind"].iloc[-1], "observed")
        # a real observation date after the issue date must stop the figure:
        # the guard runs on the assembled table, whatever produced the date
        from unittest import mock

        with mock.patch.object(sd, "last_observed", return_value=date(2026, 9, 3)):
            with self.assertRaises(ValueError) as cm:
                sd.build_tracks(self.fc, self.cid, [sd.INDICATOR_META["ndvi"]], country=COUNTRY,
                                crop=CROP, target_year=LIVE, cfg=cfg, obs_dates=obs)
        self.assertIn("causality", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
