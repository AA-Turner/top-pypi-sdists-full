"""how a run meets its supervisor: exit codes, the supervisor gone, stop signals per run."""

from __future__ import annotations
import json
import os
from probe.daemon.host import lease
EXIT_DO_NOT_RESPAWN = 3
#: Set by a supervisor that respawns by the switch itself (tap 0.9.12+, whose
#: `wanted()` is False while inline): a worker leaving for `/probe inline` exits
#: 0. Without it (taps 0.9.9-0.9.11, whose `wanted()` is True there) it exits
#: EXIT_DO_NOT_RESPAWN, or that tap would start a worker again at once.
SUPERVISOR_FOLLOWS_INLINE_ENV = "PROBE_TAP_FOLLOWS_INLINE"
#: A newer tap recognizes read-only inline markers too. Without this capability,
#: a read-only quota handoff must latch the older supervisor until a switch move.
SUPERVISOR_READ_ONLY_INLINE_ENV = "PROBE_TAP_READ_ONLY_INLINE"
#: The worker crashed: the supervisor waits before it starts another.
EXIT_CRASHED = 4
#: The worker left because of the SWITCH (unreadable, or not `daemon`): the
#: supervisor starts one again as soon as the switch reads `daemon` -- never
#: "gave up", which a switch readable again by the time it looks would pin (T11).
EXIT_RESPAWN_LATER = 5
#: The daemon's AI libraries are missing: the supervisor tries again later
#: (LIBS_RETRY_SECONDS on its side), because an update or `probe daemon install`
#: puts them back. Only to a supervisor that sets SUPERVISOR_RETRIES_LIBS_ENV
#: (tap 0.9.19+); an older tap gets EXIT_DO_NOT_RESPAWN, which it understands.
EXIT_RETRY_LIBS = 6
#: The machine's disk is full: a crash's wait before the next start, never a
#: crash the Probe service reports (a tap's supervisor reads it as a crash).
EXIT_DISK_FULL = 7
#: Set by a supervisor that retries after EXIT_RETRY_LIBS.
SUPERVISOR_RETRIES_LIBS_ENV = "PROBE_TAP_RETRIES_LIBS"
#: Set by the Probe service's supervisor (`probe.service.sessions.workers`):
#: `{"pid", "start", "sid"}` (JSON; `start` is `probe.foundation.service_api.procid`'s), the
#: exact process that supervises this worker. It is "gone" once that process
#: is: exited (a zombie included: unreaped, `kill(pid, 0)` still succeeds),
#: or its pid names another process (start time). So a service that exits while
#: this still loads (a restart right after an update) is seen gone, and the
#: worker finishes and leaves instead of running on unowned. Without it (the
#: tap's `probe`, or a service that could not read its own start time), the
#: parent is the one `getppid()` names at start.
SUPERVISOR_PID_ENV = "PROBE_DAEMON_SUPERVISOR"


def inline_exit_code(session_id: str = "") -> int:
    """Leave manual or confirmed-quota inline without an older tap respawning us.
    A tap that follows full inline may still mistake read-only inline for a reader
    daemon, so only its separate capability permits an ordinary exit there."""
    from probe.sdk.session_marker import STATE_READ_ONLY
    if (session_id and lease.session_state(session_id) == STATE_READ_ONLY
            and lease.inline(session_id)
            and os.environ.get(SUPERVISOR_READ_ONLY_INLINE_ENV) != "1"):
        return EXIT_DO_NOT_RESPAWN
    return 0 if os.environ.get(SUPERVISOR_FOLLOWS_INLINE_ENV) == "1" else EXIT_DO_NOT_RESPAWN


def supervisor_identity(session_id: str) -> tuple[int, str | None] | None:
    """SUPERVISOR_PID_ENV's `(pid, start)` when it names this session, else None.
    `start` is None when the service could not read its own start time."""
    try:
        data = json.loads(os.environ.get(SUPERVISOR_PID_ENV) or "null")
    except ValueError:
        return None
    if not isinstance(data, dict) or data.get("sid") != session_id:
        return None
    pid, start = data.get("pid"), data.get("start")
    if not isinstance(pid, int) or isinstance(pid, bool) or pid <= 1:
        return None
    return pid, (start if isinstance(start, str) and start else None)


def parent_gone(supervisor: tuple[int, str | None] | None, parent_pid: int) -> bool:
    """Is this worker's supervisor gone? With its identity (SUPERVISOR_PID_ENV):
    that exact process no longer runs -- a zombie or a reused pid reads as gone,
    and an interpreter that forked under it is no orphan. Known by pid alone
    (no start time): gone once that pid runs no process or a zombie, alive while
    it runs (a reused pid cannot be told then). Without it, or where nothing can
    be read: its parent at start is no longer its parent."""
    if supervisor is not None:
        pid, start = supervisor
        if os.getppid() == pid:
            return False  # still its child: that process runs (no pid reuse while it does)
        from probe.foundation.service_api import procid

        if start:
            alive = procid.alive(pid, start)
            if alive is not None:
                return not alive
        else:
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                return True
            except OSError:
                pass  # not ours to signal: it runs
            info = procid.proc(pid)
            if info is not None:
                return info.zombie
    return os.getppid() != parent_pid
