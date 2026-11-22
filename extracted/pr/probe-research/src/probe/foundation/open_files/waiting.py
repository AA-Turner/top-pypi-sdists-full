"""`select.select` for a process past 1,024 open files: select() refuses a descriptor at or above
FD_SETSIZE (1024) with ValueError, and a raised limit hands those out. Stdlib only."""

from __future__ import annotations

import errno
import math
import os
import select
from collections.abc import Iterable

_READ = select.POLLIN | select.POLLPRI if hasattr(select, "poll") else 0
_WRITE = select.POLLOUT if hasattr(select, "poll") else 0
#: Hang-up and error wake both sides, as select() does (the next read or write says what happened).
_EITHER = select.POLLHUP | select.POLLERR if hasattr(select, "poll") else 0


def wait_ready(readers: Iterable, writers: Iterable = (), timeout: float | None = None) -> tuple[list, list]:
    """(readable, writable) of what was passed (ints or objects with `fileno()`), within
    `timeout` seconds (None: until one is). poll() where there is one, as `subprocess` does;
    select() elsewhere (Windows', which has no such limit)."""
    readers, writers = list(readers), list(writers)
    if not hasattr(select, "poll"):
        readable, writable, _ = select.select(readers, writers, [], timeout)
        return readable, writable
    masks: dict[int, int] = {}
    for watched, mask in [*((r, _READ) for r in readers), *((w, _WRITE) for w in writers)]:
        fd = _get_fd(watched)
        masks[fd] = masks.get(fd, 0) | mask
    poller = select.poll()
    for fd, mask in masks.items():
        poller.register(fd, mask)
    wait_ms = None if timeout is None else math.ceil(max(0.0, timeout) * 1000)
    events = dict(poller.poll(wait_ms))
    if any(event & select.POLLNVAL for event in events.values()):
        raise OSError(errno.EBADF, os.strerror(errno.EBADF))
    readable = [r for r in readers if events.get(_get_fd(r), 0) & (_READ | _EITHER)]
    writable = [w for w in writers if events.get(_get_fd(w), 0) & (_WRITE | _EITHER)]
    return readable, writable


def _get_fd(watched) -> int:
    fd = watched if isinstance(watched, int) else watched.fileno()
    if fd < 0:
        raise ValueError("file descriptor cannot be a negative integer")
    return fd
