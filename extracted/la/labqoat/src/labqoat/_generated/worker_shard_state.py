"""WorkerShardState"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class WorkerShardState:
    """WorkerShardState"""

    shard_index: int
    status: str
    winning_output_id: str | None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> WorkerShardState:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for WorkerShardState")
        return cls(
            shard_index=JsonDocument.expect_scalar(values["shard_index"], int),
            status=JsonDocument.expect_scalar(values["status"], str),
            winning_output_id=JsonDocument.expect_optional_scalar(values.get("winning_output_id"), str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [("shard_index", True, "int", ""), ("status", True, "str", ""), ("winning_output_id", True, "str", "")],
        )
