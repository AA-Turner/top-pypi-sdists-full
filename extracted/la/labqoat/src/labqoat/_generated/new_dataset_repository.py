"""Repository name with table identity and ownership."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class NewDatasetRepository:
    """Repository name with table identity and ownership."""

    name: str
    default_branch: str | None = None
    description: str | None = None
    owners: list[JsonValue] | None = field(default_factory=list)
    table_name: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> NewDatasetRepository:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for NewDatasetRepository")
        return cls(
            default_branch=JsonDocument.expect_optional_scalar(values.get("default_branch"), str),
            description=JsonDocument.expect_optional_scalar(values.get("description"), str),
            name=JsonDocument.expect_scalar(values["name"], str),
            owners=list(JsonDocument.expect_list(values.get("owners", []))),
            table_name=JsonDocument.expect_optional_scalar(values.get("table_name"), str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("default_branch", False, "str", ""),
                ("description", False, "str", ""),
                ("name", True, "str", ""),
                ("owners", False, "list[JsonValue]", "JsonValue"),
                ("table_name", False, "str", ""),
            ],
        )
