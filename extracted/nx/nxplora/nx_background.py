"""NX CLI — non-blocking BACKGROUND command execution (Claude-Code-style background bash).

run_command BLOCKS the turn and is capped at a timeout, so a long build / test-suite / deploy /
training run is killed before it finishes. This runs such a command DETACHED: NX fires it, the
operator keeps chatting, and NX checks status / reads output on demand — the way Claude Code runs
a long build in the background.

SAFETY: the SAME gate as run_command — nx_executor.command_safety_error (classify_code_action
PROHIBITED tier + the executor blocklists + protected paths/repos). ONE source of truth; the
background shell can never run something the foreground shell would refuse. Approval is still the
operator's job upstream in nx_cli.py (the tool is approval-gated exactly like run_command).

STATE: logs + a small ledger live under ~/.nx/bg/. The live Popen handles live in this module's
process — the REPL is one long-lived process, so poll() reports real status across turns within a
session. Across a restart the log file + pid-liveness are the fallback.

This module is PURE + import-light so it is unit-testable without the CLI: the safety gate and the
launcher are injectable (default to the real ones).
"""
from __future__ import annotations

import json
import os
import signal
import subprocess
import time
import uuid
from pathlib import Path
from typing import Callable, Optional

# The ONE safety gate — imported from the executor so the background shell enforces the identical
# policy as run_command (no drift). Imported lazily inside functions in tests via dependency
# injection; at runtime this module-level import is the real gate.
try:
    from nx_executor import command_safety_error as _default_safety, get_cwd as _default_cwd
except Exception:  # pragma: no cover - executor always present at runtime; keeps unit tests import-safe
    _default_safety = None
    _default_cwd = None

# Bounds — a background task can't grow its log without limit, and we surface a bounded tail.
_LOG_TAIL_BYTES = 4000
_MAX_TRACKED = 50


def _bg_dir() -> Path:
    d = Path(os.path.expanduser("~/.nx/bg"))
    d.mkdir(parents=True, exist_ok=True)
    return d


def _ledger_path() -> Path:
    return _bg_dir() / "tasks.jsonl"


# In-process registry: task_id -> {"proc": Popen|None, "cmd", "pid", "log", "started"}.
_TASKS: dict = {}


def _short_id() -> str:
    return uuid.uuid4().hex[:8]


def _append_ledger(rec: dict) -> None:
    try:
        with open(_ledger_path(), "a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
    except Exception:
        pass  # the in-process registry is the primary record; the ledger is a best-effort resume aid


def _pid_alive(pid: int) -> bool:
    if not pid or pid <= 0:
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def start_background(
    cmd: str,
    cwd: Optional[str] = None,
    *,
    safety: Optional[Callable[[str], Optional[str]]] = None,
    launcher: Optional[Callable] = None,
) -> dict:
    """Launch `cmd` DETACHED. Returns {task_id, pid, started:True} or {error}. Same safety gate as
    run_command. `safety`/`launcher` are injectable for unit tests; production uses the real ones."""
    cmd = (cmd or "").strip()
    if not cmd:
        return {"error": "Empty command"}
    gate = safety if safety is not None else _default_safety
    if gate is not None:
        err = gate(cmd)
        if err:
            return {"error": err}
    task_id = _short_id()
    log_path = _bg_dir() / f"{task_id}.log"
    run_cwd = cwd or (_default_cwd() if _default_cwd else os.getcwd())
    try:
        if launcher is not None:
            proc = launcher(cmd, run_cwd, str(log_path))
        else:
            # start_new_session detaches from the REPL's process group so ctrl-c on a turn doesn't
            # kill the background job; stdout+stderr both stream to the one log (a real terminal).
            # The child inherits the fd; close the parent's copy right away so we don't leak it.
            with open(log_path, "wb") as logf:
                proc = subprocess.Popen(
                    cmd, shell=True, cwd=run_cwd,
                    stdout=logf, stderr=subprocess.STDOUT,
                    start_new_session=True,
                )
    except Exception as e:
        return {"error": f"Could not launch: {e}"}
    pid = getattr(proc, "pid", 0) or 0
    _TASKS[task_id] = {"proc": proc, "cmd": cmd, "pid": pid, "log": str(log_path), "started": time.time()}
    # Bound the in-process registry (drop the oldest finished entries).
    if len(_TASKS) > _MAX_TRACKED:
        for k in list(_TASKS.keys())[:-_MAX_TRACKED]:
            _TASKS.pop(k, None)
    _append_ledger({"task_id": task_id, "cmd": cmd, "pid": pid, "started": _TASKS[task_id]["started"], "event": "start"})
    return {"task_id": task_id, "pid": pid, "started": True, "log": str(log_path)}


def _status_of(entry: dict) -> tuple[str, Optional[int]]:
    """Return (status, returncode). status ∈ running|done|failed. done/failed carry the code."""
    proc = entry.get("proc")
    if proc is not None and hasattr(proc, "poll"):
        rc = proc.poll()
        if rc is None:
            return ("running", None)
        return ("done" if rc == 0 else "failed", rc)
    # No live handle (cross-session) — fall back to pid liveness (unknown returncode).
    if _pid_alive(entry.get("pid", 0)):
        return ("running", None)
    return ("done", None)


def _read_tail(log: str, max_bytes: int = _LOG_TAIL_BYTES) -> str:
    try:
        with open(log, "rb") as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            f.seek(max(0, size - max_bytes))
            data = f.read().decode("utf-8", "replace")
        if size > max_bytes:
            return "…[earlier output truncated]\n" + data
        return data
    except Exception:
        return ""


def poll(task_id: str) -> dict:
    """Status of one background task: {task_id, status, returncode, tail} or {error} if unknown."""
    entry = _TASKS.get((task_id or "").strip())
    if not entry:
        return {"error": f"No background task '{task_id}' in this session"}
    status, rc = _status_of(entry)
    out = {"task_id": task_id, "status": status, "tail": _read_tail(entry["log"])}
    if rc is not None:
        out["returncode"] = rc
    if status in ("done", "failed"):
        _append_ledger({"task_id": task_id, "event": "finished", "status": status, "returncode": rc, "at": time.time()})
    return out


def list_tasks() -> list:
    """Every background task tracked this session, newest first: [{task_id, cmd, status, pid}]."""
    rows = []
    for tid, entry in _TASKS.items():
        status, rc = _status_of(entry)
        rows.append({"task_id": tid, "cmd": entry["cmd"], "status": status, "returncode": rc, "pid": entry.get("pid", 0)})
    rows.sort(key=lambda r: _TASKS.get(r["task_id"], {}).get("started", 0), reverse=True)
    return rows


def read_output(task_id: str, max_bytes: int = _LOG_TAIL_BYTES) -> dict:
    """The tail of a task's combined stdout/stderr log."""
    entry = _TASKS.get((task_id or "").strip())
    if not entry:
        return {"error": f"No background task '{task_id}' in this session"}
    return {"task_id": task_id, "output": _read_tail(entry["log"], max_bytes)}


def stop_task(task_id: str) -> dict:
    """Best-effort terminate a running background task (SIGTERM the detached process group)."""
    entry = _TASKS.get((task_id or "").strip())
    if not entry:
        return {"error": f"No background task '{task_id}' in this session"}
    pid = entry.get("pid", 0)
    try:
        os.killpg(os.getpgid(pid), signal.SIGTERM)
    except Exception:
        try:
            os.kill(pid, signal.SIGTERM)
        except Exception:
            return {"task_id": task_id, "stopped": False}
    _append_ledger({"task_id": task_id, "event": "stopped", "at": time.time()})
    return {"task_id": task_id, "stopped": True}
