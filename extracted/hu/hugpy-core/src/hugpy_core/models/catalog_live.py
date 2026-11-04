"""Per-model catalog read live from the wrapper and discovery SQLite databases.

Both databases are opened read-only for each request (attached to one
connection as ``w`` and ``d``); nothing is copied or cached on disk. The model
list is memoised in-process until either database file changes.

Models are the wrapper's ``models`` rows, remote-only models from
``remote_pairs``, and discovery directories that hold weights the wrapper does
not know. A model's quants are its weight files (shards grouped into one quant),
remote pairs and feasibility plans.
"""
from __future__ import annotations

import glob
import json
import os
import re
import sqlite3
import threading
import time

from hugpy_resources.imports.functions.application_paths import resolve_paths

def wrapper_path():
    explicit = os.environ.get('HUGPY_CATALOG_WRAPPER_DB')
    if explicit:
        return explicit
    roots = resolve_paths()
    endpoint = os.path.join(roots['config'], 'wrapper.endpoint.json')
    try:
        with open(endpoint) as source:
            state = json.load(source).get('store')
    except FileNotFoundError:
        state = None
    return os.path.join(state or os.path.join(roots['data'], 'wrapper'), 'fitevict.sqlite3')


WRAPPER_DB = wrapper_path()
DISCOVERY_DB = os.environ.get("HUGPY_CATALOG_DISCOVERY_DB", "")
DISCOVERY_DIR = os.environ.get("HUGPY_CATALOG_DISCOVERY_DIR", "")

WEIGHT_EXT = (".gguf", ".safetensors", ".bin", ".pth", ".pt", ".ckpt", ".onnx", ".msgpack", ".h5", ".npz")
SHARD = re.compile(r"-(\d{5})-of-(\d{5})(?=\.[A-Za-z0-9]+$)")
FILE_QUANT = re.compile(r"(?i)(?:^|[._-])((?:UD-)?(?:I?Q\d(?:_[0-9A-Z]+)*|BF16|F16|F32|FP16|FP8|FP4|NVFP4))(?=[._-]|$)")
FEAS_RANK = {"fits": 0, "exceeds": 1, "unresolved": 2}
RECORD_LIMIT = 200

_cache = {"sig": None, "value": None}
_lock = threading.Lock()


class CatalogUnavailable(RuntimeError):
    pass


def discovery_path():
    if DISCOVERY_DB:
        return DISCOVERY_DB
    if DISCOVERY_DIR:
        found = glob.glob(os.path.join(DISCOVERY_DIR, "discovery-*.sqlite3"))
        return max(found, key=os.path.getmtime) if found else None
    from hugpy_settings.local_settings import values
    return values(('discovery',))['discovery_database'] or None


def _signature(paths):
    sig = []
    for p in paths:
        for suffix in ("", "-wal"):
            try:
                st = os.stat(p + suffix)
                sig.append((p + suffix, st.st_mtime_ns, st.st_size))
            except OSError:
                sig.append((p + suffix, None, None))
    return tuple(sig)


def _connect():
    if not os.access(WRAPPER_DB, os.R_OK):
        raise CatalogUnavailable(f"wrapper database not readable: {WRAPPER_DB}")
    conn = sqlite3.connect(":memory:", uri=True)
    conn.row_factory = sqlite3.Row
    conn.execute("ATTACH ? AS w", (f"file:{WRAPPER_DB}?mode=ro",))
    disc = discovery_path()
    if disc and os.access(disc, os.R_OK):
        conn.execute("ATTACH ? AS d", (f"file:{disc}?mode=ro",))
    else:
        disc = None
    return conn, disc


def _tables(conn, schema):
    return {r[0] for r in conn.execute(f"SELECT name FROM {schema}.sqlite_master WHERE type='table'")}


def _jload(text):
    try:
        return json.loads(text) if text else None
    except (TypeError, ValueError):
        return None


def _base(p):
    return (p or "").rstrip("/").split("/")[-1]


