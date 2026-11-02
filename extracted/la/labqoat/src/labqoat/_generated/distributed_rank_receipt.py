"""DistributedRankReceipt"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.distributed_rank_acknowledgement import DistributedRankAcknowledgement
from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class DistributedRankReceipt:
    """DistributedRankReceipt"""

    attempt_id: str
    evidence: DistributedRankAcknowledgement
    fingerprint: str
    id: str
    inserted_at: str
    rank: int

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> DistributedRankReceipt:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for DistributedRankReceipt")
        return cls(
            attempt_id=JsonDocument.expect_scalar(values["attempt_id"], str),
            evidence=DistributedRankAcknowledgement.from_dict(JsonDocument.expect_dict(values["evidence"])),
            fingerprint=JsonDocument.expect_scalar(values["fingerprint"], str),
            id=JsonDocument.expect_scalar(values["id"], str),
            inserted_at=JsonDocument.expect_scalar(values["inserted_at"], str),
            rank=JsonDocument.expect_scalar(values["rank"], int),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("attempt_id", True, "str", ""),
                ("evidence", True, "DistributedRankAcknowledgement", ""),
                ("fingerprint", True, "str", ""),
                ("id", True, "str", ""),
                ("inserted_at", True, "str", ""),
                ("rank", True, "int", ""),
            ],
        )
