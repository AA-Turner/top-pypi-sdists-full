"""Dashboard definition for publication. Omit dashboard identities to create; supply both to revise."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class NewDashboard:
    """Dashboard definition for publication. Omit dashboard identities to create; supply both to revise."""

    layout: list[JsonValue]
    name: str
    panels: list[JsonValue]
    dashboard_id: str | None = None
    description: str | None = None
    parameters: list[JsonValue] | None = field(default_factory=list)
    previous_version_id: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> NewDashboard:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for NewDashboard")
        return cls(
            dashboard_id=JsonDocument.expect_optional_scalar(values.get("dashboard_id"), str),
            description=JsonDocument.expect_optional_scalar(values.get("description"), str),
            layout=list(JsonDocument.expect_list(values.get("layout", []))),
            name=JsonDocument.expect_scalar(values["name"], str),
            panels=list(JsonDocument.expect_list(values.get("panels", []))),
            parameters=list(JsonDocument.expect_list(values.get("parameters", []))),
            previous_version_id=JsonDocument.expect_optional_scalar(values.get("previous_version_id"), str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("dashboard_id", False, "str", ""),
                ("description", False, "str", ""),
                ("layout", True, "list[JsonValue]", "JsonValue"),
                ("name", True, "str", ""),
                ("panels", True, "list[JsonValue]", "JsonValue"),
                ("parameters", False, "list[JsonValue]", "JsonValue"),
                ("previous_version_id", False, "str", ""),
            ],
        )
