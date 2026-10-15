#!/usr/bin/python3
"""Figures of pikobs.timeserie.

For every run: the observations of every cycle, stacked by what the
quality control did with them, and -- only when the files carry them --
the mean and the sigma of the departures, the assigned error and the
bias correction. With a control, one more figure with every run on the
same axes and the change of the number of assimilated observations.
"""

import os
import textwrap
import re
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

import matplotlib as mpl

mpl.use("Agg")
import matplotlib.dates as mdates
import matplotlib.patches
import matplotlib.transforms as mtransforms
import matplotlib.pyplot as plt
import numpy as np

import pikobs
from pikobs.figures import match_badge, save_figure
from pikobs.obsdb import open_result
from pikobs.stats import (MIN_CONFIDENCE,
                          is_significant, sigma_confidence,
                          ttest_confidence)

from pikobs.configobs.style import (
    font_size,
    CTL_BETTER,
    CTL_COLOUR,
    EXP_BETTER,
    GREY_TEXT,
    DPI,
    EXP_COLOUR,
    EXP_COLOURS,
    GREY_TEXT as _GREY,
    QC_ASSIMILATED,
    QC_BLUES,
    QC_OTHER,
    QC_PALETTE,
    STATION_CMAP,
    STYLE,
)
from pikobs.obsdb import safe_name as _safe

# every combination that carries bit 12 (the observation entered the
# analysis) is drawn in blues, from light to dark; everything else in
# its own colour, so a glance separates what was used from what was not
MAX_DIAGNOSES = 8
#: every text of a time series, and the room of its header, is 'size * FS':
#: FS gives the title (17 pt) the shared size (style.font_size)
FS = font_size("title") / 17.0
_STYLE = dict(STYLE, **{"axes.titlesize": STYLE.get("axes.titlesize", 11) * FS,
                        "axes.labelsize": STYLE.get("axes.labelsize", 10) * FS,
                        "legend.fontsize": STYLE.get("legend.fontsize", 8.5) * FS,
                        "xtick.labelsize": 10 * FS, "ytick.labelsize": 10 * FS})


def _pct(share: float) -> str:
    """'<0.1 %' instead of a 0.0 % that looks like nothing at all."""
    if share <= 0:
        return "0 %"
    return "<0.1 %" if share < 0.05 else f"{share:.1f} %"


def _bits(sig: int) -> str:
    return "+".join(str(b) for b in range(24) if int(sig) >> b & 1) or "none"


def _reason(sig: int) -> str:
    try:
        from pikobs.configobs.flags_criteria import flag_reason

        return (flag_reason(int(sig)) or "NO QC FLAG").title()
    except Exception:  # pragma: no cover
        return f"flag {sig}"


# ─────────────────────────────────────────────────────────────────────────────
# Reading
# ─────────────────────────────────────────────────────────────────────────────


def _sp_tag(spec) -> str:
    """The special value in a file name, only when there is one."""
    sp = spec.get("special_label", "all")
    return "" if sp in (None, "", "all") else f"_{_safe(sp)}"


def _sp_txt(spec) -> str:
    """The special value in a title, only when there is one."""
    sp = spec.get("special_label", "all")
    return "" if sp in (None, "", "all") else f"   •   {sp}"


def _layer_units(family):
    """(factor from the unit of the layers to that of lev, unit name) for a
    family whose levels are pressures or heights; None for channels. The
    same as scatter, which owns the layers."""
    from pikobs.configobs.levels import layer_unit as _layer_unit, vcotyp as _vcotyp, needs_layers
    from pikobs.configobs.levels import layer_unit_scale

    vcotyp = _vcotyp(family)
    if not needs_layers(vcotyp):
        return None
    return layer_unit_scale(vcotyp), _layer_unit(vcotyp)


def _layer_bounds(spec):
    """(low, high) of lev for a layer level such as '2 | 850-500 hPa', else
    None. A layer keeps its larger number, as in scatter: low < lev <= high."""
    units = _layer_units(spec["family"])
    m = re.fullmatch(r"\d+ \| ([0-9.]+)-([0-9.]+) (hPa|km)", str(spec["level"]))
    if not units or not m:
        return None
    a, b = float(m.group(1)) * units[0], float(m.group(2)) * units[0]
    return min(a, b), max(a, b)


def _where(spec) -> Tuple[str, list]:
    w = (
        "region = ? AND flag = ? AND land_ocean = ? AND special = ? "
        "AND varno = ?" + spec["stn_sql"]
    )
    args = [
        spec["region"],
        spec["flag"],
        spec["surface"],
        spec.get("special", "all"),
        spec["varno"],
    ]
    layer = _layer_bounds(spec)
    if layer:
        # a layer keeps its larger number, as in scatter: low < lev <= high
        w += " AND lev > ? AND lev <= ?"
        args += list(layer)
    elif spec["level"] != "join":
        w += " AND lev = ?"
        args.append(float(spec["level"]))
    return w, args


def read_counts(spec, db):
    """(cycles, {combination: per cycle}, assimilated, {combination: n})."""
    where, args = _where(spec)
    with open_result(db) as conn:
        rows = conn.execute(
            f"SELECT cycle, sig, SUM(n) FROM ts_qc WHERE " f"{where} GROUP BY cycle, sig;", args
        ).fetchall()
    cycles = spec["cycles"]
    idx = {c: i for i, c in enumerate(cycles)}
    by: Dict[int, np.ndarray] = {}
    combos: Dict[int, float] = {}
    assim = np.zeros(len(cycles))
    for cyc, sig, n in rows:
        if cyc not in idx:
            continue
        by.setdefault(int(sig), np.zeros(len(cycles)))[idx[cyc]] += n or 0
        combos[int(sig)] = combos.get(int(sig), 0.0) + (n or 0)
        if int(sig) & 4096:
            assim[idx[cyc]] += n or 0
    return cycles, by, assim, combos


def _member_key(spec, db) -> str:
    """What a member is here: the instrument type on a composite family
    when the data holds more than one, the station otherwise."""
    if spec.get("member_word") != "type":
        return "id_stn"
    where, args = _where(spec)
    try:
        with open_result(db) as conn:
            n = conn.execute(
                f"SELECT COUNT(DISTINCT codtyp) FROM ts_qc " f"WHERE {where};", args
            ).fetchone()[0]
    except Exception:
        return "id_stn"
    return "codtyp" if (n or 0) > 1 else "id_stn"


def _member_name(col: str, key) -> str:
    if col != "codtyp":
        return str(key)
    from pikobs.stations.stations import codtyp_name as _codtyp_name

    return f"{_codtyp_name(int(key))} ({int(key)})"


def read_by_station(spec, db, top: int = 10):
    """Over the whole period, per member: how many observations it brings
    and what quality control did with them. [(member, n, {diag: n})]."""
    where, args = _where(spec)
    col = _member_key(spec, db)
    with open_result(db) as conn:
        rows = conn.execute(
            f"SELECT {col}, sig, SUM(n) FROM ts_qc WHERE " f"{where} GROUP BY {col}, sig;", args
        ).fetchall()
    per: Dict[str, Dict[str, float]] = {}
    for key, sig, n in rows:
        stn = _member_name(col, key)
        per.setdefault(stn, {})
        d = per[stn]
        lab = _reason(sig)
        d[lab] = d.get(lab, 0.0) + (n or 0)
    out = sorted(((stn, sum(d.values()), d) for stn, d in per.items()), key=lambda t: -t[1])
    return out[:top], out[top:]


def read_counts_by_member(spec, db):
    """The observations per cycle of every station -- or of every
    instrument type, on ai, ua, sf, gp and csr, where a station is one
    report and the type is what the eye follows."""
    col = _member_key(spec, db)
    where, args = _where(spec)
    with open_result(db) as conn:
        rows = conn.execute(
            f"SELECT cycle, {col}, SUM(n) FROM ts_qc WHERE " f"{where} GROUP BY cycle, {col};",
            args,
        ).fetchall()
    cycles = spec["cycles"]
    idx = {c: i for i, c in enumerate(cycles)}
    by: Dict[str, np.ndarray] = {}
    for cyc, key, n in rows:
        if cyc not in idx:
            continue
        by.setdefault(_member_name(col, key), np.zeros(len(cycles)))[idx[cyc]] += n or 0
    return by


