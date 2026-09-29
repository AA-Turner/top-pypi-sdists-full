"""
pysqlsync: Synchronize schema and large volumes of data.

Copyright 2023-2026, Levente Hunyadi; 2026 Instructure, Inc.

:see: https://github.com/instructure-internal/pysqlsync
"""

import enum
from dataclasses import dataclass
from typing import Any, Optional

import pyodbc
from strong_typing.auxiliary import MaxLength

from pysqlsync.model.data_types import (
    SqlBooleanType,
    SqlDataType,
    SqlDateType,
    SqlDecimalType,
    SqlDoubleType,
    SqlFixedBinaryType,
    SqlFixedCharacterType,
    SqlFloatType,
    SqlIntegerType,
    SqlRealType,
    SqlTimestampType,
    SqlTimeType,
    SqlVariableBinaryType,
    SqlVariableCharacterType,
)


class MSSQLBooleanType(SqlBooleanType):
    def __str__(self) -> str:
        return "bit"

    def value_to_sql_literal(self, value: Any) -> str:
        if not isinstance(value, bool):
            raise TypeError(f"expected: value of type `bool`, got: {type(value)}")

        return "1" if value else "0"


# `varchar(n)` holds n bytes; `nvarchar(n)` holds n UTF-16 code units. Beyond
# these maxima only the `(max)` form is valid.
MAX_VARCHAR_SIZE = 8000
MAX_NVARCHAR_SIZE = 4000

# Under a UTF-8 collation `varchar(n)` budgets n *bytes*, but the `MaxLength`
# annotation it is derived from counts *characters*. A character encodes to at
# most 4 bytes in UTF-8, so a limit declared in characters is scaled to
# guarantee any input fits. Without this a 255-character value holding one
# 3-byte character overflows `varchar(255)` and SQL Server rejects the insert
# with "String or binary data would be truncated".
MAX_UTF8_BYTES_PER_CHARACTER = 4


class MSSQLEncoding(enum.Enum):
    UTF8 = "utf-8"
    UTF16 = "utf-16"


@dataclass
class MSSQLVariableCharacterType(SqlVariableCharacterType):
    # A dataclass field, not a plain attribute: the generated `__eq__` is what
    # schema synchronization compares to decide whether a column needs an
    # `ALTER`. Were `encoding` excluded, `varchar(n)` and `nvarchar(n)` would
    # compare equal and a type change would silently never be migrated.
    encoding: Optional[MSSQLEncoding] = None

    def __init__(self, limit: Optional[int] = None, encoding: Optional[MSSQLEncoding] = None) -> None:
        super().__init__(limit)
        self.encoding = encoding

    def _max_size(self) -> int:
        "Returns the widest fixed-width size this column's type family accepts."

        if self.encoding is MSSQLEncoding.UTF16:
            return MAX_NVARCHAR_SIZE
        else:
            return MAX_VARCHAR_SIZE

    def __str__(self) -> str:
        char_type = "nvarchar" if self.encoding is MSSQLEncoding.UTF16 else "varchar"

        if self.limit is not None and self.limit > 0 and self.limit <= self._max_size() and self.limit != 2147483647:
            return f"{char_type}({self.limit})"
        else:
            return f"{char_type}(max)"

    def parse_meta(self, meta: Any) -> None:
        if isinstance(meta, MaxLength):
            # `MaxLength` counts characters. `varchar(n)` budgets n *bytes*, so a
            # character limit is scaled to a byte limit; `nvarchar(n)` already
            # counts UTF-16 code units, the same unit `MaxLength` counts in, so no
            # scaling applies there.
            scale = MAX_UTF8_BYTES_PER_CHARACTER if self.encoding is not MSSQLEncoding.UTF16 else 1
            budget = meta.value * scale
            # A budget past the fixed-width maximum is held as `None`, the same
            # value discovery reports for a `(max)` column, so that a generated
            # type and the one read back from the database compare equal.
            # Keeping the overflowed count instead would make schema
            # synchronization emit a redundant `ALTER` on every run.
            self.limit = budget if budget <= self._max_size() else None
        else:
            super().parse_meta(meta)


