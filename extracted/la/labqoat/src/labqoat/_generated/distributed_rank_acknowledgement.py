"""DistributedRankAcknowledgement"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat._generated.restore_acknowledgement import RestoreAcknowledgement
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class DistributedRankAcknowledgement:
    """DistributedRankAcknowledgement"""

    payload_sha256: str
    rank: int
    restored: RestoreAcknowledgement

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> DistributedRankAcknowledgement:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for DistributedRankAcknowledgement")
        return cls(
            payload_sha256=JsonDocument.expect_scalar(values["payload_sha256"], str),
            rank=JsonDocument.expect_scalar(values["rank"], int),
            restored=RestoreAcknowledgement.from_dict(JsonDocument.expect_dict(values["restored"])),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("payload_sha256", True, "str", ""),
                ("rank", True, "int", ""),
                ("restored", True, "RestoreAcknowledgement", ""),
            ],
        )
