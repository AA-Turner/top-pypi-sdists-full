# LIFTED from legacy hugpy (read-only reference):
#   URL resolution  <- py/services/hugpy_server/src/hugpy_server/app/routes/worker_routes.py:311-356
#   HEARTBEAT_TIMEOUT_SECONDS / _is_online <- py/fleet/hugpy_fleet/src/hugpy_fleet/central/workers.py:155,666
#   register id reuse (id, else url, else uuid4) <- workers.py WorkerStore.register:4852
#   lookup_worker   <- workers.py:8066-8077
# CHANGED: the registry is LIVE IN MEMORY (no workers.json, no DB tables). A router
#   restart forgets every worker; the next heartbeat gets 410 and re-registers.
# DROPPED: admission, enrollment tokens, assignments memory, ghost supersede,
#   presence DB, every heartbeat telemetry adoption.
"""Live worker registry: register, heartbeat, liveness.

With HUGPY_CORE_SHARED_PRESENCE=1, readers also use the independent collector's
database-backed presence. HTTP restarts then retain the latest worker reports.
"""
from __future__ import annotations
from hugpy_core.imports import functions as _F

import logging
import os
import threading
import time
import uuid
from typing import Any, Dict, List, Optional

# PRESENCE IS HTTP (operator 2026-10-08, "robust and catered to an install devoid
# of hugpy dev or existing infrastructure"): a worker is online while central has
# heard from it within this window. "Heard from it" means a register/heartbeat on
# the worker contract (hugpy_worker.presence now beats over HTTP) OR an intake pass
# that reached the box through the router (feed.Box._register refreshes last_seen on
# every answered long-poll). NO box opens a Postgres session for presence anymore,
# and core asks no Postgres lock — the advisory-lock presence (classid 0x68756770)
# and its DSN probe are gone. The window is 3+ missed worker beats
# (WORKER heartbeat interval 30 s) and also covers the intake's long-poll cadence
# (the wrapper caps a poll at ~60 s, so a quiet box is re-registered at least that
# often); 120 s gives both a comfortable margin without flapping.
HEARTBEAT_TIMEOUT_SECONDS = 120.0
logger = logging.getLogger("hugpy_core.registry")

_UNREACHABLE_HOSTS = {"127.0.0.1", "127.0.1.1", "localhost", "0.0.0.0", "::1", ""}

_LOCK = threading.Lock()
_WORKERS: Dict[str, Dict[str, Any]] = {}

# Operator pool override (RE-LIFTED <- workers.py set_worker_pool): wins over the
# pool the worker reports on its beat. In-memory like the rest of this registry;
# admission itself lives in hugpy_core.admission (DB-backed), not here.
_POOL_OVERRIDE: Dict[str, str] = {}

# Fields a worker reports that the router keeps (everything else is ignored).
REGISTER_FIELDS = ("name", "port", "gpus", "free_ram", "ram_free_bytes", "swap_total", "swap_free", "ram_total", "engine",
                   "pool", "models", "pkg_version")
HEARTBEAT_FIELDS = ("gpus", "port", "free_ram", "ram_free_bytes", "swap_total", "swap_free", "ram_total", "engine", "pool",
                    "pkg_version", "loaded_models", "models_local",
                    "models_discovered", "models_central", "allocations", "storage",
                    "pid_registry",   # per-card GPU processes (console display)
                    "cpu")            # the box's cpu_state: per-CPU busy, free / reserved cores


def _is_dangerous_callback_host(host: str) -> bool:
    """Block self-advertised callback hosts that would turn central into an SSRF
    proxy: cloud-metadata / link-local (169.254.0.0/16 incl. 169.254.169.254,
    fe80::/10). LAN/private and routable (e.g. WireGuard) worker IPs are fine —
    workers are reached on their real address. A bare hostname is allowed.
    """
    h = (host or "").lower().strip("[]")
    if h in {"metadata.google.internal", "metadata"}:
        return True
    try:
        import ipaddress
        ip = ipaddress.ip_address(h)
        return ip.is_link_local or ip.is_unspecified
    except ValueError:
        return False


def _host_of(url: str) -> str:
    from urllib.parse import urlparse
    try:
        return (urlparse(url).hostname or "").lower()
    except Exception:
        return ""


def resolve_worker_url(advertised: str | None, port: int | None, client_ip: str) -> str:
    """Pick the callback URL central will store for a worker.

    If the worker advertised a usable host, trust it. Otherwise (no URL, or a
    loopback/bogus host) build one from the request's source IP + the port.
    """
    if advertised:
        host = _host_of(advertised)
        if host and host not in _UNREACHABLE_HOSTS and not _is_dangerous_callback_host(host):
            return advertised.rstrip("/")
    ip = client_ip
    p = port or 9100
    # IPv6 literal needs brackets.
    host = f"[{ip}]" if ":" in ip else ip
    return f"http://{host}:{p}"


_CHANGED = threading.Condition()
_VERSION = [0]


def _bump() -> None:
    """A worker registered / heartbeated: wake every /llm/events stream."""
    with _CHANGED:
        _VERSION[0] += 1
        _CHANGED.notify_all()


def version() -> int:
    return _VERSION[0]


def wait_change(seen: int, timeout: float) -> int:
    with _CHANGED:
        if _VERSION[0] == seen:
            _CHANGED.wait(timeout=timeout)
        return _VERSION[0]


def _now() -> float:
    return time.time()


