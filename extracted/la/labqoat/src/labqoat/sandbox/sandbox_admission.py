"""Patience with a sandbox host whose budget is full."""

from asyncio import sleep as pause_async
from collections.abc import Iterator
from time import monotonic
from time import sleep as pause
from typing import ClassVar

from labqoat.sandbox.sandbox_capacity_error import SandboxCapacityError
from labqoat.sandbox.sandbox_request import SandboxRequest
from labqoat.sandbox.sandbox_transport import SandboxTransport


class SandboxAdmission:
    """Ask for a sandbox again while the host's budget is full, until it is admitted or the wait is over.

    A refusal for capacity creates nothing, so the same request is safe to repeat. Pauses start short, so a
    sandbox freed a moment ago is taken at once, and double up to a second. The last attempt's refusal is
    the caller's.
    """

    FIRST_PAUSE: ClassVar[float] = 0.05
    LONGEST_PAUSE: ClassVar[float] = 1.0

    def __init__(self, transport: SandboxTransport, wait: float) -> None:
        """Start the wait now: no pause begins that would end more than ``wait`` seconds from this moment."""
        self._transport = transport
        self._deadline = monotonic() + wait

    def send(self, request: SandboxRequest) -> bytes:
        """Return the host's answer, pausing between refusals for capacity."""
        for seconds in self._pauses():
            try:
                return self._transport.send(request)
            except SandboxCapacityError:
                pause(seconds)
        return self._transport.send(request)

    async def send_async(self, request: SandboxRequest) -> bytes:
        """Return the host's answer without blocking the event loop between refusals."""
        for seconds in self._pauses():
            try:
                return await self._transport.send_async(request)
            except SandboxCapacityError:
                await pause_async(seconds)
        return await self._transport.send_async(request)

    def _pauses(self) -> Iterator[float]:
        """Yield each pause that still ends within the wait."""
        seconds = self.FIRST_PAUSE
        while monotonic() + seconds <= self._deadline:
            yield seconds
            seconds = min(seconds * 2, self.LONGEST_PAUSE)
