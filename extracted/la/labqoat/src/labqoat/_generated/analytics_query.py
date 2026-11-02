"""A governed query intent."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class AnalyticsQuery:
    """A governed query intent."""

    id: str
    status: str
    measures: Mapping[str, JsonValue] | None = None
    receipt: Mapping[str, JsonValue] | None = None
    result: Mapping[str, JsonValue] | None = None
    rows: list[JsonValue] | None = field(default_factory=list)

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> AnalyticsQuery:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for AnalyticsQuery")
        return cls(
            id=JsonDocument.expect_scalar(values["id"], str),
            measures=JsonDocument.expect_optional_dict(values.get("measures")),
            receipt=JsonDocument.expect_optional_dict(values.get("receipt")),
            result=JsonDocument.expect_optional_dict(values.get("result")),
            rows=list(JsonDocument.expect_list(values.get("rows", []))),
            status=JsonDocument.expect_scalar(values["status"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("id", True, "str", ""),
                ("measures", False, "Mapping[str, JsonValue]", ""),
                ("receipt", False, "Mapping[str, JsonValue]", ""),
                ("result", False, "Mapping[str, JsonValue]", ""),
                ("rows", False, "list[JsonValue]", "JsonValue"),
                ("status", True, "str", ""),
            ],
        )
