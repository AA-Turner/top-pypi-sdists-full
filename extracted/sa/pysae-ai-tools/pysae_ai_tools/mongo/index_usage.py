"""Analyse MongoDB index usage cluster-wide to surface unused indexes.

Design
------
The tool connects with the mongosh CLI (never the MongoDB MCP) in two phases:

1. **Cohorts** — every database is listed and grouped by its *collection
   signature* (the sorted set of its collection names). In a multi-tenant
   cluster most databases are per-tenant clones sharing the exact same set of
   collections — and, by assumption, the same set of indexes — so they land in
   one cohort (the tenant fleet). A database with a unique signature (e.g.
   ``shared``) is its own singleton cohort.
2. **Measurement** — for each ``<database>.<collection>`` it collects one
   measurement entry:

   - volumetry: ``data`` (uncompressed ``size``), ``disk`` (compressed
     ``storageSize``) and ``index`` (``totalIndexSize``), plus the per-index
     on-disk size;
   - usage: ``$indexStats`` operation counters and their observation window.

By default **every database is measured** — exact, exhaustive, and slower on
large clusters. ``--sample-dbs N`` is an opt-in speed knob that measures only N
databases per cohort (singletons always fully measured); it is *sound* under the
homogeneity assumption (tenant clones share structure) but yields extrapolated,
approximate figures rather than exact ones.

Verdicts are computed **globally within a cohort** over its measured members: an
index is only "unused" when it received zero operations across every measured
member, and the reclaimable space is summed over them (then extrapolated to the
full cohort size when sampling). Homogeneity violations (an index present in some
measured members but missing from others) are reported.
"""

import json
import os
import sys
from collections import defaultdict
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Annotated, Any

import typer

from .common.mongosh import MongoshError, run_mongosh

DEFAULT_EXCLUDED_DBS = ("admin", "local", "config")
# 0 = measure every database (exact, exhaustive). A positive value samples that
# many databases per cohort — an opt-in speed knob, never the default.
DEFAULT_SAMPLE_DBS = 0
DEFAULT_TIMEOUT = 3600.0
META_PREFIX = "__META__"
DBSIG_PREFIX = "__DBSIG__"
DATA_PREFIX = "__DATA__"
ERROR_PREFIX = "__ERROR__"

