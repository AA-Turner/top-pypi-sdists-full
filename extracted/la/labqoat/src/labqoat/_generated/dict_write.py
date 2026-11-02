"""DictWrite"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class DictWrite:
    """DictWrite"""

    written: int

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> DictWrite:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for DictWrite")
        return cls(
            written=JsonDocument.expect_scalar(values["written"], int),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(self, [("written", True, "int", "")])
