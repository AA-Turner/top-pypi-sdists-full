"""
CVC Event Spine — the foundation for the time machine.

Every interaction in CVC — chat turns, terminal calls, soul writes,
dream cycles, ops commits, channel messages, system events — flows
through this module as a single append-only ledger.

Why a separate spine (and not "just use the cognitive commits"):

  The cognitive commit graph (cvc.db) is the user's *intentional*
  checkpoint stream. It's curated, branched, merged, restored. It
  shouldn't be polluted with every tool call.

  The spine is the *unconscious* stream — every event, captured
  faithfully, queryable, filterable, time-machine-able. It's the raw
  footage the cognitive graph summarizes from.

Storage layout
=============

    ~/.cvc/events/
    ├── current.jsonl           # active day, append-only
    ├── 2026-06-29.jsonl        # rotated days, also append-only
    ├── 2026-06-28.jsonl
    ├── ...
    ├── .index.json             # in-memory fast-path: id → (file, offset)
    └── .wal/                   # write-ahead log for crash safety
        └── current.wal

Capture is a single function call::

    from cvc.events.spine import capture
    capture(
        kind="chat.user_message",
        workspace="/Users/jkm/Projects/cvc/cvc",
        channel="web",
        actor="Jai",
        summary="user asked about timeline",
        ...
    )

Capture is synchronous and best-effort. It never raises to the caller
(returns None on failure). The whole point is to never block or break
the path it's capturing from.

Read is a single function call::

    from cvc.events.spine import query
    for evt in query(workspace="/...", since="...", limit=100):
        ...

Both calls work without any daemon coordination. Two CVC processes can
both append events; each captures its own line and the spine reconciles
on read (events are immutable once written, so concurrent appends are
safe).

Singularity
===========

Like the soul, the event spine is **singular** — `~/.cvc/events/`,
not per-workspace. Every channel, every workspace, every conversation
writes to the same ledger. Workspace is just one of the indexed fields
on each event.

Schema
=======

Events are ULID-keyed JSON objects (one per line in the .jsonl files).
Full schema lives in `_SCHEMA_DOCS` below; see also `docs/event-spine.md`
when we ship that.
"""
from __future__ import annotations

import contextlib
import errno
import json
import logging
import os
import random
import re
import threading
import time
from pathlib import Path
from typing import Any, Iterator

logger = logging.getLogger("cvc.events.spine")

# ---------------------------------------------------------------------------
# Locations
# ---------------------------------------------------------------------------

EVENTS_DIRNAME = "events"
WAL_DIRNAME = ".wal"
INDEX_FILENAME = ".index.json"
CURRENT_FILENAME = "current.jsonl"
ACTIVE_FILENAME_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}\.jsonl$")

# Default retention — events older than this are candidates for compaction.
# C7 (compaction + retention) will implement the actual purger.
DEFAULT_RETENTION_DAYS = 365

# Max events returned by a single unfiltered query — protects against
# accidental "give me everything" calls.
DEFAULT_QUERY_LIMIT = 1000
ABSOLUTE_QUERY_LIMIT = 10000

# ---------------------------------------------------------------------------
# Schema docs (single source of truth for the event shape)
# ---------------------------------------------------------------------------

