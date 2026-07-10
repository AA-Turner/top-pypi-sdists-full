#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import snowflake.snowpark.functions as snowpark_fn
from snowflake import snowpark
from snowflake.snowpark.types import DataType, StructType
from snowflake.snowpark_connect.column_name_handler import make_unique_snowpark_name
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.typed_column import FieldType
from snowflake.snowpark_connect.utils.jvm_udf_utils import (
    decode_jvm_udf_result,
    is_decomposable_struct,
)


def unpack_struct_output_to_container(
    df: snowpark.DataFrame,
    output_column_name: str,
    output_type: DataType,
    spark_field_names: list[str] | None = None,
    cast_fields: bool = False,
    non_struct_spark_name: str | None = None,
) -> DataFrameContainer:
    """
    Unpack a struct column into separate columns and create a DataFrameContainer.

    If the output type is a StructType, extracts each field as a separate column.
    Otherwise, creates a single column with the output.
    """
    if isinstance(output_type, StructType):
        if spark_field_names is None:
            spark_field_names = [field.name for field in output_type.fields]

        field_types = [
            FieldType(field.datatype, field.nullable) for field in output_type.fields
        ]
        output_snowpark_names = [
            make_unique_snowpark_name(name) for name in spark_field_names
        ]

        output_col = snowpark_fn.col(output_column_name)
        cols = []
        for spark_name, snowpark_name, field_type in zip(
            spark_field_names, output_snowpark_names, field_types
        ):
            col_expr = snowpark_fn.get(output_col, snowpark_fn.lit(spark_name))
            if cast_fields:
                col_expr = col_expr.cast(field_type.datatype)
            cols.append(col_expr.alias(snowpark_name))

        if cols:
            df = df.select(*cols)

        return DataFrameContainer.create_with_column_mapping(
            dataframe=df,
            spark_column_names=spark_field_names,
            snowpark_column_names=output_snowpark_names,
            snowpark_column_types=field_types,
        )

    non_struct_snowpark_name = make_unique_snowpark_name(non_struct_spark_name)

    return DataFrameContainer.create_with_column_mapping(
        dataframe=df.select(
            snowpark_fn.col(output_column_name)
            .cast(output_type)
            .alias(non_struct_snowpark_name)
        ),
        spark_column_names=[non_struct_spark_name],
        snowpark_column_names=[non_struct_snowpark_name],
        snowpark_column_types=[output_type],
    )


def unpack_java_udtf_output_to_container(
    df: snowpark.DataFrame,
    output_type: DataType,
    non_struct_spark_name: str,
    java_udtf_prefix: str,
) -> DataFrameContainer:
    """
    Unpack Java UDTF output columns into a DataFrameContainer.

    Decomposable structs: reads per-field native columns (C0, C1, ...) directly.
    All other types: delegates to unpack_struct_output_to_container, which uses GET()
    to extract fields from a single VARIANT output column.
    """
    if is_decomposable_struct(output_type):
        fields = output_type.fields
        out_spark_names = [f.name for f in fields]
        out_sf_names = [make_unique_snowpark_name(n) for n in out_spark_names]
        selected = df.select(
            *[
                decode_jvm_udf_result(
                    snowpark_fn.col(java_udtf_prefix + f"C{i}"), f.datatype
                ).alias(sf_name)
                for i, (f, sf_name) in enumerate(zip(fields, out_sf_names))
            ]
        )
        return DataFrameContainer.create_with_column_mapping(
            dataframe=selected,
            spark_column_names=out_spark_names,
            snowpark_column_names=out_sf_names,
            snowpark_column_types=[FieldType(f.datatype, f.nullable) for f in fields],
        )

    output_col_name = java_udtf_prefix + "C1"
    out_snowpark_name = make_unique_snowpark_name(non_struct_spark_name)
    # For non-struct output types: native scalars (primitives, temporal epoch) are
    # reconstructed directly via decode_jvm_udf_result; VARIANT-backed types (ArrayType,
    # MapType) also take this path via .cast(dt) inside decode_jvm_udf_result.
    # Only StructType uses unpack_struct_output_to_container for field-level GET().
    if not isinstance(output_type, StructType):
        return DataFrameContainer.create_with_column_mapping(
            dataframe=df.select(
                decode_jvm_udf_result(
                    snowpark_fn.col(output_col_name), output_type
                ).alias(out_snowpark_name)
            ),
            spark_column_names=[non_struct_spark_name],
            snowpark_column_names=[out_snowpark_name],
            snowpark_column_types=[output_type],
        )

    return unpack_struct_output_to_container(
        df=df,
        output_column_name=output_col_name,
        output_type=output_type,
        cast_fields=True,
        non_struct_spark_name=non_struct_spark_name,
    )
