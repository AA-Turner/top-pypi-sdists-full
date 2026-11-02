"""QueueItemPage"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat._generated.encoded_value import EncodedValue
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class QueueItemPage:
    """QueueItemPage"""

    position: int
    values: list[EncodedValue]

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> QueueItemPage:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for QueueItemPage")
        return cls(
            position=JsonDocument.expect_scalar(values["position"], int),
            values=[
                EncodedValue.from_dict(JsonDocument.expect_dict(v))
                for v in JsonDocument.expect_list(values.get("values", []))
            ],
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self, [("position", True, "int", ""), ("values", True, "list[EncodedValue]", "EncodedValue")]
        )
