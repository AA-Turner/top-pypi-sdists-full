"""TOCTOU-safe filesystem ops for root-run MDM writes into a console user's home.

The MDM hook install runs as root (macOS bootstrap LaunchDaemon) and writes into
the console user's home (``~/.claude``, ``~/.hermes``). A non-admin user fully
controls that directory and can plant symlinks; plain ``Path.write_text`` /
``Path.read_bytes`` / ``os.chown`` follow them, letting the user redirect a root
read/write/chown to an arbitrary file (CWE-59 / CWE-61 local privilege
escalation).

These helpers walk the path component-by-component **relative to a trusted home
directory** (its parent, ``/Users`` or ``/home``, is root-owned and not
user-writable), opening each component with ``O_NOFOLLOW`` via ``dir_fd`` so any
symlink — at the final component *or* any ancestor up to home — aborts the
operation instead of being followed. All ops act on file descriptors, not
re-resolved paths, so they are also TOCTOU-safe: an attacker who swaps a
component for a symlink after our ``lstat`` still loses, because the subsequent
``O_NOFOLLOW`` open fails with ``ELOOP``.

When a final/ancestor component is already a symlink, the write helpers unlink
the *link itself* (``os.unlink`` never follows) and recreate a real file/dir, so
the install self-heals against a pre-staged attack symlink without ever touching
the link's target.

POSIX-only. ``O_NOFOLLOW`` / ``O_DIRECTORY`` do not exist on Windows; callers
gate these helpers on non-Windows (the MDM-as-root path; Windows relies on ACL
inheritance and returns early before reaching here).
"""

from __future__ import annotations

import errno
import os
import platform
import stat
from pathlib import Path
from typing import Optional

# ``getattr`` fallbacks keep this module importable on Windows (where these
# flags are absent); the helpers are never called there.
_O_NOFOLLOW = getattr(os, "O_NOFOLLOW", 0)
_O_DIRECTORY = getattr(os, "O_DIRECTORY", 0)
_O_CLOEXEC = getattr(os, "O_CLOEXEC", 0)

_DIR_OPEN_FLAGS = os.O_RDONLY | _O_DIRECTORY | _O_NOFOLLOW | _O_CLOEXEC
_FILE_READ_FLAGS = os.O_RDONLY | _O_NOFOLLOW | _O_CLOEXEC


def _relative_parts(home: Path, path: Path) -> tuple[str, ...]:
    """Components of *path* below *home*.

    Raises ``ValueError`` if *path* is not contained under *home* (so callers
    never operate outside the trusted anchor).
    """
    rel = path.relative_to(home)
    parts = rel.parts
    if not parts or ".." in parts:
        raise ValueError(f"{path} is not safely contained under {home}")
    return parts


def _lstat_at(parent_fd: int, name: str) -> Optional[os.stat_result]:
    """``lstat`` *name* relative to *parent_fd*, or ``None`` if it doesn't exist."""
    try:
        return os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
    except FileNotFoundError:
        return None


def _open_dir_component(parent_fd: int, name: str, *, create: bool) -> int:
    """Open child directory *name* under *parent_fd* without following symlinks.

    With ``create=True`` a missing directory is created and a symlink/non-dir
    placeholder is replaced (the entry is unlinked — never followed — then a
    real dir is made). With ``create=False`` a symlink/missing/non-dir entry
    raises ``OSError``.
    """
    st = _lstat_at(parent_fd, name)
    if st is not None and stat.S_ISLNK(st.st_mode):
        if not create:
            raise OSError(errno.ELOOP, "symlinked path component", name)
        os.unlink(name, dir_fd=parent_fd)
        st = None
    if st is None:
        if not create:
            raise FileNotFoundError(errno.ENOENT, "missing path component", name)
        os.mkdir(name, dir_fd=parent_fd)
    elif not stat.S_ISDIR(st.st_mode):
        if not create:
            raise NotADirectoryError(errno.ENOTDIR, "not a directory", name)
        os.unlink(name, dir_fd=parent_fd)
        os.mkdir(name, dir_fd=parent_fd)
    # ``O_NOFOLLOW`` re-checks at open time: if the entry was swapped for a
    # symlink after the lstat above, this raises ELOOP and the caller aborts.
    return os.open(name, _DIR_OPEN_FLAGS, dir_fd=parent_fd)


def _open_file_for_write(parent_fd: int, name: str, mode: int) -> int:
    """Open *name* for writing under *parent_fd* without following a symlink.

    A pre-existing symlink is unlinked (the link, not its target) and a fresh
    file created. A regular file is truncated. Anything else (dir, fifo, …) is
    refused.
    """
    st = _lstat_at(parent_fd, name)
    if st is not None and stat.S_ISLNK(st.st_mode):
        os.unlink(name, dir_fd=parent_fd)
        st = None
    flags = os.O_WRONLY | _O_NOFOLLOW | _O_CLOEXEC
    if st is None:
        flags |= os.O_CREAT | os.O_EXCL
    elif stat.S_ISREG(st.st_mode):
        flags |= os.O_TRUNC
    else:
        raise OSError(errno.EEXIST, "refusing to write non-regular file", name)
    return os.open(name, flags, mode, dir_fd=parent_fd)


