"""The POSIX calls the SDK path leans on, made to work on Windows too.

On POSIX each name here is a direct pass-through to the POSIX call -- the same
constants, the call made as it was -- so a POSIX caller behaves exactly as it
did before it came through this module. Only Windows takes the other branch.

- ``flock`` / ``LOCK_EX`` / ``LOCK_NB`` / ``LOCK_UN``: ``fcntl.flock``'s advisory
  whole-file lock. Windows has no fcntl (importing it was why ``import probe``
  failed there), so it is ``msvcrt.locking`` on ONE byte at `LOCK_OFFSET`, far
  past any lock file's content: Windows byte-range locks are MANDATORY, and a
  lock on byte 0 would stop every other process reading the pid or run id a
  lease file carries. Same semantics otherwise: exclusive, per open handle (a
  second ``open()`` in the same process conflicts, as a second open file
  description does under flock), released when the handle closes or the process
  dies. A non-blocking attempt that finds the lock taken raises
  ``BlockingIOError``, as flock does; a blocking one waits for as long as it
  takes (msvcrt's own blocking mode gives up after 10 s, so it polls). Unlocking
  a byte that is not locked is a no-op, as ``LOCK_UN`` is. Shared locks are not
  offered: nothing on the SDK path takes one.
- ``probe_pid(pid)``: ``os.kill(pid, 0)`` -- returns if ``pid`` exists, raises
  ``ProcessLookupError`` if not, ``PermissionError`` if it exists but is not ours
  to signal. On Windows ``os.kill(pid, 0)`` is NOT a probe: CPython routes every
  signal other than the two console events to ``TerminateProcess``, so it KILLS
  the process with exit code 0. There it asks ``OpenProcess`` +
  ``GetExitCodeProcess`` instead.
- ``DETACHED``: the ``subprocess.Popen`` keywords for a child that outlives its
  parent and does not share its Ctrl-C: ``start_new_session`` on POSIX (which
  Windows silently ignores), a detached, new process group on Windows.
- ``replace(src, dst)``: ``os.replace``. On Windows a rename onto a file that
  another process has open (a reader of ``status.json``, say) fails with
  ``PermissionError`` for as long as that handle lives -- Python opens files
  without ``FILE_SHARE_DELETE`` -- so it is retried for up to a second there.
- ``O_BINARY``: 0 on POSIX. On Windows ``os.open`` without it hands back a TEXT
  descriptor, which turns every ``\\n`` written into ``\\r\\n`` and ends a read at
  the first 0x1A byte -- ``tempfile`` adds it for the same reason.

Stdlib-only, like `probe.sdk.durable` (which imports it): no httpx at import.
"""

from __future__ import annotations

import errno
import os
import subprocess
import time
from typing import Any

__all__ = [
    "DETACHED",
    "LOCK_EX",
    "LOCK_NB",
    "LOCK_OFFSET",
    "LOCK_UN",
    "O_BINARY",
    "flock",
    "probe_pid",
    "replace",
]

#: Where the Windows lock sits: one byte at 2 GiB - 1, beyond the content of any
#: lock or lease file (locking past the end of a file is allowed there), and
#: below 2**31 so any C runtime's `_locking` offset arithmetic holds it.
LOCK_OFFSET = 0x7FFFFFFF

O_BINARY: int = getattr(os, "O_BINARY", 0)

try:
    import fcntl as _fcntl
except ImportError:  # Windows
    _fcntl = None  # type: ignore[assignment]

if _fcntl is not None:
    LOCK_EX: int = _fcntl.LOCK_EX
    LOCK_NB: int = _fcntl.LOCK_NB
    LOCK_UN: int = _fcntl.LOCK_UN

    def flock(fd: Any, operation: int) -> None:
        """``fcntl.flock``, looked up per call (so a test patching ``fcntl.flock``
        still reaches every caller)."""
        _fcntl.flock(fd, operation)

