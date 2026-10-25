# -*- coding: utf-8 -*-
"""Tests for the snake chart plotting core (geocif/viz/snake.py).

What must hold: run splitting with a deadband (a step of exactly the
deadband is a step), lane assignment with the three-lane cap and no cap
between merged runs, the U-turn / S-bend choice (a flat step is not a
reversal), a drawn U-turn cap that is a true semicircle in pixel space, the
causality guard and the row cap in validate_tracks (a missing observation
date is allowed), no flipping of value_std by the plotter, clipped values
marked and annotated including the latest one, lanes of one row spaced by
LANE_GAP on the rendered figure, the dark arrow on the lane of the last
point, the house style (four spines off, labels on top, the resolved font
kept at save time, only ``geocif.viz._style`` imported), wrapped header
text, and both reference fixtures rendering into tests/output/.
"""
import ast
import unittest
from datetime import date
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyArrowPatch, PathPatch
from matplotlib.path import Path as MPath

from geocif.viz import snake

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"


def _tracks(rows, issues, *, roles=None, labels=None, displays=None, invert=None):
    """Tidy table from a {row: [values]} dict and a list of issue dates."""
    out = []
    for k, (row, vals) in enumerate(rows.items()):
        role = (roles or {}).get(row, "target" if k == 0 else "input")
        for d, v in zip(issues, vals):
            out.append({
                "row": row, "role": role, "issue_date": d, "value_std": v,
                "value_raw": np.nan, "unit": "", "invert": bool((invert or {}).get(row, False)),
                "obs_date": d - pd.Timedelta(days=1),
                **({"issue_label": labels[issues.index(d)]} if labels else {}),
                **({"display": displays[row]} if displays and row in displays else {}),
            })
    return pd.DataFrame(out)


# The NYT reference, approximate net-support readings from docs/reference/nyt_uturn.png.
NYT_ISSUES = [date(2020, 10, 1), date(2024, 10, 1), date(2026, 1, 1), date(2026, 10, 1)]
NYT_LABELS = ["2020", "2024", "Jan. 2026", "Oct. 2026"]
NYT_ROWS = {
    "Age 18-29": [-25, -7, -45, -58],
    "Nonwhite": [-38, -21, -46, -52],
    "All registered voters": [-7, 0, -14, -26],
    "Age 65+": [-7, -2, -6, -12],
    "White": [9, 8, 4, -12],
}

# The invented US corn mockup from the plan (standardized anomalies).
CORN_ISSUES = [date(2026, 6, 1), date(2026, 7, 1), date(2026, 8, 1), date(2026, 9, 1)]
CORN_ROWS = {
    "Yield forecast": [0.3, 0.6, -0.2, -0.7],
    "NDVI": [0.5, 0.8, 0.1, -0.6],
    "Soil moisture (ESI)": [0.2, -0.3, -0.9, -1.4],
    "Heat days": [0.1, -0.5, -1.2, -1.35],
    "Crop condition, USDA": [0.4, 0.7, 0.0, -0.5],
}
CORN_ROLES = {"Yield forecast": "target", "NDVI": "input", "Soil moisture (ESI)": "input",
              "Heat days": "input", "Crop condition, USDA": "independent"}
CORN_DISPLAY = {"Yield forecast": "176.8 bu/ac (−2.9)", "NDVI": "0.71 (−0.04)",
                "Soil moisture (ESI)": "ESI −1.2 (−0.4)", "Heat days": "18 days (+1)",
                "Crop condition, USDA": "CCI 348 (−11)"}


def nyt_tracks():
    return _tracks(NYT_ROWS, NYT_ISSUES, roles={r: "independent" for r in NYT_ROWS},
                   labels=NYT_LABELS)


def corn_tracks():
    return _tracks(CORN_ROWS, CORN_ISSUES, roles=CORN_ROLES, displays=CORN_DISPLAY,
                   invert={"Heat days": True})


def pts(v, pos=None):
    return "0 pts." if v == 0 else f"{v:+g}".replace("-", "−")


def _lane_patches(ax):
    """PathPatches that are straight lane runs (MOVETO/LINETO only)."""
    out = []
    for p in ax.patches:
        if isinstance(p, PathPatch) and not isinstance(p, FancyArrowPatch):
            codes = p.get_path().codes
            if codes is not None and set(codes) <= {MPath.MOVETO, MPath.LINETO}:
                out.append(p)
    return out


def _cap_patches(ax):
    """PathPatches that are U-turn caps (one MOVETO then six CURVE4)."""
    out = []
    for p in ax.patches:
        if isinstance(p, PathPatch) and not isinstance(p, FancyArrowPatch):
            codes = p.get_path().codes
            if codes is not None and len(codes) == 7 and list(codes[1:]) == [MPath.CURVE4] * 6:
                out.append(p)
    return out


def assert_no_overlap(case, fig, texts):
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    boxes = [t.get_window_extent(r) for t in texts]
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i], boxes[j]
            overlap = a.x0 < b.x1 and b.x0 < a.x1 and a.y0 < b.y1 and b.y0 < a.y1
            case.assertFalse(overlap, (texts[i].get_text(), texts[j].get_text()))


def _arrows(ax):
    return [p for p in ax.patches if isinstance(p, FancyArrowPatch)]


def _dots(ax, marker="o"):
    return [ln for ln in ax.lines if ln.get_marker() == marker]


