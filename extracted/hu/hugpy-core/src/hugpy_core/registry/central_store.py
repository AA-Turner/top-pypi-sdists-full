# The walk is marker-first (hugpy.json), as transfer_api.central_model_dir
# documents, plus hugpy_storage's get_model_dirs for unstamped dirs. The key rule is LIFTED verbatim from
# fitevict adapters/llama_cpp.discover_models: model_key = the repo dir basename,
# or owner~repo when two owners hold a repo of the same name — so a model's key
# on central equals its key on a box.
"""The central store, as a hugpy_core layer (operator 2026-10-06).

Central's drive (HUGPY_CENTRAL_MODELS_HOME) is not a box: the wrapper never sees
it. Core keeps its inventory in ``central_models`` (sql/010), one row per model
dir, described by that dir's own hugpy.json. One walk seeds it; after that the
writers that change the drive call ``ingest(dir)`` (POST /llm/central/ingest) and
the operator can ``rescan()``. Central never deletes: a vanished dir is marked
``missing``.

``CentralCatalog`` hands the same rows to hugpy_storage (set_catalog_source), so
the transfer blueprint resolves a key from the DB instead of walking the drive.
"""
from __future__ import annotations

import json
import logging
import os
import shutil
from types import SimpleNamespace
from typing import Any, Optional

logger = logging.getLogger("hugpy_core.central")

_COLS = ("model_key", "owner", "repo", "dir", "rel", "hub_id", "framework", "primary_task",
         "tasks", "bytes", "hugpy_json", "marker_mtime", "missing")


def root() -> str:
    from hugpy_storage.transfer_api import central_models_home
    return central_models_home()


def store_id() -> str:
    """Stable identity of this immutable store among potentially many centrals."""
    return (os.environ.get("HUGPY_CENTRAL_STORE_ID") or "central").strip() or "central"


def _db():
    from hugpy_core.grading.grader import _db as db
    return db()


def _marker(d: str) -> "tuple[Optional[dict], Optional[float]]":
    p = os.path.join(d, "hugpy.json")
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f), os.path.getmtime(p)
    except (OSError, ValueError):
        return None, None


def _bytes(d: str, hj: Optional[dict]) -> Optional[int]:
    files = ((hj or {}).get("manifest") or {}).get("files") or []
    n = sum(int(f.get("bytes") or 0) for f in files if isinstance(f, dict))
    if n:
        return n
    total = 0
    for dp, _dn, fns in os.walk(d):
        for fn in fns:
            try:
                total += os.path.getsize(os.path.join(dp, fn))
            except OSError:
                pass
    return total or None


def _describe(d: str, base: str) -> dict:
    from hugpy_storage.model_paths import hub_id_for
    hj, mtime = _marker(d)
    hj = hj if isinstance(hj, dict) else None
    tasks = (hj or {}).get("tasks") if isinstance((hj or {}).get("tasks"), list) else None
    repo = os.path.basename(d.rstrip("/"))
    owner = os.path.basename(os.path.dirname(d.rstrip("/"))) or None
    return {"owner": owner, "repo": repo, "dir": d, "rel": os.path.relpath(d, base),
            "hub_id": (hj or {}).get("hub_id") or hub_id_for(d),
            "framework": (hj or {}).get("framework"),
            "primary_task": (hj or {}).get("primary_task") or (tasks[0] if tasks else None),
            "tasks": tasks, "bytes": _bytes(d, hj), "hugpy_json": hj, "marker_mtime": mtime}


