r"""
==========================================================
pikobs.obsscorecard -- Is the experience better, by theme
==========================================================

One card per theme -- winds, thermodynamics, surface, GPS-RO and ozone,
radiances -- with every family that observes it side by side: the
radiosonde, aircraft, AMV and radar winds on one card; the temperatures and
humidities aloft on another; what is observed at the surface (temperature
and dew point at 2 m, pressure, GPS zenith delay, the 10 m winds of the
stations and the scatterometers) on a card of its own, with a column per
region instead of empty layers, and the land stations apart from the ships
and buoys (by codtyp: their errors differ, and one would hide the other);
GPS-RO and the ozone
profiles, which reach the stratosphere, together on a third; the radiances
on a fourth, followed by one card per instrument, channel by channel (a row
per channel, a column per region, with every value under the mouse when
the channels are too many to write).
A row is a family and a region, a column a layer of height (by default the
km layers of the verifprofile scorecard; each layered theme can be given
its own edges, the pressure of a standard atmosphere written under them),
and a last column, total, for the layers shown together; the surface and
whole-column families sit in a column of their own.

Every cell says two things:

* the change over the whole period, Exp against Ctl, in percent: the
  sigma of O-P, and its |bias| in percent of the sigma of the control.
  This sets the colour: red where the experience is better, blue where it
  is worse, grey where the test does not pass or the change is below
  0.5 %;
* in how many cycles the experience was better, e.g. ``41/56``: the same
  comparison, cycle by cycle. A change made by three good days and a
  change seen every day read the same in percent; they do not here.

The test is the one of every Pikobs module: with MATCH on, the cycle block
bootstrap of the change of each cycle; with MATCH off, the t-test and the
F-test over the period; MATCH no draws without a test. The radiances are
tested on their cycles in every mode (their sigma pools channels, which
no F-test covers).

A wind is its two components as one: the sigma of the vector,
:math:`\sqrt{(\sigma_u^2 + \sigma_v^2)/2}`, and the length of its mean.
A family of channels is scored on its sigma, the channels pooled by their
counts, and on the number of observations it used: more radiances passing
the background check is a result in itself. It has no bias column, since
the bias correction takes the bias away.

Where it goes
-------------

``<pathwork>/pikobs_obsscorecard_viewer.html`` holds every card: the card
(the themes in order, each channel card after the radiances), the
comparison (the control against each experience), the criterion, the land
filter and, when several were drawn, MATCH. The surface and channel cards
give their values under the mouse. Beside every PNG, a CSV with the
numbers of its cells.

How it reads
------------

Every cycle is read once, by :mod:`pikobs.reader`, and its sums are kept in
``<pathwork>/obsscorecard/sums_<ctl>_vs_<exp>.db``: run the module again on
a longer period and it reads only the cycles it does not have yet. The
cycles whose background is the same in both runs (the first cycle of an
experiment) are found and left out, and the page says how many.
"""

import math
import os
import sys
import time
import traceback
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

import pikobs
from pikobs.configobs.special_family import SCORECARD_THEMES, scorecard_families
from pikobs.match import parse_modes
from pikobs.obsdb import (available_cycles, cycle_path, cycles as cycle_list,
                          open_result, safe_name, split_tokens)
from pikobs.reader import Ask, cells, done_cycles, read_cycle, write_sums
from pikobs.stats import (cycle_bootstrap_confidence, is_significant,
                          sigma_confidence, ttest_confidence)
from pikobs.stats.stats import BOOT_MIN_CYCLES, BOOT_MIN_PAIRS
from pikobs.verifprofile.scorecard import BANDS_KM, MIN_CHANGE_PCT, MIN_OBS_PER_CELL

MODULE = "obsscorecard"
#: the regions of a card when none is asked: the globe, its three bands and
#: North America (the classic ARCAD domains)
DEFAULT_REGIONS = ("Monde", "ExtratropiquesNord", "Tropiques", "ExtratropiquesSud",
                   "AmeriqueduNord")
#: fewer cycles common to both runs and nothing is drawn
MIN_CYCLES = 4
#: the column of the families with no height: surface, whole column
SURFACE = "sfc"
#: every level of a row together, the last column of a card
TOTAL = "total"
#: the edges of the layers, km, when none is asked: those of verifprofile
DEFAULT_EDGES_KM = [BANDS_KM[0][0]] + [hi for _, hi in BANDS_KM]
#: the themes whose rows are layered; their edges can be asked one by one
LAYERED_THEMES = ("winds", "thermodynamics", "ro_ch")
SCALE_HEIGHT_KM = 7.0


def bands_of(edges_km: Optional[Sequence[float]]) -> List[Tuple[float, float]]:
    """The layers from their edges, km (the default edges when none)."""
    e = sorted(float(x) for x in (edges_km or DEFAULT_EDGES_KM))
    if len(e) < 2:
        raise ValueError(f"layers: at least two edges, got {list(edges_km)}")
    return list(zip(e[:-1], e[1:]))


def layer_name(lo: float, hi: float) -> str:
    return f"{lo:g}-{hi:g}"


# ─────────────────────────────────────────────────────────────────────────────
# Reading: one task per run, cycle and family
# ─────────────────────────────────────────────────────────────────────────────

def sums_db(pathwork: str, ctl: str, exp: str, cell_list=()) -> str:
    """The kept sums of one Exp vs Ctl, for one set of cells: other regions,
    criteria or land filters are another file, read from the start (a
    cycle kept for some regions has nothing for the others)."""
    import hashlib
    sig = "|".join(sorted(f"{c.region},{c.flag},{c.land_ocean}" for c in cell_list))
    tag = f"_{hashlib.md5(sig.encode()).hexdigest()[:8]}" if sig else ""
    return os.path.join(pathwork, MODULE, f"sums_{safe_name(ctl)}_vs_{safe_name(exp)}{tag}.db")


