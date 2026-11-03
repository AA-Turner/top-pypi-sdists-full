"""This user's running processes by program: when each started and the few environment keys asked for (psutil, imported only when asked)."""

from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class RunningProcess:
    pid: int
    #: When the process started, epoch seconds (psutil's `create_time`; 0 when the OS would not say).
    started_at: float
    #: Only the keys asked for; None when the OS would not show its environment.
    environ: dict[str, str] | None = field(default=None, repr=False)


def list_processes(
    names: tuple[str, ...], *, path_markers: tuple[str, ...] = (), env_keys: tuple[str, ...] = ()
) -> list[RunningProcess] | None:
    """This user's processes whose name, or whose program (the first two
    command words, so `node …/cli.js` counts), is one of `names` (`.exe`
    ignored), or whose program path holds one of `path_markers`. None when the
    process table cannot be read (no psutil, a sandbox), so a caller can tell
    "none running" from "could not look"."""
    try:
        import psutil
    except ImportError:
        return None
    found: list[RunningProcess] = []
    try:
        me = psutil.Process().username()
        for process in psutil.process_iter(["pid", "name", "cmdline", "create_time", "username"]):
            info = process.info
            if info.get("username") not in (me, None):
                continue
            argv = [str(part).replace("\\", "/") for part in (info.get("cmdline") or [])[:2]]
            programs = {_stem(info.get("name") or ""), *(_stem(os.path.basename(part)) for part in argv)}
            if not (set(names) & programs or any(marker in part for marker in path_markers for part in argv)):
                continue
            environ: dict[str, str] | None = None
            if env_keys:
                try:
                    values = process.environ()
                    environ = {key: values[key] for key in env_keys if key in values}
                except (psutil.Error, OSError):
                    environ = None
            started = info.get("create_time")
            found.append(RunningProcess(pid=int(info["pid"]), started_at=float(started or 0.0), environ=environ))
    except (psutil.Error, OSError):
        return None
    return found


def _stem(program: str) -> str:
    return program[:-4] if program.lower().endswith(".exe") else program
