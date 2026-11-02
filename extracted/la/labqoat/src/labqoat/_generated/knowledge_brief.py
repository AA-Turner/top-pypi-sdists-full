"""KnowledgeBrief"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class KnowledgeBrief:
    """KnowledgeBrief"""

    attention: list[JsonValue]
    attention_counts: Mapping[str, JsonValue]
    brief: Mapping[str, JsonValue] | None
    changes: list[JsonValue]
    conclusions: list[JsonValue]
    contradictions: list[JsonValue]
    counts: list[JsonValue]
    decisions: list[JsonValue]
    experiments: list[JsonValue]
    files: list[JsonValue]
    frontier: list[JsonValue]
    hypotheses: Mapping[str, JsonValue]
    notes: list[JsonValue]
    project_id: str
    questions: list[JsonValue]
    results: list[JsonValue]
    sequence: int
    since_last_read: Mapping[str, JsonValue] | None
    sources: list[JsonValue]
    staleness: Mapping[str, JsonValue]
    truncated: bool
    truncated_fields: list[JsonValue]

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> KnowledgeBrief:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for KnowledgeBrief")
        return cls(
            attention=list(JsonDocument.expect_list(values.get("attention", []))),
            attention_counts=JsonDocument.expect_dict(values["attention_counts"]),
            brief=JsonDocument.expect_optional_dict(values["brief"]),
            changes=list(JsonDocument.expect_list(values.get("changes", []))),
            conclusions=list(JsonDocument.expect_list(values.get("conclusions", []))),
            contradictions=list(JsonDocument.expect_list(values.get("contradictions", []))),
            counts=list(JsonDocument.expect_list(values.get("counts", []))),
            decisions=list(JsonDocument.expect_list(values.get("decisions", []))),
            experiments=list(JsonDocument.expect_list(values.get("experiments", []))),
            files=list(JsonDocument.expect_list(values.get("files", []))),
            frontier=list(JsonDocument.expect_list(values.get("frontier", []))),
            hypotheses=JsonDocument.expect_dict(values["hypotheses"]),
            notes=list(JsonDocument.expect_list(values.get("notes", []))),
            project_id=JsonDocument.expect_scalar(values["project_id"], str),
            questions=list(JsonDocument.expect_list(values.get("questions", []))),
            results=list(JsonDocument.expect_list(values.get("results", []))),
            sequence=JsonDocument.expect_scalar(values["sequence"], int),
            since_last_read=JsonDocument.expect_optional_dict(values["since_last_read"]),
            sources=list(JsonDocument.expect_list(values.get("sources", []))),
            staleness=JsonDocument.expect_dict(values["staleness"]),
            truncated=JsonDocument.expect_scalar(values["truncated"], bool),
            truncated_fields=list(JsonDocument.expect_list(values.get("truncated_fields", []))),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("attention", True, "list[JsonValue]", "JsonValue"),
                ("attention_counts", True, "Mapping[str, JsonValue]", ""),
                ("brief", True, "Mapping[str, JsonValue]", ""),
                ("changes", True, "list[JsonValue]", "JsonValue"),
                ("conclusions", True, "list[JsonValue]", "JsonValue"),
                ("contradictions", True, "list[JsonValue]", "JsonValue"),
                ("counts", True, "list[JsonValue]", "JsonValue"),
                ("decisions", True, "list[JsonValue]", "JsonValue"),
                ("experiments", True, "list[JsonValue]", "JsonValue"),
                ("files", True, "list[JsonValue]", "JsonValue"),
                ("frontier", True, "list[JsonValue]", "JsonValue"),
                ("hypotheses", True, "Mapping[str, JsonValue]", ""),
                ("notes", True, "list[JsonValue]", "JsonValue"),
                ("project_id", True, "str", ""),
                ("questions", True, "list[JsonValue]", "JsonValue"),
                ("results", True, "list[JsonValue]", "JsonValue"),
                ("sequence", True, "int", ""),
                ("since_last_read", True, "Mapping[str, JsonValue]", ""),
                ("sources", True, "list[JsonValue]", "JsonValue"),
                ("staleness", True, "Mapping[str, JsonValue]", ""),
                ("truncated", True, "bool", ""),
                ("truncated_fields", True, "list[JsonValue]", "JsonValue"),
            ],
        )
