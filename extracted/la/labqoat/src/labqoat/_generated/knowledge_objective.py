"""KnowledgeObjective"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class KnowledgeObjective:
    """KnowledgeObjective"""

    direction: str
    metric: str
    require: Mapping[str, JsonValue] | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> KnowledgeObjective:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for KnowledgeObjective")
        return cls(
            direction=JsonDocument.expect_scalar(values["direction"], str),
            metric=JsonDocument.expect_scalar(values["metric"], str),
            require=JsonDocument.expect_optional_dict(values.get("require")),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("direction", True, "str", ""),
                ("metric", True, "str", ""),
                ("require", False, "Mapping[str, JsonValue]", ""),
            ],
        )
