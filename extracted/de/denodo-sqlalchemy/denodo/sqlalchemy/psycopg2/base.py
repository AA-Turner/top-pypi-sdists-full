#
# This software is part of the DenodoConnect component collection.
#
# Copyright (c) 2025 Denodo Technologies (https://www.denodo.com)
#
# This module is based on SQLAlchemy's dialect for PostgreSQL:
#
# Copyright (C) 2005-2025 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# Licensed under the MIT License.
# You may not use this file except in compliance with the License.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from __future__ import annotations

from sqlalchemy import exc
from sqlalchemy import sql
from sqlalchemy import util
from sqlalchemy.engine import default
from sqlalchemy.engine import interfaces
from sqlalchemy.engine import reflection
from sqlalchemy.engine.base import Connection
from sqlalchemy.sql import compiler
from sqlalchemy.sql import sqltypes
from sqlalchemy.types import BIGINT
from sqlalchemy.types import BINARY
from sqlalchemy.types import BOOLEAN
from sqlalchemy.types import CHAR
from sqlalchemy.types import DATE
from sqlalchemy.types import DECIMAL
from sqlalchemy.types import FLOAT
from sqlalchemy.types import INTEGER
from sqlalchemy.types import NUMERIC
from sqlalchemy.types import SMALLINT
from sqlalchemy.types import VARCHAR


from . import arraylib as _array
from .types import BIT as BIT
from .types import INTERVAL as INTERVAL
from .types import TIME as TIME
from .types import TIMESTAMP as TIMESTAMP
from .types import _DECIMAL_TYPES  # noqa: F401
from .types import _FLOAT_TYPES  # noqa: F401
from .types import _INT_TYPES  # noqa: F401

RESERVED_WORDS = {
    "all",
    "analyse",
    "analyze",
    "and",
    "any",
    "array",
    "as",
    "asc",
    "asymmetric",
    "both",
    "case",
    "cast",
    "check",
    "collate",
    "column",
    "constraint",
    "create",
    "current_catalog",
    "current_date",
    "current_role",
    "current_time",
    "current_timestamp",
    "current_user",
    "default",
    "deferrable",
    "desc",
    "distinct",
    "do",
    "else",
    "end",
    "except",
    "false",
    "fetch",
    "for",
    "foreign",
    "from",
    "grant",
    "group",
    "having",
    "in",
    "initially",
    "intersect",
    "into",
    "leading",
    "limit",
    "localtime",
    "localtimestamp",
    "new",
    "not",
    "null",
    "of",
    "off",
    "offset",
    "old",
    "on",
    "only",
    "or",
    "order",
    "placing",
    "primary",
    "references",
    "returning",
    "select",
    "session_user",
    "some",
    "symmetric",
    "table",
    "then",
    "to",
    "trailing",
    "true",
    "union",
    "unique",
    "user",
    "using",
    "variadic",
    "when",
    "where",
    "window",
    "with",
    "authorization",
    "between",
    "binary",
    "cross",
    "current_schema",
    "freeze",
    "full",
    "ilike",
    "inner",
    "is",
    "isnull",
    "join",
    "left",
    "like",
    "natural",
    "notnull",
    "outer",
    "over",
    "overlaps",
    "right",
    "similar",
    "verbose",
}

colspecs = {
    sqltypes.ARRAY: _array.ARRAY,
    sqltypes.Interval: INTERVAL,
}



col_sql_type_classes = {
    "BOOLEAN": BOOLEAN,
    "BIT": BIT,
    "TINYINT": SMALLINT,
    "SMALLINT": SMALLINT,
    "INTEGER": INTEGER,
    "BIGINT": BIGINT,
    "FLOAT": FLOAT,
    "DOUBLE": FLOAT,  # DOUBLE was added in SQLAlchemy 2.0 as a synonym to FLOAT
    "DECIMAL": DECIMAL,
    "NUMERIC": NUMERIC,
    "DATE": DATE,
    "TIME": TIME,
    "TIMESTAMP": TIMESTAMP,
    "TIMESTAMP_WITH_TIMEZONE": TIMESTAMP,
    "INTERVAL_YEAR_MONTH": VARCHAR,
    "INTERVAL_DAY_SECOND": VARCHAR,
    "CHAR": CHAR,
    "VARCHAR": VARCHAR,
    "NVARCHAR": VARCHAR,
    "CLOB": VARCHAR,
    "VARBINARY": BINARY,
    "BLOB": BINARY,
    "STRUCT": VARCHAR,
    "ARRAY": VARCHAR,
}


