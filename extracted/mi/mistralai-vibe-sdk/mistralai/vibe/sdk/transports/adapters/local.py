"""In-process channel implementation.

LocalChannel is the concrete channel adapter for same-process communication,
backed by asyncio queues.
"""

from __future__ import annotations

import asyncio
import contextlib
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mistralai.vibe.sdk.transports.events import DownstreamMessage, UpstreamMessage


class LocalChannel:
    """In-process channel backed by asyncio queues."""

    def __init__(
        self,
        downstream: asyncio.Queue[DownstreamMessage | None],
        upstream: asyncio.Queue[UpstreamMessage],
        background_task: asyncio.Task[None],
    ) -> None:
        self._downstream = downstream
        self._upstream = upstream
        self._bg = background_task

    async def __aiter__(self) -> AsyncIterator[DownstreamMessage]:
        while True:
            msg = await self._downstream.get()
            if msg is None:
                break
            yield msg
        if self._bg.done():
            exc = self._bg.exception()
            if exc is not None:
                raise exc

    async def send(self, message: UpstreamMessage) -> None:
        await self._upstream.put(message)

    async def close(self) -> None:
        self._bg.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await self._bg


__all__ = ["LocalChannel"]
