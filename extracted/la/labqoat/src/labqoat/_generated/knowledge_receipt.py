"""KnowledgeReceipt"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat._generated.knowledge_node import KnowledgeNode
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class KnowledgeReceipt:
    """KnowledgeReceipt"""

    commit_id: str
    idempotency_key: str
    project_id: str
    sequence: int
    brief: Mapping[str, JsonValue] | None = None
    file: Mapping[str, JsonValue] | None = None
    frontier: list[JsonValue] | None = field(default_factory=list)
    link: Mapping[str, JsonValue] | None = None
    links: list[JsonValue] | None = field(default_factory=list)
    node: KnowledgeNode | None = None
    nodes: list[JsonValue] | None = field(default_factory=list)
    objectives: list[JsonValue] | None = field(default_factory=list)
    status: Mapping[str, JsonValue] | None = None
    statuses: list[JsonValue] | None = field(default_factory=list)
    warnings: list[JsonValue] | None = field(default_factory=list)

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> KnowledgeReceipt:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for KnowledgeReceipt")
        return cls(
            brief=JsonDocument.expect_optional_dict(values.get("brief")),
            commit_id=JsonDocument.expect_scalar(values["commit_id"], str),
            file=JsonDocument.expect_optional_dict(values.get("file")),
            frontier=list(JsonDocument.expect_list(values.get("frontier", []))),
            idempotency_key=JsonDocument.expect_scalar(values["idempotency_key"], str),
            link=JsonDocument.expect_optional_dict(values.get("link")),
            links=list(JsonDocument.expect_list(values.get("links", []))),
            node=KnowledgeNode.from_dict(JsonDocument.expect_dict(values.get("node")))
            if values.get("node") is not None
            else None,
            nodes=list(JsonDocument.expect_list(values.get("nodes", []))),
            objectives=list(JsonDocument.expect_list(values.get("objectives", []))),
            project_id=JsonDocument.expect_scalar(values["project_id"], str),
            sequence=JsonDocument.expect_scalar(values["sequence"], int),
            status=JsonDocument.expect_optional_dict(values.get("status")),
            statuses=list(JsonDocument.expect_list(values.get("statuses", []))),
            warnings=list(JsonDocument.expect_list(values.get("warnings", []))),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("brief", False, "Mapping[str, JsonValue]", ""),
                ("commit_id", True, "str", ""),
                ("file", False, "Mapping[str, JsonValue]", ""),
                ("frontier", False, "list[JsonValue]", "JsonValue"),
                ("idempotency_key", True, "str", ""),
                ("link", False, "Mapping[str, JsonValue]", ""),
                ("links", False, "list[JsonValue]", "JsonValue"),
                ("node", False, "KnowledgeNode", ""),
                ("nodes", False, "list[JsonValue]", "JsonValue"),
                ("objectives", False, "list[JsonValue]", "JsonValue"),
                ("project_id", True, "str", ""),
                ("sequence", True, "int", ""),
                ("status", False, "Mapping[str, JsonValue]", ""),
                ("statuses", False, "list[JsonValue]", "JsonValue"),
                ("warnings", False, "list[JsonValue]", "JsonValue"),
            ],
        )