#: the families some row of a theme splits by codtyp: their sums are kept by
#: codtyp too, in a table of their own (_ct), so they never mix with sums
#: kept without it
CODTYP_FAMILIES = {r["family"] for rows in SCORECARD_THEMES.values() for r in rows
                   if r.get("codtyp")}


def flag_exp_only(family: str, families: Sequence[str]) -> bool:
    """Whether a family is read with the flag criterion on the experience
    only: named in ``families``, itself or by an alias of the catalogue."""
    if not families:
        return False
    try:
        from pikobs.configobs.families import _ALIASES, known_base
        names = set(_ALIASES.get(known_base(family) or family, (family,))) | {family}
    except Exception:
        names = {family}
    return bool(names & set(families))


def _table(family: str, mode: str, exp_flag: Sequence[str] = ()) -> str:
    base = f"{safe_name(family).replace('.', '_').replace('-', '_')}_{mode}"
    return (base + ("_ct" if family in CODTYP_FAMILIES else "")
            + ("_fx" if flag_exp_only(family, exp_flag) else ""))


def family_varnos(themes: Sequence[str]) -> Dict[str, List[int]]:
    """family -> every BUFR code the themes score it on."""
    out: Dict[str, List[int]] = {}
    for t in themes:
        for row in SCORECARD_THEMES[t]:
            for v in row["varnos"]:
                out.setdefault(row["family"], [])
                if v not in out[row["family"]]:
                    out[row["family"]].append(v)
    return out


def read_task(task: Dict[str, Any]) -> Optional[int]:
    """One family of one cycle of one Exp vs Ctl: read it in every mode it
    needs and keep its sums. Returns the number of rows kept."""
    try:
        fam, cycle = task["family"], task["cycle"]
        _, VCOORD, *_ = pikobs.family(fam)
        n = 0
        for mode in task["read_modes"]:
            group = {"varno": "varno", "level": VCOORD}
            if fam in CODTYP_FAMILIES:
                group["codtyp"] = "CAST(codtyp AS INTEGER)"
            ask = Ask(family=fam, cells=task["cells"], group=group,
                      flag_on="exp" if task.get("flag_exp") else "both",
                      varnos=task["varnos"], values=("omp", "oma"), match=mode)
            sums = read_cycle(task["ctl_file"], task["exp_file"], ask, cycle,
                              pathwork=task["pathwork"], module=MODULE)
            if sums is None:
                return None
            n += write_sums(sums, task["db"],
                            _table(fam, mode, [fam] if task.get("flag_exp") else ()), cycle)
        return n
    except Exception:
        print(f"[{MODULE}] reading failed: {task.get('family')} {task.get('cycle')}\n"
              f"{traceback.format_exc()}", file=sys.stderr, flush=True)
        return None


_SQLITE_MAGIC = b"SQLite format 3\x00"


def is_sqlite(path: str) -> bool:
    """Whether a file is an SQLite database, by its first 16 bytes: a BURP
    file or an archive in its place is told before any reading."""
    try:
        with open(path, "rb") as fh:
            return fh.read(16) == _SQLITE_MAGIC
    except OSError:
        return False


def file_name(run_path: str, family: str, cycles: Sequence[str]) -> Optional[str]:
    """The name a run's files carry for a family: the family itself, or the
    alias of the catalogue with the most cycles of the period (G2 writes
    to_amsua_allsky, a bgckalt writes ra for radar). None when there is none."""
    try:
        from pikobs.configobs.families import _ALIASES, known_base
        names = _ALIASES.get(known_base(family) or family, (family,))
    except Exception:
        names = (family,)
    names = list(dict.fromkeys([family, *names]))
    want = set(cycles)
    best = max(names, key=lambda n: len(set(available_cycles(run_path, n)) & want))
    return best if set(available_cycles(run_path, best)) & want else None


def plan_reading(control, experiment, families, varnos, cycles, read_modes, cell_list,
                 pathwork, exp_flag: Sequence[str] = ()
                 ) -> Tuple[List[Dict[str, Any]], Dict[str, List[str]]]:
    """The tasks still to run, and the cycles each family has in both runs.

    A family is read where both runs hold its file; the cycles already kept
    are not read again."""
    db = sums_db(pathwork, control[0], experiment[0], cell_list)
    os.makedirs(os.path.dirname(db), exist_ok=True)
    tasks, have = [], {}
    for fam in families:
        # each run under the name its files carry (to_amsua_allsky, ra ...)
        ctl_name = file_name(control[1], fam, cycles)
        exp_name = file_name(experiment[1], fam, cycles)
        if not (ctl_name and exp_name):
            continue
        both = sorted(set(available_cycles(control[1], ctl_name))
                      & set(available_cycles(experiment[1], exp_name)) & set(cycles))
        if not both:
            continue
        not_sqlite = [f"{run} {path}" for run, path in
                      (("Ctl", cycle_path(control[1], both[0], ctl_name)),
                       ("Exp", cycle_path(experiment[1], both[0], exp_name)))
                      if not is_sqlite(path)]
        if not_sqlite:
            print(f"[{MODULE}] {fam}: not an SQLite file (BURP?), left out: "
                  + "; ".join(not_sqlite), file=sys.stderr, flush=True)
            have[fam] = []                    # said already: not "no file" as well
            continue
        if (ctl_name, exp_name) != (fam, fam):
            print(f"[{MODULE}] {fam}: read as {ctl_name} (Ctl) and {exp_name} (Exp)", flush=True)
        have[fam] = both
        fx = flag_exp_only(fam, exp_flag)
        if fx:
            print(f"[{MODULE}] {fam}: the flag criterion on Exp only, Ctl read without it; "
                  f"on the MATCH on cards only", flush=True)
        done = set.intersection(*(set(done_cycles(db, _table(fam, m, exp_flag)))
                                  for m in read_modes))
        for c in both:
            if int(c) in done:
                continue
            tasks.append(dict(family=fam, cycle=c, varnos=varnos[fam],
                              ctl_file=cycle_path(control[1], c, ctl_name),
                              exp_file=cycle_path(experiment[1], c, exp_name),
                              read_modes=read_modes, cells=cell_list, db=db,
                              pathwork=pathwork, flag_exp=fx))
    return tasks, have