# ── model + quant assembly ───────────────────────────────────────────────────
def _assemble(conn, disc, *, index_only=False, requested_key=None):
    wt = _tables(conn, "w")
    dt = _tables(conn, "d") if disc else set()
    q = lambda sql, *p: conn.execute(sql, p).fetchall()

    d_root = None
    d_dirs = {}
    pipelines, weight_dirs, d_has_files = set(), [], set()
    if "model_records" in dt:
        d_root = (q("SELECT root FROM d.model_record_discovery_passes LIMIT 1") or [[None]])[0][0] \
            if "model_record_discovery_passes" in dt else None
        for r in q("SELECT model_dir, name, architecture, context_length, framework, primary_task, hub_id, files_total "
                   "FROM d.model_records"):
            d_dirs[r["model_dir"]] = dict(r)
        d_has_files = {r[0] for r in q("SELECT DISTINCT model_dir FROM d.model_record_files")}
        if "model_record_bundles" in dt:
            pipelines = {r[0] for r in q("SELECT model_dir FROM d.model_record_bundles WHERE kind='pipeline'")}
            weight_dirs = sorted({r[0] for r in q("SELECT model_dir FROM d.model_record_bundles WHERE role='weights' "
                                                 "AND kind IN ('single-file','shard-index')")} | pipelines)
    rel_index = {}
    if d_root:
        for dd in d_dirs:
            if dd.startswith(d_root + "/"):
                rel_index[dd[len(d_root) + 1:]] = dd

    def discovery_dir_for(model_dir):
        """Match exact directories first, then discovery-relative path suffixes."""
        # Wrapper databases also contain discovery records, without necessarily
        # having a discovery pass/root. Those records already use absolute paths.
        if model_dir in d_dirs:
            return model_dir
        parts = (model_dir or "").strip("/").split("/")
        for i in range(len(parts) - 1):  # at least owner/name, never a bare directory name
            dd = rel_index.get("/".join(parts[i:]))
            if dd:
                return dd
        return None

    under = lambda a, b: a != b and a.startswith(b + "/")

    markers = {r["model_dir"]: dict(r) for r in q(
        "SELECT model_dir, name, framework, primary_task, tasks, hub_id FROM w.model_markers")} \
        if "model_markers" in wt else {}
    records = {r["model_dir"]: dict(r) for r in q(
        "SELECT model_dir, name, architecture, context_length, framework, primary_task, hub_id, files_total, "
        "has_vision, has_tools, has_reasoning, license FROM w.model_records")} if "model_records" in wt else {}

    models = {}
    for r in q("SELECT key, path, model_dir, quant, bytes, engine, runner FROM w.models ORDER BY key"):
        mk, rec = markers.get(r["model_dir"], {}), records.get(r["model_dir"], {})
        tasks = _jload(mk.get("tasks")) or []
        models[r["key"]] = dict(
            key=r["key"], name=mk.get("name") or rec.get("name") or _base(r["model_dir"]) or r["key"],
            source="wrapper", location="local", origin_worker=None, engine=r["engine"], runner=r["runner"],
            framework=mk.get("framework") or rec.get("framework"),
            primary_task=mk.get("primary_task") or rec.get("primary_task"),
            tasks=tasks if isinstance(tasks, list) else [], hub_id=mk.get("hub_id") or rec.get("hub_id"),
            architecture=rec.get("architecture"), context_length=rec.get("context_length"),
            license=rec.get("license"), has_vision=rec.get("has_vision"), has_tools=rec.get("has_tools"),
            has_reasoning=rec.get("has_reasoning"), model_dir=r["model_dir"], selected_quant=r["quant"],
            selected_path=r["path"], bytes=r["bytes"], discovery_dir=discovery_dir_for(r["model_dir"]))
    if "remote_pairs" in wt:
        for r in q("SELECT model_key, engine, origin_worker FROM w.remote_pairs GROUP BY model_key"):
            if r["model_key"] not in models:
                models[r["model_key"]] = dict(key=r["model_key"], name=r["model_key"], source="wrapper",
                                              location="remote", origin_worker=r["origin_worker"],
                                              engine=r["engine"], tasks=[], discovery_dir=None)
    claimed = {m["discovery_dir"] for m in models.values() if m.get("discovery_dir")}
    for dd in weight_dirs:
        if dd in claimed or any(under(dd, c) for c in claimed) or any(under(dd, o) for o in weight_dirs):
            continue
        rec = d_dirs.get(dd, {})
        key = "discovery:" + (dd[len(d_root) + 1:] if d_root and dd.startswith(d_root + "/") else dd)
        models[key] = dict(key=key, name=rec.get("name") or _base(dd), source="discovery", location="local",
                           origin_worker=None, engine="pipeline" if dd in pipelines else None, tasks=[],
                           framework=rec.get("framework"), primary_task=rec.get("primary_task"),
                           hub_id=rec.get("hub_id"), architecture=rec.get("architecture"),
                           context_length=rec.get("context_length"), model_dir=dd, discovery_dir=dd)
    claimed = {m["discovery_dir"] for m in models.values() if m.get("discovery_dir")}
    for m in models.values():
        dd = m.get("discovery_dir")
        m["nested_dirs"] = [c for c in claimed if dd and under(c, dd)]
        if not dd:
            m["discovery_state"] = "not scanned" if m["location"] == "local" else None
        else:
            own = [x for x in d_has_files if (x == dd or under(x, dd)) and not any(x == n or under(x, n) for n in m["nested_dirs"])]
            m["discovery_state"] = "files" if own else "empty placeholder"

    # List navigation does not need quant inventories or folder load geometry.
    if index_only:
        return models, wt, dt
    if requested_key is not None:
        models = {requested_key: models[requested_key]} if requested_key in models else {}

    # quants
    quants = {}

    def quant(key, file, **kw):
        qd = quants.setdefault((key, file), dict(file=file, members=[], sources=[]))
        for k, v in kw.items():
            if v is not None and not qd.get(k):
                qd[k] = v
        return qd

    projectors = {}
    wfiles = {}
    for r in q("SELECT key, file, path, quant, size_bytes, sha256 FROM w.model_discovery_files"
               + (" WHERE key=?" if requested_key is not None else "") + " ORDER BY key, file",
               *([requested_key] if requested_key is not None else [])) \
            if "model_discovery_files" in wt else []:
        wfiles.setdefault(r["key"], []).append(dict(r))
    for model_key, fl in wfiles.items():
        if model_key not in models:
            continue
        loose = [f["file"] for f in fl if f["quant"] is None and f["file"].lower().endswith(WEIGHT_EXT)
                 and "mmproj" not in f["file"].lower()]
        for f in fl:
            if f["quant"] is None:
                continue
            if "mmproj" in f["file"].lower():
                projectors.setdefault(model_key, []).append({"file": f["file"], "quant": f["quant"], "bytes": f["size_bytes"]})
                continue
            head = SHARD.sub(lambda g: f"-00001-of-{g.group(2)}", f["file"])
            qd = quant(model_key, head, quant=f["quant"])
            qd["sources"].append("files")
            if f["file"] == "dir":
                qd["members"], qd["bytes"] = ["dir"] + loose, f["size_bytes"]
            else:
                qd["members"].append(f["file"])
                qd["bytes"] = (qd.get("bytes") or 0) + (f["size_bytes"] or 0)
            if f["file"] == head:
                qd["path"], qd["sha256"] = f["path"], f["sha256"]
    if "remote_pairs" in wt:
        for r in q("SELECT model_key, file, quant, origin_worker, bytes FROM w.remote_pairs"
                   + (" WHERE model_key=?" if requested_key is not None else ""), *([requested_key] if requested_key is not None else [])):
            if r["model_key"] in models:
                quant(r["model_key"], r["file"], quant=r["quant"], origin_worker=r["origin_worker"],
                      bytes=r["bytes"])["sources"].append("remote")
    if "feasibility_plans" in wt:
        for r in q("SELECT model_key, file, json_extract(verdict,'$.quant') AS quant, "
                   "json_extract(verdict,'$.feasibility.capacity_status') AS cap, "
                   "json_extract(verdict,'$.feasibility.status') AS st, "
                   "json_extract(verdict,'$.feasibility.why') AS why FROM w.feasibility_plans"
                   + (" WHERE model_key=?" if requested_key is not None else ""), *([requested_key] if requested_key is not None else [])):
            if r["model_key"] in models:
                qd = quant(r["model_key"], r["file"], quant=r["quant"])
                qd["sources"].append("feasibility")
                qd["feasibility"], qd["feasibility_why"] = r["cap"] or r["st"], r["why"]
    # discovery-only models: weight bundles are quants, a pipeline is one quant
    for m in models.values():
        if m["source"] != "discovery" or "model_record_bundles" not in dt:
            continue
        dd, pipe = m["discovery_dir"], m["discovery_dir"] in pipelines
        for r in q("SELECT bundle_id, model_dir, name, quant_method, tensor_bytes FROM d.model_record_bundles "
                   "WHERE (model_dir=? OR model_dir LIKE ?) AND role='weights' AND kind IN ('single-file','shard-index')",
                   dd, dd + "/%"):
            if pipe and r["model_dir"] != dd:
                continue
            rel = (r["model_dir"] + "/" + r["name"])[len(dd) + 1:]
            g = FILE_QUANT.search(r["name"])
            members = [x[0][len(dd) + 1:] for x in q("SELECT member FROM d.model_record_bundle_members "
                                                     "WHERE bundle_id=? AND member_kind='file'", r["bundle_id"])]
            size = sum(x[0] or 0 for x in q("SELECT bytes FROM d.model_record_files WHERE path IN (%s)" % ",".join(
                "?" * len(members)), *[dd + "/" + x for x in members])) if members else None
            quant(m["key"], rel, quant=r["quant_method"] or (g.group(1).lower() if g else None),
                  members=members or [rel], bytes=size or r["tensor_bytes"])["sources"].append("discovery")
        if pipe:
            quant(m["key"], "@pipeline", quant="pipeline", members=["@pipeline"])["sources"].append("discovery")

    folders = _folder_loads(conn, wt, models)
    for (key, file), qd in quants.items():
        m = models[key]
        members = qd["members"] or [file]
        q = dict(
            file=file, quant=qd.get("quant"), bytes=qd.get("bytes"), path=qd.get("path"), sha256=qd.get("sha256"),
            members=members, shards=max(1, len([x for x in members if x not in ("dir", "@pipeline")])),
            selected=bool(qd.get("path")) and qd.get("path") == m.get("selected_path"),
            origin_worker=qd.get("origin_worker"), feasibility=qd.get("feasibility"),
            feasibility_why=qd.get("feasibility_why"), sources=sorted(set(qd["sources"])))
        if file == "dir":
            # The wrapper stores a whole-folder model under the placeholder "dir".
            # Its own loading inventory says what actually loads; show that.
            q.update(folder_bytes=q["bytes"], selected=True, **folders.get(key, {"label": "full folder"}))
            if m.get("selected_quant") == "dir":
                m["selected_quant"] = q["label"]
        m.setdefault("quants", []).append(q)
    for m in models.values():
        qs = sorted(m.get("quants") or [], key=lambda x: (x["bytes"] is None, x["bytes"] or 0, x["file"]))
        m["quants"] = qs
        m["quant_count"] = len(qs)
        m["projectors"] = projectors.get(m["key"], [])
        m["feasibility_best"] = min((x["feasibility"] for x in qs if x["feasibility"]),
                                    key=lambda s: FEAS_RANK.get(s, 9), default=None)
        sizes = [x["bytes"] for x in qs if x["bytes"]]
        m["size_range"] = [min(sizes), max(sizes)] if sizes else None
    return models, wt, dt


