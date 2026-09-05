"""Tests for future-season (pre-season) forecasting — forecast_seasons may
name a season that has NOT started yet (e.g. south_africa maize 2027 launched
in Sep 2026, planting ~Nov 2026). Only S2S/FLDAS forecast CIDs + static
features exist for such a season.

Defects covered (all found planning the SA-2027 run):

1. ``indices_runner`` capped the CID year range at ``utcnow().year`` — a 2027
   CID file could never be generated in 2026.
2. ``process_task`` / ``_run_one_year`` returned early when the harvest-year
   frame was empty, so pre-season extraction never ran for a season with no
   in-season rows yet.
3. ``_extract_pre_season_features`` fell back to a year-less Month match when
   the target-year row was missing — silently substituting a STALE forecast
   (last year's same-month init) for the new season.
4. Raw forecast-lead values had no finite guard: NaN scaffold rows and the
   inf multi-model means from bad NOAA S2S files became features.
5. The ML CI gates used ``forecast_season == today_year`` — a future season
   is a LIVE forecast, not a hindcast, and must get confidence intervals.
6. ``read_data`` reused the cached combined statistics file even when newer
   per-year CID CSVs existed (the 2027 file would be silently ignored).
7. ``execute()`` dispatched a PS-only future season into the in-season paths,
   which fit models with an empty test set at every stage.
"""
import logging
import os
import tempfile
import time
import unittest
from pathlib import Path
from types import MethodType, SimpleNamespace

import numpy as np
import pandas as pd

_MISSING = object()


class FakeParser:
    """Minimal ConfigParser stand-in: dict of (section, option) -> str."""

    def __init__(self, opts):
        self.opts = dict(opts)

    def get(self, section, option, fallback=_MISSING):
        key = (section, option)
        if key in self.opts:
            return self.opts[key]
        if fallback is not _MISSING:
            return fallback
        raise KeyError(key)

    def getboolean(self, section, option, fallback=_MISSING):
        val = self.get(section, option, fallback=fallback)
        if isinstance(val, bool):
            return val
        return str(val).strip().lower() in ("1", "true", "yes", "on")

    def getint(self, section, option, fallback=_MISSING):
        return int(self.get(section, option, fallback=fallback))

    def has_option(self, section, option):
        return (section, option) in self.opts

    def has_section(self, section):
        return any(sec == section for sec, _ in self.opts)


def _sa_monthly_frame(tmp_s2s_values):
    """Monthly frame mimicking the preprocessed merged CSV for one SA region.

    South Africa maize calendar: plant Nov (cc=1), Dec-Feb cc=2, Mar-Apr cc=3,
    May cc=4 (dropped upstream in real data; kept out here), Jun-Oct cc=0.
    ``tmp_s2s_values``: {(year, month): lead1_value or None(=row absent) or
    "nan"/"inf"} — controls the s2s_tprate_lead1 value per init row.
    """
    cc_by_month = {11: 1, 12: 2, 1: 2, 2: 2, 3: 3, 4: 3,
                   6: 0, 7: 0, 8: 0, 9: 0, 10: 0}  # month 5 (cc=4) dropped
    rows = []
    for year in (2024, 2025, 2026):
        for month, cc in cc_by_month.items():
            key = (year, month)
            if tmp_s2s_values.get(key, "default") is None:
                continue  # row absent (e.g. forecast not issued yet)
            val = tmp_s2s_values.get(key, "default")
            if val == "default":
                val = year * 100.0 + month  # unique, identifiable
            elif val == "nan":
                val = np.nan
            elif val == "inf":
                val = np.inf
            # Season tag: in-season months belong to the harvest year
            season = year + 1 if month >= 11 else year
            row = {
                "adm0_name": "south_africa",
                "adm1_name": "free_state",
                "Month": month,
                "time": pd.Timestamp(year=year, month=month, day=15),
                "crop_cal": float(cc),
                "Season": season if cc in (1, 2, 3) else np.nan,
                "Area": 1000.0,
            }
            for lead in range(1, 7):
                row[f"s2s_tprate_lead{lead}"] = val
                row[f"s2s_t2m_lead{lead}"] = val
            rows.append(row)
    return pd.DataFrame(rows)


