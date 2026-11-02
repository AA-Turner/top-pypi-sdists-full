"""What to show for one endpoint document: a table of rows, a set of facts, or both."""

from dataclasses import dataclass

from labqoat.cli.output.inferred_columns import InferredColumns
from labqoat.cli.output.record_facts import RecordFacts
from labqoat.cli.output.view_catalog import ViewCatalog
from labqoat.cli.output.view_column import ViewColumn
from labqoat.json_document import JsonValue


@dataclass(frozen=True)
class ResourceView:
    """Separate a document's collection from the facts around it, independent of how either is drawn."""

    rows: list[JsonValue] | None
    columns: tuple[ViewColumn, ...]
    record: dict[str, JsonValue]
    facts: tuple[ViewColumn, ...]

    @classmethod
    def of(cls, document: JsonValue, command: str) -> "ResourceView":
        """A page lists its items; any other object is one record; remaining scalars stay as facts."""
        if isinstance(document, list):
            return cls.table(document, {}, command)
        if not isinstance(document, dict):
            return cls(None, (), {"value": document}, (ViewColumn("value", "value"),))
        name = cls.collection(document)
        if name is None:
            return cls(None, (), document, RecordFacts.of(document))
        rest = {key: value for key, value in document.items() if key != name}
        rows = document[name]
        return cls.table(rows if isinstance(rows, list) else [], rest, command)

    @classmethod
    def table(cls, rows: list[JsonValue], rest: dict[str, JsonValue], command: str) -> "ResourceView":
        """Prefer the curated columns of a known command when they fit the rows, and infer them otherwise."""
        columns = cls.fitting(ViewCatalog.columns(command), rows) or InferredColumns.of(rows)
        return cls(rows, tuple(column for column in columns if column.shown(rows)), rest, RecordFacts.of(rest))

    @staticmethod
    def fitting(columns: tuple[ViewColumn, ...] | None, rows: list[JsonValue]) -> tuple[ViewColumn, ...] | None:
        """Curated columns, unless no row holds their leading identity field (a different document shape)."""
        if columns is None or not rows:
            return columns
        return columns if any(columns[0].value(row) is not None for row in rows) else None

    @staticmethod
    def collection(document: dict[str, JsonValue]) -> str | None:
        """The page's ``items``, or the one list of objects in a document that is not itself a resource."""
        if isinstance(document.get("items"), list):
            return "items"
        if "id" in document:
            return None
        lists = [
            name for name, value in document.items() if isinstance(value, list) and value and isinstance(value[0], dict)
        ]
        return lists[0] if len(lists) == 1 else None
