from __future__ import annotations

import datetime
import functools
import re
from typing import Any

import google.cloud.bigquery.dbapi._helpers
import google.cloud.bigquery.dbapi.cursor
import google.cloud.bigquery.exceptions
import google.cloud.bigquery.query
import sqlalchemy.sql.functions
import sqlalchemy.sql.visitors
from sqlalchemy import BINARY, Column, DefaultClause, LargeBinary, Table, TypeDecorator
from sqlalchemy.engine import Dialect
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import CreateIndex, CreateTable, DefaultClause
from sqlalchemy.sql import FromClause, Selectable, Update
from sqlalchemy.sql.compiler import DDLCompiler
from sqlalchemy.sql.ddl import DropTable
from sqlalchemy.sql.elements import BinaryExpression, BindParameter, Cast, ColumnElement
from sqlalchemy.sql.operators import json_path_getitem_op
from sqlalchemy.sql.selectable import CTE, CompoundSelectState, SelectState
from sqlalchemy.sql.sqltypes import STRINGTYPE, NullType, _Binary  # pyright: ignore[reportPrivateUsage]
from sqlalchemy.types import JSON, DateTime, Interval
from sqlalchemy_bigquery import STRUCT, BigQueryDialect
from sqlalchemy_bigquery.base import BigQueryCompiler, BigQueryDDLCompiler, BigQueryTypeCompiler, process_string_literal


def _compile_cast(element: Cast, compiler: BigQueryCompiler, **kw: Any):
    if isinstance(element.type, JSON):
        assert isinstance(element.clause, ColumnElement)
        processed_text = compiler.process(element.clause, **kw)
        return f"PARSE_JSON({processed_text})"
    return compiler.visit_cast(element, **kw)


def _compile_drop_table(element: DropTable, compiler: BigQueryDDLCompiler, **kw: Any):
    element.if_exists = True
    return compiler.visit_drop_table(element, **kw)


def _format_datetime_as_iso(val: datetime.datetime):
    """Format a datetime as standardized ISO string, independent of platform"""
    # See https://bugs.python.org/issue13305 -- `datetime.datetime.min.isoformat()` is incorrect on linux
    # It returns 1-01-01T00:00:00 instead of 0001-01-01T00:00:00
    time_format = val.time().isoformat()
    return f"{val.year:04d}-{val.month:02d}-{val.day:02d}T{time_format}"


def _compiles_bind_param(element: BindParameter, compiler: BigQueryCompiler, **kw: Any):
    dialect = compiler.dialect
    assert isinstance(dialect, BigQueryDialect)
    if isinstance(element.type, JSON.JSONPathType):
        if element.value != []:
            raise NotImplementedError("Need to implement full JSON path parsing")
        return '"$"'  # JSON path for everything
    assert isinstance(dialect.type_compiler, BigQueryTypeCompiler)
    # FIXME: This fixes chalk sql (CHA-1356)
    if isinstance(element.type, NullType):
        return compiler.visit_bindparam(element, **kw)
    element_type = dialect.type_compiler.process(element.type)

    # FIXME: Hacking to fix a demo. Issue is that our chalk sql resolver bind params come through with this type.
    if element_type == "INTERVAL" and isinstance(element.value, datetime.timedelta):
        dt = element.value

        seconds = int(dt.seconds)
        if dt.microseconds > 0:
            seconds += float(dt.microseconds) / 1e6
        iso8601 = f'CAST("P{int(abs(dt.days))}DT{seconds}S" AS INTERVAL)'
        if dt.seconds < 0:
            iso8601 = f"- {iso8601}"
        return iso8601
    if element_type == "DATETIME" or element_type == "TIMESTAMP":
        if isinstance(element.type, TypeDecorator):
            element.value = element.type.process_bind_param(element.value, compiler.dialect)
        if isinstance(element.value, str):
            if element.value.lower() in ("infinity", "inf", "+inf", "+infinity"):
                element.value = datetime.datetime.max
                if element_type == "TIMESTAMP":
                    element.value = element.value.replace(tzinfo=datetime.timezone.utc)
            elif element.value.lower() in ("-infinity", "-inf"):
                element.value = datetime.datetime.min
                if element_type == "TIMESTAMP":
                    element.value = element.value.replace(tzinfo=datetime.timezone.utc)
        if isinstance(element.value, datetime.datetime):
            if element_type == "TIMESTAMP" and element.value.tzinfo is None:
                raise ValueError(f"TIMESTAMP types must have a timezone, but '{element.value}' is unzoned")
            if element_type == "DATETIME" and element.value.tzinfo is not None:
                raise ValueError(f"DATETIME types do not have a timezone, but '{element.value}' is zoned")
            element.value = _format_datetime_as_iso(element.value)
    return compiler.visit_bindparam(element, **kw)


def _compile_interval(element: Interval, compiler: BigQueryTypeCompiler, **kw: Any):
    return "INTERVAL"