def _make_cids(tmpdir, df, harvest_year=2027, run_time_steps="pre_season"):
    from geocif.cid.indices import CIDs

    parser = FakeParser({
        ("DEFAULT", "project_name"): "testproj",
        ("PATHS", "dir_output"): str(tmpdir),
        ("ML", "run_time_steps"): run_time_steps,
        ("ML", "compute_forecast_aggregates"): "False",
        ("DEFAULT", "use_cids"): "['all']",
    })
    obj = CIDs(
        parser=parser,
        process_type="harvest",
        file_path=str(Path(tmpdir) / "south_africa_maize_s1.csv"),
        file_name="south_africa_maize_s1.csv",
        admin_zone="admin_1",
        method="monthly_r",
        harvest_year=harvest_year,
        redo=False,
    )
    obj.df_country_crop = df
    obj.show_progress = False
    return obj


class TestPreSeasonInitMonths(unittest.TestCase):
    def test_nov_planting_init_months(self):
        from geocif.utils import get_pre_season_init_months

        self.assertEqual(get_pre_season_init_months(11), [5, 6, 7, 8, 9, 10])

    def test_march_planting_wraps_year(self):
        from geocif.utils import get_pre_season_init_months

        self.assertEqual(get_pre_season_init_months(3), [9, 10, 11, 12, 1, 2])


class TestMaxForecastSeason(unittest.TestCase):
    def test_reads_max_across_countries(self):
        from geocif.indices_runner import get_max_forecast_season

        parser = FakeParser({
            ("south_africa", "forecast_seasons"): "[2025, 2026, 2027]",
            ("kenya", "forecast_seasons"): "[2026]",
        })
        self.assertEqual(
            get_max_forecast_season(parser, ["south_africa", "kenya"]), 2027
        )

    def test_missing_option_returns_zero(self):
        from geocif.indices_runner import get_max_forecast_season

        self.assertEqual(get_max_forecast_season(FakeParser({}), ["nowhere"]), 0)


