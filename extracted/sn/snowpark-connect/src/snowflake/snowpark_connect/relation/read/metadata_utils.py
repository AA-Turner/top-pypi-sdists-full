#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""
Utilities for handling internal metadata columns in file-based DataFrames.
"""

import os

import pandas

from snowflake import snowpark
from snowflake.snowpark.column import METADATA_FILENAME
from snowflake.snowpark.types import StructField
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer

# Constant for the metadata filename column name
METADATA_FILENAME_COLUMN = "METADATA$FILENAME"


def populate_metadata(
    options: dict | None = None,
):
    # NOTE: SNOWPARK_POPULATE_FILE_METADATA_DEFAULT is an internal environment variable
    # used only for CI testing to verify no metadata columns leak in regular file operations.
    # This environment variable should NOT be exposed to end users. Users should only use snowpark.populateFileMetadata
    # to enable metadata population.
    metadata_default = os.environ.get(
        "SNOWPARK_POPULATE_FILE_METADATA_DEFAULT", "false"
    )

    return (
        options.get("snowpark.populateFileMetadata", metadata_default)
        if options
        else metadata_default
    ).lower() == "true"


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

    if populate_metadata(options):
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
    if result_container is None:
        return None

    # Handle pandas DataFrame case - return as-is
    if isinstance(result_container, pandas.DataFrame):
        return result_container

    # do not modify a 0-column container
    if result_container.has_zero_columns():
        return result_container

    return (
        result_container.without_internal_columns().without_metadata_filename_column()
    )


def without_hidden_columns(
    result_container: DataFrameContainer | pandas.DataFrame | None,
) -> DataFrameContainer | pandas.DataFrame | None:
    """
    Function-form of `DataFrameContainer.without_hidden_columns` that also
    strips the file-read `METADATA$FILENAME` column. Equivalent to
    `without_internal_columns(c).without_qualified_access_only_columns()`,
    but performed in a single Snowpark `drop` pass — which means one fewer
    plan node (and one fewer describe-query SQL hash) at user-visible
    boundaries (show, execute, analyze, write).

    Use this at every boundary where a user-visible DataFrame is exposed to
    the client; reserve `without_internal_columns` for boundaries that must
    keep `is_qualified_access_only` shadows alive (e.g. before a downstream
    operator that still needs them in scope).
    """
    if result_container is None:
        return None

    # Handle pandas DataFrame case - return as-is
    if isinstance(result_container, pandas.DataFrame):
        return result_container

    # do not modify a 0-column container
    if result_container.has_zero_columns():
        return result_container

    return result_container.without_hidden_columns().without_metadata_filename_column()
