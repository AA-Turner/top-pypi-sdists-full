#!/usr/bin/python3
"""Figures of pikobs.vdedr.

Three figures per selection, with the radiance channels on the y axis:

* ``omp_bias``  residual bias and raw bias, experience minus control
* ``omp_rel``   change of sigma(OMP) and of the number of observations, %
* ``oma_rel``   the same for OMA

Everything is computed from the sums stored by the extraction, so the
SQLite STDDEV extension is not needed any more and the numbers recombine
exactly over cycles.
"""

import os
import traceback
from typing import Any, Dict, List, Optional, Sequence, Tuple

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
import numpy as np

from pikobs.figures import match_badge, save_figure, write_hover
from pikobs.configobs.style import font_size
from pikobs.obsdb import open_result
from pikobs.stats.stats import BOOT_MIN_PAIRS, cycle_bootstrap_many, padded_rows
from pikobs.stats import (
    MIN_CONFIDENCE,
    cycle_changes,
    ttest_confidence,
    sigma_confidence,
)

# =============================================================================
# Metrics
# =============================================================================

METRICS = {
    "omp_bias": ("OMP", ("residual bias", "raw bias")),
    "omp_rel": ("OMP", ("% sigma", "% Nobs")),
    "oma_rel": ("OMA", ("% sigma", "% Nobs")),
}


# =============================================================================
# Colours
# =============================================================================

ROUGE = "#FF9999"
ROUGEPUR = "#FF0000"
VERT = "#009900"
BLEU = "#1569C7"
NOIR = "#000000"

COULEURS = [BLEU, ROUGEPUR, ROUGE, VERT, NOIR]


# Sign convention:
#
# negative -> experience better -> red
# positive -> control better    -> blue
from pikobs.configobs.style import (
    CTL_BETTER,
    CTL_COLOUR,
    EXP_COLOUR,
    EXP_BETTER,
    NEUTRAL as NEUTRAL_LINE,
)
from pikobs.obsdb import safe_name as _safe

# Alternating channel row.
BAND = "#f3f4f5"


# =============================================================================
# Layout
# =============================================================================

# Enough vertical space for channel labels.
INCH_PER_CHANNEL = 0.20

MIN_HEIGHT = 7.2
MAX_HEIGHT = 260.0
#: the panel never taller than this: past it a figure seen whole on a screen
#: has text too small to read. More channels than fit at 0.3 in a row and the
#: figure goes dense: one name in k, thin test lines, the counts under the mouse
PANEL_MAX_IN = 16.0
#: the header and the top axis (the second curve's scale), in units of FS
TOP_ROOM = 2.65
#: the colour of each x axis: the curve it measures
SIGMA_AXIS_COLOUR = "#4d4d4d"
NOBS_AXIS_COLOUR = "#2e7d32"
MATCHED_AXIS_COLOUR = "#202020"

# Wider than the old figure so that the scientific plot and the
# confidence/count columns do not compete for space.
FIGURE_WIDTH = 11.5
#: every text of a vdedr figure, its margins and its header, follow FS: the
#: title (15 pt) at the shared size (style.font_size); the figure widens
#: by as much, so the text is bigger against it, not only in points
FS = font_size("title") / 15.0
#: the top axis' ticks and numbers above the panel, in points: the column
#: titles and the summary line are lifted above them
TOP_AXIS_PT = 10.0 + 1.3 * 9.5 * FS


# Channel tick labels.
TICK_FONTSIZE_MAX = 9.0
TICK_FONTSIZE_MIN = 5.0


# PNG resolution.
DPI = 90


# Observation counts are useful when there are not too many rows.
MAX_CHANNELS_WITH_COUNTS = 300


# For very large channel sets keep the significance circles, but omit
# the numeric confidence percentage beside every circle.
MAX_CHANNELS_WITH_CONFIDENCE = 300


# =============================================================================
# Names
# =============================================================================

GRAPHE_NOMVAR = {
    11215: "U COMPONENT OF WIND (10M)",
    11216: "V COMPONENT OF WIND (10M)",
    12004: "DRY BULB TEMPERATURE AT 2M",
    10051: "PRESSURE REDUCED TO MEAN SEA LEVEL",
    10004: "PRESSURE",
    12203: "DEW POINT DEPRESSION (2M)",
    12001: "TEMPERATURE/DRY BULB",
    11003: "U COMPONENT OF WIND",
    11004: "V COMPONENT OF WIND",
    12192: "DEW POINT DEPRESSION",
    12163: "BRIGHTNESS TEMPERATURE",
    15036: "ATMOSPHERIC REFRACTIVITY",
    11001: "WIND DIRECTION",
    11002: "WIND SPEED",
    11011: "WIND DIRECTION AT 10M",
    11012: "WIND SPEED AT 10M",
}


def varno_name(varno) -> str:
    """Return a readable variable name."""

    try:
        varno = int(varno)

    except (TypeError, ValueError):
        return str(varno)

    if varno in GRAPHE_NOMVAR:
        return GRAPHE_NOMVAR[varno]

    try:
        import pikobs

        name, units, _ = pikobs.type_varno(varno)

        return f"{name} {units}".strip()

    except Exception:
        return str(varno)


# =============================================================================
# Read statistics
# =============================================================================