else:
    # fcntl's values, so a caller's `LOCK_EX | LOCK_NB` means the same thing.
    LOCK_EX = 2
    LOCK_NB = 4
    LOCK_UN = 8

    #: Errnos `msvcrt.locking` reports for "somebody else holds it":
    #: EACCES (ERROR_LOCK_VIOLATION) for a single try, EDEADLOCK after retries.
    _BUSY = {errno.EACCES, getattr(errno, "EDEADLOCK", errno.EDEADLK), errno.EDEADLK}

    def _locking(fd: int, mode: int) -> None:
        """`msvcrt.locking` on the byte at `LOCK_OFFSET`. It locks from the
        descriptor's current position, so move there and put it back: the
        handle may be a lease a caller goes on reading and writing."""
        import msvcrt

        here = os.lseek(fd, 0, os.SEEK_CUR)
        os.lseek(fd, LOCK_OFFSET, os.SEEK_SET)
        try:
            msvcrt.locking(fd, mode, 1)
        finally:
            os.lseek(fd, here, os.SEEK_SET)

    def flock(fd: Any, operation: int) -> None:  # type: ignore[misc]
        """``fcntl.flock`` for LOCK_EX, LOCK_EX | LOCK_NB and LOCK_UN."""
        import msvcrt

        if not isinstance(fd, int):
            fd = fd.fileno()
        if operation & LOCK_UN:
            try:
                _locking(fd, msvcrt.LK_UNLCK)
            except OSError:
                pass  # not locked by this handle: flock's LOCK_UN is a no-op then
            return
        if not operation & LOCK_EX:
            raise ValueError(f"unsupported flock operation {operation!r} on Windows")
        pause = 0.001
        while True:
            try:
                _locking(fd, msvcrt.LK_NBLCK)
                return
            except OSError as exc:
                if exc.errno not in _BUSY:
                    raise
                if operation & LOCK_NB:
                    raise BlockingIOError(errno.EAGAIN, "Resource temporarily unavailable") from None
            time.sleep(pause)
            pause = min(pause * 2, 0.05)


if os.name == "nt":
    _PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    _STILL_ACTIVE = 259
    _ERROR_ACCESS_DENIED = 5

    def probe_pid(pid: int) -> None:  # type: ignore[misc]
        """``os.kill(pid, 0)`` without the kill (see the module docstring)."""
        import ctypes
        from ctypes import wintypes

        pid = int(pid)
        if pid < 0 or pid > 0xFFFFFFFF:
            raise OverflowError(f"pid {pid} out of range")
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.OpenProcess.restype = wintypes.HANDLE
        kernel32.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
        kernel32.GetExitCodeProcess.argtypes = (wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD))
        kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
        handle = kernel32.OpenProcess(_PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if not handle:
            if ctypes.get_last_error() == _ERROR_ACCESS_DENIED:
                raise PermissionError(errno.EPERM, "Operation not permitted")
            raise ProcessLookupError(errno.ESRCH, "No such process")
        try:
            code = wintypes.DWORD()
            if kernel32.GetExitCodeProcess(handle, ctypes.byref(code)) and code.value != _STILL_ACTIVE:
                # Exited; the handle only outlives it while someone holds one.
                raise ProcessLookupError(errno.ESRCH, "No such process")
        finally:
            kernel32.CloseHandle(handle)

    DETACHED: dict = {
        "creationflags": subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
    }

    #: How long `replace` keeps retrying a rename another process's open handle blocks.
    REPLACE_PATIENCE_SECONDS = 1.0

    def replace(src: Any, dst: Any) -> None:  # type: ignore[misc]
        """``os.replace``, retried while an open handle elsewhere blocks it."""
        give_up = time.monotonic() + REPLACE_PATIENCE_SECONDS
        pause = 0.005
        while True:
            try:
                os.replace(src, dst)
                return
            except PermissionError:
                if time.monotonic() >= give_up:
                    raise
            time.sleep(pause)
            pause = min(pause * 2, 0.1)

else:

    def probe_pid(pid: int) -> None:  # type: ignore[misc]
        """``os.kill(pid, 0)``."""
        os.kill(pid, 0)

    DETACHED = {"start_new_session": True}

    def replace(src: Any, dst: Any) -> None:  # type: ignore[misc]
        """``os.replace``."""
        os.replace(src, dst)
