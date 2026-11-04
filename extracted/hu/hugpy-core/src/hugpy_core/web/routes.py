# The router's HTTP surface. Route shapes LIFTED from legacy hugpy (read-only):
#   POST /api/fleet/workers/register, /api/fleet/workers/<id>/heartbeat
#       <- py/services/hugpy_server/src/hugpy_server/app/routes/worker_routes.py:960,1443
#   GET /v1/models, POST /v1/chat/completions (stream + non-stream; chunk /
#   usage_chunk / [DONE] framing, non-stream assembly)
#       <- py/services/hugpy_server/src/hugpy_server/app/routes/v1_routes.py:281,654-938
# DROPPED: auth gates, admission, think splitting (fitevict already splits),
#   tools shim, status/diagnostic frames, capacity/overflow classification.
"""hugpy_core routes: the worker contract and the OpenAI /v1 surface.

Attached to two blueprints — bare and under /api — because workers call
{central}/api/fleet/workers/... while the UI's /api/* arrives prefix-stripped."""
from __future__ import annotations

import json
import logging
import os
import sys
import time
import uuid

from flask import Response, jsonify, request, stream_with_context

from abstract_flask import get_bp, register_categories, spec, merge_categories

from hugpy_core.brain import planner
from hugpy_core.registry import registry
from hugpy_core.relay.openai import completion_kwargs, finish_reason, openai_error, usage_block
from hugpy_core.relay.pick import NoWorker, pick, confirm_routed_allocation, requested_worker_name, requested_worker_names
from hugpy_core.relay.relay import WorkerHTTPError, worker_cancel, worker_payload, worker_stream

logger = logging.getLogger("hugpy_core")

# The worker installer (bootstrap.sh). Boxes install + update from PyPI.
WORKER_BOOTSTRAP = os.environ.get(
    "HUGPY_CORE_WORKER_BOOTSTRAP", os.path.join(os.path.dirname(__file__), "install.sh"))


def _client_ip() -> str:
    fwd = request.headers.get("X-Forwarded-For", "")
    return (fwd.split(",")[0].strip() if fwd else request.remote_addr) or ""


from hugpy_core.registry.releases import fleet_versions, _ver_key


def _update_hint() -> dict:
    """The update hint every register/heartbeat reply carries: the package
    versions each box converges to (pip, from PyPI)."""
    return {"required_packages": fleet_versions()}


def _add_bundle_version(reply: dict, body: dict) -> None:
    """Stamp the box's current secrets-bundle version onto a register/heartbeat
    reply when the beat carried its box credential (client_id + token). The box
    re-renders its env only when this value changes (secrets architecture). The
    field is simply absent when the beat carries no box creds or the toolserver
    cannot be reached — never faked."""
    from hugpy_core.config.settings import box_bundle_version
    bv = box_bundle_version(body.get("box_client_id"), body.get("box_token"))
    if bv is not None:
        reply["bundle_version"] = bv


def gpu_process_map() -> dict:
    """Per-worker, per-device GPU occupation from the mirrored ``gpu_state`` +
    ``residents`` tables (core's own DB — the one the intake feed writes). The
    row is byte-exact (``total = reserved + used + free``) and carries the full
    per-process split: ``processes`` {pid: bytes}, the pids that are this orbit's
    engines (``hugpy_pids``), the probe pids (``probe_pids``), and ``reserved``
    (the driver's immutable share). ``residents`` names the model each engine pid
    serves, joined here as ``pid_models`` {pid: {model_key, state}}.

    Returns ``{worker_name: {device: {...}}}``. Read ONCE per worker-list render
    and handed to :func:`ui_worker`. Tolerant: on any DB/connection failure it
    returns ``{}`` so the payload simply omits the breakdown (absence is
    explicit — the console falls back to the plain used/free bar)."""
    import psycopg
    from hugpy_core.imports.functions import core_dsn
    try:
        with psycopg.connect(core_dsn(), autocommit=True, connect_timeout=3) as c:
            gpu_rows = c.execute(
                "SELECT worker, device, total, reserved, used, free, usable, "
                "processes, hugpy_pids, probe_pids, reason, extract(epoch from at), "
                "to_jsonb(gpu_state)->'process_models' "
                "FROM gpu_state").fetchall()
            res_rows = c.execute(
                "SELECT worker, pid, key, state FROM residents WHERE pid IS NOT NULL").fetchall()
    except Exception as exc:  # noqa: BLE001 — the breakdown is display-only
        logger.warning("gpu_process_map: %s", exc)
        return {}
    pid_models: dict = {}
    for worker, pid, key, state in res_rows:
        pid_models.setdefault(worker, {})[str(int(pid))] = {"model_key": key, "state": state}
    out: dict = {}
    for (worker, device, total, reserved, used, free, usable,
         processes, hugpy_pids, probe_pids, reason, at, process_models) in gpu_rows:
        if isinstance(process_models, str):
            try:
                process_models = json.loads(process_models)
            except ValueError:
                process_models = {}
        named = dict(process_models or {})
        named.update(pid_models.get(worker, {}))
        out.setdefault(worker, {})[int(device)] = {
            "total": total, "reserved": reserved, "used": used, "free": free,
            "usable": usable,
            "processes": {str(k): int(v) for k, v in (processes or {}).items()},
            "hugpy_pids": [int(p) for p in (hugpy_pids or [])],
            "probe_pids": [int(p) for p in (probe_pids or [])],
            "pid_models": named,
            "reason": reason, "at": at,
        }
    return out


