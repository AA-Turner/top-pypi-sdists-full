#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import snowflake.snowpark.functions as snowpark_fn
from snowflake import snowpark
from snowflake.snowpark.types import DataType, StructType
from snowflake.snowpark_connect.column_name_handler import make_unique_snowpark_name
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer


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

        field_types = [field.datatype for field in output_type.fields]
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
                col_expr = col_expr.cast(field_type)
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