def _channel_stats(
    db_file: str,
    region: str,
    flag: str,
    stn_sql: str,
    varno: int,
    land_ocean: str = "all",
    special: str = "all",
) -> Dict[float, Dict[str, float]]:
    """Mean, sigma, count and mean bias correction of every channel.

    stn_sql is the station condition of the selector (empty for join), so
    several platforms are pooled by summing their moments.
    """

    with open_result(db_file) as conn:

        rows = conn.execute(
            f"""
            SELECT
                vcoord,
                SUM(Ntot),
                SUM(s_omp),
                SUM(s2_omp),
                SUM(s_oma),
                SUM(s2_oma),
                SUM(n_bcorr),
                SUM(s_bcorr)
            FROM serie_vdedr
            WHERE
                region = ?
                AND flag = ?
                AND land_ocean = ?
                AND special = ?
                AND varno = ?{stn_sql}
            GROUP BY vcoord;
            """,
            (region, flag, land_ocean, special, int(varno)),
        ).fetchall()

    out: Dict[float, Dict[str, float]] = {}

    for vcoord, n, s_omp, q_omp, s_oma, q_oma, n_bc, s_bc in rows:

        if not n:
            continue

        n = float(n)

        stat = {"n": n}

        for tag, s, q in (("omp", s_omp, q_omp), ("oma", s_oma, q_oma)):

            if s is None:

                stat[f"avg_{tag}"] = np.nan
                stat[f"std_{tag}"] = np.nan

                continue

            mean = s / n

            var = max((q or 0.0) / n - mean * mean, 0.0)

            stat[f"avg_{tag}"] = mean
            stat[f"std_{tag}"] = np.sqrt(var)

        stat["bcorr"] = s_bc / n_bc if n_bc and s_bc is not None else np.nan

        out[float(vcoord)] = stat

    return out


# =============================================================================
# Figure dimensions
# =============================================================================


_PAIR_WHERE = ("region = ? AND flag = ? AND land_ocean = ? AND special = ? AND varno = ?")


def _pair_args(task):
    return (task["region"], task["flag"], task.get("land_ocean", "all"),
            task.get("special", "all"), int(task["varno"]))


def _pair_channel_stats(task, stn_sql):
    """MATCH on: the statistics of the control and of the experiment per
    channel, both from the pairs -- the keys of _channel_stats, so every
    figure draws them as it draws each run's own."""
    path = task.get("db_pairs")
    if not path or not os.path.isfile(path):
        return None
    with open_result(path) as conn:
        rows = conn.execute(
            "SELECT vcoord, SUM(n_omp), SUM(sx_omp), SUM(sxx_omp), SUM(sy_omp), SUM(syy_omp), "
            "SUM(n_oma), SUM(sx_oma), SUM(sxx_oma), SUM(sy_oma), SUM(syy_oma), "
            "SUM(nx_bcorr), SUM(sx_bcorr), SUM(ny_bcorr), SUM(sy_bcorr) "
            f"FROM pairs_vdedr WHERE {_PAIR_WHERE}{stn_sql} GROUP BY vcoord;",
            _pair_args(task)).fetchall()

    def _m_s(n, s1, s2):
        if not n or s1 is None:
            return np.nan, np.nan
        m = s1 / n
        return m, float(np.sqrt(max((s2 or 0.0) / n - m * m, 0.0)))

    ctl, exp = {}, {}
    for (v, n, sx, sxx, sy, syy, na, sxa, sxxa, sya, syya, nbx, sbx, nby, sby) in rows:
        if not n:
            continue
        for out, (s1, s2, a1, a2, nb, sb) in ((ctl, (sx, sxx, sxa, sxxa, nbx, sbx)),
                                             (exp, (sy, syy, sya, syya, nby, sby))):
            mo, so = _m_s(n, s1, s2)
            ma, sa = _m_s(na, a1, a2)
            out[float(v)] = {"n": float(n), "avg_omp": mo, "std_omp": so, "avg_oma": ma,
                             "std_oma": sa, "bcorr": (sb / nb) if nb and sb is not None else np.nan}
    return (ctl, exp) if ctl else None


def _channel_cycle_tests(task, stn_sql, channels):
    """MATCH on: the cycle block bootstrap of every channel -- the change of
    each cycle (cycles of at least BOOT_MIN_PAIRS pairs) of the bias of O-P,
    the sigma of O-P and the sigma of O-A. NaN where a channel has fewer
    cycles than the bootstrap tests; the cycles of each channel beside."""
    conf = {k: np.full(len(channels), np.nan) for k in ("omp_bias", "omp_rel", "oma_rel")}
    n_cyc = np.zeros(len(channels), int)
    with open_result(task["db_pairs"]) as conn:
        rows = conn.execute(
            "SELECT date, vcoord, SUM(n_omp), SUM(sx_omp), SUM(sxx_omp), SUM(sy_omp), SUM(syy_omp), "
            "SUM(n_oma), SUM(sx_oma), SUM(sxx_oma), SUM(sy_oma), SUM(syy_oma) "
            f"FROM pairs_vdedr WHERE {_PAIR_WHERE}{stn_sql} GROUP BY date, vcoord;",
            _pair_args(task)).fetchall()
    where = {float(c): i for i, c in enumerate(channels)}
    per: Dict[int, list] = {}
    for r in rows:
        i = where.get(float(r[1]))
        if i is not None:
            per.setdefault(i, []).append([np.nan if v is None else float(v) for v in r[2:]])
    rows_of = {"omp_bias": ([], []), "omp_rel": ([], []), "oma_rel": ([], [])}
    for i, k in per.items():
        k = np.asarray(k)
        ok = k[:, 0] >= BOOT_MIN_PAIRS
        n_cyc[i] = int(ok.sum())
        if ok.any():
            bias, d_sig = cycle_changes(k[ok, 0], k[ok, 1], k[ok, 2], None, k[ok, 3], k[ok, 4])
            for key, series in (("omp_bias", bias), ("omp_rel", d_sig)):
                rows_of[key][0].append(i)
                rows_of[key][1].append(series)
        oka = np.isfinite(k[:, 5]) & (k[:, 5] >= BOOT_MIN_PAIRS)
        if oka.any():
            _, d_sig_a = cycle_changes(k[oka, 5], k[oka, 6], k[oka, 7], None, k[oka, 8], k[oka, 9])
            rows_of["oma_rel"][0].append(i)
            rows_of["oma_rel"][1].append(d_sig_a)
    for key, (idx, series) in rows_of.items():
        if idx:
            # every channel at once: the same confidences, ten times faster
            conf[key][idx] = cycle_bootstrap_many(padded_rows(series))
    conf["_cycles"] = n_cyc
    return conf


