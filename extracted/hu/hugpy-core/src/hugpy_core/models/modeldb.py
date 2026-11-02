"""The console's DATABASE RELAY over the hugpy_core DB.

Shapes and semantics LIFTED from legacy hugpy (instructions/hugpy/database and
services/hugpy_server .../llm_storage_routes.py + query_registry.py):

  GET  /models/database?q=&limit=                     rows with quants[] + workers[]
  POST /models/database/<key>/workers/<wid>/knobs     {set:{...}, unset:[...]}
  POST /models/database/<key>/workers/<wid>/assigned  {assigned, source?}
  POST /models/database/<key>/workers/<wid>/pinned    {pinned}
  POST /fleet/workers/<wid>/moe                         {model_key, value} | {all, value}

<key> is the model_key (the model's directory name); rows carry id == name ==
model_key so the console's name matching works unchanged.

Rules: an assigned pair appears in the worker roster; Pin makes its assignment
persistent and worker-specific; unpin leaves it transient until API restart;
unassign requires unpinning first; non-operator changes cannot alter pinned pairs;
``tuned_for`` is server-managed and never unset.
"""
from __future__ import annotations
from hugpy_core.imports import constants as _C
from hugpy_core.imports import functions as _F

import os
import json
import threading

from flask import has_request_context, request


DB = _F.core_dsn()


def _conn():
    import psycopg
    from psycopg.rows import dict_row
    return psycopg.connect(DB, row_factory=dict_row)


def forget_unpinned_assignments() -> int:
    """Discard transient worker allocations when the Core API starts again."""
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("UPDATE model_workers SET assigned=false, source='reload', updated_at=now() "
                    "WHERE assigned=true AND pinned=false")
        count = cur.rowcount
        conn.commit()
    return count


def discovery_quants(copies, measured=()):
    """Compile explicit discovery inventory without inventing measured facts."""
    import posixpath
    rows = {r['file']: dict(r) for r in measured if r.get('file')}
    for copy in copies:
        details = copy.get('details') or {}
        weights = details.get('weights') or []
        variants = details.get('variants')
        inventory = variants if isinstance(variants, list) and variants else weights
        for item in inventory:
            file = item.get('entry') or item.get('file')
            if not file or item.get('mmproj') or item.get('shard_of'):
                continue
            row = rows.setdefault(file, {'file': file, 'source': 'discovery.file_inventory'})
            if row.get('size_bytes') is None:
                row['size_bytes'] = item.get('bytes')
                row['bytes'] = item.get('bytes')
            for field in ('quant', 'members', 'complete'):
                if row.get(field) is None and item.get(field) is not None:
                    row[field] = item[field]
            row.setdefault('locations', []).append({
                'kind': copy.get('location_kind'), 'id': copy.get('location_id'),
                'path': posixpath.join(details.get('dir') or copy.get('path') or '', file),
                'observed_at': copy.get('observed_at'), 'source': 'model_copies.details'})
    return [rows[file] for file in sorted(rows)]


