"""Tests for the shared outlook-DB loader (geocif/viz/_outlook_db.py).

Prove-It coverage for the bugs the module exists to bury:
(a) the dedup sorted the string Date/Time columns lexicographically, but the
    writer emits them month-name-first (Date='September_06_2026',
    Time='September-06-2026 11:31:05'; geocif/geocif.py builds them with
    arrow's MMMM_DD_YYYY / MMMM-DD-YYYY HH:mm:ss), so alphabetical order is
    not chronological and keep='last' could keep a STALE row;
(b) leadtime.load did not dedup at all, so a re-run DB double-weighted every
    region-year in the national lead-time skill scores;
(c) leadtime.prepare failed OPEN — an empty common sample silently scored
    every model on whatever rows it happened to have;
(d) leadtime.prepare derived the common sample from ONE probe model, so a
    model missing a (region, year) was scored on a different sample than the
    rest.
"""
import sqlite3
import tempfile
import unittest
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import pandas as pd

OBS = "Observed Yield (tn per ha)"
PRED = "Predicted Yield (tn per ha)"


def _row(model="tabpfn", region="iowa", year=2019, stage="Apr 1-Mar 31",
         swd="Mar 1-Apr 30", pred=3.0, obs=3.1, date=None, time=None):
    """One outlook row with the schema the real writer produces."""
    return {"Experiment Name": "outlook", "Model": model, "Region": region,
            "Harvest Year": str(year), "Stage Name": stage,
            "Stage Window Display": swd, PRED: pred, OBS: obs,
            "Area (ha)": 100.0, "alpha": 0.2,
            "lower CI": pred - 0.4, "upper CI": pred + 0.4,
            "Date": date, "Time": time}


def _write_db(rows, table="united_states_of_america_maize"):
    db = Path(tempfile.mkdtemp()) / "outlook_test.db"
    con = sqlite3.connect(db)
    pd.DataFrame(rows).to_sql(table, con, index=False)
    con.close()
    return db


class TestDedupKeepsTheChronologicallyLatest(unittest.TestCase):
    """(a) parse Date/Time before sorting — never sort the raw strings."""

    def test_september_rerun_survives_a_lexicographic_trap(self):
        # 'September_06_2026' sorts BEFORE 'September_10_2025' as a string
        # (the day digit '0' < '1' is compared before the year ever is), so
        # the old lexicographic keep='last' kept the 2025 row. The fresh row
        # is inserted FIRST so insertion order cannot rescue the assertion.
        from geocif.viz import cone

        fresh = _row(pred=4.0, date="September_06_2026",
                     time="September-06-2026 11:31:05")
        stale = _row(pred=1.0, date="September_10_2025",
                     time="September-10-2025 08:00:00")
        db = _write_db([fresh, stale])
        out = cone.load(db, "united_states_of_america_maize")
        self.assertEqual(len(out), 1)
        self.assertAlmostEqual(float(out.iloc[0][PRED]), 4.0, places=9)

    def test_month_names_do_not_sort_chronologically(self):
        # Within one year: 'December...' < 'February...' as strings, so the
        # old sort kept the stale February copy of a December re-run.
        from geocif.viz import cone

        fresh = _row(pred=4.0, date="December_01_2026",
                     time="December-01-2026 12:00:00")
        stale = _row(pred=1.0, date="February_15_2026",
                     time="February-15-2026 08:00:00")
        db = _write_db([fresh, stale])
        out = cone.load(db, "united_states_of_america_maize")
        self.assertEqual(len(out), 1)
        self.assertAlmostEqual(float(out.iloc[0][PRED]), 4.0, places=9)


