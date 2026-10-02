"""pikobs.obschain: how many observations every stage of the chain keeps.

An observation goes through dbase, cutoff, derialt, evalalt, bgckalt and
postalt before it reaches the analysis, and at every stage some of them
stay behind. obschain follows a family along that chain and counts what is
left at each stage, variable by variable, per region and per station; at
postalt it also splits what is left by what quality control made of it,
with the groups of pikobs.flags.

Give it the directories of the stages you have, in any order: each one is
recognised by its name and they are put in the order of the chain. The
files of a family at every stage come from configobs/cutoff_to_postalt.csv;
at dbase from the names of the files (<name>_dbase, the name starting with
the family, ozone going to ch).

Four rules keep the numbers honest:

  - only the files that lead to postalt are counted: two versions of the
    same observations (atms and atms_allsky) are never summed;
  - a family whose postalt keeps RARS apart is followed as two branches:
    RARS, a chain of its own with its own files at every stage, and global,
    which counts global and RARS together before evalalt -- its evalalt
    file already holds both (to_amsua: 2,108,415 global + 3,126,675 RARS at
    derialt = 5,235,090 global at evalalt);
  - only the variables that reach the last stage are shown (dbase also
    holds the metadata of the reports, which never arrive), and a count
    below a later one is partial: the variable is derived later;
  - a file that is the copy of another one is counted once.

A radiance is counted channel by channel: every stage keeps fewer of the
channels of the instrument (dbase holds all of them), and the summary says
how many are left at each stage.

This first part extracts and stores the counts; the figures read them.
"""
import csv
import hashlib
import os
import re
import sqlite3
import sys
import time
import traceback
from collections import OrderedDict, defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Sequence, Tuple

STAGES = ["dbase", "cutoff", "derialt", "evalalt", "bgckalt", "postalt"]
CYCLE_HOURS = 6

_SHOWN_TRACEBACK = []


# ---- the chain -----------------------------------------------------------

def chain_table() -> Dict[str, Dict[str, List[str]]]:
    """{family: {stage: [file names]}} from configobs/cutoff_to_postalt.csv."""
    import pikobs.configobs as co
    path = os.path.join(os.path.dirname(co.__file__), "cutoff_to_postalt.csv")
    table = {}
    with open(path, newline="") as fh:
        for row in csv.DictReader(fh):
            row = {k.strip(): (v or "").strip() for k, v in row.items()}
            table[row["family"]] = {st: row.get(st, "").split() for st in STAGES[1:]}
    return table


def stage_of(path: str) -> Optional[str]:
    """The stage of a directory, from its name."""
    name = os.path.basename(os.path.normpath(path)).lower()
    return next((st for st in STAGES if st in name), None)


def dbase_family(name: str, families) -> Optional[str]:
    """The family a dbase file belongs to: ozone to ch, else the longest
    family its name starts with."""
    if name.startswith("o3_"):
        return "ch"
    hits = [f for f in families if name == f or name.startswith(f + "_")]
    if not hits:
        # a RARS dbase converted by hand, named as in cutoff: rars_atms_dbase
        # belongs to atms, rars_amsua_dbase to to_amsua
        bare = "_".join(t for t in name.split("_") if t != "rars")
        if bare != name:
            hits = [f for f in families
                    for b in (bare, "to_" + bare) if b == f or b.startswith(f + "_")]
    return max(hits, key=len) if hits else None


def is_rars(name: str) -> bool:
    """A file of the RARS stream: rars in its name."""
    return "rars" in str(name).lower().split("_")


def splits_rars(family: str, table) -> bool:
    """Does postalt keep the RARS stream of this family apart?"""
    return any(is_rars(n) for n in table.get(family, {}).get("postalt", []))


# the radiance families of the chain, when pikobs cannot tell from the family
RADIANCES = ("atms", "cris", "csr", "iasi", "mwhs2", "ssmis", "to_amsua", "to_amsub")


def is_radiance(family: str, table) -> bool:
    """A family on channels (its vertical coordinate is CANAL), as flags
    reads it; the names of its postalt files are asked first."""
    try:
        import pikobs
        for name in table.get(family, {}).get("postalt", []) + [family]:
            try:
                return str(pikobs.family(name)[5]).strip().upper().startswith("CANAL")
            except Exception:
                continue
    except Exception:
        pass
    return family in RADIANCES


def lineage(names: Sequence[str], postalt: Sequence[str]) -> List[str]:
    """The files of a stage that lead to postalt: when some of the names are
    the ones of postalt (with _qc at evalalt), only those count."""
    def norm(n):
        # the RARS mark sits anywhere in a name (rars_mwhs2, mwhs2_rars): the
        # trunk, global and RARS together, keeps both streams of a version
        return "_".join(t for t in re.sub(r"_qc$", "", n).split("_") if t != "rars")
    ends = {norm(n) for n in postalt}
    keep = [n for n in names if norm(n) in ends]
    return keep or list(names)


