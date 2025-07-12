import typing
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import pypika
from pypika import AliasedQuery
from pypika import Field
from pypika import Interval
from pypika import Order
from pypika import Table
from pypika import analytics
from pypika.dialects import MySQLQuery
from pypika.dialects import PostgreSQLQuery
from pypika.dialects import SnowflakeQuery
from pypika.enums import Comparator
from pypika.functions import Cast
from pypika.functions import DateAdd
from pypika.queries import Query
from pypika.queries import Selectable
from pypika.terms import AnalyticFunction
from pypika.terms import Function
from pypika.terms import LiteralValue
from pypika.terms import Term
from pypika.terms import Tuple as TupleTerm
from pypika.terms import WindowFrameAnalyticFunction
from pypika.utils import builder
from pypika.utils import format_alias_sql

from tecton_core.aggregation_utils import QueryWindowSpec
from tecton_core.compute_mode import ComputeMode
from tecton_core.data_types import DataType
from tecton_core.query.dialect import Dialect
from tecton_proto.data.feature_store__client_pb2 import FeatureStoreFormatVersion


class CaseSensitiveSnowflakeQueryBuilder(pypika.dialects.SnowflakeQueryBuilder):
    QUOTE_CHAR = '"'


class CaseSensitiveSnowflakeQuery(pypika.queries.Query):
    @classmethod
    def _builder(cls, **kwargs: Any) -> CaseSensitiveSnowflakeQueryBuilder:
        return CaseSensitiveSnowflakeQueryBuilder(**kwargs)


class DuckDBQuery(pypika.queries.Query):
    @classmethod
    def _builder(cls, **kwargs: Any) -> "DuckDBQueryBuilder":
        return DuckDBQueryBuilder(**kwargs)

    @classmethod
    def with_(
        cls, table: Union[str, Selectable], name: str, materialized: Optional[bool] = False, **kwargs: Any
    ) -> "DuckDBQueryBuilder":
        return cls._builder(**kwargs).with_(table, name, materialized)


class DuckDBAliasedQuery(pypika.queries.AliasedQuery):
    def __init__(self, name: str, query: Optional[Selectable] = None, materialized: Optional[bool] = False) -> None:
        super().__init__(name, query)
        self.materialized = materialized


class WindowClause(Term):
    def __init__(self, windows: List[QueryWindowSpec]) -> None:
        self.windows = windows

    def _get_window_expr(self, spec: QueryWindowSpec) -> str:
        return (
            WindowFrameAnalyticFunction("")
            .over(*[Field(x) for x in spec.partition_cols])
            .orderby(*[Field(spec.order_by_col)])
            .range(spec.range_start, spec.range_end)
            .get_partition_sql()
        )

    def get_sql(self, **kwargs: Any) -> str:
        window_sqls = [f"{w.alias} AS ({self._get_window_expr(w)})" for w in self.windows]
        return f"WINDOW {', '.join(window_sqls)}"


class DuckDBQueryBuilder(pypika.dialects.PostgreSQLQueryBuilder):
    ALIAS_QUOTE_CHAR = None

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(as_keyword=True, **kwargs)
        self._window = None

    @builder
    def with_(self, selectable: Selectable, name: str, materialized: Optional[bool] = False) -> "DuckDBQueryBuilder":
        t = DuckDBAliasedQuery(name, selectable, materialized)
        self._with.append(t)

    @builder
    def window(self, window_clause: WindowClause) -> "DuckDBQueryBuilder":
        self._window = window_clause

    def _from_sql(self, with_namespace: bool = False, **kwargs: Any) -> str:
        sql = super(DuckDBQueryBuilder, self)._from_sql(with_namespace, **kwargs)
        if self._window:
            sql += f" {self._window.get_sql()}"
        return sql

    def _with_sql(self, **kwargs: Any) -> str:
        return "WITH " + ",".join(
            clause.name
            + f" AS {'MATERIALIZED' if clause.materialized else ''} ("
            + clause.get_sql(subquery=False, with_alias=False, **kwargs)
            + ") "
            for clause in self._with
        )


