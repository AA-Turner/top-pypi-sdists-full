"""Immutable checkpoint manifest with captured metadata schema, exact compute execution and opaque payload identity."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class Checkpoint:
    """Immutable checkpoint manifest with captured metadata schema, exact compute execution and opaque payload identity."""

    id: str
    manifest: Mapping[str, JsonValue]
    manifest_digest: str
    run_id: str
    step: int
    attempt_id: str | None = None
    cycle_number: int | None = None
    fence: int | None = None
    inserted_at: str | None = None
    lineage_id: str | None = None
    recovery_role: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> Checkpoint:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for Checkpoint")
        return cls(
            attempt_id=JsonDocument.expect_optional_scalar(values.get("attempt_id"), str),
            cycle_number=JsonDocument.expect_optional_scalar(values.get("cycle_number"), int),
            fence=JsonDocument.expect_optional_scalar(values.get("fence"), int),
            id=JsonDocument.expect_scalar(values["id"], str),
            inserted_at=JsonDocument.expect_optional_scalar(values.get("inserted_at"), str),
            lineage_id=JsonDocument.expect_optional_scalar(values.get("lineage_id"), str),
            manifest=JsonDocument.expect_dict(values["manifest"]),
            manifest_digest=JsonDocument.expect_scalar(values["manifest_digest"], str),
            recovery_role=JsonDocument.expect_optional_scalar(values.get("recovery_role"), str),
            run_id=JsonDocument.expect_scalar(values["run_id"], str),
            step=JsonDocument.expect_scalar(values["step"], int),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("attempt_id", False, "str", ""),
                ("cycle_number", False, "int", ""),
                ("fence", False, "int", ""),
                ("id", True, "str", ""),
                ("inserted_at", False, "str", ""),
                ("lineage_id", False, "str", ""),
                ("manifest", True, "Mapping[str, JsonValue]", ""),
                ("manifest_digest", True, "str", ""),
                ("recovery_role", False, "str", ""),
                ("run_id", True, "str", ""),
                ("step", True, "int", ""),
            ],
        )
