"""Per-model catalog read live from hugpy-discovery's published export.

Discovery owns the model inventory (docs/discovery-wrapper-responsibilities.md);
core reads only what it publishes: the ``api_*_v1`` views materialised into
``<export>/discovery.sqlite3`` (never discovery's live WAL store, and never the
wrapper's own database — the wrapper's state reaches core over HTTP telemetry).

A model is one ``api_units_v1`` key; its quants are the key's variations. File
detail comes from ``api_unit_files_v1``, on-drive state from
``api_unit_presence_v1``. The model list is memoised in-process until the
export's ``api_meta_v1.generation`` changes.
"""
from __future__ import annotations

import os
import re
import sqlite3
import threading
import time

from hugpy_core import discovery

WEIGHT_EXT = (".gguf", ".safetensors", ".bin", ".pth", ".pt", ".ckpt", ".onnx", ".msgpack", ".h5", ".npz")
SHARD = re.compile(r"-(\d{5})-of-(\d{5})(?=\.[A-Za-z0-9]+$)")
FILE_QUANT = re.compile(r"(?i)(?:^|[._-])((?:UD-)?(?:I?Q\d(?:_[0-9A-Z]+)*|BF16|F16|F32|FP16|FP8|FP4|NVFP4))(?=[._-]|$)")
RECORD_LIMIT = 200

# Published views with per-model rows, in the order the Records tab lists them.
UNIT_VIEWS = ("api_units_v1", "api_unit_files_v1", "api_unit_presence_v1", "api_unit_chunks_v1",
              "api_unit_dependencies_v1", "api_unit_representations_v1", "api_unit_envs_v1",
              "api_unit_integrity_v1", "api_placements_v1")

_cache = {"sig": None, "value": None}
_lock = threading.Lock()


class CatalogUnavailable(RuntimeError):
    pass


def discovery_path():
    """The export database this catalog reads (HUGPY_CATALOG_DISCOVERY_DB overrides)."""
    return os.environ.get("HUGPY_CATALOG_DISCOVERY_DB") or discovery.export_db()


def _signature(path):
    try:
        st = os.stat(path)
        return (path, st.st_mtime_ns, st.st_size)
    except OSError:
        return (path, None, None)


def _connect():
    path = discovery_path()
    try:
        return discovery.connect(path), path
    except discovery.DiscoveryError as exc:
        raise CatalogUnavailable(str(exc)) from exc