class MSSQLDateTimeType(SqlTimestampType):
    def __init__(self) -> None:
        self.precision = 7

    def __str__(self) -> str:
        return "datetime2"


# Character parameters bind as the wide ODBC types, whose declared size is in
# UTF-16 code units and so cannot exceed the `nvarchar` maximum — half what a
# `varchar` column may declare. A wider declaration describes a fixed-width
# Unicode type that does not exist, and ODBC Driver 18 rejects the descriptor
# with HY104 "Invalid precision value". Report such a column as unbounded: the
# driver then binds it as a LOB, which carries any length without error.
MAX_WIDE_COLUMN_SIZE = MAX_NVARCHAR_SIZE


def _wide_column_size(limit: Optional[int]) -> int:
    """
    Returns the column size to declare for a wide (Unicode) character parameter.

    :param limit: The column's declared character limit, or `None` if unbounded.
    :returns: The limit if it fits a fixed-width wide type, or 0 to bind as a LOB.
    """

    if not limit or limit > MAX_WIDE_COLUMN_SIZE:
        return 0
    return limit


def sql_to_odbc_type(data_type: SqlDataType) -> tuple[int, int, int]:
    """
    Returns the ODBC data type associated with the SQL data type.

    Passing the right data types to `setinputsizes` eliminates data-based guessing, and can speed up `executemany`
    by a significant factor.
    """

    if isinstance(data_type, MSSQLBooleanType):
        return pyodbc.SQL_BIT, 0, 0

    elif isinstance(data_type, SqlIntegerType):
        if data_type.width == 1:
            return pyodbc.SQL_TINYINT, 0, 0
        elif data_type.width == 2:
            return pyodbc.SQL_SMALLINT, 0, 0
        elif data_type.width == 4:
            return pyodbc.SQL_INTEGER, 0, 0
        else:
            return pyodbc.SQL_BIGINT, 0, 0

    elif isinstance(data_type, SqlRealType):
        return pyodbc.SQL_REAL, 0, 0
    elif isinstance(data_type, SqlDoubleType):
        return pyodbc.SQL_DOUBLE, 0, 0
    elif isinstance(data_type, SqlFloatType):
        return pyodbc.SQL_FLOAT, data_type.precision or 53, 0
    elif isinstance(data_type, SqlDecimalType):
        return pyodbc.SQL_DECIMAL, data_type.precision or 15, data_type.scale or 0

    elif isinstance(data_type, SqlTimestampType):
        return pyodbc.SQL_TYPE_TIMESTAMP, data_type.precision or 6, 0
    elif isinstance(data_type, SqlDateType):
        return pyodbc.SQL_TYPE_DATE, 0, 0
    elif isinstance(data_type, SqlTimeType):
        return pyodbc.SQL_TYPE_TIME, data_type.precision or 6, 0

    elif isinstance(data_type, SqlFixedCharacterType):
        # Bind as a wide (Unicode) type so the driver describes the parameter
        # buffer in terms of UTF-16 code units, not bytes. `char`/`varchar`
        # columns under a UTF-8 collation hold multibyte data; binding them as
        # the narrow `SQL_CHAR`/`SQL_VARCHAR` makes `fast_executemany` miscount
        # the buffer width, observed to silently corrupt non-Latin text. SQL
        # Server converts UTF-16 to the column's UTF-8 storage on insert.
        return pyodbc.SQL_WCHAR, _wide_column_size(data_type.limit), 0
    elif isinstance(data_type, SqlVariableCharacterType):
        return pyodbc.SQL_WVARCHAR, _wide_column_size(data_type.limit), 0
    elif isinstance(data_type, SqlFixedBinaryType):
        return pyodbc.SQL_BINARY, data_type.storage or 0, 0
    elif isinstance(data_type, SqlVariableBinaryType):
        return pyodbc.SQL_VARBINARY, data_type.storage or 0, 0

    return pyodbc.SQL_UNKNOWN_TYPE, 0, 0
