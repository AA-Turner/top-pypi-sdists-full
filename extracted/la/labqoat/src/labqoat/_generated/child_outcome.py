"""ChildOutcome"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class ChildOutcome:
    """ChildOutcome"""

    id: str
    status: str
    attempt_id: str | None = None
    cycle_number: int | None = None
    observation_id: str | None = None
    parent_attempt_id: str | None = None
    result: Mapping[str, JsonValue] | None = None
    result_receipt_id: str | None = None
    state_version: int | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> ChildOutcome:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for ChildOutcome")
        return cls(
            attempt_id=JsonDocument.expect_optional_scalar(values.get("attempt_id"), str),
            cycle_number=JsonDocument.expect_optional_scalar(values.get("cycle_number"), int),
            id=JsonDocument.expect_scalar(values["id"], str),
            observation_id=JsonDocument.expect_optional_scalar(values.get("observation_id"), str),
            parent_attempt_id=JsonDocument.expect_optional_scalar(values.get("parent_attempt_id"), str),
            result=JsonDocument.expect_optional_dict(values.get("result")),
            result_receipt_id=JsonDocument.expect_optional_scalar(values.get("result_receipt_id"), str),
            state_version=JsonDocument.expect_optional_scalar(values.get("state_version"), int),
            status=JsonDocument.expect_scalar(values["status"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("attempt_id", False, "str", ""),
                ("cycle_number", False, "int", ""),
                ("id", True, "str", ""),
                ("observation_id", False, "str", ""),
                ("parent_attempt_id", False, "str", ""),
                ("result", False, "Mapping[str, JsonValue]", ""),
                ("result_receipt_id", False, "str", ""),
                ("state_version", False, "int", ""),
                ("status", True, "str", ""),
            ],
        )