def _upsert(c, rows: list) -> None:
    """Write ``rows`` (described dirs), then re-derive every key with the front
    door's rule over the whole store (a new clash renames both sides)."""
    for r in rows:
        c.execute("INSERT INTO central_models (model_key, owner, repo, dir, rel, hub_id, framework,"
                  " primary_task, tasks, bytes, hugpy_json, marker_mtime, missing, ingested_at)"
                  " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s::jsonb,%s,%s::jsonb,%s,false,now())"
                  " ON CONFLICT (dir) DO UPDATE SET owner=EXCLUDED.owner, repo=EXCLUDED.repo,"
                  " rel=EXCLUDED.rel, hub_id=EXCLUDED.hub_id, framework=EXCLUDED.framework,"
                  " primary_task=EXCLUDED.primary_task, tasks=EXCLUDED.tasks, bytes=EXCLUDED.bytes,"
                  " hugpy_json=EXCLUDED.hugpy_json, marker_mtime=EXCLUDED.marker_mtime,"
                  " missing=false, ingested_at=now()",
                  ("tmp:" + r["dir"], r["owner"], r["repo"], r["dir"], r["rel"], r["hub_id"],
                   r["framework"], r["primary_task"], json.dumps(r["tasks"]), r["bytes"],
                   json.dumps(r["hugpy_json"]) if r["hugpy_json"] is not None else None,
                   r["marker_mtime"]))
    _rekey(c)
    # Central is a reported copy in the Core-owned census, not the census.
    # A marker/size report is not yet a digest verification.
    for r in rows:
        key = c.execute("SELECT model_key FROM central_models WHERE dir=%s", (r["dir"],)).fetchone()[0]
        c.execute("UPDATE model_copies SET present=false,verified=false,observed_at=now() "
                  "WHERE location_kind='central' AND location_id=%s AND path=%s "
                  "AND model_key<>%s AND present", (store_id(), r["dir"], key))
        if store_id() != "central":
            c.execute("UPDATE model_copies SET location_id=%s WHERE model_key=%s "
                      "AND location_kind='central' AND location_id='central' AND path=%s "
                      "AND NOT EXISTS (SELECT 1 FROM model_copies newer WHERE "
                      "newer.model_key=%s AND newer.location_kind='central' AND newer.location_id=%s)",
                      (store_id(), key, r["dir"], key, store_id()))
        c.execute(
            "INSERT INTO model_census (model_key,hub_id,framework,primary_task,metadata) "
            "VALUES (%s,%s,%s,%s,%s::jsonb) ON CONFLICT (model_key) DO UPDATE SET "
            "hub_id=coalesce(EXCLUDED.hub_id,model_census.hub_id), "
            "framework=coalesce(EXCLUDED.framework,model_census.framework), "
            "primary_task=coalesce(EXCLUDED.primary_task,model_census.primary_task),updated_at=now()",
            (key, r["hub_id"], r["framework"], r["primary_task"], json.dumps(r["hugpy_json"] or {})))
        c.execute(
            "INSERT INTO model_copies (model_key,location_kind,location_id,path,bytes,present,verified) "
            "VALUES (%s,'central',%s,%s,%s,true,false) "
            "ON CONFLICT (model_key,location_kind,location_id) DO UPDATE SET "
            "path=EXCLUDED.path,bytes=EXCLUDED.bytes,present=true,verified=false,observed_at=now()",
            (key, store_id(), r["dir"], r["bytes"]))


def _rekey(c) -> None:
    rows = c.execute("SELECT dir, owner, repo, model_key, rel FROM central_models").fetchall()
    counts: dict = {}
    for _d, _o, repo, _k, _rel in rows:
        counts[repo] = counts.get(repo, 0) + 1
    want = {d: (f"{o}~{repo}" if counts[repo] > 1 else repo) for d, o, repo, _k, _rel in rows}
    # NEW (not in the front door's rule): the same owner/repo stored twice on
    # central (an old layout copy). The shortest path keeps the key; each other
    # copy is keyed by its own path, so no copy is hidden or overwritten.
    dupes: dict = {}
    for d, _o, _r, _k, rel in rows:
        dupes.setdefault(want[d], []).append((rel.count(os.sep), rel, d))
    for group in dupes.values():
        for _n, rel, d in sorted(group)[1:]:
            want[d] = rel.replace(os.sep, "~")
    stale = [(d, want[d]) for d, _o, _r, k, _rel in rows if k != want[d]]
    if not stale:
        return
    # two passes so a swap never trips the primary key
    for d, _k in stale:
        c.execute("UPDATE central_models SET model_key = %s WHERE dir = %s", ("tmp:" + d, d))
    for d, k in stale:
        c.execute("UPDATE central_models SET model_key = %s WHERE dir = %s", (k, d))