def read_values(spec, db) -> Optional[Dict[str, np.ndarray]]:
    """Per cycle: mean and sigma of O-P and O-A, mean assigned error,
    mean bias correction; None if the files carry none of them."""
    where, args = _where(spec)
    with open_result(db) as conn:
        rows = conn.execute(
            f"SELECT cycle, SUM(n_omp), SUM(s_omp), SUM(s2_omp), SUM(n_oma), "
            f"SUM(s_oma), SUM(s2_oma), SUM(n_err), SUM(s_err), SUM(n_bc), "
            f"SUM(s_bc) FROM ts_val WHERE {where} GROUP BY cycle;",
            args,
        ).fetchall()
    if not rows:
        return None
    cycles = spec["cycles"]
    idx = {c: i for i, c in enumerate(cycles)}
    keys = ("m_omp", "s_omp", "m_oma", "s_oma", "m_err", "m_bc", "n_omp", "n_oma")
    out = {k: np.full(len(cycles), np.nan) for k in keys}
    found = False
    for cyc, np_, sp, s2p, na, sa, s2a, ne, se, nb, sb in rows:
        if cyc not in idx:
            continue
        i = idx[cyc]
        out["n_omp"][i], out["n_oma"][i] = (np_ or np.nan), (na or np.nan)
        if np_:
            m = sp / np_
            out["m_omp"][i] = m
            out["s_omp"][i] = max(s2p / np_ - m * m, 0) ** 0.5
            found = True
        if na:
            m = sa / na
            out["m_oma"][i] = m
            out["s_oma"][i] = max(s2a / na - m * m, 0) ** 0.5
            found = True
        if ne:
            out["m_err"][i] = se / ne
            found = True
        if nb:
            out["m_bc"][i] = sb / nb
            found = True
    return out if found else None


def read_shared(spec, db):
    """(shared, only in the control, only in the experience) over the
    period, or None when the runs were not matched."""
    where, args = _where(spec)
    try:
        with open_result(db) as conn:
            if not conn.execute(
                "SELECT 1 FROM sqlite_master WHERE type = " "'table' AND name = 'ts_pair';"
            ).fetchone():
                return None
            row = conn.execute(
                f"SELECT SUM(n_both), SUM(n_ctl_only), "
                f"SUM(n_exp_only) FROM ts_pair WHERE "
                f"{where};",
                args,
            ).fetchone()
    except Exception:
        return None
    if not row or not row[0]:
        return None
    return tuple(float(v or 0) for v in row)


def read_matched(spec, db):
    """Per cycle, over the observations both runs have: the mean and the
    sigma of each of them, and the confidence of the t-test and of the F-test."""
    _f = spec.get("function", "omp")  # the sums of O-P or of O-A
    _n = "n_a" if _f == "oma" else "n_p"
    where, args = _where(spec)
    try:
        with open_result(db) as conn:
            if not conn.execute(
                "SELECT 1 FROM sqlite_master WHERE type = " "'table' AND name = 'ts_pair';"
            ).fetchone():
                return None
            rows = conn.execute(
                f"SELECT cycle, SUM({_n}), SUM(c_{_f}), SUM(c2_{_f}), "
                f"SUM(e_{_f}), SUM(e2_{_f}), SUM(ce_{_f}) FROM ts_pair "
                f"WHERE {where} GROUP BY cycle;",
                args,
            ).fetchall()
    except Exception:
        return None
    cycles = spec["cycles"]
    idx = {c: i for i, c in enumerate(cycles)}
    keys = ("n", "mc", "sc", "me", "se", "cov", "c", "c2", "e", "e2")
    out = {k: np.full(len(cycles), np.nan) for k in keys}
    for cyc, n, c, c2, e, e2, ce in rows:
        if cyc not in idx or not n:
            continue
        i = idx[cyc]
        out["c"][i], out["c2"][i], out["e"][i], out["e2"][i] = c, c2, e, e2
        mc, me = c / n, e / n
        out["n"][i] = n
        out["mc"][i] = mc
        out["me"][i] = me
        out["sc"][i] = max(c2 / n - mc * mc, 0) ** 0.5
        out["se"][i] = max(e2 / n - me * me, 0) ** 0.5
        out["cov"][i] = ce / n - mc * me
    if not np.any(np.isfinite(out["n"])):
        return None
    ok = np.isfinite(out["n"])
    out["t_conf"] = np.full(len(cycles), np.nan)
    out["f_conf"] = np.full(len(cycles), np.nan)
    # Welch on the mean and the F-test on the sigma, on the pairs: the same
    # tests as MATCH off, so the two modes differ by the observations they
    # compare, not by the test
    out["t_conf"][ok] = ttest_confidence(
        out["mc"][ok], out["sc"][ok], out["n"][ok],
        out["me"][ok], out["se"][ok], out["n"][ok],
    )
    out["f_conf"][ok] = sigma_confidence(
        out["sc"][ok] ** 2, out["se"][ok] ** 2, out["n"][ok], out["n"][ok]
    )
    return out


def alerts_of(counts: np.ndarray, cycles, pct: float, days: int = 4):
    """Cycles that bring far fewer observations than they usually do.

    Every cycle is compared with the median of the SAME hour on the days
    before it. A family like ua lives on a synoptic rhythm -- thousands of
    observations at 00 and 12 UTC, a handful at 06 and 18 -- so comparing
    a cycle with the ones just before it would flag every 06 and every 18,
    day after day, and say nothing.

    [(index, n, median of the same hour, drop %)]
    """
    out = []
    if pct <= 0:
        return out
    hours = [str(c)[8:10] for c in cycles]
    for i in range(len(counts)):
        before = [counts[j] for j in range(i) if hours[j] == hours[i]]
        if len(before) < 2:
            continue  # not enough history at that hour
        med = float(np.median(before[-days:]))
        if med > 0 and counts[i] < med * (1 - pct / 100.0):
            out.append((i, float(counts[i]), med, 100.0 * (1 - counts[i] / med)))
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Planning
# ─────────────────────────────────────────────────────────────────────────────