def _folder_loads(conn, wt, models):
    """For whole-folder models: the wrapper's selected load set (tf_structure.loading_inventory)."""
    if "tf_structure" not in wt:
        return {}
    out = {}
    for r in conn.execute("SELECT key, geometry, tensor_bytes, tensor_bytes_bnb4 FROM w.tf_structure "
                          "WHERE key IN (%s)" % ",".join("?" for _ in models), tuple(models)):
        m = models.get(r["key"])
        geo = _jload(r["geometry"]) or {}
        inv = geo.get("loading_inventory") or {}
        if not m or not inv:
            continue
        md = m.get("model_dir") or ""
        parts = inv.get("components") or {"": inv}
        components, rel_paths = [], []
        for name, c in parts.items():
            files = [f"{name}/{f}" if name else f for f in (c.get("files") or [])]
            rel_paths += files
            components.append({"name": name or "model", "files": files, "bytes": c.get("serialized_bytes")})
        dtype = None
        if rel_paths and "model_record_tensor_types" in wt:
            row = conn.execute(
                "SELECT tensor_type, sum(count) n FROM w.model_record_tensor_types WHERE model_dir=? AND rel_path IN (%s) "
                "GROUP BY tensor_type ORDER BY n DESC LIMIT 1" % ",".join("?" * len(rel_paths)), (md, *rel_paths)).fetchone()
            dtype = row["tensor_type"].lower() if row else None
        kind = "full pipeline" if inv.get("kind") == "pipeline" else "full model"
        selected = set(rel_paths)
        unused = []
        if "model_discovery_files" in wt:
            unused = [{"file": f["file"], "bytes": f["size_bytes"]} for f in conn.execute(
                "SELECT file, size_bytes FROM w.model_discovery_files WHERE key=? AND file != 'dir'", (r["key"],))
                if f["file"].lower().endswith(WEIGHT_EXT) and f["file"] not in selected]
        out[r["key"]] = {"label": f"{dtype} · {kind}" if dtype else kind, "quant": dtype or kind,
                         "bytes": inv.get("serialized_bytes") or r["tensor_bytes"], "bytes_4bit": r["tensor_bytes_bnb4"],
                         "components": components, "unused_weights": unused}
    return out


