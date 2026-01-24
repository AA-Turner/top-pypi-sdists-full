#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import copy
from dataclasses import dataclass

import pyspark.sql.connect.proto.relations_pb2 as relation_proto

import snowflake.snowpark.functions as snowpark_fn
from snowflake import snowpark
from snowflake.snowpark import Column
from snowflake.snowpark._internal.analyzer.unary_expression import Alias
from snowflake.snowpark.types import DataType, StructType
from snowflake.snowpark_connect.column_name_handler import (
    make_column_names_snowpark_compatible,
)
from snowflake.snowpark_connect.column_qualifier import ColumnQualifier
from snowflake.snowpark_connect.dataframe_container import (
    AggregateMetadata,
    DataFrameContainer,
)
from snowflake.snowpark_connect.expression.literal import get_literal_field_and_name
from snowflake.snowpark_connect.expression.map_expression import (
    map_single_column_expression,
)
from snowflake.snowpark_connect.expression.typer import ExpressionTyper
from snowflake.snowpark_connect.relation.map_relation import map_relation
from snowflake.snowpark_connect.relation.output_struct_utils import (
    unpack_struct_output_to_container,
)
from snowflake.snowpark_connect.relation.utils import (
    create_pivot_column_condition,
    map_pivot_value_to_spark_column_name,
)
from snowflake.snowpark_connect.typed_column import TypedColumn
from snowflake.snowpark_connect.utils import expression_transformer
from snowflake.snowpark_connect.utils.context import (
    grouping_by_scala_udf_key,
    set_current_grouping_columns,
)


