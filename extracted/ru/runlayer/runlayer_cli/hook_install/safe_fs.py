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

The descriptor-relative helpers are POSIX-only because ``O_NOFOLLOW`` /
``O_DIRECTORY`` do not exist on Windows. Windows SYSTEM callers use a
conservative symlink/reparse-point preflight. All MDM-scope writes on Windows
(``home=None``) follow up with a ``CreateFileW`` open using
``FILE_FLAG_OPEN_REPARSE_POINT`` so the write itself is atomic with reparse-
point detection at the **final** path component — closing the TOCTOU window
between the preflight and ``os.open`` that a symlink planted in the race could
otherwise exploit (CWE-59/61). Note: ``FILE_FLAG_OPEN_REPARSE_POINT`` protects
only the final component; intermediate directory reparse points (junctions)
swapped after the preflight may still be traversed, as Windows lacks a
per-component ``O_NOFOLLOW`` equivalent for ancestor directories.
"""

from __future__ import annotations

import ctypes
import ctypes.wintypes
import errno
import os
import platform
import stat
from pathlib import Path
from typing import Callable, Optional, TypedDict

try:
    import msvcrt
except ImportError:
    msvcrt = None  # ty: ignore[invalid-assignment]

# ``getattr`` fallbacks keep this module importable on Windows (where these
# flags are absent); the helpers are never called there.
_O_NOFOLLOW = getattr(os, "O_NOFOLLOW", 0)
_O_DIRECTORY = getattr(os, "O_DIRECTORY", 0)
_O_CLOEXEC = getattr(os, "O_CLOEXEC", 0)
_O_BINARY = getattr(os, "O_BINARY", 0)

_DIR_OPEN_FLAGS = os.O_RDONLY | _O_DIRECTORY | _O_NOFOLLOW | _O_CLOEXEC
_FILE_READ_FLAGS = os.O_RDONLY | _O_NOFOLLOW | _O_CLOEXEC

# ``O_NOFOLLOW`` is absent on Windows. All MDM-scope writes (``home=None``)
# use ``CreateFileW`` with these constants to make the open itself refuse a
# reparse-point final component — closing the TOCTOU window at the final step.
_FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000
_FILE_ATTRIBUTE_REPARSE_POINT = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
_WIN32_TO_ERRNO: dict[int, int] = {
    2: errno.ENOENT,  # ERROR_FILE_NOT_FOUND
    3: errno.ENOENT,  # ERROR_PATH_NOT_FOUND
    5: errno.EACCES,  # ERROR_ACCESS_DENIED
    80: errno.EEXIST,  # ERROR_FILE_EXISTS
    183: errno.EEXIST,  # ERROR_ALREADY_EXISTS
}


class FileReadResult(TypedDict):
    """Bytes and permission bits captured from the same open file."""

    data: bytes
    mode: int


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


def _open_dir_component(
    parent_fd: int,
    name: str,
    *,
    create: bool,
    replace_symlink: bool = True,
) -> int:
    """Open child directory *name* under *parent_fd* without following symlinks.

    With ``create=True`` a missing directory is created and a non-dir placeholder
    is replaced. Symlinks are replaced only when *replace_symlink* is true.
    With ``create=False`` a symlink/missing/non-dir entry raises ``OSError``.
    """
    st = _lstat_at(parent_fd, name)
    if st is not None and stat.S_ISLNK(st.st_mode):
        if not create or not replace_symlink:
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


def _open_file_for_write(
    parent_fd: int,
    name: str,
    mode: int,
    *,
    replace_symlink: bool,
) -> int:
    """Open *name* for writing under *parent_fd* without following a symlink.

    A pre-existing symlink is unlinked (the link, not its target) and a fresh
    file created. Regular files remain intact until the caller applies the
    requested mode. Anything else (dir, fifo, …) is refused.
    """
    st = _lstat_at(parent_fd, name)
    if st is not None and stat.S_ISLNK(st.st_mode):
        if not replace_symlink:
            raise OSError(errno.ELOOP, "refusing to replace symlink", name)
        os.unlink(name, dir_fd=parent_fd)
        st = None
    flags = os.O_WRONLY | _O_NOFOLLOW | _O_CLOEXEC
    if st is None:
        flags |= os.O_CREAT | os.O_EXCL
    elif not stat.S_ISREG(st.st_mode):
        raise OSError(errno.EEXIST, "refusing to write non-regular file", name)
    return os.open(name, flags, mode, dir_fd=parent_fd)


def _open_home_dir(home: Path) -> int:
    """Open *home* as a directory, refusing to follow a symlinked home."""
    return os.open(home, _DIR_OPEN_FLAGS)


def _walk_parents(
    home_fd: int,
    parts: tuple[str, ...],
    *,
    create: bool,
    replace_symlink: bool = True,
) -> list[int]:
    """Open dir fds for every component except the last, relative to *home_fd*.

    Returns the opened fds in order (caller owns closing them). The returned
    list does NOT include *home_fd*.
    """
    fds: list[int] = []
    parent_fd = home_fd
    try:
        for name in parts[:-1]:
            child = _open_dir_component(
                parent_fd,
                name,
                create=create,
                replace_symlink=replace_symlink,
            )
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


def _write_all(fd: int, data: bytes, path: Path) -> None:
    view = memoryview(data)
    written = 0
    while written < len(view):
        write_count = os.write(fd, view[written:])
        if write_count == 0:
            raise OSError(errno.EIO, "write returned zero bytes", path)
        written += write_count


def safe_write_bytes(
    home: Path,
    path: Path,
    data: bytes,
    *,
    mode: int = 0o644,
    replace_symlink: bool = True,
) -> None:
    """Write *data* to *path* (under *home*) without following any symlink.

    Creates missing parent dirs safely. Sets *path* to *mode* (via ``fchmod``,
    bypassing umask). Raises ``ValueError`` if *path* is not under *home*, or
    ``OSError`` on any filesystem error. When *replace_symlink* is false, an
    existing symlink anywhere below *home* is preserved and raises ``ELOOP``.
    """
    parts = _relative_parts(home, path)
    # ``home`` (e.g. ``/Users/alice``) and everything above it is root-owned and
    # not user-swappable, so creating it is safe; the symlink defense only needs
    # to apply to the components *below* home that the user controls.
    os.makedirs(home, exist_ok=True)
    home_fd = _open_home_dir(home)
    parent_fds: list[int] = []
    try:
        parent_fds = _walk_parents(
            home_fd,
            parts,
            create=True,
            replace_symlink=replace_symlink,
        )
        parent_fd = parent_fds[-1] if parent_fds else home_fd
        file_fd = _open_file_for_write(
            parent_fd,
            parts[-1],
            mode,
            replace_symlink=replace_symlink,
        )
        try:
            os.fchmod(file_fd, mode)
            os.ftruncate(file_fd, 0)
            _write_all(file_fd, data, path)
        finally:
            os.close(file_fd)
    finally:
        _close_all(parent_fds)
        os.close(home_fd)


def safe_write_text(
    home: Path,
    path: Path,
    text: str,
    *,
    mode: int = 0o644,
    replace_symlink: bool = True,
) -> None:
    """UTF-8 ``safe_write_bytes``."""
    safe_write_bytes(
        home,
        path,
        text.encode("utf-8"),
        mode=mode,
        replace_symlink=replace_symlink,
    )


def safe_read_file(home: Path, path: Path) -> Optional[FileReadResult]:
    """Read *path* and its mode without following any symlink.

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
    result: Optional[FileReadResult] = None
    try:
        parent_fds = _walk_parents(home_fd, parts, create=False)
        parent_fd = parent_fds[-1] if parent_fds else home_fd
        st = _lstat_at(parent_fd, parts[-1])
        if st is not None and stat.S_ISREG(st.st_mode):
            fd = os.open(parts[-1], _FILE_READ_FLAGS, dir_fd=parent_fd)
            try:
                opened_st = os.fstat(fd)
                if stat.S_ISREG(opened_st.st_mode):
                    chunks: list[bytes] = []
                    while True:
                        chunk = os.read(fd, 65536)
                        if not chunk:
                            break
                        chunks.append(chunk)
                    result = {
                        "data": b"".join(chunks),
                        "mode": stat.S_IMODE(opened_st.st_mode),
                    }
            finally:
                os.close(fd)
    except OSError:
        result = None
    finally:
        _close_all(parent_fds)
        os.close(home_fd)
    return result


