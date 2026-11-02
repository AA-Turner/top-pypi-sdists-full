"""LocationRegistry"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class LocationRegistry:
    """LocationRegistry"""

    default_location: str
    locations: list[JsonValue]
    revision: int

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> LocationRegistry:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for LocationRegistry")
        return cls(
            default_location=JsonDocument.expect_scalar(values["default_location"], str),
            locations=list(JsonDocument.expect_list(values.get("locations", []))),
            revision=JsonDocument.expect_scalar(values["revision"], int),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("default_location", True, "str", ""),
                ("locations", True, "list[JsonValue]", "JsonValue"),
                ("revision", True, "int", ""),
            ],
        )