def catalog_index():
    """Navigation fields only; no quant assembly, file lists or record counts."""
    conn, disc = _connect()
    try:
        models, _, _ = _assemble(conn, disc, index_only=True)
        return {"object": "list", "generated_at": time.time(), "view": "index",
                "data": sorted(({k: v for k, v in m.items() if k != "nested_dirs"}
                                for m in models.values()),
                               key=lambda m: (m["name"] or m["key"]).lower())}
    finally:
        conn.close()


def catalog():
    """All models with their quants nested; memoised until a database file changes."""
    disc = discovery_path()
    sig = _signature([WRAPPER_DB] + ([disc] if disc else []))
    with _lock:
        if _cache["sig"] == sig and _cache["value"] is not None:
            return _cache["value"]
    conn, disc = _connect()
    try:
        models, _, _ = _assemble(conn, disc)
    finally:
        conn.close()
    value = {"object": "list", "generated_at": time.time(),
             "sources": {"wrapper": WRAPPER_DB, "discovery": disc},
             "data": sorted(({k: v for k, v in m.items() if k != "nested_dirs"} for m in models.values()),
                           key=lambda m: (m["name"] or m["key"]).lower())}
    with _lock:
        _cache.update(sig=sig, value=value)
    return value


# ── per-model detail ─────────────────────────────────────────────────────────
def _records(conn, schema, table, where, params, rows=False, offset=0, limit=RECORD_LIMIT):
    total = conn.execute(f'SELECT count(*) FROM {schema}."{table}" WHERE {where}', params).fetchone()[0]
    if not total:
        return None
    out = {"table": table, "total": total}
    if rows:
        out["offset"] = offset
        out["rows"] = [{k: f"<{len(v)} bytes>" if isinstance(v, bytes) else v for k, v in dict(r).items()}
                       for r in conn.execute(f'SELECT rowid AS _rowid, * FROM {schema}."{table}" WHERE {where} '
                                             f'ORDER BY rowid LIMIT {int(limit)} OFFSET {int(offset)}', params)]
    return out


