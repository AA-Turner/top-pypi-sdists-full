#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import hashlib
import json
from typing import Any, Callable, Iterator

import cloudpickle
import pandas as pd
import pyarrow as pa
from pyspark.sql.connect.proto.expressions_pb2 import CommonInlineUserDefinedFunction

import snowflake.snowpark.functions as snowpark_fn
from snowflake import snowpark
from snowflake.snowpark.types import (
    IntegerType,
    PandasDataFrameType,
    StructType,
    VariantType,
)

# Removed error imports to avoid UDF serialization issues
# from snowflake.snowpark_connect.error.error_codes import ErrorCodes
# from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code

# Package name for telemetry
TELEMETRY_PACKAGE = "snowflake-telemetry-python"


# DUPLICATED CODE from udtf_utils.py to avoid incorrect loading for stored procedure UDTF creation
def process_dependencies_string_array(input_str: str) -> list[str]:
    """
    Parse a string representation of a dependency array into a list of strings.

    Converts a bracket-enclosed, comma-separated string (e.g., "[scipy, pandas, numpy]")
    into a list of trimmed package names (e.g., ["scipy", "pandas", "numpy"]).

    Args:
        input_str: A string in the format "[item1, item2, ...]" or "item1, item2, ...".
                   Can also be empty or None.

    Returns:
        A list of trimmed dependency names. Returns an empty list if input is empty or None.

    Examples:
        >>> process_dependencies_string_array("[scipy, pandas]")
        ['scipy', 'pandas']
        >>> process_dependencies_string_array("numpy, pyarrow")
        ['numpy', 'pyarrow']
        >>> process_dependencies_string_array("")
        []
    """
    if input_str and len(input_str) > 0:
        return [i.strip() for i in input_str.strip("[] ").split(",") if i.strip()]
    return []


def process_udtf_packages(
    packages_str: str,
    is_arrow_enabled: bool = False,
    custom_packages: list[str] | None = None,
) -> list[str]:
    packages = process_dependencies_string_array(packages_str)
    # Include pyarrow in packages when using Arrow-enabled UDTF
    if is_arrow_enabled and "pyarrow" not in packages:
        packages += ["pyarrow"]

    if "pyspark" not in packages:
        # need this to support table argument in UDTF.
        packages += ["pyspark"]

    if custom_packages:
        for custom_package in custom_packages:
            if custom_package not in packages:
                packages.append(custom_package)

    return packages


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
    udtf_packages: str,
    udtf_imports: str,
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
        packages=process_udtf_packages(
            udtf_packages, custom_packages=["pandas", TELEMETRY_PACKAGE]
        ),
        imports=process_dependencies_string_array(udtf_imports),
        is_permanent=False,
    )


def create_pandas_udtf_with_arrow(
    udtf_proto: CommonInlineUserDefinedFunction,
    spark_column_names: list[str],
    input_schema: StructType,
    return_schema: StructType,
    udtf_packages: str,
    udtf_imports: str,
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
        packages=process_udtf_packages(
            udtf_packages,
            is_arrow_enabled=True,
            custom_packages=["pandas", TELEMETRY_PACKAGE],
        ),
        imports=process_dependencies_string_array(udtf_imports),
        is_permanent=False,
    )


