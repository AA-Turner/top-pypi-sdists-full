"""Flask fleet routes backed by Core telemetry and model projections."""
from __future__ import annotations

import json
import hmac
import os
from pathlib import Path
import re
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

from flask import Response, jsonify, request, send_file, stream_with_context
from abstract_flask import get_bp, register_categories, spec

from hugpy_core.web.worker_connect import connect_wrapper, saved_connections
from hugpy_core.registry import drive_display as drives

recovered_surfaces_bp, logger = get_bp("recovered_surfaces_bp", __name__)


def worker_fit_captures(name):
    """List saved fit-station traces for the existing tester UI."""
    if not re.fullmatch(r"[a-zA-Z0-9_-]+", name):
        return _error("Invalid worker name", 400)
    root = Path("/var/lib/hugpy-core/fit-captures")
    captures = []
    for path in sorted(root.glob(f"{name}-*.json"), key=lambda p: p.stat().st_mtime, reverse=True)[:20]:
        if path.stem.endswith("-actions"):
            continue
        capture_id = path.stem[len(name) + 1:]
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        captures.append({"id": capture_id, "captured_at": doc.get("captured_at"),
                         "models": doc.get("models") or [], "actions": len(doc.get("actions") or []),
                         "calls": len(doc.get("calls") or []),
                         "evictions": len(doc.get("evictions") or [])})
    return {"captures": captures}


def worker_fit_capture(name, capture):
    """Browser-readable, immutable fit-station run artifacts kept in Core state."""
    if not re.fullmatch(r"[a-zA-Z0-9_-]+", name) or not re.fullmatch(
            r"[a-zA-Z0-9_-]+(?:\.json)?", capture):
        return _error("Invalid capture name", 400)
    suffix = ".json" if capture.endswith(".json") else ".html"
    stem = capture[:-5] if suffix == ".json" else capture
    path = Path("/var/lib/hugpy-core/fit-captures") / f"{name}-{stem}{suffix}"
    if not path.is_file():
        return _error("Capture not found", 404)
    return send_file(path, mimetype="application/json" if suffix == ".json" else "text/html")


def _error(message, status):
    # Bare (payload, status): the native-response registrar jsonifies it and
    # sets the status, so handlers never call jsonify themselves.
    return {"error": {"message": message}}, status


def _live_capabilities():
    """Fresh discovery flags from the active registry, keyed by model and box."""
    from hugpy_core.registry import registry
    result = {}
    for worker in registry.all_workers():
        name = worker.get("name") or worker.get("id")
        for key, model in (worker.get("models_discovered") or {}).items():
            marker = model.get("hugpy_json") or {}
            result[(key, name)] = (bool(marker.get("moe_capable")),
                                   bool(marker.get("bnb_capable")))
    return result


def api_version():
    from importlib.metadata import version
    return {"ok": True, "api": 1, "service": "hugpy-core",
            "capabilities": ["routing-workers-v1"],
            "version": version("hugpy-core")}


def _worker(name):
    from hugpy_core.registry.registrations import get
    return get(name)


def fleet_resources():
    """Harness fleet resources from intake observations; no remote I/O or actions."""
    from hugpy_core.router.observability import store as routing
    from hugpy_core.registry import registry
    class RequestView:
        client_address = (request.remote_addr or '', 0)
        headers = request.headers
        request = request.environ.get('werkzeug.socket')
    denied = routing.KEYS.check(RequestView(), 'use')
    if denied:
        status, body = denied
        return body, status
    workers = []
    for worker in registry.all_workers():
        resources = worker.get('resources')
        workers.append({'worker': worker.get('name') or worker.get('id'),
                        'worker_id': worker.get('id'),
                        'url': worker.get('url'), 'online': registry.is_online(worker),
                        'observed_at': worker.get('last_seen'),
                        'error': '' if resources is not None else 'Wrapper resource snapshot unavailable',
                        'resources': resources or {}})
    return {'scope': 'fleet', 'workers': workers}


def fleet_workers():
    """The console's worker list: the same native array as the legacy reader."""
    from hugpy_core.web.routes import workers_list
    return workers_list()


