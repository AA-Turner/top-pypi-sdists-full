"""The card of obsscorecard: one theme, Exp against Ctl.

Two tables side by side, read on a slide: the sigma of O-P on the left and,
for winds and thermodynamics, its |bias| on the right; for the radiances,
the sigma and the number of observations used. A row is a family and a
region, a column a layer of height (the surface and whole-column families
in a column of their own). In every cell the change over the period, and
under it in how many cycles the experience was better.
"""
import math
import textwrap
from typing import Dict, List, Optional, Sequence, Tuple

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt                                  # noqa: E402
from matplotlib.patches import Rectangle                         # noqa: E402
import numpy as np                                               # noqa: E402
import pandas as pd                                              # noqa: E402

import pikobs                                                    # noqa: E402
from pikobs.configobs.style import (CTL_BETTER, CTL_COLOUR, DPI,  # noqa: E402
                                    EXP_BETTER, EXP_COLOUR, GREY_TEXT, font_size)
from pikobs.figures import match_badge, save_figure              # noqa: E402
from pikobs.stats import is_significant                          # noqa: E402
from pikobs.verifprofile.scorecard import (MIN_CHANGE_PCT, MIN_OBS_PER_CELL,  # noqa: E402
                                           SCALE_HEIGHT_KM)

GREY_FACE, GREY_TEXT_CELL = "#D1D5DB", "#6B7280"
THEME_TITLE = {"winds": "winds", "thermodynamics": "thermodynamics", "surface": "surface",
               "ro_ch": "GPS-RO and ozone", "radiances": "radiances"}


def _header(fig, fig_h, head_in, title, names, datestart, dateend, n_cycles, n_skipped,
            flag, land_ocean, mode, off_bootstrap: Optional[str] = None) -> None:
    """The top of a card: title, period, the two runs, what the colours
    mean, the test, the MATCH badge. ``off_bootstrap`` names what is tested
    on the cycles even with MATCH off (the pooled radiances)."""
    ctl, exp = names

    def at(inch):
        return 1 - inch / fig_h

    def _when(s):
        s = str(s)
        return f"{s[:4]}-{s[4:6]}-{s[6:8]} {s[8:10]} UTC"
    fig.text(0.012, at(0.15), title, fontsize=font_size("title"), fontweight="bold",
             color="#1F2933", va="top")
    parts = [f"{_when(datestart)} to {_when(dateend)}",
             f"{n_cycles} cycles" + (f" ({n_skipped} with the same background left out)"
                                     if n_skipped else ""), f"flag {flag}"]
    if land_ocean != "all":
        parts.append(land_ocean)
    fig.text(0.012, at(0.85), "  \u00b7  ".join(parts), fontsize=font_size("note"),
             color=GREY_TEXT, va="top")
    t = fig.text(0.012, at(1.45), f"Ctl  {ctl}", fontsize=font_size("names"),
                 fontweight="bold", color=CTL_COLOUR, va="top")
    box = t.get_window_extent(renderer=fig.canvas.get_renderer())
    x = fig.transFigure.inverted().transform((box.x1, box.y0))[0] + 0.02
    fig.text(x, at(1.45), f"Exp  {exp}", fontsize=font_size("names"), fontweight="bold",
             color=EXP_COLOUR, va="top")
    fig.text(0.012, at(2.15), "red: Exp better  \u00b7  blue: Exp worse  \u00b7  strong: "
             "significant (95 %)  \u00b7  pale: not significant  \u00b7  41/56: cycles Exp "
             "better / cycles compared", fontsize=font_size("note"), color="#30343A", va="top")
    test = {"on": "tested on the cycles (cycle block bootstrap) from 20 cycles",
            "off": "t-test and F-test" + (f"; {off_bootstrap} (bootstrap)" if off_bootstrap
                                          else ""),
            "no": "no test: every colour pale"}[mode]
    fig.text(0.012, at(2.7), f"grey: below {MIN_CHANGE_PCT:g} %; empty: no data, or "
             f"fewer than {MIN_OBS_PER_CELL} observations; {test}",
             fontsize=0.8 * font_size("note"), color=GREY_TEXT, va="top")
    if mode != "no":
        method = ("cycle block bootstrap, 95 %" if mode == "on"
                  else "t-test and F-test, 95 %")
        match_badge(fig, mode == "on", top_in=0.15, method=method)
    fig.add_artist(mpl.lines.Line2D([0.012, 0.993], [at(head_in - 0.12)] * 2,
                                    transform=fig.transFigure, color="#D9DDE2", lw=1.5))


