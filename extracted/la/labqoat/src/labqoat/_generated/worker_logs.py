"""Sequenced log entries; identical replay succeeds, changed content conflicts."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class WorkerLogs:
    """Sequenced log entries; identical replay succeeds, changed content conflicts."""

    entries: list[JsonValue]

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> WorkerLogs:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for WorkerLogs")
        return cls(
            entries=list(JsonDocument.expect_list(values.get("entries", []))),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(self, [("entries", True, "list[JsonValue]", "JsonValue")])
