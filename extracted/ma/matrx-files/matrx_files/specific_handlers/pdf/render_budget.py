"""How many pixels one PDF page may become.

A page's size in points says nothing about its bytes: a 724 KB phone photo saved
as a PDF is two 2268 × 4032 pt pages, and OCR's 300 DPI turns each into 159
megapixels — 476 MB of samples before Tesseract needs another 2.3 GB. Four runs of
that one file killed four live server tasks (2026-11-04), and every run in flight
on them died with it (`runtime_execution_abandoned`). So every render of a page
asks here first: the requested DPI stands unless it would exceed the budget, and
then it drops just enough to fit. A smaller picture of a huge page reads as well
as the huge one; a killed server reads nothing.

The budget is ``media.file_service.render_max_megapixels`` (host-bound, see
``specific_handlers/knobs.py``).
"""

from __future__ import annotations

import logging
import math

from ..knobs import extraction_knob

logger = logging.getLogger(__name__)

# KNOB MIRROR: media.file_service.render_max_megapixels. Tabloid paper at 268 DPI;
# anything ordinary keeps its full DPI (Letter at 300 DPI is 8.4 megapixels).
RENDER_MAX_MEGAPIXELS = 24


def bounded_render_dpi(width_pt: float, height_pt: float, dpi: float) -> int:
    """The DPI to render a ``width_pt`` × ``height_pt`` area at: ``dpi``, or less when
    ``dpi`` would exceed the render budget. Never below 1, and never above ``dpi``."""
    budget = float(extraction_knob("render_max_megapixels", RENDER_MAX_MEGAPIXELS)) * 1_000_000
    pixels = (width_pt * dpi / 72.0) * (height_pt * dpi / 72.0)
    if pixels <= budget:
        return int(dpi)
    bounded = max(int(dpi * math.sqrt(budget / pixels)), 1)
    logger.info(
        "PDF render lowered from %s to %s DPI: a %.0f x %.0f pt area would be %.0f megapixels",
        dpi,
        bounded,
        width_pt,
        height_pt,
        pixels / 1_000_000,
    )
    return bounded


__all__ = ["RENDER_MAX_MEGAPIXELS", "bounded_render_dpi"]