def ui_worker(w: dict, gpu_procs: dict | None = None, workers: list | None = None) -> dict:
    """A registry row in the shape the UI's worker screen reads.

    ``gpu_procs`` is the :func:`gpu_process_map` result and ``workers`` the
    :func:`registry.all_workers` list; when the caller renders a list of workers
    it reads each ONCE and passes it in (with shared presence, all_workers reads
    every persisted row). When omitted they are read here, so a lone call is
    still complete."""
    v = registry.public_view(w)
    from hugpy_core.web.resources import storage_view, unique_gpus
    v["storage_view"] = storage_view(w, registry.all_workers() if workers is None else workers)
    from hugpy_core.relay.admission import state_of
    v["admission"] = state_of(v.get("id") or "")
    gpus = [dict(g) for g in (v.get("gpus") or [])]
    # GPU occupation by process (console strip). Attach the mirrored gpu_state
    # row to each card, matched by device index, so the console can draw the
    # per-PID breakdown that sums byte-exact to the card total. Tolerant: when
    # no row is mirrored for a card, the card simply carries no ``gpu_state``.
    if gpus:
        if gpu_procs is None:
            gpu_procs = gpu_process_map()
        by_device = gpu_procs.get(v.get("name")) or {}
        for g in gpus:
            idx = g.get("index")
            if idx is None:
                continue
            gs = by_device.get(int(idx))
            if gs is not None:
                g["gpu_state"] = gs
                if g.get("memory_reserved") is None and gs.get("reserved") is not None:
                    g["memory_reserved"] = gs["reserved"]
    gpus = unique_gpus(gpus)
    cards = v.get('cards') or []
    for g in gpus:
        card = next((c for c in cards if
                     (c.get('uuid') == g.get('uuid') if c.get('uuid') and g.get('uuid')
                      else c.get('device') == g.get('index'))), None)
        if card is not None:
            g['card_ledger'] = card
    v["gpus"] = gpus
    v["vram_total"] = sum(int(g.get("memory_total") or 0) for g in gpus) or None
    v["vram_used"] = (sum(int(g.get("memory_total") or 0) - int(g.get("memory_free") or 0)
                          for g in gpus) if gpus else None)
    if v.get("ram_total") and v.get("free_ram") is not None:
        v["ram_used"] = int(v["ram_total"]) - int(v["free_ram"])
    disc = v.get("models_discovered") or {}
    allocs = [a for a in (v.get("allocations") or []) if isinstance(a, dict)]
    v["allocations"] = allocs
    # Residency/pin render only when config is present; fitevict has no
    # static-residency or pin concept, so every model is on-demand, unpinned.
    from hugpy_core.models.modeldb import worker_view_extras, worker_alloc_modes, worker_routing_view
    extras = worker_view_extras(v["id"])
    v["config"] = extras.get("config") or {"residency": {}, "pinned": {}}
    v["limits"] = extras.get("limits") or {}
    # Current swap snapshot persisted by the planner alongside physical budgets.
    # The same SwapFree value is used for anonymous-memory feasibility.
    v["swap_total"] = v.get("swap_total") if v.get("swap_total") is not None else extras.get("swap_total")
    v["swap_free"] = v.get("swap_free") if v.get("swap_free") is not None else extras.get("swap_free")
    # Effective pair knobs per model (stored value else Auto default): the console
    # shows auto_goal / quality_alternatives / cpu_floor_cores / max_wait_s /
    # ctx_restore and the ctx/alloc knobs without knowing the defaults (item 3).
    v["model_pair_settings"] = extras.get("pair_settings") or {}
    # Per-(model, worker) operator block (worker_controls .../block) and the wheel
    # version the Update button converges to (fleet_versions, from PyPI).
    v["blocked_models"] = extras.get("blocked_models") or {}
    package = "hugpy-worker" if v.get("pkg_version") else "hugpy-wrapper"
    v["required_pkg_version"] = fleet_versions().get(package)
    running = v.get('pkg_version') or v.get('wrapper_version')
    desired = v['required_pkg_version']
    v['version_ok'] = running == desired if running and desired else None
    if package == 'hugpy-wrapper':
        v['wrapper_update_available'] = bool(running and desired and _ver_key(desired) > _ver_key(running))
        from hugpy_core.registry.releases import release
        selected = release(version=desired) if desired else None
        if selected and selected.get('artifact') and running and _ver_key(running) < _ver_key('0.1.168'):
            v['wrapper_update_available'] = False
            v['wrapper_update_reason'] = 'Install the Wrapper 0.1.168 apt package when idle to enable staged updates.'
    # Allocation (console issue 2026-10-04): the operator's placement PIN per
    # (model, worker) — the pinned alloc_mode or "auto" (no pin = GPU-only →
    # RAM-only → split). "auto" means CLEAR, never max-gpu. Plus the last ACTUAL
    # decided mode per model from the call log, shown as a secondary label.
    v["model_alloc_modes"] = worker_alloc_modes(v["id"])
    from hugpy_core.web.console_routes import placements_by_worker
    v["model_placements"] = placements_by_worker(v.get("name"))
    # MoE: capability from each model's hugpy.json (legacy moe_capable reads the
    # same marker flag); effective = a running child with experts on CPU.
    # Only an engine with an expert split can honour the MoE tick: GGUF via
    # llama.cpp --n-cpu-moe. The transformers loader has no expert offload
    # (device_map=auto on the card, spill forbidden, or the CPU), so a
    # transformers MoE is never offered the tick (operator 2026-10-06: "MoE tick
    # stopped doing anything … alloc hasn't changed" — those were transformers).
    v["moe_capable"] = {k: True for k, d in disc.items()
                        if (d.get("hugpy_json") or {}).get("moe_capable")
                        and d.get("engine") != "transformers"}
    v["moe_effective"] = {a["model_key"]: True for a in allocs if a.get("n_cpu_moe")}
    # 4-bit (bitsandbytes nf4): offered for the pairs whose hugpy.json marks them
    # bnb_capable — the transformers ("dir") models the wrapper now prices with a
    # memory.bnb_4bit / auto.bnb_4bit verdict (so the Alloc/Memory cells re-derive
    # at ~30% of fp16). Same marker source as moe_capable above. GGUF carries its
    # own quantization and is never bnb_capable, so a GGUF-only box still gets {}.
    v["bnb_available"] = {k: True for k, d in disc.items()
                          if (d.get("hugpy_json") or {}).get("bnb_capable")}
    wildcard, pair_assignments = worker_routing_view(v["id"])
    v["wildcard"] = wildcard
    # The worker's model listbox is the assigned roster, not disk/runtime
    # inventory. Pair rows are the source of truth: unpinned assignments are
    # cleared on Core API restart, while pinned pairs remain listed.
    explicit_keys = {k for k, on in pair_assignments.items() if on}
    v["assigned_models"] = sorted(explicit_keys)
    v["models"] = sorted(explicit_keys)
    by_key = {a["model_key"]: a for a in allocs}
    v["loaded_detail"] = {k: {"model_bytes": d.get("bytes"), "quant": d.get("quant"),
                              "vram_bytes": (by_key.get(k) or {}).get("vram_bytes"),
                              "ram_resident_bytes": (by_key.get(k) or {}).get("rss_bytes"),
                              "ctx": (by_key.get(k) or {}).get("ctx"),
                              "file": d.get("file"), "path": d.get("path")}
                          for k, d in disc.items()}
    # The console reads these two maps for presence and a few marker facts; the
    # full entries (derivation evidence, manifests, per-tensor weights) stay in
    # the registry and the model database, so the roster stays light enough that
    # the worker screen renders without waiting on the whole model inventory.
    for field in ("models_central", "models_discovered"):
        if isinstance(v.get(field), dict):
            v[field] = {k: _roster_entry(e) for k, e in v[field].items()}
    return v


