"""A complete checkpoint manifest bound permanently to an attempt-owned operation key, independently of its step."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class WorkerCheckpoint:
    """A complete checkpoint manifest bound permanently to an attempt-owned operation key, independently of its step."""

    key: str
    manifest: Mapping[str, JsonValue]

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> WorkerCheckpoint:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for WorkerCheckpoint")
        return cls(
            key=JsonDocument.expect_scalar(values["key"], str),
            manifest=JsonDocument.expect_dict(values["manifest"]),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self, [("key", True, "str", ""), ("manifest", True, "Mapping[str, JsonValue]", "")]
        )