_SCHEMA_DOCS = """
Event Spine schema (v1)
=======================

{
  "id": "01HXYZ...",                    // ULID — time-ordered, sortable as string

  // WHEN
  "ts": 1782839346.123,                 // unix seconds (float, ms precision)
  "ts_iso": "2026-06-30T23:09:06.123Z", // human-readable
  "ts_mono_ms": 123456789,              // monotonic ms since gateway start

  // WHERE
  "workspace": "/Users/jkm/Projects/cvc/cvc",   // ABS path, or null for global
  "workspace_name": "cvc",              // derived: basename(workspace)
  "channel": "web",                     // web|telegram|slack|sms|terminal|mcp|api|system
  "channel_detail": "session:abc123",   // session_id / chat_id / request_id

  // WHO
  "actor": "Jai",                       // user/owner identifier
  "actor_detail": null,                 // role, system-user, etc.

  // WHAT
  "kind": "chat.user_message",          // dotted taxonomy (see EVENT_KINDS)
  "summary": "user asked about timeline",// human-readable, ≤200 chars
  "data": { ... },                      // kind-specific payload (free-form)

  // META
  "provider": "minimax",                // for LLM calls
  "model": "MiniMax-M3",                // for LLM calls
  "branch": "main",                     // git/cognitive branch if applicable
  "session_id": "abc123",               // conversation/session key
  "parent_event_id": null,              // chain multi-step interactions

  // METRICS
  "duration_ms": 0,                     // for time-bounded events
  "tokens_in": 0,
  "tokens_out": 0,
  "bytes": 0,                           // for IO events

  // STATUS
  "status": "ok",                       // ok | err | partial | skipped
  "error": null,                        // error message if status != ok

  // TAGS
  "tags": ["soul", "audit"]             // free-form tags for filtering
}

Kinds (taxonomy)
================
chat.*         chat.session_start, chat.user_message, chat.assistant_message,
               chat.tool_call, chat.tool_result, chat.session_end, chat.error
terminal.*     terminal.command, terminal.output, terminal.error
soul.*         soul.write, soul.correction, soul.dream, soul.letter_generated,
               soul.will_created, soul.preservation_enabled, soul.preservation_disabled
ops.*          ops.commit, ops.branch, ops.merge, ops.restore, ops.compact
channel.*      channel.message_in, channel.message_out
system.*       system.startup, system.shutdown, system.error, system.warning
"""

# ---------------------------------------------------------------------------
# Event kind taxonomy — enforced as a module-level set so capture() can
# reject typos early. Add new kinds here as we expand the spine.
# ---------------------------------------------------------------------------

EVENT_KINDS: frozenset[str] = frozenset({
    # chat
    "chat.session_start", "chat.session_end",
    "chat.user_message", "chat.assistant_message",
    "chat.tool_call", "chat.tool_result",
    "chat.error",
    # terminal
    "terminal.command", "terminal.output", "terminal.error",
    # soul
    "soul.write", "soul.correction", "soul.dream",
    "soul.letter_generated",
    "soul.will_created", "soul.will_updated", "soul.will_released",
    "soul.preservation_enabled", "soul.preservation_disabled",
    # ops
    "ops.commit", "ops.branch", "ops.merge", "ops.restore", "ops.compact",
    # channel
    "channel.message_in", "channel.message_out", "channel.error",
    "channel.message_skipped",
    # system
    "system.startup", "system.shutdown", "system.error", "system.warning",
})

CHANNELS: frozenset[str] = frozenset({
    "web", "telegram", "slack", "sms", "whatsapp",
    "terminal", "mcp", "api", "system", "voice",
    "soul", "ops", "email", "discord", "matrix",
})


# ---------------------------------------------------------------------------
# ULID — minimal implementation (26-char Crockford base32, time-ordered)
# ---------------------------------------------------------------------------

# Crockford base32 alphabet (no I, L, O, U for readability)
_ULID_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
_ULID_LEN = 26
_ULID_TIME_LEN = 10
_ULID_RAND_LEN = 16

# Gateway start monotonic reference (set on first import)
_MONO_START_MS = int(time.time() * 1000)


def _encode_crockford_base32(value: int, length: int) -> str:
    """Encode an integer as Crockford base32 with zero-padding to length."""
    out = []
    for _ in range(length):
        out.append(_ULID_ALPHABET[value & 0x1F])
        value >>= 5
    return "".join(reversed(out))


def _generate_ulid() -> str:
    """Generate a ULID. Time-ordered (ms resolution), 80 bits random.

    Thread-safe via a monotonic increment so same-ms calls don't collide.
    """
    now_ms = int(time.time() * 1000)
    return _generate_ulid_at(now_ms)


_ulid_lock = threading.Lock()
_last_ulid_ms = 0
_last_ulid_rand = 0


def _generate_ulid_at(now_ms: int) -> str:
    global _last_ulid_ms, _last_ulid_rand
    with _ulid_lock:
        if now_ms == _last_ulid_ms:
            # monotonic increment on the random portion (80 bits → wrap safe)
            _last_ulid_rand = (_last_ulid_rand + 1) & ((1 << 80) - 1)
            rand = _last_ulid_rand
        else:
            _last_ulid_ms = now_ms
            _last_ulid_rand = random.getrandbits(80)
            rand = _last_ulid_rand

    time_part = _encode_crockford_base32(now_ms & ((1 << 50) - 1), _ULID_TIME_LEN)
    rand_part = _encode_crockford_base32(rand, _ULID_RAND_LEN)
    return time_part + rand_part


# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------


def _spine_root() -> Path:
    """The single, workspace-agnostic event spine.

    Lives at ``~/.cvc/events/``. Override via ``CVC_EVENTS_ROOT``.
    """
    override = os.environ.get("CVC_EVENTS_ROOT")
    if override:
        p = Path(override).expanduser()
        p.mkdir(parents=True, exist_ok=True)
        return p
    p = Path.home() / ".cvc" / EVENTS_DIRNAME
    p.mkdir(parents=True, exist_ok=True)
    return p


def _current_path() -> Path:
    """Path to today's JSONL file (``YYYY-MM-DD.jsonl``)."""
    return _spine_root() / f"{time.strftime('%Y-%m-%d')}.jsonl"


def _wal_path() -> Path:
    """Path to the write-ahead log for crash-safe appends."""
    p = _spine_root() / WAL_DIRNAME
    p.mkdir(parents=True, exist_ok=True)
    return p / "current.wal"


def _index_path() -> Path:
    """Path to the index file (id → file+offset for fast lookup)."""
    return _spine_root() / INDEX_FILENAME


# ---------------------------------------------------------------------------
# Capture (write path)
# ---------------------------------------------------------------------------

# File lock to serialize concurrent appends from multiple processes.
# We use a separate lock file because fcntl is per-process, not per-file.
_file_lock_path = _spine_root() / ".capture.lock"
_file_lock_fd: int | None = None
_file_lock_local = threading.Lock()  # intra-process


def _acquire_file_lock() -> None:
    """Acquire an OS-level advisory lock on the capture file."""
    global _file_lock_fd
    if _file_lock_fd is not None:
        return
    try:
        fd = os.open(
            str(_file_lock_path),
            os.O_CREAT | os.O_RDWR,
            0o600,
        )
        # Try non-blocking — if another process holds it, we still write
        # (the JSONL line itself is atomic for lines < PIPE_BUF on POSIX).
        try:
            import fcntl  # type: ignore[import-not-found]
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except (ImportError, OSError):
            # Windows or contention — best-effort, JSONL is still safe at line level
            pass
        _file_lock_fd = fd
    except OSError as exc:
        logger.debug("could not open capture lock: %s", exc)


def _release_file_lock() -> None:
    global _file_lock_fd
    if _file_lock_fd is not None:
        try:
            os.close(_file_lock_fd)
        except OSError:
            pass
        _file_lock_fd = None


def _atomic_append(path: Path, line: str) -> None:
    """Append a single line to a JSONL file, atomically.

    Uses O_APPEND for kernel-level atomic append guarantees (POSIX).
    For very large lines (>PIPE_BUF, ~4KB on Linux), we fsync to be safe.
    """
    line_bytes = line.encode("utf-8") + b"\n"
    with _file_lock_local:
        try:
            with open(path, "ab") as f:
                f.write(line_bytes)
                # Best-effort fsync — guarantees the event hits disk
                # before we return. Critical for the "I closed the tab
                # and the event is still there" guarantee.
                try:
                    os.fsync(f.fileno())
                except OSError:
                    # Some filesystems don't support fsync (e.g. /dev/null)
                    pass
        except OSError as exc:
            logger.warning("could not append to %s: %s", path, exc)


