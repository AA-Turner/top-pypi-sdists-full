"""Tests for the shift maps (viz/shift_map.py) and the S2S replay they need.

What must hold: the direction convention (brown/right is always the worse
outcome, for both metrics), the election-map consistency rule, chronological
issue order from parsed dates rather than labels, one arrow per region, and
the as_of_init replay choosing each combination's own offset.
"""
import sqlite3
import tempfile
import unittest
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

from geocif.viz import shift_map as sm


def _series(values, issues=None, **cols):
    """A one-region series with the given values, in the order given."""
    issues = issues or [f"2026-{8 + i:02d}" for i in range(len(values))]
    base = {"region_id": "ZW1", "region": "Harare", "country": "Zimbabwe",
            "crop": "maize", "season": "Main", "year": 2027, "skill": True}
    base.update(cols)
    return pd.DataFrame([{**base, "issue": iss, "issue_order": i,
                          "value": v}
                         for i, (iss, v) in enumerate(zip(issues, values))])


class TestDirectionConvention(unittest.TestCase):
    def test_a_rise_in_p_low_and_a_fall_in_yield_both_point_worse(self):
        up = sm.compute_shifts(_series([40.0, 50.0]), sm.P_LOW)
        self.assertGreater(up["signed"].iloc[0], 0)
        down = sm.compute_shifts(_series([2.0, 1.5]), sm.YIELD_MGHA)
        self.assertGreater(down["signed"].iloc[0], 0)
        self.assertLess(down["delta"].iloc[0], 0)
        better = sm.compute_shifts(_series([50.0, 40.0]), sm.P_LOW)
        self.assertLess(better["signed"].iloc[0], 0)

    def test_angles_and_lengths(self):
        angle, length = sm.arrow_geometry([12.0, -12.0, 0.5, 80.0], sm.P_LOW)
        self.assertEqual(list(angle), [sm.TILT, 180 - sm.TILT, sm.TILT,
                                       sm.TILT])
        self.assertAlmostEqual(length[0], 1.2)         # 10 pp per cm
        self.assertAlmostEqual(length[1], 1.2)
        self.assertEqual(length[2], sm.MIN_CM)         # floor
        self.assertEqual(length[3], sm.P_LOW.max_cm)   # cap

    def test_colours_are_the_fews_ramp_ends(self):
        from geocif.viz.s2s_africa import FEWS_CPT

        self.assertEqual(sm.WORSE, FEWS_CPT[-1][1])
        self.assertEqual(sm.BETTER, FEWS_CPT[0][1])
        self.assertNotEqual(sm.WORSE, sm.BETTER)


class TestConsistencyRule(unittest.TestCase):
    def test_same_direction_every_step_is_drawn(self):
        s = sm.compute_shifts(_series([40.0, 45.0, 50.0]), sm.P_LOW)
        self.assertTrue(s["consistent"].iloc[0])
        self.assertTrue(s["drawn"].iloc[0])
        self.assertEqual(s["path"].iloc[0], "40 > 45 > 50")

    def test_a_reversal_is_listed_not_drawn_unless_all(self):
        series = _series([40.0, 50.0, 45.0])
        s = sm.compute_shifts(series, sm.P_LOW)
        self.assertFalse(s["consistent"].iloc[0])
        self.assertFalse(s["drawn"].iloc[0])
        self.assertIn("direction changed", s["reason"].iloc[0])
        s_all = sm.compute_shifts(series, sm.P_LOW, select="all")
        self.assertTrue(s_all["drawn"].iloc[0])
        self.assertAlmostEqual(s_all["delta"].iloc[0], 5.0)

    def test_a_flat_step_is_not_a_shift(self):
        s = sm.compute_shifts(_series([40.0, 40.0, 50.0]), sm.P_LOW)
        self.assertFalse(s["consistent"].iloc[0])
        self.assertIn("neither way", s["reason"].iloc[0])

    def test_small_net_change_is_not_drawn(self):
        s = sm.compute_shifts(_series([40.0, 41.0]), sm.P_LOW)
        self.assertFalse(s["drawn"].iloc[0])
        self.assertIn("below", s["reason"].iloc[0])

    def test_single_issue_has_no_shift(self):
        self.assertTrue(sm.compute_shifts(_series([40.0]), sm.P_LOW).empty)

    def test_unknown_select_is_refused(self):
        with self.assertRaises(ValueError):
            sm.compute_shifts(_series([1.0, 2.0]), sm.P_LOW, select="some")

    def test_order_comes_from_issue_order_not_labels(self):
        """Labels listed out of order, issue_order in order."""
        s = _series([50.0, 40.0], issues=["2026-10", "2026-09"])
        s["issue_order"] = [2, 1]
        out = sm.compute_shifts(s, sm.P_LOW)
        self.assertEqual(out["first_issue"].iloc[0], "2026-09")
        self.assertAlmostEqual(out["delta"].iloc[0], 10.0)


