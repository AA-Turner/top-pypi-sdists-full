#!/usr/bin/python3
"""Figures of pikobs.cardio.

Four synchronised panels per figure: mean departures, sigma, physical
values and counts. Everything is derived from the sums written by the
extraction, so a figure can merge stations or channels exactly.
"""

import json
import math
import os
import random
from datetime import datetime
from typing import Any, Dict, Optional

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.transforms as mtransforms
import matplotlib.pyplot as plt
import numpy as np

import pikobs
from pikobs.figures import count_formatter, match_badge, save_figure
from pikobs.configobs.style import font_size

#: every text of a cardiogram, and the room of its header, is 'size * FS':
#: FS gives the title the shared size (style.font_size), the rest follows
FS = font_size("title") / 14.0
from pikobs.configobs.style import CTL_BETTER, CTL_COLOUR, EXP_BETTER, EXP_COLOUR, GREY_TEXT
from pikobs.obsdb import open_result
from pikobs.stats import (
    MIN_CONFIDENCE,
    is_significant,
    moments_from_sums,
    ttest_confidence,
    sigma_confidence,
)
from pikobs.obsdb import safe_name as _safe

ROUGE = "#FF9999"
ROUGEPUR = "#FF0000"
VERT = "#009900"
BLEU = "#1569C7"
NOIR = "#000000"

DPI = 110

# The comparison: the control is drawn with a solid line and the
# experience with a dashed one, so the two are told apart even in black
# and white; a circle marks the cycles where the difference passes the
# test, red when the experience wins and blue when the control does.
CTL_STYLE = "-"
EXP_STYLE = "--"
MARK_SIZE = 380              # the circles of MATCH off, as big as the text
MARK_ALPHA = 0.35


def figure_name(
    experience, flag, family, id_stn, region, chan, varno, land_ocean="all", special="all"
) -> str:
    """Name of the PNG; the viewer and the plot must agree on it. The land
    filter and the special value are in the name only when there is one,
    so a run without them keeps the names it always had."""
    from pikobs.configobs.special_family import special_label

    land = "" if land_ocean in (None, "", "all") else f"_{_safe(land_ocean)}"
    # the label of the special value, as every module (IR_channel, 0.5)
    land += "" if special in (None, "", "all") else f"_{_safe(special_label(family, special))}"
    return (
        f"serie_{_safe(experience)}_{_safe(flag)}_{_safe(family)}_"
        f"{_safe(id_stn)}_id_stn_{_safe(region)}{land}_ch{_safe(chan)}_"
        f"varno{_safe(varno)}.png"
    )


