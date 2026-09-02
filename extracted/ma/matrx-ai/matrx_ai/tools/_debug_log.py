"""Tool-dispatch debug log — one focused file per server start.

Goal: when investigating a tool-call session, you can read the file from
top to bottom and see exactly what happened — which tools were
dispatched, which executor was selected, which were rejected by surface
gating, which hit the loop guard, which had no viable executor.

Design:
  - One log file per Python process. Path captured at first write,
    timestamped with the process start time.
  - Lazy: file is only created when the first event fires.
  - Best-effort: any I/O failure is swallowed (this is a debugging
    aide, never block the request path).
  - Concise: one event per line, fixed kind column, key=value pairs.

File location:
  - ``MATRX_TOOL_DEBUG_LOG_DIR`` env var if set
  - else: walk up from CWD looking for ``.git``; create
    ``<repo>/.matrx-debug/`` (gitignored)
  - else: ``/tmp/matrx-debug/``

Filename: ``tool-trace-YYYY-MM-DD_HH-MM-SS.log`` using the process
start time so subsequent events all land in the same file. Restarting
the server creates a fresh file.

Convenience symlinks (refreshed on first event / on conv changes):
  - ``<log_dir>/current.log`` → active file for this process
  - ``<log_dir>/conv-<short>.log`` → active file, per conversation short id

Verbose mode: set ``MATRX_TOOL_DEBUG_VERBOSE=1`` so callers (executor)
include ``args=`` and a truncated ``result=`` on every event, not just
``FAIL``. Use this when chasing a silent-success bug — the file grows
much faster but you get forensic detail without joining ``cx_tool_call``.

At first write, header-only files (≤ 100 bytes — left behind by previous
processes that started but never dispatched a tool) are auto-deleted to
keep the directory readable.

Disable: set ``MATRX_TOOL_DEBUG_LOG_DISABLED=1`` to silence all output
without touching the call sites.
"""
from __future__ import annotations

import os
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# Captured ONCE at module import — defines the filename for this process.
_PROCESS_START = datetime.now(UTC)
_log_file_path: Path | None = None
_path_lock = threading.Lock()

# Conversations whose symlink we've already pointed at the active file.
# Avoids unnecessary unlink/symlink syscalls on every event.
_linked_convs: set[str] = set()
_linked_convs_lock = threading.Lock()

# Set ONLY by `trace_sinks_enabled()` — the escape hatch for tests that assert
# on the sinks themselves. See `sinks_disabled_by_stage`.
_sinks_forced = False


def sinks_disabled_by_stage() -> bool:
    """True during a pytest run — BOTH trace sinks stay silent.

    The test suite deliberately exercises every failure path (`LOOP_BLOCK`,
    `NO_EXECUTOR`, `SURFACE_REJECT`, timeouts), so a sink that records those as
    real dispatch events buries the production signal it exists to surface.
    Measured 2026-07-28: ~1,250 of ~1,570 non-OK events across 544 trace files
    (80%) were pytest fixtures, and the session-start trace-check hook reported
    "484 FAILs since last triage" for a suite that was passing (feedback
    e6e1d47b).

    Resolved per call, not cached: a test may legitimately flip the stage.
    Never raises — the runtime env crashes by design when `MATRX_STAGE` is
    unset on a production host, and telemetry must not be the thing that
    surfaces it.
    """
    if _sinks_forced:
        return False
    try:
        from matrx_utils import get_runtime_env

        return get_runtime_env().is_test
    except Exception:
        # Fall back to pytest's own marker so the guard still holds in a bare
        # test env that never configured a runtime stage.
        return "PYTEST_CURRENT_TEST" in os.environ


@contextmanager
def trace_sinks_enabled() -> Iterator[None]:
    """Re-enable both trace sinks inside a test that is testing THE SINKS.

    The only sanctioned way past :func:`sinks_disabled_by_stage`. A test that
    merely *exercises a tool* must never use it — that is exactly the traffic
    the stage guard exists to keep out of `.matrx-debug` and `cx_tool_trace`.
    """
    global _sinks_forced
    previous = _sinks_forced
    _sinks_forced = True
    try:
        yield
    finally:
        _sinks_forced = previous


def is_verbose() -> bool:
    """True when callers should include ``args=`` and ``result=`` on
    every event (not just ``FAIL``). Driven by ``MATRX_TOOL_DEBUG_VERBOSE=1``.

    Cheap — checks env var on each call so flipping the variable mid-run
    takes effect on the next event without restarting the process."""
    return os.environ.get("MATRX_TOOL_DEBUG_VERBOSE") == "1"


def _cleanup_header_only_files(log_dir: Path, keep: Path) -> None:
    """Delete any ``tool-trace-*.log`` file ≤ 100 bytes in ``log_dir``
    other than ``keep``. Header-only files mark a process that started
    but never dispatched a tool — harmless but they accumulate fast in
    dev where every code change spawns a new process. Symlinks are left
    alone."""
    try:
        for f in log_dir.glob("tool-trace-*.log"):
            if f.is_symlink() or f == keep:
                continue
            try:
                if f.stat().st_size <= 100:
                    f.unlink()
            except OSError:
                continue
    except OSError:
        return


