"""Was Probe's state removed under this process (`probe uninstall` while a run kept training)? Then
nothing of Probe's makes it again here: no queued write, no capture file, no service (vespper U-D5).

Stdlib only. A folder counts as removed when this process saw it and it is gone or replaced
(another inode: a reinstall in between) the next time it looks. Once one is, `was_removed` holds
for the rest of the process. Why and the traps: DESIGN.md (removal.py).
"""

from __future__ import annotations

import os
import threading
from pathlib import Path

_lock = threading.Lock()
#: str(path) -> st_ino of each watched folder, as this process first saw it (never st_dev: a
#: remounted network home keeps its inodes and may change its device number).
_seen: dict[str, int] = {}
_has_seen_removal = False


def is_removed(path: str | os.PathLike) -> bool:
    """Was `path` removed under this process? One `stat`; remembers the folder the first time it
    is there. True also once anything watched was removed (`was_removed`)."""
    global _has_seen_removal
    if _has_seen_removal:
        return True
    key = str(Path(path))
    try:
        found: int | None = os.stat(key).st_ino
    except FileNotFoundError:
        found = None
    except OSError:
        return False  # cannot tell (a mount that hangs, no permission): never a removal
    with _lock:
        seen = _seen.get(key)
        if seen is None:
            if found is not None:
                _seen[key] = found
        elif found != seen:
            _has_seen_removal = True  # only ever set here: another thread's True stays
        return _has_seen_removal


def get_watched_folder() -> Path | None:
    """This machine's Probe service folder where `probe uninstall` removes it,
    `~/.local/state/probe/service/<machine key>`, never a root an environment or a fallback names
    (a tmp reaper may take that); None when it cannot be named."""
    from probe.foundation.durable import homedir

    if homedir.real_home() is None:
        return None  # a stand-in home under $TMPDIR: a reaper's to take, never an uninstall
    try:
        from probe.foundation.service_api import paths

        return paths.state_dir() / paths.SERVICE_DIRNAME / paths.machine_key()
    except Exception:  # noqa: BLE001 -- cannot tell: nothing watched
        return None


def was_removed() -> bool:
    """Has a watched folder been removed under this process (no file is touched)?"""
    return _has_seen_removal


def forget() -> None:
    """This process removed it itself (`probe uninstall`, an installer finishing one and going
    on): it is no bystander, and may make Probe's state again."""
    global _has_seen_removal
    with _lock:
        _seen.clear()
        _has_seen_removal = False
