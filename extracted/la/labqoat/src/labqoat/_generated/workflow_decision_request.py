"""WorkflowDecisionRequest"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class WorkflowDecisionRequest:
    """WorkflowDecisionRequest"""

    input_digest: str
    key: str
    value: Mapping[str, JsonValue] | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> WorkflowDecisionRequest:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for WorkflowDecisionRequest")
        return cls(
            input_digest=JsonDocument.expect_scalar(values["input_digest"], str),
            key=JsonDocument.expect_scalar(values["key"], str),
            value=JsonDocument.expect_optional_dict(values.get("value")),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("input_digest", True, "str", ""),
                ("key", True, "str", ""),
                ("value", False, "Mapping[str, JsonValue]", ""),
            ],
        )
