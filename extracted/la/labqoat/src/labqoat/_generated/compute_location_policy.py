"""ComputeLocationPolicy"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class ComputeLocationPolicy:
    """ComputeLocationPolicy"""

    instance_types: list[JsonValue]
    location_id: str
    paused: bool
    provenance: str
    revision: int
    snapshot_at: str | None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> ComputeLocationPolicy:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for ComputeLocationPolicy")
        return cls(
            instance_types=list(JsonDocument.expect_list(values.get("instance_types", []))),
            location_id=JsonDocument.expect_scalar(values["location_id"], str),
            paused=JsonDocument.expect_scalar(values["paused"], bool),
            provenance=JsonDocument.expect_scalar(values["provenance"], str),
            revision=JsonDocument.expect_scalar(values["revision"], int),
            snapshot_at=JsonDocument.expect_optional_scalar(values.get("snapshot_at"), str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("instance_types", True, "list[JsonValue]", "JsonValue"),
                ("location_id", True, "str", ""),
                ("paused", True, "bool", ""),
                ("provenance", True, "str", ""),
                ("revision", True, "int", ""),
                ("snapshot_at", True, "str", ""),
            ],
        )
