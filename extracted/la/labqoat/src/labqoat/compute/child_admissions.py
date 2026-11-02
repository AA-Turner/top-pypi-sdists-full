"""Coalesce authored submissions behind one parent-fenced exchange without changing their durable keys."""

import asyncio
import json
from dataclasses import dataclass, field

from labqoat.json_document import JsonDocument, JsonValue
from labqoat.worker.worker_api import WorkerApi
from labqoat.worker.rejection_advice import RejectionAdvice
from labqoat.worker.worker_api_error import WorkerApiError
from labqoat.worker.replay_request import ReplayRequest


@dataclass
class ChildAdmissions:
    """Own bounded request batches; cancelling one caller never cancels another child's acceptance."""

    api: WorkerApi
    _pending: list[tuple[dict[str, JsonValue], asyncio.Future[JsonDocument], int]] = field(
        default_factory=list, init=False
    )
    _scheduled: asyncio.Handle | None = field(default=None, init=False)
    _tasks: set[asyncio.Task[None]] = field(default_factory=set, init=False)

    async def submit(self, document: dict[str, JsonValue]) -> JsonDocument:
        """Preserve submitted concurrency while amortizing HTTP setup and authentication."""
        loop = asyncio.get_running_loop()
        size = len(json.dumps(document, separators=(",", ":"), allow_nan=False).encode())
        future: asyncio.Future[JsonDocument] = loop.create_future()
        self._pending.append((document, future, size))
        if self._scheduled is None and not self._tasks:
            self._scheduled = loop.call_soon(self._dispatch)
        return await future

    async def close(self) -> None:
        """Join already-dispatched effects and cancel work never sent before the owning invocation exits."""
        if self._scheduled is not None:
            self._scheduled.cancel()
            self._scheduled = None
        for _, future, _ in self._pending:
            future.cancel()
        self._pending.clear()
        if self._tasks:
            await asyncio.gather(*self._tasks)

    def _dispatch(self) -> None:
        """Snapshot at most 64 independent calls per wire request and own every in-flight task."""
        self._scheduled = None
        batch = self._take()
        task = asyncio.create_task(self._send(batch))
        self._tasks.add(task)
        task.add_done_callback(self._finished)

    def _finished(self, task: asyncio.Task[None]) -> None:
        """Combine arrivals during admission instead of queuing competing transactions on the same parent lock."""
        self._tasks.discard(task)
        if self._pending:
            self._scheduled = asyncio.get_running_loop().call_soon(self._dispatch)

    def _take(self) -> list[tuple[dict[str, JsonValue], asyncio.Future[JsonDocument]]]:
        """Bound combined payload size while preserving large individually valid submissions."""
        size, count = 0, 0
        for _, _, incoming in self._pending[:64]:
            if count and size + incoming > 1_048_576:
                break
            count += 1
            size += incoming
        batch, self._pending = self._pending[:count], self._pending[count:]
        return [(document, future) for document, future, _ in batch]

    async def _send(self, batch: list[tuple[dict[str, JsonValue], asyncio.Future[JsonDocument]]]) -> None:
        """Expose per-key rejections independently and reject incomplete response cardinality."""
        try:
            response = await ReplayRequest(self.api).send_async(
                "/api/v1/worker/runs/batch", {"items": [item for item, _ in batch]}
            )
            receipts = JsonDocument.expect_list(response["items"])
            if len(receipts) != len(batch):
                raise WorkerApiError("Child batch receipt count does not match the submitted calls")
            for (_, future), receipt in zip(batch, receipts, strict=True):
                self._settle(future, JsonDocument.expect_dict(receipt))
        except Exception as error:
            for _, future in batch:
                if not future.done():
                    future.set_exception(error)

    @staticmethod
    def _settle(future: asyncio.Future[JsonDocument], receipt: JsonDocument) -> None:
        """A cancelled observer leaves accepted remote work durable and peers unaffected."""
        if future.done():
            return
        if "error" in receipt:
            reason = str(receipt["error"])
            future.set_exception(
                WorkerApiError(f"Child submission rejected: {reason}{RejectionAdvice.explain(reason)}", 409)
            )
        else:
            future.set_result(receipt)
