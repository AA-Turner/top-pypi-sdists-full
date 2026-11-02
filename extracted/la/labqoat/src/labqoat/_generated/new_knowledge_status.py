"""NewKnowledgeStatus"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class NewKnowledgeStatus:
    """NewKnowledgeStatus"""

    idempotency_key: str
    status: str
    by: str | None = None
    evidence: str | None = None
    note: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> NewKnowledgeStatus:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for NewKnowledgeStatus")
        return cls(
            by=JsonDocument.expect_optional_scalar(values.get("by"), str),
            evidence=JsonDocument.expect_optional_scalar(values.get("evidence"), str),
            idempotency_key=JsonDocument.expect_scalar(values["idempotency_key"], str),
            note=JsonDocument.expect_optional_scalar(values.get("note"), str),
            status=JsonDocument.expect_scalar(values["status"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("by", False, "str", ""),
                ("evidence", False, "str", ""),
                ("idempotency_key", True, "str", ""),
                ("note", False, "str", ""),
                ("status", True, "str", ""),
            ],
        )
