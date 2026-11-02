"""WorkflowDecisionReceipt"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class WorkflowDecisionReceipt:
    """WorkflowDecisionReceipt"""

    attempt_id: str | None
    effect_key: str
    id: str | None
    input_digest: str
    key: str
    recorded: bool
    value: Mapping[str, JsonValue] | None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> WorkflowDecisionReceipt:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for WorkflowDecisionReceipt")
        return cls(
            attempt_id=JsonDocument.expect_optional_scalar(values.get("attempt_id"), str),
            effect_key=JsonDocument.expect_scalar(values["effect_key"], str),
            id=JsonDocument.expect_optional_scalar(values.get("id"), str),
            input_digest=JsonDocument.expect_scalar(values["input_digest"], str),
            key=JsonDocument.expect_scalar(values["key"], str),
            recorded=JsonDocument.expect_scalar(values["recorded"], bool),
            value=JsonDocument.expect_optional_dict(values["value"]),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("attempt_id", True, "str", ""),
                ("effect_key", True, "str", ""),
                ("id", True, "str", ""),
                ("input_digest", True, "str", ""),
                ("key", True, "str", ""),
                ("recorded", True, "bool", ""),
                ("value", True, "Mapping[str, JsonValue]", ""),
            ],
        )
