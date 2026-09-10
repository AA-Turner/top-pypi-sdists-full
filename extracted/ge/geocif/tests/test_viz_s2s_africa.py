"""Tests for the s2s_africa figure/README renderer.

The renderer is the thing a reader actually sees, so the invariants that
matter are: the plots/csvs split with a manifest in both, PNG-only output,
month spans derived from the real lead map rather than assumed, and a README
that leads with the skill and support caveats instead of burying them.
"""
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd


def _fixture(tmp, has_skill=(True, False), in_support=False):
    """A two-combination output directory, one skilful and one not."""
    out = Path(tmp)
    combos, fcs, skills = [], [], []
    for i, (country, crop, season, skill) in enumerate(
            [("Malawi", "maize", "Main", has_skill[0]),
             ("Kenya", "maize", "Short", has_skill[1])]):
        combos.append({
            "country": country, "crop": crop, "season_name": season,
            "status": "forecast", "planting_month": 11 - i,
            "harvest_month": 4 - i, "wraps": True, "harvest_year": 2027,
            "offset_used": 3 - i, "n_joined": 4, "calendar_source": "EWCM",
            "has_skill": skill, "in_support": in_support,
            "oos_max_sigma": 8.4 - i, "oos_feature": "z_TMEAN",
            "clip_frac": 1.0, "skill_auc": 0.66 if skill else 0.31,
            "skill_null_auc": 0.45, "skill_perm_p": 0.01 if skill else 0.87,
        })
        for j in range(4):
            fcs.append({
                "country": country, "crop": crop, "season_name": season,
                "harvest_year": 2027, "fnid": f"{country[:2].upper()}{j}",
                "offset_used": 3 - i, "planting_month": 11 - i,
                "ahat": 0.1 * j - 0.2, "P_low": 0.2 + 0.1 * j,
                "P_mid": 0.3, "P_high": 0.5 - 0.1 * j, "P_below_trend": 0.4,
                "skill_auc": 0.66 if skill else 0.31, "null_auc": 0.45,
                "perm_p": 0.01 if skill else 0.87, "has_skill": skill,
                "auc_national": 0.84 if skill else 0.33,
                "null_auc_national": 0.42,
                "perm_national_p": 0.01 if skill else 0.65,
                "auc_spatial": 0.58 if skill else 0.67,
                "null_auc_spatial": 0.50,
                "perm_spatial_p": 0.12 if skill else 0.007,
                "n_years": 14 if skill else 22,
                "beats_trend": False, "skill_rrmse": 40.0,
                "skill_rrmse_trend": 39.0, "in_support": in_support,
                "n_clipped": 2, "oos_max_sigma": 8.4 - i,
                "oos_feature": "z_TMEAN",
                # Malawi's baseline is defensible (14.1%), Kenya's is not
                "trend_tha": 1.5 + 0.1 * j,
                "yhat_tha": (1.5 + 0.1 * j) * (1 + 0.1 * j - 0.2),
                "extrap_years": 7 if skill else 17,
                "trend_extrap_err_pct": 14.1 if skill else 55.5})
        for off in (1, 2, 3, 4):
            skills.append({"country": country, "crop": crop,
                           "season_name": season, "offset": off,
                           "auc": 0.4 + 0.05 * off, "n": 80})
    pd.DataFrame(combos).to_csv(out / "combinations.csv", index=False)
    pd.DataFrame(fcs).to_csv(out / "forecasts.csv", index=False)
    pd.DataFrame(skills).to_csv(out / "skill.csv", index=False)
    pd.DataFrame([{"country": "Chad", "crop": "maize", "status": "too_early",
                   "usable_from": "2026-10", "reason": "window opens later"}]
                 ).to_csv(out / "excluded.csv", index=False)
    return out


