"""pikobs.obschain figures: what is left of dbase at every stage.

One figure per family, branch, region and variable -- the variables of
the family in pikobs that reach postalt, each from the stage where it
first appears: a row per stage, from dbase to
postalt, with its observations, its channels for a radiance, a bar with its
share of dbase and what that step lost; then postalt split by what quality
control made of it -- assimilated, with its kinds, and not assimilated, by
its first reason, with the groups of pikobs.flags, the blacklist among them
-- each also as a share of dbase, and with its channels. For a radiance the
header says, per satellite, how many channels are wholly on the blacklist. The bars are on a log scale of the share: a stage that keeps 0.25 %
would not show beside 100 % otherwise.

A stage is compared with dbase on the variables every stage of the family
holds: a variable made on the way (the wind components) would inflate the
shares otherwise. A branch (the RARS stream kept apart until postalt) is
compared with the trunk it comes from: dbase and the stages before the
branches part, global and RARS together.

A CSV beside the figures holds the same numbers for every family.
"""
import csv
import os
import re
import sqlite3
from collections import OrderedDict, defaultdict
from typing import Dict, List, Optional, Sequence, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.lines  # noqa: E402
import matplotlib.ticker  # noqa: E402
import matplotlib.transforms  # noqa: E402

STAGE_COLOUR = "#7B8794"
ASSIM_COLOUR = "#2E7D32"
REJECT_COLOURS = ["#C62828", "#EF6C00", "#6A1B9A", "#1565C0", "#00838F",
                  "#AD1457", "#795548", "#9E9D24", "#546E7A", "#D81B60"]


# ---- reading ---------------------------------------------------------------

def _stages(conn) -> List[str]:
    return [r[0] for r in conn.execute("SELECT stage FROM stages ORDER BY position")]


def stations_of(path: str, region: str) -> List[str]:
    """The stations that reach the last stage."""
    with sqlite3.connect(path) as conn:
        last = _stages(conn)[-1]
        return [r[0] for r in conn.execute(
            "SELECT DISTINCT id_stn FROM counts WHERE stage = ? AND region = ? "
            "ORDER BY id_stn", (last, region))]


# the CMC codtyp of the conventional reports; a type not here takes the
# name of the cutoff file it comes from (ua_radiosonde -> RADIOSONDE)
CODTYP = {12: "SYNOP", 13: "SHIP", 14: "SYNOP MOBIL", 15: "METAR", 16: "SPECI",
          18: "DRIFTER", 32: "PILOT", 33: "PILOT SHIP", 34: "PILOT MOBIL",
          35: "TEMP", 36: "TEMP SHIP", 37: "TEMP DROP", 38: "TEMP MOBIL",
          42: "AMDAR", 128: "AIREP", 157: "ACARS", 177: "ADS"}


# the codtyp a type has before it is recoded, read from the G2: ua 235
# (cutoff) becomes 135 (derialt on), with the same order of counts
CODTYP_SOURCE = {"135": ("235",)}


def codtyp_names(path: str) -> Dict[str, str]:
    """{codtyp: 'TEMP (35)'} of a family grouped by type; {} otherwise.
    Every type the family has at any stage gets one."""
    with sqlite3.connect(path) as conn:
        if not conn.execute("SELECT 1 FROM sqlite_master WHERE name = 'codtyp_names'").fetchone():
            return {}
        from_files = dict(conn.execute("SELECT codtyp, name FROM codtyp_names"))
        every = [r[0] for r in conn.execute("SELECT DISTINCT id_stn FROM counts")]
    out = {}
    for ct in every:
        try:
            name = CODTYP.get(int(float(ct))) or from_files.get(ct)
        except ValueError:
            name = from_files.get(ct)
        out[ct] = f"{name} ({ct})" if name else f"type {ct}"
    return out


# the codes a variable of postalt travels under before it is made: the
# same observations, another code (read from G2: ua carries 12101 and 12103
# until derialt writes 12001 and 12192 with the same counts; ai and ua the
# wind direction and speed until evalalt writes u and v; sc its 10 m wind)
SOURCE_CODES = {
    12001: (12101,),          # temperature        <- air temperature
    12192: (12103,),          # dew point depression <- dew point
    12004: (12104,),          # 2 m temperature    <- 2 m air temperature
    12006: (12106,),          # 2 m dew point depression <- 2 m dew point
    11003: (11001,),          # u                  <- wind direction
    11004: (11002,),          # v                  <- wind speed
    11215: (11011,),          # 10 m u             <- 10 m wind direction
    11216: (11012,),          # 10 m v             <- 10 m wind speed
}