# mongosh collector. Volumetry (sizes) is read once from the primary; index-usage
# operation counters are read from EVERY replica-set member (via directConnection)
# and summed, since $indexStats only reflects the node it runs on. All values are
# pre-normalised to plain JSON in JS (ints via Number(), dates via toISOString(),
# index keys via JSON.stringify) so the Python side needs no Extended-JSON decoding.
COLLECTOR_JS = r"""
const uri = process.env.PYSAE_MONGO_URI;
if (!uri) { print("__ERROR__ missing PYSAE_MONGO_URI"); quit(1); }
let opts = {};
try { opts = JSON.parse(process.env.PYSAE_MONGO_OPTS || "{}"); } catch (e) { opts = {}; }
const excluded = new Set(opts.excludeDbs || []);
const includeOnly = (opts.includeDbs && opts.includeDbs.length) ? new Set(opts.includeDbs) : null;
const collFilter = (opts.collections && opts.collections.length) ? new Set(opts.collections) : null;
const sampleDbs = (opts.sampleDbs && opts.sampleDbs > 0) ? opts.sampleDbs : 0;
const SEP = String.fromCharCode(1);

function hashStr(s) {
  let h = 5381;
  for (let i = 0; i < s.length; i++) h = ((h << 5) + h + s.charCodeAt(i)) | 0;
  return (h >>> 0).toString(16);
}

// The `user:pass` credential block from the URI, reused verbatim (still encoded)
// to build directConnection URIs to individual members.
function authPart(u) {
  const m = u.match(/^mongodb(?:\+srv)?:\/\/([^@]+)@/);
  return m ? m[1] : "";
}

// Sum $indexStats operation counts from one node into the shared index refs.
function gatherUsage(client, dbNames, dbCollsMap, refMap) {
  for (const dbName of dbNames) {
    const cdb = client.getDB(dbName);
    for (const collName of dbCollsMap[dbName]) {
      let usage;
      try { usage = cdb.getCollection(collName).aggregate([{ $indexStats: {} }]).toArray(); }
      catch (e) { continue; }
      for (const u of usage) {
        const ref = refMap[dbName + SEP + collName + SEP + u.name];
        if (!ref) continue;
        const acc = u.accesses || {};
        ref.ops += acc.ops ? Number(acc.ops) : 0;
        if (acc.since) {
          const s = acc.since.toISOString();
          if (ref.since === null || s > ref.since) ref.since = s;  // most recent reset across nodes
        }
      }
    }
  }
}

const conn = new Mongo(uri);
const admin = conn.getDB("admin");

const meta = {};
try {
  const ss = admin.serverStatus();
  meta.host = ss.host; meta.uptimeSecs = ss.uptime; meta.version = ss.version;
} catch (e) { meta.serverStatusError = String(e); }
let members = [];
try {
  const hello = admin.runCommand({ hello: 1 });
  meta.setName = hello.setName || null;
  meta.isPrimary = !!(hello.isWritablePrimary || hello.ismaster);
  members = (hello.hosts || []).slice();
} catch (e) { /* standalone */ }

let dbList;
try { dbList = admin.adminCommand({ listDatabases: 1, nameOnly: true }).databases.map(d => d.name); }
catch (e) { dbList = conn.getDBNames(); }

// Phase 1 — collection signature per database.
const dbColls = {};
const dbSig = {};
for (const dbName of dbList) {
  if (excluded.has(dbName)) continue;
  if (includeOnly && !includeOnly.has(dbName)) continue;
  let names;
  try { names = conn.getDB(dbName).getCollectionNames(); } catch (e) { continue; }
  if (collFilter) {
    names = names.filter(n => collFilter.has(n));
    if (names.length === 0) continue;
  }
  names.sort();
  dbColls[dbName] = names;
  dbSig[dbName] = hashStr(names.join(""));
}

const bySig = {};
for (const db in dbSig) { (bySig[dbSig[db]] = bySig[dbSig[db]] || []).push(db); }

const measured = new Set();
for (const sig in bySig) {
  const group = bySig[sig].slice().sort();
  const take = (sampleDbs === 0 || group.length <= sampleDbs) ? group.length : sampleDbs;
  for (let i = 0; i < take; i++) measured.add(group[i]);
}

const sigOut = [];
for (const db in dbSig) {
  sigOut.push({ db: db, sig: dbSig[db], collCount: dbColls[db].length, measured: measured.has(db) });
}
print("__DBSIG__" + JSON.stringify(sigOut));

const measuredList = Object.keys(dbColls).filter(d => measured.has(d));
let collTotal = 0;
for (const d of measuredList) collTotal += dbColls[d].length;
print("__PROGRESS__" + JSON.stringify({ phase: "start", dbTotal: measuredList.length, collTotal: collTotal }));

// Phase 2a — volumetry + index specs from the primary. Sizes are replicated, so
// they are read once here; ops start at 0 and are filled from every member below.
const out = [];
const idxRef = {};
let collDone = 0;
for (let di = 0; di < measuredList.length; di++) {
  const dbName = measuredList[di];
  const db = conn.getDB(dbName);
  const colls = dbColls[dbName];
  for (let ci = 0; ci < colls.length; ci++) {
    const collName = colls[ci];
    collDone++;
    if (collDone % 500 === 0) {
      const tick = { phase: "tick", sub: "sizes", collDone: collDone, collTotal: collTotal, db: dbName };
      print("__PROGRESS__" + JSON.stringify(tick));
    }
    const coll = db.getCollection(collName);
    let storage = null;
    try {
      const cs = coll.aggregate([{ $collStats: { storageStats: {} } }]).toArray();
      if (cs.length) storage = cs[0].storageStats || {};
    } catch (e) { continue; }
    if (!storage || (storage.size === undefined && storage.indexSizes === undefined)) continue;
    const indexSizes = storage.indexSizes || {};
    let specs = [];
    try { specs = coll.getIndexes(); } catch (e) { specs = []; }

    const indexes = [];
    for (const s of specs) {
      const obj = {
        name: s.name,
        key: JSON.stringify(s.key || {}),
        ops: 0,
        since: null,
        size: indexSizes[s.name] ? Number(indexSizes[s.name]) : 0,
        unique: !!s.unique,
        ttl: s.expireAfterSeconds !== undefined,
        partial: s.partialFilterExpression !== undefined,
        sparse: !!s.sparse,
      };
      indexes.push(obj);
      idxRef[dbName + SEP + collName + SEP + s.name] = obj;
    }
    out.push({
      db: dbName,
      collection: collName,
      docCount: storage.count ? Number(storage.count) : 0,
      dataSize: storage.size ? Number(storage.size) : 0,
      storageSize: storage.storageSize ? Number(storage.storageSize) : 0,
      totalIndexSize: storage.totalIndexSize ? Number(storage.totalIndexSize) : 0,
      indexes: indexes,
    });
  }
  const dbProgress = {
    phase: "db", sub: "sizes", dbIndex: di + 1, dbTotal: measuredList.length,
    db: dbName, collDone: collDone, collTotal: collTotal,
  };
  print("__PROGRESS__" + JSON.stringify(dbProgress));
}

// Phase 2b — index usage from every replica-set member, summed into idxRef.
const auth = authPart(uri);
let nodesQueried = 0;
if (members.length === 0) {
  gatherUsage(conn, measuredList, dbColls, idxRef);  // standalone
  nodesQueried = 1;
} else {
  const directOpts = "/?directConnection=true&tls=true&authSource=admin";
  for (let mi = 0; mi < members.length; mi++) {
    const host = members[mi];
    const node = { phase: "node", nodeIndex: mi + 1, nodeTotal: members.length, host: host };
    print("__PROGRESS__" + JSON.stringify(node));
    let mc;
    try {
      mc = new Mongo("mongodb://" + (auth ? auth + "@" : "") + host + directOpts);
    } catch (e) { continue; }
    try { gatherUsage(mc, measuredList, dbColls, idxRef); nodesQueried++; } catch (e) { /* unreachable */ }
  }
}

meta.members = members.length;
meta.nodesQueried = nodesQueried;
print("__META__" + JSON.stringify(meta));
print("__DATA__" + JSON.stringify(out));
"""


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------
class Verdict(str, Enum):
    KEEP = "KEEP"  # _id_ — never droppable
    CONSTRAINT = "CONSTRAINT"  # unique / TTL — backs a constraint, may show 0 ops
    UNUSED = "UNUSED"  # 0 ops across every measured member, old enough to trust
    INCONCLUSIVE = "INCONCLUSIVE"  # 0 ops but observation window too short
    USED = "USED"