_SKIP = {"_archive", "archive", "ARCHIVE", "cache", "incoming", "outgoing", "_held", "discarded"}


def model_dirs(base: str, max_depth: int = 5) -> list:
    """Every model dir on the central drive. Marker-first (hugpy.json is
    authoritative — transfer_api's own rule): a dir holding hugpy.json is one
    model and is not descended into. hugpy_storage's get_model_dirs entries with
    no marker anywhere beneath them (unstamped dirs) are kept as models too."""
    from hugpy_storage.model_paths import get_model_dirs
    marked = []
    for dp, dns, fns in os.walk(base):
        rel = os.path.relpath(dp, base)
        depth = 0 if rel == "." else rel.count(os.sep) + 1
        if "hugpy.json" in fns and depth:
            marked.append(dp)
            dns[:] = []
            continue
        dns[:] = [d for d in dns if d not in _SKIP and not d.startswith(".") and depth < max_depth]
    out = list(marked)
    for d in get_model_dirs(models_home=base):
        if not any(m == d or m.startswith(d.rstrip(os.sep) + os.sep) or d.startswith(m + os.sep)
                   for m in marked):
            out.append(d)
    return sorted(set(out))


def rescan() -> dict:
    """Walk the central store once: (re)describe every model dir, mark vanished
    ones missing (central never deletes)."""
    base = root()
    dirs = model_dirs(base)
    rows = [_describe(d, base) for d in dirs]
    with _db() as c:
        with c.transaction():
            _upsert(c, rows)
            gone = c.execute("UPDATE central_models SET missing = true WHERE NOT (dir = ANY(%s))"
                             " AND NOT missing RETURNING model_key", (list(dirs),)).fetchall()
            c.execute("UPDATE model_copies SET present=false,verified=false,observed_at=now() "
                      "WHERE location_kind='central' AND location_id=%s AND present "
                      "AND NOT (path = ANY(%s))", (store_id(), list(dirs)))
    logger.info("central rescan: %d model dirs under %s, %d newly missing", len(rows), base, len(gone))
    _replan("rescan")
    return {"root": base, "models": len(rows), "newly_missing": [g[0] for g in gone]}


def ingest(d: str) -> dict:
    """Re-describe ONE dir on the central drive (a writer just changed it)."""
    base = os.path.realpath(root())
    d = os.path.realpath(d)
    if not (d == base or d.startswith(base + os.sep)):
        raise ValueError(f"{d} is not under the central store {base}")
    with _db() as c:
        with c.transaction():
            if os.path.isdir(d):
                _upsert(c, [_describe(d, base)])
            else:
                c.execute("UPDATE central_models SET missing = true WHERE dir = %s", (d,))
                c.execute("UPDATE model_copies SET present=false,verified=false,observed_at=now() "
                          "WHERE location_kind='central' AND location_id=%s AND path=%s", (store_id(), d))
        row = c.execute("SELECT model_key, missing FROM central_models WHERE dir = %s", (d,)).fetchone()
    _replan("ingest " + os.path.basename(d))
    return {"dir": d, "model_key": row[0] if row else None, "missing": bool(row and row[1])}


def remove(model_key: str) -> dict:
    """Delete one local central archive directory named by its catalog key.

    This is an explicit operator action from the Models page.  It deliberately
    removes only this central's bytes: worker copies are observations owned by
    their workers and must never be reached through the central filesystem.
    The catalog row is retained as ``missing`` so an archive sweep/re-download
    can reconcile it later rather than silently losing identity history.
    """
    key = str(model_key or "").strip()
    if not key:
        raise ValueError("model key is required")
    base = os.path.realpath(root())
    with _db() as c:
        with c.transaction():
            row = c.execute("SELECT dir FROM central_models WHERE model_key=%s AND NOT missing FOR UPDATE",
                            (key,)).fetchone()
            if row is None:
                raise LookupError(f"no local central files for model {key!r}")
            original = row[0]
            target = os.path.realpath(original)
            # The database is not permission to remove an arbitrary path.  A
            # stale/corrupt row, symlink or central root itself stops here.
            if (os.path.islink(original) or target == base or
                    not target.startswith(base.rstrip(os.sep) + os.sep)):
                raise ValueError("central model path is outside the central archive")
            if not os.path.isdir(target):
                # The bytes are already gone; converge the record instead of
                # returning a false 404 to the operator.
                removed = 0
            else:
                removed = _bytes(target, _marker(target)[0]) or 0
                shutil.rmtree(target)
            c.execute("UPDATE central_models SET missing=true, ingested_at=now() WHERE model_key=%s", (key,))
            c.execute("UPDATE model_copies SET present=false,verified=false,observed_at=now() "
                      "WHERE model_key=%s AND location_kind='central' AND location_id=%s AND path=%s",
                      (key, store_id(), original))
    _replan("remove " + key)
    return {"model_key": key, "path": target, "bytes_removed": removed,
            "warning": "Deleted this central archive copy only; worker-drive copies, if any, remain unchanged."}


