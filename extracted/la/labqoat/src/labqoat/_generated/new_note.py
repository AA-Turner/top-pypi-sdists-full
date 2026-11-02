"""Submitted representation for creating a note."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class NewNote:
    """Submitted representation for creating a note."""

    title: str
    body: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> NewNote:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for NewNote")
        return cls(
            body=JsonDocument.expect_optional_scalar(values.get("body"), str),
            title=JsonDocument.expect_scalar(values["title"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(self, [("body", False, "str", ""), ("title", True, "str", "")])