class TestOnePerRegion(unittest.TestCase):
    def test_larger_move_wins_and_drawn_beats_undrawn(self):
        a = sm.compute_shifts(_series([40.0, 45.0], season="Main"), sm.P_LOW)
        b = sm.compute_shifts(_series([40.0, 52.0], season="Short"), sm.P_LOW)
        c = sm.compute_shifts(_series([40.0, 41.0], season="Flat"), sm.P_LOW)
        out = sm.one_per_region(pd.concat([a, b, c]))
        self.assertEqual(len(out), 1)
        self.assertEqual(out["season"].iloc[0], "Short")
        only_flat = sm.one_per_region(pd.concat([c, a]))
        self.assertEqual(only_flat["season"].iloc[0], "Main")


def _run_dir(root, init, rows):
    d = Path(root) / f"run_{init}"
    d.mkdir()
    pd.DataFrame([{"country": "Zimbabwe", "crop": "maize",
                   "season_name": "Main", "harvest_year": 2027,
                   "init_used": init, **r} for r in rows]).to_csv(
        d / "forecasts.csv", index=False)
    return d


class TestS2sSeries(unittest.TestCase):
    def test_values_units_order_and_skill(self):
        with tempfile.TemporaryDirectory() as td:
            runs = [
                _run_dir(td, "2026-10", [{"fnid": "ZW1", "P_low": 0.6,
                                          "ahat": -0.4,
                                          "region_skill": "skill"}]),
                _run_dir(td, "2026-09", [{"fnid": "ZW1", "P_low": 0.5,
                                          "ahat": -0.3,
                                          "region_skill": "no_skill"}]),
            ]
            s = sm.s2s_series(runs, sm.P_LOW)
            out = sm.compute_shifts(s, sm.P_LOW)
            pct = sm.compute_shifts(sm.s2s_series(runs, sm.YIELD_PCT),
                                    sm.YIELD_PCT)
        self.assertEqual(out["first_issue"].iloc[0], "2026-09")   # by date
        self.assertAlmostEqual(out["first"].iloc[0], 50.0)       # in pp
        self.assertAlmostEqual(out["delta"].iloc[0], 10.0)
        self.assertEqual(bool(out["skill"].iloc[0]), True)       # latest issue
        self.assertAlmostEqual(pct["delta"].iloc[0], -10.0)
        self.assertGreater(pct["signed"].iloc[0], 0)

    def test_run_without_init_used_is_refused(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td) / "old"
            d.mkdir()
            pd.DataFrame([{"country": "Zimbabwe", "crop": "maize",
                           "season_name": "Main", "harvest_year": 2027,
                           "fnid": "ZW1", "P_low": 0.5}]).to_csv(
                d / "forecasts.csv", index=False)
            with self.assertRaises(ValueError) as cm:
                sm.s2s_series([d], sm.P_LOW)
        self.assertIn("init_used", str(cm.exception))

    def test_duplicate_issue_keeps_the_later_listed_run(self):
        with tempfile.TemporaryDirectory() as td:
            runs = [_run_dir(td, "2026-09", [{"fnid": "ZW1", "P_low": 0.5}]),
                    Path(td) / "again"]
            runs[1].mkdir()
            pd.read_csv(runs[0] / "forecasts.csv").assign(P_low=0.7).to_csv(
                runs[1] / "forecasts.csv", index=False)
            with self.assertLogs(sm.logger, "WARNING"):
                s = sm.s2s_series(runs, sm.P_LOW)
        self.assertEqual(len(s), 1)
        self.assertAlmostEqual(s["value"].iloc[0], 70.0)