class CaseInsensitiveSnowflakeQueryBuilder(pypika.dialects.SnowflakeQueryBuilder):
    QUOTE_CHAR = None
    ALIAS_QUOTE_CHAR = None
    QUERY_ALIAS_QUOTE_CHAR = ""
    QUERY_CLS = SnowflakeQuery


class CustomQuery(pypika.queries.QueryBuilder):
    """
    Defines a custom-query class. It's needed for us to wrap some user-defined sql string from transformations in a QueryBuilder object.
    """

    def __init__(self, sql: str) -> None:
        super().__init__()
        self.sql = sql
        self.withs: List[Selectable] = []

    def with_(self, selectable: Selectable, name: str) -> "CustomQuery":
        """
        overrides QueryBuilder.with_
        """
        t = AliasedQuery(name, selectable)
        self.withs.append(t)
        return self

    def get_sql(self, with_alias: bool = False, subquery: bool = False, **kwargs: Any) -> str:
        """
        overrides QueryBuilder.get_sql
        """
        sql = ""
        if self.withs:
            sql += "WITH " + ",".join(
                clause.name + " AS (" + clause.get_sql(subquery=False, with_alias=False, **kwargs) + ") "
                for clause in self.withs
            )
        sql += self.sql
        if with_alias:
            self.alias = "sq0"
            sql = f"({sql})"
            return format_alias_sql(sql, self.alias or self._table_name, **kwargs)
        return sql


class LastValue(analytics.LastValue):
    """
    Fixed version of pypika's LastValue to handle Snowflake and Athena wanting "ignore nulls"
     to be outside the parens of the window func, and Spark using a bool param.
    """

    def __init__(self, dialect: "Dialect", *args: Any, **kwargs: Any) -> None:
        self._dialect = dialect
        super().__init__(*args, **kwargs)

    def get_special_params_sql(self, **kwargs: Any) -> Optional[str]:
        if self._dialect == Dialect.SPARK:
            # see: https://docs.databricks.com/sql/language-manual/functions/last_value.html
            # for sparkSQL syntax
            return f", {self._ignore_nulls}"
        elif self._dialect == Dialect.DUCKDB and self._ignore_nulls:
            # see: https://duckdb.org/docs/sql/window_functions.html
            # for DuckDB syntax
            return " IGNORE NULLS"
        # Snowflake does not support adding a function param to indicate "ignore nulls"
        # It looks like LAST_VALUE(...) IGNORE NULLS OVER(...)
        # see: https://docs.snowflake.com/en/sql-reference/functions/last_value.html
        # Nor does Athena - Athena docs don't make this clear though.
        else:
            return None

    def get_function_sql(self, **kwargs: Any) -> str:
        if self._dialect == Dialect.SPARK or self._dialect == Dialect.DUCKDB:
            return super(LastValue, self).get_function_sql(**kwargs)
        else:
            function_sql = super(AnalyticFunction, self).get_function_sql(**kwargs)
            partition_sql = self.get_partition_sql(**kwargs)

            sql = function_sql
            if self._ignore_nulls:
                sql += " IGNORE NULLS"
            if self._include_over:
                sql += " OVER({partition_sql})".format(partition_sql=partition_sql)
            return sql


