"""A function run that saves a memory snapshot of itself once its function is imported and its server listens."""

import json
import os
import traceback
from pathlib import Path
from typing import cast

from labqoat._generated.compute_publication import ComputePublication
from labqoat.compute.descriptor_output import DescriptorOutput
from labqoat.compute.memory_snapshot_point import MemorySnapshotPoint
from labqoat.compute.output_routing import OutputRouting
from labqoat.compute.run_telemetry import RunTelemetry
from labqoat.compute.web_servers import WebServer
from labqoat.compute.worker.compile_caches import CompileCaches
from labqoat.compute.worker.context_factory import ContextFactory
from labqoat.compute.worker.delivered_source import DeliveredSource
from labqoat.compute.worker.failure_report import FailureReport
from labqoat.compute.worker.invocation import Invocation
from labqoat.compute.worker.retained_inputs import RetainedInputs
from labqoat.json_document import JsonDocument
from labqoat.run_context import RunContext
from labqoat.volumes.mounted_volumes import MountedVolumes
from labqoat.worker.worker_api import WorkerApi


class FunctionSnapshot:
    """Prepare a call up to its snapshot under short-lived authority, checkpoint, and continue in whichever copy runs.

    Preparing installs the function's source and imports its module; a web server function also starts its server
    and waits until it listens. Nothing that holds the run's identity survives the checkpoint: the client, lease,
    volumes and output routing of the preparation are all closed first. Either copy then runs its call as any worker
    does, with the module imported and the server listening already.
    """

    def __init__(self, scratch: Path, point: MemorySnapshotPoint | None = None) -> None:
        """Keep the scratch the prepared call lives in and the checkpoint it is saved at."""
        self.scratch = scratch
        self.point = point or MemorySnapshotPoint()

    def prepare(self) -> tuple[str, int]:
        """Prepare and checkpoint, returning how far the preparation's logs went in its attempt."""
        logged = self._prepare()
        self.point.take()
        return logged

    def _prepare(self) -> tuple[str, int]:
        """Run the preparation under the run's own authority, closed again before the checkpoint."""
        api = WorkerApi.from_environment()
        MountedVolumes.current().start()
        try:
            captured = RetainedInputs(api).capture(
                JsonDocument.expect_dict(json.loads(os.environ["LABQOAT_CONTEXT_JSON"]))
            )
            context = ContextFactory(api, self.scratch).create(captured)
            with (
                api.lease().maintained(confirmed=captured["claimed"] is True),
                OutputRouting().installed() as output,
                output.bind([context]),
            ):
                self._started(api, captured, context)
            return context.attempt_id, cast(RunTelemetry, context._telemetry).logs.sequence
        finally:
            MountedVolumes.released()
            api.close()

    def _started(self, api: WorkerApi, captured: JsonDocument, context: RunContext) -> None:
        """Import the function and start its server; a failure fails the run and the snapshot alike."""
        publication = ComputePublication.from_dict(JsonDocument.expect_dict(captured["compute"]))
        try:
            DeliveredSource.install(publication, context.assets, self.scratch)
            CompileCaches.ensure(self.scratch)
            with DescriptorOutput.captured(context):
                invocation = Invocation.load(publication, JsonDocument.expect_dict(captured["args"]))
            if captured["claimed"] is not True:
                api.json("POST", "/api/v1/worker/assignments/claim", {"shard_index": 0})
            WebServer.start(invocation.target.local, context)
        except Exception as error:
            traceback.print_exc()
            summary = FailureReport.summary(error)
            self.point.report(
                {"outcome": "failed", "detail": ("the function could not be prepared: " + summary)[:2000]}
            )
            api.json("POST", "/api/v1/worker/assignments/fail", {"retryable": False, "reason": summary[:2000]})
            raise
        finally:
            # A worker's context always has telemetry of its own.
            cast(RunTelemetry, context._telemetry).finish()
            api.flush_telemetry()
