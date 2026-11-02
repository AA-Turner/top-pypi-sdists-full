"""JSON Merge Patch document with omitted-versus-null tracking."""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field as dataclass_field

from labqoat.json_document import JsonDocument, JsonValue


@dataclass
class NotePatch:
    """Partial note change. Missing fields are preserved."""

    values: dict[str, JsonValue] = dataclass_field(default_factory=dict)

    @classmethod
    def empty(cls) -> NotePatch:
        """Build a patch that changes nothing."""
        return cls(values={})

    @classmethod
    def with_title(cls, title: str) -> NotePatch:
        """Build a patch that sets the title."""
        return cls(values={"title": title})

    @classmethod
    def with_body(cls, body: str | None) -> NotePatch:
        """Build a patch that sets or clears the body."""
        return cls(values={"body": body})

    def merge(self, other: NotePatch) -> NotePatch:
        """Combine two patches, with the other winning."""
        combined = dict(self.values)
        combined.update(other.values)
        return NotePatch(values=combined)

    def to_dict(self) -> JsonDocument:
        """Encode only explicitly set fields."""
        return JsonDocument(self.values)
