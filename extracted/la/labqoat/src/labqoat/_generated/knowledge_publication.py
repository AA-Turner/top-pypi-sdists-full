"""KnowledgePublication"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat._generated.knowledge_step_brief import KnowledgeStepBrief
from labqoat._generated.knowledge_step_link import KnowledgeStepLink
from labqoat._generated.knowledge_step_status import KnowledgeStepStatus
from labqoat._generated.new_knowledge_node import NewKnowledgeNode
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class KnowledgePublication:
    """KnowledgePublication"""

    idempotency_key: str
    brief: KnowledgeStepBrief | None = None
    links: list[KnowledgeStepLink] | None = field(default_factory=list)
    nodes: list[NewKnowledgeNode] | None = field(default_factory=list)
    statuses: list[KnowledgeStepStatus] | None = field(default_factory=list)

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> KnowledgePublication:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for KnowledgePublication")
        return cls(
            brief=KnowledgeStepBrief.from_dict(JsonDocument.expect_dict(values.get("brief")))
            if values.get("brief") is not None
            else None,
            idempotency_key=JsonDocument.expect_scalar(values["idempotency_key"], str),
            links=[
                KnowledgeStepLink.from_dict(JsonDocument.expect_dict(v))
                for v in JsonDocument.expect_list(values.get("links", []))
            ],
            nodes=[
                NewKnowledgeNode.from_dict(JsonDocument.expect_dict(v))
                for v in JsonDocument.expect_list(values.get("nodes", []))
            ],
            statuses=[
                KnowledgeStepStatus.from_dict(JsonDocument.expect_dict(v))
                for v in JsonDocument.expect_list(values.get("statuses", []))
            ],
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("brief", False, "KnowledgeStepBrief", ""),
                ("idempotency_key", True, "str", ""),
                ("links", False, "list[KnowledgeStepLink]", "KnowledgeStepLink"),
                ("nodes", False, "list[NewKnowledgeNode]", "NewKnowledgeNode"),
                ("statuses", False, "list[KnowledgeStepStatus]", "KnowledgeStepStatus"),
            ],
        )