def _allocations(conn, dt, key, file):
    """Feasibility per allocation mode: can this quant fit gpu-only, ram-only, ...? Nothing is placed."""
    if "discovery_feasibility_cells" not in dt:
        return []
    return [dict(r) for r in conn.execute(
        "SELECT variant, placement AS allocation, status, context_tokens, gpu_bytes, ram_bytes, reason "
        "FROM d.discovery_feasibility_cells WHERE model_key=? AND file=? ORDER BY variant, placement", (key, file))]


def model(key, records=None, offset=0):
    """One model: summary, quant detail, files and a count of every related source record.

    ``records="wrapper.<table>"`` or ``"discovery.<table>"`` returns that table's rows instead."""
    conn, disc = _connect()
    try:
        models, wt, dt = _assemble(conn, disc, requested_key=key)
        m = models.get(key)
        if m is None:
            return None
        md, dd, nested = m.get("model_dir"), m.get("discovery_dir"), m.get("nested_dirs") or []
        q = lambda sql, *p: conn.execute(sql, p).fetchall()
        quant_files = sorted({f for x in m["quants"] for f in x["members"] + [x["file"]]} |
                             {p["file"] for p in m["projectors"]})

        for x in m["quants"]:
            f = x["file"]
            x["allocations"] = _allocations(conn, dt, key, f)
            if "model_quant_facts" in wt:
                kv = q("SELECT kv_cost FROM w.model_quant_facts WHERE model_key=? AND file=?", key, f)
                x["kv_cost"] = _jload(kv[0][0]) if kv else None
            if "load_estimates" in wt:
                le = q("SELECT drive, load_class, est_load_s, est_cold_s, est_warm_s FROM w.load_estimates "
                       "WHERE model_key=? AND file=? LIMIT 1", key, f)
                x["load_estimate"] = dict(le[0]) if le else None
            if md and "model_record_artifacts" in wt:
                art = q("SELECT arch, block_count, ctx_train, swa_window, moe_is_moe, moe_experts, "
                        "moe_experts_per_token, tensor_count, base_load_bytes, kv_f16_bytes_per_token "
                        "FROM w.model_record_artifacts WHERE model_dir=? AND artifact IN (?, 'dir') LIMIT 1", md, f)
                x["facts"] = dict(art[0]) if art else None
            if md and "model_record_tensor_types" in wt:
                x["tensor_types"] = [dict(r) for r in q(
                    "SELECT tensor_type, sum(count) AS count FROM w.model_record_tensor_types WHERE model_dir=? "
                    "AND rel_path IN (%s) GROUP BY tensor_type ORDER BY 2 DESC" % ",".join("?" * len(x["members"])),
                    md, *x["members"])]
            if "feasibility_plans" in wt:
                v = q("SELECT json_extract(verdict,'$.feasibility') AS f, json_extract(verdict,'$.auto') AS a, "
                      "json_extract(verdict,'$.ctx_train') AS c FROM w.feasibility_plans WHERE model_key=? AND file=?", key, f)
                if v:
                    x["feasibility_detail"] = {"feasibility": _jload(v[0]["f"]), "auto": _jload(v[0]["a"]),
                                               "ctx_train": v[0]["c"]}

        files = []
        if m["source"] == "wrapper" and "model_discovery_files" in wt:
            for r in q("SELECT file, quant, size_bytes, sha256 FROM w.model_discovery_files WHERE key=? ORDER BY file", key):
                role = ("projector" if "mmproj" in r["file"].lower() else "weights" if r["file"] in quant_files
                        else "weights" if r["file"].lower().endswith(WEIGHT_EXT) else "supporting")
                files.append({"file": r["file"], "quant": r["quant"], "bytes": r["size_bytes"], "sha256": r["sha256"],
                              "role": role, "source": "wrapper"})
        if dd and "model_record_files" in dt:
            excl = "".join(" AND model_dir != ? AND model_dir NOT LIKE ?" for _ in nested)
            nparams = [v for n in nested for v in (n, n + "/%")]
            for r in q("SELECT model_dir, rel_path, role, weight_class, bytes, detected_format FROM d.model_record_files "
                       f"WHERE (model_dir=? OR model_dir LIKE ?){excl} ORDER BY model_dir, rel_path", dd, dd + "/%", *nparams):
                files.append({"file": (r["model_dir"] + "/" + r["rel_path"])[len(dd) + 1:], "bytes": r["bytes"],
                              "role": r["role"], "weight_class": r["weight_class"], "format": r["detected_format"],
                              "source": "discovery"})

        # related source records, grouped by database
        rec = {"wrapper": [], "discovery": []}

        def add(group, schema, table, where, *params):
            if records and records != f"{group}.{table}":
                return
            if table in (wt if schema == "w" else dt):
                r = _records(conn, schema, table, where, params, rows=bool(records), offset=offset)
                if r:
                    rec[group].append(r)

        if m["source"] == "wrapper":
            add("wrapper", "w", "models", "key=?", key)
            for table, col in (("model_discovery_facts", "key"), ("model_discovery_files", "key"),
                               ("feasibility_plans", "model_key"), ("model_quant_facts", "model_key"),
                               ("remote_pairs", "model_key"), ("weight_hashes", "model_key"),
                               ("load_estimates", "model_key"), ("pulls", "model_key"), ("ctx_probe_facts", "key"),
                               ("pair_settings", "model_key"), ("operator_actions", "model_key"),
                               ("evictions", "key"), ("residents", "key"), ("tf_structure", "key"),
                               ("tf_measure_facts", "key")):
                add("wrapper", "w", table, f"{col}=?", key)
            if md:
                for table in ("model_markers", "model_records", "model_record_files", "model_record_artifacts",
                              "model_record_layers", "model_record_kv_scales", "model_record_gguf_kv",
                              "model_record_tensor_types", "model_record_values", "model_record_documents",
                              "model_record_leaves"):
                    add("wrapper", "w", table, "model_dir=?", md)
                add("wrapper", "w", "call_log", "model_path=? OR model_path LIKE ?", md, md + "/%")
                add("wrapper", "w", "gguf_structure", "path LIKE ?", md + "/%")
                add("wrapper", "w", "storage_content_hashes", "path LIKE ?", md + "/%")
            if quant_files:
                ph = ",".join("?" * len(quant_files))
                for table in ("gguf_projection_facts", "kv_structure", "projector_facts"):
                    add("wrapper", "w", table, f"file IN ({ph})", *quant_files)
        if dd:
            excl = lambda col: "".join(f" AND {col} != ? AND {col} NOT LIKE ?" for _ in nested)
            np_ = [v for n in nested for v in (n, n + "/%")]
            for table in ("model_records", "model_record_values", "model_record_documents", "model_record_leaves",
                          "model_record_files", "model_record_artifacts", "model_record_gguf_kv",
                          "model_record_tensor_types", "model_record_bundles"):
                add("discovery", "d", table, f"(model_dir=? OR model_dir LIKE ?){excl('model_dir')}", dd, dd + "/%", *np_)
            add("discovery", "d", "model_record_directory_snapshots",
                f"(directory=? OR directory LIKE ?){excl('directory')}", dd, dd + "/%", *np_)
            for table in ("model_record_discovery_facts", "model_record_analysis"):
                add("discovery", "d", table, f"(subject=? OR subject LIKE ? OR subject LIKE ?){excl('subject')}",
                    dd, dd + "/%", dd + "::%", *np_)
            for table in ("model_record_tensor_facts", "model_record_evidence"):
                add("discovery", "d", table, f"path LIKE ?{excl('path')}", dd + "/%", *np_)
            for table in ("model_record_bundle_members", "model_record_layer_facts", "model_record_dependencies"):
                add("discovery", "d", table, f"(bundle_id LIKE ? OR bundle_id LIKE ?){excl('bundle_id')}",
                    dd + "/%", dd + "::%", *np_)
        for table in ("discovery_feasibility_models", "discovery_feasibility_cells"):
            add("discovery", "d", table, "model_key=?", key)

        m.pop("nested_dirs", None)
        if records:
            found = rec["wrapper"] + rec["discovery"]
            return found[0] if found else {"table": records.partition(".")[2], "total": 0, "offset": offset, "rows": []}
        return {**m, "files": files, "records": rec, "sources": {"wrapper": WRAPPER_DB, "discovery": disc}}
    finally:
        conn.close()
