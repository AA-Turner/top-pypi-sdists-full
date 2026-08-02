"""Channel port for task communication."""

from collections.abc import AsyncIterator
from typing import Protocol, runtime_checkable

from mistralai.vibe.sdk.transports.events import DownstreamMessage, UpstreamMessage


@runtime_checkable
class Channel(Protocol):
    """The parent's handle to a running task."""

    def __aiter__(self) -> AsyncIterator[DownstreamMessage]: ...
    async def send(self, message: UpstreamMessage) -> None: ...
    async def close(self) -> None: ...


__all__ = ["Channel"]
