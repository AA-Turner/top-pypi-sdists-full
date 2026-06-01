from collections.abc import Sequence
from typing import Any

from fastapi import HTTPException

from csrd.models.model_parser import ModelParserMixin
from csrd.models.model_parser._types import ResponseModelType

from ._database_adapter import DBProtocol
from .types import DBQuery


def _compile(query: DBQuery, params: dict[str, Any] | None) -> tuple[str, dict[str, Any] | None]:
    """Convert a query (raw SQL *or* SQLAlchemy Executable) into (sql_string, params)."""
    if isinstance(query, str):
        return query, params

    # SQLAlchemy Executable — compile to SQL + extract bound params
    compiled = query.compile(compile_kwargs={"literal_binds": False})
    sql = str(compiled)
    compiled_params = dict(compiled.params) if compiled.params else {}
    if params:
        compiled_params.update(params)
    return sql, compiled_params or None


class BaseRepository(ModelParserMixin):
    _adapter: DBProtocol

    def __init__(self, adapter: DBProtocol):
        if adapter is None:
            raise TypeError("BaseRepository requires a database adapter — got None")
        self._adapter = adapter
        super().__init__(extractor=self._adapter.extractor)

    @property
    def extract(self):
        return self._adapter.extractor.extract

    async def fetch_one(self, query: DBQuery, params: dict[str, Any] | None = None) -> Any | None:
        sql, resolved = _compile(query, params)
        raw = await self._adapter.fetch_one(sql, resolved)
        return self._resolve_payload(raw)

    async def require_one(
        self,
        query: DBQuery,
        params: dict[str, Any] | None = None,
        *,
        model: ResponseModelType | None = None,
        status_code: int = 404,
        detail: str = "Not found",
    ) -> Any:
        """Fetch a single row and raise if not found.

        Combines ``fetch_one``, not-found guard, and optional model
        parsing in a single call — the repository equivalent of the
        delegate's ``_parse_status_code`` + ``apply_model`` chain.

        Args:
            query: SQL query or SQLAlchemy Executable.
            params: Query parameters.
            model: Optional Pydantic model to parse the row into.
            status_code: HTTP status code to raise when the row is ``None``.
            detail: Error detail message.

        Returns:
            The parsed model instance, or the raw extracted dict if
            *model* is ``None``.

        Raises:
            HTTPException: When the query returns no rows.
        """
        row = await self.fetch_one(query, params)
        if row is None:
            raise HTTPException(status_code=status_code, detail=detail)
        if model is not None:
            return self.apply_model(row, model=model)
        return row

    async def fetch_all(
        self, query: DBQuery, params: dict[str, Any] | None = None
    ) -> Sequence[Any]:
        sql, resolved = _compile(query, params)
        raw = await self._adapter.fetch_all(sql, resolved)
        result = self._resolve_payload(raw)
        return list(result) if isinstance(result, (list, tuple)) else [result]

    async def require_any(
        self,
        query: DBQuery,
        params: dict[str, Any] | None = None,
        *,
        model: ResponseModelType | None = None,
        status_code: int = 404,
        detail: str = "Not found",
    ) -> Sequence[Any]:
        """Fetch rows and raise if none are returned.

        Combines ``fetch_all``, empty-guard, and optional model parsing.
        Useful when an empty result set indicates a missing parent entity.

        Args:
            query: SQL query or SQLAlchemy Executable.
            params: Query parameters.
            model: Optional ``list[Model]`` to parse each row into.
            status_code: HTTP status code to raise when no rows are found.
            detail: Error detail message.

        Returns:
            A list of parsed model instances, or raw extracted dicts
            if *model* is ``None``.

        Raises:
            HTTPException: When the query returns no rows.
        """
        rows = await self.fetch_all(query, params)
        if not rows:
            raise HTTPException(status_code=status_code, detail=detail)
        if model is not None:
            result = self.apply_model(rows, model=model)
            return result if isinstance(result, list) else [result]
        return rows

    async def execute(self, query: DBQuery, params: dict[str, Any] | None = None) -> Any:
        sql, resolved = _compile(query, params)
        return await self._adapter.execute(sql, resolved)

    async def execute_returning(self, query: DBQuery, params: dict[str, Any] | None = None) -> Any:
        sql, resolved = _compile(query, params)
        return await self._adapter.execute_returning(sql, resolved)

    async def insert(self, table: str, values: dict[str, Any], *args, **kwargs) -> Any:
        return await self._adapter.insert(table, values, *args, **kwargs)

    async def update(self, table: str, values: dict[str, Any], where: dict[str, Any]) -> int:
        return await self._adapter.update(table, values, where)

    async def upsert(self, table: str, values: dict[str, Any], where: dict[str, Any]) -> int:
        return await self._adapter.upsert(table, values, where)

    async def delete(self, table: str, where: dict[str, Any]) -> int:
        return await self._adapter.delete(table, where)
