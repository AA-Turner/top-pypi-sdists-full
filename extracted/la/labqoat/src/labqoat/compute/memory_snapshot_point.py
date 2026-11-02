"""The moment a worker saves its memory, after which it goes on as itself or as a worker restored from it."""

import sys

from labqoat.compute.pool_worker.memory_checkpoint import MemoryCheckpoint
from labqoat.compute.pool_worker.spec_environment import SpecEnvironment
from labqoat.json_document import JsonValue
from labqoat.worker.worker_api import WorkerApi
from labqoat.worker.worker_api_error import WorkerApiError


class MemorySnapshotPoint:
    """Checkpoint this workload now and tell the platform which copy of it continues.

    The worker that saved the snapshot says whether it was written. A worker restored from it takes up its own
    environment and says it runs again, so failures of its own later work are not taken for a broken snapshot.
    Nothing here holds credentials across the checkpoint: every report opens and closes its own client.
    """

    def __init__(self, checkpoint: MemoryCheckpoint | None = None, environment: SpecEnvironment | None = None) -> None:
        """Keep the runtime's checkpoint and the environment a restored copy takes up."""
        self.checkpoint = checkpoint or MemoryCheckpoint()
        self.environment = environment or SpecEnvironment()

    def take(self) -> None:
        """Checkpoint, then report as the worker that saved the snapshot or as one restored from it."""
        outcome, detail = self.checkpoint.take()
        if outcome == "restore":
            self.environment.adopt()
            print("Continuing from a memory snapshot.", file=sys.stderr, flush=True)
            self.report({"outcome": "restored"})
            return
        self.report({"outcome": "captured"} if outcome == "resume" else {"outcome": "failed", "detail": detail[:2000]})

    @staticmethod
    def report(report: dict[str, JsonValue]) -> None:
        """Tell the platform about the snapshot; a report that cannot be delivered leaves the worker running."""
        api = WorkerApi.from_environment()
        try:
            api.json("POST", "/api/v1/worker/memory-snapshot", report)
        except WorkerApiError as error:
            print(f"The memory snapshot could not be reported: {error}", file=sys.stderr, flush=True)
        finally:
            api.close()