def _maintain_symlink(symlink: Path, target_name: str) -> None:
    """Point ``symlink`` at ``target_name`` (relative). Idempotent — if
    the symlink already points at the right target, no-op. Removes a
    stale file or wrong-target symlink atomically enough for the
    operator's purposes (we don't care about concurrent readers of the
    symlink itself).

    Symlinks may fail on some filesystems (CIFS, some Docker volumes); we
    swallow the error rather than degrading the actual log write."""
    try:
        if symlink.is_symlink():
            try:
                if os.readlink(symlink) == target_name:
                    return
            except OSError:
                pass
            symlink.unlink()
        elif symlink.exists():
            symlink.unlink()
        symlink.symlink_to(target_name)
    except OSError:
        return


def _resolve_log_path() -> Path | None:
    """Resolve and create the log directory if needed. Cached after first
    call. Returns None when the environment opted out, in which case
    callers skip the write entirely."""
    global _log_file_path

    if os.environ.get("MATRX_TOOL_DEBUG_LOG_DISABLED") == "1":
        return None

    if sinks_disabled_by_stage():
        return None

    if _log_file_path is not None:
        return _log_file_path

    with _path_lock:
        if _log_file_path is not None:
            return _log_file_path

        env_dir = os.environ.get("MATRX_TOOL_DEBUG_LOG_DIR")
        if env_dir:
            log_dir = Path(env_dir).expanduser()
        else:
            cwd = Path.cwd().resolve()
            log_dir = None
            for parent in [cwd, *cwd.parents]:
                if (parent / ".git").exists():
                    log_dir = parent / ".matrx-debug"
                    break
            if log_dir is None:
                log_dir = Path("/tmp/matrx-debug")  # noqa: S108 — debugging only

        try:
            log_dir.mkdir(parents=True, exist_ok=True)
        except OSError:
            return None

        timestamp = _PROCESS_START.strftime("%Y-%m-%d_%H-%M-%S")
        _log_file_path = log_dir / f"tool-trace-{timestamp}.log"

        # One-time init: clean up header-only files from previous
        # processes, then write our own header, then publish the
        # ``current.log`` symlink and announce ourselves to stderr.
        _cleanup_header_only_files(log_dir, keep=_log_file_path)
        try:
            with _log_file_path.open("a", encoding="utf-8") as f:
                f.write(
                    f"# tool-trace log — process started "
                    f"{_PROCESS_START.isoformat(timespec='seconds')} "
                    f"(pid={os.getpid()}, verbose={is_verbose()})\n"
                )
        except OSError:
            pass
        _maintain_symlink(log_dir / "current.log", _log_file_path.name)
        # Single stderr line so operators (and SessionStart hooks) can
        # discover the active path without grepping. Cheap and one-shot.
        try:
            import sys

            print(
                f"[matrx-debug] active tool-trace log: {_log_file_path}",
                file=sys.stderr,
                flush=True,
            )
        except Exception:
            pass

        return _log_file_path


def _truncate(value: Any, limit: int = 240) -> str:
    """240 chars per field — enough to show full args dicts and most
    error messages without cutting off the actionable part. Lines stay
    readable; the alternative (joining cx_tool_call rows by call_id to
    fetch full detail) defeats the purpose of having a quick-look log.
    """
    s = str(value) if not isinstance(value, str) else value
    s = s.replace("\n", " ").replace("\r", " ")
    if len(s) > limit:
        return s[: limit - 3] + "..."
    return s


def log_event(event: str, /, **fields: Any) -> None:
    """Append a single event line to the active log file.

    ``event`` is the event type (DISPATCH, RESULT, SURFACE_REJECT, etc.)
    and is positional-only so kwargs can include a ``kind`` field
    without colliding with the parameter name.

    Format:
        ``[HH:MM:SS.mmm] EVENT_PADDED key=value key=value ...``

    Empty / None fields are dropped to keep lines tight. Values longer
    than 240 chars are truncated with ``...``.

    Side-effect: if ``fields`` contains a ``conv`` key (short conversation
    id), refresh ``<log_dir>/conv-<conv>.log`` to point at the active
    file. Once per conv per process (cached in ``_linked_convs``).

    Never raises — all I/O failures are swallowed so this can't break
    the dispatch path.
    """
    path = _resolve_log_path()
    if path is None:
        return

    conv = fields.get("conv")
    if isinstance(conv, str) and conv:
        with _linked_convs_lock:
            need_link = conv not in _linked_convs
            if need_link:
                _linked_convs.add(conv)
        if need_link:
            _maintain_symlink(path.parent / f"conv-{conv}.log", path.name)

    try:
        ts = datetime.now(UTC).strftime("%H:%M:%S.%f")[:-3]
        parts: list[str] = [f"[{ts}]", f"{event:<14}"]
        for key, val in fields.items():
            if val is None:
                continue
            if isinstance(val, str) and val == "":
                continue
            parts.append(f"{key}={_truncate(val)}")
        with path.open("a", encoding="utf-8") as f:
            f.write(" ".join(parts) + "\n")
    except OSError:
        return


def log_path() -> Path | None:
    """Public accessor — useful for printing the active log path at
    server startup so the operator knows where to find it."""
    return _resolve_log_path()
