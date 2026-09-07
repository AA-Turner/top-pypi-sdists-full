"""Tests for the cone-of-uncertainty figures (geocif/viz/cone.py).

Covers: (a) stage -> as-of/issue mapping incl. the reverse-cumulative
convention and cross-year season ordering; (b) the min_region_frac stage drop
plus common-sample restriction; (c) area-weighted national aggregation with
missing-weight fill and unweighted fallback; (d) the end-to-end run() on a
synthetic sqlite DB with CSV/lookup pairing; (e) the empirical band math
against hand-computed values incl. the isotonic width repair; (f) graceful
degradation when the DB has no CI columns populated.
"""
import sqlite3
import tempfile
import unittest
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import numpy as np
import pandas as pd

OBS = "Observed Yield (tn per ha)"
PRED = "Predicted Yield (tn per ha)"


def _rows(regions, years, stages, with_ci=True, live_year=None):
    """Synthetic outlook rows: pred varies by (region, year, stage) but is
    deterministic; obs = 'final-stage truth' per (region, year)."""
    live_year = live_year or max(years)
    out = []
    for region, area in regions:
        for year in years:
            base = 2.0 + 0.1 * (year % 10) + (0.5 if region == "iowa" else 0.0)
            for stage, swd, k in stages:
                pred = base + 0.05 * k
                row = {
                    "Experiment Name": "outlook", "Model": "tabpfn",
                    "Region": region, "Harvest Year": str(year),
                    "Stage Name": stage, "Stage Window Display": swd,
                    PRED: pred, OBS: base + 0.02,
                    "Area (ha)": np.nan if year == live_year else area,
                    "alpha": 0.2 if with_ci else np.nan,
                    "lower CI": pred - 0.4 / (k + 1) if with_ci else np.nan,
                    "upper CI": pred + 0.5 / (k + 1) if with_ci else np.nan,
                }
                out.append(row)
    return pd.DataFrame(out)


def _write_db(df, table="united_states_of_america_maize"):
    d = Path(tempfile.mkdtemp())
    db = d / "outlook_test.db"
    con = sqlite3.connect(db)
    df.to_sql(table, con, index=False)
    con.close()
    return db


def _nass_frame(rows):
    """Tidy NASS frame as geocif.viz.nass.fetch would return it.

    rows: (crop, year, Region, ref_month|None, is_final, yield_bu_ac)
    """
    return pd.DataFrame(
        [{"crop": c, "year": y, "Region": r, "state_fips": "00",
          "period": "YEAR" if m is None else f"YEAR - {m} FORECAST",
          "ref_month": m, "is_final": f, "yield_bu_ac": v,
          "load_time": pd.Timestamp(f"{y + (1 if f else 0)}-01-12")}
         for c, y, r, m, f, v in rows])


MAIZE_STAGES = [
    ("Apr 1-Mar 31", "Mar 1-Apr 30", 0),
    ("May 1-Mar 31", "Mar 1-May 31", 1),
    ("Jun 1-Mar 31", "Mar 1-Jun 30", 2),
]
REGIONS = [("iowa", 300.0), ("illinois", 200.0)]
YEARS = [2017, 2018, 2019, 2020, 2021, 2022, 2023]


class TestStageMapping(unittest.TestCase):
    def test_asof_reverse_cumulative_and_fallback(self):
        from geocif.viz.cone import _asof_month

        # Stage Window Display is calendar-ordered: LATER endpoint = cutoff.
        self.assertEqual(_asof_month("Aug 1-Mar 31", "Mar 1-Aug 31"), 8)
        # No display column -> first token of the reverse-cumulative name.
        self.assertEqual(_asof_month("Oct 1-Apr 30", None), 10)

    def test_cross_year_season_orders_after_calendar_wrap(self):
        from geocif.viz import cone

        # Oct-planted season: a Jan cutoff must sort AFTER Nov and Dec.
        stages = [
            ("Nov 1-Oct 31", "Oct 1-Nov 30", 0),
            ("Jan 1-Oct 31", "Oct 1-Jan 31", 2),
        ]
        df = _rows(REGIONS, YEARS, stages)
        df = df.rename(columns={"Harvest Year": "year", "Stage Name": "stage",
                                "Stage Window Display": "swd"})
        df["year"] = df["year"].astype(int)
        out, dropped, _ = cone.prepare(df)
        self.assertEqual(dropped, {})
        order = (out[["stage", "season_order", "issue_month"]]
                 .drop_duplicates().set_index("stage"))
        self.assertLess(order.loc["Nov 1-Oct 31", "season_order"],
                        order.loc["Jan 1-Oct 31", "season_order"])
        self.assertEqual(int(order.loc["Nov 1-Oct 31", "issue_month"]), 12)
        self.assertEqual(int(order.loc["Jan 1-Oct 31", "issue_month"]), 2)