@dataclass
class IndexEntry:
    name: str
    key: str
    ops: int
    since: datetime | None
    size: int
    unique: bool
    ttl: bool
    partial: bool
    sparse: bool


@dataclass
class CollectionEntry:
    """One ``<database>.<collection>`` measurement."""

    db: str
    collection: str
    doc_count: int
    data_size: int
    storage_size: int
    total_index_size: int
    indexes: list[IndexEntry]


@dataclass
class DbSig:
    db: str
    sig: str
    coll_count: int
    measured: bool


@dataclass
class GlobalIndex:
    """An index aggregated across every measured member of a cohort."""

    collection: str
    name: str
    keys: list[str]
    total_ops: int
    total_size: int
    present_in: int  # measured members carrying this index
    used_in: int  # measured members with ops > 0
    oldest_since: datetime | None
    unique: bool
    ttl: bool
    partial: bool
    verdict: Verdict


@dataclass
class CollectionVolumetry:
    """Volumetry of one collection summed over a cohort's measured databases."""

    collection: str
    db_count: int
    data_size: int  # uncompressed logical size
    storage_size: int  # compressed on-disk size
    total_index_size: int  # on-disk index size
    doc_count: int


@dataclass
class HomogeneityIssue:
    collection: str
    index: str
    present_in: int
    missing_from: list[str]


@dataclass
class Cohort:
    signature_id: int
    databases: list[str]  # every member
    measured_databases: list[str]
    collection_count: int
    is_singleton: bool
    indexes: list[GlobalIndex]
    volumetry: list[CollectionVolumetry] = field(default_factory=list)
    homogeneity_issues: list[HomogeneityIssue] = field(default_factory=list)

    @property
    def measured_reclaimable_bytes(self) -> int:
        return sum(i.total_size for i in self.indexes if i.verdict == Verdict.UNUSED)

    @property
    def estimated_reclaimable_bytes(self) -> int:
        """Measured reclaimable extrapolated to the full cohort."""
        measured = len(self.measured_databases)
        if measured == 0:
            return 0
        return round(self.measured_reclaimable_bytes * len(self.databases) / measured)


