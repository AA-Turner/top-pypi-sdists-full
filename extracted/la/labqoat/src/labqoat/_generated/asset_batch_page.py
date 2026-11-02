"""Ordered per-item outcomes; records carry identity, failures carry errors."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class AssetBatchPage:
    """Ordered per-item outcomes; records carry identity, failures carry errors."""

    items: list[JsonValue]

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> AssetBatchPage:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for AssetBatchPage")
        return cls(
            items=list(JsonDocument.expect_list(values.get("items", []))),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(self, [("items", True, "list[JsonValue]", "JsonValue")])