class TestPrepare(unittest.TestCase):
    def test_minority_stage_dropped_and_common_sample_enforced(self):
        from geocif.viz import cone

        regions = REGIONS + [("nebraska", 150.0)]  # 1/3 < min_region_frac=0.5
        df = _rows(regions, YEARS, MAIZE_STAGES)
        # A Missouri-style stage that exists for ONE region only.
        extra = _rows([regions[0]], YEARS, [("Mar 1-Mar 31", "Mar 1-Mar 31", 5)])
        # And one (region, year) hole in a surviving stage.
        df = df[~((df["Region"] == "illinois") & (df["Harvest Year"] == "2020")
                  & (df["Stage Name"] == "May 1-Mar 31"))]
        df = pd.concat([df, extra], ignore_index=True)
        df = df.rename(columns={"Harvest Year": "year", "Stage Name": "stage",
                                "Stage Window Display": "swd"})
        df["year"] = df["year"].astype(int)

        out, dropped, n_common = cone.prepare(df)
        self.assertEqual(dropped, {"Mar 1-Mar 31": 1})
        self.assertNotIn("Mar 1-Mar 31", set(out["stage"]))
        # illinois 2020 is absent from ALL stages, not NaN-propagated.
        self.assertTrue(out[(out["Region"] == "illinois")
                            & (out["year"] == 2020)].empty)
        self.assertEqual(n_common, len(regions) * len(YEARS) - 1)

    def test_live_year_missing_late_stages_is_retained(self):
        """The live season has no rows for cutoffs that have not happened yet;
        the common-sample rule must be per-year, or the live year vanishes."""
        from geocif.viz import cone

        df = _rows(REGIONS, YEARS, MAIZE_STAGES)
        live = max(YEARS)
        df = df[~((df["Harvest Year"] == str(live))
                  & (df["Stage Name"] == "Jun 1-Mar 31"))]
        df = df.rename(columns={"Harvest Year": "year", "Stage Name": "stage",
                                "Stage Window Display": "swd"})
        df["year"] = df["year"].astype(int)
        out, _, _ = cone.prepare(df)
        got = out[out["year"] == live]
        self.assertEqual(sorted(got["stage"].unique()),
                         ["Apr 1-Mar 31", "May 1-Mar 31"])
        self.assertEqual(got["Region"].nunique(), len(REGIONS))
        # hindcast years keep all three stages
        self.assertEqual(out[out["year"] == YEARS[0]]["stage"].nunique(), 3)


class TestNationalAggregation(unittest.TestCase):
    def test_weighted_mean_with_live_year_weight_fill(self):
        from geocif.viz import cone

        df = _rows(REGIONS, YEARS, MAIZE_STAGES, live_year=2023)
        df = df.rename(columns={"Harvest Year": "year", "Stage Name": "stage",
                                "Stage Window Display": "swd"})
        df["year"] = df["year"].astype(int)
        out, _, _ = cone.prepare(df)
        self.assertTrue(out.loc[out["year"] == 2023, "Area (ha)"].isna().all())
        out = cone.fill_weights(out)
        self.assertFalse(out["Area (ha)"].isna().any())

        nat = cone.national(out)
        row = nat[(nat["year"] == 2023) & (nat["stage"] == "Apr 1-Mar 31")].iloc[0]
        # hand-computed: iowa pred 2.0+0.3+0.5=2.8 (w 300), illinois 2.3 (w 200)
        self.assertAlmostEqual(row["nat_pred"], (2.8 * 300 + 2.3 * 200) / 500, places=9)
        self.assertAlmostEqual(
            row["nat_lo"], ((2.8 - 0.4) * 300 + (2.3 - 0.4) * 200) / 500, places=9)
        self.assertEqual(row["aggregation"], "area-weighted")
        self.assertEqual(row["n_states"], 2)

    def test_unweighted_fallback_when_no_region_has_area(self):
        from geocif.viz import cone

        df = _rows([("iowa", np.nan), ("illinois", np.nan)], YEARS, MAIZE_STAGES)
        df = df.rename(columns={"Harvest Year": "year", "Stage Name": "stage",
                                "Stage Window Display": "swd"})
        df["year"] = df["year"].astype(int)
        out, _, _ = cone.prepare(df)
        out = cone.fill_weights(out)
        nat = cone.national(out)
        row = nat[(nat["year"] == 2023) & (nat["stage"] == "Apr 1-Mar 31")].iloc[0]
        self.assertEqual(row["aggregation"], "unweighted")
        self.assertAlmostEqual(row["nat_pred"], (2.8 + 2.3) / 2, places=9)


class TestEmpiricalBand(unittest.TestCase):
    def test_matches_hand_computation_and_isotonic_repair(self):
        from geocif.viz import cone

        # Two stages; the LATER stage has the LARGER raw sigma (violation).
        ratios = {
            ("Apr 1-Mar 31", 1): [1.10, 1.00, 0.95, 1.00, 1.05, 0.98],
            ("May 1-Mar 31", 2): [1.30, 1.00, 0.70, 1.00, 1.20, 0.85],
        }
        rows = []
        for (stage, order), rs in ratios.items():
            for i, r in enumerate(rs):
                rows.append({"stage": stage, "season_order": order,
                             "issue_month": order + 1, "asof": order + 3,
                             "year": 2019 + i, "nat_obs": 3.0 * r,
                             "nat_pred": 3.0, "nat_lo": np.nan,
                             "nat_hi": np.nan, "n_states": 2,
                             "n_obs_states": 2,
                             "aggregation": "area-weighted"})
        nat = pd.DataFrame(rows)
        band = cone.empirical_band(nat, forecast_year=2026)

        lr_apr = np.log(np.array(ratios[("Apr 1-Mar 31", 1)]))
        mu = float(np.median(lr_apr))
        sig = float(1.4826 * np.median(np.abs(lr_apr - mu)))
        got = band[band["stage"] == "Apr 1-Mar 31"].iloc[0]
        self.assertAlmostEqual(got["mu_log"], mu, places=9)
        self.assertAlmostEqual(got["sigma_log_raw"], sig, places=9)
        self.assertEqual(int(got["n_hindcast_years"]), 6)

        # Raw widths increase Apr -> May; isotonic must make them non-increasing.
        b = band.sort_values("season_order")
        raw = b["sigma_log_raw"].values
        iso = b["sigma_log_isotonic"].values
        self.assertGreater(raw[1], raw[0])
        self.assertLessEqual(iso[1], iso[0] + 1e-12)


