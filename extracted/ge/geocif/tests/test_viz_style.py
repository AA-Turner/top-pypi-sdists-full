# -*- coding: utf-8 -*-
"""Drift guards for the shared style module (geocif/viz/_style.py).

Every constant here used to be restated per module and every one of those
copies had drifted (NODATA in two colour systems, a despine missing the
orphaned-tick fix, a hand-mirrored annotation offset in two files). These
tests pin the single-home property so a copy cannot quietly come back.
"""
import unittest
from pathlib import Path

VIZ = Path(__file__).resolve().parents[1] / "geocif" / "viz"


class TestSingleHome(unittest.TestCase):
    def test_every_consumer_binds_the_same_objects(self):
        from geocif.viz import _style, leadtime, nass, plot, s2s_africa

        self.assertIs(s2s_africa.NODATA, _style.NODATA)
        self.assertIs(plot.NODATA, _style.NODATA)
        self.assertIs(s2s_africa.MON, _style.MONTHS)
        self.assertIs(leadtime._MONTHS, _style.MONTHS)
        self.assertIs(leadtime.style_ctx, _style.style_ctx)
        self.assertEqual(nass._MONTH_NUM["SEP"], 9)
        self.assertEqual(len(nass._MONTH_NUM), 12)

    def test_no_nodata_literal_outside_the_home_and_bridge(self):
        """_pygmt_render keeps NO literal (it dual-imports); the only hex
        spelling lives in _style. plot.py's mpl tuple is pinned below."""
        for f in VIZ.glob("*.py"):
            if f.name == "_style.py":
                continue
            src = f.read_text(encoding="utf-8")
            code = "\n".join(ln for ln in src.splitlines()
                             if not ln.lstrip().startswith("#")
                             and "``" not in ln)
            self.assertNotIn('"#d9d9d9"', code, f.name)

    def test_mpl_excluded_gray_matches_nodata(self):
        """plot._region_fill expresses NODATA as an RGBA tuple that a grep
        for the hex cannot find — this is the sync."""
        from matplotlib.colors import to_hex

        from geocif.viz import _style

        self.assertEqual(to_hex((0.85, 0.85, 0.85)), _style.NODATA)

    def test_annot_val_offset_is_derived_not_restated(self):
        from geocif.viz import _style

        self.assertEqual(_style.ANNOT_OFFSET, "0c/0.16c")
        self.assertEqual(_style.ANNOT_VAL_OFFSET, "0c/-0.16c")
        # derived in source, so changing ANNOT_OFFSET cannot un-mirror it
        src = (VIZ / "_style.py").read_text(encoding="utf-8")
        self.assertIn('ANNOT_VAL_OFFSET = "0c/-" + ANNOT_OFFSET', src)
        # and the raw mirror literal appears nowhere else in viz code
        for f in VIZ.glob("*.py"):
            if f.name == "_style.py":
                continue
            code = "\n".join(
                ln for ln in f.read_text(encoding="utf-8").splitlines()
                if not ln.lstrip().startswith("#"))
            self.assertNotIn('"0c/-0.16c"', code, f.name)

    def test_style_is_stdlib_only(self):
        """The whole point: importable by the pygmt bridge script and by
        GMT-free modules alike.

        Walks the tree rather than scanning tree.body, so a module-level
        `try: import matplotlib` (a Try node, not an Import node) or a
        second alias in `import a, b` cannot slip past.
        """
        import ast

        tree = ast.parse((VIZ / "_style.py").read_text(encoding="utf-8"))
        fn_bodies = {n for f in ast.walk(tree)
                     if isinstance(f, ast.FunctionDef)
                     for n in ast.walk(f)}
        top = set()
        for node in ast.walk(tree):
            if node in fn_bodies:
                continue                      # lazy imports are fine
            if isinstance(node, ast.Import):
                top |= {a.name.split(".")[0] for a in node.names}
            elif isinstance(node, ast.ImportFrom) and node.module:
                top.add(node.module.split(".")[0])
        self.assertLessEqual(top, {"logging"}, f"non-stdlib import: {top}")
        # and the heavy ones must be present ONLY inside functions
        lazy = set()
        for f in ast.walk(tree):
            if isinstance(f, ast.FunctionDef):
                for n in ast.walk(f):
                    if isinstance(n, ast.Import):
                        lazy |= {a.name.split(".")[0] for a in n.names}
        self.assertIn("matplotlib", lazy)

    def test_pygmt_render_dual_imports_for_the_bridge(self):
        """`python _pygmt_render.py` runs in a conda env with no geocif on
        the path; the same-directory fallback is what keeps it alive."""
        src = (VIZ / "_pygmt_render.py").read_text(encoding="utf-8")
        self.assertIn("from geocif.viz._style import", src)
        self.assertIn("except ImportError:", src)
        self.assertIn("from _style import", src)


