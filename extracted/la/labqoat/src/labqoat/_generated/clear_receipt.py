"""ClearReceipt"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class ClearReceipt:
    """ClearReceipt"""

    removed: int

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> ClearReceipt:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for ClearReceipt")
        return cls(
            removed=JsonDocument.expect_scalar(values["removed"], int),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(self, [("removed", True, "int", "")])