# Marker facts the console reads from a roster entry's hugpy_json.
ROSTER_MARKER_KEYS = ("framework", "primary_task", "tasks", "hub", "hub_id", "name", "filename",
                      "model_dir", "moe_capable", "bnb_capable", "needs_classification", "source",
                      "marker_schema")
# Entry fields that stay out of the roster (read them from the model database).
ROSTER_OMITTED_KEYS = ("weights",)


def _roster_entry(entry):
    """A roster model entry without its heavy evidence: hugpy_json keeps only
    ROSTER_MARKER_KEYS and ROSTER_OMITTED_KEYS are dropped."""
    if not isinstance(entry, dict):
        return entry
    slim = {k: val for k, val in entry.items() if k not in ROSTER_OMITTED_KEYS}
    marker = entry.get("hugpy_json")
    if isinstance(marker, dict):
        slim["hugpy_json"] = {k: marker[k] for k in ROSTER_MARKER_KEYS if k in marker}
    return slim


def catalog_rows(q: str = "", limit: int | None = None, offset: int = 0, *, compact: bool = False) -> list:
    """Build the Models repository from the census and model database.

    Census rows carry richer identity/copy metadata when worker observations
    have been persisted successfully.  The model database is the durable
    allocation/quant source, though, and must keep allocated models visible if
    that optional projection is empty or stale.
    """
    from hugpy_core.models.census import rows as census_rows
    from hugpy_core.models.modeldb import fetch_rows
    workers = {w["id"]: w for w in registry.all_workers()}
    try:
        if limit is None and not q and not offset:
            # Preserve the legacy complete catalog response for older callers.
            census_list = census_rows()
            page = fetch_rows(limit=1000, include_evidence=False)
            census = {entry["model_key"]: entry for entry in census_list}
            keys = sorted(set(census) | {entry["model_key"] for entry in page})
            database = {entry["model_key"]: entry for entry in page}
        else:
            # Page the durable key index first. It is the union of catalog,
            # worker, central, and observed model identities, so each page has
            # a stable global alphabetical order without materializing dossiers.
            page = fetch_rows(q=q, limit=limit or 1000, offset=offset, include_evidence=False)
            keys = [entry["model_key"] for entry in page]
            database = {entry["model_key"]: entry for entry in page}
            census = {entry["model_key"]: entry for entry in census_rows(keys)} if keys else {}
    except Exception:
        logger.exception("model database catalog read failed")
        keys, database, census = [], {}, {}
    from hugpy_core.registry import central_store
    from hugpy_core.registry.central_store import store_id
    central_id = store_id()
    # Central keys can be bare repo names while workers report owner~repo.
    # Join by the canonical Hub identity too, or the UI loses central presence
    # and the only known size for that model.
    central_rows = central_store.rows(include_missing=True, summary=compact)
    central_aliases = {}
    repo_counts = {}
    for row in central_rows:
        repo_counts[row.get("repo")] = repo_counts.get(row.get("repo"), 0) + 1
    for row in central_rows:
        owner_repo = f"{row.get('owner')}/{row.get('repo')}" if row.get("owner") else None
        forms = {row.get("model_key"), row.get("hub_id"), owner_repo,
                 owner_repo.replace("/", "~") if owner_repo else None}
        if repo_counts.get(row.get("repo")) == 1:
            forms.add(row.get("repo"))
        for form in forms:
            if form:
                central_aliases.setdefault(form, row)
    out = []
    from hugpy_core.registry.registrations import all as _saved_connections, is_connected as _is_connected
    try:
        connected_names = {c.get("name") for c in _saved_connections() if _is_connected(c)}
    except Exception:  # noqa: BLE001 — no registry: only Core's own scan counts as central
        connected_names = set()
    for key in keys:
        entry = census.get(key) or {}
        db_entry = database.get(key) or {}
        pairs = db_entry.get("workers") or []
        discoveries = [(wid, (worker.get("models_discovered") or {}).get(key) or {})
                       for wid, worker in workers.items()
                       if key in (worker.get("models_discovered") or {})]
        copies = entry.get("copies") or db_entry.get("copies") or []
        central_row = (central_aliases.get(key) or central_aliases.get(entry.get("hub_id"))
                       or central_aliases.get(db_entry.get("hub_id")))
        # CENTRAL is a drive role, not a place (operator 2026-10-23): a copy is central
        # when Core scanned it OR a connected worker reports it from a drive it gave
        # the central role. A disconnected / removed worker's copies do not count.
        centrals = [c for c in copies if c["location_kind"] == "central"
                    or (c["location_kind"] == "worker" and c.get("location_id") in connected_names
                        and ((c.get("details") or {}).get("storage_role") == "central"))]
        central = next((c for c in centrals if c["location_id"] == central_id), None)
        if central is None and central_row and not central_row.get("missing"):
            central = {"model_key": key, "location_kind": "central", "location_id": central_id,
                       "path": central_row.get("dir"), "bytes": central_row.get("bytes"),
                       "verified": False, "present": True}
            centrals.append(central)
            copies = [*copies, central]
        local = [c for c in copies if c["location_kind"] == "worker"]
        observed = (local[0].get("details") or {}) if local else (discoveries[0][1] if discoveries else {})
        marker = (entry.get("metadata") or db_entry.get("metadata") or observed.get("hugpy_json")
                  or (central_row or {}).get("hugpy_json") or {})
        marker = marker if isinstance(marker, dict) else {}
        tasks = marker.get("tasks") or []
        hub_meta = marker.get("hub_meta") or marker.get("hub") or {}
        hub_meta = hub_meta if isinstance(hub_meta, dict) else {}
        primary_task = (entry.get("primary_task") or db_entry.get("task") or marker.get("primary_task")
                        or marker.get("task_override") or (tasks[0] if tasks else None)
                        or hub_meta.get("pipeline_tag"))
        if not tasks and primary_task:
            tasks = [primary_task]
        worker_ids = {c["location_id"] for c in local}
        worker_ids.update(wid for wid, _ in discoveries)
        names = {wid: (workers.get(wid) or {}).get("name") or wid for wid in worker_ids}
        quant_facts = db_entry.get("quants") or []
        size = next((c.get("bytes") for c in copies if c.get("bytes")), None)
        size = size or (central_row or {}).get("bytes")
        size = size or next((d.get("bytes") for _, d in discoveries if d.get("bytes")), None)
        size = size or next((f.get("bytes") for f in quant_facts if f.get("bytes")), None)
        framework = (entry.get("framework") or db_entry.get("framework") or marker.get("framework")
                     or (central_row or {}).get("framework"))
        if not framework and any(str(f.get("file") or "").lower().endswith(".gguf") for f in quant_facts):
            framework = "gguf"
        out.append({"model_key": key, "name": key,
                    "hub_id": (entry.get("hub_id") or db_entry.get("hub_id") or marker.get("hub_id")
                               or (central_row or {}).get("hub_id")),
                    "framework": framework,
                    "task": primary_task, "primary_task": primary_task,
                    "tasks": tasks, "hugpy_json": marker or None,
                    "size_bytes": size,
                    "file": observed.get("path") or next((f.get("file") for f in quant_facts if f.get("file")), None),
                    "quant": observed.get("quant") or next((f.get("quant") for f in quant_facts if f.get("quant")), None),
                    "weights": observed.get("weights") or next((f.get("weights") for f in quant_facts if f.get("weights")), None),
                    "moe_capable": marker.get("moe_capable"), "bnb_capable": marker.get("bnb_capable"),
                    "hugpy_json_error": observed.get("hugpy_json_error"),
                    "status": "installed" if copies or discoveries or (central_row and not central_row.get("missing")) else "unknown",
                    "source": "census" if key in census else "modeldb",
                    "workers": sorted(names.values()),
                    "on_central": bool(centrals), "central_copies": centrals,
                    "central_key": key if central else None,
                    "central_dir": central.get("path") if central else None,
                    "central_canonical_key": (central_row or {}).get("model_key"),
                    "copies": copies, "quants": quant_facts,
                    "worker_assignments": pairs})
    return out