def register_wrapper():
    """Keep the existing wrapper install contract on the Flask Core API."""
    expected = os.environ.get("HUGPY_ROUTER_KEY") or ""
    supplied = request.headers.get("Authorization", "")
    supplied = supplied[7:].strip() if supplied.lower().startswith("bearer ") else ""
    if not expected:
        return _error("Core registration key is not configured", 503)
    if not hmac.compare_digest(supplied, expected):
        return _error("Forbidden", 403)
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return _error("Expected a JSON object", 400)
    try:
        from hugpy_core.registry.registrations import upsert
        worker = upsert(body)
    except ValueError as exc:
        return _error(str(exc), 400)
    return {"name": worker["name"], "url": worker["url"]}, 200


def _proxy_worker(name, path, payload=None):
    worker = _worker(name)
    if worker is None:
        return _error("Unknown worker", 404)
    url = worker["url"].rstrip("/") + path
    headers = {"Accept": "application/json"}
    if worker.get("key"):
        headers["Authorization"] = "Bearer " + worker["key"]
    if payload is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=json.dumps(payload).encode() if payload is not None else None,
                                 headers=headers, method="POST" if payload is not None else "GET")
    try:
        with urllib.request.urlopen(req, timeout=20) as reply:
            return jsonify(json.load(reply)), reply.status
    except urllib.error.HTTPError as exc:
        try:
            return jsonify(json.load(exc)), exc.code
        except (ValueError, OSError):
            return _error(f"Worker returned HTTP {exc.code}", exc.code)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return _error(f"Worker unavailable: {exc}", 502)


def _compute_fleet_models():
    """The authoritative (and slow, ~15s) fleet model projection. Always the heavy read."""
    from hugpy_core.web import native_fleet
    rows = native_fleet.models()
    live = _live_capabilities()
    for row in rows:
        for worker in row.get("workers") or []:
            moe, bnb = live.get((row["model_key"], worker), (False, False))
            row["moe_capable"] = bool(row.get("moe_capable")) or moe
            row["bnb_capable"] = bool(row.get("bnb_capable")) or bnb
    return rows


# --- Materialized models catalog (Postgres) -------------------------------------
# The fleet projection is assembled in Python across ~10 normalized tables (~15s),
# so it must not run on every console #models load. We materialize the assembled
# rows into a Postgres table `console_fleet_cache`, refreshed by a background
# thread (timer + event hook). The route then serves a single cheap SELECT.
# Because the table is in the DB it survives Core restarts (no cold rebuild on the
# first post-restart load) and is shared across processes/consumers.
_FLEET_TTL = float(os.environ.get("HUGPY_FLEET_MODELS_TTL", "45"))  # refresh cadence (s)
_FLEET_KIND = "fleet_models"
_fleet_state = {"building": False, "error": None}
_fleet_cv = threading.Condition()
_fleet_started = False


def _fleet_table(cur):
    cur.execute("CREATE TABLE IF NOT EXISTS console_fleet_cache ("
                "kind text PRIMARY KEY, payload jsonb NOT NULL, "
                "as_of timestamptz NOT NULL DEFAULT now())")


def _fleet_read():
    """Return (rows, as_of_epoch) from the materialized table, or (None, None)."""
    from hugpy_core.models import modeldb
    with modeldb._conn() as conn, conn.cursor() as cur:
        _fleet_table(cur)
        cur.execute("SELECT payload, extract(epoch FROM as_of) AS as_of "
                    "FROM console_fleet_cache WHERE kind=%s", (_FLEET_KIND,))
        row = cur.fetchone()
    return (row["payload"], float(row["as_of"])) if row else (None, None)


def _fleet_json_default(o):
    # Match Flask's default JSON provider so the materialized payload is byte-for-byte
    # identical to the old jsonify output (datetimes as HTTP-date strings).
    from datetime import date, datetime
    from werkzeug.http import http_date
    if isinstance(o, (date, datetime)):
        return http_date(o)
    return str(o)


def _fleet_build():
    """Recompute the heavy projection and upsert it into the materialized table."""
    try:
        from hugpy_core.models import modeldb
        from psycopg.types.json import Jsonb
        rows = _compute_fleet_models()
        payload = Jsonb(rows, dumps=lambda o: json.dumps(o, default=_fleet_json_default))
        with modeldb._conn() as conn, conn.cursor() as cur:
            _fleet_table(cur)
            cur.execute("INSERT INTO console_fleet_cache (kind,payload,as_of) "
                        "VALUES (%s,%s,now()) ON CONFLICT (kind) DO UPDATE "
                        "SET payload=EXCLUDED.payload, as_of=now()", (_FLEET_KIND, payload))
            conn.commit()
        with _fleet_cv:
            _fleet_state["error"] = None
    except Exception as exc:  # noqa: BLE001 - cache boundary: keep last-good, record error
        with _fleet_cv:
            _fleet_state["error"] = str(exc)
        logger.exception("fleet/models cache build failed")
    finally:
        with _fleet_cv:
            _fleet_state["building"] = False
            _fleet_cv.notify_all()