def _compile_struct(element: STRUCT, compiler: BigQueryTypeCompiler, **kw: Any):
    fields = ", ".join(
        f"`{name}` {compiler.process(type_, **kw)}"
        for name, type_ in element._STRUCT_fields  # pyright: ignore[reportPrivateUsage]
    )
    return f"STRUCT<{fields}>"


def _compile_create_index(element: CreateIndex, compiler: BigQueryDDLCompiler, **kw: Any):
    if element.element.dialect_options.get(compiler.dialect.name, {}).get("skip_index", False):
        # No-op query to prevent creation of the index
        return "SELECT 1"
    # Otherwise, best-effort to create the index
    sql_str = compiler.visit_create_index(element, **kw)
    return sql_str.replace("CREATE INDEX", "CREATE SEARCH INDEX")


def _compile_create_table(element: CreateTable, compiler: BigQueryDDLCompiler, **kw: Any):
    element.if_not_exists = True
    options = []
    dialect_options = element.element.dialect_options.get(compiler.dialect.name, {})
    if (bigquery_expiration := dialect_options.get("expiration")) is not None:
        assert isinstance(bigquery_expiration, datetime.datetime), "bigquery_expiration must be a datetime instance"
        options.append(f'expiration_timestamp=TIMESTAMP "{_format_datetime_as_iso(bigquery_expiration)}"')
    if element.element.comment is not None:
        options.append(f"description={process_string_literal(element.element.comment)}")
    if (bigquery_labels := dialect_options.get("labels")) is not None:
        assert isinstance(bigquery_labels, dict), "bigquery_labels must be a dict"
        labels = (
            "["
            + ",".join(
                "(" + process_string_literal(str(k)) + "," + process_string_literal(str(v)) + ")"
                for (k, v) in bigquery_labels.items()
            )
            + "]"
        )
        options.append(f"labels={labels}")
    partition = ""
    if (bigquery_partition := dialect_options.get("partition")) is not None:
        assert isinstance(bigquery_partition, str), "bigquery_partition must be string"
        partition = f"PARTITION BY {bigquery_partition}"
    cluster = ""
    if (bigquery_cluster := dialect_options.get("cluster")) is not None:
        assert isinstance(bigquery_cluster, (list, tuple)), "bigquery_cluster must a list of tuple of cluster columns"
        cluster = f"CLUSTER BY " + ", ".join(f"`{x}`" for x in bigquery_cluster)
    # Temporarily monkeypatching the compiler to skip the `post_create_table`, since we manually specify the options below
    original_post_create_table = compiler.post_create_table
    compiler.post_create_table = lambda *args, **kwargs: ""
    try:
        sql_str = compiler.visit_create_table(element, **kw)
    finally:
        compiler.post_create_table = original_post_create_table

    return "{sql_str} {partition} {cluster} {options}".format(
        sql_str=sql_str,
        partition=partition,
        cluster=cluster,
        options="" if len(options) == 0 else f"OPTIONS({', '.join(options)})",
    )


def _patched_get_column_default_string(self: DDLCompiler, column: Column):
    # Patching this function to include a cast
    if isinstance(column.server_default, DefaultClause):
        if isinstance(column.server_default.arg, str):
            return self.sql_compiler.render_literal_value(column.server_default.arg, STRINGTYPE)
        else:
            expected_type = self.type_compiler.process(column.type)
            return (
                f"CAST({self.sql_compiler.process(column.server_default.arg, literal_binds=True)} as {expected_type})"
            )
    else:
        return None


def _compile_func_now(element: sqlalchemy.sql.functions.now, compiler: BigQueryCompiler, **kw: Any):
    return "CURRENT_TIMESTAMP()"


def _compiles_binary_expression(element: BinaryExpression, compiler: BigQueryCompiler, **kw: Any):
    if element.operator == json_path_getitem_op:
        lhs = compiler.process(element.left, **kw)
        rhs = compiler.process(element.right, **kw)
        dialect = compiler.dialect
        element_type = dialect.type_compiler.process(element.type)
        assert isinstance(dialect, BigQueryDialect)
        return f"CAST(JSON_VALUE({lhs}, {rhs}) AS {element_type})"
    return compiler.visit_binary(element, **kw)


def _compile_datetime(element: DateTime, compiler: BigQueryTypeCompiler, **kw: Any):
    if element.timezone:
        return "TIMESTAMP"
    else:
        return "DATETIME"


def _patched_known_tables(self: BigQueryCompiler):
    # Copied from https://github.com/googleapis/python-bigquery-sqlalchemy/blob/94d113dcb0b763c74ef56842d1fbb0b046edfd11/sqlalchemy_bigquery/base.py#L257
    # and patched to work with compound select statements
    known_tables = set()
    compile_states = []
    if isinstance(self.compile_state, CompoundSelectState):
        for select in self.compile_state.statement.selects:
            compile_state = SelectState(select, self)
            compile_states.append(compile_state)
    else:
        compile_states.append(self.compile_state)

    for compile_state in compile_states:
        for from_ in compile_state.froms:
            if isinstance(from_, Table):
                known_tables.add(from_.name)
            elif isinstance(from_, CTE):
                for column in from_.original.selected_columns:  # type: ignore
                    table = getattr(column, "table", None)
                    if table is not None:
                        known_tables.add(table.name)

    return known_tables


