from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
    field,
)


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class SchemaId:
    name: Identifier


@dataclass(frozen=True)
class TableId:
    name: Identifier


@dataclass(frozen=True)
class ColumnId:
    name: Identifier


@dataclass(frozen=True)
class DbTableId:
    schema: SchemaId
    table: TableId


@dataclass(frozen=True)
class Identifier:
    """a.k.a. delimited identifier."""

    _private: _Private = field(repr=False, hash=False, compare=False)
    _inner: str

    @staticmethod
    def new(raw: str) -> Identifier:
        """To lower case + double quotes escaping."""
        escaped = raw.replace('"', '""')
        return Identifier(_Private(), escaped.lower())

    def to_str(self) -> str:
        return self._inner