def _replan(reason: str) -> None:
    """Central's inventory changed: every worker's verdicts cover every central
    model (planner.central_entries), so every worker re-plans. Best effort."""
    try:
        from hugpy_core.brain import planner
        planner.replan_all(reason)
    except Exception:  # noqa: BLE001 — the inventory write already happened
        logger.exception("re-plan after %s failed", reason)


def seed_if_empty() -> None:
    """The one seed walk: only when the table has never been filled."""
    try:
        with _db() as c:
            n = c.execute("SELECT count(*) FROM central_models").fetchone()[0]
        if not n:
            rescan()
    except Exception:  # noqa: BLE001 — core serves without the central layer
        logger.exception("central seed failed")


_DISCOVERED = {"at": 0.0, "rows": []}
_DISCOVERED_TTL_S = 60.0


def _own_rows() -> bool:
    with _db() as c:
        return c.execute("SELECT 1 FROM central_models LIMIT 1").fetchone() is not None


def discovered() -> list:
    """Central as discovery publishes it, in this table's row shape. Discovery owns the central
    drive's inventory; an install that never walked a central folder of its own answers with
    this. Framework, tasks and hub id come from Core's catalog entry of the same key. A unit
    whose directory is not there is ``missing``. Held for a minute: the export changes often."""
    import time
    if _DISCOVERED["rows"] and time.time() - _DISCOVERED["at"] < _DISCOVERED_TTL_S:
        return _DISCOVERED["rows"]
    from hugpy_core import discovery
    try:
        units = discovery.central_units()
    except Exception as exc:  # noqa: BLE001 — no export on this host: there is nothing to add
        logger.debug("central: no discovery export (%s)", exc)
        return []
    catalog = {}
    try:
        with _db() as c:
            for key, framework, primary, metadata in c.execute(
                    "SELECT model_key, framework, primary_task, metadata FROM models").fetchall():
                catalog[key] = (framework, primary, metadata or {})
                # the catalog describes a model by its units (key::variation) too: what a unit
                # says of framework and task holds for the model's directory
                head = key.split("::", 1)[0]
                if head != key and framework and not (catalog.get(head) or (None,))[0]:
                    catalog[head] = (framework, (catalog.get(head) or (None, primary))[1] or primary,
                                     (catalog.get(head) or (None, None, {}))[2] or metadata or {})
    except Exception:  # noqa: BLE001 — the list is still worth having without the catalog's facts
        logger.debug("central: catalog facts unavailable", exc_info=True)
    out = []
    for unit in units:
        key, directory, base = unit["key"], unit["dir"], (unit["root"] or "").rstrip("/")
        framework, primary, metadata = catalog.get(key) or (None, None, {})
        owner, _, repo = key.rpartition("/")
        tasks = list(dict.fromkeys(t for t in [primary or unit["task"], *(metadata.get("tasks") or [])] if t))
        out.append({
            "model_key": key, "owner": owner or None, "repo": repo, "dir": directory,
            "rel": os.path.relpath(directory, base) if base and directory.startswith(base + "/") else directory,
            "hub_id": metadata.get("hub_id") or (key if owner else None),
            "framework": framework or ("gguf" if unit["gguf"] else None),
            "primary_task": primary or unit["task"], "tasks": tasks, "bytes": int(unit["bytes"] or 0),
            "hugpy_json": None, "marker_mtime": None, "missing": not os.path.isdir(directory)})
    _DISCOVERED.update(at=time.time(), rows=out)
    return out