def _hpa(z_km: float) -> float:
    return 1013.25 * math.exp(-z_km / SCALE_HEIGHT_KM)


def _p(value: float) -> str:
    if value >= 20:
        return f"{value:.0f}"
    if value >= 1:
        return f"{value:.1f}"
    return f"{value:.2g}"


def _colour(change: float, conf: float, better_if_negative: bool, mode: str):
    """(face, alpha, text colour, bold) of a cell. Red where Exp is better,
    blue where it is worse: strong when the test passes, pale when it does
    not (the sign still shows), grey below MIN_CHANGE_PCT. With MATCH no
    there is no test, so every colour is pale."""
    if not np.isfinite(change) or abs(change) < MIN_CHANGE_PCT:
        return GREY_FACE, 0.35, GREY_TEXT_CELL, False
    better = change < 0 if better_if_negative else change > 0
    face = EXP_BETTER if better else CTL_BETTER
    significant = mode != "no" and bool(is_significant(np.array([conf]))[0])
    if not significant:
        return face, 0.20, "#1F2933", False
    alpha = min(0.50 + abs(change) / 4.0, 0.95)
    return face, alpha, "white", True


def _height_rank(layer: str) -> float:
    """surface first, the layers by their lower edge, the total last."""
    if layer == "sfc":
        return -1.0
    if layer in ("total", "all"):
        return 1e9
    return float(layer.split("-")[0])


def _columns(cells: pd.DataFrame, theme: str) -> List[str]:
    """The columns some row reaches, in order of height, the total last."""
    if theme == "radiances":
        return ["all"]
    return sorted(set(cells["layer"]), key=_height_rank)


def _rows(cells: pd.DataFrame, regions: Sequence[str]) -> List[Tuple[str, str, str]]:
    """(block, label, region) in the order of the theme, then the regions."""
    order = list(dict.fromkeys(zip(cells["block"], cells["label"])))
    reg = {r: i for i, r in enumerate(regions)}
    out = []
    for fam, lab in order:
        here = cells[(cells["block"] == fam) & (cells["label"] == lab)]
        for r in sorted(set(here["region"]), key=lambda x: reg.get(x, 99)):
            out.append((fam, lab, r))
    return out


def _table(ax, cells, rows, cols, metric, conf, wins, total, better_if_negative, mode):
    n_rows = len(rows)
    idx = {(r.block, r.label, r.region, r.layer): r for r in cells.itertuples(index=False)}
    for i, (fam, lab, reg) in enumerate(rows):
        y = n_rows - 1 - i
        for j, col in enumerate(cols):
            c = idx.get((fam, lab, reg, col))
            if c is None or not np.isfinite(getattr(c, metric, np.nan)):
                ax.add_patch(Rectangle((j, y), 1, 1, fc="white", ec="#E5E7EB", lw=0.8))
                continue
            val = getattr(c, metric)
            face, alpha, tc, bold = _colour(val, getattr(c, conf, np.nan),
                                            better_if_negative, mode)
            ax.add_patch(Rectangle((j, y), 1, 1, fc=face, alpha=alpha, ec="white", lw=2.5))
            ax.text(j + 0.5, y + 0.63, f"{val:+.1f}", ha="center", va="center",
                    fontsize=font_size("cell"), color=tc,
                    fontweight="bold" if bold else "normal")
            w, t = getattr(c, wins, 0), getattr(c, total, 0)
            if t:
                ax.text(j + 0.5, y + 0.24, f"{int(w)}/{int(t)}", ha="center", va="center",
                        fontsize=0.72 * font_size("cell"), color=tc)
    ax.set_xlim(0, len(cols))
    ax.set_ylim(0, n_rows)
    ax.set_xticks([])
    ax.set_yticks([])
    for j, col in enumerate(cols):
        if col == "sfc":
            top, under = "surface", "column"
        elif col == "all":
            top, under = "all", "channels"
        elif col == "total":
            top, under = "total", "all levels"
        else:
            lo, hi = (float(x) for x in col.split("-"))
            top, under = col, f"{_p(_hpa(lo))}-{_p(_hpa(hi))}"
        ax.text(j + 0.5, n_rows + 0.62, top, ha="center", va="bottom",
                fontsize=font_size("column"), color="#1F2933")
        ax.text(j + 0.5, n_rows + 0.12, under, ha="center", va="bottom",
                fontsize=0.7 * font_size("column"), color=GREY_TEXT)
    for side in ax.spines.values():
        side.set_visible(False)
    if "total" in cols and len(cols) > 1:            # the total apart
        ax.axvline(cols.index("total"), color="#4B5563", lw=4.0, clip_on=False)