class TestDespine(unittest.TestCase):
    """These run under rc_context({'xtick.top': True, 'ytick.right': True}).

    Without it the tests are vacuous: default rcParams already have
    top/right ticks off, so the orphaned-tick condition the helper exists
    to fix cannot manifest and a despine with the tick_params line deleted
    passes every assertion. scienceplots is what turns all four sides on,
    and it is not installed everywhere, so the rc_context stands in for it.
    """

    FOUR_SIDED = {"xtick.top": True, "ytick.right": True,
                  "xtick.labeltop": False, "ytick.labelright": False}

    @staticmethod
    def _axes():
        import matplotlib

        matplotlib.use("Agg", force=True)
        import matplotlib.pyplot as plt

        return plt

    def test_hides_spines_and_their_ticks(self):
        """The s2s copy had lost the tick_params line, leaving orphaned
        tick dashes floating where the hidden spines used to be."""
        import matplotlib

        plt = self._axes()
        from geocif.viz._style import despine

        with matplotlib.rc_context(self.FOUR_SIDED):
            fig, (ax1, ax2) = plt.subplots(1, 2)
            for ax in (ax1, ax2):
                self.assertTrue(
                    ax.xaxis.get_tick_params(which="major")["top"],
                    "fixture failed: ticks are not four-sided, so this "
                    "test cannot detect the regression it guards")
            despine(ax1, ax2)
            for ax in (ax1, ax2):
                self.assertFalse(ax.spines["top"].get_visible())
                self.assertFalse(ax.spines["right"].get_visible())
                self.assertTrue(ax.spines["left"].get_visible())
                # the ticks go with the spines, or they are left orphaned
                self.assertFalse(
                    ax.xaxis.get_tick_params(which="major")["top"])
                self.assertFalse(
                    ax.yaxis.get_tick_params(which="major")["right"])
            plt.close(fig)

    def test_left_despine_keeps_y_ticks_alive(self):
        """leadtime's crossing chart hides the left spine but still needs
        its y labels, so despine must never disable left ticks/labels."""
        import matplotlib

        plt = self._axes()
        from geocif.viz._style import despine

        with matplotlib.rc_context(self.FOUR_SIDED):
            fig, ax = plt.subplots()
            ax.barh(["alpha", "beta", "gamma"], [1, 2, 3])
            despine(ax, sides=("top", "right", "left"))
            self.assertFalse(ax.spines["left"].get_visible())
            # hard non-emptiness: get_ticklabels() FILTERS OUT invisible
            # labels, so `labels[0].get_visible() if labels else True`
            # silently passes exactly when the labels have vanished
            labels = ax.yaxis.get_ticklabels()
            self.assertTrue(labels, "y tick labels vanished entirely")
            self.assertTrue(all(t.get_visible() for t in labels))
            params = ax.yaxis.get_tick_params(which="major")
            self.assertTrue(params.get("labelleft", True))
            plt.close(fig)

    def test_no_inline_despine_survives_in_viz(self):
        """A new hand-rolled spine loop is the drift coming back."""
        import re

        offenders = []
        for f in VIZ.glob("*.py"):
            if f.name == "_style.py":
                continue
            src = f.read_text(encoding="utf-8")
            if re.search(r'spines\[.{0,30}\]\.set_visible\(False\)', src):
                offenders.append(f.name)
        self.assertEqual(offenders, [])


class TestStyleCtx(unittest.TestCase):
    def test_returns_a_usable_context(self):
        import matplotlib

        matplotlib.use("Agg", force=True)
        import matplotlib.pyplot as plt

        from geocif.viz._style import style_ctx

        with style_ctx():
            fig, ax = plt.subplots()
            plt.close(fig)

    def test_only_one_scienceplots_probe_in_viz(self):
        probes = [f.name for f in VIZ.glob("*.py")
                  if "import scienceplots" in f.read_text(encoding="utf-8")]
        self.assertEqual(probes, ["_style.py"])