def files_of(stage: str, path: str, family: str, cycle: str, table,
             stream: str) -> Dict[str, List[str]]:
    """The files of a family, a stream and a stage at one cycle: found, the
    ones the table expects and are missing, the other versions not counted,
    and the files of the family the table does not name."""
    try:
        on_disk = sorted(f[len(cycle) + 1:] for f in os.listdir(path)
                         if f.startswith(cycle + "_"))
    except OSError:
        on_disk = []
    split = splits_rars(family, table) and stream != "trunk"
    if stream == "rars":            # the RARS route: its own files only
        mine = is_rars
    elif split:                     # the global branch of a split family
        mine = lambda n: not is_rars(n)
    else:                           # the trunk, or a family not split
        mine = lambda n: True
    if stage == "dbase":
        names = [n[:-len("_dbase")] for n in on_disk if n.endswith("_dbase")]
        found = [f"{n}_dbase" for n in names
                 if dbase_family(n, table) == family and mine(n)]
        return dict(found=found, missing=[], versions=[], others=[])
    named = [n for n in table.get(family, {}).get(stage, []) if mine(n)]
    postalt = [n for n in table.get(family, {}).get("postalt", []) if mine(n)]
    expected = lineage(named, postalt)
    on_disk = [n for n in on_disk if mine(n)]
    return dict(
        found=[n for n in expected if n in on_disk],
        missing=[n for n in expected if n not in on_disk],
        versions=[n for n in named if n not in expected and n in on_disk],
        others=[n for n in on_disk if (n == family or n.startswith(family + "_"))
                and n not in named])


def _fingerprint(path: str) -> Tuple:
    """Size and the hash of the first and last megabyte: two files with the
    same fingerprint are the same file for counting."""
    size = os.path.getsize(path)
    h = hashlib.md5()
    with open(path, "rb") as fh:
        h.update(fh.read(1 << 20))
        if size > 2 << 20:
            fh.seek(-(1 << 20), os.SEEK_END)
            h.update(fh.read(1 << 20))
    return size, h.hexdigest()


def has_rars(family: str, table) -> bool:
    """Does the chain of this family carry RARS files at some stage?"""
    return any(is_rars(n) for names in table.get(family, {}).values() for n in names)


def streams_of(family: str, table) -> List[str]:
    """The branches of a family: global, and RARS when postalt keeps it
    apart (mwhs2, to_amsua, to_amsub), followed from the first stage that
    has its files. A RARS that does not reach postalt (atms) has no branch:
    the global one sums its files while it lasts, and says so."""
    return ["global", "rars"] if splits_rars(family, table) else ["global"]


# the stages before the branches part: there the global and RARS files of a
# family are counted together, as one trunk -- somewhere between dbase and
# evalalt the two streams exchange observations, so a branch has no stage
# of its own before evalalt
TRUNK_STAGES = ("dbase", "cutoff", "derialt")


# families whose stations are aircraft, ships or ground stations by the
# thousand: they are grouped by type of report (codtyp) instead, and the
# type is kept where the station would be. Its name comes from the cutoff
# files, which are split by type (ai_acars, sf_synop, ua_radiosonde ...).
BY_CODTYP = ("ai", "sf", "ua", "gp")


# the header columns that make a report: a second row with all of them equal
# is a copy of the report, not a new one
REPORT_KEY = ("id_stn", "codtyp", "lat", "lon", "date", "time")


def dedups(family: str, name: str, table=None) -> bool:
    """Files counted report by report, each once: those of the families
    grouped by type (cutoff repeats ACARS reports twice or more) and of the
    families with a RARS stream, every file of them -- the RARS files repeat
    their reports, and so does a dbase that holds them (mwhs2_dbase: 665 420
    reports, 363 091 distinct); counting one file of the family once and
    another as it is would make a loss that is not one. Elsewhere dbase and
    cutoff hold the same rows and the check would only cost time."""
    if family in BY_CODTYP or is_rars(name):
        return True
    return bool(table) and any(is_rars(n) for names in table.get(family, {}).values()
                               for n in names)


def codtyp_label(family: str, name: str) -> str:
    """The name of a type from the cutoff file holding it: sf_synop_b -> SYNOP."""
    n = re.sub(r"_b$", "", name)
    n = n[len(family) + 1:] if n.startswith(family + "_") else n
    return n.upper()


# ---- counting ------------------------------------------------------------