class TestRuns(unittest.TestCase):
    def test_reversal_starts_a_run_sharing_the_turning_point(self):
        runs, dirs = snake.split_runs([0.3, 0.6, -0.2, -0.7], deadband=0.1)
        self.assertEqual(runs, [[0, 1], [1, 2, 3]])
        self.assertEqual(dirs, [1, -1])

    def test_monotonic_is_one_run(self):
        runs, dirs = snake.split_runs([0.2, -0.3, -0.9, -1.4], deadband=0.1)
        self.assertEqual(runs, [[0, 1, 2, 3]])
        self.assertEqual(dirs, [-1])

    def test_deadband_step_does_not_reverse(self):
        runs, dirs = snake.split_runs([0.0, 0.5, 0.45, 0.9], deadband=0.1)
        self.assertEqual(runs, [[0, 1, 2, 3]])
        self.assertEqual(dirs, [1])
        runs, _ = snake.split_runs([0.0, 0.5, 0.3, 0.9], deadband=0.1)
        self.assertEqual(len(runs), 3)

    def test_deadband_boundary_is_a_step_whatever_the_operands(self):
        # 0.5-0.4 and 0.2-0.1 differ in the last binary digit; both are steps
        self.assertEqual(len(snake.split_runs([0, 0.5, 0.4, 0.9])[0]), 3)
        self.assertEqual(len(snake.split_runs([0, 0.2, 0.1, 0.9])[0]), 3)
        self.assertEqual(len(snake.split_runs([0, 0.5, 0.35, 0.9])[0]), 3)
        self.assertEqual(snake.step_direction(0.5, 0.4, 0.1), -1)
        self.assertEqual(snake.step_direction(0.5, 0.45, 0.1), 0)
        self.assertEqual(snake.step_direction(5, 5, 0.0), 0)

    def test_flat_start_takes_the_first_real_direction(self):
        runs, dirs = snake.split_runs([0.0, 0.05, -0.5], deadband=0.1)
        self.assertEqual(runs, [[0, 1, 2]])
        self.assertEqual(dirs, [-1])

    def test_lanes_cap_at_max_and_merge_the_earliest(self):
        self.assertEqual(snake.assign_lanes([[0], [1], [2]], 3), ([0, 1, 2], False))
        lanes, merged = snake.assign_lanes([[0]] * 5, 3)
        self.assertEqual(lanes, [0, 0, 0, 1, 2])
        self.assertTrue(merged)

    def test_lanes_merge_the_smallest_reversal_not_the_earliest(self):
        # Afghanistan poppy, Southern 2026 rainfall: a 1.2 sigma drop after the
        # wet January must keep its U-turn; the 0.2 sigma June dip shares a lane
        vals = [-1.147, -1.180, 0.911, -0.314, -0.104, 0.134, -0.087, -0.102]
        runs, _ = snake.split_runs(vals, deadband=0.1)
        self.assertEqual(runs, [[0, 1, 2], [2, 3], [3, 4, 5], [5, 6, 7]])
        self.assertEqual(snake.assign_lanes(runs, 3, vals), ([0, 1, 2, 2], True))
        plan = snake.layout_row(vals, list(range(8)))
        self.assertEqual(plan["connectors"], ["uturn", "uturn", "same"])

    def test_connector_kind(self):
        self.assertEqual(snake.connector_kind(1, -1), "uturn")
        self.assertEqual(snake.connector_kind(-1, -1), "sbend")
        self.assertEqual(snake.connector_kind(0, -1), "sbend")

    def test_split_layout_matches_the_nyt_rows(self):
        up = snake.layout_row([-25, -7, -45, -58], [0, 1, 2, 3], layout="split", split=1)
        self.assertEqual(up["runs"], [[0, 1], [1, 2, 3]])
        self.assertEqual(up["connectors"], ["uturn"])
        self.assertEqual(up["turn_dirs"][0], 1)          # the cap bulges to the right
        self.assertEqual(up["point_lane"], [0, 0, 1, 1])
        white = snake.layout_row([9, 8, 4, -12], [0, 1, 2, 3], layout="split", split=1)
        self.assertEqual(white["connectors"], ["sbend"])

    def test_split_uses_the_travel_direction_into_the_turn(self):
        # upper lane goes left then right: the cap must bulge right, not left
        plan = snake.layout_row([0, -10, -5, -30], [0, 1, 2, 3], layout="split", split=2)
        self.assertEqual(plan["connectors"], ["uturn"])
        self.assertEqual(plan["turn_dirs"][0], 1)
        # a flat step before the split is not a reversal
        flat = snake.layout_row([5, 5, 10, 12], [0, 1, 2, 3], layout="split", split=1)
        self.assertEqual(flat["connectors"], ["sbend"])

    def test_split_index_is_a_figure_wide_issue_index(self):
        # a row missing the first issue still turns at issue 1
        plan = snake.layout_row([-7, -45, -58], [1, 2, 3], layout="split", split=1)
        self.assertEqual(plan["runs"], [[0], [0, 1, 2]])
        self.assertEqual(plan["point_lane"], [0, 1, 1])

    def test_runs_layout_lanes_for_the_corn_mockup(self):
        two = snake.layout_row(CORN_ROWS["Yield forecast"], [0, 1, 2, 3])
        self.assertEqual(two["n_lanes"], 2)
        self.assertEqual(two["connectors"], ["uturn"])
        one = snake.layout_row(CORN_ROWS["Heat days"], [0, 1, 2, 3])
        self.assertEqual(one["n_lanes"], 1)

    def test_a_dip_inside_the_deadband_does_not_cancel_a_reversal(self):
        # right, a -0.03 dip (inside the deadband), then left: a U-turn
        plan = snake.layout_row([-0.119, 0.16, 0.131, -0.054], [0, 1, 2, 3], deadband=0.1)
        self.assertEqual(plan["runs"], [[0, 1, 2], [2, 3]])
        self.assertEqual(plan["connectors"], ["uturn"])
        self.assertEqual(plan["turn_dirs"][0], 1)

    def test_auto_limits_leave_room_for_the_cap(self):
        rows = {"Yield forecast": [0.3, 0.6, -0.2, -0.7], "NDVI": [1.0, 1.94, 2.5, 2.29]}
        fig, ax = snake.plot_snake(_tracks(rows, CORN_ISSUES))
        lo, hi = ax.get_xlim()
        for cap in _cap_patches(ax):
            v = cap.get_path().vertices
            self.assertLessEqual(v[:, 0].max(), hi)
            self.assertGreaterEqual(v[:, 0].min(), lo)
        self.assertEqual(hi, 3.0)
        plt.close(fig)

    def test_small_wiggles_stay_on_one_lane(self):
        # the Kenya 2026 yield row: right, left, left, right, all but one step
        # inside the 0.1 sigma deadband -> one lane, no curve
        kenya = [-0.066, -0.057, -0.14, -0.494, -0.476]
        plan = snake.layout_row(kenya, list(range(5)))
        self.assertEqual(plan["runs"], [[0, 1, 2, 3, 4]])
        self.assertEqual(plan["connectors"], [])
        fig, ax = snake.plot_snake(_tracks({"Yield forecast": kenya,
                                            "NDVI": [1.45, 1.31, 1.05, 0.57, 0.15]},
                                           [date(2026, m, 1) for m in range(5, 10)]))
        caps = [c for c in _cap_patches(ax) if np.mean(c.get_path().vertices[:, 1]) < 1]
        self.assertEqual(caps, [])
        plt.close(fig)
        # deadband=0 gives every reversal its own lane
        plan0 = snake.layout_row(kenya, list(range(5)), deadband=0.0)
        self.assertEqual(plan0["lanes"], [0, 1, 2])
        self.assertEqual(plan0["connectors"], ["uturn", "uturn"])

    def test_no_headers_and_no_change_by_default(self):
        t = _tracks({"Yield forecast": [0.3, 0.6, -0.2, -0.7], "NDVI": [0.5, 0.8, 0.1, -0.6]},
                    CORN_ISSUES)
        t["value_raw"] = [4.6, 4.7, 4.5, 4.4, 0.6, 0.7, 0.65, 0.62]
        t["unit"] = ["t/ha"] * 4 + [""] * 4
        fig, ax = snake.plot_snake(t)
        texts = [x.get_text() for x in ax.texts]
        for header in ("Indicator", "Standardized anomaly", "Latest"):
            self.assertFalse(any(header in x for x in texts), header)
        self.assertIn("4.40 t/ha", texts)
        self.assertFalse(any("(" in x for x in texts if "t/ha" in x))
        # the header band shrinks to the tick labels
        self.assertAlmostEqual(fig.get_size_inches()[1], snake.figure_size(2, headers=False)[1])
        plt.close(fig)

    def test_roles_and_footer_off_by_default(self):
        fig, ax = snake.plot_snake(corn_tracks())
        texts = [t.get_text() for t in ax.texts] + [t.get_text() for t in fig.texts]
        self.assertFalse(any(r in texts for r in snake.ROLE_TEXT.values()))
        self.assertEqual(fig.texts, [])
        plt.close(fig)

    def test_merged_runs_have_no_connector(self):
        plan = snake.layout_row([0.0, 0.5, -0.5, 0.5, -0.5, 0.5], list(range(6)))
        self.assertTrue(plan["merged"])
        self.assertEqual(plan["lanes"], [0, 0, 0, 1, 2])
        self.assertEqual(plan["connectors"], ["same", "same", "uturn", "uturn"])

    def test_lane_y_is_centred(self):
        self.assertAlmostEqual(snake.lane_y(0.5, 0, 1), 0.5)
        self.assertAlmostEqual(snake.lane_y(0.5, 0, 2), 0.5 - snake.LANE_GAP / 2)
        self.assertAlmostEqual(snake.lane_y(0.5, 1, 2), 0.5 + snake.LANE_GAP / 2)

    def test_bad_layout_and_label_rows_are_refused(self):
        with self.assertRaises(ValueError):
            snake.layout_row([1, 2], [0, 1], layout="zigzag")
        with self.assertRaises(ValueError):
            snake.plot_snake(corn_tracks(), label_rows="frist")