def observed_skip(varno: int) -> bool:
    """A code that is not an observation: class 33 of BUFR table B, the
    quality information (33007 per cent confidence, say)."""
    return 33000 <= int(varno) < 34000


def wanted_varnos(family: str) -> List[int]:
    """The variables pikobs follows for a family (its list of elements);
    [] when pikobs does not say."""
    tries = []
    try:
        from pikobs.configobs.families import family_varnos
        tries.append(lambda: family_varnos(family))
    except Exception:
        pass
    try:
        import pikobs
        tries.append(lambda: pikobs.family_varnos(family))
        tries.append(lambda: str(pikobs.family(family)[4]).split(","))
    except Exception:
        pass
    for t in tries:
        try:
            out = [int(str(v).strip()) for v in t() if str(v).strip()]
            if out:
                return out
        except Exception:
            continue
    return []


def rars_name(path: str, family: str) -> str:
    """The name of the RARS branch in the family selector: its file at the
    last stage it reaches (mwhs2_rars, to_amsua_allsky_rars; rars_atms for a
    route that ends in cutoff)."""
    with sqlite3.connect(path) as conn:
        stages = _stages(conn)
        best = None
        for stage, names in conn.execute("SELECT DISTINCT stage, files FROM files WHERE stream = 'rars'"):
            if best is None or stages.index(stage) > stages.index(best[0]):
                best = (stage, names.split()[0])
    return best[1] if best else f"{family}_rars"


def postalt_varnos(path: str) -> Dict[str, List[int]]:
    """{branch: the variables of the last stage}; the global branch takes
    the trunk."""
    with sqlite3.connect(path) as conn:
        last = _stages(conn)[-1]
        out = defaultdict(set)
        for stream, varno in conn.execute(
                "SELECT DISTINCT stream, varno FROM counts WHERE stage = ?", (last,)):
            out["global" if stream == "trunk" else stream].add(int(varno))
    return {k: sorted(v) for k, v in out.items()}


def twice_of(conn, region, parts, stn_codes, common) -> int:
    """The observations of postalt assimilated more than once (the same
    observation in two of its rows or files)."""
    if not conn.execute("SELECT 1 FROM sqlite_master WHERE name = 'twice'").fetchone():
        return 0
    q = ("SELECT varno, SUM(n) FROM twice WHERE region = ? "
         f"AND stream IN ({','.join('?' * len(parts))})"
         + (f" AND id_stn IN ({','.join('?' * len(stn_codes))})" if stn_codes else "")
         + " GROUP BY varno")
    return sum(n for v, n in conn.execute(q, [region] + list(parts) + list(stn_codes))
               if v in common)


