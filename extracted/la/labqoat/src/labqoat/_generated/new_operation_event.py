"""Type, run scope, and payload."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class NewOperationEvent:
    """Type, run scope, and payload."""

    type: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> NewOperationEvent:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for NewOperationEvent")
        return cls(
            type=JsonDocument.expect_scalar(values["type"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(self, [("type", True, "str", "")])