@dataclass
class Meta:
    host: str = ""
    uptime_secs: int = 0
    version: str = ""
    set_name: str | None = None
    is_primary: bool | None = None
    members: int = 0
    nodes_queried: int = 0


@dataclass
class Report:
    meta: Meta
    entries: list[CollectionEntry]
    cohorts: list[Cohort]
    min_age_days: int

    @property
    def estimated_reclaimable_bytes(self) -> int:
        return sum(c.estimated_reclaimable_bytes for c in self.cohorts)


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------
def _parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def parse_output(stdout: str) -> tuple[Meta, list[DbSig], list[CollectionEntry]]:
    """Extract the ``__META__``, ``__DBSIG__`` and ``__DATA__`` payloads."""
    meta = Meta()
    db_sigs: list[DbSig] = []
    entries: list[CollectionEntry] = []
    for line in stdout.splitlines():
        if line.startswith(META_PREFIX):
            raw = json.loads(line[len(META_PREFIX) :])
            meta = Meta(
                host=raw.get("host", ""),
                uptime_secs=int(raw.get("uptimeSecs", 0) or 0),
                version=raw.get("version", ""),
                set_name=raw.get("setName"),
                is_primary=raw.get("isPrimary"),
                members=int(raw.get("members", 0) or 0),
                nodes_queried=int(raw.get("nodesQueried", 0) or 0),
            )
        elif line.startswith(DBSIG_PREFIX):
            for rec in json.loads(line[len(DBSIG_PREFIX) :]):
                db_sigs.append(
                    DbSig(
                        db=rec["db"],
                        sig=rec["sig"],
                        coll_count=int(rec.get("collCount", 0)),
                        measured=bool(rec.get("measured")),
                    )
                )
        elif line.startswith(DATA_PREFIX):
            for rec in json.loads(line[len(DATA_PREFIX) :]):
                entries.append(
                    CollectionEntry(
                        db=rec["db"],
                        collection=rec["collection"],
                        doc_count=int(rec.get("docCount", 0)),
                        data_size=int(rec.get("dataSize", 0)),
                        storage_size=int(rec.get("storageSize", 0)),
                        total_index_size=int(rec.get("totalIndexSize", 0)),
                        indexes=[
                            IndexEntry(
                                name=ix["name"],
                                key=ix.get("key", "{}"),
                                ops=int(ix.get("ops", 0)),
                                since=_parse_iso(ix.get("since")),
                                size=int(ix.get("size", 0)),
                                unique=bool(ix.get("unique")),
                                ttl=bool(ix.get("ttl")),
                                partial=bool(ix.get("partial")),
                                sparse=bool(ix.get("sparse")),
                            )
                            for ix in rec.get("indexes", [])
                        ],
                    )
                )
    return meta, db_sigs, entries


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------
def _classify(
    name: str,
    total_ops: int,
    unique: bool,
    ttl: bool,
    newest_since: datetime | None,
    now: datetime,
    min_age_days: int,
) -> Verdict:
    if name == "_id_":
        return Verdict.KEEP
    if total_ops > 0:
        return Verdict.USED
    if unique or ttl:
        return Verdict.CONSTRAINT
    # Gate on the most recent stats-reset seen on any node/db: only trust a
    # zero-op verdict once every observation window is at least min_age_days.
    if newest_since is not None and (now - newest_since).days < min_age_days:
        return Verdict.INCONCLUSIVE
    return Verdict.UNUSED