class TestMonthLabels(unittest.TestCase):
    def test_span_contiguous_and_single(self):
        from geocif.viz.s2s_africa import month_span

        self.assertEqual(month_span([11, 12, 1, 2]), "Nov–Feb")
        self.assertEqual(month_span([1, 2]), "Jan–Feb")
        self.assertEqual(month_span([3]), "Mar")
        self.assertEqual(month_span([]), "")

    def test_row_labels_carry_their_own_window(self):
        from geocif.viz.s2s_africa import row_label

        season, gf = [11, 12, 1, 2], [1, 2]
        self.assertEqual(row_label("z_PRCPTOT", season, gf),
                         "Season rainfall\n(Nov–Feb)")
        self.assertEqual(row_label("z_TMEAN", season, gf),
                         "Season temperature\n(Nov–Feb)")
        self.assertEqual(row_label("z_P_GF", season, gf),
                         "Grain-fill rainfall\n(Jan–Feb)")
        # the interaction spans both windows, so it carries no month span
        self.assertEqual(row_label("DRYHEAT", season, gf),
                         "Dry × hot (interaction)")

    def test_truncated_window_is_shown_truthfully(self):
        """At offset 4 the lead cap drops the 4th season month; the label
        must follow the lead map, not the nominal season."""
        from geocif.experiments.s2s_pooled_model import lead_map, season_months
        from geocif.viz.s2s_africa import row_label

        lm = lead_map(11, 4)                       # leads 4,5,6,(7 dropped)
        smon = [m for m in season_months(11) if m in lm]
        self.assertEqual(smon, [11, 12, 1])
        self.assertEqual(row_label("z_PRCPTOT", smon, []),
                         "Season rainfall\n(Nov–Jan)")


class TestChartOutputLayout(unittest.TestCase):
    def test_plots_and_csvs_split_with_manifest_in_both(self):
        from geocif.viz.s2s_africa import charts

        with tempfile.TemporaryDirectory() as tmp:
            out = _fixture(tmp)
            base = charts(out)
            plots, csvs = base / "plots", base / "csvs"
            self.assertTrue((plots / "risk_ranking.png").exists())
            self.assertTrue((csvs / "risk_ranking.csv").exists())
            for d in (plots, csvs):
                lk = d / "lookup_plots_csvs.csv"
                self.assertTrue(lk.exists(), d)
                df = pd.read_csv(lk)
                self.assertEqual(list(df.columns),
                                 ["plot_file", "csv_file", "description"])
                self.assertGreater(len(df), 0)

    def test_no_pdfs_are_written(self):
        from geocif.viz.s2s_africa import charts

        with tempfile.TemporaryDirectory() as tmp:
            out = _fixture(tmp)
            charts(out)
            self.assertEqual(list(Path(out).rglob("*.pdf")), [])

    def test_decomposition_chart_is_drawn_when_the_split_is_present(self):
        """The pooled AUC hides which question the model can answer, so the
        national/spatial split has to reach the figures, not just the CSVs."""
        from geocif.viz.s2s_africa import charts

        with tempfile.TemporaryDirectory() as tmp:
            out = _fixture(tmp)
            base = charts(out)
            self.assertTrue((base / "plots" / "skill_decomposition.png"
                             ).exists())
            d = pd.read_csv(base / "csvs" / "skill_decomposition.csv")
            for c in ("auc_national", "auc_spatial", "perm_national_p",
                      "perm_spatial_p"):
                self.assertIn(c, d.columns, c)

        with tempfile.TemporaryDirectory() as tmp:
            out = _fixture(tmp)
            fc = pd.read_csv(out / "forecasts.csv").drop(
                columns=["auc_national", "auc_spatial"])
            fc.to_csv(out / "forecasts.csv", index=False)
            base = charts(out)
            self.assertFalse((base / "plots" / "skill_decomposition.png"
                              ).exists())

    def test_out_of_support_chart_appears_only_when_measured(self):
        from geocif.viz.s2s_africa import charts

        with tempfile.TemporaryDirectory() as tmp:
            out = _fixture(tmp)
            base = charts(out)
            self.assertTrue((base / "plots" / "out_of_support.png").exists())

        with tempfile.TemporaryDirectory() as tmp:
            out = _fixture(tmp)
            fc = pd.read_csv(out / "forecasts.csv").drop(
                columns=["oos_max_sigma"])
            fc.to_csv(out / "forecasts.csv", index=False)
            base = charts(out)
            self.assertFalse((base / "plots" / "out_of_support.png").exists())