def fetch_rows(q: str = "", limit: int = 1000, keys: list[str] | None = None, *, include_evidence: bool = True, offset: int = 0) -> list:
    like = f"%{q}%" if q else "%"
    with _conn() as conn, conn.cursor() as cur:
        if keys is None:
            cur.execute("SELECT model_key FROM model_dossier_keys WHERE model_key ILIKE %s "
                        "OR model_key IN (SELECT model_key FROM model_key_aliases WHERE alias_key ILIKE %s) "
                        "ORDER BY model_key LIMIT %s OFFSET %s", (like, like, int(limit), max(0, int(offset))))
        else:
            cur.execute("SELECT model_key FROM model_dossier_keys WHERE model_key = ANY(%s) "
                        "OR model_key IN (SELECT model_key FROM model_key_aliases WHERE alias_key=ANY(%s)) "
                        "ORDER BY model_key", (keys, keys))
        keys = [r["model_key"] for r in cur.fetchall()]
        if not keys:
            return []
        cur.execute("SELECT model_key,alias_key FROM model_key_aliases WHERE model_key=ANY(%s)", (keys,))
        aliases = {}
        for r in cur.fetchall():
            aliases.setdefault(r['model_key'], []).append(r['alias_key'])
        cur.execute("SELECT * FROM model_quant_facts WHERE model_key = ANY(%s) ORDER BY file", (keys,))
        facts: dict = {}
        for r in cur.fetchall():
            r["bytes"] = r.get("size_bytes")
            facts.setdefault(r.pop("model_key"), []).append(r)
        cur.execute("SELECT * FROM model_worker_quants WHERE model_key = ANY(%s) ORDER BY file", (keys,))
        verdicts: dict = {}
        for r in cur.fetchall():
            verdicts.setdefault((r.pop("model_key"), r.pop("worker_id")), []).append(r)
        cur.execute("SELECT w.*,p.plan AS plan FROM model_workers w LEFT JOIN model_pair_plans p USING(model_key,worker_id) WHERE w.model_key = ANY(%s) ORDER BY w.worker_id", (keys,))
        workers: dict = {}
        for r in cur.fetchall():
            k = r.pop("model_key")
            r["verdicts"] = verdicts.get((k, r["worker_id"]), [])
            workers.setdefault(k, []).append(r)
        cur.execute("SELECT * FROM pair_live WHERE model_key = ANY(%s)", (keys,))
        live = {(r["model_key"], r["worker_id"]): r for r in cur.fetchall()}
        for key, pairs in workers.items():
            for pair in pairs:
                pair["live"] = live.get((key, pair["worker_id"]))
        relation = "models" if include_evidence else "model_census"
        columns = "model_key,hub_id,framework,primary_task,metadata"
        if include_evidence:
            columns += ",variables,source_refs,updated_at"
        cur.execute(f"SELECT {columns} FROM {relation} WHERE model_key = ANY(%s)", (keys,))
        census = {r["model_key"]: r for r in cur.fetchall()}
        # A canonical key can predate the classified central/workflow copy.
        # Retain explicit capability facts from every source key, including
        # the lightweight picker read which does not materialize dossiers.
        cur.execute("SELECT coalesce(a.model_key,c.model_key) AS model_key,c.hub_id,c.framework,"
                    "c.primary_task,c.metadata FROM model_census c "
                    "LEFT JOIN model_key_aliases a ON a.alias_key=c.model_key "
                    "WHERE coalesce(a.model_key,c.model_key)=ANY(%s) "
                    "UNION ALL SELECT coalesce(a.model_key,c.model_key),c.hub_id,c.framework,"
                    "c.primary_task,c.hugpy_json FROM central_models c "
                    "LEFT JOIN model_key_aliases a ON a.alias_key=c.model_key "
                    "WHERE NOT c.missing AND coalesce(a.model_key,c.model_key)=ANY(%s)", (keys,keys))
        for source in cur.fetchall():
            key = source['model_key']
            entry = census.setdefault(key, {})
            for field in ('hub_id','framework','primary_task'):
                if not entry.get(field) and source.get(field):
                    entry[field] = source[field]
            metadata = dict(entry.get('metadata') or {})
            extra = source.get('metadata') or {}
            if not isinstance(extra, dict):
                extra = {}
            tasks = [*(metadata.get('tasks') or []), *(extra.get('tasks') or [])]
            for task in (entry.get('primary_task'), source.get('primary_task')):
                if task:
                    tasks.append(task)
            if tasks:
                metadata['tasks'] = list(dict.fromkeys(t for t in tasks if isinstance(t,str)))
            for field in ('adapter','serveable','unserveable_reason','task_override'):
                if metadata.get(field) is None and extra.get(field) is not None:
                    metadata[field] = extra[field]
            entry['metadata'] = metadata
        cur.execute("SELECT coalesce(a.model_key,c.model_key) AS model_key,"
                    "c.location_kind,c.location_id,c.path,c.bytes,c.details,c.verified,c.observed_at "
                    "FROM model_copies c LEFT JOIN model_key_aliases a ON a.alias_key=c.model_key "
                    "WHERE c.present AND coalesce(a.model_key,c.model_key) = ANY(%s)", (keys,))
        copies: dict = {}
        for r in cur.fetchall():
            copies.setdefault(r.pop("model_key"), []).append(r)
        cur.execute("SELECT DISTINCT ON (model_key,suite,category,tier) "
                    "model_key,suite,category,tier,request_id,passed,at "
                    "FROM grades WHERE model_key = ANY(%s) AND passed IS NOT NULL "
                    "ORDER BY model_key,suite,category,tier,at DESC", (keys,))
        grade_refs: dict = {}
        for r in cur.fetchall():
            grade_refs.setdefault(r.pop("model_key"), []).append(r)
    rows = []
    for k in keys:
        facts[k] = discovery_quants(copies.get(k, []), facts.get(k, []))
        fw = "gguf" if any(str(f.get("file", "")).lower().endswith(".gguf") for f in facts.get(k, [])) else None
        entry = census.get(k) or {}
        identities = [{**(c.get('details') or {}).get('identity', {}),
                       'worker': c.get('location_id')} for c in copies.get(k, [])
                      if isinstance((c.get('details') or {}).get('identity'), dict)]
        variables = dict(entry.get('variables') or {})
        variables['discovery_identity'] = identities
        handles = sorted(set(aliases.get(k, []) + [h for i in identities for h in i.get('handles', [])]))
        rows.append({"id": k, "name": k, "model_key": k, 'aliases': handles,
                     "framework": entry.get("framework") or fw,
                     "hub_id": entry.get("hub_id"), "task": entry.get("primary_task"),
                     "metadata": entry.get("metadata") or {}, "copies": copies.get(k, []),
                     "grade_refs": grade_refs.get(k, []),
                     "variables": variables,
                     "source_refs": entry.get("source_refs") or [],
                     "catalog_updated_at": entry.get("updated_at"),
                     "quants": facts.get(k, []), "workers": workers.get(k, [])})
    return rows


def _pair(cur, key: str, wid: str) -> dict:
    cur.execute("INSERT INTO model_workers (model_key, worker_id) VALUES (%s,%s)"
                " ON CONFLICT DO NOTHING", (key, wid))
    cur.execute("SELECT * FROM model_workers WHERE model_key=%s AND worker_id=%s", (key, wid))
    return cur.fetchone()