# HTTP presence (operator 2026-10-08): online = heard from within
# HEARTBEAT_TIMEOUT_SECONDS. last_seen is stamped by register()/heartbeat() (the
# worker's HTTP beat) and by the intake's per-pass register() (the router reaching
# the box). No Postgres lock, no DSN probe, no cache to invalidate — one in-memory
# timestamp comparison, so a box that goes away simply ages out of the window.
def is_online(worker: Dict[str, Any]) -> bool:
    if worker.get("connected") is False:
        return False
    last = worker.get("last_seen")
    return bool(last) and (_now() - last) <= HEARTBEAT_TIMEOUT_SECONDS


def announce_started() -> None:
    """Core's registry is in memory: after a core restart it has forgotten every
    worker. A connected worker's next HTTP beat gets 410 and re-registers on its
    own (hugpy_worker._sync_once), so this NOTIFY is only a nudge for any component
    still LISTENing on hugpy_worker_cfg (e.g. the local wrapper); it is never
    required for a worker to come back, and a DB that is down is not fatal here."""
    try:
        import psycopg
        with psycopg.connect(_F.core_dsn(), autocommit=True, connect_timeout=3) as c:
            c.execute("SELECT pg_notify('hugpy_worker_cfg', %s)", ('{"core":"started"}',))
    except Exception as exc:  # noqa: BLE001
        logger.warning("could not announce core start to workers: %s", exc)


def public_view(worker: Dict[str, Any]) -> Dict[str, Any]:
    out = {k: v for k, v in worker.items() if not k.startswith("_")}
    out["status"] = "online" if is_online(worker) else "offline"
    ov = _POOL_OVERRIDE.get(worker.get("id"))
    if ov is not None:
        out["pool"] = ov
    return out


def effective_pool(worker: Dict[str, Any]) -> str:
    """The pool used for routing: the operator override when set, else the pool
    the worker reports on its beat."""
    ov = _POOL_OVERRIDE.get(worker.get("id"))
    return ov if ov is not None else (worker.get("pool") or "")


def set_pool_override(worker_id: str, pool: str) -> Optional[Dict[str, Any]]:
    """Operator pool override ('' clears). None when the id is unknown."""
    pool = (pool or "").strip()
    with _LOCK:
        if worker_id not in _WORKERS:
            return None
        if pool:
            _POOL_OVERRIDE[worker_id] = pool
        else:
            _POOL_OVERRIDE.pop(worker_id, None)
        out = dict(_WORKERS[worker_id])
    _bump()
    return public_view(out)


def remove(worker_id: str) -> bool:
    """Forget a worker (and its pool override). A live worker's next presence sync
    re-registers it, matching the legacy DELETE semantics. Admission lives in the
    DB (hugpy_core.admission) and is left intact — a block survives a forget."""
    with _LOCK:
        existed = _WORKERS.pop(worker_id, None) is not None
        _POOL_OVERRIDE.pop(worker_id, None)
    if existed:
        _bump()
    return existed


def pg_notify(channel: str, payload: str) -> None:
    """Fire one Postgres NOTIFY on ``channel`` (the worker's presence loop LISTENs
    on the config channels and resyncs on any beat). Raises on a DB failure so the
    caller can report it — never swallowed into a fake success."""
    import psycopg
    with psycopg.connect(_F.core_dsn(), autocommit=True, connect_timeout=3) as c:
        c.execute("SELECT pg_notify(%s, %s)", (channel, payload))


def register(body: dict, url: str) -> Dict[str, Any]:
    """Upsert by explicit worker id; unnamed workers may reuse a URL row."""
    with _LOCK:
        wid = body.get("worker_id")
        if not wid:
            wid = next((k for k, w in _WORKERS.items() if w.get("url") == url),
                       None) or uuid.uuid4().hex
        w = _WORKERS.setdefault(wid, {"id": wid, "registered_at": _now()})
        for k in REGISTER_FIELDS + HEARTBEAT_FIELDS:
            if k in body:
                w[k] = body[k]
        w["url"] = url
        w["models"] = list(w.get("models") or [])
        w["last_seen"] = _now()
        out = dict(w)
    _bump()
    return out


def heartbeat(worker_id: str, body: dict, url: str) -> Optional[Dict[str, Any]]:
    """Refresh a worker; None when the id is unknown (-> 410, re-register)."""
    with _LOCK:
        w = _WORKERS.get(worker_id)
        if w is None:
            return None
        for k in HEARTBEAT_FIELDS:
            if k in body:
                w[k] = body[k]
        w["url"] = url
        w["last_seen"] = _now()
        out = dict(w)
    _bump()
    return out


def stamp_picked(worker_id: str) -> None:
    with _LOCK:
        if worker_id in _WORKERS:
            _WORKERS[worker_id]["last_picked"] = _now()


def all_workers() -> List[Dict[str, Any]]:
    with _LOCK:
        workers = {k: dict(w) for k, w in _WORKERS.items()}
    if os.environ.get('HUGPY_CORE_SHARED_PRESENCE') == '1':
        from hugpy_core.intake.store import workers as persisted_workers
        for worker in persisted_workers():
            key = worker['id']
            if worker.get('last_seen', 0) >= workers.get(key, {}).get('last_seen', 0):
                workers[key] = worker
    return list(workers.values())


def lookup_worker(name_or_id: str) -> Optional[Dict[str, Any]]:
    """Exact registry lookup for an explicitly named request target.

    No serving-policy filter belongs here: the caller has already selected the
    worker.  The subsequent relay/provisioning attempt supplies the real result.
    """
    want = str(name_or_id or "").strip()
    if not want:
        return None
    return next((w for w in all_workers()
                 if want in (w.get("id"), w.get("name"))), None)
