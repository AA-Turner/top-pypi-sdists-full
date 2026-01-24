#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto

import snowflake.snowpark.functions as snowpark_fn
from snowflake.snowpark._internal.analyzer.expression import Literal
from snowflake.snowpark.types import (
    ArrayType,
    MapType,
    NullType,
    StructType,
    _IntegralType,
)
from snowflake.snowpark_connect.column_name_handler import ColumnNameMap
from snowflake.snowpark_connect.config import global_config
from snowflake.snowpark_connect.expression.typer import ExpressionTyper
from snowflake.snowpark_connect.typed_column import TypedColumn


def _check_if_array_type(
    child_typed_column: TypedColumn, extract_typed_column: TypedColumn
):
    extract_typed_column_type = extract_typed_column.types
    container_type = child_typed_column.types
    return (
        len(extract_typed_column_type) == 1
        and isinstance(extract_typed_column_type[0], ArrayType)
        and len(container_type) == 1
        and isinstance(container_type[0], (_IntegralType, NullType))
    )


def map_unresolved_extract_value(
    exp: expressions_proto.Expression,
    column_mapping: ColumnNameMap,
    typer: ExpressionTyper,
) -> tuple[str, TypedColumn]:
    from snowflake.snowpark_connect.expression.map_expression import (
        map_single_column_expression,
    )

    child_name, child_typed_column = map_single_column_expression(
        exp.unresolved_extract_value.child, column_mapping, typer
    )
    extract_name, extract_typed_column = map_single_column_expression(
        exp.unresolved_extract_value.extraction,
        column_mapping,
        typer,
    )
    spark_function_name = (
        f"{child_name}.{extract_name}"
        if isinstance(child_typed_column.typ, StructType)
        else f"{child_name}[{extract_name}]"
    )
    # Spark respects "spark.sql.caseSensitive" for struct fields
    # map keys are compared as-is
    if global_config.spark_sql_caseSensitive or isinstance(
        child_typed_column.typ, MapType
    ):
        extract_fn = snowpark_fn.get
    else:
        extract_fn = snowpark_fn.get_ignore_case
    is_array = _check_if_array_type(extract_typed_column, child_typed_column)
    if is_array:
        if isinstance(extract_typed_column.typ, NullType):
            result_exp = snowpark_fn.lit(None)
        else:
            if (
                isinstance(extract_typed_column.col._expression, Literal)
                and extract_typed_column.col._expression.value is not None
            ):
                # Using NULL in NVL triggers Snowflake Optimiser to be much more efficient comparing to using a number.
                # This unfortunately has a side effect of throwing and error when attempting to get the item from array.
                # That's why we need to have a separate branch for fetching Nullable literals and non-literal expressions.
                extracted_index = snowpark_fn.nvl(
                    extract_typed_column.col, snowpark_fn.lit(None)
                )
            else:
                extracted_index = snowpark_fn.nvl(
                    extract_typed_column.col, snowpark_fn.lit(0)
                )

            result_exp = snowpark_fn.when(
                snowpark_fn.nvl(
                    (extract_typed_column.col < 0)
                    | (extract_typed_column.col > 2_147_483_647),
                    snowpark_fn.lit(True),
                ),
                snowpark_fn.lit(None),
            ).otherwise(
                snowpark_fn.get(
                    child_typed_column.col,
                    extracted_index,
                )
            )

    else:
        result_exp = extract_fn(child_typed_column.col, extract_typed_column.col)

    spark_sql_ansi_enabled = global_config.spark_sql_ansi_enabled

    if spark_sql_ansi_enabled and is_array:
        invalid_array_index = (
            snowpark_fn.array_size(child_typed_column.col) <= extract_typed_column.col
        ) | (extract_typed_column.col < 0)
        result_exp = snowpark_fn.when(
            invalid_array_index,
            child_typed_column.col.getItem("[snowpark_connect::INVALID_ARRAY_INDEX]"),
        ).otherwise(result_exp)

    def _get_extracted_value_type():
        if is_array:
            return [child_typed_column.typ.element_type]
        elif isinstance(child_typed_column.typ, MapType):
            return [child_typed_column.typ.value_type]
        elif (
            isinstance(child_typed_column.typ, StructType)
            and isinstance(extract_typed_column.col._expr1, Literal)
            and isinstance(extract_typed_column.col._expr1.value, str)
        ):
            struct = dict(
                {
                    (
                        f.name
                        if global_config.spark_sql_caseSensitive
                        else f.name.lower(),
                        f.datatype,
                    )
                    for f in child_typed_column.typ.fields
                }
            )
            key = extract_typed_column.col._expr1.value
            key = key if global_config.spark_sql_caseSensitive else key.lower()

            return [struct[key]] if key in struct else typer.type(result_exp)
        return typer.type(result_exp)

    return spark_function_name, TypedColumn(result_exp, _get_extracted_value_type)
