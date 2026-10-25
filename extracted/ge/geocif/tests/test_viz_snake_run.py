# -*- coding: utf-8 -*-
"""Tests for the snake chart runner (geocif/viz/snake_run.py) and the
yield_outlook hook.

What must hold: ``[snake]`` keys are read only when written there (no
``[DEFAULT]`` leak), the run folder follows the DB name, one figure per
season that can be built (a season that cannot is skipped, not fatal), the
PNG and companion CSV are written (no PDF, no lookup manifest), the unit
name is the default title, a non
``monthly_r`` run is refused, and ``_render_snake_figures`` writes beside
``outlook/``.
"""
import sqlite3
import tempfile
import unittest
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import pandas as pd

from geocif.viz import snake_run as sr
from tests.test_viz_snake_data import COUNTRY, CROP, write_cid, write_db

DB_NAME = "outlook_09_17_2026_14h18.db"


def make_project(tmp, snake_section=None, default_extra=""):
    out = Path(tmp) / "outputs"
    root = out / "proj"
    (root / "ml" / "db").mkdir(parents=True)
    db = write_db(root / "ml" / "db")
    write_cid(root)
    cfg = Path(tmp) / "geocif.txt"
    snake_section = snake_section if snake_section is not None else (
        "[snake]\nrows = ['ndvi', 'rain', 'heat']\n")
    cfg.write_text(
        "[DEFAULT]\nproject_name = proj\ncrops = ['maize']\n" + default_extra +
        f"\n[PATHS]\ndir_output = {out.as_posix()}\n\n[ML]\nyield_units = Mg/ha\n\n" + snake_section,
        encoding="utf-8")
    return [cfg], root, db


class TestConfig(unittest.TestCase):
    def test_snake_keys_only_from_the_section(self):
        tmp = tempfile.mkdtemp()
        cfgs, root, _ = make_project(tmp, default_extra="model = catboost\nwindow = month\n")
        cfg = sr.read_config(cfgs)
        self.assertIsNone(cfg["model"])            # [DEFAULT] model does not leak
        self.assertEqual(cfg["window"], "stage")
        self.assertEqual(cfg["rows"], ["ndvi", "rain", "heat"])
        self.assertEqual(cfg["root"], root)

    def test_display_for(self):
        cfg = {"yield_display": {"maize": ["bu/ac", 15.9318]}, "yield_units": "Mg/ha"}
        self.assertEqual(sr.display_for(cfg, "maize"), ("bu/ac", 15.9318))
        self.assertEqual(sr.display_for(cfg, "rice"), ("Mg/ha", 1.0))

    def test_unknown_row_is_refused(self):
        with self.assertRaises(ValueError):
            sr.indicator_metas(["ndvi", "soil_magic"])


