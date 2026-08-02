r"""Provide a DuckDB-backed store for records with optional typed
metadata schema."""

from __future__ import annotations

__all__ = ["TypedDuckDBRecordStore"]

import json
import logging
from typing import TYPE_CHECKING, Any

from zenpyre.record_stores.duckdb import BaseDuckDBRecordStore
from zenpyre.records import Record

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path

logger: logging.Logger = logging.getLogger(__name__)


class TypedDuckDBRecordStore(BaseDuckDBRecordStore):
    """A DuckDB-backed store for records with metadata filtering.

    Persists records to a DuckDB database and supports adding,
    retrieving, and filtering by metadata fields.  An optional
    ``metadata_schema`` maps known metadata field names to DuckDB
    types.  Known fields are stored as typed columns for fast,
    index-friendly queries.  Any metadata fields not in the schema are
    stored in an ``extra`` JSON overflow column, so nothing is lost.

    Args:
        path: Path to the DuckDB file, or ``":memory:"`` for an
            in-memory database (useful for testing).
        metadata_schema: Optional mapping of metadata field names to
            DuckDB type strings (e.g. ``{"ticker": "VARCHAR", "cik":
            "INTEGER", "year": "INTEGER"}``).  Fields in the schema get
            native typed columns; all other metadata fields go into the
            ``extra`` JSON overflow column.  Defaults to ``None``,
            which stores all metadata as JSON only.
        **kwargs: Additional keyword arguments to pass to ``duckdb.connect``.

    Example:
        ```pycon
        >>> from zenpyre.record_stores import TypedDuckDBRecordStore
        >>> from zenpyre.records import Record
        >>> schema = {"author": "VARCHAR", "year": "INTEGER", "category": "VARCHAR"}
        >>> store = TypedDuckDBRecordStore(":memory:", metadata_schema=schema)
        >>> records = [
        ...     Record(
        ...         id="1",
        ...         metadata={"author": "Alice", "year": 2022, "category": "Programming"},
        ...     ),
        ...     Record(
        ...         id="2",
        ...         metadata={"author": "Alice", "year": 2023, "category": "Programming"},
        ...     ),
        ...     Record(
        ...         id="3",
        ...         metadata={"author": "Bob", "year": 2021, "category": "History"},
        ...     ),
        ... ]
        >>> store.add_records(records)
        >>> len(store.filter(author="Alice"))
        2
        >>> len(store.filter(author="Alice", category="Programming"))
        2
        >>> len(store.filter(category="History"))
        1

        ```
    """

    def __init__(
        self,
        path: Path | str = ":memory:",
        metadata_schema: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(path, **kwargs)
        self._schema: dict[str, str] = metadata_schema or {}
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        if not self._kwargs.get("read_only", False):
            self._conn.execute(self._build_create_table())

    def add_records(self, records: list[Record]) -> None:
        if records:
            self._conn.executemany(
                self._build_insert(),
                [self._record_to_row(record) for record in records],
            )
        logger.info("Added %s records.", f"{len(records):,}")

    def get(self, record_id: str) -> Record | None:
        row = self._conn.execute("SELECT * FROM records WHERE id = ?", [record_id]).fetchone()
        return self._row_to_record(row) if row else None

    def get_many(self, record_ids: list[str]) -> list[Record | None]:
        placeholders = ", ".join("?" * len(record_ids))
        rows = self._conn.execute(
            f"SELECT * FROM records WHERE id IN ({placeholders})",  # noqa: S608
            record_ids,
        ).fetchall()
        by_id = {row[0]: self._row_to_record(row) for row in rows}
        return [by_id.get(record_id) for record_id in record_ids]

    def filter(self, **metadata_filters: Any) -> list[Record]:
        if not metadata_filters:
            return self.all()

        conditions, values = [], []
        for key, value in metadata_filters.items():
            if key in self._schema:
                conditions.append(f"{key} = ?")
            else:
                conditions.append(f"json_extract_string(extra, '$.{key}') = ?")
            values.append(value)

        where = " AND ".join(conditions)
        rows = self._conn.execute(
            f"SELECT * FROM records WHERE {where}",  # noqa: S608
            values,
        ).fetchall()
        return [self._row_to_record(row) for row in rows]

    def check_ids(self, record_ids: list[str]) -> tuple[list[str], list[str]]:
        if not record_ids:
            return [], []
        placeholders = ", ".join("?" * len(record_ids))
        existing = {
            row[0]
            for row in self._conn.execute(
                f"SELECT id FROM records WHERE id IN ({placeholders})",  # noqa: S608
                record_ids,
            ).fetchall()
        }
        found = [i for i in record_ids if i in existing]
        missing = [i for i in record_ids if i not in existing]
        return found, missing

    def all(self) -> list[Record]:
        rows = self._conn.execute("SELECT * FROM records").fetchall()
        return [self._row_to_record(row) for row in rows]

    def iter_batches(self, batch_size: int = 1000) -> Iterator[list[Record]]:
        if batch_size < 1:
            msg = f"batch_size must be a positive integer, got {batch_size}"
            raise ValueError(msg)

        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM records")
        while rows := cursor.fetchmany(batch_size):
            yield [self._row_to_record(row) for row in rows]

    # ---------------------------------------------------------------------------
    # Private helpers
    # ---------------------------------------------------------------------------

    def _build_create_table(self) -> str:
        """Build the CREATE TABLE statement from the schema."""
        typed_cols = "".join(f", {name} {dtype}" for name, dtype in self._schema.items())
        return (
            f"CREATE TABLE IF NOT EXISTS records (id VARCHAR PRIMARY KEY{typed_cols}, extra JSON)"
        )

    def _build_insert(self) -> str:
        """Build the INSERT OR REPLACE statement from the schema."""
        col_names = ["id", *self._schema.keys(), "extra"]
        placeholders = ", ".join("?" * len(col_names))
        return f"INSERT OR REPLACE INTO records ({', '.join(col_names)}) VALUES ({placeholders})"  # noqa: S608

    def _record_to_row(self, record: Record) -> tuple:
        """Convert a Record to an INSERT row tuple."""
        known = [record.metadata.get(k) for k in self._schema]
        extra = {k: v for k, v in record.metadata.items() if k not in self._schema}
        return (record.id, *known, json.dumps(extra) if extra else None)

    def _row_to_record(self, row: tuple) -> Record:
        """Convert a raw database row back to a Record."""
        # row layout: id, [schema cols...], extra
        record_id = row[0]
        schema_vals = dict(zip(self._schema.keys(), row[1 : 1 + len(self._schema)]))
        extra_json = row[1 + len(self._schema)]
        metadata = {k: v for k, v in schema_vals.items() if v is not None}
        if extra_json:
            metadata.update(json.loads(extra_json))
        return Record(id=record_id, metadata=metadata)
