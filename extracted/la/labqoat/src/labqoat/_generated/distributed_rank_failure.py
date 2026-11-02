"""DistributedRankFailure"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class DistributedRankFailure:
    """DistributedRankFailure"""

    failure_class: str
    rank: int
    reason: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> DistributedRankFailure:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for DistributedRankFailure")
        return cls(
            failure_class=JsonDocument.expect_scalar(values["failure_class"], str),
            rank=JsonDocument.expect_scalar(values["rank"], int),
            reason=JsonDocument.expect_scalar(values["reason"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self, [("failure_class", True, "str", ""), ("rank", True, "int", ""), ("reason", True, "str", "")]
        )
