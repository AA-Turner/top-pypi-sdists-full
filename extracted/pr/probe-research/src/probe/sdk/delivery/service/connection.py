"""Connection: one client's connection to a Probe service, as the SDK's methods (`methods.py`) need it:
who is on the other end, the fds its request passed, and a way to send it a line. The machine service's
connection (`service/server/connections`) is this plus its subscriptions."""

from __future__ import annotations

import asyncio
import contextlib

from probe.foundation.service_api.wire import encode

#: A client whose unread messages pass this is dropped, not buffered forever.
MAX_SUBSCRIBER_BUFFER = 4 * 1024 * 1024


class Connection:
    def __init__(self, writer: asyncio.StreamWriter, peer_pid: int | None = None) -> None:
        self.writer = writer
        #: The connecting process, as the kernel says (plan D9); None where it cannot.
        self.peer_pid = peer_pid
        #: Its start time when it connected: the same process later, or not.
        self.peer_start: str | None = None
        self.hello = False
        self.client: str | None = None
        self.keepalive = False
        #: The open files the request being handled passed (`fds.py`); its handler takes them
        #: (`take_fds`), and what it leaves is closed after it.
        self.fds: list[int] = []
        #: The id of the request being handled (an event about it names it: `api.progress`).
        self.request_id: object = None

    def take_fds(self) -> list[int]:
        """The request's fds, now the caller's to close."""
        fds, self.fds = self.fds, []
        return fds

    def is_gone(self) -> bool:
        transport = self.writer.transport
        return transport is None or transport.is_closing()

    def send_nowait(self, message: dict) -> bool:
        transport = self.writer.transport
        if transport is None or transport.is_closing():
            return False
        if transport.get_write_buffer_size() > MAX_SUBSCRIBER_BUFFER:
            transport.abort()
            return False
        self.writer.write(encode(message))
        return True

    async def send(self, message: dict) -> None:
        if self.send_nowait(message):
            with contextlib.suppress(ConnectionError, OSError):
                await self.writer.drain()