def load_sums(db: str, family: str, mode: str, cycles: Sequence[str],
              exp_flag: Sequence[str] = ()) -> Optional[pd.DataFrame]:
    """The kept sums of a family, for the cycles of the period only."""
    if not os.path.isfile(db):
        return None
    table = _table(family, mode, exp_flag)
    with open_result(db) as conn:
        ok = conn.execute("SELECT 1 FROM sqlite_master WHERE name = ?;", (table,)).fetchone()
        if not ok:
            return None
        df = pd.read_sql_query(f"SELECT * FROM {table};", conn)
    # numbers as numbers, whatever the table declared (a table written by an
    # older reader may hold them as text)
    for col in df.columns:
        if col in ("region", "flag", "land_ocean", "special"):
            continue
        try:
            df[col] = pd.to_numeric(df[col])
        except (ValueError, TypeError):
            pass
    return df[df["cycle"].astype(int).astype(str).isin(set(cycles))]


# ─────────────────────────────────────────────────────────────────────────────
# Layers
# ─────────────────────────────────────────────────────────────────────────────

def layer_of(levels: np.ndarray, vcotyp: str,
             bands: Optional[Sequence[Tuple[float, float]]] = None) -> np.ndarray:
    """The column of each level: 'sfc' for the families with no height,
    the km layer otherwise (a layer holds its top edge, the first its
    bottom too, as in verifprofile)."""
    kind = str(vcotyp).upper()
    lev = np.asarray(levels, float)
    if kind.startswith("PRESSION"):
        with np.errstate(divide="ignore", invalid="ignore"):
            z = -SCALE_HEIGHT_KM * np.log(lev / 101325.0)
    elif kind.startswith("HAUTEUR"):
        z = lev / 1000.0
    else:
        return np.full(lev.shape, SURFACE, dtype=object)
    out = np.full(lev.shape, None, dtype=object)
    for b, (lo, hi) in enumerate(bands or bands_of(None)):
        sel = ((z > lo) | ((b == 0) & (z >= lo))) & (z <= hi)
        out[sel] = layer_name(lo, hi)
    return out


# ─────────────────────────────────────────────────────────────────────────────
# The score of a cell
# ─────────────────────────────────────────────────────────────────────────────

def _moments(n, s, s2):
    with np.errstate(divide="ignore", invalid="ignore"):
        m = np.where(n > 0, s / n, np.nan)
        v = np.maximum(np.where(n > 0, s2 / n - m * m, np.nan), 0.0)
    return m, v


def _bias_sigma(comp: Dict[str, np.ndarray], side: str, combine: str):
    """(bias, sigma, n) of one run from the sums of its components, along the
    last axis of the arrays (one value per cycle, or the period)."""
    n, s, s2 = comp[f"n{side}"], comp[f"s{side}"], comp[f"s{side}2"]
    m, v = _moments(n, s, s2)                       # shape (components, ...)
    ntot = n.sum(axis=0)
    with np.errstate(divide="ignore", invalid="ignore"):
        if combine == "vector":
            bias = np.sqrt(np.nansum(m * m, axis=0))
            sigma = np.sqrt(np.where(ntot > 0, np.nansum(n * v, axis=0) / ntot, np.nan))
        else:
            bias, sigma = m[0], np.sqrt(v[0])
    return bias, sigma, ntot


def _wins(better: np.ndarray, worse: np.ndarray) -> Tuple[int, int]:
    """(cycles the experience won, cycles that counted): a tie counts for
    neither."""
    return int(np.sum(better)), int(np.sum(better | worse))


def score_cell(per_cycle: Dict[str, np.ndarray], combine: str, mode: str) -> Optional[Dict]:
    """The score of one cell from the sums of every cycle.

    ``per_cycle`` holds, per component (first axis) and cycle (second),
    nc, sc, sc2, ne, se, se2 (and sce with MATCH on), and nallc, nalle.
    """
    period = {k: v.sum(axis=1) for k, v in per_cycle.items()}
    bc, sc, nc = _bias_sigma({k: v[:, None] for k, v in period.items()}, "c", combine)
    be, se, ne = _bias_sigma({k: v[:, None] for k, v in period.items()}, "e", combine)
    bc, sc, nc, be, se, ne = (float(x[0]) for x in (bc, sc, nc, be, se, ne))
    if nc < MIN_OBS_PER_CELL or ne < MIN_OBS_PER_CELL or not sc > 0:
        return None
    out = {"n_ctl": nc, "n_exp": ne, "bias_ctl": bc, "bias_exp": be,
           "sigma_ctl": sc, "sigma_exp": se,
           "d_sigma": 100.0 * (se - sc) / sc,
           "d_bias": 100.0 * (abs(be) - abs(bc)) / sc}
    # cycle by cycle, in units of the sigma of the control over the period
    kbc, ksc, knc = _bias_sigma(per_cycle, "c", combine)
    kbe, kse, kne = _bias_sigma(per_cycle, "e", combine)
    ok = (knc >= BOOT_MIN_PAIRS) & (kne >= BOOT_MIN_PAIRS)
    dsig = np.where(ok, 100.0 * (kse - ksc) / sc, np.nan)
    dbia = np.where(ok, 100.0 * (np.abs(kbe) - np.abs(kbc)) / sc, np.nan)
    out["sigma_wins"], out["cycles"] = _wins(ok & (kse < ksc), ok & (kse > ksc))
    out["bias_wins"], out["bias_cycles"] = _wins(ok & (np.abs(kbe) < np.abs(kbc)),
                                                 ok & (np.abs(kbe) > np.abs(kbc)))
    if mode == "on":
        out["sigma_conf"] = float(cycle_bootstrap_confidence(dsig))
        out["bias_conf"] = float(cycle_bootstrap_confidence(dbia))
    elif mode == "off":
        out["sigma_conf"] = float(sigma_confidence(np.array([sc * sc]), np.array([se * se]),
                                                   np.array([nc]), np.array([ne]))[0])
        out["bias_conf"] = (float(ttest_confidence(np.array([bc]), np.array([sc]), np.array([nc]),
                                                   np.array([be]), np.array([se]),
                                                   np.array([ne]))[0])
                            if combine == "scalar" else float("nan"))
    else:
        out["sigma_conf"] = out["bias_conf"] = float("nan")
    return out


