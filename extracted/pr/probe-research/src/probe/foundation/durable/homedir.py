"""The user's home, else a private ``$TMPDIR/probe-home-<uid>``; every SDK path under ``~`` uses :func:`home`.

Stdlib only: `probe.sdk.settings.settings` imports it on every ``Client()``. Why: DESIGN.md (homedir.py).
"""

from __future__ import annotations

import os
import stat
import tempfile
from pathlib import Path

_stand_in: Path | None = None


def real_home() -> Path | None:
    """``Path.home()``, or None when this process has no home directory."""
    try:
        return Path.home()
    except (RuntimeError, KeyError, OSError):
        return None


def _uid() -> int | str:
    return os.getuid() if hasattr(os, "getuid") else "user"


def _private(path: Path) -> bool:
    try:
        info = os.lstat(path)
    except OSError:
        return False
    return (
        stat.S_ISDIR(info.st_mode)
        and (not hasattr(os, "getuid") or info.st_uid == os.getuid())
        and not info.st_mode & 0o077
    )


def stand_in() -> Path:
    """The private directory used as ``~`` when there is no home."""
    global _stand_in
    # Windows: every directory reads 0o777, so `_private` never passes; keep this process's own
    # `mkdtemp` rather than minting one per call.
    if _stand_in is not None and (os.name == "nt" or _private(_stand_in)):
        return _stand_in
    root = Path(tempfile.gettempdir()) / f"probe-home-{_uid()}"
    try:
        os.mkdir(root, 0o700)
    except OSError:
        pass
    if not _private(root):
        root = Path(tempfile.mkdtemp(prefix=f"probe-home-{_uid()}-"))
    _stand_in = root
    return root


def home() -> Path:
    """``~`` for every SDK path: the real home, else :func:`stand_in`."""
    return real_home() or stand_in()


#: ``str(base)`` -> whether SDK state can be written under it (see `state_base`).
_state_writable: dict[str, bool] = {}


def _can_write(path: Path) -> bool:
    """Whether a file can be created in ``path`` or its nearest existing folder (creating no
    folders on the way). `Journal.usable` minus the lock, which capture state does not need."""
    probe_dir = path
    while not probe_dir.exists() and probe_dir.parent != probe_dir:
        probe_dir = probe_dir.parent
    try:
        with tempfile.TemporaryFile(dir=probe_dir, prefix=".probe-usable-"):
            pass
    except OSError:
        return False
    return True


def state_base() -> Path:
    """The folder capture state lives under: ``$XDG_STATE_HOME``, else ``~/.local/state``, or
    :func:`stand_in`'s ``.local/state`` when nothing can be written there (``HOME=/``, a
    read-only HOME; environment suite, lane E3). Decided once per folder per process, so a
    run's capture never moves mid-run. Why: DESIGN.md (homedir.py)."""
    xdg = os.environ.get("XDG_STATE_HOME")
    base = Path(xdg) if xdg else home() / ".local" / "state"
    key = str(base)
    writable = _state_writable.get(key)
    if writable is None:
        writable = _state_writable[key] = _can_write(base / "probe")
    return base if writable else stand_in() / ".local" / "state"
