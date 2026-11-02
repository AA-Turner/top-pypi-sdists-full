"""ShardOutcome"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class ShardOutcome:
    """ShardOutcome"""

    attempt_id: str
    cycle_id: str | None
    id: str
    inserted_at: str
    outcome: str
    output_id: str | None
    run_id: str
    shard_index: int

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> ShardOutcome:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for ShardOutcome")
        return cls(
            attempt_id=JsonDocument.expect_scalar(values["attempt_id"], str),
            cycle_id=JsonDocument.expect_optional_scalar(values.get("cycle_id"), str),
            id=JsonDocument.expect_scalar(values["id"], str),
            inserted_at=JsonDocument.expect_scalar(values["inserted_at"], str),
            outcome=JsonDocument.expect_scalar(values["outcome"], str),
            output_id=JsonDocument.expect_optional_scalar(values.get("output_id"), str),
            run_id=JsonDocument.expect_scalar(values["run_id"], str),
            shard_index=JsonDocument.expect_scalar(values["shard_index"], int),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("attempt_id", True, "str", ""),
                ("cycle_id", True, "str", ""),
                ("id", True, "str", ""),
                ("inserted_at", True, "str", ""),
                ("outcome", True, "str", ""),
                ("output_id", True, "str", ""),
                ("run_id", True, "str", ""),
                ("shard_index", True, "int", ""),
            ],
        )