def _n_score(nallc: np.ndarray, nalle: np.ndarray, mode: str) -> Dict[str, float]:
    """The change in the number of observations used: over the period, in
    how many cycles the experience used more, and its test on the cycles
    (the only test a count has here)."""
    with np.errstate(divide="ignore", invalid="ignore"):
        dn = np.where(nallc > 0, 100.0 * (nalle - nallc) / nallc, np.nan)
    ok = np.isfinite(dn)
    wins, total = _wins(ok & (dn > 0), ok & (dn < 0))
    # nothing in the control: there is no percent to give (the cell stays empty)
    d_n = (100.0 * (nalle.sum() - nallc.sum()) / nallc.sum() if nallc.sum() > 0
           else float("nan"))
    return {"d_n": d_n,
            "n_wins": wins, "n_cycles": total,
            # more observations is better: the test sees a decrease as a gain
            "n_conf": float("nan") if mode == "no" else float(cycle_bootstrap_confidence(-dn))}


def score_channels(per_chan: Dict[int, Dict[str, np.ndarray]], mode: str) -> Optional[Dict]:
    """The score of a family of channels: the sigma change of each channel,
    pooled by its count, and the change in the number of observations used.
    Tested on the cycles in every mode."""
    d_period, w_period, d_cycles, w_cycles = [], [], [], []
    nallc = nalle = None
    for ch, pc in per_chan.items():
        p = {k: v.sum(axis=1) for k, v in pc.items()}
        _, sc, nc = _bias_sigma({k: v[:, None] for k, v in p.items()}, "c", "scalar")
        _, se, ne = _bias_sigma({k: v[:, None] for k, v in p.items()}, "e", "scalar")
        sc, se, nc = float(sc[0]), float(se[0]), float(nc[0])
        nallc = pc["nallc"][0] if nallc is None else nallc + pc["nallc"][0]
        nalle = pc["nalle"][0] if nalle is None else nalle + pc["nalle"][0]
        if nc < MIN_OBS_PER_CELL or not sc > 0:
            continue
        d_period.append(100.0 * (se - sc) / sc)
        w_period.append(nc)
        _, ksc, knc = _bias_sigma(pc, "c", "scalar")
        _, kse, kne = _bias_sigma(pc, "e", "scalar")
        ok = (knc >= BOOT_MIN_PAIRS) & (kne >= BOOT_MIN_PAIRS)
        d_cycles.append(np.where(ok, 100.0 * (kse - ksc) / sc, 0.0))
        w_cycles.append(np.where(ok, knc, 0.0))
    if not w_period or nallc is None:
        return None
    w = np.array(w_period)
    dc, wc = np.array(d_cycles), np.array(w_cycles)
    with np.errstate(divide="ignore", invalid="ignore"):
        dsig = np.where(wc.sum(axis=0) > 0, (dc * wc).sum(axis=0) / wc.sum(axis=0), np.nan)
    out = {"n_ctl": float(nallc.sum()), "n_exp": float(nalle.sum()),
           "d_sigma": float((np.array(d_period) * w).sum() / w.sum()),
           "channels": len(w_period), **_n_score(nallc, nalle, mode)}
    ok = np.isfinite(dsig)
    out["sigma_wins"], out["cycles"] = _wins(ok & (dsig < 0), ok & (dsig > 0))
    out["sigma_conf"] = (float("nan") if mode == "no"
                         else float(cycle_bootstrap_confidence(dsig)))
    return out


# ─────────────────────────────────────────────────────────────────────────────
# A whole card
# ─────────────────────────────────────────────────────────────────────────────

def _components(df: pd.DataFrame, varnos: Sequence[int], cyc_index: Dict[int, int],
                mode: str) -> Dict[str, np.ndarray]:
    """The sums of every component (one per varno) and cycle, O-P."""
    k, n_cyc = len(varnos), len(cyc_index)
    names = {"nc": "nc_omp", "sc": "sc_omp", "sc2": "sc2_omp", "ne": "ne_omp",
             "se": "se_omp", "se2": "se2_omp", "nallc": "nallc_omp", "nalle": "nalle_omp"}
    out = {key: np.zeros((k, n_cyc)) for key in names}
    for j, v in enumerate(varnos):
        sub = df[df["varno"].astype(int) == int(v)]
        if sub.empty:
            continue
        g = sub.groupby("cycle")[list(names.values())].sum()
        idx = [cyc_index[int(c)] for c in g.index]
        for key, col in names.items():
            out[key][j, idx] = g[col].fillna(0.0).to_numpy(float)
    # with MATCH on the pairs count for both runs
    return out


