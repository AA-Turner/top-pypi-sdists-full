"""Fenced rank receipts bind actual restored state to one coordinated immutable snapshot."""

import json
from dataclasses import dataclass
from typing import Literal

from labqoat._generated.distributed_rank_acknowledgement import DistributedRankAcknowledgement
from labqoat._generated.distributed_rank_failure import DistributedRankFailure
from labqoat._generated.distributed_rank_receipt import DistributedRankReceipt
from labqoat.compute.checkpoint_group import CheckpointGroup
from labqoat.json_document import JsonDocument
from labqoat.schemas.identity import Identity
from labqoat.training.recovery.restore_snapshot import RestoreSnapshot
from labqoat.training.recovery.restore_state import RestoreState
from labqoat.worker.replay_request import ReplayRequest
from labqoat.worker.worker_api import WorkerApi


@dataclass(frozen=True)
class GroupRestoration:
    """Broker rank acknowledgements through the invocation's existing assignment credentials."""

    api: WorkerApi
    snapshot: RestoreSnapshot
    group: CheckpointGroup

    def validate(self) -> None:
        """Reject substituted membership, bytes, topology or progress before launching any rank."""
        self.snapshot.envelope.verify_snapshot(self.snapshot.manifest)
        recovery = JsonDocument.expect_dict(self.snapshot.manifest.document["recovery"])
        if self.group.document() != recovery.get("group"):
            raise ValueError("Distributed group does not match the accepted checkpoint")
        compatibility = JsonDocument.expect_dict(recovery["compatibility"])
        if compatibility["world_size"] != len(self.group.ranks):
            raise ValueError("Distributed world size does not match the accepted checkpoint")

    def acknowledge(self, rank: int, state: RestoreState) -> DistributedRankReceipt:
        """Replay exact rank evidence and reject receipts for another rank, generation or state."""
        self._rank(rank)
        evidence = DistributedRankAcknowledgement(
            self.group.ranks[rank].sha256, rank, state.evidence(self.snapshot.envelope)
        ).to_dict()
        response = ReplayRequest(self.api).send("/api/v1/worker/restore/groups/ranks", evidence)
        receipt = DistributedRankReceipt.from_dict(response)
        if (
            receipt.attempt_id != self.snapshot.envelope.document["attempt_id"]
            or receipt.rank != rank
            or receipt.fingerprint != Identity.digest(evidence)
            or receipt.evidence.to_dict() != evidence
        ):
            raise ValueError("Distributed rank receipt does not match restored state")
        return receipt

    def fail(
        self, rank: int, failure_class: Literal["startup", "restore", "collective", "training"], reason: str
    ) -> None:
        """Report whole-group failure after local termination without decoding the empty success body."""
        self._rank(rank)
        if not reason or len(reason.encode()) > 2000:
            raise ValueError("Rank failure requires a bounded diagnostic")
        evidence = DistributedRankFailure(failure_class, rank, reason).to_dict()
        body = json.dumps(evidence, separators=(",", ":"), allow_nan=False).encode()
        self.api.request("POST", "/api/v1/worker/restore/groups/failure", body, "application/json")

    def _rank(self, rank: int) -> None:
        """Reject booleans and out-of-group ranks rather than letting indexing reinterpret them."""
        if type(rank) is not int or not 0 <= rank < len(self.group.ranks):
            raise ValueError("Invalid distributed rank")
