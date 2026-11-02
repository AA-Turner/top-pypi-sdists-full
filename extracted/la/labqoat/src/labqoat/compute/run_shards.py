"""Explicit independent-shard execution using retained selection and immutable per-shard outcomes."""

from dataclasses import dataclass

from labqoat._generated.shard_outcome import ShardOutcome
from labqoat._generated.worker_shard_snapshot import WorkerShardSnapshot
from labqoat.json_document import JsonDocument
from labqoat.worker.replay_request import ReplayRequest
from labqoat.worker.worker_api import WorkerApi


@dataclass(frozen=True)
class RunShards:
    """Execute only remaining independent work through the current assignment's fenced authority."""

    api: WorkerApi

    def snapshot(self) -> WorkerShardSnapshot:
        """Read bounded current work and the original frozen recovery selection without claiming anything."""
        response = self.api.json("GET", "/api/v1/worker/assignments/shards")
        snapshot = WorkerShardSnapshot.from_dict(response)
        if snapshot.protocol_version != 1:
            raise ValueError("Unsupported independent-shard protocol")
        return snapshot

    def claim(self, index: int) -> None:
        """Claim one remaining shard; preserved successes and stale assignments are rejected by the server."""
        request = self._request(index)
        ReplayRequest(self.api).send("/api/v1/worker/assignments/shards/claim", request)

    def succeed(self, index: int, payload: JsonDocument) -> ShardOutcome:
        """Retain an exact output before reporting success, without regenerating bytes during transport replay."""
        self._request(index)
        output = dict(payload)
        if "shard_index" in output and output["shard_index"] != index:
            raise ValueError("Output shard conflicts with the claimed shard")
        output["shard_index"] = index
        ReplayRequest(self.api).send("/api/v1/worker/assignments/output", output)
        return self._finish(index, "succeeded")

    def fail(self, index: int) -> ShardOutcome:
        """Record one explicit failed shard without declaring failures from arbitrary result JSON."""
        return self._finish(index, "failed")

    def _finish(self, index: int, outcome: str) -> ShardOutcome:
        """Verify the exact immutable outcome returned for this requested shard."""
        request = self._request(index)
        request["outcome"] = outcome
        response = ReplayRequest(self.api).send("/api/v1/worker/assignments/shards/finish", request)
        receipt = ShardOutcome.from_dict(response)
        if receipt.shard_index != index or receipt.outcome != outcome:
            raise ValueError("Shard receipt does not match the requested outcome")
        return receipt

    @staticmethod
    def _request(index: int) -> JsonDocument:
        """Reject malformed indexes before issuing any assignment effect."""
        if type(index) is not int or not 0 <= index < 64:
            raise ValueError("Shard index must be an integer from 0 through 63")
        return JsonDocument({"protocol_version": 1, "shard_index": index})
