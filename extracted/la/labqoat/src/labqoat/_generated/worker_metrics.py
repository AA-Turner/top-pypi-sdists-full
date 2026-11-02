"""Step/name/value entries; identical replay succeeds, changed values conflict."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class WorkerMetrics:
    """Step/name/value entries; identical replay succeeds, changed values conflict."""

    entries: list[JsonValue]

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> WorkerMetrics:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for WorkerMetrics")
        return cls(
            entries=list(JsonDocument.expect_list(values.get("entries", []))),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(self, [("entries", True, "list[JsonValue]", "JsonValue")])