class CompatFunctions:
    def __init__(self, compute_mode: Optional[ComputeMode] = None) -> None:
        self.compute_mode = compute_mode

    @staticmethod
    def for_dialect(d: Dialect, compute_mode: Optional[ComputeMode] = None) -> "CompatFunctions":
        if d == Dialect.SPARK:
            return _Spark(compute_mode=compute_mode)
        elif d == Dialect.DUCKDB:
            return _DuckDB(compute_mode=compute_mode)
        elif d == Dialect.SNOWFLAKE:
            return _Snowflake(compute_mode=compute_mode)
        elif d == Dialect.ATHENA:
            return _Athena(compute_mode=compute_mode)
        elif d == Dialect.BIGQUERY:
            return _Bigquery(compute_mode=compute_mode)
        elif d == Dialect.ARROW:
            return CompatFunctions(compute_mode=compute_mode)
        msg = f"Unexpected dialect {d}"
        raise Exception(msg)

    @classmethod
    def query(cls) -> typing.Type[Query]:
        raise NotImplementedError()

    @classmethod
    def struct(cls, field_names: List[str]) -> Term:
        raise NotImplementedError()

    @classmethod
    def struct_extract(
        cls, name: str, field_names: List[str], aliases: List[str], schema: Dict[str, DataType]
    ) -> List[Field]:
        raise NotImplementedError()

    @classmethod
    def ordered_filtered_list(
        cls, from_column: Term, order_by_column: Term, filter_clause: Term, direction: Order = Order.asc
    ) -> Term:
        raise NotImplementedError()

    @classmethod
    def list(cls, column: str) -> WindowFrameAnalyticFunction:
        raise NotImplementedError()

    @classmethod
    def any(cls, column: str) -> Term:
        raise NotImplementedError()

    @classmethod
    def list_filter_nulls(cls, column: str) -> Term:
        raise NotImplementedError()

    @classmethod
    def list_transform(cls, column: Term, lambda_func: str) -> Term:
        raise NotImplementedError()

    @classmethod
    def to_timestamp(cls, time_str: str) -> Term:
        raise NotImplementedError()

    @classmethod
    def to_timestamp_microseconds(cls, time_str: str) -> Term:
        raise NotImplementedError()

    @classmethod
    def date_add(cls, interval: str, amount: int, time_field: Term) -> Term:
        raise NotImplementedError()

    @classmethod
    def to_unixtime(cls, timestamp: Term) -> Term:
        raise NotImplementedError()

    @classmethod
    def to_utc(cls, timestamp: Term) -> Term:
        raise NotImplementedError()

    @classmethod
    def from_unixtime(cls, unix_timestamp: Term) -> Term:
        raise NotImplementedError()

    @classmethod
    def strftime(cls, timestamp: Term, fmt: Union[Term, str]) -> Term:
        raise NotImplementedError()

    @classmethod
    def int_div(cls, a: Union[Term, int], b: Union[Term, int]) -> Term:
        raise NotImplementedError()

    @classmethod
    def convert_epoch_term_in_seconds(
        cls, timestamp: Term, time_stamp_feature_store_format_version: FeatureStoreFormatVersion
    ) -> Term:
        """
        Converts an epoch term to a timestamp column
        :param timestamp: epoch column [V0 : Seconds, V1 : Nanoseconds]
        :param time_stamp_feature_store_format_version: Feature Store Format Version
        :return: epoch in seconds
        """
        if time_stamp_feature_store_format_version == FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_DEFAULT:
            return timestamp
        # Cast explicitly to an integer (which is the expectation), since otherwise SQL will often treat integer
        # division as outputting a double, which is incompatible with to_timestamp(epoch_seconds) functions
        return timestamp / int(1e9)

    @classmethod
    def convert_epoch_seconds_to_feature_store_format_version(
        cls, timestamp: Term, feature_store_format_version: FeatureStoreFormatVersion
    ) -> Term:
        if feature_store_format_version == FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_DEFAULT:
            return timestamp
        return Cast(timestamp * int(1e9), as_type="bigint")

    @classmethod
    def over_window(cls, term: Term, window_spec: QueryWindowSpec) -> Term:
        return (
            term.over(*[Field(x) for x in window_spec.partition_cols])
            .orderby(*[Field(window_spec.order_by_col)])
            .range(window_spec.range_start, window_spec.range_end)
        )


class OverWindowAlias(Term):
    def __init__(self, function: Term, window_alias: str) -> None:
        self.function = function
        self.window_alias = window_alias
        super().__init__()

    def get_sql(self, **kwargs: Any) -> str:
        sql = f"{self.function.get_sql(**kwargs)} OVER {self.window_alias}"
        return format_alias_sql(sql, self.alias, **kwargs)


