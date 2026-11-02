"""Pinned manifest and fence for one assignment."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class WorkerInputs:
    """Pinned manifest and fence for one assignment."""

    fence: int
    manifest: Mapping[str, JsonValue]
    run_id: str
    arguments: Mapping[str, JsonValue] | None = None
    capabilities: list[JsonValue] | None = field(default_factory=list)
    recovery: Mapping[str, JsonValue] | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> WorkerInputs:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for WorkerInputs")
        return cls(
            arguments=JsonDocument.expect_optional_dict(values.get("arguments")),
            capabilities=list(JsonDocument.expect_list(values.get("capabilities", []))),
            fence=JsonDocument.expect_scalar(values["fence"], int),
            manifest=JsonDocument.expect_dict(values["manifest"]),
            recovery=JsonDocument.expect_optional_dict(values.get("recovery")),
            run_id=JsonDocument.expect_scalar(values["run_id"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("arguments", False, "Mapping[str, JsonValue]", ""),
                ("capabilities", False, "list[JsonValue]", "JsonValue"),
                ("fence", True, "int", ""),
                ("manifest", True, "Mapping[str, JsonValue]", ""),
                ("recovery", False, "Mapping[str, JsonValue]", ""),
                ("run_id", True, "str", ""),
            ],
        )
