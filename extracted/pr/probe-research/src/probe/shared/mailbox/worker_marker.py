"""the running worker's marker: does it take writer requests, does it read the service's run-alert hand-off."""

from __future__ import annotations
import os
from pathlib import Path


def worker_marker_path(session_id: str) -> Path:
    # A dot file: the Stop hook's bash fast path globs `w*.json` for open
    # requests, and a marker it matched would start Python on every Stop.
    return requests_dir(session_id) / ".worker.json"


def _accepts_record(pid: "int | None") -> dict:
    return {"pid": os.getpid() if pid is None else pid, "requests": 1, "request_chars": REQUEST_MAX_CHARS}


def mark_worker_accepts(session_id: str, pid: "int | None" = None) -> None:
    """The running worker takes requests: written at its start, removed at its end."""
    _write_json(worker_marker_path(session_id), _accepts_record(pid))


def worker_request_chars(session_id: str) -> int:
    """The longest request the session's running worker takes whole: its marker's
    `request_chars`, else LEGACY_REQUEST_MAX_CHARS (a worker from before it)."""
    data = _read_json(worker_marker_path(session_id)) or {}
    n = data.get("request_chars")
    if isinstance(n, bool) or not isinstance(n, int) or n <= 0:
        return LEGACY_REQUEST_MAX_CHARS
    return min(n, REQUEST_MAX_CHARS)


def keep_worker_marker(session_id: str, *, config: "str | None" = None) -> bool:
    """The running worker's every poll: its marker again when it is gone, with
    its run-alert offer (`config`, `offer_run_alerts`), in one write. Without
    one `probe ask --writer` reads the live worker as one from before requests,
    and another worker's start-up sweep may take the session
    (`sweep_stale_sessions`): an SDK's dead-run recovery deleted the whole
    `requests/` folder (#3616). True when it was written."""
    if worker_marker_path(session_id).exists():
        return False
    _write_json(worker_marker_path(session_id),
                {**_accepts_record(None), **({"run_alerts": 1, "config": config} if config else {})})
    return True


def clear_worker_accepts(session_id: str, pid: "int | None" = None) -> None:
    """Remove the marker -- only this worker's own (a newer worker may have written it since)."""
    data = _read_json(worker_marker_path(session_id))
    if data is not None and data.get("pid") == (os.getpid() if pid is None else pid):
        worker_marker_path(session_id).unlink(missing_ok=True)


def offer_run_alerts(session_id: str, config: "str | None", pid: "int | None" = None) -> bool:
    """Say in this worker's marker that it reads the run-alert answers the Probe
    service leaves it (`alerts_handoff_path`), polled with the daemon key of
    `config` (the CLI config this worker reads); `None` takes that back. Only
    this worker's own marker changes (a newer worker may have written it
    since). True when it was written."""
    data = _read_json(worker_marker_path(session_id))
    if data is None or data.get("pid") != (os.getpid() if pid is None else pid):
        return False
    data.pop("run_alerts", None)
    data.pop("config", None)
    if config:
        data["run_alerts"] = 1
        data["config"] = config
    _write_json(worker_marker_path(session_id), data)
    return True


def alerts_handoff_path(session_id: str) -> Path:
    """Where the Probe service leaves this session's run alerts as the server
    answered them (`probe.service.watch.alertpoll`): `{sid, polled_at, alerts (a
    listing or null), refused_until (null or epoch seconds), every (seconds
    between its polls), pid}`."""
    return root() / "alerts" / f"{_safe(session_id)}.json"


def read_alerts_handoff(session_id: str) -> "dict | None":
    """The service's last hand-off for this session, when it is one (its own
    sid, a numeric `polled_at`); None else."""
    data = _read_json(alerts_handoff_path(session_id))
    if not data or data.get("sid") != session_id:
        return None
    polled = data.get("polled_at")
    if isinstance(polled, bool) or not isinstance(polled, (int, float)):
        return None
    alerts = data.get("alerts")
    if alerts is not None and not isinstance(alerts, list):
        return None
    return data


def accepts_requests(session_id: str) -> bool:
    """Does the session's running worker take requests? Its marker names a live
    process: a worker from before requests never writes one, and a marker left
    by a worker that died names a process that is gone."""
    data = _read_json(worker_marker_path(session_id))
    if data is None or data.get("requests") != 1:
        return False
    try:
        pid = int(data.get("pid"))
        from probe._shared import oscompat  # os.kill(pid, 0) answers nothing on Windows

        oscompat.probe_pid(pid)
    except (TypeError, ValueError, ProcessLookupError):
        return False
    except PermissionError:
        return True  # alive, another user's: not ours to judge
    return True
from probe.shared.mailbox.asks import LEGACY_REQUEST_MAX_CHARS, REQUEST_MAX_CHARS, requests_dir  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.mailbox.layout import _read_json, _safe, _write_json, root  # noqa: E402 -- pieces need each other; the front door loads this one first