def get_cogroup_pandas_udtf(
    user_function: Callable,
    input1_spark_column_names: list[str],
    input2_spark_column_names: list[str],
    output_column_names: list[str],
    output_column_original_names: list[str],
) -> Any:
    """
    Create and return a CoGroupPandasUDTF class with the given parameters.

    Args:
        user_function: User function that takes two pandas DataFrames and returns one
        input1_spark_column_names: Column names for the first DataFrame
        input2_spark_column_names: Column names for the second DataFrame
        output_column_names: List of expected output column names (snowflake names)
        output_column_original_names: List of original column names from user schema

    Returns:
        CoGroupPandasUDTF class that can be used with pandas_udtf
    """

    class CoGroupPandasUDTF:
        def __init__(self) -> None:
            self.user_function = user_function
            self.output_column_names = output_column_names
            self.output_column_original_names = output_column_original_names
            self.input1_spark_column_names = input1_spark_column_names
            self.input2_spark_column_names = input2_spark_column_names
            self.value_col = "__SC_COGROUP_VALUE__"
            self.source_col = "__SC_COGROUP_SOURCE__"

        def end_partition(self, df: pd.DataFrame):
            if df.empty:
                empty_df = pd.DataFrame(columns=self.output_column_names)
                yield empty_df
                return

            df1_rows = df[df[self.source_col] == 1]
            df2_rows = df[df[self.source_col] == 2]

            df1_values = df1_rows[self.value_col].tolist()
            df1_records = []
            for val in df1_values:
                if isinstance(val, str):
                    df1_records.append(json.loads(val))
                elif isinstance(val, dict):
                    df1_records.append(val)
                else:
                    df1_records.append({})

            df2_values = df2_rows[self.value_col].tolist()
            df2_records = []
            for val in df2_values:
                if isinstance(val, str):
                    df2_records.append(json.loads(val))
                elif isinstance(val, dict):
                    df2_records.append(val)
                else:
                    df2_records.append({})

            df1_data = pd.DataFrame(df1_records, columns=self.input1_spark_column_names)
            df2_data = pd.DataFrame(df2_records, columns=self.input2_spark_column_names)

            result_df = self.user_function(df1_data, df2_data)

            if result_df is not None and not isinstance(result_df, pd.DataFrame):
                raise RuntimeError(
                    f"[snowpark_connect::type_mismatch] Return type of the co-group function should be "
                    f"pandas.DataFrame, but is {type(result_df).__name__}"
                )

            if result_df is None or result_df.empty:
                empty_df = pd.DataFrame(columns=self.output_column_names)
                yield empty_df
                return

            generated_output_column_names = list(result_df.columns)

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
            reordered_df = result_df[self.output_column_original_names]
            reordered_df.columns = self.output_column_names
            yield reordered_df

    return CoGroupPandasUDTF


def create_cogroup_pandas_udtf(
    udtf_proto: CommonInlineUserDefinedFunction,
    input1_spark_column_names: list[str],
    input2_spark_column_names: list[str],
    return_schema: StructType,
    udtf_packages: str,
    udtf_imports: str,
):
    """
    Create a pandas UDTF for co-group operations (applyInPandas on cogrouped data).

    The UDTF receives rows from a UNION ALL of both DataFrames with a source marker.
    Each row has: value (JSON object with column data), source (1 or 2).
    It separates the rows by source, reconstructs two pandas DataFrames, and calls
    the user function with both DataFrames.
    """
    udtf_name = (
        "cogroup_pandas_udtf_" + hashlib.md5(udtf_proto.python_udf.command).hexdigest()
    )

    user_function, _ = cloudpickle.loads(udtf_proto.python_udf.command)
    output_column_names = [field.name for field in return_schema.fields]
    output_column_original_names = [
        field.original_column_identifier for field in return_schema.fields
    ]

    CoGroupPandasUDTF = get_cogroup_pandas_udtf(
        user_function,
        input1_spark_column_names,
        input2_spark_column_names,
        output_column_names,
        output_column_original_names,
    )

    from snowflake.snowpark_connect.relation.map_cogroup_map import (
        SOURCE_COL_NAME,
        VALUE_COL_NAME,
    )

    return snowpark_fn.pandas_udtf(
        CoGroupPandasUDTF,
        output_schema=PandasDataFrameType(
            [field.datatype for field in return_schema.fields],
            [field.name for field in return_schema.fields],
        ),
        input_types=[PandasDataFrameType([VariantType(), IntegerType()])],
        input_names=[VALUE_COL_NAME, SOURCE_COL_NAME],
        name=udtf_name,
        replace=True,
        packages=process_udtf_packages(
            udtf_packages, custom_packages=["pandas", TELEMETRY_PACKAGE]
        ),
        imports=process_dependencies_string_array(udtf_imports),
        is_permanent=False,
    )
