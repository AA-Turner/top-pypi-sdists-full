"""NewKnowledgeObjectives"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat._generated.knowledge_objective import KnowledgeObjective
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class NewKnowledgeObjectives:
    """NewKnowledgeObjectives"""

    idempotency_key: str
    objectives: list[KnowledgeObjective]

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> NewKnowledgeObjectives:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for NewKnowledgeObjectives")
        return cls(
            idempotency_key=JsonDocument.expect_scalar(values["idempotency_key"], str),
            objectives=[
                KnowledgeObjective.from_dict(JsonDocument.expect_dict(v))
                for v in JsonDocument.expect_list(values.get("objectives", []))
            ],
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("idempotency_key", True, "str", ""),
                ("objectives", True, "list[KnowledgeObjective]", "KnowledgeObjective"),
            ],
        )
