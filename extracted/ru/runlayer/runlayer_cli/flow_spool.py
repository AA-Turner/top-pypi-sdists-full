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
from typing import Any, TypedDict

from runlayer_cli.flow_contract import MAX_FLOWS_PER_ENVELOPE, build_envelope
from runlayer_cli.paths import get_runlayer_dir
from runlayer_cli.safe_parse import parse_json

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
# Byte budget for other hosts' lines a per-host drain writes back (newest
# kept). A host that is never posted to again must not fill the spool and
# starve appends for the host that is.
_MAX_FOREIGN_BYTES = _MAX_SPOOL_BYTES // 4


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


class _Partition(TypedDict):
    flows: list[dict[str, Any]]  # ship in this envelope
    foreign: list[bytes]  # other hosts' raw lines, written back
    dropped: int  # lines lost from this envelope (malformed / stale)
    foreign_trimmed: bool  # foreign lines fell off the byte cap


def _partition(raw: bytes, target_host: str | None) -> _Partition:
    """Split raw spool bytes by destination (rules in ``spool_drain``)."""
    now = time.time()
    flows: list[dict[str, Any]] = []
    foreign: list[bytes] = []
    dropped = 0
    for line in raw.split(b"\n"):
        if not line.strip():
            continue
        # Per-row exception-complete decode: one poisoned row (deep nesting
        # raises RecursionError, not JSONDecodeError) must count as dropped
        # and leave its siblings shippable, not escape to the outer
        # ``except`` and wedge the whole spool.
        outcome = parse_json(line)
        if outcome["error"] is not None:
            dropped += 1
            continue
        summary = outcome["value"]
        if not isinstance(summary, dict):
            dropped += 1
            continue
        ts = summary.get("ts")
        if isinstance(ts, (int, float)) and (now - ts) > _MAX_AGE_SECONDS:
            dropped += 1
            continue
        host = summary.get("target_host")
        if target_host is not None and isinstance(host, str) and host != target_host:
            foreign.append(line + b"\n")
            continue
        flows.append(summary)
    # Keep the newest foreign lines that fit the byte budget, oldest trimmed
    # first. Not counted in ``dropped``: that is another host's loss, not
    # this envelope's.
    kept: list[bytes] = []
    budget = _MAX_FOREIGN_BYTES
    foreign_trimmed = False
    for line in reversed(foreign):
        if len(line) > budget:
            foreign_trimmed = True
            break
        kept.append(line)
        budget -= len(line)
    kept.reverse()
    return _Partition(
        flows=flows, foreign=kept, dropped=dropped, foreign_trimmed=foreign_trimmed
    )


def spool_drain(*, target_host: str | None = None) -> dict[str, Any] | None:
    """Drain spooled flows into a ``client_flows`` envelope, or ``None``.

    Returns ``None`` when the spool is empty, the lock is contended (another
    hook process is draining), or anything fails — callers attach nothing and
    the data waits for the next invocation. Malformed/partial trailing lines
    (crash during append) and entries older than 24 h are discarded; beyond
    ``MAX_FLOWS_PER_ENVELOPE`` the newest flows win and the rest count as
    ``dropped``.

    ``target_host`` (hostname the carrier POST goes to, compared lowercased)
    restricts the drain to summaries stamped with that host plus legacy lines
    with no ``target_host``. Other hosts' lines are written back under the
    same lock — byte-capped (``_MAX_FOREIGN_BYTES``, oldest trimmed first),
    still 24 h-pruned — for a later POST to their own host, so a device with
    a stale ``default_host`` cannot make one deployment ingest another's hook
    failures. ``None`` drains everything.
    """
    try:
        path = _spool_path()
        if not os.path.exists(path):
            return None
        wanted = target_host.lower() if target_host else None
        lock_fd = os.open(_lock_path(), os.O_CREAT | os.O_RDWR, 0o600)
        try:
            if not _try_lock(lock_fd):
                return None
            try:
                with open(path, "rb") as f:
                    raw = f.read()
                part = _partition(raw, wanted)
                flows = part["flows"]
                dropped = part["dropped"]
                # Skip the rewrite when nothing shipped and nothing was
                # pruned (an all-foreign spool is not churned on every hook).
                if flows or dropped or part["foreign_trimmed"]:
                    # Truncate then write with O_APPEND: a hook that appends a
                    # line between the truncate and this write lands after
                    # our bytes instead of being overwritten mid-record. A
                    # line appended between the read and the truncate is
                    # still lost (as before) — a line is never torn.
                    fd = os.open(path, os.O_WRONLY | os.O_TRUNC | os.O_APPEND, 0o600)
                    try:
                        if part["foreign"]:
                            os.write(fd, b"".join(part["foreign"]))
                    finally:
                        os.close(fd)
            finally:
                _unlock(lock_fd)
        finally:
            os.close(lock_fd)

        if len(flows) > MAX_FLOWS_PER_ENVELOPE:
            dropped += len(flows) - MAX_FLOWS_PER_ENVELOPE
            flows = flows[-MAX_FLOWS_PER_ENVELOPE:]
        if not flows:
            return None
        return build_envelope(flows, dropped)
    except Exception:
        return None
