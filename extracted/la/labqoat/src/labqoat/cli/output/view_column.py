"""One labeled field of a resource, addressed by a dotted path."""

from dataclasses import dataclass

from labqoat.json_document import JsonValue


@dataclass(frozen=True)
class ViewColumn:
    """Name a field, where it lives in the document, and the role that decides its formatting."""

    header: str
    path: str
    kind: str = "text"
    optional: bool = False  # dropped from a table where no row has a value

    def shown(self, rows: list[JsonValue]) -> bool:
        """Whether a table of these rows keeps the column."""
        return not self.optional or any(self.value(row) not in (None, "") for row in rows)

    def value(self, document: JsonValue) -> JsonValue:
        """Follow the path through nested objects; anything missing reads as absent."""
        current = document
        for part in self.path.split("."):
            if not isinstance(current, dict):
                return None
            current = current.get(part)
        return current