def draw_card(cells: pd.DataFrame, theme: str, names: Tuple[str, str], mode: str,
              datestart: str, dateend: str, flag: str, land_ocean: str, n_cycles: int,
              n_skipped: int, regions: Sequence[str], out_png: str, svg: bool = False) -> str:
    rows = _rows(cells, regions)
    cols = _columns(cells, theme)
    radiances = theme == "radiances"
    if radiances:
        tables = [("d_sigma", "sigma_conf", "sigma_wins", "cycles", True,
                   "sigma of O-P\n(Exp - Ctl) / Ctl  [%]"),
                  ("d_n", "n_conf", "n_wins", "n_cycles", False,
                   "observations used\n(Exp - Ctl) / Ctl  [%]")]
    else:
        tables = [("d_sigma", "sigma_conf", "sigma_wins", "cycles", True,
                   "sigma of O-P: (Exp - Ctl) / Ctl  [%]"),
                  ("d_bias", "bias_conf", "bias_wins", "bias_cycles", True,
                   "|bias| of O-P, in % of sigma Ctl")]

    head_in, cols_in, row_in, foot_in = 3.3, 1.75, 0.95, 0.3
    if radiances:
        cols_in = 2.5                     # the titles take two lines
    daggers = "flag_exp_only" in cells and bool(cells["flag_exp_only"].any())
    if daggers:
        foot_in = 0.9                     # room for what the dagger means
    # every card the same width: the header and the badge keep their room
    label_w, width_tab, fig_w = 0.265, 0.355, 26.0
    # every layer column as wide as on a card of seven layers: a theme with
    # more of them (GPS-RO and ozone) grows wider instead of squeezing its
    # columns until their names run into each other
    if not radiances and len(cols) > 7:
        col_in = 26.0 * 0.355 / 7
        label_in, gap_in, right_in = 26.0 * 0.265, 26.0 * 0.02, 0.15
        tab_in = col_in * len(cols)
        fig_w = label_in + len(tables) * (tab_in + gap_in) + right_in
        label_w, width_tab = label_in / fig_w, tab_in / fig_w
    fig_h = head_in + cols_in + row_in * len(rows) + foot_in
    fig = plt.figure(figsize=(fig_w, fig_h), facecolor="white")

    def at(inch):
        return 1 - inch / fig_h

    body = [foot_in / fig_h, row_in * len(rows) / fig_h]
    if radiances:
        label_w, width_tab = 0.30, 0.24
    axes = []
    x = label_w
    for t in tables:
        ax = fig.add_axes([x, body[0], width_tab, body[1]])
        _table(ax, cells, rows, cols, *t[:5], mode)
        ax.text(len(cols) / 2, len(rows) + 1.45, t[5], ha="center", va="bottom",
                fontsize=font_size("table_title"), fontweight="bold", color="#30343A",
                transform=ax.transData)
        axes.append(ax)
        x += width_tab + 0.02

    # the row labels: the family and variable once per block, the region beside
    lab_tr = mpl.transforms.blended_transform_factory(fig.transFigure, axes[0].transData)
    n_rows = len(rows)
    # the units of the layers, once, left of the first table
    if any(c not in ("sfc", "all") for c in cols):
        fig.text(label_w - 0.007, n_rows + 0.62, "height (km)", transform=lab_tr, ha="right",
                 va="bottom", fontsize=font_size("column"), color="#1F2933")
        fig.text(label_w - 0.007, n_rows + 0.12, "pressure (hPa)", transform=lab_tr,
                 ha="right", va="bottom", fontsize=0.7 * font_size("column"), color=GREY_TEXT)
    prev = None
    for i, (fam, lab, reg) in enumerate(rows):
        y = n_rows - i
        fig.text(label_w - 0.007, y - 0.5, reg, transform=lab_tr, ha="right", va="center",
                 fontsize=font_size("row"), color="#1F2933")
        if (fam, lab) != prev:
            for ax in axes:
                ax.axhline(y, color="#6B7280", lw=2.0, clip_on=False)
            dagger = bool(cells[(cells["block"] == fam) & (cells["label"] == lab)]
                          .get("flag_exp_only", pd.Series([False])).any())
            name = fam + ("" if radiances else f"  {lab}") + (" \u2020" if dagger else "")
            fig.text(0.008, y - 0.15, "\n".join(textwrap.wrap(name, 16)), transform=lab_tr,
                     ha="left", va="top", linespacing=1.15, fontsize=font_size("block"),
                     fontweight="bold", color="#1F2933")
            prev = (fam, lab)

    if daggers:
        fig.text(0.012, 0.25 / fig_h, f"\u2020 the flag criterion ({flag}) on Exp only: Ctl "
                 "does not assimilate this family and is read without it (from its bgckalt); "
                 "the pairs are what Exp assimilated, with the background of Ctl on them.",
                 fontsize=0.8 * font_size("note"), color=GREY_TEXT, va="bottom")
    title = THEME_TITLE.get(theme, theme)
    if theme == "ro_ch" and not (cells["family"] == "ch").any():
        title = "GPS-RO"                      # the runs have no ozone file
    _header(fig, fig_h, head_in, f"Scorecard  \u00b7  {title}  "
            f"\u00b7  O-P, Exp against Ctl", names, datestart, dateend, n_cycles, n_skipped,
            flag, land_ocean, mode, "radiances on the cycles" if radiances else None)
    save_figure(fig, out_png, svg=svg, dpi=DPI)
    plt.close(fig)
    return out_png


