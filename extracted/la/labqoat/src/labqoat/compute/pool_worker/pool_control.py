"""Replay physical-worker operations across transient disconnects without changing delivery credentials."""

import asyncio
import secrets
import time
from collections.abc import Awaitable, Callable
from collections.abc import AsyncIterator, AsyncGenerator
from contextlib import asynccontextmanager, aclosing
from dataclasses import dataclass
from functools import partial
from uuid import uuid4

from labqoat.json_document import JsonDocument, JsonValue
from labqoat.worker.worker_api import WorkerApi
from labqoat.worker.worker_api_error import WorkerApiError
from labqoat.worker.session.session_bridge import SessionBridge
from labqoat.worker.session.worker_session import WorkerSession
from labqoat.compute.pool_worker.pool_delivery_stream import PoolDeliveryStream


@dataclass
class PoolControl:
    """Use only the physical worker's scoped authority; each delivered input receives separate credentials."""

    api: WorkerApi
    bridge: SessionBridge | None = None
    capabilities: frozenset[str] = frozenset()

    def accepts_reasons(self) -> bool:
        """Whether the service takes a reason with a failed input, as it says in its deliveries."""
        return "failure_reason" in self.capabilities

    @asynccontextmanager
    async def connected(self, attempt: str, enabled: bool) -> AsyncIterator[None]:
        """Own one session and local bridge for the full lifetime of all admitted input executions."""
        if not enabled:
            yield
            return
        session = WorkerSession(self.api.session_endpoint(), attempt)
        self.bridge = SessionBridge(session)
        try:
            async with session.lifetime(), self.bridge.lifetime():
                yield
        finally:
            self.bridge = None

    async def deliveries(self) -> AsyncGenerator[JsonDocument, None]:
        """Use the negotiated persistent transport while retaining compatibility with older workers."""
        if self.bridge is not None:
            while (delivery := await self.bridge.session.deliveries.get()) is not None:
                yield delivery
            return
        async with aclosing(PoolDeliveryStream(self.api).receive()) as stream:
            async for delivery in stream:
                yield delivery

    async def claim(self, initialized: bool = False) -> JsonDocument:
        """Retain the request nonce across retries so a lost response cannot rotate live input credentials."""
        request: dict[str, JsonValue] = {"delivery_id": str(uuid4()), "secret": secrets.token_hex(32)}
        if initialized:
            request["initialized"] = True
        return await self._retry(partial(self.api.json_async, "POST", "/api/v1/worker/pool/inputs", request))

    async def release(self, attempt_id: str) -> None:
        """Idempotently return an already-finished physical input slot."""
        if self.bridge is not None:
            await self._release(attempt_id, False)
            return
        await self._retry(partial(self.api.json_async, "POST", f"/api/v1/worker/pool/inputs/{attempt_id}/release", {}))

    async def fail_initialization(self, detail: str = "") -> None:
        """Fail waiting inputs with the initializer's bounded diagnostic while physical capacity stays held."""
        request: dict[str, JsonValue] = {
            "delivery_id": str(uuid4()),
            "secret": secrets.token_hex(32),
            "initialization_failed": True,
            "detail": detail[:2000],
        }
        await self._retry(partial(self.api.json_async, "POST", "/api/v1/worker/pool/inputs", request))

    async def fail(self, attempt_id: str, detail: str | None = None, reason: str | None = None) -> None:
        """Atomically fail and release finished authored work before a replacement can observe the old slot.

        A `reason` names why the input's process ended when the supervisor knows, such as `out_of_memory`.
        """
        request: dict[str, JsonValue] = {"failed": True}
        if detail is not None:
            request["detail"] = detail[:2000]
        if reason is not None:
            request["reason"] = reason
        if self.bridge is not None:
            await self._release(attempt_id, True, request)
            return
        await self._retry(
            partial(self.api.json_async, "POST", f"/api/v1/worker/pool/inputs/{attempt_id}/release", request)
        )

    async def _release(self, attempt: str, failed: bool, request: dict[str, JsonValue] | None = None) -> None:
        """Drop delegated local authority only after a durable physical-capacity receipt."""
        bridge = self.bridge
        if bridge is None:
            raise RuntimeError("Worker session has no local bridge")
        await self._retry(partial(bridge.session.request, "release", attempt, request or {"failed": failed}))
        bridge.credentials.release(attempt)

    async def changes(self, revision: int) -> JsonDocument:
        """Reconnect a push-based subscription from the last authoritative fleet revision."""
        path = f"/api/v1/worker/pool/changes?after={revision}"
        return await self._retry(partial(self.api.completion_async, path, "compute_pool"))

    @staticmethod
    async def _retry(operation: Callable[[], Awaitable[JsonDocument]]) -> JsonDocument:
        """Recover transient transport failures only within the control assignment's renewal margin."""
        started = time.monotonic()
        delay = 1.0
        while True:
            try:
                return await operation()
            except WorkerApiError as error:
                transient = error.status is None or error.status >= 500 or error.status in {408, 429}
                if not transient or time.monotonic() - started >= 600:
                    raise
                await asyncio.sleep(delay)
                delay = min(delay * 2, 30)
