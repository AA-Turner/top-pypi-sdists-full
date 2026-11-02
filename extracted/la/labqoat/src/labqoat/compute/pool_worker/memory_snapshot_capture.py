"""A pool worker that saves a memory snapshot of itself once its class is initialized."""

import asyncio
from pathlib import Path

from labqoat.compute.memory_snapshot_point import MemorySnapshotPoint
from labqoat.compute.pool_worker.input_execution import InputExecution
from labqoat.compute.pool_worker.memory_checkpoint import MemoryCheckpoint
from labqoat.compute.pool_worker.pool_control import PoolControl
from labqoat.compute.pool_worker.reusable_invocation import ReusableInvocation
from labqoat.compute.pool_worker.spec_environment import SpecEnvironment
from labqoat.compute.pool_worker.worker_initialization import WorkerInitialization
from labqoat.compute.worker.failure_report import FailureReport
from labqoat.json_document import JsonDocument
from labqoat.volumes.mounted_volumes import MountedVolumes
from labqoat.worker.worker_api import WorkerApi


class MemorySnapshotCapture:
    """Initialize up to the snapshot under short-lived authority, checkpoint, and continue in whichever copy runs.

    Nothing that holds the worker's identity survives the checkpoint: the client, lease, volumes and output routing
    of the initialization are all closed first. The worker that saved the snapshot reports it and goes on as itself;
    a worker restored from it takes up its own environment and says it runs again. Both then serve inputs with the
    class already initialized, after the initializer every worker runs.
    """

    def __init__(
        self,
        scratch: Path,
        checkpoint: MemoryCheckpoint | None = None,
        environment: SpecEnvironment | None = None,
    ) -> None:
        """Keep the model scratch the initialized class lives in, and the runtime's checkpoint and environment."""
        self.scratch = scratch
        self.point = MemorySnapshotPoint(checkpoint, environment)

    def prepared(self) -> ReusableInvocation:
        """The initialized invocation, after the snapshot was taken or restored from."""
        invocation = ReusableInvocation(self.scratch, deferred=True)
        initialized = self._initialize(invocation)
        invocation.resume()
        if initialized:
            self.point.take()
        return invocation

    def _initialize(self, invocation: ReusableInvocation) -> bool:
        """Run the class's snapshot initializer under the worker's own authority, closed again afterwards."""
        api = WorkerApi.from_environment()
        MountedVolumes.current().start()
        try:
            with api.lease().maintained(confirmed=True):
                return asyncio.run(self._prepare(PoolControl(api), invocation))
        finally:
            MountedVolumes.released()
            api.close()

    async def _prepare(self, control: PoolControl, invocation: ReusableInvocation) -> bool:
        """Initialize from the platform's initialization delivery; a worker without one has nothing to save."""
        async with control.api.async_session():
            initialization = (await control.claim()).get("initialization")
            if initialization is None:
                return False
            execution = InputExecution(control, invocation)
            with execution.output.installed():
                try:
                    await WorkerInitialization(execution).prepare(JsonDocument.expect_dict(initialization))
                except Exception as error:
                    await control.fail_initialization("Worker initialization failed: " + FailureReport.summary(error))
                    raise
            return True
