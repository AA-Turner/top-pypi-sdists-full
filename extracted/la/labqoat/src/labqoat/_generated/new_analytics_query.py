"""Governed query over a pinned revision snapshot."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class NewAnalyticsQuery:
    """Governed query over a pinned revision snapshot."""

    dataset_revision_ref: str
    fields: list[JsonValue] | None = field(default_factory=list)
    filters: Mapping[str, JsonValue] | None = None
    group_by: list[JsonValue] | None = field(default_factory=list)
    limit: int | None = None
    measures: list[JsonValue] | None = field(default_factory=list)
    ordering: list[JsonValue] | None = field(default_factory=list)

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> NewAnalyticsQuery:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for NewAnalyticsQuery")
        return cls(
            dataset_revision_ref=JsonDocument.expect_scalar(values["dataset_revision_ref"], str),
            fields=list(JsonDocument.expect_list(values.get("fields", []))),
            filters=JsonDocument.expect_optional_dict(values.get("filters")),
            group_by=list(JsonDocument.expect_list(values.get("group_by", []))),
            limit=JsonDocument.expect_optional_scalar(values.get("limit"), int),
            measures=list(JsonDocument.expect_list(values.get("measures", []))),
            ordering=list(JsonDocument.expect_list(values.get("ordering", []))),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("dataset_revision_ref", True, "str", ""),
                ("fields", False, "list[JsonValue]", "JsonValue"),
                ("filters", False, "Mapping[str, JsonValue]", ""),
                ("group_by", False, "list[JsonValue]", "JsonValue"),
                ("limit", False, "int", ""),
                ("measures", False, "list[JsonValue]", "JsonValue"),
                ("ordering", False, "list[JsonValue]", "JsonValue"),
            ],
        )
