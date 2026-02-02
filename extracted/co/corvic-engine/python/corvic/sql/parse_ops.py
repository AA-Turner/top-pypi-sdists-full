"""Parse table operation logs into sql statements."""

import functools
from typing import Protocol, TypeGuard, get_args

import pyarrow as pa
import sqlglot
import structlog

from corvic import op_graph
from corvic.result import InvalidArgumentError
from corvic.well_known_types import VectorSimilarityMetric
from corvic_generated.orm.v1 import table_pb2

_logger = structlog.get_logger()

_SqlComputableOp = (
    op_graph.op.SelectFromStaging
    | op_graph.op.RenameColumns
    | op_graph.op.Join
    | op_graph.op.SelectColumns
    | op_graph.op.LimitRows
    | op_graph.op.OrderBy
    | op_graph.op.FilterRows
    | op_graph.op.DistinctRows
    | op_graph.op.UpdateMetadata
    | op_graph.op.SetMetadata
    | op_graph.op.RemoveFromMetadata
    | op_graph.op.UpdateFeatureTypes
    | op_graph.op.RollupByAggregation
    | op_graph.op.Empty
    | op_graph.op.SelectFromVectorStaging
    | op_graph.op.AggregateColumns
    | op_graph.op.Union
)
"""The subset of table ops that can be computed by sql queries."""


def can_be_sql_computed(
    op: op_graph.Op, *, recursive=False
) -> TypeGuard[_SqlComputableOp]:
    if recursive and not all(
        can_be_sql_computed(sub_op, recursive=recursive) for sub_op in op.sources()
    ):
        return False
    if not isinstance(op, _SqlComputableOp):
        return False
    match op:
        case (
            op_graph.op.SelectFromStaging()
            | op_graph.op.RenameColumns()
            | op_graph.op.Join()
            | op_graph.op.SelectColumns()
            | op_graph.op.LimitRows()
            | op_graph.op.OrderBy()
            | op_graph.op.FilterRows()
            | op_graph.op.DistinctRows()
            | op_graph.op.UpdateMetadata()
            | op_graph.op.SetMetadata()
            | op_graph.op.RemoveFromMetadata()
            | op_graph.op.UpdateFeatureTypes()
            | op_graph.op.RollupByAggregation()
            | op_graph.op.Empty()
            | op_graph.op.SelectFromVectorStaging()
            | op_graph.op.AggregateColumns()
            | op_graph.op.Union()
        ):
            # these are always computeable
            return True


def _to_vector_similarity_metric(val: str) -> VectorSimilarityMetric:
    for arg in get_args(VectorSimilarityMetric):
        if val == arg:
            return arg
    _logger.warning(
        "given metric is unknown, defaulting to cosine for similarity", given_metric=val
    )
    return "cosine"


class StagingQueryGenerator(Protocol):
    """A callable that generates a staging query for some backend."""

    def __call__(
        self, blob_names: list[str], column_names: list[str]
    ) -> sqlglot.exp.Query: ...


class VectorSearchQueryGenerator(Protocol):
    """A callable that generates a vector search staging query for some backend."""

    def __call__(
        self,
        input_vector: list[float],
        vector_blob_names: list[str],
        vector_column_name: str,
        column_names: list[str],
        similarity_metric: VectorSimilarityMetric,
    ) -> sqlglot.exp.Query: ...