class _Snowflake(CompatFunctions):
    def query(self) -> typing.Type[Query]:
        # executing snowflake queries in unified Tecton mode will have ComputeMode.DUCK_DB
        return CaseSensitiveSnowflakeQuery

    @classmethod
    def struct(cls, field_names: List[str]) -> Term:
        return Function("array_construct", *[Field(n) for n in field_names])

    @classmethod
    def struct_extract(
        cls, name: str, field_names: List[str], aliases: List[str], schema: Dict[str, DataType]
    ) -> List[Field]:
        res = []
        for idx in range(len(aliases)):
            val = Function("get", Field(name), idx)
            if field_names[idx] in schema:
                feature_type = schema[field_names[idx]].sql_type
                val = Cast(val, feature_type)
            res.append(val.as_(aliases[idx]))
        return res

    @classmethod
    def to_timestamp(cls, time_str: str) -> Term:
        return Function("to_timestamp", time_str)

    @classmethod
    def date_add(cls, interval: str, amount: int, time_field: Term) -> Term:
        # snowflake uses dateadd rather than date_add;
        # https://docs.snowflake.com/en/sql-reference/functions/dateadd.html

        # LiteralValue will not put quotes around.
        # So we get dateadd(second, ...)
        interval = LiteralValue(interval)
        return Function("dateadd", interval, amount, time_field)

    @classmethod
    def to_unixtime(cls, timestamp: Term) -> Term:
        return Function("date_part", Field("epoch_second"), timestamp)

    @classmethod
    def from_unixtime(cls, unix_timestamp: Term) -> Term:
        return Function("to_timestamp", unix_timestamp)

    @classmethod
    def strftime(cls, timestamp: Term, fmt: Union[Term, str]) -> Term:
        raise NotImplementedError()

    @classmethod
    def int_div(cls, a: Union[Term, int], b: Union[Term, int]) -> Term:
        raise NotImplementedError()


class DuckDBList(WindowFrameAnalyticFunction):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(DuckDBList, self).__init__("LIST", *args, **kwargs)


class DuckDBOrderedFilteredList(Term):
    def __init__(
        self,
        from_column: Term,
        order_by_column: Term,
        filter_clause: Term,
        direction: Order = Order.asc,
    ) -> None:
        super().__init__()
        self.from_column = from_column
        self.order_by_column = order_by_column
        self.direction = direction
        self.filter_clause = filter_clause

    def get_sql(self, **kwargs: Any) -> str:
        """
        Returns a `LIST()` with an `ORDER BY` and `FILTER` clauses. Pypika doesn't support ARRAY_AGG or LIST operations
        by default.
        """
        query_sql = (
            f"LIST({self.from_column.get_sql(**kwargs)} "
            f"ORDER BY {self.order_by_column.get_sql(**kwargs)} {self.direction.value}) "
            f"FILTER (WHERE {self.filter_clause.get_sql(**kwargs)})"
        )
        return format_alias_sql(query_sql, self.alias, **kwargs)


class DuckDBAny(Term):
    def __init__(self, column: Term) -> None:
        super().__init__()
        self.column = column

    def get_sql(self, **kwargs: Any) -> str:
        """
        Returns `ANY()`. Pypika doesn't support this function by default.
        """
        query_sql = f"ANY({self.column.get_sql(**kwargs)})"
        return format_alias_sql(query_sql, self.alias, **kwargs)


class DuckDBListValue(Term):
    def __init__(self, columns: List[Term]) -> None:
        super().__init__()
        self.columns = columns

    def get_sql(self, **kwargs: Any) -> str:
        cols_sql = ", ".join(col.get_sql(**kwargs) for col in self.columns)
        query_sql = f"LIST_VALUE({cols_sql})"
        return format_alias_sql(query_sql, self.alias, **kwargs)


class DuckDBArrayValue(Term):
    def __init__(self, columns: Term) -> None:
        super().__init__()
        self.columns = columns

    def get_sql(self, **kwargs: Any) -> str:
        query_sql = f"Array_VALUE({self.columns.get_sql(**kwargs)})"
        return format_alias_sql(query_sql, self.alias, **kwargs)


class DuckDBListFilterNulls(Term):
    def __init__(self, column: Term) -> None:
        super().__init__()
        self.column = column

    def get_sql(self, **kwargs: Any) -> str:
        """
        Returns an filtered list with non-null elements. Pypika doesn't support this function by default.
        """
        query_sql = f"array_filter({self.column.get_sql(**kwargs)}, element -> element IS NOT NULL)"
        return format_alias_sql(query_sql, self.alias, **kwargs)


