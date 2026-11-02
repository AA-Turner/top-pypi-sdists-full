"""Multiplex concurrent result waiters into bounded resumable completion streams."""

import asyncio
from dataclasses import dataclass, field
from functools import partial
from contextlib import aclosing

from labqoat.json_document import JsonDocument
from labqoat.worker.worker_api import WorkerApi
from labqoat.worker.child_result_frame import ChildResultFrame
from labqoat.worker.replay_request import ReplayRequest


@dataclass
class ChildObservations:
    """Only unfinished child IDs are resent after each completion; result ownership remains server-authorized."""

    api: WorkerApi
    _pending: list[tuple[str, asyncio.Future[JsonDocument]]] = field(default_factory=list, init=False)
    _scheduled: asyncio.Handle | None = field(default=None, init=False)
    _tasks: set[asyncio.Task[None]] = field(default_factory=set, init=False)

    async def result(self, identity: str) -> JsonDocument:
        """Share one stream for all waits submitted during this event-loop turn."""
        loop = asyncio.get_running_loop()
        future: asyncio.Future[JsonDocument] = loop.create_future()
        self._pending.append((identity, future))
        if self._scheduled is None:
            self._scheduled = loop.call_soon(self._dispatch)
        return await future

    async def close(self) -> None:
        """Close all observation streams before their assignment-owned HTTP session is released."""
        if self._scheduled is not None:
            self._scheduled.cancel()
            self._scheduled = None
        for _, future in self._pending:
            future.cancel()
        self._pending.clear()
        for task in self._tasks:
            task.cancel()
        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)

    def _dispatch(self) -> None:
        """Keep each subscription bounded and retain independent cancellation ownership."""
        self._scheduled = None
        batch, self._pending = self._pending[:64], self._pending[64:]
        task = asyncio.create_task(self._follow(batch))
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)
        for _, future in batch:
            future.add_done_callback(partial(self._cancel_unused, task, batch))
        if self._pending:
            self._scheduled = asyncio.get_running_loop().call_soon(self._dispatch)

    async def _follow(self, pending: list[tuple[str, asyncio.Future[JsonDocument]]]) -> None:
        """Drain available results, then resume only unresolved waits without rerunning authored effects."""
        observed = {identity for identity, _ in pending}
        try:
            async with aclosing(ReplayRequest(self.api).updates([identity for identity, _ in pending])) as updates:
                async for response in updates:
                    pending = self._receive(pending, response, observed)
        except Exception as error:
            for _, future in pending:
                if not future.done():
                    future.set_exception(error)
        finally:
            for _, future in pending:
                future.cancel()

    def _receive(
        self, pending: list[tuple[str, asyncio.Future[JsonDocument]]], response: JsonDocument, observed: set[str]
    ) -> list[tuple[str, asyncio.Future[JsonDocument]]]:
        """Settle one server-acknowledged subset while retaining all unfinished observer identities."""
        parent = self.api.attempt_id if "versioned_child_observations" in self.api.capabilities else None
        results = ChildResultFrame.capture(response, observed, parent)
        for identity, future in pending:
            if identity in results and not future.done():
                future.set_result(results[identity])
        return [(identity, future) for identity, future in pending if not future.done()]

    @staticmethod
    def _cancel_unused(
        task: asyncio.Task[None],
        batch: list[tuple[str, asyncio.Future[JsonDocument]]],
        _completed: asyncio.Future[JsonDocument],
    ) -> None:
        """Close local I/O promptly when the last observer leaves its shared stream."""
        if all(future.done() for _, future in batch):
            task.cancel()
