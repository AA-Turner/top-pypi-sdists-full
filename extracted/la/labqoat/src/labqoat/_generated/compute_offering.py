"""ComputeOffering"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class ComputeOffering:
    """ComputeOffering"""

    architecture: str
    gpu_family: str | None
    id: str
    location_id: str
    observed_at: str
    price: Mapping[str, JsonValue] | None
    region: str
    resources: Mapping[str, JsonValue]
    selected: bool
    shape: str
    zones: list[JsonValue]

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> ComputeOffering:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for ComputeOffering")
        return cls(
            architecture=JsonDocument.expect_scalar(values["architecture"], str),
            gpu_family=JsonDocument.expect_optional_scalar(values.get("gpu_family"), str),
            id=JsonDocument.expect_scalar(values["id"], str),
            location_id=JsonDocument.expect_scalar(values["location_id"], str),
            observed_at=JsonDocument.expect_scalar(values["observed_at"], str),
            price=JsonDocument.expect_optional_dict(values["price"]),
            region=JsonDocument.expect_scalar(values["region"], str),
            resources=JsonDocument.expect_dict(values["resources"]),
            selected=JsonDocument.expect_scalar(values["selected"], bool),
            shape=JsonDocument.expect_scalar(values["shape"], str),
            zones=list(JsonDocument.expect_list(values.get("zones", []))),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("architecture", True, "str", ""),
                ("gpu_family", True, "str", ""),
                ("id", True, "str", ""),
                ("location_id", True, "str", ""),
                ("observed_at", True, "str", ""),
                ("price", True, "Mapping[str, JsonValue]", ""),
                ("region", True, "str", ""),
                ("resources", True, "Mapping[str, JsonValue]", ""),
                ("selected", True, "bool", ""),
                ("shape", True, "str", ""),
                ("zones", True, "list[JsonValue]", "JsonValue"),
            ],
        )
