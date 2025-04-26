from __future__ import annotations

import functools
from datetime import timedelta
from typing import Any

import orjson
import sqlalchemy
import sqlalchemy.pool
import sqlalchemy.sql.sqltypes
from sqlalchemy import ARRAY, BINARY, TEXT, VARBINARY, VARCHAR, Interval, LargeBinary, String, Text
from sqlalchemy.engine import Dialect
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import ColumnElement
from sqlalchemy.sql.type_api import NativeForEmulated, TypeEngine
from sqlalchemy_redshift.dialect import SUPER as RedshiftSuper
from sqlalchemy_redshift.dialect import RedshiftDialectMixin, RedshiftTypeCompiler, RedshiftTypeEngine


def _compile_array(element: ARRAY, compiler: RedshiftTypeCompiler, **kw: Any):
    return "SUPER"


class RedshiftBinary(RedshiftTypeEngine):
    """Redshift binary needs to be decoded via bytes.fromhex, and we want to default to a much large size"""

    __visit_name__ = "VARBINARY"

    @property
    def python_type(self):
        return bytes

    def __init__(self, length: int | None = None):
        super().__init__()
        self.length = length

    def as_generic(self, allow_nulltype: bool = True) -> TypeEngine[Any]:
        return LargeBinary(self.length)

    def get_dbapi_type(self, dbapi: Any):
        return dbapi.VARBINARY

    def compile(self, dialect: Dialect | None = None) -> Any:
        length = self.length
        if length is None:
            # By default, redshift creates binary columns that are 64K wide
            # That is too small, instead going to default it to the max
            # See https://docs.aws.amazon.com/redshift/latest/dg/r_VARBYTE_type.html
            length = 1024000
        return f"VARBINARY({length})"

    def result_processor(self, dialect: Dialect, coltype: ColumnElement):
        return lambda val: None if val is None else bytes.fromhex(val)


def _compile_binary(element: BINARY | LargeBinary | VARBINARY, compiler: RedshiftTypeCompiler, **kw: Any):
    length = element.length
    if length is None:
        length = 1_024_000
    return f"VARBINARY({length})"


def _compile_varchar(element: VARCHAR | String | Text | TEXT, compiler: RedshiftTypeCompiler, **kw: Any):
    length = element.length
    if length is None:
        length = 65535
    return f"VARCHAR({length})"


class SUPER(RedshiftTypeEngine):
    """
    Redshift defines a SUPER column type
    https://docs.aws.amazon.com/redshift/latest/dg/c_Supported_data_types.html

    Adding an explicit type to the RedshiftDialect allows us follow the
    SqlAlchemy conventions for "vendor-specific types."

    https://docs.sqlalchemy.org/en/13/core/type_basics.html#vendor-specific-types
    """

    __visit_name__ = "SUPER"

    def get_dbapi_type(self, dbapi: Any):
        return dbapi.SUPER

    def bind_expression(self, bindvalue: ColumnElement):
        # Parse the json string into the super value
        return sqlalchemy.func.json_parse(bindvalue)

    def bind_processor(self, dialect: Dialect):
        # Convert any python values into a json string when serializing
        # Using orjson instead of json for performance and to coerce nan/+inf/-inf to null values
        return lambda x: orjson.dumps(x).decode("utf8")

    def result_processor(self, dialect: Dialect, coltype: Any):
        def _result_processor(val: str | None):
            if val is None:
                return None
            return orjson.loads(val)

        return _result_processor


class INTERVAL(NativeForEmulated, sqlalchemy.sql.sqltypes._AbstractInterval):  # pyright: ignore[reportPrivateUsage]
    __visit_name__ = "INTERVAL"
    native = True

    @property
    def python_type(self):
        return timedelta

    @classmethod
    def adapt_emulated_to_native(cls, impl: Interval, **kw: Any):
        return cls()

    @property
    def _type_affinity(self):
        return Interval

    def as_generic(self, allow_nulltype: bool = False):
        return Interval(native=True)

    def coerce_compared_value(self, op: Any, value: Any):
        return self


@functools.lru_cache(None)
def register_redshift_compiler_hooks():
    """
    Parameters
    ----------
    :param backup_default: Default value for the `backup YES | NO` when creating a table, if the `redshift_backup` argument is not specified in the table
    constructor
    """
    colspecs = dict(RedshiftDialectMixin.colspecs)
    colspecs[ARRAY] = SUPER
    # Our super is more super than their super ;)
    colspecs[RedshiftSuper] = SUPER
    colspecs[Interval] = INTERVAL
    colspecs[LargeBinary] = RedshiftBinary
    colspecs[BINARY] = RedshiftBinary
    colspecs[VARBINARY] = RedshiftBinary
    RedshiftDialectMixin.colspecs = colspecs
    compiles(ARRAY, "redshift")(_compile_array)
    compiles(LargeBinary, "redshift")(_compile_binary)
    compiles(BINARY, "redshift")(_compile_binary)
    compiles(VARBINARY, "redshift")(_compile_binary)
    compiles(VARCHAR, "redshift")(_compile_varchar)
    compiles(String, "redshift")(_compile_varchar)
    compiles(Text, "redshift")(_compile_varchar)
    compiles(TEXT, "redshift")(_compile_varchar)
