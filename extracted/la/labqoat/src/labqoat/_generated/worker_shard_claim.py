"""WorkerShardClaim"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class WorkerShardClaim:
    """WorkerShardClaim"""

    protocol_version: int
    shard_index: int

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> WorkerShardClaim:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for WorkerShardClaim")
        return cls(
            protocol_version=JsonDocument.expect_scalar(values["protocol_version"], int),
            shard_index=JsonDocument.expect_scalar(values["shard_index"], int),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self, [("protocol_version", True, "int", ""), ("shard_index", True, "int", "")]
        )
