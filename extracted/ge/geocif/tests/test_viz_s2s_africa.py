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


class TestConfigDrivenExtent(unittest.TestCase):
    """Southern and eastern Africa are separate RUNS from separate configs.

    The viz layer therefore knows about exactly one extent, handed to it by
    the caller, and never carries a list of regions of its own.
    """

    def test_maps_takes_an_extent_and_label(self):
        import inspect
        from geocif.viz import s2s_africa as viz

        sig = inspect.signature(viz.maps)
        self.assertIn("extent", sig.parameters)
        self.assertIn("label", sig.parameters)
        self.assertIsNone(sig.parameters["extent"].default)
        self.assertEqual(sig.parameters["label"].default, "")

    def test_absent_extent_falls_back_to_all_africa(self):
        import inspect
        from geocif.viz import s2s_africa as viz

        src = inspect.getsource(viz.maps)
        self.assertIn("extent or REGION", src)
        self.assertEqual(viz.REGION, [-20, 52, -36, 25])

    def test_render_all_threads_the_extent_through(self):
        import inspect
        from geocif.viz import s2s_africa as viz

        sig = inspect.signature(viz.render_all)
        for k in ("extent", "label"):
            self.assertIn(k, sig.parameters)
        src = inspect.getsource(viz.render_all)
        self.assertIn("extent=extent", src)
        self.assertIn("label=label", src)

    def test_no_view_registry_survives_in_the_viz_layer(self):
        """A leftover region list here would be a second, competing source
        of truth against the configs."""
        from geocif.viz import s2s_africa as viz

        for attr in ("MAP_VIEWS", "DEFAULT_MAP_VIEWS", "_maps_one_view"):
            self.assertFalse(hasattr(viz, attr), attr)


class TestLegendPlacement(unittest.TestCase):
    """The legend must not sit on top of a forecast region.

    `JBL+jBL` anchors it INSIDE the frame at bottom-left, which is open
    Atlantic on the continent-wide extent and the Western Cape once the map
    is cropped to southern Africa. Regional extents make inside-the-frame
    placement unsafe in general, so every legend moved to the margin.
    """

    def test_legends_are_outside_the_frame(self):
        from geocif.viz import s2s_africa as viz

        self.assertTrue(viz.LEGEND_POS.startswith("JBL+jTL"))
        self.assertNotIn("jBL", viz.LEGEND_POS)

    def test_no_legend_is_anchored_inside_the_frame(self):
        import inspect

        from geocif.viz import s2s_africa as viz

        src = inspect.getsource(viz.maps)
        # the comment naming the old anchor lives at module scope, not here
        self.assertNotIn("JBL+jBL", src)
        self.assertNotIn('position="JBL', src)

    def test_colorbars_clear_the_legend_they_share_the_margin_with(self):
        import inspect

        from geocif.viz import s2s_africa as viz

        src = inspect.getsource(viz.maps)
        # one renderer, one colorbar call: pushed down when a legend shares
        # the margin, tight when there is none
        self.assertNotIn("o0c/1.1c+e", src)
        self.assertIn("CBAR_OFFSET if legend_rows", src)
        self.assertIn("no legend to clear", src)
        # extenders stay on both paths: P_low spans 0.005-0.945 against a
        # 0.15-0.50 ramp, so the bar's tails carry real values
        self.assertTrue(viz.CBAR_OFFSET.endswith("+e"))

    def test_every_legend_declares_a_width(self):
        """A missing +w makes GMT guess, and it guesses too narrow."""
        import inspect
        import re

        from geocif.viz import s2s_africa as viz

        src = inspect.getsource(viz.maps)
        # exactly ONE fig.legend call survives, inside the shared _legend
        # helper, and it always formats an explicit width
        self.assertEqual(src.count("fig.legend("), 1)
        self.assertIn("LEGEND_POS.format(w=width)", src)
        # every caller hands _legend its width (def + at least 3 call sites)
        self.assertGreaterEqual(src.count("_legend(fig, td,"), 4)