def _open_home_dir(home: Path) -> int:
    """Open *home* as a directory, refusing to follow a symlinked home."""
    return os.open(home, _DIR_OPEN_FLAGS)


def _walk_parents(home_fd: int, parts: tuple[str, ...], *, create: bool) -> list[int]:
    """Open dir fds for every component except the last, relative to *home_fd*.

    Returns the opened fds in order (caller owns closing them). The returned
    list does NOT include *home_fd*.
    """
    fds: list[int] = []
    parent_fd = home_fd
    try:
        for name in parts[:-1]:
            child = _open_dir_component(parent_fd, name, create=create)
            fds.append(child)
            parent_fd = child
    except BaseException:
        # An intermediate component failed mid-walk (symlink, TOCTOU race,
        # mkdir/open error). Close the fds already opened before re-raising —
        # the caller never received the list, so it can't close them itself.
        _close_all(fds)
        raise
    return fds


def _close_all(fds: list[int]) -> None:
    for fd in reversed(fds):
        try:
            os.close(fd)
        except OSError:
            pass


def safe_write_bytes(home: Path, path: Path, data: bytes, *, mode: int = 0o644) -> None:
    """Write *data* to *path* (under *home*) without following any symlink.

    Creates missing parent dirs safely. Sets *path* to *mode* (via ``fchmod``,
    bypassing umask). Raises ``ValueError`` if *path* is not under *home*, or
    ``OSError`` on any filesystem error.
    """
    parts = _relative_parts(home, path)
    # ``home`` (e.g. ``/Users/alice``) and everything above it is root-owned and
    # not user-swappable, so creating it is safe; the symlink defense only needs
    # to apply to the components *below* home that the user controls.
    os.makedirs(home, exist_ok=True)
    home_fd = _open_home_dir(home)
    parent_fds: list[int] = []
    try:
        parent_fds = _walk_parents(home_fd, parts, create=True)
        parent_fd = parent_fds[-1] if parent_fds else home_fd
        file_fd = _open_file_for_write(parent_fd, parts[-1], mode)
        try:
            os.fchmod(file_fd, mode)
            view = memoryview(data)
            written = 0
            while written < len(view):
                written += os.write(file_fd, view[written:])
        finally:
            os.close(file_fd)
    finally:
        _close_all(parent_fds)
        os.close(home_fd)


def safe_write_text(home: Path, path: Path, text: str, *, mode: int = 0o644) -> None:
    """UTF-8 ``safe_write_bytes``."""
    safe_write_bytes(home, path, text.encode("utf-8"), mode=mode)


def safe_read_bytes(home: Path, path: Path) -> Optional[bytes]:
    """Read *path* (under *home*) without following any symlink.

    Returns ``None`` (rather than raising) when the file is absent, is reached
    through a symlinked component, is itself a symlink, or is not a regular
    file — so callers treat a hostile/missing target as "no existing config".
    """
    try:
        parts = _relative_parts(home, path)
    except ValueError:
        return None
    try:
        home_fd = _open_home_dir(home)
    except OSError:
        return None
    parent_fds: list[int] = []
    data: Optional[bytes] = None
    try:
        parent_fds = _walk_parents(home_fd, parts, create=False)
        parent_fd = parent_fds[-1] if parent_fds else home_fd
        st = _lstat_at(parent_fd, parts[-1])
        if st is not None and stat.S_ISREG(st.st_mode):
            fd = os.open(parts[-1], _FILE_READ_FLAGS, dir_fd=parent_fd)
            try:
                chunks: list[bytes] = []
                while True:
                    chunk = os.read(fd, 65536)
                    if not chunk:
                        break
                    chunks.append(chunk)
                data = b"".join(chunks)
            finally:
                os.close(fd)
    except OSError:
        data = None
    finally:
        _close_all(parent_fds)
        os.close(home_fd)
    return data


def safe_read_text(home: Path, path: Path) -> Optional[str]:
    """UTF-8 ``safe_read_bytes``; returns ``None`` on missing/hostile/undecodable."""
    raw = safe_read_bytes(home, path)
    if raw is None:
        return None
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return None