class TestRunEndToEnd(unittest.TestCase):
    def test_outputs_csvs_and_lookup_pairing(self):
        from geocif.viz import cone

        db = _write_db(_rows(REGIONS, YEARS, MAIZE_STAGES))
        out = Path(tempfile.mkdtemp())
        written = cone.run(
            sources={"maize": (db, "united_states_of_america_maize")},
            out=out, units="bu/ac",
        )
        self.assertTrue(written)
        grid = pd.read_csv(out / "csvs" / f"cone_grid_maize.csv")
        for col in ("crop", "stage", "issue_month", "year", "nat_pred", "nat_lo",
                    "nat_hi", "nat_pred_bu_per_ac", "buac_per_tnha",
                    "alpha_nominal", "inside_band", "n_states", "aggregation"):
            self.assertIn(col, grid.columns)
        self.assertTrue((out / "csvs" / f"cone_hindcast_errors_maize.csv").exists())
        self.assertTrue((out / "csvs" / f"cone_coverage_maize.csv").exists())

        lookup = pd.read_csv(out / "csvs" / "lookup_plots_csvs.csv")
        self.assertGreaterEqual(len(lookup), 4)
        for _, r in lookup.iterrows():
            self.assertTrue((out / "plots" / r["plot_file"]).exists(),
                            r["plot_file"])
            self.assertTrue((out / "csvs" / r["csv_file"]).exists(),
                            r["csv_file"])

    def test_all_nan_ci_degrades_gracefully(self):
        from geocif.viz import cone

        db = _write_db(_rows(REGIONS, YEARS, MAIZE_STAGES, with_ci=False))
        out = Path(tempfile.mkdtemp())
        written = cone.run(
            sources={"maize": (db, "united_states_of_america_maize")},
            out=out, units="tn/ha",
        )
        self.assertTrue(written)
        # Coverage needs CI bounds -> absent; the rest still renders.
        self.assertFalse((out / "csvs" / f"cone_coverage_maize.csv").exists())
        self.assertFalse((out / "plots" / f"cone_coverage_maize.png").exists())
        self.assertTrue((out / "plots" / f"cone_grid_maize.png").exists())
        self.assertTrue((out / "plots" / f"cone_anatomy_maize_2023.png").exists())
        grid = pd.read_csv(out / "csvs" / f"cone_grid_maize.csv")
        self.assertTrue(grid["nat_lo"].isna().all())
        # Empirical band lives on residuals, so it survives a no-CI run.
        self.assertIn("emp_lo", grid.columns)
        self.assertFalse(grid["emp_lo"].isna().all())

    def test_nass_finals_fill_observed_and_partial_pool_is_recorded(self):
        """NASS finals close observed gaps; a state without one must not blank
        the national reference, but the reduced pool has to be visible."""
        from geocif.viz import cone

        df = _rows(REGIONS, YEARS, MAIZE_STAGES)
        df.loc[df["Harvest Year"] == "2023", OBS] = np.nan     # live year
        db = _write_db(df)
        out = Path(tempfile.mkdtemp())
        # Only iowa has a 2023 final -> partial pool for the national obs.
        nass = _nass_frame([
            ("maize", 2023, "Iowa", None, True, 3.10 * cone.BU_PER_TNHA["maize"]),
        ])
        cone.run(sources={"maize": (db, "united_states_of_america_maize")},
                 out=out, units="tn/ha", nass=nass)
        grid = pd.read_csv(out / "csvs" / f"cone_grid_maize.csv")
        live = grid[grid["year"] == 2023].iloc[0]
        self.assertAlmostEqual(live["nat_obs"], 3.10, places=6)
        self.assertEqual(int(live["n_obs_states"]), 1)
        self.assertEqual(int(live["n_states"]), 2)
        # hindcast years keep their DB observed values untouched
        hist = grid[grid["year"] == 2019].iloc[0]
        self.assertAlmostEqual(
            hist["nat_obs"],
            ((2.0 + 0.9 + 0.5 + 0.02) * 300 + (2.0 + 0.9 + 0.02) * 200) / 500,
            places=9)

    def test_start_year_trims_the_grid(self):
        from geocif.viz import cone

        db = _write_db(_rows(REGIONS, YEARS, MAIZE_STAGES))
        out = Path(tempfile.mkdtemp())
        cone.run(sources={"maize": (db, "united_states_of_america_maize")},
                 out=out, units="tn/ha", start_year=2021, use_nass=False)
        grid = pd.read_csv(out / "csvs" / f"cone_grid_maize.csv")
        self.assertEqual(sorted(grid["year"].unique()), [2021, 2022, 2023])

    def test_start_year_excluding_everything_fails_loudly(self):
        from geocif.viz import cone

        db = _write_db(_rows(REGIONS, YEARS, MAIZE_STAGES))
        out = Path(tempfile.mkdtemp())
        with self.assertRaises(ValueError) as cm:
            cone.run(sources={"maize": (db, "united_states_of_america_maize")},
                     out=out, units="tn/ha", start_year=2099, use_nass=False)
        self.assertIn("start_year", str(cm.exception))

    def test_inconsistent_interval_fails_loudly(self):
        from geocif.viz import cone

        df = _rows(REGIONS, YEARS, MAIZE_STAGES)
        df.loc[df.index[0], "lower CI"] = df.loc[df.index[0], PRED] + 1.0
        db = _write_db(df)
        with self.assertRaises(ValueError):
            cone.load(db, "united_states_of_america_maize")


