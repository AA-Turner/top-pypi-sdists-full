"""Defines a general sqlalchemy function for uuid."""

from typing import Any

from sqlalchemy import sql
from sqlalchemy.ext.compiler import (
    compiles,  # pyright: ignore[reportUnknownVariableType]
)
from sqlalchemy.types import UUID


class UUIDFunction(sql.expression.FunctionElement[Any]):
    """Adds a uuid() expression based on backend db used.

    Implementation follows from documentation from sqlalchemy source at
    sqlalchemy/ext/compiler.py.
    """

    type = UUID()
    inherit_cache = True


@compiles(UUIDFunction, "postgresql")
def pg_uuid(
    element: sql.expression.FunctionElement[Any],
    compiler: sql.compiler.SQLCompiler,
    **kw: Any,
):
    # https://www.postgresql.org/docs/current/functions-uuid.html
    return "gen_random_uuid()"


@compiles(UUIDFunction)
def default_sql_uuid(
    element: sql.expression.FunctionElement[Any],
    compiler: sql.compiler.SQLCompiler,
    **kw: Any,
):
    raise NotImplementedError()


@compiles(UUIDFunction, "sqlite")
def sqlite_uuid(
    element: sql.expression.FunctionElement[Any],
    compiler: sql.compiler.SQLCompiler,
    **kw: Any,
):
    return "lower(hex(randomblob(16)))"
