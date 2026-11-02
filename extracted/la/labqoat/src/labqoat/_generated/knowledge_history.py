"""KnowledgeHistory"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat._generated.knowledge_revision import KnowledgeRevision
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class KnowledgeHistory:
    """KnowledgeHistory"""

    items: list[KnowledgeRevision]
    next_before: int | None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> KnowledgeHistory:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for KnowledgeHistory")
        return cls(
            items=[
                KnowledgeRevision.from_dict(JsonDocument.expect_dict(v))
                for v in JsonDocument.expect_list(values.get("items", []))
            ],
            next_before=JsonDocument.expect_optional_scalar(values.get("next_before"), int),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self, [("items", True, "list[KnowledgeRevision]", "KnowledgeRevision"), ("next_before", True, "int", "")]
        )