class TestFutureSeasonExtraction(unittest.TestCase):
    """_extract_pre_season_features for harvest_year = current + 1."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def _extract(self, df, init_month, harvest_year=2027):
        obj = _make_cids(self.tmpdir, df, harvest_year=harvest_year)
        obj.crop, obj.season = "maize", 1
        obj.country = "south_africa"
        return obj._extract_pre_season_features(
            ("south_africa", "free_state"), init_month
        )

    def test_future_year_uses_prior_calendar_year(self):
        """PS rows for 2027 must come from calendar-2026 init rows."""
        df = _sa_monthly_frame({})
        out = self._extract(df, init_month=9)
        self.assertFalse(out.empty)
        self.assertTrue((out["Harvest Year"] == 2027).all())
        self.assertTrue((out["Stage"] == "PS_9").all())
        lead1 = out[out["Index"] == "MEAN_S2S_tprate_LEAD1"]
        self.assertEqual(len(lead1), 1)
        # 2026*100 + 9: the Sep-2026 value, NOT Sep-2025's 202509
        self.assertAlmostEqual(float(lead1["CID"].iloc[0]), 202609.0)

    def test_missing_init_month_is_skipped_not_stale(self):
        """Oct-2026 forecast not issued yet: must return empty, never the
        Oct-2025 row (the old year-less fallback did exactly that)."""
        df = _sa_monthly_frame({(2026, 10): None})  # drop Oct 2026 row
        out = self._extract(df, init_month=10)
        self.assertTrue(
            out.empty,
            f"stale fallback resurfaced: got values {out['CID'].unique() if not out.empty else ''}",
        )

    def test_nan_rows_produce_no_features(self):
        """Scaffold rows exist but forecast columns are NaN → no PS rows."""
        df = _sa_monthly_frame({(2026, 7): "nan"})
        out = self._extract(df, init_month=7)
        self.assertTrue(out.empty)

    def test_inf_values_are_dropped(self):
        """inf multi-model means (bad NOAA S2S files) never become features."""
        df = _sa_monthly_frame({(2026, 6): "inf"})
        out = self._extract(df, init_month=6)
        self.assertTrue(out.empty)
        # ...and a finite month is unaffected
        out9 = self._extract(df, init_month=9)
        self.assertFalse(out9.empty)
        self.assertTrue(np.isfinite(out9["CID"]).all())

    def test_historical_year_still_works(self):
        """Regression: hindcast years keep producing PS rows as before."""
        df = _sa_monthly_frame({})
        out = self._extract(df, init_month=8, harvest_year=2026)
        self.assertFalse(out.empty)
        lead1 = out[out["Index"] == "MEAN_S2S_tprate_LEAD1"]
        self.assertAlmostEqual(float(lead1["CID"].iloc[0]), 202508.0)


class TestRunOneYearFutureSeason(unittest.TestCase):
    """_run_one_year end-to-end for a season with NO in-season rows yet."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def test_future_season_writes_ps_only_csv(self):
        from geocif.cid import indices

        df = _sa_monthly_frame({(2026, 10): None})  # Oct init not issued yet
        # Make the frame LOOK future: drop in-season rows dated after "today"
        # is unnecessary — filter_data_for_harvest_year drops crop_cal=0 and
        # future dates; harvest 2027 in-season rows (Nov 2026+) are absent
        # from this frame entirely, mimicking Sep-2026 reality.
        df = df[~((df["Season"] == 2027) & df["crop_cal"].isin([1.0, 2.0, 3.0]))]

        obj = _make_cids(self.tmpdir, df, harvest_year=2027)
        self.assertTrue(obj.pre_season_mode)
        self.assertTrue(obj.filter_data_for_harvest_year().empty)

        indices._run_one_year(obj)

        out_path = obj._output_path()
        self.assertTrue(
            out_path.exists(),
            "future season produced no CID file — pre-season bypass broken",
        )
        out = pd.read_csv(out_path)
        self.assertTrue((out["Harvest Year"] == 2027).all())
        self.assertTrue(out["Stage"].str.startswith("PS_").all())
        # init months present: Jun-Sep 2026 (May is cc=4/absent, Oct missing)
        got_months = sorted(
            int(s.split("_")[1]) for s in out["Stage"].unique()
        )
        self.assertEqual(got_months, [6, 7, 8, 9])
        self.assertTrue(np.isfinite(out["CID"]).all())

    def test_non_preseason_future_season_still_skips(self):
        from geocif.cid import indices

        df = _sa_monthly_frame({})
        df = df[~((df["Season"] == 2027) & df["crop_cal"].isin([1.0, 2.0, 3.0]))]
        obj = _make_cids(self.tmpdir, df, harvest_year=2027,
                         run_time_steps="latest")
        self.assertFalse(obj.pre_season_mode)
        indices._run_one_year(obj)
        # prepare_directories never ran; no output must exist anywhere
        out_root = Path(self.tmpdir) / "testproj"
        csvs = list(out_root.rglob("*2027*.csv")) if out_root.exists() else []
        self.assertEqual(csvs, [])


