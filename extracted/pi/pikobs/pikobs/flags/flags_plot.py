#!/usr/bin/python3
"""Figures of pikobs.flags.

One figure per selection, organised in four visual blocks:

* a stacked bar chart of the flag combinations, cycle by cycle, in percent
* a legend listing each combination, its bits, its average share and its
  average number of observations
* a summary over the channels that took part in the assimilation
* one pie chart per configured group of bits

The groups and the meaning of the bits come from
``pikobs.configobs.flag_groups``, so a new instrument is edited there.
"""

import colorsys
import hashlib
import json
import os
import re
import textwrap
import traceback

from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

import matplotlib
matplotlib.use('Agg')

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.patches import FancyBboxPatch

import pikobs

from pikobs.figures import save_figure
from pikobs.configobs.style import EXP_COLOUR
from pikobs.obsdb import open_result
from pikobs.configobs.flag_groups import (
    BIT_ASSIMILATED,
    ASSIMILATED_KINDS,
    OTHER_NOT_ASSIMILATED,
    NO_BIT_SET,
    Titled,
    first_match,
    is_radiance,
    reasons_for,
    BIT_DESCRIPTIONS,
    NOT_IN_SUMMARY,
    bits_active,
    group_title,
    groups_for,
    matches,
)


# =============================================================================
# General configuration
# =============================================================================

CYCLE_HOURS = 6
DPI = 110


# =============================================================================
# Figure geometry
# =============================================================================

# The bar chart grows with the period so long periods remain zoomable
# in the web viewer.
INCH_PER_CYCLE = 0.050

BAR_MIN_WIDTH = 16.0
BAR_MAX_WIDTH = 46.0

# Main time-series block.
BAR_HEIGHT = 6.2

# Legend.
LEGEND_ROW_HEIGHT = 0.15
LEGEND_MIN_HEIGHT = 0.8

# Summary block.
SUMMARY_HEIGHT = 1.6

# Pie charts.
#
# A little extra vertical room is deliberately reserved because the title
# of the next row must never collide with the percentage of the row above.
PIE_HEIGHT = 5.6
PIES_PER_ROW = 2                    # two group lists a row
LIST_ROWS = 8                       # combinations listed per group

# Maximum number of flag combinations explicitly listed.
MAX_LEGEND_ENTRIES = 40


# =============================================================================
# Visual style
# =============================================================================

GRID_COLOUR = '#d7dadd'

TEXT_DARK = '#202428'
TEXT_MID = '#535960'
TEXT_LIGHT = '#737980'

SEPARATOR = '#357ABD'

SUMMARY_FACE = '#f6f8fa'
SUMMARY_EDGE = '#c8cdd2'

PIE_EDGE = '#666666'


# =============================================================================
# Helpers
# =============================================================================

def _safe(text: Any) -> str:
    return re.sub(
        r'[^A-Za-z0-9._+-]',
        '_',
        str(text),
    )


def figure_name(
    experience,
    family,
    region,
    id_stn,
    vcoord,
    varno,
    land_ocean='all',
    special='all',
) -> str:
    """Name of the PNG; the viewer and the plot must agree on it. The
    land filter and the special value are in it only when there is one."""

    extra = "".join(f"_{_safe(x)}" for x in (land_ocean, special)
                    if x not in (None, '', 'all'))

    return (
        f"flags_{_safe(experience)}_"
        f"{_safe(family)}_"
        f"{_safe(region)}{extra}_"
        f"{_safe(id_stn)}_"
        f"ch{_safe(vcoord)}_"
        f"varno{_safe(varno)}.png"
    )


def _cycles(
    date_start: str,
    date_end: str,
) -> List[str]:
    """Every expected 6-hour cycle in the requested period."""

    cur = datetime.strptime(
        str(date_start),
        '%Y%m%d%H',
    )

    end = datetime.strptime(
        str(date_end),
        '%Y%m%d%H',
    )

    out = []

    while cur <= end:

        out.append(
            cur.strftime('%Y%m%d%H')
        )

        cur += timedelta(
            hours=CYCLE_HOURS
        )

    return out