def _count_obs(conn, task, regions, conds):
    """The families grouped by type, counted observation by observation
    across every file of the stage: the same observation (station, place,
    time, variable, level) in two rows -- of one file or of two (ua_radiosonde
    and ua_radiosonde_b, sf_synop and sf_synop_b) -- is one. What is left
    out is kept as copies, and at the last stage the observations
    assimilated more than once."""
    try:
        from pikobs.configobs import flag_groups as fg
        bit = 1 << int(fg.BIT_ASSIMILATED)
    except Exception:
        bit = 1 << 12
    rc = ", ".join(f"r{i} INTEGER" for i in range(len(regions)))
    conn.execute("DROP TABLE IF EXISTS temp.o")
    conn.execute(f"CREATE TEMP TABLE o (k TEXT, stn TEXT, varno INTEGER, flag INTEGER, "
                 f"file TEXT, {rc})")
    sources = defaultdict(set)
    for name in task["files"]:
        path = os.path.join(task["dir"], f"{task['cycle']}_{name}")
        conn.execute("ATTACH DATABASE ? AS db", (f"file:{path}?mode=ro",))
        try:
            cols = {r[1].lower() for r in conn.execute("PRAGMA db.table_info(header)")}
            parts = [f"COALESCE(h.{c}, '')" if c in ("id_stn", "date", "time") else
                     f"COALESCE(ROUND(h.{c}, 2), '')"
                     for c in ("id_stn", "lat", "lon", "date", "time") if c in cols]
            key = " || '/' || ".join(parts + ["d.varno", "COALESCE(d.vcoord, '')"])
            regs = ", ".join(f"CASE WHEN {c} THEN 1 ELSE 0 END" for c in conds)
            conn.execute(f"INSERT INTO o SELECT {key}, TRIM(CAST(h.codtyp AS TEXT)), d.varno, "
                         f"COALESCE(d.flag, 0), ?, {regs} "
                         f"FROM db.header h JOIN db.data d ON h.id_obs = d.id_obs "
                         f"WHERE d.obsvalue IS NOT NULL", (name,))
            if task["stage"] == "cutoff":
                for (ct,) in conn.execute("SELECT DISTINCT codtyp FROM db.header"):
                    if ct is not None:
                        sources[str(ct).strip()].add(codtyp_label(task["family"], name))
        finally:
            conn.commit()               # a DETACH inside the open insert fails
            conn.execute("DETACH DATABASE db")
    by_file = defaultdict(int)
    sel = ", ".join(f"SUM(r{i})" for i in range(len(regions)))
    for row in conn.execute(f"SELECT file, varno, {sel} FROM o GROUP BY file, varno"):
        for i, region in enumerate(regions):
            if row[2 + i]:
                by_file[(region, int(row[1]), row[0])] += row[2 + i]
    # one row per observation: the smallest type it has (35 before 235), in the regions any
    # of its rows is in; its flag the one of a row that was assimilated, if any
    mx = ", ".join(f"MAX(r{i}) AS r{i}" for i in range(len(regions)))
    conn.execute("DROP TABLE IF EXISTS temp.u")
    conn.execute(f"CREATE TEMP TABLE u AS SELECT CAST(MIN(CAST(stn AS INTEGER)) AS TEXT) AS stn, varno, COUNT(*) AS n, "
                 f"SUM(CASE WHEN flag & {bit} THEN 1 ELSE 0 END) AS na, "
                 f"COALESCE(MAX(CASE WHEN flag & {bit} THEN flag END), MIN(flag)) AS flag, {mx} "
                 f"FROM o GROUP BY k")
    counts, copies, twice, flags = (defaultdict(int) for _ in range(4))
    q = ", ".join(f"SUM(r{i}), SUM(r{i} * (n - 1)), SUM(CASE WHEN na > 1 THEN r{i} ELSE 0 END)"
                  for i in range(len(regions)))
    for row in conn.execute(f"SELECT stn, varno, {q} FROM u GROUP BY stn, varno"):
        for i, region in enumerate(regions):
            k = (region, int(row[1]), str(row[0]), None)
            n, c, t = row[2 + 3 * i: 5 + 3 * i]
            if n:
                counts[k] += n
            if c:
                copies[k] += c
            if t and task["flags"]:
                twice[k] += t
    if task["flags"]:
        for row in conn.execute(f"SELECT varno, stn, flag, {sel} FROM u GROUP BY varno, stn, flag"):
            for i, region in enumerate(regions):
                if row[3 + i]:
                    flags[(region, int(row[0]), None, str(row[1]), int(row[2] or 0))] += row[3 + i]
    conn.execute("DROP TABLE IF EXISTS temp.o")
    conn.execute("DROP TABLE IF EXISTS temp.u")
    return counts, flags, copies, by_file, sources, twice


