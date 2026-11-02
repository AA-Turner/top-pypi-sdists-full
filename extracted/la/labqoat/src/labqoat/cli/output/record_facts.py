"""The facts of a single resource, flattened one level for reading."""

from labqoat.cli.output.field_text import FieldText
from labqoat.cli.output.inferred_columns import InferredColumns
from labqoat.cli.output.view_column import ViewColumn
from labqoat.json_document import JsonValue


class RecordFacts:
    """Keep what describes a resource and leave links, digests, empties and deep structure to JSON output."""

    @classmethod
    def of(cls, document: dict[str, JsonValue]) -> tuple[ViewColumn, ...]:
        """Top-level scalars first by identity, then the scalar members of each nested object."""
        own = [name for name, value in document.items() if cls.shown(name, value) and not isinstance(value, dict)]
        nested = [
            f"{name}.{child}"
            for name, value in document.items()
            if isinstance(value, dict) and name != "links"
            for child, member in value.items()
            if cls.shown(child, member) and not isinstance(member, dict)
        ]
        ordered = sorted(own, key=InferredColumns.rank) + nested
        return tuple(ViewColumn(path, path, FieldText.kind(path.rsplit(".", 1)[-1])) for path in ordered)

    @staticmethod
    def shown(name: str, value: JsonValue) -> bool:
        """Present scalars and scalar lists are facts; lists of objects are rendered as tables elsewhere."""
        if name == "links" or value is None or value == "" or value == [] or value == {}:
            return False
        if isinstance(value, str) and value.startswith("sha256:"):
            return False
        return not (isinstance(value, list) and isinstance(value[0], (dict, list)))