def _fleet_ensure_build():
    """Kick a background rebuild if one is not already running."""
    with _fleet_cv:
        if _fleet_state["building"]:
            return
        _fleet_state["building"] = True
    threading.Thread(target=_fleet_build, name="fleet-models-cache", daemon=True).start()


def fleet_models_invalidate():
    """Event hook: force a background refresh of the materialized catalog."""
    _fleet_ensure_build()


def _fleet_refresher():
    while True:
        _fleet_ensure_build()
        time.sleep(_FLEET_TTL)


def fleet_models():
    global _fleet_started
    now = time.time()
    with _fleet_cv:
        if not _fleet_started:
            _fleet_started = True
            threading.Thread(target=_fleet_refresher, name="fleet-models-refresher",
                             daemon=True).start()
    try:
        data, as_of = _fleet_read()
    except Exception:  # noqa: BLE001 - DB hiccup: fall through to a (re)build
        logger.exception("fleet/models cache read failed")
        data, as_of = None, None
    if data is None or (as_of and now - as_of > _FLEET_TTL):
        _fleet_ensure_build()
    if data is None:
        # Table empty (fresh DB only): block once for the initial build.
        with _fleet_cv:
            _fleet_cv.wait_for(lambda: not _fleet_state["building"], timeout=30)
        try:
            data, as_of = _fleet_read()
        except Exception:  # noqa: BLE001
            data, as_of = None, None
    with _fleet_cv:
        building = _fleet_state["building"]
        error = _fleet_state["error"]
    return {"object": "list", "data": data or [],
            "cache": {"as_of": as_of,
                      "age_s": round(now - as_of, 1) if as_of else None,
                      "building": building,
                      "stale": bool(as_of and now - as_of > _FLEET_TTL),
                      "error": error, "store": "postgres"}}


def fleet_model(key):
    from hugpy_core.web import native_fleet
    result = native_fleet.model(key)
    return result if result is not None else _error("Unknown model", 404)


def fleet_catalog(view=None, **_):
    """Model navigation index, or full quant summaries when no view is specified."""
    from hugpy_core.models import catalog_live
    try:
        return catalog_live.catalog_index() if view == "index" else catalog_live.catalog()
    except catalog_live.CatalogUnavailable as exc:
        return _error(str(exc), 503)


def fleet_catalog_model(key, records=None, offset=0, **_):
    """One catalog model; ``?records=wrapper.<table>`` pages that source table's rows."""
    from hugpy_core.models import catalog_live
    try:
        result = catalog_live.model(key, records=records or None, offset=max(0, int(offset or 0)))
    except catalog_live.CatalogUnavailable as exc:
        return _error(str(exc), 503)
    return result if result is not None else _error("Unknown model", 404)


def central_drives():
    from hugpy_core.web.native_fleet import central_copies
    copies = central_copies()
    result = []
    for drive in drives.declared_drives():
        mine = [c for c in copies if c["drive"] == drive["path"]]
        result.append({**drives.drive_usage(drive, sum(int(c.get("bytes") or 0) for c in mine)),
                       "copies": len(mine),
                       "verified": sum(1 for c in mine if c.get("verified")),
                       "unhashed": sum(1 for c in mine if not c.get("verified")),
                       "unhashed_bytes": sum(int(c.get("bytes") or 0) for c in mine if not c.get("verified")),
                       "models": sorted({c["model_key"] for c in mine}),
                       "real_path": os.path.realpath(drive["path"])})
    return {"drives": result}


def central_drives_save(drives_list=None, drives=None, **_):
    """POST /fleet/central/drives {drives: [{path, max_gib}]}: central's drive list and
    budgets, set like any worker's (the env designation is only the default)."""
    from hugpy_core.registry import drive_display
    try:
        saved = drive_display.save_drives(drives if drives is not None else drives_list)
    except ValueError as exc:
        return _error(str(exc), 400)
    return {"ok": True, "drives": saved, **central_drives()}


