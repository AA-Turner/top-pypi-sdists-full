"""Per-input lease and output lifetimes around one shared scalar or batch execution."""

import asyncio
import traceback
from collections.abc import Awaitable
from contextlib import AsyncExitStack, ExitStack
from dataclasses import dataclass, field

from labqoat.compute.pool_worker.accepted_input import AcceptedInput
from labqoat.compute.worker.failure_report import FailureReport
from labqoat.compute.pool_worker.input_batch import InputBatch
from labqoat.compute.pool_worker.pool_control import PoolControl
from labqoat.compute.pool_worker.reusable_invocation import ReusableInvocation
from labqoat.json_document import JsonDocument, JsonValue
from labqoat.compute.output_routing import OutputRouting
from labqoat.volumes.mounted_volumes import MountedVolumes


@dataclass(frozen=True)
class InputExecution:
    """Validate the complete batch before acknowledging individual outputs and release only finished slots."""

    control: PoolControl
    invocation: ReusableInvocation
    output: OutputRouting = field(default_factory=OutputRouting)

    async def run(self, envelopes: list[JsonDocument]) -> None:
        """Own all opened clients even if a later input cannot establish its assignment lease."""
        with ExitStack() as lifetime:
            inputs = await InputBatch.open(envelopes, lifetime)
            await self._execute(inputs)

    async def _invoke(self, inputs: list[AcceptedInput]) -> list[dict[str, JsonValue]]:
        """Drain scoped child transports before any input publishes its authoritative completion."""
        async with AsyncExitStack() as sessions:
            for item in inputs:
                await sessions.enter_async_context(item.context.runs.session())
            with self.output.bind([item.context for item in inputs]):
                return await self.invocation.execute(inputs)

    async def _execute(self, inputs: list[AcceptedInput]) -> None:
        """An authored batch error fails each member under that member's own configured retry policy."""
        try:
            results = await self._invoke(inputs)
            await asyncio.to_thread(MountedVolumes.commit_current)
        except Exception as error:
            traceback.print_exc()
            await asyncio.to_thread(MountedVolumes.quietly)
            detail = FailureReport.summary(error)
            await self._settle([self._fail(item, detail) for item in inputs])
        else:
            await self._settle([self._finish(item, result) for item, result in zip(inputs, results, strict=True)])

    @staticmethod
    async def _settle(operations: list[Awaitable[None]]) -> None:
        """Drain every owned completion or failure before closing shared sessions, even after cancellation."""
        pending = asyncio.gather(*operations, return_exceptions=True)
        try:
            outcomes = await asyncio.shield(pending)
        finally:
            await pending
        for outcome in outcomes:
            if isinstance(outcome, BaseException):
                raise outcome

    async def _fail(self, item: AcceptedInput, detail: str) -> None:
        """Stop only the failed input's renewal, then record why it failed before its retry and slot release."""
        await asyncio.to_thread(item.lifetime.close)
        await self.control.fail(item.context.attempt_id, detail)

    async def _finish(self, item: AcceptedInput, result: dict[str, JsonValue]) -> None:
        """Release a completed slot promptly without waiting behind another input's result upload."""
        await asyncio.to_thread(self._complete, item, result)
        await self.control.release(item.context.attempt_id)

    @staticmethod
    def _complete(item: AcceptedInput, result: dict[str, JsonValue]) -> None:
        """Stop renewal immediately after authoritative completion to avoid revoking a healthy shared worker."""
        try:
            item.complete(result)
        finally:
            item.lifetime.close()