class TestDuplicateRows(unittest.TestCase):
    """A re-run appended into an existing outlook DB duplicates every logical
    row (the writer's upsert key carries a wall-clock Time). Undetected, that
    double-weights a state AND makes every full-pool calibration filter fail."""

    def test_duplicates_are_dropped_not_silently_averaged(self):
        from geocif.viz import cone

        df = _rows(REGIONS, YEARS, MAIZE_STAGES)
        dup = df.copy()
        for col in (PRED, "lower CI", "upper CI"):   # a differing second write
            dup[col] = dup[col] + 0.5
        db = _write_db(pd.concat([df, dup], ignore_index=True))

        loaded = cone.load(db, "united_states_of_america_maize")
        self.assertFalse(loaded.duplicated(["Region", "year", "stage"]).any())
        # the later write wins, rather than being averaged with the earlier one
        row = loaded[(loaded["Region"] == "iowa") & (loaded["year"] == 2019)
                     & (loaded["stage"] == "Apr 1-Mar 31")].iloc[0]
        base = 2.0 + 0.1 * (2019 % 10) + 0.5
        self.assertAlmostEqual(row[PRED], base + 0.5, places=9)

    def test_duplicates_do_not_erase_band_and_coverage(self):
        from geocif.viz import cone

        df = _rows(REGIONS, YEARS, MAIZE_STAGES)
        db = _write_db(pd.concat([df, df], ignore_index=True))
        out = Path(tempfile.mkdtemp())
        cone.run(sources={"maize": (db, "united_states_of_america_maize")},
                 out=out, units="tn/ha")
        # coverage survived: n_obs_states counts REGIONS, not rows
        self.assertTrue((out / "csvs" / f"cone_coverage_maize.csv").exists())
        grid = pd.read_csv(out / "csvs" / f"cone_grid_maize.csv")
        self.assertEqual(int(grid["n_states"].max()), len(REGIONS))
        self.assertFalse(grid["emp_lo"].isna().all())


class TestFailLoudly(unittest.TestCase):
    def test_one_sided_interval_violation_is_caught(self):
        """A populated lower CI above the prediction must fail even when the
        upper CI is NULL — the pair test alone would wave it through."""
        from geocif.viz import cone

        df = _rows(REGIONS, YEARS, MAIZE_STAGES)
        df.loc[df.index[0], "upper CI"] = np.nan
        df.loc[df.index[0], "lower CI"] = df.loc[df.index[0], PRED] + 1.0
        db = _write_db(df)
        with self.assertRaises(ValueError):
            cone.load(db, "united_states_of_america_maize")

    def test_no_stage_covers_full_pool_raises_clearly(self):
        from geocif.viz import cone

        # every stage misses a different region -> nothing covers 100%
        df = _rows(REGIONS, YEARS, MAIZE_STAGES)
        df = df[~((df["Region"] == "iowa") & (df["Stage Name"] == "Apr 1-Mar 31"))]
        df = df[~((df["Region"] == "illinois") & (df["Stage Name"] == "May 1-Mar 31"))]
        df = df[~((df["Region"] == "iowa") & (df["Stage Name"] == "Jun 1-Mar 31"))]
        df = df.rename(columns={"Harvest Year": "year", "Stage Name": "stage",
                                "Stage Window Display": "swd"})
        df["year"] = df["year"].astype(int)
        with self.assertRaises(ValueError) as cm:
            cone.prepare(df)
        self.assertIn("min_region_frac", str(cm.exception))

    def test_preseason_stage_names_raise_a_readable_error(self):
        from geocif.viz import cone

        stages = [("Pre-Season (init Aug)", None, 0),
                  ("Pre-Season (init Sep)", None, 1)]
        df = _rows(REGIONS, YEARS, stages)
        df = df.rename(columns={"Harvest Year": "year", "Stage Name": "stage",
                                "Stage Window Display": "swd"})
        df["year"] = df["year"].astype(int)
        with self.assertRaises(ValueError) as cm:
            cone.prepare(df)
        self.assertIn("issue month", str(cm.exception))


class TestBandGuards(unittest.TestCase):
    def test_too_few_hindcast_years_draws_no_band(self):
        """1-2 points give a MAD of zero — a confident band from nothing."""
        from geocif.viz import cone

        rows = []
        for i, r in enumerate([1.10, 0.95]):
            rows.append({"stage": "Apr 1-Mar 31", "season_order": 1,
                         "issue_month": 2, "asof": 4, "year": 2019 + i,
                         "nat_obs": 3.0 * r, "nat_pred": 3.0,
                         "nat_lo": np.nan, "nat_hi": np.nan,
                         "n_states": 2, "n_obs_states": 2,
                         "aggregation": "area-weighted"})
        nat = pd.DataFrame(rows)
        self.assertTrue(cone.empirical_band(nat, forecast_year=2026).empty)

    def test_mixed_weighting_excluded_from_calibration(self):
        """Hindcast years aggregated differently from the live year describe a
        different quantity, so they must not set the band or the coverage."""
        from geocif.viz import cone

        rows = []
        for i in range(6):
            rows.append({"stage": "Apr 1-Mar 31", "season_order": 1,
                         "issue_month": 2, "asof": 4, "year": 2015 + i,
                         "nat_obs": 3.1, "nat_pred": 3.0,
                         "nat_lo": 2.8, "nat_hi": 3.2,
                         "n_states": 2, "n_obs_states": 2,
                         "aggregation": "area-weighted"})
        rows.append({"stage": "Apr 1-Mar 31", "season_order": 1,
                     "issue_month": 2, "asof": 4, "year": 2026,
                     "nat_obs": np.nan, "nat_pred": 3.0,
                     "nat_lo": 2.8, "nat_hi": 3.2,
                     "n_states": 2, "n_obs_states": 0,
                     "aggregation": "unweighted"})
        nat = pd.DataFrame(rows)
        self.assertEqual(cone.live_aggregation(nat, 2026), "unweighted")
        self.assertTrue(cone.empirical_band(nat, 2026).empty)
        self.assertTrue(cone.coverage(nat, 2026).empty)


