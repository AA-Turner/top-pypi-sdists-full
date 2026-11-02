"""KnowledgeOrientation"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class KnowledgeOrientation:
    """KnowledgeOrientation"""

    project_id: str
    sequence: int
    attention: list[JsonValue] | None = field(default_factory=list)
    attention_counts: Mapping[str, JsonValue] | None = None
    briefs: list[JsonValue] | None = field(default_factory=list)
    by_actor: Mapping[str, JsonValue] | None = None
    commits: int | None = None
    files: int | None = None
    from_sequence: int | None = None
    links: int | None = None
    objectives: list[JsonValue] | None = field(default_factory=list)
    objectives_changed: bool | None = None
    previous_read: int | None = None
    research: list[JsonValue] | None = field(default_factory=list)
    research_changed: int | None = None
    to_sequence: int | None = None
    truncated: bool | None = None
    unranked_metrics: list[JsonValue] | None = field(default_factory=list)

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> KnowledgeOrientation:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for KnowledgeOrientation")
        return cls(
            attention=list(JsonDocument.expect_list(values.get("attention", []))),
            attention_counts=JsonDocument.expect_optional_dict(values.get("attention_counts")),
            briefs=list(JsonDocument.expect_list(values.get("briefs", []))),
            by_actor=JsonDocument.expect_optional_dict(values.get("by_actor")),
            commits=JsonDocument.expect_optional_scalar(values.get("commits"), int),
            files=JsonDocument.expect_optional_scalar(values.get("files"), int),
            from_sequence=JsonDocument.expect_optional_scalar(values.get("from_sequence"), int),
            links=JsonDocument.expect_optional_scalar(values.get("links"), int),
            objectives=list(JsonDocument.expect_list(values.get("objectives", []))),
            objectives_changed=JsonDocument.expect_optional_scalar(values.get("objectives_changed"), bool),
            previous_read=JsonDocument.expect_optional_scalar(values.get("previous_read"), int),
            project_id=JsonDocument.expect_scalar(values["project_id"], str),
            research=list(JsonDocument.expect_list(values.get("research", []))),
            research_changed=JsonDocument.expect_optional_scalar(values.get("research_changed"), int),
            sequence=JsonDocument.expect_scalar(values["sequence"], int),
            to_sequence=JsonDocument.expect_optional_scalar(values.get("to_sequence"), int),
            truncated=JsonDocument.expect_optional_scalar(values.get("truncated"), bool),
            unranked_metrics=list(JsonDocument.expect_list(values.get("unranked_metrics", []))),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("attention", False, "list[JsonValue]", "JsonValue"),
                ("attention_counts", False, "Mapping[str, JsonValue]", ""),
                ("briefs", False, "list[JsonValue]", "JsonValue"),
                ("by_actor", False, "Mapping[str, JsonValue]", ""),
                ("commits", False, "int", ""),
                ("files", False, "int", ""),
                ("from_sequence", False, "int", ""),
                ("links", False, "int", ""),
                ("objectives", False, "list[JsonValue]", "JsonValue"),
                ("objectives_changed", False, "bool", ""),
                ("previous_read", False, "int", ""),
                ("project_id", True, "str", ""),
                ("research", False, "list[JsonValue]", "JsonValue"),
                ("research_changed", False, "int", ""),
                ("sequence", True, "int", ""),
                ("to_sequence", False, "int", ""),
                ("truncated", False, "bool", ""),
                ("unranked_metrics", False, "list[JsonValue]", "JsonValue"),
            ],
        )