class DuckDBStructPack(Term):
    def __init__(self, *fields: Term) -> None:
        super().__init__()
        self.fields = fields

    def get_sql(self, **kwargs: Any) -> str:
        """
        Returns `STRUCT_PACK()`. Pypika doesn't support this function by default.
        """
        query_sql = f"STRUCT_PACK({','.join(field.get_sql(**kwargs) for field in self.fields)})"
        return format_alias_sql(query_sql, self.alias, **kwargs)


class DuckDBNamedStructPack(Term):
    # NOTE: DuckDB requires named arguments inside struct_pack, e.g.:
    #   struct_pack(sum_int_col := SUM("int_col"))
    # However, PyPika does not natively support named arguments (:=) in function calls.
    #
    # This StructPackFunction class is a custom PyPika term that allows us to manually render
    # the struct_pack expression with the required named arguments using string interpolation.
    #
    # Without this, calling struct_pack(SUM("int_col")) would result in the field name inside
    # the struct being inferred from the expression (e.g., "sum(int_col)"), which leads to
    # mismatches when comparing output against expected field names like "sum_int_col".

    def __init__(self, fields: List[Tuple[str, Term]]) -> None:
        super().__init__()
        self.fields = fields

    def get_sql(self, **kwargs: Any) -> str:
        parts = [f"{name} := {str(expr)}" for name, expr in self.fields]
        return f"struct_pack({', '.join(parts)})"


class DuckDBListTransform(Term):
    def __init__(self, column: Term, lambda_func: str) -> None:
        super().__init__()
        self.column = column
        self.lambda_func = lambda_func

    def get_sql(self, **kwargs: Any) -> str:
        """
        Returns `LIST_TRANSFORM()`. Pypika doesn't support this function by default.
        """
        query_sql = f"LIST_TRANSFORM({self.column.get_sql(**kwargs)}, {self.lambda_func})"
        return format_alias_sql(query_sql, self.alias, **kwargs)


class DuckDBTupleTerm(TupleTerm):
    def get_sql(self, **kwargs):
        return f"row{super().get_sql(**kwargs)}"


class DuckDBComparatorExtension(Comparator):
    IS_NOT_DISTINCT_FROM = " IS NOT DISTINCT FROM "


class Values(Term):
    def __init__(
        self, values: List[pypika.Tuple], alias: Optional[str] = None, columns: Optional[List[str]] = None
    ) -> None:
        super().__init__()
        self.values = values
        self.alias = alias
        self.columns = columns

    def get_sql(self, **kwargs: Any) -> str:
        """
        Returns a VALUES clause of the format
        VALUES (a, b, c), (d,e,f) Alias(col1, col2, col3)
        """
        sql = "VALUES {values}".format(values=",".join([row.get_sql() for row in self.values]))

        if self.alias is not None:
            columns = ""
            if self.columns is not None:
                columns = "({columns})".format(columns=",".join(self.columns))

            sql = "({values}) {alias}{columns}".format(values=sql, alias=self.alias, columns=columns)

        return sql


