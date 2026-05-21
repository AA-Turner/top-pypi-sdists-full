#!/usr/bin/env python3
"""Continuously aggregate every drydock TUI's messages.jsonl into a
single rolling JSONL log so any watcher can see the full picture.

One worker per running drydock. New sessions are picked up
automatically by re-scanning the session-publishing files every 10s:

  - `~/.drydock/sessions_by_pid/<pid>.txt`
  - `~/.drydock/current_session.txt`            (legacy global)
  - `*/.drydock/current_session.txt`            (per-project, where
                                                 we know the cwd)

Output: a single `~/.drydock/all_tui.jsonl` with one record per real
message — each record is the original JSON plus the session_id and a
captured-at timestamp. The `tui_watch.py` companion script tails this
file and surfaces findings.
"""
from __future__ import annotations

import json
import os
import signal
import sys
import threading
import time
from pathlib import Path

OUT_PATH = Path.home() / ".drydock" / "all_tui.jsonl"
PID_DIR = Path.home() / ".drydock" / "sessions_by_pid"
GLOBAL_MARKER = Path.home() / ".drydock" / "current_session.txt"
POLL_INTERVAL = 5.0
TAIL_INTERVAL = 1.0

# Each entry: session_dir -> (offset_in_messages_jsonl, last_mtime)
_state: dict[str, tuple[int, float]] = {}
_state_lock = threading.Lock()
_stop = threading.Event()


def _emit(record: dict) -> None:
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("a") as f:
        f.write(json.dumps(record, default=str) + "\n")


def _tail_one(session_dir: Path) -> None:
    mjsonl = session_dir / "messages.jsonl"
    if not mjsonl.exists():
        return
    key = str(session_dir)
    with _state_lock:
        offset, _ = _state.get(key, (0, 0.0))
    try:
        size = mjsonl.stat().st_size
    except OSError:
        return
    if size < offset:
        # File truncated/rotated — rewind.
        offset = 0
    if size == offset:
        return
    try:
        with mjsonl.open() as f:
            f.seek(offset)
            for line in f:
                line = line.rstrip("\n")
                if not line:
                    continue
                try:
                    parsed = json.loads(line)
                except Exception:
                    continue
                _emit({
                    "captured_at": time.time(),
                    "session_id": session_dir.name,
                    "session_dir": key,
                    "msg": parsed,
                })
            new_offset = f.tell()
    except OSError:
        return
    with _state_lock:
        _state[key] = (new_offset, time.time())


SESSION_ROOT = Path.home() / ".drydock" / "logs" / "session"
ACTIVE_WINDOW_SEC = 120.0


def _is_noise_path(p: Path) -> bool:
    """Skip pytest-internal session dirs. The drydock test suite spawns
    short-lived sessions under /tmp/pytest-of-*/pytest-N/... that produce
    deliberate tool errors (e.g. grep `/nonexistent` to verify the error
    response). Those polluted ~/.drydock/tui_findings.jsonl with 22+
    fake findings; the bug-finding pipeline was chasing ghosts.
    Observed 2026-05-20."""
    s = str(p)
    return ("/pytest-of-" in s
            or "/tmp/pytest-" in s
            or "/popen-gw" in s)


def _discover_sessions() -> set[Path]:
    """Return the set of session_dirs currently being written by an
    active drydock process.

    We trust three sources, broadest-first to catch every running TUI:

    1. Any session_dir whose messages.jsonl was modified in the last
       ACTIVE_WINDOW_SEC seconds. This is the catch-all that doesn't
       depend on the publish-current-session code firing — useful
       because some drydock builds skip the per-pid/per-project write
       for reasons we haven't pinned down yet.
    2. `~/.drydock/sessions_by_pid/<pid>.txt` for living PIDs.
    3. `~/.drydock/current_session.txt` (legacy global).

    Pytest-internal session dirs are filtered out (see _is_noise_path).
    """
    found: set[Path] = set()
    now = time.time()

    # (1) recent-activity scan — most robust signal we have.
    if SESSION_ROOT.is_dir():
        try:
            for entry in SESSION_ROOT.iterdir():
                if not entry.is_dir():
                    continue
                if _is_noise_path(entry):
                    continue
                mjsonl = entry / "messages.jsonl"
                if not mjsonl.exists():
                    continue
                try:
                    if now - mjsonl.stat().st_mtime <= ACTIVE_WINDOW_SEC:
                        found.add(entry)
                except OSError:
                    continue
        except OSError:
            pass

    # (2) per-pid markers
    if PID_DIR.is_dir():
        for pidfile in PID_DIR.iterdir():
            if pidfile.suffix != ".txt":
                continue
            try:
                pid = int(pidfile.stem)
            except ValueError:
                continue
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                continue  # stale
            except PermissionError:
                pass  # alive
            try:
                p = Path(pidfile.read_text().strip())
                if p.is_dir() and not _is_noise_path(p):
                    found.add(p)
            except Exception:
                continue

    # (3) legacy global
    try:
        p = Path(GLOBAL_MARKER.read_text().strip())
        if p.is_dir() and not _is_noise_path(p):
            found.add(p)
    except Exception:
        pass
    return found


def _loop() -> None:
    _emit({"captured_at": time.time(), "event": "capture_started",
           "pid": os.getpid()})
    last_discovery = 0.0
    sessions: set[Path] = set()
    while not _stop.is_set():
        now = time.time()
        if now - last_discovery >= POLL_INTERVAL:
            new = _discover_sessions()
            added = new - sessions
            removed = sessions - new
            for d in added:
                _emit({"captured_at": now, "event": "session_attached",
                       "session_dir": str(d)})
            for d in removed:
                _emit({"captured_at": now, "event": "session_detached",
                       "session_dir": str(d)})
            sessions = new
            last_discovery = now
        for d in list(sessions):
            try:
                _tail_one(d)
            except Exception as e:
                _emit({"captured_at": time.time(), "event": "tail_error",
                       "session_dir": str(d), "error": repr(e)})
        time.sleep(TAIL_INTERVAL)


def main() -> int:
    def _handle(_sig, _frame):
        _stop.set()

    signal.signal(signal.SIGTERM, _handle)
    signal.signal(signal.SIGINT, _handle)
    try:
        _loop()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