# ── core HTTP surface as pure functions (register_categories convention) ─────
# Input arrives as kwargs (JSON body / form / query, via get_request_datas);
# path params from the original rules (worker_id, request_id) are now kwargs.
# request is read only for headers/host (install.sh, _client_ip) — never for
# body input. Handlers return a Response (jsonify / Response) so the original
# bodies and status codes pass through register_route unchanged.

def _json(payload, status=200):
    r = jsonify(payload)
    r.status_code = status
    return r


def _openai(message, status, err_type="invalid_request_error"):
    """openai_error returns (Response, status); return the Response with that
    status set so register_route passes it through (a tuple would be re-wrapped)."""
    resp, code = openai_error(message, status, err_type)
    resp.status_code = code
    return resp


# The console chat panel's live worker handles, keyed by request_id (chat_stream
# registers; chat_cancel / the stream's finally clear).
_chat_workers: dict = {}


# ── the central store (central_store.py; sql/010) ────────────────────────────
def central_rescan(**kwargs):
    """Walk the central drive once and refresh central_models."""
    from hugpy_core.registry import central_store
    return jsonify({"ok": True, **central_store.rescan()})


def central_ingest(**kwargs):
    """A writer changed ONE dir on the central drive: {"dir": <path>}."""
    d = (kwargs.get("dir") or "").strip()
    if not d:
        return _json({"ok": False, "error": "dir is required"}, 400)
    from hugpy_core.registry import central_store
    try:
        return jsonify({"ok": True, **central_store.ingest(d)})
    except ValueError as exc:
        return _json({"ok": False, "error": str(exc)}, 400)


