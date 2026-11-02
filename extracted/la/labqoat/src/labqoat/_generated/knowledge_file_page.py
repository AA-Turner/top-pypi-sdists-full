"""KnowledgeFilePage"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class KnowledgeFilePage:
    """KnowledgeFilePage"""

    items: list[JsonValue]
    next_before: int | None = None
    next_cursor: str | None = None
    sequence: int | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> KnowledgeFilePage:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for KnowledgeFilePage")
        return cls(
            items=list(JsonDocument.expect_list(values.get("items", []))),
            next_before=JsonDocument.expect_optional_scalar(values.get("next_before"), int),
            next_cursor=JsonDocument.expect_optional_scalar(values.get("next_cursor"), str),
            sequence=JsonDocument.expect_optional_scalar(values.get("sequence"), int),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("items", True, "list[JsonValue]", "JsonValue"),
                ("next_before", False, "int", ""),
                ("next_cursor", False, "str", ""),
                ("sequence", False, "int", ""),
            ],
        )