def _figure_size(n_channels: int) -> Tuple[float, float]:
    """Figure size adapted to the number of channels."""

    # wider by FS: the text grows against the figure as well. The panel
    # takes at least 8 in, or 0.3 in per channel; the header and the foot
    # come on top, in the same scale as the text
    panel = min(max(8.0, 0.30 * n_channels), PANEL_MAX_IN)
    return FIGURE_WIDTH * FS, min(panel + (TOP_ROOM + 0.80) * FS, MAX_HEIGHT)


def _tick_fontsize(n_channels: int, fig_height: float) -> float:
    """Largest readable channel font for the available vertical space."""

    if n_channels <= 0:
        return TICK_FONTSIZE_MAX * FS

    # the panel's own height: the figure less its header and its foot
    plot_height = max(fig_height - (TOP_ROOM + 0.80) * FS, 1.0)

    inch_per_row = plot_height / n_channels

    points = inch_per_row * 72.0 / 1.35

    return float(np.clip(points, TICK_FONTSIZE_MIN, TICK_FONTSIZE_MAX * FS))


# =============================================================================
# Public plotting entry point
# =============================================================================


def _land_special(task, sep="_") -> str:
    """The land filter and the special value, only when there is one: a
    run without them keeps its file names and its titles."""
    bits = []
    if task.get("land_ocean", "all") not in (None, "", "all"):
        bits.append(str(task["land_ocean"]))
    if task.get("special_label", "all") not in (None, "", "all"):
        bits.append(str(task["special_label"]))
    if sep == "_":
        return "".join(f"_{_safe(b)}" for b in bits)
    return "".join(f"{sep}{b}" for b in bits)


def vdedr_plot_task(task: Dict[str, Any]) -> Optional[List[Dict[str, str]]]:
    """Draw the three figures of one selection; returns their paths."""

    try:
        return _plot(task)

    except Exception:

        print(
            f"[vdedr] plot failed for "
            f"{task.get('family')} "
            f"{task.get('id_stn')} "
            f"varno {task.get('varno')}:\n"
            f"{traceback.format_exc()}",
            flush=True,
        )

        plt.close("all")

        return None


# =============================================================================
# Main plot
# =============================================================================

# The columns at the right of the axes, in axes fraction:
#
#       sigma test    Confidence    N control    N experience
#         ○         99.7%         18976          28196
CIRCLE_X = 1.015
CONF_X = 1.085
N_CTL_X = 1.220
N_EXP_X = 1.350


def _column_reader(channels):
    """col(stats, key): one value per channel, in the order of `channels`."""

    def col(src, key):

        return np.array([src[c][key] for c in channels], dtype=float)

    return col


def _read_runs(task):
    """The statistics of the control and the experiment, per channel, and
    the channels both have (None when they share none)."""

    stn_sql = task.get("stn_sql", "")

    ctl = _channel_stats(
        task["files_in"][0],
        task["region"],
        task["flag"],
        stn_sql,
        task["varno"],
        task.get("land_ocean", "all"),
        task.get("special", "all"),
    )

    exp = _channel_stats(
        task["files_in"][1],
        task["region"],
        task["flag"],
        stn_sql,
        task["varno"],
        task.get("land_ocean", "all"),
        task.get("special", "all"),
    )

    channels = sorted(set(ctl) & set(exp))   # small channels at the bottom, large at the top

    if not channels:
        return None

    return ctl, exp, channels, stn_sql


def _series(ctl, exp, col, n1, n2):
    """The two curves of each of the three figures."""

    with np.errstate(divide="ignore", invalid="ignore"):

        series = {
            "omp_bias": (
                col(exp, "avg_omp") - col(ctl, "avg_omp"),
                (col(exp, "avg_omp") - col(exp, "bcorr"))
                - (col(ctl, "avg_omp") - col(ctl, "bcorr")),
            ),
            "omp_rel": (
                100.0 * (col(exp, "std_omp") - col(ctl, "std_omp")) / col(ctl, "std_omp"),
                100.0 * (n2 - n1) / n1,
            ),
            "oma_rel": (
                100.0 * (col(exp, "std_oma") - col(ctl, "std_oma")) / col(ctl, "std_oma"),
                100.0 * (n2 - n1) / n1,
            ),
        }

    return series


