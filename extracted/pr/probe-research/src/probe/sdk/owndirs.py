"""The SDK's own folders: never a run's code, reads or outputs.

Probe keeps files on the machine: the outbox (``PROBE_OUTBOX_DIR``, else
``<state>/probe/outbox``, and any explicit ``spool_dir``), the state folder
(``<state>/probe``: read spools, run logs, the capture registry;
``<state>/probe-telemetry``), and in ``$TMPDIR`` the private stand-ins a
process without a usable home takes -- ``probe-outbox-<uid>[-XXXX]`` (the
outbox fallback, plan 1.5), ``probe-home-<uid>[-XXXX]`` (``~``, #2109, and
capture state when HOME cannot be written) -- plus the hardware collector's
election lock ``probe-hw-<run>-<host>.lock``.

A run started in a folder that holds one of them -- ``$TMPDIR``
(``docker run -w /tmp``), a HOME with the default state folder, a project
with ``XDG_STATE_HOME`` inside it -- used to take the SDK's own queue files
as its code (found by the environment suite, lane E3). :func:`current` answers
"is this path Probe's own?" for the code snapshot, read capture and the
output sweep, whatever the working directory.

A path is Probe's own when it, or a folder above it, is one of those
folders. Checked by walking up the path through a set, never by scanning a
list of prefixes: a process may have used thousands of outboxes (the test
suite does), and read capture asks on every ``open()``.
"""

from __future__ import annotations

import os
import sys
import tempfile
import threading

from . import homedir

#: Why a capture skipped a path under one of these folders (``skipped`` in a
#: code manifest).
REASON = "probe_state"

_lock = threading.Lock()
#: Every outbox a `Client` of this process queued in, both spellings.
_noted: set[str] = set()
_cached: tuple[tuple, Owned] | None = None


def _uid() -> int | str:
    return os.getuid() if hasattr(os, "getuid") else "user"


def _spellings(path: str) -> set[str]:
    """``path`` as given (absolute, normalized) and resolved: a folder is
    named both ways, and a walk may meet it either way."""
    given = os.path.abspath(os.path.expanduser(path))
    return {given, os.path.realpath(given)}


def _tmp_name(name: str) -> bool:
    """A name the SDK takes directly in ``$TMPDIR``."""
    uid = _uid()
    for stem in (f"probe-outbox-{uid}", f"probe-home-{uid}"):
        if name == stem or name.startswith(stem + "-"):
            return True
    return name.startswith("probe-hw-") and name.endswith(".lock")


def _heads(path: str, *, whole: bool = False):
    """``(folder, its parent)`` for each folder on the way down to ``path``,
    from the top: ``/a/b/c`` gives ``(/a, /)``, ``(/a/b, /a)``, and with
    ``whole`` also ``(/a/b/c, /a/b)``."""
    root = os.path.splitdrive(path)[0] + os.sep
    start = len(root)
    parent = root
    while True:
        end = path.find(os.sep, start)
        if end < 0:
            if whole and start < len(path):
                yield path, parent
            return
        head = path[:end]
        yield head, parent
        parent = head
        start = end + 1


def note(path: str | os.PathLike | None) -> None:
    """Remember a folder this process keeps SDK files in (a `Client`'s
    outbox, which may be an explicit ``spool_dir`` no environment names)."""
    if path is None:
        return
    global _cached
    try:
        spellings = _spellings(os.fspath(path))
    except (OSError, TypeError, ValueError):
        return
    with _lock:
        if not spellings <= _noted:
            _noted.update(spellings)
            _cached = None


