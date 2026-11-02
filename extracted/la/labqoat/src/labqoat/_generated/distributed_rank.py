"""DistributedRank"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class DistributedRank:
    """DistributedRank"""

    byte_size: int
    id: str
    path: str
    progress: Mapping[str, JsonValue]
    rank: int
    sha256: str
    state: list[JsonValue]
    receipt_fingerprint: str | None = None
    restored_at: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> DistributedRank:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for DistributedRank")
        return cls(
            byte_size=JsonDocument.expect_scalar(values["byte_size"], int),
            id=JsonDocument.expect_scalar(values["id"], str),
            path=JsonDocument.expect_scalar(values["path"], str),
            progress=JsonDocument.expect_dict(values["progress"]),
            rank=JsonDocument.expect_scalar(values["rank"], int),
            receipt_fingerprint=JsonDocument.expect_optional_scalar(values.get("receipt_fingerprint"), str),
            restored_at=JsonDocument.expect_optional_scalar(values.get("restored_at"), str),
            sha256=JsonDocument.expect_scalar(values["sha256"], str),
            state=list(JsonDocument.expect_list(values.get("state", []))),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("byte_size", True, "int", ""),
                ("id", True, "str", ""),
                ("path", True, "str", ""),
                ("progress", True, "Mapping[str, JsonValue]", ""),
                ("rank", True, "int", ""),
                ("receipt_fingerprint", False, "str", ""),
                ("restored_at", False, "str", ""),
                ("sha256", True, "str", ""),
                ("state", True, "list[JsonValue]", "JsonValue"),
            ],
        )