class TestCapGeometry(unittest.TestCase):
    def test_cap_formula(self):
        fig, ax = plt.subplots(figsize=(7, 5))
        fig.subplots_adjust(left=0.27, right=0.8, top=0.85, bottom=0.1)
        ax.set_xlim(-2, 2)
        ax.set_ylim(5, 0)
        bulge = snake.cap_bulge(ax, snake.LANE_GAP)
        px_x, px_y = snake.px_per_unit(ax)
        self.assertLessEqual(abs(bulge * px_x - snake.LANE_GAP * px_y / 2), 1.0)
        verts, codes = snake.cap_path(0.0, 1.0, 1.0 + snake.LANE_GAP, bulge)
        self.assertEqual(len(verts), 7)
        self.assertAlmostEqual(verts[3][0], bulge)
        self.assertAlmostEqual(verts[3][1], 1.0 + snake.LANE_GAP / 2)
        plt.close(fig)

    def test_drawn_caps_are_semicircles_in_pixels(self):
        fig, ax = snake.plot_snake(corn_tracks())
        fig.canvas.draw()
        caps = _cap_patches(ax)
        self.assertEqual(len(caps), 3)                   # yield, NDVI, crop condition
        for cap in caps:
            v = ax.transData.transform(cap.get_path().vertices)
            radius_px = abs(v[6, 1] - v[0, 1]) / 2
            self.assertLessEqual(abs(abs(v[3, 0] - v[0, 0]) - radius_px), 1.0)
            # the quarter-arc control points lie at the Bézier circle constant
            self.assertLessEqual(abs(abs(v[1, 0] - v[0, 0]) - snake.KAPPA * radius_px), 1.0)
            self.assertGreater(radius_px, 5)
        plt.close(fig)

    def test_sbend_endpoints(self):
        verts, _ = snake.sbend_path(8, 1.0, 4, 1.35)
        self.assertEqual(verts[0], (8, 1.0))
        self.assertEqual(verts[-1], (4, 1.35))