class TestLeadtimeNoLongerDoubleCounts(unittest.TestCase):
    """(b) upsert duplicates collapse to one row per (Model, Region, year,
    stage) — and different models must NOT be collapsed into each other."""

    def test_upsert_duplicates_collapse_to_one_row(self):
        from geocif.viz import leadtime

        rows = []
        for model in ("tabpfn", "trend"):
            for region in ("iowa", "illinois"):
                for year in (2018, 2019):
                    for stage, swd in (("Apr 1-Mar 31", "Mar 1-Apr 30"),
                                       ("May 1-Mar 31", "Mar 1-May 31")):
                        rows.append(_row(model=model, region=region, year=year,
                                         stage=stage, swd=swd, pred=3.0,
                                         date="April_10_2026",
                                         time="April-10-2026 09:00:00"))
        rerun = [dict(r, **{PRED: r[PRED] + 0.5, "Date": "September_06_2026",
                            "Time": "September-06-2026 11:31:05"})
                 for r in rows]
        db = _write_db(rows + rerun)

        out = leadtime.load(db, "united_states_of_america_maize")
        # one copy per logical row, not two — the double-count is gone,
        # and the model axis survived intact (16 = 2*2*2*2, not 8).
        self.assertEqual(len(out), len(rows))
        self.assertFalse(
            out.duplicated(["Model", "Region", "year", "stage"]).any())
        # the September re-run's values are the ones that get scored
        self.assertTrue((out[PRED] == 3.5).all())


class TestPrepareFailsClosed(unittest.TestCase):
    """(c) an empty common sample raises instead of silently proceeding."""

    def test_empty_common_sample_raises(self):
        from geocif.viz import leadtime

        # iowa exists only in the April stage, illinois only in May: no
        # (region, year) covers both stages. The OLD code returned the frame
        # UNRESTRICTED here and scored shifting pools as if comparable.
        rows = [_row(region="iowa", year=y, stage="Apr 1-Mar 31",
                     swd="Mar 1-Apr 30") for y in (2018, 2019)]
        rows += [_row(region="illinois", year=y, stage="May 1-Mar 31",
                      swd="Mar 1-May 31") for y in (2018, 2019)]
        db = _write_db(rows)
        df = leadtime.load(db, "united_states_of_america_maize")
        with self.assertRaises(ValueError) as cm:
            leadtime.prepare(df)
        self.assertIn("common sample", str(cm.exception))


class TestCommonSampleIsIntersectionAcrossModels(unittest.TestCase):
    """(d) one probe model no longer defines everyone's sample."""

    def test_hole_in_one_model_shrinks_the_sample_for_all(self):
        from geocif.viz import leadtime

        stages = (("Apr 1-Mar 31", "Mar 1-Apr 30"),
                  ("May 1-Mar 31", "Mar 1-May 31"))
        rows = []
        for model in ("tabpfn", "cubist"):
            for region in ("iowa", "illinois"):
                for year in (2017, 2018, 2019):
                    for stage, swd in stages:
                        rows.append(_row(model=model, region=region,
                                         year=year, stage=stage, swd=swd))
        # cubist is missing illinois 2019 entirely; the probe model under the
        # old rule (whichever loads first) has it in every stage, so the old
        # sample kept the pair and scored the two models on unlike rows.
        rows = [r for r in rows if not (r["Model"] == "cubist"
                                        and r["Region"] == "illinois"
                                        and r["Harvest Year"] == "2019")]
        db = _write_db(rows)
        df = leadtime.load(db, "united_states_of_america_maize")
        out, dropped, n_common = leadtime.prepare(df)

        self.assertEqual(dropped, {})
        self.assertEqual(n_common, 5)          # 2 regions x 3 years, minus 1
        # the hole is gone for EVERY model, tabpfn included
        self.assertTrue(out[(out["Region"] == "illinois")
                            & (out["year"] == 2019)].empty)
        # identical sample by construction: same row count per model
        self.assertEqual(out.groupby("Model").size().nunique(), 1)

    def test_model_missing_an_entire_stage_fails_closed(self):
        from geocif.viz import leadtime

        stages = (("Apr 1-Mar 31", "Mar 1-Apr 30"),
                  ("May 1-Mar 31", "Mar 1-May 31"))
        rows = []
        for model in ("tabpfn", "cubist"):
            for region in ("iowa", "illinois"):
                for year in (2018, 2019):
                    for stage, swd in stages:
                        rows.append(_row(model=model, region=region,
                                         year=year, stage=stage, swd=swd))
        # cubist lost its whole May stage (the known truncation failure mode):
        # it can never be scored on the same sample at that stage, so the
        # comparison must refuse rather than draw a curve anyway.
        rows = [r for r in rows if not (r["Model"] == "cubist"
                                        and r["Stage Name"] == "May 1-Mar 31")]
        db = _write_db(rows)
        df = leadtime.load(db, "united_states_of_america_maize")
        with self.assertRaises(ValueError) as cm:
            leadtime.prepare(df)
        self.assertIn("cubist", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
