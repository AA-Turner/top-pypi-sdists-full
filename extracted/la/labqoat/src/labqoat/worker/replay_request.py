"""Replay only protocol operations with a durable exact-request receipt."""

import time
import asyncio
from collections.abc import Awaitable, Callable, AsyncGenerator
from contextlib import aclosing
from functools import partial
from dataclasses import dataclass
from pathlib import Path

from labqoat.json_document import JsonDocument, JsonValue
from labqoat.worker.scoped_api import ScopedApi
from labqoat.worker.worker_api_error import WorkerApiError
from labqoat.worker.child_result_frame import ChildResultFrame


@dataclass(frozen=True)
class ReplayRequest:
    """Bound transient retries without replaying arbitrary authored effects or legacy mutations."""

    api: ScopedApi

    def send(self, path: str, body: dict[str, JsonValue]) -> JsonDocument:
        """Retry the exact idempotent envelope after uncertain delivery; permanent failures propagate."""
        failures = 0
        started = time.monotonic()
        while True:
            try:
                return self.api.json("POST", path, body)
            except WorkerApiError as error:
                failures += 1
                if not self._retryable(error, failures, started):
                    raise
                time.sleep(min(0.05 * 2 ** (failures - 1), 2.0))

    async def send_async(self, path: str, body: dict[str, JsonValue]) -> JsonDocument:
        """Replay a batch of independently keyed admissions after uncertain response delivery."""
        return await self._replay(partial(self.api.json_async, "POST", path, body))

    def upload(self, path: str, source: Path, byte_size: int) -> bytes:
        """Replay immutable asset bytes, reopening the file from its beginning on each attempt."""
        failures = 0
        started = time.monotonic()
        while True:
            try:
                return self.api.upload_file(path, source, byte_size)
            except WorkerApiError as error:
                failures += 1
                if not self._retryable(error, failures, started):
                    raise
                time.sleep(min(0.05 * 2 ** (failures - 1), 2.0))

    async def completions(self, ids: list[str]) -> JsonDocument:
        """Reconnect the same pending result identities after a transient stream failure."""
        return await self._replay(partial(self.api.child_completions, ids))

    async def updates(self, ids: list[str]) -> AsyncGenerator[JsonDocument, None]:
        """Resume only undelivered children after local or remote stream interruption."""
        pending = list(ids)
        failures, started = 0, time.monotonic()
        while pending:
            updates = self._updates(pending)
            try:
                async for response in updates:
                    failures, started = 0, time.monotonic()
                    yield response
            except WorkerApiError as error:
                failures += 1
                if not self._retryable(error, failures, started):
                    raise
                await asyncio.sleep(min(0.05 * 2 ** (failures - 1), 2.0))
            finally:
                await updates.aclose()

    async def _updates(self, pending: list[str]) -> AsyncGenerator[JsonDocument, None]:
        """Validate each pushed subset before advancing the mutable reconnect cursor."""
        previous = list(pending)
        async with aclosing(self.api.child_updates(list(pending))) as updates:
            async for response in updates:
                results = ChildResultFrame.capture(response, set(pending))
                pending[:] = [identity for identity in pending if identity not in results]
                yield response
        if pending == previous:
            raise WorkerApiError("Child completion stream closed without progress")

    async def _replay(self, operation: Callable[[], Awaitable[JsonDocument]]) -> JsonDocument:
        """Bound retries to the same exact idempotent internal protocol operation."""
        failures = 0
        started = time.monotonic()
        while True:
            try:
                return await operation()
            except WorkerApiError as error:
                failures += 1
                if not self._retryable(error, failures, started):
                    raise
                await asyncio.sleep(min(0.05 * 2 ** (failures - 1), 2.0))

    @classmethod
    def _retryable(cls, error: WorkerApiError, failures: int, started: float) -> bool:
        """Survive brief endpoint handoffs without multiplying slow timeouts beyond the lease margin."""
        return failures < 10 and cls._transient(error) and time.monotonic() - started < 30.0

    @staticmethod
    def _transient(error: WorkerApiError) -> bool:
        """Only transport, overload and server failures may conceal a committed receipt."""
        return error.status is None or error.status >= 500 or error.status in {408, 429}
