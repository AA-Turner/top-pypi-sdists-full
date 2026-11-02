"""Basic console response shapes backed by the unified Flask Core database.

These projections use the model dossier, call mirror and copy records already
maintained by Flask intake. A fresh installation needs no Basic database.
"""
from __future__ import annotations

import ipaddress
import os
import threading

from psycopg.rows import dict_row

from hugpy_core.imports.functions import core_dsn
from hugpy_core.models import modeldb


def _conn():
    import psycopg
    return psycopg.connect(core_dsn(), row_factory=dict_row, connect_timeout=5)


def _central(copies: list[dict]) -> dict | None:
    central = [copy for copy in copies if copy.get("location_kind") == "central"
               or (copy.get('details') or {}).get('storage_role') == 'central']
    if not central:
        return None
    return {"drives": sorted({_drive_for_path(copy.get("path")) for copy in central
                              if _drive_for_path(copy.get("path"))}),
            "bytes": sum(int(copy.get("bytes") or 0) for copy in central),
            "verified": all(bool(copy.get("verified")) for copy in central)}


# declared_drives() opens a Postgres connection per call; a catalog build asks
# for the same list once per central copy, so one request caches it here.
_REQUEST = threading.local()


def _drive_roots() -> list[str]:
    roots = getattr(_REQUEST, "roots", None)
    if roots is None:
        from hugpy_core.registry.drive_display import declared_drives
        roots = [d["path"] for d in declared_drives()]
        roots.append(os.environ.get("HUGPY_CENTRAL_MODELS_HOME", ""))
    return roots


def _drive_for_path(path: str | None) -> str:
    if not path:
        return ""
    roots = _drive_roots()
    return next((root for root in roots if root and
                 (path == root or path.startswith(root.rstrip("/") + "/"))), "")


def _catalog_row(priced: dict) -> dict:
    key = priced["model_key"]
    pairs = priced.get("workers") or []
    copies = priced.get("copies") or []
    quants = priced.get("quants") or []
    worker_names = sorted({copy['location_id'] for copy in copies
                           if copy.get('location_kind') == 'worker' and copy.get('location_id')
                           and (copy.get('details') or {}).get('storage_role') != 'central'})
    resident_on = sorted({pair["worker_id"] for pair in pairs
                          if isinstance(pair.get("live"), dict) and pair["live"].get("resident")})
    available = any(pair.get("assigned") or (pair.get("live") or {}).get("gpu_fit") is True
                    or any((v.get('inputs') or {}).get('feasibility',{}).get('admissible') is True
                           for v in pair.get('verdicts') or [])
                    for pair in pairs)
    # External endpoints have no managed placement/assignment row. Their
    # owning Wrapper still reports residency through the current inventory.
    external_workers = {copy.get("location_id") for copy in copies
                        if copy.get("location_kind") == "worker"
                        and (copy.get("details") or {}).get("external")}
    if external_workers:
        from hugpy_core.registry import registry
        for worker_id in external_workers:
            worker = registry.lookup_worker(worker_id)
            if not worker or not registry.is_online(worker):
                continue
            endpoint = (worker.get("models_discovered") or {}).get(key) or {}
            if endpoint.get("external") and endpoint.get("resident"):
                resident_on.append(worker_id)
                available = True
        resident_on = sorted(set(resident_on))
    chosen = max(quants, key=lambda q: int(q.get("size_bytes") or 0), default={})
    hub_id = priced.get("hub_id")
    marker = priced.get("metadata") or {}
    marker = marker if isinstance(marker, dict) else {}
    primary_task = priced.get("task") or marker.get("primary_task")
    marker_tasks = marker.get("tasks")
    marker_tasks = marker_tasks if isinstance(marker_tasks, list) else []
    tasks = list(dict.fromkeys([task for task in
                                [primary_task, *marker_tasks]
                                if isinstance(task, str) and task]))
    return {"id": key, "model_key": key, "object": "model",
            "aliases": priced.get("aliases") or [],
            **{field: marker[field] for field in
               ("adapter", "serveable", "unserveable_reason", "task_override") if field in marker},
            "name": hub_id.rsplit("/", 1)[-1] if hub_id else key,
            "framework": priced.get("framework"), "hub_id": hub_id,
            "primary_task": primary_task,
            "tasks": tasks,
            "moe_capable": bool(priced.get("moe_capable", marker.get("moe_capable"))),
            "bnb_capable": bool(priced.get("bnb_capable", marker.get("bnb_capable"))),
            "workers": worker_names, "worker_count": len(worker_names),
            "plan_workers": sorted({p['worker_id'] for p in pairs if p.get('worker_id')}),
            "resident": bool(resident_on), "resident_on": resident_on,
            "available": available, "quant_count": len(quants),
            "disk_quants": sorted({q.get("quant") for q in quants if q.get("quant")}),
            "hub_quants": [], "hub_quant_count": 0,
            "file": chosen.get("file"), "quant": chosen.get("quant"),
            "bytes": chosen.get("size_bytes"), "central": _central(copies),
            "calls": 0, "avg_tok_per_s": None, "last_call_at": None,
            "repo_url": "https://huggingface.co/" + hub_id if hub_id and "/" in hub_id else None}