def _region_table(ax, idx, row_keys, regs, metric, conf, wins, total, neg, mode, many,
                  hover, title, row_in, name, text_scale: float = 1.0) -> None:
    """A table with a row per key (first at the bottom) and a column per
    region: the change in colour, the value and the cycles won written in
    the cell unless the rows are ``many``; every cell's text for the mouse
    goes into ``hover``."""
    for yi, key in enumerate(row_keys):
        for j, reg in enumerate(regs):
            c = idx.get((reg, key))
            val = getattr(c, metric, np.nan) if c is not None else np.nan
            if c is None or not np.isfinite(val):
                ax.add_patch(Rectangle((j, yi), 1, 1, fc="white", ec="#E5E7EB", lw=0.6))
                continue
            face, alpha, tc, bold = _colour(val, getattr(c, conf, np.nan), neg, mode)
            patch = ax.add_patch(Rectangle((j, yi), 1, 1, fc=face, alpha=alpha,
                                           ec="white", lw=1.5 if many else 2.5))
            w, t = int(getattr(c, wins, 0) or 0), int(getattr(c, total, 0) or 0)
            hover.append((patch, f"{name(key)} \u00b7 {reg} \u00b7 {title.splitlines()[0]} "
                                 f"{val:+.1f} % \u00b7 Exp better in {w}/{t} cycles \u00b7 "
                                 f"n {int(c.n_ctl)} / {int(c.n_exp)}"))
            if not many:
                ax.text(j + 0.5, yi + 0.63, f"{val:+.1f}", ha="center", va="center",
                        fontsize=text_scale * font_size("cell"), color=tc,
                        fontweight="bold" if bold else "normal")
                if t:
                    ax.text(j + 0.5, yi + 0.24, f"{w}/{t}", ha="center", va="center",
                            fontsize=0.72 * text_scale * font_size("cell"), color=tc)
    n = len(row_keys)
    ax.set_xlim(0, len(regs))
    ax.set_ylim(0, n)
    ax.set_xticks([])
    ax.set_yticks([])
    for side in ax.spines.values():
        side.set_visible(False)
    # the region names upright and whole, the title above the tallest one
    for j, reg in enumerate(regs):
        ax.text(j + 0.5, n + (0.3 / row_in), str(reg), ha="center", va="bottom",
                rotation=90, fontsize=0.8 * font_size("column"), color="#1F2933")
    ax.text(len(regs) / 2, n + ((0.3 + _labels_in(regs) + 0.25) / row_in), title,
            ha="center", va="bottom", fontsize=font_size("table_title"),
            fontweight="bold", color="#30343A")


