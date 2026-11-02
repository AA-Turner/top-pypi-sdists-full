"""KnowledgeNode"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat._generated.knowledge_revision import KnowledgeRevision
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class KnowledgeNode:
    """KnowledgeNode"""

    head_revision_id: str
    id: str
    inserted_at: str
    kind: str
    parents: list[JsonValue]
    project_id: str
    revision: KnowledgeRevision
    status: str
    links: list[JsonValue] | None = field(default_factory=list)
    links_truncated: bool | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> KnowledgeNode:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for KnowledgeNode")
        return cls(
            head_revision_id=JsonDocument.expect_scalar(values["head_revision_id"], str),
            id=JsonDocument.expect_scalar(values["id"], str),
            inserted_at=JsonDocument.expect_scalar(values["inserted_at"], str),
            kind=JsonDocument.expect_scalar(values["kind"], str),
            links=list(JsonDocument.expect_list(values.get("links", []))),
            links_truncated=JsonDocument.expect_optional_scalar(values.get("links_truncated"), bool),
            parents=list(JsonDocument.expect_list(values.get("parents", []))),
            project_id=JsonDocument.expect_scalar(values["project_id"], str),
            revision=KnowledgeRevision.from_dict(JsonDocument.expect_dict(values["revision"])),
            status=JsonDocument.expect_scalar(values["status"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("head_revision_id", True, "str", ""),
                ("id", True, "str", ""),
                ("inserted_at", True, "str", ""),
                ("kind", True, "str", ""),
                ("links", False, "list[JsonValue]", "JsonValue"),
                ("links_truncated", False, "bool", ""),
                ("parents", True, "list[JsonValue]", "JsonValue"),
                ("project_id", True, "str", ""),
                ("revision", True, "KnowledgeRevision", ""),
                ("status", True, "str", ""),
            ],
        )