def chain_rows(path: str, region: str, stn: Optional[str] = None,
               varno: Optional[int] = None) -> List[Dict]:
    """Per branch: the observations and channels of every stage, the trunk
    stages included, on the variables every one of them holds -- or on one
    variable, from the stage where it first appears; and the flags of the
    last stage on the same variables."""
    out = []
    with sqlite3.connect(path) as conn:
        stages = _stages(conn)
        # a type counted under another code before it is recoded (ua: the
        # BUFR TEMP is 235 until derialt writes it as 135)
        stn_codes = ((stn,) + CODTYP_SOURCE.get(stn, ())) if stn is not None else ()
        streams = [r[0] for r in conn.execute("SELECT DISTINCT stream FROM counts")]
        branches = [s for s in ("global", "rars") if s in streams]
        trunk = "trunk" in streams
        for branch in branches:
            # the global branch takes the trunk; the RARS branch has its own
            parts = (["trunk"] if trunk and branch == "global" else []) + [branch]
            per = OrderedDict()
            for stage in stages:
                one = (f" AND id_stn IN ({','.join('?' * len(stn_codes))})"
                       if stn is not None else "")
                arg = list(stn_codes) if stn is not None else []
                q = ("SELECT varno, SUM(n) FROM counts WHERE stage = ? AND region = ? "
                     f"AND stream IN ({','.join('?' * len(parts))}){one} GROUP BY varno")
                v = dict(conn.execute(q, [stage, region] + parts + arg))
                if v:
                    ch = conn.execute(
                        "SELECT COUNT(DISTINCT channel) FROM counts WHERE stage = ? AND region = ? "
                        f"AND channel IS NOT NULL AND stream IN ({','.join('?' * len(parts))}){one}",
                        [stage, region] + parts + arg).fetchone()[0]
                    per[stage] = (v, ch)
            if not per:
                continue
            if varno is not None:
                # one variable: the stages that hold it; the ones before it
                # appears are left out (a wind component made at evalalt)
                # before it is made, the same quantity travels under another
                # code (ua: the temperature 12101 until derialt makes 12001,
                # the wind direction and speed until evalalt makes u and v):
                # a stage counts the one of them it holds most of
                codes = (varno,) + SOURCE_CODES.get(varno, ())
                present = [st for st in per if any(c in per[st][0] for c in codes)]
                if not present:
                    continue
                left_out = [st for st in stages if st in per and
                            stages.index(st) < stages.index(present[0])]
                via = {}
                new = OrderedDict()
                for st in present:
                    c = max((c for c in codes if c in per[st][0]), key=lambda c: per[st][0][c])
                    if c != varno:
                        via[st] = c
                    new[st] = ({varno: per[st][0][c]}, per[st][1])
                per = new
                common = {varno}
            # only observed quantities: a code of class 33 (quality information)
            # qualifies an observation -- in cutoff it goes with variables that
            # are gone later, and would inflate that stage
            for st in (list(per) if varno is None else []):
                v, ch = per[st]
                v = {x: n for x, n in v.items() if not observed_skip(x)}
                if v:
                    per[st] = (v, ch)
                else:
                    del per[st]
            # a stage at the start sharing no variable with the ones after it
            # (dbase of sc holds none of the winds that reach postalt) is left
            # out, and the figure says so
            if varno is None:
                left_out, via = [], {}
            while varno is None and len(per) > 2 and not set.intersection(*[set(v) for v, _ in per.values()]):
                first = next(iter(per))
                left_out.append(first)
                del per[first]
            if not per:
                continue
            if varno is None:
                common = set.intersection(*[set(v) for v, _ in per.values()])
            # the copies of reports left out of the count, on the same variables
            dup = defaultdict(int)
            if conn.execute("SELECT 1 FROM sqlite_master WHERE name = 'copies'").fetchone():
                for stage, v_, n in conn.execute(
                        "SELECT stage, varno, SUM(n) FROM copies WHERE region = ? "
                        f"AND stream IN ({','.join('?' * len(parts))}){one} GROUP BY stage, varno",
                        [region] + parts + arg):
                    if v_ in common:
                        dup[stage] += n
            # a stage summing a RARS file with others (atms: cutoff counts atms
            # and rars_atms, dbase only the first) says what the RARS file adds
            rars_note, no_rars = {}, []
            if stn is None and conn.execute(
                    "SELECT 1 FROM sqlite_master WHERE name = 'file_counts'").fetchone():
                for st in per:
                    code = via.get(st, varno) if varno is not None else None
                    q = ("SELECT file, SUM(n) FROM file_counts WHERE stage = ? AND region = ? "
                         f"AND stream IN ({','.join('?' * len(parts))})"
                         + (" AND varno = ?" if code is not None else
                            f" AND varno IN ({','.join('?' * len(common))})") + " GROUP BY file")
                    got = dict(conn.execute(q, [st, region] + parts +
                                            ([code] if code is not None else sorted(common))))
                    named = set()
                    for (fl,) in conn.execute(
                            "SELECT files FROM files WHERE stage = ? "
                            f"AND stream IN ({','.join('?' * len(parts))})", [st] + parts):
                        named.update(fl.split())
                    rars = sorted(f for f in named | set(got) if "rars" in f.split("_"))
                    if rars and len(named | set(got)) > 1:
                        rars_note[st] = "of which " + ",  ".join(
                            f"{f} {got[f]:,d}" if got.get(f) else f"{f} empty" for f in rars)
                    elif not rars:
                        no_rars.append(st)
                # the dbase without a RARS file that cutoff has (PSMON does not
                # convert the RARS of ATMS): the dbase is short, not the chain
                if rars_note and no_rars and no_rars[0] == next(iter(per)) \
                        and not any(r.endswith("empty") for r in rars_note.values()
                                    if r == rars_note.get(no_rars[0])):
                    first = no_rars[0]
                    tot = {st: sum(per[st][0].get(x, 0) for x in common) for st in per}
                    # only when it is short of that stage: mwhs2_dbase holds
                    # the RARS too, under a name without the mark
                    if any(stages.index(st) > stages.index(first) and tot[st] > tot[first]
                           for st in rars_note):
                        rars_note[first] = "no RARS file in this stage"
            rows = [dict(stage=st, n=sum(v[x] for x in common), channels=ch, copies=dup[st],
                         via=via.get(st), rars=rars_note.get(st))
                    for st, (v, ch) in per.items()]
            flags = defaultdict(int)
            q = ("SELECT varno, channel, id_stn, flag, SUM(n) FROM flags WHERE region = ? "
                 "AND stream = ?" + (f" AND id_stn IN ({','.join('?' * len(stn_codes))})"
                                     if stn is not None else "") +
                 " GROUP BY varno, channel, id_stn, flag")
            for v_, channel, st, flag, n in conn.execute(
                    q, (region, branch) + tuple(stn_codes)):
                if v_ in common:
                    flags[(channel, st, flag)] += n
            out.append(dict(branch=branch, trunk=trunk and branch == "global",
                            rows=rows, flags=dict(flags),
                            twice=twice_of(conn, region, [branch] + (["trunk"] if trunk and branch == "global" else []),
                                           stn_codes, common),
                            twin=bool(conn.execute(
                                "SELECT 1 FROM notes WHERE note LIKE '% rars: the same observations%'"
                            ).fetchone()) if branch == "global" else False,
                            varnos=sorted(common), left_out=left_out, varno=varno,
                            ends=[st for st in stages
                                  if stages.index(st) > stages.index(list(per)[-1])]))
    return out