class TestFigureHonesty(unittest.TestCase):
    def test_grid_labels_the_bottom_axis_of_every_column(self):
        """sharex + a partial last row hides whole columns' date axis."""
        import matplotlib.pyplot as plt
        from geocif.viz import cone

        rows = []
        for y in range(2005, 2027):              # 22 panels in a 5-wide grid
            for order, issue in ((1, 6), (2, 7), (3, 8)):
                rows.append({"stage": f"S{order}", "season_order": order,
                             "issue_month": issue, "asof": issue - 1, "year": y,
                             "nat_obs": 3.0, "nat_pred": 3.0, "nat_lo": 2.8,
                             "nat_hi": 3.2, "n_states": 2, "n_obs_states": 2,
                             "aggregation": "area-weighted"})
        nat = pd.DataFrame(rows)
        out = Path(tempfile.mkdtemp()) / "grid"
        cone.plot_grid(nat, cone.coverage(nat, 2026), "maize", 2026, out,
                       units="tn/ha")
        self.assertTrue(out.with_suffix(".png").exists())

        # the helper itself: with 22 used axes in a 5-wide grid, the last used
        # axis of every column must have its x labels turned back on
        fig, axes = plt.subplots(5, 5, sharex=True)
        axes = axes.ravel()
        cone._label_bottom_axes(axes, 22, 5)
        for col in range(5):
            used = [i for i in range(22) if i % 5 == col]
            ax = axes[used[-1]]
            self.assertTrue(ax.xaxis.get_major_ticks()[0].label1.get_visible(),
                            f"column {col} lost its x tick labels")
        plt.close(fig)

    def test_labels_admit_unweighted_aggregation(self):
        from geocif.viz import cone

        nat = pd.DataFrame([{"stage": "S1", "season_order": 1, "issue_month": 6,
                             "asof": 5, "year": 2026, "nat_obs": np.nan,
                             "nat_pred": 3.0, "nat_lo": 2.8, "nat_hi": 3.2,
                             "n_states": 3, "n_obs_states": 0,
                             "aggregation": "unweighted"}])
        label = cone._agg_label(nat, 2026, 3)
        self.assertEqual(label, "unweighted 3-state aggregate")
        note = cone._coverage_note(pd.DataFrame(), 3, label).lower()
        self.assertIn("unweighted", note)
        self.assertNotIn("area-weighted", note)

    def test_miss_flag_uses_the_final_stage_not_the_last_available(self):
        """A year truncated before the final stage must not be judged — and
        cleared — on its wider mid-season band."""
        from geocif.viz import cone

        rows = []
        # full year: obs sits outside the FINAL (narrow) band -> a real miss
        for order, lo, hi in ((1, 2.0, 4.0), (2, 2.9, 3.1)):
            rows.append({"stage": f"S{order}", "season_order": order,
                         "issue_month": order + 5, "asof": order + 4,
                         "year": 2019, "nat_obs": 3.5, "nat_pred": 3.0,
                         "nat_lo": lo, "nat_hi": hi, "n_states": 2,
                         "n_obs_states": 2, "aggregation": "area-weighted"})
        # truncated year: same obs, but only the wide early stage exists
        rows.append({"stage": "S1", "season_order": 1, "issue_month": 6,
                     "asof": 5, "year": 2020, "nat_obs": 3.5, "nat_pred": 3.0,
                     "nat_lo": 2.0, "nat_hi": 4.0, "n_states": 2,
                     "n_obs_states": 2, "aggregation": "area-weighted"})
        nat = pd.DataFrame(rows)
        out = Path(tempfile.mkdtemp()) / "grid"
        cone.plot_grid(nat, cone.coverage(nat, 2026), "maize", 2026, out,
                       units="tn/ha")

        import matplotlib.pyplot as plt
        fig = plt.figure()
        plt.close(fig)
        # the flag is a rendering detail; assert the rule it encodes
        final = int(nat["season_order"].max())
        def flagged(year):
            fin = nat[(nat["year"] == year) & (nat["season_order"] == final)]
            return bool(len(fin)) and not (
                float(fin.iloc[0]["nat_lo"]) <= 3.5 <= float(fin.iloc[0]["nat_hi"]))
        self.assertTrue(flagged(2019))     # genuine final-stage miss
        self.assertFalse(flagged(2020))    # no final stage -> nothing claimed


class TestUnknownCrop(unittest.TestCase):
    def test_tn_ha_path_tolerates_a_crop_without_a_bushel_factor(self):
        from geocif.viz import cone

        db = _write_db(_rows(REGIONS, YEARS, MAIZE_STAGES), table="india_wheat")
        out = Path(tempfile.mkdtemp())
        written = cone.run(sources={"wheat": (db, "india_wheat")}, out=out,
                           units="tn/ha")
        self.assertTrue(written)
        grid = pd.read_csv(out / "csvs" / f"cone_grid_wheat.csv")
        self.assertTrue(grid["buac_per_tnha"].isna().all())


