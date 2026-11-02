"""NewKnowledgeLink"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class NewKnowledgeLink:
    """NewKnowledgeLink"""

    from_node_id: str
    idempotency_key: str
    kind: str
    target: str
    note: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> NewKnowledgeLink:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for NewKnowledgeLink")
        return cls(
            from_node_id=JsonDocument.expect_scalar(values["from_node_id"], str),
            idempotency_key=JsonDocument.expect_scalar(values["idempotency_key"], str),
            kind=JsonDocument.expect_scalar(values["kind"], str),
            note=JsonDocument.expect_optional_scalar(values.get("note"), str),
            target=JsonDocument.expect_scalar(values["target"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("from_node_id", True, "str", ""),
                ("idempotency_key", True, "str", ""),
                ("kind", True, "str", ""),
                ("note", False, "str", ""),
                ("target", True, "str", ""),
            ],
        )