class PGCompiler(compiler.SQLCompiler):

    def render_bind_cast(self, type_, dbapi_type, sqltext):
        if dbapi_type._type_affinity is sqltypes.String and dbapi_type.length:
            # use VARCHAR with no length for VARCHAR cast.
            # see #9511
            dbapi_type = sqltypes.STRINGTYPE
        return f"""{sqltext}::{
            self.dialect.type_compiler_instance.process(
                dbapi_type, identifier_preparer=self.preparer
            )
        }"""

    def render_literal_value(self, value, type_):
        value = super().render_literal_value(value, type_)

        if self.dialect._backslash_escapes:
            value = value.replace("\\", "\\\\")
        return value

    def limit_clause(self, select, **kw):
        # This implementation adapts to Denodo VDP's needs for the OFFSET and LIMIT clauses
        text = ""
        if select._offset_clause is not None:
            text += "\nOFFSET " + self.process(select._offset_clause, **kw)
        if select._limit_clause is not None:
            text += "\nLIMIT " + self.process(select._limit_clause, **kw)
        return text

    def fetch_clause(self, select, **kw):
        # pg requires parens for non literal clauses. It's also required for
        # bind parameters if a ::type casts is used by the driver (asyncpg),
        # so it's easiest to just always add it
        text = ""
        if select._offset_clause is not None:
            text += "\n OFFSET (%s) ROWS" % self.process(
                select._offset_clause, **kw
            )
        if select._fetch_clause is not None:
            text += "\n FETCH FIRST (%s)%s ROWS %s" % (
                self.process(select._fetch_clause, **kw),
                " PERCENT" if select._fetch_clause_options["percent"] else "",
                (
                    "WITH TIES"
                    if select._fetch_clause_options["with_ties"]
                    else "ONLY"
                ),
            )
        return text