def _tests(task, stn_sql, channels, ctl, exp, col, n1, n2):
    """MATCH off: each channel tested on each run's own moments -- the
    t-test on the bias, the F-test on the sigma -- and, for the bias,
    which run is closer to zero. (MATCH on is _channel_cycle_tests.)"""

    conf = {
        "omp_rel": sigma_confidence(
            np.square(col(ctl, "std_omp")), np.square(col(exp, "std_omp")), n1, n2),
        "oma_rel": sigma_confidence(
            np.square(col(ctl, "std_oma")), np.square(col(exp, "std_oma")), n1, n2),
        "omp_bias": ttest_confidence(
            col(ctl, "avg_omp"), col(ctl, "std_omp"), n1,
            col(exp, "avg_omp"), col(exp, "std_omp"), n2),
    }
    # for the bias, winner means the run whose mean is closer to zero
    winner = {"omp_bias": np.abs(col(exp, "avg_omp")) - np.abs(col(ctl, "avg_omp"))}
    return None, conf, winner


def _columns(n1, n2, tick_fs, test_name="bootstrap"):
    """The room right of the panel, in inches: the test circle, then one
    column of counts (MATCH on: the pairs) or two, each as wide as the
    longest count of the figure, a fixed gap between them -- close to the
    test, never running into each other, whatever the counts."""
    vals = np.concatenate([np.asarray(n1, float), np.asarray(n2, float)])
    vals = vals[np.isfinite(vals)]
    digits = max(len(f"{int(v)}") for v in vals) if vals.size else 5
    n_cols = 1 if n1 is n2 else 2
    head_fs = 8.2 * FS                                         # the column titles
    title = "N pairs" if n_cols == 1 else "N Ctl"
    # a column is as wide as its longest number or its title
    num_in = max(digits * 0.62 * tick_fs, len(title) * 0.66 * head_fs) / 72.0
    circle_in, gap_in = 0.35, 0.45
    # the test's title is centred on the circle: the first column starts past it
    test_half_in = 0.5 * len(test_name) * 0.66 * head_fs / 72.0
    first_in = circle_in + max(0.25, test_half_in) + gap_in + num_in / 2.0
    right_in = first_in + (n_cols - 1) * (num_in + gap_in) + num_in / 2.0 + 0.5
    return {"circle_in": circle_in, "first_in": first_in, "step_in": num_in + gap_in,
            "num_in": num_in, "n_cols": n_cols, "right_in": right_in}


def _place_columns(ax, fig_w, cols) -> None:
    """The columns of a figure in axes fractions, kept on the axes."""
    axw = ax.get_position().width * fig_w
    ctl = 1.0 + cols["first_in"] / axw
    exp = ctl + cols["step_in"] / axw
    last = exp if cols["n_cols"] == 2 else ctl
    ax._pikobs_cols = {"circle": 1.0 + cols["circle_in"] / axw, "ctl": ctl, "exp": exp,
                       "right": last + 0.5 * cols["num_in"] / axw}


def _col(ax, name):
    """A column position of this figure (the old fixed ones as a fallback)."""
    fixed = {"circle": CIRCLE_X, "ctl": N_CTL_X, "exp": N_EXP_X, "right": N_EXP_X + 0.025}
    return getattr(ax, "_pikobs_cols", fixed)[name]


def _new_figure(fig_w, fig_h, right_in=None):
    """The figure and its axes, with fixed physical margins."""

    fig, ax = plt.subplots(figsize=(fig_w, fig_h), facecolor="white")

    ax.set_facecolor("#fcfcfc")

    # Fixed physical margins.
    left_in = 0.95 * FS

    # A little more room than before for:
    #
    # sigma test | Confidence | N control | N experience
    right_in = right_in if right_in is not None else 3.00 * FS

    top_in = TOP_ROOM * FS
    bottom_in = 0.80 * FS

    fig.subplots_adjust(
        left=left_in / fig_w,
        right=1.0 - right_in / fig_w,
        top=1.0 - top_in / fig_h,
        bottom=bottom_in / fig_h,
    )

    return fig, ax, left_in


def _background(ax, idlev):
    """Bands every other channel, the grid, the zero line, the frame."""

    for y in idlev[::2]:

        ax.axhspan(y - 0.5, y + 0.5, color=BAND, zorder=0)

    ax.grid(True, axis="x", linestyle=":", linewidth=0.65, color="#a0a0a0", alpha=0.48, zorder=1)

    ax.set_axisbelow(True)

    ax.axvline(0.0, color="#404040", lw=1.15, alpha=0.85, zorder=2)

    for spine in ax.spines.values():

        spine.set_color("#555555")

        spine.set_linewidth(0.75)