class TestExecuteGuardPsOnlySeason(unittest.TestCase):
    """execute() must not send a PS-only future season down in-season paths."""

    def _ns(self, df_inputs, run_time_steps="all", forecast_season=2027):
        from geocif.geocif import Geocif

        called = {"pre": 0, "single": 0, "multi": 0}
        ns = SimpleNamespace(
            is_pre_season=False,
            run_time_steps=run_time_steps,
            df_inputs=df_inputs,
            forecast_season=forecast_season,
            country="south_africa",
            crop="maize",
            logger=logging.getLogger("test"),
            _is_forecast_only=lambda: False,
            _execute_pre_season=lambda include_in_season=False: called.__setitem__("pre", called["pre"] + 1),
            _execute_single_pass=lambda: called.__setitem__("single", called["single"] + 1),
            _execute_multi_step=lambda: called.__setitem__("multi", called["multi"] + 1),
        )
        ns.execute = MethodType(Geocif.execute, ns)
        return ns, called

    def test_ps_only_season_returns_early(self):
        df = pd.DataFrame({
            "Harvest Year": [2026, 2026, 2027, 2027],
            "Stage_ID": ["9_8_7", "9_8", "PS_9", "PS_8"],
        })
        ns, called = self._ns(df)
        ns.execute()
        self.assertEqual(called, {"pre": 0, "single": 0, "multi": 0})

    def test_normal_season_dispatches(self):
        df = pd.DataFrame({
            "Harvest Year": [2026, 2026],
            "Stage_ID": ["9_8_7", "9_8"],
        })
        ns, called = self._ns(df, forecast_season=2026)
        ns.execute()
        self.assertEqual(called["multi"], 1)

    def test_mixed_stage_forecast_season_dispatches(self):
        """A started season (PS + real stages) is NOT blocked."""
        df = pd.DataFrame({
            "Harvest Year": [2027, 2027],
            "Stage_ID": ["PS_9", "12_11"],
        })
        ns, called = self._ns(df)
        ns.execute()
        self.assertEqual(called["multi"], 1)


class TestCiGateFutureSeason(unittest.TestCase):
    """Future forecast season = live forecast → CIs must be estimated."""

    def test_add_ci_wraps_model_for_future_season(self):
        import geocif.geocif as gc_mod

        sentinel = object()
        obj = SimpleNamespace(
            estimate_ci=True,
            estimate_ci_for_all=False,
            forecast_season=2027,
            today_year=2026,
            model_type="REGRESSION",
            model_name="catboost",
            model=sentinel,
            alpha=0.1,
            ci_method="crepes",
        )
        ns = SimpleNamespace(obj=obj)
        ns._add_confidence_intervals_if_needed = MethodType(
            gc_mod.ModelTrainer._add_confidence_intervals_if_needed, ns
        )
        orig = gc_mod.trainers.estimate_ci
        gc_mod.trainers.estimate_ci = lambda *a, **k: "WRAPPED"
        try:
            ns._add_confidence_intervals_if_needed()
        finally:
            gc_mod.trainers.estimate_ci = orig
        self.assertEqual(obj.model, "WRAPPED")

    def test_hindcast_season_still_skips_ci(self):
        import geocif.geocif as gc_mod

        sentinel = object()
        obj = SimpleNamespace(
            estimate_ci=True,
            estimate_ci_for_all=False,
            forecast_season=2020,
            today_year=2026,
            model=sentinel,
        )
        ns = SimpleNamespace(obj=obj)
        ns._add_confidence_intervals_if_needed = MethodType(
            gc_mod.ModelTrainer._add_confidence_intervals_if_needed, ns
        )
        ns._add_confidence_intervals_if_needed()
        self.assertIs(obj.model, sentinel)