def _aggregate_cohort_indexes(
    members: list[CollectionEntry], now: datetime, min_age_days: int
) -> tuple[list[GlobalIndex], list[HomogeneityIssue]]:
    """Aggregate index usage per (collection, index) across a cohort's measured members."""
    agg: dict[tuple[str, str], dict[str, Any]] = {}
    coll_member_dbs: dict[str, set[str]] = defaultdict(set)
    index_dbs: dict[tuple[str, str], set[str]] = defaultdict(set)

    for entry in members:
        coll_member_dbs[entry.collection].add(entry.db)
        for ix in entry.indexes:
            gkey = (entry.collection, ix.name)
            index_dbs[gkey].add(entry.db)
            acc = agg.setdefault(
                gkey,
                {
                    "keys": set(),
                    "total_ops": 0,
                    "total_size": 0,
                    "used_in": 0,
                    "oldest_since": None,
                    "newest_since": None,
                    "unique": False,
                    "ttl": False,
                    "partial": False,
                },
            )
            acc["keys"].add(ix.key)
            acc["total_ops"] += ix.ops
            acc["total_size"] += ix.size
            acc["used_in"] += 1 if ix.ops > 0 else 0
            acc["unique"] = acc["unique"] or ix.unique
            acc["ttl"] = acc["ttl"] or ix.ttl
            acc["partial"] = acc["partial"] or ix.partial
            if ix.since is not None:
                old = acc["oldest_since"]
                acc["oldest_since"] = ix.since if old is None else min(old, ix.since)
                new = acc["newest_since"]
                acc["newest_since"] = ix.since if new is None else max(new, ix.since)

    indexes: list[GlobalIndex] = []
    homogeneity: list[HomogeneityIssue] = []
    for (collection, name), acc in agg.items():
        verdict = _classify(name, acc["total_ops"], acc["unique"], acc["ttl"], acc["newest_since"], now, min_age_days)
        present_in = len(index_dbs[(collection, name)])
        indexes.append(
            GlobalIndex(
                collection=collection,
                name=name,
                keys=sorted(acc["keys"]),
                total_ops=acc["total_ops"],
                total_size=acc["total_size"],
                present_in=present_in,
                used_in=acc["used_in"],
                oldest_since=acc["oldest_since"],
                unique=acc["unique"],
                ttl=acc["ttl"],
                partial=acc["partial"],
                verdict=verdict,
            )
        )
        all_dbs = coll_member_dbs[collection]
        if name != "_id_" and present_in < len(all_dbs):
            missing = sorted(all_dbs - index_dbs[(collection, name)])
            homogeneity.append(
                HomogeneityIssue(collection=collection, index=name, present_in=present_in, missing_from=missing)
            )

    indexes.sort(key=lambda i: (i.collection, i.name))
    homogeneity.sort(key=lambda h: (h.collection, h.index))
    return indexes, homogeneity


def _aggregate_cohort_volumetry(members: list[CollectionEntry]) -> list[CollectionVolumetry]:
    """Sum per-collection volumetry across a cohort's measured databases."""
    agg: dict[str, CollectionVolumetry] = {}
    for entry in members:
        v = agg.get(entry.collection)
        if v is None:
            v = CollectionVolumetry(entry.collection, 0, 0, 0, 0, 0)
            agg[entry.collection] = v
        v.db_count += 1
        v.data_size += entry.data_size
        v.storage_size += entry.storage_size
        v.total_index_size += entry.total_index_size
        v.doc_count += entry.doc_count
    return sorted(agg.values(), key=lambda x: -(x.storage_size + x.total_index_size))


def analyze(
    db_sigs: list[DbSig],
    entries: list[CollectionEntry],
    meta: Meta,
    *,
    min_age_days: int,
    now: datetime | None = None,
) -> Report:
    """Group databases into cohorts by collection signature and score each index."""
    now = now or datetime.now(timezone.utc)

    entries_by_db: dict[str, list[CollectionEntry]] = defaultdict(list)
    for entry in entries:
        entries_by_db[entry.db].append(entry)

    by_sig: dict[str, list[DbSig]] = defaultdict(list)
    for s in db_sigs:
        by_sig[s.sig].append(s)

    cohorts: list[Cohort] = []
    ordered = sorted(by_sig.items(), key=lambda kv: (-len(kv[1]), sorted(d.db for d in kv[1])[0]))
    for sig_id, (_sig, members) in enumerate(ordered):
        dbs = sorted(m.db for m in members)
        measured_dbs = sorted(m.db for m in members if m.measured)
        coll_count = max((m.coll_count for m in members), default=0)
        measured_entries = [e for db in measured_dbs for e in entries_by_db[db]]
        cohort_indexes, homogeneity = _aggregate_cohort_indexes(measured_entries, now, min_age_days)
        volumetry = _aggregate_cohort_volumetry(measured_entries)
        cohorts.append(
            Cohort(
                signature_id=sig_id,
                databases=dbs,
                measured_databases=measured_dbs,
                collection_count=coll_count,
                is_singleton=len(dbs) == 1,
                indexes=cohort_indexes,
                volumetry=volumetry,
                homogeneity_issues=homogeneity,
            )
        )

    return Report(meta=meta, entries=entries, cohorts=cohorts, min_age_days=min_age_days)