# ---- the flags of the last stage, as pikobs.flags reads them ---------------

def describe(pattern) -> str:
    """The bits of a combination, as they read: [9+16], [0 or 7],
    [0 or 2 or 9, not 16]."""
    alts, cur, nots = [], [], []
    for item in pattern:
        if isinstance(item, str) and item.startswith("n") and item != "or":
            nots.append(item[1:])
        elif item == "or":
            alts.append(cur)
            cur = []
        else:
            cur.append(str(item))
    if cur:
        alts.append(cur)
    text = " or ".join("+".join(a) for a in alts if a)
    if nots:
        text += (", " if text else "") + "not " + "+".join(nots)
    return f"[{text}]"


def _groups_of(family_key: str, radiance: bool):
    """The groups of the flags module for this family, those of the
    assimilated apart: the first that matches is the group of an
    observation not assimilated."""
    from pikobs.configobs import flag_groups as fg
    groups = fg.groups_for(family_key) if radiance else fg.DEFAULT_GROUPS
    rejected = [g for g in groups if fg.BIT_ASSIMILATED not in [x for x in g if isinstance(x, int)]]
    if not radiance:
        rejected = list(fg.REASONS_DEFAULT)
    return rejected


def _category(flag: int, groups) -> Tuple[str, str, bool, bool]:
    """(title, bits, assimilated, a group of the flags module) of a flag."""
    from pikobs.configobs import flag_groups as fg
    bits = fg.bits_active(flag)
    if fg.BIT_ASSIMILATED in bits:
        g = fg.first_match(fg.ASSIMILATED_KINDS, bits)
        if g is None:
            return ("ASSIMILATED", "[12]", True, True)
        return (fg.group_title(g), describe(g), True, True)
    if not bits:
        return (fg.NO_BIT_SET.title, "[no bit]", False, True)
    g = fg.first_match(groups, bits)
    if g is not None:
        title = fg.group_title(g)
        return ("BLACKLISTED" if tuple(g) == (8,) else title, describe(g), False, True)
    return ("NOT A GROUP OF THE FLAGS MODULE", "[" + "+".join(map(str, bits)) + "]",
            False, False)


def flag_split(flags: Dict[Tuple, int], radiance: bool,
               family_key: str = "") -> List[Tuple[str, str, bool, bool, int, int]]:
    """(title, bits, assimilated, in the flags module, observations,
    channels): every observation once -- the assimilated ones by kind, the
    others in the first group of the flags module for the family, in its
    order; what no group holds, one row per combination of bits."""
    groups = _groups_of(family_key, radiance)
    n_of, ch_of = defaultdict(int), defaultdict(set)
    for (channel, _stn, flag), n in flags.items():
        key = _category(flag, groups)
        n_of[key] += n
        if channel is not None:
            ch_of[key].add(channel)
    return sorted(((t, b, a, m, n, len(ch_of[(t, b, a, m)])) for (t, b, a, m), n in n_of.items()),
                  key=lambda x: (not x[2], not x[3], -x[4]))