def _draw_series(ax, metric, first, second, idlev, legend):
    """The metric (coloured by which run is better) and its second curve."""

    signed = metric in ("omp_rel", "oma_rel")

    ax.plot(
        first,
        idlev,
        linestyle="-",
        linewidth=1.45,
        zorder=3,
        color=(NEUTRAL_LINE if signed else NEUTRAL_LINE),
        label=(f"{legend[0]}  (red: Exp better, blue: Ctl better)" if signed else legend[0]),
    )

    if signed:

        # Negative -> experiment better -> red.
        ax.plot(
            np.where(first < 0, first, np.nan),
            idlev,
            linestyle="none",
            marker="o",
            markersize=5.0,
            markeredgewidth=0.0,
            color=EXP_BETTER,
            zorder=4,
            label="_nolegend_",
        )

        # Positive -> control better -> blue.
        ax.plot(
            np.where(first > 0, first, np.nan),
            idlev,
            linestyle="none",
            marker="o",
            markersize=5.0,
            markeredgewidth=0.0,
            color=CTL_BETTER,
            zorder=4,
            label="_nolegend_",
        )

    else:

        ax.plot(
            first,
            idlev,
            linestyle="none",
            marker="o",
            markersize=4.8,
            markeredgewidth=0.0,
            color=NEUTRAL_LINE,
            zorder=4,
        )

    # Nobs / second metric, on its own axis on top: its scale is not the
    # sigma's (a few % against up to 100 %), one of them was squashed. With
    # MATCH on, the share of each run's observations that is matched, one
    # curve per run in its colour
    matched = isinstance(second, tuple)
    curves = ([(second[0], CTL_COLOUR, "% of Ctl matched"), (second[1], EXP_COLOUR, "% of Exp matched")]
              if matched else [(second, COULEURS[3], legend[1])])
    top = ax.twiny()
    ax._pikobs_top = top
    every = np.concatenate([np.asarray(v, float).ravel() for v, _, _ in curves])
    every = every[np.isfinite(every)]
    if matched:                         # a share: up to 100 %
        low = float(np.nanmin(every)) if every.size else 0.0
        top.set_xlim(max(0.0, np.floor(low / 10.0) * 10.0 - 5.0), 102.0)
    else:                               # a change: around 0, as the sigma's
        lim = float(np.nanmax(np.abs(every))) * 1.12 if every.size else 1.0
        top.set_xlim(-max(lim, 1e-6), max(lim, 1e-6))
    if signed:
        # the sigma's change around 0 too: both zeros in the middle, one line
        f = np.asarray(first, float)
        f = f[np.isfinite(f)]
        lim_b = float(np.nanmax(np.abs(f))) * 1.12 if f.size else 1.0
        ax.set_xlim(-max(lim_b, 1e-6), max(lim_b, 1e-6))
    top_colour = MATCHED_AXIS_COLOUR if matched else NOBS_AXIS_COLOUR
    top.set_xlabel(f"{legend[1]}  (blue Ctl, red Exp)" if matched else legend[1],
                   fontsize=12 * FS, fontweight="bold", labelpad=8, color=top_colour)
    top.tick_params(axis="x", labelsize=9.5 * FS, length=6, width=1.6, pad=4, colors=top_colour)
    top.spines["top"].set_color(top_colour)
    top.spines["top"].set_linewidth(1.8)
    for label in top.get_xticklabels():
        label.set_fontweight("bold")
    for values, colour, label in curves:
        top.plot(
            values,
            idlev,
            linestyle="-",
            marker="o",
            color=colour,
            markersize=3.6,
            markeredgewidth=0.0,
            linewidth=1.35,
            zorder=3,
            label=label,
        )


def _channel_axis(ax, channels, idlev, tick_fs, legend, step: int = 1):
    """One tick per channel -- one in ``step`` when the figure is dense --
    and the axis labels."""

    ax.set_yticks(idlev[::step])

    ax.set_yticklabels([f"{c:g}" for c in list(channels)[::step]], fontsize=tick_fs)

    ax.set_ylim(idlev[0] - 0.5, idlev[-1] + 0.5)

    ax.tick_params(axis="y", pad=5, length=2.5, width=0.6, labelcolor="#202020")

    ax.tick_params(axis="x", labelsize=9.5 * FS, length=6, width=1.2, pad=6)

    ax.set_ylabel("Channel", fontsize=12 * FS, fontweight="semibold", color="#202020", labelpad=11)

    ax.set_xlabel(legend[0], fontsize=12 * FS, fontweight="bold", labelpad=8, color=SIGMA_AXIS_COLOUR)
    ax.tick_params(axis="x", colors=SIGMA_AXIS_COLOUR, width=1.6)
    ax.spines["bottom"].set_color(SIGMA_AXIS_COLOUR)
    ax.spines["bottom"].set_linewidth(1.8)
    for label in ax.get_xticklabels():
        label.set_fontweight("bold")


def _summary_line(ax, pieces) -> None:
    """The line above the test and count columns, its pieces in their
    colours, right-aligned on the counts, placed from right to left."""
    fig = ax.figure
    renderer = fig.canvas.get_renderer()
    lift = mtransforms.ScaledTranslation(0, (34.0 + TOP_AXIS_PT) / 72.0, fig.dpi_scale_trans)
    x = _col(ax, "right")
    for text, colour, weight in reversed(pieces):
        t = ax.text(x, 1.0, text, transform=ax.transAxes + lift, ha="right", va="bottom",
                    fontsize=9.0 * FS, fontweight=weight, color=colour, clip_on=False)
        box = t.get_window_extent(renderer=renderer)
        gap = 0.45 * 9.0 * FS * fig.dpi / 72.0               # a space between pieces
        x = ax.transAxes.inverted().transform((box.x0 - gap, box.y0))[0]