def map_group_by_aggregate(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Groups the DataFrame using the specified columns.

    Aggregations come in as expressions, which are mapped to `snowpark.Column`
    objects.
    """
    input_df_container, columns = map_aggregate_helper(rel)
    input_df_actual = input_df_container.dataframe

    if len(columns.grouping_expressions()) == 0:
        result = input_df_actual.agg(*columns.aggregation_expressions())
    else:
        result = input_df_actual.group_by(*columns.grouping_expressions()).agg(
            *columns.aggregation_expressions()
        )

    for rel_aggregate_expression, aggregate_original_column in zip(
        rel.aggregate.aggregate_expressions, columns.aggregation_columns
    ):
        aggregate_original_data_type = aggregate_original_column.data_type

        if not (
            rel_aggregate_expression.HasField("unresolved_function")
            and rel_aggregate_expression.unresolved_function.function_name == "reduce"
        ) or not isinstance(aggregate_original_data_type, StructType):
            continue

        if not result.columns or len(result.columns) != 1:
            raise ValueError(
                "Expected result DataFrame to have exactly one column for reduce(StructType)"
            )

        return unpack_struct_output_to_container(
            df=result,
            output_column_name=result.columns[0],
            output_type=aggregate_original_data_type,
            spark_field_names=input_df_container.column_map.get_spark_columns(),
        )

    # Store aggregate metadata for ORDER BY resolution
    aggregate_metadata = AggregateMetadata(
        input_column_map=input_df_container.column_map,
        input_dataframe=input_df_actual,
        grouping_expressions=list(rel.aggregate.grouping_expressions),
        aggregate_expressions=list(rel.aggregate.aggregate_expressions),
        spark_columns=columns.spark_names(),
        raw_aggregations=[
            (col.spark_name, TypedColumn(col.expression, col.data_type))
            for col in columns.aggregation_columns
        ],
    )

    return DataFrameContainer.create_with_column_mapping(
        dataframe=result,
        spark_column_names=columns.spark_names(),
        snowpark_column_names=columns.snowpark_names(),
        snowpark_column_types=columns.data_types(),
        column_qualifiers=columns.get_qualifiers(),
        parent_column_name_map=input_df_container.column_map,
        equivalent_snowpark_names=columns.get_equivalent_snowpark_names(),
        aggregate_metadata=aggregate_metadata,
    )


def map_rollup_aggregate(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Create a multidimensional rollup for the current DataFrame using the specified columns.

    Aggregations come in as expressions, which are mapped to `snowpark.Column`
    objects.
    """
    input_container, columns = map_aggregate_helper(rel)
    input_df_actual = input_container.dataframe

    if len(columns.grouping_expressions()) == 0:
        result = input_df_actual.agg(*columns.aggregation_expressions())
    else:
        result = input_df_actual.rollup(*columns.grouping_expressions()).agg(
            *columns.aggregation_expressions()
        )

    # NOTE: Do NOT attach aggregate_metadata for ROLLUP
    # Spark does not allow ORDER BY to reference pre-aggregation columns for ROLLUP
    # Only regular GROUP BY supports this

    return DataFrameContainer.create_with_column_mapping(
        dataframe=result,
        spark_column_names=columns.spark_names(),
        snowpark_column_names=columns.snowpark_names(),
        snowpark_column_types=columns.data_types(),
        column_qualifiers=columns.get_qualifiers(),
        parent_column_name_map=input_container.column_map,
        equivalent_snowpark_names=columns.get_equivalent_snowpark_names(),
    )


def map_cube_aggregate(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Create a multidimensional cube for the current DataFrame using the specified columns.

    Aggregations come in as expressions, which are mapped to `snowpark.Column`
    objects.
    """
    input_container, columns = map_aggregate_helper(rel)
    input_df_actual = input_container.dataframe

    if len(columns.grouping_expressions()) == 0:
        result = input_df_actual.agg(*columns.aggregation_expressions())
    else:
        result = input_df_actual.cube(*columns.grouping_expressions()).agg(
            *columns.aggregation_expressions()
        )

    # NOTE: Do NOT attach aggregate_metadata for CUBE
    # Spark does not allow ORDER BY to reference pre-aggregation columns for CUBE
    # Only regular GROUP BY supports this

    return DataFrameContainer.create_with_column_mapping(
        dataframe=result,
        spark_column_names=columns.spark_names(),
        snowpark_column_names=columns.snowpark_names(),
        snowpark_column_types=columns.data_types(),
        column_qualifiers=columns.get_qualifiers(),
        parent_column_name_map=input_container.column_map,
        equivalent_snowpark_names=columns.get_equivalent_snowpark_names(),
    )


def map_pivot_aggregate(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Pivots a column of the current DataFrame and performs the specified aggregation.

    There are 2 versions of the pivot function: one that requires the caller to specify the list of the distinct values
    to pivot on and one that does not.
    """
    input_container, columns = map_aggregate_helper(rel, pivot=True, skip_alias=True)
    input_df_actual = input_container.dataframe

    pivot_column = map_single_column_expression(
        rel.aggregate.pivot.col,
        input_container.column_map,
        ExpressionTyper(input_df_actual),
    )
    pivot_values = [
        get_literal_field_and_name(lit)[0] for lit in rel.aggregate.pivot.values
    ]

    if not pivot_values:
        distinct_col_values = (
            input_df_actual.select(pivot_column[1].col)
            .distinct()
            .sort(snowpark_fn.asc_nulls_first(pivot_column[1].col))
            .collect()
        )
        pivot_values = [
            row[0].as_dict() if isinstance(row[0], snowpark.Row) else row[0]
            for row in distinct_col_values
        ]

    agg_expressions = columns.aggregation_expressions(unalias=True)

    spark_col_names = []
    aggregations = []
    final_pivot_names = []
    grouping_columns_qualifiers = []
    grouping_eq_snowpark_names = []

    grouping_columns = columns.grouping_expressions()
    if grouping_columns:
        for col in grouping_columns:
            snowpark_name = col.get_name()
            spark_col_name = input_container.column_map.get_spark_column_name_from_snowpark_column_name(
                snowpark_name
            )
            qualifiers = input_container.column_map.get_qualifiers_for_snowpark_column(
                snowpark_name
            )
            grouping_columns_qualifiers.append(qualifiers)
            spark_col_names.append(spark_col_name)
            grouping_eq_snowpark_names.append(
                input_container.column_map.get_equivalent_snowpark_names_for_snowpark_name(
                    snowpark_name
                )
            )

    for pv_value in pivot_values:
        pv_value_spark, pv_is_null = map_pivot_value_to_spark_column_name(pv_value)

        for i, agg_expression in enumerate(agg_expressions):
            agg_fun_expr = copy.deepcopy(agg_expression._expr1)

            condition = create_pivot_column_condition(
                pivot_column[1].col,
                pv_value,
                pv_is_null,
                pivot_column[1].typ if isinstance(pv_value, (list, dict)) else None,
            )

            expression_transformer.inject_condition_to_all_agg_functions(
                agg_fun_expr, condition
            )

            curr_expression = Column(agg_fun_expr)

            spark_col_name = (
                f"{pv_value_spark}_{columns.aggregation_columns[i].spark_name}"
                if len(agg_expressions) > 1
                else f"{pv_value_spark}"
            )

            snowpark_col_name = make_column_names_snowpark_compatible(
                [spark_col_name],
                rel.common.plan_id,
                len(grouping_columns) + len(agg_expressions),
            )[0]

            curr_expression = curr_expression.alias(snowpark_col_name)

            aggregations.append(curr_expression)
            spark_col_names.append(spark_col_name)
            final_pivot_names.append(snowpark_col_name)

    result_df = (
        input_df_actual.group_by(*grouping_columns)
        .agg(*aggregations)
        .select(*grouping_columns, *final_pivot_names)
    )

    return DataFrameContainer.create_with_column_mapping(
        dataframe=result_df,
        spark_column_names=spark_col_names,
        snowpark_column_names=result_df.columns,
        snowpark_column_types=[
            result_df.schema.fields[idx].datatype
            for idx, _ in enumerate(result_df.columns)
        ],
        column_qualifiers=grouping_columns_qualifiers
        + [set() for _ in final_pivot_names],
        parent_column_name_map=input_container.column_map,
        equivalent_snowpark_names=grouping_eq_snowpark_names
        + [set() for _ in final_pivot_names],
    )


@dataclass(frozen=True)
class _ColumnMetadata:
    expression: snowpark.Column
    spark_name: str
    snowpark_name: str
    data_type: DataType
    qualifiers: set[ColumnQualifier]
    equivalent_snowpark_names: set[str]


@dataclass(frozen=True)
class _Columns:
    grouping_columns: list[_ColumnMetadata]
    aggregation_columns: list[_ColumnMetadata]
    can_infer_schema: bool

    def grouping_expressions(self) -> list[snowpark.Column]:
        return [col.expression for col in self.grouping_columns]

    def aggregation_expressions(self, unalias: bool = False) -> list[snowpark.Column]:
        def _unalias(col: snowpark.Column) -> snowpark.Column:
            if unalias and hasattr(col, "_expr1") and isinstance(col._expr1, Alias):
                return _unalias(Column(col._expr1.child))
            else:
                return col

        return [_unalias(col.expression) for col in self.aggregation_columns]

    def expressions(self) -> list[snowpark.Column]:
        return self.grouping_expressions() + self.aggregation_expressions()

    def snowpark_names(self) -> list[str]:
        return [
            col.snowpark_name
            for col in self.grouping_columns + self.aggregation_columns
            if col.snowpark_name is not None
        ]

    def spark_names(self) -> list[str]:
        return [
            col.spark_name for col in self.grouping_columns + self.aggregation_columns
        ]

    def get_qualifiers(self) -> list[set[ColumnQualifier]]:
        return [
            col.qualifiers for col in self.grouping_columns + self.aggregation_columns
        ]

    def data_types(self) -> list[DataType] | None:
        if not self.can_infer_schema:
            return None
        return [
            col.data_type
            for col in self.grouping_columns + self.aggregation_columns
            if col.data_type is not None
        ]

    def get_equivalent_snowpark_names(self) -> list[set[str]]:
        return [
            col.equivalent_snowpark_names
            for col in self.grouping_columns + self.aggregation_columns
        ]


def map_aggregate_helper(
    rel: relation_proto.Relation, pivot: bool = False, skip_alias: bool = False
):
    input_container = map_relation(rel.aggregate.input)
    input_df = input_container.dataframe
    grouping_expressions = rel.aggregate.grouping_expressions
    expressions = rel.aggregate.aggregate_expressions
    groupings: list[_ColumnMetadata] = []
    aggregations: list[_ColumnMetadata] = []

    typer = ExpressionTyper(input_df)
    schema_inferrable = True

    for exp in grouping_expressions:
        with grouping_by_scala_udf_key(
            exp.WhichOneof("expr_type") == "common_inline_user_defined_function"
            and exp.common_inline_user_defined_function.scalar_scala_udf is not None
        ):
            new_name, snowpark_column = map_single_column_expression(
                exp, input_container.column_map, typer
            )

        alias = make_column_names_snowpark_compatible(
            [new_name], rel.common.plan_id, len(groupings)
        )[0]

        equivalent_snowpark_names = (
            input_container.column_map.get_equivalent_snowpark_names_for_snowpark_name(
                snowpark_column.col.get_name()
            )
        )

        groupings.append(
            _ColumnMetadata(
                snowpark_column.col if skip_alias else snowpark_column.col.alias(alias),
                new_name,
                None if skip_alias else alias,
                None if pivot else snowpark_column.typ,
                qualifiers=snowpark_column.get_qualifiers(),
                equivalent_snowpark_names=equivalent_snowpark_names,
            )
        )

    grouping_cols = [g.spark_name for g in groupings]
    set_current_grouping_columns(grouping_cols)

    for exp in expressions:
        new_name, snowpark_column = map_single_column_expression(
            exp, input_container.column_map, typer
        )
        alias = make_column_names_snowpark_compatible(
            [new_name], rel.common.plan_id, len(groupings) + len(aggregations)
        )[0]

        def type_agg_expr(
            agg_exp: TypedColumn, schema_inferrable: bool
        ) -> DataType | None:
            if pivot or not schema_inferrable:
                return None
            try:
                return agg_exp.typ
            except Exception:
                # This type used for schema inference optimization purposes.
                # typer may not be able to infer the type of some expressions
                # in that case we return None, and the optimization will not be applied.
                return None

        agg_col_typ = type_agg_expr(snowpark_column, schema_inferrable)
        if agg_col_typ is None:
            schema_inferrable = False

        aggregations.append(
            _ColumnMetadata(
                snowpark_column.col if skip_alias else snowpark_column.col.alias(alias),
                new_name,
                None if skip_alias else alias,
                agg_col_typ,
                qualifiers=set(),
                equivalent_snowpark_names=set(),
            )
        )

    return (
        input_container,
        _Columns(
            grouping_columns=groupings,
            aggregation_columns=aggregations,
            can_infer_schema=schema_inferrable,
        ),
    )