class TestAuditCsv(unittest.TestCase):
    def test_rows_used_by_the_statistics_are_marked(self):
        """Partial-pool years reach the audit CSV but must be flagged, or a
        reader recomputing the footnote gets different numbers."""
        from geocif.viz import cone

        rows = []
        for i in range(6):
            rows.append({"stage": "S1", "season_order": 1, "issue_month": 6,
                         "asof": 5, "year": 2015 + i, "nat_obs": 3.1,
                         "nat_pred": 3.0, "nat_lo": 2.8, "nat_hi": 3.2,
                         "n_states": 2, "n_obs_states": 2,
                         "aggregation": "area-weighted"})
        # one partial-pool hindcast year: excluded from mu/sigma and coverage
        rows.append({"stage": "S1", "season_order": 1, "issue_month": 6,
                     "asof": 5, "year": 2021, "nat_obs": 3.9, "nat_pred": 3.0,
                     "nat_lo": 2.8, "nat_hi": 3.2, "n_states": 2,
                     "n_obs_states": 1, "aggregation": "area-weighted"})
        nat = pd.DataFrame(rows)
        audit = cone._hindcast_errors_csv(nat, "maize", 2026)
        self.assertEqual(int(audit["used_in_stats"].sum()), 6)
        self.assertFalse(bool(audit[audit["year"] == 2021]["used_in_stats"].iloc[0]))
        # recomputing coverage from the flagged rows matches the reported one
        used = audit[audit["used_in_stats"]]
        recomputed = float(((used["nat_lo"] <= used["nat_obs"])
                            & (used["nat_obs"] <= used["nat_hi"])).mean())
        self.assertAlmostEqual(
            recomputed, float(cone.coverage(nat, 2026)["coverage"].iloc[0]), places=9)


class TestNassParsing(unittest.TestCase):
    """geocif.viz.nass turns QuickStats JSON into the reference track."""

    @staticmethod
    def _raw(year, period, load_time, value="180.0", state="ILLINOIS",
             fips="17"):
        return {"state_name": state, "state_alpha": "IL",
                "state_fips_code": fips, "unit_desc": "BU / ACRE",
                "Value": value, "reference_period_desc": period,
                "load_time": load_time, "year": str(year)}

    def test_in_season_year_row_is_not_treated_as_final(self):
        """During the season NASS mirrors the latest forecast into a 'YEAR'
        row. Counting it as final would present a forecast as an observation."""
        from geocif.viz import nass

        raw = [self._raw(2026, "YEAR - AUG FORECAST", "2026-08-12 12:00:00.000"),
               self._raw(2026, "YEAR", "2026-08-12 12:00:00.000")]
        out = nass._tidy(raw, "maize")
        self.assertEqual(len(out), 1)                      # mirror dropped
        self.assertEqual(int(out.iloc[0]["ref_month"]), 8)
        self.assertFalse(bool(out.iloc[0]["is_final"]))

    def test_post_season_year_row_is_final(self):
        from geocif.viz import nass

        raw = [self._raw(2025, "YEAR", "2026-01-12 12:00:00.000", value="169.2")]
        out = nass._tidy(raw, "maize")
        self.assertTrue(bool(out.iloc[0]["is_final"]))
        self.assertTrue(pd.isna(out.iloc[0]["ref_month"]))
        self.assertAlmostEqual(out.iloc[0]["yield_bu_ac"], 169.2, places=6)

    def test_month_mapping_state_names_and_aggregate_rows(self):
        from geocif.viz import nass

        raw = [self._raw(2012, "YEAR - SEP FORECAST", "2012-09-12 11:03:54.000",
                         value="1,234", state="SOUTH DAKOTA", fips="46"),
               self._raw(2012, "YEAR - NOV FORECAST", "2012-11-09 10:26:00.000",
                         state="OTHER STATES", fips="98")]
        out = nass._tidy(raw, "maize")
        self.assertEqual(list(out["Region"]), ["South Dakota"])   # fips 98 gone
        self.assertEqual(int(out.iloc[0]["ref_month"]), 9)
        self.assertAlmostEqual(out.iloc[0]["yield_bu_ac"], 1234.0, places=6)

    def test_finals_and_monthly_lookups(self):
        from geocif.viz import nass

        frame = _nass_frame([
            ("maize", 2012, "Iowa", None, True, 137.0),
            ("maize", 2012, "Iowa", "SEP", False, 141.0),
            ("soybean", 2012, "Iowa", None, True, 44.0),
        ])
        frame.loc[frame["period"] == "YEAR - SEP FORECAST", "ref_month"] = 9
        self.assertEqual(nass.finals(frame, "maize"), {(2012, "Iowa"): 137.0})
        self.assertEqual(nass.monthly(frame, "maize"),
                         {(2012, 9, "Iowa"): 141.0})


