"""ComputeHostShare"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class ComputeHostShare:
    """ComputeHostShare"""

    cpu_millicores: int
    gpu_device_ids: list[JsonValue]
    memory_mb: int
    ephemeral_storage_mb: int | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> ComputeHostShare:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for ComputeHostShare")
        return cls(
            cpu_millicores=JsonDocument.expect_scalar(values["cpu_millicores"], int),
            ephemeral_storage_mb=JsonDocument.expect_optional_scalar(values.get("ephemeral_storage_mb"), int),
            gpu_device_ids=list(JsonDocument.expect_list(values.get("gpu_device_ids", []))),
            memory_mb=JsonDocument.expect_scalar(values["memory_mb"], int),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("cpu_millicores", True, "int", ""),
                ("ephemeral_storage_mb", False, "int", ""),
                ("gpu_device_ids", True, "list[JsonValue]", "JsonValue"),
                ("memory_mb", True, "int", ""),
            ],
        )