class _DuckDB(CompatFunctions):
    @classmethod
    def query(cls) -> typing.Type[Query]:
        return DuckDBQuery

    @classmethod
    def struct(cls, field_names: List[str]) -> Term:
        return DuckDBStructPack(*[Field(n) for n in field_names])

    @classmethod
    def struct_by_name(cls, fields: List[Tuple[str, Term]]) -> Term:
        return DuckDBNamedStructPack(fields)

    @classmethod
    def list(cls, column: str) -> WindowFrameAnalyticFunction:
        return DuckDBList(Field(column))

    @classmethod
    def any(cls, column: str) -> Term:
        return DuckDBAny(Field(column))

    @classmethod
    def list_filter_nulls(cls, column: str) -> Term:
        return DuckDBListFilterNulls(Field(column))

    @classmethod
    def list_value(cls, column_names: List[str]) -> Term:
        return DuckDBListValue([Field(name) for name in column_names])

    @classmethod
    def array_value(cls, from_column: Term) -> Term:
        return DuckDBArrayValue(from_column)

    @classmethod
    def ordered_filtered_list(
        cls, from_column: Term, order_by_column: Term, filter_clause: Term, direction: Order = Order.asc
    ) -> Term:
        return DuckDBOrderedFilteredList(from_column, order_by_column, filter_clause, direction)

    @classmethod
    def list_transform(cls, column: Term, lambda_func: str) -> Term:
        return DuckDBListTransform(column, lambda_func)

    @classmethod
    def struct_extract(
        cls, name: str, field_names: List[str], aliases: List[str], schema: Dict[str, DataType]
    ) -> List[Field]:
        assert len(field_names) == len(aliases)
        return [getattr(Table(name), field).as_(alias) for (field, alias) in zip(field_names, aliases)]

    @classmethod
    def to_timestamp(cls, time_col: Union[Term, str]) -> Term:
        return Cast(time_col, as_type="timestamptz")

    @classmethod
    def to_timestamp_microseconds(cls, time_col: Union[Term, str]) -> Term:
        return Cast(time_col, as_type="timestamp")

    @classmethod
    def date_add(cls, interval: str, amount: int, time_field: Term) -> Term:
        return _Spark.date_add(interval, amount, time_field)

    @classmethod
    def to_unixtime(cls, timestamp: Term) -> Term:
        # IMPORTANT: date_part function returns float type. We keep it as float to preserve higher granularity.
        # The caller of this function must convert it to integer if required
        return Function("date_part", "epoch", cls.to_timestamp(timestamp))

    @classmethod
    def to_utc(cls, timestamp: Term) -> Term:
        """
        When DuckDB converts a timestamp column to UTC, the timezone is removed if the original column had a
        timezone. But if the original column did not have a timezone, the timezone is set to UTC.
        We need to make sure that timestamp always has a timezone, because in duckdb >= 0.10
        timezone-naive timestamp can't be compared with timezone-aware timestamp.
        Cast to TIMESTAMPTZ relies on the fact that DuckDB session timezone was set to UTC.
        """
        return Cast(Function("timezone", "UTC", timestamp), "timestamptz")

    @classmethod
    def from_unixtime(cls, unix_timestamp: Term) -> Term:
        """
        Function `to_timestamp` returns timezone-aware results starting version 0.9.0.
        """
        return Function("to_timestamp", unix_timestamp)

    @classmethod
    def int_div(cls, a: Union[Term, int], b: Union[Term, int]) -> Term:
        return Function("_tecton_int_div", a, b)

    @classmethod
    def strftime(cls, timestamp: Term, fmt: Union[Term, str]) -> Term:
        return Function("strftime", timestamp, fmt)

    @classmethod
    def over_window(cls, term: Term, window_spec: QueryWindowSpec) -> Term:
        return OverWindowAlias(term, window_spec.alias)


class _Spark(CompatFunctions):
    @classmethod
    def query(cls) -> typing.Type[Query]:
        # Spark (similar to HiveSQL) uses backticks like MySQL
        return MySQLQuery

    @classmethod
    def struct(cls, field_names: List[str]) -> Term:
        return Function("struct", *[Field(n) for n in field_names])

    @classmethod
    def struct_extract(
        cls, name: str, field_names: List[str], aliases: List[str], schema: Dict[str, DataType]
    ) -> List[Field]:
        assert len(field_names) == len(aliases)
        return [getattr(Table(name), field).as_(alias) for (field, alias) in zip(field_names, aliases)]

    @classmethod
    def to_timestamp(cls, time_str: str) -> Term:
        return Function("to_timestamp", time_str)

    @classmethod
    def date_add(cls, interval: str, amount: int, time_field: Term) -> Term:
        if interval == "second":
            return time_field + Interval(seconds=amount)
        elif interval == "millisecond":
            # Note: PyPika has a bug where for microseconds, it does not correctly respect negative values
            if amount >= 0:
                return time_field + Interval(microseconds=amount * 1000)
            else:
                return time_field - Interval(microseconds=abs(amount) * 1000)
        else:
            msg = f"Unexpected date_add interval {interval}"
            raise NotImplementedError(msg)

    @classmethod
    def to_unixtime(cls, timestamp: Term) -> Term:
        return Function("unix_timestamp", timestamp)

    @classmethod
    def from_unixtime(cls, unix_timestamp: Term) -> Term:
        return Cast(Function("from_unixtime", unix_timestamp), as_type="timestamp")

    @classmethod
    def strftime(cls, timestamp: Term, fmt: Union[Term, str]) -> Term:
        raise NotImplementedError()

    @classmethod
    def int_div(cls, a: Union[Term, int], b: Union[Term, int]) -> Term:
        raise NotImplementedError()