class _OpLogParser:
    def __init__(
        self,
        make_staging_query: StagingQueryGenerator,
        make_vector_search_staging_query: VectorSearchQueryGenerator,
    ):
        self._make_staging_query = make_staging_query
        self._make_vector_search_staging_query = make_vector_search_staging_query
        self._id = 0

    @staticmethod
    def _quote(val: str):
        return sqlglot.to_identifier(val, quoted=True)

    @staticmethod
    def _column(val: str, table: sqlglot.exp.Identifier | None = None):
        return sqlglot.column(val, table=table, quoted=True)

    @classmethod
    def _column_as_type(
        cls,
        val: str,
        dtype: sqlglot.exp.DATA_TYPE,
        table: sqlglot.exp.Identifier | None = None,
    ):
        return sqlglot.exp.TryCast(this=cls._column(val, table), to=dtype)

    @classmethod
    def _cast_join_column_pair(
        cls,
        op: op_graph.op.Join,
        left_name: str,
        right_name: str,
        left_table_name: sqlglot.exp.Identifier,
        right_table_name: sqlglot.exp.Identifier,
    ):
        # This function will only cast null and integer columns to strings.
        # If a column is null it will be cast to a string type.
        # If one column is an integer and the other is not, then the integer
        # column will be cast to a string.
        left_field = op.left_source.schema[left_name]
        right_field = op.right_source.schema[right_name]
        cast_left_column = pa.types.is_null(left_field.dtype)
        cast_right_column = pa.types.is_null(right_field.dtype)

        if pa.types.is_integer(left_field.dtype):
            if not pa.types.is_integer(right_field.dtype):
                cast_left_column = True
        elif pa.types.is_integer(right_field.dtype):
            cast_right_column = True

        left_column = (
            cls._column_as_type(left_name, "TEXT", left_table_name)
            if cast_left_column
            else cls._column(left_name, left_table_name)
        )
        right_column = (
            cls._column_as_type(right_name, "TEXT", right_table_name)
            if cast_right_column
            else cls._column(right_name, right_table_name)
        )
        return (left_column, right_column)

    def _next_name_id(self):
        val = self._id
        self._id += 1
        return val

    def _unique_name(self, name: str):
        return self._quote(f"{name}-{self._next_name_id()}")

    def _select_from_staging_to_sql(
        self, op: op_graph.op.SelectFromStaging
    ) -> sqlglot.exp.Query:
        columns = [field.name for field in op.arrow_schema]
        query = self._make_staging_query(list(op.blob_names), columns)

        def _promote_select(
            expr: sqlglot.Expression,
        ) -> sqlglot.exp.Column | sqlglot.exp.Alias:
            match expr:
                case sqlglot.exp.Column():
                    return expr
                case sqlglot.exp.Literal():
                    return self._column(expr.output_name)
                case sqlglot.exp.Alias():
                    return expr
                case _:
                    raise op_graph.OpParseError(
                        "select must be a literal, a column type, or an alias"
                    )

        return query.select(
            *(_promote_select(expr) for expr in query.selects), append=False
        )

    def _select_from_vector_staging_to_sql(
        self, op: op_graph.op.SelectFromVectorStaging
    ) -> sqlglot.exp.Query:
        columns = [field.name for field in op.arrow_schema]
        query = self._make_vector_search_staging_query(
            input_vector=list(op.input_vector),
            vector_blob_names=list(op.blob_names),
            vector_column_name=op.vector_column_name,
            column_names=columns,
            similarity_metric=_to_vector_similarity_metric(op.similarity_metric),
        )

        def _promote_select(
            expr: sqlglot.Expression,
        ) -> sqlglot.exp.Column | sqlglot.exp.Alias:
            match expr:
                case sqlglot.exp.Column():
                    return expr
                case sqlglot.exp.Literal():
                    return self._column(expr.output_name)
                case sqlglot.exp.Alias():
                    return expr
                case _:
                    raise op_graph.OpParseError(
                        "select must be a literal, a column type, or an alias"
                    )

        return query.select(
            *(_promote_select(expr) for expr in query.selects), append=False
        )

    def _rename_columns_to_sql(
        self,
        op: op_graph.op.RenameColumns,
    ) -> sqlglot.exp.Query:
        source_query = self.parse(op.source)

        def replace_select_if_needed(expr: sqlglot.Expression) -> sqlglot.Expression:
            if expr.output_name not in op.old_name_to_new:
                return expr
            return expr.unalias().as_(op.old_name_to_new[expr.output_name])

        return source_query.select(
            *(replace_select_if_needed(expr) for expr in source_query.selects),
            append=False,
        )

    def _join_to_sql(
        self,
        op: op_graph.op.Join,
    ) -> sqlglot.exp.Query:
        left_subquery = self.parse(op.left_source)
        left_table_name = self._unique_name("left_table")
        right_subquery = self.parse(op.right_source)
        right_table_name = self._unique_name("right_table")

        match op.how:
            case table_pb2.JOIN_TYPE_INNER:
                join_type = "INNER"
            case table_pb2.JOIN_TYPE_LEFT_OUTER:
                join_type = "LEFT OUTER"
            case _:
                join_type = "INNER"

        join_columns = (
            self._cast_join_column_pair(
                op, left_name, right_name, left_table_name, right_table_name
            )
            for left_name, right_name in zip(
                op.left_join_columns, op.right_join_columns, strict=True
            )
        )

        on_clause = functools.reduce(
            lambda first, second: first.and_(second),
            (left_col.eq(right_col) for left_col, right_col in join_columns),
        )

        name_to_column: dict[str, sqlglot.exp.Column | sqlglot.exp.Alias] = {
            name: self._column(name, left_table_name)
            for name in left_subquery.named_selects
        }
        for name in right_subquery.named_selects:
            if name in op.right_join_columns:
                continue
            if name not in name_to_column:
                name_to_column[name] = self._column(name, right_table_name)

        return (
            sqlglot.select(*name_to_column.values())
            .from_(left_table_name)
            .join(
                right_table_name,
                on=on_clause,
                join_type=join_type,
            )
            .with_(left_table_name, as_=left_subquery)
            .with_(right_table_name, as_=right_subquery)
        )

    def _select_columns_to_sql(
        self,
        op: op_graph.op.SelectColumns,
    ) -> sqlglot.exp.Query:
        if len(op.columns) == 0:
            return self._empty_to_sql()

        sub_table_name = self._unique_name("sub_table")

        columns = (self._column(column) for column in op.columns)

        return (
            sqlglot.select(*columns)
            .from_(sub_table_name)
            .with_(sub_table_name, as_=self.parse(op.source))
        )

    def _limit_rows_to_sql(
        self,
        op: op_graph.op.LimitRows,
    ) -> sqlglot.exp.Query:
        return self.parse(op.source).limit(op.num_rows)

    def _order_by_to_sql(
        self,
        op: op_graph.op.OrderBy,
    ) -> sqlglot.exp.Query:
        table_name = self._unique_name("order_by_table")

        query = self.parse(op.source)
        if not isinstance(query, sqlglot.exp.Select):
            raise op_graph.OpParseError(
                "order_by needs to be executed on a select query"
            )

        columns = (self._column(name, table_name) for name in query.named_selects)

        order_by_columns = (
            self._column(column, table_name).desc()
            if op.desc
            else self._column(column, table_name)
            for column in op.columns
        )

        return (
            sqlglot.select(*columns)
            .order_by(*order_by_columns)
            .from_(table_name)
            .with_(table_name, as_=query)
        )

    def _row_filter_to_condition(  # noqa: C901
        self, row_filter: op_graph.RowFilter, table_name: sqlglot.exp.Identifier
    ) -> sqlglot.exp.Condition:
        match row_filter:
            case op_graph.row_filter.CompareColumnToLiteral():
                column = sqlglot.column(
                    sqlglot.to_identifier(row_filter.column_name, quoted=True),
                    table_name,
                )
                match row_filter.comparison_type:
                    case table_pb2.COMPARISON_TYPE_EQ:
                        return column.eq(row_filter.literal_as_py)
                    case table_pb2.COMPARISON_TYPE_NE:
                        return column.neq(row_filter.literal_as_py)
                    case table_pb2.COMPARISON_TYPE_LT:
                        return column < row_filter.literal_as_py
                    case table_pb2.COMPARISON_TYPE_GT:
                        return column > row_filter.literal_as_py
                    case table_pb2.COMPARISON_TYPE_LE:
                        return column <= row_filter.literal_as_py
                    case table_pb2.COMPARISON_TYPE_GE:
                        return column >= row_filter.literal_as_py
                    case _:
                        raise op_graph.OpParseError(
                            "unknown comparison type value in row filter",
                            value=row_filter.comparison_type,
                        )
            case op_graph.row_filter.CombineFilters():
                sub_filters = (
                    self._row_filter_to_condition(sub_filter, table_name)
                    for sub_filter in row_filter.row_filters
                )
                match row_filter.combination_op:
                    case table_pb2.LOGICAL_COMBINATION_ANY:
                        return functools.reduce(
                            lambda left, right: left.or_(right), sub_filters
                        )
                    case table_pb2.LOGICAL_COMBINATION_ALL:
                        return functools.reduce(
                            lambda left, right: left.and_(right), sub_filters
                        )
                    case _:
                        raise op_graph.OpParseError(
                            "unknown logical combination op value in row filter",
                            value=row_filter.combination_op,
                        )

    def _filter_rows_to_sql(
        self,
        op: op_graph.op.FilterRows,
    ) -> sqlglot.exp.Query:
        table_name = self._unique_name("filter_rows_table")
        where_cond = self._row_filter_to_condition(op.row_filter, table_name)
        sub_table = self.parse(op.source)
        columns = (
            self._column(column, table_name) for column in sub_table.named_selects
        )
        return (
            sqlglot.select(*columns)
            .from_(table_name)
            .where(where_cond)
            .with_(table_name, as_=sub_table)
        )

    def _distinct_rows_to_sql(
        self,
        op: op_graph.op.DistinctRows,
    ) -> sqlglot.exp.Query:
        table_name = self._unique_name("distinct_rows_table")
        sub_table = self.parse(op.source)
        columns = (
            self._column(column, table_name) for column in sub_table.named_selects
        )
        return (
            sqlglot.select(*columns)
            .distinct()
            .from_(table_name)
            .with_(table_name, as_=sub_table)
        )

    def _rollup_by_aggregation_to_sql(
        self, op: op_graph.op.RollupByAggregation
    ) -> sqlglot.exp.Query:
        table_name = self._unique_name("rollup_table")
        agg_mapping = {
            table_pb2.AGGREGATION_TYPE_MODE: "mode",
            table_pb2.AGGREGATION_TYPE_COUNT: "count",
            table_pb2.AGGREGATION_TYPE_MAX: "max",
            table_pb2.AGGREGATION_TYPE_MIN: "min",
            table_pb2.AGGREGATION_TYPE_AVG: "avg",
            table_pb2.AGGREGATION_TYPE_SUM: "sum",
        }

        match op.aggregation_type:
            case table_pb2.AGGREGATION_TYPE_MODE:
                agg = agg_mapping.get(op.aggregation_type)
                target_column_name = self._column(op.target_column_name)
                group_by_column_names = [
                    self._column(column) for column in op.group_by_column_names
                ]
                output_identifier = self._quote(
                    f"{agg}_{op.target_column_name}_{'_'.join(op.group_by_column_names)}"
                )
                expr = (
                    f"FIRST_VALUE({target_column_name}) OVER(PARTITION BY "
                    f"{','.join(str(i) for i in group_by_column_names)} "
                    f"ORDER BY COUNT(*) DESC) "
                    f"{output_identifier}"
                )
                query = (
                    sqlglot.select(*group_by_column_names, expr)
                    .distinct()
                    .group_by(*group_by_column_names, target_column_name)
                )
            case table_pb2.AGGREGATION_TYPE_COUNT:
                agg = agg_mapping.get(op.aggregation_type)
                target_column_name = self._column(op.target_column_name)
                group_by_column_names = [
                    self._column(column) for column in op.group_by_column_names
                ]
                output_identifier = self._quote(
                    f"{agg}_{op.target_column_name}_{'_'.join(op.group_by_column_names)}"
                )
                expr = sqlglot.func(
                    str(agg), sqlglot.func("DISTINCT", target_column_name)
                ).as_(output_identifier)
                query = (
                    sqlglot.select(*group_by_column_names, expr)
                    .distinct()
                    .group_by(*group_by_column_names)
                )
            case (
                table_pb2.AGGREGATION_TYPE_MAX
                | table_pb2.AGGREGATION_TYPE_MIN
                | table_pb2.AGGREGATION_TYPE_AVG
                | table_pb2.AGGREGATION_TYPE_SUM
            ):
                agg = agg_mapping.get(op.aggregation_type)
                target_column_name = self._column(op.target_column_name)
                group_by_column_names = [
                    self._column(column) for column in op.group_by_column_names
                ]
                output_identifier = self._quote(
                    f"{agg}_{op.target_column_name}_{'_'.join(op.group_by_column_names)}"
                )
                expr = sqlglot.func(str(agg), target_column_name).as_(output_identifier)
                query = (
                    sqlglot.select(*group_by_column_names, expr)
                    .distinct()
                    .group_by(*group_by_column_names)
                )
            case _:
                query = sqlglot.select()
        return query.from_(table_name).with_(table_name, as_=self.parse(op.source))

    def _empty_to_sql(self):
        # This returns a single column named by the null expression with no length
        # works for sqlite, and according to this discussion should work on postgres too
        # https://stackoverflow.com/questions/1456106/how-to-select-an-empty-result-set
        return sqlglot.select(sqlglot.exp.null()).limit(0)

    def _aggregate_columns_to_sql(self, op: op_graph.op.AggregateColumns):
        table_name = self._unique_name("aggregate_columns")
        query = self.parse(op.source)
        columns = (self._column(column) for column in op.column_names)
        match op.aggregation:
            case op_graph.aggregation.Min():
                query = sqlglot.select(
                    *(
                        sqlglot.exp.Min(
                            this=column,
                        ).as_(column.name)
                        for column in columns
                    ),
                )

            case op_graph.aggregation.Max():
                query = sqlglot.select(
                    *(
                        sqlglot.exp.Max(
                            this=column,
                        ).as_(column.name)
                        for column in columns
                    ),
                )
            case op_graph.aggregation.Mean():
                query = sqlglot.select(
                    *(
                        sqlglot.exp.Avg(
                            this=sqlglot.exp.TryCast(
                                this=column,
                                to=sqlglot.exp.DataType.build(
                                    sqlglot.exp.DataType.Type.DOUBLE
                                ),
                            )
                        ).as_(column.name)
                        for column in columns
                    ),
                )
            case op_graph.aggregation.Std():
                query = sqlglot.select(
                    *(
                        sqlglot.exp.Stddev(
                            this=sqlglot.exp.TryCast(
                                this=column,
                                to=sqlglot.exp.DataType.build(
                                    sqlglot.exp.DataType.Type.DOUBLE
                                ),
                            )
                        ).as_(column.name)
                        for column in columns
                    ),
                )
            case op_graph.aggregation.Quantile():
                query = sqlglot.select(
                    *(
                        sqlglot.exp.func(
                            "quantile_disc",
                            sqlglot.exp.TryCast(
                                this=column,
                                to=sqlglot.exp.DataType.build(
                                    sqlglot.exp.DataType.Type.DOUBLE
                                ),
                            ),
                            op.aggregation.quantile,
                            dialect="duckdb",
                        ).as_(column.name)
                        for column in columns
                    ),
                )
            case op_graph.aggregation.Count():
                query = sqlglot.select(
                    *(
                        sqlglot.exp.Count(
                            this=column,
                        ).as_(column.name)
                        for column in columns
                    ),
                )
            case op_graph.aggregation.NullCount():
                query = sqlglot.select(
                    *(
                        sqlglot.exp.Count(this=sqlglot.exp.Star())
                        - sqlglot.exp.Count(this=column).as_(column.name)
                        for column in columns
                    ),
                )
        return (
            query.from_(table_name)
            .with_(table_name, as_=self.parse(op.source))
            .limit(1)
        )

    def _union_to_sql(self, op: op_graph.op.Union):
        return functools.reduce(
            lambda left, right: left.union(right, distinct=op.distinct),
            (self.parse(t) for t in op.sources()),
        )

    def parse(  # noqa: C901
        self,
        op: op_graph.Op,
    ) -> sqlglot.exp.Query:
        """Parse the op log into a sql query."""
        if not can_be_sql_computed(op, recursive=False):
            raise InvalidArgumentError(
                "table op not computable via SQL", op_type=op.__class__.__name__
            )

        match op:
            case op_graph.op.SelectFromStaging():
                return self._select_from_staging_to_sql(op)
            case op_graph.op.SelectFromVectorStaging():
                return self._select_from_vector_staging_to_sql(op)
            case op_graph.op.RenameColumns():
                return self._rename_columns_to_sql(op)
            case op_graph.op.Join():
                return self._join_to_sql(op)
            case op_graph.op.SelectColumns():
                return self._select_columns_to_sql(op)
            case op_graph.op.LimitRows():
                return self._limit_rows_to_sql(op)
            case op_graph.op.OrderBy():
                return self._order_by_to_sql(op)
            case op_graph.op.FilterRows():
                return self._filter_rows_to_sql(op)
            case op_graph.op.DistinctRows():
                return self._distinct_rows_to_sql(op)
            case (
                op_graph.op.SetMetadata()
                | op_graph.op.UpdateMetadata()
                | op_graph.op.RemoveFromMetadata()
                | op_graph.op.UpdateFeatureTypes()
            ):
                return self.parse(op.source)
            case op_graph.op.RollupByAggregation() as op:
                return self._rollup_by_aggregation_to_sql(op)
            case op_graph.op.Empty():
                return self._empty_to_sql()
            case op_graph.op.AggregateColumns():
                return self._aggregate_columns_to_sql(op)
            case op_graph.op.Union():
                return self._union_to_sql(op)


def parse_op_graph(
    op: op_graph.Op | table_pb2.TableComputeOp,
    make_staging_query: StagingQueryGenerator,
    make_vector_search_query: VectorSearchQueryGenerator,
) -> sqlglot.exp.Query:
    """Parse the op log into a sql query."""
    if isinstance(op, table_pb2.TableComputeOp):
        op = op_graph.op.from_proto(op)

    return _OpLogParser(make_staging_query, make_vector_search_query).parse(op)
