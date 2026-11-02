"""the agent processes this importer started: register, kill the whole tree, stop them all."""

from __future__ import annotations

import os
import signal
import subprocess
import threading


#: Every agent process this run has started and not yet reaped.
#:
#: A registry, not a local, because leaving the wizard has to stop EVERYTHING
#: and the thing being left is spread across threads: the import pass runs
#: several agents at once, and whichever thread takes the Ctrl-C can only see
#: its own. A 106,007-file import kept reading after "Cancelled by user" for
#: exactly this reason.
#:
#: The outbox is deliberately NOT in here. It is a background drainer with its
#: own `probe outbox pause`, and killing it on the way out would abandon files
#: that are already queued and already the user's -- the one thing leaving a
#: wizard must not do.
_LIVE: set = set()
_LIVE_LOCK = threading.Lock()


def _kill_tree(proc) -> None:
    """Kill an agent and everything it started.

    The PROCESS GROUP, not the process. An agent starts MCP servers, subagents
    and shells; `proc.kill()` reaps the direct child and orphans the rest,
    which keep running with no parent to stop them.

    SIGTERM first, because Claude Code writes the missing tool_result on the
    way down and that transcript is what `--resume` replays -- a SIGKILL here
    costs the unit its resumability. SIGKILL only for what ignores it.
    """
    if proc.poll() is not None:
        return
    for sig, grace in ((signal.SIGTERM, 3.0), (signal.SIGKILL, 2.0)):
        try:
            os.killpg(os.getpgid(proc.pid), sig)
        except (ProcessLookupError, PermissionError, OSError):
            # No group (Windows, or already reaped) -- fall back to the child.
            try:
                proc.kill()
            except OSError:
                return
        try:
            proc.wait(timeout=grace)
            return
        except subprocess.TimeoutExpired:
            continue


def stop_all() -> None:
    """Stop every agent this process started. Safe to call more than once.

    What "leaving the wizard" means. Called from the interrupt path and from a
    `finally` at the top of the import, so no exit route leaves an agent
    reading someone's folder.
    """
    with _LIVE_LOCK:
        processs = list(_LIVE)
        _LIVE.clear()
    for proc in processs:
        _release_agent(proc)


def _register_agent(proc, cancel_event: threading.Event | None = None) -> bool:
    """Register a launch, or stop it if cancellation overtook its spawn.

    The cancellation event is sticky. If stop_all snapshots the registry before
    this child arrives, the child sees the event here and releases itself. If
    cancellation comes afterwards, the child is already in stop_all's snapshot.
    No lock is held while spawning, waiting for model output, or killing a child.
    """
    with _LIVE_LOCK:
        _LIVE.add(proc)
        cancelled = cancel_event is not None and cancel_event.is_set()
    if cancelled:
        _release_agent(proc)
    return not cancelled


def _release_agent(proc) -> None:
    """Stop a still-live launch before releasing its durable ownership.

    The job supervisor interrupts with a BaseException, which can reach a
    launch's finally without passing through its KeyboardInterrupt handler.
    Removing that live process from _LIVE first used to orphan it even on a
    graceful worker stop.
    """
    from ... import jobs as import_jobs

    pid = getattr(proc, "pid", None)
    if isinstance(pid, int):
        if proc.poll() is None:
            _kill_tree(proc)
        if proc.poll() is None:
            return  # Keep the durable registry until the process really stops.
        try:
            import_jobs.unregister_child(pid)
        except Exception:
            # A stale entry is safe: recovery verifies its original process
            # identity. Cleanup must still stop every other registered child.
            pass
    with _LIVE_LOCK:
        _LIVE.discard(proc)