def blacklist(flags: Dict[Tuple, int]) -> List[Tuple[str, int, int, int]]:
    """Per satellite: (satellite, channels wholly on the blacklist -- every
    observation with bit 8 --, channels partly on it, channels at the last
    stage)."""
    total, black = defaultdict(lambda: defaultdict(int)), defaultdict(lambda: defaultdict(int))
    for (channel, stn, flag), n in flags.items():
        if channel is None:
            continue
        total[stn][channel] += n
        if flag & (1 << 8):
            black[stn][channel] += n
    out = []
    for stn in sorted(total):
        whole = sum(1 for c, n in black[stn].items() if n == total[stn][c])
        part = sum(1 for c, n in black[stn].items() if 0 < n < total[stn][c])
        out.append((stn, whole, part, len(total[stn])))
    return out


# ---- the figure ------------------------------------------------------------

def _pct(x: float) -> str:
    if x == 0:
        return "0 %"
    if x >= 10:
        return f"{x:.1f} %"
    if x >= 0.01:
        return f"{x:.2f} %"
    return f"{x:.1e} %"


def chain_figure(family: str, region: str, chain: Dict, radiance: bool, when: str,
                 run: str, out_png: str, stn: Optional[str] = None,
                 stn_label: Optional[str] = None) -> Tuple[str, List[Dict]]:
    """The figure of one family, branch and region, and its rows for the CSV."""
    rows = chain["rows"]
    base = rows[0]["n"] or 1
    base_stage = rows[0]["stage"]
    split = flag_split(chain["flags"], radiance, chain.get("family_key", family)) if chain["flags"] else []
    last = rows[-1]["n"] or 1
    table = []
    prev = None
    for r in rows:
        table.append(dict(kind="stage", label=r["stage"], n=r["n"], channels=r["channels"],
                          copies=r.get("copies", 0), via=r.get("via"), rars=r.get("rars"),
                          of_base=100.0 * r["n"] / base,
                          step=(100.0 * (prev - r["n"]) / prev if prev else None)))
        prev = r["n"]
    # the observations of the channels in use: postalt without its blacklist
    black_n = sum(n for (_c, _s, fl), n in chain["flags"].items() if fl & (1 << 8))
    in_use = (last - black_n) if radiance else last
    for title, bits, assim, in_module, n, nch in split:
        table.append(dict(kind="assimilated" if assim else "not assimilated", label=title,
                          bits=bits, in_module=in_module, n=n, channels=nch or None,
                          of_base=100.0 * n / base, of_last=100.0 * n / last,
                          of_in_use=(100.0 * n / in_use if (assim and radiance and in_use) else None)))
    black = blacklist(chain["flags"]) if radiance else []

    branch = {"global": "", "rars": " (RARS)"}[chain["branch"]]
    n_rows = len(table) + 2
    fig = plt.figure(figsize=(15.5, 1.9 + 0.46 * n_rows))
    h = fig.get_figheight()
    top = 1 - 1.25 / h
    ax = fig.add_axes([0.40, 0.55 / h, 0.37, top - 0.55 / h - 0.05 / h])
    y = list(range(len(table)))[::-1]
    lo = min([t["of_base"] for t in table if t["of_base"] > 0] + [1.0])
    colours, k = [], 0
    for t in table:
        if t["kind"] == "stage":
            colours.append(STAGE_COLOUR)
        elif t["kind"] == "assimilated":
            colours.append(ASSIM_COLOUR)
        else:
            colours.append(REJECT_COLOURS[k % len(REJECT_COLOURS)])
            k += 1
    # a stage with repeated observations: behind its bar, a pale one as long
    # as all its rows -- the 900 % it would show counted row by row
    raw = [100.0 * (t["n"] + t["copies"]) / base if t.get("copies") else None for t in table]
    for yy, r in zip(y, raw):
        if r:
            ax.barh(yy, r, color="none", edgecolor="#B42318", hatch="////", lw=0.6,
                    height=0.62, zorder=1)
    ax.barh(y, [max(t["of_base"], lo / 10) for t in table], color=colours, height=0.62, zorder=2)
    ax.set_xscale("log")
    ax.set_xlim(lo / 10, max([150] + [1.4 * r for r in raw if r]))
    ax.set_ylim(-0.7, len(table) + 0.4)
    ax.set_yticks([])
    ax.set_xlabel(f"share of {base_stage} (log scale)", fontsize=9)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g} %"))
    ax.tick_params(axis="x", labelsize=8)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    n_stages = sum(1 for t in table if t["kind"] == "stage")
    if n_stages < len(table):
        ax.axhline(len(table) - n_stages - 0.5, color="#9AA5B1", lw=0.8, ls="--")
    # the texts of every row: in figure coordinates across, data down
    tf = matplotlib.transforms.blended_transform_factory(fig.transFigure, ax.transData)
    for i, t in enumerate(table):
        yy = y[i]
        stage = t["kind"] == "stage"
        label = t["label"] if stage else "   " + t["label"].lower()
        ax.text(0.03, yy, label, transform=tf, ha="left", va="center", fontsize=9.5,
                fontweight="bold" if stage else "normal",
                color="#1F2933" if stage else colours[i],
                style="normal" if stage or t.get("in_module", True) else "italic")
        sub = []
        if stage and t.get("via"):
            sub.append(f"as {t['via']}")
        if stage and t.get("rars"):
            sub.append(t["rars"])
        if stage and t.get("copies"):
            rows_n = t["n"] + t["copies"]
            sub.append(f"{rows_n:,d} rows ({_pct(100.0 * rows_n / base)}) = "
                       f"{t['n']:,d} obs + {t['copies']:,d} repeated")
        if sub:
            ax.text(0.03, yy - 0.34, "   " + "  ·  ".join(sub),
                    transform=tf, ha="left", va="center", fontsize=7.5, color="#7B8794")
        if not stage:
            twice = (f"  ·  {chain['twice']:,d} of them assimilated twice or more"
                     if t["kind"] == "assimilated" and chain.get("twice") else "")
            ax.text(0.03, yy - 0.34, "      bits " + t["bits"][1:-1] +
                    ("" if t["in_module"] else "  -- not a group of the flags module") + twice,
                    transform=tf, ha="left", va="center", fontsize=7.5, color="#7B8794")
        ax.text(0.30, yy, f"{t['n']:,d}", transform=tf, ha="right", va="center", fontsize=9.5)
        if t["channels"]:
            ax.text(0.37, yy, f"{t['channels']:,d} ch.", transform=tf, ha="right",
                    va="center", fontsize=8.5, color="#52606D")
        # three columns: of dbase; the step, or of postalt; of the channels in use
        ax.text(0.785, yy, _pct(t["of_base"]), transform=tf, ha="left", va="center",
                fontsize=9, color="#1F2933" if stage else "#52606D")
        if stage and t.get("step") is not None:
            mid = ("no loss" if t["step"] == 0 else
                   f"{'-' if t['step'] > 0 else '+'}{_pct(abs(t['step']))} at this step")
        else:
            mid = "" if stage else _pct(t["of_last"])
        ax.text(0.845, yy, mid, transform=tf, ha="left", va="center", fontsize=9,
                color="#1F2933" if stage else "#52606D")
        if t.get("of_in_use") is not None:
            ax.text(0.93, yy, _pct(t["of_in_use"]), transform=tf, ha="left", va="center",
                    fontsize=9, color=ASSIM_COLOUR, fontweight="bold")
    top_y = len(table) - 0.3
    for x, head in ((0.785, f"of {base_stage}"),
                    (0.845, f"step  /  of {rows[-1]['stage']}"),
                    (0.93, "of ch. in use" if radiance else "")):
        ax.text(x, top_y + 0.35, head, transform=tf, ha="left", va="bottom", fontsize=8.5,
                color="#7B8794", fontweight="bold")
    who = f"  ·  {stn_label or stn}" if stn is not None else ""
    goal = "the analysis" if not chain.get("ends") else rows[-1]["stage"]
    fig.text(0.03, 1 - 0.12 / h, f"{family}{branch}{who}  ·  from {base_stage} to {goal}",
             ha="left", va="top", fontsize=15, fontweight="bold", color="#1F2933")
    fig.text(0.97, 1 - 0.14 / h, when, ha="right", va="top", fontsize=10.5, color="#52606D")
    trunk = ("  ·  global and RARS together until evalalt, whose global file holds both"
             if chain["trunk"] else "")
    vias = sorted({r["via"] for r in rows if r.get("via")})
    if chain.get("left_out") and chain.get("varno") is not None:
        gone = (f"  ·  not in {', '.join(chain['left_out'])}: made on the way, "
                f"it first appears at {rows[0]['stage']}")
    elif vias:
        gone = f"  ·  before it is made, counted as {', '.join(map(str, vias))}"
    elif chain.get("left_out"):
        gone = f"  ·  {', '.join(chain['left_out'])} left out: none of these variables there"
    else:
        gone = ""
    if chain.get("twin"):
        gone += "  ·  its RARS files hold the same observations from evalalt on: shown once"
    if chain.get("ends"):
        gone += (f"  ·  the route ends at {rows[-1]['stage']}: "
                 f"nothing in {', '.join(chain['ends'])}")
    what = (f"varno {chain['varno']}" if chain.get("varno") is not None
            else f"variable(s) {', '.join(map(str, chain['varnos']))}")
    fig.text(0.03, 1 - 0.50 / h, f"{region}  ·  {what}{trunk}{gone}",
             ha="left", va="top", fontsize=10, color="#52606D")
    if run:
        fig.text(0.03, 1 - 0.80 / h, f"Exp  {run}", ha="left", va="top", fontsize=12,
                 fontweight="bold", color="#C62828")
    assim = sum(t["n"] for t in table if t["kind"] == "assimilated")
    if assim:
        head = f"assimilated in all: {assim:,d}"
        if radiance and in_use:
            head += f" = {_pct(100.0 * assim / in_use)} of the channels in use"
        head += f",  {_pct(100.0 * assim / last)} of {rows[-1]['stage']},  {_pct(100.0 * assim / base)} of {base_stage}"
        fig.text(0.97, 1 - 0.80 / h, head, ha="right", va="top", fontsize=10.5,
                 fontweight="bold", color=ASSIM_COLOUR)
    if black:
        parts = []
        for sat, whole, part, total in black:
            parts.append(f"{sat} {whole} of {total} ch." + (f" (+{part} in part)" if part else ""))
        fig.text(0.97, 1 - 0.50 / h, "blacklist (bit 8):  " + ",  ".join(parts),
                 ha="right", va="top", fontsize=9.5, color="#52606D")
    fig.lines.append(matplotlib.lines.Line2D([0.03, 0.97], [1 - 1.08 / h] * 2,
                     transform=fig.transFigure, lw=0.8, color="#D9DDE2"))
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    fig.savefig(out_png, dpi=110)
    plt.close(fig)
    csv_rows = [dict(family=family, branch=chain["branch"], region=region,
                     id_stn=stn if stn is not None else "join",
                     varno=chain.get("varno") or "", kind=t["kind"],
                     label=t["label"], observations=t["n"], channels=t["channels"] or "",
                     pct_of_dbase=round(t["of_base"], 6),
                     pct_of_postalt=(round(t["of_last"], 6) if "of_last" in t else ""),
                     pct_lost_at_step=("" if t.get("step") is None else round(t["step"], 6)),
                     bits=t.get("bits", ""),
                     flags_module=("" if t["kind"] == "stage" else
                                   ("yes" if t.get("in_module", True) else "no")),
                     pct_of_channels_in_use=("" if t.get("of_in_use") is None
                                             else round(t["of_in_use"], 6)))
                for t in table]
    csv_rows += [dict(family=family, branch=chain["branch"], region=region,
                      id_stn=stn if stn is not None else "join",
                      varno=chain.get("varno") or "", kind="blacklist",
                      label=f"{sat}: channels wholly blacklisted (of {total}, +{part} in part)",
                      observations="", channels=whole, pct_of_dbase="", pct_of_postalt="",
                      pct_lost_at_step="", bits="[8]", flags_module="yes",
                      pct_of_channels_in_use="")
                 for sat, whole, part, total in black]
    return out_png, csv_rows


