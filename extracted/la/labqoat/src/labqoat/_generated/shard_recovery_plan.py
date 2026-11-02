"""ShardRecoveryPlan"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat._generated.shard_recovery_item import ShardRecoveryItem
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class ShardRecoveryPlan:
    """ShardRecoveryPlan"""

    items: list[ShardRecoveryItem]
    version: int

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> ShardRecoveryPlan:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for ShardRecoveryPlan")
        return cls(
            items=[
                ShardRecoveryItem.from_dict(JsonDocument.expect_dict(v))
                for v in JsonDocument.expect_list(values.get("items", []))
            ],
            version=JsonDocument.expect_scalar(values["version"], int),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self, [("items", True, "list[ShardRecoveryItem]", "ShardRecoveryItem"), ("version", True, "int", "")]
        )