def safe_read_bytes(home: Path, path: Path) -> Optional[bytes]:
    """Bytes-only counterpart of :func:`safe_read_file`."""
    result = safe_read_file(home, path)
    return result["data"] if result is not None else None


def safe_read_text(home: Path, path: Path) -> Optional[str]:
    """UTF-8 ``safe_read_bytes``; returns ``None`` on missing/hostile/undecodable."""
    raw = safe_read_bytes(home, path)
    if raw is None:
        return None
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return None


def safe_unlink(home: Path, path: Path) -> bool:
    """Delete *path* descriptor-relatively without following ancestor links."""
    try:
        parts = _relative_parts(home, path)
        home_fd = _open_home_dir(home)
    except (OSError, ValueError):
        return False
    parent_fds: list[int] = []
    removed = False
    try:
        parent_fds = _walk_parents(home_fd, parts, create=False)
        parent_fd = parent_fds[-1] if parent_fds else home_fd
        if _lstat_at(parent_fd, parts[-1]) is not None:
            os.unlink(parts[-1], dir_fd=parent_fd)
            removed = True
    except OSError:
        removed = False
    finally:
        _close_all(parent_fds)
        os.close(home_fd)
    return removed


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

    MDM-scope VS Code / Claude Code / Hermes installs run as root and write into
    the console user's home (``~/.copilot/hooks`` / ``~/.claude`` /
    ``~/.hermes``), which a non-admin user controls and can seed with symlinks.
    Every read/write must walk from a trusted anchor whose parent (``/Users`` /
    ``/home``) is root-owned and not user-swappable, so a planted symlink can't
    redirect a root op (ENG-3217 / CWE-59,61).

    The anchor is the *console user's home* itself, resolved from
    ``find_console_user_home()`` (the same source ``enterprise_vscode_dir`` /
    ``enterprise_claude_code_dir`` / ``enterprise_hermes_dir`` build the config
    dir from). Deriving it from the config file's own depth
    (``config_dir.parent``) only holds for the current depth-2 layout; a config
    nested deeper would silently anchor the walk inside user-controlled
    territory. When no console user resolves (dev / single-user, where
    ``enterprise_*_dir`` falls back under ``Path.home()``), fall back to the
    running user's home rather than assuming a fixed config depth.

    Returns ``None`` for user scope (the running user owns the path; no
    privilege boundary) and on Windows (the ``safe_fs`` O_NOFOLLOW/O_DIRECTORY
    helpers are POSIX-only). Windows MDM callers must first use
    :func:`is_unsafe_windows_mdm_path` before falling through to plain path ops.
    """
    if not mdm or platform.system() == "Windows":
        return None
    # Imported lazily — ``console_user`` pulls in ``credential_gate`` and would
    # otherwise create an import cycle (``console_user`` imports from here).
    from runlayer_cli.hook_install.console_user import (  # noqa: PLC0415
        find_console_user_home,
    )

    home = find_console_user_home()
    if home is not None:
        return home
    running_home = Path.home()
    try:
        config_dir.relative_to(running_home)
    except ValueError:
        return config_dir.parent
    return running_home


def path_has_link_or_reparse_point(path: Path) -> bool:
    """Whether *path* or an existing ancestor is a symlink/reparse point.

    Windows lacks the descriptor-relative ``O_NOFOLLOW`` walk used above.
    SYSTEM-context callers use this conservative preflight before plain path
    operations so a user-controlled symlink or junction is never traversed.
    Missing components are allowed; an unreadable component is treated as
    unsafe. ``st_file_attributes`` keeps this compatible with Python 3.10,
    where :meth:`Path.is_junction` is unavailable.
    """
    current = path
    while True:
        try:
            path_stat = current.lstat()
        except FileNotFoundError:
            pass
        except OSError:
            return True
        else:
            attributes = getattr(path_stat, "st_file_attributes", 0)
            if stat.S_ISLNK(path_stat.st_mode) or attributes & getattr(
                stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400
            ):
                return True
        parent = current.parent
        if parent == current:
            return False
        current = parent


def is_unsafe_windows_mdm_path(
    path: Path,
    *,
    mdm: bool,
    path_check: Callable[[Path], bool] = path_has_link_or_reparse_point,
) -> bool:
    """Whether a Windows MDM path crosses a user-controlled reparse point.

    User-scope operations run with the same privileges as the path owner, so
    they intentionally retain the normal filesystem behavior. Windows MDM
    operations run as SYSTEM and must preflight every console-home path because
    the POSIX descriptor-relative helpers are unavailable there.
    """
    return mdm and platform.system() == "Windows" and path_check(path)


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


def maybe_safe_read_file(
    path: Path, *, home: Optional[Path]
) -> Optional[FileReadResult]:
    """Read bytes and mode from one descriptor; link-safe when *home* is set."""
    if home is not None:
        return safe_read_file(home, path)
    if not path.exists():
        return None
    try:
        with path.open("rb") as file:
            opened_st = os.fstat(file.fileno())
            if not stat.S_ISREG(opened_st.st_mode):
                return None
            return {
                "data": file.read(),
                "mode": stat.S_IMODE(opened_st.st_mode),
            }
    except OSError:
        return None


def _windows_open_no_reparse(path: Path, mode: int) -> int:
    """Open *path* for writing on Windows, refusing to follow a reparse point.

    ``CreateFileW`` with ``FILE_FLAG_OPEN_REPARSE_POINT`` opens the entry at
    *path* itself — never a symlink/junction target at the **final** component.
    After the open, the handle's ``st_file_attributes`` is checked atomically:
    a reparse point raises ``ELOOP`` before any data is written, closing the
    TOCTOU window a preflight ``lstat`` + plain ``os.open`` would leave at the
    final component. Intermediate directory reparse points may still be
    traversed (Windows limitation — no per-component ``O_NOFOLLOW`` for
    ancestor directories).

    ctypes seam (hard to unit-test on non-Windows); callers monkeypatch this in
    tests.
    """
    if msvcrt is None:
        # Not on a real Windows system (e.g. tests with ``platform.system``
        # mocked to "Windows" while running on POSIX). Fall back to a plain
        # ``os.open`` with an ``is_symlink`` guard so the caller's write path
        # remains exercisable. The real TOCTOU-safe ``CreateFileW`` path runs
        # only on actual Windows.
        if path.is_symlink():
            raise OSError(errno.ELOOP, "refusing to write through symlink", str(path))
        return os.open(
            path,
            os.O_WRONLY | os.O_CREAT | _O_CLOEXEC | _O_BINARY,
            mode,
        )

    _GENERIC_WRITE = 0x40000000
    _FILE_SHARE_ALL = 0x00000007
    _OPEN_ALWAYS = 4
    _FILE_ATTRIBUTE_NORMAL = 0x80

    # Use use_last_error=True so ctypes captures the thread-local LastError
    # value immediately after the CreateFileW call and ctypes.get_last_error()
    # returns it accurately (without use_last_error the value is stale/zero).
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)  # ty: ignore[unresolved-attribute]
    create_file = kernel32.CreateFileW
    create_file.restype = ctypes.wintypes.HANDLE
    create_file.argtypes = [
        ctypes.wintypes.LPCWSTR,
        ctypes.wintypes.DWORD,
        ctypes.wintypes.DWORD,
        ctypes.c_void_p,
        ctypes.wintypes.DWORD,
        ctypes.wintypes.DWORD,
        ctypes.wintypes.HANDLE,
    ]

    handle = create_file(
        str(path),
        _GENERIC_WRITE,
        _FILE_SHARE_ALL,
        None,
        _OPEN_ALWAYS,
        _FILE_FLAG_OPEN_REPARSE_POINT | _FILE_ATTRIBUTE_NORMAL,
        None,
    )
    invalid = ctypes.c_void_p(-1).value
    if not handle or handle == invalid:
        code = int(ctypes.get_last_error())  # ty: ignore[unresolved-attribute]
        raise OSError(
            _WIN32_TO_ERRNO.get(code, errno.EIO),
            f"CreateFileW failed (Win32 error {code})",
            str(path),
        )
    try:
        fd = msvcrt.open_osfhandle(handle, 0)  # ty: ignore[unresolved-attribute]
    except OSError:
        kernel32.CloseHandle(handle)
        raise
    try:
        msvcrt.setmode(fd, _O_BINARY)  # ty: ignore[unresolved-attribute]
        opened_st = os.fstat(fd)
        attributes = getattr(opened_st, "st_file_attributes", 0)
        if attributes & _FILE_ATTRIBUTE_REPARSE_POINT:
            raise OSError(
                errno.ELOOP, "refusing to write through reparse point", str(path)
            )
    except BaseException:
        os.close(fd)
        raise
    return fd


def maybe_safe_write_text(
    path: Path,
    text: str,
    *,
    home: Optional[Path],
    mode: int = 0o644,
    replace_symlink: bool = True,
) -> None:
    """Link-safe write when *home* is set, plain write otherwise.

    The plain branch creates missing parents and writes UTF-8 at *mode*, so both
    branches leave the same on-disk result.
    """
    maybe_safe_write_bytes(
        path,
        text.encode("utf-8"),
        home=home,
        mode=mode,
        replace_symlink=replace_symlink,
    )


def maybe_safe_write_bytes(
    path: Path,
    data: bytes,
    *,
    home: Optional[Path],
    mode: int = 0o644,
    replace_symlink: bool = True,
) -> None:
    """Bytes counterpart of :func:`maybe_safe_write_text`."""
    if home is not None:
        safe_write_bytes(
            home,
            path,
            data,
            mode=mode,
            replace_symlink=replace_symlink,
        )
        return
    # Windows MDM writes (home=None) run as SYSTEM into user-controlled
    # directories. The POSIX O_NOFOLLOW walk is unavailable, so
    # ``_windows_open_no_reparse`` uses ``CreateFileW`` with
    # ``FILE_FLAG_OPEN_REPARSE_POINT`` to make the open itself atomic with
    # reparse-point detection at the final component — closing the TOCTOU
    # window between the preflight ``is_unsafe_windows_mdm_path`` and the
    # write (CWE-59/61, ENG-3217). This applies to all home=None writes on
    # Windows, not only those with replace_symlink=False, because every MDM
    # caller may reach a user-controlled path.
    is_windows = platform.system() == "Windows"
    if not is_windows and not replace_symlink and path.is_symlink():
        raise OSError(errno.ELOOP, "refusing to replace symlink", path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if is_windows:
        file_fd = _windows_open_no_reparse(path, mode)
    else:
        flags = os.O_WRONLY | os.O_CREAT | _O_CLOEXEC | _O_BINARY
        file_fd = os.open(path, flags, mode)
    try:
        if is_windows:
            os.chmod(path, mode)
        else:
            os.fchmod(file_fd, mode)
        os.ftruncate(file_fd, 0)
        _write_all(file_fd, data, path)
    finally:
        os.close(file_fd)


def maybe_safe_unlink(path: Path, *, home: Optional[Path]) -> bool:
    """Descriptor-relative unlink when *home* is set, plain unlink otherwise."""
    if home is not None:
        return safe_unlink(home, path)
    try:
        path.unlink()
    except FileNotFoundError:
        return False
    return True


__all__ = [
    "console_home_anchor",
    "is_unsafe_windows_mdm_path",
    "maybe_safe_read_bytes",
    "maybe_safe_read_file",
    "maybe_safe_read_text",
    "maybe_safe_unlink",
    "maybe_safe_write_bytes",
    "maybe_safe_write_text",
    "path_has_link_or_reparse_point",
    "safe_chown_within_home",
    "safe_read_bytes",
    "safe_read_file",
    "safe_read_text",
    "safe_unlink",
    "safe_write_bytes",
    "safe_write_text",
]
