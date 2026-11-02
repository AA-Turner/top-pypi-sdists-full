"""Replay physical input deliveries over one persistent scoped connection without reminting credentials."""

import asyncio
import secrets
import time
from collections.abc import AsyncGenerator
from contextlib import aclosing
from dataclasses import dataclass
from uuid import uuid4

from labqoat.json_document import JsonDocument
from labqoat.worker.worker_api import WorkerApi
from labqoat.worker.worker_api_error import WorkerApiError


@dataclass(frozen=True)
class PoolDeliveryStream:
    """Reconnect within the physical lease margin using exactly the same delivery identity and secret."""

    api: WorkerApi

    async def receive(self) -> AsyncGenerator[JsonDocument, None]:
        """Retain active assignments across disconnects; authoritative closure ends delivery cleanly."""
        async with aclosing(self._receive()) as deliveries:
            async for delivery in deliveries:
                if delivery.get("heartbeat") is not True:
                    yield delivery

    async def _receive(self) -> AsyncGenerator[JsonDocument, None]:
        """Only uninterrupted transport failure consumes the reconnect budget; activity resets it."""
        request = JsonDocument(delivery_id=str(uuid4()), secret=secrets.token_hex(32))
        started: float | None = None
        delay = 1.0
        while True:
            connection = self._connection(request)
            try:
                async for delivery in connection:
                    started, delay = None, 1.0
                    yield delivery
                return
            except WorkerApiError as error:
                now = time.monotonic()
                started = now if started is None else started
                transient = error.status is None or error.status >= 500 or error.status in {408, 429}
                if not transient or now - started >= 600:
                    raise
                await asyncio.sleep(delay)
                delay = min(delay * 2, 30)
            finally:
                await connection.aclose()

    async def _connection(self, request: JsonDocument) -> AsyncGenerator[JsonDocument, None]:
        """Own one transport and distinguish authoritative closure from a truncated connection."""
        async with aclosing(self.api.pool_deliveries(request)) as deliveries:
            async for delivery in deliveries:
                if delivery.get("closed") is True:
                    return
                yield delivery
        raise WorkerApiError("Worker delivery stream closed before authoritative shutdown")
