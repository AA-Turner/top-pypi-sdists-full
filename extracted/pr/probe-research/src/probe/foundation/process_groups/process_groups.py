"""End a daemon host's recorded tools: the host itself, its service after a crash, an updater
after a kill. Stdlib only (the service's start path imports it)."""

from __future__ import annotations

import contextlib
import os
import signal
import time

from probe.foundation.service_api import procid

#: A recorded tool's process group gets this long after SIGTERM before SIGKILL.
END_TOOLS_GRACE_S = 5.0


def end_tool_groups(children: dict) -> int:
    """End the tools a host recorded (`host-children-<pid>.json`'s `{pid: {"start"}}`), each its
    own process group, only while that very process runs: TERM, then KILL after
    END_TOOLS_GRACE_S. Returns how many were running."""
    alive = []
    for raw, info in (children.items() if isinstance(children, dict) else ()):
        try:
            pid = int(raw)
        except (TypeError, ValueError):
            continue
        start = info.get("start") if isinstance(info, dict) else None
        if pid > 1 and start and procid.alive(pid, start):
            alive.append(pid)
    running = len(alive)
    for pid in alive:
        with contextlib.suppress(OSError):
            os.killpg(pid, signal.SIGTERM)
    deadline = time.monotonic() + END_TOOLS_GRACE_S
    while alive and time.monotonic() < deadline:
        time.sleep(0.2)
        alive = [pid for pid in alive if is_group_alive(pid)]
    for pid in alive:
        with contextlib.suppress(OSError):
            os.killpg(pid, signal.SIGKILL)
    return running


def is_group_alive(pgid: int) -> bool:
    """Does process group `pgid` still have a member? Unknown (not ours to signal): yes."""
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return False
    except OSError:
        return True
    return True
