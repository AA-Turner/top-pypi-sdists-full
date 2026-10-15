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


# ---------------------------------------------------------------------------
# What every comparison figure says the same way
# ---------------------------------------------------------------------------

#: the badge of each MATCH: its colour, what it says, what is drawn and tested
MATCH_BADGE = {
    True: ("#14684A", "MATCH ON", "matched observations\ncycle block bootstrap, 95 %"),
    False: ("#B8590B", "MATCH OFF", "all observations\nt-test and F-test, 95 %"),
}


def match_badge(fig, matched: bool, top_in: float = 0.12, right: float = 0.993,
                method: str = None, scale: float = 1.0):
    """MATCH ON or MATCH OFF, big, in a coloured box at the top right of a
    figure, with what it means under it: the first thing read on a slide.
    ``top_in`` is its distance from the top of the figure, in inches.
    ``method`` names the test when it is not the default of MATCH_BADGE --
    the badge must say the test the figure really draws.
    Returns the box, so a header can keep clear of it."""
    from matplotlib.offsetbox import AnchoredOffsetbox, TextArea, VPacker
    from pikobs.configobs.style import font_size
    colour, head, sub = MATCH_BADGE[bool(matched)]
    if method:
        sub = sub.split("\n")[0] + "\n" + method
    head_t = TextArea(head, textprops=dict(color="white", fontweight="bold",
                                           fontsize=scale * font_size("badge")))
    sub_t = TextArea(sub, textprops=dict(color="white", fontweight="bold",
                                         fontsize=scale * font_size("badge_sub"),
                                         ha="center", linespacing=1.2))
    box = AnchoredOffsetbox(loc="upper right", pad=0.5, borderpad=0, frameon=True,
                            child=VPacker(children=[head_t, sub_t], align="center", sep=4),
                            bbox_to_anchor=(right, 1 - top_in / fig.get_figheight()),
                            bbox_transform=fig.transFigure)
    box.patch.set(facecolor=colour, edgecolor="none", boxstyle="round,pad=0.4")
    fig.add_artist(box)
    return box


def count_label(value) -> str:
    """A count as it reads best on an axis: 950, 12K, 3.4M."""
    v = float(value)
    for scale, unit in ((1e6, "M"), (1e3, "K")):
        if abs(v) >= scale:
            return f"{v / scale:.3g}{unit}"
    return f"{v:g}"


def count_formatter():
    """The tick formatter of an axis of counts: 12K rather than 12000."""
    from matplotlib.ticker import FuncFormatter
    return FuncFormatter(lambda v, _pos: count_label(v))


