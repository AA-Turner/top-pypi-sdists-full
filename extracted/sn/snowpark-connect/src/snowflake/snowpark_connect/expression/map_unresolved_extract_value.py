#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import uuid
from collections import defaultdict

import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto
from pyspark.errors.exceptions.connect import AnalysisException

import snowflake.snowpark.functions as snowpark_fn
from snowflake.snowpark import Session
from snowflake.snowpark._internal.analyzer.expression import Literal
from snowflake.snowpark.types import (
    ArrayType,
    MapType,
    NullType,
    StructType,
    VariantType,
    _IntegralType,
)
from snowflake.snowpark_connect.column_name_handler import ColumnNameMap
from snowflake.snowpark_connect.config import global_config
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
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


def _is_array_struct_field_access(
    child_typed_column: TypedColumn, extract_typed_column: TypedColumn
) -> bool:
    """True when .getField(string) targets an ArrayType(StructType(...)).

    Spark extracts the named field from every element, producing
    ArrayType(field_type) via TRANSFORM.
    """
    child_types = child_typed_column.types
    return (
        child_types is not None
        and len(child_types) == 1
        and isinstance(child_types[0], ArrayType)
        and isinstance(child_types[0].element_type, StructType)
        and isinstance(extract_typed_column.col._expression, Literal)
        and isinstance(extract_typed_column.col._expression.value, str)
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
    display_child_name = child_typed_column._spark_struct_field_path or child_name
    # Spark respects "spark.sql.caseSensitive" for struct fields
    # map keys are compared as-is
    if global_config.spark_sql_caseSensitive or isinstance(
        child_typed_column.typ, MapType
    ):
        extract_fn = snowpark_fn.get
    else:
        extract_fn = snowpark_fn.get_ignore_case

    is_array = _check_if_array_type(extract_typed_column, child_typed_column)
    is_array_struct_field = _is_array_struct_field_access(
        child_typed_column, extract_typed_column
    )

    if isinstance(child_typed_column.typ, StructType) or is_array_struct_field:
        spark_function_name = f"{display_child_name}.{extract_name}"
    else:
        spark_function_name = f"{display_child_name}[{extract_name}]"

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

    elif is_array_struct_field:
        var_name = f"item_{uuid.uuid4().hex[:8]}"
        inner_exp = extract_fn(snowpark_fn.sql_expr(var_name), extract_typed_column.col)
        inner_exp = snowpark_fn.iff(
            snowpark_fn.call_function(
                "IS_NULL_VALUE", snowpark_fn.to_variant(inner_exp)
            ),
            snowpark_fn.lit(None),
            inner_exp,
        )
        analyzer = Session.get_active_session()._analyzer
        inner_sql = analyzer.analyze(inner_exp._expression, defaultdict())
        result_exp = snowpark_fn.call_function(
            "transform",
            child_typed_column.col,
            snowpark_fn.sql_expr(f"{var_name} -> {inner_sql}"),
        )

    else:
        # VariantType is intentionally accepted here even though it is not named
        # in the error message below: a Snowflake VARIANT can hold any of the
        # complex shapes (object/array), so extraction is valid. The message
        # lists only STRUCT/ARRAY/MAP to stay byte-for-byte identical to Spark.
        if (
            global_config.snowpark_connect_enableInputTypeCheckForExtractValueFunction
            and not isinstance(
                child_typed_column.typ,
                (StructType, ArrayType, MapType, VariantType),
            )
        ):
            # Spark renders NullType as "VOID" in this message; Snowpark's
            # simpleString() returns "null", so special-case it to stay D0.
            if isinstance(child_typed_column.typ, NullType):
                base_type_name = "VOID"
            else:
                base_type_name = child_typed_column.typ.simpleString().upper()
            exception = AnalysisException(
                f"[INVALID_EXTRACT_BASE_FIELD_TYPE] Can't extract a value from "
                f'"{display_child_name}". '
                f"Need a complex type [STRUCT, ARRAY, MAP] but got "
                f'"{base_type_name}".'
            )
            attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
            raise exception

        result_exp = extract_fn(child_typed_column.col, extract_typed_column.col)
        # Snowflake's GET/GET_IGNORE_CASE on structured types may return a value
        # where JSON null != SQL NULL. Spark treats null struct fields as SQL NULL,
        # so we convert JSON null -> SQL NULL here to match Spark semantics.
        if isinstance(child_typed_column.typ, StructType):
            result_exp = snowpark_fn.iff(
                snowpark_fn.call_function(
                    "IS_NULL_VALUE", snowpark_fn.to_variant(result_exp)
                ),
                snowpark_fn.lit(None),
                result_exp,
            )

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
        elif is_array_struct_field:
            element_struct = child_typed_column.typ.element_type
            field_name = extract_typed_column.col._expression.value
            if not global_config.spark_sql_caseSensitive:
                field_name = field_name.lower()
            for f in element_struct.fields:
                name = (
                    f.name if global_config.spark_sql_caseSensitive else f.name.lower()
                )
                if name == field_name:
                    return [ArrayType(f.datatype)]
            return typer.type(result_exp)
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
