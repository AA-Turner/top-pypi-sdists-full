"""Regression test for the `diag` NameError in _plot_combined_map_mape.

Bug (fixed 0.4.888): _plot_combined_map_mape referenced ``diag._draw_axis_break``
inside its ``do_cap`` branch (only entered when a region's MAPE > 150%) but never
imported ``diag`` — every other function imports ``from .viz import diagnostics as
diag`` locally, this one imported only ``_label_with_pct``. The branch was dormant
until the brazil 2001-2020 run produced a >150% MAPE region, then crashed the whole
diagnostics phase with ``NameError: name 'diag' is not defined``.

Structural guard: assert the function's source imports the diagnostics module so the
``diag.*`` references resolve. Avoids needing cartopy + a live plot_map to exercise
the do_cap path.
"""
import inspect

import geocif.yield_outlook as yo


def test_combined_map_mape_imports_diag():
    src = inspect.getsource(yo._plot_combined_map_mape)
    assert "import diagnostics as diag" in src or "diagnostics as diag" in src, (
        "_plot_combined_map_mape must import the diagnostics module as `diag` so "
        "the do_cap-branch `diag._draw_axis_break(...)` call resolves"
    )
    # and it must actually reference diag (otherwise the import guard is moot)
    assert "diag._draw_axis_break" in src
