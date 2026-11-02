"""ShardRecoveryItem"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class ShardRecoveryItem:
    """ShardRecoveryItem"""

    action: str
    output_id: str | None
    shard_index: int
    source_outcome_id: str | None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> ShardRecoveryItem:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for ShardRecoveryItem")
        return cls(
            action=JsonDocument.expect_scalar(values["action"], str),
            output_id=JsonDocument.expect_optional_scalar(values.get("output_id"), str),
            shard_index=JsonDocument.expect_scalar(values["shard_index"], int),
            source_outcome_id=JsonDocument.expect_optional_scalar(values.get("source_outcome_id"), str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("action", True, "str", ""),
                ("output_id", True, "str", ""),
                ("shard_index", True, "int", ""),
                ("source_outcome_id", True, "str", ""),
            ],
        )
