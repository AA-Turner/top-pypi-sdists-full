"""mark version folders in use and delete the ones past KEEP."""

from __future__ import annotations

import contextlib
import os
import shutil
import subprocess
import time
from pathlib import Path

from .. import handoff
#: Versions kept beside the active one when pruning (the previous one always).
KEEP = 3
#: A version folder younger than this is never pruned (a run may have just started on it).
PRUNE_MIN_AGE_S = 24 * 3600


def discard(env: Path, tools: Path | None = None) -> None:
    """Delete a version env that will not be used: never the active one, the
    one to switch back to, nor one a process runs from (`protected`)."""
    holder = env.parent
    if active(tools) is not None and active(tools) == env.resolve():
        return
    if versions_root(tools) in holder.parents and protected(holder, tools):
        return
    shutil.rmtree(holder, ignore_errors=True)


# -- pruning ---------------------------------------------------------------------


#: Each machine marks the versions its processes run from (`.used-<machine key>`):
#: a home shared by several machines (NFS) has one versions folder, and a
#: machine sees only its own processes. A mark this fresh keeps a version.
USED_PREFIX = ".used-"
USED_FRESH_S = 3 * 24 * 3600


def _commands() -> list[str] | None:
    """Every running process's command line and executable, once; None when
    they cannot be read (unknown: everything reads as in use)."""
    proc = Path("/proc")
    if proc.is_dir():
        found = []
        try:
            for entry in proc.iterdir():
                if not entry.name.isdigit():
                    continue
                with contextlib.suppress(OSError):
                    found.append((entry / "cmdline").read_bytes().decode("utf-8", "replace"))
                with contextlib.suppress(OSError):
                    found.append(os.readlink(entry / "exe"))
        except OSError:
            return None
        return found
    try:
        out = subprocess.run(["ps", "-axww", "-o", "command="], capture_output=True, text=True, timeout=10, check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    return None if out.returncode != 0 else (out.stdout or "").splitlines()


def _in_use(folder: Path, commands: list[str] | None = None) -> bool:
    """Does any running process run from `folder`? (Its command line names it,
    either spelling of the path.) Unknown reads as yes."""
    commands = _commands() if commands is None else commands
    if commands is None:
        return True
    needles = {str(folder)}
    with contextlib.suppress(OSError):
        needles.add(str(folder.resolve()))
    return any(n in c for c in commands for n in needles)


def _machine() -> str:
    try:
        from probe.foundation.service_api import paths

        return paths.machine_key()
    except Exception:  # noqa: BLE001
        return "unknown"


def _mtime(path: Path) -> float:
    try:
        return path.stat().st_mtime
    except OSError:
        return 0.0


def mark_in_use(tools: Path | None = None) -> list[Path]:
    """Mark (`.used-<this machine>`) every version folder a process here runs
    from, and clear this machine's mark on the others. Returns the marked.
    Never raises."""
    try:
        tools = tools or tool_dir()
        folders = [p for p in versions_root(tools).iterdir() if p.is_dir()]
    except OSError:
        return []
    commands = _commands()
    mine = USED_PREFIX + _machine()
    marked = []
    for folder in folders:
        mark = folder / mine
        with contextlib.suppress(OSError):
            if commands is not None and not _in_use(folder, commands):
                mark.unlink(missing_ok=True)
                continue
            mark.touch()
            marked.append(folder)
    return marked


def _version_key(name: str) -> tuple:
    """A version folder's place in line by its NAME alone: `(release, generation)`;
    a name that is no release sorts first. `_place` reads the env's dist-info first."""
    version, generation, _leftover = folder_parts(name)
    return handoff.release(version) or (), generation


def _place(folder: Path) -> tuple:
    """A version folder's place in prune's line: the version its env HOLDS (its
    dist-info, no interpreter started where it has one), else its name's; then
    its generation, so a rebuilt `<v>+g<N>` counts as `<v>` (newer than the
    `<v>` it replaced), never as junk; then when it was installed. A folder
    with no env in it (junk, whatever its name) sorts first, and goes first."""
    env = folder / DIST
    named, generation = _version_key(folder.name)
    if not env_python(env).exists():
        return (), 0, _installed_at(folder)
    return handoff.release(handoff.env_version(env, timeout=10.0)) or named, generation, _installed_at(folder)


def _installed_at(folder: Path) -> float:
    for marker in (folder / DIST / "pyvenv.cfg", folder / DIST / "bin" / "python"):
        try:
            return marker.lstat().st_mtime
        except OSError:
            continue
    return _mtime(folder)


def _used_elsewhere(folder: Path, now: float) -> bool:
    mine = USED_PREFIX + _machine()
    try:
        marks = [m for m in folder.iterdir() if m.name.startswith(USED_PREFIX) and m.name != mine]
    except OSError:
        return True
    return any(now - _mtime(m) < USED_FRESH_S for m in marks)


def prune(tools: Path | None = None, *, keep: int = KEEP, now: float | None = None) -> list[Path]:
    """Delete version folders beyond the newest `keep`, never the active or the
    previous one, never one younger than PRUNE_MIN_AGE_S, never one a running
    process uses -- here, or on another machine sharing this home (its mark,
    `mark_in_use`, younger than USED_FRESH_S). Returns what was deleted. Never raises."""
    tools = tools or tool_dir()
    root = versions_root(tools)
    now = time.time() if now is None else now
    try:
        folders = [p for p in root.iterdir() if p.is_dir()]
    except OSError:
        return []
    protected = set()
    for env in (active(tools), previous(tools)):
        if env is not None:
            with contextlib.suppress(OSError):
                protected.add(env.parent.resolve())
    moving = record(tools).get("migrating")
    if isinstance(moving, dict) and isinstance(moving.get("to"), str):
        with contextlib.suppress(OSError):
            protected.add(Path(moving["to"]).parent.resolve())  # what `recover` puts back
    commands = _commands()
    mark_in_use(tools)
    # Newest first by the version each env holds, then its generation (a
    # folder's own mtime moves with its marks), aged by when its env was made
    # (`pyvenv.cfg`, written once at install).
    folders.sort(key=_place, reverse=True)
    removed: list[Path] = []
    for folder in folders[keep:]:
        try:
            if (folder.resolve() in protected or now - _installed_at(folder) < PRUNE_MIN_AGE_S
                    or _in_use(folder, commands) or _used_elsewhere(folder, now)):
                continue
            shutil.rmtree(folder)
            removed.append(folder)
        except OSError:
            continue
    return removed
from probe.shared.updates.installs.active_record import active, record  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.updates.installs.installs import previous, protected  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.updates.installs.layout import DIST, folder_parts, tool_dir, versions_root  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.updates.installs.link import env_python  # noqa: E402 -- pieces need each other; the front door loads this one first
