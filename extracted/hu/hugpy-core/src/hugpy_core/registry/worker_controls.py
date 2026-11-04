"""Console worker-control handlers for hugpy_core (Compute page → GPU workers).

The natural home for the pure handlers behind ``registry.routes``' worker tree:
every view is a plain function taking kwargs (never touches ``request``). The
former path params ``<worker_id>`` / ``<key>`` / ``<wid>`` / ``<token_id>`` arrive
as the same-named kwargs, JSON-body / query values arrive as their own kwargs, and
the operator identity (was the ``X-Hugpy-Operator`` header / remote addr) arrives
as the kwarg ``operator`` (default ``console``).

The worker's front door owns its operator-action queue and outcome rows. Core
submits over the registered worker endpoint and reads that same queue back.

Three groups, labelled per route:

  LIFTED  (done here, in core): forget worker, pool override, model×worker
          block/unblock, central-address, GET /llm/slots.
  RELAYED (event-driven convergence): update (Upgrade) = NOTIFY hugpy_updates →
          the worker's presence loop resyncs and self-updates from PyPI; a
          wrapper without a package converges over its registered updater API.
  OPERATOR ACTIONS: unload / evict / free-ram / restart / remove-model are
          submitted to the box's own front door (/v1/operator/actions) and the
          box's recorded outcome is read back and relayed.
  501 NotInThisBuild: verbs whose legacy backing was removed in the fitevict
          build — reported as an honest ``NotInThisBuild`` with the real reason.

The ``*_path`` helpers keep the shipped console's worker-ID URLs on these same
handlers while preserving each route's HTTP status contract (see ``routes.py``).
"""
from __future__ import annotations

import json
import socket
import time

from hugpy_core.registry import registry

# The hugpy_worker PyPI package whose version the Update button converges to.
WORKER_PKG = "hugpy-worker"
OPERATOR_WAIT_S = 8.0     # how long a click waits for the box's outcome before it reports "requested"


# ── route-layer helpers (pure; the operator identity is a kwarg, not a header) ─
def _not_in_build(verb: str, why: str) -> dict:
    """A verb the console calls but this build has no backing for. Reason stated
    from facts (the HTTP 501 collapses under this convention; the ``code`` field
    keeps the machine signal)."""
    # The console renders `error` directly. Keep it a string for humans while
    # retaining the structured machine signal separately.
    return {"ok": False, "error": why,
            "error_detail": {"code": "NotInThisBuild", "verb": verb, "message": why}}


