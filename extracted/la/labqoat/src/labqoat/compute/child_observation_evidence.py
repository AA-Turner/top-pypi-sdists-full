"""Immutable producing generation and result receipt attached to a delivered child outcome."""

from dataclasses import dataclass

from labqoat.json_document import JsonDocument
from labqoat.references import ResourceId
from labqoat.worker.worker_api_error import WorkerApiError


@dataclass(frozen=True)
class ChildObservationEvidence:
    """Identify exactly which terminal cycle a parent attempt observed without changing the authored result."""

    parent_attempt_id: str
    observation_id: str
    attempt_id: str | None
    cycle_number: int
    state_version: int
    result_receipt_id: str | None

    @classmethod
    def capture(cls, outcome: JsonDocument, parent_attempt_id: str | None = None) -> "ChildObservationEvidence | None":
        """Accept legacy unversioned responses only when versioned observations were not negotiated."""
        if "observation_id" not in outcome and parent_attempt_id is None:
            return None
        try:
            evidence = cls(
                JsonDocument.expect_scalar(outcome["parent_attempt_id"], str),
                JsonDocument.expect_scalar(outcome["observation_id"], str),
                JsonDocument.expect_optional_scalar(outcome["attempt_id"], str),
                JsonDocument.expect_scalar(outcome["cycle_number"], int),
                JsonDocument.expect_scalar(outcome["state_version"], int),
                JsonDocument.expect_optional_scalar(outcome["result_receipt_id"], str),
            )
            evidence._validate(outcome, parent_attempt_id)
            return evidence
        except (KeyError, TypeError, ValueError) as error:
            raise WorkerApiError("Child outcome generation evidence is invalid", 422) from error

    def _validate(self, outcome: JsonDocument, parent_attempt_id: str | None) -> None:
        """Reject substituted parent authority, invented counters and contradictory result ownership."""
        for identity in (self.parent_attempt_id, self.observation_id, self.attempt_id, self.result_receipt_id):
            if identity is not None:
                ResourceId.parse(identity)
        if self.cycle_number < 1 or self.state_version < 0:
            raise ValueError("Invalid child generation counters")
        if parent_attempt_id is not None and self.parent_attempt_id != parent_attempt_id:
            raise ValueError("Child observation belongs to a different parent attempt")
        self._result(outcome)

    def _result(self, outcome: JsonDocument) -> None:
        """Successful observations require immutable output ownership; failures never contain successful receipts."""
        if outcome["status"] == "completed":
            if self.result_receipt_id is None or self.attempt_id is None or "result" not in outcome:
                raise ValueError("Completed child observation is missing its result receipt")
        elif (
            outcome["status"] not in ("failed", "cancelled", "completed_with_errors")
            or self.result_receipt_id is not None
            or "result" in outcome
        ):
            raise ValueError("Invalid terminal child observation")