def central_models(**kwargs):
    from hugpy_core.registry import central_store
    rows = central_store.rows(include_missing=bool(kwargs.get("missing")))
    for r in rows:
        r.pop("hugpy_json", None)
    return jsonify({"root": central_store.root(), "count": len(rows), "models": rows})


# ── admission (the console's admit / block buttons) ──────────────────────────
def workers_admit(worker_id=None, **kwargs):
    """``worker_id`` was the path param (/fleet/workers/<worker_id>/admit); now a kwarg."""
    from hugpy_core.relay.admission import set_state
    w = registry.lookup_worker(worker_id)
    set_state((w or {}).get("id") or worker_id, "approved")
    return jsonify({"ok": True, "worker_id": worker_id, "admission": "approved"})


def workers_block(worker_id=None, **kwargs):
    """``worker_id`` was the path param (/fleet/workers/<worker_id>/block); now a kwarg."""
    from hugpy_core.relay.admission import set_state
    w = registry.lookup_worker(worker_id)
    set_state((w or {}).get("id") or worker_id, "blocked")
    return jsonify({"ok": True, "worker_id": worker_id, "admission": "blocked",
                    "note": "no longer routed to; admit to restore"})


# ── worker contract ─────────────────────────────────────────────────────────
def workers_register(**body):
    if not body.get("name"):
        return _json({"error": "Malformed worker registration body."}, 400)
    url = registry.resolve_worker_url(body.get("url"), body.get("port"), _client_ip())
    w = registry.register(body, url)
    planner.maybe_refresh(w)
    logger.info("registered %s (%s) at %s", w.get("name"), w["id"], url)
    from hugpy_core.models.modeldb import host_constraints, worker_activations
    reply = {**registry.public_view(w), "fitevict_limits": host_constraints(w["id"]),
             "activations": worker_activations(w["id"]), **_update_hint()}
    _add_bundle_version(reply, body)
    return jsonify(reply)


def workers_heartbeat(worker_id=None, **body):
    """``worker_id`` was the path param (/fleet/workers/<worker_id>/heartbeat); now a kwarg."""
    url = registry.resolve_worker_url(body.get("url"), body.get("port"), _client_ip())
    w = registry.heartbeat(worker_id, body, url)
    if w is not None:
        planner.maybe_refresh(w)
    if w is None:
        # The agent thinks it's registered but the router forgot it
        # (restart). 410 tells the agent to re-register.
        return _json({"error": f"no worker {worker_id!r} in the registry; re-register"}, 410)
    from hugpy_core.models.modeldb import host_constraints, worker_activations
    reply = {**registry.public_view(w), "fitevict_limits": host_constraints(w["id"]),
             "activations": worker_activations(w["id"]), **_update_hint()}
    _add_bundle_version(reply, body)
    return jsonify(reply)


def workers_list(**kwargs):
    gp = gpu_process_map()
    workers = registry.all_workers()
    return jsonify([ui_worker(w, gp, workers) for w in workers])


def snapshot_feeds() -> dict:
    """The console snapshot feeds (also consumed by console_routes.llm_events)."""
    gp = gpu_process_map()
    workers = registry.all_workers()
    from hugpy_core.web.console_routes import liveness_feed, queue_feed
    return {
        "workers": [ui_worker(w, gp, workers) for w in workers],
        "activity": __import__("hugpy_core.registry.live", fromlist=["gpu_feed"]).gpu_feed().get("activity", {}),
        "liveness": liveness_feed(),
        "queue": queue_feed(),
        "settings": {w.get("name") or w.get("id"): w["settings_report"]
                     for w in workers if isinstance(w.get("settings_report"), dict)},
        "slots": {"slots": [], "resources": {"used_bytes": 0, "total_bytes": 0}},
        "peers": [],
    }


def llm_snapshot(**kwargs):
    return jsonify({"feeds": snapshot_feeds()})


# The console chat panel's native stream (ChatPanel/chatStore.js): hugpy
# events, not OpenAI chunks — request, status{served_by,worker_*}, then the
# worker's own token/done/error events relayed as they arrive.
def chat_stream(**body):
    mk = body.get("model_key")
    if not mk:
        return _json({"error": "model_key is required"}, 400)
    from hugpy_core.calllog.call_record import current
    rid = (current() or {}).get("request_id") or str(body.get("request_id") or uuid.uuid4().hex)
    try:
        worker = pick(mk, pool=body.get("pool") or "",
                      pin=requested_worker_name(body.get("alloc")),
                      workers=requested_worker_names(body.get("alloc")))
    except NoWorker as exc:
        return _json({"error": str(exc)}, exc.status)
    from hugpy_core.brain.intent import stamp
    wp = worker_payload({**body, "request_id": rid, "task": body.get("task") or "chat",
                         "metadata": stamp(body.get("metadata"), body.get("intent"))}, worker)
    _chat_workers[rid] = worker

    def sse(d: dict) -> bytes:
        return f"data: {json.dumps(d, ensure_ascii=False)}\n\n".encode("utf-8")

    def gen():
        try:
            yield sse({"type": "request", "request_id": rid})
            yield sse({"type": "status", "stage": "dispatch", "served_by": "worker",
                       "worker_id": worker["id"], "worker_name": worker.get("name")})
            for ev in worker_stream(worker, wp):
                if ev.get("type") == "done":
                    confirm_routed_allocation(mk, worker, source="chat")
                yield sse({**ev, "request_id": rid})
        except Exception as exc:  # noqa: BLE001
            if current():
                current().update(error=str(exc), http_status=502)
            yield sse({"type": "error", "request_id": rid,
                       "message": f"{type(exc).__name__}: {exc}"})
        finally:
            _chat_workers.pop(rid, None)

    return Response(stream_with_context(gen()), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no",
                             "Connection": "keep-alive"})


