"""
obstimedb_plot.py — plotting layer for pikobs.obstimedb.

Per family, the report shows:

  0. PROFILE SUMMARY TABLE (top of report): per (family, id_stn), the
     number of profiles today / yesterday / this week / last week / at
     run time / averaged over the last 10 days at the same synoptic
     hour ("PASS") as the run, each compared to its reference period as
     a percent difference. See :func:`_draw_profile_summary_table` for
     the exact period and percentage-difference definitions (matches a
     reference PSMON-style report given directly by the user).

  0b. PASS VALIDATION (right under the volume composition chart): two
     charts answering a question none of the others answer directly --
     is the composition of THIS cycle normal? The first puts the
     current cycle's Nobs beside its mean at the same synoptic hour
     over the last `PASS_BASELINE_DAYS` days, family by family and
     station by station; the second expresses the same comparison as a
     percentage, sorted worst first, using the mosaic's colour tiers.
     See :func:`_draw_pass_vs_baseline` and
     :func:`_draw_pass_deviation`.

  1. MOSAIC (heatmap): rows = id_stn, columns = date/cycle (every 6h).
     Colour is driven ONLY by Nobs (never by Nobsprofile):
       - GREEN  : Nobs within the expected range.
       - YELLOW : Nobs dropped >= alert_yellow % vs the same-hour baseline.
       - ORANGE : Nobs dropped >= alert_orange %.
       - RED    : Nobs dropped >= alert_red % (this also covers a hard
                  zero — an outage is a -100% drop, always >= alert_red).
       - GREY   : not enough history yet (< 3 prior same-hour cycles).
       - WHITE  : this station had not yet reported at this point.

  2. GLOBAL time series (the whole set of stations, summed per cycle):
     one full-width plot for Nobs, one full-width plot for Nobsprofile —
     same width and same tick marks as the mosaic, so they all line up.

  3. PER-STATION time series: one full-width Nobs-only plot per id_stn
     (not a small-multiples grid) — same width/ticks as the mosaic too,
     so any two stations (or the mosaic) can be compared directly. Each
     station's own alert cycles are marked on its curve in the matching
     tier colour.

  4. PER-CHANNEL time series (RADIANCE families only — any family whose
     `channel` column isn't entirely NULL, i.e. VCOTYP=='CANAL' in
     pikobs.family()): a heatmap, rows = channel, columns = cycle,
     coloured by Nobs (sequential colour scale, NOT the alert tiers —
     this is a volume-shape view, not an alert view). Shown TWICE per
     family: first ALL STATIONS COMBINED (summed Nobs per channel,
     shown directly, not collapsed — the primary view), then ONE per
     individual station, each collapsed behind a native HTML <details>
     element (click to expand) since some instruments carry hundreds of
     channels and a report with all of them always open would be
     enormous.

A "families with issues" quick-navigation menu is shown near the top,
listing every family that has at least one yellow/orange/red cell
anywhere in the period, each linking straight to that family's card
further down the page (native #anchor links, no JS needed).

Baseline logic (core of the alert):
  For each (family, id_stn, hour) time series, sorted by calendar day,
  baseline(day) = mean(Nobs) over the preceding `window_days` calendar
  days at the SAME hour (current day excluded). Implemented with
  pandas shift(1).rolling(window_days, min_periods=3).mean().
"""

import os
import re
import sqlite3
import io
import base64

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.transforms as mtransforms
from matplotlib.colors import ListedColormap, BoundaryNorm
from rich.console import Console
from rich.table import Table
from rich import box

AGR_METRICS = ('omp', 'oma')

# Status codes: 0=no data, 1=grey(insufficient history), 2=green(normal),
# 3=yellow, 4=orange, 5=red, 6=dark green (notably ABOVE the baseline).
# Colour-coding is driven ONLY by Nobs.
STATUS_NODATA, STATUS_GREY, STATUS_GREEN = 0, 1, 2
STATUS_YELLOW, STATUS_ORANGE, STATUS_RED = 3, 4, 5
STATUS_DARKGREEN = 6
_STATUS_COLORS = ['#FFFFFF', '#BDBDBD', '#4CAF50', '#FFC107', '#FB8C00',
                  '#E53935', '#1B5E20']
_STATUS_CMAP = ListedColormap(_STATUS_COLORS)
_STATUS_BOUNDS = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]
_STATUS_NORM = BoundaryNorm(_STATUS_BOUNDS, _STATUS_CMAP.N)

_ALERT_STATUSES = (STATUS_YELLOW, STATUS_ORANGE, STATUS_RED)

REF_COLOR = '#2166AC'   # single-experience series colour (time series)

_SYNOPTIC_HOURS = (0, 6, 12, 18)

# Baseline window for the pass-validation charts, in calendar days. Same
# 10 days as the "Last 10 days (same PASS)" column of the profile summary
# table, deliberately: the two must never disagree with each other.
PASS_BASELINE_DAYS = 10

# Whether the current cycle counts toward its own baseline. Kept False
# (i.e. it DOES count) so these charts reproduce the DIFF_10DAY column of
# the summary table exactly -- that convention was verified against real
# reference reports. Flip to True if you'd rather grade the cycle against
# history alone, the way the mosaic's rolling baseline does (shift(1));
# the drops then come out slightly larger, since a collapsed cycle stops
# dragging its own reference down.
PASS_BASELINE_EXCLUDES_CURRENT = False


def _plot_by_hour(ax, dates_col, values_col, hour_col, **plot_kwargs):
    """Plot `values_col` vs `dates_col` as FOUR separate line segments,
    one per synoptic hour (00/06/12/18). Each segment only connects
    points that share the same hour across days — it never draws a
    line between (e.g.) a 00h value and the following 06h value.

    This matters here because the rolling baseline (and its threshold
    lines) is computed independently per synoptic hour: the 00h curve
    only depends on previous 00h cycles, the 06h curve only on previous
    06h cycles, etc. Plotting it as ONE continuous line across all
    hours would visually suggest a single trend that doesn't exist —
    each hour is its own independent reference curve.

    A legend label (if given in plot_kwargs) is applied only to the
    first hour's segment, so the legend shows one entry, not four."""
    label = plot_kwargs.pop('label', None)
    first = True
    for h in _SYNOPTIC_HOURS:
        mask = hour_col == h
        if not mask.any():
            continue
        kw = dict(plot_kwargs)
        if first and label:
            kw['label'] = label
        ax.plot(dates_col[mask], values_col[mask], **kw)
        first = False


def _shared_fig_width(n_date):
    """Figure width (inches) shared by every full-width plot in a
    family's report (mosaic, global time series, per-station plots), so
    they all line up when stacked in the HTML report."""
    return max(9, min(0.22 * n_date, 32))


def _draw_hierarchical_xaxis(ax, dates, hour_fontsize=7, day_fontsize=9,
                             month_fontsize=9, n_bottom_rows=2):
    """
    Draws a 3-level x-axis under `ax`, matching the reference PSMON
    monitoring style (Year-Month -> Day -> Hour):

      Row 1 (the axis' own ticks): hour label (00/06/12/18) for EVERY
        cycle in `dates` — dense, one per column.
      Row 2 (below the axis): the day-of-month number, centered under
        that day's block of cycles, with a thin vertical separator at
        each day boundary.
      Row 3 (further below): YYYYMM, centered under that month's block
        of days, with a slightly heavier vertical separator at each
        month boundary.

    `dates` gives the x-axis in CATEGORICAL/INTEGER positions
    (0..len(dates)-1) — every plot that uses this (mosaic, global and
    per-station time series) must plot against that same integer
    position, not against real datetime values, so everything lines up
    column-for-column across every image in the report.

    Row 2/3 sit at a FIXED INCH distance below the axes (via
    ScaledTranslation on top of the axes transform), not a fraction of
    the axes' own height -- an earlier version used an axes-fraction
    offset (e.g. -0.05*n_bottom_rows), which put the day/month rows a
    CONSTANT FRACTION of the plot's height below it. That looks fine
    for any one fixed plot height, but this same function backs mosaics
    of wildly different heights (3 rows vs 150+), so a fraction-based
    offset put these rows barely below a very short plot (leaving a
    huge, unexplained gap before whatever the caller draws next, e.g. a
    colorbar) and far too low for a very tall one (overlapping the next
    element instead). Fixed inches makes the gap look the same
    regardless of how tall the particular chart happens to be.
    """
    n = len(dates)
    x = np.arange(n)
    ax.set_xticks(x)
    ax.set_xticklabels([f'{d.hour:02d}' for d in dates],
                       fontsize=hour_fontsize, rotation=0)
    ax.tick_params(axis='x', pad=3, length=2)
    ax.set_xlim(-0.5, n - 0.5)

    fig = ax.get_figure()
    day_trans = mtransforms.blended_transform_factory(
        ax.transData,
        ax.transAxes + mtransforms.ScaledTranslation(0, -0.20, fig.dpi_scale_trans))
    month_trans = mtransforms.blended_transform_factory(
        ax.transData,
        ax.transAxes + mtransforms.ScaledTranslation(0, -0.42, fig.dpi_scale_trans))

    # Row 2: one label per day, centered under that day's cycles; thin
    # vertical separator at each day boundary.
    day_idx = {}
    for i, d in enumerate(dates):
        day_idx.setdefault(d.date(), []).append(i)
    for day, idxs in sorted(day_idx.items()):
        cx = (idxs[0] + idxs[-1]) / 2.0
        ax.text(cx, 0, f'{day.day:02d}', transform=day_trans,
                ha='center', va='top', fontsize=day_fontsize,
                fontweight='bold', color='#14328c', clip_on=False)
        ax.axvline(idxs[0] - 0.5, color='#444', lw=0.7, alpha=0.55, zorder=0)

    # Row 3: one label per calendar month, centered under that month's
    # days; heavier vertical separator at each month boundary.
    month_idx = {}
    for i, d in enumerate(dates):
        month_idx.setdefault((d.year, d.month), []).append(i)
    for (y, m), idxs in sorted(month_idx.items()):
        cx = (idxs[0] + idxs[-1]) / 2.0
        ax.text(cx, 0, f'{y}{m:02d}', transform=month_trans,
                ha='center', va='top', fontsize=month_fontsize,
                fontweight='bold', color='#14328c', clip_on=False)
        ax.axvline(idxs[0] - 0.5, color='#000000', lw=1.3, alpha=0.85, zorder=0)


def _safe_filename(s):
    return re.sub(r'[^A-Za-z0-9_.-]+', '_', str(s))


def _safe_anchor(s):
    """HTML id/anchor-safe version of a string (family name, etc)."""
    return re.sub(r'[^A-Za-z0-9_-]+', '-', str(s)).strip('-')


def _norm_agr(agr):
    if agr is None:
        return []
    if isinstance(agr, str):
        agr = [agr]
    out = []
    for a in agr:
        a = str(a).strip().lower()
        if a in AGR_METRICS and a not in out:
            out.append(a)
    return out


