"""A named dataset revision family with table identity."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class DatasetRepository:
    """A named dataset revision family with table identity."""

    id: str
    links: Mapping[str, JsonValue]
    name: str
    archived: bool | None = None
    default_branch: str | None = None
    description: str | None = None
    head: Mapping[str, JsonValue] | None = None
    inserted_at: str | None = None
    owners: list[JsonValue] | None = field(default_factory=list)
    table_name: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> DatasetRepository:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for DatasetRepository")
        return cls(
            archived=JsonDocument.expect_optional_scalar(values.get("archived"), bool),
            default_branch=JsonDocument.expect_optional_scalar(values.get("default_branch"), str),
            description=JsonDocument.expect_optional_scalar(values.get("description"), str),
            head=JsonDocument.expect_optional_dict(values.get("head")),
            id=JsonDocument.expect_scalar(values["id"], str),
            inserted_at=JsonDocument.expect_optional_scalar(values.get("inserted_at"), str),
            links=JsonDocument.expect_dict(values["links"]),
            name=JsonDocument.expect_scalar(values["name"], str),
            owners=list(JsonDocument.expect_list(values.get("owners", []))),
            table_name=JsonDocument.expect_optional_scalar(values.get("table_name"), str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("archived", False, "bool", ""),
                ("default_branch", False, "str", ""),
                ("description", False, "str", ""),
                ("head", False, "Mapping[str, JsonValue]", ""),
                ("id", True, "str", ""),
                ("inserted_at", False, "str", ""),
                ("links", True, "Mapping[str, JsonValue]", ""),
                ("name", True, "str", ""),
                ("owners", False, "list[JsonValue]", "JsonValue"),
                ("table_name", False, "str", ""),
            ],
        )
