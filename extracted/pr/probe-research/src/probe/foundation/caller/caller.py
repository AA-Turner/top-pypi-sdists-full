"""Which process a piece of work runs for: this one, or the `probe` shim a `cli.run` child serves.

A `probe` command runs in a child the Probe service forks (service-only D5), so its own parent is
the service's CLI host, not the agent's shell. The service names the shim it serves in
CALLER_PID_ENV (and its start time), which the child's subprocesses inherit: every walk up to
"who started this" starts at the caller instead of `os.getppid()` (service-only T6). The vendored
`session_marker._ancestors` reads the same variable (it cannot import this).
"""

from __future__ import annotations

import os
from dataclasses import dataclass

#: Whether the caller is fenced ("1"/"0"), set by the service only (D27).
from probe.foundation.service_api.env import CALLER_FENCED_ENV  # noqa: F401 -- re-exported

#: Set by the service in a `cli.run` child: the shim's pid. Never the caller's word (`commands.child`).
CALLER_PID_ENV = "PROBE_CALLER_PID"
#: ... and that shim's start time (`procid.start_time`), so a reused pid never passes for it.
CALLER_START_ENV = "PROBE_CALLER_START"


@dataclass(frozen=True)
class Caller:
    """The process this work runs for. `is_remote`: another process (a `cli.run` child's shim)."""

    pid: int
    start: str | None = None
    is_remote: bool = False

    @classmethod
    def get_current(cls) -> Caller:
        """The shim a `cli.run` child serves (CALLER_PID_ENV), else this process. A named
        caller whose start time is not the running process's (its pid reused by another, once a
        detached child outlived it) is no caller: this process."""
        raw = os.environ.get(CALLER_PID_ENV, "")
        if raw.isdigit() and int(raw) > 1:
            start = os.environ.get(CALLER_START_ENV) or None
            if start is None or _is_same_process(int(raw), start):
                return cls(int(raw), start, True)
        return cls(os.getpid())

    @staticmethod
    def adopt(pid: int, start: str | None) -> None:
        """This process (and what it starts) now works for `pid`: the service's word, never the request's."""
        os.environ[CALLER_PID_ENV] = str(pid)
        if start:
            os.environ[CALLER_START_ENV] = start
        else:
            os.environ.pop(CALLER_START_ENV, None)

    def get_parent_pid(self) -> int | None:
        """The caller's parent (where an ancestry walk starts, as `os.getppid()` did); None if unreadable."""
        if not self.is_remote:
            return os.getppid()
        from probe.foundation.service_api import procid

        found = procid.proc(self.pid)
        return found.ppid if found is not None else None

    def get_lineage(self) -> set[int]:
        """This process, the caller, and every process above either (a `cli.run` child's own
        parents are the service's CLI host and the service)."""
        from probe.foundation.service_api import procid

        seen: set[int] = set()
        for start in {os.getpid(), self.pid}:
            pid = start
            seen.add(pid)
            for _ in range(64):
                found = procid.proc(pid)
                if found is None or found.ppid <= 1:
                    break
                pid = found.ppid
                seen.add(pid)
        return seen


#: `(pid, start)` -> whether that process runs: one /proc read (a `ps` elsewhere) per caller.
_SEEN: dict[tuple[int, str], bool] = {}


def _is_same_process(pid: int, start: str) -> bool:
    """Does `pid` still run as the process that started at `start`? An unreadable start time
    (no such process, or `ps` failing) reads as no."""
    key = (pid, start)
    if key not in _SEEN:
        from probe.foundation.service_api import procid

        _SEEN[key] = procid.start_time(pid) == start
    return _SEEN[key]