class TestStatisticsFileStaleness(unittest.TestCase):
    def _ns(self, tmpdir):
        from geocif.geocif import Geocif

        parser = FakeParser({
            ("south_africa", "admin_level"): "admin_1",
            ("south_africa", "seasons"): "[1]",
        })
        ns = SimpleNamespace(
            parser=parser,
            dir_output=Path(tmpdir),
            method="monthly_r",
            logger=logging.getLogger("test"),
        )
        ns._statistics_file_stale = MethodType(Geocif._statistics_file_stale, ns)
        return ns

    def test_newer_cid_file_marks_stale(self):
        tmpdir = tempfile.mkdtemp()
        ns = self._ns(tmpdir)
        cid_dir = (Path(tmpdir) / "cid" / "indices" / "monthly_r" / "admin_1"
                   / "south_africa" / "maize")
        cid_dir.mkdir(parents=True)
        stats = Path(tmpdir) / "stats.csv"
        stats.write_text("x")
        old = time.time() - 3600
        os.utime(stats, (old, old))
        cid_file = cid_dir / "south_africa_maize_s1_2027.csv"
        cid_file.write_text("y")
        self.assertTrue(ns._statistics_file_stale("south_africa", "maize", stats))

    def test_older_cid_files_not_stale(self):
        tmpdir = tempfile.mkdtemp()
        ns = self._ns(tmpdir)
        cid_dir = (Path(tmpdir) / "cid" / "indices" / "monthly_r" / "admin_1"
                   / "south_africa" / "maize")
        cid_dir.mkdir(parents=True)
        cid_file = cid_dir / "south_africa_maize_s1_2026.csv"
        cid_file.write_text("y")
        old = time.time() - 3600
        os.utime(cid_file, (old, old))
        stats = Path(tmpdir) / "stats.csv"
        stats.write_text("x")
        self.assertFalse(ns._statistics_file_stale("south_africa", "maize", stats))


def _monthly_frame(cc_by_month, in_season_months, years=(2024, 2025, 2026),
                   overrides=None, wrap=False):
    """Generic monthly frame builder (see _sa_monthly_frame for SA specifics).

    ``overrides``: {(year, month): value | None(absent) | "nan" | "inf"}.
    ``wrap``: in-season months >= 11 belong to harvest year ``year + 1``.
    """
    overrides = overrides or {}
    rows = []
    for year in years:
        for month, cc in cc_by_month.items():
            val = overrides.get((year, month), "default")
            if val is None:
                continue
            if val == "default":
                val = year * 100.0 + month
            elif val == "nan":
                val = np.nan
            elif val == "inf":
                val = np.inf
            in_season = month in in_season_months
            season = (year + 1 if (wrap and month >= 11) else year) if in_season else np.nan
            row = {
                "adm0_name": "testland",
                "adm1_name": "region_a",
                "Month": month,
                "time": pd.Timestamp(year=year, month=month, day=15),
                "crop_cal": float(cc),
                "Season": season,
                "Area": 1000.0,
            }
            for lead in range(1, 7):
                row[f"s2s_tprate_lead{lead}"] = val
                row[f"s2s_t2m_lead{lead}"] = val
            rows.append(row)
    return pd.DataFrame(rows)