def plan_figures(
    family,
    all_runs,
    control,
    selectors,
    regions,
    flags,
    channels,
    pathwork,
    datestart,
    dateend,
    db_path,
    svg,
    alert_pct,
    match="off",
    functions=("omp",),
    pressure_layers=(),
    height_layers=(),
) -> List[Dict[str, Any]]:
    from pikobs.obsdb import cycles as _cycles
    from pikobs.configobs.special_family import special_label

    cycles = _cycles(datestart, dateend)
    dbs = {n: db_path(pathwork, family, n, datestart, dateend) for n, _ in all_runs}
    # what to draw comes from every run, not from the first one: a varno
    # or a region present in one run only still gets its figures
    combos, levels = set(), set()
    for db in dbs.values():
        try:
            with open_result(db) as conn:
                combos.update(
                    conn.execute(
                        "SELECT DISTINCT region, flag, land_ocean, special, varno " "FROM ts_qc;"
                    )
                )
                levels.update(
                    r[0]
                    for r in conn.execute("SELECT DISTINCT lev FROM ts_qc WHERE lev IS NOT NULL;")
                )
        except Exception:
            continue
    if not combos:
        return []
    combos = sorted(combos, key=lambda c: (str(c[0]), str(c[1]), str(c[2]), str(c[3]), c[4]))
    levels = sorted(levels)
    lv = []
    for c in channels:
        if c == "join":
            lv.append("join")
        elif c == "all":
            lv += [f"{v:g}" for v in levels]
        else:
            # a number is a channel, for the radiances; a family on levels
            # takes it only when that level is in its data
            try:
                known = _layer_units(family) is None or float(c) in levels
            except ValueError:
                known = False
            if known:
                lv.append(c)
    # the layers of pressure or of height, one series each, beside CHANNEL
    # the layers of scatter: same edges, same rank, same label
    from pikobs.configobs.levels import family_layers, layer_display as _layer_display, vcotyp as _vcotyp

    for iv in family_layers(family, pressure_layers, height_layers)[1:]:
        lv.append(_layer_display(iv, _vcotyp(family)))
    word = "type" if family in ("ai", "sf", "ua", "gp", "csr") else "station"
    figs = []
    for sel in selectors:
        for region, flag, surface, special, varno in combos:
            for level in dict.fromkeys(lv):
                base = {
                    "family": family,
                    "region": region,
                    "flag": flag,
                    "surface": surface,
                    "varno": varno,
                    "level": level,
                    "special": special,
                    "special_label": special_label(family, special),
                    "stn_sql": sel.sql(),
                    "stn_label": sel.display,
                    "selector": sel,
                    "stn_tag": sel.tag,
                    "member_word": word,
                    "cycles": cycles,
                    "pathwork": pathwork,
                    "datestart": datestart,
                    "dateend": dateend,
                    "svg": svg,
                    "alert_pct": alert_pct,
                    "pooled": sel.kind in ("join", "prefix", "like", "codtyp_group", "list"),
                }
                for name, _ in all_runs:
                    figs.append(
                        dict(
                            base,
                            mode="run",
                            name=name,
                            db_file=dbs[name],
                            control=control[0] if control else None,
                        )
                    )
                if control:
                    # off: each run with all of its own; on: the same
                    # observations; all: both, and the viewer switches
                    # each asked mode: on (the pairs), off and no (all
                    # observations, no with no test)
                    views = [m for m in str(match).split() if m in ("on", "off", "no")] or ["off"]
                    exps = [n for n, _ in all_runs if n != control[0]]
                    for fn in functions:
                        for mode in views:
                            use_matched = mode == "on"
                            # MATCH on: one figure per experience, every panel
                            # from its pairs with the control; MATCH off: all
                            # the runs together, each with all its observations
                            groups = ([[control[0], e] for e in exps] if use_matched
                                      else [[n for n, _ in all_runs]])
                            for runs in groups:
                                figs.append(
                                    dict(
                                        base,
                                        mode="all",
                                        function=fn,
                                        control=control[0],
                                        runs=runs,
                                        dbs=dbs,
                                        matched=use_matched,
                                        match_mode=mode,
                                    )
                                )
    for f in figs:
        if f["mode"] == "run":
            label = f["name"]
        else:
            exps = [r for r in f["runs"] if r != f["control"]]
            label = f"{(f['runs'][1] if f.get('matched') else exps[0])} vs {f['control']}"
            if not f.get("matched"):
                # the MATCH off figure holds every experience: it is listed
                # under each of them, so the viewer's Match switch flips
                # between an experience's pairs and all the observations
                f["viewer_labels"] = [f"{r} vs {f['control']}" for r in exps]
        f["viewer"] = {
            "experience": label,
            "family": family,
            # one run draws O-P and O-A together: both
            "fonction": ("*" if f["mode"] == "run" else f["function"]),
            "region": f["region"],
            "flag_criteria": f["flag"],
            "land_ocean": f["surface"],
            "special": f.get("special_label", "all"),
            "id_stn": f["stn_label"],
            "varno": str(f["varno"]),
            # a layer in its own section, as in scatter
            "layer": (f["level"] if _layer_bounds(f) else "layer_all"),
            "channel": ("join" if _layer_bounds(f) else f["level"]),
            "match": f.get("match_mode", ""),
        }
    return figs


# ─────────────────────────────────────────────────────────────────────────────
# Figures
# ─────────────────────────────────────────────────────────────────────────────


def _style(ax) -> None:
    """Common presentation style for all time-series panels."""
    ax.set_facecolor("#FCFCFC")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#AEB4BA")
        ax.spines[side].set_linewidth(0.8)
    ax.tick_params(labelsize=11.5 * FS, colors="#333333", width=0.8, length=3.5)
    ax.grid(True, ls="--", lw=0.6, color="#AAB2B9", alpha=0.20)
    ax.set_axisbelow(True)
    ax.yaxis.label.set_size(12 * FS)
    ax.yaxis.label.set_color("#30343A")


def _dates(cycles):
    return np.array([datetime.strptime(c, "%Y%m%d%H") for c in cycles])


def members_text(spec, db, limit: int = 6) -> str:
    """'join -> GOES18, METOP-1, NOAA20 (+2 more)': a pooled selection
    should say what it pooled, not just that it pooled something."""
    label = str(spec["stn_label"])
    if not spec.get("pooled"):
        return label
    # a prefix, a pattern or a list names its stations under the figure
    if getattr(spec.get("selector"), "kind", "") in ("prefix", "like", "list"):
        return label
    try:
        top, rest = read_by_station(spec, db, top=limit)
    except Exception:
        return label
    names = [str(n) for n, _, _ in top]
    if not names:
        return label
    more = f" (+{len(rest)} more)" if rest else ""
    return f"{label} -> {', '.join(names)}{more}"


def _header(fig, spec, head, extra: str = ""):
    """The header of every module, kept in inches from the top: the
    variable, the dates top right, a grey line with what the figure holds,
    the runs in their colours, a note, the rule."""
    var_name, units, _ = pikobs.type_varno(str(spec["varno"]))
    try:
        channels = str(pikobs.family(spec["family"])[5]).strip().upper().startswith("CANAL")
    except Exception:
        channels = False
    if spec["level"] == "join":
        lev = "all channels" if channels else "whole column"
    else:
        lev = f"{'channel' if channels else 'level'} {spec['level']}"
        if _layer_bounds(spec):
            lev = f"layer {spec['level']}"
    db = spec.get("db_file") or next(iter(spec.get("dbs", {}).values()), "")
    label, word = str(spec["stn_label"]), spec["member_word"]
    # three names at most: the line must end before the MATCH badge
    pooled = str(members_text(spec, db, limit=3) if db else label)
    names = pooled.split(" -> ", 1)[1] if " -> " in pooled else ""
    who = f"all {word}s" if label == "join" else f"{word} {label}"
    if names:
        who += f": {names}"

    def _when(stamp) -> str:
        s = str(stamp)
        return f"{s[:4]}-{s[4:6]}-{s[6:8]} {s[8:10]} UTC"

    parts = [spec["family"], spec["region"], f"flag {spec['flag']}"]
    if spec.get("surface", "all") != "all":
        parts.append(spec["surface"])
    sp = _sp_txt(spec).strip(" \u2022|,")
    if sp:
        parts.append(sp)
    parts.append(who)

    h = fig.get_figheight()

    def at(inch):
        return 1 - inch * FS / h

    fig.text(
        0.055,
        at(0.12),
        f"{var_name} {units}  \u00b7  {lev}",
        ha="left",
        va="top",
        fontsize=17 * FS,
        fontweight="bold",
        color="#1F2933",
    )
    # the period on the grey line, not on the right: the MATCH badge sits
    # there, and a comparison's line stops before it
    grey = "  \u00b7  ".join([f"{_when(spec['datestart'])} to {_when(spec['dateend'])}"] + parts)
    if spec.get("mode") == "all" and spec.get("match_mode") != "no":
        room_in = fig.get_figwidth() * (1 - 0.055) - 7.2       # the badge: about 7 in
        fit = int(room_in * 72.0 / (0.56 * 12 * FS))
        grey = textwrap.shorten(grey, width=max(fit, 40), placeholder=" \u2026")
    fig.text(0.055, at(0.47), grey, ha="left", va="top", fontsize=12 * FS, color=_GREY)
    # the runs in their colours, on one line
    if spec.get("mode") == "all":
        ctl = spec["control"]
        exps = [r for r in spec["runs"] if r != ctl]
        runs = [("Ctl", ctl, CTL_COLOUR)] + [
            ("Exp", r, EXP_COLOURS[i % len(EXP_COLOURS)]) for i, r in enumerate(exps)
        ]
    else:
        is_ctl = bool(spec.get("control")) and spec["name"] == spec["control"]
        runs = [("Ctl" if is_ctl else "Exp", spec["name"], CTL_COLOUR if is_ctl else EXP_COLOUR)]
    renderer = fig.canvas.get_renderer()
    x = 0.055
    for word_, name, colour in runs:
        t = fig.text(
            x,
            at(0.74),
            f"{word_}  {name}",
            ha="left",
            va="top",
            fontsize=14 * FS,
            fontweight="bold",
            color=colour,
        )
        box = t.get_window_extent(renderer=renderer)
        x = fig.transFigure.inverted().transform((box.x1, box.y0))[0] + 0.02
    note = str(extra or "").strip().replace("\n", "  \u00b7  ")
    if note:
        fig.text(
            0.055,
            at(1.0),
            note,
            ha="left",
            va="top",
            fontsize=12 * FS,
            fontweight="semibold",
            color="#30343A",
        )
    rule = at(1.24 if note else 1.0)
    fig.add_artist(
        mpl.lines.Line2D(
            [0.055, 0.985], [rule, rule], transform=fig.transFigure, color="#D9DDE2", lw=0.9
        )
    )
    return units


