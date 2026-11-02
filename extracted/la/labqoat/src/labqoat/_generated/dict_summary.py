"""DictSummary"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class DictSummary:
    """DictSummary"""

    created_at: str
    entries: int
    name: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> DictSummary:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for DictSummary")
        return cls(
            created_at=JsonDocument.expect_scalar(values["created_at"], str),
            entries=JsonDocument.expect_scalar(values["entries"], int),
            name=JsonDocument.expect_scalar(values["name"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self, [("created_at", True, "str", ""), ("entries", True, "int", ""), ("name", True, "str", "")]
        )