class TestValidate(unittest.TestCase):
    def test_causality_guard_fires(self):
        t = corn_tracks()
        t.loc[0, "obs_date"] = t.loc[0, "issue_date"] + pd.Timedelta(days=3)
        with self.assertRaises(ValueError) as cm:
            snake.validate_tracks(t)
        self.assertIn("causality", str(cm.exception))

    def test_missing_obs_dates_are_allowed(self):
        t = corn_tracks()
        t["obs_date"] = pd.to_datetime(t["obs_date"])
        t.loc[0, "obs_date"] = pd.NaT                    # datetime64 column with a NaT
        out = snake.validate_tracks(t)
        self.assertIsNone(out.loc[0, "obs_date"])
        self.assertEqual(out.loc[1, "obs_date"], CORN_ISSUES[1] - pd.Timedelta(days=1))
        t2 = corn_tracks()
        t2["obs_date"] = None
        self.assertEqual(len(snake.validate_tracks(t2)), 20)

    def test_input_frame_is_not_modified(self):
        t = corn_tracks()
        before = t.copy()
        snake.validate_tracks(t)
        pd.testing.assert_frame_equal(t, before)

    def test_more_than_four_indicators_raise(self):
        rows = dict(CORN_ROWS)
        rows["Rainfall"] = [0.1, 0.2, 0.3, 0.4]
        t = _tracks(rows, CORN_ISSUES, roles={**CORN_ROLES, "Rainfall": "input"})
        with self.assertRaises(ValueError):
            snake.validate_tracks(t)

    def test_exactly_one_target(self):
        t = corn_tracks()
        t.loc[t["row"] == "NDVI", "role"] = "target"
        with self.assertRaises(ValueError):
            snake.validate_tracks(t)
        self.assertEqual(len(snake.validate_tracks(nyt_tracks(), require_target=False)), 20)

    def test_unknown_role_and_non_bool_invert(self):
        t = corn_tracks()
        t.loc[0, "role"] = "feature"
        with self.assertRaises(ValueError):
            snake.validate_tracks(t)
        t = corn_tracks()
        t["invert"] = 0
        with self.assertRaises(ValueError):
            snake.validate_tracks(t)

    def test_nan_values_are_gaps_not_errors(self):
        t = corn_tracks()
        t.loc[(t["row"] == "NDVI") & (t["issue_date"] == CORN_ISSUES[1]), "value_std"] = np.nan
        out = snake.validate_tracks(t)
        self.assertEqual(len(out), 19)

    def test_plotter_does_not_flip_inverted_rows(self):
        t = corn_tracks()
        fig, ax = snake.plot_snake(t, label_rows="none")
        heat_x = [ln.get_xdata()[0] for ln in _dots(ax) if abs(ln.get_ydata()[0] - 3.5) < 0.5]
        self.assertTrue(any(abs(x - 0.1) < 1e-9 for x in heat_x))
        plt.close(fig)