def physical_pair_key(cur, key: str, wid: str) -> str:
    """Resolve an owner-qualified catalog key to this worker's proven copy key.

    A bare name alone is never proof: comfy/sd-turbo and stabilityai/sd-turbo
    coexist. Require both the discovered hub identity and the owner/repo path.
    If the worker has no matching copy yet, retain the catalog key for a future
    central pull.
    """
    cur.execute('SELECT model_key FROM model_key_aliases WHERE alias_key=%s', (key,))
    alias = cur.fetchone()
    if alias:
        return alias['model_key']
    if not key or "~" not in key:
        return key
    cur.execute(
        "SELECT COALESCE((SELECT hub_id FROM model_census WHERE model_key=%s), "
        "(SELECT hub_id FROM central_models WHERE model_key=%s)) AS hub_id",
        (key, key))
    row = cur.fetchone()
    hub_id = (row or {}).get("hub_id") or key.replace("~", "/", 1)
    if "/" not in hub_id or key.lower() != hub_id.replace("/", "~", 1).lower():
        return key
    cur.execute(
        "SELECT DISTINCT c.key FROM worker_model_copies c "
        "JOIN model_census m ON m.model_key=c.key "
        "WHERE c.worker=%s AND lower(m.hub_id)=lower(%s) "
        "AND right(lower(c.model_dir), length(%s))=%s",
        (wid, hub_id, "/" + hub_id.lower(), "/" + hub_id.lower()))
    matches = [r["key"] for r in cur.fetchall()]
    return matches[0] if len(matches) == 1 else key


_routing_ready = False
_routing_lock = threading.Lock()


def _ensure_worker_routing() -> None:
    """Persist the per-worker wildcard switch without relying on a local file."""
    global _routing_ready
    if _routing_ready:
        return
    with _routing_lock:
        if _routing_ready:
            return
        with _conn() as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS worker_routing ("
                         "worker_id text PRIMARY KEY, wildcard boolean NOT NULL DEFAULT true, "
                         "updated_at timestamptz NOT NULL DEFAULT now())")
        _routing_ready = True


def worker_routing_view(wid: str) -> tuple[bool, dict]:
    """(wildcard, {model_key: assigned}) for a worker's UI roster."""
    _ensure_worker_routing()
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT wildcard FROM worker_routing WHERE worker_id=%s", (wid,))
        row = cur.fetchone()
        wildcard = bool(row["wildcard"]) if row else True
        cur.execute("SELECT model_key, assigned, source FROM model_workers WHERE worker_id=%s", (wid,))
        # Planner/discovery rows default to assigned=false. Only the operator's
        # explicit false is an x/tombstone; all other false rows follow wildcard.
        pairs = {r["model_key"]: bool(r["assigned"]) for r in cur.fetchall()
                 if r["assigned"] or r["source"] == "operator"}
    return wildcard, pairs


def routing_snapshot(model_key: str) -> tuple[dict, dict]:
    """Explicit pair state and worker wildcard values, read once per pick."""
    _ensure_worker_routing()
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT worker_id, assigned, pinned, source FROM model_workers WHERE model_key=%s",
                    (model_key,))
        pairs = {r["worker_id"]: (bool(r["assigned"]), bool(r["pinned"]),
                                   not r["assigned"] and r["source"] == "operator")
                 for r in cur.fetchall()}
        cur.execute("SELECT worker_id, wildcard FROM worker_routing")
        wildcards = {r["worker_id"]: bool(r["wildcard"]) for r in cur.fetchall()}
    return pairs, wildcards


def record_routed_allocation(model_key: str, wid: str, source: str = "routing") -> bool:
    """Keep a selected route until restart, unless the operator excluded it.

    Routing, wildcard calls and probes may add temporary allocations. They
    never clear one or change its pin. Only an explicit operator unassign or
    the startup sweep removes an allocation.
    """
    with _conn() as conn, conn.cursor() as cur:
        key = physical_pair_key(cur, model_key, wid)
        cur.execute("INSERT INTO model_workers(model_key,worker_id) VALUES (%s,%s) "
                    "ON CONFLICT DO NOTHING", (key, wid))
        cur.execute("SELECT assigned, source FROM model_workers WHERE model_key=%s "
                    "AND worker_id=%s FOR UPDATE", (key, wid))
        row = cur.fetchone()
        if row["assigned"]:
            return True
        if row["source"] in ("operator", "operator-delete"):
            return False
        cur.execute("UPDATE model_workers SET assigned=true, source=%s, updated_at=now() "
                    "WHERE model_key=%s AND worker_id=%s", (source, key, wid))
        conn.commit()
    return True


def set_worker_wildcard(wid: str, enabled: bool) -> None:
    _ensure_worker_routing()
    with _conn() as conn:
        conn.execute("INSERT INTO worker_routing (worker_id, wildcard) VALUES (%s,%s) "
                     "ON CONFLICT (worker_id) DO UPDATE SET wildcard=EXCLUDED.wildcard, "
                     "updated_at=now()", (wid, enabled))


def get_knobs(key: str, wid: str) -> dict:
    """The pair's user_settings ({} when the pair has none)."""
    try:
        with _conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT user_settings FROM model_workers WHERE model_key=%s AND worker_id=%s",
                        (key, wid))
            r = cur.fetchone()
            return dict(r["user_settings"] or {}) if r else {}
    except Exception:  # noqa: BLE001 — knobs never block a call
        return {}


GiB = 2 ** 30


def host_constraints(wid: str) -> dict:
    """What this worker's wrapper must honour: the operator cap (bytes, None =
    physical) and the protected set (pairs with residency 'static')."""
    try:
        with _conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT gpu_limit, ram_limit FROM worker_budgets WHERE worker_id=%s", (wid,))
            b = cur.fetchone() or {}
            cur.execute("SELECT model_key FROM model_workers WHERE worker_id=%s"
                        " AND user_settings->>'residency' = 'static' ORDER BY model_key", (wid,))
            prot = [r["model_key"] for r in cur.fetchall()]
        return {"gpu_limit": b.get("gpu_limit"), "ram_limit": b.get("ram_limit"),
                "protected": prot}
    except Exception:  # noqa: BLE001 — constraints never break a heartbeat
        return {"gpu_limit": None, "ram_limit": None, "protected": []}


