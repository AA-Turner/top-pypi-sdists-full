#!/usr/bin/python3
"""Channel summaries of pikobs.cardio: every channel of a selection at a glance.

A cardiogram follows one channel through the period; with IASI or CrIS that
is hundreds of figures. A summary puts them in one: a row per channel (the
smallest at the bottom) and a column per cycle.

* ``<family>_resume_<run>...`` -- one run: the bias and the sigma of O-P and
  O-A, and the number of observations, per channel and cycle. With a control,
  every run gets its own -- the control (Ctl, in blue) and each experience --
  on the same colour scales, so the same colour means the same number.
* ``<family>_scorecard_...`` -- a comparison, once per MATCH mode: the same
  cells as Exp against Ctl, the change of |bias| and of sigma, coloured only
  where the test passes -- red where Exp is better, blue where Ctl is, grey
  where it is noise. Each cell is tested as the dots of the cardiograms: the
  t-test and the F-test of that cycle, on its pairs with MATCH on, on all its
  observations with MATCH off. The narrow ``period`` column beside each panel
  tests the whole period: the cycle block bootstrap with MATCH on, the t-test
  and the F-test on the pooled observations with MATCH off. MATCH no: the
  changes, no test.

Each summary is written as a PNG for the viewer, which gives the channel
under the mouse (``<png>.map.json``), and as a self-contained HTML page next
to it, where the mouse gives the channel, the cycle and the value of every
cell. Everything comes from the sums cardio already stored: no input file is
read again.
"""

import base64
import html
import io
import json
import math
import os
import sys
import traceback
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.colors import BoundaryNorm, ListedColormap, Normalize
from matplotlib.ticker import MaxNLocator

import pikobs
from pikobs.configobs.special_family import special_label
from pikobs.configobs.style import CTL_COLOUR, EXP_COLOUR, GREY_TEXT, font_size
from pikobs.figures.figures import (count_formatter, fit_texts, match_badge, save_figure,
                                    write_hover_rects)
from pikobs.obsdb import open_result
from pikobs.obsdb import safe_name as _safe
from pikobs.stats.stats import (BOOT_MIN_CYCLES, BOOT_MIN_PAIRS, MIN_CONFIDENCE,
                                cycle_bootstrap_many, is_significant, moments_from_sums,
                                sigma_confidence, ttest_confidence)

#: every text is 'size * FS', as in the cardiograms
# a little larger than the cardiograms: the summary is read whole, at once
FS = 1.15 * font_size("title") / 14.0
DPI = 110
#: the cells of a comparison: the test did not pass (grey), no data (white)
NOISE = "#DCDEE1"
EMPTY = "#FFFFFF"
ZERO = "#F4F4F2"              # exactly no change
#: the steps of a colour scale: 1-2-5 in physical units, doubling in %
STEPS_UNIT = (0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0,
              20.0, 50.0, 100.0)
STEPS_PCT = (1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0)
STEPS_COUNT = (2.0, 5.0, 10.0, 20.0, 50.0, 100.0)
#: light to dark: red where Exp is better, blue where Ctl is (and, for the
#: bias of one run, red above zero and blue below, as scatter)
REDS = ["#FBD5D5", "#F5A8A8", "#EA7272", "#D43D42", "#A8202A", "#6E0F17"]
BLUES = ["#D6E5F5", "#AACBEA", "#73A7D8", "#3C7EC0", "#1F5A99", "#0E3768"]
#: more or fewer observations is neither better nor worse: purple and orange
MORE = ["#E2DDF0", "#C2B5DB", "#9E8AC4", "#7759A7", "#542788", "#2D004B"]
FEWER = ["#FDE0C2", "#FDB863", "#F08A2B", "#C55A11", "#7F3B08", "#4A2205"]
SUMMARY = "summary"           # the value of the channel selector in the viewer


# ─────────────────────────────────────────────────────────────────────────────
# Tasks
# ─────────────────────────────────────────────────────────────────────────────

_GROUP_KEYS = ("experience", "control", "family", "region", "flag_criteria", "land_ocean",
               "special", "stn_tag", "stn_sql", "varno", "match_mode")
_SELECTION_KEYS = ("family", "region", "flag_criteria", "land_ocean", "special", "stn_tag",
                   "stn_sql", "varno")