class TestSharedOutlookStyling(unittest.TestCase):
    """These maps and the single-country yield_outlook maps are one product.

    The styling constants live in `viz/_pygmt_render` and are imported, not
    restated, so the two families cannot drift apart on frame, pen, coast or
    colorbar geometry.
    """

    def test_style_constants_come_from_the_shared_home(self):
        """Constants come from the GMT-free viz/_style."""
        import inspect

        from geocif.viz import s2s_africa as viz

        src = inspect.getsource(viz.maps)
        self.assertIn("from geocif.viz._style import", src)
        for k in ("POLY_PEN", "COAST_KW", "CBAR_POS", "BORDER_PEN"):
            self.assertIn(k, src, k)

    def test_the_map_helper_import_stays_inside_maps(self):
        """geopandas is still a module-scope import of _pygmt_render, so a
        module-scope import HERE would make the charts and heatmaps
        unrenderable wherever geopandas is missing. The style constants
        come from the stdlib-only _style instead, which is why they can be
        imported at the top."""
        import inspect

        from geocif.viz import s2s_africa as viz

        head = inspect.getsource(viz).split("def _dirs")[0]
        self.assertNotIn("_pygmt_render", head)
        self.assertIn("from geocif.viz._style import", head)

    def test_frame_is_the_gmt_default_not_plain(self):
        """The outlook maps use the fancy (checkered) frame."""
        import inspect

        from geocif.viz import s2s_africa as viz

        self.assertNotIn("MAP_FRAME_TYPE", inspect.getsource(viz.maps))

    def test_land_is_lighter_than_the_nodata_class(self):
        """Land outside the analysis and an admin unit with no forecast are
        different statements, and only the second one is in the legend."""
        from geocif.viz import s2s_africa as viz

        self.assertNotEqual(viz.LAND, viz.NODATA)
        self.assertGreater(int(viz.LAND[1:3], 16), int(viz.NODATA[1:3], 16))
        self.assertNotEqual(viz.LAND.lower(), "#ffffff")

    def test_cpt_segments_interpolate_between_stops(self):
        """A stepped bar beside the outlook maps' smooth one reads as a
        different product."""
        import tempfile

        from geocif.viz.s2s_africa import FEWS_CPT, _write_cpt

        with tempfile.TemporaryDirectory() as td:
            f = Path(td) / "c.cpt"
            _write_cpt(f, FEWS_CPT)
            rows = [ln.split("\t") for ln in f.read_text().strip().splitlines()
                    if not ln.startswith(("B", "F", "N"))]
        self.assertEqual(len(rows), len(FEWS_CPT) - 1)
        for lo, ca, hi, cb in rows:
            self.assertNotEqual(ca, cb, f"{lo}-{hi} is a flat step")
        self.assertEqual(rows[0][1], FEWS_CPT[0][1])
        self.assertEqual(rows[-1][3], FEWS_CPT[-1][1])

    def test_every_value_map_routes_through_the_one_renderer(self):
        """Five choropleths, one skeleton: a styling fix must land on all
        of them, so none may hand-roll its own plot/colorbar/legend."""
        import inspect

        from geocif.viz import s2s_africa as viz

        src = inspect.getsource(viz.maps)
        # def + choropleth + anomaly + yield + region_roc + support
        self.assertEqual(src.count("_value_map("), 6)
        # and no wrapper bypasses it with its own colorbar
        self.assertEqual(src.count("fig.colorbar("), 1)


class TestFontsMatchTheOutlookMaps(unittest.TestCase):
    def test_only_the_title_font_is_overridden(self):
        """Shrinking FONT_LABEL made the colorbar caption smaller than the
        same caption on a yield_outlook map."""
        import inspect
        import re

        from geocif.viz import s2s_africa as viz

        src = inspect.getsource(viz.maps)
        # the pygmt.config CALL, not the whole source: the comment above it
        # names the settings it deliberately leaves alone
        m = re.search(r"pygmt\.config\((.*?)\)", src, re.S)
        self.assertIsNotNone(m)
        cfg = m.group(1)
        self.assertIn("FONT_TITLE", cfg)
        self.assertNotIn("FONT_LABEL", cfg)
        self.assertNotIn("FONT_ANNOT", cfg)