def worker_activations(wid: str) -> list:
    """Models the operator marked ACTIVATE for this worker that are still
    PENDING a pull (user_settings.activate.state == 'requested'). Carried on the
    register/heartbeat reply so the box pulls them from central (the worker
    skips any already on its disk, and flips state to 'pulling'/'done' as it
    progresses — so a model in flight or finished is no longer 'requested' and
    is not re-sent). Empty on any DB error — activation never breaks a beat."""
    try:
        with _conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT model_key FROM model_workers WHERE worker_id=%s"
                        " AND user_settings->'activate'->>'state' = 'requested'"
                        " ORDER BY model_key", (wid,))
            return [{"model_key": r["model_key"]} for r in cur.fetchall()]
    except Exception:  # noqa: BLE001 — activation never breaks a heartbeat
        return []


def record_activation(key: str, wid: str, state: str, *, done_bytes=None,
                      total_bytes=None, file=None, error=None) -> dict:
    """Write one ACTIVATE state/progress/result onto the pair's
    user_settings.activate (one table per model; the model_workers trigger
    fires fitevict_cache_core, which the box already LISTENs on — pushed, not
    polled). Returns the stored activate block."""
    from psycopg.types.json import Jsonb
    import datetime
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with _conn() as conn, conn.cursor() as cur:
        row = _pair(cur, key, wid)
        us = dict(row["user_settings"] or {})
        act = {"state": state, "at": now}
        if done_bytes is not None:
            act["done_bytes"] = int(done_bytes)
        if total_bytes is not None:
            act["total_bytes"] = int(total_bytes)
        if file is not None:
            act["file"] = file
        if error is not None:
            act["error"] = error
        us["activate"] = act
        cur.execute("UPDATE model_workers SET user_settings=%s, updated_at=now()"
                    " WHERE model_key=%s AND worker_id=%s", (Jsonb(us), key, wid))
        conn.commit()
    return act


def worker_view_extras(wid: str) -> dict:
    """UI fields from the DB: limits, measured swap capacity, and config maps."""
    try:
        with _conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT gpu_limit, ram_limit, swap_total, swap_free FROM worker_budgets WHERE worker_id=%s", (wid,))
            b = cur.fetchone() or {}
            cur.execute("SELECT model_key, user_settings, pinned FROM model_workers WHERE worker_id=%s",
                        (wid,))
            rows = cur.fetchall()
    except Exception:  # noqa: BLE001
        return {}
    limits = {}
    if b.get("gpu_limit"):
        limits["gpu_mem_gib"] = round(b["gpu_limit"] / GiB, 2)
    if b.get("ram_limit"):
        limits["ram_max_gib"] = round(b["ram_limit"] / GiB, 2)
    return {"limits": limits, "swap_total": b.get("swap_total"), "swap_free": b.get("swap_free"),
            "config": {"residency": {r["model_key"]: "static" for r in rows
                                     if (r["user_settings"] or {}).get("residency") == "static"},
                       "pinned": {r["model_key"]: True for r in rows if r["pinned"]}},
            # The EFFECTIVE pair knobs per model (the stored value else the Auto
            # default — ONE server-side source, functions.effective_pair_settings),
            # from the same read, so the console shows them without knowing the
            # defaults or recomputing (operator 2026-10-08 new pair settings).
            "pair_settings": {r["model_key"]: _F.effective_pair_settings(r["user_settings"])
                              for r in rows},
            # Per-(model, worker) operator block (worker_controls .../block): the
            # UI reads worker.blocked_models[model_key.lower()].{blocked, by}.
            "blocked_models": {r["model_key"].lower():
                               {"blocked": True,
                                "by": "operator" if (r["user_settings"] or {}).get("blocked")
                                      else "automatic-fit",
                                "reason": (r["user_settings"] or {}).get("auto_blocked")}
                               for r in rows if ((r["user_settings"] or {}).get("blocked")
                                                or (r["user_settings"] or {}).get("auto_blocked"))}}


def blocked_worker_ids(model_key: str) -> set:
    """Operator-blocked pairs, including equivalent model-key aliases.

    A DB failure must not silently re-enable a blocked route. The picker already
    needs the DB for its allocation snapshot, so propagating the failure is the
    safe and honest outcome.
    """
    from hugpy_core.models.keys import model_key_forms, serveable_match
    wanted = model_key_forms(model_key)
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT model_key, worker_id FROM model_workers WHERE user_settings ? 'blocked' "
                    "OR user_settings ? 'auto_blocked'")
        return {r["worker_id"] for r in cur.fetchall()
                if serveable_match(model_key, wanted, [r["model_key"]])}


def _mode_bytes(mem: dict, mode: str) -> dict:
    """{gpu_bytes, ram_bytes} for one mode out of a verdict's memory table."""
    from hugpy_core.intake.schema import cell as _cell
    cell = _cell(mem, mode) or {}
    return {"gpu_bytes": cell.get("gpu_bytes"), "ram_bytes": cell.get("ram_bytes")}