class Owned:
    """The SDK's folders at one moment: ``dirs`` (absolute, both spellings)
    and the ``$TMPDIR`` spellings whose Probe-named entries are its own."""

    def __init__(self, dirs: set[str], tmpdirs: set[str]) -> None:
        self.dirs = frozenset(dirs)
        self.tmpdirs = frozenset(tmpdirs)
        #: Every folder above one of ours, and ``$TMPDIR`` itself: a path
        #: leaving this set on its way down can hold nothing of ours, so most
        #: paths are answered after a few components.
        self._above = frozenset(
            head for path in self.dirs | self.tmpdirs for head, _ in _heads(path)
        ) | self.tmpdirs

    def is_own(self, path: str) -> bool:
        """``path`` (absolute, normalized) itself is one of the folders, or a
        Probe-named entry of ``$TMPDIR``."""
        if path in self.dirs:
            return True
        parent, name = os.path.split(path)
        return parent in self.tmpdirs and _tmp_name(name)

    def owns(self, path: str) -> bool:
        """``path`` (absolute) is Probe's own, or inside something that is."""
        for head, parent in _heads(os.path.normpath(path), whole=True):
            if head in self.dirs:
                return True
            if parent in self.tmpdirs and _tmp_name(head[len(parent):].lstrip(os.sep)):
                return True
            if head not in self._above:
                return False
        return False

    def within(self, root: str) -> Within | None:
        """What is Probe's own strictly BELOW ``root`` (an absolute, resolved
        folder a capture walks), or None when nothing can be -- the common
        case, which then costs a walk nothing. A root that is itself inside
        one of the folders is the caller's own choice of place: nothing
        above it is consulted."""
        root = os.path.normpath(root)
        prefix = root if root.endswith(os.sep) else root + os.sep
        dirs = {d for d in self.dirs if d.startswith(prefix)}
        tmps = {t for t in self.tmpdirs if t == root or t.startswith(prefix)}
        if not dirs and not tmps:
            return None
        return Within(root, Owned(dirs, tmps))


class Within:
    """`Owned` for one capture root, asked about paths relative to it."""

    def __init__(self, root: str, owned: Owned) -> None:
        self.root = root
        self._owned = owned
        #: relative folder -> the top-most own part of it, or None.
        self._dirs: dict[str, str | None] = {}

    def top(self, rel: str) -> str | None:
        """The top-most part of ``rel`` (posix, relative to the root) that is
        Probe's own -- the folder a capture skips and reports once -- or
        None."""
        head, _, name = rel.rpartition("/")
        found = self._dir_top(head) if head else None
        if found is not None:
            return found
        return rel if self._owned.is_own(os.path.join(self.root, *rel.split("/"))) else None

    def _dir_top(self, rel_dir: str) -> str | None:
        if rel_dir in self._dirs:
            return self._dirs[rel_dir]
        head, _, _ = rel_dir.rpartition("/")
        found = self._dir_top(head) if head else None
        if found is None and self._owned.is_own(os.path.join(self.root, *rel_dir.split("/"))):
            found = rel_dir
        self._dirs[rel_dir] = found
        return found


def _state_bases() -> list[str]:
    """Every state folder SDK files may be under, without creating one."""
    bases = []
    xdg = os.environ.get("XDG_STATE_HOME")
    if xdg:
        bases.append(xdg)
    real = homedir.real_home()
    if real is not None:
        bases.append(os.path.join(str(real), ".local", "state"))
    stand_in = homedir._stand_in
    if stand_in is not None:
        bases.append(os.path.join(str(stand_in), ".local", "state"))
    return bases


def current() -> Owned:
    """The SDK's folders now. Cached until the environment that names them
    (or the set of noted outboxes) changes; creates nothing."""
    global _cached
    journal = sys.modules.get("probe.sdk.journal")
    key = (
        os.environ.get("PROBE_OUTBOX_DIR"),
        os.environ.get("PROBE_SPOOL_DIR"),
        os.environ.get("XDG_STATE_HOME"),
        os.environ.get("HOME"),
        tempfile.gettempdir(),
        homedir._stand_in,
        getattr(journal, "_private_fallback", None),
    )
    cached = _cached
    if cached is not None and cached[0] == key:
        return cached[1]
    dirs: set[str] = set()
    named = [os.environ.get("PROBE_OUTBOX_DIR"), os.environ.get("PROBE_SPOOL_DIR"), key[5], key[6]]
    for base in _state_bases():
        named += [os.path.join(base, "probe"), os.path.join(base, "probe-telemetry")]
    for path in named:
        if path:
            try:
                dirs |= _spellings(os.fspath(path))
            except (OSError, TypeError, ValueError):
                continue
    with _lock:
        dirs |= _noted
        owned = Owned(dirs, _spellings(key[4]))
        _cached = (key, owned)
    return owned


def owns(path: str) -> bool:
    """Whether the absolute ``path`` is Probe's own (see the module docstring)."""
    try:
        return current().owns(path)
    except Exception:  # noqa: BLE001 -- a filter must never break a capture
        return False
