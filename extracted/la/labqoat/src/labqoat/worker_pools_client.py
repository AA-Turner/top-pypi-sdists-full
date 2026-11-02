"""Explicit management of immutable reusable worker fleets and their warm-container lifetime."""

import json
from labqoat._generated.compute_worker_pool import ComputeWorkerPool
from labqoat.base_client import BaseClient


class WorkerPoolsClient(BaseClient):
    """Inspect fleet policy or suspend and resume dispatch using explicit host credentials."""

    def get(self, pool_id: str) -> ComputeWorkerPool:
        """Read the fleet identity retained on each pooled input's placement."""
        path = f"/api/v1/worker-pools/{self.encode_ref(pool_id)}"
        return self.decode(self.send("GET", path), path, ComputeWorkerPool.from_dict)

    def set_active(self, pool_id: str, active: bool) -> ComputeWorkerPool:
        """Suspend new dispatch and drain idle workers, or resume dispatch of queued demand."""
        if type(active) is not bool:
            raise ValueError("Pool active state must be a boolean")
        path = f"/api/v1/worker-pools/{self.encode_ref(pool_id)}"
        response = self.send_content(
            "PATCH", path, json.dumps({"active": active}).encode(), "application/merge-patch+json"
        )
        return self.decode(response, path, ComputeWorkerPool.from_dict)