def _db(path, rows, table="kenya_maize"):
    cols = ["Experiment Name", "Model", "Country", "Crop", "Region",
            "Harvest Year", "Stage Name", "Stage Window Display",
            "Predicted Yield (tn per ha)", "Observed Yield (tn per ha)",
            "Date", "Time"]
    con = sqlite3.connect(path)
    con.execute(f'CREATE TABLE "{table}" ({", ".join(chr(34) + c + chr(34) for c in cols)})')
    con.executemany(f'INSERT INTO "{table}" VALUES ({", ".join("?" * len(cols))})',
                    [[r.get(c) for c in cols] for r in rows])
    con.commit()
    con.close()


class TestOutlookSeries(unittest.TestCase):
    #: as-of months 4, 5, 6; the window labels sort Apr < Jun < May
    #: alphabetically, so label order would put June before May
    STAGES = [("Apr 1-Apr 30", "Apr 1-Apr 30"), ("May 1-Apr 30", "Apr 1-May 31"),
              ("Jun 1-Apr 30", "Apr 1-Jun 30")]

    def _rows(self, model="trend", year=2026, values=(2.0, 2.5, 3.0)):
        return [{"Experiment Name": "outlook", "Model": model,
                 "Country": "kenya", "Crop": "maize", "Region": "Nakuru",
                 "Harvest Year": year, "Stage Name": st,
                 "Stage Window Display": swd,
                 "Predicted Yield (tn per ha)": v,
                 "Observed Yield (tn per ha)": None,
                 "Date": "September_17_2026", "Time": "September-17-2026 11:31:05"}
                for (st, swd), v in zip(self.STAGES, values)]

    def test_stages_in_as_of_order_and_mgha_values(self):
        with tempfile.TemporaryDirectory() as td:
            db = Path(td) / "o.db"
            _db(db, self._rows())
            s = sm.outlook_series(db, "kenya_maize")
            out = sm.compute_shifts(s, sm.YIELD_MGHA)
        self.assertEqual(s["region_id"].iloc[0], "kenya nakuru")
        self.assertEqual(out["first_issue"].iloc[0], "Apr 1-Apr 30")
        self.assertEqual(out["last_issue"].iloc[0], "Apr 1-Jun 30")
        self.assertTrue(out["consistent"].iloc[0])          # 2.0 > 2.5 > 3.0
        self.assertAlmostEqual(out["delta"].iloc[0], 1.0)
        self.assertLess(out["signed"].iloc[0], 0)            # higher = better
        self.assertTrue(pd.isna(out["skill"].iloc[0]))

    def test_two_models_need_a_choice(self):
        with tempfile.TemporaryDirectory() as td:
            db = Path(td) / "o.db"
            _db(db, self._rows("trend") + self._rows("cubist"))
            with self.assertRaises(ValueError):
                sm.outlook_series(db, "kenya_maize")
            s = sm.outlook_series(db, "kenya_maize", model="cubist")
        self.assertEqual(len(s), 3)

    def test_latest_year_by_default(self):
        with tempfile.TemporaryDirectory() as td:
            db = Path(td) / "o.db"
            _db(db, self._rows(year=2025) + self._rows(year=2026))
            s = sm.outlook_series(db, "kenya_maize")
            s25 = sm.outlook_series(db, "kenya_maize", year=2025)
        self.assertEqual(set(s["year"]), {2026})
        self.assertEqual(set(s25["year"]), {2025})

    def test_only_mgha_from_the_db(self):
        with self.assertRaises(ValueError):
            sm.outlook_series("x.db", "kenya_maize", metric=sm.P_LOW)

    def test_pooled_table_keys_each_row_by_its_own_country(self):
        """A pooled run writes Title Case countries; the key normalises
        them and every row keeps its own country."""
        rows = self._rows()
        for r in rows:
            r["Country"] = "South Africa"
        rows += [dict(r, Country="kenya", Region="Nakuru") for r in self._rows()]
        with tempfile.TemporaryDirectory() as td:
            db = Path(td) / "o.db"
            _db(db, rows, table="pooled_maize")
            s = sm.outlook_series(db, "pooled_maize")
        self.assertEqual(set(s["region_id"]),
                         {"south africa nakuru", "kenya nakuru"})
        self.assertEqual(set(s["country"]), {"South Africa", "kenya"})

    def test_missing_year_is_named(self):
        with tempfile.TemporaryDirectory() as td:
            db = Path(td) / "o.db"
            _db(db, self._rows())
            with self.assertRaises(ValueError) as cm:
                sm.outlook_series(db, "kenya_maize", year=2019)
        self.assertIn("2019", str(cm.exception))


