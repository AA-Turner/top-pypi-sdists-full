"""Initialize reusable class state under constructor-only physical assignment authority."""

import traceback
from contextlib import ExitStack
from dataclasses import dataclass

from labqoat._generated.compute_publication import ComputePublication
from labqoat.compute.pool_worker.accepted_input import AcceptedInput
from labqoat.compute.pool_worker.input_execution import InputExecution
from labqoat.compute.worker.context_factory import ContextFactory
from labqoat.json_document import JsonDocument
from labqoat.stage_timer import StageTimer


@dataclass(frozen=True)
class WorkerInitialization:
    """Keep model scratch and physical credentials alive before accepting any logical input."""

    execution: InputExecution

    async def prepare(self, captured: JsonDocument) -> None:
        """Acknowledge readiness only after imports, constructor and initializer all succeed."""
        api = self.execution.control.api
        context = ContextFactory(api, self.execution.invocation.scratch).create(captured)
        self.execution.invocation.continue_logs(context)
        publication = ComputePublication.from_dict(JsonDocument.expect_dict(captured["compute"]))
        with ExitStack() as lifetime:
            item = AcceptedInput(api, context, publication, dict(JsonDocument.expect_dict(captured["args"])), lifetime)
            await self._prepare(item)
            # Only now has the last of the initialization's output, its timing line among it, been numbered.
            self.execution.invocation.remember_logs(context)

    async def _prepare(self, item: AcceptedInput) -> None:
        """Flush initializer evidence before readiness or a failed startup tears down the physical worker."""
        async with item.context.runs.session():
            with self.execution.output.bind([item.context]), StageTimer.stderr().span("worker.initialize"):
                try:
                    await self.execution.invocation.prepare(item)
                except Exception:
                    traceback.print_exc()
                    raise
                finally:
                    self._flush(item)

    @staticmethod
    def _flush(item: AcceptedInput) -> None:
        """Drain physical initialization telemetry without closing its lifetime-owned transport."""
        if item.context._telemetry is not None:
            item.context._telemetry.finish()
        item.api.flush_telemetry()