# ---------------------------------------------------------------------------
# Collection (live)
# ---------------------------------------------------------------------------
def collect(
    uri: str,
    *,
    exclude_dbs: tuple[str, ...] = DEFAULT_EXCLUDED_DBS,
    include_dbs: tuple[str, ...] = (),
    collections: tuple[str, ...] = (),
    sample_dbs: int = DEFAULT_SAMPLE_DBS,
    timeout: float = DEFAULT_TIMEOUT,
    on_progress: Callable[[str], None] | None = None,
) -> tuple[Meta, list[DbSig], list[CollectionEntry]]:
    opts = json.dumps(
        {
            "excludeDbs": list(exclude_dbs),
            "includeDbs": list(include_dbs),
            "collections": list(collections),
            "sampleDbs": sample_dbs,
        }
    )
    stdout = run_mongosh(COLLECTOR_JS, uri, opts_json=opts, timeout=timeout, on_progress=on_progress)
    if ERROR_PREFIX in stdout and DATA_PREFIX not in stdout:
        raise MongoshError(stdout.strip())
    return parse_output(stdout)


def _progress_reporter() -> Callable[[str], None]:
    """Render ``__PROGRESS__`` payloads on stderr as a live, single-line gauge."""
    tty = sys.stderr.isatty()

    def report(body: str) -> None:
        try:
            ev = json.loads(body)
        except ValueError:
            return
        phase = ev.get("phase")
        if phase == "start":
            msg = f"scanning {ev.get('dbTotal', 0)} databases, {ev.get('collTotal', 0)} collections…"
        elif phase in ("tick", "db"):
            done, total = ev.get("collDone", 0), ev.get("collTotal", 0)
            pct = (100 * done / total) if total else 0
            db = ev.get("db", "")
            suffix = ""
            if phase == "db":
                suffix = f"  [db {ev.get('dbIndex', 0)}/{ev.get('dbTotal', 0)}]"
            msg = f"sizes {done}/{total} collections ({pct:.0f}%) — {db}{suffix}"
        elif phase == "node":
            msg = f"usage: querying member {ev.get('nodeIndex', 0)}/{ev.get('nodeTotal', 0)} — {ev.get('host', '')}"
        else:
            return
        if tty:
            sys.stderr.write("\r\033[K" + msg)
        else:
            sys.stderr.write(msg + "\n")
        sys.stderr.flush()

    return report


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------
def human_bytes(n: int) -> str:
    size = float(n)
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if size < 1024 or unit == "TiB":
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TiB"


def _serialize(report: Report) -> dict[str, Any]:
    def index_dict(ix: GlobalIndex) -> dict[str, Any]:
        d = asdict(ix)
        d["verdict"] = ix.verdict.value
        d["oldest_since"] = ix.oldest_since.isoformat() if ix.oldest_since else None
        return d

    def entry_dict(e: CollectionEntry) -> dict[str, Any]:
        d = asdict(e)
        for ix in d["indexes"]:
            ix["since"] = ix["since"].isoformat() if ix["since"] else None
        return d

    return {
        "meta": asdict(report.meta),
        "min_age_days": report.min_age_days,
        "estimated_reclaimable_bytes": report.estimated_reclaimable_bytes,
        "entries": [entry_dict(e) for e in report.entries],
        "cohorts": [
            {
                "signature_id": c.signature_id,
                "databases": c.databases,
                "measured_databases": c.measured_databases,
                "collection_count": c.collection_count,
                "is_singleton": c.is_singleton,
                "measured_reclaimable_bytes": c.measured_reclaimable_bytes,
                "estimated_reclaimable_bytes": c.estimated_reclaimable_bytes,
                "volumetry": [asdict(v) for v in c.volumetry],
                "indexes": [index_dict(i) for i in c.indexes],
                "homogeneity_issues": [asdict(h) for h in c.homogeneity_issues],
            }
            for c in report.cohorts
        ],
    }