def parse_flexible_date(date_str: str) -> datetime:
    date_str = str(date_str).strip()
    for fmt in ("%Y%m%d%H", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%Y%m%d"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"The date format '{date_str}' is unknown.")


def get_smart_limit(
    pathwork: str, region: str, family: str, channel: str, panel_id: str, current_data_max: float
) -> float:
    """Y limit shared by every figure of a region, so they compare.

    One file per region; a larger limit replaces a smaller one, which keeps
    the panels of different criteria and experiences on the same scale.
    """
    config_file = os.path.join(pathwork, f"y_limits_{_safe(region)}.json")
    limits: Dict[str, Any] = {}
    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as fh:
                limits = json.load(fh)
        except (json.JSONDecodeError, IOError):
            limits = {}

    limits.setdefault(family, {})
    chan_key = f"ch_{channel}"
    if not isinstance(limits[family].get(chan_key), dict):
        limits[family][chan_key] = {}

    if current_data_max <= 0 or not np.isfinite(current_data_max):
        calculated = 1.0
    else:
        order = 10 ** int(math.log10(current_data_max))
        step = order / 2 if order >= 10 else 0.1
        calculated = float(math.ceil(current_data_max / step) * step * 1.15)

    existing = limits[family][chan_key].get(panel_id, 0.0)
    if calculated <= existing:
        return existing

    limits[family][chan_key][panel_id] = calculated
    tmp = f"{config_file}.tmp.{os.getpid()}.{random.randint(0, 10000)}"
    try:
        with open(tmp, "w") as fh:
            json.dump(limits, fh, indent=4)
        os.replace(tmp, config_file)
    except Exception:
        if os.path.exists(tmp):
            os.remove(tmp)
    return calculated


def _series(
    task: Dict[str, Any], db_file: Optional[str] = None
) -> Optional[Dict[str, np.ndarray]]:
    """Per-cycle statistics of one selection, from the stored sums."""
    db_file = db_file or task["db_file"]
    where = ["region = ?", "flag = ?", "land_ocean = ?", "special = ?", "varno = ?"]
    args = [
        task["region"],
        task["flag_criteria"],
        task.get("land_ocean", "all"),
        task.get("special", "all"),
        task["varno"],
    ]
    if str(task["vcoord"]) != "join":
        where.append("Chan = ?")
        args.append(task["vcoord"])
    clause = " AND ".join(where) + task.get("stn_sql", "")

    with open_result(db_file) as conn:
        rows = conn.execute(
            f"""
            SELECT date, SUM(Nrej), SUM(Nacc), SUM(Nprofile), SUM(Nloc),
                   SUM(n_omp), SUM(s_omp), SUM(s2_omp),
                   SUM(n_oma), SUM(s_oma), SUM(s2_oma),
                   SUM(n_obs), SUM(s_obs), SUM(n_bcorr), SUM(s_bcorr),
                   MIN(min_omp), MAX(max_omp), MIN(min_oma), MAX(max_oma)
            FROM serie_cardio
            WHERE {clause}
            GROUP BY date ORDER BY date;
        """,
            args,
        ).fetchall()
    if not rows:
        return None

    arr = np.array(
        [[r[0]] + [float(v) if v is not None else np.nan for v in r[1:]] for r in rows],
        dtype=float,
    )

    def mean(n_col, s_col):
        n, s = arr[:, n_col], arr[:, s_col]
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.where(n > 0, s / n, np.nan)

    def std(n_col, s_col, q_col):
        n, s, q = arr[:, n_col], arr[:, s_col], arr[:, q_col]
        with np.errstate(divide="ignore", invalid="ignore"):
            m = np.where(n > 0, s / n, np.nan)
            return np.sqrt(np.maximum(np.where(n > 0, q / n - m * m, np.nan), 0.0))

    return {
        "dates": [str(int(d)) for d in arr[:, 0]],
        "nrej": arr[:, 1],
        "nacc": arr[:, 2],
        "nprofile": arr[:, 3],
        "nloc": arr[:, 4],
        "ndata": arr[:, 5],
        "avg_omp": mean(5, 6),
        "std_omp": std(5, 6, 7),
        "avg_oma": mean(8, 9),
        "std_oma": std(8, 9, 10),
        "avg_obs": mean(11, 12),
        "n_bcorr": arr[:, 13],
        "avg_bcorr": mean(13, 14),
        "min_omp": arr[:, 15],
        "max_omp": arr[:, 16],
        "min_oma": arr[:, 17],
        "max_oma": arr[:, 18],
    }


def _align(ref: Dict[str, np.ndarray], exp: Dict[str, np.ndarray]):
    """Keep the cycles both runs have, in order."""
    common = [d for d in exp["dates"] if d in set(ref["dates"])]
    if not common:
        return None, None
    i_ref = [ref["dates"].index(d) for d in common]
    i_exp = [exp["dates"].index(d) for d in common]

    def _take(src, idx):
        out = {"dates": common}
        for k, v in src.items():
            if k == "dates":
                continue
            out[k] = np.asarray(v)[idx]
        return out

    return _take(ref, i_ref), _take(exp, i_exp)


def _pairs(task, dates) -> Optional[Dict[str, np.ndarray]]:
    """The sums of the matched observations of this selection, per cycle.

    Returns None when the run has no pair database -- an older output, or
    a run without a control -- and the caller falls back on Welch.
    """
    path = task.get("db_pairs")
    if not path or not os.path.isfile(path):
        return None
    where = ["region = ?", "flag = ?", "land_ocean = ?", "special = ?", "varno = ?"]
    params = [
        task["region"],
        task["flag_criteria"],
        task.get("land_ocean", "all"),
        task.get("special", "all"),
        task["varno"],
    ]
    if str(task["vcoord"]) != "join":
        where.append("Chan = ?")
        params.append(task["vcoord"])
    where = " AND ".join(where) + task.get("stn_sql", "")
    try:
        with open_result(path) as conn:
            rows = conn.execute(
                f"SELECT date, "
                f"SUM(n_omp), SUM(sx_omp), SUM(sy_omp), SUM(sxx_omp), "
                f"SUM(syy_omp), SUM(sxy_omp), "
                f"SUM(n_oma), SUM(sx_oma), SUM(sy_oma), SUM(sxx_oma), "
                f"SUM(syy_oma), SUM(sxy_oma) "
                f"FROM pairs_cardio WHERE {where} GROUP BY date;",
                params,
            ).fetchall()
    except Exception:
        return None
    if not rows:
        return None
    by_date = {int(r[0]): r[1:] for r in rows}
    out = {}
    for j, tag in enumerate(("omp", "oma")):
        base = j * 6
        for k, name in enumerate(("n", "sx", "sy", "sxx", "syy", "sxy")):
            out[f"{name}_{tag}"] = np.array(
                [float(by_date.get(int(d), [np.nan] * 12)[base + k] or 0.0) for d in dates],
                dtype=float,
            )
    return out


def _pair_where(task):
    where = ["region = ?", "flag = ?", "land_ocean = ?", "special = ?", "varno = ?"]
    params = [task["region"], task["flag_criteria"], task.get("land_ocean", "all"),
              task.get("special", "all"), task["varno"]]
    if str(task["vcoord"]) != "join":
        where.append("Chan = ?")
        params.append(task["vcoord"])
    return " AND ".join(where) + task.get("stn_sql", ""), params


def _pair_series(task):
    """MATCH on: the series of the control and of the experience, both from
    the pairs -- every panel then rests on the same observations. Returns
    (ref, exp, sums): the two series with the keys of _series, and the
    per-cycle sums the verdict of the period is computed from."""
    path = task.get("db_pairs")
    if not path or not os.path.isfile(path):
        return None, None, None
    where, params = _pair_where(task)
    q = ("SELECT date, SUM(n_omp), SUM(sx_omp), SUM(sxx_omp), SUM(sy_omp), SUM(syy_omp), "
         "MIN(minx_omp), MAX(maxx_omp), MIN(miny_omp), MAX(maxy_omp), "
         "SUM(n_oma), SUM(sx_oma), SUM(sxx_oma), SUM(sy_oma), SUM(syy_oma), "
         "MIN(minx_oma), MAX(maxx_oma), MIN(miny_oma), MAX(maxy_oma), "
         "SUM(n_obs), SUM(sx_obs), SUM(sy_obs), SUM(nx_bcorr), SUM(sx_bcorr), "
         "SUM(ny_bcorr), SUM(sy_bcorr), SUM(nloc), SUM(sxy_omp), SUM(sxy_oma) "
         f"FROM pairs_cardio WHERE {where} GROUP BY date ORDER BY date;")
    try:
        with open_result(path) as conn:
            rows = conn.execute(q, params).fetchall()
    except Exception:
        return None, None, None
    if not rows:
        return None, None, None
    a = np.array([[float(v) if v is not None else np.nan for v in r] for r in rows])
    dates = [str(int(d)) for d in a[:, 0]]

    def _m(n, s1):
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.where(n > 0, s1 / n, np.nan)

    def _sd(n, s1, s2):
        m = _m(n, s1)
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.sqrt(np.maximum(np.where(n > 0, s2 / n - m * m, np.nan), 0.0))

    nan = np.full(len(a), np.nan)

    def _side(o):
        # o: 0 for the control (x), 1 for the experience (y)
        sp, sq, lo, hi = (2, 3, 6, 7) if o == 0 else (4, 5, 8, 9)
        ap, aq, alo, ahi = (11, 12, 15, 16) if o == 0 else (13, 14, 17, 18)
        nbc, sbc = (22, 23) if o == 0 else (24, 25)
        return {"dates": dates, "nrej": nan, "nacc": a[:, 1], "nprofile": nan,
                "nloc": a[:, 26], "ndata": a[:, 1],
                "avg_omp": _m(a[:, 1], a[:, sp]), "std_omp": _sd(a[:, 1], a[:, sp], a[:, sq]),
                "avg_oma": _m(a[:, 10], a[:, ap]), "std_oma": _sd(a[:, 10], a[:, ap], a[:, aq]),
                "avg_obs": _m(a[:, 19], a[:, 20 + o]), "n_bcorr": a[:, nbc],
                "avg_bcorr": _m(a[:, nbc], a[:, sbc]),
                "min_omp": a[:, lo], "max_omp": a[:, hi], "min_oma": a[:, alo], "max_oma": a[:, ahi]}

    sums = {"omp": (a[:, 1], a[:, 2], a[:, 3], a[:, 4], a[:, 5], a[:, 27]),
            "oma": (a[:, 10], a[:, 11], a[:, 12], a[:, 13], a[:, 14], a[:, 28])}
    return _side(0), _side(1), sums


def _paired_cycle_tests(sums) -> Dict[str, Dict[str, Dict[str, np.ndarray]]]:
    """MATCH on: the test of each date, on its own pairs -- the t-test on the
    bias, the F-test on the sigma, as with MATCH off: the two modes differ
    by the observations they compare, not by the test -- in the shape of
    _cycle_tests, for the dots of the strip."""
    out: Dict[str, Dict[str, Dict[str, np.ndarray]]] = {}
    for metric, (n, sx, sxx, sy, syy, sxy) in (sums or {}).items():
        mx, vx = moments_from_sums(n, sx, sxx)
        my, vy = moments_from_sums(n, sy, syy)
        sdx, sdy = np.sqrt(np.maximum(vx, 0)), np.sqrt(np.maximum(vy, 0))
        out[metric] = {
            "mean": {"conf": ttest_confidence(mx, sdx, n, my, sdy, n),
                     "side": np.abs(my) - np.abs(mx)},
            "std": {"conf": sigma_confidence(vx, vy, n, n),
                    "side": sdy - sdx},
        }
    return out


def _verdict_text(verdict, is_oma: bool) -> list:
    """The verdict as (text, colour) pieces, read along one line."""
    pieces = []
    for metric in ("omp", "oma") if is_oma else ("omp",):
        v = verdict.get(metric)
        if not v:
            continue
        pieces.append((f"{'O-P' if metric == 'omp' else 'O-A'}:  ", "#30343A"))
        for q in ("bias", "sigma"):
            conf, change, n_cyc = v[q]
            if not np.isfinite(conf):
                pieces.append((f"{q} not tested ({n_cyc} cycles)    ", GREY_TEXT))
            elif conf >= MIN_CONFIDENCE:
                better = change < 0
                pieces.append((f"{q} {'Exp' if better else 'Ctl'} better ({conf:.0f} %)    ",
                               EXP_BETTER if better else CTL_BETTER))
            else:
                pieces.append((f"{q} no clear change ({conf:.0f} %)    ", GREY_TEXT))
    return pieces


def _test_strip(strip, ax, x, quantity, key, tests, verdict, on, is_oma) -> None:
    """The tests of a panel, in the strip under it: a line for O-P, one for
    O-A, and on them only dots -- filled where the change is significant
    (red: Exp better, blue: Ctl better), hollow where it is not. One dot
    per date, under it: Welch on the bias and the F-test on the sigma, on
    the pairs of that date with MATCH on, on all its observations with
    MATCH off."""
    metrics = ("omp", "oma") if is_oma else ("omp",)
    rows = {m: len(metrics) - 1 - i for i, m in enumerate(metrics)}
    beside = mtransforms.blended_transform_factory(strip.transAxes, strip.transData)

    def _dots(xs, yrow, sig, side, size, transform=None):
        kw = {"transform": transform} if transform is not None else {}
        filled = np.where(side < 0, EXP_BETTER, CTL_BETTER)
        if sig.any():
            strip.scatter(xs[sig], np.full(sig.sum(), yrow), s=size, facecolors=filled[sig],
                          edgecolors=filled[sig], linewidths=1.5, zorder=3, clip_on=False, **kw)
        if (~sig).any():
            strip.scatter(xs[~sig], np.full((~sig).sum(), yrow), s=size, facecolors="white",
                          edgecolors="#333333", linewidths=2.0, zorder=3, clip_on=False, **kw)

    for m, yrow in rows.items():
        strip.axhline(yrow, color="#D0D4D9", lw=1.2, zorder=1)
        t = (tests or {}).get(m, {}).get(key)
        if t:
            conf, side = np.asarray(t["conf"], float), np.asarray(t["side"], float)
            ok = np.isfinite(conf) & np.isfinite(side)
            _dots(np.asarray(x)[ok], yrow, is_significant(conf[ok]), side[ok], 170)
        v = (verdict or {}).get(m, {}).get(quantity) if on else None
        if v and np.isfinite(v[0]):
            _dots(np.array([1.035]), yrow, np.array([v[0] >= MIN_CONFIDENCE]),
                  np.array([v[1]]), 520, transform=beside)
    if on:
        strip.text(1.035, len(metrics) - 0.3, "period", transform=beside, ha="center",
                   va="bottom", fontsize=8 * FS, color=GREY_TEXT, clip_on=False)
    strip.set_ylim(-0.7, len(metrics) - 0.3)
    strip.set_yticks(list(rows.values()))
    strip.set_yticklabels(["O-P" if m == "omp" else "O-A" for m in rows], fontsize=9 * FS)
    strip.tick_params(axis="y", length=0, pad=14)
    # the dates, as big as on every panel
    strip.tick_params(axis="x", labelsize=10 * FS, width=1.5, length=6)
    strip.grid(True, axis="x", linestyle=":", color="grey")
    for side_name in ("top", "right", "left"):
        strip.spines[side_name].set_visible(False)
    # the dates under the strip, not between it and its panel
    ax.tick_params(axis="x", labelbottom=False)


def _cycle_tests(ref, exp) -> Dict[str, Dict[str, np.ndarray]]:
    """MATCH off: per date, does the change of bias or sigma pass the test?
    The t-test on the bias and the F-test on the sigma, on each run's own
    moments -- the same tests MATCH on runs on the pairs of each date
    (_paired_cycle_tests), from :mod:`pikobs.stats`."""
    out: Dict[str, Dict[str, np.ndarray]] = {}
    for metric in ("omp", "oma"):
        n1 = ref[f"n_{metric}"] if f"n_{metric}" in ref else ref["ndata"]
        n2 = exp[f"n_{metric}"] if f"n_{metric}" in exp else exp["ndata"]
        m1, m2 = ref[f"avg_{metric}"], exp[f"avg_{metric}"]
        s1, s2 = ref[f"std_{metric}"], exp[f"std_{metric}"]
        out[metric] = {
            # for the bias, better means closer to zero
            "mean": {"conf": ttest_confidence(m1, s1, n1, m2, s2, n2), "side": np.abs(m2) - np.abs(m1)},
            "std": {"conf": sigma_confidence(s1**2, s2**2, n1, n2), "side": s2 - s1},
        }
    return out


def _mark_significant(ax, x, values, conf, side) -> int:
    """The cycles where the change passes the test: counted only, the dots
    are drawn in the strip under the panel (_test_strip)."""
    ok = is_significant(conf) & np.isfinite(values) & np.isfinite(side)
    return int(np.sum(ok))


def _chan_text(v) -> str:
    """A channel or a level as it is read: 23, not 23.0; join as it is."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return str(v)
    return str(int(f)) if f.is_integer() else f"{f:g}"


def _new_cardiogram(runs, task, tests, varno, exp):
    """The figure, its six panels and the time axis they share."""

    is_oma = any(np.isfinite(d["avg_oma"]).any() for _, d, _ in runs)
    is_bcor = any(np.isfinite(d["avg_bcorr"]).any() for _, d, _ in runs)

    # one panel per row, across the whole width: a period of one or two
    # months needs the room along the time axis. Every room in inches, so
    # nothing overlaps
    # the header: title, subtitle, rule, runs, dates, the key, the note or
    # the verdict of the period
    compared = bool(task.get("db_control"))
    header_in = 2.45 * FS
    panel_h, gap_in = 3.8, 2.1          # the gap: the dates, then the next titles
    left_in, right_in = 2.4, 0.6
    fig_w = 30.0 if task.get("plot_type") == "wide" else 26.0
    fig_h = header_in + 0.6 + 6 * panel_h + 6 * gap_in
    fig_size = (fig_w, fig_h)
    fig = plt.figure(figsize=fig_size, facecolor="white")
    pw = fig_w - left_in - right_in
    axes, strips = [], {}
    # the tests: O-P and O-A, a line each -- none with MATCH no
    strip_h = 1.0 if compared and task.get("match_mode") != "no" else 0.0
    for k in range(6):
        x = left_in
        y_top = header_in + 0.6 + k * (panel_h + gap_in)
        h = panel_h - (strip_h if k < 2 else 0.0)
        ax = fig.add_axes([x / fig_w, 1 - (y_top + h) / fig_h, pw / fig_w, h / fig_h])
        axes.append(ax)
        if k < 2 and strip_h:
            strips[k] = fig.add_axes([x / fig_w, 1 - (y_top + panel_h) / fig_h,
                                      pw / fig_w, strip_h / fig_h], sharex=ax)
    fig._pikobs_strips = strips
    ax1, ax2, ax3, ax4, ax5, ax6 = axes

    variable_name, unit, _ = pikobs.type_varno(f"{varno}")
    x = mdates.date2num([parse_flexible_date(d) for d in exp["dates"]])
    xmi = mdates.date2num(parse_flexible_date(task["datestart"]))
    xma = mdates.date2num(parse_flexible_date(task["dateend"]))
    if xmi == xma:
        xmi, xma = xmi - 0.25, xma + 0.25
    for ax in axes:
        ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=4, maxticks=12))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        ax.set_xlim([xmi, xma])
        ax.tick_params(axis="both", which="major", labelsize=10 * FS, width=1.5, length=6)
        ax.grid(True, linestyle=":", color="grey")

    return is_oma, is_bcor, fig_size, fig, ax1, ax2, ax3, ax4, ax5, ax6, variable_name, unit, x


def _draw_bias(runs, is_bcor, ax1, x, _look, is_oma, tests, exp, unit):
    """Panel 1: the mean departures, with the cycles where the runs differ marked."""

    # ── panel 1: mean departures ──
    for name, d, style in runs:
        bcor = np.nan_to_num(d["avg_bcorr"]) if is_bcor else np.zeros_like(d["avg_omp"])
        ax1.plot(x, d["avg_omp"], **_look(style, ROUGEPUR, "-"), lw=2, label=f"O-P {name}")
        if is_oma:
            ax1.plot(x, d["avg_oma"], **_look(style, BLEU, "--"), lw=2, label=f"O-A {name}")
        if is_bcor:
            ax1.plot(x, bcor, **_look(style, VERT, ":"), lw=1.5, label=f"bcor {name}")
    n_marks = 0
    if tests:
        n_marks += _mark_significant(
            ax1, x, exp["avg_omp"], tests["omp"]["mean"]["conf"], tests["omp"]["mean"]["side"]
        )
        if is_oma:
            n_marks += _mark_significant(
                ax1, x, exp["avg_oma"], tests["oma"]["mean"]["conf"], tests["oma"]["mean"]["side"]
            )
    ax1.axhline(0, color=NOIR, lw=1.2, zorder=1)
    ax1.set_ylabel(f"Bias {unit}", fontsize=12 * FS)
    ax1.set_title(_summary_line(runs, "avg", is_oma, is_bcor), fontsize=11 * FS, loc="left")

    return n_marks


def _draw_sigma(runs, ax2, x, _look, is_oma, tests, exp, n_marks, unit):
    """Panel 2: the sigma of the departures, with the same marks."""

    # ── panel 2: sigma ──
    for name, d, style in runs:
        ax2.plot(x, d["std_omp"], **_look(style, ROUGEPUR, "-"), lw=2, label=f"O-P {name}")
        if is_oma:
            ax2.plot(x, d["std_oma"], **_look(style, BLEU, "--"), lw=2, label=f"O-A {name}")
    if tests:
        n_marks += _mark_significant(
            ax2, x, exp["std_omp"], tests["omp"]["std"]["conf"], tests["omp"]["std"]["side"]
        )
        if is_oma:
            n_marks += _mark_significant(
                ax2, x, exp["std_oma"], tests["oma"]["std"]["conf"], tests["oma"]["std"]["side"]
            )
    ax2.set_ylabel(f"Sigma {unit}", fontsize=12 * FS)
    ax2.set_title(_summary_line(runs, "std", is_oma, False), fontsize=11 * FS, loc="left")

    return n_marks


def _draw_values(runs, exp_name, ax3, x, _look, is_oma, unit):
    """Panel 3: the physical values (the trial and the analysis)."""

    # ── panel 3: physical values ──
    for name, d, style in runs:
        if name == exp_name:  # the same observations in both runs: once, in black
            ax3.plot(x, d["avg_obs"], color=NOIR, linestyle="-.", lw=1.4, label="observation")
        ax3.plot(
            x, d["avg_obs"] - d["avg_omp"], **_look(style, ROUGEPUR, "-"), label=f"Trial {name}"
        )
        if is_oma:
            ax3.plot(
                x, d["avg_obs"] - d["avg_oma"], **_look(style, BLEU, "--"), label=f"Anal {name}"
            )
    ax3.set_ylabel(f"Obsvalue {unit}", fontsize=12 * FS)


def _draw_counts(runs, ax4, x, _look):
    """Panel 4: observations and locations."""

    # ── panel 4: counts ──
    for name, d, style in runs:
        ax4.plot(x, d["ndata"], **_look(style, NOIR, "-"), label=f"Ndata {name}")
        ax4.plot(x, d["nloc"], **_look(style, "#888888", "--"), lw=1.2, label=f"Nlocs {name}")
    ax4.set_ylabel("Observations", fontsize=12 * FS)
    # no legend on the curves: a title line, as the extremes have
    ax4.set_title(
        "Ndata (solid): observations  \u00b7  Nlocs (dashed): locations",
        fontsize=10 * FS,
        loc="left",
        color="#555555",
    )


def _draw_extremes(ax5, ax6, runs, x, _look, unit, fig):
    """Panels 5 and 6: the extremes of O-P and O-A in each cycle."""

    # ── panels 5 and 6: the extremes of each cycle ──
    for ax, metric, colour in ((ax5, "omp", ROUGEPUR), (ax6, "oma", BLEU)):
        drawn = False
        for name, d, style in runs:
            lo, hi = d[f"min_{metric}"], d[f"max_{metric}"]
            if not (np.isfinite(lo).any() or np.isfinite(hi).any()):
                continue
            drawn = True
            dash = "-" if metric == "omp" else "--"
            ax.plot(x, hi, **_look(style, colour, dash), lw=1.6, label=f"max {name}")
            ax.plot(x, lo, **_look(style, colour, dash), lw=1.6, alpha=0.65, label=f"min {name}")
            if style == CTL_STYLE:
                ax.fill_between(x, lo, hi, alpha=0.10, color=_look(style, colour, dash)["color"])
        ax.axhline(0, color=NOIR, lw=1.0, zorder=1)
        what = "O-P" if metric == "omp" else "O-A"
        ax.set_ylabel(f"{what} range {unit}", fontsize=12 * FS)
        if not drawn:
            ax.text(
                0.5,
                0.5,
                f"no {metric.upper()} in this selection",
                transform=ax.transAxes,
                ha="center",
                va="center",
                color="#999999",
                fontsize=11 * FS,
            )
        ax.set_title(
            f"Extremes of {what} per cycle",
            fontsize=10 * FS,
            loc="left",
            color="#555555",
        )

    fig.autofmt_xdate()


def _draw_cardio_header(
    fig_size,
    task,
    family,
    region,
    flag,
    id_stn,
    channel,
    fig,
    variable_name,
    unit,
    ref,
    exp_name,
    ctl_name,
    is_bcor,
    tests,
    n_marks,
    verdict=None,
    on: bool = False,
):
    """The header: variable, selection, runs, dates, the key and the note;
    with MATCH on the verdict of the period, and the MATCH badge whenever
    two runs are compared."""

    # the header, as in scatter and zone: the variable, a grey line with
    # what the figure holds, a light rule, the runs in their colours, the
    # dates, one key for every panel, the note of the circles small
    from matplotlib.lines import Line2D

    def _when(stamp) -> str:
        s = str(stamp)
        return f"{s[:4]}-{s[4:6]}-{s[6:8]} {s[8:10]} UTC"

    def _y(inch: float) -> float:
        return 1.0 - inch * FS / fig_size[1]

    land = task.get("land_ocean", "all")
    sp = task.get("special_label", "all")
    try:
        is_channel = str(pikobs.family(family)[5]).upper() == "CANAL"
    except Exception:
        is_channel = False
    word = "channel" if is_channel else "level"
    parts = [
        family,
        region if land in (None, "", "all") else f"{region} ({land})",
        f"flag {flag}",
        f"station {id_stn}",
        f"all {word}s" if str(channel) == "join" else f"{word} {_chan_text(channel)}",
    ]
    if sp not in (None, "", "all"):
        parts.append(f"method {sp}")
    x0 = 0.10
    fig.text(
        0.5,
        _y(0.18),
        f"{variable_name} {unit}",
        ha="center",
        va="top",
        fontsize=15 * FS,
        fontweight="bold",
        color="#1F2933",
    )
    fig.text(
        0.5, _y(0.52), "  ·  ".join(parts), ha="center", va="top", fontsize=11 * FS, color=GREY_TEXT
    )
    fig.add_artist(
        Line2D(
            [x0, 0.90], [_y(0.80)] * 2, color="#c8c8c8", linewidth=0.9, transform=fig.transFigure
        )
    )
    y_in = 0.92
    who = (
        [("Exp", exp_name, EXP_COLOUR), ("Ctl", ctl_name, CTL_COLOUR)]
        if ref is not None
        else [("Exp", exp_name, EXP_COLOUR)]
    )
    for label, name, colour in who:
        fig.text(
            x0,
            _y(y_in),
            f"{label}  {name}",
            ha="left",
            va="top",
            fontsize=12 * FS,
            fontweight="bold",
            color=colour,
        )
        y_in += 0.25
    fig.text(
        x0,
        _y(y_in),
        f"{_when(task['datestart'])}  to  " f"{_when(task['dateend'])}",
        ha="left",
        va="top",
        fontsize=10 * FS,
        color=GREY_TEXT,
    )
    y_in += 0.24
    # one key for every panel: the colour says the run, the line the quantity
    key = [
        Line2D([], [], color="#444444", ls="-", lw=2, label="O-P, trial, Ndata"),
        Line2D([], [], color="#444444", ls="--", lw=2, label="O-A, analysis, Nlocs"),
        Line2D([], [], color=NOIR, ls="-.", lw=1.4, label="observation"),
    ]
    if is_bcor:
        key.append(Line2D([], [], color="#444444", ls=":", lw=1.5, label="bias correction"))
    if tests:
        key.append(
            Line2D(
                [],
                [],
                color="#888888",
                ls="",
                marker="o",
                markersize=9,
                alpha=0.4,
                label=f"change above {MIN_CONFIDENCE:.0f} %",
            )
        )
    fig.legend(
        handles=key,
        loc="upper left",
        ncol=len(key),
        frameon=False,
        fontsize=10 * FS,
        handlelength=3,
        borderaxespad=0,
        bbox_to_anchor=(x0 - 0.008, _y(y_in)),
    )
    y_in += 0.30
    if verdict:
        # the verdict of the period, a line per departure, its pieces in
        # their colours one after the other
        renderer = fig.canvas.get_renderer()
        fig.text(x0, _y(y_in), "period, cycle block bootstrap:", ha="left", va="top",
                 fontsize=10.5 * FS, fontweight="bold", color="#30343A")
        pieces = _verdict_text(verdict, True)
        lines, cur = [], []
        for text, colour in pieces:
            if text.startswith(("O-P", "O-A")) and cur:
                lines.append(cur)
                cur = []
            cur.append((text, colour))
        if cur:
            lines.append(cur)
        for line in lines:
            y_in += 0.27
            x = x0 + 0.02
            for text, colour in line:
                t = fig.text(x, _y(y_in), text, ha="left", va="top", fontsize=10.5 * FS,
                             fontweight="bold", color=colour)
                box = t.get_window_extent(renderer=renderer)
                x = fig.transFigure.inverted().transform((box.x1, box.y0))[0]
    if ref is not None and task.get("match_mode") != "no":
        # MATCH on: Welch and F on the pairs of each date, as off does on all
        match_badge(fig, on, top_in=0.12 * FS, method="t-test and F-test, 95 %" if on else None)
    if tests:
        fig.text(
            x0,
            _y(y_in),
            f"circles: a change above {MIN_CONFIDENCE:.0f} % "
            f"confidence, red where Exp is better, blue where Ctl is  "
            f"({n_marks} in this figure)",
            ha="left",
            va="top",
            fontsize=9.5 * FS,
            color=GREY_TEXT,
        )


def _save_cardiogram(pathwork, family, exp_name, flag, task, id_stn, region, channel, varno, fig):
    """Write the figure; returns its path."""

    out_dir = os.path.join(pathwork, family)
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(
        out_dir,
        figure_name(
            exp_name,
            flag,
            family,
            task.get("stn_tag", id_stn),
            region,
            channel,
            varno,
            task.get("land_ocean", "all"),
            task.get("special_label", "all"),
        ),
    )
    if task.get("db_control") and task.get("match_mode") in ("off", "no"):
        # MATCH off and no have their own files, beside the MATCH on one
        out_file = out_file[: -len(".png")] + f"_match{task['match_mode']}.png"
    save_figure(fig, out_file, svg=task.get("svg", False), dpi=DPI)
    plt.close(fig)
    return out_file


def cardio_plot(task: Dict[str, Any]) -> Optional[str]:
    """Draw the cardiogram; returns the path of the PNG.

    With a control in the task, the two runs share every panel: the
    control solid, the experience dashed, and a circle on each cycle
    where the difference passes the test.
    """
    on = bool(task.get("db_control")) and task.get("match_mode") == "on"
    if on:
        # MATCH on: both runs from their pairs, every panel; no mark per
        # cycle, the verdict of the period instead
        ref, exp, sums = _pair_series(task)
        if exp is None:
            return None
        tests = _paired_cycle_tests(sums)
    else:
        exp = _series(task)
        if exp is None:
            return None
        ref = None
        if task.get("db_control"):
            ref = _series(task, task["db_control"])
            if ref is not None:
                ref, exp = _align(ref, exp)
                if ref is None:
                    return None
        # MATCH off: each run with all its observations, Welch and the
        # F-test cycle by cycle
        tests = (_cycle_tests(ref, exp)
                 if ref is not None and task.get("match_mode") != "no" else {})

    pathwork = task["pathwork"]
    family, region = task["family"], task["region"]
    flag, varno = task["flag_criteria"], task["varno"]
    channel, id_stn = task["vcoord"], task["id_stn"]
    exp_name = task["experience"]
    ctl_name = task.get("control")

    runs = ([(ctl_name, ref, CTL_STYLE)] if ref is not None else []) + [
        (exp_name, exp, EXP_STYLE if ref is not None else CTL_STYLE)
    ]

    # The colour says which run, the line style which quantity: red the
    # experience and blue the control, in a single run too; O-P and the
    # trial solid, O-A and the analysis dashed. Every figure reads the same.
    def _look(style, colour, dash):
        own = CTL_COLOUR if (ref is not None and style == CTL_STYLE) else EXP_COLOUR
        return dict(linestyle=dash, color=own)

    is_oma, is_bcor, fig_size, fig, ax1, ax2, ax3, ax4, ax5, ax6, variable_name, unit, x = (
        _new_cardiogram(runs, task, tests, varno, exp)
    )
    n_marks = _draw_bias(runs, is_bcor, ax1, x, _look, is_oma, tests, exp, unit)
    n_marks = _draw_sigma(runs, ax2, x, _look, is_oma, tests, exp, n_marks, unit)
    _draw_values(runs, exp_name, ax3, x, _look, is_oma, unit)
    _draw_counts(runs, ax4, x, _look)
    _draw_extremes(ax5, ax6, runs, x, _look, unit, fig)
    strips = getattr(fig, "_pikobs_strips", {})
    for k, (ax, quantity, key) in enumerate(((ax1, "bias", "mean"), (ax2, "sigma", "std"))):
        if k in strips:
            # only the dot of each date: no dot of the whole period
            _test_strip(strips[k], ax, x, quantity, key, tests, None, False, is_oma)
    # the lines as thick as the text is big, the counts as 1K, 2K
    for ax in (ax1, ax2, ax3, ax4, ax5, ax6):
        for line in ax.get_lines():
            line.set_linewidth(line.get_linewidth() * 1.8)
    ax4.yaxis.set_major_formatter(count_formatter())
    _draw_cardio_header(
        fig_size,
        task,
        family,
        region,
        flag,
        id_stn,
        channel,
        fig,
        variable_name,
        unit,
        ref,
        exp_name,
        ctl_name,
        is_bcor,
        {},          # the tests are in the strips: no note, no key for them
        n_marks,
        verdict=None,
        on=on,
    )
    return _save_cardiogram(
        pathwork, family, exp_name, flag, task, id_stn, region, channel, varno, fig
    )


def _summary_line(runs, kind: str, is_oma: bool, is_bcor: bool) -> str:
    """The numbers of the whole period, one run after the other."""
    bits = []
    for name, d, style in runs:
        who = "Ctl" if (len(runs) > 1 and style == CTL_STYLE) else "Exp"
        n = d["ndata"]
        tot = np.nansum(n) or 1.0

        def _w(values):
            return float(np.nansum(np.where(np.isfinite(values), values, 0.0) * n) / tot)

        if kind == "avg":
            part = f"{who}: O-P {_w(d['avg_omp']):.3f}"
            if is_oma:
                part += f"  O-A {_w(d['avg_oma']):.3f}"
            if is_bcor:
                part += f"  bcor {_w(d['avg_bcorr']):.3f}"
        else:
            part = f"{who}: sigma O-P {_w(d['std_omp']):.3f}"
            if is_oma:
                part += f"  O-A {_w(d['std_oma']):.3f}"
        bits.append(part)
    return "\n".join(bits)
