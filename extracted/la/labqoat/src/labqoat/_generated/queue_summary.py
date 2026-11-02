"""QueueSummary"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class QueueSummary:
    """QueueSummary"""

    created_at: str
    items: int
    name: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> QueueSummary:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for QueueSummary")
        return cls(
            created_at=JsonDocument.expect_scalar(values["created_at"], str),
            items=JsonDocument.expect_scalar(values["items"], int),
            name=JsonDocument.expect_scalar(values["name"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self, [("created_at", True, "str", ""), ("items", True, "int", ""), ("name", True, "str", "")]
        )