def central_connect(path=""):
    """Connect a drive already declared in Core's storage configuration."""
    from pathlib import Path
    from hugpy_core.registry import central_store

    path = str(path or "").strip()
    declared = {d["path"] for d in drives.declared_drives()}
    if path not in declared or not os.path.isdir(path):
        return _error("Choose a mounted drive listed under Central storage", 400)
    state = Path("/var/lib/hugpy-core/central-models-home")
    staged = state.with_suffix(".new")
    staged.write_text(path + "\n", encoding="utf-8")
    os.replace(staged, state)
    os.environ["HUGPY_CENTRAL_MODELS_HOME"] = path
    return {"ok": True, **central_store.rescan()}


def box_settings_get(name):
    """The worker's box settings with the worker's OWN schema (its /v1/settings/schema):
    the console shows exactly the settings that wrapper has — labels, ranges and help
    as it reports them. Core keeps no copy of the schema."""
    response = _proxy_worker(name, "/v1/settings/box")
    if not (isinstance(response, tuple) and response[1] < 400):
        return response
    data = response[0].get_json()
    schema = _proxy_worker(name, "/v1/settings/schema")
    entries = schema[0].get_json() if isinstance(schema, tuple) and schema[1] < 400 else {}
    accepts = set(data.get("accepts") or [])
    box_only = set(data.get("box_only_accepts") or (data.get("box_only") or {}).keys())
    every = (entries.get("box") or []) + [k for k in (entries.get("model") or [])
                                          if k["key"] not in {e["key"] for e in entries.get("box") or []}]
    data["knobs"] = [k for k in every if k["key"] in accepts]
    data["box_knobs"] = [k for k in every if k["key"] in box_only]
    data["schema_source"] = "worker"
    return data


def box_settings_post(name, settings=None):
    if not isinstance(settings, dict):
        return _error("a settings object is required", 400)
    from hugpy_core.intake.wrapper_settings import box_command
    try:
        report = box_command(name, settings)
    except Exception as exc:
        return _error(f'Wrapper change was not confirmed: {exc}', 502)
    from hugpy_core.web.native_fleet import operation
    operation(name, 'box-settings', {'settings': settings})
    return report


def worker_updates_get(name):
    """GET /fleet/workers/<name>/updates: the box's pending wrapper updates."""
    return _proxy_worker(name,'/v1/updates')


def worker_updates_approve(name, approved=None, **_body):
    """POST /fleet/workers/<name>/updates {approved: true}: explicit operator
    approval (the JSON boolean itself; the registrar keeps its type)."""
    if approved is not True:return _error('Explicit operator approval is required',400)
    return _proxy_worker(name,'/v1/updates',{'approved':True,**_body})


def worker_update_status(name,update_id):
    if not re.fullmatch('[a-f0-9]{32}',update_id):return _error('Invalid update id',400)
    return _proxy_worker(name,'/v1/updates/'+update_id)


def worker_drives(name):
    return _proxy_worker(name, "/v1/drives")


# Raw-request adapter: the POST derives ``requested_by`` from the live operator
# header / remote address, so it keeps ``inputs="path"`` and reads the request.
def worker_station(name):
    """The fit station's authenticated worker lease and action relay."""
    if request.method == "GET":
        return _proxy_worker(name, "/v1/station")
    body = request.get_json(silent=True) or {}
    action = body.get("action")
    if action not in ("station-reserve", "station-release", "station-free", "station-stage", "station-load", "activate-model", "refresh-models"):
        return _error("Unknown fit station action", 400)
    if action in ("station-stage", "station-load", "activate-model") and not body.get("model_key"):
        return _error("model_key is required", 400)
    if action == "station-free" and (body.get("params") or {}).get("resource") not in ("vram", "ram", "swap", "all"):
        return _error("resource must be vram, ram, swap, or all", 400)
    return _proxy_worker(name, "/v1/operator/actions", {
        "action": action, "model_key": body.get("model_key"),
        "requested_by": request.headers.get("X-Hugpy-Operator") or request.remote_addr or "fit station",
        "params": body.get("params") or {},
    })


def worker_station_action(name, action_id):
    return _proxy_worker(name, f"/v1/operator/actions/{action_id}")