class PGDialect(default.DefaultDialect):

    supports_statement_cache = True
    max_identifier_length = 63
    supports_sane_rowcount = True

    bind_typing = 3 # equivalent to "interfaces.BindTyping.RENDER_CASTS" in SQLAlchemy 2.0

    supports_native_enum = False
    supports_native_boolean = True
    supports_native_uuid = False

    supports_sequences = False
    postfetch_lastrowid = False
    use_insertmanyvalues = True

    supports_comments = True
    supports_constraint_comments = False
    supports_default_values = True

    supports_empty_insert = False
    supports_multivalues_insert = True

    supports_identity_columns = True

    default_paramstyle = "pyformat"
    col_sql_type_classes = col_sql_type_classes
    colspecs = colspecs

    _backslash_escapes = True

    statement_compiler = PGCompiler


    def __init__(self, **kwargs):
        paramstyle = kwargs.pop("paramstyle", PGDialect.default_paramstyle)
        if paramstyle != PGDialect.default_paramstyle:
            raise ValueError(f"paramstyle values supported by dialect: {PGDialect.default_paramstyle} (was: {paramstyle})")
        default.DefaultDialect.__init__(self, **kwargs)

    def _get_server_version_info(self, connection):
        # Return 9.6.8 in order to establish that compatibility level throughout the PostgreSQL code of the dialect
        return (9, 6, 8)

    def _get_database_name(self, connection: Connection):
        if not isinstance(connection, Connection):
            raise exc.ArgumentError(
                f"The connection argument passed to the dialect's metadata methods "
                f"should be a {Connection}, got {type(connection)}. ")
        return connection.engine.url.database

    @reflection.cache
    def get_schema_names(self, connection, **kw):
        # No schemas to be used
        return []

    @reflection.cache
    def has_table(self, connection, table_name, schema=None, **kw):
        database_name = self._get_database_name(connection)
        result = connection.execute(
            sql.text(
                "select name as relname "
                "FROM GET_VIEWS() "
                "WHERE input_name = :name and input_database_name = :database_name"
            ).bindparams(
                sql.bindparam("name", table_name, type_=sqltypes.Unicode),
                sql.bindparam("database_name", database_name, type_=sqltypes.Unicode)
            ))
        return bool(result.first())


    def has_sequence(self, connection, sequence_name, schema=None, **kw):
        # No sequences in Denodo VDP
        return False

    @reflection.cache
    def get_table_names(self, connection, schema=None, **kw):
        database_name = self._get_database_name(connection)
        result = connection.execute(
            sql.text(
                "select name as relname "
                "FROM GET_ELEMENTS() "
                "WHERE input_database_name = :database_name and input_type = 'Views' "
                "and subtype = 'base'"
            ).bindparams(
                sql.bindparam("database_name", database_name, type_=sqltypes.Unicode)
            ))
        return [name for name, in result]

    def get_temp_table_names(self, connection, **kw):
        return []

    @reflection.cache
    def get_view_names(self, connection, schema=None, **kw):
        database_name = self._get_database_name(connection)
        result = connection.execute(
            sql.text(
                "SELECT name as relname "
                "FROM GET_ELEMENTS() "
                "WHERE input_database_name = :database_name and input_type = 'Views' "
                "and subtype IN ('derived', 'interface')"
            ).bindparams(
                sql.bindparam("database_name", database_name, type_=sqltypes.Unicode)
            )
        )
        return [name for name, in result]

    def get_materialized_view_names(self, connection, schema=None, **kw):
        return []

    def get_temp_view_names(self, connection, schema=None, **kw):
        return []

    def get_sequence_names(self, connection, schema=None, **kw):
        return []

    def get_view_definition(self, connection, view_name, schema=None, **kw):
        return view_name

    @reflection.cache
    def get_columns(self, connection, table_name, schema=None, **kw):
        database_name = self._get_database_name(connection)
        SQL_COLS = """
SELECT 
       column_name as col_name,
       column_sql_type as col_sql_type,
       column_size as col_size,
       column_decimals as col_decimals,
       column_radix as col_radix,
       column_is_nullable as col_nullable,
       column_is_primary_key as col_is_primary_key,
       column_is_autoincrement as col_is_autoincrement,
       column_is_generated as col_is_generated,
       column_remarks as col_description
FROM GET_VIEW_COLUMNS()
WHERE input_database_name = :database_name and input_view_name= :table_name
ORDER BY ordinal_position
        """
        s = (
            sql.text(SQL_COLS)
            .bindparams(sql.bindparam("table_name", table_name, type_=sqltypes.Unicode),
                        sql.bindparam("database_name", database_name, type_=sqltypes.Unicode))
            .columns(attname=sqltypes.Unicode, format_type=sqltypes.Unicode, default=sqltypes.Unicode)
        )
        c = connection.execute(s, dict(table_name=table_name, schema=schema))
        rows = c.fetchall()

        # dictionary with (name, ) if default search path or (schema, name)
        # as keys
        domains = self._load_domains(connection)

        # dictionary with (name, ) if default search path or (schema, name)
        # as keys
        enums = dict(
            ((rec["name"],), rec)
            if rec["visible"]
            else ((rec["schema"], rec["name"]), rec)
            for rec in self._load_enums(connection, schema="*")
        )

        # format columns
        columns = []
        generated = False

        for (
            col_name,
            col_sql_type,
            col_size,
            col_decimals,
            col_radix,
            col_nullable,
            col_is_primary_key,
            col_is_autoincrement,
            col_is_generated,
            col_description,
        ) in rows:
            column_info = self._get_column_info(
                col_name,
                col_sql_type,
                col_size,
                col_decimals,
                col_radix,
                col_nullable,
                col_is_primary_key,
                col_is_autoincrement,
                col_is_generated,
                col_description,
            )
            columns.append(column_info)

        return columns

    def _get_column_info(
            self,
            col_name,
            col_sql_type,
            col_size,
            col_decimals,
            col_radix,
            col_nullable,
            col_is_primary_key,
            col_is_autoincrement,
            col_is_generated,
            col_description
    ):

        args = ()
        kwargs = {}
        is_array = False

        if col_sql_type in ("FLOAT", "DOUBLE"):
            args = (64,)
        elif col_sql_type in ("DECIMAL", "NUMERIC"):
            args = (int(col_size), int(col_decimals))
        elif col_sql_type in ("TIME", "TIMESTAMP"):
            kwargs["timezone"] = False
            if col_size:
                kwargs["precision"] = int(col_size)
        elif col_sql_type == "TIMESTAMP_WITH_TIMEZONE":
            kwargs["timezone"] = True
            if col_size:
                kwargs["precision"] = int(col_size)
        # Commented out for now as interval support is still not fully implemented
        # elif col_sql_type == "INTERVAL_YEAR_MONTH":
        #     if col_size:
        #         kwargs["precision"] = int(col_size)
        #     kwargs["fields"] = "YEAR TO MONTH"
        # elif col_sql_type == "INTERVAL_DAY_SECOND":
        #     if col_size:
        #         kwargs["precision"] = int(col_size)
        #     kwargs["fields"] = "DAY TO SECOND"
        elif col_sql_type in ("CHAR", "VARCHAR", "CLOB"):
            args = (int(col_size),) if col_size else ()
        elif col_sql_type in ("VARBINARY", "BLOB"):
            args = (int(col_size),) if col_size else ()
        elif col_sql_type == "STRUCT":
            # Will display these as str
            pass
        elif col_sql_type == "ARRAY":
            # Will display these as str
            is_array = True
            pass

        col_sql_type_class = self.col_sql_type_classes.get(col_sql_type, None)

        if col_sql_type_class:
            col_type = col_sql_type_class(*args, **kwargs)
            # Commented out for now as arrays are processed as strs
            # if is_array:
            #     col_type = self.col_sql_type_classes["_array"](coltype)
        else:
            util.warn(
                "Did not recognize type '%s' of column '%s'" % (col_sql_type_class, col_name)
            )
            col_type = sqltypes.NULLTYPE

        column_info = dict(
            name=col_name,
            type=col_type,
            nullable=col_nullable,
            default=None, # We don't have such information in VDP
            primary_key=col_is_primary_key,
            autoincrement=col_is_autoincrement,
            comment=col_description,
        )
        return column_info

    @reflection.cache
    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        database_name = self._get_database_name(connection)
        SQL_PKS = """
SELECT 
        column_name as col_name,
        primary_key_name as col_pk_name
FROM GET_PRIMARY_KEYS()
WHERE input_database_name = :database_name and input_view_name= :table_name
            """
        s = (
            sql.text(SQL_PKS)
            .bindparams(sql.bindparam("table_name", table_name, type_=sqltypes.Unicode),
                        sql.bindparam("database_name", database_name, type_=sqltypes.Unicode))
            .columns(attname=sqltypes.Unicode, format_type=sqltypes.Unicode, default=sqltypes.Unicode)
        )
        c = connection.execute(s, dict(table_name=table_name, schema=schema))
        rows = c.fetchall()

        pk_name = None
        columns = []
        for col_name, col_pk_name in rows:
            if pk_name is not None and pk_name != col_pk_name:
                raise ValueError(f"More than one primary key found for table '{table_name}'")
            pk_name = col_pk_name
            columns.append(col_name)

        if len(columns) == 0:
            return {
                "constrained_columns": [],
                "name": None
            }

        return {
            "constrained_columns": columns,
            "name": pk_name,
            "comment": None     # No descriptions available for PKs in VDP
        }

    @reflection.cache
    def get_multi_pk_constraint(self, connection, schema, filter_names, scope, kind, **kw):
        return (
            (
                (schema, table_name),
                self.get_pk_constraint(connection, table_name, schema)
            )
            for table_name in filter_names
        )

    @reflection.cache
    def get_table_comment(self, connection, table_name, schema=None, **kw):
        database_name = self._get_database_name(connection)
        SQL_COMMENTS = """
SELECT 
        name as view_name,
        description as view_description
FROM GET_VIEWS()
WHERE input_database_name = :database_name and input_name= :table_name
            """
        s = (
            sql.text(SQL_COMMENTS)
            .bindparams(sql.bindparam("table_name", table_name, type_=sqltypes.Unicode),
                        sql.bindparam("database_name", database_name, type_=sqltypes.Unicode))
            .columns(attname=sqltypes.Unicode, format_type=sqltypes.Unicode, default=sqltypes.Unicode)
        )
        c = connection.execute(s, dict(table_name=table_name, schema=schema))
        rows = c.fetchall()

        if len(rows) != 1:
            raise ValueError(f"Exactly one metadata should have been returned for table '{table_name}' but got {len(rows)}")
        (_, view_description) = rows[0]

        if not view_description:
            return {
                "text": None
            }

        return {
            "text": str(view_description)
        }

    @reflection.cache
    def get_multi_table_comment(self, connection, schema, filter_names, scope, kind, **kw):
        return (
            (
                (schema, table_name),
                self.get_table_comment(connection, table_name, schema)
            )
            for table_name in filter_names
        )

    def get_foreign_keys(self, connection, table_name, schema=None, postgresql_ignore_search_path=False, **kw):
        return []

    def get_indexes(self, connection, table_name, schema=None, **kw):
        return []

    def get_unique_constraints(self, connection, table_name, schema=None, **kw):
        return []

    def get_table_comment(self, connection, table_name, schema=None, **kw):
        return {"text": ""}

    def get_check_constraints(self, connection, table_name, schema=None, **kw):
        return []

    def _load_enums(self, connection, schema=None):
        return []

    def _load_domains(self, connection):
        return []