class TestText(unittest.TestCase):
    def test_sigma_labels_use_unicode_minus(self):
        self.assertEqual(snake.sigma_formatter(-2), "−2σ")
        self.assertEqual(snake.sigma_formatter(0), "0")
        self.assertEqual(snake.sigma_formatter(1), "+1σ")
        self.assertEqual(snake.fmt_signed(-0.004), "+0.00")
        self.assertEqual(snake.fmt_signed(-0.006), "−0.01")

    def test_default_display(self):
        g = pd.DataFrame({"issue_date": CORN_ISSUES[:2], "value_raw": [4.83, 4.62],
                          "unit": ["t/ha", "t/ha"]})
        self.assertEqual(snake.default_display(g), "4.62 t/ha")
        self.assertEqual(snake.default_display(g, change=True), "4.62 t/ha (−0.21)")
        neg = pd.DataFrame({"issue_date": CORN_ISSUES[:2], "value_raw": [-0.8, -1.2],
                            "unit": ["", ""]})
        self.assertEqual(snake.default_display(neg, change=True), "−1.20 (−0.40)")
        self.assertNotIn("-", snake.default_display(neg, change=True))

    def test_suggest_title_and_source_line(self):
        title = snake.suggest_title(corn_tracks())
        self.assertIn("Yield forecast weakened", title)
        self.assertIn("September", title)
        line = snake.source_line({"issues": CORN_ISSUES, "sources": ["GEOCIF tabpfn", "NDVI"],
                                  "baseline": (2015, 2025), "target_year": 2026,
                                  "notes": ["Earlier 2026 issues are re-forecasts"]})
        self.assertTrue(line.endswith("Right = more favorable for yield."))
        self.assertIn("Baseline 2015-2025, 2026 excluded", line)
        self.assertIn("Issues Jun to Sep 2026", line)

    def test_wrapping_grows_the_header_and_keeps_the_width(self):
        long_title = "A " * 60 + "long headline"
        w, h_long = snake.figure_size(5, title=long_title)
        _, h_short = snake.figure_size(5, title="Short")
        self.assertEqual(w, 7.0)
        self.assertGreater(h_long, h_short)
        _, h2 = snake.figure_size(2)
        _, h5 = snake.figure_size(5)
        self.assertAlmostEqual(h5 - h2, 3 * snake.ROW_IN)
        fig, ax = snake.plot_snake(corn_tracks(), title=long_title,
                                   subtitle="word " * 80, source="source " * 60)
        self.assertEqual(tuple(fig.get_size_inches()), (7.0, snake.figure_size(
            5, title=long_title, subtitle="word " * 80, source="source " * 60,
            headers=False)[1]))
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        fig_w = fig.get_size_inches()[0] * fig.dpi
        for t in fig.texts:
            self.assertIn("\n", t.get_text())
            self.assertLessEqual(t.get_window_extent(renderer).x1, fig_w + 1)
        plt.close(fig)

    def test_long_row_labels_wrap(self):
        rows = {"A very long indicator name that would overrun": [0.1, 0.2, 0.3, 0.4],
                "NDVI": [0.5, 0.8, 0.1, -0.6]}
        fig, ax = snake.plot_snake(_tracks(rows, CORN_ISSUES))
        labels = [t.get_text() for t in ax.texts if t.get_text().startswith("A very long")]
        self.assertEqual(len(labels), 1)
        self.assertIn("\n", labels[0])
        self.assertTrue(labels[0].startswith("A very long indicator\n"))
        self.assertLessEqual(labels[0].count("\n"), 1)      # at most two lines, then an ellipsis
        self.assertTrue(labels[0].endswith(chr(8230)))
        plt.close(fig)