def models(*, picker_facts=False) -> list[dict]:
    _REQUEST.roots = _drive_roots()      # one drive lookup for the whole catalog build
    try:
        return _models(picker_facts=picker_facts)
    finally:
        _REQUEST.roots = None


def _models(*, picker_facts=False) -> list[dict]:
    result = []
    offset = 0
    while True:
        batch = modeldb.fetch_rows(limit=1000, offset=offset, include_evidence=False)
        for row in batch:
            item = _catalog_row(row)
            if picker_facts:
                item['status'] = 'installed' if item.get('central') else None
                item['archived'] = (row.get('metadata') or {}).get('archive')
                item['model_max_length'] = row.get('ctx_train') or row.get('max_ctx')
                item['_modelDatabase'] = {'workers':[
                    {**{k:p.get(k) for k in ('worker_id','fits','live','plan')},
                     'verdicts':[{'fits':v.get('fits'), 'modes':v.get('modes')} for v in p.get('verdicts') or []]}
                    for p in row.get('workers') or []]}
            result.append(item)
        if len(batch) < 1000:
            break
        offset += len(batch)
    with _conn() as conn:
        usage = conn.execute("SELECT model_name,count(*) AS calls,max(received_at) AS last_call_at "
                             "FROM call_log WHERE model_name IS NOT NULL GROUP BY model_name").fetchall()
    by_name = {row["model_name"]: row for row in usage}
    for row in result:
        if row["model_key"] in by_name:
            row["calls"] = by_name[row["model_key"]]["calls"]
            row["last_call_at"] = by_name[row["model_key"]]["last_call_at"]
    return result


def model(key: str) -> dict | None:
    priced = modeldb.fetch_rows(keys=[key])
    if not priced:
        return None
    priced = priced[0]
    row = _catalog_row(priced)
    row["metadata"] = priced.get("metadata") or {}
    workers = [{"worker": p["worker_id"], "model_key": key,
                "available": p.get("assigned") or (p.get("live") or {}).get("gpu_fit"),
                "resident": bool((p.get("live") or {}).get("resident")),
                "knobs": p.get("user_settings") or {}} for p in priced.get("workers") or []]
    quants = [{**q, "bytes": q.get("size_bytes"), "on_disk": False}
              for q in priced.get("quants") or []]
    with _conn() as conn:
        calls = conn.execute("SELECT * FROM call_log WHERE model_name=%s "
                             "ORDER BY received_at DESC LIMIT 50", (key,)).fetchall()
        metrics = conn.execute(
            "SELECT worker,count(*) AS calls,count(*) FILTER (WHERE call_state='done') AS done,"
            "count(*) FILTER (WHERE call_state='failed') AS failed,"
            "max(received_at) AS last_call_at,"
            "sum(prompt_tokens) AS prompt_tokens,sum(completion_tokens) AS completion_tokens "
            "FROM call_log WHERE model_name=%s GROUP BY worker ORDER BY worker", (key,)).fetchall()
        evictions = conn.execute(
            "SELECT * FROM evictions WHERE key=%s ORDER BY started_at DESC LIMIT 50", (key,)).fetchall()
    calls = [{field: str(value) if isinstance(value, (ipaddress.IPv4Address, ipaddress.IPv6Address))
              else value for field, value in call.items()} for call in calls]
    from hugpy_settings.imports.constants import KNOB_SCHEMA
    return {"model": row, "workers": workers, "quants": quants,
            "metrics": metrics, "calls": calls, "evictions": evictions,
            "knobs": KNOB_SCHEMA, "priced": priced}


def central_copies() -> list[dict]:
    with _conn() as conn:
        rows = conn.execute("SELECT model_key,path,bytes,verified "
                            "FROM model_copies WHERE present AND location_kind='central'").fetchall()
    return [{**row, "drive": _drive_for_path(row.get("path"))} for row in rows]


def operation(worker: str, action: str, payload: dict) -> None:
    from psycopg.types.json import Jsonb
    with _conn() as conn:
        conn.execute("INSERT INTO core_operations(worker,action,payload) VALUES (%s,%s,%s)",
                     (worker, action, Jsonb(payload)))