def _labels_in(regs) -> float:
    """How tall the upright region names are, in inches: the longest one."""
    longest = max((len(str(r)) for r in regs), default=0)
    return longest * 0.8 * font_size("column") * 0.62 / 72.0


def _cols_in(regs) -> float:
    """The band above a table of regions: the names upright, then the title
    of the table on its two lines, with some room between them."""
    title_in = 2 * font_size("table_title") * 1.35 / 72.0
    return 0.3 + _labels_in(regs) + 0.25 + title_in + 0.15


def _two_lines(region: str) -> str:
    """A region name over two lines where its words meet: ExtratropiquesNord
    -> Extratropiques / Nord, AmeriqueduNord -> Ameriquedu / Nord."""
    import re
    cut = [m.start() for m in re.finditer(r"(?<=[a-z])(?=[A-Z])", region)]
    return region if not cut else region[:cut[-1]] + "\n" + region[cut[-1]:]


#: more channels than this and the rows and their text are smaller (every
#: channel is still written, with its value and its cycles)
TEXT_ROWS_MAX = 30


def draw_channel_card(cells: pd.DataFrame, family: str, names: Tuple[str, str], mode: str,
                      datestart: str, dateend: str, flag: str, land_ocean: str,
                      n_cycles: int, n_skipped: int, regions: Sequence[str], out_png: str,
                      svg: bool = False) -> str:
    """One family of channels, channel by channel: a row per channel (small
    at the bottom, large at the top), a column per region; the sigma of O-P
    on the left, the observations used on the right."""
    from pikobs.figures import write_hover_rects
    chans = sorted(set(cells["channel"]))                  # small first = bottom
    regs = [r for r in regions if r in set(cells["region"])]
    # every channel with its value and its cycles, as the other cards; when
    # there are many (IASI, CrIS) the rows and the text are only smaller
    many = False
    dense = len(chans) > TEXT_ROWS_MAX
    head_in, cols_in, foot_in = 3.3, 2.5, 0.3
    cols_in = max(cols_in, _cols_in(locals().get('regs') or locals().get('regions') or ()))
    row_in = 0.62 if dense else 0.95
    fig_h = head_in + cols_in + row_in * len(chans) + foot_in
    fig = plt.figure(figsize=(26.0, fig_h), facecolor="white")
    body = [foot_in / fig_h, row_in * len(chans) / fig_h]
    idx = {(r.region, r.channel): r for r in cells.itertuples(index=False)}
    tables = [("d_sigma", "sigma_conf", "sigma_wins", "cycles", True,
               "sigma of O-P\n(Exp - Ctl) / Ctl  [%]"),
              ("d_n", "n_conf", "n_wins", "n_cycles", False,
               "observations used\n(Exp - Ctl) / Ctl  [%]")]
    label_w, width_tab = 0.12, 0.425
    hover = []
    axes = []
    x = label_w
    for metric, conf, wins, total, neg, title in tables:
        ax = fig.add_axes([x, body[0], width_tab, body[1]])
        _region_table(ax, idx, chans, regs, metric, conf, wins, total, neg, mode, many,
                      hover, title, row_in, lambda ch: f"channel {ch:g}",
                      text_scale=0.78 if dense else 1.0)
        axes.append(ax)
        x += width_tab + 0.015
    # every channel down the left
    tr = mpl.transforms.blended_transform_factory(fig.transFigure, axes[0].transData)
    for yi, ch in enumerate(chans):
        fig.text(label_w - 0.006, yi + 0.5, f"{ch:g}", transform=tr, ha="right",
                 va="center", fontsize=(0.8 if dense else 1.0) * font_size("row"),
                 color="#1F2933")
    fig.text(label_w - 0.006, len(chans) + (0.3 / row_in), "channel", transform=tr,
             ha="right", va="bottom", fontsize=font_size("column"), color="#1F2933")
    fig.text(0.008, len(chans) - 0.5, pikobs.family(family)[0], transform=tr, ha="left",
             va="top", fontsize=font_size("block"), fontweight="bold", color="#1F2933")
    _header(fig, fig_h, head_in, f"Scorecard  \u00b7  {pikobs.family(family)[0]} channel by "
            f"channel  \u00b7  O-P, Exp against Ctl", names, datestart, dateend, n_cycles,
            n_skipped, flag, land_ocean, mode, "observations used on the cycles")
    save_figure(fig, out_png, svg=svg, dpi=DPI)
    fig.canvas.draw()
    write_hover_rects(fig, out_png, [(*p.get_window_extent().extents, t) for p, t in hover],
                      dpi=DPI)
    plt.close(fig)
    return out_png