class TestStyle(unittest.TestCase):
    def test_only_style_is_imported_from_geocif(self):
        src = (HERE.parent / "geocif" / "viz" / "snake.py").read_text(encoding="utf-8")
        tree = ast.parse(src)
        mods = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                mods.add(node.module)
            elif isinstance(node, ast.Import):
                mods.update(a.name for a in node.names)
        geocif_mods = {m for m in mods if m.startswith("geocif")}
        self.assertEqual(geocif_mods, {"geocif.viz._style"})
        self.assertNotIn("plt.style.use", src)
        self.assertNotIn("import scienceplots", src)

    def test_spines_off_labels_on_top(self):
        fig, ax = snake.plot_snake(corn_tracks())
        fig.canvas.draw()
        self.assertFalse(any(sp.get_visible() for sp in ax.spines.values()))
        ticks = ax.xaxis.get_major_ticks()
        self.assertTrue(all(t.label2.get_visible() for t in ticks))
        self.assertFalse(any(t.label1.get_visible() for t in ticks))
        self.assertFalse(any(t.tick1line.get_visible() or t.tick2line.get_visible()
                             for t in ticks))
        self.assertEqual(ax.get_xlim(), (-2.0, 2.0))
        labels = [t.label2.get_text() for t in ticks]
        self.assertIn("0", labels)
        self.assertIn("−2σ", labels)
        plt.close(fig)

    def test_symmetric_limit_rule(self):
        self.assertEqual(snake.symmetric_xmax([2.3]), 2.5)
        self.assertEqual(snake.symmetric_xmax([2.5]), 2.5)
        self.assertEqual(snake.symmetric_xmax([0.4]), 2.0)
        self.assertEqual(snake.symmetric_xmax([-2.01]), 2.5)
        t = corn_tracks()
        t.loc[(t["row"] == "NDVI") & (t["issue_date"] == CORN_ISSUES[1]), "value_std"] = 2.3
        fig, ax = snake.plot_snake(t)
        # 2.3 plus room for a cap and the round stroke end rounds up to 3.0
        self.assertEqual(ax.get_xlim(), (-3.0, 3.0))
        plt.close(fig)

    def test_font_is_concrete_and_survives_the_context(self):
        before = list(matplotlib.rcParams["font.family"])
        fig, ax = snake.plot_snake(corn_tracks())
        self.assertEqual(list(matplotlib.rcParams["font.family"]), before)
        fam = snake.resolve_font_family()
        for t in ax.texts + fig.texts:
            self.assertEqual(t.get_fontfamily()[0], fam)
        for t in ax.xaxis.get_major_ticks():
            self.assertEqual(t.label2.get_fontfamily()[0], fam)
        plt.close(fig)

    def test_no_arrows_dots_darken_by_issue_month(self):
        fig, ax = snake.plot_snake(corn_tracks())
        self.assertEqual(_arrows(ax), [])
        colors = snake.issue_colors(4)
        self.assertEqual(colors, snake.issue_colors(4, "viridis"))  # the default
        self.assertEqual(snake.issue_colors(4, "blues")[0], snake.DOT_LIGHT)
        self.assertEqual(snake.issue_colors(4, "blues")[-1], snake.DOT_DARK)

        def luminance(c):
            r, g, b = matplotlib.colors.to_rgb(c)
            return 0.2126 * r + 0.7152 * g + 0.0722 * b

        lum = [luminance(c) for c in colors]
        self.assertEqual(lum, sorted(lum, reverse=True))          # light -> dark
        # every dot takes its issue month's colour, the same in every row
        x_to_step = {}
        for row, vals in CORN_ROWS.items():
            for k, v in enumerate(vals):
                x_to_step.setdefault(round(v, 6), set()).add(k)
        dots = _dots(ax)
        self.assertEqual(len(dots), 20)
        for ln in dots:
            k = x_to_step[round(ln.get_xdata()[0], 6)]
            self.assertIn(matplotlib.colors.to_hex(ln.get_markerfacecolor()), {colors[j] for j in k})
        # later issues sit on top of earlier ones
        last = [ln for ln in dots if matplotlib.colors.to_hex(ln.get_markerfacecolor()) == colors[-1]]
        first = [ln for ln in dots if matplotlib.colors.to_hex(ln.get_markerfacecolor()) == colors[0]]
        self.assertGreater(min(ln.get_zorder() for ln in last), max(ln.get_zorder() for ln in first))
        plt.close(fig)

    def test_palettes(self):
        for name in snake.PALETTES:
            cols = snake.issue_colors(5, name)
            self.assertEqual(len(cols), 5)
            self.assertEqual(len(set(cols)), 5, name)
        acc = snake.issue_colors(4, "accent")
        self.assertEqual(acc[-1], "#d95f02")
        self.assertEqual(snake.issue_colors(3, ["#000000", "#111111", "#222222"]),
                         ["#000000", "#111111", "#222222"])
        self.assertEqual(len(snake.issue_colors(3, "cividis")), 3)
        fig, ax = snake.plot_snake(corn_tracks(), palette="oranges")
        legend = [matplotlib.colors.to_hex(h.get_markerfacecolor())
                  for h in ax.get_legend().legend_handles]
        self.assertEqual(legend, snake.issue_colors(4, "oranges"))
        plt.close(fig)

    def test_month_key_under_the_axes(self):
        fig, ax = snake.plot_snake(corn_tracks())
        leg = ax.get_legend()
        self.assertIsNotNone(leg)
        self.assertEqual([t.get_text() for t in leg.get_texts()], ["Jun", "Jul", "Aug", "Sep"])
        fig.canvas.draw()
        r = fig.canvas.get_renderer()
        self.assertLess(leg.get_window_extent(r).y1, ax.get_window_extent(r).y0 + 1)
        self.assertGreaterEqual(leg.get_window_extent(r).y0, 0)
        plt.close(fig)
        fig, ax = snake.plot_snake(corn_tracks(), show_key=False)
        self.assertIsNone(ax.get_legend())
        plt.close(fig)

    def test_change_column_is_against_normal(self):
        g = pd.DataFrame({"issue_date": CORN_ISSUES[:2], "value_raw": [374.0, 514.6],
                          "unit": ["mm", "mm"], "normal_raw": [642.8, 852.9]})
        # 2026 added 140.6 mm while a normal August adds 210.1 mm: (514.6 - 852.9) - (374.0 - 642.8)
        self.assertEqual(snake.default_display(g, change=True), "514.6 mm (\u221269.5)")