def _finish_x(ax, dates):
    loc = mdates.AutoDateLocator(minticks=5, maxticks=14)
    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))
    ax.set_xlim(dates[0], dates[-1])
    ax.tick_params(axis="x", labelsize=11.5 * FS, pad=5)


def _lo_tag(spec) -> str:
    """The surface in a file name, only when there is a filter: the
    naming convention of every module."""
    lo = spec.get("surface", "all")
    return "" if lo in (None, "", "all") else f"_{_safe(lo)}"


def _out(spec, what) -> str:
    d = os.path.join(spec["pathwork"], spec["family"])
    os.makedirs(d, exist_ok=True)
    return os.path.join(
        d,
        f"timeserie_{_safe(what)}_{spec['family']}_"
        f"varno{_safe(spec['varno'])}_"
        f"lev{_safe(spec['level'])}_"
        f"{_safe(spec['stn_tag'])}_{_safe(spec['region'])}"
        f"{_lo_tag(spec)}{_sp_tag(spec)}_"
        f"{_safe(spec['flag'])}.png",
    )


def _stack_combinations(ax, dates, by_sig: Dict[int, np.ndarray]):
    """Every flag combination, stacked: the ones that carry bit 12 in
    blues from light to dark, the others in their own colour."""
    order = sorted(by_sig, key=lambda k: -by_sig[k].sum())
    top, rest = order[:MAX_DIAGNOSES], order[MAX_DIAGNOSES:]
    total = sum(v.sum() for v in by_sig.values()) or 1.0
    used = [s for s in top if int(s) & 4096]
    blues = iter(
        QC_BLUES
        if len(used) <= len(QC_BLUES)
        else [
            mpl.colormaps.get_cmap("Blues")(0.35 + 0.6 * i / max(len(used) - 1, 1))
            for i in range(len(used))
        ]
    )
    pal = iter(QC_PALETTE)
    bottom = np.zeros(len(dates))
    layers = [(s, by_sig[s]) for s in top]
    if rest:
        layers.append((None, sum(by_sig[s] for s in rest)))
    for sig, vals in layers:
        if sig is None:
            colour, label = QC_OTHER, f"{len(rest)} more"
        else:
            # the bits only: what each one means is in the key below
            colour = next(blues, QC_ASSIMILATED) if int(sig) & 4096 else next(pal, "#666666")
            label = _bits(sig)
        ax.fill_between(
            dates,
            bottom,
            bottom + vals,
            step="mid",
            color=colour,
            alpha=0.9,
            lw=0,
            label=f"{_pct(100 * vals.sum() / total):>7s}  " f"{label}",
        )
        bottom = bottom + vals
    ax.step(dates, bottom, where="mid", color="#333333", lw=1.0)
    return bottom


def _stack_members(ax, dates, by: Dict[str, np.ndarray], top_n: int = 12):
    """Every station -- or instrument type -- stacked, one colour each."""
    order = sorted(by, key=lambda k: -by[k].sum())
    total = sum(v.sum() for v in by.values()) or 1.0
    cmap = mpl.colormaps.get_cmap(STATION_CMAP)
    bottom = np.zeros(len(dates))
    layers = [(k, by[k]) for k in order[:top_n]]
    if order[top_n:]:
        layers.append((f"{len(order) - top_n} more", sum(by[k] for k in order[top_n:])))
    for i, (name, vals) in enumerate(layers):
        colour = (
            QC_OTHER
            if name.endswith("more") and i == len(layers) - 1 and len(order) > top_n
            else cmap(i % 20)
        )
        ax.fill_between(
            dates,
            bottom,
            bottom + vals,
            step="mid",
            color=colour,
            alpha=0.9,
            lw=0,
            label=f"{_pct(100 * vals.sum() / total):>7s}  " f"{str(name)[:18]}",
        )
        bottom = bottom + vals
    ax.step(dates, bottom, where="mid", color="#333333", lw=1.0)


def _bits_key(ax, combos: Dict[int, float], y_top: float, y_bottom: float) -> None:
    """Explain the active flag bits in a compact presentation card."""
    try:
        from pikobs.configobs.flag_groups import BIT_DESCRIPTIONS
    except Exception:  # pragma: no cover
        BIT_DESCRIPTIONS = {}

    used = sorted({b for sig in combos for b in range(24) if int(sig) >> b & 1})
    if not used:
        return

    lines = [f"{b:2d}   {BIT_DESCRIPTIONS.get(b, '')}" for b in used]
    box = ax.get_window_extent()
    inches = max(y_top - y_bottom, 0.05) * box.height / ax.get_figure().dpi
    size = float(np.clip(inches * 72.0 / (1.45 * (len(lines) + 1)), 8.0, 11.5))

    ax.text(
        0.0,
        y_top,
        "BITS USED",
        transform=ax.transAxes,
        va="top",
        fontsize=min(size + 1.0, 12.5) * FS,
        fontweight="bold",
        color="#1F2933",
    )
    ax.text(
        0.0,
        y_top - 0.035,
        "\n".join(lines),
        transform=ax.transAxes,
        va="top",
        fontsize=size * FS,
        family="monospace",
        color="#30343A",
        linespacing=1.35,
        bbox=dict(boxstyle="round,pad=0.55", fc="#F7F8FA", ec="#D1D5D9", lw=0.8),
    )