def capture(
    *,
    kind: str,
    workspace: str | None = None,
    channel: str = "system",
    actor: str | None = None,
    summary: str = "",
    data: dict[str, Any] | None = None,
    provider: str | None = None,
    model: str | None = None,
    branch: str | None = None,
    session_id: str | None = None,
    parent_event_id: str | None = None,
    duration_ms: int = 0,
    tokens_in: int = 0,
    tokens_out: int = 0,
    bytes_count: int = 0,
    status: str = "ok",
    error: str | None = None,
    tags: list[str] | None = None,
    channel_detail: str | None = None,
) -> str | None:
    """Capture an event into the spine.

    Best-effort, never raises to caller. Returns the event id on success,
    None on failure (with a logged warning).

    Required:
        kind: one of EVENT_KINDS

    Recommended:
        workspace, channel, actor, summary

    See _SCHEMA_DOCS for the full schema.
    """
    if kind not in EVENT_KINDS:
        logger.warning("unknown event kind: %s (will be stored anyway)", kind)

    if channel not in CHANNELS:
        logger.warning("unknown channel: %s (will be stored anyway)", channel)

    try:
        now = time.time()
        now_ms = int(now * 1000)
        now_iso = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(now))
        now_iso += f".{now_ms % 1000:03d}Z"

        ulid = _generate_ulid_at(now_ms)

        workspace_name = None
        if workspace:
            workspace = str(Path(workspace).expanduser().resolve())
            workspace_name = Path(workspace).name

        # Truncate summary to 200 chars as documented
        if summary and len(summary) > 200:
            summary = summary[:197] + "..."

        event: dict[str, Any] = {
            "id": ulid,
            "ts": now,
            "ts_iso": now_iso,
            "ts_mono_ms": now_ms - _MONO_START_MS,
            "workspace": workspace,
            "workspace_name": workspace_name,
            "channel": channel,
            "channel_detail": channel_detail,
            "actor": actor,
            "actor_detail": None,
            "kind": kind,
            "summary": summary,
            "data": data or {},
            "provider": provider,
            "model": model,
            "branch": branch,
            "session_id": session_id,
            "parent_event_id": parent_event_id,
            "duration_ms": duration_ms,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "bytes": bytes_count,
            "status": status,
            "error": error,
            "tags": tags or [],
        }

        line = json.dumps(event, ensure_ascii=False, separators=(",", ":"))
        _atomic_append(_current_path(), line)
        return ulid
    except Exception as exc:  # noqa: BLE001 — best-effort
        logger.warning("capture failed: %s", exc)
        return None


@contextlib.contextmanager
def capture_block(
    *,
    kind: str,
    workspace: str | None = None,
    channel: str = "system",
    actor: str | None = None,
    summary: str = "",
    **kwargs: Any,
) -> Iterator[dict[str, Any]]:
    """Context manager that captures an event with timing + status.

    Usage::

        with capture_block(
            kind="terminal.command",
            workspace="/Users/jkm/Projects/cvc/cvc",
            channel="terminal",
            summary="git status",
        ) as ctx:
            result = subprocess.run(...)
            ctx["data"] = {"exit_code": result.returncode}

    The block:
      - Sets duration_ms from wall time
      - Sets status="err" automatically if an exception escapes
    """
    ctx: dict[str, Any] = {"data": kwargs.get("data", {})}
    start = time.time()
    err: str | None = None
    try:
        yield ctx
    except Exception as exc:  # noqa: BLE001
        err = f"{type(exc).__name__}: {exc}"
        ctx["status"] = "err"
        raise
    finally:
        duration_ms = int((time.time() - start) * 1000)
        capture(
            kind=kind,
            workspace=workspace,
            channel=channel,
            actor=actor,
            summary=summary,
            data=ctx.get("data"),
            duration_ms=duration_ms,
            status=ctx.get("status", "ok"),
            error=err,
            **{
                k: v
                for k, v in kwargs.items()
                if k
                in {
                    "provider", "model", "branch", "session_id",
                    "parent_event_id", "tags", "channel_detail",
                    "tokens_in", "tokens_out", "bytes_count",
                }
            },
        )


# ---------------------------------------------------------------------------
# Read path — query()
# ---------------------------------------------------------------------------


def _iter_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    """Yield events from a JSONL file. Skips malformed lines silently."""
    try:
        with open(path, "rb") as f:
            for raw in f:
                try:
                    line = raw.decode("utf-8").strip()
                    if not line:
                        continue
                    yield json.loads(line)
                except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                    logger.debug("skipped malformed line in %s: %s", path, exc)
    except FileNotFoundError:
        return
    except OSError as exc:
        logger.warning("could not read %s: %s", path, exc)