class TestLegendAndText(unittest.TestCase):
    def test_legend_names_both_directions_and_the_scale(self):
        rows = sm.legend_rows(sm.P_LOW, faded=True)
        self.assertEqual(len(rows), 5)
        self.assertIn(sm.WORSE, rows[0])
        # the symbol code must carry the head size: `v+e` draws nothing
        self.assertIn(f"v{sm.HEAD}+e", rows[0])
        self.assertIn(sm.BETTER, rows[1])
        self.assertIn(f"v{sm.HEAD}+b", rows[1])       # head at the start
        self.assertTrue(sm.STYLE.startswith(f"v{sm.HEAD}+e"))
        self.assertIn(sm.FADE, rows[2])
        # the region outline: a hollow square in the outline pen, its text
        # aligned with the arrow rows
        self.assertIn(f"s 0.32c - {sm.OUTLINE_PEN} 1.5c Forecast region",
                      rows[3])
        self.assertIn("1 cm of arrow = 10 pp", rows[4])
        self.assertIn("25 pp", rows[4])
        self.assertEqual(len(sm.legend_rows(sm.YIELD_MGHA, faded=False)), 4)
        self.assertIn("0.5 Mg/ha", sm.legend_rows(sm.YIELD_MGHA, False)[-1])

    def test_subtitle_states_span_and_rule(self):
        t = sm.subtitle_text("init", ["Aug 2026", "Sep 2026", "Oct 2026"],
                             "consistent")
        self.assertIn("Inits Aug 2026 to Oct 2026", t)
        self.assertIn("same way", t)
        self.assertLess(len(t), 80)                  # one unwrapped line
        self.assertIn("net change",
                      sm.subtitle_text("init", ["Aug 2026", "Sep 2026",
                                                "Oct 2026"], "all"))
        # a pair has one step: no rule to state
        two = sm.subtitle_text("issue", ["Aug 2026", "Sep 2026"], "consistent")
        self.assertEqual(two, "Issues Aug 2026 to Sep 2026; change between "
                              "the two")

    def test_spans_are_the_full_span_then_each_consecutive_pair(self):
        s = pd.concat([_series([40.0, 45.0, 50.0], region_id="A"),
                       _series([30.0, 20.0], issues=["2026-09", "2026-10"],
                               region_id="B").assign(issue_order=[1, 2])])
        got = list(sm.spans(s))
        self.assertEqual([i for i, _ in got],
                         [["2026-08", "2026-09", "2026-10"],
                          ["2026-08", "2026-09"], ["2026-09", "2026-10"]])
        # B has no Aug issue: it shifts in the second pair only
        first = sm.compute_shifts(got[1][1], sm.P_LOW)
        second = sm.compute_shifts(got[2][1], sm.P_LOW)
        self.assertEqual(set(first["region_id"]), {"A"})
        self.assertEqual(set(second["region_id"]), {"A", "B"})
        self.assertAlmostEqual(
            second.set_index("region_id").loc["B", "delta"], -10.0)
        # a two-issue series is its own only pair; pairs=False: span only
        self.assertEqual(len(list(sm.spans(_series([1.0, 2.0])))), 1)
        self.assertEqual(len(list(sm.spans(s, pairs=False))), 1)

    def test_month_label(self):
        self.assertEqual(sm.month_label("2026-08"), "Aug 2026")
        self.assertEqual(sm.month_label("Apr 1-Apr 30"), "Apr 1-Apr 30")


