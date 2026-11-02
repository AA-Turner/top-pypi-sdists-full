"""ProjectMove"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class ProjectMove:
    """ProjectMove"""

    apps: list[JsonValue] | None = field(default_factory=list)
    dashboards: list[JsonValue] | None = field(default_factory=list)
    datasets: list[JsonValue] | None = field(default_factory=list)
    runs: list[JsonValue] | None = field(default_factory=list)

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> ProjectMove:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for ProjectMove")
        return cls(
            apps=list(JsonDocument.expect_list(values.get("apps", []))),
            dashboards=list(JsonDocument.expect_list(values.get("dashboards", []))),
            datasets=list(JsonDocument.expect_list(values.get("datasets", []))),
            runs=list(JsonDocument.expect_list(values.get("runs", []))),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("apps", False, "list[JsonValue]", "JsonValue"),
                ("dashboards", False, "list[JsonValue]", "JsonValue"),
                ("datasets", False, "list[JsonValue]", "JsonValue"),
                ("runs", False, "list[JsonValue]", "JsonValue"),
            ],
        )