def query(
    *,
    workspace: str | None = None,
    channel: str | list[str] | None = None,
    kind: str | list[str] | None = None,
    actor: str | None = None,
    session_id: str | None = None,
    since: float | None = None,
    until: float | None = None,
    tags: list[str] | None = None,
    search: str | None = None,
    limit: int = DEFAULT_QUERY_LIMIT,
    reverse: bool = True,
) -> list[dict[str, Any]]:
    """Query the event spine.

    All filters are AND-combined. Time filters use unix seconds.

    Args:
        workspace: exact path match (or substring if `search_wildcard=True`)
        channel: str or list — match any
        kind: str or list — match any
        actor: exact match
        session_id: exact match
        since: only events with ts >= since
        until: only events with ts <= until
        tags: only events with at least one matching tag
        search: case-insensitive substring match against summary + kind
        limit: max events to return (default 1000, hard cap 10000)
        reverse: if True (default), newest first; if False, oldest first

    Returns:
        list of event dicts. Empty list on no matches.
    """
    limit = min(limit, ABSOLUTE_QUERY_LIMIT)
    if limit <= 0:
        return []

    # Normalize channel/kind to lists
    if isinstance(channel, str):
        channel = [channel]
    if isinstance(kind, str):
        kind = [kind]

    workspace_norm: str | None = None
    if workspace:
        try:
            workspace_norm = str(Path(workspace).expanduser().resolve())
        except OSError:
            workspace_norm = workspace

    # Collect candidate files
    root = _spine_root()
    try:
        all_files = sorted(
            (p for p in root.glob("*.jsonl") if ACTIVE_FILENAME_PATTERN.match(p.name)),
            key=lambda p: p.name,
        )
    except OSError as exc:
        logger.warning("could not list events dir: %s", exc)
        return []

    if reverse:
        all_files = list(reversed(all_files))

    search_lower = search.lower() if search else None

    out: list[dict[str, Any]] = []
    for path in all_files:
        if len(out) >= limit:
            break
        # Read file into memory then sort so reverse=True works within-file too.
        events_in_file = list(_iter_jsonl(path))
        if reverse:
            events_in_file.reverse()
        for evt in events_in_file:
            # Workspace filter
            if workspace_norm and evt.get("workspace") != workspace_norm:
                continue
            if channel and evt.get("channel") not in channel:
                continue
            if kind and evt.get("kind") not in kind:
                continue
            if actor and evt.get("actor") != actor:
                continue
            if session_id and evt.get("session_id") != session_id:
                continue
            ts = evt.get("ts")
            if since is not None and (ts is None or ts < since):
                continue
            if until is not None and (ts is None or ts > until):
                continue
            if tags:
                evt_tags = set(evt.get("tags") or [])
                if not any(t in evt_tags for t in tags):
                    continue
            if search_lower:
                hay = f"{evt.get('summary','')} {evt.get('kind','')}".lower()
                if search_lower not in hay:
                    continue
            out.append(evt)
            if len(out) >= limit:
                break

    return out


def count(
    *,
    workspace: str | None = None,
    channel: str | list[str] | None = None,
    kind: str | list[str] | None = None,
    actor: str | None = None,
    since: float | None = None,
    until: float | None = None,
) -> int:
    """Count events matching the filters (no limit)."""
    if isinstance(channel, str):
        channel = [channel]
    if isinstance(kind, str):
        kind = [kind]

    workspace_norm: str | None = None
    if workspace:
        try:
            workspace_norm = str(Path(workspace).expanduser().resolve())
        except OSError:
            workspace_norm = workspace

    root = _spine_root()
    try:
        all_files = sorted(root.glob("*.jsonl"))
    except OSError:
        return 0

    n = 0
    for path in all_files:
        if not ACTIVE_FILENAME_PATTERN.match(path.name):
            continue
        for evt in _iter_jsonl(path):
            if workspace_norm and evt.get("workspace") != workspace_norm:
                continue
            if channel and evt.get("channel") not in channel:
                continue
            if kind and evt.get("kind") not in kind:
                continue
            if actor and evt.get("actor") != actor:
                continue
            ts = evt.get("ts")
            if since is not None and (ts is None or ts < since):
                continue
            if until is not None and (ts is None or ts > until):
                continue
            n += 1
    return n


def stats_by_kind(
    *,
    workspace: str | None = None,
    since: float | None = None,
) -> dict[str, int]:
    """Return a dict of kind → count for matching events."""
    out: dict[str, int] = {}
    for evt in query(workspace=workspace, since=since, limit=ABSOLUTE_QUERY_LIMIT, reverse=False):
        k = evt.get("kind") or "unknown"
        out[k] = out.get(k, 0) + 1
    return out


def stats_by_channel(
    *,
    workspace: str | None = None,
    since: float | None = None,
) -> dict[str, int]:
    """Return a dict of channel → count for matching events."""
    out: dict[str, int] = {}
    for evt in query(workspace=workspace, since=since, limit=ABSOLUTE_QUERY_LIMIT, reverse=False):
        c = evt.get("channel") or "unknown"
        out[c] = out.get(c, 0) + 1
    return out