def identical_cycles(db: str, families: Sequence[str], cycles: Sequence[str],
                     exp_flag: Sequence[str] = ()) -> List[int]:
    """The cycles whose background is the same in both runs: every pair has
    O-P equal in the two (the first cycle of an experiment). Needs MATCH on."""
    tot: Dict[int, List[float]] = {}
    for fam in families:
        df = load_sums(db, fam, "on", cycles, exp_flag)
        if df is None or df.empty:
            continue
        d = df.assign(diff=df["sc2_omp"].fillna(0) + df["se2_omp"].fillna(0)
                      - 2 * df["sce_omp"].fillna(0), ref=df["sc2_omp"].fillna(0))
        for c, g in d.groupby("cycle"):
            t = tot.setdefault(int(c), [0.0, 0.0])
            t[0] += float(g["diff"].sum())
            t[1] += float(g["ref"].sum())
    return sorted(c for c, (d, r) in tot.items() if r > 0 and abs(d) <= 1e-12 * r)


def score_theme(theme: str, db: str, mode: str, cycles: Sequence[str], skip: Sequence[int],
                regions: Sequence[str], flag: str, land_ocean: str,
                exp_flag: Sequence[str] = (),
                bands: Optional[Sequence[Tuple[float, float]]] = None) -> pd.DataFrame:
    """Every cell of one card: one row per (theme row, region, layer), and
    for a row with heights, its total over every level."""
    read_mode = "on" if mode == "on" else "off"
    keep = [c for c in cycles if int(c) not in set(skip)]
    cyc_index = {int(c): i for i, c in enumerate(keep)}
    out = []
    for row in SCORECARD_THEMES[theme]:
        fam = row["family"]
        df = load_sums(db, fam, read_mode, keep, exp_flag)
        if df is None or df.empty:
            continue
        df = df[(df["flag"] == flag) & (df["land_ocean"] == land_ocean)]
        vcotyp = pikobs.family(fam)[5]
        fx = flag_exp_only(fam, exp_flag)
        if fx and mode != "on":
            # the control read without the flag holds every observation, the
            # rejected ones too: only the pairs (MATCH on) put the two runs
            # on the same observations, those the experience assimilated
            continue
        if row.get("codtyp"):
            df_row = df[df["codtyp"].astype("Int64").astype(str).isin(
                [str(c) for c in row["codtyp"]])]
        else:
            df_row = df
        block = row.get("block") or pikobs.family(fam)[0]
        for region in regions:
            reg = df_row[df_row["region"] == region]
            if reg.empty:
                continue
            base = {"theme": theme, "family": fam, "block": block, "label": row["label"],
                    "region": region, "flag": flag, "land_ocean": land_ocean,
                    "combine": row["combine"], "flag_exp_only": fx}
            if row["combine"] == "channels":
                per_chan = {}
                for ch, g in reg.groupby("level"):
                    per_chan[ch] = _components(g, row["varnos"], cyc_index, read_mode)
                s = score_channels(per_chan, mode)
                if s:
                    out.append({**base, "layer": "all", **s})
                continue
            # the surface theme has no heights: its "level" is 10 m for sf,
            # 9999 for sc and the latitude for gp, none of them a layer
            layers = (np.full(len(reg), SURFACE, dtype=object)
                      if row.get("column") or theme == "surface"
                      else layer_of(reg["level"].to_numpy(), vcotyp, bands))
            reg = reg.assign(layer=layers)
            for layer, g in reg.groupby("layer"):
                s = score_cell(_components(g, row["varnos"], cyc_index, read_mode),
                               row["combine"], mode)
                if s:
                    out.append({**base, "layer": layer, **s})
            # the layers of the card together, when the row has more than one:
            # the observations of the columns shown, none above or below them
            inside = reg[reg["layer"].notna() & (reg["layer"] != SURFACE)]
            if theme in LAYERED_THEMES and not inside.empty:
                s = score_cell(_components(inside, row["varnos"], cyc_index, read_mode),
                               row["combine"], mode)
                if s:
                    out.append({**base, "layer": TOTAL, **s})
    return pd.DataFrame(out)


def score_by_channel(db: str, mode: str, cycles: Sequence[str], skip: Sequence[int],
                     regions: Sequence[str], flag: str, land_ocean: str) -> pd.DataFrame:
    """The radiances channel by channel: one row per (family, region,
    channel), each channel scored as any scalar cell (with MATCH off its
    sigma has its F-test), and the change in the observations it used."""
    read_mode = "on" if mode == "on" else "off"
    keep = [c for c in cycles if int(c) not in set(skip)]
    cyc_index = {int(c): i for i, c in enumerate(keep)}
    out = []
    for row in SCORECARD_THEMES["radiances"]:
        fam = row["family"]
        df = load_sums(db, fam, read_mode, keep)
        if df is None or df.empty:
            continue
        df = df[(df["flag"] == flag) & (df["land_ocean"] == land_ocean)]
        for region in regions:
            for ch, g in df[df["region"] == region].groupby("level"):
                comp = _components(g, row["varnos"], cyc_index, read_mode)
                base = {"family": fam, "region": region, "channel": float(ch),
                        "n_ctl": float(comp["nallc"].sum()), "n_exp": float(comp["nalle"].sum())}
                if base["n_ctl"] < MIN_OBS_PER_CELL and base["n_exp"] < MIN_OBS_PER_CELL:
                    continue
                s = score_cell(comp, "scalar", mode) or {}
                out.append({**base, **_n_score(comp["nallc"][0], comp["nalle"][0], mode),
                            **{k: s.get(k, float("nan")) for k in
                               ("d_sigma", "sigma_conf", "sigma_wins", "cycles",
                                "sigma_ctl", "sigma_exp")}})
    return pd.DataFrame(out)


# ─────────────────────────────────────────────────────────────────────────────
# The run
# ─────────────────────────────────────────────────────────────────────────────

