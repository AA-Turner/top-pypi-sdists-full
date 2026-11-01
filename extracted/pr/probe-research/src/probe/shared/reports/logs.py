"""read log tails and keep only the lines a report may carry (the service's own, recent)."""

from __future__ import annotations
import json
import os
import re
import time
from pathlib import Path
#: Device logs older than this say nothing about the incident.
LOG_MAX_AGE_S = 24 * 3600
UUID = re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b")

#: The service's own log lines (`service.log`): everything else in that file
#: is a hook host's raw stderr, or another tool's.
_SERVICE_LINE = re.compile(r"^\[[0-9TZ:-]+\] probe-service(?:-guard|-keeper)?\[\d+\]:")
_SERVICE_STAMP = re.compile(r"^\[(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})Z\]")
_DEVICE_STAMP = re.compile(r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}) ")


# ---------------------------------------------------------------------------
# Reading files: tails, never whole logs
# ---------------------------------------------------------------------------


def read_tail(path: Path, cap: int) -> str | None:
    """The last `cap` bytes of `path` as text, None when it cannot be read. A
    tail that starts mid-line loses that clipped first line: half a record can
    hide half a credential from the scrubber. Only a regular file is opened: a
    FIFO where a log should be would block the reader forever."""
    try:
        if not Path(path).is_file():
            return None
        with open(path, "rb") as handle:
            handle.seek(0, os.SEEK_END)
            size = handle.tell()
            start = max(0, size - cap)
            handle.seek(start)
            data = handle.read(cap)
    except OSError:
        return None
    if start > 0:
        newline = data.find(b"\n")
        data = data[newline + 1:] if newline >= 0 else b""
    return data.decode("utf-8", errors="replace")


def read_json(path: Path) -> object | None:
    try:
        if not Path(path).is_file():
            return None
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _stamp_age_s(line: str, now: float) -> float | None:
    """How old a log line is, from its own leading timestamp; None when it has none."""
    import calendar

    match = _SERVICE_STAMP.match(line)
    if match:
        try:
            return now - calendar.timegm(time.strptime(match.group(1), "%Y-%m-%dT%H:%M:%S"))
        except ValueError:
            return None
    match = _DEVICE_STAMP.match(line)
    if match:  # `daemon-errors.log` writes local time (`worker._device_error`)
        try:
            return now - time.mktime(time.strptime(match.group(1), "%Y-%m-%dT%H:%M:%S"))
        except (ValueError, OverflowError):
            return None
    return None


def keep_lines(text: str, *, allowed_sessions: set[str], service_only: bool, now: float,
               max_age_s: float | None = LOG_MAX_AGE_S) -> str:
    """The lines of a SHARED log a report may carry: the service's own lines
    only (`service_only`), none older than `max_age_s`, and a line naming a
    session only when that session is one of `allowed_sessions`."""
    kept: list[str] = []
    home = str(Path.home())
    for line in text.splitlines():
        if not line.strip():
            continue
        if service_only and not _SERVICE_LINE.match(line):
            continue
        if max_age_s is not None:
            age = _stamp_age_s(line, now)
            if age is not None and age > max_age_s:
                continue
        # A UUID in this machine's home folder's path (a scratchpad, a CI job's
        # folder) names no session.
        named = {match.lower() for match in UUID.findall(line.replace(home, "~") if len(home) > 1 else line)}
        if named and not named <= allowed_sessions:
            continue
        kept.append(line)
    return "\n".join(kept) + ("\n" if kept else "")


#: STAFF log tails: name -> cap (plan B1's table).
_TAIL_CAPS = {
    "daemon_errors": 32 * 1024,
    "tap_log": 64 * 1024,
    "worker_output": 64 * 1024,
    "worker_log": 128 * 1024,
    "service_log": 64 * 1024,
    "service_log_1": 32 * 1024,
    "update_log": 32 * 1024,
}


def staff_logs(sid: str | None, allowed: set[str], include_session: bool, now: float,
               skipped: dict[str, str]) -> dict[str, str]:
    """The log tails a STAFF report carries, each scrubbed as one text."""
    logs: dict[str, str] = {}

    def add(name: str, text: str | None) -> None:
        if not text:
            return
        try:
            logs[name] = scrub_for(text, Scope.STAFF)
        except Exception as exc:  # noqa: BLE001 -- withheld, never sent raw
            skipped[name] = f"could not be scrubbed ({type(exc).__name__})"

    errors = read_tail(state_root() / "daemon-errors.log", _TAIL_CAPS["daemon_errors"] * 4)
    if errors:
        add("daemon_errors", _tail_text(keep_lines(errors, allowed_sessions=allowed, service_only=False, now=now),
                                        _TAIL_CAPS["daemon_errors"]))
    folder = service_dir()
    if folder is not None:
        for name, file in (("service_log", "service.log"), ("service_log_1", "service.log.1")):
            text = read_tail(folder / file, _TAIL_CAPS[name] * 4)
            if text:
                add(name, _tail_text(keep_lines(text, allowed_sessions=allowed, service_only=True, now=now),
                                     _TAIL_CAPS[name]))
        add("update_log", read_tail(folder / "update.log", _TAIL_CAPS["update_log"]))
    if sid and include_session:
        root = session_state_root(sid)
        add("worker_output", read_tail(root / "daemon" / f"{_safe(sid)}.log", _TAIL_CAPS["worker_output"]))
        add("worker_log", read_tail(root / "daemon" / "sessions" / _safe(sid) / "worker.log",
                                    _TAIL_CAPS["worker_log"]))
        for index, (_harness, path) in enumerate(tap_log_paths(sid)):
            add("tap_log" if index == 0 else f"tap_log_{index}", read_tail(path, _TAIL_CAPS["tap_log"]))
    return logs


def _tail_text(text: str, cap: int) -> str:
    data = text.encode("utf-8")
    if len(data) <= cap:
        return text
    cut = data[-cap:]
    newline = cut.find(b"\n")
    return cut[newline + 1:].decode("utf-8", errors="replace") if newline >= 0 else ""
from probe.shared.reports.reports import Scope  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.reports.scrub import scrub_for  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.reports.sessions import _safe, service_dir, session_state_root, state_root, tap_log_paths  # noqa: E402 -- pieces need each other; the front door loads this one first