def _cohort_label(c: Cohort) -> str:
    if c.is_singleton:
        return f"singleton db `{c.databases[0]}`"
    sample = ", ".join(c.databases[:3])
    more = f" (+{len(c.databases) - 3} more)" if len(c.databases) > 3 else ""
    return f"fleet of {len(c.databases)} dbs [{sample}{more}]"


def format_report(report: Report, *, top: int = 40) -> str:
    lines: list[str] = []
    m = report.meta
    lines.append("MongoDB index usage")
    node = m.host or "?"
    if m.set_name:
        role = "PRIMARY" if m.is_primary else "SECONDARY"
        node += f" ({m.set_name}/{role})"
    uptime_days = m.uptime_secs / 86400 if m.uptime_secs else 0
    lines.append(f"  primary: {node}  mongo {m.version}  uptime {uptime_days:.1f}d")
    if m.members:
        lines.append(
            f"  $indexStats ops summed across {m.nodes_queried}/{m.members} replica-set members; "
            "verdicts gated on the most recent stats reset among them."
        )
        if m.nodes_queried < m.members:
            lines.append(
                f"  ⚠ only {m.nodes_queried}/{m.members} members answered — usage may be undercounted; "
                "treat UNUSED with caution."
            )
    else:
        lines.append("  note: standalone node — $indexStats reflects this node only.")
    lines.append("")

    exact = all(len(c.measured_databases) == len(c.databases) for c in report.cohorts)
    lines.append(f"Cohorts (databases grouped by identical collection set): {len(report.cohorts)}")
    for c in report.cohorts:
        measured = f"measured {len(c.measured_databases)}/{len(c.databases)}"
        lines.append(f"  [{c.signature_id}] {_cohort_label(c)} — {c.collection_count} collections, {measured}")
    if not exact:
        lines.append("  (sampling active — figures are extrapolated; run without --sample-dbs for exact numbers)")
    lines.append("")

    for c in report.cohorts:
        lines.append(f"══ cohort [{c.signature_id}] — {_cohort_label(c)}")

        lines.append("  Collection totals over measured dbs (data / disk / index / disk+index):")
        for v in c.volumetry:
            lines.append(
                f"    {v.collection} [{v.db_count} dbs]: "
                f"data {human_bytes(v.data_size)} / disk {human_bytes(v.storage_size)} / "
                f"index {human_bytes(v.total_index_size)} / total {human_bytes(v.storage_size + v.total_index_size)}"
                f"  ({v.doc_count:,} docs)"
            )
        lines.append("")

        lines.append("  Volumetry per <database>.<collection> (data / disk / index):")
        cohort_dbs = set(c.measured_databases)
        for entry in sorted(report.entries, key=lambda e: (e.db, e.collection)):
            if entry.db not in cohort_dbs:
                continue
            lines.append(
                f"    {entry.db}.{entry.collection}: "
                f"data {human_bytes(entry.data_size)} / disk {human_bytes(entry.storage_size)} / "
                f"index {human_bytes(entry.total_index_size)}  ({entry.doc_count} docs)"
            )

        cohort_exact = len(c.measured_databases) == len(c.databases)
        droppable = [i for i in c.indexes if i.verdict in (Verdict.UNUSED, Verdict.INCONCLUSIVE)]
        droppable.sort(key=lambda i: (i.verdict != Verdict.UNUSED, -i.total_size))
        lines.append("")
        if cohort_exact:
            reclaim = f"reclaimable {human_bytes(c.measured_reclaimable_bytes)}"
        else:
            reclaim = (
                f"measured {human_bytes(c.measured_reclaimable_bytes)}, "
                f"est. cohort-wide {human_bytes(c.estimated_reclaimable_bytes)}"
            )
        lines.append(f"  Unused / candidate indexes ({reclaim}):")
        if not droppable:
            lines.append("    (none)")
        for i in droppable[:top]:
            since = i.oldest_since.date().isoformat() if i.oldest_since else "n/a"
            lines.append(
                f"    [{i.verdict.value}] {i.collection}.{i.name} {i.keys[0] if i.keys else ''}  "
                f"size {human_bytes(i.total_size)}  ops {i.total_ops}  "
                f"used in {i.used_in}/{i.present_in} measured dbs  since {since}"
            )

        constraint = [i for i in c.indexes if i.verdict == Verdict.CONSTRAINT and i.total_ops == 0]
        if constraint:
            lines.append("  Zero-op but required (unique/TTL — DO NOT drop):")
            for i in constraint:
                lines.append(f"    {i.collection}.{i.name}  size {human_bytes(i.total_size)}")

        if c.homogeneity_issues:
            lines.append("  ⚠ Homogeneity anomalies (index absent from some measured members):")
            for h in c.homogeneity_issues[:top]:
                miss = ", ".join(h.missing_from[:5])
                more = f" (+{len(h.missing_from) - 5})" if len(h.missing_from) > 5 else ""
                lines.append(f"    {h.collection}.{h.index}: missing from {miss}{more}")
        lines.append("")

    total_label = "exact" if exact else "estimated, extrapolated to full cohorts"
    lines.append(
        f"TOTAL reclaimable ({total_label}, UNUSED indexes): " f"{human_bytes(report.estimated_reclaimable_bytes)}"
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main(
    uri: Annotated[
        str | None,
        typer.Option("--uri", help="MongoDB URI (prefer --uri-env to keep it out of the process list)"),
    ] = None,
    uri_env: Annotated[str, typer.Option("--uri-env", help="Environment variable holding the URI")] = "MONGO_URI",
    exclude_db: Annotated[list[str] | None, typer.Option("--exclude-db", help="Database to skip (repeatable)")] = None,
    include_db: Annotated[
        list[str] | None, typer.Option("--include-db", help="Restrict to these databases (repeatable)")
    ] = None,
    collection: Annotated[
        list[str] | None, typer.Option("--collection", help="Restrict to these collections (repeatable)")
    ] = None,
    sample_dbs: Annotated[
        int,
        typer.Option(
            "--sample-dbs",
            help="0 = every database (default, exact); >0 samples N dbs per cohort (faster, approximate).",
        ),
    ] = DEFAULT_SAMPLE_DBS,
    min_age_days: Annotated[
        int, typer.Option("--min-age-days", help="Min $indexStats window to trust a zero-op verdict")
    ] = 7,
    top: Annotated[int, typer.Option("--top", help="Max rows per section in the text report")] = 40,
    timeout: Annotated[float, typer.Option("--timeout", help="mongosh timeout (seconds)")] = DEFAULT_TIMEOUT,
    json_output: Annotated[bool, typer.Option("--json", help="Emit the full report as JSON")] = False,
) -> None:
    """Detect unused MongoDB indexes cluster-wide via $indexStats, reasoning per cohort."""
    resolved = uri or os.environ.get(uri_env)
    if not resolved:
        typer.echo(
            f"No MongoDB URI: pass --uri or set {uri_env} "
            f'(e.g. eval "$(pysae-ai-tools env resolve --set MONGO_URI_DEV)").',
            err=True,
        )
        raise typer.Exit(2)

    excluded = tuple(exclude_db) if exclude_db else DEFAULT_EXCLUDED_DBS
    try:
        meta, db_sigs, entries = collect(
            resolved,
            exclude_dbs=excluded,
            include_dbs=tuple(include_db or ()),
            collections=tuple(collection or ()),
            sample_dbs=sample_dbs,
            timeout=timeout,
            on_progress=_progress_reporter(),
        )
    except MongoshError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(1) from exc
    except KeyboardInterrupt:
        typer.echo("\ninterrupted — mongosh stopped, no report produced.", err=True)
        raise typer.Exit(130) from None
    finally:
        if sys.stderr.isatty():
            sys.stderr.write("\r\033[K")
            sys.stderr.flush()

    report = analyze(db_sigs, entries, meta, min_age_days=min_age_days)

    if json_output:
        json.dump(_serialize(report), sys.stdout, indent=2, default=str)
        sys.stdout.write("\n")
    else:
        typer.echo(format_report(report, top=top))


app = typer.Typer(add_completion=False)
app.command()(main)

if __name__ == "__main__":
    app()