def _test_lines(ax, c_vals, sign, idlev):
    """A dense figure: the test of each channel as a short horizontal line in
    the test column -- red (Exp better) or blue (Ctl better) when it passes,
    thin grey when it does not, lighter and thinner when not tested -- as in
    profile: circles would pile up into a column. Drawn as line-shaped
    markers, which the tight frame of the saved image takes into account."""
    c_vals = np.asarray(c_vals, float)
    sign = np.asarray(sign, float)
    y = np.asarray(idlev)
    tested = np.isfinite(c_vals)
    sig = tested & (np.nan_to_num(c_vals) > MIN_CONFIDENCE)
    long_pt = 0.55 * 72.0                                    # the length of a line
    for keep, colour, width in (
            (sig & (sign <= 0), EXP_BETTER, 2.6 * FS),
            (sig & (sign > 0), CTL_BETTER, 2.6 * FS),
            (tested & ~sig, "#B8BEC5", 0.9 * FS),
            (~tested, "#D5D9DE", 0.7 * FS)):
        if np.any(keep):
            ax.scatter(np.full(int(keep.sum()), _col(ax, "circle")), y[keep], s=long_pt ** 2,
                       marker="_", color=colour, linewidths=width, zorder=5, clip_on=False,
                       transform=ax.get_yaxis_transform())
    # the saved image is cut to its texts, not to markers outside the panel:
    # an invisible one just right of the column keeps the lines in it
    ax.text(_col(ax, "circle") + 0.03, y[0] if len(y) else 0, "M", alpha=0.0,
            fontsize=10 * FS, va="center", transform=ax.get_yaxis_transform())


def _draw_confidence(ax, metric, conf, winner, first, channels, idlev, tick_fs, dense=False):
    """The test of each channel as a short line, and the summary above."""

    c_vals = conf.get(metric)

    if c_vals is not None:

        cycles = conf.get("_cycles")
        test_name = ("bootstrap" if cycles is not None
                     else "t-test" if metric == "omp_bias" else "F-test")
        show_confidence_value = False

        # every figure the same way, few channels or many: a short line per
        # channel -- red or blue when it passes, grey when it does not,
        # lighter when not tested; the channel's counts and test are under
        # the mouse in the viewer
        _test_lines(ax, c_vals, winner.get(metric, first), idlev)

        # -----------------------------------------------------------------
        # Test summary
        # -----------------------------------------------------------------

        sig = np.nan_to_num(c_vals) > MIN_CONFIDENCE
        side = winner.get(metric, first)
        n_better = int(np.nansum(sig & (side < 0)))
        n_worse = int(np.nansum(sig & (side > 0)))
        # one line, read at a glance: what passed the test in its colour,
        # a zero in grey, how many channels were tested at all
        _summary_line(ax, [
            (f"Exp better {n_better}", EXP_BETTER if n_better else "#9AA0A6", "bold"),
            ("\u00b7", "#9AA0A6", "normal"),
            (f"Ctl better {n_worse}", CTL_BETTER if n_worse else "#9AA0A6", "bold"),
        ])

        # -----------------------------------------------------------------
        # Column headers
        # -----------------------------------------------------------------

        ax.annotate(
            test_name,
            xy=(_col(ax, "circle"), 1.0),
            xycoords="axes fraction",
            xytext=(0, 14 + TOP_AXIS_PT),
            textcoords="offset points",
            fontsize=8.2 * FS,
            fontweight="bold",
            color="#303030",
            ha="center",
        )

        if show_confidence_value:

            ax.annotate(
                "conf.",
                xy=(CONF_X, 1.0),
                xycoords="axes fraction",
                xytext=(0, 14 + TOP_AXIS_PT),
                textcoords="offset points",
                fontsize=8.2 * FS,
                fontweight="bold",
                color="#303030",
                ha="center",
            )


def _draw_counts(ax, channels, idlev, n1, n2, tick_fs):
    """The number of observations of each run, per channel; with MATCH on
    (n1 is n2: the pairs) one column, the pairs both runs share."""

    if len(channels) <= MAX_CHANNELS_WITH_COUNTS and n1 is n2:
        x = _col(ax, "ctl")
        ax.annotate("N pairs", xy=(x, 1.0), xycoords="axes fraction", xytext=(0, 14 + TOP_AXIS_PT),
                    textcoords="offset points", fontsize=8.2 * FS, fontweight="bold",
                    color="#30343A", ha="center")
        for y in idlev:
            ax.text(x, y, f"{int(n1[y])}", fontsize=tick_fs, color="#30343A", va="center",
                    ha="center", transform=ax.get_yaxis_transform())
        return

    if len(channels) <= MAX_CHANNELS_WITH_COUNTS:

        # -----------------------------------------------------------------
        # Column headers
        # -----------------------------------------------------------------

        ax.annotate(
            "N Ctl",
            xy=(_col(ax, "ctl"), 1.0),
            xycoords="axes fraction",
            xytext=(0, 14 + TOP_AXIS_PT),
            textcoords="offset points",
            fontsize=8.2 * FS,
            fontweight="bold",
            color=CTL_COLOUR,
            ha="center",
        )

        ax.annotate(
            "N Exp",
            xy=(_col(ax, "exp"), 1.0),
            xycoords="axes fraction",
            xytext=(0, 14 + TOP_AXIS_PT),
            textcoords="offset points",
            fontsize=8.2 * FS,
            fontweight="bold",
            color=EXP_COLOUR,
            ha="center",
        )

        # -----------------------------------------------------------------
        # Count values
        # -----------------------------------------------------------------

        for y in idlev:

            ax.text(
                _col(ax, "ctl"),
                y,
                f"{int(n1[y])}",
                fontsize=tick_fs,
                color=CTL_COLOUR,
                va="center",
                ha="center",
                transform=ax.get_yaxis_transform(),
            )

            ax.text(
                _col(ax, "exp"),
                y,
                f"{int(n2[y])}",
                fontsize=tick_fs,
                color=EXP_COLOUR,
                va="center",
                ha="center",
                transform=ax.get_yaxis_transform(),
            )


