"""Patience with the platform while it finds a sandbox room, or launches a host to make some."""

from asyncio import sleep as pause_async
from asyncio import to_thread
from collections.abc import Iterator
from time import monotonic
from time import sleep as pause
from typing import ClassVar

from labqoat.sandbox.sandbox_capacity_error import SandboxCapacityError
from labqoat.sandbox.sandbox_error import SandboxError
from labqoat.sandbox.sandbox_host_template import SandboxHostTemplate
from labqoat.sandbox.sandbox_request import SandboxRequest
from labqoat.sandbox.sandbox_transport import SandboxTransport


class SandboxPlacement:
    """Ask for a sandbox again while no host has room, until it is placed or the wait is over.

    A refusal for room places nothing, and asking again under the same identifier starts at most one sandbox,
    so the request is safe to repeat. A project the platform has no host function for yet is given it, once,
    before the request is repeated. Pauses start short and double up to two seconds; the last attempt's
    refusal is the caller's.
    """

    FIRST_PAUSE: ClassVar[float] = 0.25
    LONGEST_PAUSE: ClassVar[float] = 2.0

    def __init__(self, transport: SandboxTransport, template: SandboxHostTemplate, wait: float) -> None:
        """Start the wait now: no pause begins that would end more than ``wait`` seconds from this moment."""
        self._transport = transport
        self._template = template
        self._deadline = monotonic() + wait
        self._published = False

    def send(self, request: SandboxRequest) -> bytes:
        """Return the platform's answer, pausing between refusals for room."""
        for seconds in self._pauses():
            try:
                return self._transport.send(request)
            except SandboxCapacityError:
                pause(seconds)
            except SandboxError as error:
                self._publish(error)
        return self._transport.send(request)

    async def send_async(self, request: SandboxRequest) -> bytes:
        """Return the platform's answer without blocking the event loop between refusals."""
        for seconds in self._pauses():
            try:
                return await self._transport.send_async(request)
            except SandboxCapacityError:
                await pause_async(seconds)
            except SandboxError as error:
                await self._publish_async(error)
        return await self._transport.send_async(request)

    def _publish(self, error: SandboxError) -> None:
        """Give the host function when that is what the platform needs; any other refusal is the caller's."""
        self._first_template(error)
        self._template.give(self._transport)

    async def _publish_async(self, error: SandboxError) -> None:
        """Give the host function without blocking the event loop; see ``_publish``."""
        self._first_template(error)
        await to_thread(self._template.give, self._transport)

    def _first_template(self, error: SandboxError) -> None:
        """Re-raise anything but the first request for the host function."""
        if error.code != "host_template_required" or self._published:
            raise error
        self._published = True

    def _pauses(self) -> Iterator[float]:
        """Yield each pause that still ends within the wait."""
        seconds = self.FIRST_PAUSE
        while monotonic() + seconds <= self._deadline:
            yield seconds
            seconds = min(seconds * 2, self.LONGEST_PAUSE)
