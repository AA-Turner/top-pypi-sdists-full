"""The user's home directory, or a private stand-in when the process has none.

A container running an arbitrary uid (OpenShift, ``docker run --user 12345``,
many managed-job runners) can start with HOME unset and no passwd entry. Then
there is no home at all: ``Path.home()`` raises ``RuntimeError: Could not
determine home directory`` -- which crashed ``probe.init()`` before it opened a
run -- and ``os.path.expanduser("~")`` hands back ``"~"`` unchanged, so a
``~/.local/state`` join lands in a directory literally named ``~`` inside the
user's project.

Every SDK path under ``~`` goes through :func:`home`. With no home it answers
``$TMPDIR/probe-home-<uid>``: created ``0700``, used only when it is a real
directory this user owns that nobody else can write (the outbox fallback's
rule, ``journal.trusted_dir``), else a fresh ``mkdtemp``. Chosen once per
process. Like the outbox fallback it does not survive the machine: a process
with no home has nowhere durable to keep state, and the outbox's own warning
already says so for the part that matters.

A home that exists but cannot be written (``HOME=/`` for an arbitrary uid, a
read-only mount) is still the home for reading config; only capture state
moves, through :func:`state_base`.

Stdlib only: `probe.sdk.config` imports it on every ``Client()``.
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
    # Windows: mode bits say nothing there (every directory reads 0o777), so
    # `_private` never passes and the stand-in is always this process's own
    # `mkdtemp` -- kept for the process, not re-minted on every call.
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
    """Whether a file can be created in ``path``, or in the nearest folder of
    it that exists (nothing is created on the way: a read-only probe must not
    leave folders behind). The outbox's own test (`Journal.usable`) minus
    the lock, which capture state does not need."""
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
    """The folder capture state lives under: ``$XDG_STATE_HOME``, else
    ``~/.local/state`` -- or :func:`stand_in`'s ``.local/state`` when nothing
    can be written there.

    ``HOME=/`` is what Docker gives a uid it has no passwd entry for, and a
    hardened pod can mount HOME read-only. The outbox falls back to ``$TMPDIR``
    there (plan 1.5); output and read capture used to stop instead, so the run
    lost ``probe/run.log`` and its read list (environment suite, lane E3). They
    now take the same private ``$TMPDIR`` directory a process with no home at
    all uses, chosen by the same rule (`journal.trusted_dir`). Decided once
    per folder per process, so a run's capture never moves mid-run, and every
    process of this user on the machine decides alike."""
    xdg = os.environ.get("XDG_STATE_HOME")
    base = Path(xdg) if xdg else home() / ".local" / "state"
    key = str(base)
    writable = _state_writable.get(key)
    if writable is None:
        writable = _state_writable[key] = _can_write(base / "probe")
    return base if writable else stand_in() / ".local" / "state"