_SCHEMES: Dict[Tuple[str, str], Optional[str]] = {}


def scheme_of(family: str, path: str, region: str, pathwork: str) -> Optional[str]:
    """The scheme of the files of a family in a region, drawn once."""
    key = (family, region)
    if key not in _SCHEMES:
        try:
            from pikobs.obschain.obschain_scheme import draw_scheme
            _SCHEMES[key] = draw_scheme(family, path, os.path.join(
                pathwork, "figures", "schemes", f"obschain_{family}_files_{region}.png"), region)
        except Exception as e:
            print(f"[obschain] {family}: no scheme of files ({e})", flush=True)
            _SCHEMES[key] = None
    return _SCHEMES[key]


def stack_below(top_png: str, bottom_png: str) -> None:
    """Put one image under the other, on a white page as wide as the wider."""
    import numpy as np
    import matplotlib.image as mpimg
    a, b = mpimg.imread(top_png), mpimg.imread(bottom_png)
    def rgba(x):
        return x if x.shape[2] == 4 else np.dstack([x, np.ones(x.shape[:2])])
    a, b = rgba(a), rgba(b)
    w = max(a.shape[1], b.shape[1])
    def pad(x):
        out = np.ones((x.shape[0], w, 4), dtype=x.dtype)
        out[:, :x.shape[1]] = x
        return out
    gap = np.ones((20, w, 4), dtype=a.dtype)
    rule = np.ones((2, w, 4), dtype=a.dtype); rule[:, :, :3] = 0.85
    mpimg.imsave(top_png, np.vstack([pad(a), gap, rule, gap, pad(b)]))


