"""NewKnowledgeNode"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class NewKnowledgeNode:
    """NewKnowledgeNode"""

    client_id: str
    kind: str
    title: str
    attachments: list[JsonValue] | None = field(default_factory=list)
    attempt_id: str | None = None
    body: str | None = None
    client_label: str | None = None
    parents: list[JsonValue] | None = field(default_factory=list)
    properties: Mapping[str, JsonValue] | None = None
    run_id: str | None = None
    schema_version: int | None = None
    summary: str | None = None
    supersedes: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> NewKnowledgeNode:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for NewKnowledgeNode")
        return cls(
            attachments=list(JsonDocument.expect_list(values.get("attachments", []))),
            attempt_id=JsonDocument.expect_optional_scalar(values.get("attempt_id"), str),
            body=JsonDocument.expect_optional_scalar(values.get("body"), str),
            client_id=JsonDocument.expect_scalar(values["client_id"], str),
            client_label=JsonDocument.expect_optional_scalar(values.get("client_label"), str),
            kind=JsonDocument.expect_scalar(values["kind"], str),
            parents=list(JsonDocument.expect_list(values.get("parents", []))),
            properties=JsonDocument.expect_optional_dict(values.get("properties")),
            run_id=JsonDocument.expect_optional_scalar(values.get("run_id"), str),
            schema_version=JsonDocument.expect_optional_scalar(values.get("schema_version"), int),
            summary=JsonDocument.expect_optional_scalar(values.get("summary"), str),
            supersedes=JsonDocument.expect_optional_scalar(values.get("supersedes"), str),
            title=JsonDocument.expect_scalar(values["title"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("attachments", False, "list[JsonValue]", "JsonValue"),
                ("attempt_id", False, "str", ""),
                ("body", False, "str", ""),
                ("client_id", True, "str", ""),
                ("client_label", False, "str", ""),
                ("kind", True, "str", ""),
                ("parents", False, "list[JsonValue]", "JsonValue"),
                ("properties", False, "Mapping[str, JsonValue]", ""),
                ("run_id", False, "str", ""),
                ("schema_version", False, "int", ""),
                ("summary", False, "str", ""),
                ("supersedes", False, "str", ""),
                ("title", True, "str", ""),
            ],
        )
