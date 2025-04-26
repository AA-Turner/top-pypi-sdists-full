from __future__ import annotations

import datetime
import functools
from typing import Any

import orjson
import sqlalchemy as sa
from snowflake.sqlalchemy import ARRAY, OBJECT
from snowflake.sqlalchemy.base import SnowflakeCompiler, SnowflakeDDLCompiler, SnowflakeTypeCompiler
from snowflake.sqlalchemy.snowdialect import TIMESTAMP_LTZ, TIMESTAMP_NTZ, TIMESTAMP_TZ, SnowflakeDialect
from sqlalchemy.engine import Dialect
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import CreateIndex, DropIndex
from sqlalchemy.sql import functions  # noqa # pyright thinks this doesn't exist
from sqlalchemy.sql.functions import AnsiFunction
from sqlalchemy.sql.sqltypes import DATETIME, TIMESTAMP
from sqlalchemy.sql.type_api import NativeForEmulated
from sqlalchemy.types import TypeEngine

from chalk.utils.collections import get_unique_item


def _datetime_bind_processor(self: TypeEngine, dialect: Dialect):
    def _processor(val: datetime.datetime | None):
        if val is None:
            return None
        return _format_datetime_as_iso(val)

    return _processor


class IntervalType(NativeForEmulated, TypeEngine):
    __visit_name__ = "INTERVAL"
    native = True

    @property
    def python_type(self):
        return datetime.timedelta

    def compile(self, dialect: Dialect | None = None):
        return "INTERVAL"

    def as_generic(self, allow_nulltype: bool = True) -> TypeEngine[Any]:
        return sa.Interval(native=True)

    def bind_expression(self, bindvalue: Any) -> Any:
        return sa.func.interval(bindvalue)

    def bind_processor(self, dialect: Dialect):
        def _processor(val: datetime.timedelta | None):
            assert isinstance(val, datetime.timedelta), "intervals must be timedeltas"
            if val < datetime.timedelta(0):
                raise ValueError(
                    (
                        f"Interval '{val}' is negative, which is not supported on snowflake. "
                        "Instead, please modify the query to subtract a positive internal instead of adding a negative interval."
                    )
                )
            parts: list[str] = []
            parts.append(f"{val.days} d")
            if val.seconds > 0:
                parts.append(f"{val.seconds} s")
            if val.microseconds > 0:
                parts.append(f"{val.microseconds} us")
            return ", ".join(parts)

        return _processor


class interval(AnsiFunction):
    inherit_cache = True


def _compile_interval_func(element: interval, compiler: SnowflakeCompiler, **kw: Any):
    clause = get_unique_item(element.clauses.clauses)
    return f"interval {compiler.process(clause, **kw)}"


def _compile_interval(element: IntervalType, compiler: SnowflakeTypeCompiler, **kw: Any):
    return "INTERVAL"


def _compile_func_now(element: functions.now, compiler: SnowflakeCompiler, **kw: Any):
    return "CURRENT_TIMESTAMP()"


def _compile_create_index(element: CreateIndex, compiler: SnowflakeDDLCompiler, **kw: Any):
    # Snowflake does not support indexing
    return "SELECT 1"


def _compile_drop_index(element: DropIndex, compiler: SnowflakeDDLCompiler, **kw: Any):
    # Snowflake does not support indexing
    return "SELECT 1"


def _compile_datetime(element: sa.DateTime | sa.TIMESTAMP | sa.DATETIME, compiler: SnowflakeTypeCompiler, **kw: Any):
    if element.timezone:
        return "TIMESTAMP_TZ"
    else:
        return "TIMESTAMP_NTZ"


class ArrayType(ARRAY):
    def get_dbapi_type(self, dbapi: Any):
        return dbapi.ARRAY

    def bind_processor(self, dialect: Dialect, **kw: Any):
        # Convert any python values into a json string when serializing
        # Using orjson instead of json for performance and to coerce nan/+inf/-inf to null values
        return lambda x: orjson.dumps(x).decode("utf8")

    def result_processor(self, dialect: Dialect, coltype: Any):
        def _result_processor(val: str | None):
            if val is None:
                return None
            return orjson.loads(val)

        return _result_processor


class ObjectType(OBJECT):
    def get_dbapi_type(self, dbapi: Any):
        return dbapi.OBJECT

    def bind_processor(self, dialect: Dialect, **kw: Any):
        # Convert any python values into a json string when serializing
        # Using orjson instead of json for performance and to coerce nan/+inf/-inf to null values
        return lambda x: orjson.dumps(x).decode("utf8")

    def result_processor(self, dialect: Dialect, coltype: Any):
        def _result_processor(val: str | None):
            if val is None:
                return None
            return orjson.loads(val)

        return _result_processor


def _format_datetime_as_iso(val: datetime.datetime):
    """Format a datetime as standardized ISO string, independent of platform"""
    # See https://bugs.python.org/issue13305 -- `datetime.datetime.min.isoformat()` is incorrect on linux
    # It returns 1-01-01T00:00:00 instead of 0001-01-01T00:00:00
    time_format = val.time().isoformat()
    return f"{val.year:04d}-{val.month:02d}-{val.day:02d}T{time_format}"


@functools.lru_cache(None)
def register_snowflake_compiler_hooks():
    colspecs = dict(SnowflakeDialect.colspecs)
    colspecs[sa.ARRAY] = ArrayType
    colspecs[ARRAY] = ArrayType
    colspecs[sa.Interval] = IntervalType
    colspecs[DATETIME] = TIMESTAMP_NTZ
    colspecs[TIMESTAMP] = TIMESTAMP_TZ
    TIMESTAMP_NTZ.bind_processor = _datetime_bind_processor
    TIMESTAMP_TZ.bind_processor = _datetime_bind_processor
    TIMESTAMP_LTZ.bind_processor = _datetime_bind_processor
    colspecs[OBJECT] = ObjectType
    SnowflakeDialect.colspecs = colspecs
    compiles(CreateIndex, "snowflake")(_compile_create_index)
    compiles(DropIndex, "snowflake")(_compile_drop_index)
    compiles(IntervalType, "snowflake")(_compile_interval)
    compiles(sa.DateTime, "snowflake")(_compile_datetime)
    compiles(sa.TIMESTAMP, "snowflake")(_compile_datetime)
    compiles(sa.DATETIME, "snowflake")(_compile_datetime)
    compiles(interval, "snowflake")(_compile_interval_func)
    compiles(functions.now, "snowflake")(_compile_func_now)
