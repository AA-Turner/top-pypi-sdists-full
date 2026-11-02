"""KnowledgeStepBrief"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class KnowledgeStepBrief:
    """KnowledgeStepBrief"""

    body: str
    expected_version: int

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> KnowledgeStepBrief:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for KnowledgeStepBrief")
        return cls(
            body=JsonDocument.expect_scalar(values["body"], str),
            expected_version=JsonDocument.expect_scalar(values["expected_version"], int),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(self, [("body", True, "str", ""), ("expected_version", True, "int", "")])