class _Athena(CompatFunctions):
    @classmethod
    def query(cls) -> typing.Type[Query]:
        # Athena (similar to PrestoSQL) uses doublequotes like Postgres
        return PostgreSQLQuery

    @classmethod
    def struct(cls, field_names: List[str]) -> Term:
        return Function("row", *[Field(n) for n in field_names])

    @classmethod
    def struct_extract(
        cls, name: str, field_names: List[str], aliases: List[str], schema: Dict[str, DataType]
    ) -> List[Field]:
        return [getattr(Table(name), f"field{idx}").as_(aliases[idx]) for idx in range(len(aliases))]

    @classmethod
    def to_timestamp(cls, time_str: str) -> Term:
        return Function("from_iso8601_timestamp", time_str)

    @classmethod
    def date_add(cls, interval: str, amount: int, time_field: Term) -> Term:
        interval = f"'{interval}'"
        return DateAdd(interval, amount, time_field)

    @classmethod
    def to_unixtime(cls, timestamp: Term) -> Term:
        return Function("to_unixtime", timestamp)

    @classmethod
    def from_unixtime(cls, unix_timestamp: Term) -> Term:
        return Function("from_unixtime", unix_timestamp)

    @classmethod
    def strftime(cls, timestamp: Term, fmt: Union[Term, str]) -> Term:
        raise NotImplementedError()

    @classmethod
    def int_div(cls, a: Union[Term, int], b: Union[Term, int]) -> Term:
        raise NotImplementedError()


class _Bigquery(CompatFunctions):
    @classmethod
    def query(cls) -> typing.Type[Query]:
        # BigQuery backticks to quote fields, similar to MySQL
        return MySQLQuery

    @classmethod
    def struct(cls, field_names: List[str]) -> Term:
        return Function("STRUCT", *[Field(n) for n in field_names])

    @classmethod
    def struct_extract(
        cls, name: str, field_names: List[str], aliases: List[str], schema: Dict[str, DataType]
    ) -> List[Field]:
        return [Field(f"{name}.{field_names[idx]}").as_(aliases[idx]) for idx in range(len(aliases))]

    @classmethod
    def to_timestamp(cls, time_str: str) -> Term:
        return Function("TIMESTAMP", time_str)

    @classmethod
    def date_add(cls, interval: str, amount: int, time_field: Term) -> Term:
        interval = LiteralValue(f"INTERVAL {amount} {interval}")
        return Function("DATE_ADD", time_field, interval)

    @classmethod
    def to_unixtime(cls, timestamp: Term) -> Term:
        return Function("UNIX_SECONDS", timestamp)

    @classmethod
    def from_unixtime(cls, unix_timestamp: Term) -> Term:
        return Function("TIMESTAMP_SECONDS", unix_timestamp)

    @classmethod
    def strftime(cls, timestamp: Term, fmt: Union[Term, str]) -> Term:
        return Function("FORMAT_TIMESTAMP", fmt, timestamp)

    @classmethod
    def int_div(cls, a: Union[Term, int], b: Union[Term, int]) -> Term:
        return Function("SAFE_DIVIDE", a, b)

    @classmethod
    def ordered_filtered_list(
        cls, from_column: Term, order_by_column: Term, filter_clause: Term, direction: Order = Order.asc
    ) -> Term:
        raise NotImplementedError()

    @classmethod
    def list(cls, column: str) -> WindowFrameAnalyticFunction:
        raise NotImplementedError()

    @classmethod
    def list_transform(cls, column: Term, lambda_func: str) -> Term:
        raise NotImplementedError()

    @classmethod
    def any(cls, column: str) -> Term:
        raise NotImplementedError()

    @classmethod
    def list_filter_nulls(cls, column: str) -> Term:
        raise NotImplementedError()

    @classmethod
    def to_utc(cls, timestamp: Term) -> Term:
        raise NotImplementedError()
