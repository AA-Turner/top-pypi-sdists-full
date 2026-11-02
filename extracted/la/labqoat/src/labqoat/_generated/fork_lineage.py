"""ForkLineage"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class ForkLineage:
    """ForkLineage"""

    actor: str
    id: str
    inherited_usage: Mapping[str, JsonValue]
    inserted_at: str
    reason: str
    run_id: str
    source_run_id: str
    source_state_version: int
    checkpoint_digest: str | None = None
    checkpoint_id: str | None = None
    source_definition_digest: str | None = None
    source_usage: Mapping[str, JsonValue] | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> ForkLineage:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for ForkLineage")
        return cls(
            actor=JsonDocument.expect_scalar(values["actor"], str),
            checkpoint_digest=JsonDocument.expect_optional_scalar(values.get("checkpoint_digest"), str),
            checkpoint_id=JsonDocument.expect_optional_scalar(values.get("checkpoint_id"), str),
            id=JsonDocument.expect_scalar(values["id"], str),
            inherited_usage=JsonDocument.expect_dict(values["inherited_usage"]),
            inserted_at=JsonDocument.expect_scalar(values["inserted_at"], str),
            reason=JsonDocument.expect_scalar(values["reason"], str),
            run_id=JsonDocument.expect_scalar(values["run_id"], str),
            source_definition_digest=JsonDocument.expect_optional_scalar(values.get("source_definition_digest"), str),
            source_run_id=JsonDocument.expect_scalar(values["source_run_id"], str),
            source_state_version=JsonDocument.expect_scalar(values["source_state_version"], int),
            source_usage=JsonDocument.expect_optional_dict(values.get("source_usage")),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("actor", True, "str", ""),
                ("checkpoint_digest", False, "str", ""),
                ("checkpoint_id", False, "str", ""),
                ("id", True, "str", ""),
                ("inherited_usage", True, "Mapping[str, JsonValue]", ""),
                ("inserted_at", True, "str", ""),
                ("reason", True, "str", ""),
                ("run_id", True, "str", ""),
                ("source_definition_digest", False, "str", ""),
                ("source_run_id", True, "str", ""),
                ("source_state_version", True, "int", ""),
                ("source_usage", False, "Mapping[str, JsonValue]", ""),
            ],
        )