def make_obsscorecard(experiments, control, pathwork, datestart, dateend,
                      regions=DEFAULT_REGIONS, flags=("assimilee",), themes=None,
                      land_ocean=("all",), match=("on",), n_cpu=1, svg=False,
                      min_cycles=MIN_CYCLES, exp_flag: Sequence[str] = (),
                      layers: Optional[Dict[str, Sequence[float]]] = None) -> int:
    """Read what is missing, score every card, draw them. Returns 0 when at
    least one card was drawn. ``layers``: theme -> the edges of its layers
    in km (winds, thermodynamics, ro_ch); a theme not given takes the
    default edges."""
    from pikobs.parallel import run_tasks, start_workers, stop_workers

    t0 = time.time()
    themes = [t for t in (themes or list(SCORECARD_THEMES)) if t in SCORECARD_THEMES]
    modes, _ = parse_modes(match)
    # off and no read the same sums; on reads the pairs
    read_modes = sorted({"on" if m == "on" else "off" for m in modes})
    families = scorecard_families(themes)
    varnos = family_varnos(themes)
    cyc = cycle_list(datestart, dateend)
    cell_list = cells(regions, flags, land_ocean)
    bands = {t: bands_of((layers or {}).get(t)) for t in LAYERED_THEMES}
    print(f"[{MODULE}] {len(cyc)} cycles, themes {', '.join(themes)}, "
          f"regions {', '.join(regions)}, MATCH {' '.join(modes)}", flush=True)
    for t in LAYERED_THEMES:
        if t in themes:
            print(f"[{MODULE}] {t} layers (km): "
                  + " ".join(layer_name(*b) for b in bands[t])
                  + ("" if (layers or {}).get(t) else "  (default)"), flush=True)

    # (client, its own temporary folder): only that folder is removed at the end
    client, dask_dir = start_workers(n_cpu, MODULE)
    figures, runs = [], []
    try:
        for exp in experiments:
            tasks, have = plan_reading(control, exp, families, varnos, cyc, read_modes,
                                       cell_list, pathwork, exp_flag)
            absent = [f for f in families if f not in have]
            have = {f: c for f, c in have.items() if c}
            if absent:
                print(f"[{MODULE}] {exp[0]}: no file in both runs for "
                      f"{', '.join(absent)} -- left out", flush=True)
            if tasks:
                print(f"[{MODULE}] {exp[0]}: reading {len(tasks)} family-cycles "
                      f"({sum(len(v) for v in have.values()) - len(tasks)} already kept)",
                      flush=True)
                run_tasks(read_task, [(t,) for t in tasks], client, label=f"{MODULE} read")
            db = sums_db(pathwork, control[0], exp[0], cell_list)
            common = sorted(set().union(*have.values())) if have else []
            skip = (identical_cycles(db, list(have), common, exp_flag)
                    if "on" in read_modes else [])
            if skip:
                print(f"[{MODULE}] {exp[0]}: {len(skip)} cycle(s) with the same background "
                      f"in both runs, left out: {' '.join(map(str, skip))}", flush=True)
            n_used = len(common) - len(skip)
            if n_used < min_cycles:
                print(f"[{MODULE}] {exp[0]}: only {n_used} usable cycles, fewer than "
                      f"{min_cycles}: no card", file=sys.stderr, flush=True)
                continue
            if n_used < BOOT_MIN_CYCLES and "on" in modes:
                print(f"[{MODULE}] {exp[0]}: {n_used} cycles; the cycle bootstrap tests "
                      f"from {BOOT_MIN_CYCLES}, so MATCH on cells stay grey", flush=True)
            runs.append(dict(exp=exp[0], db=db, common=common, skip=skip, n_used=n_used))

        # 2. the cards of each experience, every theme, in parallel
        card_tasks = [dict(theme=theme, mode=mode, flag=flag, lo=lo, ctl=control[0],
                           regions=list(regions), datestart=datestart, dateend=dateend,
                           pathwork=pathwork, svg=svg, exp_flag=list(exp_flag),
                           layers=bands, **run)
                      for run in runs for mode in modes for flag in flags
                      for lo in land_ocean for theme in themes]
        all_cells = []
        for r in run_tasks(card_task, [(t,) for t in card_tasks], client,
                           label=f"{MODULE} cards"):
            if r:
                figures += r["items"]
                if r["cells"] is not None:
                    all_cells.append(r["cells"])

        # 3. every experience side by side: a card per theme and region
        if len(runs) > 1 and all_cells:
            every = pd.concat(all_cells, ignore_index=True)
            names = [r["exp"] for r in runs]
            used = sorted({r["n_used"] for r in runs})
            n_txt = f"{used[0]}" if len(used) == 1 else f"{used[0]} to {used[-1]}"
            all_tasks = []
            for (mode, flag, lo, theme), g in every.groupby(["match", "flag", "land_ocean",
                                                             "theme"], sort=False):
                for region in regions:
                    gr = g[g["region"] == region]
                    if not gr.empty:
                        all_tasks.append(dict(cells=gr, theme=theme, mode=mode, flag=flag,
                                              lo=lo, region=region, exps=names,
                                              ctl=control[0], n_cycles=n_txt,
                                              datestart=datestart, dateend=dateend,
                                              pathwork=pathwork, svg=svg))
            figures += [r for r in run_tasks(all_card_task, [(t,) for t in all_tasks], client,
                                             label=f"{MODULE} all experiences") if r]
    finally:
        stop_workers(client, dask_dir)
    print(f"[{MODULE}] {len(figures)} card(s) in {time.time() - t0:.0f} s", flush=True)
    if figures:
        write_viewer(figures, pathwork, themes, experiments, control, (datestart, dateend))
    return 0 if figures else 1