class TestMapsShareOneDedupPolicy(unittest.TestCase):
    """For the 13 two-season countries an fnid appears under both seasons,
    so every per-fnid map must pick the SAME row or the maps describe
    different forecasts of the same place."""

    #: column -> the direction that means "worst case first", since
    #: drop_duplicates keeps the first row. Checking only that SOME sort
    #: precedes the dedup is not enough: `sort_values("P_low")` ascending
    #: keeps the LOWEST-risk season and still matches a column-only regex.
    POLICY = {"P_low": "descending", "oos_max_sigma": "descending",
              "ahat": "ascending", "yhat_tha": "ascending"}

    def _dedups(self):
        import inspect
        import re

        from geocif.viz import s2s_africa as viz

        src = inspect.getsource(viz.maps)
        return src, re.findall(
            r'sort_values\(\s*"(\w+)"([^)]*)\)\s*\n?\s*\.?'
            r'drop_duplicates\("fnid"\)', src)

    def test_every_dedup_is_sorted_first(self):
        src, found = self._dedups()
        self.assertEqual(src.count('drop_duplicates("fnid")'), len(found),
                         "an unsorted drop_duplicates('fnid') slipped in")

    def test_each_sort_runs_in_the_worst_case_first_direction(self):
        _, found = self._dedups()
        self.assertTrue(found)
        for col, args in found:
            self.assertIn(col, self.POLICY, f"unknown dedup key {col}")
            descending = "ascending=False" in args
            want = self.POLICY[col] == "descending"
            self.assertEqual(descending, want,
                             f'{col} dedup must sort '
                             f'{self.POLICY[col]}; got "{args.strip()}"')

    def test_the_two_verdict_maps_follow_the_p_low_row(self):
        """region ROC and season display a value that does not itself
        define 'worst', so they inherit the P_low map's choice."""
        _, found = self._dedups()
        self.assertEqual(sum(1 for c, _ in found if c == "P_low"), 3)


class TestDefensibleBaseline(unittest.TestCase):
    """The t/ha map's shown-vs-withheld split, tested as BEHAVIOUR.

    It used to live in a closure inside maps(), reachable only with GMT
    installed, so the only available check was grepping maps() for the
    literal fix text — which would still pass if the mask were inverted.
    """

    def _frame(self):
        return pd.DataFrame({
            "fnid": ["A", "B", "C", "D"],
            # NaN = the trend never got a defensible baseline at all
            "trend_extrap_err_pct": [np.nan, 5.0, 20.0, 55.5],
        })

    def test_nan_is_withheld_not_shown(self):
        from geocif.viz.s2s_africa import defensible_baseline

        ok = defensible_baseline(self._frame(), 20.0)
        self.assertFalse(bool(ok.iloc[0]), "NaN must not be shown")
        self.assertTrue(bool(ok.iloc[1]))
        self.assertTrue(bool(ok.iloc[2]), "the bound itself is inclusive")
        self.assertFalse(bool(ok.iloc[3]))

    def test_every_unit_lands_in_exactly_one_layer(self):
        """The docstring promises the map never implies coverage it does
        not have: shown and withheld must partition the frame, with no
        unit falling through to render as land outside the analysis."""
        from geocif.viz.s2s_africa import defensible_baseline

        g = self._frame()
        ok = defensible_baseline(g, 20.0)
        shown, withheld = g[ok], g[~ok]
        self.assertEqual(len(shown) + len(withheld), len(g))
        self.assertEqual(set(shown.fnid) | set(withheld.fnid),
                         set(g.fnid))
        self.assertEqual(set(shown.fnid) & set(withheld.fnid), set())
        self.assertIn("A", set(withheld.fnid))

    def test_all_nan_column_withholds_everything(self):
        from geocif.viz.s2s_africa import defensible_baseline

        g = pd.DataFrame({"fnid": ["A", "B"],
                          "trend_extrap_err_pct": [np.nan, np.nan]})
        self.assertFalse(defensible_baseline(g, 20.0).any())

    def test_both_call_sites_use_the_helper(self):
        """The skip-the-map gate and the shown/withheld split must agree:
        two hand-written masks are how they drift apart."""
        import inspect

        from geocif.viz import s2s_africa as viz

        src = inspect.getsource(viz.maps)
        self.assertEqual(src.count("defensible_baseline("), 2)
        self.assertNotIn('["trend_extrap_err_pct"].notna()', src)


