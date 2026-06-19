"""Regression tests for ``geocif.viz.diagnostics``.

Currently pins matplotlib >= 3.11 compatibility: the ``labels=`` kwarg
on ``Axes.boxplot`` was deprecated in 3.9 and REMOVED in 3.11. The
HPC env (matplotlib 3.11.0) crashes with::

    TypeError: Axes.boxplot() got an unexpected keyword argument 'labels'

while older matplotlib accepts ``labels=`` with only a DeprecationWarning.
A behavioural smoke test passes silently on the older matplotlib, so
this test is source-based — it catches the regression on every
matplotlib version.
"""
import inspect
import re
import unittest


# Regex for `labels=` as a kwarg position — preceded by a non-word
# character (start, comma, whitespace, open-paren). This excludes
# `tick_labels=` which contains "labels=" as an inner substring.
_LABELS_KWARG = re.compile(r"(?<!\w)labels\s*=")


class TestBoxplotKwargCompat(unittest.TestCase):
    def test_mape_box_by_region_uses_tick_labels(self):
        from geocif.viz import diagnostics
        src = inspect.getsource(diagnostics.mape_box_by_region)
        # Local assignment `labels = (_label_with_pct(...) if ...)` is fine.
        # What we ban is passing `labels=...` to a function call.
        # Heuristic: look for `, labels=` or `(labels=` patterns inside
        # a `.boxplot(` call — easier to scope by checking the whole
        # function body has tick_labels and not the boxplot-shaped labels.
        self.assertIn(
            "tick_labels=labels", src,
            msg="boxplot must use tick_labels= (labels= removed in matplotlib 3.11)",
        )
        # The fix replaces `labels=labels` with `tick_labels=labels`. After
        # the fix, only the LOCAL ASSIGNMENT `labels = (...)` should remain
        # as a `labels =` use — no `, labels=` kwarg patterns.
        self.assertNotRegex(
            src, r",\s*labels\s*=\s*labels",
            msg="found `, labels=labels` kwarg — rename to tick_labels=",
        )

    def test_no_boxplot_labels_kwarg_anywhere_in_diagnostics(self):
        """Belt-and-braces: scan the whole module source for the
        kwarg-position `labels=` pattern at any boxplot call.
        Catches any new boxplot call that reintroduces the old kwarg."""
        from geocif.viz import diagnostics
        src = inspect.getsource(diagnostics)
        # `labels=labels` and `labels=[str(...)]` are the two shapes the
        # codebase used at the two boxplot call sites. Ban both.
        self.assertNotRegex(
            src, r",\s*labels\s*=\s*labels",
            msg="found boxplot(..., labels=labels) — rename to tick_labels=",
        )
        self.assertNotRegex(
            src, r"\blabels\s*=\s*\[\s*str\s*\(",
            msg="found boxplot(..., labels=[str(...)]) — rename to tick_labels=",
        )

    def test_yield_outlook_uses_tick_labels(self):
        """Same fix had to be applied to yield_outlook.py's per-region
        MAPE boxplot. Pin it here so a refactor that re-introduces
        the old kwarg fails CI before hitting the HPC.

        Reads the source file directly rather than importing the
        module — yield_outlook.py drags pygeoutil through its import
        chain, which isn't always installed in CI envs.
        """
        from pathlib import Path
        yo_path = Path(__file__).resolve().parent.parent / "geocif" / "yield_outlook.py"
        src = yo_path.read_text(encoding="utf-8")
        self.assertNotRegex(
            src, r",\s*labels\s*=\s*labels",
            msg="yield_outlook boxplot must use tick_labels= (matplotlib >= 3.11)",
        )


if __name__ == "__main__":
    unittest.main()