def _lan_ip() -> "str | None":
    """This host's primary LAN IPv4 — the address a UDP socket to a public IP
    would egress from (no packet is sent). None when no route resolves."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return None
    finally:
        s.close()


def _operator_action(worker_id, action, model_key, who):
    """Submit to the worker's own queue and return its recorded outcome."""
    import urllib.error
    import urllib.request

    w = registry.lookup_worker(worker_id)
    if not w:
        return {"ok": False, "error": f"no such worker: {worker_id}"}
    base = (w.get("url") or "").rstrip("/")
    if not base.startswith(("http://", "https://")):
        return {"ok": False, "error": f"worker {worker_id!r} has no reachable endpoint"}
    body = json.dumps({"action": action, "model_key": model_key,
                       "requested_by": who}).encode("utf-8")
    req = urllib.request.Request(base + "/v1/operator/actions", data=body,
                                 headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            receipt = json.load(response)
    except (urllib.error.URLError, ValueError, OSError) as exc:
        return {"ok": False, "error": f"worker {w.get('name')} did not accept {action}: {exc}"}
    aid = receipt.get("id") if isinstance(receipt, dict) else None
    if not isinstance(aid, int) or aid < 1:
        return {"ok": False, "error": f"worker {w.get('name')} returned no action id"}

    state, result = "requested", {}
    deadline = time.monotonic() + OPERATOR_WAIT_S
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(base + f"/v1/operator/actions/{aid}", timeout=2) as response:
                row = json.load(response)
            state = row.get("state") or "requested"
            result = row.get("result") if isinstance(row.get("result"), dict) else {}
            if state not in ("requested", "running"):
                break
        except (urllib.error.URLError, ValueError, OSError):
            # Restart closes the front door after recording its accepted action.
            break
        time.sleep(0.25)
    out = {"action_id": aid, "worker": w.get("name"), "action": action, "model_key": model_key,
           "state": state, "request_id": result.get("request_id"),
           **{k: v for k, v in result.items() if k != "request_id"}}
    if state == "done":
        unloaded = ("bytes_freed" in result and not result.get("note"))
        return {**out, "ok": True, "evicted": (unloaded if action == "evict" else None),
                "reason": result.get("note")}
    if state in ("requested", "running"):
        return {**out, "ok": True, "pending": True,
                "reason": f"{w.get('name')}'s front door has not answered in {OPERATOR_WAIT_S:.0f} s; "
                          "the action stays queued"}
    return {**out, "ok": False, "error": result.get("error") or f"the box answered {state} with no reason"}


def _free(worker_id, who, all=None, model_key=None):
    if all is True:
        return _operator_action(worker_id, "evict-all", None, who)
    key = (model_key or "").strip()
    if not key:
        return {"ok": False, "error": "model_key is required"}
    return _operator_action(worker_id, "evict", key, who)


# ── worker lifecycle ──────────────────────────────────────────────────────────
def _saved_name(worker_id):
    """The saved connection's name for a worker id or name."""
    from hugpy_core.registry import registrations
    w = registry.lookup_worker(worker_id) or {}
    for name in (w.get("name"), worker_id):
        if name and registrations.get(name):
            return name
    return None


def workers_remove(worker_id=None, **_):
    """Disconnect a worker: core stops collecting from it and routing to it, and the
    saved connection (endpoint + key) stays, so Reconnect needs no new enrollment."""
    from hugpy_core.registry import registrations
    name = _saved_name(worker_id)
    if name:
        registrations.set_connected(name, False)
        registry.remove(worker_id)
        return {"ok": True, "removed": False, "disconnected": True, "id": worker_id, "name": name}
    if not registry.remove(worker_id):
        return {"ok": False, "removed": False, "error": f"no worker {worker_id!r} is connected or saved"}
    return {"ok": True, "removed": True, "id": worker_id}


def workers_reconnect(worker_id=None, **_):
    """Reconnect a disconnected worker from its saved connection (same endpoint + key)."""
    from hugpy_core.registry import registrations
    name = _saved_name(worker_id)
    if not name:
        return {"ok": False, "error": f"no saved connection for {worker_id!r}"}
    registrations.set_connected(name, True)
    return {"ok": True, "reconnected": True, "id": worker_id, "name": name}


def reconnect_path(worker_id=None, **kwargs):
    result = workers_reconnect(worker_id=worker_id, **kwargs)
    return result, 200 if result.get("ok") else 404


def workers_set_pool(worker_id=None, pool="", **_):
    """Operator pool override (``pool``; "" clears). Wins over the pool the worker
    reports; routing and the UI both read the override."""
    w = registry.set_pool_override(worker_id, pool if pool is not None else "")
    if w is None:
        return {"ok": False, "error": f"no worker {worker_id!r} in the registry"}
    return w


def workers_update(worker_id=None, **_):
    """Update a wrapper through its restricted SSH updater, or notify an agent."""
    from hugpy_core.registry.releases import fleet_versions
    w = registry.lookup_worker(worker_id)
    if w is None:
        return {"ok": False, "error": f"no worker {worker_id!r} in the registry"}
    if not w.get("pkg_version"):
        from . import updates
        if _.get('approved') is not True:
            return {'ok':False,'state':'refused','error':'Explicit operator approval is required'}
        try:
            result=updates.submit(w.get('name') or worker_id, version=_.get('version'),
                                  requested_by=_.get('operator') or 'Core console')
            return {'ok':True,'package':'hugpy-wrapper','worker':w.get('name'),
                    'pending':True,**result}
        except Exception as exc:
            return {'ok':False,'error':'Wrapper update request failed: '+str(exc)}
    required = fleet_versions()
    payload = json.dumps({"worker_id": worker_id, "reason": "operator-update"})
    try:
        registry.pg_notify("hugpy_updates", payload)
    except Exception as exc:  # noqa: BLE001 — report the real DB error, no fake ok
        return {"ok": False, "error": {"code": type(exc).__name__, "message": str(exc)}}
    return {"ok": True, "worker_id": worker_id, "notified": "hugpy_updates",
            "online": registry.is_online(w),
            "current_pkg_version": w.get("pkg_version"),
            "required_pkg_version": required.get(WORKER_PKG),
            "required_packages": required}


# ── model × worker block (DB truth; pick skips a blocked pair) ────────────────
def _set_pair_block(key, wid, blocked):
    from hugpy_core.models.modeldb import pair_knobs
    result = pair_knobs(key, wid, **({"set": {"blocked": "operator"}} if blocked else {"unset": ["blocked"]}))
    if isinstance(result, tuple):
        return result
    return {**result, "blocked": blocked}


def model_worker_block(key=None, wid=None, **_):
    return _set_pair_block(key, wid, True)


def model_worker_unblock(key=None, wid=None, **_):
    return _set_pair_block(key, wid, False)


# ── fleet-level ───────────────────────────────────────────────────────────────
def central_address(host="", proto="http", **_):
    """The LAN address of THIS central node. The console's reverse-proxy host/
    scheme (was the ``X-Forwarded-*`` headers / request.host) arrive as the
    ``host`` and ``proto`` kwargs."""
    ip = _lan_ip()
    host = host or ""
    port = ""
    if host.startswith("["):                       # [ipv6]:port
        port = host.split("]", 1)[1].lstrip(":")
    elif host.count(":") == 1:
        port = host.split(":", 1)[1]
    base = None
    if ip:
        base = f"{proto}://{ip}" + (f":{port}" if port and port not in ("80", "443") else "")
    return {"lan_ip": ip, "base_url": base, "host": host}


def llm_slots(**_):
    """Central's OWN serving row. hugpy_core is a router — it holds no model and
    owns no GPU slots in this build, so the slot list is empty."""
    return {"slots": [], "resources": {"used_bytes": 0, "total_bytes": 0},
            "note": "hugpy_core routes only; it serves no model locally"}


def slots_load(**_):
    return _not_in_build(
        "slots/load",
        "hugpy_core serves no model locally (it is a router); there are no central "
        "GPU slots to load into. Models load on the fitevict workers, on demand "
        "(evict-to-fit) when a request is routed to them.")


def slots_unload(**_):
    return _not_in_build(
        "slots/unload",
        "hugpy_core serves no model locally (it is a router); there are no central "
        "GPU slots to unload.")


# ── enrollment tokens (replaced by box enrollment) ────────────────────────────
def enroll_tokens_create(**_):
    return _not_in_build(
        "enroll-tokens (create)",
        "worker enrollment tokens were replaced by box enrollment (secrets "
        "architecture): enroll a box in Settings → Boxes (POST /boxes/enroll). "
        "GET /llm/enroll-tokens returns [] in this build.")


def enroll_tokens_revoke(token_id=None, **_):
    return _not_in_build(
        "enroll-tokens (revoke)",
        "worker enrollment tokens were replaced by box enrollment (secrets "
        "architecture); revoke a box in Settings → Boxes (POST /boxes/revoke).")


# ── verbs with no backing in the fitevict build (honest NotInThisBuild) ───────
_FD = ("the fitevict front door exposes only GET /v1/models,/models,/residents,"
       "/limits,/storage and POST /limits,/v1/chat/completions")
_THIN = ("hugpy_worker is a thin harness serving only /health,/infer,"
         "/infer/stream,/infer/cancel")


def workers_load(worker_id=None, model_key=None, operator="console", **_):
    """Fit and load one model on the worker now.

    The Wrapper performs the same central-to-worker transfer, reap-to-fit and
    central-read fallback used by a routed call, then records the measured
    allocation. A successful load is also the point at which a temporary route
    may be promoted to an allocation.
    """
    key = (model_key or "").strip()
    if not key:
        return {"ok": False, "error": "model_key is required"}
    result = _operator_action(worker_id, "activate-model", key, operator or "console")
    if result.get("ok") and result.get("state") == "done":
        # A manual load has crossed the same fit/load boundary as a routed
        # call; promote a temporary pair only after the Wrapper reports done.
        from hugpy_core.relay.pick import confirm_routed_allocation
        worker = registry.lookup_worker(worker_id)
        if worker is not None:
            result["allocation_recorded"] = confirm_routed_allocation(key, worker, source="operator-load")
    return result


def workers_unload(worker_id=None, operator="console", all=None, model_key=None, **_):
    """Free: the box stops this resident and its memory comes back. The model
    stays allocated and loads again on its next call."""
    return _free(worker_id, operator or "console", all=all, model_key=model_key)


def workers_evict(worker_id=None, operator="console", all=None, model_key=None, **_):
    """Evict = the same box action as Free (one verb on the front door)."""
    return _free(worker_id, operator or "console", all=all, model_key=model_key)


def workers_free_ram(worker_id=None, operator="console", **_):
    """Unload this worker's idle model processes, returning RAM to the OS."""
    return _operator_action(worker_id, "free-ram", None, operator or "console")


def workers_restart(worker_id=None, operator="console", **_):
    """Restart the box's front door: it stops every resident and exits for its
    unit to bring it back clean. The box refuses while a call is in flight."""
    return _operator_action(worker_id, "restart", None, operator or "console")


def workers_reap(worker_id=None, **_):
    return _not_in_build(
        "reap",
        f"no worker-side disk reaper in this build; the model drive is surveyed by "
        f"the fitevict front door (GET /storage) and {_THIN}.")


def workers_remove_model(worker_id=None, operator="console", model_key=None, **_):
    """Remove one worker-local model directory; never the central catalog."""
    key = (model_key or "").strip()
    if not key:
        return {"ok": False, "error": "model_key is required"}
    w = registry.lookup_worker(worker_id)
    if w is None:
        return {"ok": False, "error": f"no worker {worker_id!r}"}
    storage = w.get("storage") or {}
    if not any(m.get("model_key") == key for m in storage.get("models") or []):
        return {"ok": False, "error": "model is not on this worker drive"}
    return _operator_action(worker_id, "remove-model", key, operator or "console")


def workers_reap_approve(worker_id=None, **_):
    return _not_in_build("reap-approve", f"no worker-side disk reaper in this build; {_THIN}.")


def workers_alloc_all(worker_id=None, **_):
    return _not_in_build(
        "alloc-all",
        "allocation is per-pair in this build: assign each model with POST "
        "/models/database/<key>/workers/<wid>/assigned (DB truth). There is no "
        "bulk fit-and-allocate verb; fitevict decides fit at serve time.")


def workers_prune_designations(worker_id=None, **_):
    return _not_in_build(
        "designations/prune",
        "there is no automated-designation registry to prune in this build: "
        "assignments are explicit DB rows (model_workers.assigned), set per pair "
        "via POST /models/database/<key>/workers/<wid>/assigned.")


def workers_bnb(worker_id=None, enabled=None, value=None, all=None, model_key=None, **_):
    """4-bit (bitsandbytes nf4) as a DB pair knob. Writes
    model_workers.user_settings.bnb_4bit. ``enabled``/``value`` true|false pins
    it, null restores auto. ``all`` sweeps every bnb_capable model this worker
    discovered; ``model_key`` does one."""
    from psycopg.types.json import Jsonb
    from hugpy_core.models.modeldb import _conn, _pair
    raw = enabled if enabled is not None else value
    val = None if raw is None else bool(raw)
    w = registry.lookup_worker(worker_id)
    if w is None:
        return {"ok": False, "error": f"no worker {worker_id!r}"}
    capable = {k for k, d in (w.get("models_discovered") or {}).items()
               if (d.get("hugpy_json") or {}).get("bnb_capable")}
    if all:
        keys = sorted(capable)
    else:
        k = model_key
        if not k:
            return {"ok": False, "error": "model_key or all is required"}
        if k not in capable:
            return {"ok": False, "error": f"{k} is not bnb_capable on {w.get('name') or worker_id}"}
        keys = [k]
    from hugpy_core.models.modeldb import pair_knobs
    applied, reports = [], {}
    for key in keys:
        result = pair_knobs(key, worker_id, **({"unset": ["bnb_4bit"]} if val is None else {"set": {"bnb_4bit": val}}))
        if isinstance(result, tuple):
            return {**result[0], "confirmed_models": applied}, result[1]
        applied.append(key)
        reports[key] = result
    return {"ok": True, "count": len(applied), "value": val, "source": "wrapper", "reports": reports}


def workers_wildcard(worker_id=None, enabled=None, **_):
    from hugpy_core.models.modeldb import set_worker_wildcard
    if registry.lookup_worker(worker_id) is None:
        return {"ok": False, "error": f"no worker {worker_id!r}"}
    if not isinstance(enabled, bool):
        return {"ok": False, "error": "enabled must be a boolean"}
    set_worker_wildcard(worker_id, enabled)
    registry._bump()
    return {"ok": True, "worker_id": worker_id, "wildcard": enabled}


def workers_fit_preview(worker_id=None, **_):
    return _not_in_build(
        "fit-preview",
        "the load-gate dry run lives in the worker's fitevict (sizing.py) in this "
        f"build; core does not predict fit. {_FD}.")


def workers_calibrate(worker_id=None, **_):
    return _not_in_build(
        "calibrate",
        "predicted-vs-measured calibration is recorded by fitevict's call log in "
        "this build; there is no core calibrate job.")


def workers_calibrate_status(worker_id=None, job_id=None, **_):
    return _not_in_build(
        "calibrate (status)",
        "there is no core calibrate job in this build (see POST .../calibrate).")


# ── console worker-ID URL status contract ─────────────────────────────────────
# The shipped console places the worker id in the PATH and reads a bare JSON body
# with a meaningful HTTP status (not a convention ``{"result": ...}`` 200). These
# ``*_path`` views keep those URLs on the handlers above and carry each outcome's
# status so a refused / missing / queued operation is not reported as success.
def _worker_action_native(result):
    """Map an operator-action result to ``(body, http status)``: queued 202, ok
    200, bad input 400, unknown worker 404, box refused 409, NotInThisBuild 501,
    otherwise 502 (the box answered but not with a success)."""
    if result.get("pending"):
        status = 202
    elif result.get("ok"):
        status = 200
    elif result.get("error") in ("model_key is required", "model_key or all is required"):
        status = 400
    elif str(result.get("error", "")).startswith(("no such worker:", "no worker ")):
        status = 404
    elif result.get("state") == "refused":
        status = 409
    elif (result.get("error_detail") or {}).get("code") == "NotInThisBuild":
        status = 501
    else:
        status = 502
    return result, status


def unload_path(worker_id=None, **kw):
    return _worker_action_native(workers_unload(worker_id=worker_id, **kw))


def evict_path(worker_id=None, **kw):
    return _worker_action_native(workers_evict(worker_id=worker_id, **kw))


def free_ram_path(worker_id=None, **kw):
    return _worker_action_native(workers_free_ram(worker_id=worker_id, **kw))


def restart_path(worker_id=None, **kw):
    return _worker_action_native(workers_restart(worker_id=worker_id, **kw))


def update_path(worker_id=None, **kw):
    return _worker_action_native(workers_update(worker_id=worker_id, **kw))


def bnb_path(worker_id=None, **kw):
    return _worker_action_native(workers_bnb(worker_id=worker_id, **kw))


def calibrate_path(worker_id=None, **kw):
    """POST /fleet/workers/<worker_id>/calibrate: the NotInThisBuild answer at 501,
    as the console URL always returned (the body form answers 200 {"result"})."""
    return workers_calibrate(worker_id=worker_id, **kw), 501


def wildcard_path(worker_id=None, enabled=None, **_):
    """Console wildcard toggle with a native JSON body and useful HTTP errors."""
    if not isinstance(enabled, bool):
        return {"ok": False, "error": "enabled must be a boolean"}, 400
    result = workers_wildcard(worker_id=worker_id, enabled=enabled)
    return result, 200 if result.get("ok") else 404


def remove_path(worker_id=None, **kwargs):
    result = workers_remove(worker_id=worker_id, **kwargs)
    return result, 200 if result.get("ok") else 404


def pool_path(worker_id=None, **kwargs):
    result = workers_set_pool(worker_id=worker_id, **kwargs)
    return result, 404 if result.get("ok") is False else 200


def load_path(worker_id=None, **kwargs):
    return _worker_action_native(workers_load(worker_id=worker_id, **kwargs))


def reap_path(worker_id=None, **kwargs):
    return _worker_action_native(workers_reap(worker_id=worker_id, **kwargs))


def reap_approve_path(worker_id=None, **kwargs):
    return _worker_action_native(workers_reap_approve(worker_id=worker_id, **kwargs))
