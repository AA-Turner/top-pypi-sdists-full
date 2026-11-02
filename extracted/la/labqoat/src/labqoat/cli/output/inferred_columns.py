"""Columns for a resource list that has no curated view."""

from typing import ClassVar

from labqoat.cli.output.field_text import FieldText
from labqoat.cli.output.view_column import ViewColumn
from labqoat.json_document import JsonValue


class InferredColumns:
    """Pick the scalar fields that identify a row, most telling first, and leave bulk to JSON output."""

    leading: ClassVar[tuple[str, ...]] = (
        "id",
        "name",
        "status",
        "state",
        "kind",
        "app",
        "project",
        "region",
        "location_id",
    )
    limit = 8

    @classmethod
    def of(cls, rows: list[JsonValue]) -> tuple[ViewColumn, ...]:
        """Use fields that hold a short scalar somewhere in the page, identity first and instants last."""
        names: dict[str, None] = {}
        for row in rows:
            if isinstance(row, dict):
                names.update(dict.fromkeys(name for name, value in row.items() if cls.telling(value)))
        ordered = sorted(names, key=cls.rank)[: cls.limit]
        return tuple(ViewColumn(name.replace("_", " ").upper(), name, FieldText.kind(name)) for name in ordered)

    @classmethod
    def rank(cls, name: str) -> tuple[int, int]:
        """Known identity fields in their fixed order, then other fields, then instants."""
        if name in cls.leading:
            return (0, cls.leading.index(name))
        return (2, 0) if name.endswith("_at") else (1, 0)

    @staticmethod
    def telling(value: JsonValue) -> bool:
        """Short present scalars describe a row; digests, long text and nested data do not."""
        if value is None or isinstance(value, (dict, list)):
            return False
        text = str(value)
        return len(text) <= 60 and not text.startswith("sha256:")