class TestSharedHelpers(unittest.TestCase):
    def test_country_region_key_scalar_and_series(self):
        from geocif.utils import country_region_key

        self.assertEqual(country_region_key("south_africa", "Free State"),
                         "south africa free state")
        s = country_region_key(pd.Series(["south_africa"]),
                               pd.Series(["Free State"]))
        self.assertEqual(s.iloc[0], "south africa free state")
        self.assertEqual(country_region_key("kenya", pd.Series(["Nakuru"]))
                         .iloc[0], "kenya nakuru")

    def test_no_skill_mask_prefers_the_region_verdict(self):
        from geocif.viz.s2s_africa import no_skill_mask

        f = pd.DataFrame({"region_skill": ["skill", "no_skill", "insufficient"],
                          "has_skill": [False, False, False]})
        self.assertEqual(list(no_skill_mask(f)), [False, True, False])
        g = pd.DataFrame({"has_skill": [True, False]})
        self.assertEqual(list(no_skill_mask(g)), [False, True])
        self.assertEqual(list(no_skill_mask(pd.DataFrame({"x": [1]}))),
                         [False])


class TestOutputFolders(unittest.TestCase):
    """One dated folder per job, and outlook maps beside their outlook."""

    def test_analysis_dir_takes_a_shared_stamp(self):
        from geocif.experiments.s2s_africa import analysis_dir

        root = Path("/o/geocif")
        a = analysis_dir(root, "s2s_africa_x_asof202608", "October_14_2026_16h50")
        b = analysis_dir(root, "s2s_shift_x", "October_14_2026_16h50")
        self.assertEqual(a.parent, b.parent)
        self.assertEqual(a, root / "ml" / "analysis" / "October_14_2026_16h50"
                         / "explore" / "s2s_africa_x_asof202608")

    def test_replays_and_maps_share_the_job_stamp(self):
        import inspect

        src = inspect.getsource(sm.s2s_run)
        self.assertIn("stamp = run_stamp()", src)
        self.assertIn("replay_s2s(parser, inits, stamp=stamp", src)
        self.assertIn("analysis_dir(root, name, stamp)", src)
        self.assertIn("Path(runs[-1]).parent / name", src)
        self.assertIn("stamp=stamp", inspect.getsource(sm.replay_s2s))

    def test_outlook_run_dir_from_the_db_name(self):
        root = Path("/o/geocif")
        self.assertEqual(sm.outlook_run_dir(root, "outlook_09_17_2026_14h18.db"),
                         root / "ml" / "analysis" / "September_17_2026_14h18")
        self.assertEqual(
            sm.outlook_run_dir(root, Path("/x/db/outlook_01_05_2027_09h03.db")),
            root / "ml" / "analysis" / "January_05_2027_09h03")
        self.assertIsNone(sm.outlook_run_dir(root, "zambia_tabpfn.db"))


class TestAsOfInitReplay(unittest.TestCase):
    def test_parse_init(self):
        from geocif.experiments.s2s_africa import parse_init

        self.assertEqual(parse_init("2026-08"), (2026, 8))
        for bad in ("2026-13", "202608", "Aug 2026"):
            with self.assertRaises(ValueError):
                parse_init(bad)

    def test_offset_is_the_inverse_of_init_calendar(self):
        from geocif.experiments.s2s_africa import offset_for_init
        from geocif.experiments.s2s_pooled_model import init_calendar

        # Nov planting, wraps, harvest 2027: Aug 2026 is 3 months before
        self.assertEqual(offset_for_init(11, True, 2027, 2026, 8), 3)
        self.assertEqual(offset_for_init(11, True, 2027, 2026, 10), 1)
        self.assertEqual(offset_for_init(11, True, 2027, 2027, 1), -2)
        # Mar planting, no wrap: Dec 2026 is 3 before, May 2027 is 2 after
        self.assertEqual(offset_for_init(3, False, 2027, 2026, 12), 3)
        self.assertEqual(offset_for_init(3, False, 2027, 2027, 5), -2)
        for planting, wraps, hy, off in ((11, True, 2027, 3), (10, True, 2027, 0),
                                         (9, True, 2027, -1), (1, False, 2027, 4)):
            iy, im = init_calendar(planting, off, hy, wraps)
            self.assertEqual(offset_for_init(planting, wraps, hy, iy, im), off)

    def test_replay_judges_the_window_at_the_end_of_the_init_month(self):
        import inspect

        from geocif.experiments import s2s_africa as mod
        from geocif.experiments.s2s_eligibility import month_end

        self.assertEqual(month_end(2026, 2), date(2026, 2, 28))
        src = inspect.getsource(mod.run)
        self.assertIn("today = month_end(as_of_year, as_of_month)", src)
        self.assertIn('_asof{as_of_year}{as_of_month:02d}', src)
        self.assertIn("offset_for_init(", src)

    def test_replay_and_pin_are_exclusive(self):
        from geocif.experiments.s2s_africa import run

        with self.assertRaises(ValueError):
            run(forecast_offset=1, as_of_init="2026-08")
        with self.assertRaises(ValueError):
            run(as_of_init="2026/08")