def moe_disable_allowed(cur, key: str, wid: str) -> tuple[bool, str | None]:
    """A MoE split cannot be forced off when it is the pair's only feasible
    representation. Read the already-computed verdict; never re-price here."""
    cur.execute("SELECT user_settings,plan FROM model_workers WHERE model_key=%s AND worker_id=%s",
                (key, wid))
    pair = cur.fetchone() or {}
    settings = pair.get("user_settings") or {}
    preferred = str(settings.get("gguf_file") or (pair.get("plan") or {}).get("default_variant") or "").split("/")[-1]
    cur.execute("SELECT file,memory,auto,moe_offered FROM model_worker_quants "
                "WHERE model_key=%s AND worker_id=%s ORDER BY file", (key, wid))
    rows = cur.fetchall()
    row = next((r for r in rows if r["file"] == preferred), rows[0] if rows else None)
    if not row or not row.get("moe_offered"):
        return True, None
    memory = row.get("memory") or {}
    standard_table = (memory.get("bnb_4bit") or {}) if settings.get("bnb_4bit") else memory
    from hugpy_core.intake.schema import cell
    standard_fit = any((cell(standard_table, mode) or {}).get("fits") is not False
                       for mode in ("gpu-only", "ram-only", "max-gpu", "max-ram"))
    split_fit = (cell(memory, "explicit") or {}).get("fits") is True
    if split_fit and not standard_fit:
        return False, "the MoE split is the only feasible option on this worker"
    return True, None


def bnb_enable_allowed(cur, key: str, wid: str) -> tuple[bool, str | None]:
    cur.execute("SELECT user_settings,plan FROM model_workers WHERE model_key=%s AND worker_id=%s",
                (key, wid))
    pair = cur.fetchone() or {}
    settings = pair.get("user_settings") or {}
    preferred = str(settings.get("gguf_file") or (pair.get("plan") or {}).get("default_variant") or "").split("/")[-1]
    cur.execute("SELECT file,memory FROM model_worker_quants WHERE model_key=%s AND worker_id=%s ORDER BY file",
                (key, wid))
    rows = cur.fetchall()
    row = next((r for r in rows if r["file"] == preferred), rows[0] if rows else None)
    table = (row or {}).get("memory") or {}
    cells = table.get("bnb_4bit") or {}
    # Missing or partial Discovery detail is not a failed placement.
    assessed = [cell for cell in cells.values() if isinstance(cell, dict)]
    if assessed and all(cell.get("fits") is False for cell in assessed):
        return False, "the recorded bitsandbytes 4-bit estimates exceed this worker's capacity"
    return True, None


def _moe_display(cur, key: str, wid: str) -> "dict | None":
    """The toggled pair's size figures from the stored verdict (model_worker_quants):
    the standard auto mode's GPU/RAM bytes and the MoE split's (memory['explicit'],
    which the console shows when the split is on). Picks the pair's elected quant
    (plan.default_variant) else the first verdict. None when there is no verdict."""
    cur.execute("SELECT plan FROM model_workers WHERE model_key=%s AND worker_id=%s", (key, wid))
    pr = cur.fetchone()
    want = str(((pr or {}).get("plan") or {}).get("default_variant") or "").split("/")[-1]
    cur.execute("SELECT file, memory, auto, moe_offered FROM model_worker_quants"
                " WHERE model_key=%s AND worker_id=%s ORDER BY file", (key, wid))
    rows = cur.fetchall()
    if not rows:
        return None
    r = next((x for x in rows if x["file"] == want), rows[0])
    mem = r["memory"] or {}
    auto = r["auto"] or {}
    std_mode = ((auto.get("standard") or {}).get("mode")) or None
    return {"model_key": key, "worker_id": wid, "file": r["file"],
            "moe_offered": bool(r["moe_offered"]),
            "standard_mode": std_mode,
            "standard": _mode_bytes(mem, std_mode) if std_mode else None,
            "split": _mode_bytes(mem, "explicit")}


def worker_alloc_modes(wid: str) -> dict:
    """{model_key: pinned alloc_mode | 'auto'} for this worker — the operator's
    placement PIN per (model, worker) from model_workers.user_settings.alloc_mode,
    'auto' when the pair carries no pin (blank = GPU-only → RAM-only → split, the
    ruling default). This is what the console's Alloc control shows; the last
    ACTUAL decided mode is reported separately as model_placements."""
    try:
        with _conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT model_key, user_settings FROM model_workers WHERE worker_id=%s", (wid,))
            rows = cur.fetchall()
    except Exception:  # noqa: BLE001 — never block a worker list
        return {}
    out = {}
    for r in rows:
        am = (r["user_settings"] or {}).get("alloc_mode")
        out[r["model_key"]] = am if am else "auto"
    return out


