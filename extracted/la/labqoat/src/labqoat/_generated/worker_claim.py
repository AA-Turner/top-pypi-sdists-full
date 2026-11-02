"""Exclusive claim for one shard index of the current attempt."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class WorkerClaim:
    """Exclusive claim for one shard index of the current attempt."""

    shard_index: int

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> WorkerClaim:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for WorkerClaim")
        return cls(
            shard_index=JsonDocument.expect_scalar(values["shard_index"], int),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(self, [("shard_index", True, "int", "")])
