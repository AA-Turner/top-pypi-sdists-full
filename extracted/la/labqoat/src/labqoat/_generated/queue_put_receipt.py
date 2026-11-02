"""QueuePutReceipt"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class QueuePutReceipt:
    """QueuePutReceipt"""

    items: int

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> QueuePutReceipt:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for QueuePutReceipt")
        return cls(
            items=JsonDocument.expect_scalar(values["items"], int),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(self, [("items", True, "int", "")])
