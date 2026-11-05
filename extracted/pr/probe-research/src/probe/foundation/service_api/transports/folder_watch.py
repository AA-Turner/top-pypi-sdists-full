"""Wake when a file appears in one folder, blocking: Linux inotify (ctypes), macOS kqueue (`select.kqueue`).

The service waits on the drop folder with it (no poll: its fd is a reader on the event loop), and a
drop client waits on its answer with it. OSError where neither exists or the kernel refuses one.
"""

from __future__ import annotations

import contextlib
import errno
import os
import select
import sys

#: inotify(7): a file was made, renamed in, or closed after writing; the folder itself went away.
_IN_CLOSE_WRITE = 0x008
_IN_MOVED_TO = 0x080
_IN_CREATE = 0x100
_IN_DELETE_SELF = 0x400
#: The folder itself was renamed (a swap: the holder looks again).
_IN_MOVE_SELF = 0x800
#: A path watch: a folder, never one reached through a link (`IN_ONLYDIR`, `IN_DONT_FOLLOW`).
_IN_ONLYDIR = 0x01000000
_IN_DONT_FOLLOW = 0x02000000
_IN_NONBLOCK = 0o4000
_IN_CLOEXEC = 0o2000000
#: macOS `O_EVTONLY`: a descriptor for events only (the folder can still be deleted).
_O_EVTONLY = 0x8000


class FolderWatch:
    """A blocking watch on one folder: `wait(timeout)`, or `get_descriptor()` for an event loop's reader.
    `dir_fd`: the folder a descriptor holds open, whatever its path names now (the service's drop
    folder, ROOT 1); else `folder`, never through a link."""

    def __init__(self, folder: str | os.PathLike | None = None, *, dir_fd: int | None = None) -> None:
        self._fd: int | None = None
        self._kqueue = None
        self._folder_fd: int | None = None
        if sys.platform.startswith("linux"):
            if dir_fd is not None:
                self._fd = _make_inotify(f"/proc/self/fd/{dir_fd}".encode(), _IN_ONLYDIR)
            else:
                self._fd = _make_inotify(os.fsencode(os.fspath(folder)), _IN_ONLYDIR | _IN_DONT_FOLLOW)
        elif hasattr(select, "kqueue"):
            self._folder_fd = os.dup(dir_fd) if dir_fd is not None else os.open(
                os.fsencode(os.fspath(folder)), os.O_RDONLY | _O_EVTONLY | getattr(os, "O_NOFOLLOW", 0))
            try:
                self._kqueue = select.kqueue()
                change = select.kevent(self._folder_fd, filter=select.KQ_FILTER_VNODE,
                                       flags=select.KQ_EV_ADD | select.KQ_EV_CLEAR,
                                       fflags=select.KQ_NOTE_WRITE | select.KQ_NOTE_DELETE
                                       | select.KQ_NOTE_RENAME)
                self._kqueue.control([change], 0, 0)
            except BaseException:
                self.close()
                raise
        else:
            raise OSError(errno.ENOSYS, "no folder watch on this platform")

    def get_descriptor(self) -> int:
        return self._fd if self._fd is not None else self._kqueue.fileno()

    def clear(self) -> None:
        """Read what is pending (never blocks): the next `wait` waits for something new."""
        if self._fd is not None:
            with contextlib.suppress(BlockingIOError, InterruptedError):
                while os.read(self._fd, 65536):
                    pass
        elif self._kqueue is not None:
            with contextlib.suppress(OSError):
                self._kqueue.control(None, 64, 0)

    def wait(self, timeout: float) -> bool:
        """Did the folder change within `timeout` seconds (pending changes cleared)?"""
        ready, _, _ = select.select([self.get_descriptor()], [], [], max(0.0, timeout))
        if ready:
            self.clear()
        return bool(ready)

    def close(self) -> None:
        for name in ("_fd", "_folder_fd"):
            fd = getattr(self, name)
            if fd is not None:
                with contextlib.suppress(OSError):
                    os.close(fd)
                setattr(self, name, None)
        if self._kqueue is not None:
            with contextlib.suppress(OSError):
                self._kqueue.close()
            self._kqueue = None

    def __enter__(self) -> FolderWatch:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


def _make_inotify(path: bytes, extra: int = 0) -> int:
    import ctypes  # noqa: PLC0415 -- only where a watch is made

    libc = ctypes.CDLL(None, use_errno=True)
    fd = libc.inotify_init1(_IN_NONBLOCK | _IN_CLOEXEC)
    if fd < 0:
        code = ctypes.get_errno()
        raise OSError(code, f"inotify_init1: {os.strerror(code)}")
    mask = _IN_CREATE | _IN_MOVED_TO | _IN_CLOSE_WRITE | _IN_DELETE_SELF | _IN_MOVE_SELF | extra
    if libc.inotify_add_watch(fd, path, mask) < 0:
        code = ctypes.get_errno()
        os.close(fd)
        raise OSError(code, f"inotify_add_watch: {os.strerror(code)}")
    return fd
