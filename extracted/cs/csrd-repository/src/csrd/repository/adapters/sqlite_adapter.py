from collections.abc import Sequence
from pathlib import Path
from typing import Any

import aiosqlite

from csrd.models import BaseModel
from csrd.models.model_parser import PayloadExtractor

from .._database_adapter import ABCDatabaseAdapter
from ..execute_result import ExecuteResult
from ..types import DBParams


class SQLiteExtractor(PayloadExtractor):
    def extract(self, source: Any) -> dict | list[dict]:
        """
        Extracts payload from raw SQLite rows. Assumes source is either:
        - A single row as a dict
        - A list of rows (each as a dict)
        - Already a dict/list
        """
        if isinstance(source, list):
            return [
                {key: row[key] for key in row.keys()}  # noqa: SIM118 — sqlite3.Row iterates values, not keys
                for row in source
                if hasattr(row, "keys")
            ]
        if hasattr(source, "keys") and hasattr(source, "__getitem__"):
            # Row-like object from SQLite with keys
            return {key: source[key] for key in source.keys()}  # noqa: SIM118
        if isinstance(source, tuple) and hasattr(source, "description"):
            # Raw cursor tuples with description - unsupported in this extractor
            raise ValueError("Raw tuples with description unsupported. Use dict_factory.")
        return dict(source)  # type: ignore[call-overload]


class SQLiteAdapter(ABCDatabaseAdapter):
    """Async SQLite adapter with a persistent connection.

    Use as an async context manager or call ``connect()`` / ``close()``
    explicitly::

        async with SQLiteAdapter("app.db") as db:
            row = await db.fetch_one("SELECT ...")

    The adapter opens a **single** ``aiosqlite`` connection and reuses it
    for all queries.  Call ``close()`` (or exit the context manager) when
    the application shuts down.
    """

    _db: aiosqlite.Connection | None

    def __init__(self, db_path: str | None = None, *, extractor: PayloadExtractor | None = None):
        """Initialise with a file path or ``:memory:`` (default)."""
        super().__init__(dsn=db_path or ":memory:", extractor=extractor or SQLiteExtractor())
        self._db = None

    # ── Lifecycle ────────────────────────────────────────────────────────

    async def connect(self) -> None:
        """Open the SQLite connection. Idempotent.

        Creates the parent directory for the database file if it does
        not already exist (skipped for ``:memory:`` databases).
        """
        if self._db is not None:
            return
        if self._dsn != ":memory:":
            Path(self._dsn).parent.mkdir(parents=True, exist_ok=True)
        self._db = await aiosqlite.connect(self._dsn)
        self._db.row_factory = aiosqlite.Row

    async def close(self) -> None:
        """Close the SQLite connection. Idempotent."""
        if self._db is not None:
            await self._db.close()
            self._db = None

    @property
    def _connection(self) -> aiosqlite.Connection:
        """Return the live connection or raise if not connected."""
        if self._db is None:
            raise RuntimeError(
                "SQLiteAdapter is not connected. "
                "Call await adapter.connect() or use 'async with adapter:'."
            )
        return self._db

    # ── Query interface ──────────────────────────────────────────────────

    async def fetch_one(self, query: str, params: DBParams = None) -> dict | None:
        """Fetch a single row and parse it via the extractor."""
        async with self._connection.execute(query, params or {}) as cursor:
            row = await cursor.fetchone()
            return self.extractor.extract(row) if row else None

    async def fetch_all(self, query: str, params: DBParams = None) -> Sequence[dict]:
        """Fetch multiple rows and parse them via the extractor."""
        async with self._connection.execute(query, params or {}) as cursor:
            rows = await cursor.fetchall()
            return list(self.extractor.extract(rows))  # type: ignore[arg-type]

    async def execute(self, query: str, params: DBParams = None) -> int:
        """Execute a DML statement and return the number of affected rows."""
        cursor = await self._connection.execute(query, params or {})
        await self._connection.commit()
        return cursor.rowcount

    async def execute_returning(self, query: str, params: DBParams = None) -> ExecuteResult:
        """Execute a statement and return an ``ExecuteResult`` snapshot."""
        cursor = await self._connection.execute(query, params or {})
        await self._connection.commit()
        return ExecuteResult(rowcount=cursor.rowcount, lastrowid=cursor.lastrowid)

    async def insert(
        self, table: str, values: dict[str, Any], *, model: type[BaseModel] | None = None
    ) -> Any:
        """Insert a row. Optionally return a model instance."""
        keys = ", ".join(values.keys())
        placeholders = ", ".join(f":{key}" for key in values)
        query = f"INSERT INTO {table} ({keys}) VALUES ({placeholders})"
        result = await self.execute_returning(query, values)

        last_id = result.lastrowid
        if model:
            return model(**{**values, "id": last_id})  # type: ignore[misc]
        values["id"] = last_id
        return values

    async def update(self, table: str, values: dict[str, Any], where: dict[str, Any]) -> int:
        """Update rows matching the WHERE condition."""
        set_clause = ", ".join(f"{key} = :{key}" for key in values)
        where_clause = " AND ".join(f"{key} = :where_{key}" for key in where)
        combined_params = {**values, **{f"where_{k}": v for k, v in where.items()}}
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        return await self.execute(query, combined_params)

    async def upsert(self, table: str, values: dict[str, Any], where: dict[str, Any]) -> int:
        """Atomic upsert via ``INSERT ... ON CONFLICT``.

        ``where`` keys identify the conflict target (unique columns).
        ``values`` contains the full row data to insert or update.
        """
        all_values = {**where, **values}
        keys = ", ".join(all_values.keys())
        placeholders = ", ".join(f":{k}" for k in all_values)
        conflict_cols = ", ".join(where.keys())

        # Columns to update on conflict (everything except the conflict keys)
        update_cols = [k for k in values if k not in where]

        if update_cols:
            set_clause = ", ".join(f"{k} = excluded.{k}" for k in update_cols)
            query = (
                f"INSERT INTO {table} ({keys}) VALUES ({placeholders}) "
                f"ON CONFLICT({conflict_cols}) DO UPDATE SET {set_clause}"
            )
        else:
            query = (
                f"INSERT INTO {table} ({keys}) VALUES ({placeholders}) "
                f"ON CONFLICT({conflict_cols}) DO NOTHING"
            )

        return await self.execute(query, all_values)

    async def delete(self, table: str, where: dict[str, Any]) -> int:
        """Delete rows matching the WHERE condition."""
        where_clause = " AND ".join(f"{key} = :{key}" for key in where)
        query = f"DELETE FROM {table} WHERE {where_clause}"
        return await self.execute(query, where)