def chat_cancel(request_id=None, **kwargs):
    """``request_id`` was the path param (/llm/chat/cancel/<request_id>); now a kwarg."""
    w = _chat_workers.get(request_id)
    if w is None:
        return _json({"cancelled": False, "reason": "unknown or finished request"}, 404)
    status, out = worker_cancel(w, request_id)
    return _json(out, status)


# Worker install (UI: curl -fsSL <origin>/api/fleet/workers/install.sh | bash).
# Shape LIFTED from worker_routes.py:855 workers_install_sh + _central_base_url
# (6730): serve the bootstrap with CENTRAL= set to this router's public origin.
# The script installs the box packages from PyPI. Registered directly on web_bp
# (the ``.sh`` suffix makes a dotted endpoint name register_categories rejects).
def workers_install_sh():
    import re
    import shlex
    try:
        with open(WORKER_BOOTSTRAP, "r", encoding="utf-8") as fh:
            script = fh.read()
    except OSError as exc:
        return Response(f"echo 'bootstrap unavailable: {exc}' >&2; exit 1\n",
                        mimetype="text/x-shellscript", status=503)
    proto = request.headers.get("X-Forwarded-Proto", request.scheme)
    host = request.headers.get("X-Forwarded-Host") or request.host
    origin = f"{proto}://{host}"
    if not re.fullmatch(r"https?://[A-Za-z0-9._:-]+", origin):
        return Response("invalid central origin\n", status=400, mimetype="text/plain")
    script = re.sub(r'^CENTRAL=.*$', 'CENTRAL=' + shlex.quote(origin),
                    script, count=1, flags=re.M)
    return Response(script, mimetype="text/x-shellscript")


def workers_packages(**kwargs):
    """The box package versions (bootstrap.sh installs exactly these)."""
    return jsonify(fleet_versions())


# LIFTED from v1_routes.py:962 auth_config. The UI probes this to decide
# "live console" vs the showroom demo (Auth/authConfig.ts). Only "open"
# (no login wall) is served: the external auth proxy is not part of the
# new build, and console.hugpy.ai is LAN/WG-only at nginx.
def auth_config(**kwargs):
    return jsonify({"mode": "open", "base": None})


def models_catalog(view=None, limit=None, offset=None, q=None, **kwargs):
    """The Models repository (/models). ``?view=console`` returns the compact
    rows; console callers may page through them with ``limit``/``offset``/``q``,
    while an omitted limit preserves the legacy complete response. The query
    fields arrive as kwargs; the answer is served BARE (response="native")."""
    # Browser pickers use the console catalog permission and capability facts.
    # Allocation dossiers and live agent-session probes are unnecessary here.
    if view == "picker":
        from hugpy_core.relay.inference_catalog import picker_models
        from hugpy_core.config.model_preferences import projection
        from hugpy_core.config.settings import task_bindings
        return jsonify({"object": "list", "data": picker_models(),
                        "model_preferences": projection(),
                        "defaults": task_bindings(surface=kwargs.get("surface", "media"))})
    from hugpy_core.web.console_catalog import console_catalog_rows
    if view == "console":
        if limit is None and offset is None and q is None:
            return console_catalog_rows(catalog_rows(compact=True))
        try:
            limit = max(1, min(int(limit if limit is not None else 1000), 1000))
            offset = max(0, int(offset if offset is not None else 0))
        except (TypeError, ValueError):
            return {"error": "limit and offset must be integers"}, 400
        rows = catalog_rows(q or "", limit, offset, compact=True)
        return console_catalog_rows(rows)
    return catalog_rows()


def models_delete(model_key):
    """Explicitly remove this central's downloaded archive copy.

    Registered directly on web_bp (keeps the ``<path:model_key>`` URL param; the
    original DELETE verb collapses to GET+POST). Worker copies are intentionally
    not deleted here."""
    # The convention moves <key>/<wid> into request data, while the shipped
    # console still sends `/models/database/<key>/workers/<wid>/<verb>`.
    # This single adapter handles that whole family before the broad legacy
    # `/models/<path:model_key>` route can mistake it for a central delete.
    if model_key.startswith('database/'):
        from hugpy_core.models import routes as model_routes
        tail = model_key[len('database/'):]
        if tail.endswith('/discover'):
            return jsonify(model_routes.model_discover(tail[:-len('/discover')]))
        marker = '/workers/'
        if marker in tail:
            key, suffix = tail.split(marker, 1)
            bits = suffix.split('/')
            if len(bits) == 2 and bits[1] in {'knobs', 'assigned', 'pinned', 'activate'}:
                wid, verb = bits
                body = request.get_json(silent=True) or {}
                fn = getattr(model_routes, f'pair_{verb}')
                return jsonify(fn(key=key, wid=wid, **body))
    from hugpy_core.registry import central_store
    try:
        return jsonify({"ok": True, **central_store.remove(model_key)})
    except LookupError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 404
    except ValueError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 409


