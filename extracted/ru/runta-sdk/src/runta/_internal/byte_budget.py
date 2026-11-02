"""Cooperative scheduling after a fixed amount of data processing."""

import asyncio

_YIELD_BYTES = 1024 * 1024


class _ByteBudget:
    def __init__(self) -> None:
        self._bytes = 0

    async def processed(self, size: int) -> None:
        self._bytes += size
        if self._bytes >= _YIELD_BYTES:
            self._bytes = 0
            await asyncio.sleep(0)
