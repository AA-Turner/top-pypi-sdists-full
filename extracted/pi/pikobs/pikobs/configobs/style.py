#!/usr/bin/python3
"""The look of every pikobs figure, in one place.

A colour should mean the same thing in every module: blue is the
control, red is the experience, and when a test says one of them wins,
the verdict is written in the colour of the winner. The same goes for
the frame of an axis, the header of a figure and the size of the type --
small decisions, but a reader who moves between zone, profile and
timeserie should never have to relearn them.

Modules import what they need::

    from pikobs.configobs.style import (CTL_COLOUR, EXP_COLOUR, DPI,
                                        STYLE, header, style_axes)

    with plt.rc_context(STYLE):
        fig = plt.figure(figsize=(16, 9))
        ...
        header(fig, "A120 vs CTL", "sw  |  WIND SPEED  |  ...")

Vocabulary goes with the colours: what the figures call **sigma** is the
standard deviation of a departure, **bias** is its mean, and a departure
is **O-P** or **O-A**, never "innovation" in one module and "departure"
in the next.
"""

from typing import Optional, Sequence

import matplotlib as mpl

__all__ = ["CTL_COLOUR", "EXP_COLOUR", "EXP_COLOURS", "EXP_BETTER",
           "CTL_BETTER", "NEUTRAL", "GREY_TEXT", "QC_ASSIMILATED",
           "QC_OTHER", "QC_PALETTE", "QC_BLUES", "STATION_CMAP", "DPI",
           "STYLE", "style_axes", "header", "run_colours", "run_styles",
           "better_colour", "SIGMA", "BIAS"]

# ─────────────────────────────────────────────────────────────────────────────
# Colours
# ─────────────────────────────────────────────────────────────────────────────

CTL_COLOUR = '#2166AC'      # the control: blue, everywhere
EXP_COLOUR = '#D62728'      # the experience: red
# more than one experience: red first, then warm colours that still read
# as "not the control"
EXP_COLOURS = ['#D62728', '#E6550D', '#8C2D04', '#F768A1', '#7A0177']

# the verdict of a test takes the colour of the run that wins
EXP_BETTER = '#B2182B'
CTL_BETTER = '#2166AC'
NEUTRAL = '#777777'         # not significant, or nothing to say
GREY_TEXT = '#5F6B76'       # subtitles, notes, anything secondary

# quality control: everything carrying bit 12 in blues, light to dark,
# so a glance separates what entered the analysis from what did not
QC_ASSIMILATED = '#2C7FB8'
QC_BLUES = ['#6BAED6', '#4292C6', '#2C7FB8', '#08519C', '#08306B']
QC_OTHER = '#BDBDBD'        # the rare ones, pooled
QC_PALETTE = ['#E69F00', '#009E73', '#CC79A7', '#D55E00', '#882255',
              '#F0E442', '#44AA99', '#999933', '#AA4499', '#332288',
              '#88CCEE', '#117733']
STATION_CMAP = 'tab20'      # one colour per station or instrument type

DPI = 150

# What the words mean, so two modules do not name the same number
# differently.
SIGMA = "sigma"             # standard deviation of a departure
BIAS = "bias"               # its mean

STYLE = {"font.family": "DejaVu Sans", "axes.titlesize": 11,
         "axes.labelsize": 10, "legend.fontsize": 8.5,
         "figure.dpi": DPI, "savefig.dpi": DPI}


# ─────────────────────────────────────────────────────────────────────────────
# Axes and header
# ─────────────────────────────────────────────────────────────────────────────

def style_axes(ax, grid: bool = True) -> None:
    """Light frame, soft grid, grid under the data."""
    ax.set_facecolor("white")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#B0B0B0")
    ax.tick_params(axis="both", which="both", labelsize=9, colors="#333333")
    if grid:
        ax.grid(True, which="major", linestyle="--", linewidth=0.7,
                alpha=0.25)
    ax.set_axisbelow(True)


def header(fig, title: str, subtitle: str = "", x: float = 0.055,
           rule: bool = True) -> None:
    """The title of a figure, its subtitle, and a rule under them.

    Positions are in inches from the top, so a short figure and a tall
    one get the same header rather than one squashed against the axes.
    """
    h = fig.get_figheight()
    fig.text(x, 1 - 0.12 / h, title, ha='left', va='top', fontsize=15,
             fontweight='bold', color='#1F2933')
    if subtitle:
        fig.text(x, 1 - 0.45 / h, subtitle, ha='left', va='top', fontsize=9,
                 color=GREY_TEXT, linespacing=1.45)
    if rule:
        y = 1 - (0.45 + 0.20 * (subtitle.count("\n") + 1.6)) / h
        fig.add_artist(mpl.lines.Line2D([x, 0.985], [y, y],
                                        transform=fig.transFigure,
                                        color='#D9DDE2', lw=0.9))


# ─────────────────────────────────────────────────────────────────────────────
# Runs
# ─────────────────────────────────────────────────────────────────────────────

def run_colours(runs: Sequence[str],
                control: Optional[str] = None) -> dict:
    """A colour per run: the control blue, the experiences red and warm.

    Without a control the single run is an experience, so it is red: a
    lone blue curve would suggest a comparison that is not there.
    """
    runs = list(runs)
    if control is None:
        if len(runs) == 1:
            return {runs[0]: EXP_COLOUR}
        control = runs[0]
    out = {control: CTL_COLOUR}
    i = 0
    for r in runs:
        if r == control:
            continue
        out[r] = EXP_COLOURS[i % len(EXP_COLOURS)]
        i += 1
    return out


def run_styles(runs: Sequence[str], control: Optional[str] = None) -> dict:
    """A line style per run: where two curves agree, one would otherwise
    hide the other."""
    runs = list(runs)
    control = control if control is not None else (runs[0] if runs else None)
    dashes = ['--', '-.', (0, (3, 1, 1, 1, 1, 1)), ':']
    out, i = {}, 0
    for r in runs:
        if r == control:
            out[r] = '-'
        else:
            out[r] = dashes[i % len(dashes)]
            i += 1
    return out


def better_colour(experience_wins, significant=True) -> str:
    """The colour of a verdict: the winner, or grey when it is noise."""
    if not significant:
        return NEUTRAL
    return EXP_BETTER if experience_wins else CTL_BETTER