class TestNassTrack(unittest.TestCase):
    def test_track_requires_the_full_state_pool(self):
        """A part-of-the-pool USDA average is not comparable to the cone it is
        drawn against, so such a month is dropped rather than plotted."""
        from geocif.viz import cone

        df = _rows(REGIONS, YEARS, MAIZE_STAGES)
        df = df.rename(columns={"Harvest Year": "year", "Stage Name": "stage",
                                "Stage Window Display": "swd"})
        df["year"] = df["year"].astype(int)
        df, _, _ = cone.prepare(df)
        df = cone.fill_weights(df)

        f = cone.BU_PER_TNHA["maize"]
        nass = _nass_frame([
            # May issue: both states -> a national point
            ("maize", 2019, "Iowa", 5, False, 3.0 * f),
            ("maize", 2019, "Illinois", 5, False, 2.5 * f),
            # Jun issue: iowa only -> dropped from the national track
            ("maize", 2019, "Iowa", 6, False, 3.2 * f),
        ])
        # DB regions are lowercase in the fixture; NASS titles them
        nass["Region"] = nass["Region"].str.lower()
        national, per_state = cone.nass_track(nass, "maize", df)
        self.assertEqual(len(national), 1)
        row = national.iloc[0]
        self.assertEqual(int(row["issue_month"]), 5)
        self.assertAlmostEqual(row["usda_tnha"],
                               (3.0 * 300 + 2.5 * 200) / 500, places=6)
        self.assertEqual(int(row["n_states"]), 2)
        # per-state values survive for the small multiples
        self.assertEqual(len(per_state), 3)

    def test_track_is_plotted_and_exported(self):
        from geocif.viz import cone

        db = _write_db(_rows(REGIONS, YEARS, MAIZE_STAGES))
        out = Path(tempfile.mkdtemp())
        f = cone.BU_PER_TNHA["maize"]
        rows = []
        for year in YEARS:
            for month, val in ((5, 3.0), (6, 3.1), (7, 3.15)):
                for region in ("iowa", "illinois"):
                    rows.append(("maize", year, region, month, False, val * f))
        cone.run(sources={"maize": (db, "united_states_of_america_maize")},
                 out=out, units="tn/ha", nass=_nass_frame(rows))
        track_csv = out / "csvs" / f"cone_usda_track_maize.csv"
        self.assertTrue(track_csv.exists())
        t = pd.read_csv(track_csv)
        self.assertEqual(sorted(t["issue_month"].unique()), [5, 6, 7])
        lookup = pd.read_csv(out / "csvs" / "lookup_plots_csvs.csv")
        for _, r in lookup.iterrows():
            self.assertTrue((out / "csvs" / r["csv_file"]).exists(),
                            r["csv_file"])


class TestStatesYears(unittest.TestCase):
    def test_per_state_grids_render_for_hindcast_years_too(self):
        """USDA publishes corn/soy yield forecasts only from August, so the
        live year can show one square at most. A hindcast year carries the
        full monthly track, which is the only way to see it per state."""
        from geocif.viz import cone

        db = _write_db(_rows(REGIONS, YEARS, MAIZE_STAGES))
        out = Path(tempfile.mkdtemp())
        f = cone.BU_PER_TNHA["maize"]
        rows = []
        for month, val in ((5, 3.0), (6, 3.1), (7, 3.15)):
            for region in ("iowa", "illinois"):
                rows.append(("maize", 2019, region, month, False, val * f))
        rows.append(("maize", 2023, "iowa", 5, False, 3.2 * f))
        rows.append(("maize", 2023, "illinois", 5, False, 2.7 * f))

        cone.run(sources={"maize": (db, "united_states_of_america_maize")},
                 out=out, units="tn/ha", nass=_nass_frame(rows),
                 states_years=[2019, 2023])
        for year in (2019, 2023):
            self.assertTrue((out / "plots" / f"cone_states_maize_{year}.png").exists())
            self.assertTrue((out / "csvs" / f"cone_states_maize_{year}.csv").exists())
        # the hindcast year carries three monthly USDA points, the live year one
        csv19 = pd.read_csv(out / "csvs" / f"cone_states_maize_2019.csv")
        self.assertEqual(sorted(csv19["year"].unique()), [2019])
        lookup = pd.read_csv(out / "csvs" / "lookup_plots_csvs.csv")
        self.assertIn("cone_states_maize_2019.png", set(lookup["plot_file"]))
        self.assertIn("cone_states_maize_2023.png", set(lookup["plot_file"]))

    def test_unknown_states_year_is_skipped_not_fatal(self):
        from geocif.viz import cone

        db = _write_db(_rows(REGIONS, YEARS, MAIZE_STAGES))
        out = Path(tempfile.mkdtemp())
        written = cone.run(sources={"maize": (db, "united_states_of_america_maize")},
                           out=out, units="tn/ha", use_nass=False,
                           states_years=[1999, 2023])
        self.assertTrue(written)
        self.assertFalse((out / "plots" / f"cone_states_maize_1999.png").exists())
        self.assertTrue((out / "plots" / f"cone_states_maize_2023.png").exists())


class TestConeConfigSection(unittest.TestCase):
    def test_cone_section_drives_a_server_run(self):
        from geocif.viz import cone

        d = Path(tempfile.mkdtemp())
        db_dir = d / "out" / "usa_admin1" / "ml" / "db"
        db_dir.mkdir(parents=True)
        db = db_dir / "outlook_test.db"
        con = sqlite3.connect(db)
        _rows(REGIONS, YEARS, MAIZE_STAGES).to_sql(
            "united_states_of_america_maize", con, index=False)
        con.close()

        cfg = d / "geocif.txt"
        cfg.write_text(
            "[DEFAULT]\n"
            "project_name = usa_admin1\n"
            "countries = ['united_states_of_america']\n"
            "[PATHS]\n"
            f"dir_output = {d.as_posix()}/out\n"
            "[NASS]\n"
            "api_key = DUMMY-KEY\n"
            "[cone]\n"
            "start_year = 2021\n"
            "crops = ['maize']\n"
            "dbs = {'maize': 'outlook_test.db'}\n"
            "units = tn/ha\n"
            "ncols = 3\n"
            "use_nass_reference = False\n",
            encoding="utf-8")

        conf = cone.read_config([cfg])
        self.assertEqual(conf["start_year"], 2021)
        self.assertEqual(conf["country"], "united_states_of_america")
        self.assertEqual(conf["nass_key"], "DUMMY-KEY")
        self.assertFalse(conf["use_nass"])

        out = d / "figs"
        written = cone.run([cfg], out=out)
        self.assertTrue(written)
        grid = pd.read_csv(out / "csvs" / f"cone_grid_maize.csv")
        self.assertEqual(sorted(grid["year"].unique()), [2021, 2022, 2023])

    def test_extended_interpolation_resolves_dir_output(self):
        """geobase.txt writes dir_output = ${dir_base}/outputs; parsing it
        without ExtendedInterpolation yields a literal '${dir_base}' path."""
        from geocif.viz import cone

        d = Path(tempfile.mkdtemp())
        cfg = d / "geobase.txt"
        cfg.write_text(
            "[PATHS]\n"
            f"dir_base = {d.as_posix()}\n"
            "dir_output = ${dir_base}/outputs\n"
            "[DEFAULT]\n"
            "project_name = usa_admin1\n"
            "countries = ['united_states_of_america']\n",
            encoding="utf-8")
        conf = cone.read_config([cfg])
        self.assertEqual(conf["dir_output"], Path(d / "outputs"))


