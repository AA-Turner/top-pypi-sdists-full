"""Service-owned reusable worker launcher with physical and per-input lease lifetimes."""

import asyncio
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory

from labqoat.compute.pool_worker.pool_control import PoolControl
from labqoat.compute.pool_worker.pool_executor import PoolExecutor
from labqoat.compute.pool_worker.reusable_invocation import ReusableInvocation
from labqoat.json_document import JsonDocument
from labqoat.volumes.mounted_volumes import MountedVolumes
from labqoat.worker.worker_api import WorkerApi


class PoolWorker:
    """Maintain the physical control assignment until scaledown or authoritative termination."""

    @staticmethod
    def main() -> None:
        """Retain model scratch for the worker lifetime, initializing up to a memory snapshot first when asked to.

        A worker asked to capture a snapshot initializes, checkpoints and only then serves; the copy of it a later
        worker restores continues from the same point, with its own environment.
        """
        with TemporaryDirectory(prefix="labqoat-model-") as directory:
            scratch = Path(directory)
            invocation = None
            if PoolWorker._capturing():
                from labqoat.compute.pool_worker.memory_snapshot_capture import MemorySnapshotCapture

                invocation = MemorySnapshotCapture(scratch).prepared()
            PoolWorker.serve(scratch, invocation)

    @staticmethod
    def serve(scratch: Path, invocation: ReusableInvocation | None) -> None:
        """Consume explicitly injected control credentials and serve inputs until the platform closes the worker.

        The first claim proves the assignment is still owned, so the lease starts renewing without a separate
        heartbeat first. A worker whose inputs each run in a fresh process starts that process's template before
        claiming, when the platform says so in the worker's context.
        """
        api = WorkerApi.from_environment()
        context = JsonDocument.expect_dict(json.loads(os.environ.get("LABQOAT_CONTEXT_JSON") or "{}"))
        MountedVolumes.current().start()
        try:
            with api.lease().maintained(confirmed=True):
                warm = context.get("isolated_inputs") is True
                executor = PoolExecutor(PoolControl(api), scratch, warm=warm, invocation=invocation)
                asyncio.run(executor.run())
        finally:
            MountedVolumes.quietly()
            api.close()

    @staticmethod
    def _capturing() -> bool:
        """Whether the platform started this worker to save a memory snapshot of itself."""
        return os.environ.get("LABQOAT_MEMORY_SNAPSHOT") == "capture"