def _count_task(task: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Count one family, stream and stage at one cycle: per region, variable
    and station, and at the last stage per region, variable and flag."""
    try:
        from pikobs.configobs import regionsobs
        regions, pathwork = task["regions"], task["pathwork"]
        conn = sqlite3.connect(":memory:")
        regionsobs.register(conn, regions, pathwork)
        conds = [f"(1=1 {regionsobs.criteria(r, pathwork)})" for r in regions]
        sums = ", ".join(f"SUM(CASE WHEN {c} THEN 1 ELSE 0 END)" for c in conds)
        counts, flags, copies = defaultdict(int), defaultdict(int), defaultdict(int)
        sources = defaultdict(set)
        by_file = defaultdict(int)
        twice = {}
        if task.get("by_obs"):
            counts, flags, copies, by_file, sources, twice = _count_obs(conn, task, regions, conds)
        for name in ([] if task.get("by_obs") else task["files"]):
            path = os.path.join(task["dir"], f"{task['cycle']}_{name}")
            conn.execute("ATTACH DATABASE ? AS db", (f"file:{path}?mode=ro",))
            try:
                src = ("FROM db.header h JOIN db.data d ON h.id_obs = d.id_obs "
                       "WHERE d.obsvalue IS NOT NULL")
                if task.get("rows"):            # one slice of a big file
                    src += f" AND d.rowid BETWEEN {task['rows'][0]} AND {task['rows'][1]}"
                raw_src = src
                if task.get("dedup") or dedups(task["family"], name):
                    cols = {r[1].lower() for r in conn.execute("PRAGMA db.table_info(header)")}
                    key = ", ".join(k for k in REPORT_KEY if k in cols)
                    conn.execute("DROP TABLE IF EXISTS temp.keep")
                    conn.execute(f"CREATE TEMP TABLE keep AS SELECT MIN(id_obs) AS id "
                                 f"FROM db.header GROUP BY {key}")
                    conn.execute("CREATE INDEX temp.idx_keep ON keep (id)")
                    src += " AND h.id_obs IN (SELECT id FROM temp.keep)"
                # a radiance is counted channel by channel, anything else
                # per variable only (its levels would be too many)
                chan = "CAST(d.vcoord AS INTEGER)" if task["by_channel"] else "NULL"
                stn = "h.codtyp" if task.get("by_codtyp") else "h.id_stn"
                if task.get("by_codtyp") and task["stage"] == "cutoff" and (task.get("rows") or (1,))[0] == 1:
                    for (ct,) in conn.execute("SELECT DISTINCT codtyp FROM db.header"):
                        if ct is not None:
                            sources[str(ct).strip()].add(codtyp_label(task["family"], name))
                def per_key(where):
                    out = defaultdict(int)
                    for row in conn.execute(
                            f"SELECT {stn}, d.varno, {chan}, {sums} {where} "
                            f"GROUP BY {stn}, d.varno, 3"):
                        for i, region in enumerate(regions):
                            if row[3 + i]:
                                out[(region, int(row[1]), str(row[0]).strip(), row[2])] += row[3 + i]
                    return out
                here = per_key(src)
                for k, n in here.items():
                    counts[k] += n
                    by_file[(k[0], k[1], name)] += n
                if raw_src != src:
                    # the copies left out: every row of the file, less the ones counted
                    for k, n in per_key(raw_src).items():
                        if n > here.get(k, 0):
                            copies[k] += n - here.get(k, 0)
                if task["flags"]:
                    # per satellite too: the blacklist is kept per satellite and channel
                    for row in conn.execute(
                            f"SELECT d.varno, {chan}, {stn}, d.flag, {sums} {src} "
                            f"GROUP BY d.varno, 2, {stn}, d.flag"):
                        for i, region in enumerate(regions):
                            if row[4 + i]:
                                flags[(region, int(row[0]), row[1], str(row[2]).strip(),
                                       int(row[3] or 0))] += row[4 + i]
            finally:
                conn.execute("DROP TABLE IF EXISTS temp.keep")
                conn.execute("DETACH DATABASE db")
        conn.close()
        if task["stream"] == "version":
            # another version of the files: counted for the scheme of the
            # files only, never in the chain
            counts, flags, copies, twice = {}, {}, {}, {}
        return dict(task, counts=dict(counts), flag_counts=dict(flags), copies=dict(copies),
                    twice=dict(twice),
                    by_file=dict(by_file),
                    sources={k: sorted(v) for k, v in sources.items()})
    except Exception as exc:
        if not _SHOWN_TRACEBACK:
            _SHOWN_TRACEBACK.append(True)
            print(f"[obschain] counting failed for {task.get('family')} "
                  f"{task.get('stage')} {task.get('cycle')}:\n{traceback.format_exc()}",
                  file=sys.stderr, flush=True)
        else:
            print(f"[obschain] counting failed for {task.get('family')} "
                  f"{task.get('stage')} {task.get('cycle')}: {exc}",
                  file=sys.stderr, flush=True)
        return None


# a file bigger than this is counted in slices of its data table, by
# several workers at once: one worker reading 24 GB of CrIS alone would
# keep the others waiting
SLICE_BYTES = 500 * 2 ** 20


def _slices(path: str) -> List[Optional[Tuple[int, int]]]:
    """The row ranges of the data table to count apart: [None] (the whole
    file at once) for a small file."""
    size = os.path.getsize(path)
    if size <= SLICE_BYTES:
        return [None]
    with sqlite3.connect(f"file:{path}?mode=ro", uri=True) as c:
        last = c.execute("SELECT MAX(rowid) FROM data").fetchone()[0] or 0
    n = -(-size // SLICE_BYTES)
    step = -(-last // n) if last else 1
    return [(lo, min(lo + step - 1, last)) for lo in range(1, last + 1, step)] or [None]


def merge(results: List[Optional[Dict]]) -> List[Dict]:
    """The slices of a file, and the files of a stage, summed back into one
    row per (family, stream, stage, cycle)."""
    out = OrderedDict()
    for r in results:
        if not r:
            continue
        key = (r["family"], r["stream"], r["stage"], r["cycle"])
        if key not in out:
            out[key] = dict(r, counts=defaultdict(int), flag_counts=defaultdict(int),
                            files=[], sources=defaultdict(set), copies=defaultdict(int),
                            by_file=defaultdict(int), twice=defaultdict(int))
        m = out[key]
        for k, n in r["counts"].items():
            m["counts"][k] += n
        for k, n in r["flag_counts"].items():
            m["flag_counts"][k] += n
        m["files"] += [f for f in r["files"] if f not in m["files"]]
        for k, v in r.get("sources", {}).items():
            m["sources"][k].update(v)
        for k, n in r.get("copies", {}).items():
            m["copies"][k] += n
        for k, n in r.get("by_file", {}).items():
            m["by_file"][k] += n
        for k, n in r.get("twice", {}).items():
            m["twice"][k] += n
    return list(out.values())


def _cycles(date_start: str, date_end: str) -> List[str]:
    t, end = datetime.strptime(date_start, "%Y%m%d%H"), datetime.strptime(date_end, "%Y%m%d%H")
    out = []
    while t <= end:
        out.append(t.strftime("%Y%m%d%H"))
        t += timedelta(hours=CYCLE_HOURS)
    return out


def _cycle_ranges(cycles: Sequence[str]) -> str:
    """2026092900..2026092912 for consecutive 6-h cycles, else a list."""
    out, run = [], []
    for c in sorted(cycles):
        t = datetime.strptime(c, "%Y%m%d%H")
        if run and t - datetime.strptime(run[-1], "%Y%m%d%H") == timedelta(hours=CYCLE_HOURS):
            run.append(c)
        else:
            if run:
                out.append(run)
            run = [c]
    if run:
        out.append(run)
    return ", ".join(r[0] if len(r) == 1 else f"{r[0]}..{r[-1]}" for r in out)


def plan(stage_paths: Sequence[str], families: Sequence[str], regions: Sequence[str],
         cycles: Sequence[str], pathwork: str) -> Tuple[List[Dict], List[str]]:
    """One task per piece to count (a file, or a slice of a big one), and
    the notes of what the chain holds.

    A cycle counts only when every stage has it for the family, and for
    both of its branches: a cycle that dbase has and postalt does not yet
    would look like a loss that is not one. The cycles left out are noted,
    with the stages that lacked them."""
    table = chain_table()
    stages = sorted(((stage_of(p), os.path.expanduser(p)) for p in stage_paths),
                    key=lambda x: STAGES.index(x[0]) if x[0] else 99)
    unknown = [d for st, d in stages if st is None]
    if unknown:
        raise ValueError(f"not a stage of the chain ({', '.join(STAGES)}): {unknown}")
    absent = [d for _, d in stages if not os.path.isdir(d)]
    if absent:
        raise ValueError(f"no such directory: {', '.join(absent)}")
    last = stages[-1][0]
    what = {"copies": "a copy of another file, counted once",
            "missing": "missing (the table expects them)",
            "versions": "not counted (another version, not the one that reaches postalt)",
            "others": "not named in the table"}
    tasks, notes = [], []
    for family in families:
        if family not in table:
            notes.append(f"{family}: not in cutoff_to_postalt.csv, skipped")
            continue
        branches = streams_of(family, table)
        split = splits_rars(family, table)
        # the global branch takes the trunk (global and RARS together) before
        # evalalt, where its file already holds both; the RARS branch is a
        # chain of its own, its own files at every stage
        runs = ([("trunk", [(st, d) for st, d in stages if st in TRUNK_STAGES])] if split else [])
        runs += [(b, [(st, d) for st, d in stages
                      if not (split and b == "global" and st in TRUNK_STAGES)])
                 for b in branches]
        # what every stage holds at every cycle
        found = {(stream, stage, cycle): files_of(stage, d, family, cycle, table, stream)
                 for stream, st_list in runs for stage, d in st_list for cycle in cycles}
        # a RARS branch may have no files of its own before the branches
        # part (mwhs2: dbase keeps one file, global and RARS together, which
        # the trunk counts): there it is not required, and its chain starts
        # at the first stage that has its files
        def required(stream, stage):
            # a RARS route is never required: it starts and ends where its
            # files are (none of its own in the dbase of mwhs2, none after
            # derialt for atms)
            return stream != "rars"
        keep = [c for c in cycles
                if all(found[(stream, stage, c)]["found"]
                       for stream, st_list in runs for stage, _ in st_list
                       if required(stream, stage))]
        lacking = defaultdict(set)
        for c in cycles:
            if c not in keep:
                for stream, st_list in runs:
                    for stage, _ in st_list:
                        if required(stream, stage) and not found[(stream, stage, c)]["found"]:
                            lacking[c].add(f"{stage}{' (RARS)' if stream == 'rars' else ''}")
        if lacking:
            by_stages = defaultdict(list)
            for c, sts in lacking.items():
                by_stages[tuple(sorted(sts, key=lambda x: STAGES.index(x.split()[0])))].append(c)
            for sts, cs in by_stages.items():
                notes.append(f"{family}: cycle(s) {_cycle_ranges(cs)} left out of every "
                             f"stage, {', '.join(sts)} lack(s) them")
        if not keep:
            notes.append(f"{family}: no cycle that every stage has, nothing counted")
            continue
        for stream, st_list in runs:
            seen_notes = defaultdict(set)
            for stage, d in st_list:
                for cycle in keep:
                    f = found[(stream, stage, cycle)]
                    for kind in ("missing", "versions", "others"):
                        if f[kind]:
                            seen_notes[(stage, kind, " ".join(f[kind]))].add(cycle)
                    base = dict(family=family, stream=stream, stage=stage, dir=d,
                                cycle=cycle, regions=list(regions), pathwork=pathwork,
                                flags=(stage == last),
                                by_channel=is_radiance(family, table),
                                by_codtyp=family in BY_CODTYP,
                                dedup=dedups(family, "", table))
                    seen = set()
                    # the other versions (ua_a, sf2, the clear-sky atms): what
                    # they hold goes to the scheme of the files, not the chain
                    if stream in ("global", "trunk"):
                        for name in f["versions"]:
                            path = os.path.join(d, f"{cycle}_{name}")
                            if os.path.exists(path):
                                tasks += [dict(base, stream="version", flags=False,
                                               files=[name], rows=rows)
                                          for rows in _slices(path)]
                    whole = []
                    for name in f["found"]:
                        path = os.path.join(d, f"{cycle}_{name}")
                        fp = _fingerprint(path)
                        if fp in seen:          # a copy of a file already counted
                            seen_notes[(stage, "copies", name)].add(cycle)
                            continue
                        seen.add(fp)
                        if family in BY_CODTYP:
                            whole.append(name)
                        else:
                            tasks += [dict(base, files=[name], rows=rows)
                                      for rows in _slices(path)]
                    if whole:
                        # all its files at once: an observation in two of them is one
                        tasks.append(dict(base, files=whole, rows=None, by_obs=True))
            for (stage, kind, names), cs in sorted(seen_notes.items()):
                when = "" if len(cs) == len(keep) else f" (cycle(s) {_cycle_ranges(cs)})"
                notes.append(f"{family} {stream} {stage}: {names} -- {what[kind]}{when}")
    return tasks, notes


def _run(tasks: List[Dict], n_cpus: int) -> List[Optional[Dict]]:
    """The counting of every task: in Dask workers, or here with one CPU."""
    if n_cpus <= 1:
        return [_count_task(t) for t in tasks]
    import dask
    from dask.distributed import Client
    from pikobs.parallel import run_tasks
    dask.config.set({"distributed.worker.daemon": False})
    client = Client(processes=True, threads_per_worker=1, n_workers=n_cpus,
                    silence_logs=50, dashboard_address=None)
    try:
        return run_tasks(_count_task, [(t,) for t in tasks], client, label="counting")
    finally:
        client.close(timeout=30)


_DDL = """
CREATE TABLE IF NOT EXISTS counts (
    date TEXT, stream TEXT, stage TEXT, region TEXT,
    varno INTEGER, id_stn TEXT, channel INTEGER, n INTEGER);
CREATE TABLE IF NOT EXISTS flags (
    date TEXT, stream TEXT, region TEXT, varno INTEGER,
    channel INTEGER, id_stn TEXT, flag INTEGER, n INTEGER);
CREATE TABLE IF NOT EXISTS files (
    date TEXT, stream TEXT, stage TEXT, files TEXT);
CREATE TABLE IF NOT EXISTS notes (note TEXT);
CREATE TABLE IF NOT EXISTS stages (stage TEXT, position INTEGER, dir TEXT);
CREATE TABLE IF NOT EXISTS codtyp_names (codtyp TEXT, name TEXT);
CREATE TABLE IF NOT EXISTS twice (
    date TEXT, stream TEXT, region TEXT, varno INTEGER, id_stn TEXT, channel INTEGER, n INTEGER);
CREATE TABLE IF NOT EXISTS file_counts (
    date TEXT, stream TEXT, stage TEXT, region TEXT, varno INTEGER, file TEXT, n INTEGER);
CREATE TABLE IF NOT EXISTS copies (
    date TEXT, stream TEXT, stage TEXT, region TEXT,
    varno INTEGER, id_stn TEXT, channel INTEGER, n INTEGER);
"""


def db_path(pathwork: str, family: str) -> str:
    return os.path.join(pathwork, f"obschain_{family}.db")


def drop_twins(rows: List[Dict], notes: List[str]) -> List[Dict]:
    """A RARS branch whose counts are those of the global branch, at every
    cycle, stage, region, variable and station, holds the same observations
    under another name: it is dropped, with a note."""
    def key(stream):
        out = {}
        for r in rows:
            if r["stream"] == stream:
                for k, n in r["counts"].items():
                    out[(r["cycle"], r["stage"]) + k] = n
        return out
    rars = key("rars")
    if not rars:
        return rows
    glob = key("global")
    # the stages both branches count on their own (not the trunk ones)
    rars = {k: n for k, n in rars.items() if k[1] not in TRUNK_STAGES}
    if rars and all(glob.get(k) == n for k, n in rars.items()):
        family = rows[0]["family"]
        # the same observations under two names (mwhs2: all of it comes as
        # rars_mwhs2 and evalalt writes it twice, as mwhs2_qc and
        # mwhs2_rars_qc): one figure, which says so
        notes.append(f"{family} rars: the same observations as the global branch "
                     f"from evalalt on -- shown once")
        print(f"[obschain] {family}: the RARS branch holds the same observations "
              f"as the global one -- shown once", flush=True)
        return [r for r in rows if r["stream"] != "rars"]
    return rows


def store(results: List[Optional[Dict]], pathwork: str, notes: List[str],
          stage_paths: Sequence[str]) -> List[str]:
    """Write the counts into one database per family."""
    os.makedirs(pathwork, exist_ok=True)
    by_family = defaultdict(list)
    for r in results:
        if r:
            by_family[r["family"]].append(r)
    # the scheme of the files keeps every file, the twin RARS ones included
    every = {family: list(rows) for family, rows in by_family.items()}
    for family in list(by_family):
        by_family[family] = drop_twins(by_family[family], notes)
    written = []
    for family, rows in by_family.items():
        path = db_path(pathwork, family)
        if os.path.exists(path):
            os.remove(path)
        with sqlite3.connect(path) as conn:
            conn.executescript(_DDL)
            conn.executemany("INSERT INTO counts VALUES (?,?,?,?,?,?,?,?)",
                             [(r["cycle"], r["stream"], r["stage"], reg, v, stn, ch, n)
                              for r in rows for (reg, v, stn, ch), n in r["counts"].items()])
            conn.executemany("INSERT INTO twice VALUES (?,?,?,?,?,?,?)",
                             [(r["cycle"], r["stream"], reg, v, stn, ch, n)
                              for r in rows for (reg, v, stn, ch), n in r.get("twice", {}).items()])
            conn.executemany("INSERT INTO file_counts VALUES (?,?,?,?,?,?,?)",
                             [(r["cycle"], r["stream"], r["stage"], reg, v, f, n)
                              for r in every[family]
                              for (reg, v, f), n in r.get("by_file", {}).items()])
            conn.executemany("INSERT INTO copies VALUES (?,?,?,?,?,?,?,?)",
                             [(r["cycle"], r["stream"], r["stage"], reg, v, stn, ch, n)
                              for r in rows for (reg, v, stn, ch), n in r.get("copies", {}).items()])
            conn.executemany("INSERT INTO flags VALUES (?,?,?,?,?,?,?,?)",
                             [(r["cycle"], r["stream"], reg, v, ch, stn, fl, n)
                              for r in rows for (reg, v, ch, stn, fl), n in r["flag_counts"].items()])
            conn.executemany("INSERT INTO files VALUES (?,?,?,?)",
                             [(r["cycle"], r["stream"], r["stage"], " ".join(r["files"]))
                              for r in every[family]])
            names = defaultdict(set)
            for r in rows:
                for ct, v in r.get("sources", {}).items():
                    names[ct].update(v)
            conn.executemany("INSERT INTO codtyp_names VALUES (?,?)",
                             [(ct, " / ".join(sorted(v))) for ct, v in sorted(names.items())])
            conn.executemany("INSERT INTO notes VALUES (?)",
                             [(n,) for n in notes if n.startswith(family + " ")])
            order = sorted({(stage_of(p), p) for p in stage_paths},
                           key=lambda x: STAGES.index(x[0]))
            conn.executemany("INSERT INTO stages VALUES (?,?,?)",
                             [(st, STAGES.index(st), p) for st, p in order])
            conn.execute("CREATE INDEX idx_counts ON counts (stream, region, varno, stage, date)")
            conn.execute("CREATE INDEX idx_flags ON flags (stream, region, varno, date)")
        written.append(path)
    return written


def summary(path: str, region: str) -> List[str]:
    """Over the whole period, the observations of every variable that
    reaches the last stage, stage by stage, per branch: * marks a count below
    a later one (partial, the variable is derived later)."""
    lines = []
    with sqlite3.connect(path) as conn:
        stages = [r[0] for r in conn.execute("SELECT stage FROM stages ORDER BY position")]
        family = os.path.basename(path)[len("obschain_"):-3]
        for (stream,) in conn.execute(
                "SELECT DISTINCT stream FROM counts "
                "ORDER BY CASE stream WHEN 'trunk' THEN 0 WHEN 'global' THEN 1 ELSE 2 END"):
            tot = defaultdict(dict)
            for stage, varno, n in conn.execute(
                    "SELECT stage, varno, SUM(n) FROM counts WHERE stream = ? AND region = ? "
                    "GROUP BY stage, varno", (stream, region)):
                tot[varno][stage] = n
            present = [st for st in stages if any(st in t for t in tot.values())]
            if not present:
                continue
            nchan = dict(conn.execute(
                "SELECT stage, COUNT(DISTINCT channel) FROM counts WHERE stream = ? "
                "AND region = ? AND channel IS NOT NULL GROUP BY stage", (stream, region)))
            last = present[-1]
            varnos = sorted(v for v, t in tot.items() if last in t)
            label = {"trunk": " -- trunk, global and RARS together",
                     "rars": " (RARS)"}.get(stream, "")
            lines.append(f"{family}{label}, {region}:")
            w = max(14, 2 + max(len(f"{n:,d}") for t in tot.values() for n in t.values()))
            lines.append(f"{'varno':>7s}" + "".join(f"{st:>{w}s}" for st in present))
            for v in varnos:
                cells = []
                for i, st in enumerate(present):
                    if st not in tot[v]:
                        cells.append(f"{'-':>{w}s}")
                        continue
                    later = [tot[v][s2] for s2 in present[i + 1:] if s2 in tot[v]]
                    mark = "*" if later and tot[v][st] < max(later) else " "
                    cells.append(f"{tot[v][st]:>{w - 1},d}{mark}")
                lines.append(f"{v:>7d}" + "".join(cells))
            if nchan:
                lines.append(f"{'chan.':>7s}" + "".join(
                    f"{nchan.get(st, 0):>{w - 1},d} " if st in nchan else f"{'-':>{w}s}"
                    for st in present))
    return lines


def make_obschain(stage_paths: Sequence[str], pathwork: str, datestart: str,
                  dateend: str, families: Sequence[str], regions: Sequence[str],
                  n_cpus: int = 1, run: str = "",
                  id_stn: Sequence[str] = ("join",)) -> int:
    """Count every family along the chain and store the counts."""
    t0 = time.time()
    cycles = _cycles(datestart, dateend)
    tasks, notes = plan(stage_paths, families, regions, cycles, pathwork)
    print(f"[obschain] {len(cycles)} cycle(s), {len(tasks)} piece(s) to count, "
          f"{n_cpus} worker(s)", flush=True)
    for n in notes:
        print(f"[obschain] note: {n}", flush=True)
    sliced = sum(1 for t in tasks if t.get("rows"))
    if sliced:
        print(f"[obschain] {sliced} of them are slices of big files, counted "
              f"by several workers at once", flush=True)
    results = _run(tasks, n_cpus)
    failed = sum(r is None for r in results)
    written = store(merge(results), pathwork, notes, stage_paths)
    print(f"[obschain] counted in {time.time() - t0:.1f}s"
          f"{f', {failed} failed' if failed else ''}", flush=True)
    for path in written:
        print("\n" + "\n".join(summary(path, regions[0])), flush=True)
    # the figures: what is left of dbase at every stage, and postalt by flag
    from pikobs.obschain.obschain_plot import make_figures
    table = chain_table()
    when = (f"{datestart[:4]}-{datestart[4:6]}-{datestart[6:8]} {datestart[8:10]} UTC"
            if datestart == dateend else f"{datestart} .. {dateend}")
    def key_of(family, branch):
        """The name the flags module knows the family by: its postalt file,
        without the RARS mark (to_amsua_allsky for to_amsua_allsky_rars)."""
        names = [n for n in table.get(family, {}).get("postalt", [])
                 if is_rars(n) == (branch == "rars")] or [family]
        return re.sub(r"_rars$", "", names[0])
    figs = make_figures(written, list(regions), pathwork, when, run,
                        lambda family: is_radiance(family, table), key_of, list(id_stn))
    from pikobs.obschain.obschain_plot import VIEWER, web_address
    viewer = os.path.join(pathwork, VIEWER)
    print(f"\n[obschain] {len(figs)} figure(s) in {os.path.join(pathwork, 'figures')}, "
          f"the numbers in {os.path.join(pathwork, 'obschain_summary.csv')}", flush=True)
    if os.path.exists(viewer):
        print(f"Viewer: {viewer}", flush=True)
        if web_address(viewer):
            print(f"Web:    {web_address(viewer)}", flush=True)
    return 1 if failed and failed == len(results) else 0


def _split_tokens(raw) -> List[str]:
    out = []
    for item in raw or []:
        out += [t for t in re.split(r"[\s,]+", str(item)) if t]
    return out


def arg_call() -> None:
    import argparse
    p = argparse.ArgumentParser(prog="pikobs-obschain",
                                description="Observations kept at every stage of the chain.")
    p.add_argument("--stage_paths", nargs="+", required=True,
                   help="the directories of the stages, in any order: dbase, cutoff, "
                        "derialt, evalalt, bgckalt, postalt")
    p.add_argument("--pathwork", required=True)
    p.add_argument("--datestart", required=True)
    p.add_argument("--dateend", required=True)
    p.add_argument("--family", nargs="+", required=True)
    p.add_argument("--region", nargs="+", default=["Monde"])
    p.add_argument("--n_cpus", "--n_cpu", type=int, default=1, dest="n_cpus")
    p.add_argument("--id_stn", nargs="+", default=["join"],
                   help="join (every station together), all (one figure per station), "
                        "or station names; several at once")
    p.add_argument("--experience_name", default="",
                   help="the name of the run, shown in the header of the figures")
    p.add_argument("--no_submit", action="store_true")
    args = p.parse_args()
    sys.exit(make_obschain(_split_tokens(args.stage_paths), args.pathwork,
                           args.datestart, args.dateend, _split_tokens(args.family),
                           _split_tokens(args.region), args.n_cpus, args.experience_name,
                           _split_tokens(args.id_stn)))


if __name__ == "__main__":
    arg_call()