def view_root() -> str:
    """The root the rows of rows() live under: this install's central home when it keeps its own
    inventory, else the central root discovery declares."""
    try:
        if not _own_rows() and discovered():
            from hugpy_core import discovery
            declared = discovery.drive_roots().get("central") or []
            if declared:
                return declared[0].rstrip("/")
    except Exception:  # noqa: BLE001
        logger.debug("central: view root falls back", exc_info=True)
    return root()


def rows(include_missing: bool = False, *, summary: bool = False) -> list:
    if not _own_rows():
        return [row for row in discovered() if include_missing or not row["missing"]]
    columns = list(_COLS)
    if summary:
        # Compact catalog pages need classification, not every file/tensor in
        # every model's manifest. Project in SQL before decoding JSON in Python.
        fields = ('tasks', 'primary_task', 'task_override', 'framework', 'hub_id',
                  'moe_capable', 'bnb_capable')
        marker = ', '.join(f"'{key}', hugpy_json->'{key}'" for key in fields)
        marker += ", 'hub', jsonb_build_object('pipeline_tag', COALESCE(hugpy_json#>'{hub_meta,pipeline_tag}', hugpy_json#>'{hub,pipeline_tag}'))"
        columns[columns.index('hugpy_json')] = f'jsonb_strip_nulls(jsonb_build_object({marker}))'
    with _db() as c:
        got = c.execute(f"SELECT {', '.join(columns)} FROM central_models"
                        + ("" if include_missing else " WHERE NOT missing")
                        + " ORDER BY model_key").fetchall()
    return [dict(zip(_COLS, r)) for r in got]


# ── hugpy_storage's catalog seam, backed by central_models ──────────────────
class CentralCatalog:
    """hugpy_storage.catalog_source protocol over the central_models rows."""

    def _find(self, model_key: str) -> Optional[dict]:
        k = str(model_key or "").strip()
        if not k:
            return None
        forms = {k, k.replace("/", "~"), k.replace("~", "/")}
        leaf = k.replace("~", "/").rsplit("/", 1)[-1]
        with _db() as c:
            r = c.execute(f"SELECT {', '.join(_COLS)} FROM central_models WHERE NOT missing AND"
                          " (model_key = ANY(%s) OR hub_id = ANY(%s) OR (owner || '/' || repo) = ANY(%s))"
                          " ORDER BY model_key LIMIT 1", (list(forms), list(forms), list(forms))).fetchone()
            if r is None:
                hits = c.execute(f"SELECT {', '.join(_COLS)} FROM central_models"
                                 " WHERE NOT missing AND repo = %s", (leaf,)).fetchall()
                r = hits[0] if len(hits) == 1 else None
        return dict(zip(_COLS, r)) if r else None

    def rows(self) -> "dict[str, dict]":
        return {r["model_key"]: r for r in rows()}

    def get(self, model_key: str) -> Any:
        r = self._find(model_key)
        if not r:
            return None
        hj = r.get("hugpy_json") or {}
        return SimpleNamespace(**{**hj, **{k: v for k, v in r.items() if k != "hugpy_json"},
                                  "extra": hj.get("extra") or {}})

    def canonical_key(self, model_key: str) -> Optional[str]:
        r = self._find(model_key)
        return r["model_key"] if r else None

    def resolve_dir(self, model_key: str) -> Optional[str]:
        r = self._find(model_key)
        return r["dir"] if r else None

    def register(self, model_key: str, row: dict) -> bool:
        raise NotImplementedError("central rows come from the drive (ingest), not registration")

    def refresh(self) -> None:
        raise NotImplementedError("use central_store.rescan()")


def on_storage_install(_model: dict, directory: str) -> None:
    """Download-daemon hook: publish the completed bundle into Core's census."""
    if os.environ.get("HUGPY_CENTRAL_MODELS_HOME"):
        ingest(directory)
