"""Assignment-scoped lifecycle around one typed root function execution."""

import json
import os
import tempfile
import traceback
from dataclasses import dataclass, field
from pathlib import Path

from labqoat._generated.compute_publication import ComputePublication
from labqoat.compute.descriptor_output import DescriptorOutput
from labqoat.compute.worker.compile_caches import CompileCaches
from labqoat.compute.worker.context_factory import ContextFactory
from labqoat.compute.worker.delivered_source import DeliveredSource
from labqoat.compute.worker.failure_report import FailureReport
from labqoat.compute.worker.invocation import Invocation
from labqoat.compute.worker.retained_inputs import RetainedInputs
from labqoat.compute.worker.input_completion import InputCompletion
from labqoat.json_document import JsonDocument, JsonValue
from labqoat.run_context import RunContext
from labqoat.worker.worker_api import WorkerApi
from labqoat.compute.output_routing import OutputRouting
from labqoat.stage_timer import StageTimer
from labqoat.volumes.mounted_volumes import MountedVolumes


@dataclass(frozen=True)
class ComputeWorker:
    """Keep execution leased and publish its result through the same fenced API as other managed workers."""

    api: WorkerApi
    report_failure: bool = True
    preclaimed: bool = False
    timing: StageTimer = field(default_factory=StageTimer, compare=False)

    def run(self, publication: ComputePublication, arguments: dict[str, JsonValue], context: RunContext) -> None:
        """Require live ownership before imports or authored effects, and acknowledge only validated output."""
        lease = self.api.lease()
        with (
            lease.maintained(confirmed=self.preclaimed),
            OutputRouting().installed() as output,
            output.bind([context]),
        ):
            retryable = False
            try:
                DeliveredSource.install(publication, context.assets, context.scratch)
                CompileCaches.ensure(context.scratch)
                self.timing.stage("worker.source_delivered")
                with DescriptorOutput.captured(context):
                    invocation = Invocation.load(publication, arguments)
                self.timing.stage("worker.authored_import")
                if not self.preclaimed:
                    self.api.json("POST", "/api/v1/worker/assignments/claim", {"shard_index": 0})
                self.timing.stage("worker.claimed")
                retryable = (publication.function.retries or 0) > 0
                with DescriptorOutput.captured(context), MountedVolumes.settled():
                    result = invocation.execute(arguments, context)
                self.timing.stage("worker.execution")
                if context._telemetry is not None:
                    context._telemetry.finish()
                self.api.flush_telemetry()
            except Exception as error:
                self._fail(retryable, error)
                raise
            lease.stop()
            InputCompletion(self.api).finish(result)
            self.timing.stage("worker.completion")

    def _fail(self, retryable: bool, error: Exception) -> None:
        """Retain failure diagnostics while reporting failure even if telemetry delivery breaks."""
        try:
            traceback.print_exc()
            self.api.flush_telemetry()
        finally:
            if self.report_failure:
                reason = f"{type(error).__name__}: {error}"[:2000]
                self.api.json("POST", "/api/v1/worker/assignments/fail", {"retryable": retryable, "reason": reason})

    @classmethod
    def main(cls) -> None:
        """Run one call with scratch owned by this worker lifetime, saving a memory snapshot first when asked to.

        A worker started to save a snapshot imports the function and starts its web server, checkpoints, and only
        then runs the call; a worker restored from it continues from the same point as a run of its own.
        """
        with tempfile.TemporaryDirectory(prefix="labqoat-call-") as scratch:
            try:
                logged = None
                if os.environ.get("LABQOAT_MEMORY_SNAPSHOT") == "capture":
                    from labqoat.compute.worker.function_snapshot import FunctionSnapshot

                    logged = FunctionSnapshot(Path(scratch)).prepare()
                cls.call(Path(scratch), logged)
            except Exception as error:
                FailureReport.record(error)
                raise

    @classmethod
    def call(cls, scratch: Path, logged: tuple[str, int] | None = None) -> None:
        """Consume service-injected assignment data, numbering logs after a snapshot's preparation of the attempt."""
        captured = JsonDocument.expect_dict(json.loads(os.environ["LABQOAT_CONTEXT_JSON"]))
        api = WorkerApi.from_environment()
        MountedVolumes.current().start()
        timing = StageTimer.stderr()
        try:
            captured = RetainedInputs(api).capture(captured)
            timing.stage("worker.inputs_claimed")
            arguments = JsonDocument.expect_dict(captured["args"])
            publication = ComputePublication.from_dict(JsonDocument.expect_dict(captured["compute"]))
            context = ContextFactory(api, scratch).create(captured)
            if context._telemetry is not None and logged is not None and logged[0] == context.attempt_id:
                context._telemetry.logs.resume_from(logged[1])
            cls(
                api,
                report_failure=os.environ.get("LABQOAT_ISOLATED_INPUT") != "1",
                preclaimed=captured["claimed"] is True,
                timing=timing,
            ).run(publication, dict(arguments), context)
        finally:
            api.close()