def _draw_header(fig, task, metric, fig_w, fig_h, left_in, name1, name2, pairs):
    """Title, period, selection, the two runs and the MATCH line."""

    def at(inch):
        return 1.0 - inch * FS / fig_h

    def _when(stamp) -> str:
        s = str(stamp)
        return f"{s[:4]}-{s[4:6]}-{s[6:8]} {s[8:10]} UTC"

    what = {"omp_bias": "bias of O-P", "omp_rel": "sigma of O-P", "oma_rel": "sigma of O-A"}.get(
        metric, metric
    )
    x0, grey = left_in / fig_w, "#5F6B76"
    fig.text(
        x0,
        at(0.12),
        f"{varno_name(task['varno'])}  \u00b7  {what}",
        ha="left",
        va="top",
        fontsize=15 * FS,
        fontweight="bold",
        color="#1F2933",
    )
    fig.text(
        x0,
        at(0.45),
        "  \u00b7  ".join(
            [
                f"{_when(task['datestart'])} to {_when(task['dateend'])}",
                task["family"],
                f"{task['region']}{_land_special(task, ', ')}",
                f"flag {task['flag']}",
                f"platforms {task['id_stn']}",
            ]
        ),
        ha="left",
        va="top",
        fontsize=11 * FS,
        color=grey,
    )
    t = fig.text(
        x0,
        at(0.72),
        f"Ctl  {name1}",
        ha="left",
        va="top",
        fontsize=13 * FS,
        fontweight="bold",
        color=CTL_COLOUR,
    )
    box = t.get_window_extent(renderer=fig.canvas.get_renderer())
    fig.text(
        fig.transFigure.inverted().transform((box.x1, box.y0))[0] + 0.02,
        at(0.72),
        f"Exp  {name2}",
        ha="left",
        va="top",
        fontsize=13 * FS,
        fontweight="bold",
        color=EXP_COLOUR,
    )
    fig.add_artist(
        plt.Line2D(
            [x0, 0.985],
            [at(1.24), at(1.24)],
            transform=fig.transFigure,
            color="#D9DDE2",
            linewidth=0.9,
        )
    )
    if task.get("match_mode") != "no":            # MATCH no: no badge at all
        match_badge(fig, task.get("match_mode") == "on", top_in=0.12 * FS)


def _draw_legend(fig, ax, fig_h):
    """The legend of the curves, under the header."""

    handles, labels = ax.get_legend_handles_labels()
    top = getattr(ax, "_pikobs_top", None)
    if top is not None:                 # the second curve, on the top axis
        h2, l2 = top.get_legend_handles_labels()
        handles, labels = handles + h2, labels + l2

    if handles:

        legend_y = 1.0 - 1.50 * FS / fig_h

        fig.legend(
            handles,
            labels,
            loc="upper left",
            bbox_to_anchor=(ax.get_position().x0, legend_y),
            bbox_transform=fig.transFigure,
            ncol=min(3, len(handles)),   # rows, not one long line: the summary is on the right
            fontsize=11.0 * FS,
            frameon=False,
            columnspacing=1.6,
            handletextpad=0.5,
            handlelength=2.0,
            borderaxespad=0.0,
        )


def _hover_rows(channels, idlev, n1, n2, c_vals, cycles, test_name):
    """What the viewer names under the mouse, channel by channel: the
    channel, its counts, its test."""
    rows = []
    two = n1 is not n2
    for i, (y, c) in enumerate(zip(idlev, channels)):
        parts = [f"{c:g}"]
        a = n1[i] if n1 is not None and i < len(n1) else np.nan
        b = n2[i] if two and n2 is not None and i < len(n2) else np.nan
        if np.isfinite(a):
            parts.append(f"N {int(a):,}" + (f" / {int(b):,}" if two and np.isfinite(b) else ""))
        if c_vals is not None and test_name:
            v = c_vals[i]
            if np.isfinite(v):
                parts.append(f"{test_name} {v:.0f} %")
            elif cycles is not None:
                parts.append(f"not tested ({int(cycles[i])} cycles)")
        rows.append((y, "  ·  ".join(parts)))
    return rows


def _save(fig, task, metric, name1, name2, ax=None, hover=None):
    """Write the figure, and beside it what the viewer names under the
    mouse; returns its entry for the viewer."""

    rel = os.path.join(
        task["family"],
        (
            f"{metric}_"
            f"{_safe(task['family'])}_"
            f"{_safe(task.get('stn_tag', task['id_stn']))}_"
            f"{_safe(name1)}-{_safe(name2)}_"
            f"{_safe(task['region'])}{_land_special(task)}_"
            f"{_safe(task['flag'])}_"
            f"varno{int(task['varno'])}"
            f"{('_match' + task['match_mode']) if task.get('match_mode') in ('off', 'no') else ''}.png"
        ),
    )

    path = os.path.join(task["pathwork"], rel)

    os.makedirs(os.path.dirname(path), exist_ok=True)

    from pikobs.figures.figures import members_footer
    members_footer(fig, task.get('selector'))
    save_figure(fig, path, svg=task.get("svg", False), dpi=DPI)
    if ax is not None and hover:
        write_hover(fig, path, ax, hover, word="channel", dpi=DPI)

    plt.close(fig)

    return {"metric": metric, "filename": rel}


