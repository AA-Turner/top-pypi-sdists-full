# -*- coding: utf-8 -*-
"""Shared look-and-feel for every geocif figure family.

Stdlib-only on purpose: ``viz/_pygmt_render.py`` re-exports the map
constants and must stay importable both as part of the package and as a
standalone script inside a pygmt-only bridge env, and ``viz/s2s_africa.py``
must stay importable on a machine with no GMT C library. Anything needing
matplotlib imports it lazily inside the function.

History: these values used to be restated per module — NODATA four times
in two colour systems, the month table five times, three style contexts,
four despine variants (one of which had lost the orphaned-tick fix). Same-
intent copies drift; every one of those already had. The single home is
the point of this module.
"""
import logging

logger = logging.getLogger(__name__)

#: Region excluded from the analysis. Never white, which reads as water.
#: The matplotlib path expresses the same colour as an RGBA tuple in
#: ``plot._region_fill`` — a drift-guard test pins the two together.
NODATA = "#d9d9d9"

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# ---------------------------------------------------------------------------
# PyGMT map furniture. Plain strings and dicts — no pygmt import needed, so
# GMT-free modules can share them.
# ---------------------------------------------------------------------------
#: Background coast. No `land=` fill: the map's white ground is what makes
#: the choropleth read as the only data on it.
COAST_KW = dict(shorelines="0.3p,gray60", borders="1/0.2p,gray70",
                area_thresh=5000)
#: Admin-unit outline. Heavy enough to separate neighbours at a glance.
POLY_PEN = "0.4p,black"
#: Admin-1 overlay pen, drawn AFTER the choropleth so it sits on top.
BORDER_PEN = "2/0.7p,black"
#: Horizontal colorbar under the frame.
CBAR_POS = "JBC+w12c/0.35c+h"
#: Region annotations: name above the centroid, value below (GMT text has
#: no reliable newline, so two offset calls).
ANNOT_FONT = "8p,Helvetica,black"
ANNOT_VAL_FONT = "7p,Helvetica-Oblique,black"
ANNOT_BOX = dict(fill="white@30", pen="0.2p,gray40")
ANNOT_OFFSET = "0c/0.16c"
#: Derived, not restated: the value line mirrors the name line below the
#: centroid, and a hand-kept mirror is exactly what un-mirrors.
ANNOT_VAL_OFFSET = "0c/-" + ANNOT_OFFSET.split("/", 1)[1]
#: fig.coast islet-clutter threshold shared by every map.
AREA_THRESH = COAST_KW["area_thresh"]

# probed once per process, on first use
_HAS_SCIENCE_STYLE = None


def style_ctx():
    """scienceplots 'science'+'no-latex' when available, default otherwise.

    Probes once and WARNS on the first failure — of the three contexts
    this replaces, only the diagnostics one would tell you the house theme
    had silently vanished from an env.
    """
    global _HAS_SCIENCE_STYLE
    import matplotlib.pyplot as plt

    if _HAS_SCIENCE_STYLE is None:
        try:
            import scienceplots  # noqa: F401
            _HAS_SCIENCE_STYLE = True
        except Exception as exc:  # noqa: BLE001 — any failure means "absent"
            _HAS_SCIENCE_STYLE = False
            logger.warning(
                f"scienceplots unavailable ({type(exc).__name__}: {exc}); "
                f"figures will use the matplotlib default style")
    if _HAS_SCIENCE_STYLE:
        try:
            return plt.style.context(["science", "no-latex"])
        except OSError as exc:  # importable but styles not registered
            _HAS_SCIENCE_STYLE = False
            logger.warning(f"scienceplots styles not registered ({exc}); "
                           f"falling back to the matplotlib default")
    return plt.style.context("default")


def despine(*axes, sides=("top", "right")):
    """Hide the given spines AND their ticks.

    scienceplots turns ticks on all four sides; with the spines hidden
    those become orphaned dashes floating at the plot edge, so the ticks
    go with them. Only top/right ticks are touched — a hidden LEFT spine
    (leadtime's crossing chart) keeps its y labels.
    """
    for ax in axes:
        ax.spines[list(sides)].set_visible(False)
        off = {s: False for s in sides if s in ("top", "right")}
        if off:
            ax.tick_params(which="both", **off)
