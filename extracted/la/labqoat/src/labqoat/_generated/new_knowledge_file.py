"""NewKnowledgeFile"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class NewKnowledgeFile:
    """NewKnowledgeFile"""

    asset_id: str
    expected_version: int
    idempotency_key: str
    path: str

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> NewKnowledgeFile:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for NewKnowledgeFile")
        return cls(
            asset_id=JsonDocument.expect_scalar(values["asset_id"], str),
            expected_version=JsonDocument.expect_scalar(values["expected_version"], int),
            idempotency_key=JsonDocument.expect_scalar(values["idempotency_key"], str),
            path=JsonDocument.expect_scalar(values["path"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("asset_id", True, "str", ""),
                ("expected_version", True, "int", ""),
                ("idempotency_key", True, "str", ""),
                ("path", True, "str", ""),
            ],
        )