class TestDrawing(unittest.TestCase):
    def test_lanes_of_one_row_are_lane_gap_apart(self):
        fig, ax = snake.plot_snake(corn_tracks())
        lanes = _lane_patches(ax)
        self.assertGreaterEqual(len(lanes), 8)      # 3 two-lane rows + 2 one-lane rows
        by_row = {}
        for p in lanes:
            v = p.get_path().vertices
            y = float(np.mean(v[:, 1]))
            by_row.setdefault(int(np.floor(y)), []).append((v[:, 0].min(), v[:, 0].max(), y))
        for row, segs in by_row.items():
            for i in range(len(segs)):
                for j in range(i + 1, len(segs)):
                    a, b = segs[i], segs[j]
                    if a[0] <= b[1] and b[0] <= a[1]:            # x extents overlap
                        self.assertGreaterEqual(abs(a[2] - b[2]), snake.LANE_GAP - 1e-9)
        ys = sorted(round(s[2], 3) for s in by_row[0])
        self.assertEqual(ys, [round(0.5 - snake.LANE_GAP / 2, 3), round(0.5 + snake.LANE_GAP / 2, 3)])
        plt.close(fig)

    def test_latest_dot_sits_on_the_last_lane(self):
        fig, ax = snake.plot_snake(corn_tracks())
        dark = [ln for ln in _dots(ax)
                if matplotlib.colors.to_hex(ln.get_markerfacecolor()) == snake.issue_colors(4)[-1]]
        self.assertEqual(len(dark), 5)
        for i, row in enumerate(CORN_ROWS):
            plan = snake.layout_row(CORN_ROWS[row], [0, 1, 2, 3])
            y_expect = snake.lane_y(i + 0.5, plan["point_lane"][-1], plan["n_lanes"])
            hit = [ln for ln in dark if abs(ln.get_ydata()[0] - y_expect) < 1e-9
                   and abs(ln.get_xdata()[0] - CORN_ROWS[row][-1]) < 1e-9]
            self.assertEqual(len(hit), 1, row)
        plt.close(fig)

    def test_month_labels_on_the_first_row_only(self):
        fig, ax = snake.plot_snake(corn_tracks())               # default: no labels, the key names them
        self.assertEqual([t for t in ax.texts if t.get_text() in ("Jun", "Jul", "Aug", "Sep")], [])
        plt.close(fig)
        fig, ax = snake.plot_snake(corn_tracks(), label_rows="first")
        months = [t for t in ax.texts if t.get_text() in ("Jun", "Jul", "Aug", "Sep")]
        self.assertEqual(len(months), 4)
        self.assertTrue(all(0 <= t.xy[1] <= 1 for t in months))
        plt.close(fig)
        fig, ax = snake.plot_snake(corn_tracks(), label_rows="all")
        self.assertEqual(len([t for t in ax.texts if t.get_text() in ("Jun", "Jul", "Aug", "Sep")]), 20)
        plt.close(fig)
        fig, ax = snake.plot_snake(corn_tracks(), label_rows="none")
        self.assertEqual(len([t for t in ax.texts if t.get_text() in ("Jun", "Jul", "Aug", "Sep")]), 0)
        plt.close(fig)

    def test_missing_issue_draws_a_dashed_gap_in_place(self):
        t = corn_tracks()
        t = t[~((t["row"] == "NDVI") & (t["issue_date"] == CORN_ISSUES[1]))]
        fig, ax = snake.plot_snake(t)
        dashed = [ln for ln in ax.lines if ln.get_linestyle() not in ("-", "None", "none")]
        self.assertEqual(len(dashed), 1)
        self.assertEqual(list(dashed[0].get_xdata()), [0.5, 0.1])
        self.assertEqual(list(dashed[0].get_ydata()), [1.5, 1.5])
        ndvi = [p for p in _lane_patches(ax) if 1 < np.mean(p.get_path().vertices[:, 1]) < 2]
        self.assertEqual(len(ndvi), 1)
        xs = ndvi[0].get_path().vertices[:, 0]
        self.assertEqual((round(xs.min(), 6), round(xs.max(), 6)), (-0.6, 0.1))
        plt.close(fig)

    def test_merged_lanes_label_every_dot_without_a_cap_stub(self):
        zig = {"Yield forecast": [0.0, 0.5, -0.5, 0.5, -0.5, 0.5],
               "NDVI": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]}
        issues = [date(2026, m, 1) for m in range(4, 10)]
        fig, ax = snake.plot_snake(_tracks(zig, issues), label_rows="first")
        caps = _cap_patches(ax)
        self.assertEqual(len(caps), 2)                   # only the two lane changes
        pad = 1e-6
        for p in ax.patches:
            if isinstance(p, PathPatch) and not isinstance(p, FancyArrowPatch):
                v = p.get_path().vertices
                if np.mean(v[:, 1]) < 1 and not any(np.array_equal(v, c.get_path().vertices) for c in caps):
                    self.assertGreaterEqual(v[:, 0].min(), -0.5 - pad)
                    self.assertLessEqual(v[:, 0].max(), 0.5 + pad)
        texts = [t for t in ax.texts if t.get_text() in ("Apr", "May", "Jun", "Jul", "Aug", "Sep")]
        # with labels on, the merged row labels its dots; May and Jul sit on
        # the same spot, so one of the two is dropped, never overprinted
        self.assertEqual(len(texts), 5)
        self.assertIn("Sep", [t.get_text() for t in texts])
        self.assertTrue(all(t.xy[1] < 1 for t in texts))
        assert_no_overlap(self, fig, texts)
        plt.close(fig)

    def test_crowded_labels_never_overlap_and_keep_the_latest(self):
        crowd = {"Yield forecast": [-0.066, -0.057, -0.14, -0.494, -0.476],
                 "NDVI": [1.45, 1.31, 1.05, 0.57, 0.15]}
        issues = [date(2026, m, 1) for m in range(5, 10)]
        fig, ax = snake.plot_snake(_tracks(crowd, issues), xmax=3, label_rows="first")
        texts = [t for t in ax.texts if t.get_text() in ("May", "Jun", "Jul", "Aug", "Sep")]
        self.assertIn("Sep", [t.get_text() for t in texts])
        self.assertGreaterEqual(len(texts), 3)
        assert_no_overlap(self, fig, texts)
        # no label sits on a dot of its row
        fig.canvas.draw()
        r = fig.canvas.get_renderer()
        for t in texts:
            bb = t.get_window_extent(r)
            for ln in _dots(ax):
                if ln.get_ydata()[0] < 1:
                    cx, cy = ax.transData.transform((ln.get_xdata()[0], ln.get_ydata()[0]))
                    self.assertFalse(bb.x0 < cx < bb.x1 and bb.y0 < cy < bb.y1)
        plt.close(fig)

    def test_clipped_values_are_marked_and_annotated_including_the_last(self):
        t = corn_tracks()
        t.loc[(t["row"] == "NDVI") & (t["issue_date"] == CORN_ISSUES[1]), "value_std"] = 3.4
        fig, ax = snake.plot_snake(t, xmax=2)
        texts = [a.get_text() for a in ax.texts]
        self.assertTrue(any("+3.4σ" in s for s in texts))
        self.assertEqual(len(_dots(ax, ">")), 1)
        plt.close(fig)
        # a clipped LAST value: a wedge at the edge in the latest colour, true value written
        t = corn_tracks()
        t.loc[(t["row"] == "NDVI") & (t["issue_date"] == CORN_ISSUES[3]), "value_std"] = -3.4
        fig, ax = snake.plot_snake(t, xmax=2)
        self.assertTrue(any("−3.4σ" in a.get_text() for a in ax.texts))
        wedge = [ln for ln in _dots(ax, "<") if 1 < ln.get_ydata()[0] < 2]
        self.assertEqual(len(wedge), 1)
        self.assertAlmostEqual(wedge[0].get_xdata()[0], -2.0)
        self.assertEqual(matplotlib.colors.to_hex(wedge[0].get_markerfacecolor()),
                         snake.issue_colors(4)[-1])
        plt.close(fig)
        # asymmetric limits clip each side independently and annotate every clipped point
        fig, ax = snake.plot_snake(corn_tracks(), xlim=(-1, 4))
        clipped = [v for vals in CORN_ROWS.values() for v in vals if v < -1 or v > 4]
        ann = [a for a in ax.texts if a.get_text().endswith("σ") and a.get_text()[0] == "−"]
        self.assertEqual(len(ann), len(clipped))
        self.assertEqual({ln.get_marker() for ln in _dots(ax, "<") + _dots(ax, ">")}, {"<"})
        plt.close(fig)


