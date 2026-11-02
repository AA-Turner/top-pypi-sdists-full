"""EncodedValue"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class EncodedValue:
    """EncodedValue"""

    data: str
    encoding: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> EncodedValue:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for EncodedValue")
        return cls(
            data=JsonDocument.expect_scalar(values["data"], str),
            encoding=JsonDocument.expect_scalar(values["encoding"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(self, [("data", True, "str", ""), ("encoding", True, "str", "")])