def worker_station_task(name, model_key=None, task=None, lease_id=None, knobs=None):
    """Run one real task call through the reserved worker, with a fixed fixture."""
    from hugpy_core.web import station_tasks
    worker = _worker(name)
    if worker is None:
        return _error("Unknown worker", 404)
    if not all(isinstance(x, str) and 0 < len(x) < 256 for x in (model_key, task, lease_id)):
        return _error("model_key, task and lease_id are required", 400)
    knobs = knobs or {}
    if not isinstance(knobs, dict):
        return _error("knobs must be an object", 400)
    try:
        result, status = station_tasks.run(worker, task, model_key, lease_id, knobs)
        return result, status
    except ValueError as exc:
        return _error(str(exc), 400)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return _error(f"Worker task failed: {exc}", 502)


def worker_station_runs_get(name):
    from hugpy_core.web import station_runs
    worker = _worker(name)
    if worker is None:
        return _error("Unknown worker", 404)
    return {"runs": station_runs.list_runs(name)}


def worker_station_runs_post(name, **body):
    from hugpy_core.web import station_runs
    worker = _worker(name)
    if worker is None:
        return _error("Unknown worker", 404)
    try:
        return station_runs.start(worker, body), 202
    except ValueError as exc:
        return _error(str(exc), 409)
    except (OSError, RuntimeError) as exc:
        return _error(str(exc), 502)


def worker_model_copies_get(name):
    """Independent, sequential central-to-worker copy queue; no station lease or task calls."""
    from hugpy_core.web import station_runs
    worker = _worker(name)
    if worker is None:
        return _error("Unknown worker", 404)
    return {"runs": [r for r in station_runs.list_runs(name) if r["kind"] == "copy"]}


def worker_model_copies_post(name, models=None):
    from hugpy_core.web import station_runs
    worker = _worker(name)
    if worker is None:
        return _error("Unknown worker", 404)
    if not isinstance(models, list):
        return _error("models must be a list", 400)
    try:
        return station_runs.start(worker, {"kind": "copy", "models": models}), 202
    except ValueError as exc:
        return _error(str(exc), 409)
    except (OSError, RuntimeError) as exc:
        return _error(str(exc), 502)


def cancel_worker_model_copies(name, run_id):
    from hugpy_core.web import station_runs
    if _worker(name) is None:
        return _error("Unknown worker", 404)
    try:
        return station_runs.cancel(name, run_id)
    except ValueError as exc:
        return _error(str(exc), 404)


