"""A machine with capacity and allocations."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class Node:
    """A machine with capacity and allocations."""

    id: str
    allocatable: Mapping[str, JsonValue] | None = None
    allocations: int | None = None
    capacity: Mapping[str, JsonValue] | None = None
    environment_id: str | None = None
    gpu_devices: list[JsonValue] | None = field(default_factory=list)
    gpu_models: list[JsonValue] | None = field(default_factory=list)
    instance_family: str | None = None
    location_id: str | None = None
    machine_capacity: Mapping[str, JsonValue] | None = None
    offering: Mapping[str, JsonValue] | None = None
    paused: bool | None = None
    placement: Mapping[str, JsonValue] | None = None
    pool: str | None = None
    provider: str | None = None
    region: str | None = None
    reserved: Mapping[str, JsonValue] | None = None
    runtime_versions: Mapping[str, JsonValue] | None = None
    state: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> Node:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for Node")
        return cls(
            allocatable=JsonDocument.expect_optional_dict(values.get("allocatable")),
            allocations=JsonDocument.expect_optional_scalar(values.get("allocations"), int),
            capacity=JsonDocument.expect_optional_dict(values.get("capacity")),
            environment_id=JsonDocument.expect_optional_scalar(values.get("environment_id"), str),
            gpu_devices=list(JsonDocument.expect_list(values.get("gpu_devices", []))),
            gpu_models=list(JsonDocument.expect_list(values.get("gpu_models", []))),
            id=JsonDocument.expect_scalar(values["id"], str),
            instance_family=JsonDocument.expect_optional_scalar(values.get("instance_family"), str),
            location_id=JsonDocument.expect_optional_scalar(values.get("location_id"), str),
            machine_capacity=JsonDocument.expect_optional_dict(values.get("machine_capacity")),
            offering=JsonDocument.expect_optional_dict(values.get("offering")),
            paused=JsonDocument.expect_optional_scalar(values.get("paused"), bool),
            placement=JsonDocument.expect_optional_dict(values.get("placement")),
            pool=JsonDocument.expect_optional_scalar(values.get("pool"), str),
            provider=JsonDocument.expect_optional_scalar(values.get("provider"), str),
            region=JsonDocument.expect_optional_scalar(values.get("region"), str),
            reserved=JsonDocument.expect_optional_dict(values.get("reserved")),
            runtime_versions=JsonDocument.expect_optional_dict(values.get("runtime_versions")),
            state=JsonDocument.expect_optional_scalar(values.get("state"), str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("allocatable", False, "Mapping[str, JsonValue]", ""),
                ("allocations", False, "int", ""),
                ("capacity", False, "Mapping[str, JsonValue]", ""),
                ("environment_id", False, "str", ""),
                ("gpu_devices", False, "list[JsonValue]", "JsonValue"),
                ("gpu_models", False, "list[JsonValue]", "JsonValue"),
                ("id", True, "str", ""),
                ("instance_family", False, "str", ""),
                ("location_id", False, "str", ""),
                ("machine_capacity", False, "Mapping[str, JsonValue]", ""),
                ("offering", False, "Mapping[str, JsonValue]", ""),
                ("paused", False, "bool", ""),
                ("placement", False, "Mapping[str, JsonValue]", ""),
                ("pool", False, "str", ""),
                ("provider", False, "str", ""),
                ("region", False, "str", ""),
                ("reserved", False, "Mapping[str, JsonValue]", ""),
                ("runtime_versions", False, "Mapping[str, JsonValue]", ""),
                ("state", False, "str", ""),
            ],
        )