# ── OpenAI surface ───────────────────────────────────────────────────────────
def v1_models(**kwargs):
    seen: dict = {}
    # The engine reads this endpoint as its live capability catalog. Preserve
    # the OpenAI model-list fields and attach Core's model dossier facts so
    # Media can resolve summarize/vision against this Core.
    try:
        from hugpy_core.web.native_fleet import models as fleet_models
        catalog = {row["model_key"]: row for row in fleet_models()}
        vision_keys = {key for key, row in catalog.items()
                       if "image-text-to-text" in (row.get("tasks") or [])}
    except Exception as exc:  # a DB outage must not hide routable model IDs
        logger.warning("v1 model capability catalog unavailable: %s", exc)
        catalog = {}
        vision_keys = set()
    # Pickers need the whole catalog, including cold central models. Worker
    # advertisements describe current placement, not catalog membership.
    aliases = {alias: key for key, row in catalog.items() for alias in row.get("aliases") or []}
    for key, row in catalog.items():
        seen[key] = {**row, "id": key, "object": "model", "created": 0,
                     "owned_by": "hugpy", "workers": [], "loaded_on": [],
                     "available": False}
    for w in registry.all_workers():
        if not registry.is_online(w):
            continue
        loaded = set(w.get("loaded_models") or [])
        for reported in set(w.get("models") or []) | loaded:
            k = aliases.get(reported, reported)
            m = seen.setdefault(k, {"id": k, "object": "model", "created": 0,
                                    "owned_by": "hugpy", "workers": [],
                                    "loaded_on": [], "available": True,
                                    **{field: catalog.get(k, {}).get(field)
                                       for field in ("name", "framework", "tasks", "primary_task",
                                                     "hub_id", "file", "task_override")}})
            if k in vision_keys and m.get("framework") == "gguf":
                m["tasks"] = list(dict.fromkeys([*(m.get("tasks") or []), "image-text-to-text"]))
            m["available"] = True
            if w.get("name") not in m["workers"]:
                m["workers"].append(w.get("name"))
            if reported in loaded and w.get("name") not in m["loaded_on"]:
                m["loaded_on"].append(w.get("name"))
    # the online named sessions, each callable as `session:<name>`
    try:
        from hugpy_core.web.agent_sessions import session_models
        for m in session_models():
            seen.setdefault(m["id"], m)
    except Exception as exc:  # the session registry must not hide the fleet's models
        logger.warning("v1 session models unavailable: %s", exc)
    from hugpy_core.config.model_preferences import projection
    return jsonify({"object": "list", "data": sorted(seen.values(), key=lambda m: m["id"]),
                    "model_preferences": projection()})


def v1_task_bindings(**kwargs):
    """Expose the operator's stored task defaults to standalone arms and UIs."""
    from hugpy_core.config.settings import task_bindings
    return jsonify({"defaults": task_bindings(surface="video" if kwargs.get("surface") == "video" else "media")})


def v1_chat(**payload):
    model = payload.get("model")
    if isinstance(model, str) and model.startswith("session:"):
        # a named session as a model: one turn in that session (agent_sessions)
        from hugpy_core.web.agent_sessions import session_chat
        return session_chat(payload)
    try:
        kw = completion_kwargs(payload)
    except ValueError as exc:
        return _openai(str(exc), 400)
    from hugpy_core.calllog.call_record import current
    if current():
        kw["request_id"] = current()["request_id"]
    try:
        if kw.get("model_key"):
            worker = pick(kw["model_key"], pool=payload.get("pool") or "",
                          pin=requested_worker_name(kw.get("alloc")),
                          workers=requested_worker_names(kw.get("alloc")))
        else:
            # no model named: central inference chooses (relay/central.py)
            from hugpy_core.relay.central import choose
            kw["model_key"], worker, chosen = choose(
                task=payload.get("task"), messages=kw.get("messages"),
                pool=payload.get("pool") or "", pin=requested_worker_name(kw.get("alloc")),
                workers=requested_worker_names(kw.get("alloc")))
            kw["metadata"] = {**(kw.get("metadata") or {}), "central_choice": {
                k: chosen[k] for k in ("task", "chosen_via", "model_key")}}
    except NoWorker as exc:
        return _openai(str(exc), exc.status)
    except ValueError as exc:
        return _openai(str(exc), 400)
    wp = worker_payload(kw, worker)
    model = kw["model_key"]
    completion_id = f"chatcmpl-{uuid.uuid4().hex}"
    created = int(time.time())
    served = {"worker": worker.get("name"), "worker_id": worker["id"],
              "request_id": kw["request_id"]}

    if payload.get("stream"):
        include_usage = bool((payload.get("stream_options") or {}).get("include_usage"))

        def chunk(delta: dict, finish=None, hugpy=None) -> bytes:
            body = {
                "id": completion_id,
                "object": "chat.completion.chunk",
                "created": created,
                "model": model,
                "choices": [{"index": 0, "delta": delta, "finish_reason": finish}],
            }
            if hugpy:
                body["hugpy"] = hugpy
            return ("data: " + json.dumps(body, ensure_ascii=False) + "\n\n").encode("utf-8")

        def usage_chunk(usage) -> bytes:
            return (
                "data: " + json.dumps({
                    "id": completion_id,
                    "object": "chat.completion.chunk",
                    "created": created,
                    "model": model,
                    "choices": [],
                    "usage": usage_block(usage),
                }, ensure_ascii=False) + "\n\n"
            ).encode("utf-8")

        def sse():
            usage = None
            yield chunk({"role": "assistant", "content": ""})
            try:
                for ev in worker_stream(worker, wp):
                    t = ev["type"]
                    if t == "token":
                        if ev["text"]:
                            yield chunk({"content": ev["text"]})
                    elif t == "done":
                        usage = ev.get("usage")
                        served["execution_request_id"] = ev.get("execution_request_id")
                        confirm_routed_allocation(model, worker, source="routing")
                        yield chunk({}, finish=finish_reason(ev["finish_reason"]), hugpy=served)
                    elif t == "error":
                        yield chunk({"content": f"\n[error: {ev['message']}]"}, finish="stop")
            except Exception as exc:  # noqa: BLE001
                logger.exception("v1 stream failed")
                if current():
                    current().update(error=str(exc), http_status=502)
                yield chunk({"content": f"\n[error: {exc}]"}, finish="stop")
            if include_usage:
                yield usage_chunk(usage)
            yield b"data: [DONE]\n\n"

        return Response(stream_with_context(sse()), mimetype="text/event-stream",
                        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no",
                                 "Connection": "keep-alive"})

    # non-streaming: drain the same event stream and assemble one body
    text_parts: list[str] = []
    finish = "stop"
    error_message = None
    usage = None
    timings = None
    completed = False
    try:
        for ev in worker_stream(worker, wp):
            t = ev["type"]
            if t == "token":
                text_parts.append(ev["text"])
            elif t == "done":
                finish = finish_reason(ev["finish_reason"])
                usage = ev.get("usage")
                timings = ev.get("timings")
                served["execution_request_id"] = ev.get("execution_request_id")
                completed = True
            elif t == "error":
                error_message = ev["message"]
    except WorkerHTTPError as exc:
        return _openai(str(exc), 503 if exc.status == 503 else 502, "api_error")
    except Exception as exc:  # noqa: BLE001
        logger.exception("v1 completion failed")
        return _openai(f"{type(exc).__name__}: {exc}", 502, "api_error")
    if completed:
        confirm_routed_allocation(model, worker, source="routing")
    if error_message and not text_parts:
        status = 404 if "not found" in error_message.lower() else 500
        return _openai(error_message, status, "api_error")
    result = {
        "id": completion_id,
        "object": "chat.completion",
        "created": created,
        "model": model,
        "choices": [{"index": 0,
                     "message": {"role": "assistant", "content": "".join(text_parts)},
                     "finish_reason": finish}],
        "usage": usage_block(usage),
        "hugpy": served,
    }
    if isinstance(timings, dict) and timings:
        result["timings"] = timings
    return jsonify(result)