def draw_surface_card(cells: pd.DataFrame, names: Tuple[str, str], mode: str,
                      datestart: str, dateend: str, flag: str, land_ocean: str,
                      n_cycles: int, n_skipped: int, regions: Sequence[str], out_png: str,
                      svg: bool = False) -> str:
    """What is observed at the surface (or over the column): a row per
    family and variable, in the order of the theme from the top, a column
    per region; the sigma of O-P on the left, its |bias| on the right."""
    from pikobs.figures import write_hover_rects
    order = list(dict.fromkeys(zip(cells["block"], cells["label"])))
    keys = list(reversed(order))                           # the first row at the top
    regs = [r for r in regions if r in set(cells["region"])]
    idx = {(r.region, (r.block, r.label)): r for r in cells.itertuples(index=False)}
    head_in, cols_in, row_in, foot_in = 3.3, 2.5, 0.95, 0.3
    cols_in = max(cols_in, _cols_in(regions))
    fig_h = head_in + cols_in + row_in * len(keys) + foot_in
    fig = plt.figure(figsize=(26.0, fig_h), facecolor="white")
    body = [foot_in / fig_h, row_in * len(keys) / fig_h]
    tables = [("d_sigma", "sigma_conf", "sigma_wins", "cycles", True,
               "sigma of O-P\n(Exp - Ctl) / Ctl  [%]"),
              ("d_bias", "bias_conf", "bias_wins", "bias_cycles", True,
               "|bias| of O-P\nin % of sigma Ctl")]
    label_w, width_tab = 0.28, 0.35
    hover, axes, x = [], [], label_w
    for metric, conf, wins, total, neg, title in tables:
        ax = fig.add_axes([x, body[0], width_tab, body[1]])
        _region_table(ax, idx, keys, regs, metric, conf, wins, total, neg, mode, False,
                      hover, title, row_in, lambda k: f"{k[0]} {k[1]}")
        axes.append(ax)
        x += width_tab + 0.015
    tr = mpl.transforms.blended_transform_factory(fig.transFigure, axes[0].transData)
    # by variable: the variable once, in bold, on the first of its rows from
    # the top; the kind of station on every row, with a line between variables
    for yi, (blk, lab) in enumerate(keys):
        fig.text(label_w - 0.006, yi + 0.5, blk, transform=tr, ha="right", va="center",
                 fontsize=font_size("row"), color="#1F2933")
        above = keys[yi + 1][1] if yi + 1 < len(keys) else None
        if lab != above:
            fig.text(0.008, yi + 0.5, lab, transform=tr, ha="left",
                     va="center", fontsize=font_size("block"), fontweight="bold",
                     color="#1F2933")
            if yi + 1 < len(keys):
                for ax in axes:
                    ax.axhline(yi + 1, color="#6B7280", lw=2.0, clip_on=False)
    _header(fig, fig_h, head_in, "Scorecard  \u00b7  surface  \u00b7  O-P, Exp against Ctl",
            names, datestart, dateend, n_cycles, n_skipped, flag, land_ocean, mode)
    save_figure(fig, out_png, svg=svg, dpi=DPI)
    fig.canvas.draw()
    write_hover_rects(fig, out_png, [(*p.get_window_extent().extents, t) for p, t in hover],
                      dpi=DPI)
    plt.close(fig)
    return out_png


def _layer_label(layer: str) -> str:
    if layer == "sfc":
        return "surface"
    if layer == "all":
        return "all channels"
    if layer == "total":
        return "total, all levels"
    lo, hi = (float(x) for x in layer.split("-"))
    return f"{layer} km  ({_p(_hpa(lo))}-{_p(_hpa(hi))} hPa)"


