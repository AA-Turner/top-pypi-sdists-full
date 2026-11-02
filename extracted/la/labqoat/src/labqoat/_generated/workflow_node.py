"""WorkflowNode"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class WorkflowNode:
    """WorkflowNode"""

    attempt_id: str | None
    cancellation_cause: str | None
    checkpoint_digest: str | None
    checkpoint_id: str | None
    classification: str
    cycle_id: str | None
    execution_outcome: str | None
    expected_state_version: int
    has_children: bool
    id: str
    mode: str | None
    operation_id: str | None
    parent_id: str | None
    reason: str | None
    released: bool
    result_receipt_id: str | None
    run_id: str
    source_cycle_number: int
    source_fence: int
    status: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> WorkflowNode:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for WorkflowNode")
        return cls(
            attempt_id=JsonDocument.expect_optional_scalar(values.get("attempt_id"), str),
            cancellation_cause=JsonDocument.expect_optional_scalar(values.get("cancellation_cause"), str),
            checkpoint_digest=JsonDocument.expect_optional_scalar(values.get("checkpoint_digest"), str),
            checkpoint_id=JsonDocument.expect_optional_scalar(values.get("checkpoint_id"), str),
            classification=JsonDocument.expect_scalar(values["classification"], str),
            cycle_id=JsonDocument.expect_optional_scalar(values.get("cycle_id"), str),
            execution_outcome=JsonDocument.expect_optional_scalar(values.get("execution_outcome"), str),
            expected_state_version=JsonDocument.expect_scalar(values["expected_state_version"], int),
            has_children=JsonDocument.expect_scalar(values["has_children"], bool),
            id=JsonDocument.expect_scalar(values["id"], str),
            mode=JsonDocument.expect_optional_scalar(values.get("mode"), str),
            operation_id=JsonDocument.expect_optional_scalar(values.get("operation_id"), str),
            parent_id=JsonDocument.expect_optional_scalar(values.get("parent_id"), str),
            reason=JsonDocument.expect_optional_scalar(values.get("reason"), str),
            released=JsonDocument.expect_scalar(values["released"], bool),
            result_receipt_id=JsonDocument.expect_optional_scalar(values.get("result_receipt_id"), str),
            run_id=JsonDocument.expect_scalar(values["run_id"], str),
            source_cycle_number=JsonDocument.expect_scalar(values["source_cycle_number"], int),
            source_fence=JsonDocument.expect_scalar(values["source_fence"], int),
            status=JsonDocument.expect_scalar(values["status"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("attempt_id", True, "str", ""),
                ("cancellation_cause", True, "str", ""),
                ("checkpoint_digest", True, "str", ""),
                ("checkpoint_id", True, "str", ""),
                ("classification", True, "str", ""),
                ("cycle_id", True, "str", ""),
                ("execution_outcome", True, "str", ""),
                ("expected_state_version", True, "int", ""),
                ("has_children", True, "bool", ""),
                ("id", True, "str", ""),
                ("mode", True, "str", ""),
                ("operation_id", True, "str", ""),
                ("parent_id", True, "str", ""),
                ("reason", True, "str", ""),
                ("released", True, "bool", ""),
                ("result_receipt_id", True, "str", ""),
                ("run_id", True, "str", ""),
                ("source_cycle_number", True, "int", ""),
                ("source_fence", True, "int", ""),
                ("status", True, "str", ""),
            ],
        )
