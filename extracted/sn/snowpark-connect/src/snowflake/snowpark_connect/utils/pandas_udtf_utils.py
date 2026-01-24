#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from typing import Any, Callable, Iterator

import cloudpickle
import pandas as pd
import pyarrow as pa
from pyspark.sql.connect.proto.expressions_pb2 import CommonInlineUserDefinedFunction

import snowflake.snowpark.functions as snowpark_fn
from snowflake import snowpark
from snowflake.snowpark.types import IntegerType, PandasDataFrameType, StructType

# Removed error imports to avoid UDF serialization issues
# from snowflake.snowpark_connect.error.error_codes import ErrorCodes
# from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code


def get_map_in_arrow_udtf(
    user_function: Callable,
    spark_column_names: list[str],
    output_column_names: list[str],
) -> Any:
    """
    Create and return a MapInArrowUDTF class with the given parameters.

    Args:
        user_function: Arrow function that processes RecordBatch iterators
        spark_column_names: List of spark column names of the given dataframe.
        output_column_names: List of expected output column names

    Returns:
        MapInArrowUDTF class that can be used with pandas_udtf
    """

    class MapInArrowUDTF:
        def __init__(self) -> None:
            self.user_function = user_function
            self.output_column_names = output_column_names
            self.spark_column_names = spark_column_names

        def end_partition(self, df: pd.DataFrame):
            if df.empty:
                empty_df = pd.DataFrame(columns=self.output_column_names)
                yield empty_df
                return

            df_without_dummy = df.drop(
                columns=["_DUMMY_PARTITION_KEY"], errors="ignore"
            )
            df_without_dummy.columns = self.spark_column_names

            # Convert pandas DataFrame to Arrow format
            table = pa.Table.from_pandas(df_without_dummy, preserve_index=False)
            batch_iterator = table.to_batches()

            result_iterator = self.user_function(batch_iterator)

            result_batches = []

            if not isinstance(result_iterator, Iterator) and not hasattr(
                result_iterator, "__iter__"
            ):
                raise RuntimeError(
                    f"[snowpark_connect::type_mismatch] Return type of the user-defined function should be "
                    f"iterator of pyarrow.RecordBatch, but is {type(result_iterator).__name__}"
                )

            for batch in result_iterator:
                if not isinstance(batch, pa.RecordBatch):
                    raise RuntimeError(
                        f"[snowpark_connect::type_mismatch] Return type of the user-defined function should "
                        f"be iterator of pyarrow.RecordBatch, but is iterator of {type(batch).__name__}"
                    )
                if batch.num_rows > 0:
                    result_batches.append(batch)

            if result_batches:
                combined_table = pa.Table.from_batches(result_batches)
                result_df = combined_table.to_pandas()
                yield result_df
            else:
                empty_df = pd.DataFrame(columns=self.output_column_names)
                yield empty_df

    return MapInArrowUDTF


def create_pandas_udtf(
    udtf_proto: CommonInlineUserDefinedFunction,
    spark_column_names: list[str],
    input_schema: StructType,
    return_schema: StructType,
):
    user_function, _ = cloudpickle.loads(udtf_proto.python_udf.command)
    output_column_names = [field.name for field in return_schema.fields]
    output_column_original_names = [
        field.original_column_identifier for field in return_schema.fields
    ]

    class MapPandasUDTF:
        def __init__(self) -> None:
            self.user_function = user_function
            self.output_column_names = output_column_names
            self.spark_column_names = spark_column_names
            self.output_column_original_names = output_column_original_names

        def end_partition(self, df: pd.DataFrame):
            if df.empty:
                empty_df = pd.DataFrame(columns=self.output_column_names)
                yield empty_df
                return

            df_without_dummy = df.drop(
                columns=["_DUMMY_PARTITION_KEY"], errors="ignore"
            )
            df_without_dummy.columns = self.spark_column_names
            result_iterator = self.user_function(
                [pd.DataFrame([row]) for _, row in df_without_dummy.iterrows()]
            )

            if not isinstance(result_iterator, Iterator) and not hasattr(
                result_iterator, "__iter__"
            ):
                raise RuntimeError(
                    f"[snowpark_connect::type_mismatch] Return type of the user-defined function should be "
                    f"iterator of pandas.DataFrame, but is {type(result_iterator).__name__}"
                )

            output_df = pd.concat(result_iterator)
            generated_output_column_names = list(output_df.columns)

            missing_columns = []
            for original_column in self.output_column_original_names:
                if original_column not in generated_output_column_names:
                    missing_columns.append(original_column)

            if missing_columns:
                unexpected_columns = [
                    column
                    for column in generated_output_column_names
                    if column not in self.output_column_original_names
                ]
                raise RuntimeError(
                    f"[snowpark_connect::invalid_operation] [RESULT_COLUMNS_MISMATCH_FOR_PANDAS_UDF] Column names of the returned pandas.DataFrame do not match specified schema. Missing: {', '.join(sorted(missing_columns))}. Unexpected: {', '.join(sorted(unexpected_columns))}"
                    "."
                )
            reordered_df = output_df[self.output_column_original_names]
            reordered_df.columns = self.output_column_names
            yield reordered_df

    return snowpark_fn.pandas_udtf(
        MapPandasUDTF,
        output_schema=PandasDataFrameType(
            [field.datatype for field in return_schema.fields],
            [field.name for field in return_schema.fields],
        ),
        input_types=[
            PandasDataFrameType(
                [field.datatype for field in input_schema.fields] + [IntegerType()]
            )
        ],
        input_names=[field.name for field in input_schema.fields]
        + ["_DUMMY_PARTITION_KEY"],
        name="map_pandas_udtf",
        replace=True,
        packages=["pandas"],
        is_permanent=False,
    )


def create_pandas_udtf_with_arrow(
    udtf_proto: CommonInlineUserDefinedFunction,
    spark_column_names: list[str],
    input_schema: StructType,
    return_schema: StructType,
) -> str | snowpark.udtf.UserDefinedTableFunction:

    user_function, _ = cloudpickle.loads(udtf_proto.python_udf.command)
    output_column_names = [field.name for field in return_schema.fields]

    MapInArrowUDTF = get_map_in_arrow_udtf(
        user_function, spark_column_names, output_column_names
    )

    return snowpark_fn.pandas_udtf(
        MapInArrowUDTF,
        output_schema=PandasDataFrameType(
            [field.datatype for field in return_schema.fields],
            [field.name for field in return_schema.fields],
        ),
        input_types=[
            PandasDataFrameType(
                [field.datatype for field in input_schema.fields] + [IntegerType()]
            )
        ],
        input_names=[field.name for field in input_schema.fields]
        + ["_DUMMY_PARTITION_KEY"],
        name="mapinarrow_udtf",
        replace=True,
        packages=["pyarrow", "pandas"],
        is_permanent=False,
    )