def summary_tasks(plot_tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """The summaries of the cardiograms, every channel together.

    One task per selection draws the resume of every run -- the control and
    each experience -- so they share their colour scales; one task per
    comparison and MATCH mode draws its scorecard."""
    resumes: Dict[tuple, Dict[str, Any]] = {}
    cards, seen = [], set()
    for t in plot_tasks:
        sel = tuple(str(t.get(k, "")) for k in _SELECTION_KEYS)
        group = resumes.get(sel)
        if group is None:
            group = dict(t, kind="resume", vcoord=SUMMARY, runs=[], db_control=None,
                         control=None, db_pairs=None, match_mode="")
            resumes[sel] = group
        names = [r[0] for r in group["runs"]]
        if t.get("db_control") and t.get("control") not in names:
            group["runs"].insert(0, (t["control"], t["db_control"], "ctl"))
            names = [r[0] for r in group["runs"]]
        if t["experience"] not in names:
            group["runs"].append((t["experience"], t["db_file"], "exp"))
        if t.get("db_control"):
            key = tuple(str(t.get(k, "")) for k in _GROUP_KEYS)
            if key not in seen:
                seen.add(key)
                cards.append(dict(t, kind="scorecard", vcoord=SUMMARY))
    return list(resumes.values()) + cards


def summary_name(task: Dict[str, Any]) -> str:
    """<family>_resume_... or <family>_scorecard_..., as the cardiograms are
    named; MATCH off and no end in _matchoff and _matchno."""
    family = task["family"]
    kind = "scorecard" if task.get("db_control") else "resume"
    land = task.get("land_ocean", "all")
    sp = task.get("special", "all")
    tail = "" if land in (None, "", "all") else f"_{_safe(land)}"
    tail += "" if sp in (None, "", "all") else f"_{_safe(special_label(family, sp))}"
    name = (f"{_safe(family)}_{kind}_{_safe(task['experience'])}_{_safe(task['flag_criteria'])}_"
            f"{_safe(task.get('stn_tag', task['id_stn']))}_id_stn_{_safe(task['region'])}{tail}_"
            f"varno{_safe(task['varno'])}")
    if task.get("db_control") and task.get("match_mode") in ("off", "no"):
        name += f"_match{task['match_mode']}"
    return name + ".png"


def _entry(task, png) -> Dict[str, str]:
    """What the viewer and the index need of a summary written."""
    compared = task.get("kind") == "scorecard"
    return {"png": png, "kind": task.get("kind", "resume"),
            "experience": (f"{task['experience']} vs {task['control']}" if compared
                           else task["experience"]),
            "flag_criteria": task["flag_criteria"], "family": task["family"],
            "region": task["region"], "land_ocean": task.get("land_ocean", "all"),
            "special": task.get("special_label", "all"), "id_stn": task["id_stn"],
            "varno": str(task["varno"]), "match": task.get("match_mode", "") if compared else ""}


def summary_task(task: Dict[str, Any]) -> Optional[List[Dict[str, str]]]:
    """Draw the summaries of one task (PNG, mouse map and HTML of each);
    returns what was written, or None. Never stops the run."""
    try:
        if task.get("kind") == "resume":
            out = resume_group(task)
        else:
            png = summary_plot(task)
            out = [_entry(task, png)] if png else []
        return out or None
    except Exception:
        print(f"[cardio] summary failed for {task['family']} {task['experience']} "
              f"{task['id_stn']}:\n{traceback.format_exc()}", file=sys.stderr, flush=True)
        return None


# ─────────────────────────────────────────────────────────────────────────────
# Reading the sums: one grid of channels x cycles
# ─────────────────────────────────────────────────────────────────────────────

def _where(task) -> Tuple[str, list]:
    where = ["region = ?", "flag = ?", "land_ocean = ?", "special = ?", "varno = ?"]
    args = [task["region"], task["flag_criteria"], task.get("land_ocean", "all"),
            task.get("special", "all"), task["varno"]]
    return " AND ".join(where) + task.get("stn_sql", ""), args


def _chan_key(c):
    try:
        return (0, float(c), "")
    except (TypeError, ValueError):
        return (1, 0.0, str(c))


def _grid(rows, down: bool = False) -> Tuple[list, list, np.ndarray]:
    """(Chan, date, v1, ..., vk) rows -> channels, dates and a [k, channel,
    cycle] array, NaN where a channel has no row at a cycle. Row 0 is drawn
    at the bottom: the smallest channel, or with ``down`` the largest value
    (the pressure of the ground)."""
    chans = sorted({r[0] for r in rows}, key=_chan_key, reverse=down)
    dates = sorted({int(r[1]) for r in rows})
    ci = {c: i for i, c in enumerate(chans)}
    di = {d: j for j, d in enumerate(dates)}
    out = np.full((len(rows[0]) - 2, len(chans), len(dates)), np.nan)
    for r in rows:
        out[:, ci[r[0]], di[int(r[1])]] = [np.nan if v is None else float(v) for v in r[2:]]
    return chans, dates, out


def _pressure(task) -> bool:
    """A family whose levels are pressures: drawn with the ground at the bottom."""
    try:
        return "PRES" in str(pikobs.family(task["family"])[5]).upper()
    except Exception:
        return False


def _run_grid(task, db_file):
    """One run: per channel and cycle, n, sum and sum of squares of O-P, O-A."""
    where, args = _where(task)
    with open_result(db_file) as conn:
        rows = conn.execute(
            f"SELECT Chan, date, SUM(n_omp), SUM(s_omp), SUM(s2_omp), "
            f"SUM(n_oma), SUM(s_oma), SUM(s2_oma) FROM serie_cardio "
            f"WHERE {where} GROUP BY Chan, date;", args).fetchall()
    return _grid(rows, _pressure(task)) if rows else None


def _pair_grid(task):
    """MATCH on: per channel and cycle, the sums of the pairs (x the control,
    y the experience) of O-P and O-A."""
    where, args = _where(task)
    with open_result(task["db_pairs"]) as conn:
        rows = conn.execute(
            f"SELECT Chan, date, SUM(n_omp), SUM(sx_omp), SUM(sxx_omp), SUM(sy_omp), "
            f"SUM(syy_omp), SUM(n_oma), SUM(sx_oma), SUM(sxx_oma), SUM(sy_oma), "
            f"SUM(syy_oma) FROM pairs_cardio WHERE {where} GROUP BY Chan, date;",
            args).fetchall()
    return _grid(rows, _pressure(task)) if rows else None


def _on_union(a, b, down: bool = False):
    """Two grids on the channels and cycles of both."""
    (ca, da, ga), (cb, db, gb) = a, b
    chans = sorted(set(ca) | set(cb), key=_chan_key, reverse=down)
    dates = sorted(set(da) | set(db))

    def place(c, d, g):
        out = np.full((g.shape[0], len(chans), len(dates)), np.nan)
        ii = [chans.index(x) for x in c]
        jj = [dates.index(x) for x in d]
        out[np.ix_(range(g.shape[0]), ii, jj)] = g
        return out

    return chans, dates, place(ca, da, ga), place(cb, db, gb)


# ─────────────────────────────────────────────────────────────────────────────
# The numbers of each panel
# ─────────────────────────────────────────────────────────────────────────────

def _moments(n, s, s2):
    n = np.where(np.nan_to_num(n) > 0, n, np.nan)
    m, v = moments_from_sums(n, s, s2)
    return n, m, v, np.sqrt(np.maximum(v, 0.0))


def _resume_panels(g) -> Dict[str, Any]:
    """One run: bias and sigma of O-P and O-A, and the counts."""
    out = {}
    for k, tag in enumerate(("omp", "oma")):
        n, m, _, sd = _moments(g[3 * k], g[3 * k + 1], g[3 * k + 2])
        if not np.isfinite(m).any():
            continue
        _, pm, _, psd = _moments(*(np.nansum(a, axis=1) for a in g[3 * k: 3 * k + 3]))
        out[tag] = {"bias": m, "sigma": sd, "bias_period": pm, "sigma_period": psd}
    out["n"] = np.where(np.nan_to_num(g[0]) > 0, g[0], np.nan)
    out["n_period"] = np.nansum(g[0], axis=1)
    return out


def _change(mc, sc, me, se):
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.abs(me) - np.abs(mc), np.where(sc > 0, 100.0 * (se - sc) / sc, np.nan)


def _scorecard_on(g) -> Dict[str, Any]:
    """MATCH on, from the pairs: each cell the t-test and the F-test of its
    cycle, as the dots of the cardiograms; the period, the cycle block
    bootstrap of the changes of the cycles, as the verifprofile scorecard."""
    out = {}
    for k, tag in enumerate(("omp", "oma")):
        n, sx, sxx, sy, syy = g[5 * k: 5 * k + 5]
        n, mx, vx, sdx = _moments(n, sx, sxx)
        _, my, vy, sdy = _moments(n, sy, syy)
        if not np.isfinite(mx).any():
            continue
        d_bias, d_sigma = _change(mx, sdx, my, sdy)
        # the period: the pooled pairs of every cycle
        N = np.nansum(n, axis=1)
        pn, pmx, _, psx = _moments(N, np.nansum(sx, axis=1), np.nansum(sxx, axis=1))
        _, pmy, _, psy = _moments(N, np.nansum(sy, axis=1), np.nansum(syy, axis=1))
        p_bias, p_sigma = _change(pmx, psx, pmy, psy)
        # the change of each cycle that holds a few pairs, in units of the
        # sigma of the control over the period
        few = ~(np.nan_to_num(n) >= BOOT_MIN_PAIRS)
        with np.errstate(divide="ignore", invalid="ignore"):
            cb = (np.abs(my) - np.abs(mx)) / psx[:, None]
            cs = 100.0 * (sdy - sdx) / psx[:, None]
        cb[few] = np.nan
        cs[few] = np.nan
        out[tag] = {
            "bias": d_bias, "sigma": d_sigma,
            "bias_conf": ttest_confidence(mx, sdx, n, my, sdy, n),
            "sigma_conf": sigma_confidence(vx, vy, n, n),
            "bias_period": p_bias, "sigma_period": p_sigma,
            "bias_period_conf": cycle_bootstrap_many(cb),
            "sigma_period_conf": cycle_bootstrap_many(cs),
        }
    out["n"] = np.where(np.nan_to_num(g[0]) > 0, g[0], np.nan)
    out["n_period"] = np.nansum(g[0], axis=1)
    out["n_kind"] = "pairs"
    return out


def _scorecard_off(gc, ge, tested: bool) -> Dict[str, Any]:
    """MATCH off (tested) and no: each run with all its observations; each
    cell the t-test and the F-test of its cycle, the period the same tests
    on the pooled observations of each run."""
    out = {}
    nan = lambda a: np.full(np.shape(a), np.nan)            # noqa: E731
    for k, tag in enumerate(("omp", "oma")):
        nc, mc, vc, sc = _moments(*gc[3 * k: 3 * k + 3])
        ne, me, ve, se = _moments(*ge[3 * k: 3 * k + 3])
        if not (np.isfinite(mc).any() and np.isfinite(me).any()):
            continue
        d_bias, d_sigma = _change(mc, sc, me, se)
        pooled = [_moments(*(np.nansum(a, axis=1) for a in g[3 * k: 3 * k + 3])) for g in (gc, ge)]
        (pnc, pmc, pvc, psc), (pne, pme, pve, pse) = pooled
        p_bias, p_sigma = _change(pmc, psc, pme, pse)
        out[tag] = {
            "bias": d_bias, "sigma": d_sigma, "bias_period": p_bias, "sigma_period": p_sigma,
            "bias_conf": ttest_confidence(mc, sc, nc, me, se, ne) if tested else nan(mc),
            "sigma_conf": sigma_confidence(vc, ve, nc, ne) if tested else nan(mc),
            "bias_period_conf": ttest_confidence(pmc, psc, pnc, pme, pse, pne) if tested else nan(pmc),
            "sigma_period_conf": sigma_confidence(pvc, pve, pnc, pne) if tested else nan(pmc),
        }
    with np.errstate(divide="ignore", invalid="ignore"):
        out["n"] = np.where(np.nan_to_num(gc[0]) > 0, 100.0 * (ge[0] - gc[0]) / gc[0], np.nan)
        nc_, ne_ = np.nansum(gc[0], axis=1), np.nansum(ge[0], axis=1)
        out["n_period"] = np.where(nc_ > 0, 100.0 * (ne_ - nc_) / nc_, np.nan)
    out["n_kind"] = "change"
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Colours: one RGBA image per panel, used by the PNG and by the HTML
# ─────────────────────────────────────────────────────────────────────────────

def _hex(c) -> np.ndarray:
    return np.array(matplotlib.colors.to_rgba(c))


def _top(values, conf=None, tested: bool = False, q: float = 98.0) -> float:
    """How far the scale must go: the 98th percentile of |value| -- of the
    significant cells only, when there is a test and some pass."""
    v = np.abs(np.asarray(values, float))
    if tested and conf is not None:
        sig = is_significant(conf) & np.isfinite(v)
        if sig.any():
            v = v[sig]
    v = v[np.isfinite(v)]
    return float(np.percentile(v, q)) if v.size else 0.0


def _symmetric(top: float, steps) -> List[float]:
    """[-b_n .. -b_1, 0, b_1 .. b_n]: the steps up to the first that reaches
    ``top``, at most five, at least three."""
    i = next((k for k, st in enumerate(steps) if st >= top), len(steps) - 1)
    pos = list(steps[max(0, i - 4): i + 1])
    if len(pos) < 3:
        pos = list(steps[:3])
    return [-st for st in pos[::-1]] + [0.0] + pos


def _shades(palette, k: int) -> list:
    """k + 1 colours from light to dark along a palette: k steps and the one beyond."""
    idx = np.round(np.linspace(0, len(palette) - 1, k + 1)).astype(int)
    return [palette[i] for i in idx]


def _diverging(bounds, below, above):
    """A scale by steps, symmetric around 0: ``below`` the colours under 0,
    ``above`` those over it, lighter near 0, and one darker beyond each end."""
    n = (len(bounds) - 1) // 2
    lo, hi = _shades(below, n), _shades(above, n)
    cmap = ListedColormap(lo[:n][::-1] + hi[:n])
    cmap.set_under(lo[n])
    cmap.set_over(hi[n])
    return cmap, BoundaryNorm(bounds, n * 2)


def _sequential(values, n: int = 8):
    """A scale by steps for a sigma: round steps from its 2nd to 98th percentile."""
    v = np.asarray(values, float)
    v = v[np.isfinite(v)]
    lo, hi = (np.percentile(v, [2, 98]) if v.size else (0.0, 1.0))
    bounds = list(MaxNLocator(nbins=n).tick_values(lo, max(hi, lo + 1e-6)))
    vir = plt.get_cmap("viridis")
    cmap = ListedColormap([vir(x) for x in np.linspace(0.05, 0.95, len(bounds) - 1)])
    cmap.set_under(vir(0.0))
    cmap.set_over(vir(1.0))
    return cmap, BoundaryNorm(bounds, len(bounds) - 1), bounds


def _rgba(values, cmap, norm, conf=None, tested: bool = False) -> np.ndarray:
    """Cells as colours: white without data; with a test, grey where it does
    not pass and the colour of the change where it does."""
    v = np.asarray(values, float)
    img = cmap(norm(np.nan_to_num(v)))
    if isinstance(norm, BoundaryNorm) and norm.boundaries[0] < 0 < norm.boundaries[-1]:
        # no change at all is neither side of a symmetric scale
        img[np.isfinite(v) & (np.abs(v) < 1e-12)] = _hex(ZERO)
    if tested:
        img[np.isfinite(v) & ~is_significant(conf)] = _hex(NOISE)
    img[~np.isfinite(v)] = _hex(EMPTY)
    return img


def _scale(kind, arrays):
    """One colour scale for the same panel of several runs: (cmap, norm, bounds)."""
    v = np.concatenate([np.ravel(np.asarray(a, float)) for a in arrays])
    v = v[np.isfinite(v)]
    if kind == "bias":
        bounds = _symmetric(_top(v), STEPS_UNIT)
        return (*_diverging(bounds, BLUES, REDS), bounds)
    if kind == "sigma":
        return _sequential(v)
    return (plt.get_cmap("Greys"),
            Normalize(0.0, max(np.percentile(v, 98) if v.size else 1.0, 1.0)), None)


def _panel(values, kind, unit, conf=None, tested=False, period=None, period_conf=None,
           row=None, scale=None):
    """What a panel draws: the RGBA image, the colour scale (its steps), and
    the numbers the mouse gives. ``row`` is the value of every channel over
    the period (the period column of a comparison, or the mouse of one run)."""
    bounds = None
    if scale is not None:                 # shared by the runs of a selection
        cmap, norm, bounds = scale
        if kind == "count":
            unit = ""
    elif kind == "bias":                  # one run: blue below 0, red above
        bounds = _symmetric(_top(values), STEPS_UNIT)
        cmap, norm = _diverging(bounds, BLUES, REDS)
    elif kind == "sigma":
        cmap, norm, bounds = _sequential(values)
    elif kind == "count":
        v = np.asarray(values, float)[np.isfinite(values)]
        cmap = plt.get_cmap("Greys")
        norm = Normalize(0.0, max(np.percentile(v, 98) if v.size else 1.0, 1.0))
        unit = ""
    elif kind == "count_change":          # fewer orange, more purple
        bounds = _symmetric(_top(values), STEPS_COUNT)
        cmap, norm = _diverging(bounds, FEWER, MORE)
    else:                                 # a change: red where Exp is better
        bounds = _symmetric(_top(values, conf, tested), STEPS_PCT if unit == "%" else STEPS_UNIT)
        cmap, norm = _diverging(bounds, REDS, BLUES)
    p = {"values": np.asarray(values, float), "conf": conf, "tested": tested, "cmap": cmap,
         "norm": norm, "label": unit, "kind": kind, "bounds": bounds,
         "rgba": _rgba(values, cmap, norm, conf, tested and kind == "change"),
         "row": None if row is None else np.asarray(row, float)}
    if period is not None:
        pv = np.asarray(period, float)[:, None]
        pc = None if period_conf is None else np.asarray(period_conf, float)[:, None]
        p["row"] = pv[:, 0]
        p["period"] = pv[:, 0]
        p["period_conf"] = None if pc is None else pc[:, 0]
        p["period_rgba"] = _rgba(pv, cmap, norm, pc, tested)
    return p


def _counts(img_panel) -> Tuple[int, int]:
    v, c = img_panel["values"], img_panel["conf"]
    if not img_panel["tested"] or c is None:
        return 0, 0
    sig = is_significant(c) & np.isfinite(v)
    return int(np.sum(sig & (v < 0))), int(np.sum(sig & (v > 0)))


def _bound_text(b: float) -> str:
    """A step as it reads: 0.05, 2, -0.1."""
    return f"{b:g}"


# ─────────────────────────────────────────────────────────────────────────────
# The figure
# ─────────────────────────────────────────────────────────────────────────────

def _date(d) -> datetime:
    return datetime.strptime(str(d), "%Y%m%d%H")


def _chan_text(v) -> str:
    try:
        f = float(v)
    except (TypeError, ValueError):
        return str(v)
    return str(int(f)) if f.is_integer() else f"{f:g}"


def _axes_labels(ax, chans, dates, show_dates: bool, show_chans: bool) -> None:
    nc, nt = len(chans), len(dates)
    k = max(1, math.ceil(nc / 22))                    # one channel named in k
    ax.set_yticks(np.arange(0, nc, k) + 0.5)
    ax.set_yticklabels([_chan_text(chans[i]) for i in range(0, nc, k)] if show_chans else [],
                       fontsize=8.5 * FS)
    step = max(1, math.ceil(nt / 7))
    ax.set_xticks(np.arange(0, nt, step) + 0.5)
    ax.set_xticklabels([f"{_date(d):%b %d}\n{_date(d):%H}Z" for d in dates[::step]]
                       if show_dates else [], fontsize=8.5 * FS)
    ax.tick_params(axis="both", length=5, width=1.2)


def _draw(fig, rect_in, fig_in, p, title, chans, dates, show_dates, show_chans, word):
    """One panel: the image, its period column, its colour bar, its title.
    Returns the axes (the image, the period column or None)."""
    fw, fh = fig_in
    x, y, w, h = rect_in                              # inches, y from the top
    period = "period_rgba" in p
    pw = 0.9 if period else 0.0
    ax = fig.add_axes([x / fw, 1 - (y + h) / fh, (w - pw - (0.2 if period else 0)) / fw, h / fh])
    nc, nt = p["rgba"].shape[:2]
    ax.imshow(p["rgba"], origin="lower", aspect="auto", interpolation="nearest",
              extent=(0, nt, 0, nc))
    _axes_labels(ax, chans, dates, show_dates, show_chans)
    if show_chans:
        ax.set_ylabel(word.capitalize(), fontsize=9 * FS)
    ax.set_title(title, loc="left", fontsize=10 * FS, pad=10)
    pax = None
    if period:
        pax = fig.add_axes([(x + w - pw) / fw, 1 - (y + h) / fh, pw / fw, h / fh])
        pax.imshow(p["period_rgba"], origin="lower", aspect="auto", interpolation="nearest",
                   extent=(0, 1, 0, nc))
        pax.set_xticks([0.5])
        pax.set_xticklabels(["period"], fontsize=8 * FS, rotation=90)
        pax.set_yticks([])
    cax = fig.add_axes([(x + w + 0.25) / fw, 1 - (y + h) / fh, 0.35 / fw, h / fh])
    if p["bounds"] is not None:
        # one colour per step, every step named, darker beyond the ends
        cb = fig.colorbar(ScalarMappable(norm=p["norm"], cmap=p["cmap"]), cax=cax,
                          extend="both", ticks=p["bounds"], spacing="uniform")
        cb.ax.set_yticklabels([_bound_text(b) for b in p["bounds"]])
    else:
        cb = fig.colorbar(ScalarMappable(norm=p["norm"], cmap=p["cmap"]), cax=cax)
        cb.ax.yaxis.set_major_formatter(count_formatter())
    cb.ax.tick_params(labelsize=8 * FS)
    if p["label"]:
        cb.set_label(p["label"], fontsize=9 * FS)
    return ax, pax


def _header(fig, fig_in, task, variable, unit, n_chans, word, on, compared) -> None:
    fw, fh = fig_in
    kind = "scorecard" if compared else "resume"

    def yy(inch):
        return 1.0 - inch * FS / fh

    land = task.get("land_ocean", "all")
    sp = task.get("special_label", "all")
    parts = [task["family"],
             task["region"] if land in (None, "", "all") else f"{task['region']} ({land})",
             f"flag {task['flag_criteria']}", f"station {task['id_stn']}",
             f"{n_chans} {word}s"]
    if sp not in (None, "", "all"):
        parts.append(f"method {sp}")
    x0, y = 0.06, 0.85
    fig.text(x0, yy(0.15), f"{task['family']}_{kind}   ·   {variable} {unit}", ha="left",
             va="top", fontsize=15 * FS, fontweight="bold", color="#1F2933")
    fig.text(x0, yy(0.50), "  ·  ".join(parts), ha="left", va="top", fontsize=11 * FS,
             color=GREY_TEXT)
    if task.get("role") == "ctl":
        who = [("Ctl", task["experience"], CTL_COLOUR)]
    else:
        who = [("Exp", task["experience"], EXP_COLOUR)]
    if compared:
        who.append(("Ctl", task["control"], CTL_COLOUR))
    for label, name, colour in who:
        fig.text(x0, yy(y), f"{label}  {name}", ha="left", va="top", fontsize=12 * FS,
                 fontweight="bold", color=colour)
        y += 0.26
    s, e = str(task["datestart"]), str(task["dateend"])
    fig.text(x0, yy(y), f"{s[:4]}-{s[4:6]}-{s[6:8]} {s[8:10]} UTC  to  "
             f"{e[:4]}-{e[4:6]}-{e[6:8]} {e[8:10]} UTC", ha="left", va="top",
             fontsize=10 * FS, color=GREY_TEXT)
    y += 0.26
    if compared:
        mode = task.get("match_mode")
        if mode == "no":
            note = "MATCH no: the changes, no test -- red where Exp is better, blue where Ctl is"
        else:
            note = (f"only the cells whose change passes the test ({MIN_CONFIDENCE:.0f} %) are "
                    f"coloured: red where Exp is better, blue where Ctl is, grey is noise; the "
                    f"'period' column tests the whole period"
                    + (f" (from {BOOT_MIN_CYCLES} cycles)" if on else ""))
        fig.text(x0, yy(y), note, ha="left", va="top", fontsize=9.5 * FS, color=GREY_TEXT)
        badge = None
        if mode != "no":
            badge = match_badge(fig, on, top_in=0.12 * FS,
                                method=("cells: t-test, F-test · period: cycle bootstrap"
                                        if on else None))
        # no line of the header under the badge, however long the family name
        fit_texts(fig, badge)
    else:
        fig.text(x0, yy(y), f"in the viewer the mouse gives the {word} and its value over the "
                 f"period; the HTML beside the PNG gives every cell", ha="left",
                 va="top", fontsize=9.5 * FS, color=GREY_TEXT)


def summary_plot(task: Dict[str, Any]) -> Optional[str]:
    """The summary of one selection; returns the path of its PNG, or None
    when there is nothing to summarise (one channel only, no data)."""
    compared = bool(task.get("db_control"))
    mode = task.get("match_mode") or ""
    on = compared and mode == "on"
    if on:
        grid = _pair_grid(task) if task.get("db_pairs") else None
        if grid is None:
            return None
        chans, dates, g = grid
        data = _scorecard_on(g)
    elif compared:
        a, b = _run_grid(task, task["db_control"]), _run_grid(task, task["db_file"])
        if a is None or b is None:
            return None
        chans, dates, gc, ge = _on_union(a, b, _pressure(task))
        data = _scorecard_off(gc, ge, tested=(mode != "no"))
    else:
        grid = _run_grid(task, task["db_file"])
        if grid is None:
            return None
        chans, dates, g = grid
        data = _resume_panels(g)
    if len(chans) < 2 or not any(t in data for t in ("omp", "oma")):
        return None
    return _figure(task, chans, dates, data, compared, on, mode)


def resume_group(task: Dict[str, Any]) -> List[Dict[str, str]]:
    """The resume of every run of a selection: the control and each
    experience, each its own figure, all on the same colour scales."""
    runs = []
    for name, db, role in task["runs"]:
        grid = _run_grid(task, db) if db and os.path.isfile(db) else None
        if grid is None or len(grid[0]) < 2:
            continue
        chans, dates, g = grid
        data = _resume_panels(g)
        if any(t in data for t in ("omp", "oma")):
            runs.append((name, db, role, chans, dates, data))
    if not runs:
        return []
    scales = {"n": _scale("count", [d["n"] for *_, d in runs])}
    for tag in ("omp", "oma"):
        for q in ("bias", "sigma"):
            arrays = [d[tag][q] for *_, d in runs if tag in d]
            if arrays:
                scales[(tag, q)] = _scale(q, arrays)
    out = []
    for name, db, role, chans, dates, data in runs:
        t = dict(task, experience=name, db_file=db, role=role, kind="resume")
        png = _figure(t, chans, dates, data, False, False, "", scales)
        out.append(_entry(t, png))
    return out


def _figure(task, chans, dates, data, compared, on, mode, scales=None) -> str:
    """Draw a summary from its numbers: the PNG, its mouse map and its HTML."""
    family, varno = task["family"], task["varno"]
    try:
        variable, unit, _ = pikobs.type_varno(f"{varno}")
    except Exception:
        variable, unit = f"varno {varno}", ""
    try:
        word = "channel" if str(pikobs.family(family)[5]).upper() == "CANAL" else "level"
    except Exception:
        word = "channel"
    tested = compared and mode != "no"

    # the panels: a row per departure, bias on the left and sigma on the
    # right, and the counts across the bottom
    rows = []
    for tag, name in (("omp", "O-P"), ("oma", "O-A")):
        if tag not in data:
            continue
        d = data[tag]
        if compared:
            left = _panel(d["bias"], "change", unit, d.get("bias_conf"), tested,
                          d["bias_period"], d.get("bias_period_conf"))
            right = _panel(d["sigma"], "change", "%", d.get("sigma_conf"), tested,
                           d["sigma_period"], d.get("sigma_period_conf"))
            titles = [f"Bias of {name}: |Exp| - |Ctl|", f"Sigma of {name}: (Exp - Ctl) / Ctl"]
            left["short"], right["short"] = f"bias {name}", f"sigma {name}"
            for p, t in zip((left, right), titles):
                n_exp, n_ctl = _counts(p)
                p["title"] = (t + (f"\n{n_exp} cells Exp better  ·  {n_ctl} Ctl better"
                                   if tested else "\nno test"))
        else:
            sc = scales or {}
            left = _panel(d["bias"], "bias", unit, row=d["bias_period"],
                          scale=sc.get((tag, "bias")))
            right = _panel(d["sigma"], "sigma", unit, row=d["sigma_period"],
                           scale=sc.get((tag, "sigma")))
            left["title"], right["title"] = f"Bias of {name} (mean)", f"Sigma of {name}"
            left["short"], right["short"] = f"bias {name}", f"sigma {name}"
        rows.append((tag, left, right))
    if compared and data.get("n_kind") == "change":
        bottom = _panel(data["n"], "count_change", "%", row=data["n_period"])
        bottom["title"] = ("Data: how many more (purple) or fewer (orange) observations Exp "
                           "has than Ctl, in %  --  neither better nor worse")
    else:
        bottom = _panel(data["n"], "count", "", row=data["n_period"],
                        scale=(scales or {}).get("n") if not compared else None)
        bottom["title"] = ("Data: the pairs each cell is computed from (observations "
                           "both runs kept)  --  white: none" if compared
                           else f"Data: the observations of each {word} and cycle  --  "
                           f"white: none")

    bottom["short"] = "data"
    nc = len(chans)
    header_in = (1.75 if compared else 1.5) * FS
    panel_h = float(np.clip(5.0 + nc * 0.012, 6.0, 11.0))
    gap_in = 2.6 * FS / 2.5
    left_in, mid_in, right_in = 3.4, 3.6, 2.8
    fig_w = 34.0
    col_w = (fig_w - left_in - mid_in - right_in) / 2.0
    n_rows = len(rows) + 1
    fig_h = header_in + 1.2 + n_rows * (panel_h + gap_in)
    fig = plt.figure(figsize=(fig_w, fig_h), facecolor="white")
    fig_in = (fig_w, fig_h)
    _header(fig, fig_in, task, variable, unit, nc, word, on, compared)

    y = header_in + 1.2
    drawn = []
    for r, (tag, left, right) in enumerate(rows):
        for c, p in enumerate((left, right)):
            x = left_in + c * (col_w + mid_in)
            ax, pax = _draw(fig, (x, y, col_w, panel_h), fig_in, p, p["title"], chans, dates,
                            show_dates=True, show_chans=True, word=word)
            drawn.append((ax, pax, p))
        y += panel_h + gap_in
    ax, _ = _draw(fig, (left_in, y, 2 * col_w + mid_in, panel_h), fig_in, bottom,
                  bottom["title"], chans, dates, show_dates=True, show_chans=True, word=word)
    drawn.append((ax, None, bottom))

    out_dir = os.path.join(task["pathwork"], family)
    os.makedirs(out_dir, exist_ok=True)
    png = os.path.join(out_dir, summary_name(task))
    from pikobs.figures.figures import members_footer
    members_footer(fig, task.get('selector'))
    save_figure(fig, png, svg=task.get("svg", False), dpi=DPI)
    _mouse_map(fig, png, drawn, chans, dates, word)
    plt.close(fig)
    _write_html(png, task, chans, dates, rows, bottom, variable, unit, word, compared, on, mode)
    return png


def _value_text(p, v) -> str:
    """A value as the mouse says it."""
    if not np.isfinite(v):
        return "no data"
    if p["kind"] == "count":
        return f"{int(round(v))} obs"
    if p["kind"] in ("change", "count_change", "bias"):
        return f"{v:+.3g} {p['label']}".strip()
    return f"{v:.3g} {p['label']}".strip()


def _mouse_map(fig, png, drawn, chans, dates, word) -> None:
    """The viewer's mouse. A small grid (a few levels): every cell gives its
    channel, cycle, value and test. A large one (hundreds of channels): every
    row gives its channel and its value over the period, with its test --
    the cells of every cycle are in the HTML."""
    n_cells = sum(len(chans) * len(dates) for _ in drawn)
    per_cell = n_cells <= 25000
    rects = []
    for ax, pax, p in drawn:
        tested = p["tested"] and p["kind"] == "change"
        for a, is_period in ((ax, False), (pax, True)):
            if a is None:
                continue
            for i, c in enumerate(chans):
                y0 = a.transData.transform((0, i))[1]
                y1 = a.transData.transform((0, i + 1))[1]
                head = f"{p.get('short', '')}  ·  {word} {_chan_text(c)}"
                if is_period or not per_cell:
                    e = a.get_window_extent()
                    row = p.get("row")
                    v = row[i] if row is not None else np.nan
                    text = f"{head}  ·  period: {_value_text(p, v)}"
                    if tested:
                        conf = p["period_conf"][i] if p.get("period_conf") is not None else np.nan
                        text += "  ·  " + _verdict(v, conf, True, "")
                    rects.append((e.x0, y0, e.x1, y1, text))
                    continue
                for j, d in enumerate(dates):
                    x0 = a.transData.transform((j, 0))[0]
                    x1 = a.transData.transform((j + 1, 0))[0]
                    v = p["values"][i, j]
                    text = f"{head}  ·  {_date(d):%Y-%m-%d %H}Z  ·  {_value_text(p, v)}"
                    if tested:
                        text += "  ·  " + _verdict(v, p["conf"][i, j], True, "")
                    rects.append((x0, y0, x1, y1, text))
    write_hover_rects(fig, png, rects, dpi=DPI)


def _verdict(value, conf, tested, unit="") -> str:
    """What the test says of a change."""
    if not np.isfinite(value):
        return "no data"
    if not tested:
        return "no test"
    if not np.isfinite(conf):
        return "not tested (too few cycles)"
    if conf > MIN_CONFIDENCE:
        return f"{'Exp' if value < 0 else 'Ctl'} better ({conf:.1f} %)"
    return f"no clear change ({conf:.1f} %)"


# ─────────────────────────────────────────────────────────────────────────────
# The HTML: the same panels, the channel, the cycle and the value under the mouse
# ─────────────────────────────────────────────────────────────────────────────

def _png_uri(rgba) -> str:
    buf = io.BytesIO()
    plt.imsave(buf, np.ascontiguousarray(rgba[::-1]), format="png")   # row 0 at the bottom
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def _legend(p) -> Dict[str, Any]:
    """The colour scale of a panel for the HTML: its steps, or a gradient."""
    if p["bounds"] is None:
        lo, hi = float(p["norm"].vmin), float(p["norm"].vmax)
        cols = [matplotlib.colors.to_hex(p["cmap"](p["norm"](x))) for x in np.linspace(lo, hi, 9)]
        return {"grad": "linear-gradient(to right, " + ", ".join(cols) + ")",
                "labels": [f"{lo:g}", f"{hi:g}"]}
    cm = p["cmap"]
    n = len(p["bounds"]) - 1
    cols = ([matplotlib.colors.to_hex(cm.get_under())]
            + [matplotlib.colors.to_hex(cm(k)) for k in range(n)]
            + [matplotlib.colors.to_hex(cm.get_over())])
    return {"steps": cols, "labels": [_bound_text(b) for b in p["bounds"]]}


def _num(a, digits: int = 4):
    """A grid as JSON: rounded, null where there is no value."""
    a = np.asarray(a, float)
    out = []
    for row in a:
        out.append([None if not np.isfinite(v) else float(f"{v:.{digits}g}") for v in row])
    return out


def _write_html(png, task, chans, dates, rows, bottom, variable, unit, word, compared, on, mode):
    panels = []
    for tag, left, right in rows:
        for p in (left, right):
            panels.append(p)
    panels.append(bottom)
    spec = []
    for k, p in enumerate(panels):
        item = {"id": k, "title": p["title"].replace("\n", " · "), "unit": p["label"],
                "kind": p["kind"], "tested": bool(p["tested"]), "img": _png_uri(p["rgba"]),
                "legend": _legend(p), "values": _num(p["values"]), "wide": p is bottom}
        if p.get("row") is not None:
            item["row"] = [None if not np.isfinite(v) else float(f"{v:.4g}") for v in p["row"]]
        if p.get("conf") is not None:
            item["conf"] = _num(p["conf"], 3)
        if "period_rgba" in p:
            item["period_img"] = _png_uri(p["period_rgba"])
            item["period"] = [None if not np.isfinite(v) else float(f"{v:.4g}") for v in p["period"]]
            pc = p.get("period_conf")
            item["period_conf"] = (None if pc is None else
                                   [None if not np.isfinite(v) else round(float(v), 1) for v in pc])
        spec.append(item)
    kind = "scorecard" if compared else "resume"
    head = {
        "title": f"{task['family']}_{kind} · {variable} {unit}",
        "exp": task["experience"], "ctl": task.get("control") if compared else None,
        "role": task.get("role", "exp"),
        "selection": " · ".join(str(x) for x in (task["region"], f"flag {task['flag_criteria']}",
                                                  f"station {task['id_stn']}")),
        "dates": [f"{_date(d):%Y-%m-%d %H}Z" for d in dates],
        "chans": [_chan_text(c) for c in chans], "word": word,
        "match": (mode if compared else ""), "min_conf": MIN_CONFIDENCE,
        "exp_colour": EXP_COLOUR, "ctl_colour": CTL_COLOUR,
    }
    page = (_HTML.replace("__TITLE__", html.escape(head["title"]))
                 .replace("__DATA__", json.dumps({"head": head, "panels": spec},
                                                 separators=(",", ":"))))
    with open(png[:-len(".png")] + ".html", "w", encoding="utf-8") as fh:
        fh.write(page)


_HTML = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>__TITLE__</title>
<style>
 body{font-family:"DejaVu Sans",Arial,sans-serif;margin:18px 26px;color:#1F2933;background:#fff}
 h1{font-size:22px;margin:0 0 4px} .sub{color:#5F6B76;font-size:14px;margin-bottom:6px}
 .runs span{font-weight:bold;margin-right:22px;font-size:15px}
 #tip{position:sticky;top:0;z-index:5;background:#F3F5F7;border:1px solid #D9DDE2;border-radius:6px;
      padding:9px 14px;font-size:15px;min-height:22px;margin:10px 0 14px}
 .grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:26px 34px}
 .wide{grid-column:1 / span 2} .ptitle{font-size:14px;margin-bottom:5px;color:#30343A}
 .row{display:flex;gap:6px;align-items:stretch} .wrap{position:relative;flex:1;cursor:crosshair}
 .wrap img{width:100%;height:100%;display:block;image-rendering:pixelated;border:1px solid #D9DDE2}
 .per{position:relative;width:34px;cursor:crosshair}
 .per img{width:100%;height:100%;display:block;image-rendering:pixelated;border:1px solid #D9DDE2}
 .hl{position:absolute;left:0;right:0;height:0;border-top:1px solid rgba(0,0,0,.65);pointer-events:none;display:none}
 .vl{position:absolute;top:0;bottom:0;width:0;border-left:1px solid rgba(0,0,0,.65);pointer-events:none;display:none}
 .bar{height:12px;border-radius:3px;margin-top:5px} .scale{display:flex;justify-content:space-between;font-size:12px;color:#5F6B76}
 .steps{display:flex;height:14px;margin-top:6px} .steps span{flex:1;border-right:1px solid #fff}
 .ticks{position:relative;height:16px;font-size:12px;color:#5F6B76}
 .ticks span{position:absolute;transform:translateX(-50%)} .steps,.ticks{margin-left:54px}
 .axis{display:flex;justify-content:space-between;font-size:12px;color:#5F6B76;margin-top:2px}
 .note{color:#5F6B76;font-size:13px;margin-top:4px}
 .lab{position:relative;width:48px;font-size:11px;color:#5F6B76}
 .lab span{position:absolute;right:5px;transform:translateY(-50%)}
 .axis,.bar,.scale{margin-left:54px}
</style></head><body>
<h1 id="h"></h1><div class="sub" id="sel"></div><div class="runs" id="runs"></div>
<div class="note" id="note"></div>
<div id="tip">Move the mouse over a cell.</div>
<div class="grid" id="grid"></div>
<script>
const D=__DATA__, H=D.head, NC=H.chans.length, NT=H.dates.length;
const fmt=(v,u)=>v===null||v===undefined?"no data":(Math.abs(v)>=1000?v.toFixed(0):(+v).toPrecision(4))+(u?" "+u:"");
document.getElementById("h").textContent=H.title;
document.getElementById("sel").textContent=H.selection+" · "+NC+" "+H.word+"s · "+H.dates[0]+" to "+H.dates[NT-1];
let r=H.role==="ctl"?'<span style="color:'+H.ctl_colour+'">Ctl '+H.exp+'</span>':'<span style="color:'+H.exp_colour+'">Exp '+H.exp+'</span>';
if(H.ctl) r+='<span style="color:'+H.ctl_colour+'">Ctl '+H.ctl+'</span>';
document.getElementById("runs").innerHTML=r;
document.getElementById("note").textContent=H.ctl?(H.match==="no"?"MATCH no: the changes, no test.":
 "MATCH "+H.match+": only the cells whose change passes the test ("+H.min_conf+" %) are coloured, red where Exp is better, blue where Ctl is; grey is noise."):
 "One run: the bias and the sigma per "+H.word+" and cycle.";
const tip=document.getElementById("tip"), lines=[];
function verdict(v,c,tested){
 if(v===null) return "no data";
 if(!tested) return "no test";
 if(c===null||c===undefined) return "not tested";
 return c>H.min_conf?((v<0?"Exp":"Ctl")+" better ("+c.toFixed(1)+" %)"):("not significant ("+c.toFixed(1)+" %)");
}
function show(i,j){
 for(const l of lines){l.h.style.display="block";l.h.style.top=((NC-1-i+0.5)/NC*100)+"%";
  if(l.v){if(j===null){l.v.style.display="none"}else{l.v.style.display="block";l.v.style.left=((j+0.5)/NT*100)+"%"}}}
}
function hide(){for(const l of lines){l.h.style.display="none";if(l.v)l.v.style.display="none"}}
D.panels.forEach(p=>{
 const box=document.createElement("div"); if(p.wide) box.className="wide";
 const h=Math.max(260,Math.min(720,NC*2.2));
 box.innerHTML='<div class="ptitle">'+p.title+'</div>';
 const row=document.createElement("div"); row.className="row"; row.style.height=h+"px";
 const lab=document.createElement("div"); lab.className="lab";
 const stp=Math.max(1,Math.ceil(NC/12)); let ls="";
 for(let i=0;i<NC;i+=stp){ls+='<span style="top:'+((NC-1-i+0.5)/NC*100)+'%">'+H.chans[i]+'</span>'}
 lab.innerHTML=ls; row.appendChild(lab);
 const wrap=document.createElement("div"); wrap.className="wrap";
 wrap.innerHTML='<img src="'+p.img+'"><div class="hl"></div><div class="vl"></div>';
 row.appendChild(wrap);
 const ln={h:wrap.querySelector(".hl"),v:wrap.querySelector(".vl")}; lines.push(ln);
 let per=null;
 if(p.period_img){per=document.createElement("div");per.className="per";per.title="period";
  per.innerHTML='<img src="'+p.period_img+'"><div class="hl"></div>';row.appendChild(per);lines.push({h:per.querySelector(".hl"),v:null});}
 box.appendChild(row);
 let leg='<div class="axis"><span>'+H.dates[0]+'</span><span>cycles</span><span>'+H.dates[NT-1]+'</span></div>';
 if(p.legend.steps){const L=p.legend, nb=L.steps.length;
  leg+='<div class="steps">'+L.steps.map(c=>'<span style="background:'+c+'"></span>').join("")+'</div><div class="ticks">'+
   L.labels.map((t,k)=>'<span style="left:'+((k+1)/nb*100)+'%">'+t+'</span>').join("")+'</div>'+
   '<div class="scale"><span></span><span>'+(p.unit||"")+'</span><span></span></div>';}
 else leg+='<div class="bar" style="background:'+p.legend.grad+'"></div><div class="scale"><span>'+p.legend.labels[0]+'</span><span>'+(p.unit||"")+'</span><span>'+p.legend.labels[1]+'</span></div>';
 box.insertAdjacentHTML("beforeend",leg);
 document.getElementById("grid").appendChild(box);
 wrap.addEventListener("mousemove",e=>{
  const b=wrap.getBoundingClientRect();
  const j=Math.min(NT-1,Math.max(0,Math.floor((e.clientX-b.left)/b.width*NT)));
  const i=Math.min(NC-1,Math.max(0,NC-1-Math.floor((e.clientY-b.top)/b.height*NC)));
  const v=p.values[i][j]; let t=H.word+" "+H.chans[i]+"  ·  "+H.dates[j]+"  ·  ";
  const pr=p.row?"   (period: "+(p.kind==="count"?(p.row[i]===null?"no data":Math.round(p.row[i])+" obs"):fmt(p.row[i],p.unit))+")":"";
  if(p.kind==="change"){t+=fmt(v,p.unit)+"  ·  "+verdict(v,p.conf?p.conf[i][j]:null,p.tested)}
  else t+=(p.kind==="count"?(v===null?"no data":Math.round(v)+" obs"):fmt(v,p.unit));
  tip.textContent=p.title+"  —  "+t+pr; show(i,j);
 });
 wrap.addEventListener("mouseleave",hide);
 if(per){per.addEventListener("mousemove",e=>{
  const b=per.getBoundingClientRect();
  const i=Math.min(NC-1,Math.max(0,NC-1-Math.floor((e.clientY-b.top)/b.height*NC)));
  const v=p.period[i];
  tip.textContent=p.title+"  —  "+H.word+" "+H.chans[i]+"  ·  whole period  ·  "+fmt(v,p.unit)+"  ·  "+
   verdict(v,p.period_conf?p.period_conf[i]:null,p.tested); show(i,null);
 }); per.addEventListener("mouseleave",hide);}
});
</script></body></html>
"""


# ─────────────────────────────────────────────────────────────────────────────
# The index of the interactive pages, linked from the viewer
# ─────────────────────────────────────────────────────────────────────────────

INDEX = "pikobs_cardio_summaries.html"


def _written(results) -> List[Dict[str, str]]:
    return [e for r in results if r for e in r if e and e.get("png")]


def write_index(pathwork: str, tasks, results) -> Optional[str]:
    """One page listing every summary written, each linked to its HTML."""
    rows = []
    for e in sorted(_written(results), key=lambda e: (e["family"], e["region"], e["flag_criteria"],
                                                      e["kind"], e["experience"])):
        rel = os.path.relpath(e["png"][:-len(".png")] + ".html", pathwork)
        cells = [e["experience"], e["family"], e["region"], e["land_ocean"], e["flag_criteria"],
                 e["id_stn"], e["special"], e["varno"], e["match"] or "-"]
        rows.append("<tr>" + "".join(f"<td>{html.escape(str(c))}</td>" for c in cells)
                    + f'<td><a href="{html.escape(rel)}">{html.escape(os.path.basename(rel))}</a></td></tr>')
    if not rows:
        return None
    heads = ["Experience", "Family", "Region", "Surface", "Criteria", "Station", "Special",
             "Varno", "Match", "Page"]
    page = ("<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'><title>Pikobs cardio: "
            "channel summaries</title><style>body{font-family:'DejaVu Sans',Arial,sans-serif;"
            "margin:20px 28px;color:#1F2933}table{border-collapse:collapse;font-size:14px}"
            "td,th{border-bottom:1px solid #E1E4E8;padding:6px 12px;text-align:left}"
            "th{background:#F3F5F7}</style></head><body><h2>Channel summaries</h2>"
            "<p style='color:#5F6B76'>Every channel of a selection at a glance: the mouse gives "
            "the channel, the cycle and the value of each cell.</p><table><tr>"
            + "".join(f"<th>{h}</th>" for h in heads) + "</tr>" + "".join(rows)
            + "</table></body></html>")
    path = os.path.join(pathwork, INDEX)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(page)
    return path


def viewer_items(tasks, results, chan_text) -> List[Dict[str, str]]:
    """The summaries in the cardio viewer, as the channel 'summary'."""
    return [{"experience": e["experience"], "flag_criteria": e["flag_criteria"],
             "family": e["family"], "region": e["region"], "land_ocean": e["land_ocean"],
             "special": e["special"], "id_stn": e["id_stn"], "varno": e["varno"],
             "vcoord": SUMMARY, "match": e["match"], "filename": os.path.basename(e["png"])}
            for e in _written(results)]