def _top_key(ax, handles, labels, title=None, ncol=None) -> None:
    """A key in rows just above its panel, never wider than the panel: as
    many columns as the longest label lets fit in its width."""
    if not handles:
        return
    if ncol is None:
        size = 10.5 * FS
        width_pt = ax.get_position().width * ax.figure.get_figwidth() * 72.0
        longest = max((len(str(lab)) for lab in labels), default=1)
        # a monospace character is 0.6 of the size; the handle and the gap
        per_entry = longest * 0.6 * size + (1.6 + 1.8 + 0.8) * size
        ncol = max(1, min(len(handles), int(width_pt // per_entry)))
    ax.legend(
        handles,
        labels,
        loc="lower left",
        bbox_to_anchor=(0, 1.0),
        ncol=ncol,
        prop={"family": "monospace", "size": 10.5 * FS},
        title=title,
        title_fontsize=11 * FS,
        alignment="left",
        frameon=False,
        borderaxespad=0.25,
        columnspacing=1.8,
        handlelength=1.6,
    )


def _bits_line(fig, combos, y) -> None:
    """The meaning of every bit that appears, on a line under the figure."""
    try:
        from pikobs.configobs.flag_groups import BIT_DESCRIPTIONS
    except Exception:  # pragma: no cover
        BIT_DESCRIPTIONS = {}
    used = sorted({b for sig in combos for b in range(24) if int(sig) >> b & 1})
    if not used:
        return
    fig.text(
        0.055,
        y,
        "BITS   "
        + "   \u00b7   ".join(f"{b} {BIT_DESCRIPTIONS.get(b, '')}".strip() for b in used),
        fontsize=10.5 * FS,
        color="#30343A",
        va="bottom",
        wrap=True,
    )


def _run_layout(spec, has_mean, has_sigma):
    """The panels: the flag combinations, the members when there are several, mean and sigma."""

    # one panel more when the selection pools several stations or types:
    # who brings the observations, cycle by cycle
    members = read_counts_by_member(spec, spec["db_file"]) if spec.get("pooled") else {}
    if len(members) < 2:
        members = {}
    n_rows = 1 + bool(members) + has_mean + has_sigma
    heights = ([2.4, 1.75] if members else [2.45]) + [1.45] * (n_rows - 1 - bool(members))
    # no column on the right: the keys sit above their panels
    fig_h = (5.9 + 2.75 * n_rows) * 1.6
    fig = plt.figure(figsize=(26, fig_h), facecolor="white")
    gs = fig.add_gridspec(
        n_rows,
        1,
        height_ratios=heights,
        hspace=0.45,
        left=0.085,          # the y labels, at the bigger size
        right=0.985,
        top=1 - 2.05 * FS / fig_h,
        bottom=1.3 * FS / fig_h,
    )
    ax0 = fig.add_subplot(gs[0, 0])
    axes = [ax0] + [fig.add_subplot(gs[i, 0], sharex=ax0) for i in range(1, n_rows)]
    for ax in axes:
        _style(ax)

    return members, fig_h, fig, ax0, axes


def _draw_run_counts(ax0, dates, by, members, axes, spec, cycles):
    """The counts stacked by flag combination, the members, and the cycles that dropped."""

    total = _stack_combinations(ax0, dates, by)
    ax0.set_ylabel(
        "observations per cycle\nby flag combination", fontsize=12.5 * FS, fontweight="semibold"
    )
    fmt_k = mpl.ticker.FuncFormatter(lambda v, _: f"{v / 1000:g}k" if v >= 1000 else f"{v:g}")
    ax0.yaxis.set_major_formatter(fmt_k)
    ax_m = None
    if members:
        ax_m = axes[1]
        _stack_members(ax_m, dates, members)
        ax_m.set_ylabel(
            "by " + ("type" if _member_key(spec, spec["db_file"]) == "codtyp" else "station")
        )
        ax_m.yaxis.set_major_formatter(fmt_k)

    alerts = []
    for i, n, med, drop in alerts_of(total, cycles, spec["alert_pct"]):
        ax0.scatter(
            [dates[i]],
            [n],
            marker="v",
            s=78,
            color="#202428",
            edgecolor="white",
            linewidth=0.5,
            zorder=6,
        )
        alerts.append(
            [
                spec["name"],
                spec["family"],
                spec["region"],
                spec["flag"],
                spec["stn_label"],
                spec["varno"],
                spec["level"],
                cycles[i],
                int(n),
                int(med),
                f"{drop:.1f}",
            ]
        )

    return ax_m, alerts


def _draw_run_values(fig, spec, members, has_mean, axes, vals, dates, has_sigma):
    """The header, then mean and sigma when there are values, and the time axis."""

    units = _header(fig, spec, spec["name"])
    # the run in its colour: red for an experience, blue for the control
    rc = CTL_COLOUR if spec.get("control") and spec["name"] == spec["control"] else EXP_COLOUR
    row = 1 + bool(members)
    style_keys = []
    if has_mean:
        ax = axes[row]
        if np.any(np.isfinite(vals["m_omp"])):
            ax.plot(dates, vals["m_omp"], "-", color=rc, lw=2.0)
            style_keys.append(("-", "O-P", "#333333"))
        if np.any(np.isfinite(vals["m_oma"])):
            ax.plot(dates, vals["m_oma"], "--", color=rc, lw=1.6)
            style_keys.append(("--", "O-A", "#333333"))
        if np.any(np.isfinite(vals["m_bc"])):
            ax.plot(dates, vals["m_bc"], ":", color="#8C510A", lw=1.8)
            style_keys.append((":", "bias correction", "#8C510A"))
        ax.axhline(0, color="#444444", ls=":", lw=0.9)
        ax.set_ylabel(f"mean  {units}")
        row += 1
    if has_sigma:
        ax = axes[row]
        if np.any(np.isfinite(vals["s_omp"])):
            ax.plot(dates, vals["s_omp"], "-", color=rc, lw=2.0)
        if np.any(np.isfinite(vals["s_oma"])):
            ax.plot(dates, vals["s_oma"], "--", color=rc, lw=1.6)
        if np.any(np.isfinite(vals["m_err"])):
            ax.plot(dates, vals["m_err"], color="#4B5563", lw=2.2, ls=(0, (1, 1.6)))
            style_keys.append((":", "OBS_ERROR used in the assimilation", "#4B5563"))
        ax.set_ylabel(f"sigma  {units}")
        ax.set_ylim(bottom=0)
    for ax in axes[:-1]:
        ax.tick_params(axis="x", labelbottom=False)
    _finish_x(axes[-1], dates)

    return style_keys


def _run_keys(ax0, ax_m, spec, style_keys, axes, members, fig, fig_h, combos, alerts):
    """The keys: flag combinations, members, line styles, the bits, the alerts."""

    # the keys, above the panels they explain: every panel the whole width
    h, l = ax0.get_legend_handles_labels()
    _top_key(ax0, h, l, "FLAG COMBINATIONS (bits)  --  blue = entered the " "analysis (bit 12)")
    if ax_m is not None:
        hm, lm = ax_m.get_legend_handles_labels()
        _top_key(
            ax_m,
            hm,
            lm,
            "by " + ("type" if _member_key(spec, spec["db_file"]) == "codtyp" else "station"),
        )
    if style_keys:
        _top_key(
            axes[1 + bool(members)],
            [mpl.lines.Line2D([0], [0], color=c, ls=s, lw=1.6) for s, t, c in style_keys],
            [t for s, t, c in style_keys],
            "DEPARTURES",
        )
    else:
        fig.text(
            0.985,
            0.62 / fig_h,
            "no departures in the files: counts only",
            ha="right",
            va="bottom",
            fontsize=10.5 * FS,
            color=_GREY,
        )
    _bits_line(fig, combos, 0.62 / fig_h)
    if alerts:
        fig.text(
            0.055,
            0.22 / fig_h,
            f"v  {len(alerts)} cycle(s) more than {spec['alert_pct']:g} % "
            f"below the median of the same hour on the days before",
            fontsize=10.5 * FS,
            color="#202428",
            va="bottom",
            bbox=dict(boxstyle="round,pad=0.35", fc="#FFF8E6", ec="#E5C56A"),
        )


def _save_run(spec, fig, alerts):
    """Write the figure; returns its path and the alerts."""

    out = _out(spec, spec["name"])
    from pikobs.figures.figures import members_footer
    members_footer(fig, spec.get('selector'))
    save_figure(fig, out, svg=spec.get("svg", False), dpi=DPI)
    plt.close(fig)
    return out, alerts


def _run_figure(spec) -> Optional[Tuple[str, list]]:
    cycles, by, assim, combos = read_counts(spec, spec["db_file"])
    if not by or sum(v.sum() for v in by.values()) == 0:
        return None
    vals = read_values(spec, spec["db_file"])
    dates = _dates(cycles)
    has_mean = vals is not None and (
        np.any(np.isfinite(vals["m_omp"])) or np.any(np.isfinite(vals["m_bc"]))
    )
    has_sigma = vals is not None and (
        np.any(np.isfinite(vals["s_omp"])) or np.any(np.isfinite(vals["m_err"]))
    )

    members, fig_h, fig, ax0, axes = _run_layout(spec, has_mean, has_sigma)
    ax_m, alerts = _draw_run_counts(ax0, dates, by, members, axes, spec, cycles)
    style_keys = _draw_run_values(fig, spec, members, has_mean, axes, vals, dates, has_sigma)
    _run_keys(ax0, ax_m, spec, style_keys, axes, members, fig, fig_h, combos, alerts)
    # the y labels in one column, whatever the width of each panel's numbers
    fig.align_ylabels([a for a in fig.axes if a.get_ylabel()])
    return _save_run(spec, fig, alerts)


def _units_of(spec) -> str:
    try:
        _, units, _ = pikobs.type_varno(str(spec["varno"]))
        return str(units)
    except Exception:  # pragma: no cover
        return ""


def _run_values(ax, parts) -> None:
    """The line above a panel, each run in its colour, as in cardio:
    'Ctl name: sigma 2.529  .  Exp name: sigma 2.534'. It never runs past
    the panel: what does not fit goes on a second line, above the first."""
    fig = ax.figure
    renderer = fig.canvas.get_renderer()
    size = 11.5 * FS
    sep = "   \u00b7   "
    ax_w = ax.get_position().width * fig.get_figwidth() * fig.dpi
    ax_h_in = ax.get_position().height * fig.get_figheight()

    def width(text, weight):
        t = fig.text(0, 0, text, fontsize=size, fontweight=weight)
        w = t.get_window_extent(renderer=renderer).width / ax_w
        t.remove()
        return w

    lines, x = [[]], 0.0
    for text, colour in parts:
        w, ws = width(text, "semibold"), (width(sep, "normal") if lines[-1] else 0.0)
        if lines[-1] and x + ws + w > 1.0:
            lines.append([])
            x, ws = 0.0, 0.0
        lines[-1].append((text, colour))
        x += ws + w
    dy = size * 1.35 / 72.0 / ax_h_in
    for i, line in enumerate(lines):
        y = 1.03 + (len(lines) - 1 - i) * dy
        x = 0.0
        for k, (text, colour) in enumerate(line):
            for piece, col, weight in ([(sep, "#6B7280", "normal")] if k else []) + [(text, colour, "semibold")]:
                t = ax.text(x, y, piece, transform=ax.transAxes, fontsize=size, fontweight=weight,
                            color=col, va="bottom")
                box = t.get_window_extent(renderer=renderer)
                x = ax.transAxes.inverted().transform((box.x1, box.y0))[0]


def _all_layout(spec, data, MK):
    """The panels: observations and their difference, then mean and sigma with theirs when there are values."""

    ax_mean = None  # bound only on some paths below
    ax_mean_diff = None  # bound only on some paths below
    ax_sigma = None  # bound only on some paths below
    ax_sigma_diff = None  # bound only on some paths below

    dates = _dates(spec["cycles"])
    has_vals = any(v[2] is not None and np.any(np.isfinite(v[2][MK])) for v in data.values())

    # Panel order:
    #   0 observations
    #   1 assimilated difference
    #   2 mean O-P
    #   3 mean O-P difference
    #   4 sigma O-P
    #   5 sigma O-P difference
    #
    # If the files do not contain departure statistics, only the first two
    # panels are produced.
    # under each difference of the values, a strip: the dots of the tests;
    # none with MATCH no, which tests nothing
    strips = has_vals and spec.get("match_mode") != "no"
    n_rows = 8 if strips else (6 if has_vals else 2)
    height_ratios = ([2.35, 0.95, 1.55, 0.95, 0.42, 1.55, 0.95, 0.42] if strips
                     else [2.35, 0.95, 1.55, 0.95, 1.55, 0.95] if has_vals else [2.35, 0.95])

    # Keep the comparison figure compact enough that a browser does not
    # shrink the whole image excessively.  The previous 22-inch canvas made
    # the text look small once the PNG was fitted to the viewer width.
    # A narrower canvas + larger fonts gives substantially better on-screen
    # readability while preserving enough vertical room for the six panels.
    fig_w = 26.0
    # the runs above the first panel, the numbers above their panels
    fig_h = ((15.8 if has_vals else 7.6) + 0.5) * 1.6
    fig = plt.figure(figsize=(fig_w, fig_h), facecolor="white")
    gs = fig.add_gridspec(
        n_rows,
        1,
        height_ratios=height_ratios,
        hspace=0.55,
        left=0.09,
        right=0.985,
        top=1 - 1.95 * FS / fig_h,
        bottom=0.9 * FS / fig_h,
    )

    ax_obs = fig.add_subplot(gs[0, 0])
    axes = [ax_obs] + [fig.add_subplot(gs[i, 0], sharex=ax_obs) for i in range(1, n_rows)]

    ax_obs_diff = axes[1]
    if strips:
        ax_mean = axes[2]
        ax_mean_diff = axes[3]
        ax_sigma = axes[5]
        ax_sigma_diff = axes[6]
        fig._pikobs_strips = {"mean": axes[4], "sigma": axes[7]}
    elif has_vals:
        ax_mean, ax_mean_diff, ax_sigma, ax_sigma_diff = axes[2], axes[3], axes[4], axes[5]
    else:
        ax_mean = ax_mean_diff = ax_sigma = ax_sigma_diff = None

    for ax in axes:
        _style(ax)
        # Comparison figures need to remain readable after the PNG is scaled
        # in the web viewer.  Use larger tick/axis text than the single-run
        # figures and slightly heavier axes/lines.
        ax.tick_params(axis="both", labelsize=13.0 * FS, width=0.9, length=4.0)
        ax.yaxis.label.set_size(13.5 * FS)
        ax.yaxis.labelpad = 12
        for side in ("left", "bottom"):
            ax.spines[side].set_linewidth(0.9)

    return (
        dates,
        has_vals,
        fig,
        ax_obs,
        axes,
        ax_obs_diff,
        ax_mean,
        ax_mean_diff,
        ax_sigma,
        ax_sigma_diff,
    )


def _draw_all_counts(
    data, ax_obs, dates, colours, styles, ctl, ax_obs_diff, has_vals, ax_mean, MK, ax_sigma, SK
):
    """1) The observations of each run, and their difference to the control just under."""

    for r, (total, assim, vals) in data.items():
        # The colour identifies the run.  The thick line is assimilated
        # observations; the thin/pale line is all observations.
        if np.any(total > assim):
            ax_obs.step(
                dates, total, where="mid", color=colours[r], lw=1.65, ls=styles[r], alpha=0.42
            )

        ax_obs.step(dates, assim, where="mid", color=colours[r], lw=2.75, ls=styles[r])

        if r != ctl:
            diff = assim - data[ctl][1]
            ok = np.isfinite(diff)
            ax_obs_diff.bar(
                dates[ok],
                diff[ok],
                width=0.20,
                color=np.where(diff[ok] >= 0, colours[r], CTL_COLOUR),
                alpha=0.75,
                zorder=3,
            )

        if has_vals and vals is not None:
            # Every run is always drawn with all of its own observations.
            # MATCH changes the statistical test used for the bars below,
            # not the curves themselves.
            ax_mean.plot(dates, vals[MK], ls=styles[r], color=colours[r], lw=2.35)
            ax_sigma.plot(dates, vals[SK], ls=styles[r], color=colours[r], lw=2.35)

    ax_obs.set_ylabel("observations", fontsize=14.0 * FS, fontweight="semibold", labelpad=13)
    ax_obs.yaxis.set_major_formatter(
        mpl.ticker.FuncFormatter(lambda v, _: f"{v / 1000:g}k" if v >= 1000 else f"{v:g}")
    )

    ax_obs_diff.axhline(0, color="#333333", lw=0.9)
    ax_obs_diff.set_ylabel("Exp \u2212 Ctl", fontsize=13.5 * FS, labelpad=12)


def _draw_all_values(
    spec,
    data,
    ctl,
    has_vals,
    matched,
    dates,
    MK,
    SK,
    ax_mean_diff,
    ax_sigma_diff,
    colours,
    ax_mean,
    FN,
    ax_sigma,
):
    """2) and 3) Mean and sigma of each run, and their differences to the control just under."""

    units_label = _units_of(spec)
    exps = [r for r in data if r != ctl]

    if has_vals:
        width = 0.20 / max(len(exps), 1)

        for k, r in enumerate(exps):
            v_c = data[ctl][2]
            v_e = data[r][2]
            if v_c is None or v_e is None:
                continue

            m = matched.get(r)

            # Several experiences are put side by side.  Width/offset are in
            # Matplotlib date units (days), hence timedelta(days=off).
            off = (k - (len(exps) - 1) / 2) * width
            x = np.array([d + timedelta(days=off) for d in dates])

            mean_vals = v_e[MK] - v_c[MK]
            sigma_vals = v_e[SK] - v_c[SK]

            mean_better = np.abs(v_e[MK]) < np.abs(v_c[MK])
            sigma_better = v_e[SK] < v_c[SK]

            mean_conf = None if m is None else m["t_conf"]
            sigma_conf = None if m is None else m["f_conf"]

            for ax, vals, better, conf in (
                (ax_mean_diff, mean_vals, mean_better, mean_conf),
                (ax_sigma_diff, sigma_vals, sigma_better, sigma_conf),
            ):
                bar_colour = np.where(better, colours[r], CTL_COLOUR)
                sig = (
                    is_significant(np.nan_to_num(conf))
                    if conf is not None
                    else np.zeros(len(dates), bool)
                )
                ok = np.isfinite(vals)

                # Filled = statistically significant when MATCH is available.
                ax.bar(
                    x[sig & ok], vals[sig & ok], width=width, color=bar_colour[sig & ok], zorder=3
                )

                # one look for every bar: the dots under the panel say which
                # change is significant
                ax.bar(
                    x[~sig & ok],
                    vals[~sig & ok],
                    width=width,
                    color=bar_colour[~sig & ok],
                    alpha=0.75,
                    zorder=2,
                )

        who = exps[0] if len(exps) == 1 else "experience"

        # Main series and its difference are adjacent by construction.
        ax_mean.axhline(0, color="#444444", ls=":", lw=0.9)
        ax_mean.set_ylabel(f"mean {FN} {units_label}", fontsize=13.5 * FS, labelpad=12)
        ax_mean_diff.axhline(0, color="#333333", lw=1.0)
        ax_mean_diff.set_ylabel("Exp \u2212 Ctl", fontsize=13.5 * FS, labelpad=12)   # its units: the panel above

        ax_sigma.set_ylabel(f"sigma {FN} {units_label}", fontsize=13.5 * FS, labelpad=12)
        ax_sigma.set_ylim(bottom=0)
        ax_sigma_diff.axhline(0, color="#333333", lw=1.0)
        ax_sigma_diff.set_ylabel("Exp \u2212 Ctl", fontsize=13.5 * FS, labelpad=12)   # its units: the panel above


def _draw_all_header(
    ctl, fig, spec, has_vals, ax_mean, FN, ax_mean_diff, ax_sigma, ax_sigma_diff, axes, dates
):
    """The header, and the time axis of the last panel."""

    head = (f"{spec['runs'][1]} against {ctl}" if spec.get("matched")
            else f"all runs against {ctl}")
    # what MATCH means is on the badge; the dots under the differences are
    # the tests: one per date, and with MATCH on the period on the right
    units = _header(
        fig,
        spec,
        head,
        ("" if spec.get("match_mode") == "no" else
         "dots under each difference, one per date: filled = significant "
         "(red: Exp better, blue: Ctl better), hollow = not"),
    )

    # _header() is also the authoritative source of the display units.  Keep
    # the labels in sync with it in case type_varno() returns a prettier unit.
    if has_vals:
        ax_mean.set_ylabel(f"mean {FN} {units}", fontsize=13.5 * FS, labelpad=12)
        ax_mean_diff.set_ylabel("Exp \u2212 Ctl", fontsize=13.5 * FS, labelpad=12)   # its units: the panel above
        ax_sigma.set_ylabel(f"sigma {FN} {units}", fontsize=13.5 * FS, labelpad=12)
        ax_sigma_diff.set_ylabel("Exp \u2212 Ctl", fontsize=13.5 * FS, labelpad=12)   # its units: the panel above

    # Only the bottom panel carries date labels; all panels still share x.
    for ax in axes[:-1]:
        ax.tick_params(axis="x", labelbottom=False)
    _finish_x(axes[-1], dates)
    axes[-1].tick_params(axis="x", labelsize=13.0 * FS, pad=6)


def _draw_all_key(data, colours, styles, matched, ax_obs):
    """The key on the right: runs, styles and what the shading means."""

    handles = [
        mpl.lines.Line2D([0], [0], color=colours[r], lw=2.0, ls=styles[r], label=r) for r in data
    ]
    handles += [
        mpl.lines.Line2D([0], [0], color="#555555", lw=2.0, label="assimilated (bit 12)"),
        mpl.lines.Line2D([0], [0], color="#555555", lw=1.1, alpha=0.45, label="all observations"),
    ]

    ax_obs.legend(
        handles=handles,
        loc="lower left",
        bbox_to_anchor=(0, 1.0),
        ncol=len(handles),
        fontsize=11 * FS,
        frameon=False,
        borderaxespad=0.25,
        columnspacing=1.8,
    )


def _draw_all_summary(
    data,
    ctl,
    MK,
    SK,
    colours,
    spec,
    ax_obs_diff,
    has_vals,
    ax_mean,
    ax_sigma,
    matched,
    ax_mean_diff,
    ax_sigma_diff,
):
    """The numbers of the period, each above the panel it is about."""

    # ---- the numbers of the period, each above the panel it is about -----
    role = {r: ("Ctl" if r == ctl else "Exp") for r in data}
    per_run = {}
    for r, (total, assim, vals) in data.items():
        if vals is not None and np.any(np.isfinite(vals[MK])):
            per_run[r] = (float(np.nanmean(vals[MK])), float(np.nanmean(vals[SK])))
    # above the change of the counts: what each run assimilated, and how
    # much of the data they share
    parts = [
        (f"{role[r]} {r}: {int(np.nansum(v[1])):,} assimilated", colours[r])
        for r, v in data.items()
    ]
    for r in data:
        if r == ctl:
            continue
        sh = read_shared(dict(spec, db_file=spec["dbs"][r]), spec["dbs"][r])
        if sh:
            both, only_c, only_e = sh
            tot = both + only_c + only_e
            parts.append(
                (
                    f"{'' if len(data) == 2 else r + ' '}shares "
                    f"{100 * both / tot:.1f} % (only Ctl "
                    f"{100 * only_c / tot:.1f} %, only Exp "
                    f"{100 * only_e / tot:.1f} %)",
                    "#30343A",
                )
            )
    _run_values(ax_obs_diff, parts)
    if has_vals and per_run:
        _run_values(
            ax_mean, [(f"{role[r]} {r}: bias {v[0]:+.3f}", colours[r]) for r, v in per_run.items()]
        )
        _run_values(
            ax_sigma,
            [(f"{role[r]} {r}: sigma {v[1]:.3f}", colours[r]) for r, v in per_run.items()],
        )
        c_m, c_s = per_run.get(ctl, (float("nan"), float("nan")))
        ctl_vals = data[ctl][2]
        mean_parts, sigma_parts = [], []
        for r, (total, assim, vals) in data.items():
            if r == ctl or r not in per_run or ctl_vals is None:
                continue
            m, sd = per_run[r]
            tag = "" if len(data) == 2 else f"{r}: "
            d_bias = (abs(m) - abs(c_m)) / abs(c_m) * 100 if c_m else float("nan")
            d_spr = (sd - c_s) / c_s * 100 if c_s else float("nan")
            ok = np.isfinite(vals[SK]) & np.isfinite(ctl_vals[SK])
            narrower = int(np.sum(vals[SK][ok] < ctl_vals[SK][ok]))
            mean_parts.append((f"{tag}|bias| Exp against Ctl {d_bias:+.1f} %", "#30343A"))
            sigma_parts.append(
                (
                    f"{tag}sigma Exp against Ctl {d_spr:+.1f} %, "
                    f"narrower in {narrower}/{int(ok.sum())} cycles",
                    "#30343A",
                )
            )
            mm = matched.get(r)
            if mm is not None:
                t_ok = is_significant(np.nan_to_num(mm["t_conf"]))
                f_ok = is_significant(np.nan_to_num(mm["f_conf"]))
                n_cyc = int(np.sum(np.isfinite(mm["n"])))
                closer = np.abs(mm["me"]) < np.abs(mm["mc"])
                mean_parts.append(
                    (
                        f"same observations: bias "
                        f"{float(np.nanmean(np.abs(mm['me']) - np.abs(mm['mc']))):+.4f}, "
                        f"the test passes in {int(np.sum(t_ok & closer))}/{n_cyc} "
                        f"cycles for Exp, {int(np.sum(t_ok & ~closer))} for Ctl",
                        "#30343A",
                    )
                )
                narrow = mm["se"] < mm["sc"]
                sigma_parts.append(
                    (
                        f"same observations: "
                        f"{float(np.nanmean(100 * (mm['se'] - mm['sc']) / mm['sc'])):+.1f} %, "
                        f"the test passes in {int(np.sum(f_ok & narrow))}/{n_cyc} "
                        f"for Exp, {int(np.sum(f_ok & ~narrow))} for Ctl",
                        "#30343A",
                    )
                )
        if not matched:
            mean_parts.append(("each run with all its own observations", _GREY))
        _run_values(ax_mean_diff, mean_parts)
        _run_values(ax_sigma_diff, sigma_parts)


def _test_strip(strip, ax_diff, dates, data, ctl, tests, verdict, k, MK, SK, on) -> None:
    """The tests of a difference panel, in the strip under it: a line per
    experience, and on it only dots -- filled where the change is
    significant (red: Exp better, blue: Ctl better), hollow where it is not.
    One dot per date: Welch on the mean and the F-test on the sigma, on the
    pairs of that date with MATCH on, on all its observations with MATCH off."""
    exps = [r for r in data if r != ctl]
    rows = {r: len(exps) - 1 - i for i, r in enumerate(exps)}
    beside = mtransforms.blended_transform_factory(strip.transAxes, strip.transData)
    vc = data[ctl][2]

    def _dots(xs, yrow, sig, side, size, transform=None):
        kw = {"transform": transform} if transform is not None else {}
        filled = np.where(np.asarray(side) < 0, EXP_BETTER, CTL_BETTER)
        sig = np.asarray(sig, bool)
        if sig.any():
            strip.scatter(np.asarray(xs, dtype=object)[sig], np.full(sig.sum(), yrow), s=size,
                          facecolors=filled[sig], edgecolors=filled[sig], linewidths=1.5,
                          zorder=3, clip_on=False, **kw)
        if (~sig).any():
            strip.scatter(np.asarray(xs, dtype=object)[~sig], np.full((~sig).sum(), yrow), s=size,
                          facecolors="white", edgecolors="#333333", linewidths=2.0, zorder=3,
                          clip_on=False, **kw)

    for r, yrow in rows.items():
        strip.axhline(yrow, color="#D0D4D9", lw=1.2, zorder=1)
        ve = data[r][2]
        if r in tests and vc is not None and ve is not None:
            conf = np.asarray(tests[r][k], float)
            side = (np.abs(ve[MK]) - np.abs(vc[MK])) if k == 0 else (ve[SK] - vc[SK])
            ok = np.isfinite(conf) & np.isfinite(side)
            _dots(np.asarray(dates, dtype=object)[ok], yrow, is_significant(conf[ok]),
                  side[ok], 150)
        v = verdict.get("mean" if k == 0 else "sigma") if on else None
        if v and np.isfinite(v[0]):
            _dots([1.035], yrow, [v[0] >= MIN_CONFIDENCE], [v[1]], 480, transform=beside)
    if on:
        strip.text(1.035, len(exps) - 0.35, "period", transform=beside, ha="center",
                   va="bottom", fontsize=11 * FS, color=GREY_TEXT, clip_on=False)
    strip.set_ylim(-0.7, len(exps) - 0.3)
    strip.set_yticks(list(rows.values()))
    strip.set_yticklabels(["Exp" if len(exps) == 1 else str(r)[:16] for r in rows], fontsize=12 * FS)
    strip.tick_params(axis="y", length=0, pad=12)
    strip.grid(False)
    for side_name in ("top", "right", "left"):
        strip.spines[side_name].set_visible(False)
    ax_diff.tick_params(axis="x", labelbottom=False)


def _save_all(spec, ctl, fn, fig):
    """Write the figure; returns its path and no alert. MATCH on: one figure
    per experience; MATCH off: all the runs, in a file of its own."""

    what = (f"{spec['runs'][1]}_vs_{ctl}" if spec.get("matched")
            else f"all_vs_{ctl}" + (f"_match{spec['match_mode']}"
                                     if spec.get("match_mode") in ("off", "no") else ""))
    out = _out(spec, what + ("" if fn == "omp" else f"_{fn}"))
    from pikobs.figures.figures import members_footer
    members_footer(fig, spec.get('selector'))
    save_figure(fig, out, svg=spec.get("svg", False), dpi=DPI)
    plt.close(fig)
    return out, []


def _all_figure(spec) -> Optional[Tuple[str, list]]:
    """Draw the control/experience comparison figure.

    The panels are deliberately organised in pairs so that every time series
    is immediately followed by its difference with respect to the control:

        observations
        assimilated difference
        mean O-P
        mean O-P difference
        sigma O-P
        sigma O-P difference

    This makes the comparison much easier to read than putting both
    difference panels at the bottom of the figure.
    """
    runs = spec["runs"]
    fn = spec.get("function", "omp")  # O-P or O-A
    MK, SK = f"m_{fn}", f"s_{fn}"
    FN = {"omp": "O-P", "oma": "O-A"}[fn]
    colours = {runs[0]: CTL_COLOUR}

    # The control is drawn solid and every experience dashed.  Where two
    # curves agree, different line styles keep both runs identifiable.
    styles = {runs[0]: "-"}
    dashes = ["--", "-.", (0, (3, 1, 1, 1, 1, 1)), ":"]
    for i, r in enumerate(runs[1:]):
        colours[r] = EXP_COLOURS[i % len(EXP_COLOURS)]
        styles[r] = dashes[i % len(dashes)]

    data, matched, tests = {}, {}, {}
    ctl = spec["control"]
    if spec.get("matched"):
        # MATCH on: one experience, and every panel from its pairs with the
        # control -- the same observations on both sides, the same counts
        exp = runs[1]
        m = read_matched(spec, spec["dbs"][exp])
        if m is None:
            return None
        nan = np.full(len(m["n"]), np.nan)

        def _vals(mean, sigma):
            v = {k: nan for k in ("m_omp", "s_omp", "m_oma", "s_oma", "m_err", "m_bc")}
            v.update({MK: mean, SK: sigma})
            return v

        data[ctl] = (m["n"], m["n"], _vals(m["mc"], m["sc"]))
        data[exp] = (m["n"], m["n"], _vals(m["me"], m["se"]))
        matched[exp] = m
        tests[exp] = (m["t_conf"], m["f_conf"])
    else:
        for r in runs:
            cycles, by, assim, _ = read_counts(spec, spec["dbs"][r])
            if not by:
                continue
            total = sum(by.values())
            data[r] = (total, assim, read_values(spec, spec["dbs"][r]))
        # MATCH off: each run with all its observations, Welch and F per
        # date; MATCH no: the same runs, and no test
        vc = data.get(ctl, (None, None, None))[2]
        for r in (data if spec.get("match_mode") != "no" else []):
            ve = data[r][2]
            if r == ctl or vc is None or ve is None:
                continue
            nc, ne = vc.get(f"n_{fn}"), ve.get(f"n_{fn}")
            if nc is None or ne is None:
                continue
            tests[r] = (ttest_confidence(vc[MK], vc[SK], nc, ve[MK], ve[SK], ne),
                        sigma_confidence(vc[SK] ** 2, ve[SK] ** 2, nc, ne))

    if ctl not in data or len(data) < 2:
        return None

    (
        dates,
        has_vals,
        fig,
        ax_obs,
        axes,
        ax_obs_diff,
        ax_mean,
        ax_mean_diff,
        ax_sigma,
        ax_sigma_diff,
    ) = _all_layout(spec, data, MK)
    _draw_all_counts(
        data, ax_obs, dates, colours, styles, ctl, ax_obs_diff, has_vals, ax_mean, MK, ax_sigma, SK
    )
    _draw_all_values(
        spec,
        data,
        ctl,
        has_vals,
        {},

        dates,
        MK,
        SK,
        ax_mean_diff,
        ax_sigma_diff,
        colours,
        ax_mean,
        FN,
        ax_sigma,
    )
    _draw_all_header(
        ctl, fig, spec, has_vals, ax_mean, FN, ax_mean_diff, ax_sigma, ax_sigma_diff, axes, dates
    )
    _draw_all_key(data, colours, styles, matched, ax_obs)
    strips = getattr(fig, "_pikobs_strips", {})
    if strips:
        # only the dot of each date: no dot of the whole period
        for k, (name, ax_diff) in enumerate((("mean", ax_mean_diff), ("sigma", ax_sigma_diff))):
            _test_strip(strips[name], ax_diff, dates, data, ctl, tests, {}, k, MK, SK, False)
    # MATCH on: Welch and F on the pairs of each date, as off does on all
    if spec.get("match_mode") != "no":           # MATCH no: no badge at all
        match_badge(fig, bool(spec.get("matched")), top_in=0.12 * FS,
                    method="t-test and F-test, 95 %" if spec.get("matched") else None)
    # the y labels in one column, whatever the width of each panel's numbers
    fig.align_ylabels([a for a in (ax_obs, ax_obs_diff, ax_mean, ax_mean_diff, ax_sigma,
                                   ax_sigma_diff) if a is not None])
    _draw_all_summary(
        data,
        ctl,
        MK,
        SK,
        colours,
        spec,
        ax_obs_diff,
        has_vals,
        ax_mean,
        ax_sigma,
        matched,
        ax_mean_diff,
        ax_sigma_diff,
    )
    return _save_all(spec, ctl, fn, fig)


def plot_task(spec: Dict[str, Any]):
    import traceback

    try:
        with plt.rc_context(_STYLE):
            if spec["mode"] == "all":
                return _all_figure(spec)
            return _run_figure(spec)
    except Exception:
        print(
            f"[timeserie] plot failed for {spec.get('family')} "
            f"{spec.get('stn_label')} {spec.get('mode')}:\n"
            f"{traceback.format_exc()}",
            file=sys.stderr,
            flush=True,
        )
        plt.close("all")
        return None
