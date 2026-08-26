from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatchcase


def _schema_name(table_ref: str) -> str:
    # A warehouse name may contain dots; schema and table names may not, which is
    # why `APIDriver._table_ref_parts` also splits from the right.
    return table_ref.rsplit(".", 2)[-2]


def _matches_pattern(table_ref: str, pattern: str) -> bool:
    # A partial pattern is anchored at the end of the ref, so `fact_*` matches any
    # table whose name starts with `fact_` while a fully qualified pattern still
    # works. `fnmatchcase`, not `fnmatch`: the latter normcases its arguments, so
    # the same pattern would match case-insensitively on macOS only.
    return fnmatchcase(table_ref, pattern) or fnmatchcase(table_ref, f"*.{pattern}")


@dataclass(frozen=True)
class TableFilters:
    """Which tables `pull` enumerates when no table refs are given on the command line."""

    configured_only: bool = False
    schemas: tuple[str, ...] = ()
    table_labels: tuple[str, ...] = ()
    table_pattern: str | None = None
    warehouse_id: int | None = None

    @property
    def applied_flags(self) -> list[str]:
        """Flags the caller actually set, for error messages."""
        flags = []
        if self.configured_only:
            flags.append("--configured_only")
        if self.schemas:
            flags.append("--schemas")
        if self.table_labels:
            flags.append("--table_labels")
        if self.table_pattern:
            flags.append("--table_pattern")
        if self.warehouse_id is not None:
            flags.append("--warehouse_id")
        return flags

    def matches_ref(self, table_ref: str) -> bool:
        """Whether a `warehouse.schema.table` ref survives the client-side filters."""
        if self.schemas and _schema_name(table_ref) not in self.schemas:
            return False
        return not (
            self.table_pattern and not _matches_pattern(table_ref, self.table_pattern)
        )