class TestRun(unittest.TestCase):
    def test_one_figure_per_modeled_unit_by_default(self):
        tmp = tempfile.mkdtemp()
        cfgs, root, db = make_project(tmp)
        written = sr.run(cfgs, db=DB_NAME, table=f"{COUNTRY}_{CROP}", model="tabpfn", year=2026,
                         out=Path(tmp) / "units")
        pngs = sorted(p.name for p in written if p.suffix == ".png")
        self.assertEqual(pngs, [f"snake_{COUNTRY}_{CROP}_tabpfn_baringo_s1_2026.png",
                                f"snake_{COUNTRY}_{CROP}_tabpfn_bomet_s1_2026.png"])
        csv = pd.read_csv(Path(tmp) / "units" / "csvs" / f"snake_{COUNTRY}_{CROP}_tabpfn_bomet_s1_2026.csv")
        self.assertEqual(set(csv["scope"]), {"Bomet"})
        self.assertFalse((Path(tmp) / "units" / "plots" / "lookup_plots_csvs.csv").exists())
        self.assertEqual(set(csv["title"]), {"Bomet"})          # the unit name by default

    def test_title_template_names_the_unit(self):
        tmp = tempfile.mkdtemp()
        cfgs, root, db = make_project(
            tmp, snake_section="[snake]\nrows = ['PRCPTOT']\ntitle = {region} {year}\n")
        sr.run(cfgs, db=db, table=f"{COUNTRY}_{CROP}", model="tabpfn", year=2026,
               out=Path(tmp) / "t", regions=["Bomet"])
        csv = pd.read_csv(Path(tmp) / "t" / "csvs" / f"snake_{COUNTRY}_{CROP}_tabpfn_bomet_s1_2026.csv")
        self.assertEqual(set(csv["title"]), {"Bomet 2026"})

    def test_end_to_end_writes_figure_csv_and_lookup(self):
        tmp = tempfile.mkdtemp()
        cfgs, root, db = make_project(tmp)
        written = sr.run(cfgs, db=DB_NAME, table=f"{COUNTRY}_{CROP}", model="tabpfn", year=2026,
                         regions=["national"])
        base = root / "ml" / "analysis" / "September_17_2026_14h18" / "snake"
        stem = f"snake_{COUNTRY}_{CROP}_tabpfn_national_s1_2026"
        for p in (base / "plots" / f"{stem}.png", base / "csvs" / f"{stem}.csv"):
            self.assertTrue(p.exists(), p)
        for p in (base / "plots" / f"{stem}.pdf", base / "plots" / "lookup_plots_csvs.csv",
                  base / "csvs" / "lookup_plots_csvs.csv"):
            self.assertFalse(p.exists(), p)
        self.assertIn(base / "plots" / f"{stem}.png", written)
        # season 2 has only live-year rows: skipped, not fatal
        self.assertFalse(any("_s2_" in p.name for p in written))
        csv = pd.read_csv(base / "csvs" / f"{stem}.csv")
        self.assertEqual(csv["row"].nunique(), 4)
        # the title is the place name; the footer text is in the CSV
        self.assertTrue(csv["source_line"].iloc[0].endswith("Right = more favorable for yield."))
        self.assertEqual(set(csv["title"]), {"Kenya"})
        self.assertIn("baseline_sd", csv.columns)


    def test_cids_option_with_invert_and_labels(self):
        tmp = tempfile.mkdtemp()
        cfgs, root, db = make_project(
            tmp, snake_section="[snake]\ncids = ['PRCPTOT', 'SU']\nrows = ['ndvi']\n"
                               "invert = {'SU': False}\nlabels = {'PRCPTOT': 'Rain'}\n")
        cfg = sr.read_config(cfgs)
        self.assertEqual(cfg["rows"], ["PRCPTOT", "SU"])          # cids wins over rows
        metas = sr.indicator_metas(cfg["rows"], cfg["invert"], cfg["labels"])
        self.assertEqual([(m.cid, m.label, m.invert) for m in metas],
                         [("PRCPTOT", "Rain", False), ("SU", "Heat days (Tmax > 25 C)", False)])
        tracks, _, _ = sr.build(cfg, db=db, table=f"{COUNTRY}_{CROP}", model="tabpfn",
                                year=2026, season=1)
        self.assertEqual(set(tracks["row"]) - {"Maize yield forecast"},
                         {"Rain", "Heat days (Tmax > 25 C)"})
        self.assertFalse(tracks.loc[tracks["cid"] == "SU", "invert"].any())
        # the default is the current selection
        self.assertEqual(sr.DEFAULTS["rows"], ["PRCPTOT", "MEAN_ESI4WK", "AUC_NDVI"])
        with self.assertRaises(ValueError):
            sr.indicator_metas(["NOT_A_CID"])

    def test_cid_names_and_last_five_years(self):
        tmp = tempfile.mkdtemp()
        cfgs, root, db = make_project(
            tmp, snake_section="[snake]\nrows = ['PRCPTOT', 'SU']\nbaseline_last = 5\n")
        cfg = sr.read_config(cfgs)
        self.assertEqual(cfg["baseline_last"], 5)
        tracks, meta, ctx = sr.build(cfg, db=db, table=f"{COUNTRY}_{CROP}", model="tabpfn",
                                     year=2026, season=1)
        ind = tracks[tracks["role"] != "target"]
        self.assertEqual(set(ind["baseline_n"]), {5})
        # the normal is the plain mean of 2021-2025 at the same window
        from tests.test_viz_snake_data import cid_value, area
        import numpy as np
        rain = ind[ind["cid"] == "PRCPTOT"].sort_values("issue_date").iloc[-1]
        nat = []
        for y in range(2021, 2026):
            w = {r: area(r, y) for r in ("Baringo", "Bomet")}
            v = {r: cid_value("PRCPTOT", r, y, "8_7_6_5_4") for r in w}
            nat.append(sum(v[r] * w[r] for r in w) / sum(w.values()))
        self.assertAlmostEqual(rain["baseline_mean"], float(np.mean(nat)), places=6)
        self.assertAlmostEqual(rain["normal_raw"], float(np.mean(nat)), places=6)

    def test_model_picked_from_the_run_when_unset(self):
        tmp = tempfile.mkdtemp()
        cfgs, root, db = make_project(tmp)
        con = sqlite3.connect(db)
        rows = pd.read_sql('SELECT * FROM "kenya_maize"', con)
        for m in ("trend", "cubist"):
            rows.assign(Model=m).to_sql("kenya_maize", con, if_exists="append", index=False)
        con.close()
        # the run's models list is ['tabpfn', 'trend'] -> tabpfn, the first ML model
        self.assertEqual(sr.pick_model(db, f"{COUNTRY}_{CROP}", ["cubist", "tabpfn", "trend"]), "tabpfn")
        self.assertEqual(sr.pick_model(db, f"{COUNTRY}_{CROP}", ["cubist", "trend"]), "cubist")
        self.assertIsNone(sr.pick_model(db, f"{COUNTRY}_{CROP}", ["trend", "null"]))
        written = sr.run(cfgs, db=db, table=f"{COUNTRY}_{CROP}", year=2026, season=1,
                         regions=["Bomet"], out=Path(tmp) / "m")
        self.assertTrue(any("_tabpfn_bomet_" in p.name for p in written))

    def test_region_figure(self):
        tmp = tempfile.mkdtemp()
        cfgs, root, db = make_project(tmp)
        written = sr.run(cfgs, db=db, table=f"{COUNTRY}_{CROP}", model="tabpfn", year=2026,
                         season=1, regions=["Bomet"], out=Path(tmp) / "o")
        self.assertTrue(any(p.name == f"snake_{COUNTRY}_{CROP}_tabpfn_bomet_s1_2026.png"
                            for p in written))

    def test_non_monthly_run_is_refused(self):
        tmp = tempfile.mkdtemp()
        cfgs, root, db = make_project(tmp)
        con = sqlite3.connect(db)
        con.execute("UPDATE config_September_17_2026 SET Value = 'biweekly_r' "
                    "WHERE Option = 'method'")
        con.commit()
        con.close()
        cfg = sr.read_config(cfgs)
        with self.assertRaises(ValueError) as cm:
            sr.build(cfg, db=db, table=f"{COUNTRY}_{CROP}", model="tabpfn", year=2026, season=1)
        self.assertIn("monthly_r", str(cm.exception))
        # the runner logs and skips instead of raising
        self.assertEqual(sr.run(cfgs, db=db, table=f"{COUNTRY}_{CROP}", model="tabpfn",
                                year=2026, out=Path(tmp) / "o"), [])

    def test_hook_writes_beside_outlook(self):
        from geocif.yield_outlook import _render_snake_figures

        tmp = tempfile.mkdtemp()
        cfgs, root, db = make_project(tmp)
        dir_outlook = Path(tmp) / "analysis" / "outlook"
        dir_outlook.mkdir(parents=True)
        written = _render_snake_figures(None, cfgs, db, dir_outlook, [COUNTRY], [CROP],
                                        ["tabpfn"], current_year=2026)
        self.assertTrue(written)
        self.assertTrue(all((dir_outlook.parent / "snake") in p.parents for p in written))
        # an unknown crop table is logged and skipped
        self.assertEqual(_render_snake_figures(None, cfgs, db, dir_outlook, [COUNTRY],
                                               ["teff"], ["tabpfn"], current_year=2026), [])


if __name__ == "__main__":
    unittest.main()


class TestSnakeDefault(unittest.TestCase):
    """[ML] make_snake_plots: unset = admin_1 countries only; set = everyone or no one."""

    def _parser(self, ml=""):
        import configparser
        p = configparser.ConfigParser(inline_comment_prefixes=(";",))
        p.read_string("[DEFAULT]\nadmin_level = admin_1\n"
                      "[kenya]\n[usa]\nadmin_level = admin_2\n[ML]\n" + ml)
        return p

    def test_unset_skips_admin_2(self):
        from geocif.yield_outlook import snake_countries
        self.assertEqual(snake_countries(self._parser(), ["kenya", "usa"]), ["kenya"])

    def test_explicit_value_applies_to_all(self):
        from geocif.yield_outlook import snake_countries
        self.assertEqual(snake_countries(self._parser("make_snake_plots = True\n"),
                                         ["kenya", "usa"]), ["kenya", "usa"])
        self.assertEqual(snake_countries(self._parser("make_snake_plots = False\n"),
                                         ["kenya", "usa"]), [])