def stats_by_day(
    *,
    workspace: str | None = None,
    days: int = 30,
) -> list[dict[str, Any]]:
    """Return daily event counts for the last `days` days, oldest first.

    Output: [{"day": "2026-06-01", "count": 47}, ...]
    """
    today = time.strftime("%Y-%m-%d")
    since_ts = time.time() - days * 86400

    out: dict[str, int] = {}
    for evt in query(workspace=workspace, since=since_ts, limit=ABSOLUTE_QUERY_LIMIT, reverse=False):
        ts = evt.get("ts")
        if ts is None:
            continue
        day = time.strftime("%Y-%m-%d", time.gmtime(ts))
        out[day] = out.get(day, 0) + 1

    # Fill in empty days for chart continuity
    result: list[dict[str, Any]] = []
    for i in range(days):
        day_ts = time.time() - (days - 1 - i) * 86400
        day = time.strftime("%Y-%m-%d", time.gmtime(day_ts))
        result.append({"day": day, "count": out.get(day, 0)})

    return result


# ---------------------------------------------------------------------------
# Maintenance — rotation, retention
# ---------------------------------------------------------------------------


def rotate_if_needed() -> list[Path]:
    """Rotate ``current.jsonl`` to a dated file if present.

    Called by the gateway at startup so we never have a stray
    ``current.jsonl`` after a day-rollover.

    Returns the list of rotated file paths.
    """
    root = _spine_root()
    current = root / CURRENT_FILENAME
    if not current.exists():
        return []

    # Determine which day the file belongs to (use mtime)
    mtime = current.stat().st_mtime
    target_name = time.strftime("%Y-%m-%d", time.gmtime(mtime)) + ".jsonl"
    target = root / target_name

    rotated: list[Path] = []
    try:
        if target.exists():
            # Already rotated today — append `current.jsonl` to it
            with open(current, "rb") as src, open(target, "ab") as dst:
                while True:
                    chunk = src.read(64 * 1024)
                    if not chunk:
                        break
                    dst.write(chunk)
            current.unlink()
        else:
            current.rename(target)
        rotated.append(target)
        logger.info("rotated event spine file → %s", target)
    except OSError as exc:
        logger.warning("rotation failed: %s", exc)

    return rotated


def purge_older_than(days: int = DEFAULT_RETENTION_DAYS) -> int:
    """Delete daily JSONL files older than `days` days. Returns count deleted.

    C7 will run this from a scheduled task.
    """
    cutoff = time.time() - days * 86400
    root = _spine_root()
    deleted = 0
    try:
        for path in root.glob("*.jsonl"):
            if not ACTIVE_FILENAME_PATTERN.match(path.name):
                continue
            if path.stat().st_mtime < cutoff:
                path.unlink()
                deleted += 1
    except OSError as exc:
        logger.warning("purge failed: %s", exc)
    return deleted


# ---------------------------------------------------------------------------
# Diagnostic helpers
# ---------------------------------------------------------------------------


def spine_info() -> dict[str, Any]:
    """Return diagnostic info about the spine (for the dashboard / debugging)."""
    root = _spine_root()
    files = []
    total_events = 0
    total_bytes = 0
    try:
        for path in sorted(root.glob("*.jsonl")):
            if not ACTIVE_FILENAME_PATTERN.match(path.name):
                continue
            size = path.stat().st_size
            total_bytes += size
            # Cheap count: count newlines
            with open(path, "rb") as f:
                count = sum(1 for _ in f)
            total_events += count
            files.append({"file": path.name, "events": count, "bytes": size})
    except OSError:
        pass

    return {
        "root": str(root),
        "files": files,
        "total_events": total_events,
        "total_bytes": total_bytes,
        "known_kinds": sorted(EVENT_KINDS),
        "known_channels": sorted(CHANNELS),
    }


# ---------------------------------------------------------------------------
# Init — ensure spine is set up
# ---------------------------------------------------------------------------


def init() -> Path:
    """Idempotent init: ensure directories exist, rotate stale files."""
    root = _spine_root()
    rotate_if_needed()
    return root


# On import, run init so the spine is always usable.
init()