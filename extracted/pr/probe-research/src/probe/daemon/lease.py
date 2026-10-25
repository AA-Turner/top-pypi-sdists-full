"""The write lease, in the tap's own file format (`tap/companion_lease.py`).

While the lease is live and the switch reads `daemon`, the `probe` CLI refuses
the coding agent's ambient writes: the daemon records. A session the researcher
set inline (`/probe inline`, state `full`), or a confirmed quota handoff (`full`
or `read-only` plus an inline marker), stops the daemon the way `off` does:
the worker releases the lease and exits (`inline`). When the daemon is down, hung or unauthorized the
lease lapses or is released with a reason, and the agent records again. v2
renews it on PROGRESS -- after every model round and every write -- and checks it
before every write (R11), so a long healthy bite never loses it mid-way. The
next version (D12) deletes the lease.
"""

from __future__ import annotations

import json
import os
import tempfile
import time
from pathlib import Path

LEASE_VERSION = 1
WRITER = "daemon"
#: The switch state in which the daemon (and only the daemon) records a session.
STATE_DAEMON = "daemon"
LEASE_TTL_SECONDS = 240.0
REASON_STOPPED = "stopped"
REASON_UNAUTHORIZED = "unauthorized"
REASON_BUDGET = "budget"
REASON_GATEWAY = "gateway"
REASON_ERROR = "error"
#: The machine's disk is full: not a worker bug, and no failure the Probe
#: service reports (`service.watch.LEASE_FAILURES`).
REASON_DISK_FULL = "disk_full"
#: A resumed session's worker took over (`worker.session_lock`); it renews at once.
REASON_HANDOVER = "handover"


def sessions_dir() -> Path:
    xdg = os.environ.get("XDG_STATE_HOME")
    base = Path(xdg) if xdg else Path.home() / ".local" / "state"
    return base / "probe" / "sessions"


def lease_path(session_id: str) -> Path:
    return sessions_dir() / (session_id + ".writer")


def _publish(path: Path, payload: dict) -> bool:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(payload, handle)
            os.replace(tmp, path)
        except BaseException:
            try:
                os.unlink(tmp)
            except OSError:
                pass
            raise
        return True
    except OSError:
        return False


def renew(session_id: str, *, now: float | None = None, ttl: float = LEASE_TTL_SECONDS) -> bool:
    at = time.time() if now is None else now
    return _publish(lease_path(session_id), {"v": LEASE_VERSION, "writer": WRITER, "pid": os.getpid(),
                                             "expires_at": at + ttl, "renewed_at": at, "reason": None})


def release(session_id: str, reason: str, *, now: float | None = None, offline: bool = False) -> bool:
    """Hand writing back to the agent, saying why. `offline`: the machine had
    no network at all (`probe._shared.offline`), which the Probe service never
    reports (`service.watch.lease_condition`)."""
    at = time.time() if now is None else now
    record = {"v": LEASE_VERSION, "writer": WRITER, "pid": os.getpid(),
              "expires_at": at, "renewed_at": at, "reason": reason}
    if offline:
        record["offline"] = True
    return _publish(lease_path(session_id), record)


def held(session_id: str, *, now: float | None = None) -> bool:
    """Do WE hold a live lease? Checked before every write."""
    try:
        data = json.loads(lease_path(session_id).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    at = time.time() if now is None else now
    return (isinstance(data, dict) and data.get("pid") == os.getpid() and data.get("reason") is None
            and float(data.get("expires_at") or 0) > at)


def session_state(session_id: str) -> str | None:
    try:
        raw = (sessions_dir() / (session_id + ".state")).read_text(encoding="utf-8")
    except OSError:
        return None
    return raw.strip().lower() or None


STATE_READ_ONLY = "read-only"


def daemon_profile(session_id: str) -> bool:
    """Did the lean daemon-profile plugin start this session (`<sid>.profile`)?"""
    try:
        raw = (sessions_dir() / (session_id + ".profile")).read_text(encoding="utf-8")
    except OSError:
        return False
    return raw.strip().lower() == "daemon"


def reads_only(session_id: str, state: str | None = None) -> bool:
    """`read only (daemon)` (Richard 2026-09-29): the switch reads `read-only` in a
    daemon-profile session. The reader keeps reading; the writer records nothing."""
    state = session_state(session_id) if state is None else state
    return state == STATE_READ_ONLY and daemon_profile(session_id) and not inline(session_id, state)


def state_changed_at(session_id: str) -> float | None:
    """When the session's switch was last written (`<sid>.state`'s mtime), or None."""
    try:
        return (sessions_dir() / (session_id + ".state")).stat().st_mtime
    except OSError:
        return None


def inline(session_id: str, state: str | None = None) -> bool:
    """`/probe inline` (Richard 2026-10-06): the researcher handed Probe to the
    agent, and the daemon is off. The format is `session_marker`'s; this only
    asks it."""
    from probe.sdk import session_marker

    return session_marker.is_inline(session_id, session_state(session_id) if state is None else state)


def records(session_id: str, state: str | None = None) -> bool:
    """Does the WRITER record this session: the switch reads `daemon`."""
    state = session_state(session_id) if state is None else state
    return state == STATE_DAEMON


def worker_wanted(session_id: str, state: str | None = None) -> bool:
    """Does this session want a worker: `daemon` or `read only (daemon)`. Never
    `off` and never `on (inline)`, where the agent reads and writes itself."""
    state = session_state(session_id) if state is None else state
    return records(session_id, state) or reads_only(session_id, state)


def may_write(session_id: str, *, now: float | None = None) -> str | None:
    """None when THIS process may write for the session now, else one line saying why not.

    Every condition is read fresh from disk, nothing is renewed here: the lease
    file names this process, carries no release reason, has not expired, AND the
    writer still records the session (`records`: the switch reads `daemon`).
    A tool checks this before it acts; a renew-then-check would undo the very
    release it is meant to notice.
    """
    state = session_state(session_id)
    if not records(session_id, state):
        return (f"the researcher moved the switch to `{state}`" if state else
                "the session's switch cannot be read") + ", so the daemon no longer records it"
    try:
        data = json.loads(lease_path(session_id).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return "this daemon holds no write lease for the session"
    if not isinstance(data, dict) or data.get("pid") != os.getpid():
        return "another daemon process holds the session's write lease"
    if data.get("reason") is not None:
        return f"the write lease was released ({data.get('reason')})"
    try:
        expires = float(data.get("expires_at") or 0)
    except (TypeError, ValueError):
        expires = 0.0
    if expires <= (time.time() if now is None else now):
        return "the write lease expired"
    return None