def _metric_figure(
    task, metric, first, second, channels, idlev, n1, n2, conf, winner, pairs, name1, name2
):
    """One figure: one metric, every channel."""

    legend = METRICS[metric][1]
    if task.get("match_mode") == "on" and metric.endswith("_rel"):
        legend = (legend[0], "% matched")   # MATCH on: the share matched, not % Nobs
    fig_w, fig_h = _figure_size(len(channels))
    # dense: more channels than fit at 0.3 in a row -- one name in k at the
    # usual size, thin test lines, the counts under the mouse
    dense = 0.30 * len(channels) > PANEL_MAX_IN
    tick_fs = TICK_FONTSIZE_MAX * FS if dense else _tick_fontsize(len(channels), fig_h)
    test_name = ("" if not conf else "bootstrap" if "_cycles" in conf else
                 ("t-test" if metric == "omp_bias" else "F-test"))

    cols = _columns(n1, n2, tick_fs, test_name)
    fig, ax, left_in = _new_figure(fig_w, fig_h, cols["right_in"])
    _place_columns(ax, fig_w, cols)
    _background(ax, idlev)
    _draw_series(ax, metric, first, second, idlev, legend)
    for line in ax.get_lines():           # as thick as the text is big
        line.set_linewidth(line.get_linewidth() * 1.8)
        line.set_markersize(line.get_markersize() * 1.8)
    step = 1
    if dense:
        row_pt = ax.get_position().height * fig_h * 72.0 / max(len(channels), 1)
        step = max(1, int(np.ceil(1.5 * tick_fs / max(row_pt, 1e-6))))
    _channel_axis(ax, channels, idlev, tick_fs, legend, step)
    _draw_confidence(ax, metric, conf, winner, first, channels, idlev, tick_fs, dense)
    # the counts of the channels named on the axis, at their height; a dense
    # figure's other channels have theirs under the mouse
    _draw_counts(ax, list(channels)[::step], np.asarray(idlev)[::step], n1, n2, tick_fs)
    _draw_header(fig, task, metric, fig_w, fig_h, left_in, name1, name2, pairs)
    _draw_legend(fig, ax, fig_h)
    hover = _hover_rows(channels, idlev, n1, n2, conf.get(metric) if conf else None,
                        conf.get("_cycles") if conf else None, test_name)
    return _save(fig, task, metric, name1, name2, ax, hover)


def _plot(task: Dict[str, Any]) -> Optional[List[Dict[str, str]]]:
    """The three figures of one selection: bias of O-P, sigma of O-P and
    sigma of O-A, control against experiment, channel by channel."""

    read = _read_runs(task)
    if read is None:
        return None
    ctl, exp, channels, stn_sql = read
    name1, name2 = task["names_in"]

    if task.get("match_mode") == "on":
        # MATCH on: both runs from their pairs, every figure; the second
        # curve of the sigma figures is the share of each run's observations
        # that is matched, and every channel is tested by the cycle block
        # bootstrap
        ctl_all, exp_all = ctl, exp
        pair = _pair_channel_stats(task, stn_sql)
        if pair is None:
            return None
        ctl, exp = pair
        channels = sorted(set(ctl) & set(exp))   # small channels at the bottom, large at the top
        if not channels:
            return None
        idlev = np.arange(len(channels))
        col = _column_reader(channels)
        n1 = n2 = col(ctl, "n")
        series = _series(ctl, exp, col, n1, n2)
        with np.errstate(divide="ignore", invalid="ignore"):
            share = (100.0 * n1 / col(ctl_all, "n"), 100.0 * n1 / col(exp_all, "n"))
        for metric in ("omp_rel", "oma_rel"):
            series[metric] = (series[metric][0], share)
        conf = _channel_cycle_tests(task, stn_sql, channels)
        winner = {"omp_bias": np.abs(col(exp, "avg_omp")) - np.abs(col(ctl, "avg_omp"))}
        pairs = None
    else:
        # MATCH off: each run with all its observations, Welch and F;
        # MATCH no: the same runs, and no test
        idlev = np.arange(len(channels))
        col = _column_reader(channels)
        n1 = col(ctl, "n")
        n2 = col(exp, "n")
        series = _series(ctl, exp, col, n1, n2)
        if task.get("match_mode") == "no":
            pairs, conf, winner = None, {}, {}
        else:
            pairs, conf, winner = _tests(dict(task, db_pairs=None), stn_sql, channels, ctl, exp,
                                         col, n1, n2)

    return [
        _metric_figure(
            task, metric, first, second, channels, idlev, n1, n2, conf, winner, pairs, name1, name2
        )
        for metric, (first, second) in series.items()
    ]


# =============================================================================
# Viewer
# =============================================================================


def vdedr_viewer_items(
    tasks: Sequence[Dict[str, Any]], results: Sequence[Any]
) -> List[Dict[str, str]]:
    """One viewer entry per figure actually written."""

    items: List[Dict[str, str]] = []

    for task, res in zip(tasks, results):

        if not res:
            continue

        for fig in res:

            items.append(
                {
                    "comparison": task["comparison"],
                    "metric": fig["metric"],
                    "family": str(task["family"]).strip(),
                    "region": str(task["region"]).strip(),
                    "land_ocean": str(task.get("land_ocean", "all")),
                    "special": str(task.get("special_label", "all")),
                    "flag": str(task["flag"]).strip(),
                    "id_stn": str(task["id_stn"]).strip(),
                    "varno": str(task["varno"]).strip(),
                    "match": task.get("match_mode", ""),
                    "filename": fig["filename"],
                }
            )

    return items