# ── console database RELAY + worker-write handlers ──────────────────────────────
# Plain kwargs-in / JSON-able-out views for models_bp (abstract_flask
# register_categories): key/wid arrive as path params or body fields, merged by
# the registrar. Lifted here from models/routes.py so the relay has one source.
def models_database(q="", limit=200, view="", keys=""):
    try:
        limit = max(1, min(int(limit), 1000))
    except (ValueError, TypeError):
        limit = 200
    # The console sends repeated ?key=... parameters for its visible rows.
    # The route adapter supplies scalar kwargs, so read the multi-value query
    # here to keep the requested batch instead of returning the first 200 keys.
    selected_keys = request.args.getlist("key") if has_request_context() else []
    if keys:
        import json
        try:
            packed = json.loads(keys) if isinstance(keys, str) else keys
            if not isinstance(packed, list):
                return {"source": "models", "rows": [], "error": "keys must be a list of at most 50 strings"}
            selected_keys.extend(packed)
        except (ValueError, TypeError):
            return {"source": "models", "rows": [], "error": "invalid keys JSON"}
    if len(selected_keys) > 50 or any(not isinstance(key, str) or not key for key in selected_keys):
        return {"source": "models", "rows": [], "error": "keys must be a list of at most 50 strings"}
    rows = fetch_rows(q or "", limit, selected_keys or None,
                              include_evidence=view not in ("summary", "pair"))
    from hugpy_core.registry import central_store, registry
    central_rows = central_store.rows(include_missing=True)
    central_aliases = {}
    repo_counts = {}
    for c in central_rows:
        repo_counts[c.get("repo")] = repo_counts.get(c.get("repo"), 0) + 1
    for c in central_rows:
        owner_repo = f"{c.get('owner')}/{c.get('repo')}" if c.get("owner") else None
        aliases = {c.get("model_key"), c.get("hub_id"), owner_repo,
                   owner_repo.replace("/", "~") if owner_repo else None}
        if repo_counts.get(c.get("repo")) == 1:
            aliases.add(c.get("repo"))
        for alias in aliases:
            if alias:
                central_aliases.setdefault(alias, c)
    discovered = {}
    for worker in registry.all_workers():
        for key, item in (worker.get("models_discovered") or {}).items():
            discovered.setdefault(key, []).append(item.get("hugpy_json") or {})
    for row in rows:
        key = row["model_key"]
        metadata = dict(row.get("metadata") or {})
        central_row = central_aliases.get(key) or central_aliases.get(row.get("hub_id"))
        source = (central_row or {}).get("hugpy_json") or {}
        same_central = bool(central_row and (not row.get("hub_id") or
                            not central_row.get("hub_id") or central_row.get("hub_id") == row.get("hub_id")))
        if central_row:
            row["central_canonical_key"] = central_row.get("model_key")
            row["hub_id"] = row.get("hub_id") or central_row.get("hub_id")
            row["framework"] = row.get("framework") or central_row.get("framework")
            row["size_bytes"] = row.get("size_bytes") or central_row.get("bytes")
            row["ctx_train"] = source.get("ctx_train") or source.get("context_length") or row.get("ctx_train")
            # Keep the full central record in the compiled dossier, with provenance.
            variables = row.setdefault("variables", {})
            variables["central_models"] = [central_row]
            row.setdefault("source_refs", []).append({
                "source_table": "central_models",
                "source_key": {"model_key": central_row.get("model_key"), "dir": central_row.get("dir")}})
            copies = row.setdefault("copies", [])
            if not any(c.get("location_kind") == "central" for c in copies):
                from hugpy_core.registry.central_store import store_id
                copies.append({"model_key": key, "location_kind": "central", "location_id": store_id(),
                               "path": central_row.get("dir"), "bytes": central_row.get("bytes"),
                               "present": not central_row.get("missing"), "verified": False})
        if same_central:
            metadata.update({k: source[k] for k in ("moe_capable", "bnb_capable") if k in source})
        if not row.get("ctx_train"):
            contexts = [int((v.get("inputs") or {}).get("ctx_train") or 0)
                        for pair in (row.get("workers") or [])
                        for v in (pair.get("verdicts") or [])]
            if contexts:
                row["ctx_train"] = max(contexts)
        if any(f.get("is_moe") for f in (row.get("quants") or [])):
            metadata["moe_capable"] = True
        for marker in discovered.get(key, []):
            metadata["moe_capable"] = bool(metadata.get("moe_capable")) or bool(marker.get("moe_capable"))
            if not (same_central and "bnb_capable" in source):
                metadata["bnb_capable"] = bool(metadata.get("bnb_capable")) or bool(marker.get("bnb_capable"))
        row["metadata"] = metadata
        row["moe_capable"] = bool(metadata.get("moe_capable"))
        row["bnb_capable"] = bool(metadata.get("bnb_capable"))
    if view == "summary":
        rows = [{**row, "quant_count": len(row.get("quants") or []),
                 "bytes": max([int(f.get("size_bytes") or 0) for f in (row.get("quants") or [])]
                              + [int(c.get("bytes") or 0) for c in (row.get("copies") or [])], default=0),
                 "central": any(c.get("location_kind") == "central" for c in (row.get("copies") or [])),
                 "quants": [], "grade_refs": [], "copies": [],
                 "workers": [{"worker_id": pair["worker_id"], "assigned": pair.get("assigned"),
                              "pinned": pair.get("pinned"), "user_settings": pair.get("user_settings") or {},
                              "live": pair.get("live")}
                             for pair in row["workers"]]} for row in rows]
    return {"source": "models", "rows": rows}


def model_discover(key=None, **_):
    """Return the current stored facts/verdict summary for one model.

    The independent intake already refreshes worker inventories; this endpoint
    must not perform a filesystem walk or require hugpy_storage just to render
    the console's targeted-discovery result.
    """
    import time
    started = time.monotonic()
    rows = fetch_rows(str(key or ""), 1000)
    row = next((r for r in rows if r.get("model_key") == key), None)
    if row is None:
        return {"facts": {}, "workers": {}, "took_s": round(time.monotonic() - started, 2),
                "error": f"no model facts found for {key}"}
    facts = {}
    for fact in row.get("quants") or []:
        name = fact.get("file") or fact.get("name") or "unknown"
        facts[name] = {"shards": int(fact.get("shards") or 1),
                       "is_moe": bool(fact.get("is_moe") or (fact.get("predict") or {}).get("is_moe"))}
    workers = {}
    for worker in row.get("workers") or []:
        wid = worker.get("worker_id")
        verdicts = worker.get("verdicts") or []
        workers[wid] = {"verdicts": len(verdicts),
                        "fits": any(bool(v.get("fits")) for v in verdicts if isinstance(v, dict)),
                        "explicit_band": any(bool(v.get("explicit_band")) for v in verdicts if isinstance(v, dict)),
                        "moe_offered": any(bool(v.get("moe_offered")) for v in verdicts if isinstance(v, dict))}
    return {"facts": facts, "workers": workers, "took_s": round(time.monotonic() - started, 2)}


