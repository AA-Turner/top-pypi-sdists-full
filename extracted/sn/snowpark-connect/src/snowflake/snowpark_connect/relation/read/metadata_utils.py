#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""
Utilities for handling internal metadata columns in file-based DataFrames.
"""

import os

import pandas
from pyspark.errors.exceptions.base import AnalysisException

from snowflake import snowpark
from snowflake.snowpark.column import METADATA_FILENAME
from snowflake.snowpark.functions import col
from snowflake.snowpark.types import StructField, StructType
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code

# Constant for the metadata filename column name
METADATA_FILENAME_COLUMN = "METADATA$FILENAME"


def add_filename_metadata_to_reader(
    reader: snowpark.DataFrameReader,
    options: dict | None = None,
) -> snowpark.DataFrameReader:
    """
    Add filename metadata to a DataFrameReader based on configuration.

    Args:
        reader: Snowpark DataFrameReader instance
        options: Dictionary of options to check for metadata configuration

    Returns:
        DataFrameReader with filename metadata enabled if configured, otherwise unchanged
    """
    # NOTE: SNOWPARK_POPULATE_FILE_METADATA_DEFAULT is an internal environment variable
    # used only for CI testing to verify no metadata columns leak in regular file operations.
    # This environment variable should NOT be exposed to end users. Users should only use snowpark.populateFileMetadata
    # to enable metadata population.
    metadata_default = os.environ.get(
        "SNOWPARK_POPULATE_FILE_METADATA_DEFAULT", "false"
    )

    populate_metadata = (
        options.get("snowpark.populateFileMetadata", metadata_default)
        if options
        else metadata_default
    ).lower() == "true"

    if populate_metadata:
        return reader.with_metadata(METADATA_FILENAME)
    else:
        return reader


def get_non_metadata_fields(schema_fields: list[StructField]) -> list[StructField]:
    """
    Filter out METADATA$FILENAME fields from a list of schema fields.

    Args:
        schema_fields: List of StructField objects from a DataFrame schema

    Returns:
        List of StructField objects excluding METADATA$FILENAME
    """
    return [field for field in schema_fields if field.name != METADATA_FILENAME_COLUMN]


def get_non_metadata_column_names(schema_fields: list[StructField]) -> list[str]:
    """
    Get column names from schema fields, excluding METADATA$FILENAME.

    Args:
        schema_fields: List of StructField objects from a DataFrame schema

    Returns:
        List of column names (strings) excluding METADATA$FILENAME
    """
    return [
        field.name for field in schema_fields if field.name != METADATA_FILENAME_COLUMN
    ]


def filter_metadata_column_name(column_names: list[str]) -> list[str]:
    """
    Get column names from column_names, excluding METADATA$FILENAME.

    Returns:
        List of column names (strings) excluding METADATA$FILENAME
    """
    return [
        col_name for col_name in column_names if col_name != METADATA_FILENAME_COLUMN
    ]


def without_internal_columns(
    result_container: DataFrameContainer | pandas.DataFrame | None,
) -> DataFrameContainer | pandas.DataFrame | None:
    """
    Filters internal columns like:
     * METADATA$FILENAME from DataFrame container for execution and write operations
     * hidden columns needed for outer joins implementation

    Args:
        result_container: DataFrameContainer or pandas DataFrame to filter

    Returns:
        Filtered container (callers can access dataframe via container.dataframe)
    """
    # Handle pandas DataFrame case - return as-is
    if isinstance(result_container, pandas.DataFrame):
        return result_container

    if result_container is None:
        return None

    # do not modify a 0-column container
    if result_container.has_zero_columns():
        return result_container

    result_container = result_container.without_hidden_columns()
    result_df = result_container.dataframe
    if not isinstance(result_df, snowpark.DataFrame):
        return result_container

    df_columns = result_container.column_map.get_snowpark_columns()
    has_metadata_filename = any(name == METADATA_FILENAME_COLUMN for name in df_columns)

    if not has_metadata_filename:
        return result_container

    non_metadata_columns = filter_metadata_column_name(df_columns)

    if len(non_metadata_columns) == 0:
        # DataFrame contains only metadata columns (METADATA$FILENAME), no actual data columns remaining.
        # We don't have a way to return an empty dataframe.
        exception = AnalysisException(
            "[DATAFRAME_MISSING_DATA_COLUMNS] Cannot perform operation on DataFrame that contains no data columns."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
        raise exception

    filtered_df = result_df.select([col(name) for name in non_metadata_columns])

    original_spark_columns = result_container.column_map.get_spark_columns()
    original_snowpark_columns = result_container.column_map.get_snowpark_columns()

    filtered_spark_columns = []
    filtered_snowpark_columns = []

    for i, colname in enumerate(df_columns):
        if colname != METADATA_FILENAME_COLUMN:
            filtered_spark_columns.append(original_spark_columns[i])
            filtered_snowpark_columns.append(original_snowpark_columns[i])

    new_container = DataFrameContainer.create_with_column_mapping(
        dataframe=filtered_df,
        spark_column_names=filtered_spark_columns,
        snowpark_column_names=filtered_snowpark_columns,
        column_metadata=result_container.column_map.column_metadata,
        table_name=result_container.table_name,
        alias=result_container.alias,
        partition_hint=result_container.partition_hint,
        # we don't want to evaluate `filtered_df` schema since it will always trigger a describe query
        cached_schema_getter=lambda: StructType(
            [f for f in result_df.schema if f.name != METADATA_FILENAME_COLUMN]
        ),
    )

    return new_container
