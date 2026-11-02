"""QueueValues"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat._generated.encoded_value import EncodedValue
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class QueueValues:
    """QueueValues"""

    values: list[EncodedValue]

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> QueueValues:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for QueueValues")
        return cls(
            values=[
                EncodedValue.from_dict(JsonDocument.expect_dict(v))
                for v in JsonDocument.expect_list(values.get("values", []))
            ],
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(self, [("values", True, "list[EncodedValue]", "EncodedValue")])
