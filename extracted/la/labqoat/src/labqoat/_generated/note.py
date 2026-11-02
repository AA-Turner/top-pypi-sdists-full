"""A persisted example note with navigation links."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from labqoat._generated.emitter_helpers import EmitterHelpers
from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class Note:
    """A persisted example note with navigation links."""

    created_at: str
    id: str
    links: Mapping[str, JsonValue]
    title: str
    updated_at: str
    body: str | None = None

    @classmethod
    def from_dict(cls, values: Mapping[str, JsonValue]) -> Note:
        """Build a model from decoded JSON."""
        if not isinstance(values, dict):
            raise TypeError("expected a JSON object for Note")
        return cls(
            body=JsonDocument.expect_optional_scalar(values.get("body"), str),
            created_at=JsonDocument.expect_scalar(values["created_at"], str),
            id=JsonDocument.expect_scalar(values["id"], str),
            links=JsonDocument.expect_dict(values["links"]),
            title=JsonDocument.expect_scalar(values["title"], str),
            updated_at=JsonDocument.expect_scalar(values["updated_at"], str),
        )

    def to_dict(self) -> JsonDocument:
        """Encode the model, omitting unset optional values."""
        return EmitterHelpers.encode_model(
            self,
            [
                ("body", False, "str", ""),
                ("created_at", True, "str", ""),
                ("id", True, "str", ""),
                ("links", True, "Mapping[str, JsonValue]", ""),
                ("title", True, "str", ""),
                ("updated_at", True, "str", ""),
            ],
        )