def flag_color(
    flag: Any,
    mapping: Optional[Dict[str, str]] = None,
) -> str:
    """A stable colour per flag value, identical in every figure."""

    key = str(flag)

    if mapping and key in mapping:
        return mapping[key]

    h = int(
        hashlib.md5(
            key.encode('utf-8')
        ).hexdigest(),
        16,
    )

    hue = (
        h % 1000
    ) / 1000.0

    sat = (
        0.50
        + ((h // 1000) % 40) / 100.0
    )

    val = (
        0.60
        + ((h // 40000) % 30) / 100.0
    )

    return mcolors.to_hex(
        colorsys.hsv_to_rgb(
            hue,
            sat,
            val,
        )
    )


def _load_colour_mapping() -> Dict[str, str]:

    path = os.path.join(
        os.path.dirname(pikobs.__file__),
        'extension',
        'color_mapping.json',
    )

    try:

        with open(path) as fh:
            return json.load(fh)

    except (
        OSError,
        json.JSONDecodeError,
    ):
        return {}


def _fmt_pct(value: float) -> str:
    """Readable percentage without unnecessary digits."""

    if value >= 10:
        return f"{value:.1f}"

    if value >= 1:
        return f"{value:.2f}"

    if value >= 0.01:
        return f"{value:.3f}"

    return f"{value:.3g}"


def _fmt_obs(
    total: float,
    n_cycles: int,
) -> str:
    """Average number of observations per cycle."""

    per_cycle = (
        total
        / max(n_cycles, 1)
    )

    if per_cycle >= 1:
        return f"{int(round(per_cycle)):,}"

    return f"{per_cycle:.2g}"


# =============================================================================
# Data
# =============================================================================

def _where(
    task: Dict[str, Any],
) -> Tuple[str, list]:

    clause = [
        'region = ?',
        'land_ocean = ?',
        'special = ?',
        'varno = ?',
    ]

    args: list = [
        task['region'],
        task.get('land_ocean', 'all'),
        task.get('special', 'all'),
        task['varno'],
    ]

    if str(task['vcoord']) != 'join':

        clause.append(
            'vcoord = ?'
        )

        args.append(
            task['vcoord']
        )

    return (
        ' AND '.join(clause)
        + task.get(
            'stn_sql',
            '',
        ),
        args,
    )


def _read(
    task: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """Counts per cycle/flag plus channels involved in assimilation."""

    where, args = _where(
        task
    )

    with open_result(
        task['db_file']
    ) as conn:

        rows = conn.execute(
            f"""
            SELECT date, flag, SUM(n)
            FROM flag_observations
            WHERE {where}
            GROUP BY date, flag;
            """,
            args,
        ).fetchall()

        # Channels of THIS selection that participated in assimilation.
        assim = [
            r[0]
            for r in conn.execute(
                f"""
                SELECT DISTINCT vcoord
                FROM flag_observations
                WHERE {where}
                  AND (flag & {1 << BIT_ASSIMILATED})
                      = {1 << BIT_ASSIMILATED};
                """,
                args,
            )
        ]

        per_channel = conn.execute(
            f"""
            SELECT vcoord, flag, SUM(n)
            FROM flag_observations
            WHERE {where}
            GROUP BY vcoord, flag;
            """,
            args,
        ).fetchall()

    if not rows:
        return None

    counts: Dict[
        str,
        Dict[int, int],
    ] = defaultdict(dict)

    for date, flag, n in rows:

        counts[str(date)][int(flag)] = int(
            n or 0
        )

    return {
        'counts': counts,
        'assimilated_channels': set(assim),
        'per_channel': per_channel,
    }


# =============================================================================
# Main figure
# =============================================================================

def flags_plot(
    task: Dict[str, Any],
) -> Optional[str]:
    """Draw the flag distribution of one selection."""

    data = _read(
        task
    )

    if data is None:
        return None

    dates = [
        d
        for d in _cycles(
            task['datestart'],
            task['dateend'],
        )
        if d in data['counts']
    ]

    if not dates:
        return None

    counts = data['counts']

    mapping = _load_colour_mapping()

    # -------------------------------------------------------------------------
    # Global statistics
    # -------------------------------------------------------------------------

    totals = {
        d: sum(
            counts[d].values()
        )
        for d in dates
    }

    grand_total = (
        sum(totals.values())
        or 1
    )

    flags = sorted(
        {
            f
            for d in dates
            for f in counts[d]
        },
        key=lambda f: -sum(
            counts[d].get(
                f,
                0,
            )
            for d in dates
        ),
    )

    share = {
        f:
            sum(
                counts[d].get(
                    f,
                    0,
                )
                for d in dates
            )
            / grand_total
            * 100
        for f in flags
    }

    obs = {
        f:
            sum(
                counts[d].get(
                    f,
                    0,
                )
                for d in dates
            )
        for f in flags
    }

    # -------------------------------------------------------------------------
    # Groups / pies / summary
    # -------------------------------------------------------------------------

    groups = groups_for(
        task['family']
    )

    # every observation once: assimilated or not, its kind or its first
    # reason; a radiance leaves its blacklist out
    breakdown = _breakdown(data, task['family'])
    pie_total = breakdown['total'] or 1
    pie_scope = ('of the observations of the channels in use'
                 if breakdown['radiance'] else 'of all observations')
    pie_data = _breakdown_pies(breakdown)

    n_pies = len(
        pie_data
    )
    # a row of group lists is as tall as its longest list
    list_rows_by_row = [max(min(len(p[2]), LIST_ROWS) + (len(p[2]) > LIST_ROWS)
                            for p in pie_data[r:r + PIES_PER_ROW])
                        for r in range(0, len(pie_data), PIES_PER_ROW)] or [1]
    pie_heights = [0.80 + 0.30 * n for n in list_rows_by_row]

    summary = _breakdown_text(breakdown)

    pie_rows = (
        int(
            np.ceil(
                n_pies
                / PIES_PER_ROW
            )
        )
        if n_pies
        else 0
    )

    # -------------------------------------------------------------------------
    # Legend
    # -------------------------------------------------------------------------

    legend_entries = min(
        len(flags),
        MAX_LEGEND_ENTRIES,
    )

    legend_flags = flags[
        :legend_entries
    ]

    legend_labels = [
        _legend_label(
            flag,
            share[flag],
            obs[flag],
            len(dates),
        )
        for flag in legend_flags
    ]

    # Full descriptions need width, so use at most two columns.
    # one column up to 8 combinations, two up to 24, three beyond
    legend_cols = (1 if legend_entries <= 8
                   else 2 if legend_entries <= 24 else 3)

    # -------------------------------------------------------------------------
    # Real legend height
    # -------------------------------------------------------------------------

    line_counts = [
        max(
            1,
            label.count('\n') + 1,
        )
        for label in legend_labels
    ]

    rows_per_col = max(
        1,
        int(
            np.ceil(
                legend_entries
                / legend_cols
            )
        ),
    )

    column_lines = []

    for col in range(
        legend_cols
    ):

        start = (
            col
            * rows_per_col
        )

        end = min(
            start + rows_per_col,
            legend_entries,
        )

        visual_lines = 0.0

        for n_lines in line_counts[
            start:end
        ]:

            visual_lines += (
                n_lines
                + 0.35
            )

        column_lines.append(
            visual_lines
        )

    max_legend_lines = (
        max(column_lines)
        if column_lines
        else 1.0
    )

    legend_height = max(
        LEGEND_MIN_HEIGHT,
        LEGEND_ROW_HEIGHT
        * max_legend_lines
        + 0.2,
    )

    # -------------------------------------------------------------------------
    # Figure dimensions
    # -------------------------------------------------------------------------

    width = float(
        np.clip(
            7.0
            + INCH_PER_CYCLE
            * len(dates),
            BAR_MIN_WIDTH,
            BAR_MAX_WIDTH,
        )
    )

    # the table of the summary: as tall as its lines
    summary_height = ((0.3 + 0.19 * (summary.count('\n') + 1))
                      if summary else 0.0)

    pie_section_header = (
        0.48
        if n_pies
        else 0.0
    )

    height = (
        BAR_HEIGHT
        + legend_height
        + summary_height
        + pie_section_header
        + sum(pie_heights[:pie_rows])
    )
    # in inches: the header, the blocks at their height, one fixed gap
    # between two blocks -- nothing grows with the size of the pies
    TOP_IN, BOTTOM_IN, GAP_IN = 1.35, 0.9, 1.0
    n_blocks = 2 + bool(summary) + bool(n_pies) + pie_rows
    height = TOP_IN + height + GAP_IN * (n_blocks - 1) + BOTTOM_IN

    fig = plt.figure(
        figsize=(
            width,
            height,
        ),
        facecolor='white',
    )

    # -------------------------------------------------------------------------
    # Use 8 grid columns.
    #
    # Each normal pie occupies two columns:
    #
    #   [0:2] [2:4] [4:6] [6:8]
    #
    # This lets us centre incomplete final rows.
    # -------------------------------------------------------------------------

    GRID_COLS = (
        PIES_PER_ROW * 2
    )

    ratios = [
        BAR_HEIGHT,
        legend_height,
    ]

    if summary:

        ratios.append(
            summary_height
        )

    if n_pies:

        ratios.append(
            pie_section_header
        )

    ratios.extend(
        pie_heights[:pie_rows]
    )

    gs = fig.add_gridspec(
        len(ratios),
        GRID_COLS,
        height_ratios=ratios,

        # the gap between two blocks: GAP_IN inches, whatever their size
        hspace=GAP_IN / float(np.mean(ratios)),

        wspace=0.20,
        left=0.055,
        right=0.975,
        top=1.0 - TOP_IN / height,
        bottom=BOTTOM_IN / height,
    )

    # =========================================================================
    # Figure header
    # =========================================================================

    def at(inch):
        return 1.0 - inch / height

    def _when(stamp) -> str:
        s = str(stamp)
        return f"{s[:4]}-{s[4:6]}-{s[6:8]} {s[8:10]} UTC"

    try:
        var_name = pikobs.type_varno(str(task['varno']))[0]
    except Exception:
        var_name = f"varno {task['varno']}"
    x0 = 0.055
    fig.text(x0, at(0.12), f"{var_name}  \u00b7  flag combinations per 6-h cycle",
             ha='left', va='top', fontsize=16, fontweight='bold', color=TEXT_DARK)
    fig.text(0.975, at(0.14), f"{_when(task['datestart'])}  to  "
             f"{_when(task['dateend'])}", ha='right', va='top', fontsize=11,
             color=TEXT_MID)
    where = str(task['region']) + ''.join(
        f", {x}" for x in (task.get('land_ocean', 'all'),
                          task.get('special_label', 'all'))
        if x not in (None, '', 'all'))
    fig.text(x0, at(0.47), "  \u00b7  ".join(
        [str(task['family']), where, f"stations {task['id_stn']}",
         f"channel {task['vcoord']}"]),
        ha='left', va='top', fontsize=11.5, color=TEXT_MID)
    fig.text(x0, at(0.76), f"Exp  {task['experience']}", ha='left', va='top',
             fontsize=13.5, fontweight='bold', color=EXP_COLOUR)
    fig.add_artist(plt.Line2D([x0, 0.975], [at(1.08), at(1.08)],
                              transform=fig.transFigure, color='#D9DDE2',
                              linewidth=0.9))

    # =========================================================================
    # Stacked bar chart
    # =========================================================================

    ax = fig.add_subplot(
        gs[
            0,
            :,
        ]
    )

    ax.set_facecolor(
        '#fcfcfc'
    )
    ax_bars = ax

    x = np.arange(
        len(dates)
    )

    bottom = np.zeros(
        len(dates)
    )
    segments = []                  # every band, for the map under the mouse

    for flag in flags:

        values = np.array(
            [
                counts[d].get(
                    flag,
                    0,
                )
                / (
                    totals[d]
                    or 1
                )
                * 100
                for d in dates
            ]
        )

        ax.bar(
            x,
            values,
            bottom=bottom,
            width=1.0,
            align='edge',
            color=flag_color(
                flag,
                mapping,
            ),
            linewidth=0,
            label=_legend_label(
                flag,
                share[flag],
                obs[flag],
                len(dates),
            ),
        )

        segments.append((flag, bottom.copy(), values.copy()))
        bottom += values

    ax.set_xlim(
        0,
        len(dates),
    )

    ax.set_ylim(
        0,
        100,
    )

    ax.set_yticks(
        np.arange(
            0,
            101,
            20,
        )
    )

    ax.grid(
        axis='y',
        color=GRID_COLOUR,
        linewidth=0.6,
        linestyle=':',
        alpha=0.70,
    )

    ax.set_axisbelow(
        True
    )

    # -------------------------------------------------------------------------
    # Cycle ticks
    # -------------------------------------------------------------------------

    # a tick at 00 UTC with the day, fewer on a long period; the month where
    # it changes -- as in timeserie
    days = [i for i, d in enumerate(dates) if str(d)[8:10] == '00'] or [0]
    step = max(1, int(np.ceil(len(days) / 16)))
    tick_indices = np.array(days[::step])
    tick_labels, month = [], None
    for i in tick_indices:
        day = datetime.strptime(str(dates[i])[:8], '%Y%m%d')
        tick_labels.append(day.strftime('%d %b') if day.month != month
                           else day.strftime('%d'))
        month = day.month
    ax.set_xticks(tick_indices + 0.5)
    ax.set_xticklabels(tick_labels, fontsize=10)
    ax.tick_params(
        axis='y',
        labelsize=10.5,
        length=3,
        width=0.6,
    )

    ax.tick_params(
        axis='x',
        length=3,
        width=0.6,
    )

    ax.set_xlabel(
        'Cycle',
        fontsize=12,
        fontweight='semibold',
        labelpad=8,
    )

    ax.set_ylabel(
        'Percentage of observations',
        fontsize=12,
        fontweight='semibold',
        labelpad=8,
    )

    for spine in ax.spines.values():

        spine.set_linewidth(
            0.7
        )

        spine.set_color(
            '#777777'
        )

    # =========================================================================
    # Flag legend
    # =========================================================================

    ax_leg = fig.add_subplot(
        gs[
            1,
            :,
        ]
    )

    ax_leg.axis(
        'off'
    )

    handles, _ = (
        ax.get_legend_handles_labels()
    )

    ax_leg.text(
        0.0,
        1.08,
        'Flag combinations',
        transform=ax_leg.transAxes,
        fontsize=11.5,
        fontweight='bold',
        va='bottom',
        color=TEXT_DARK,
    )

    note = (
        "Share = percentage over the complete period"
        "    •    "
        "obs/cycle = mean number per 6-h cycle"
        "    •    "
        "a group below = its flag combinations, largest first"
    )

    if len(flags) > legend_entries:

        note += (
            f"    •    "
            f"{len(flags) - legend_entries} "
            f"rarer combinations are not listed"
        )

    ax_leg.text(
        0.0,
        1.00,
        note,
        transform=ax_leg.transAxes,
        fontsize=9.2,
        fontstyle='italic',
        va='bottom',
        color=TEXT_LIGHT,
    )

    ax_leg.legend(
        handles[:legend_entries],
        legend_labels,
        loc='upper left',
        bbox_to_anchor=(
            0.0,
            0.94,
        ),
        ncol=legend_cols,
        frameon=False,
        fontsize=8.8,
        handlelength=1.35,
        handletextpad=0.55,
        columnspacing=2.1,
        borderaxespad=0.0,
        labelspacing=0.68,
    )

    # =========================================================================
    # Assimilation summary
    # =========================================================================

    current_row = 2

    if summary:

        ax_sum = fig.add_subplot(
            gs[
                current_row,
                :,
            ]
        )

        ax_sum.axis(
            'off'
        )

        ax_sum.text(0.0, 1.0, summary, transform=ax_sum.transAxes,
                    ha='left', va='top', family='monospace',
                    fontsize=10.5, color=TEXT_DARK, linespacing=1.4)

        current_row += 1

    # =========================================================================
    # Pie section heading
    # =========================================================================

    if n_pies:

        ax_pie_title = fig.add_subplot(
            gs[
                current_row,
                :,
            ]
        )

        ax_pie_title.axis(
            'off'
        )

        ax_pie_title.text(
            0.0,
            0.70,
            'Flag groups — share ' + pie_scope,
            ha='left',
            va='center',
            fontsize=12,
            fontweight='bold',
            color=TEXT_DARK,
            transform=ax_pie_title.transAxes,
        )

        ax_pie_title.plot(
            [
                0.0,
                1.0,
            ],
            [
                0.15,
                0.15,
            ],
            transform=ax_pie_title.transAxes,
            color='#d0d4d8',
            linewidth=0.8,
            clip_on=False,
        )

        current_row += 1

    # =========================================================================
    # Pie charts
    # =========================================================================

    n_full_rows = (
        n_pies
        // PIES_PER_ROW
    )

    n_last = (
        n_pies
        % PIES_PER_ROW
    )

    pie_flags = []                 # every pie, for the map under the mouse
    for i, (
        group,
        pct,
        per_flag,
    ) in enumerate(
        pie_data
    ):

        pie_row = (
            i
            // PIES_PER_ROW
        )

        pos_in_row = (
            i
            % PIES_PER_ROW
        )

        # ---------------------------------------------------------------------
        # Exact centring with an 8-column GridSpec.
        #
        # Full row:
        #
        #   0:2   2:4   4:6   6:8
        #
        # Last row:
        #
        #   1 pie  -> 3:5
        #   2 pies -> 2:4 and 4:6
        #   3 pies -> 1:3, 3:5 and 5:7
        # ---------------------------------------------------------------------

        is_last_incomplete_row = (
            n_last > 0
            and pie_row == n_full_rows
        )

        if is_last_incomplete_row:

            total_span = (
                n_last
                * 2
            )

            start_offset = (
                GRID_COLS
                - total_span
            ) // 2

            col_start = (
                start_offset
                + pos_in_row * 2
            )

        else:

            col_start = (
                pos_in_row
                * 2
            )

        col_end = (
            col_start
            + 2
        )

        row = (
            current_row
            + pie_row
        )

        ax_pie = fig.add_subplot(
            gs[
                row,
                col_start:col_end,
            ]
        )

        # the group as a list: its combinations one per row, largest first,
        # a bar of its share of the group and its numbers written
        ax_pie.axis('off')
        ax_pie.set_xlim(0, 1)
        ax_pie.set_ylim(0, 1)
        items = sorted(per_flag.items(), key=lambda kv: -kv[1])
        rest = items[LIST_ROWS:]
        rows = [(f, c) for f, c in items[:LIST_ROWS]]
        if rest:
            rows.append((None, sum(c for _, c in rest)))
        n_group = sum(per_flag.values()) or 1
        step = 1.0 / (list_rows_by_row[i // PIES_PER_ROW] + 2.6)
        tr = ax_pie.transAxes
        ax_pie.text(0.0, 1.0, group_title(group), transform=tr, ha='left',
                    va='top', fontsize=11, fontweight='bold', color=TEXT_DARK)
        # its share on its own line: a long one never runs into the title
        ax_pie.text(0.0, 1.0 - 1.05 * step,
                    f"{_pct_text(pct)}  {pie_scope}   \u00b7   {n_group:,} obs",
                    transform=tr, ha='left', va='top', fontsize=9.5,
                    color=TEXT_MID)
        bar_x0, bar_w = 0.30, 0.34
        row_items = []
        for r_i, (flag, count) in enumerate(rows):
            y = 1.0 - (r_i + 2.6) * step
            share = count / n_group
            if flag is None:
                label, colour = f"{len(rest)} other combinations", '#cfd3d8'
            else:
                bits = bits_active(flag)
                label = ("no bit set" if not bits
                         else "bits " + "+".join(str(b) for b in bits))
                colour = flag_color(flag, mapping)
            ax_pie.text(0.0, y, label, transform=tr, ha='left', va='center',
                        fontsize=9.5, color=TEXT_DARK)
            ax_pie.add_patch(plt.Rectangle(
                (bar_x0, y - 0.32 * step), bar_w, 0.64 * step, transform=tr,
                facecolor='#f3f4f6', edgecolor='#d9dde2', linewidth=0.6))
            ax_pie.add_patch(plt.Rectangle(
                (bar_x0, y - 0.32 * step), bar_w * max(share, 0.004),
                0.64 * step, transform=tr, facecolor=colour, linewidth=0))
            ax_pie.text(bar_x0 + bar_w + 0.02, y,
                        f"{_pct_text(100.0 * share)} of the group   "
                        f"{_pct_text(100.0 * count / pie_total)} of the total",
                        transform=tr, ha='left', va='center', fontsize=9,
                        color=TEXT_MID)
            row_items.append((flag, count, y, step, [f for f, _ in rest]))
        pie_flags.append((ax_pie, group, row_items, n_group))

    # =========================================================================
    # Output
    # =========================================================================

    out_dir = os.path.join(
        task['pathwork'],
        task['family'],
    )

    os.makedirs(
        out_dir,
        exist_ok=True,
    )

    out_file = os.path.join(
        out_dir,
        figure_name(
            task['experience'],
            task['family'],
            task['region'],
            task.get(
                'stn_tag',
                task['id_stn'],
            ),
            task['vcoord'],
            task['varno'],
            task.get('land_ocean', 'all'),
            task.get('special_label', 'all'),
        ),
    )

    save_figure(
        fig,
        out_file,
        svg=task.get(
            'svg',
            False,
        ),
        dpi=DPI,
    )
    _write_map(fig, ax_bars, out_file, segments, dates, counts,
               pie_flags, pie_total)

    plt.close(
        fig
    )

    return out_file


# =============================================================================
# Legend
# =============================================================================

def _legend_label(
    flag,
    share,
    obs,
    n_cycles,
) -> str:
    """Legend entry with the complete active-bit description.

    Descriptions are wrapped onto following lines instead of being truncated.
    """

    bits = bits_active(
        flag
    )

    descriptions = [
        BIT_DESCRIPTIONS.get(
            b,
            f'bit {b}',
        )
        for b in bits
    ]

    description = (
        ', '.join(
            descriptions
        )
        if descriptions
        else 'No active bit description'
    )

    wrapped_description = textwrap.fill(
        description,
        width=78,
        subsequent_indent='    ',
    )

    return (
        f"flag {flag}"
        f"   |   {_fmt_pct(share)}%"
        f"   |   {_fmt_obs(obs, n_cycles)} obs/cycle"
        f"   |   bits {bits}\n"
        f"    {wrapped_description}"
    )


# =============================================================================
# Pie data
# =============================================================================

def _pct_text(x: float) -> str:
    """A share for the eye: 0 when there is none, scientific notation
    when it is tiny, two decimals otherwise."""
    if x == 0:
        return "0 %"
    return f"{x:.1e} %" if abs(x) < 0.01 else f"{x:.2f} %"


def _breakdown(data, family) -> Dict[str, Any]:
    """Every observation once: assimilated or not; its kind, or its first
    reason and every reason it carries. A radiance leaves its blacklist out."""
    radiance = is_radiance(family)
    reasons = reasons_for(family)
    per_flag_n: Dict[int, int] = defaultdict(int)
    for per in data['counts'].values():
        for flag, n in per.items():
            per_flag_n[int(flag)] += int(n or 0)
    total = black = 0
    first: Dict[Tuple[str, str], Dict[int, int]] = defaultdict(lambda: defaultdict(int))
    carries: Dict[str, int] = defaultdict(int)
    pattern: Dict[str, Tuple] = {}
    for flag, n in per_flag_n.items():
        bits = bits_active(flag)
        if radiance and 8 in bits:
            black += n
            continue
        total += n
        if BIT_ASSIMILATED in bits:
            g = first_match(ASSIMILATED_KINDS, bits) or ASSIMILATED_KINDS[-1]
            first[('a', g.title)][flag] += n
        else:
            g = (NO_BIT_SET if not bits else
                 first_match(reasons, bits) or OTHER_NOT_ASSIMILATED)
            first[('r', g.title)][flag] += n
            for title in {r.title for r in reasons if matches(r, bits)}:
                carries[title] += n
        pattern.setdefault(g.title, g)
    order = {'a': list(dict.fromkeys(k.title for k in ASSIMILATED_KINDS)),
             'r': list(dict.fromkeys([r.title for r in reasons]
                                     + [NO_BIT_SET.title,
                                        OTHER_NOT_ASSIMILATED.title]))}
    return {'radiance': radiance, 'total': total, 'black': black,
            'first': first, 'carries': carries, 'pattern': pattern,
            'order': order}


def _breakdown_pies(b) -> List[Tuple]:
    """The pies, in every family: ASSIMILATED split into its combinations,
    then one per reason of what is not assimilated."""
    total = b['total'] or 1
    per_a: Dict[int, int] = defaultdict(int)
    for (side, _), per in b['first'].items():
        if side == 'a':
            for flag, n in per.items():
                per_a[flag] += n
    out = []
    if per_a:
        out.append((Titled((BIT_ASSIMILATED,), "ASSIMILATED"),
                    sum(per_a.values()) / total * 100, dict(per_a)))
    for title in b['order']['r']:
        per = b['first'].get(('r', title))
        if per:
            out.append((b['pattern'][title], sum(per.values()) / total * 100,
                        dict(per)))
    return out


def _breakdown_text(b) -> str:
    """The table: ASSIMILATED and every combination with bit 12, NOT
    ASSIMILATED and its reasons (first reason, carries it): 100 % in all."""
    total = b['total']
    if not total:
        return ''

    def pct(n):
        return _pct_text(100.0 * n / total)

    w = 84
    lines = []
    if b['radiance']:
        whole = total + b['black']
        lines.append(f"Blacklisted (bit 8): {100.0 * b['black'] / whole:.2f} % of all "
                     f"observations ({b['black']:,} of {whole:,}), left out -- "
                     f"the shares are over the channels in use")
    lines.append(f"{'':{w}s}{'first reason':>14s}{'obs':>14s}{'carries it':>14s}")
    per_a: Dict[int, int] = defaultdict(int)
    for (side, _), per in b['first'].items():
        if side == 'a':
            for flag, n in per.items():
                per_a[flag] += n
    lines.append(f"{'ASSIMILATED':{w}s}{pct(sum(per_a.values())):>14s}"
                 f"{sum(per_a.values()):>14,d}")
    shown = sorted(per_a.items(), key=lambda kv: -kv[1])
    for flag, n in shown[:12]:
        bits = bits_active(flag)
        other = [x for x in bits if x != BIT_ASSIMILATED]
        what = ", ".join(BIT_DESCRIPTIONS.get(x, f"bit {x}") for x in other) \
            or "Assimilated"
        label = f"bits {'+'.join(str(x) for x in bits)}  {what}"
        lines.append(f"  {label[:w - 3]:{w - 2}s}{pct(n):>14s}{n:>14,d}")
    if len(shown) > 12:
        n_rest = sum(n for _, n in shown[12:])
        lines.append(f"  {'other combinations':{w - 2}s}{pct(n_rest):>14s}{n_rest:>14,d}")
    rows = [(t, sum(b['first'].get(('r', t), {}).values())) for t in b['order']['r']]
    n_not = sum(n for _, n in rows)
    lines.append(f"{'NOT ASSIMILATED':{w}s}{pct(n_not):>14s}{n_not:>14,d}")
    for title, n in rows:
        carry = b['carries'].get(title, 0)
        if not n and not carry:
            continue
        line = f"  {title[:w - 3]:{w - 2}s}{pct(n):>14s}{n:>14,d}"
        if title not in (OTHER_NOT_ASSIMILATED.title, NO_BIT_SET.title):
            line += f"{pct(carry):>14s}"
        lines.append(line)
    lines.append(f"{'':{w}s}{'--------':>14s}{'--------':>14s}")
    lines.append(f"{'':{w}s}{pct(total):>14s}{total:>14,d}")
    return "\n".join(lines)


def _pie_data(
    data,
    groups,
    grand_total,
):
    """Per group: its share and all flag combinations that compose it."""

    per_group: Dict[
        Tuple,
        Dict[int, int],
    ] = defaultdict(
        lambda: defaultdict(int)
    )

    for date, per_flag in data['counts'].items():

        for flag, n in per_flag.items():

            bits = bits_active(
                flag
            )

            for group in groups:

                if matches(
                    group,
                    bits,
                ):

                    per_group[
                        tuple(group)
                    ][flag] += n

    out = []

    for group, per_flag in per_group.items():

        pct = (
            sum(
                per_flag.values()
            )
            / grand_total
            * 100
        )

        out.append(
            (
                group,
                pct,
                dict(per_flag),
            )
        )

    out.sort(
        key=lambda g: -g[1]
    )

    return out


# =============================================================================
# Assimilated-channel summary
# =============================================================================

def _summary_text(
    data,
    groups,
    task,
) -> str:
    """Shares over channels that participated in assimilation."""

    channels = data[
        'assimilated_channels'
    ]

    if not channels:

        return (
            "Assimilated channels: none in this selection,\n"
            "so no share over assimilated data is shown."
        )

    totals: Dict[
        Tuple,
        int,
    ] = defaultdict(int)

    total = 0

    for (
        vcoord,
        flag,
        n,
    ) in data['per_channel']:

        if vcoord not in channels:
            continue

        n = int(
            n or 0
        )

        total += n

        bits = bits_active(
            int(flag)
        )

        for group in groups:

            if matches(
                group,
                bits,
            ):

                totals[
                    tuple(group)
                ] += n

    if not total:
        return ''

    excluded = {
        tuple(g)
        for g in NOT_IN_SUMMARY
    }

    lines = [
        'Share over the channels that are assimilated',
    ]

    for group, count in sorted(
        totals.items(),
        key=lambda kv: -kv[1],
    ):

        if tuple(group) in excluded:
            continue

        lines.append(
            f"{group_title(group)}:"
            f"{count * 100 / total:.4g}%"
        )

    return '\n'.join(
        lines
    )


def _draw_summary(
    ax,
    summary: str,
) -> None:
    """Draw the assimilation summary as a readable four-column grid."""

    lines = [
        line.strip()
        for line in summary.splitlines()
        if line.strip()
    ]

    if not lines:
        return

    title = lines[0]

    raw_entries = lines[
        1:
    ]

    entries = []

    for line in raw_entries:

        if ':' in line:

            name, value = line.rsplit(
                ':',
                1,
            )

        else:

            name = line
            value = ''

        entries.append(
            (
                name.strip(),
                value.strip(),
            )
        )

    ax.set_xlim(
        0,
        1,
    )

    ax.set_ylim(
        0,
        1,
    )

    panel = FancyBboxPatch(
        (
            0.0,
            0.03,
        ),
        1.0,
        0.94,
        boxstyle='round,pad=0.012',
        facecolor=SUMMARY_FACE,
        edgecolor=SUMMARY_EDGE,
        linewidth=0.8,
        transform=ax.transAxes,
        clip_on=False,
    )

    ax.add_patch(
        panel
    )

    # -------------------------------------------------------------------------
    # Summary title
    # -------------------------------------------------------------------------

    ax.text(
        0.022,
        0.86,
        title,
        ha='left',
        va='center',
        fontsize=11.3,
        fontweight='bold',
        color=TEXT_DARK,
        transform=ax.transAxes,
    )

    if not entries:
        return

    # -------------------------------------------------------------------------
    # Four-column metric grid
    # -------------------------------------------------------------------------

    n_cols = min(
        4,
        len(entries),
    )

    n_rows = int(
        np.ceil(
            len(entries)
            / n_cols
        )
    )

    left = 0.025
    right = 0.985

    usable_width = (
        right
        - left
    )

    col_width = (
        usable_width
        / n_cols
    )

    if n_rows == 1:

        row_positions = [
            0.42
        ]

    else:

        row_positions = np.linspace(
            0.61,
            0.19,
            n_rows,
        )

    for i, (
        name,
        value,
    ) in enumerate(
        entries
    ):

        row = (
            i
            // n_cols
        )

        col = (
            i
            % n_cols
        )

        x = (
            left
            + col
            * col_width
        )

        y = row_positions[
            row
        ]

        wrapped_name = '\n'.join(
            textwrap.wrap(
                name,
                29,
            )
        )

        # Category.
        ax.text(
            x,
            y + 0.080,
            wrapped_name,
            ha='left',
            va='center',
            fontsize=9.0,
            color=TEXT_MID,
            transform=ax.transAxes,
            linespacing=1.05,
        )

        # Percentage.
        ax.text(
            x,
            y - 0.070,
            value,
            ha='left',
            va='center',
            fontsize=11.5,
            fontweight='bold',
            color=TEXT_DARK,
            transform=ax.transAxes,
        )


# =============================================================================
# Safe task wrapper
# =============================================================================

def _write_map(fig, ax, out_file, segments, dates, counts,
               pie_flags=(), pie_total=1) -> None:
    """<png>.map.json: every band of the bars as a rectangle in pixels of the
    PNG, with what it is -- for the viewer to show under the mouse."""
    import json as _json
    import matplotlib.image as _mpimg
    try:
        fig.canvas.draw()
        h_png, w_png = _mpimg.imread(out_file).shape[:2]
        w_in, h_in = fig.get_size_inches()
        if abs(w_png - w_in * DPI) <= 2 and abs(h_png - h_in * DPI) <= 2:
            x0_in, y1_in = 0.0, float(h_in)                  # the whole figure
        else:                                                 # a tight crop
            box = fig.get_tightbbox(fig.canvas.get_renderer()).padded(0.1)
            x0_in, y1_in = box.x0, box.y1
        to_in = fig.dpi_scale_trans.inverted()
        texts, index, rects = [], {}, []
        for flag, bottom, values in segments:
            bits = [b for b in range(24) if int(flag) >> b & 1]
            meaning = ", ".join(BIT_DESCRIPTIONS.get(b, f"bit {b}") for b in bits)
            for i, (lo, v) in enumerate(zip(bottom, values)):
                if v <= 0:
                    continue
                (xa, ya), (xb, yb) = to_in.transform(
                    ax.transData.transform([(i, lo), (i + 1, lo + v)]))
                d = str(dates[i])
                n = counts[dates[i]].get(flag, 0)
                text = (f"{d[:4]}-{d[4:6]}-{d[6:8]} {d[8:10]} UTC\n"
                        f"flag {flag}   bits {'+'.join(str(b) for b in bits)}\n"
                        f"{meaning}\n{n} obs, {v:.1f} % of the cycle")
                k = index.setdefault(text, len(texts))
                if k == len(texts):
                    texts.append(text)
                rects.append([round((xa - x0_in) * DPI, 1), round((y1_in - yb) * DPI, 1),
                              round((xb - x0_in) * DPI, 1), round((y1_in - ya) * DPI, 1), k])
        # the rows of the group lists: one rectangle each, with its text
        for ax_p, group, row_items, n_group in pie_flags:
            for flag, count, y, step, rest_flags in row_items:
                (xa, ya), (xb, yb) = to_in.transform(ax_p.transAxes.transform(
                    [(0.0, y - 0.5 * step), (1.0, y + 0.5 * step)]))
                if flag is None:
                    text = (f"{group_title(group)}\n{len(rest_flags)} other combinations: "
                            + ", ".join(str(f) for f in rest_flags[:12])
                            + ("..." if len(rest_flags) > 12 else "")
                            + f"\n{count} obs: {100.0 * count / n_group:.1f} % of the group")
                else:
                    bits = [b for b in range(24) if int(flag) >> b & 1]
                    meaning = ", ".join(BIT_DESCRIPTIONS.get(b, f"bit {b}")
                                        for b in bits) or "no bit set"
                    text = (f"{group_title(group)}\n"
                            f"flag {flag}   bits {'+'.join(str(b) for b in bits) or '-'}\n"
                            f"{meaning}\n{count} obs: "
                            f"{100.0 * count / n_group:.1f} % of the group, "
                            f"{100.0 * count / (pie_total or 1):.3g} % of the total")
                k = index.setdefault(text, len(texts))
                if k == len(texts):
                    texts.append(text)
                rects.append([round(float(xa - x0_in) * DPI, 1),
                              round(float(y1_in - yb) * DPI, 1),
                              round(float(xb - x0_in) * DPI, 1),
                              round(float(y1_in - ya) * DPI, 1), k])
        # the whole text first: a failure never leaves half a map behind
        payload = _json.dumps({"w": int(w_png), "h": int(h_png),
                               "rects": [[float(v) for v in r[:4]] + [r[4]] for r in rects],
                               "pies": [], "texts": texts}, separators=(",", ":"))
        with open(out_file + ".map.json", "w") as fh:
            fh.write(payload)
    except Exception as exc:                                  # never fatal
        print(f"[flags] no hover map for {os.path.basename(out_file)}: {exc}")


def flags_plot_task(
    task: Dict[str, Any],
) -> Optional[str]:

    try:

        return flags_plot(
            task
        )

    except Exception:

        print(
            f"[flags] plot failed for "
            f"{task.get('family')} "
            f"{task.get('id_stn')} "
            f"ch {task.get('vcoord')}:\n"
            f"{traceback.format_exc()}",
            flush=True,
        )

        plt.close(
            'all'
        )

        return None


# =============================================================================
# Viewer
# =============================================================================

def flags_viewer_items(
    tasks,
    results,
) -> List[Dict[str, str]]:

    items = []

    for task, path in zip(
        tasks,
        results,
    ):

        if not path:
            continue

        items.append(
            {
                'experience':
                    task['experience'],

                'family':
                    task['family'],

                'region':
                    task['region'],

                'land_ocean':
                    task.get('land_ocean', 'all'),

                'special':
                    task.get('special_label', 'all'),

                'id_stn':
                    task['id_stn'],

                'varno':
                    str(
                        task['varno']
                    ),

                'vcoord':
                    str(
                        task['vcoord']
                    ),

                'filename':
                    os.path.basename(
                        path
                    ),
            }
        )

    return items