# ── the one blueprint + the merged category map ──────────────────────────────
web_bp, logger = get_bp("web_bp", __name__)

# category -> {route_name: callable}; URL = /{category}/{route_name} (+ slash),
# GET+POST. category = the original path prefix, route_name = the last literal
# segment, so the URLs match the originals (path params collapse to kwargs).
LOCAL_CATEGORIES = {
    # Worker routes live under fleet. Deep category merging keeps controls and
    # telemetry declared by separate modules on the same worker tree.
    "llm": {
        "central": {"rescan": central_rescan, "ingest": central_ingest,
                    "models": central_models},
        "snapshot": llm_snapshot,
        "chat": {"cancel": chat_cancel},
    },
    "fleet": {"workers": {
        "admit": workers_admit, "block": workers_block,
        "register": workers_register, "heartbeat": workers_heartbeat,
        "packages": workers_packages,
        "install.sh": workers_install_sh, "bootstrap.sh": workers_install_sh,
        "<worker_id>": {
            "admit": spec(workers_admit, "POST", response="native"),
            "block": spec(workers_block, "POST", response="native"),
            "heartbeat": spec(workers_heartbeat, "POST", response="native"),
        },
    }},
    "chat": {"stream": chat_stream},
    "auth": {"config": auth_config},
    "v1": {"models": v1_models, "task-bindings": v1_task_bindings,
           "chat": {"completions": v1_chat}},
    # /models (the catalog) and /models/<path:model_key> (the central archive
    # delete + the shipped console's database/<key>/workers/<wid>/<verb> family).
    # Both answer BARE JSON. ``models_catalog`` takes the query fields as kwargs;
    # ``models_delete`` is a raw-request dispatcher that forwards the exact JSON
    # body to the model_routes pair_* handlers, so it reads the request itself
    # (inputs="path"). The "" key is the node's own /models index route.
    "models": {"": spec(models_catalog, "GET,POST", response="native"),
               "<path:model_key>": spec(models_delete, "GET,POST", response="native",
                                        inputs="path")},
}


def _merge(*cat_maps) -> dict:
    """Merge section trees with abstract_flask's recursive conflict checking."""
    return merge_categories(*cat_maps, name="web")


from hugpy_core.web.console_routes import (  # noqa: E402
    CONSOLE_CATEGORIES, installed_arms as _installed_arms, readiness as _readiness)
from hugpy_core.web.db_viewer import DB_CATEGORIES  # noqa: E402
from hugpy_core.web.setup_routes import SETUP_CATEGORIES  # noqa: E402
from hugpy_core.web.predictions import PREDICTIONS_CATEGORIES  # noqa: E402

# /arms and /readiness fold in as single-segment routes (callable leaves);
# install.sh / bootstrap.sh fold under fleet/workers now that register_categories
# dot-sanitises endpoint names (abstract_flask >= 0.0.0.1058). The worker
# activity/health path forms and the /models catalog/delete routes are declared
# as nested path-parameter keys in their own trees (console_routes.py and
# LOCAL_CATEGORIES above) — no absolute "rule" strings, no "exact" pseudo-node.
ALL_CATEGORIES = _merge(LOCAL_CATEGORIES, CONSOLE_CATEGORIES, DB_CATEGORIES, SETUP_CATEGORIES,
                        PREDICTIONS_CATEGORIES,
                        {"arms": _installed_arms, "readiness": _readiness})
register_categories(web_bp, ALL_CATEGORIES)