def safe_chown_within_home(home: Path, path: Path, uid: int, gid: int) -> None:
    """Chown *path* and its ancestor dirs up to (excluding) *home* to *uid*/*gid*.

    Walks the chain with ``O_NOFOLLOW`` and chowns the resulting fds via
    ``fchown``, so no symlink is ever followed. This reclaims historical
    root-owned config that older installs left in the user's home, without the
    link-following escalation of a plain ``os.chown``. Raises ``ValueError`` if
    *path* is not under *home*, or ``OSError`` if any component is a symlink or
    missing (the operation is all-or-nothing).
    """
    parts = _relative_parts(home, path)
    home_fd = _open_home_dir(home)
    fds: list[int] = []
    try:
        fds = _walk_parents(home_fd, parts, create=False)
        parent_fd = fds[-1] if fds else home_fd
        # Final component may be a file or a dir; refuse to follow a symlink.
        st = _lstat_at(parent_fd, parts[-1])
        if st is None:
            raise FileNotFoundError(errno.ENOENT, "missing target", parts[-1])
        if stat.S_ISLNK(st.st_mode):
            raise OSError(errno.ELOOP, "symlinked target", parts[-1])
        # Open the final target with flags matching its type: a dir needs
        # ``O_DIRECTORY`` so the ``O_NOFOLLOW`` open can't be tricked into
        # succeeding on a non-dir, keeping it consistent with the ancestor walk.
        final_flags = _DIR_OPEN_FLAGS if stat.S_ISDIR(st.st_mode) else _FILE_READ_FLAGS
        final_fd = os.open(parts[-1], final_flags, dir_fd=parent_fd)
        fds.append(final_fd)
        for fd in fds:
            os.fchown(fd, uid, gid)
    finally:
        _close_all(fds)
        os.close(home_fd)


# --- Scope-aware dispatch --------------------------------------------------
#
# Callers that write/read the same config in two scopes (root-in-user-home vs
# the running user's own home) share one branch here instead of re-deriving
# ``if mdm: safe_* else: plain`` at every call site. ``home is None`` means
# "no privilege boundary" (the running user owns the path) and uses plain path
# ops; a non-``None`` ``home`` is the trusted anchor for the link-safe walk.


def console_home_anchor(config_dir: Path, *, mdm: bool) -> Optional[Path]:
    """Trusted ``O_NOFOLLOW`` anchor for a root MDM write into the console home.

    MDM-scope Claude Code / Hermes installs run as root and write into the
    console user's home (``~/.claude`` / ``~/.hermes``), which a non-admin user
    controls and can seed with symlinks. Every read/write must walk from a
    trusted anchor whose parent (``/Users`` / ``/home``) is root-owned and not
    user-swappable, so a planted symlink can't redirect a root op (ENG-3217 /
    CWE-59,61).

    The anchor is the *console user's home* itself, resolved from
    ``find_console_user_home()`` (the same source ``enterprise_claude_code_dir``
    / ``enterprise_hermes_dir`` build the config dir from). Deriving it from the
    config file's own depth (``config_dir.parent``) only holds for the current
    depth-2 layout; a config nested deeper would silently anchor the walk inside
    user-controlled territory. When no console user resolves (dev / single-user,
    where ``enterprise_*_dir`` falls back to ``Path.home()/.<client>``), fall
    back to ``config_dir.parent`` — which is then the running user's own home.

    Returns ``None`` for user scope (the running user owns the path; no
    privilege boundary) and on Windows (the ``safe_fs`` O_NOFOLLOW/O_DIRECTORY
    helpers are POSIX-only), letting the ``maybe_safe_*`` dispatch fall through
    to plain path ops.
    """
    if not mdm or platform.system() == "Windows":
        return None
    # Imported lazily — ``console_user`` pulls in ``credential_gate`` and would
    # otherwise create an import cycle (``console_user`` imports from here).
    from runlayer_cli.hook_install.console_user import (  # noqa: PLC0415
        find_console_user_home,
    )

    home = find_console_user_home()
    return config_dir.parent if home is None else home


def maybe_safe_read_text(path: Path, *, home: Optional[Path]) -> Optional[str]:
    """Link-safe read when *home* is set, plain read otherwise.

    Returns ``None`` when the file is missing or unreadable (and, in link-safe
    mode, when it is reached through / is itself a symlink or non-regular file).
    """
    if home is not None:
        return safe_read_text(home, path)
    if not path.exists():
        return None
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def maybe_safe_read_bytes(path: Path, *, home: Optional[Path]) -> Optional[bytes]:
    """Bytes counterpart of :func:`maybe_safe_read_text`."""
    if home is not None:
        return safe_read_bytes(home, path)
    if not path.exists():
        return None
    try:
        return path.read_bytes()
    except OSError:
        return None


def maybe_safe_write_text(
    path: Path, text: str, *, home: Optional[Path], mode: int = 0o644
) -> None:
    """Link-safe write when *home* is set, plain write otherwise.

    The plain branch creates missing parents and writes UTF-8 at *mode*, so both
    branches leave the same on-disk result.
    """
    maybe_safe_write_bytes(path, text.encode("utf-8"), home=home, mode=mode)


def maybe_safe_write_bytes(
    path: Path, data: bytes, *, home: Optional[Path], mode: int = 0o644
) -> None:
    """Bytes counterpart of :func:`maybe_safe_write_text`."""
    if home is not None:
        safe_write_bytes(home, path, data, mode=mode)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    os.chmod(path, mode)


__all__ = [
    "console_home_anchor",
    "maybe_safe_read_bytes",
    "maybe_safe_read_text",
    "maybe_safe_write_bytes",
    "maybe_safe_write_text",
    "safe_chown_within_home",
    "safe_read_bytes",
    "safe_read_text",
    "safe_write_bytes",
    "safe_write_text",
]
