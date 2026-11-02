"""One bounded page of notes with pagination links."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat._generated.note import Note
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class NotePage:
    """One bounded page of notes with pagination links."""

    items: list[Note]
    links: Mapping[str, JsonValue]

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> NotePage:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for NotePage")
        return cls(
            items=[
                Note.from_dict(JsonDocument.expect_dict(v)) for v in JsonDocument.expect_list(values.get("items", []))
            ],
            links=JsonDocument.expect_dict(values["links"]),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self, [("items", True, "list[Note]", "Note"), ("links", True, "Mapping[str, JsonValue]", "")]
        )
