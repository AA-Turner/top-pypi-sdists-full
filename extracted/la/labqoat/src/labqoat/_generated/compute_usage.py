"""ComputeUsage"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class ComputeUsage:
    """ComputeUsage"""

    elastic: Mapping[str, JsonValue]
    families: list[JsonValue]
    observed_at: str
    policy_revision: int
    workload: Mapping[str, JsonValue]

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> ComputeUsage:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for ComputeUsage")
        return cls(
            elastic=JsonDocument.expect_dict(values["elastic"]),
            families=list(JsonDocument.expect_list(values.get("families", []))),
            observed_at=JsonDocument.expect_scalar(values["observed_at"], str),
            policy_revision=JsonDocument.expect_scalar(values["policy_revision"], int),
            workload=JsonDocument.expect_dict(values["workload"]),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("elastic", True, "Mapping[str, JsonValue]", ""),
                ("families", True, "list[JsonValue]", "JsonValue"),
                ("observed_at", True, "str", ""),
                ("policy_revision", True, "int", ""),
                ("workload", True, "Mapping[str, JsonValue]", ""),
            ],
        )