def pair_knobs(key=None, wid=None, **body):
    """Send edited knobs to the wrapper; return only its read-back values."""
    sets_in = body.get("set", {})
    unset_in = body.get("unset", [])
    if not isinstance(sets_in, dict) or not isinstance(unset_in, list) or not all(isinstance(u, str) for u in unset_in):
        return {"ok": False, "error": "body is {set:{...}, unset:[...]}"}, 400
    sets = {_C.PAIR_KNOB_RENAMES.get(k, k): v for k, v in sets_in.items()}
    if set(sets) & set(unset_in):
        return {"ok": False, "error": "a knob cannot be set and unset together"}, 400
    unset = [_C.PAIR_KNOB_RENAMES.get(u, u) for u in unset_in if u != "tuned_for"]
    with _conn() as conn, conn.cursor() as cur:
        key = physical_pair_key(cur, key, wid)
        _pair(cur, key, wid)
    try:
        from hugpy_core.intake.wrapper_settings import command, apply_confirmed_pair
        report = command(wid, key, sets, unset)
    except Exception as exc:
        return {"ok": False, "error": f"Wrapper change was not confirmed: {exc}"}, 502
    # The readback is an observation from the owning wrapper. Mirror it before
    # the UI refetches, rather than waiting for the next telemetry batch. The
    # existing model_workers trigger also wakes the model-row event stream.
    with _conn() as conn:
        apply_confirmed_pair(conn, wid, key, report["settings"])
    # The saved knob is confirmed before repricing. Refresh the owning Wrapper's
    # plan asynchronously; no inference or resident reload happens in this path.
    # Ordinary collector refreshes can skip unchanged hardware for up to 60s.
    import threading
    def refresh_plan():
        try:
            from hugpy_core.registry import registry
            from hugpy_core.brain.wrapper_verdicts import refresh
            worker = registry.lookup_worker(wid)
            if worker:
                refresh(worker, force=True)
        except Exception:
            import logging
            logging.getLogger(__name__).exception('Plan refresh after knob save failed for %s/%s', wid, key)
    threading.Thread(target=refresh_plan, name='knob-plan-refresh', daemon=True).start()
    return {"ok": True, "model_key": key, "worker_id": wid,
            "user_settings": report["settings"],
            "effective_settings": report.get("effective") or report["settings"],
            "source": "wrapper", "confirmation": report.get("confirmation")}


def pair_assigned(key=None, wid=None, assigned=False, source=None):
    assigned = bool(assigned)
    source = source or "operator"
    with _conn() as conn, conn.cursor() as cur:
        key = physical_pair_key(cur, key, wid)
        row = _pair(cur, key, wid)
        if row["pinned"] and (source != "operator" or not assigned):
            return {"ok": False, "error": "pair is pinned by the operator; unpin before unassigning"}
        if assigned:
            cur.execute("UPDATE model_workers SET assigned=true, source=%s, updated_at=now()"
                        " WHERE model_key=%s AND worker_id=%s", (source, key, wid))
        else:   # unassign clears the pin
            cur.execute("UPDATE model_workers SET assigned=false, pinned=false, pinned_by=NULL,"
                        " pinned_at=NULL, source=%s, updated_at=now()"
                        " WHERE model_key=%s AND worker_id=%s", (source, key, wid))
        conn.commit()
    from hugpy_core.registry import registry
    registry._bump()
    return {"ok": True, "model_key": key, "worker_id": wid, "assigned": assigned}


def pair_pinned(key=None, wid=None, pinned=False):
    import datetime
    pinned = bool(pinned)
    with _conn() as conn, conn.cursor() as cur:
        key = physical_pair_key(cur, key, wid)
        row = _pair(cur, key, wid)
        if pinned and not row["assigned"]:
            return {"ok": False, "error": "pin requires a model already assigned to this worker"}
        if pinned:
            # Pin changes permanence and routing contract for an existing
            # assignment; the roster/assignment action owns assigned=true.
            cur.execute("UPDATE model_workers SET pinned=true,pinned_by='operator',pinned_at=%s,updated_at=now() "
                        "WHERE model_key=%s AND worker_id=%s",
                        (datetime.datetime.now(datetime.timezone.utc), key, wid))
        else:
            # Unpin removes durability, not the active assignment.
            cur.execute("UPDATE model_workers SET pinned=false,pinned_by=NULL,pinned_at=NULL,updated_at=now() "
                        "WHERE model_key=%s AND worker_id=%s", (key, wid))
        conn.commit()
    from hugpy_core.registry import registry
    registry._bump()
    return {"ok": True, "model_key": key, "worker_id": wid, "pinned": pinned}