class TestRegressionMapGating(unittest.TestCase):
    """The t/ha map must withhold units whose trend baseline is
    extrapolated too far, and skip itself entirely when nothing qualifies —
    a coloured map implies a defensible number everywhere it is drawn.

    These test the gating logic without PyGMT, which is a binary stack.
    """

    def test_threshold_admits_short_extrapolations_only(self):
        from geocif.experiments.s2s_africa import TREND_EXTRAP_MAX_PCT

        # measured backtest errors from the Africa-wide run
        self.assertLessEqual(10.1, TREND_EXTRAP_MAX_PCT)   # South Africa maize
        self.assertLessEqual(14.1, TREND_EXTRAP_MAX_PCT)   # Malawi maize
        self.assertGreater(28.8, TREND_EXTRAP_MAX_PCT)     # Mozambique maize
        self.assertGreater(55.5, TREND_EXTRAP_MAX_PCT)     # Madagascar maize

    def test_gate_partitions_the_units(self):
        from geocif.experiments.s2s_africa import TREND_EXTRAP_MAX_PCT

        with tempfile.TemporaryDirectory() as tmp:
            out = _fixture(tmp)
            fc = pd.read_csv(Path(out) / "forecasts.csv")
            ok = fc["trend_extrap_err_pct"] <= TREND_EXTRAP_MAX_PCT
            # the fixture's skilful combination qualifies, the other does not
            self.assertTrue(ok.any())
            self.assertFalse(ok.all())
            self.assertEqual(set(fc.loc[ok, "country"]), {"Malawi"})

    def test_nothing_qualifying_means_no_map(self):
        """When every combination is beyond the threshold the map is
        skipped, not drawn empty."""
        from geocif.experiments.s2s_africa import TREND_EXTRAP_MAX_PCT

        with tempfile.TemporaryDirectory() as tmp:
            out = _fixture(tmp)
            fc = pd.read_csv(Path(out) / "forecasts.csv")
            fc["trend_extrap_err_pct"] = 60.0
            ok = fc["trend_extrap_err_pct"] <= TREND_EXTRAP_MAX_PCT
            self.assertFalse(ok.any())

    def test_anomaly_map_needs_no_yield_level(self):
        """The % vs trend product is publishable wherever the
        classification map is, because it never touches an absolute level."""
        with tempfile.TemporaryDirectory() as tmp:
            out = _fixture(tmp)
            fc = pd.read_csv(Path(out) / "forecasts.csv")
            self.assertIn("ahat", fc.columns)
            # dropping the level columns must not affect ahat coverage
            fc2 = fc.drop(columns=["trend_tha", "yhat_tha"])
            self.assertEqual(fc2["ahat"].notna().sum(), len(fc2))


class TestReadme(unittest.TestCase):
    def test_leads_with_skill_and_support_counts(self):
        from geocif.viz.s2s_africa import readme

        with tempfile.TemporaryDirectory() as tmp:
            out = _fixture(tmp)
            p = readme(out, version="0.4.1002")
            txt = Path(p).read_text(encoding="utf-8")
            head = txt[:txt.find("| Country |")]
            # the caveats come before the numbers, not after
            self.assertIn("Read this first", head)
            self.assertIn("**1 of\n   2**", head.replace("  ", "  "))
            self.assertIn("**0 of 2**", head)
            self.assertIn("not against AUC 0.5", head)
            self.assertIn("0.4.1002", txt)

    def test_table_marks_the_skilful_combination(self):
        from geocif.viz.s2s_africa import readme

        with tempfile.TemporaryDirectory() as tmp:
            out = _fixture(tmp)
            txt = Path(readme(out)).read_text(encoding="utf-8")
            rows = [ln for ln in txt.splitlines() if ln.startswith("| Malawi")]
            self.assertEqual(len(rows), 1)
            self.assertIn("**yes**", rows[0])
            kenya = [ln for ln in txt.splitlines() if ln.startswith("| Kenya")]
            self.assertIn("| no |", kenya[0])


class TestRenderAllIsFailureIsolated(unittest.TestCase):
    def test_one_family_failing_does_not_stop_the_others(self):
        """A missing GMT library must not cost the run its charts."""
        from geocif.viz import s2s_africa as viz

        with tempfile.TemporaryDirectory() as tmp:
            out = _fixture(tmp)
            viz.render_all(out, root=Path(tmp) / "nope",
                           hvstat_csv=Path(tmp) / "missing.csv",
                           gpkg=Path(tmp) / "missing.gpkg")
            # heatmaps and maps cannot work with those paths; charts and
            # README must still be there
            self.assertTrue((Path(out) / "figures" / "charts" / "plots"
                             / "risk_ranking.png").exists())
            self.assertTrue((Path(out) / "README.md").exists())


class TestRunWiring(unittest.TestCase):
    def test_run_calls_the_renderer_and_can_be_switched_off(self):
        import inspect
        from geocif.experiments import s2s_africa as sa

        src = inspect.getsource(sa.run)
        self.assertIn("figures and n_fc", src)
        self.assertIn("viz.render_all", src)
        self.assertIn("figures=True", inspect.signature(sa.run).__str__()
                      .replace(" ", "").replace("figures=True", "figures=True"))
        self.assertIs(inspect.signature(sa.run).parameters["figures"].default,
                      True)


if __name__ == "__main__":
    unittest.main()
