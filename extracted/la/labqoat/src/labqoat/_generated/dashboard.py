"""An immutable published dashboard version."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class Dashboard:
    """An immutable published dashboard version."""

    dashboard_id: str
    id: str
    inserted_at: str
    name: str
    version_number: int
    description: str | None = None
    layout: list[JsonValue] | None = field(default_factory=list)
    panels: list[JsonValue] | None = field(default_factory=list)
    parameters: list[JsonValue] | None = field(default_factory=list)
    previous_version_id: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> Dashboard:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for Dashboard")
        return cls(
            dashboard_id=JsonDocument.expect_scalar(values["dashboard_id"], str),
            description=JsonDocument.expect_optional_scalar(values.get("description"), str),
            id=JsonDocument.expect_scalar(values["id"], str),
            inserted_at=JsonDocument.expect_scalar(values["inserted_at"], str),
            layout=list(JsonDocument.expect_list(values.get("layout", []))),
            name=JsonDocument.expect_scalar(values["name"], str),
            panels=list(JsonDocument.expect_list(values.get("panels", []))),
            parameters=list(JsonDocument.expect_list(values.get("parameters", []))),
            previous_version_id=JsonDocument.expect_optional_scalar(values.get("previous_version_id"), str),
            version_number=JsonDocument.expect_scalar(values["version_number"], int),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("dashboard_id", True, "str", ""),
                ("description", False, "str", ""),
                ("id", True, "str", ""),
                ("inserted_at", True, "str", ""),
                ("layout", False, "list[JsonValue]", "JsonValue"),
                ("name", True, "str", ""),
                ("panels", False, "list[JsonValue]", "JsonValue"),
                ("parameters", False, "list[JsonValue]", "JsonValue"),
                ("previous_version_id", False, "str", ""),
                ("version_number", True, "int", ""),
            ],
        )