def pair_activate(key=None, wid=None, activate=True):
    """ACTIVATE: the operator pre-pulls a central model onto this box.
    {activate:true} records the intent; {activate:false} cancels a pending one."""
    activate = bool(activate)
    with _conn() as conn, conn.cursor() as cur:
        key = physical_pair_key(cur, key, wid)
    if activate:
        act = record_activation(key, wid, "requested")
        return {"ok": True, "model_key": key, "worker_id": wid, "activate": act}
    from psycopg.types.json import Jsonb
    with _conn() as conn, conn.cursor() as cur:
        row = _pair(cur, key, wid)
        us = dict(row["user_settings"] or {})
        us.pop("activate", None)
        cur.execute("UPDATE model_workers SET user_settings=%s, updated_at=now()"
                    " WHERE model_key=%s AND worker_id=%s", (Jsonb(us), key, wid))
        conn.commit()
    return {"ok": True, "model_key": key, "worker_id": wid, "activate": None}


def worker_activation_report(wid=None, model_key=None, state=None, done_bytes=None,
                             total_bytes=None, file=None, error=None):
    """The box pings ACTIVATE progress here as it pulls. The OUTCOME is the
    pull call-log row (task 'central-pull'), not the box's self-report."""
    key = model_key
    if not key or state not in ("pulling", "done", "absent", "error"):
        return {"ok": False,
                "error": "body is {model_key, state in pulling|done|absent|error, ...}"}
    from hugpy_core.calllog import calllog
    from hugpy_core.registry import registry
    wname = (registry.lookup_worker(wid) or {}).get("name")
    pull = calllog.central_pulls(key, wname) if wname else None
    act = record_activation(key, wid, (pull or {}).get("state", state),
                                    done_bytes=done_bytes, total_bytes=total_bytes, file=file,
                                    error=pull.get("error") if pull is not None else error)
    return {"ok": True, "model_key": key, "worker_id": wid, "activate": act,
            "pull_request_id": (pull or {}).get("request_id")}


def worker_limits(wid=None, **body):
    """Operator resource limits {"limits": {"gpu_mem_gib", "ram_max_gib"}}; {}
    clears. Clamped to the box's physical totals."""
    from hugpy_core.brain import planner
    from hugpy_core.registry import registry
    lim = body.get("limits", body) if isinstance(body.get("limits", body), dict) else {}
    w = registry.lookup_worker(wid)
    if w is None:
        return {"ok": False, "error": f"no worker {wid!r}"}
    gpus = w.get("gpus") or []
    gpu_total = sum(int(g.get("memory_total") or 0) for g in gpus) or None
    ram_total = int(w.get("ram_total") or 0) or None

    def gib(name, cap):
        v = lim.get(name)
        if v in (None, "", 0):
            return None
        try:
            b = int(float(v) * GiB)
        except (TypeError, ValueError):
            raise ValueError(f"{name} must be a number of GiB")
        if b <= 0:
            raise ValueError(f"{name} must be > 0")
        return min(b, cap) if cap else b
    try:
        gpu_limit, ram_limit = gib("gpu_mem_gib", gpu_total), gib("ram_max_gib", ram_total)
    except ValueError as exc:
        return {"ok": False, "error": str(exc)}
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("INSERT INTO worker_budgets (worker_id, name) VALUES (%s,%s)"
                    " ON CONFLICT DO NOTHING", (wid, w.get("name")))
        cur.execute("UPDATE worker_budgets SET gpu_limit=%s, ram_limit=%s, observed_at=now()"
                    " WHERE worker_id=%s", (gpu_limit, ram_limit, wid))
        conn.commit()
    planner.invalidate(wid)
    return {"ok": True, "worker_id": wid, **worker_view_extras(wid)}


def worker_config(wid=None, residency=None):
    """Forward each residency edit to the owning wrapper."""
    if not isinstance(residency, dict):
        return {"ok": False, "error": "residency must be an object"}, 400
    applied = []
    for key, mode in residency.items():
        result = pair_knobs(key, wid, **({"set": {"residency": "static"}} if mode == "static" else {"unset": ["residency"]}))
        if isinstance(result, tuple):
            return {**result[0], "confirmed_models": applied}, result[1]
        applied.append(key)
    return {"ok": True, "worker_id": wid, "confirmed_models": applied, "source": "wrapper"}


def worker_moe(wid=None, **body):
    """Forward MoE preferences through the same wrapper knob command."""
    raw = body.get("value", body.get("enabled"))
    if raw is not None and not isinstance(raw, bool):
        return {"ok": False, "error": "value must be a boolean or null"}, 400
    value = True if raw else None
    if body.get("all"):
        with _conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT DISTINCT model_key FROM model_worker_quants WHERE worker_id=%s AND moe_offered", (wid,))
            keys = [r["model_key"] for r in cur.fetchall()]
    elif body.get("model_key"):
        keys = [body["model_key"]]
    else:
        return {"ok": False, "error": "model_key is required"}, 400
    applied, reports = [], {}
    for key in keys:
        placement = ['alloc_mode', 'attention_gpu_layers', 'experts_cpu_layers', 'explicit_spill',
                     'n_gpu_layers', 'n_cpu_moe', 'gpu_mem_gib', 'cpu_mem_gib', 'gpu_model_pct', 'leniency_pct', 'priority_device']
        sets = {'moe': True, 'bnb_4bit': False, 'alloc_mode': 'explicit', 'n_gpu_layers': -1,
                'explicit_spill': False} if value else {}
        result = pair_knobs(key, wid, set=sets,
                            unset=[k for k in (placement if value else ['moe', *placement]) if k not in sets])
        if isinstance(result, tuple):
            return {**result[0], "confirmed_models": applied}, result[1]
        applied.append(key)
        reports[key] = result
    return {"ok": True, "count": len(applied), "value": value, "source": "wrapper", "reports": reports}