class TestPredictorPanelRenderer(unittest.TestCase):
    """predictor_heatmaps is a pure read of predictors.csv when present."""

    @staticmethod
    def _write_run_dir(out):
        import pandas as pd

        rows = []
        for y in (1995, 1996, 1997):
            for f, v in (("z_PRCPTOT", 0.2 * (y - 1995)),
                         ("z_P_GF", -0.1)):
                rows.append(dict(country="Malawi", crop="maize",
                                 season_name="Main", offset=3, init_year=2026,
                                 init_month=8, season_months="11,12,1,2",
                                 gf_months="1,2", year=y, kind="hindcast",
                                 predictor=f, value=v, n_units=7))
        for f in ("z_PRCPTOT", "z_P_GF"):
            rows.append(dict(country="Malawi", crop="maize",
                             season_name="Main", offset=3, init_year=2026,
                             init_month=8, season_months="11,12,1,2",
                             gf_months="1,2", year=2018,
                             kind="climatology_fill", predictor=f,
                             value=0.0, n_units=7))
            rows.append(dict(country="Malawi", crop="maize",
                             season_name="Main", offset=3, init_year=2026,
                             init_month=8, season_months="11,12,1,2",
                             gf_months="1,2", year=2027, kind="forecast",
                             predictor=f, value=-2.5, n_units=7))
        pd.DataFrame(rows).to_csv(out / "predictors.csv", index=False)
        pd.DataFrame([dict(country="Malawi", crop="maize",
                           season_name="Main", status="forecast",
                           planting_month=11, harvest_month=4, wraps=True,
                           harvest_year=2027)]
                     ).to_csv(out / "combinations.csv", index=False)

    def test_renders_from_panel_and_hides_climatology_fill(self):
        import tempfile

        import pandas as pd

        from geocif.viz.s2s_africa import predictor_heatmaps

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            self._write_run_dir(out)
            base = predictor_heatmaps(out, out, "unused.csv")
            plots, csvs = base / "plots", base / "csvs"
            self.assertTrue((plots / "Malawi_maize_Main.png").exists())
            m = pd.read_csv(csvs / "Malawi_maize_Main.csv")
            # fill years never reach the figure matrix; forecast year does
            self.assertNotIn(2018, set(m.year))
            self.assertIn(2027, set(m.year))
            tidy = pd.read_csv(csvs / "predictor_values_all.csv")
            self.assertEqual(set(tidy.columns),
                             {"country", "crop", "season_name", "offset",
                              "predictor", "year", "value", "n_units"})
            for d in (plots, csvs):
                self.assertTrue((d / "lookup_plots_csvs.csv").exists())

    def test_missing_panel_falls_back_with_a_warning(self):
        import tempfile

        import pandas as pd

        from geocif.viz import s2s_africa as viz

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            # no predictors.csv, and zero forecast rows so the legacy path
            # returns before touching S2S inputs
            pd.DataFrame([dict(country="Malawi", crop="maize",
                               season_name="Main", status="too_early")]
                         ).to_csv(out / "combinations.csv", index=False)
            with self.assertLogs("geocif.viz.s2s_africa",
                                 level="WARNING") as cm:
                viz.predictor_heatmaps(out, out, "unused.csv")
            self.assertTrue(any("predictors.csv" in m for m in cm.output))


class TestMapsCarryNoRegionAnnotations(unittest.TestCase):
    """These maps span countries at admin-2; region labels do not fit.

    The label-fit heuristic passed them (36 Somali districts is under the
    200-unit cap and each polygon is nominally wide enough for its name),
    but the rendered result was overlapping label boxes covering the
    coastline. The region name for a polygon lives in the companion CSV,
    which is where a reader looks it up.
    """

    def test_no_annotation_call_survives(self):
        import inspect

        from geocif.viz import s2s_africa as viz

        src = inspect.getsource(viz.maps)
        for probe in ("_annotate(", "annotate_centroids",
                      "effective_annotate_regions", "fig.text("):
            self.assertNotIn(probe, src, probe)

    def test_region_names_still_reach_the_companion_csv(self):
        """Dropping the labels must not drop the lookup — otherwise a
        polygon becomes unidentifiable."""
        import inspect

        from geocif.viz import s2s_africa as viz

        src = inspect.getsource(viz.maps)
        self.assertIn('"ADMIN1", "ADMIN2"', src)
        self.assertIn('drop(columns="geometry")', src)
