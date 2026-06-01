import asyncio
import re
from collections.abc import Sequence
from importlib import import_module
from typing import Any, cast

from csrd.models.model_parser import PayloadExtractor

from .._database_adapter import ABCDatabaseAdapter
from ..execute_result import ExecuteResult

# Match :param_name but NOT ::type_cast.
_NAMED_PARAM_RE = re.compile(r"(?<!:):([a-zA-Z_]\w*)")


def _normalize_query(query: str) -> str:
    """Convert ``:param`` style placeholders to ``%(param)s`` for pymysql."""
    return _NAMED_PARAM_RE.sub(r"%(\1)s", query)


class MariaExtractor(PayloadExtractor):
    def extract(self, source: Any) -> dict | list[dict]:
        if isinstance(source, list):
            return [dict(row) for row in source]
        if source is None:
            return {}
        return dict(source)


class MariaAdapter(ABCDatabaseAdapter):
    """Async MariaDB adapter backed by pymysql connections in worker threads."""

    def __init__(self, *, host: str, port: int, user: str, password: str, database: str) -> None:
        super().__init__(
            dsn=f"mysql://{user}:***@{host}:{port}/{database}",
            extractor=MariaExtractor(),
        )
        pymysql = import_module("pymysql")
        dict_cursor = import_module("pymysql.cursors").DictCursor
        self._pymysql = pymysql
        self._conn_kwargs = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database,
            "cursorclass": dict_cursor,
            "autocommit": True,
        }

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
        _rowcount, lastrowid = await asyncio.to_thread(self._execute_returning_sync, query, values)
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
        updates = ", ".join(f"{key}=VALUES({key})" for key in values)
        query = (
            f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) "
            f"ON DUPLICATE KEY UPDATE {updates}"
        )
        return await self.execute(query, payload)

    async def delete(self, table: str, where: dict[str, Any]) -> int:
        where_clause = " AND ".join(f"{key} = %({key})s" for key in where)
        query = f"DELETE FROM {table} WHERE {where_clause}"
        return await self.execute(query, where)

    def _fetch_one_sync(self, query: str, params: dict[str, Any] | None) -> dict[str, Any] | None:
        with self._pymysql.connect(**self._conn_kwargs) as conn, conn.cursor() as cur:
            cur.execute(_normalize_query(query), params or {})
            row = cur.fetchone()
            return cast(dict[str, Any] | None, row)

    def _fetch_all_sync(self, query: str, params: dict[str, Any] | None) -> list[dict[str, Any]]:
        with self._pymysql.connect(**self._conn_kwargs) as conn, conn.cursor() as cur:
            cur.execute(_normalize_query(query), params or {})
            return list(cur.fetchall())

    def _execute_sync(self, query: str, params: dict[str, Any] | None) -> int:
        with self._pymysql.connect(**self._conn_kwargs) as conn, conn.cursor() as cur:
            cur.execute(_normalize_query(query), params or {})
            return int(cur.rowcount)

    def _execute_returning_sync(
        self, query: str, params: dict[str, Any] | None
    ) -> tuple[int, int | None]:
        with self._pymysql.connect(**self._conn_kwargs) as conn, conn.cursor() as cur:
            cur.execute(_normalize_query(query), params or {})
            return int(cur.rowcount), cur.lastrowid


__all__ = ("MariaAdapter", "MariaExtractor")
