"""Bounded shards with ownership and winning outputs."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class ShardPage:
    """Bounded shards with ownership and winning outputs."""

    items: list[JsonValue]
    next_cursor: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> ShardPage:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for ShardPage")
        return cls(
            items=list(JsonDocument.expect_list(values.get("items", []))),
            next_cursor=JsonDocument.expect_optional_scalar(values.get("next_cursor"), str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self, [("items", True, "list[JsonValue]", "JsonValue"), ("next_cursor", False, "str", "")]
        )
