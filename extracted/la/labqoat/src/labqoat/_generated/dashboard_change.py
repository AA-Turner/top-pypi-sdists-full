"""A watched panel's leader was replaced or its frontier moved."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class DashboardChange:
    """A watched panel's leader was replaced or its frontier moved."""

    cursor: str
    dashboard_id: str
    data: Mapping[str, JsonValue]
    id: str
    inserted_at: str
    kind: str
    panel_id: str
    panel_title: str
    version_id: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> DashboardChange:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for DashboardChange")
        return cls(
            cursor=JsonDocument.expect_scalar(values["cursor"], str),
            dashboard_id=JsonDocument.expect_scalar(values["dashboard_id"], str),
            data=JsonDocument.expect_dict(values["data"]),
            id=JsonDocument.expect_scalar(values["id"], str),
            inserted_at=JsonDocument.expect_scalar(values["inserted_at"], str),
            kind=JsonDocument.expect_scalar(values["kind"], str),
            panel_id=JsonDocument.expect_scalar(values["panel_id"], str),
            panel_title=JsonDocument.expect_scalar(values["panel_title"], str),
            version_id=JsonDocument.expect_scalar(values["version_id"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("cursor", True, "str", ""),
                ("dashboard_id", True, "str", ""),
                ("data", True, "Mapping[str, JsonValue]", ""),
                ("id", True, "str", ""),
                ("inserted_at", True, "str", ""),
                ("kind", True, "str", ""),
                ("panel_id", True, "str", ""),
                ("panel_title", True, "str", ""),
                ("version_id", True, "str", ""),
            ],
        )
