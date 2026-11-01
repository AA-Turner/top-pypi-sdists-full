"""find this machine's state folders and registered sessions, and whether a session is bound to this server and key."""

from __future__ import annotations
import hashlib
import time
from pathlib import Path


# ---------------------------------------------------------------------------
# Where things are
# ---------------------------------------------------------------------------


def state_root() -> Path:
    """`$XDG_STATE_HOME/probe` (or `~/.local/state/probe`): this process's own."""
    from probe.sdk import session_marker

    return session_marker.state_dir()


def reports_dir() -> Path:
    return state_root() / "daemon" / "reports"


def _safe(session_id: str) -> str:
    """A session id as the daemon names its files (`daemon.store.store_path`)."""
    return "".join(c for c in session_id if c.isalnum() or c in "-_") or "session"


def service_dir() -> Path | None:
    try:
        from probe.service import paths

        return paths.service_dir()
    except Exception:  # noqa: BLE001 -- no service folder: its sources are skipped
        return None


def registry_sessions() -> list[dict]:
    """The Probe service's registered sessions (`sessions.json`), as stored."""
    folder = service_dir()
    if folder is None:
        return []
    data = read_json(folder / "sessions.json")
    sessions = data.get("sessions") if isinstance(data, dict) else None
    return [s for s in sessions if isinstance(s, dict) and isinstance(s.get("sid"), str)] if isinstance(
        sessions, list) else []


def live_sessions() -> list[dict]:
    """Registered sessions that are not off and whose owner still runs (or, with
    no owner, whose registrant re-registered within the heartbeat TTL)."""
    try:
        from probe.service import procid
        from probe.service.registry import HEARTBEAT_TTL_S
    except Exception:  # noqa: BLE001
        return []
    now = time.time()
    live = []
    for session in registry_sessions():
        if session.get("mode") == "off":
            continue
        owner = session.get("owner")
        if isinstance(owner, dict):
            try:
                if procid.alive(int(owner.get("pid") or 0), str(owner.get("start_time") or "")) is False:
                    continue
            except Exception:  # noqa: BLE001 -- unreadable: counted live, as the registry does
                pass
        elif now - float(session.get("heartbeat_at") or 0) >= HEARTBEAT_TTL_S:
            continue
        live.append(session)
    return live


def session_state_root(sid: str) -> Path:
    """The state folder a session registered with the service (plan D13), else
    this process's own."""
    for session in registry_sessions():
        if session.get("sid") == sid and isinstance(session.get("state_dir"), str):
            return Path(session["state_dir"])
    return state_root()


def daemon_key() -> str | None:
    try:
        from probe.sdk.settings.settings import load_context

        key = (load_context() or {}).get("companion_token")
    except Exception:  # noqa: BLE001 -- an unreadable config holds no key
        return None
    return key if isinstance(key, str) and key else None


def base_url() -> str | None:
    try:
        from probe.sdk.settings.settings import resolve

        return resolve().base_url
    except Exception:  # noqa: BLE001
        return None


def bound(sid: str, root: Path | None = None) -> bool:
    """Is this session's daemon trace folder recorded under THIS server and THIS
    daemon key? The trace shipper's rule (`daemon.shipper.bound_here`), read
    only: a session another account recorded on this machine is not."""
    key, url = daemon_key(), base_url()
    if not key or not url:
        return False
    folder = (root or session_state_root(sid)) / "daemon" / "sessions" / _safe(sid)
    meta = read_json(folder / "meta.json")
    key_id = hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]
    return isinstance(meta, dict) and meta.get("base_url") == url.rstrip("/") and meta.get("key") == key_id


def tap_log_paths(sid: str) -> list[tuple[str, Path]]:
    """Each coding agent's tap log for this session, with the agent's id
    (recorder and supervisor; hosted recorder threads write there too)."""
    found = []
    try:
        from probe.foundation.harness_registry import get_registry

        for harness in get_registry().captured():
            if harness.capture is None:
                continue
            path = harness.capture.state_dir() / "logs" / f"{_safe(sid)}.log"
            if path.is_file():
                found.append((harness.id, path))
    except Exception:  # noqa: BLE001 -- no registry: no tap logs
        pass
    return found
from probe.shared.reports.logs import read_json  # noqa: E402 -- pieces need each other; the front door loads this one first
