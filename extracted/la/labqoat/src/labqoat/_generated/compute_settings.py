"""ComputeSettings"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class ComputeSettings:
    """ComputeSettings"""

    defaults: Mapping[str, JsonValue]
    elastic_instance_rate_usd_per_hour: str | None
    machine_idle_seconds: int
    queue_timeout_seconds: int
    revision: int
    worker_idle_seconds: int
    workload_limits: Mapping[str, JsonValue]

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> ComputeSettings:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for ComputeSettings")
        return cls(
            defaults=JsonDocument.expect_dict(values["defaults"]),
            elastic_instance_rate_usd_per_hour=JsonDocument.expect_optional_scalar(
                values.get("elastic_instance_rate_usd_per_hour"), str
            ),
            machine_idle_seconds=JsonDocument.expect_scalar(values["machine_idle_seconds"], int),
            queue_timeout_seconds=JsonDocument.expect_scalar(values["queue_timeout_seconds"], int),
            revision=JsonDocument.expect_scalar(values["revision"], int),
            worker_idle_seconds=JsonDocument.expect_scalar(values["worker_idle_seconds"], int),
            workload_limits=JsonDocument.expect_dict(values["workload_limits"]),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("defaults", True, "Mapping[str, JsonValue]", ""),
                ("elastic_instance_rate_usd_per_hour", True, "str", ""),
                ("machine_idle_seconds", True, "int", ""),
                ("queue_timeout_seconds", True, "int", ""),
                ("revision", True, "int", ""),
                ("worker_idle_seconds", True, "int", ""),
                ("workload_limits", True, "Mapping[str, JsonValue]", ""),
            ],
        )