def draw_all_card(cells: pd.DataFrame, theme: str, region: str, exps: Sequence[str],
                  ctl: str, mode: str, datestart: str, dateend: str, flag: str,
                  land_ocean: str, n_cycles, out_png: str, svg: bool = False) -> str:
    """One theme in one region, every experience against the control side
    by side: a row per family, variable and layer (the highest layer at the
    top of its block), a column per experience."""
    from pikobs.figures import write_hover_rects
    radiances = theme == "radiances"
    surface = theme == "surface"
    blocks = list(dict.fromkeys(zip(cells["block"], cells["label"])))
    top_down = []
    for blk, lab in blocks:
        here = cells[(cells["block"] == blk) & (cells["label"] == lab)]
        # the total first, then from the highest layer down
        for layer in sorted(set(here["layer"]), key=lambda c: -_height_rank(c)):
            top_down.append((blk, lab, layer))
    keys = list(reversed(top_down))                      # yi = 0 at the bottom
    cols = [e for e in exps if e in set(cells["exp"])]
    idx = {(r.exp, (r.block, r.label, r.layer)): r for r in cells.itertuples(index=False)}
    many = len(keys) > 45
    head_in, cols_in, foot_in = 3.3, 2.5, 0.3
    cols_in = max(cols_in, _cols_in(locals().get('regs') or locals().get('regions') or ()))
    row_in = 0.32 if many else 0.85
    fig_h = head_in + cols_in + row_in * len(keys) + foot_in
    fig = plt.figure(figsize=(26.0, fig_h), facecolor="white")
    body = [foot_in / fig_h, row_in * len(keys) / fig_h]
    if radiances:
        tables = [("d_sigma", "sigma_conf", "sigma_wins", "cycles", True,
                   "sigma of O-P\n(Exp - Ctl) / Ctl  [%]"),
                  ("d_n", "n_conf", "n_wins", "n_cycles", False,
                   "observations used\n(Exp - Ctl) / Ctl  [%]")]
    else:
        tables = [("d_sigma", "sigma_conf", "sigma_wins", "cycles", True,
                   "sigma of O-P\n(Exp - Ctl) / Ctl  [%]"),
                  ("d_bias", "bias_conf", "bias_wins", "bias_cycles", True,
                   "|bias| of O-P\nin % of sigma Ctl")]
    label_w, width_tab = 0.33, 0.325
    hover, axes, x = [], [], label_w
    for metric, conf, wins, total, neg, title in tables:
        ax = fig.add_axes([x, body[0], width_tab, body[1]])
        _region_table(ax, idx, keys, cols, metric, conf, wins, total, neg, mode, many,
                      hover, title, row_in, lambda k: f"{k[0]} {k[1]} {_layer_label(k[2])}")
        axes.append(ax)
        x += width_tab + 0.012
    tr = mpl.transforms.blended_transform_factory(fig.transFigure, axes[0].transData)
    for yi, (blk, lab, layer) in enumerate(keys):
        # the surface by variable: the variable in bold, the kind of station beside
        fig.text(label_w - 0.006, yi + 0.5, blk if surface else _layer_label(layer),
                 transform=tr, ha="right", va="center", fontsize=0.85 * font_size("row"),
                 color="#1F2933")
        group = (lambda k: k[1]) if surface else (lambda k: k[:2])
        above = group(keys[yi + 1]) if yi + 1 < len(keys) else None
        if group((blk, lab, layer)) != above:            # the top row of its block
            for ax in axes:
                ax.axhline(yi + 1, color="#6B7280", lw=2.0, clip_on=False)
            name = blk if radiances else (lab if surface else f"{blk}  {lab}")
            dagger = bool(cells[(cells["block"] == blk) & (cells["label"] == lab)]
                          .get("flag_exp_only", pd.Series([False])).any())
            fig.text(0.008, yi + 0.5, "\n".join(textwrap.wrap(name + (" \u2020" if dagger
                                                                     else ""), 22)),
                     transform=tr, ha="left", va="center", fontsize=font_size("block"),
                     fontweight="bold", color="#1F2933")
    title = THEME_TITLE.get(theme, theme)
    if theme == "ro_ch" and not (cells["family"] == "ch").any():
        title = "GPS-RO"
    _header(fig, fig_h, head_in, f"Scorecard  \u00b7  {title}  \u00b7  {region}  \u00b7  "
            f"every experience against Ctl", (ctl, ", ".join(cols)), datestart, dateend,
            n_cycles, 0, flag, land_ocean, mode, "radiances on the cycles" if radiances else None)
    save_figure(fig, out_png, svg=svg, dpi=DPI)
    fig.canvas.draw()
    write_hover_rects(fig, out_png, [(*p.get_window_extent().extents, t) for p, t in hover],
                      dpi=DPI)
    plt.close(fig)
    return out_png
