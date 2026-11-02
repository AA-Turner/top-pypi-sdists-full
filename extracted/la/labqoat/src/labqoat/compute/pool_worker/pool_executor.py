"""One shared event loop multiplexes physical input slots and demand notifications."""

from __future__ import annotations

import asyncio
import os
from contextlib import AsyncExitStack, aclosing
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import TYPE_CHECKING

from labqoat.compute.pool_worker.batch_queue import BatchQueue
from labqoat.compute.pool_worker.isolated_execution import IsolatedExecution
from labqoat.compute.pool_worker.pool_control import PoolControl
from labqoat.json_document import JsonDocument
from labqoat.stage_timer import StageTimer

if TYPE_CHECKING:
    from labqoat.compute.pool_worker.input_execution import InputExecution
    from labqoat.compute.pool_worker.reusable_invocation import ReusableInvocation


class PoolExecutor:
    """Keep admitted work bounded by service-owned slots while sharing initialized model state.

    Ordinary functions run each input in a fresh process from a credential-free template, which ``warm`` starts
    before the first claim. Workers that keep state between inputs load the in-process executor only when they
    need it, so a supervisor of fresh processes never imports authored-code machinery.
    """

    def __init__(
        self, control: PoolControl, scratch: Path, *, warm: bool = False, invocation: ReusableInvocation | None = None
    ) -> None:
        """Own control and invocation state without reading environment variables or loading models.

        A worker that saved or restored a memory snapshot brings the invocation already holding its model.
        """
        self.control = control
        self.scratch = scratch
        self.warm = warm
        self.execution: InputExecution | None = None
        self.isolated = IsolatedExecution(control, timing=StageTimer.stderr())
        self._lifetime = AsyncExitStack()
        self._invocation = invocation

    async def run(self) -> None:
        """Install shared output proxies for in-process inputs only, and stop the template on every exit."""
        async with self._lifetime, self.control.api.async_session():
            try:
                if self.warm:
                    self.isolated.reserve.warm()
                await self._run()
            finally:
                await self.isolated.reserve.close()

    def reusable(self) -> InputExecution:
        """The in-process executor, loaded and given its output routing the first time a worker needs it."""
        if self.execution is None:
            from labqoat.compute.pool_worker.input_execution import InputExecution
            from labqoat.compute.pool_worker.reusable_invocation import ReusableInvocation

            invocation = self._invocation or ReusableInvocation(self.scratch)
            self.execution = InputExecution(self.control, invocation)
            self._lifetime.enter_context(self.execution.output.installed())
        return self.execution

    async def _run(self) -> None:
        """Configure a bounded thread budget, then respond to committed demand and slot-release events."""
        delivery = await self._ready()
        policy = JsonDocument.expect_dict(delivery["policy"])
        isolated = policy.get("isolated") is True
        if not isolated:
            await self.isolated.reserve.close()
        concurrency = JsonDocument.expect_dict(policy["concurrency"])
        maximum = JsonDocument.expect_scalar(concurrency["max_inputs"], int)
        asyncio.get_running_loop().set_default_executor(
            ThreadPoolExecutor(max_workers=maximum + 4, thread_name_prefix="labqoat-input")
        )
        batching = JsonDocument.expect_dict(policy.get("batching", {}))
        queue = BatchQueue(
            JsonDocument.expect_scalar(batching.get("max_batch_size", 1), int),
            JsonDocument.expect_scalar(batching.get("wait_ms", 0), int),
        )
        capabilities = JsonDocument.expect_list(delivery.get("capabilities", []))
        self.control.capabilities = frozenset(str(capability) for capability in capabilities)
        async with (
            self.control.connected(os.environ.get("LABQOAT_ATTEMPT_ID", ""), "worker_session" in capabilities),
            asyncio.TaskGroup() as tasks,
        ):
            tasks.create_task(self._consume(queue, tasks, isolated))
            await self._deliver(queue, delivery)
            queue.put(None)

    async def _ready(self) -> JsonDocument:
        """Preload new class workers before accepting slots, retaining older worker compatibility."""
        delivery = await self.control.claim()
        if "initialization" in delivery:
            from labqoat.compute.pool_worker.worker_initialization import WorkerInitialization
            from labqoat.compute.worker.failure_report import FailureReport

            try:
                await WorkerInitialization(self.reusable()).prepare(
                    JsonDocument.expect_dict(delivery["initialization"])
                )
            except Exception as error:
                await self.control.fail_initialization("Worker initialization failed: " + FailureReport.summary(error))
                raise
            delivery = await self.control.claim(initialized=True)
        return delivery

    async def _deliver(self, queue: BatchQueue, delivery: JsonDocument) -> None:
        """Sleep on push notifications when no slots are available instead of polling for inputs."""
        if "pool_delivery_stream" in JsonDocument.expect_list(delivery.get("capabilities", [])):
            await self._stream(queue, delivery)
            return
        while True:
            for envelope in JsonDocument.expect_list(delivery["inputs"]):
                queue.put(JsonDocument.expect_dict(envelope))
            revision = JsonDocument.expect_scalar(delivery["revision"], int)
            changed = await self.control.changes(revision)
            if changed.get("closed") is True:
                return
            delivery = await self.control.claim()

    async def _stream(self, queue: BatchQueue, initial: JsonDocument) -> None:
        """Deduplicate replayed active assignments with memory bounded by the physical slot limit."""
        known: set[str] = set()
        self._enqueue(queue, initial, known)
        async with aclosing(self.control.deliveries()) as deliveries:
            async for delivery in deliveries:
                active = {
                    JsonDocument.expect_scalar(item, str) for item in JsonDocument.expect_list(delivery["active"])
                }
                known.intersection_update(active)
                self._enqueue(queue, delivery, known)

    def _enqueue(self, queue: BatchQueue, delivery: JsonDocument, known: set[str]) -> None:
        """An assignment may execute only once even if its delivery acknowledgement was lost."""
        for value in JsonDocument.expect_list(delivery["inputs"]):
            envelope = JsonDocument.expect_dict(value)
            attempt = JsonDocument.expect_scalar(envelope["attempt_id"], str)
            if attempt not in known:
                known.add(attempt)
                if self.control.bridge is not None:
                    envelope = self.control.bridge.register(envelope)
                queue.put(envelope)

    async def _consume(self, queue: BatchQueue, tasks: asyncio.TaskGroup, isolated: bool = False) -> None:
        """Dispatch independent executions while the queue assembles the next bounded-latency batch."""
        async with AsyncExitStack() as lifetime:
            execution = await lifetime.enter_async_context(self.isolated.session()) if isolated else self.reusable()
            while batch := await queue.take():
                if queue.maximum > 1 or isolated:
                    await execution.run(batch)
                else:
                    tasks.create_task(execution.run(batch))