class TestWithinYearLatePlantingAnchor(unittest.TestCase):
    """[prior bug] The month->year walk seeded harvest_year-1 flatly, mapping
    EVERY pre-season month one year early for within-year seasons planted
    Jul-Dec. The walk is now anchored to the season's true start date."""

    def _extract(self, df, init_month, harvest_year, aggregates=False):
        from geocif.cid.indices import CIDs

        tmpdir = tempfile.mkdtemp()
        parser = FakeParser({
            ("DEFAULT", "project_name"): "testproj",
            ("PATHS", "dir_output"): tmpdir,
            ("ML", "run_time_steps"): "pre_season",
            ("ML", "compute_forecast_aggregates"): str(aggregates),
            ("DEFAULT", "use_cids"): "['all']",
        })
        obj = CIDs(
            parser=parser, process_type="harvest",
            file_path=str(Path(tmpdir) / "testland_maize_s1.csv"),
            file_name="testland_maize_s1.csv", admin_zone="admin_1",
            method="monthly_r", harvest_year=harvest_year, redo=False,
        )
        obj.df_country_crop = df
        obj.show_progress = False
        obj.crop, obj.season = "maize", 1
        obj.country = "testland"
        return obj._extract_pre_season_features(("testland", "region_a"), init_month)

    def test_sep_planting_pre_months_use_harvest_year(self):
        # Planting Sep, harvest Dec (within-year). Pre months [3..8] are in
        # the HARVEST year itself, not harvest_year - 1.
        cc = {9: 1, 10: 2, 11: 2, 12: 3, 1: 0, 2: 0, 3: 0, 4: 0,
              5: 0, 6: 0, 7: 0, 8: 0}
        df = _monthly_frame(cc, in_season_months={9, 10, 11, 12})
        out = self._extract(df, init_month=5, harvest_year=2026)
        self.assertFalse(out.empty)
        lead1 = out[out["Index"] == "MEAN_S2S_tprate_LEAD1"]
        # May of 2026 (202605), NOT May 2025 (202505 = the old off-by-one)
        self.assertAlmostEqual(float(lead1["CID"].iloc[0]), 202605.0)

    def test_wrap_season_anchor_unchanged(self):
        # SA-style wrap: planting Nov, harvest Apr. Pre months stay in
        # harvest_year - 1 exactly as before.
        cc = {11: 1, 12: 2, 1: 2, 2: 2, 3: 3, 4: 3,
              6: 0, 7: 0, 8: 0, 9: 0, 10: 0}
        df = _monthly_frame(cc, in_season_months={11, 12, 1, 2, 3, 4}, wrap=True)
        out = self._extract(df, init_month=8, harvest_year=2026)
        lead1 = out[out["Index"] == "MEAN_S2S_tprate_LEAD1"]
        self.assertAlmostEqual(float(lead1["CID"].iloc[0]), 202508.0)

    def test_prev_init_revision_row_year(self):
        # Planting Jul: pre months [1..6]. For init Jan, the previous init is
        # December of the PRIOR year. The old fallback fetched December of
        # the SAME year -- 11 months in the future.
        cc = {7: 1, 8: 2, 9: 2, 10: 3, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0,
              11: 0, 12: 0}
        overrides = {
            (2026, 1): 100.0,   # current init row (Jan 2026)
            (2025, 12): 90.0,   # correct prev row (Dec 2025)
            (2026, 12): 999.0,  # poison: the old wrong-year prev row
        }
        df = _monthly_frame(cc, in_season_months={7, 8, 9, 10},
                            overrides=overrides)
        out = self._extract(df, init_month=1, harvest_year=2026,
                            aggregates=True)
        rev = out[out["Index"] == "REV_S2S_tprate"]
        self.assertEqual(len(rev), 1)
        # |100 - 90| averaged over the lead pairs = 10; the poison row would
        # have produced 899.
        self.assertAlmostEqual(float(rev["CID"].iloc[0]), 10.0, places=4)


class TestReadDataPooledStaleness(unittest.TestCase):
    def test_pooled_rebuilds_when_stale(self):
        from geocif.geocif import Geocif

        calls = []
        df_stub = pd.DataFrame({
            "Country": ["A"], "Region": ["r"], "Harvest Year": [2026],
        })

        ns = SimpleNamespace(
            logger=logging.getLogger("test"),
            update_input_file=False,
            rename_target=False,
            fixed_columns=[],
            df_inputs=None,
        )
        ns._get_statistics_file_path = lambda c, cr: Path(tempfile.mkdtemp()) / "x.csv"
        ns._statistics_file_stale = lambda c, cr, p: True
        def _create(c, cr, p):
            calls.append(c)
            ns.df_inputs = df_stub.copy()
        ns._create_statistics_file = _create
        ns._apply_training_year_filter = lambda: None
        ns.read_data_pooled = MethodType(Geocif.read_data_pooled, ns)

        ns.read_data_pooled(["a_land"], "maize", 2027)
        self.assertEqual(calls, ["a_land"],
                         "stale stats file was not rebuilt in pooled mode")


if __name__ == "__main__":
    unittest.main()