def legend_ncol(labels, size: float, width_pt: float, handle: float = 4.0) -> int:
    """How many columns of a key fit a width: the most columns whose widest
    labels add up to the width (a key fills its columns top to bottom).
    Each label is estimated at 0.6 of the font size a character, plus the
    room of its handle and the gap to the next column."""
    widths = [(len(str(l)) * 0.6 + handle) * size for l in labels]
    for ncol in range(len(widths), 0, -1):
        rows = -(-len(widths) // ncol)
        cols = [widths[c * rows:(c + 1) * rows] for c in range(ncol)]
        if sum(max(c) for c in cols if c) <= width_pt:
            return ncol
    return 1


def fit_texts(fig, badge=None, right: float = 0.99, floor: float = 0.70) -> None:
    """No line of a figure runs past its right edge, nor under the MATCH
    badge: one that would is made smaller, just enough (never under 70 % of
    its size). Saved with a tight frame, a line too long would widen the
    image and squeeze the plots."""
    renderer = fig.canvas.get_renderer()
    b = badge.get_window_extent(renderer) if badge is not None else None
    for t in fig.texts:
        if not t.get_text().strip():
            continue
        e = t.get_window_extent(renderer)
        beside = b is not None and e.y0 < b.y1 and e.y1 > b.y0
        edge = (b.x0 - 12.0) if beside else right * fig.bbox.width
        size = t.get_fontsize()
        low = floor * size
        while t.get_window_extent(renderer).x1 > edge and size > low:
            size *= 0.96
            t.set_fontsize(size)


def write_hover(fig, png_path: str, ref_ax, rows, word: str = "channel", dpi: int = 100) -> None:
    """Beside a saved figure, ``<png>.map.json`` -- the viewer's map of what
    is under the mouse (as flags writes it): for each row of the vertical
    axis, a rectangle over every panel, in pixels of the PNG, with its text.

    ``rows`` is [(y in data units of ref_ax, label)]; the text is
    ``word label``. A row's rectangle reaches half way to its neighbours.
    Call it right after ``save_figure``, before the figure is closed."""
    import json

    import matplotlib.image as mpimg

    try:
        h_png, w_png = mpimg.imread(png_path).shape[:2]
        renderer = fig.canvas.get_renderer()
        w_in, h_in = fig.get_size_inches()
        if abs(w_png - w_in * dpi) <= 2 and abs(h_png - h_in * dpi) <= 2:
            x0_in, y1_in = 0.0, float(h_in)                    # the whole figure
        else:                                                  # a tight crop
            box = fig.get_tightbbox(renderer).padded(0.1)
            x0_in, y1_in = box.x0, box.y1

        def px_x(disp):
            return (disp / fig.dpi - x0_in) * dpi

        def px_y(disp):
            return (y1_in - disp / fig.dpi) * dpi

        panels = [a for a in fig.axes if a.get_visible() and a.get_subplotspec() is not None]
        x_mid = ref_ax.get_xlim()[0]
        ys = sorted(((px_y(ref_ax.transData.transform((x_mid, y))[1]), str(lab)) for y, lab in rows))
        texts, rects = [], []
        for i, (y, lab) in enumerate(ys):
            up = (y + ys[i - 1][0]) / 2.0 if i else y - 6.0
            down = (y + ys[i + 1][0]) / 2.0 if i + 1 < len(ys) else y + 6.0
            texts.append(f"{word} {lab}")
            for a in panels:
                e = a.get_window_extent(renderer)
                rects.append([round(px_x(e.x0), 1), round(up, 1), round(px_x(e.x1), 1), round(down, 1), i])
        with open(png_path + ".map.json", "w", encoding="utf-8") as fh:
            json.dump({"w": int(w_png), "h": int(h_png), "rects": rects, "texts": texts}, fh)
    except Exception as exc:                          # a convenience: never fail the figure
        print(f"[pikobs] no mouse map for {os.path.basename(png_path)}: {exc}", file=sys.stderr, flush=True)


def write_hover_rects(fig, png_path: str, rects, dpi: int = 100) -> None:
    """Beside a saved figure, ``<png>.map.json`` from any rectangles: each
    (x0, y0, x1, y1, text) in display units of the figure (as an artist's
    window extent), turned into pixels of the PNG. For what is not a row of
    an axis: the boxes of a map, the bars of a histogram. Call it right
    after ``save_figure``, before the figure is closed."""
    import json

    import matplotlib.image as mpimg

    try:
        h_png, w_png = mpimg.imread(png_path).shape[:2]
        renderer = fig.canvas.get_renderer()
        w_in, h_in = fig.get_size_inches()
        if abs(w_png - w_in * dpi) <= 2 and abs(h_png - h_in * dpi) <= 2:
            x0_in, y1_in = 0.0, float(h_in)
        else:
            box = fig.get_tightbbox(renderer).padded(0.1)
            x0_in, y1_in = box.x0, box.y1
        texts, out = [], []
        for x0, y0, x1, y1, text in rects:
            px0, px1 = sorted(((x0 / fig.dpi - x0_in) * dpi, (x1 / fig.dpi - x0_in) * dpi))
            py0, py1 = sorted(((y1_in - y1 / fig.dpi) * dpi, (y1_in - y0 / fig.dpi) * dpi))
            texts.append(str(text))
            out.append([round(px0, 1), round(py0, 1), round(px1, 1), round(py1, 1), len(texts) - 1])
        with open(png_path + ".map.json", "w", encoding="utf-8") as fh:
            json.dump({"w": int(w_png), "h": int(h_png), "rects": out, "texts": texts}, fh)
    except Exception as exc:                          # a convenience: never fail the figure
        print(f"[pikobs] no mouse map for {os.path.basename(png_path)}: {exc}", file=sys.stderr, flush=True)



def members_footer(fig, selection, fontsize: float = None) -> None:
    """The stations of a prefix, a pattern or a list (a selector, or the text
    itself), under everything already drawn, left, wrapped to the width of
    the figure. save_figure's tight box takes it in; nothing else moves."""
    text = selection if isinstance(selection, str) else \
        getattr(selection, "members_text", "")
    if not text:
        return
    import textwrap
    if fontsize is None:
        # as big as the dates under the panels: in a figure of a few
        # thousand pixels a fixed small size vanishes once fitted to a screen
        sizes = [t.get_fontsize() for ax in fig.axes for t in ax.get_xticklabels()]
        fontsize = max(sizes) if sizes else 9.0
    w_in, h_in = fig.get_size_inches()
    chars = max(40, int(w_in * 72 / (fontsize * 0.60)))
    lines = textwrap.wrap(text, chars, break_long_words=False,
                          break_on_hyphens=False)
    try:
        bottom = fig.get_tightbbox(fig.canvas.get_renderer()).y0 / h_in
    except Exception:
        bottom = 0.0
    fig.text(0.02, bottom - 0.12 / h_in, "\n".join(lines), ha="left",
             va="top", fontsize=fontsize, color="#30343A")