def _patched_update_from(
    self: BigQueryCompiler,
    update_stmt: Update,
    from_table: FromClause,
    extra_froms: list[Selectable],
    from_hints: Any,
    **kw: Any,
):
    # Copied from https://github.com/sqlalchemy/sqlalchemy/blob/e15d00303580a78d6e54da896406ba1ec3685ca1/lib/sqlalchemy/dialects/postgresql/base.py#L1991
    kw["asfrom"] = True
    return "FROM " + ", ".join(
        t._compiler_dispatch(self, fromhints=from_hints, **kw)  # pyright: ignore -- this _compiler_dispatch exists
        for t in extra_froms
    )


def _patch_bigquery_dbapi():
    """Monkeypatching the `extract_types` function to handle struct field names with backticks"""
    # See https://github.com/googleapis/python-bigquery/blob/0bf95460866089c8e955c97ae02f2fa443e1ef62/google/cloud/bigquery/dbapi/cursor.py#L495
    # for the original source
    extract_types_sub = re.compile(
        r"""
            (%*)          # Extra %s.  We'll deal with these in the replacement code

            %             # Beginning of replacement, %s, %(...)s

            (?:\(         # Begin of optional name and/or type
            ([^:)]*)      # name
            (?::          # ':' introduces type
            (             # start of type group
                [a-zA-Z0-9_<>`, ]+ # First part, no parens  # <------------------ THIS IS THE LINE THAT DIFFERS

                (?:               # start sets of parens + non-paren text
                \([0-9 ,]+\)      # comma-separated groups of digits in parens
                                    # (e.g. string(10))
                (?=[, >)])        # Must be followed by ,>) or space
                [a-zA-Z0-9<>, ]*  # Optional non-paren chars
                )*                # Can be zero or more of parens and following text
            )             # end of type group
            )?            # close type clause ":type"
            \))?          # End of optional name and/or type

            s             # End of replacement
            """,
        re.VERBOSE,
    ).sub

    google.cloud.bigquery.dbapi.cursor._extract_types.__defaults__ = (  # pyright: ignore[reportPrivateUsage]
        extract_types_sub,
    )

    complex_query_parameter_parse = re.compile(
        r"""
        \s*
        (ARRAY|STRUCT|RECORD)  # Type
        \s*
        <([A-Z0-9_<>` ,()]+)>   # Subtype(s)    # <------------------ THIS IS THE LINE THAT DIFFERS
        \s*$
        """,
        re.IGNORECASE | re.VERBOSE,
    ).match
    google.cloud.bigquery.dbapi._helpers._parse_type.__defaults__ = (  # pyright: ignore[reportPrivateUsage]
        complex_query_parameter_parse,
    )

    parse_struct_field = re.compile(
        r"""
        (?:`?(\w+)`?\s+)    # field name   # <------------------ THIS IS THE LINE THAT DIFFERS
        ([A-Z0-9<> ,()]+)  # Field type
        $""",
        re.VERBOSE | re.IGNORECASE,
    ).match
    google.cloud.bigquery.dbapi._helpers._parse_struct_fields.__defaults__ = (  # pyright: ignore[reportPrivateUsage]
        parse_struct_field,
    )


class BQBINARY(BINARY):
    def literal_processor(self, dialect: Dialect):
        return lambda value: repr(value.replace(b"%", b"%%"))


class BQLargeBinary(LargeBinary):
    def literal_processor(self, dialect: Dialect):
        return lambda value: repr(value.replace(b"%", b"%%"))


@functools.lru_cache(None)
def register_bigquery_compiler_hooks():
    colspecs = dict(BigQueryDialect.colspecs)
    colspecs.pop(_Binary)
    colspecs[BINARY] = BQBINARY
    colspecs[LargeBinary] = BQLargeBinary
    BigQueryDialect.colspecs = colspecs
    BigQueryCompiler.update_from_clause = _patched_update_from
    BigQueryCompiler._known_tables = _patched_known_tables  # pyright: ignore[reportPrivateUsage]
    BigQueryDDLCompiler.get_column_default_string = _patched_get_column_default_string  # type: ignore -- stubs are incorrect
    compiles(BindParameter, "bigquery")(_compiles_bind_param)
    compiles(Interval, "bigquery")(_compile_interval)
    compiles(CreateIndex, "bigquery")(_compile_create_index)
    compiles(sqlalchemy.sql.functions.now, "bigquery")(_compile_func_now)
    compiles(BinaryExpression, "bigquery")(_compiles_binary_expression)
    compiles(Cast, "bigquery")(_compile_cast)
    compiles(CreateTable, "bigquery")(_compile_create_table)
    compiles(DropTable, "bigquery")(_compile_drop_table)
    compiles(DateTime, "bigquery")(_compile_datetime)
    compiles(STRUCT, "bigquery")(_compile_struct)
    _patch_bigquery_dbapi()
