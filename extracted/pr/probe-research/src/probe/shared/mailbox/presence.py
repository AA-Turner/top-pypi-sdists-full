"""who serves a session now: reader on/off, worker lock, finishing/hand-over marks, reader health, hint-lane and deliverer heartbeats."""

from __future__ import annotations
import os
import time
from pathlib import Path

from probe.foundation.compat.compat import StrEnum
#: A deliverer touches its `alive/<sid>.json` at most this often.
ALIVE_EVERY_S = 30.0


def enabled(env: "dict[str, str] | None" = None, *, source: "str | None" = None) -> bool:
    """Is the reader on for coding agent `source` (a harness registry id)?
    Yes when the wizard's "Who records" row put that agent on the daemon profile
    (`session_marker.recorder`), or when `PROBE_DAEMON_READS=on` (the developer
    override the benches use). Without a source only the override counts."""
    value = (env if env is not None else os.environ).get(ENV_READS, "")
    if value.strip().lower() in ("1", "on", "true", "yes"):
        return True
    if not source:
        return False
    from probe.sdk import session_marker

    try:
        return session_marker.recorder(source) == session_marker.RECORDER_DAEMON
    except Exception:  # noqa: BLE001 - an unreadable config is today's profile
        return False


def worker_alive(session_id: str) -> bool:
    """Does a daemon worker hold this session's lock right now? (A free lock is
    taken for an instant and let go: nobody holds it.)"""
    from probe._shared import oscompat as fcntl  # fcntl.flock, or msvcrt on Windows

    from probe.daemon.store.store import store_path

    path = store_path(session_id).with_suffix(".lock")
    if not path.exists():
        return False
    try:
        with path.open("a") as handle:
            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                return True
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            return False
    except OSError:
        return False


def finishing_path(session_id: str) -> Path:
    """Written by a worker when its session ended and it is finishing its queue;
    removed when it exits. A resumed session's `probe ask` reads it."""
    from probe.daemon.store.store import store_path

    return store_path(session_id).with_suffix(".finishing")


def handover_path(session_id: str) -> Path:
    """Written by a resumed session's worker waiting for the lock: the finishing
    worker hands over at its next model round instead of draining its queue."""
    from probe.daemon.store.store import store_path

    return store_path(session_id).with_suffix(".handover")


def finishing(session_id: str) -> bool:
    return finishing_path(session_id).exists()


def status_path(session_id: str) -> Path:
    """The reader's health (`reader_lane.write_status`): the hooks show the
    researcher one line when its state changes."""
    return root() / "status" / f"{_safe(session_id)}.json"


class Status(StrEnum):
    """The reader's health as `status_path` records it."""

    OK = "ok"
    FAILING = "reader_failing"
    TURN_STOPPED = "reader_turn_stopped"
    READS_UNAVAILABLE = "reads_unavailable"


#: The daemon itself is down (its lease is not live): a state of the worker, not the reader.
DAEMON_STOPPED = "daemon_stopped"

#: What the RESEARCHER sees when something fails (the approved text:
#: `~/daemon-prompts/reads/researcher-facing/failure-messages.NEW.md`) - a hook
#: `systemMessage` once when the state changes, and `probe doctor`. Never in the
#: model's context.
FAILURE_MESSAGES = {
    DAEMON_STOPPED: "Probe daemon stopped: {reason}. Recording and reads resume when it restarts.",
    Status.FAILING: "Probe daemon's reader failing: {reason}.",
    Status.TURN_STOPPED: "Probe daemon's reader stopped a turn: {why}.",
    Status.READS_UNAVAILABLE: "Probe reads unavailable: {reason}.",
    Status.OK: "Probe daemon is running again.",
}
#: The states after which "running again" is worth saying (a stopped turn is an
#: event, not an outage).
OUTAGES = (DAEMON_STOPPED, Status.FAILING, Status.READS_UNAVAILABLE)


def read_status(session_id: str) -> dict:
    """The reader's recorded health: {state, reason, since}; {} if none."""
    data = _read_json(status_path(session_id))
    return data if isinstance(data, dict) else {}


def researcher_line(state: str, *, reason: str = "") -> str:
    """The one line the researcher sees for `state` ("" for an unknown state)."""
    text = FAILURE_MESSAGES.get(state)
    if text is None:
        return ""
    return text.format(reason=reason or "unknown", why=reason or "unknown")


def hints_live_path(session_id: str) -> Path:
    """Touched by the Probe service's hint lane while it serves the session
    (`service.hints.HintLane`); its age tells the session's daemon whether a
    hint covers a prompt (`model.hints_live`)."""
    return root() / "hints" / f"{_safe(session_id)}.live"


def hints_window_path(session_id: str) -> Path:
    """Touched by the Probe service's hint lane only while its WINDOW hints work
    for the session (plan hints-window-trigger W3, `HintLane._window_works`:
    its harness shows a hint mid-turn, the lane reads its transcript and looked
    at its work lately, its server and key answered a window lookup as one, and
    fewer than two window lookups in a row failed); its age tells the session's
    daemon whether the reader's 30-minute check-ins are covered
    (`model.window_hints_live`). An older service never writes it, so a mixed
    install keeps its check-ins."""
    return root() / "hints" / f"{_safe(session_id)}.window"


def hints_delivery_path(session_id: str) -> Path:
    """The Probe service's hint lane's last word on whether its hints reach the
    session's agent (`service.hints.delivery_receipt`), for `probe doctor`."""
    return root() / "hints" / f"{_safe(session_id)}.delivery"


def write_hints_delivery(session_id: str, receipt: dict) -> None:
    try:
        _write_json(hints_delivery_path(session_id), receipt)
    except (OSError, Late):
        pass


def read_hints_deliveries() -> "dict[str, dict]":
    """Every session's `hints_delivery_path` under this root: session id -> receipt."""
    out: dict[str, dict] = {}
    folder = root() / "hints"
    for path in folder.glob("*.delivery") if folder.is_dir() else ():
        data = _read_json(path)
        if isinstance(data, dict):
            out[path.stem] = data
    return out


def alive_path(session_id: str) -> Path:
    """A deliverer's heartbeat for the session (`touch_alive`)."""
    return root() / "alive" / f"{_safe(session_id)}.json"


def touch_alive(session_id: str, *, by: str, now: "float | None" = None) -> None:
    """A deliverer runs for the session: its heartbeat, at most every
    ALIVE_EVERY_S. Never raises (a deliverer that cannot write still delivers)."""
    now = time.time() if now is None else now
    path = alive_path(session_id)
    try:
        if now - path.stat().st_mtime < ALIVE_EVERY_S:
            return
    except OSError:
        pass
    try:
        _write_json(path, {"by": by, "at": now})
    except (OSError, Late):
        pass


def read_alive(session_id: str) -> "dict | None":
    """The session's deliverer heartbeat, or None (no deliverer has written one:
    none ran, or one from before heartbeats)."""
    data = _read_json(alive_path(session_id))
    return data if isinstance(data, dict) and isinstance(data.get("at"), (int, float)) else None
from probe.shared.mailbox.layout import ENV_READS, Late, _read_json, _safe, _write_json, root  # noqa: E402 -- pieces need each other; the front door loads this one first
