"""Saving figures, shared by the Pikobs modules.

Every module writes its figures as PNG, which is what the web viewer
shows. With ``--svg on`` it writes the same figure again as SVG, next to
the PNG, for the times a figure has to be edited before going into a
presentation: in Inkscape or Illustrator the titles, the legends and the
colours stay editable, and the text is real text, not curves.

The SVG is never used by the viewer, so turning it on changes nothing
else.

Usage::

    from pikobs.figures import save_figure

    save_figure(fig, out_file, svg=task.get('svg', False), dpi=DPI)

A word of warning worth repeating in each module's documentation: an SVG
keeps every element of the figure, so a map with thousands of boxes or a
bar chart of four months weighs tens of megabytes and opens slowly. Ask
for it on the one or two figures you actually need:

    ID_STN=(=NOAA20)  CHANNEL=(5)  SVG="on"
"""

import os
import sys
from typing import Any, Optional

import matplotlib

# text stays text in the SVG, so a title can be edited afterwards
matplotlib.rcParams['svg.fonttype'] = 'none'

# a figure larger than this is reported when it is written, because it is
# usually a selection that was wider than intended
SVG_WARN_MB = 25.0


def save_figure(fig, png_path: str, svg: bool = False,
                dpi: int = 100, **kwargs: Any) -> str:
    """Write the figure as PNG, and as SVG beside it when asked.

    Returns the path of the PNG, which is what the viewer references.
    """
    os.makedirs(os.path.dirname(png_path) or '.', exist_ok=True)
    fig.savefig(png_path, format='png', dpi=dpi,
                bbox_inches=kwargs.pop('bbox_inches', 'tight'), **kwargs)
    if svg:
        svg_path = os.path.splitext(png_path)[0] + '.svg'
        try:
            fig.savefig(svg_path, format='svg', bbox_inches='tight')
            size_mb = os.path.getsize(svg_path) / (1024 ** 2)
            if size_mb > SVG_WARN_MB:
                print(f"[pikobs] the SVG of {os.path.basename(svg_path)} "
                      f"weighs {size_mb:.0f} MB: it will be slow to open, "
                      f"narrow the selection if you meant to edit it",
                      file=sys.stderr, flush=True)
        except Exception as exc:
            print(f"[pikobs] could not write {os.path.basename(svg_path)}: "
                  f"{exc}", file=sys.stderr, flush=True)
    return png_path


def svg_enabled(value: Optional[str]) -> bool:
    """Read the --svg argument: 'on' / 'off' (anything else is off)."""
    return str(value).strip().lower() in ('on', 'true', 'yes', '1')