def card_task(t: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """One theme of one Exp vs Ctl: its cells, its card (and, for the
    radiances, its channel cards). Returns the viewer items and the cells."""
    from pikobs.obsscorecard.obsscorecard_plot import draw_card, draw_surface_card
    try:
        theme, mode, flag, lo, exp, ctl = (t[k] for k in ("theme", "mode", "flag", "lo",
                                                          "exp", "ctl"))
        cells_df = score_theme(theme, t["db"], mode, t["common"], t["skip"], t["regions"],
                               flag, lo, t["exp_flag"], t["layers"].get(theme))
        if cells_df.empty:
            # say it: a card that is not drawn must not vanish silently
            print(f"[{MODULE}] {theme}: no card, no cell for {ctl} vs {exp} "
                  f"({flag}, {lo}, MATCH {mode}): none of its families scored in "
                  f"these regions", flush=True)
            return {"items": [], "cells": None}
        stem = (f"{MODULE}_{theme}_{safe_name(exp)}_vs_{safe_name(ctl)}_{safe_name(flag)}_"
                f"{safe_name(lo)}_match{mode}")
        out_dir = os.path.join(t["pathwork"], MODULE, theme)
        os.makedirs(out_dir, exist_ok=True)
        cells_df.to_csv(os.path.join(out_dir, stem + ".csv"), index=False)
        args = ((ctl, exp), mode, t["datestart"], t["dateend"], flag, lo, t["n_used"],
                len(t["skip"]), t["regions"], os.path.join(out_dir, stem + ".png"))
        png = (draw_surface_card(cells_df, *args, svg=t["svg"]) if theme == "surface"
               else draw_card(cells_df, theme, *args, svg=t["svg"]))
        item = {"comparison": f"{ctl} vs {exp}", "region": "every region", "flag": flag,
                "land_ocean": lo, "match": mode}
        items = [{**item, "card": _card_key(theme),
                  "filename": os.path.relpath(png, t["pathwork"])}]
        if theme == "radiances":
            for fam, p in _channel_cards(t["db"], mode, t["common"], t["skip"], t["regions"],
                                         flag, lo, ctl, exp, t["datestart"], t["dateend"],
                                         t["n_used"], t["pathwork"], t["svg"]):
                items.append({**item, "card": _card_key(theme, fam),
                              "filename": os.path.relpath(p, t["pathwork"])})
        return {"items": items, "cells": cells_df.assign(match=mode, exp=exp)}
    except Exception:
        print(f"[{MODULE}] card failed: {t.get('theme')} {t.get('exp')} {t.get('mode')}\n"
              f"{traceback.format_exc()}", file=sys.stderr, flush=True)
        return None


def all_card_task(t: Dict[str, Any]) -> Optional[Dict[str, str]]:
    """One theme in one region, every experience side by side."""
    from pikobs.obsscorecard.obsscorecard_plot import draw_all_card
    try:
        theme, mode, flag, lo, region = (t[k] for k in ("theme", "mode", "flag", "lo",
                                                        "region"))
        stem = (f"{MODULE}_{theme}_all_vs_{safe_name(t['ctl'])}_{safe_name(region)}_"
                f"{safe_name(flag)}_{safe_name(lo)}_match{mode}")
        out_dir = os.path.join(t["pathwork"], MODULE, "all_experiences")
        os.makedirs(out_dir, exist_ok=True)
        t["cells"].to_csv(os.path.join(out_dir, stem + ".csv"), index=False)
        png = draw_all_card(t["cells"], theme, region, t["exps"], t["ctl"], mode,
                            t["datestart"], t["dateend"], flag, lo, t["n_cycles"],
                            os.path.join(out_dir, stem + ".png"), svg=t["svg"])
        return {"comparison": f"{t['ctl']} vs every experience", "region": region,
                "flag": flag, "land_ocean": lo, "match": mode, "card": _card_key(theme),
                "filename": os.path.relpath(png, t["pathwork"])}
    except Exception:
        print(f"[{MODULE}] card failed: {t.get('theme')} {t.get('region')} every "
              f"experience\n{traceback.format_exc()}", file=sys.stderr, flush=True)
        return None


def _card_key(theme: str, family: Optional[str] = None) -> str:
    """The value of a card in the viewer: numbered so the cards come in the
    order of the themes, the channel cards after their theme."""
    order = list(SCORECARD_THEMES)
    n = order.index(theme) + 1 if theme in order else 99
    return f"{n}_{theme}" + (f"_{family}" if family else "")


def write_viewer(items: List[Dict[str, str]], pathwork: str, themes, experiments, control,
                 period) -> str:
    """pikobs_obsscorecard_viewer.html in PATHWORK: a card, a comparison,
    a criterion (and MATCH when there are several) to choose; the values
    under the mouse where a card has them."""
    from pikobs.obsscorecard.obsscorecard_plot import THEME_TITLE
    from pikobs.web.runs import runs_block
    from pikobs.web.viewer import generate_web
    keys = ["card", "comparison", "region", "flag", "land_ocean"]
    if len({it["match"] for it in items}) > 1:
        keys.append("match")
    labels = {}
    for it in items:
        num, rest = it["card"].split("_", 1)
        for t in SCORECARD_THEMES:
            if rest == t:
                labels[it["card"]] = THEME_TITLE.get(t, t)
            elif rest.startswith(t + "_"):
                fam = rest[len(t) + 1:]
                labels[it["card"]] = f"{THEME_TITLE.get(t, t)}: {pikobs.family(fam)[0]} by channel"
    return generate_web(
        items, keys, os.path.join(pathwork, f"pikobs_{MODULE}_viewer.html"),
        title="Pikobs scorecards by theme",
        subtitle=("O-P of each experience against the control, theme by theme: the change "
                  "over the period in colour, the cycles the experience won under it."
                  + runs_block(experiments, control, period)),
        value_labels={"card": labels, "match": {"on": "on", "off": "off", "no": "no"}},
        key_labels={"card": "Card", "comparison": "Comparison", "region": "Region",
                    "flag": "Criteria", "land_ocean": "Land filter", "match": "Match"})


def _channel_cards(db, mode, common, skip, regions, flag, lo, ctl, exp, datestart, dateend,
                   n_used, pathwork, svg) -> List[Tuple[str, str]]:
    """One card per family of channels, channel by channel: (family, png)."""
    from pikobs.obsscorecard.obsscorecard_plot import draw_channel_card
    detail = score_by_channel(db, mode, common, skip, regions, flag, lo)
    out = []
    if detail.empty:
        return out
    out_dir = os.path.join(pathwork, MODULE, "radiances_by_channel")
    os.makedirs(out_dir, exist_ok=True)
    for fam, g in detail.groupby("family", sort=False):
        stem = (f"{MODULE}_channels_{safe_name(fam)}_{safe_name(exp)}_vs_{safe_name(ctl)}_"
                f"{safe_name(flag)}_{safe_name(lo)}_match{mode}")
        g.to_csv(os.path.join(out_dir, stem + ".csv"), index=False)
        png = draw_channel_card(g, fam, (ctl, exp), mode, datestart, dateend, flag, lo,
                                n_used, len(skip), regions, os.path.join(out_dir, stem + ".png"),
                                svg=svg)
        out.append((fam, png))
    return out


_UNSET = ("", "undefined", None)


def arg_call() -> None:
    import argparse
    from pikobs.figures import svg_enabled
    from pikobs.pbs_submit import maybe_submit_to_pbs

    p = argparse.ArgumentParser(prog="pikobs-obsscorecard",
                                description="Scorecards by theme, control vs experience(s).")
    p.add_argument("--path_control_files", default="")
    p.add_argument("--control_name", default="")
    p.add_argument("--path_experience_files", nargs="+", default=[])
    p.add_argument("--experience_name", nargs="+", default=[])
    p.add_argument("--pathwork", default=None)
    p.add_argument("--datestart", default=None)
    p.add_argument("--dateend", default=None)
    p.add_argument("--region", nargs="+", default=list(DEFAULT_REGIONS))
    p.add_argument("--flags_criteria", nargs="+", default=["assimilee"])
    p.add_argument("--themes", nargs="+", default=list(SCORECARD_THEMES),
                   help=f"Cards to draw: {' '.join(SCORECARD_THEMES)}.")
    p.add_argument("--land_ocean", nargs="+", default=["all"], choices=["all", "land", "ocean"])
    p.add_argument("--match", nargs="+", default=["on"],
                   help="on: matched observations, cycle bootstrap. off: all observations, "
                        "t-test and F-test. no: no test. Several at once: on off no.")
    p.add_argument("--min_cycles", type=int, default=MIN_CYCLES)
    for t in LAYERED_THEMES:
        p.add_argument(f"--layers_{t}", nargs="*", type=float, default=[],
                       help=f"Edges of the {t} layers, km (e.g. 0 1 2 3 5 7). Empty: "
                            f"{' '.join(f'{x:g}' for x in DEFAULT_EDGES_KM)}.")
    p.add_argument("--flag_exp_only", nargs="*", default=[],
                   help="Families whose flag criterion is applied to the experience only, the "
                        "control read without it: for a control that does not assimilate the "
                        "family, read from its bgckalt (e.g. radar against a run without radar).")
    p.add_argument("--svg", default="off", choices=["on", "off"])
    p.add_argument("--n_cpus", "--n_cpu", default=1, type=int, dest="n_cpus")
    p.add_argument("--no_submit", action="store_true",
                   help="Skip PBS auto-submission and run locally.")
    args = p.parse_args()
    for attr in ("region", "flags_criteria", "themes", "flag_exp_only"):
        setattr(args, attr, split_tokens(getattr(args, attr)))
    for arg in vars(args):
        print(f"--{arg} {getattr(args, arg)}", flush=True)
    for attr in ("pathwork", "datestart", "dateend"):
        if getattr(args, attr) in _UNSET:
            p.error(f"--{attr} is required ({attr.upper()} in the wrapper)")
    paths = [x for x in split_tokens(args.path_experience_files) if x not in _UNSET]
    names = [x for x in split_tokens(args.experience_name) if x not in _UNSET]
    if not paths or len(paths) != len(names):
        p.error("one EXPERIENCE_NAME for each path of PATH_EXPERIENCE_FILES")
    if args.path_control_files in _UNSET or args.control_name in _UNSET:
        p.error("a scorecard compares experiences with a control: PATH_CONTROL_FILES and "
                "CONTROL_NAME are required. With a single run there is nothing to score: "
                "see cardio's resume, timeserie or vdedr")
    bad = [m for m in split_tokens(args.match) if m not in ("on", "off", "no")]
    if bad:
        p.error(f"--match takes on, off and no (several at once too), not {bad}")
    unknown = [t for t in args.themes if t not in SCORECARD_THEMES]
    if unknown:
        p.error(f"--themes: unknown {unknown}; known: {' '.join(SCORECARD_THEMES)}")
    control = (args.control_name, args.path_control_files.rstrip("/") or "/")
    experiments = [(n, x.rstrip("/") or "/") for n, x in zip(names, paths)]
    maybe_submit_to_pbs(args)
    sys.exit(make_obsscorecard(experiments, control, args.pathwork, args.datestart,
                               args.dateend, regions=args.region, flags=args.flags_criteria,
                               themes=args.themes, land_ocean=args.land_ocean,
                               match=args.match, n_cpu=args.n_cpus,
                               svg=svg_enabled(args.svg), min_cycles=args.min_cycles,
                               exp_flag=[x for x in args.flag_exp_only if x not in _UNSET],
                               layers={t: getattr(args, f"layers_{t}") for t in LAYERED_THEMES
                                       if getattr(args, f"layers_{t}")}))


if __name__ == "__main__":
    arg_call()
