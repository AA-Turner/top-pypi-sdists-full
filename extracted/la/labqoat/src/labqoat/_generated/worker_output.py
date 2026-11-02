"""Result object attached to the claimed shard; shard_index selects a non-zero shard."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class WorkerOutput:
    """Result object attached to the claimed shard; shard_index selects a non-zero shard."""

    shard_index: int | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> WorkerOutput:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for WorkerOutput")
        return cls(
            shard_index=JsonDocument.expect_optional_scalar(values.get("shard_index"), int),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(self, [("shard_index", False, "int", "")])
