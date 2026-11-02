"""ComputeWorkerPool"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class ComputeWorkerPool:
    """ComputeWorkerPool"""

    active: bool
    environment_id: str
    id: str
    policy: Mapping[str, JsonValue]
    prototype_run_id: str
    revision: int

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> ComputeWorkerPool:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for ComputeWorkerPool")
        return cls(
            active=JsonDocument.expect_scalar(values["active"], bool),
            environment_id=JsonDocument.expect_scalar(values["environment_id"], str),
            id=JsonDocument.expect_scalar(values["id"], str),
            policy=JsonDocument.expect_dict(values["policy"]),
            prototype_run_id=JsonDocument.expect_scalar(values["prototype_run_id"], str),
            revision=JsonDocument.expect_scalar(values["revision"], int),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("active", True, "bool", ""),
                ("environment_id", True, "str", ""),
                ("id", True, "str", ""),
                ("policy", True, "Mapping[str, JsonValue]", ""),
                ("prototype_run_id", True, "str", ""),
                ("revision", True, "int", ""),
            ],
        )
