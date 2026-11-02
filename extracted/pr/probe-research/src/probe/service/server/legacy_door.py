"""the socket clients from before the machine key still connect to."""

from __future__ import annotations

import asyncio
import contextlib
import os
import socket
import time
from collections.abc import Callable
from pathlib import Path

from ...foundation.service_api import paths
from ...foundation.service_api.wire import MAX_LINE_BYTES
from probe.service.server.lifecycle import STOPPING_NAME, STOPPING_WAIT_S
from probe.service.server.policy import _env_float, log
#: While another process holds the pre-machine-key folder's lock (a service
#: from before the key, still running), look again this often (plan D8).
LEGACY_RETRY_S = 10.0
LEGACY_RETRY_ENV = "PROBE_SERVICE_LEGACY_RETRY_S"


class LegacyDoor:
    """The socket clients from before the machine key connect to (plan D8).

    A session started before the update that brought the key runs a tap, and
    a desktop app not yet updated computes, `~/.local/state/probe/service/
    service.sock`. This service serves that path too whenever it holds that
    folder's `service.lock`, exactly as the service of that time did, so those
    clients register, read status and run actions here. While another process
    holds it (a service from before the key, still running), it looks again
    every LEGACY_RETRY_S. One per HOME: on a shared home folder, one machine's
    service serves the old clients, as before the key."""

    def __init__(self) -> None:
        self.fd: int | None = None
        self.server: asyncio.AbstractServer | None = None
        self.bound: tuple[int, int] | None = None
        self.path = paths.legacy_socket_path()
        self._retry: asyncio.TimerHandle | None = None
        self._loop: asyncio.AbstractEventLoop | None = None
        self._handler: Callable | None = None
        self.retry_s = _env_float(LEGACY_RETRY_ENV, LEGACY_RETRY_S)

    async def open(self, loop: asyncio.AbstractEventLoop, handler: Callable) -> None:
        self._loop, self._handler = loop, handler
        await self._try()

    async def _try(self) -> None:
        self._retry = None
        if self.server is not None or self._loop is None:
            return
        fd = _take_lock(paths.legacy_lock_path(), wait_for_stopping=False)
        if fd is None:
            self._retry = self._loop.call_later(self.retry_s, lambda: asyncio.ensure_future(self._try()))
            return
        try:
            paths.private_dir(self.path.parent)
            listen = _bind(self.path)
            st = os.stat(self.path)
            self.server = await asyncio.start_unix_server(self._handler, sock=listen, limit=MAX_LINE_BYTES + 1)
        except OSError as exc:
            log(f"cannot serve the pre-machine-key socket {self.path}: {exc}")
            os.close(fd)
            self._retry = self._loop.call_later(self.retry_s, lambda: asyncio.ensure_future(self._try()))
            return
        self.fd = fd
        self.bound = (st.st_dev, st.st_ino)
        log(f"also serving {self.path} (clients from before the machine key)")

    def close(self) -> None:
        if self._retry is not None:
            self._retry.cancel()
            self._retry = None
        if self.server is not None:
            self.server.close()
            self.server = None
        # Unlink only OUR socket, and before the lock goes, as `run_service` does.
        with contextlib.suppress(OSError):
            st = os.stat(self.path)
            if self.bound is not None and (st.st_dev, st.st_ino) == self.bound:
                os.unlink(self.path)
        if self.fd is not None:
            with contextlib.suppress(OSError):
                os.close(self.fd)
            self.fd = None


def _take_lock(path: Path | None = None, *, wait_for_stopping: bool = True) -> int | None:
    """The life-long `service.lock` (this machine's, unless `path` names
    another), or None when another service holds it."""
    try:
        fd = os.open(path or paths.lock_path(), os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0), 0o600)
    except OSError:
        if path is None:
            raise
        return None
    deadline = None
    while True:
        if paths.try_lock(fd):
            return fd
        # A service that is stopping lets go within moments; one that runs
        # does not, and then this instance is the duplicate and leaves.
        if not wait_for_stopping or not (paths.service_dir() / STOPPING_NAME).exists():
            os.close(fd)
            return None
        if deadline is None:
            deadline = time.monotonic() + STOPPING_WAIT_S
        if time.monotonic() >= deadline:
            os.close(fd)
            return None
        time.sleep(0.05)


def _bind(path: Path) -> socket.socket:
    """Bind the socket 0600 (we hold service.lock, so anything there is stale)."""
    with contextlib.suppress(FileNotFoundError):
        os.unlink(path)
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    old = os.umask(0o177)
    try:
        sock.bind(str(path))
    finally:
        os.umask(old)
    os.chmod(path, 0o600)
    sock.listen(64)
    sock.setblocking(False)
    return sock
