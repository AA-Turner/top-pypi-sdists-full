import asyncio
import re
from collections.abc import Sequence
from importlib import import_module
from typing import Any, cast

from csrd.models.model_parser import PayloadExtractor

from .._database_adapter import ABCDatabaseAdapter
from ..execute_result import ExecuteResult

# Match :param_name but NOT ::type_cast (PostgreSQL cast syntax).
_NAMED_PARAM_RE = re.compile(r"(?<!:):([a-zA-Z_]\w*)")


def _normalize_query(query: str) -> str:
    """Convert ``:param`` style placeholders to ``%(param)s`` for psycopg."""
    return _NAMED_PARAM_RE.sub(r"%(\1)s", query)


class PGExtractor(PayloadExtractor):
    def extract(self, source: Any) -> dict | list[dict]:
        if isinstance(source, list):
            return [dict(row) for row in source]
        if source is None:
            return {}
        return dict(source)


class PGAdapter(ABCDatabaseAdapter):
    """Async Postgres adapter backed by psycopg connections in worker threads."""

    def __init__(self, *, host: str, port: int, user: str, password: str, database: str) -> None:
        super().__init__(
            dsn=f"postgresql://{user}:***@{host}:{port}/{database}",
            extractor=PGExtractor(),
        )
        psycopg = import_module("psycopg")
        dict_row = import_module("psycopg.rows").dict_row
        self._psycopg = psycopg
        self._dict_row = dict_row
        self._conninfo = (
            f"host={host} port={port} user={user} password={password} dbname={database}"
        )

    async def connect(self) -> None:
        return None

    async def close(self) -> None:
        return None

    async def fetch_one(self, query: str, params: dict[str, Any] | None = None) -> dict | None:
        return await asyncio.to_thread(self._fetch_one_sync, query, params)

    async def fetch_all(self, query: str, params: dict[str, Any] | None = None) -> Sequence[dict]:
        return await asyncio.to_thread(self._fetch_all_sync, query, params)

    async def execute(self, query: str, params: dict[str, Any] | None = None) -> int:
        return await asyncio.to_thread(self._execute_sync, query, params)

    async def execute_returning(
        self, query: str, params: dict[str, Any] | None = None
    ) -> ExecuteResult:
        rowcount, lastrowid = await asyncio.to_thread(self._execute_returning_sync, query, params)
        return ExecuteResult(rowcount=rowcount, lastrowid=lastrowid)

    async def insert(self, table: str, values: dict[str, Any]) -> Any:
        columns = ", ".join(values)
        placeholders = ", ".join(f"%({key})s" for key in values)
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        query_with_returning = f"{query} RETURNING id"
        undefined_column = getattr(getattr(self._psycopg, "errors", None), "UndefinedColumn", None)
        try:
            _rowcount, lastrowid = await asyncio.to_thread(
                self._execute_returning_sync, query_with_returning, values
            )
        except Exception as exc:
            # Some tables use custom primary keys (e.g. item_id) and don't expose an id column.
            has_undefined_column_error = isinstance(undefined_column, type) and isinstance(
                exc, undefined_column
            )
            if has_undefined_column_error or ('column "id" does not exist' in str(exc).lower()):
                await self.execute(query, values)
                return dict(values)
            raise
        return {**values, "id": lastrowid}

    async def update(self, table: str, values: dict[str, Any], where: dict[str, Any]) -> int:
        set_clause = ", ".join(f"{key} = %({key})s" for key in values)
        where_params = {f"where_{key}": value for key, value in where.items()}
        where_clause = " AND ".join(f"{key} = %(where_{key})s" for key in where)
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        return await self.execute(query, {**values, **where_params})

    async def upsert(self, table: str, values: dict[str, Any], where: dict[str, Any]) -> int:
        payload = {**where, **values}
        columns = ", ".join(payload)
        placeholders = ", ".join(f"%({key})s" for key in payload)
        conflict = ", ".join(where)
        updates = ", ".join(f"{key}=EXCLUDED.{key}" for key in values if key not in where)
        query = (
            f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) "
            f"ON CONFLICT ({conflict}) DO UPDATE SET {updates}"
        )
        return await self.execute(query, payload)

    async def delete(self, table: str, where: dict[str, Any]) -> int:
        where_clause = " AND ".join(f"{key} = %({key})s" for key in where)
        query = f"DELETE FROM {table} WHERE {where_clause}"
        return await self.execute(query, where)

    def _fetch_one_sync(self, query: str, params: dict[str, Any] | None) -> dict[str, Any] | None:
        with self._psycopg.connect(
            self._conninfo, row_factory=self._dict_row, autocommit=True
        ) as conn:
            row = conn.execute(_normalize_query(query), params or {}).fetchone()
            return cast(dict[str, Any] | None, row)

    def _fetch_all_sync(self, query: str, params: dict[str, Any] | None) -> list[dict[str, Any]]:
        with self._psycopg.connect(
            self._conninfo, row_factory=self._dict_row, autocommit=True
        ) as conn:
            return list(conn.execute(_normalize_query(query), params or {}).fetchall())

    def _execute_sync(self, query: str, params: dict[str, Any] | None) -> int:
        with self._psycopg.connect(
            self._conninfo, row_factory=self._dict_row, autocommit=True
        ) as conn:
            cursor = conn.execute(_normalize_query(query), params or {})
            return int(cursor.rowcount)

    def _execute_returning_sync(
        self, query: str, params: dict[str, Any] | None
    ) -> tuple[int, int | None]:
        """Execute a statement with an optional RETURNING clause.

        If the query contains a RETURNING clause the first column of the first
        returned row is used as ``lastrowid``.  Without RETURNING the cursor
        reports no rows and ``lastrowid`` is ``None``.
        """
        with self._psycopg.connect(
            self._conninfo, row_factory=self._dict_row, autocommit=True
        ) as conn:
            cursor = conn.execute(_normalize_query(query), params or {})
            rowcount = int(cursor.rowcount)
            try:
                row = cursor.fetchone()
                lastrowid = next(iter(row.values())) if row else None
            except Exception:
                lastrowid = None
            return rowcount, lastrowid


__all__ = ("PGAdapter", "PGExtractor")