def make_figures(db_paths: List[str], regions: List[str], pathwork: str, when: str,
                 run: str, radiance_of, key_of=lambda family, branch: family,
                 id_stn: Sequence[str] = ("join",)) -> List[str]:
    """Every figure, and the CSV of every family. id_stn: join (every
    station together), all (one figure per station reaching the last
    stage), or station names; several at once."""
    written, all_rows, items, labels = [], [], [], {}
    for path in db_paths:
        family = os.path.basename(path)[len("obschain_"):-3]
        names = codtyp_names(path)
        for ct, lab in names.items():
            labels[ct] = lab if labels.get(ct) in (None, lab) else f"{labels[ct]} / {lab}"
        wanted = wanted_varnos(family)
        at_end = postalt_varnos(path)
        for region in regions:
            reaching = stations_of(path, region)
            picks = []
            for tok in id_stn:
                if tok == "join":
                    picks.append(None)
                elif tok == "all":
                    picks += reaching
                else:
                    picks.append(tok)
            # the variables of the family (its list in pikobs) that reach
            # postalt; without a list, every observed one that reaches it
            end_all = sorted(set().union(*at_end.values())) if at_end else []
            varnos = [v for v in wanted if v in end_all] or \
                     [v for v in end_all if not observed_skip(v)]
            for stn in list(dict.fromkeys(picks)):
                tag = "join" if stn is None else re.sub(r"[^A-Za-z0-9._-]+", "_", stn)
                for varno in varnos:
                    for chain in chain_rows(path, region, stn, varno):
                        # a RARS route that ends before postalt follows the
                        # variables the global branch brings there
                        if varno not in (at_end.get(chain["branch"]) or at_end.get("global", [])):
                            continue
                        chain["family_key"] = key_of(family, chain["branch"])
                        png = os.path.join(pathwork, "figures",
                                           f"obschain_{family}_{chain['branch']}_{tag}_"
                                           f"{region}_{varno}.png")
                        out, rows = chain_figure(family, region, chain, radiance_of(family),
                                                 when, run, png, stn, names.get(stn))
                        below = scheme_of(family, path, region, pathwork)
                        if below:
                            stack_below(out, below)
                        written.append(out)
                        all_rows += rows
                        items.append(dict(family=family if chain["branch"] != "rars" else rars_name(path, family),
                                          branch=chain["branch"], region=region,
                                          id_stn="join" if stn is None else stn,
                                          varno=str(varno),
                                          filename=os.path.relpath(out, pathwork)))

    if all_rows:
        with open(os.path.join(pathwork, "obschain_summary.csv"), "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(all_rows[0]))
            w.writeheader()
            w.writerows(all_rows)
    if items:
        write_viewer(items, pathwork, when, run, labels)
    return written


VIEWER = "pikobs_obschain_viewer.html"


def write_viewer(items: List[Dict], pathwork: str, when: str, run: str,
                 labels: Optional[Dict[str, str]] = None) -> str:
    """The viewer of the run: one page, choosing the family, the branch,
    the region and the station, with the viewer every module uses."""
    from pikobs.web.viewer import generate_web
    out = os.path.join(pathwork, VIEWER)
    generate_web(items, ["family", "region", "id_stn", "varno"], out,
                 title="obschain -- from dbase to the analysis",
                 subtitle=f"{run + '  ·  ' if run else ''}{when}",
                 key_labels={"branch": "Branch", "id_stn": "Station or type", "varno": "Variable"},
                 value_labels={"branch": {"global": "global", "rars": "RARS"},
                               "id_stn": {"join": "all together", **(labels or {})}})
    return out


def web_address(path: str) -> Optional[str]:
    """The address of a file under /home/<user>/sites8, else None."""
    home = os.path.expanduser("~")
    user = os.path.basename(home)
    real = os.path.realpath(path)
    for base in (os.path.join(home, "sites8"), os.path.realpath(os.path.join(home, "sites8"))):
        if real.startswith(base + os.sep):
            return (f"https://goc-dx-u3.science.gc.ca/~{user}/sites8/"
                    f"{os.path.relpath(real, base)}")
    return None
