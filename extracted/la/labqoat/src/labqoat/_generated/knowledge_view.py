"""KnowledgeView"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class KnowledgeView:
    """KnowledgeView"""

    items: list[JsonValue]
    limit: int
    next_cursor: str | None
    project_id: str
    sequence: int
    truncated: bool
    warnings: list[JsonValue]
    evidence: Mapping[str, JsonValue] | None = None
    retrieval: Mapping[str, JsonValue] | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> KnowledgeView:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for KnowledgeView")
        return cls(
            evidence=JsonDocument.expect_optional_dict(values.get("evidence")),
            items=list(JsonDocument.expect_list(values.get("items", []))),
            limit=JsonDocument.expect_scalar(values["limit"], int),
            next_cursor=JsonDocument.expect_optional_scalar(values.get("next_cursor"), str),
            project_id=JsonDocument.expect_scalar(values["project_id"], str),
            retrieval=JsonDocument.expect_optional_dict(values.get("retrieval")),
            sequence=JsonDocument.expect_scalar(values["sequence"], int),
            truncated=JsonDocument.expect_scalar(values["truncated"], bool),
            warnings=list(JsonDocument.expect_list(values.get("warnings", []))),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("evidence", False, "Mapping[str, JsonValue]", ""),
                ("items", True, "list[JsonValue]", "JsonValue"),
                ("limit", True, "int", ""),
                ("next_cursor", True, "str", ""),
                ("project_id", True, "str", ""),
                ("retrieval", False, "Mapping[str, JsonValue]", ""),
                ("sequence", True, "int", ""),
                ("truncated", True, "bool", ""),
                ("warnings", True, "list[JsonValue]", "JsonValue"),
            ],
        )