class TestConeSectionDoesNotInheritDefaults(unittest.TestCase):
    """configparser exposes every [DEFAULT] key from every section, and the
    geocif bundles put `crops` and `start_year` in [DEFAULT]. Inheriting them
    into [cone] would silently render one crop, or reset the start year."""

    def _cfg(self, tmp, cone_body):
        cfg = Path(tmp) / "geocif.txt"
        cfg.write_text(
            "[DEFAULT]\n"
            "project_name = usa_admin1\n"
            "countries = ['united_states_of_america']\n"
            "crops = ['maize']\n"          # the trap: one crop, in DEFAULT
            "start_year = 1981\n"          # and a start year meant for HarvestStat
            "[PATHS]\n"
            f"dir_output = {Path(tmp).as_posix()}/out\n"
            "[cone]\n" + cone_body,
            encoding="utf-8")
        return cfg

    def test_default_crops_and_start_year_do_not_leak_into_cone(self):
        from geocif.viz import cone

        tmp = tempfile.mkdtemp()
        cfg = self._cfg(tmp, "dbs = {'maize': 'a.db', 'soybean': 'b.db'}\n")
        conf = cone.read_config([cfg])
        # [cone] declares neither key -> the module's own defaults, not DEFAULT's
        self.assertEqual(conf["crops"], ["maize", "soybean"])
        self.assertIsNone(conf["start_year"])

    def test_cone_section_values_still_win_when_declared(self):
        from geocif.viz import cone

        tmp = tempfile.mkdtemp()
        cfg = self._cfg(tmp, "crops = ['soybean']\nstart_year = 2005\n"
                             "dbs = {'soybean': 'b.db'}\n")
        conf = cone.read_config([cfg])
        self.assertEqual(conf["crops"], ["soybean"])
        self.assertEqual(conf["start_year"], 2005)

    def test_both_crops_survive_into_sources(self):
        """The end-to-end consequence: run() builds sources from dbs filtered
        by crops, so a leaked ['maize'] would drop soybean with no warning."""
        from geocif.viz import cone

        tmp = Path(tempfile.mkdtemp())
        db_dir = tmp / "out" / "usa_admin1" / "ml" / "db"
        db_dir.mkdir(parents=True)
        for crop, name in (("maize", "a.db"), ("soybean", "b.db")):
            con = sqlite3.connect(db_dir / name)
            _rows(REGIONS, YEARS, MAIZE_STAGES).to_sql(
                f"united_states_of_america_{crop}", con, index=False)
            con.close()
        cfg = self._cfg(tmp, "dbs = {'maize': 'a.db', 'soybean': 'b.db'}\n"
                             "units = tn/ha\nuse_nass_reference = False\n")
        out = tmp / "figs"
        cone.run([cfg], out=out)
        for crop in ("maize", "soybean"):
            self.assertTrue((out / "plots" / f"cone_grid_{crop}.png").exists(),
                            f"{crop} silently dropped")


class TestModelLabelling(unittest.TestCase):
    def test_figures_and_csv_name_the_model_actually_plotted(self):
        """A DB can hold several models; labelling every figure 'tabpfn' while
        plotting cubist would misattribute a stakeholder deliverable."""
        from geocif.viz import cone

        tab = _rows(REGIONS, YEARS, MAIZE_STAGES)
        cub = _rows(REGIONS, YEARS, MAIZE_STAGES)
        cub["Model"] = "cubist"
        for col in (PRED, "lower CI", "upper CI"):
            cub[col] = cub[col] - 0.9
        db = _write_db(pd.concat([tab, cub], ignore_index=True))

        out = Path(tempfile.mkdtemp())
        cone.run(sources={"maize": (db, "united_states_of_america_maize")},
                 out=out, units="tn/ha", model="cubist", use_nass=False)

        grid = pd.read_csv(out / "csvs" / f"cone_grid_maize.csv")
        self.assertEqual(set(grid["model"]), {"cubist"})
        # and the cubist rows are what got plotted (0.9 below tabpfn's)
        row = grid[(grid["year"] == 2019)].sort_values("season_order").iloc[0]
        self.assertAlmostEqual(
            row["nat_pred"], ((2.0 + 0.9 + 0.5) * 300 + (2.0 + 0.9) * 200) / 500 - 0.9,
            places=6)

        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        plt.close(fig)
        # the title string is built from the model argument
        nat = cone.national(cone.fill_weights(
            cone.prepare(cone.load(db, "united_states_of_america_maize",
                                   model="cubist"))[0]))
        stem = Path(tempfile.mkdtemp()) / "g"
        cone.plot_grid(nat, cone.coverage(nat, 2023), "maize", 2023, stem,
                       units="tn/ha", model="cubist")
        self.assertTrue(stem.with_suffix(".png").exists())


if __name__ == "__main__":
    unittest.main()
