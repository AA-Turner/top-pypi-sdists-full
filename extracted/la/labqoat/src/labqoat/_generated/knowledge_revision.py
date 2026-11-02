"""KnowledgeRevision"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class KnowledgeRevision:
    """KnowledgeRevision"""

    actor: str
    body: str
    commit_id: str
    digest: str
    id: str
    inserted_at: str
    node_id: str
    number: int
    project_id: str
    properties: Mapping[str, JsonValue]
    schema_version: int
    summary: str
    title: str
    attachments: list[JsonValue] | None = field(default_factory=list)
    attempt_id: str | None = None
    client_label: str | None = None
    execution: Mapping[str, JsonValue] | None = None
    run_id: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> KnowledgeRevision:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for KnowledgeRevision")
        return cls(
            actor=JsonDocument.expect_scalar(values["actor"], str),
            attachments=list(JsonDocument.expect_list(values.get("attachments", []))),
            attempt_id=JsonDocument.expect_optional_scalar(values.get("attempt_id"), str),
            body=JsonDocument.expect_scalar(values["body"], str),
            client_label=JsonDocument.expect_optional_scalar(values.get("client_label"), str),
            commit_id=JsonDocument.expect_scalar(values["commit_id"], str),
            digest=JsonDocument.expect_scalar(values["digest"], str),
            execution=JsonDocument.expect_optional_dict(values.get("execution")),
            id=JsonDocument.expect_scalar(values["id"], str),
            inserted_at=JsonDocument.expect_scalar(values["inserted_at"], str),
            node_id=JsonDocument.expect_scalar(values["node_id"], str),
            number=JsonDocument.expect_scalar(values["number"], int),
            project_id=JsonDocument.expect_scalar(values["project_id"], str),
            properties=JsonDocument.expect_dict(values["properties"]),
            run_id=JsonDocument.expect_optional_scalar(values.get("run_id"), str),
            schema_version=JsonDocument.expect_scalar(values["schema_version"], int),
            summary=JsonDocument.expect_scalar(values["summary"], str),
            title=JsonDocument.expect_scalar(values["title"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("actor", True, "str", ""),
                ("attachments", False, "list[JsonValue]", "JsonValue"),
                ("attempt_id", False, "str", ""),
                ("body", True, "str", ""),
                ("client_label", False, "str", ""),
                ("commit_id", True, "str", ""),
                ("digest", True, "str", ""),
                ("execution", False, "Mapping[str, JsonValue]", ""),
                ("id", True, "str", ""),
                ("inserted_at", True, "str", ""),
                ("node_id", True, "str", ""),
                ("number", True, "int", ""),
                ("project_id", True, "str", ""),
                ("properties", True, "Mapping[str, JsonValue]", ""),
                ("run_id", False, "str", ""),
                ("schema_version", True, "int", ""),
                ("summary", True, "str", ""),
                ("title", True, "str", ""),
            ],
        )
