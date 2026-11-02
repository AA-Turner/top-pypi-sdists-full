"""Reattach to a durable owned child using only the current parent's assignment credentials."""

from dataclasses import dataclass, field
from typing import Generic, TypeVar
from urllib.parse import quote

from labqoat.compute.value_codec import ValueCodec
from labqoat.compute.child_observations import ChildObservations
from labqoat.compute.child_observation_evidence import ChildObservationEvidence
from labqoat.json_document import JsonDocument
from labqoat.schemas.schema_document import SchemaDocument
from labqoat.worker.worker_api import WorkerApi
from labqoat.worker.worker_api_error import WorkerApiError

R = TypeVar("R")


@dataclass(frozen=True)
class ChildRunHandle(Generic[R]):
    """Observe committed child completion and its exact typed result through push-based service events."""

    id: str
    api: WorkerApi
    result_type: type[R]
    observations: ChildObservations | None = None
    evidence: ChildObservationEvidence | None = field(default=None, init=False, compare=False)

    def result(self) -> R:
        """Require successful owned completion; failures and mismatched output never become successful values."""
        outcome = self.api.completion(f"/api/v1/worker/runs/{quote(self.id, safe='')}/completion", "run")
        return self._decode(outcome)

    async def result_async(self) -> R:
        """Await durable completion without blocking other children; cancelling observation does not cancel execution."""
        outcome = (
            await self.observations.result(self.id)
            if self.observations is not None and "child_completion_batches" in self.api.capabilities
            else await self.api.completion_async(f"/api/v1/worker/runs/{quote(self.id, safe='')}/completion", "run")
        )
        return self._decode(outcome)

    @staticmethod
    def _cause(outcome: JsonDocument) -> str:
        """Carry the child's own retained failure into the parent's error instead of only its identity."""
        failure = outcome.get("failure")
        summary = failure.get("detail") or failure.get("reason") if isinstance(failure, dict) else None
        return f" ({outcome.get('status')}): {summary}" if summary else f" ({outcome.get('status')})"

    def _decode(self, outcome: JsonDocument) -> R:
        """Apply the same authority and result checks after either transport completes."""
        if outcome.get("id") != self.id:
            raise WorkerApiError("Child observation returned another Run identity")
        parent = self.api.attempt_id if "versioned_child_observations" in self.api.capabilities else None
        evidence = ChildObservationEvidence.capture(outcome, parent)
        if self.evidence is not None and self.evidence != evidence:
            raise WorkerApiError("A delivered child observation cannot change its producing generation", 409)
        object.__setattr__(self, "evidence", evidence)
        if outcome.get("status") != "completed":
            raise WorkerApiError(f"Child Run {self.id} did not complete successfully{self._cause(outcome)}")
        result = JsonDocument.expect_dict(outcome["result"])
        codec = ValueCodec(self.result_type)
        expected = SchemaDocument.capture(codec.schema()).digest
        if set(result) != {"schema_digest", "data"} or result["schema_digest"] != expected:
            raise WorkerApiError("Child result schema does not match the requested Python type")
        return codec.decode(result["data"])