def _tables(conn):
    return {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view')")}


def _base(p):
    return (p or "").rstrip("/").split("/")[-1]


def _quant_of(name):
    g = FILE_QUANT.search(name or "")
    return g.group(1) if g else None


# ── model + quant assembly ───────────────────────────────────────────────────
def _assemble(conn, *, index_only=False, requested_key=None):
    present_tables = _tables(conn)
    q = lambda sql, *p: conn.execute(sql, p).fetchall()
    narrow = " WHERE key=?" if requested_key is not None else ""
    args = (requested_key,) if requested_key is not None else ()

    on_drive = {}
    if "api_unit_presence_v1" in present_tables:
        for r in q("SELECT key, variation, role, present, complete_bytes, missing_bytes, chunks_in_process "
                   "FROM api_unit_presence_v1" + narrow, *args):
            on_drive.setdefault((r["key"], r["variation"]), []).append(dict(r))

    models = {}
    for r in q("SELECT * FROM api_units_v1" + narrow + " ORDER BY key, variation", *args):
        key = r["key"]
        m = models.get(key)
        if m is None:
            m = models[key] = dict(
                key=key, name=_base(key) or key, source="discovery", location="local",
                origin_worker=None, engine=r["descriptor_engine"],
                framework="gguf" if r["gguf_model"] else None,
                primary_task=r["task"], tasks=[r["task"]] if r["task"] else [],
                hub_id=key if "/" in key and "@" not in key else None,
                architecture=r["arch"], context_length=r["ctx_train"],
                model_dir=r["central_dir"] or r["worker_dir"], discovery_dir=r["central_dir"],
                selected_quant=None, selected_path=None, variations=[])
        m["engine"] = m["engine"] or r["descriptor_engine"]
        m["architecture"] = m["architecture"] or r["arch"]
        m["context_length"] = m["context_length"] or r["ctx_train"]
        m["primary_task"] = m["primary_task"] or r["task"]
        copies = on_drive.get((key, r["variation"]), [])
        m["variations"].append(dict(
            file=r["variation"] or "@directory", quant=_quant_of(r["variation"]),
            bytes=r["weight_bytes"], kind=r["kind"], files=r["files"],
            drives=sorted({c["role"] for c in copies if c["present"]}),
            fetching=any(c["chunks_in_process"] for c in copies)))
    for m in models.values():
        drives = sorted({d for v in m["variations"] for d in v["drives"]})
        m["discovery_state"] = "files" if drives else "not on a drive"
        m["on_drives"] = drives

    if index_only:
        for m in models.values():
            m["quant_count"] = len(m.pop("variations"))
        return models, present_tables
    if requested_key is not None:
        models = {requested_key: models[requested_key]} if requested_key in models else {}

    # files: members, shards and projectors per variation
    members, projectors = {}, {}
    if models and "api_unit_files_v1" in present_tables:
        for r in q("SELECT key, variation, rel_path, bytes, role, projector, dependency, shard, shards, hash_status "
                   "FROM api_unit_files_v1" + narrow + " ORDER BY key, variation, ord", *args):
            if r["key"] not in models:
                continue
            unit = (r["key"], r["variation"] or "@directory")
            if r["projector"]:
                projectors.setdefault(r["key"], []).append(
                    {"file": r["rel_path"], "quant": _quant_of(r["rel_path"]), "bytes": r["bytes"]})
            elif not r["dependency"]:
                members.setdefault(unit, []).append(dict(r))

    for m in models.values():
        quants = []
        for v in m["variations"]:
            unit_files = members.get((m["key"], v["file"]), [])
            names = [f["rel_path"] for f in unit_files] or [v["file"]]
            quants.append(dict(
                file=v["file"], quant=v["quant"], bytes=v["bytes"], path=None, sha256=None,
                members=names, shards=max([f["shards"] or 1 for f in unit_files], default=1),
                selected=False, origin_worker=None, feasibility=None, feasibility_why=None,
                sources=["discovery"], drives=v["drives"], fetching=v["fetching"], kind=v["kind"]))
        m.pop("variations")
        m["quants"] = sorted(quants, key=lambda x: (x["bytes"] is None, x["bytes"] or 0, x["file"]))
        m["quant_count"] = len(m["quants"])
        m["projectors"] = projectors.get(m["key"], [])
        # Feasibility is the wrapper's (its /v1/feasibility and queue plan);
        # discovery publishes none, so the catalog does not claim one.
        m["feasibility_best"] = None
        sizes = [x["bytes"] for x in m["quants"] if x["bytes"]]
        m["size_range"] = [min(sizes), max(sizes)] if sizes else None
    return models, present_tables


def catalog_index():
    """Navigation fields only; no quant assembly, file lists or record counts."""
    conn, _ = _connect()
    try:
        models, _ = _assemble(conn, index_only=True)
        return {"object": "list", "generated_at": time.time(), "view": "index",
                "data": sorted(models.values(), key=lambda m: (m["name"] or m["key"]).lower())}
    finally:
        conn.close()


def catalog():
    """All models with their quants nested; memoised until the export's generation changes."""
    path = discovery_path()
    sig = (_signature(path), discovery.export_generation())
    with _lock:
        if _cache["sig"] == sig and _cache["value"] is not None:
            return _cache["value"]
    conn, path = _connect()
    try:
        models, _ = _assemble(conn)
        generation = discovery.export_generation(conn)
    finally:
        conn.close()
    value = {"object": "list", "generated_at": time.time(),
             "sources": {"discovery": path}, "generation": generation,
             "data": sorted(models.values(), key=lambda m: (m["name"] or m["key"]).lower())}
    with _lock:
        _cache.update(sig=sig, value=value)
    return value


# ── per-model detail ─────────────────────────────────────────────────────────
def _records(conn, table, where, params, rows=False, offset=0, limit=RECORD_LIMIT):
    total = conn.execute(f'SELECT count(*) FROM "{table}" WHERE {where}', params).fetchone()[0]
    if not total:
        return None
    out = {"table": table, "total": total}
    if rows:
        out["offset"] = offset
        out["rows"] = [{k: f"<{len(v)} bytes>" if isinstance(v, bytes) else v for k, v in dict(r).items()}
                       for r in conn.execute(f'SELECT rowid AS _rowid, * FROM "{table}" WHERE {where} '
                                             f'ORDER BY rowid LIMIT {int(limit)} OFFSET {int(offset)}', params)]
    return out


def model(key, records=None, offset=0):
    """One model: summary, quant detail, files and a count of every related export view.

    ``records="discovery.<api view>"`` returns that view's rows for the model instead."""
    conn, path = _connect()
    try:
        models, present_tables = _assemble(conn, requested_key=key)
        m = models.get(key)
        if m is None:
            return None
        q = lambda sql, *p: conn.execute(sql, p).fetchall()

        placements = {}
        if "api_placements_v1" in present_tables:
            for r in q("SELECT variation, destination_role, present, fits, bytes_to_fetch, "
                       "copy_seconds, price_seconds, price_route FROM api_placements_v1 WHERE key=?", key):
                placements.setdefault(r["variation"] or "@directory", []).append(dict(r))
        envs = {}
        if "api_unit_envs_v1" in present_tables:
            for r in q("SELECT variation, engine, env, status, missing, reason FROM api_unit_envs_v1 WHERE key=?", key):
                envs.setdefault(r["variation"] or "@directory", []).append(dict(r))
        for x in m["quants"]:
            x["placements"] = placements.get(x["file"], [])
            x["envs"] = envs.get(x["file"], [])
            # Memory-fit verdicts belong to the wrapper now; nothing is claimed here.
            x["allocations"] = []

        files = []
        if "api_unit_files_v1" in present_tables:
            seen = set()
            for r in q("SELECT variation, rel_path, bytes, role, projector, dependency, dep_key, hash_status "
                       "FROM api_unit_files_v1 WHERE key=? ORDER BY variation, ord", key):
                if r["rel_path"] in seen:
                    continue
                seen.add(r["rel_path"])
                files.append({"file": r["rel_path"], "quant": _quant_of(r["rel_path"]), "bytes": r["bytes"],
                              "role": "projector" if r["projector"] else r["role"],
                              "dependency": r["dep_key"] if r["dependency"] else None,
                              "hash_status": r["hash_status"], "source": "discovery"})

        rec = {"discovery": []}
        for view in UNIT_VIEWS:
            if records and records != f"discovery.{view}":
                continue
            if view in present_tables:
                r = _records(conn, view, "key=?", (key,), rows=bool(records), offset=offset)
                if r:
                    rec["discovery"].append(r)
        if records:
            found = rec["discovery"]
            return found[0] if found else {"table": records.partition(".")[2], "total": 0, "offset": offset, "rows": []}
        return {**m, "files": files, "records": rec, "sources": {"discovery": path}}
    finally:
        conn.close()
