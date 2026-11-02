"""Between 1 and 50 asset references with per-item outcomes."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class AssetBatchComplete:
    """Between 1 and 50 asset references with per-item outcomes."""

    refs: list[JsonValue]

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> AssetBatchComplete:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for AssetBatchComplete")
        return cls(
            refs=list(JsonDocument.expect_list(values.get("refs", []))),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(self, [("refs", True, "list[JsonValue]", "JsonValue")])