class TestRenderSmoke(unittest.TestCase):
    """End to end on two synthetic polygons; needs pygmt and geopandas."""

    def setUp(self):
        try:
            import geopandas  # noqa: F401
            import pygmt  # noqa: F401
        except ImportError as exc:
            self.skipTest(f"{exc}")

    def test_png_and_csv_with_one_arrow_per_region(self):
        import geopandas as gpd
        from shapely.geometry import box

        gdf = gpd.GeoDataFrame(
            {"fnid": ["A", "B", "C"], "ADMIN0": ["X"] * 3,
             "ADMIN1": ["a", "b", "c"], "ADMIN2": ["", "", ""]},
            geometry=[box(30, -20, 31, -19), box(31, -20, 32, -19),
                      box(32, -20, 33, -19)], crs="EPSG:4326")
        series = pd.concat([
            _series([40.0, 50.0], region_id="A"),
            _series([50.0, 40.0], region_id="B", skill=False),
            _series([40.0, 41.0], region_id="C")])
        shifts = sm.one_per_region(sm.compute_shifts(series, sm.P_LOW))
        with tempfile.TemporaryDirectory() as td:
            # a second polygon for "A" must not become a second arrow
            twice = pd.concat([gdf, gdf.iloc[[0]]], ignore_index=True)
            regions = sm.region_frame(twice, "fnid", labels=twice["ADMIN1"])
            self.assertEqual(len(regions), 3)
            lookup = []
            png = sm.render(shifts, regions, sm.P_LOW, title="t", subtitle="s",
                            stem="shift_p_low_maize", dir_plots=Path(td),
                            dir_csvs=Path(td), extent=[29, 34, -21, -18],
                            lookup=lookup)
            self.assertTrue(png.exists())
            tab = pd.read_csv(Path(td) / "shift_p_low_maize.csv")
        self.assertEqual(len(lookup), 1)
        self.assertEqual(len(tab), 3)
        self.assertEqual(int(tab["drawn"].sum()), 2)
        self.assertEqual(list(tab.sort_values("region_id")["region"]),
                         ["a", "b", "c"])

    def test_render_series_writes_the_span_and_each_pair(self):
        import geopandas as gpd
        from shapely.geometry import box

        gdf = gpd.GeoDataFrame({"fnid": ["A"]}, geometry=[box(30, -20, 31, -19)],
                               crs="EPSG:4326")
        series = _series([40.0, 45.0, 50.0], region_id="A")
        with tempfile.TemporaryDirectory() as td:
            lookup = []
            sm.render_series(series, sm.P_LOW, sm.region_frame(gdf, "fnid"),
                             title="t", stem="shift_p_low_maize",
                             issue_word="init", select="consistent",
                             pairs=True, dir_plots=Path(td), dir_csvs=Path(td),
                             lookup=lookup, extent=[29, 32, -21, -18],
                             desc="maize 2027: change in P(low)")
            names = sorted(p.name for p in Path(td).glob("*.png"))
        self.assertEqual(names, ["shift_p_low_maize.png",
                                 "shift_p_low_maize_2026_08_to_2026_09.png",
                                 "shift_p_low_maize_2026_09_to_2026_10.png"])
        self.assertEqual(len(lookup), 3)
        self.assertIn("from the Aug 2026 to the Sep 2026 init", lookup[1][2])


if __name__ == "__main__":
    unittest.main()
