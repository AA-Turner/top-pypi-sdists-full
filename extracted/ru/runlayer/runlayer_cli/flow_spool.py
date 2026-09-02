"""JSONL spool for hook flow summaries (one-shot ``aiwatch hook`` processes).

A hook process has no "next request" of its own, so completed flow summaries
spool to ``~/.runlayer/flow-spool.jsonl`` and the *next* hook invocation drains
the spool into a ``client_flows`` envelope piggybacked on its fire-and-forget
``event`` POST (see ``hook/relay.py``) — lag-one across processes, zero extra
HTTP requests.

Concurrency/safety contract (hooks are on the AI client's critical path and
must never wait):
- Append is a single ``O_APPEND`` write of one line <=4 KB — atomic on POSIX,
  so concurrent hook processes append lock-free.
- Drain takes a NON-blocking exclusive lock on a sidecar ``.lock`` file; if
  another process holds it, drain returns ``None`` immediately.
- The spool is size-capped (sustained growth means the backend is unreachable,
  so the data is low-value) and stale entries are pruned at drain time.

Stdlib-only (cli/AGENTS.md): in the ``aiwatch`` PyInstaller closure.
"""

from __future__ import annotations

import json
import os
import sys
import time
from typing import Any

from runlayer_cli.flow_contract import MAX_FLOWS_PER_ENVELOPE, build_envelope
from runlayer_cli.paths import get_runlayer_dir

if sys.platform == "win32":
    import msvcrt
else:
    import fcntl

_SPOOL_FILENAME = "flow-spool.jsonl"
_LOCK_FILENAME = "flow-spool.lock"

# Skip appends once the spool exceeds this (no drain is keeping up).
_MAX_SPOOL_BYTES = 256 * 1024
# One summary line; anything larger is malformed/bloated and not worth shipping.
_MAX_LINE_BYTES = 4096
# Entries older than this are operationally stale; prune at drain.
_MAX_AGE_SECONDS = 24 * 60 * 60


def _spool_path() -> str:
    return str(get_runlayer_dir() / _SPOOL_FILENAME)


def _lock_path() -> str:
    return str(get_runlayer_dir() / _LOCK_FILENAME)


def spool_append(summary: dict[str, Any]) -> None:
    """Flow sink for the hook path. Best-effort; never raises, never blocks."""
    try:
        line = json.dumps(summary) + "\n"
        data = line.encode("utf-8")
        if len(data) > _MAX_LINE_BYTES:
            return
        path = _spool_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            # Best-effort, per-process cap: concurrent hooks each stat then
            # append lock-free, so the file can overshoot by ~(N procs * line)
            # before they all observe the cap. That bounded overshoot is fine —
            # the cap only exists to stop unbounded growth when the backend is
            # unreachable (drain never runs), not to enforce a hard ceiling.
            if os.stat(path).st_size > _MAX_SPOOL_BYTES:
                return
        except FileNotFoundError:
            pass
        fd = os.open(path, os.O_APPEND | os.O_CREAT | os.O_WRONLY, 0o600)
        try:
            os.write(fd, data)
        finally:
            os.close(fd)
    except Exception:
        pass


def _try_lock(fd: int) -> bool:
    try:
        if sys.platform == "win32":
            msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
        else:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return True
    except OSError:
        return False


def _unlock(fd: int) -> None:
    try:
        if sys.platform == "win32":
            msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
        else:
            fcntl.flock(fd, fcntl.LOCK_UN)
    except OSError:
        pass


def spool_drain() -> dict[str, Any] | None:
    """Drain spooled flows into a ``client_flows`` envelope, or ``None``.

    Returns ``None`` when the spool is empty, the lock is contended (another
    hook process is draining), or anything fails — callers attach nothing and
    the data waits for the next invocation. Malformed/partial trailing lines
    (crash during append) and entries older than 24 h are discarded; beyond
    ``MAX_FLOWS_PER_ENVELOPE`` the newest flows win and the rest count as
    ``dropped``.
    """
    try:
        path = _spool_path()
        if not os.path.exists(path):
            return None
        lock_fd = os.open(_lock_path(), os.O_CREAT | os.O_RDWR, 0o600)
        try:
            if not _try_lock(lock_fd):
                return None
            try:
                with open(path, "rb") as f:
                    raw = f.read()
                # Truncate under the lock: appends racing the drain may slip a
                # line in after the read; acceptable loss (they O_APPEND whole
                # lines, so truncation never corrupts a future line).
                with open(path, "wb"):
                    pass
            finally:
                _unlock(lock_fd)
        finally:
            os.close(lock_fd)

        if not raw:
            return None
        now = time.time()
        flows: list[dict[str, Any]] = []
        dropped = 0
        for line in raw.split(b"\n"):
            if not line.strip():
                continue
            try:
                summary = json.loads(line)
            except (json.JSONDecodeError, UnicodeDecodeError):
                dropped += 1
                continue
            if not isinstance(summary, dict):
                dropped += 1
                continue
            ts = summary.get("ts")
            if isinstance(ts, (int, float)) and (now - ts) > _MAX_AGE_SECONDS:
                dropped += 1
                continue
            flows.append(summary)
        if len(flows) > MAX_FLOWS_PER_ENVELOPE:
            dropped += len(flows) - MAX_FLOWS_PER_ENVELOPE
            flows = flows[-MAX_FLOWS_PER_ENVELOPE:]
        if not flows:
            return None
        return build_envelope(flows, dropped)
    except Exception:
        return None
