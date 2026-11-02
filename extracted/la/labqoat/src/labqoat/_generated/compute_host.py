"""ComputeHost"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.compute_host_share import ComputeHostShare
from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class ComputeHost:
    """ComputeHost"""

    capacity: Mapping[str, JsonValue] | None
    gpu_devices: list[JsonValue]
    id: str
    lease_expires_at: str | None
    location_id: str
    share: ComputeHostShare | None
    state: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> ComputeHost:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for ComputeHost")
        return cls(
            capacity=JsonDocument.expect_optional_dict(values["capacity"]),
            gpu_devices=list(JsonDocument.expect_list(values.get("gpu_devices", []))),
            id=JsonDocument.expect_scalar(values["id"], str),
            lease_expires_at=JsonDocument.expect_optional_scalar(values.get("lease_expires_at"), str),
            location_id=JsonDocument.expect_scalar(values["location_id"], str),
            share=ComputeHostShare.from_dict(JsonDocument.expect_dict(values["share"]))
            if values["share"] is not None
            else None,
            state=JsonDocument.expect_scalar(values["state"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("capacity", True, "Mapping[str, JsonValue]", ""),
                ("gpu_devices", True, "list[JsonValue]", "JsonValue"),
                ("id", True, "str", ""),
                ("lease_expires_at", True, "str", ""),
                ("location_id", True, "str", ""),
                ("share", True, "ComputeHostShare", ""),
                ("state", True, "str", ""),
            ],
        )