class TestFixtures(unittest.TestCase):
    """The two reference figures render and land in tests/output/."""

    def test_nyt_split_fixture(self):
        t = nyt_tracks()
        fig, ax = snake.plot_snake(
            t, layout="split", split=1, highlight="All registered voters",
            show_roles=False, show_values=False, require_target=False,
            tick_formatter=pts, xlabel="Net support", gutter_label="Group",
            xlim=(-65, 15), xtick_step=10, label_rows="first",
            title="How support for Trump has changed",
            subtitle="Fixture reproducing the NYT chart layout from approximate readings "
                     "of the reference screenshot; values are net support points.",
            source="Source: New York Times/Siena University polls as read from "
                   "docs/reference/nyt_uturn.png. Fixture for geocif.viz.snake.")
        self.assertEqual(ax.get_xlim(), (-65.0, 15.0))
        self.assertEqual(_dots(ax, "<") + _dots(ax, ">"), [])
        for ln in _dots(ax):
            self.assertTrue(-65 <= ln.get_xdata()[0] <= 15)
        self.assertEqual(len(_cap_patches(ax)), 4)          # all rows but White turn
        self.assertEqual(_arrows(ax), [])
        self.assertEqual(len(_dots(ax)), 20)
        written = snake.save_snake(fig, OUT / "snake_fixture_nyt_split")
        self.assertEqual({p.suffix for p in written}, {".png", ".pdf"})
        self.assertTrue(all(p.exists() and p.stat().st_size > 0 for p in written))
        from PIL import Image

        with Image.open(OUT / "snake_fixture_nyt_split.png") as im:
            self.assertAlmostEqual(im.info["dpi"][0], 300, delta=1)
        plt.close(fig)

    def test_nyt_fixture_clips_a_value_beyond_the_left_edge(self):
        t = nyt_tracks()
        t.loc[(t["row"] == "Age 18-29") & (t["issue_date"] == NYT_ISSUES[2]), "value_std"] = -70
        fig, ax = snake.plot_snake(t, layout="split", split=1, require_target=False,
                                   tick_formatter=pts, xlim=(-65, 15), xtick_step=10,
                                   show_roles=False, show_values=False)
        wedges = _dots(ax, "<")
        self.assertEqual(len(wedges), 1)
        self.assertAlmostEqual(wedges[0].get_xdata()[0], -65)
        self.assertIn(pts(-70), [a.get_text() for a in ax.texts])
        plt.close(fig)

    def test_corn_runs_fixture(self):
        t = corn_tracks()
        fig, ax = snake.plot_snake(
            t, title=snake.suggest_title(t),
            subtitle="Invented US corn values from the plan; two-lane rows turn after July.",
            source=snake.source_line({"issues": CORN_ISSUES,
                                      "sources": ["GEOCIF (mockup)", "NDVI", "ESI", "USDA NASS"],
                                      "baseline": (2005, 2025), "target_year": 2026}))
        for row, expect_lanes in [("Yield forecast", 2), ("NDVI", 2), ("Soil moisture (ESI)", 1),
                                  ("Heat days", 1), ("Crop condition, USDA", 2)]:
            plan = snake.layout_row(CORN_ROWS[row], [0, 1, 2, 3])
            self.assertEqual(plan["n_lanes"], expect_lanes, row)
        self.assertEqual(fig.get_size_inches()[0], 7.0)
        written = snake.save_snake(fig, OUT / "snake_fixture_corn_runs")
        self.assertEqual({p.suffix for p in written}, {".png", ".pdf"})
        plt.close(fig)


if __name__ == "__main__":
    unittest.main()