def worker_station_run_stream(name):
    from hugpy_core.web import station_runs
    if _worker(name) is None:
        return _error("Unknown worker", 404)

    def generate():
        for event in station_runs.events(name):
            yield "data: " + json.dumps(event) + "\n\n" if event else ": keepalive\n\n"

    return Response(stream_with_context(generate()), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


def worker_fit_project(name, occupants=None):
    """A faux occupancy event evaluated by the same pair_live DB projector."""
    from hugpy_core.brain import gpu_live
    if _worker(name) is None:
        return _error("Unknown worker", 404)
    occupants = occupants or []
    if not isinstance(occupants, list) or len(occupants) > 500 or any(
        not isinstance(item, dict) or not isinstance(item.get("key"), str)
        or (item.get("file") is not None and not isinstance(item["file"], str))
        or (item.get("mode") is not None and not isinstance(item["mode"], str))
        for item in occupants
    ):
        return _error("occupants must be a list of model keys and optional file/mode", 400)
    try:
        return gpu_live.project(name, occupants)
    except ValueError as exc:
        return _error(str(exc), 404)


def worker_station_run_cancel(name, run_id):
    from hugpy_core.web import station_runs
    try:
        return station_runs.cancel(name, run_id)
    except ValueError as exc:
        return _error(str(exc), 404)


def worker_models(name):
    response = _proxy_worker(name, "/v1/models")
    if isinstance(response, tuple) and response[1] < 400:
        data = response[0].get_json()
        return {"models": [{"model_key": m.get("model_key") or m.get("id"),
                            "name": m.get("name") or m.get("id")}
                           for m in (data.get("models") or data.get("data") or [])]}
    return response


def storage_owners():
    """Storage ownership is scoped by host; remote paths are never core paths."""
    from hugpy_core.registry import registry, central_store
    owners = []
    for w in registry.all_workers():
        name = w.get('name') or w.get('id')
        owners.append({'owner_worker': name, 'source_protocol': 'wrapper',
                       'models_central': w.get('models_central') or {},
                       'drives_url': '/fleet/workers/' + urllib.parse.quote(name, safe='') + '/drives'})
    owners.append({'owner_worker': None, 'source_protocol': 'core',
                   'models_central': {r['model_key']: r for r in central_store.rows()}})
    return {'owners': owners}


def delegate_transfer(name, **body):
    """Core chooses an enrolled source; the destination owns all filesystem work."""
    from hugpy_core.registry import registry
    key, drive = body.get('model_key'), body.get('destination_drive')
    if not isinstance(key, str) or not key or not isinstance(drive, str) or not drive:
        return _error('model_key and destination_drive are required', 400)
    if _worker(name) is None:
        return _error('Unknown destination worker', 404)
    response = _proxy_worker(name, '/v1/drives')
    if not isinstance(response, tuple) or response[1] != 200:
        return response
    report = response[0].get_json()
    if 'receive-model-v1' not in report.get('transfer_capabilities', []):
        return _error('Destination wrapper requires the receive-model upgrade', 409)
    roots = report.get('drives', []) + report.get('central_drives', [])
    if not any(r.get('drive_id') == drive and r.get('writable') for r in roots):
        return _error('Destination is not an advertised writable drive', 409)
    requested = body.get('source_worker')
    candidates = [w for w in registry.all_workers()
                  if key in (w.get('models_central') or {}) or key in (w.get('models_discovered') or {})]
    candidates.sort(key=lambda w: (0 if key in (w.get('models_central') or {}) else 1,
                                   str(w.get('name') or w.get('id'))))
    if requested:
        candidates = [w for w in candidates if (w.get('name') or w.get('id')) == requested]
    source = next((_worker(w.get('name') or w.get('id')) for w in candidates
                   if _worker(w.get('name') or w.get('id')) is not None), None)
    protocol = 'wrapper'
    # Every byte goes through Core (operator 2026-10-23): the destination pulls from
    # Core's address, which every worker reaches; Core streams from the source
    # wrapper (web/transfer_relay.py). The credential is for this transfer only.
    from hugpy_core.web.transfer_relay import mint
    core_url = (os.environ.get('HUGPY_CORE_URL') or '').rstrip('/')
    if not core_url:
        return _error('Core requires HUGPY_CORE_URL to relay a delegated transfer', 409)
    if source:
        owner = source['name']
        # Core's API lives under /api (bare /fleet/* and /llm/* are the web apps)
        url = core_url + '/api/fleet/workers/' + urllib.parse.quote(owner, safe='')
        headers = {'Authorization': 'Bearer ' + mint(owner, key, name)}
    elif not requested or requested == 'core':
        from hugpy_core.registry import central_store
        if not any(r['model_key'] == key for r in central_store.rows()):
            return _error('No enrolled source reports this model', 409)
        url = core_url + '/api'
        headers = {'Authorization': 'Bearer ' + mint('core', key, name)}
        protocol, owner = 'core', None
    else:
        return _error('Requested source does not report this model', 409)
    # Source credentials are sent only to the destination job, never returned.
    response = _proxy_worker(name, '/v1/operator/actions', {
        'action': 'receive-model', 'model_key': key, 'requested_by': 'core transfer',
        'params': {'source_url': url, 'source_protocol': protocol, 'headers': headers,
                   'destination_drive': drive, 'file': body.get('file')}})
    if isinstance(response, tuple) and response[1] < 400:
        result = response[0].get_json()
        result.update({'source_worker': owner, 'destination_worker': name, 'destination_drive': drive})
        return result, response[1]
    return response


def delete_worker_model_files_get(name, model_key=None):
    """Preview exact worker-owned bytes for a model (read-only)."""
    if not isinstance(model_key, str) or not model_key:
        return _error('model_key is required', 400)
    return _proxy_worker(name, '/v1/operator/delete-preview?model_key=' + urllib.parse.quote(model_key, safe=''))


def delete_worker_model_files_post(name, model_key=None, confirmation=None):
    """Delegate explicit whole-unit deletion after re-confirming the preview."""
    from hugpy_core.web import station_runs
    if not isinstance(model_key, str) or not model_key:
        return _error('model_key is required', 400)
    preview = _proxy_worker(name, '/v1/operator/delete-preview?model_key=' + urllib.parse.quote(model_key, safe=''))
    if not isinstance(preview, tuple) or preview[1] != 200:
        return preview
    plan = preview[0].get_json()
    if confirmation != plan.get('confirmation'):
        return _error('Model directory changed; review deletion again', 409)
    keys = plan['model_keys']
    for run in station_runs.list_runs(name):
        if run.get('state') == 'running' and any(m['key'] in keys for m in run.get('models', [])):
            return _error('Stop this model’s active copy or test run before deleting its files', 409)
    # This action deletes a worker-drive copy only. Core allocation and pin are
    # separate routing state; a later routed call may stage the bytes again.
    return _proxy_worker(name, '/v1/operator/actions', {
        'action': 'delete-worker-model', 'model_key': model_key, 'requested_by': 'operator delete files',
        'params': {'confirmation': plan['confirmation']}})

# The frozen packaged-console URLs expressed as the real category tree: dict
# nesting IS the path, a ``<name>`` / ``<path:key>`` / ``<int:action_id>`` key is
# a path parameter reaching the handler as the same-named kwarg, and a LIST on a
# key puts the GET and POST views on one URL. Every route answers bare JSON
# (``response="native"``), exactly as the console reads them today. Three leaves
# keep ``inputs="path"`` because they are genuine raw-request readers (the two
# registration/identity gates and the update-approval bool check).
ALL_CATEGORIES = {
    "v1": {"telemetry": {"resources": spec(fleet_resources, "GET", response="native", inputs="path")}},
    "version": spec(api_version, "GET", response="native"),                 # /version
    "fleet": {
        "models": {
            "": spec(fleet_models, "GET", response="native"),               # /fleet/models
            "<path:key>": spec(fleet_model, "GET", response="native"),      # /fleet/models/<path:key>
        },
        "catalog": {
            "": spec(fleet_catalog, "GET", response="native"),              # /fleet/catalog
            "<path:key>": spec(fleet_catalog_model, "GET", response="native"),  # /fleet/catalog/<path:key>
        },
        "central": {
            "drives": [spec(central_drives, "GET", response="native"),      # /fleet/central/drives
                       spec(central_drives_save, "POST", response="native")],
            "connect": spec(central_connect, "POST", response="native"),    # /fleet/central/connect
        },
        "storage": {
            "owners": spec(storage_owners, "GET", response="native"),       # /fleet/storage/owners
        },
        "workers": {
            "connect": spec(connect_wrapper, "POST", response="native", inputs="path"),
            "saved": spec(saved_connections, "GET", response="native"),     # /fleet/workers/saved
            # Raw-request gate: reads the Authorization header before upsert.
            "": [spec(fleet_workers, "GET", response="native"),
                 spec(register_wrapper, "POST", response="native", inputs="path")],
            "<name>": {
                "box-settings": [spec(box_settings_get, "GET", response="native"),
                                 spec(box_settings_post, "POST", response="native")],
                "drives": spec(worker_drives, "GET", response="native"),
                "fit-captures": {
                    "": spec(worker_fit_captures, "GET", response="native"),
                    "<capture>": spec(worker_fit_capture, "GET", response="native"),
                },
                "fit-project": spec(worker_fit_project, "POST", response="native"),
                "model-copies": {
                    "": [spec(worker_model_copies_get, "GET", response="native"),
                         spec(worker_model_copies_post, "POST", response="native")],
                    "<run_id>": {"cancel": spec(cancel_worker_model_copies, "POST", response="native")},
                },
                "models": {
                    "": spec(worker_models, "GET", response="native"),
                    "delete": [spec(delete_worker_model_files_get, "GET", response="native"),
                               spec(delete_worker_model_files_post, "POST", response="native")],
                },
                "station": {
                    # Raw-request adapter: the POST reads the operator identity header.
                    "": spec(worker_station, "GET,POST", response="native", inputs="path"),
                    "actions": {"<int:action_id>": spec(worker_station_action, "GET", response="native")},
                    "runs": {
                        "": [spec(worker_station_runs_get, "GET", response="native"),
                             spec(worker_station_runs_post, "POST", response="native")],
                        "stream": spec(worker_station_run_stream, "GET", response="native"),
                        "<run_id>": {"cancel": spec(worker_station_run_cancel, "POST", response="native")},
                    },
                    "task": spec(worker_station_task, "POST", response="native"),
                },
                "transfers": spec(delegate_transfer, "POST", response="native"),
                "updates": {
                    # GET lists; POST needs the EXACT approved=True bool (merged
                    # inputs would coerce it to 1), so this stays a raw reader.
                    "": [spec(worker_updates_get, "GET", response="native"),
                          spec(worker_updates_approve, "POST", response="native")],
                    "<update_id>": spec(worker_update_status, "GET", response="native"),
                },
            },
        },
    },
}
register_categories(recovered_surfaces_bp, ALL_CATEGORIES)