def _dedupe_moyenne_inplace(db_path):
    """Safety net applied every time a family's accumulator db is opened
    for reading here -- independent of obstimedb.py's own dedupe pass
    (which only runs when the FULL extract-then-plot pipeline is used).
    If this report is instead regenerated by calling obstimedb_plot
    directly against an already-extracted .db (skipping extraction,
    e.g. to iterate on the report faster), obstimedb.py's pass never
    runs -- so this file needs its OWN copy of the same fix, applied
    right here, so Today/Yesterday/This week/Last week (which sum
    across every cycle in a multi-day window, unlike Run time or Last
    10 days same PASS, which only ever touch a single hour) are never
    computed from duplicated rows regardless of how this report was
    invoked. For every (date, id_stn, channel) combination, keeps
    exactly one row (the smallest SQLite rowid) and drops the rest.
    Cheap even when there's nothing to clean, so it always runs, no
    "was this risky" check gating it."""
    conn = sqlite3.connect(db_path)
    try:
        tables = [r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='moyenne';")]
        if not tables:
            return
        before = conn.execute("SELECT COUNT(*) FROM moyenne").fetchone()[0]
        conn.execute("""
            DELETE FROM moyenne
            WHERE rowid NOT IN (
                SELECT MIN(rowid) FROM moyenne GROUP BY date, id_stn, channel
            );
        """)
        conn.commit()
        after = conn.execute("SELECT COUNT(*) FROM moyenne").fetchone()[0]
        if before != after:
            print(f"[WARNING] _dedupe_moyenne_inplace: removed {before - after} "
                  f"duplicate row(s) from {os.path.basename(db_path)} before "
                  f"reading it -- Today/This week/etc were inflated until now.",
                  flush=True)
    finally:
        conn.close()


def _fmt_departure(val):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return "n/a"
    a = abs(val)
    if a == 0:
        return "0"
    if a >= 100:
        return f"{val:,.1f}"
    elif a >= 1:
        return f"{val:.2f}"
    elif a >= 0.001:
        return f"{val:.3f}"
    else:
        return f"{val:.2e}"


# Explicit colour per family. Hashing a name into a small palette (what
# this module did before) guarantees collisions once there are more
# families than palette entries -- with 16 families over 10 colours,
# cris and atms_allsky came out the same pink in a real report, which
# defeats the point of colouring by family at all. A written-down table
# also means a family keeps its colour forever, across runs and across
# whatever subset of families a given run happens to request.
#
# Every entry is mid-to-dark on purpose: station shades are produced by
# lightening these, and a base that starts out pale has nowhere to go.
_FAMILY_COLORS = {
    'ai':               '#1F5FA9',   # blue
    'atms_allsky':      '#3FA0D8',   # azure
    'atms':             '#3FA0D8',
    'ro':               '#0E8577',   # teal
    'gpsro':            '#0E8577',
    'mwhs2':            '#35B5A0',   # turquoise
    'sf':               '#1E7B34',   # green
    'iasi':             '#6FA82B',   # olive
    'sc':               '#A07C10',   # ochre
    'csr':              '#8B5E3C',   # brown
    'sw':               '#E2761B',   # orange
    'to_amsub_allsky':  '#C0491C',   # burnt orange
    'to_amsub':         '#C0491C',
    'ua':               '#B01F2E',   # red
    'to_amsua_allsky':  '#E05A78',   # rose
    'to_amsua':         '#E05A78',
    'ch':               '#99196B',   # magenta
    'cris':             '#D45BAC',   # pink
    'crisfsr':          '#D45BAC',
    'gp':               '#5E35A8',   # purple
    'ssmis':            '#9B7BD4',   # lavender
}

# Only reached by a family not in the table above (a new instrument, a
# renamed stream). Deliberately a different region of colour space from
# most of the table so an unmapped family stands out as unmapped.
_FALLBACK_FAMILY_COLORS = ['#546E7A', '#795548', '#37474F', '#6D4C41',
                           '#455A64', '#4E342E']


def _family_color(family):
    """Stable colour for a family. Falls back to a hashed neutral for
    anything not in _FAMILY_COLORS -- add it to the table when a new
    family becomes permanent."""
    import hashlib
    key = str(family).strip().lower()
    if key in _FAMILY_COLORS:
        return _FAMILY_COLORS[key]
    h = int(hashlib.md5(key.encode()).hexdigest(), 16)
    return _FALLBACK_FAMILY_COLORS[h % len(_FALLBACK_FAMILY_COLORS)]


def _lighten(hex_color, frac):
    """Blend a hex colour `frac` of the way toward white (0 = unchanged,
    1 = white)."""
    hex_color = hex_color.lstrip('#')
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    r, g, b = (int(round(c + (255 - c) * frac)) for c in (r, g, b))
    return f'#{r:02X}{g:02X}{b:02X}'


def _station_color(family, stn):
    """A station is drawn as a lightened version of its family's colour,
    so a bar's family is readable from its hue and a station bar never
    competes with the family bar it belongs to.

    Which of the four tints a station gets is hashed from its own name,
    not from its position in the family's station list -- position would
    reshuffle every colour in a family the day a satellite is added or
    retired, and the whole point here is that a station keeps its
    appearance between runs. Two stations in the same family can land on
    the same tint; they are still labelled, and the tint is carrying
    'which family' rather than 'which station'."""
    import hashlib
    base = _family_color(family)
    tints = (0.15, 0.28, 0.41, 0.54)
    h = int(hashlib.md5(str(stn).encode()).hexdigest(), 16)
    return _lighten(base, tints[h % len(tints)])


def _split_stn_label(label):
    """'ai / BUFR' -> ('ai', 'BUFR'). Tolerates a station name that
    itself contains ' / '."""
    parts = str(label).split(' / ', 1)
    return (parts[0], parts[1]) if len(parts) == 2 else (parts[0], parts[0])


def _stn_label_color(label):
    """Colour for a combined 'family / id_stn' label."""
    fam, stn = _split_stn_label(label)
    return _station_color(fam, stn)


def _compute_status(df, window_days, alert_yellow, alert_orange, alert_red,
                    alert_high=10.0, min_history=None):
    """
    df: columns [family, id_stn, date(datetime64), hour(int), Nobs]
    Returns df with added columns: baseline, pct_change, status (int
    code). Computed independently per (family, id_stn, hour) group,
    sorted by date. Colour-coding is Nobs-only — Nobsprofile plays no
    part here.

    min_history: minimum number of PRIOR same-hour cycles required
    before a baseline is considered valid. Defaults to 1 -- a baseline
    is computed from WHATEVER prior same-hour history exists (even a
    single prior cycle), using pandas rolling's own min_periods to
    average over however many of the last `window_days` are actually
    available, rather than requiring a full window before grading
    anything. Confirmed this matters in practice: a rarely-reporting
    codtyp (e.g. ua/TEMP SHIP, ua/TEMP PILOT MOBIL) can go a very long
    time without accumulating a full `window_days` of PRIOR cycles,
    staying grey the whole time under the old "require the full
    window" default. Pass a larger min_history only if you deliberately
    want to require more history before grading (e.g. min_history=3 to
    avoid grading off a single, possibly-unusual prior cycle).

    alert_high: percent ABOVE the baseline (e.g. 10.0 -> Nobs >= 110% of
    baseline) that gets the DARK GREEN tier, distinguishing "clearly
    more than usual" from plain "normal".
    """
    if min_history is None:
        min_history = 1

    df = df.sort_values(['family', 'id_stn', 'hour', 'date']).copy()
    grp = df.groupby(['family', 'id_stn', 'hour'], sort=False)['Nobs']

    df['baseline'] = grp.transform(
        lambda s: s.shift(1).rolling(window_days, min_periods=min_history).mean())
    df['n_hist'] = grp.transform(
        lambda s: s.shift(1).rolling(window_days, min_periods=1).count())

    with np.errstate(invalid='ignore', divide='ignore'):
        df['pct_change'] = np.where(
            (df['baseline'].notna()) & (df['baseline'] > 0),
            (df['Nobs'] - df['baseline']) / df['baseline'] * 100.0,
            np.nan)

    status = np.full(len(df), STATUS_GREEN, dtype=int)
    pct = df['pct_change'].values
    has_pct = df['pct_change'].notna().values
    status[has_pct & (pct >= abs(alert_high))] = STATUS_DARKGREEN
    status[has_pct & (pct <= -abs(alert_yellow))] = STATUS_YELLOW
    status[has_pct & (pct <= -abs(alert_orange))] = STATUS_ORANGE
    status[has_pct & (pct <= -abs(alert_red))] = STATUS_RED

    status[df['n_hist'].values < min_history] = STATUS_GREY

    # Explicit rule: a hard zero with established history is ALWAYS a RED
    # alert, even once the rolling baseline itself has decayed to zero
    # after a long-standing outage (otherwise pct_change becomes 0-vs-0
    # -> NaN -> would silently look normal, hiding an ongoing data loss).
    zero_mask = (df['Nobs'].values == 0) & (df['n_hist'].values >= min_history)
    status[zero_mask] = STATUS_RED

    df['status'] = status
    return df


def _fill_gaps_since_first_seen(df_fam, datestart, dateend):
    """
    A station whose observations vanish from the RDB simply stops having
    rows in the source data — it does NOT appear as an explicit Nobs=0.
    Left as-is, that cycle is just ABSENT from df_fam.

    Fix: for every id_stn, once it has appeared at least once, fill any
    later missing cycle (up to `dateend`) with an explicit Nobs=0 (and
    Nprofile=0) row. This turns a silent gap into a real zero that flows
    through _compute_status (caught by its explicit zero-Nobs rule).
    Cycles BEFORE a station's first appearance are left absent (white —
    it simply wasn't being monitored/reporting yet, not a data loss).
    """
    full_dates = pd.date_range(
        pd.to_datetime(str(datestart), format='%Y%m%d%H'),
        pd.to_datetime(str(dateend), format='%Y%m%d%H'), freq='6h')

    out = []
    for stn, g in df_fam.groupby('id_stn', sort=False):
        g = g.sort_values('date')
        first_date = g['date'].min()
        expected = full_dates[full_dates >= first_date]

        g_idx = g.set_index('date')
        reind = g_idx.reindex(expected)
        reind['Nobs'] = reind['Nobs'].fillna(0.0)
        if 'Nprofile' in reind.columns:
            reind['Nprofile'] = reind['Nprofile'].fillna(0.0)
        reind['id_stn'] = stn
        reind['family'] = g['family'].iloc[0]
        reind['hour'] = reind.index.hour
        # avg_omp/avg_oma stay NaN on filled rows (nothing to average).
        reind = reind.reset_index().rename(columns={'index': 'date'})
        out.append(reind)
    return pd.concat(out, ignore_index=True) if out else df_fam


def _calc_pct_diff(current, reference):
    """Percent difference of `current` vs `reference`, per the
    convention given directly by the user for the profile summary
    table: missing data counts as zero, and if the REFERENCE period is
    zero the result is clamped to +100% (grew from nothing) or 0%
    (both periods empty) instead of NaN/inf -- it is NEVER computed as
    a literal division by zero. A zero CURRENT against a nonzero
    reference is NOT a special case: (0 - ref)/ref*100 already equals
    exactly -100% under the plain formula, so no separate branch is
    needed for that side."""
    current = 0.0 if (current is None or (isinstance(current, float) and np.isnan(current))) else float(current)
    reference = 0.0 if (reference is None or (isinstance(reference, float) and np.isnan(reference))) else float(reference)
    if reference == 0:
        return 0.0 if current == 0 else 100.0
    return (current - reference) / reference * 100.0


def _draw_profile_summary_table(df_all, run_time, name_in='experience'):
    """
    Builds the "Average Nobs profiles per 6 hours" summary table shown
    at the very top of the report, matching a reference PSMON-style
    report given directly by the user. Grouped by (family, id_stn) --
    NOTE: this uses the SAME id_stn field as the rest of the report,
    which for composite families (ai/sf/gp/csr/ua) already holds the
    codtyp label (e.g. "AMDAR") rather than a raw station id; there is
    no separate id_stn+codtyp two-level breakdown the way the original
    reference report has it, since that finer split isn't tracked
    separately in `moyenne` here.

    Periods, all relative to `run_time` (the latest cycle present).
    Every period below is an AVERAGE across however many passes/cycles
    actually fall in it (matching the table's own title, "Average Nobs
    Profiles per 6 Hours") -- NOT a total. Confirmed directly against a
    real reference report: a plain SUM over Today's 4 cycles came out
    ~4x the reference value; dividing by the number of cycles found
    matched it exactly.
      Today:      date > run_time - 24h  and date <= run_time
      Yesterday:  date > run_time - 72h  and date <= run_time - 48h
      This week:  date > run_time - 7d   and date <= run_time
      Last week:  date > run_time - 15d  and date <= run_time - 8d
      Last 10 days, same PASS: date > run_time - 10d and date <=
        run_time, restricted to the SAME synoptic hour as run_time
        (this window DOES include run_time itself, exactly as given).
    Note the 1-day GAP between Today/Yesterday and This week/Last
    week -- also confirmed against the reference report, not adjacent
    windows.

    Percent differences use :func:`_calc_pct_diff` (missing/zero
    reference -> +100%/0%, never NaN).

    The table is sortable (click a header to sort by that column,
    ascending/descending, numeric or alphabetic as appropriate -- via
    the generic `sortObsTable()` JS helper emitted once in the report)
    and each row is clickable: it jumps straight to that station's Nobs
    time series further down the page (an 'ALL' row jumps to the
    family's section instead, since there's no single-station plot to
    point an 'ALL' row at).

    Returns (legend_html, table_html, df_summary) -- df_summary has one
    row per (family, id_stn) PLUS one 'ALL' row per family, matching
    the reference report's per-family total row.
    """
    # NOTE: "Yesterday" and "Last week" are NOT immediately adjacent to
    # "Today"/"This week" -- confirmed against TWO independent reference
    # tables given directly by the user (run_time 2026082600/00Z and
    # 2026083112/12Z), both consistently showing a 1-DAY GAP: Yesterday
    # ends a full 24h before Today starts, and Last week ends a full
    # day before This week starts. This was a real bug in an earlier
    # version of this function (computed both as immediately adjacent,
    # no gap) -- fixed here to match the confirmed convention exactly.
    today_start = run_time - pd.Timedelta(hours=24)
    yesterday_end = run_time - pd.Timedelta(hours=48)
    yesterday_start = run_time - pd.Timedelta(hours=72)
    week_start = run_time - pd.Timedelta(days=7)
    lastweek_end = run_time - pd.Timedelta(days=8)
    lastweek_start = run_time - pd.Timedelta(days=15)
    tenday_start = run_time - pd.Timedelta(days=10)
    run_hour = run_time.hour

    def _fmtd(d):
        return d.strftime('%Y%m%d%H')

    # ---- Explicit legend block, matching the reference report's own
    # layout, with the ACTUAL computed dates for this run (not just the
    # abstract formulas) -- so it's immediately clear which real dates
    # "Today"/"Yesterday"/etc. resolve to for THIS report. ----
    legend_html = f"""
    <div class="explain" style="background:#eef4ff;border-color:#cdd9f0;">
        <b>File Type:</b> {name_in} &nbsp;&middot;&nbsp;
        <b>Run time:</b> {_fmtd(run_time)} &nbsp;&middot;&nbsp;
        <b>PASS:</b> {run_hour:02d}Z<br><br>
        <b>Definitions of periods</b> (computed for this run):<br>
        Today: date &gt; {_fmtd(today_start)} and date &le; {_fmtd(run_time)}<br>
        Yesterday: date &gt; {_fmtd(yesterday_start)} and date &le; {_fmtd(yesterday_end)}<br>
        This week: date &gt; {_fmtd(week_start)} and date &le; {_fmtd(run_time)}<br>
        Last week: date &gt; {_fmtd(lastweek_start)} and date &le; {_fmtd(lastweek_end)}<br>
        Last 10 days (same PASS {run_hour:02d}Z): date &gt; {_fmtd(tenday_start)}
        and date &le; {_fmtd(run_time)}<br><br>
        Every period above is an <b>average per 6-hour pass</b>, not a
        total -- e.g. "Today" is the mean profiles-per-cycle across
        today's passes, not their sum. Being averages, they are not
        whole numbers: values under 10 are shown with decimals, so that
        a rarely-reporting codtyp averaging 0.25 profiles/pass stays
        visibly different from one that reported nothing at all, and so
        the percentage beside it can be reconciled with the two columns
        it came from.<br><br>
        <b>Percentage difference calculations:</b><br>
        DIFFERENCE 1 DAY: (avg profiles/pass today &minus; avg profiles/pass yesterday) / avg profiles/pass yesterday &times; 100%<br>
        DIFFERENCE 1 WEEK: (avg profiles/pass this week &minus; avg profiles/pass last week) / avg profiles/pass last week &times; 100%<br>
        DIFFERENCE 10 DAYS SAME PASS: (profiles at run time &minus; average profiles last 10 days
        same PASS) / average profiles last 10 days same PASS &times; 100%<br><br>
        Missing data is treated as zero; a period with no observations to compare
        against shows as &plusmn;100% rather than an undefined value.<br><br>
        <i>Click a column header to sort. Click a row to jump to that station's
        Nobs time series below (an "ALL" row jumps to the family's section).</i>
    </div>
    """

    def _period_mean(df, start, end, same_hour=False):
        # "Average Nobs Profiles per 6 Hours" -- the table's OWN title
        # says average, not total. Confirmed directly: the reference
        # report's Today value for ai/BUFR was 83,670; a plain SUM
        # across that day's 4 cycles gave ~334,679 -- almost exactly
        # 4x too high. 334,679 / 4 = 83,670 (matches). Averaging across
        # the DISTINCT dates found in the window (not dividing by a
        # hardcoded "4" or "28") is also naturally correct if a cycle
        # is genuinely missing from this period -- the average is over
        # however many passes actually exist, not an assumed count.
        mask = (df['date'] > start) & (df['date'] <= end)
        if same_hour:
            mask &= (df['hour'] == run_hour)
        vals = df.loc[mask, 'Nprofile']
        return vals.mean() if len(vals) else np.nan

    rows = []

    def _build_row(family, id_stn, g):
        today = _period_mean(g, today_start, run_time)
        yesterday = _period_mean(g, yesterday_start, yesterday_end)
        this_week = _period_mean(g, week_start, run_time)
        last_week = _period_mean(g, lastweek_start, lastweek_end)
        at_run = g.loc[g['date'] == run_time, 'Nprofile'].sum()
        tenday_avg = _period_mean(g, tenday_start, run_time, same_hour=True)
        return {
            'FAMILY': family, 'ID_STN': id_stn,
            'NB_TODAY': today, 'NB_YESTERDAY': yesterday,
            'DIFF_1DAY': _calc_pct_diff(today, yesterday),
            'NB_THISWEEK': this_week, 'NB_LASTWEEK': last_week,
            'DIFF_1WEEK': _calc_pct_diff(this_week, last_week),
            'NB_RUNTIME': at_run, 'NB_10DAY_SAMEPASS': tenday_avg,
            'DIFF_10DAY': _calc_pct_diff(at_run, tenday_avg),
        }

    def _sum_row(family, id_stn, individual_rows):
        """Build an "ALL" row by SUMMING the already-computed per-pass
        averages of the given individual rows -- NOT by re-averaging
        the raw per-cycle data pooled together. Each individual row is
        itself an average-per-pass for ONE id_stn/codtyp; those
        averages have wildly different scale from one another (e.g.
        BUFR ~83k/pass vs AIREP ~98/pass), so averaging their raw rows
        together would blend them into a number that means nothing --
        summing the already-correct per-id_stn averages is what
        "total average profiles per pass, across every station" means.
        The percentage columns are recomputed from the summed values,
        not summed themselves (a % of a % isn't meaningful)."""
        def s(key):
            vals = [r[key] for r in individual_rows if pd.notna(r[key])]
            return sum(vals) if vals else np.nan
        today, yesterday = s('NB_TODAY'), s('NB_YESTERDAY')
        this_week, last_week = s('NB_THISWEEK'), s('NB_LASTWEEK')
        at_run, tenday_avg = s('NB_RUNTIME'), s('NB_10DAY_SAMEPASS')
        return {
            'FAMILY': family, 'ID_STN': id_stn,
            'NB_TODAY': today, 'NB_YESTERDAY': yesterday,
            'DIFF_1DAY': _calc_pct_diff(today, yesterday),
            'NB_THISWEEK': this_week, 'NB_LASTWEEK': last_week,
            'DIFF_1WEEK': _calc_pct_diff(this_week, last_week),
            'NB_RUNTIME': at_run, 'NB_10DAY_SAMEPASS': tenday_avg,
            'DIFF_10DAY': _calc_pct_diff(at_run, tenday_avg),
        }

    # Build every individual (family, id_stn) row FIRST, then derive the
    # "ALL" rows from THOSE results via summing -- never straight from
    # the raw per-cycle data (see _sum_row's docstring for why).
    all_individual_rows = []
    family_rows_map = {}
    for family, g_fam in df_all.groupby('family', sort=False):
        family_individual = []
        for id_stn, g_stn in g_fam.groupby('id_stn', sort=False):
            row = _build_row(family, id_stn, g_stn)
            family_individual.append(row)
            all_individual_rows.append(row)
        family_rows_map[family] = family_individual

    # ONLY the grand-total row (FAMILY='ALL', ID_STN='ALL') is pulled to
    # the very top and stays pinned there (via the JS sort function
    # below) regardless of sorting -- it's the one running total meant
    # to always be visible at a glance. Per-family "ALL" rows (e.g.
    # ai/ALL) stay WITH their own family's individual rows below, and
    # sort normally along with them, same as the reference report.
    rows = [_sum_row('ALL', 'ALL', all_individual_rows)]
    for family, g_fam in df_all.groupby('family', sort=False):
        rows.extend(family_rows_map[family])
        rows.append(_sum_row(family, 'ALL', family_rows_map[family]))

    df_summary = pd.DataFrame(rows)

    def _fmt_diff(v):
        return f"{v:+.1f}%"

    def _fmt_int(v):
        """Format one of the count columns.

        These are AVERAGES per 6h pass, not integer counts, so rounding
        them all to whole numbers makes the low-volume rows unreadable:
        a codtyp averaging 0.25 profiles/pass against a period averaging
        0.0 prints as "0  0  +100.0%", and one averaging 2.5 against 3.0
        prints as "2  3  -16.7%" when 2 vs 3 would obviously be -33.3%.
        The percentages were right in both cases -- they come from the
        unrounded values -- but the two columns beside them said
        otherwise, which is worse than either being wrong on its own.

        So: anything at or above 10 still prints as a plain rounded
        integer with thousands separators (BUFR does not need decimals),
        and anything below it keeps enough decimals to stay distinct
        from a true zero. A literal 0 still prints as "0"."""
        if pd.isna(v):
            return "n/a"
        a = abs(v)
        if a == 0:
            return "0"
        if a >= 10:
            return f"{int(round(v)):,}"
        if a >= 1:
            return f"{v:.1f}"
        if a >= 0.01:
            return f"{v:.2f}"
        return f"{v:.3f}"

    def _diff_color(v):
        if v > 0:
            return 'color:#1B5E20;font-weight:bold;'
        elif v < 0:
            return 'color:#E53935;font-weight:bold;'
        return ''

    # data-sort on each <th> flags the column type for the JS sorter
    # ('text' or 'num'); data-sort on each <td> gives the RAW value to
    # sort by (so a formatted "+58.8%"/"n/a" cell still sorts correctly
    # as a number, and "1,234" sorts as 1234 not lexically).
    # Inline style baked directly into every cell (not just the page's
    # CSS) -- a plain copy-paste into Teams/Outlook/etc typically keeps
    # each element's own computed/inline style but drops the external
    # stylesheet, so putting it on the cells themselves is what actually
    # survives the paste and keeps the table small there too.
    _CS = "font-size:11px;padding:2px 6px;"
    header = ("<tr>"
             f"<th style='{_CS}' data-sort='text' onclick='sortObsTable(this)'>Family</th>"
             f"<th style='{_CS}' data-sort='text' onclick='sortObsTable(this)'>Id_stn</th>"
             f"<th style='{_CS}' data-sort='num' onclick='sortObsTable(this)'>Today</th>"
             f"<th style='{_CS}' data-sort='num' onclick='sortObsTable(this)'>Yesterday</th>"
             f"<th style='{_CS}' data-sort='num' onclick='sortObsTable(this)'>Diff 1 day</th>"
             f"<th style='{_CS}' data-sort='num' onclick='sortObsTable(this)'>This week</th>"
             f"<th style='{_CS}' data-sort='num' onclick='sortObsTable(this)'>Last week</th>"
             f"<th style='{_CS}' data-sort='num' onclick='sortObsTable(this)'>Diff 1 week</th>"
             f"<th style='{_CS}' data-sort='num' onclick='sortObsTable(this)'>Run time</th>"
             f"<th style='{_CS}' data-sort='num' onclick='sortObsTable(this)'>Last 10d (same PASS)</th>"
             f"<th style='{_CS}' data-sort='num' onclick='sortObsTable(this)'>Diff 10d same PASS</th>"
             "</tr>")
    body_rows = []
    for _, r in df_summary.iterrows():
        is_grand_total = (r['FAMILY'] == 'ALL' and r['ID_STN'] == 'ALL')
        if is_grand_total:
            row_style = "background:#dbe4f7;font-weight:bold;border-top:2px solid #4C72B0;"
        elif r['ID_STN'] == 'ALL':
            row_style = "background:#f5f7ff;font-weight:bold;"
        else:
            row_style = ""
        if is_grand_total:
            # No single section corresponds to "every family combined" --
            # nothing meaningful to jump to, so this row isn't clickable.
            onclick_attr = ""
        elif r['ID_STN'] == 'ALL':
            target = f"#family-{_safe_anchor(r['FAMILY'])}"
            row_style += "cursor:pointer;"
            onclick_attr = f" onclick=\"location.href='{target}'\""
        else:
            target = f"#station-{_safe_anchor(r['FAMILY'])}-{_safe_anchor(r['ID_STN'])}"
            row_style += "cursor:pointer;"
            onclick_attr = f" onclick=\"location.href='{target}'\""
        body_rows.append(
            f"<tr style='{row_style}'{onclick_attr}>"
            f"<td style='{_CS}' data-v='{r['FAMILY']}'>{r['FAMILY']}</td>"
            f"<td style='{_CS}' data-v='{r['ID_STN']}'>{r['ID_STN']}</td>"
            f"<td style='{_CS}' data-v='{r['NB_TODAY']}'>{_fmt_int(r['NB_TODAY'])}</td>"
            f"<td style='{_CS}' data-v='{r['NB_YESTERDAY']}'>{_fmt_int(r['NB_YESTERDAY'])}</td>"
            f"<td style='{_CS}{_diff_color(r['DIFF_1DAY'])}' data-v='{r['DIFF_1DAY']}'>{_fmt_diff(r['DIFF_1DAY'])}</td>"
            f"<td style='{_CS}' data-v='{r['NB_THISWEEK']}'>{_fmt_int(r['NB_THISWEEK'])}</td>"
            f"<td style='{_CS}' data-v='{r['NB_LASTWEEK']}'>{_fmt_int(r['NB_LASTWEEK'])}</td>"
            f"<td style='{_CS}{_diff_color(r['DIFF_1WEEK'])}' data-v='{r['DIFF_1WEEK']}'>{_fmt_diff(r['DIFF_1WEEK'])}</td>"
            f"<td style='{_CS}' data-v='{r['NB_RUNTIME']}'>{_fmt_int(r['NB_RUNTIME'])}</td>"
            f"<td style='{_CS}' data-v='{r['NB_10DAY_SAMEPASS']}'>{_fmt_int(r['NB_10DAY_SAMEPASS'])}</td>"
            f"<td style='{_CS}{_diff_color(r['DIFF_10DAY'])}' data-v='{r['DIFF_10DAY']}'>{_fmt_diff(r['DIFF_10DAY'])}</td>"
            f"</tr>")

    table_html = f"<table id='profileSummaryTable'>{header}{''.join(body_rows)}</table>"
    return legend_html, table_html, df_summary


def _row_click_boxes(fig, ax, labels, save_dpi=70):
    """Pixel rectangles, one per bar row, for an HTML image map.

    Must be called AFTER the figure's final layout (tight_layout /
    subplots_adjust) and BEFORE plt.close, since it reads the axes'
    actual position on the canvas.

    Two conversions are easy to get wrong here. Matplotlib's display
    coordinates have their origin at the BOTTOM-left and are expressed
    at the figure's own dpi, while an image map counts from the TOP-left
    of the saved file at whatever dpi savefig used -- so the y axis is
    flipped and both axes are rescaled by save_dpi/fig.dpi.

    Each box spans from the very left edge of the figure (not the left
    edge of the axes) so that clicking the row's LABEL works too, which
    is what anyone actually aims at.
    """
    scale = save_dpi / fig.dpi
    fig_h_px = fig.get_figheight() * save_dpi
    x_right = ax.transAxes.transform((1, 0))[0] * scale

    boxes = []
    for i, lbl in enumerate(labels):
        y_a = fig_h_px - ax.transData.transform((0, i - 0.5))[1] * scale
        y_b = fig_h_px - ax.transData.transform((0, i + 0.5))[1] * scale
        y0, y1 = sorted((y_a, y_b))
        boxes.append((str(lbl), 0, int(round(y0)), int(round(x_right)),
                      int(round(y1))))
    return boxes


def _row_href(label):
    """Where a bar row jumps to. 'ai / BUFR' goes to that station's own
    time series; a bare family name goes to the family's card. Both
    anchors are emitted further down the report by obstimedb_plot."""
    parts = str(label).split(' / ', 1)
    if len(parts) == 2:
        return f'#station-{_safe_anchor(parts[0])}-{_safe_anchor(parts[1])}'
    return f'#family-{_safe_anchor(label)}'


def _click_map_html(map_name, boxes):
    """An <map> of <area> rectangles. Plain HTML, no JS -- the browser
    handles the hit-testing, and the areas stay correct because these
    images are rendered at their natural size inside .scrollwrap
    (max-width:none), so one image pixel is one screen pixel."""
    if not boxes:
        return ""

    def _esc(s):
        return (str(s).replace('&', '&amp;').replace('"', '&quot;')
                .replace('<', '&lt;').replace('>', '&gt;'))

    areas = []
    for lbl, x0, y0, x1, y1 in boxes:
        safe = _esc(lbl)
        areas.append(
            f'<area shape="rect" coords="{x0},{y0},{x1},{y1}" '
            f'href="{_row_href(lbl)}" alt="{safe}" title="Go to {safe}">')
    return f'<map name="{map_name}">{"".join(areas)}</map>'


def _draw_nobs_composition(df_status, region, flag_criteria, datestart, dateend, out_path):
    """
    Summary chart shown at the very top of the report, BEFORE the
    mosaic: total Nobs (summed over the whole period) for each family,
    and for each individual id_stn, each bar labelled with its count,
    the % of the grand total it represents, AND the average Nobs per
    single 6h cycle/file — a quick "who has how much data, and how much
    per file" overview before diving into the alert-status detail below.

    The totals cover the FULL requested period (`datestart` to
    `dateend`), not just the most recent cycle -- stated explicitly in
    the title so it's never mistaken for a single-cycle or "all-time"
    figure. For the complementary "is the CURRENT cycle normal" view,
    see _draw_pass_vs_baseline / _draw_pass_deviation, drawn right
    after this one in the same card.
    """
    fam_totals = (df_status.groupby('family')['Nobs'].sum()
                 .sort_values(ascending=False))
    grand_total = fam_totals.sum()

    # Average per 6h cycle for a FAMILY = the family's total Nobs for
    # that cycle (summed across all its stations), averaged over cycles.
    fam_by_cycle = df_status.groupby(['family', 'date'])['Nobs'].sum()
    fam_avg = fam_by_cycle.groupby('family').mean().reindex(fam_totals.index)

    df_status = df_status.copy()
    df_status['stn_label'] = (df_status['family'].astype(str) + ' / '
                              + df_status['id_stn'].astype(str))
    stn_totals = (df_status.groupby('stn_label')['Nobs'].sum()
                 .sort_values(ascending=False))
    # Average per 6h cycle for a STATION = its own mean Nobs per cycle.
    stn_avg = df_status.groupby('stn_label')['Nobs'].mean().reindex(stn_totals.index)

    n_fam = len(fam_totals)
    n_stn = len(stn_totals)
    fig_h = max(4, 0.32 * n_fam) + max(4, 0.28 * n_stn) + 2.0
    fig, (ax_fam, ax_stn) = plt.subplots(
        2, 1, figsize=(14, fig_h),
        gridspec_kw={'height_ratios': [max(2, 0.32 * n_fam),
                                       max(3, 0.28 * n_stn)]})

    def _bar_panel(ax, totals, avgs, title, colors=None):
        labels = totals.index.tolist()
        values = totals.values
        y = np.arange(len(labels))
        bar_colors = colors if colors is not None else REF_COLOR
        ax.barh(y, values, color=bar_colors, edgecolor='#333', linewidth=0.4)
        ax.set_yticks(y)
        ax.set_yticklabels(labels, fontsize=9)
        ax.invert_yaxis()  # largest at top
        xmax = values.max() if len(values) else 1
        for yi, v, lbl in zip(y, values, labels):
            pct = (v / grand_total * 100.0) if grand_total > 0 else 0.0
            avg = avgs.loc[lbl]
            ax.text(v + xmax * 0.01, yi,
                    f'{int(v):,}  ({pct:.1f}%)   |   avg/6h file: {avg:,.0f}',
                    va='center', ha='left', fontsize=8.5, color='#222')
        ax.set_xlim(0, xmax * 1.34)
        ax.set_xlabel('Total Nobs (whole period)', fontsize=11, fontweight='bold')
        ax.set_title(title, fontsize=13, fontweight='bold', loc='left')
        ax.grid(True, axis='x', linestyle=':', alpha=0.5)
        ax.tick_params(labelsize=9)

    fam_colors = [_family_color(f) for f in fam_totals.index]
    _bar_panel(ax_fam, fam_totals, fam_avg, 'Total Nobs by family', colors=fam_colors)

    stn_colors = [_stn_label_color(lbl) for lbl in stn_totals.index]
    _bar_panel(ax_stn, stn_totals, stn_avg, 'Total Nobs by station (family / id_stn)',
              colors=stn_colors)

    fig.suptitle(f'Observation Volume Composition — {region} — {flag_criteria}\n'
                f'Period: {datestart} \u2192 {dateend}   (grand total: {int(grand_total):,})',
                fontsize=15, fontweight='bold')
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    boxes = (_row_click_boxes(fig, ax_fam, fam_totals.index)
             + _row_click_boxes(fig, ax_stn, stn_totals.index))
    fig.savefig(out_path, dpi=70)
    plt.close(fig)
    return out_path, boxes


def _pass_composition_frames(df_all, run_time,
                             exclude_current=PASS_BASELINE_EXCLUDES_CURRENT):
    """
    Shared data prep for both pass-validation charts.

    Returns a dict with four pandas Series -- fam_cur, fam_base, stn_cur,
    stn_base -- plus n_cycles (how many cycles the baseline averaged
    over), run_hour and window_start, or None if there's nothing to
    compare.

    Two details worth knowing:

    * A FAMILY's baseline is the mean of its per-cycle TOTALS, not the
      mean of its individual station rows. Those are different numbers
      as soon as a family has more than one station (the row-wise mean
      gives a per-station average, which is not what the current-pass
      bar next to it represents), so the per-cycle sum has to happen
      first.

    * The index is the UNION of stations seen in the current cycle and
      in the baseline window, not just the current cycle's. A station
      that reported for ten days and then vanished entirely has no row
      at run_time at all -- indexing off the current cycle would
      silently drop it from both charts, which is precisely the failure
      these charts exist to catch. Missing on either side becomes 0.
      (df_all has already been through _fill_gaps_since_first_seen by
      the time it gets here, so most vanished stations arrive as an
      explicit Nobs=0 anyway; the union is the belt-and-braces case for
      anything that slips past it.)
    """
    run_hour = int(run_time.hour)
    window_start = run_time - pd.Timedelta(days=PASS_BASELINE_DAYS)

    cur = df_all[df_all['date'] == run_time]
    base_mask = ((df_all['date'] > window_start)
                 & (df_all['date'] <= run_time)
                 & (df_all['hour'] == run_hour))
    if exclude_current:
        base_mask &= (df_all['date'] != run_time)
    base = df_all[base_mask]

    if cur.empty and base.empty:
        return None

    def _labelled(df):
        df = df.copy()
        df['stn_label'] = (df['family'].astype(str) + ' / '
                           + df['id_stn'].astype(str))
        return df

    cur, base = _labelled(cur), _labelled(base)

    def _current_totals(df, key):
        if df.empty:
            return pd.Series(dtype=float)
        return df.groupby(key)['Nobs'].sum()

    def _baseline_means(df, key):
        if df.empty:
            return pd.Series(dtype=float)
        per_cycle = df.groupby([key, 'date'])['Nobs'].sum()
        return per_cycle.groupby(level=0).mean()

    def _prior_cycle_counts(df, key):
        """How many cycles OTHER than the current one back this group's
        baseline. Zero means the bar has nothing to be compared against:
        with the inclusive convention the group's baseline is then just
        the current cycle repeated back at itself, which comes out as a
        flawless 0% and reads as 'normal' when the truth is 'first time
        we have ever seen this one at this pass'. Both charts use this
        to say 'no baseline' instead."""
        if df.empty:
            return pd.Series(dtype=float)
        prior = df[df['date'] != run_time]
        if prior.empty:
            return pd.Series(0, index=df[key].unique(), dtype=float)
        return prior.groupby(key)['date'].nunique().astype(float)

    out = {}
    for name, key in (('fam', 'family'), ('stn', 'stn_label')):
        c = _current_totals(cur, key)
        b = _baseline_means(base, key)
        idx = c.index.union(b.index)
        out[f'{name}_cur'] = c.reindex(idx).fillna(0.0)
        out[f'{name}_base'] = b.reindex(idx)
        out[f'{name}_nhist'] = _prior_cycle_counts(base, key).reindex(idx).fillna(0.0)

    out['n_cycles'] = int(base['date'].nunique()) if not base.empty else 0
    out['run_hour'] = run_hour
    out['window_start'] = window_start
    return out


def _draw_pass_vs_baseline(df_all, run_time, region, flag_criteria, out_path):
    """
    Chart 1 of the pass-validation pair: for every family and every
    station, the current cycle's Nobs next to its mean for the same
    synoptic hour over the last PASS_BASELINE_DAYS days.

    Paired bars rather than one bar of the difference, because the two
    readings answer different questions and both matter: a station can
    be 30% down and still be the largest contributor in the family, or
    be perfectly on-baseline at a volume so small it can't explain
    anything. Ordered by current volume, largest first, matching the
    composition chart above it so the same row sits in roughly the same
    place.

    Returns out_path, or None when there's nothing to draw.
    """
    frames = _pass_composition_frames(df_all, run_time)
    if frames is None:
        return None, []

    def _ordered(cur, base, nhist):
        order = cur.sort_values(ascending=False).index
        return cur.reindex(order), base.reindex(order), nhist.reindex(order)

    fam_cur, fam_base, fam_nhist = _ordered(
        frames['fam_cur'], frames['fam_base'], frames['fam_nhist'])
    stn_cur, stn_base, stn_nhist = _ordered(
        frames['stn_cur'], frames['stn_base'], frames['stn_nhist'])
    if fam_cur.empty and stn_cur.empty:
        return None, []

    n_fam, n_stn = len(fam_cur), len(stn_cur)
    fam_h = max(2.5, 0.42 * n_fam)
    stn_h = max(3.5, 0.38 * n_stn)
    fig, (ax_fam, ax_stn) = plt.subplots(
        2, 1, figsize=(14, fam_h + stn_h + 2.2),
        gridspec_kw={'height_ratios': [fam_h, stn_h]})

    def _panel(ax, cur, base, nhist, title, colors):
        labels = list(cur.index)
        y = np.arange(len(labels))
        h = 0.38
        # A group with no prior cycle has no baseline to draw, whatever
        # the inclusive window computed for it -- blank it out rather
        # than draw a hatched twin identical to the solid bar.
        no_hist = (nhist.fillna(0).values <= 0) | base.isna().values
        base_draw = np.where(no_hist, 0.0, base.fillna(0).values)
        vals = np.concatenate([cur.values, base_draw])
        xmax = vals.max() if len(vals) and vals.max() > 0 else 1.0

        ax.barh(y - h / 2, cur.values, h, color=colors, edgecolor='#333',
                linewidth=0.4, label='This pass')
        ax.barh(y + h / 2, base_draw, h, color=colors, alpha=0.38,
                edgecolor='#333', linewidth=0.4, hatch='///',
                label=f'{PASS_BASELINE_DAYS}-day mean, same pass')

        for yi, c, b, nb in zip(y, cur.values, base_draw, no_hist):
            ax.text(c + xmax * 0.008, yi - h / 2, f'{int(round(c)):,}',
                    va='center', ha='left', fontsize=8, color='#222')
            btxt = 'no baseline yet' if nb else f'{int(round(b)):,}'
            ax.text((0 if nb else b) + xmax * 0.008, yi + h / 2, btxt,
                    va='center', ha='left', fontsize=8, color='#666')

        ax.set_yticks(y)
        ax.set_yticklabels(labels, fontsize=9)
        ax.invert_yaxis()
        ax.set_xlim(0, xmax * 1.22)
        ax.set_xlabel('Nobs per 6h pass', fontsize=11, fontweight='bold')
        ax.set_title(title, fontsize=13, fontweight='bold', loc='left')
        ax.grid(True, axis='x', linestyle=':', alpha=0.5)
        ax.legend(fontsize=9, loc='lower right', framealpha=0.95)
        ax.tick_params(labelsize=9)

    _panel(ax_fam, fam_cur, fam_base, fam_nhist, 'By family',
           [_family_color(f) for f in fam_cur.index])
    _panel(ax_stn, stn_cur, stn_base, stn_nhist, 'By station (family / id_stn)',
           [_stn_label_color(l) for l in stn_cur.index])

    fig.suptitle(
        f'Pass composition vs baseline \u2014 {region} \u2014 {flag_criteria}\n'
        f'This pass: {run_time:%Y%m%d} {frames["run_hour"]:02d}Z   |   '
        f'baseline: mean of {frames["n_cycles"]} cycle(s) at '
        f'{frames["run_hour"]:02d}Z since {frames["window_start"]:%Y%m%d}',
        fontsize=15, fontweight='bold')
    fig.tight_layout(rect=[0, 0, 1, 0.955])
    boxes = (_row_click_boxes(fig, ax_fam, fam_cur.index)
             + _row_click_boxes(fig, ax_stn, stn_cur.index))
    fig.savefig(out_path, dpi=70)
    plt.close(fig)
    return out_path, boxes


def _draw_pass_deviation(df_all, run_time, region, flag_criteria,
                         alert_yellow, alert_orange, alert_red, alert_high,
                         out_path):
    """
    Chart 2 of the pair: the same comparison expressed as a percent
    change, sorted worst first so whatever is wrong with this pass sits
    at the top of the panel rather than somewhere in the middle of it.

    Bars are coloured with the mosaic's own tiers, so a red bar here and
    a red cell in that station's rightmost mosaic column mean the same
    thing. Percentages come from _calc_pct_diff, the same helper the
    summary table uses -- an empty baseline gives +100%/0% rather than
    an infinity, and the bar is drawn grey in that case, since "no
    history to compare against" is not the same finding as "normal".
    """
    frames = _pass_composition_frames(df_all, run_time)
    if frames is None:
        return None, []

    def _pct(cur, base):
        vals = [_calc_pct_diff(c, b) for c, b in zip(cur.values, base.values)]
        s = pd.Series(vals, index=cur.index, dtype=float)
        return s.sort_values(ascending=True)

    fam_pct = _pct(frames['fam_cur'], frames['fam_base'])
    stn_pct = _pct(frames['stn_cur'], frames['stn_base'])
    if fam_pct.empty and stn_pct.empty:
        return None, []

    # "No baseline" covers two distinct situations, both of which must
    # not be read as a verdict: an empty/zero reference, and a group
    # whose only contributing cycle IS the current one (which the
    # inclusive convention would otherwise score as a flawless 0%).
    fam_no_base = (frames['fam_base'].isna() | (frames['fam_base'] == 0)
                   | (frames['fam_nhist'] <= 0))
    stn_no_base = (frames['stn_base'].isna() | (frames['stn_base'] == 0)
                   | (frames['stn_nhist'] <= 0))

    def _color(pct, unknown):
        if unknown:
            return _STATUS_COLORS[STATUS_GREY]
        if pct >= abs(alert_high):
            return _STATUS_COLORS[STATUS_DARKGREEN]
        if pct > -abs(alert_yellow):
            return _STATUS_COLORS[STATUS_GREEN]
        if pct > -abs(alert_orange):
            return _STATUS_COLORS[STATUS_YELLOW]
        if pct > -abs(alert_red):
            return _STATUS_COLORS[STATUS_ORANGE]
        return _STATUS_COLORS[STATUS_RED]

    n_fam, n_stn = len(fam_pct), len(stn_pct)
    fam_h = max(2.5, 0.34 * n_fam)
    stn_h = max(3.5, 0.30 * n_stn)
    fig, (ax_fam, ax_stn) = plt.subplots(
        2, 1, figsize=(14, fam_h + stn_h + 2.4),
        gridspec_kw={'height_ratios': [fam_h, stn_h]})

    def _panel(ax, pct, cur, base, unknown, title):
        labels = list(pct.index)
        vals = pct.values
        unk = unknown.reindex(pct.index).fillna(True).values
        cur_v = cur.reindex(pct.index).values
        base_v = base.reindex(pct.index).values
        y = np.arange(len(labels))
        ax.barh(y, vals, 0.72,
                color=[_color(v, u) for v, u in zip(vals, unk)],
                edgecolor='#333', linewidth=0.4)

        lo = min(vals.min(), -abs(alert_red)) if len(vals) else -abs(alert_red)
        hi = max(vals.max(), abs(alert_high)) if len(vals) else abs(alert_high)
        span = max(hi - lo, 1.0)
        # Right margin is wide enough to clear the counts column below,
        # which is anchored in axes coordinates rather than data ones.
        ax.set_xlim(lo - span * 0.16, hi + span * 0.62)

        for thr, col in ((-abs(alert_yellow), _STATUS_COLORS[STATUS_YELLOW]),
                         (-abs(alert_orange), _STATUS_COLORS[STATUS_ORANGE]),
                         (-abs(alert_red), _STATUS_COLORS[STATUS_RED]),
                         (abs(alert_high), _STATUS_COLORS[STATUS_DARKGREEN])):
            ax.axvline(thr, color=col, lw=1.0, ls='--', alpha=0.75, zorder=0)
        ax.axvline(0, color='#222', lw=1.2, zorder=1)

        # The counts column. A percentage on its own cannot be acted on:
        # -100% is a catastrophe when 35,154 observations went missing
        # and a footnote when 16 did, and both look identical as a bar.
        # Anchored at a fixed axes fraction (x in axes coords, y in data
        # coords) so the numbers line up as a readable column instead of
        # trailing each bar at a different place.
        count_trans = mtransforms.blended_transform_factory(
            ax.transAxes, ax.transData)

        def _n(v):
            if pd.isna(v):
                return 'n/a'
            return f'{v:,.0f}' if abs(v) >= 10 or v == 0 else f'{v:,.1f}'

        pad = span * 0.012
        for yi, v, u, c, b in zip(y, vals, unk, cur_v, base_v):
            txt = 'no baseline' if u else f'{v:+.1f}%'
            if v >= 0:
                ax.text(v + pad, yi, txt, va='center', ha='left', fontsize=8,
                        color='#222', fontweight='bold')
            else:
                ax.text(v - pad, yi, txt, va='center', ha='right', fontsize=8,
                        color='#222', fontweight='bold')
            ax.text(0.995, yi, f'{_n(c)}  \u2190  {_n(b)}', transform=count_trans,
                    va='center', ha='right', fontsize=7.5, color='#555',
                    family='monospace')

        ax.set_yticks(y)
        ax.set_yticklabels(labels, fontsize=9)
        ax.invert_yaxis()
        ax.set_xlabel(f'% change vs the {PASS_BASELINE_DAYS}-day mean at the '
                      f'same pass', fontsize=11, fontweight='bold')
        ax.set_title(f'{title}   \u2014   right column: Nobs this pass '
                     f'\u2190 baseline', fontsize=13, fontweight='bold',
                     loc='left')
        ax.grid(True, axis='x', linestyle=':', alpha=0.5)
        ax.tick_params(labelsize=9)

    _panel(ax_fam, fam_pct, frames['fam_cur'], frames['fam_base'],
           fam_no_base, 'By family (worst first)')
    _panel(ax_stn, stn_pct, frames['stn_cur'], frames['stn_base'],
           stn_no_base, 'By station (worst first)')

    handles = [
        plt.Rectangle((0, 0), 1, 1, fc=_STATUS_COLORS[STATUS_DARKGREEN],
                      label=f'>= +{alert_high:.0f}%'),
        plt.Rectangle((0, 0), 1, 1, fc=_STATUS_COLORS[STATUS_GREEN],
                      label='Normal'),
        plt.Rectangle((0, 0), 1, 1, fc=_STATUS_COLORS[STATUS_YELLOW],
                      label=f'>= {alert_yellow:.0f}% drop'),
        plt.Rectangle((0, 0), 1, 1, fc=_STATUS_COLORS[STATUS_ORANGE],
                      label=f'>= {alert_orange:.0f}% drop'),
        plt.Rectangle((0, 0), 1, 1, fc=_STATUS_COLORS[STATUS_RED],
                      label=f'>= {alert_red:.0f}% drop / outage'),
        plt.Rectangle((0, 0), 1, 1, fc=_STATUS_COLORS[STATUS_GREY],
                      label='No baseline yet'),
    ]
    fig.legend(handles=handles, loc='lower center', ncol=6, fontsize=9,
               frameon=True, bbox_to_anchor=(0.5, 0.005))

    fig.suptitle(
        f'Pass deviation from baseline \u2014 {region} \u2014 {flag_criteria}\n'
        f'This pass: {run_time:%Y%m%d} {frames["run_hour"]:02d}Z   |   '
        f'baseline: mean of {frames["n_cycles"]} cycle(s) at '
        f'{frames["run_hour"]:02d}Z since {frames["window_start"]:%Y%m%d}',
        fontsize=15, fontweight='bold')
    fig.tight_layout(rect=[0, 0.035, 1, 0.955])
    boxes = (_row_click_boxes(fig, ax_fam, fam_pct.index)
             + _row_click_boxes(fig, ax_stn, stn_pct.index))
    fig.savefig(out_path, dpi=70)
    plt.close(fig)
    return out_path, boxes


def _draw_mosaic(df_fam, family, region, flag_criteria, window_days,
                 alert_yellow, alert_orange, alert_red, alert_high, dates, out_path):
    """df_fam: rows for ONE family, columns [id_stn, date, hour, Nobs,
    baseline, pct_change, status]. Draws a rows=id_stn x cols=date heatmap.
    dates: the family's shared, sorted list of cycle dates."""
    stns = sorted(df_fam['id_stn'].unique())
    if not stns or not dates:
        return None

    n_stn, n_date = len(stns), len(dates)
    stn_idx = {s: i for i, s in enumerate(stns)}
    date_idx = {d: i for i, d in enumerate(dates)}

    # Missing cells default to RED — whether a station hasn't started
    # reporting yet or a cycle is otherwise absent, treat it as an alert
    # rather than a neutral/invisible white cell (easy to miss otherwise).
    grid = np.full((n_stn, n_date), STATUS_RED, dtype=int)
    nobs_grid = np.full((n_stn, n_date), np.nan)
    for row in df_fam.itertuples(index=False):
        i, j = stn_idx[row.id_stn], date_idx[row.date]
        grid[i, j] = row.status
        nobs_grid[i, j] = row.Nobs

    fig_w = _shared_fig_width(n_date)
    fig_h = max(3.5, min(0.32 * n_stn, 60)) + 1.8
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.imshow(grid, aspect='auto', cmap=_STATUS_CMAP, norm=_STATUS_NORM,
              interpolation='nearest')

    # Per-cell text labels ("215,942" etc.) need real horizontal room --
    # the previous "n_date <= 40" cutoff didn't account for how WIDE
    # each cell actually is: _shared_fig_width has a 9" floor, so even
    # at n_date=40 each cell is under 0.25" wide, nowhere near enough
    # for a 6-7 character number at fontsize=8 -- confirmed directly
    # from a real report where the numbers ran together illegibly.
    # Computing the actual per-cell width and gating on THAT (not a
    # fixed date count) is the fix.
    plot_width_inches = (0.99 - 0.06) * fig_w
    cell_width_inches = plot_width_inches / n_date if n_date else 0

    if n_stn <= 60 and cell_width_inches >= 0.55:
        for i in range(n_stn):
            for j in range(n_date):
                # grid[i, j] defaults to STATUS_RED (not STATUS_NODATA)
                # for any (station, date) combination genuinely absent
                # from df_fam -- e.g. a station/satellite that only
                # starts reporting partway through the period, so
                # cycles before its first appearance are legitimately
                # missing (see _fill_gaps_since_first_seen's docstring).
                # For those cells nobs_grid[i, j] stays NaN even though
                # grid[i, j] != STATUS_NODATA, so the NaN check here is
                # required -- without it, int(nan) crashes the whole
                # report the first time any family has a station that
                # didn't report from day one (a common, expected case,
                # confirmed directly from a real production traceback).
                if grid[i, j] != STATUS_NODATA and not np.isnan(nobs_grid[i, j]):
                    ax.text(j, i, f'{int(nobs_grid[i, j]):,}', ha='center',
                            va='center', fontsize=8, color='#222')

    # Left margin sized to the LONGEST station/codtyp name actually
    # present, not a fixed 0.06 -- a fixed fraction was fine for short
    # names but clipped longer ones (e.g. "ACARS"/"AMDAR" rendered as
    # "CARS"/"MDAR" in a real report), and is nowhere near enough for
    # families with much longer id_stn labels (e.g. "GROUND BASED GPS",
    # "AURA-MLS-O3"). ~0.11"/character at fontsize=11 is a conservative
    # per-character estimate; +0.15" is just a small padding buffer
    # (no rotated axis-title label to reserve room for any more).
    max_label_chars = max((len(str(s)) for s in stns), default=4)
    left_margin_inches = 0.11 * max_label_chars + 0.15
    left_frac = min(0.45, left_margin_inches / fig_w)

    ax.set_yticks(range(n_stn))
    ax.set_yticklabels(stns, fontsize=11)
    _draw_hierarchical_xaxis(ax, dates, n_bottom_rows=2)
    # id_stn axis label removed -- the station names are already the
    # y-tick labels themselves, an extra "id_stn" title was redundant.
    ax.set_title(
        f'Mosaic — {family} ({region}) — {flag_criteria}  (Nobs-based only)\n'
        f'vs mean of same hour over previous {window_days} days\n'
        f'Yellow >= {alert_yellow:.0f}% drop   Orange >= {alert_orange:.0f}%   '
        f'Red >= {alert_red:.0f}% (incl. outage)   |   Dark green >= +{alert_high:.0f}%',
        fontsize=12)

    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, fc=_STATUS_COLORS[STATUS_DARKGREEN], label=f'>= +{alert_high:.0f}% (above baseline)'),
        plt.Rectangle((0, 0), 1, 1, fc=_STATUS_COLORS[STATUS_GREEN], label='Normal'),
        plt.Rectangle((0, 0), 1, 1, fc=_STATUS_COLORS[STATUS_YELLOW], label=f'>= {alert_yellow:.0f}% drop'),
        plt.Rectangle((0, 0), 1, 1, fc=_STATUS_COLORS[STATUS_ORANGE], label=f'>= {alert_orange:.0f}% drop'),
        plt.Rectangle((0, 0), 1, 1, fc=_STATUS_COLORS[STATUS_RED], label=f'>= {alert_red:.0f}% drop / outage / no data'),
        plt.Rectangle((0, 0), 1, 1, fc=_STATUS_COLORS[STATUS_GREY], label='Insufficient history'),
    ]
    # ncol scales with figure width -- forcing all 6 entries onto one row
    # (a fixed ncol=6) made the legend wider than the figure itself for
    # any narrow chart (few dates), clipping it at the left/right edges.
    legend_ncol = 2 if fig_w < 12 else (3 if fig_w < 18 else 6)

    # Top/bottom margins reserved in FIXED INCHES (title ~0.95" for the
    # 3-line title, x-axis hierarchy ~1.5", legend ~0.9"), converted to
    # a fraction of THIS figure's own height -- a fixed FRACTION (e.g.
    # bottom=0.40) is fine for a short mosaic but wastes enormous
    # whitespace on a tall one: with 75 stations (fig_h ~26"), a fixed
    # 40% bottom margin reserves ~10" of blank space for content that
    # only ever needs ~2.5", pushing the mosaic itself far down the
    # page below its own heading -- confirmed directly from a real
    # 75-row combined mosaic. The legend's bbox_to_anchor y-offset is
    # in AXES-fraction units (relative to the plot's own height), so
    # it's computed from the axes' actual height in inches to land at
    # a fixed inch distance below the x-axis labels regardless of
    # fig_h, the same fix already applied to the channel mosaic.
    title_h = 0.95
    # Now that _draw_hierarchical_xaxis positions its day/month rows at
    # a FIXED inch distance below the axes (not a fraction of the
    # axes' own height), the space it actually needs is small and
    # constant (~0.6") regardless of how tall this particular mosaic
    # is -- the old 1.5" reservation was sized for the fraction-based
    # version and left a large unexplained gap before the legend on
    # any short-to-medium mosaic.
    xaxis_h = 0.65
    legend_h = 0.85 + 0.28 * ((len(legend_handles) + legend_ncol - 1) // legend_ncol)
    top_frac = max(0.55, 1.0 - title_h / fig_h)
    bottom_frac = min(0.45, (xaxis_h + legend_h) / fig_h)
    axes_height_inches = (top_frac - bottom_frac) * fig_h
    legend_y_axes_frac = -(xaxis_h + 0.40) / axes_height_inches

    ax.legend(handles=legend_handles, loc='upper center',
             bbox_to_anchor=(0.5, legend_y_axes_frac),
             ncol=legend_ncol, fontsize=9, frameon=True)

    fig.subplots_adjust(left=left_frac, right=0.99, top=top_frac, bottom=bottom_frac)
    fig.savefig(out_path, dpi=70)
    plt.close(fig)
    return out_path


def _draw_channel_mosaic(df_chan_stn, family, stn, region, flag_criteria,
                         dates, out_path):
    """RADIANCE families only: rows = channel, columns = cycle, coloured
    by Nobs itself (sequential colourmap) -- a volume-SHAPE view, not an
    alert view (no yellow/orange/red tiers here; that grading is
    per-station, not per-channel, in this first version). df_chan_stn:
    rows for ONE (family, id_stn), columns [channel, date, Nobs].

    A cycle can have Nobs in the MAIN (non-channel) time series while
    having NOTHING here, if every observation that cycle happened to
    carry no channel number (vcoord IS NULL) -- confirmed as a real,
    occurring scenario, not just a hypothetical edge case. Rather than
    leave that column blank/white (which reads as a rendering glitch,
    indistinguishable from "this script is broken"), those NaN cells
    are drawn in an explicit light grey via `cmap.set_bad()`, and the
    column count is reported back so the caller can add a note.

    Returns (out_path, n_gap_cycles) -- n_gap_cycles is how many of
    `dates` had NO channel data at all (fully-grey columns).
    """
    channels = sorted(df_chan_stn['channel'].dropna().unique())
    if not channels or not dates:
        return None, 0

    n_chan, n_date = len(channels), len(dates)
    chan_idx = {c: i for i, c in enumerate(channels)}
    date_idx = {d: i for i, d in enumerate(dates)}

    grid = np.full((n_chan, n_date), np.nan)
    for row in df_chan_stn.itertuples(index=False):
        if row.channel not in chan_idx or row.date not in date_idx:
            continue
        i, j = chan_idx[row.channel], date_idx[row.date]
        grid[i, j] = row.Nobs

    # Columns that are ENTIRELY NaN -- every channel missing that cycle
    # (e.g. every obs that cycle had vcoord IS NULL) -- reported back so
    # the HTML note can say how many cycles this affected.
    n_gap_cycles = int(np.all(np.isnan(grid), axis=0).sum())

    # Every OTHER chart in this report (mosaic, global time series,
    # per-station time series) uses left=0.06/right=0.99 of
    # _shared_fig_width(n_date) for its plot area. A RIGHT-side vertical
    # colorbar competes with that chart for HORIZONTAL space (an earlier
    # version of this function tried reserving extra width for it, but
    # in practice the plot area still didn't line up column-for-column
    # with the other charts). Putting the colorbar BELOW the plot
    # instead -- horizontal, under the hierarchical x-axis labels --
    # sidesteps the problem entirely: the main axes can use the exact
    # same fig_w/left/right as every other chart, no compensation
    # needed, since the colorbar only costs extra HEIGHT, which none of
    # the other charts share or care about.
    fig_w = _shared_fig_width(n_date)
    plot_h = max(3.0, min(0.18 * n_chan, 40))
    title_h = 0.5          # top margin for the title
    xaxis_h = 0.65          # hierarchical x-axis, now fixed-inch (see
                            # _draw_hierarchical_xaxis) -- no longer
                            # needs to be sized as if it scaled with
                            # the axes' own height
    cbar_gap = 0.20          # gap between x-axis labels and the colorbar
    cbar_rect_h = 0.18       # the coloured gradient bar itself
    cbar_labels_h = 0.55     # room BELOW the bar for its tick numbers + "Nobs" label
    bottom_margin = 0.08     # tiny margin at the very bottom of the figure
    fig_h = (plot_h + title_h + xaxis_h + cbar_gap + cbar_rect_h
             + cbar_labels_h + bottom_margin)

    left_frac = 0.06
    right_frac = 0.99
    top_frac = 1.0 - title_h / fig_h
    cbar_bottom_frac = (bottom_margin + cbar_labels_h) / fig_h
    cbar_top_frac = cbar_bottom_frac + cbar_rect_h / fig_h
    plot_bottom_frac = cbar_top_frac + (cbar_gap + xaxis_h) / fig_h

    fig = plt.figure(figsize=(fig_w, fig_h))
    ax = fig.add_axes([left_frac, plot_bottom_frac, right_frac - left_frac,
                       top_frac - plot_bottom_frac])
    cmap = plt.get_cmap('viridis').copy()
    cmap.set_bad(color='#BDBDBD')  # explicit grey for NaN, matches the
    # main mosaic's "insufficient history" grey -- the earlier #D9D9D9
    # was too close to the page's own light background colour, so a
    # sparse family (most cells legitimately NaN, e.g. GPS-RO satellites
    # that only report occasionally) rendered as what looked like a
    # large blank gap rather than visibly-grey "no data" cells.
    im = ax.imshow(grid, aspect='auto', cmap=cmap, interpolation='nearest')

    cbar_ax = fig.add_axes([left_frac, cbar_bottom_frac, right_frac - left_frac,
                            cbar_top_frac - cbar_bottom_frac])
    cbar = fig.colorbar(im, cax=cbar_ax, orientation='horizontal')
    cbar.set_label('Nobs', fontsize=9)
    cbar.ax.tick_params(labelsize=8)

    # Keep channel labels readable even with many channels: thin them
    # out to at most ~40 shown ticks.
    step = max(1, n_chan // 40)
    ytick_pos = list(range(0, n_chan, step))
    ax.set_yticks(ytick_pos)
    ax.set_yticklabels([f'{int(channels[i])}' for i in ytick_pos], fontsize=10)
    _draw_hierarchical_xaxis(ax, dates, hour_fontsize=6, day_fontsize=7,
                             month_fontsize=7, n_bottom_rows=2)
    # "Channel" axis-title label removed -- the channel numbers are
    # already the y-tick labels themselves; freeing this space up is
    # the simplest way to keep the (now bigger, fontsize=10) numbers
    # from getting clipped on the left.
    title = f'Per-channel Nobs — {family} / {stn} ({region}) — {flag_criteria}'
    if n_gap_cycles:
        title += f'  (grey = no channel data, {n_gap_cycles} cycle{"s" if n_gap_cycles != 1 else ""})'
    ax.set_title(title, fontsize=11)

    fig.savefig(out_path, dpi=70)
    plt.close(fig)
    return out_path, n_gap_cycles


def _draw_global_timeseries(df_fam_global, family, region, flag_criteria,
                            agr_list, out_path, dates, value_col='Nobs',
                            value_label='Nobs (all stations)',
                            title_prefix='Global Time Series (all stations)'):
    """One full-width plot for a single summed metric (Nobs OR
    Nobsprofile) across the whole set of stations, per cycle. Plotted
    against the SAME integer cycle positions as the mosaic (not real
    datetimes), with the same hierarchical Year-Month/Day/Hour axis, so
    every column lines up exactly with the mosaic above it. Optional
    --agr overlay (only meaningful for the Nobs plot; pass agr_list=[]
    for profiles)."""
    n_date = len(dates)
    # Reindex to the family's full cycle list so a cycle with no data at
    # all still has its column (as a gap in the line, not a shift).
    date_pos = {d: i for i, d in enumerate(dates)}
    df_fam_global = df_fam_global.set_index('date').reindex(dates)
    x = np.arange(n_date)

    fig_w = _shared_fig_width(n_date)
    n_rows = 1 + len(agr_list)
    row_h = 2.8
    fig, axes = plt.subplots(n_rows, 1, figsize=(fig_w, 2.4 + row_h * n_rows),
                             sharex=True, squeeze=False)
    axes = axes[:, 0]

    # Left margin sized to the actual magnitude of the values being
    # plotted, not a fixed 0.06 -- a fixed fraction clipped the leading
    # digit(s) of large Nobs values in a real report (tick labels
    # showing "00000" instead of "150000"). ~0.10"/digit at fontsize=10
    # is a conservative per-character estimate; +0.35" covers the
    # rotated y-axis title plus a small padding buffer.
    try:
        max_val = np.nanmax(np.abs(df_fam_global[value_col].values))
        n_digits = len(str(int(max_val))) if np.isfinite(max_val) else 5
    except (ValueError, TypeError):
        n_digits = 5
    left_margin_inches = 0.10 * max(n_digits, 4) + 0.35
    left_frac = min(0.35, left_margin_inches / fig_w)

    ax_n = axes[0]
    ax_n.axhline(0.0, color='#444444', lw=1.0, ls='-', alpha=0.65, zorder=1)
    ax_n.plot(x, df_fam_global[value_col], marker='o',
              markersize=5, linestyle='-', linewidth=2.0, color=REF_COLOR,
              label=value_label, zorder=2)
    ax_n.set_ylabel(value_label, fontsize=13, fontweight='bold')
    ax_n.grid(True, linestyle=':', alpha=0.6)
    ax_n.legend(fontsize=10, loc='best', ncol=2)
    ax_n.tick_params(labelsize=10)

    for k, metric in enumerate(agr_list, start=1):
        ax_m = axes[k]
        col = f'avg_{metric}'
        ax_m.axhline(0.0, color='gray', lw=0.8, ls='-', alpha=0.5)
        if col in df_fam_global.columns and df_fam_global[col].notna().any():
            ax_m.plot(x, df_fam_global[col],
                      marker='^', markersize=5, linestyle='--', linewidth=1.8,
                      color=REF_COLOR, label=f'AVG({metric})')
            mval = float(np.nanmean(df_fam_global[col].values))
            ax_m.set_title(f'Mean AVG({metric}) over period: {_fmt_departure(mval)}',
                           fontsize=11, loc='right', color='#555')
        ax_m.set_ylabel(f'AVG({metric})', fontsize=13, fontweight='bold')
        ax_m.grid(True, linestyle=':', alpha=0.6)
        ax_m.legend(fontsize=11, loc='best')
        ax_m.tick_params(labelsize=10)

    ax_bottom = axes[-1]
    _draw_hierarchical_xaxis(ax_bottom, dates, n_bottom_rows=2)

    fig.suptitle(f'{title_prefix} — {family} ({region}) — {flag_criteria}',
                fontsize=15, fontweight='bold')
    fig.subplots_adjust(left=left_frac, right=0.99, top=0.90, bottom=0.20)
    fig.savefig(out_path, dpi=70)
    plt.close(fig)
    return out_path


def _draw_station_full_timeseries(df_stn, stn, family, region, flag_criteria,
                                  dates, window_days, alert_yellow, alert_orange,
                                  alert_red, out_path):
    """ONE full-width Nobs-only plot for a single station — plotted
    against the SAME integer cycle positions as the mosaic, with the
    same hierarchical Year-Month/Day/Hour axis, so every station's plot
    (and the mosaic itself) lines up column-for-column. Shows the
    actual Nobs curve with alert cycles marked in their tier colour
    (dark green above baseline / yellow / orange / red below it)."""
    n_date = len(dates)
    date_pos = {d: i for i, d in enumerate(dates)}
    df_stn = df_stn.set_index('date').reindex(dates)
    df_stn['_x'] = np.arange(n_date)
    fig_w = _shared_fig_width(n_date)
    stn_col = _station_color(family, stn)

    # Same dynamic left margin as _draw_global_timeseries -- sized to
    # the actual magnitude of this station's Nobs values, not a fixed
    # 0.06 (which clipped large values' leading digits in a real report).
    try:
        max_val = np.nanmax(np.abs(df_stn['Nobs'].values))
        n_digits = len(str(int(max_val))) if np.isfinite(max_val) else 5
    except (ValueError, TypeError):
        n_digits = 5
    left_margin_inches = 0.10 * max(n_digits, 4) + 0.35
    left_frac = min(0.35, left_margin_inches / fig_w)

    fig, ax = plt.subplots(figsize=(fig_w, 4.6))
    ax.axhline(0.0, color='#444444', lw=1.0, ls='-', alpha=0.65, zorder=1)
    ax.plot(df_stn['_x'], df_stn['Nobs'], linestyle='-', linewidth=1.6,
            color=REF_COLOR, zorder=2)

    # Every point gets a marker in its OWN status colour (not just the
    # alert-worthy tiers) -- green for normal, dark green for above
    # baseline, yellow/orange/red for the drop tiers, grey for
    # insufficient history -- so the curve communicates status at a
    # glance along its whole length, the same colour scheme as the
    # mosaic above it, not just where something's flagged.
    for tier, label in ((STATUS_GREEN, 'Normal'), (STATUS_DARKGREEN, 'Above baseline'),
                        (STATUS_YELLOW, 'Yellow'), (STATUS_ORANGE, 'Orange'),
                        (STATUS_RED, 'Red'), (STATUS_GREY, 'Insufficient history')):
        pts = df_stn[df_stn['status'] == tier]
        if not pts.empty:
            ax.scatter(pts['_x'], pts['Nobs'], marker='o', s=40,
                      color=_STATUS_COLORS[tier], edgecolor='#333',
                      linewidth=0.6, zorder=3, label=label)

    n_alerts = int(df_stn['status'].isin([STATUS_YELLOW, STATUS_ORANGE, STATUS_RED]).sum())
    ax.set_ylabel('Nobs', fontsize=13, fontweight='bold')
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(fontsize=10, loc='best', ncol=4)
    ax.tick_params(labelsize=10)

    _draw_hierarchical_xaxis(ax, dates, n_bottom_rows=2)

    ax.set_title(f'Station: {stn}  —  {family} ({region})  —  '
                f'{n_alerts} alert cycle{"s" if n_alerts != 1 else ""}',
                fontsize=14, fontweight='bold', color='white',
                bbox=dict(boxstyle='round,pad=0.4', facecolor=stn_col, edgecolor='none'))

    for spine in ax.spines.values():
        spine.set_edgecolor(stn_col)
        spine.set_linewidth(1.6)

    fig.subplots_adjust(left=left_frac, right=0.99, top=0.86, bottom=0.24)
    fig.savefig(out_path, dpi=70)
    plt.close(fig)
    return out_path, stn_col


def obstimedb_plot(
    region,
    families,
    datestart,
    dateend,
    pathwork,
    name_in,
    flag_criteria,
    agr=None,
    path_in=None,
    window_days=10,
    alert_yellow=10.0,
    alert_orange=15.0,
    alert_red=20.0,
    alert_high=10.0,
):
    console = Console(width=220)
    agr_list = _norm_agr(agr)

    list_df = []
    list_df_chan = []
    console.print(f"[bold yellow]Extracting data from databases in: {pathwork}[/bold yellow]")

    for family in families:
        db_file = os.path.join(pathwork, family, f'{name_in}_{region}_{datestart}_{dateend}_{flag_criteria}_{family}.db')
        if not os.path.exists(db_file):
            console.print(f"[red]  Warning: File not found {db_file}[/red]")
            continue

        _dedupe_moyenne_inplace(db_file)

        conn = sqlite3.connect(db_file)
        select_extra = ["SUM(Nobsdata) as Nobs", "SUM(Nobsprofile) as Nprofile"]
        for metric in agr_list:
            col = f"avg_{metric}"
            select_extra.append(f"SUM({col} * Nobsdata) as _wsum_{metric}")
            select_extra.append(
                f"SUM(CASE WHEN {col} IS NOT NULL THEN Nobsdata ELSE 0 END) as _wden_{metric}")
        query = ("SELECT date, id_stn, " + ", ".join(select_extra) +
                 " FROM moyenne WHERE channel IS NULL GROUP BY date, id_stn;")
        try:
            df = pd.read_sql_query(query, conn)
        except Exception as e:
            console.print(f"[red]  Could not read {db_file}: {e}[/red]")
            conn.close()
            continue

        # ---- Per-channel extraction (radiance families only) ----
        # A family has channel data iff `channel` isn't entirely NULL --
        # no need to separately call pikobs.family() here, the data
        # itself tells us (VCOTYP=='CANAL' is exactly what populates
        # `channel` on the extraction side, in obstimedb.py).
        try:
            chan_probe = pd.read_sql_query(
                "SELECT COUNT(*) as n FROM moyenne WHERE channel IS NOT NULL", conn)
            has_channel = int(chan_probe['n'].iloc[0]) > 0
        except Exception:
            has_channel = False

        if has_channel:
            df_chan = pd.read_sql_query(
                "SELECT date, id_stn, channel, SUM(Nobsdata) as Nobs "
                "FROM moyenne WHERE channel IS NOT NULL "
                "GROUP BY date, id_stn, channel;", conn)
            df_chan['family'] = family
            list_df_chan.append(df_chan)

        conn.close()

        for metric in agr_list:
            wsum, wden = df.get(f"_wsum_{metric}"), df.get(f"_wden_{metric}")
            if wsum is not None and wden is not None:
                with np.errstate(invalid='ignore', divide='ignore'):
                    df[f"avg_{metric}"] = np.where(wden > 0, wsum / wden, np.nan)
                df = df.drop(columns=[f"_wsum_{metric}", f"_wden_{metric}"])

        df['family'] = family
        list_df.append(df)

    if not list_df:
        console.print("[red]No data extracted — nothing to plot.[/red]")
        return

    df_all = pd.concat(list_df, ignore_index=True)
    df_all['date_raw'] = df_all['date'].astype(str).str.strip()
    df_all['date'] = pd.to_datetime(df_all['date_raw'], format='%Y%m%d%H', errors='coerce')
    df_all = df_all.dropna(subset=['date'])
    df_all['hour'] = df_all['date'].dt.hour

    df_chan_all = None
    if list_df_chan:
        df_chan_all = pd.concat(list_df_chan, ignore_index=True)
        df_chan_all['date'] = pd.to_datetime(
            df_chan_all['date'].astype(str).str.strip(), format='%Y%m%d%H', errors='coerce')
        df_chan_all = df_chan_all.dropna(subset=['date'])

    console.print(f"[bold yellow]  Period: {datestart} -> {dateend}  |  "
                 f"Baseline window: {window_days} days  |  "
                 f"Thresholds: Y>={alert_yellow:.0f}% O>={alert_orange:.0f}% R>={alert_red:.0f}%[/bold yellow]")

    # ---- Fill gaps: a station whose obs vanish from the RDB must show up
    # as an explicit Nobs=0 (not a silent absent/white cell). ----
    df_all = pd.concat(
        [_fill_gaps_since_first_seen(df_all[df_all['family'] == fam], datestart, dateend)
         for fam in families if fam in df_all['family'].unique()],
        ignore_index=True)

    # ---- Per-(family, id_stn, hour) status computation (Nobs-only) ----
    df_status = _compute_status(df_all, window_days, alert_yellow, alert_orange, alert_red, alert_high)

    html_content = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Observation Time Report ({region}) | Criteria: {flag_criteria} | Period: {datestart} {dateend}</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background-color: #f9f9f9; font-size: 16px; }}
            h1 {{ color: #333; border-bottom: 2px solid #4C72B0; padding-bottom: 10px; }}
            h2 {{ color: #333; font-size: 1.5em; }}
            h3 {{ color: #333; font-size: 1.2em; }}
            .note {{ font-size: 0.95em; color: #555; margin-bottom: 8px; }}
            .explain {{ background: #fffbe6; border: 1px solid #f0e2a0; border-radius: 8px;
                       padding: 16px 20px; margin-bottom: 28px; font-size: 0.98em; line-height: 1.55; color: #444; }}
            .explain b {{ color: #222; }}
            .swatch {{ display:inline-block; width:14px; height:14px; border-radius:3px; margin-right:6px; vertical-align:middle; }}
            .card {{ background: white; padding: 18px; border: 1px solid #ddd; border-radius: 8px;
                     box-shadow: 0 2px 5px rgba(0,0,0,0.08); margin-bottom: 44px; scroll-margin-top: 20px; }}
            .scrollwrap {{ overflow-x: auto; overflow-y: hidden; border: 1px solid #eee;
                          border-radius: 6px; margin-bottom: 18px; background: #fff; }}
            .scrollwrap img {{ max-width: none; height: auto; display: block; }}
            img {{ max-width: 100%; height: auto; display: block; margin: 0 auto; }}
            table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; font-size: 0.92em; }}
            table th, table td {{ border: 1px solid #ddd; padding: 6px 10px; text-align: right; }}
            table th {{ background: #4C72B0; color: white; text-align: center; position: sticky; top: 0; }}
            table td:first-child, table td:nth-child(2) {{ text-align: left; }}
            .problem-menu {{ background: #fff0f0; border: 1px solid #f0b8b8; border-radius: 8px;
                            padding: 12px 18px; margin-bottom: 24px; }}
            .problem-menu a {{ display: inline-block; margin: 3px 8px 3px 0; padding: 4px 10px;
                              background: #E53935; color: white; border-radius: 5px;
                              text-decoration: none; font-size: 0.9em; font-weight: bold; }}
            .problem-menu a:hover {{ background: #B71C1C; }}
            details.channel-details {{ margin-top: 14px; border: 1px solid #ddd; border-radius: 6px;
                                      padding: 8px 12px; background: #fafafa; }}
            details.channel-details summary {{ cursor: pointer; font-weight: bold; color: #2a4d8f; padding: 4px 0; }}
            #profileSummaryTable th {{ cursor: pointer; user-select: none; }}
            #profileSummaryTable th:hover {{ background: #35578f; }}
            /* Compact sizing so the table stays small when copy-pasted
               into Teams/Outlook/etc -- baked into the cells themselves
               (not just the page's own CSS) so it survives a plain
               copy-paste, which usually keeps inline/computed styles
               but not an external stylesheet. */
            #profileSummaryTable {{ font-size: 0.75em; }}
            #profileSummaryTable th, #profileSummaryTable td {{ padding: 3px 6px; }}
            #profileSummaryTable tbody tr:hover {{ background: #eef4ff !important; }}
        </style>
        <script>
            // Generic click-to-sort for any table built with this report's
            // convention: <th data-sort="num|text" onclick="sortObsTable(this)">
            // and each <td data-v="raw value">. Toggles ascending/descending
            // on repeated clicks of the same header.
            function sortObsTable(th) {{
                var table = th.closest('table');
                var headerRow = table.rows[0];
                var allRows = Array.prototype.slice.call(table.rows, 1);
                // ONLY the grand-total row (family AND id_stn both
                // 'ALL') is pinned at the top, excluded from sorting.
                // Per-family "ALL" rows (e.g. ai/ALL, sf/ALL) sort
                // normally along with the individual id_stn rows.
                var pinnedRows = allRows.filter(function(r) {{
                    return r.cells[0].getAttribute('data-v') === 'ALL'
                        && r.cells[1].getAttribute('data-v') === 'ALL';
                }});
                var rows = allRows.filter(function(r) {{
                    return !(r.cells[0].getAttribute('data-v') === 'ALL'
                        && r.cells[1].getAttribute('data-v') === 'ALL');
                }});
                var idx = Array.prototype.indexOf.call(headerRow.children, th);
                var type = th.getAttribute('data-sort');
                var asc = th.getAttribute('data-asc') !== 'true';
                Array.prototype.forEach.call(headerRow.children, function(h) {{
                    if (h !== th) h.removeAttribute('data-asc');
                }});
                th.setAttribute('data-asc', asc);
                rows.sort(function(a, b) {{
                    var ca = a.cells[idx], cb = b.cells[idx];
                    var va = ca.getAttribute('data-v') !== null ? ca.getAttribute('data-v') : ca.textContent;
                    var vb = cb.getAttribute('data-v') !== null ? cb.getAttribute('data-v') : cb.textContent;
                    if (type === 'num') {{
                        va = parseFloat(va); if (isNaN(va)) va = -Infinity;
                        vb = parseFloat(vb); if (isNaN(vb)) vb = -Infinity;
                    }} else {{
                        va = va.toLowerCase(); vb = vb.toLowerCase();
                    }}
                    if (va < vb) return asc ? -1 : 1;
                    if (va > vb) return asc ? 1 : -1;
                    return 0;
                }});
                pinnedRows.forEach(function(r) {{ table.appendChild(r); }});
                rows.forEach(function(r) {{ table.appendChild(r); }});
            }}
        </script>
    </head>
    <body>
        <h1>Single-experience time diagnostics — {name_in} | Region: {region} | Criteria: {flag_criteria}</h1>
        <p class="note">Period: {datestart} &rarr; {dateend}, every 6h.</p>
    """

    if path_in:
        html_content += (
            "<div style='background:#eef4ff; border:1px solid #cdd9f0; "
            "border-radius:8px; padding:10px 14px; margin-bottom:24px; "
            "font-size:0.95em; color:#2a4d8f;'>"
            f"<b>{name_in}</b> &nbsp;=&nbsp; <code>{path_in}</code>"
            "</div>"
        )

    # ---- Profile summary table: shown FIRST, before everything else,
    # matching the reference report's own ordering. ----
    if not df_all.empty:
        run_time = df_all['date'].max()
        legend_html, summary_html, df_summary = _draw_profile_summary_table(
            df_all, run_time, name_in=name_in)
        html_content += f"""
        <div class="card">
            <h2>Average Nobs Profiles per 6 Hours</h2>
            {legend_html}
            {summary_html}
        </div>
        """

    # ---- Nobs composition summary: total Nobs by family and by station
    # over the FULL requested period, followed by two pass-validation
    # charts answering a different question -- is THIS cycle's
    # composition normal, or is something missing right now. ----
    if not df_status.empty:
        comp_path = os.path.join(pathwork, f"NobsComposition_{region}_{flag_criteria}.png")
        _, comp_boxes = _draw_nobs_composition(
            df_status, region, flag_criteria, datestart, dateend, comp_path)
        with open(comp_path, 'rb') as f:
            comp_b64 = base64.b64encode(f.read()).decode('utf-8')
        comp_map = _safe_anchor(f'map-comp-{region}-{flag_criteria}')
        html_content += f"""
        <div class="card">
            <h2>Observation Volume Composition</h2>
            <p class="note">Total Nobs for the period {datestart} &rarr; {dateend}
            (the same start/end dates used for the whole report), by
            family and by individual station, with the % of the grand
            total each one represents. <b>Click any bar</b> to jump to
            that family or station further down the page.</p>
            <div class="scrollwrap">
                {_click_map_html(comp_map, comp_boxes)}
                <img src="data:image/png;base64,{comp_b64}" alt="Nobs composition"
                     usemap="#{comp_map}">
            </div>
        """

        run_time = df_all['date'].max()
        run_hour = int(run_time.hour)

        vs_path = os.path.join(
            pathwork, f"PassVsBaseline_{region}_{flag_criteria}.png")
        vs_result, vs_boxes = _draw_pass_vs_baseline(
            df_all, run_time, region, flag_criteria, vs_path)
        if vs_result:
            with open(vs_path, 'rb') as f:
                vs_b64 = base64.b64encode(f.read()).decode('utf-8')
            vs_map = _safe_anchor(f'map-vs-{region}-{flag_criteria}')
            html_content += f"""
            <h3 style="margin-top:34px;">This pass vs its {PASS_BASELINE_DAYS}-day baseline
            ({run_time:%Y%m%d} {run_hour:02d}Z)</h3>
            <p class="note">Solid bar: what this cycle actually carried. Hatched bar:
            the mean over the last {PASS_BASELINE_DAYS} days at the same {run_hour:02d}Z
            pass. Read them together &mdash; a family whose two bars match is
            contributing its usual share, and a solid bar visibly shorter than its
            hatched twin is where this cycle lost data. <b>Click any bar</b> to jump
            to its time series.</p>
            <div class="scrollwrap">
                {_click_map_html(vs_map, vs_boxes)}
                <img src="data:image/png;base64,{vs_b64}" alt="Pass vs baseline"
                     usemap="#{vs_map}">
            </div>
            """

        dev_path = os.path.join(
            pathwork, f"PassDeviation_{region}_{flag_criteria}.png")
        dev_result, dev_boxes = _draw_pass_deviation(
            df_all, run_time, region, flag_criteria,
            alert_yellow, alert_orange, alert_red, alert_high, dev_path)
        if dev_result:
            with open(dev_path, 'rb') as f:
                dev_b64 = base64.b64encode(f.read()).decode('utf-8')
            dev_map = _safe_anchor(f'map-dev-{region}-{flag_criteria}')
            html_content += f"""
            <h3 style="margin-top:34px;">Deviation of this pass from the
            {PASS_BASELINE_DAYS}-day baseline</h3>
            <p class="note">The same comparison as a percentage, worst first, with the
            mosaic's colour tiers: a bar past &minus;{alert_red:.0f}% is red here and red
            in that station's last mosaic column too. Bars to the right of zero carried
            more than usual. The right-hand column gives the absolute Nobs
            (this pass &larr; baseline), because a &minus;100% on fourteen observations
            and a &minus;100% on thirty-five thousand are the same bar and very
            different problems. Grey means there is no history at this pass yet, which
            is not the same as normal. Percentages match the <i>Diff 10d same PASS</i>
            column of the summary table at the top of this report.
            <b>Click any bar</b> to jump to its time series.</p>
            <div class="scrollwrap">
                {_click_map_html(dev_map, dev_boxes)}
                <img src="data:image/png;base64,{dev_b64}" alt="Pass deviation"
                     usemap="#{dev_map}">
            </div>
            """

        html_content += """
        </div>
        """

    # ---- Combined overview mosaic: every family's stations, all in ONE
    # image, so the whole experiment's health can be seen at a glance
    # before drilling into the per-family sections below. ----
    if len(families) > 1 and not df_status.empty:
        df_combined = df_status.copy()
        df_combined['id_stn'] = (df_combined['family'].astype(str) + ' / '
                                 + df_combined['id_stn'].astype(str))
        dates_all = sorted(df_combined['date'].unique())
        combined_path = os.path.join(pathwork, f"Mosaic_ALL_{region}_{flag_criteria}.png")
        _draw_mosaic(df_combined, 'ALL FAMILIES combined', region, flag_criteria,
                    window_days, alert_yellow, alert_orange, alert_red, alert_high,
                    dates_all, combined_path)
        with open(combined_path, 'rb') as f:
            comb_b64 = base64.b64encode(f.read()).decode('utf-8')
        n_rows_comb = df_combined['id_stn'].nunique()
        html_content += f"""
        <div class="card">
            <h2>Combined Overview — All Families</h2>
            <p class="note">Every family's stations stacked into one mosaic
            ({n_rows_comb} rows), so you can see the whole experiment's
            observation health at a glance before the per-family detail
            below. Same colour rules as every other mosaic in this report.</p>
            <div class="scrollwrap">
                <img src="data:image/png;base64,{comb_b64}" alt="Combined mosaic all families">
            </div>
        </div>
        """

    for family in families:
        df_fam = df_status[df_status['family'] == family]
        if df_fam.empty:
            continue

        dates_fam = sorted(df_fam['date'].unique())
        n_date = len(dates_fam)
        fam_anchor = _safe_anchor(family)

        # ---- 1. Mosaic (global view — all stations at a glance) ----
        mosaic_path = os.path.join(pathwork, f"Mosaic_{family}_{region}_{flag_criteria}.png")
        _draw_mosaic(df_fam, family, region, flag_criteria, window_days,
                    alert_yellow, alert_orange, alert_red, alert_high, dates_fam, mosaic_path)

        # ---- 2. Global time series: Nobs AND Nobsprofile, whole set ----
        # Sum the per-station rolling baseline too (min_count=1 so a
        # cycle where every station still lacks history stays NaN
        # instead of misleadingly summing to 0).
        agg_dict = {'Nobs': 'sum', 'Nprofile': 'sum',
                    'baseline': lambda s: s.sum(min_count=1)}
        for metric in agr_list:
            col = f'avg_{metric}'
            if col in df_fam.columns:
                agg_dict[col] = 'mean'
        df_global = df_fam.groupby('date', as_index=False).agg(agg_dict)
        df_global['hour'] = df_global['date'].dt.hour

        ts_path = os.path.join(pathwork, f"TimeSeries_{family}_{region}_{flag_criteria}.png")
        _draw_global_timeseries(df_global, family, region, flag_criteria, agr_list,
                                ts_path, dates_fam, value_col='Nobs',
                                value_label='Nobs (all stations)',
                                title_prefix='Global Time Series — Nobs (all stations)')

        prof_path = os.path.join(pathwork, f"Profiles_{family}_{region}_{flag_criteria}.png")
        _draw_global_timeseries(df_global, family, region, flag_criteria, [],
                                prof_path, dates_fam, value_col='Nprofile',
                                value_label='Nobsprofile (all stations)',
                                title_prefix='Global Time Series — Nobsprofile (all stations)')

        n_alerts = int(df_fam['status'].isin([STATUS_YELLOW, STATUS_ORANGE, STATUS_RED]).sum())
        n_stn = df_fam['id_stn'].nunique()
        n_cycles = n_date

        table = Table(title=f"Family: {family} — {n_stn} stations, {n_cycles} cycles, "
                            f"{n_alerts} alert cells (yellow+orange+red)",
                     box=box.SIMPLE, header_style="bold magenta")
        table.add_column("id_stn", justify="left")
        table.add_column("Last cycle Nobs", justify="right")
        table.add_column("Baseline", justify="right")
        table.add_column("% change", justify="right")
        table.add_column("Status", justify="center")
        last_date = df_fam['date'].max()
        df_last = df_fam[df_fam['date'] == last_date].sort_values('id_stn')
        _status_lbl = {STATUS_DARKGREEN: '[bold green]HIGH[/]', STATUS_GREEN: '[green]OK[/]',
                      STATUS_YELLOW: '[yellow]YELLOW[/]',
                      STATUS_ORANGE: '[bold orange3]ORANGE[/]', STATUS_RED: '[bold red]RED[/]',
                      STATUS_GREY: '[dim]n/a[/]', STATUS_NODATA: '-'}
        for _, row in df_last.iterrows():
            baseline = "n/a" if pd.isna(row['baseline']) else f"{row['baseline']:,.0f}"
            pct = "n/a" if pd.isna(row['pct_change']) else f"{row['pct_change']:+.1f}%"
            table.add_row(str(row['id_stn']), f"{int(row['Nobs']):,}", baseline, pct,
                         _status_lbl.get(row['status'], '-'))
        console.print(table)

        with open(mosaic_path, 'rb') as f:
            mo_b64 = base64.b64encode(f.read()).decode('utf-8')
        with open(ts_path, 'rb') as f:
            ts_b64 = base64.b64encode(f.read()).decode('utf-8')
        with open(prof_path, 'rb') as f:
            pr_b64 = base64.b64encode(f.read()).decode('utf-8')

        html_content += f"""
        <div class="card" id="family-{fam_anchor}">
            <h2>Family: {family}</h2>
            <p class="note">{n_stn} stations &middot; {n_cycles} cycles &middot;
            {n_alerts} alert cells (last cycle: {last_date}).</p>
            <h3>Station Mosaic (global view, Nobs-based)</h3>
            <p class="note">Wide image — scroll sideways to see the full period at readable size.</p>
            <div class="scrollwrap">
                <img src="data:image/png;base64,{mo_b64}" alt="Mosaic {family}">
            </div>
            <h3>Global Time Series — Nobs (whole set, same scale and ticks as mosaic)</h3>
            <div class="scrollwrap">
                <img src="data:image/png;base64,{ts_b64}" alt="Nobs time series {family}">
            </div>
            <h3>Global Time Series — Nobsprofile (whole set, same scale and ticks as mosaic)</h3>
            <div class="scrollwrap">
                <img src="data:image/png;base64,{pr_b64}" alt="Nobsprofile time series {family}">
            </div>
        """

        # ---- Per-family, per-channel data slice (radiance only) ----
        df_chan_fam = None
        if df_chan_all is not None:
            slice_ = df_chan_all[df_chan_all['family'] == family]
            if not slice_.empty:
                df_chan_fam = slice_

        # ---- 3a. Per-channel, ALL stations combined (radiance only) ----
        # Shown FIRST and NOT collapsed -- the primary channel view for
        # this family, summing Nobs per (date, channel) across every
        # id_stn/satellite. The per-station breakdown that follows is
        # the secondary, collapsed detail.
        if df_chan_fam is not None:
            df_chan_fam_all = (df_chan_fam.groupby(['date', 'channel'], as_index=False)['Nobs']
                               .sum())
            all_png = os.path.join(
                pathwork, f"Channels_ALL_{family}_{region}_{flag_criteria}.png")
            _, n_gap_cycles = _draw_channel_mosaic(df_chan_fam_all, family, 'ALL stations',
                                                   region, flag_criteria, dates_fam, all_png)
            with open(all_png, 'rb') as f:
                all_chan_b64 = base64.b64encode(f.read()).decode('utf-8')
            n_chan_fam = df_chan_fam_all['channel'].nunique()
            gap_note = ""
            if n_gap_cycles:
                gap_note = (f" <b>{n_gap_cycles} cycle{'s' if n_gap_cycles != 1 else ''}</b> "
                           f"had NO channel-tagged data at all (grey columns) even though "
                           f"the main Nobs series above still has a value there -- every "
                           f"observation that cycle happened to carry no channel number.")
            html_content += f"""
            <h3 style="margin-top:30px;">Per-channel Time Series — All Stations Combined ({n_chan_fam} channels)</h3>
            <p class="note">Nobs per channel, summed across every station/satellite in this family.{gap_note}</p>
            <div class="scrollwrap">
                <img src="data:image/png;base64,{all_chan_b64}" alt="Channels ALL {family}">
            </div>
            """

        # ---- 3b. Per-station, one full-width Nobs-only plot each ----
        html_content += """
            <h3 style="margin-top:30px;">Per-station Time Series (Nobs only)</h3>
            <p class="note">One full-width plot per station, same scale and cycle axis as the
            mosaic above — easy to compare station to station. Alert cycles are marked on
            the curve in their tier colour.</p>
        """
        for stn in sorted(df_fam['id_stn'].unique()):
            df_stn = df_fam[df_fam['id_stn'] == stn]
            stn_png = os.path.join(
                pathwork, f"Station_{_safe_filename(stn)}_{family}_{region}_{flag_criteria}.png")
            _draw_station_full_timeseries(df_stn, stn, family, region, flag_criteria,
                                          dates_fam, window_days, alert_yellow,
                                          alert_orange, alert_red, stn_png)
            with open(stn_png, 'rb') as f:
                stn_b64 = base64.b64encode(f.read()).decode('utf-8')
            stn_anchor = _safe_anchor(stn)
            html_content += f"""
            <div class="scrollwrap" id="station-{fam_anchor}-{stn_anchor}" style="scroll-margin-top: 20px;">
                <img src="data:image/png;base64,{stn_b64}" alt="Station {stn}">
            </div>
            """

            # ---- 4. Per-channel time series (radiance only), collapsed ----
            if df_chan_fam is not None:
                df_chan_stn = df_chan_fam[df_chan_fam['id_stn'] == stn]
                if not df_chan_stn.empty:
                    chan_png = os.path.join(
                        pathwork,
                        f"Channels_{_safe_filename(stn)}_{family}_{region}_{flag_criteria}.png")
                    _, n_gap_cycles_stn = _draw_channel_mosaic(df_chan_stn, family, stn, region,
                                                               flag_criteria, dates_fam, chan_png)
                    with open(chan_png, 'rb') as f:
                        chan_b64 = base64.b64encode(f.read()).decode('utf-8')
                    n_chan = df_chan_stn['channel'].nunique()
                    gap_note_stn = (f" &middot; {n_gap_cycles_stn} cycle"
                                    f"{'s' if n_gap_cycles_stn != 1 else ''} with no channel data"
                                    if n_gap_cycles_stn else "")
                    html_content += f"""
                    <details class="channel-details">
                        <summary>Per-channel Nobs — {stn} ({n_chan} channels{gap_note_stn}) — click to expand</summary>
                        <div class="scrollwrap">
                            <img src="data:image/png;base64,{chan_b64}" alt="Channels {stn}">
                        </div>
                    </details>
                    """

        html_content += "</div>"

    html_content += "</body></html>"

    html_filepath = os.path.join(pathwork, f"Full_Report_{region}_{flag_criteria}.html")
    with open(html_filepath, "w", encoding="utf-8") as f:
        f.write(html_content)

    console.print(f"[bold cyan]Process finished! Web report saved to: {html_filepath}[/bold cyan]")
