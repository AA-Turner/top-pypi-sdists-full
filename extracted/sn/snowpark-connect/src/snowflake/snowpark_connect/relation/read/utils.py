#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import functools
import re
import time
from collections.abc import Callable
from typing import (  # noqa: F401
    Any,
    Dict,
    Generator,
    Iterator,
    List,
    Literal,
    NewType,
    Optional,
    Protocol,
    Tuple,
    Type,
    Union,
    get_args,
    get_origin,
)

from snowflake import snowpark
from snowflake.snowpark._internal.analyzer import analyzer_utils
from snowflake.snowpark.exceptions import SnowparkClientException
from snowflake.snowpark_connect.column_name_handler import (
    make_column_names_snowpark_compatible,
)
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger

# Maximum number of files allowed in COPY INTO with FILES parameter
MAX_FILES_PER_COPY_INTO = 1000

STATEMENT_PARAMS_DATA_SOURCE = "SNOWPARK_PYTHON_DATASOURCE"


DATA_SOURCE_DBAPI_SIGNATURE = "DataFrameReader.dbapi"
DATA_SOURCE_SQL_COMMENT = (
    f"/* Python:snowflake.snowpark.{DATA_SOURCE_DBAPI_SIGNATURE} */"
)

INDEXED_COLUMN_NAME_PATTERN = re.compile(r"(^\"c)(\d+)(\"$)")


def _split_into_chunks(items: list, chunk_size: int) -> list[list]:
    """
    Split a list into chunks of specified size.

    Args:
        items: The list to split.
        chunk_size: Maximum size of each chunk.

    Returns:
        A list of chunks, each with at most chunk_size items.
    """
    return [items[i : i + chunk_size] for i in range(0, len(items), chunk_size)]


def generate_stage_path_groups(paths: list[str]) -> list[tuple[str, list[str]]]:
    """
    Group quoted Snowflake stage paths by their stage.

    Args:
        paths: List of quoted Snowflake stage paths like "'@stage_name/path/to/file.csv'".
               Each path must be wrapped in single quotes and start with '@'.

    Returns:
        A list of tuples (stage, paths) where each tuple represents a group.
        Each group contains at most MAX_FILES_PER_COPY_INTO files.

    Raises:
        ValueError: If any path is not a properly quoted Snowflake stage path.

    Example:
        Input: ["'@stage/file1.csv'", "'@stage/file2.csv'"]
        Output: [("'@stage'", ["'@stage/file1.csv'", "'@stage/file2.csv'"])]
    """
    # First, group paths by stage
    stage_path_dict: dict[str, list[str]] = {}
    for path in paths:
        stage = extract_stage_from_path(path)
        if stage not in stage_path_dict:
            stage_path_dict[stage] = []
        stage_path_dict[stage].append(path)

    result: list[tuple[str, list[str]]] = []

    for stage, stage_paths in stage_path_dict.items():
        for chunk in _split_into_chunks(stage_paths, MAX_FILES_PER_COPY_INTO):
            result.append((stage, chunk))

    return result


def apply_metadata_exclusion_pattern(options: dict) -> None:
    """
    Exclude metadata and hidden files from reads, matching Spark's behavior.

    Automatically filters out internal metadata files that should never be read as data:
        - _SUCCESS, _metadata, _common_metadata (Spark/Parquet metadata)
        - .crc (Hadoop checksum files)
        - .DS_Store (macOS system files)
        - Any file starting with _ or .

    Pattern used: ".*/[^_.][^/]*$|^[^_.][^/]*$"
        - Matches files where filename does NOT start with _ or .
        - Works at any directory depth (flat or partitioned data)
        - Allows files with or without extensions

    Examples of excluded files:
        ❌ _SUCCESS, _metadata, _common_metadata (Spark/Parquet metadata)
        ❌ .crc, .DS_Store, .hidden (system/hidden files)
        ❌ year=2024/_SUCCESS (metadata in partitioned directories)

    Examples of allowed files:
        ✅ part-00000.parquet, data.csv, output.json (data files)
        ✅ success, myfile (files without extensions, don't start with _ or .)
        ✅ year=2024/month=01/part-00000.parquet (partitioned data)

    User pattern handling:
        - No pattern or "*" or ".*" → Apply metadata exclusion
        - Custom patterns → Default to user provided pattern.

    Leak cases (user explicitly requests metadata files and are intentional):
        ⚠️ "_*" → Matches _SUCCESS, _metadata (explicit underscore prefix)
        ⚠️ "*SUCCESS*" → Matches _SUCCESS (broad wildcard side effect)
        ⚠️ "[_.].*" → Matches _SUCCESS, .crc (character class includes _)

    Args:
        options: Dictionary of Snowpark read options (modified in place)
    """
    if "PATTERN" not in options or options["PATTERN"] in ("*", ".*"):
        options["PATTERN"] = ".*/[^_.][^/]*$|^[^_.][^/]*$"


def subtract_one(match: re.Match[str]) -> str:
    """Spark column names are 0 indexed, Snowpark is 1 indexed."""
    return f"_c{str(int(match.group(2)) - 1)}"


def get_spark_column_names_from_snowpark_columns(
    snowpark_column_names: List[str],
) -> List[str]:
    return [
        analyzer_utils.unquote_if_quoted(
            INDEXED_COLUMN_NAME_PATTERN.sub(subtract_one, c)
        )
        for c in snowpark_column_names
    ]


def rename_columns_as_snowflake_standard(
    df: snowpark.DataFrame, plan_id: int
) -> tuple[snowpark.DataFrame, list[str]]:
    """
    Renames the columns of a Snowflake DataFrame to follow a standard format.
    Args:
        df (snowpark.DataFrame): The input Snowflake DataFrame.

    Returns:
        tuple[snowpark.DataFrame, list[str]]: A tuple containing the modified DataFrame
        with renamed columns and a list of the new column names.
    """

    if df.columns is None or len(df.columns) == 0:
        return df, []

    new_columns = make_column_names_snowpark_compatible(df.columns, plan_id)
    result_df = df.select(
        *(df.col(orig).alias(alias) for orig, alias in zip(df.columns, new_columns))
    )

    # do not flatten initial rename when reading table
    # TODO: remove once SNOW-2203826 is done
    if result_df._select_statement is not None:
        result_df._select_statement.flatten_disabled = True

    return result_df, new_columns


class Connection(Protocol):
    """External datasource connection created from user-input create_connection function."""

    def cursor(self) -> "Cursor":
        pass

    def close(self):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass


class Cursor(Protocol):
    """Cursor created from external datasource connection"""

    def execute(self, sql: str, *params: Any) -> "Cursor":
        pass

    def fetchall(self):
        pass

    def fetchone(self):
        pass

    def close(self):
        pass


def extract_stage_from_path(path: str) -> str:
    """
    Extract the Snowflake stage prefix from a quoted stage path.

    The input path is expected to be a quoted Snowflake stage path like:
        "'@stage_name/path/to/file.csv'" -> "'@stage_name'"

    Args:
        path: A quoted Snowflake stage path like "'@stage_name/path/to/file.csv'"

    Returns:
        The quoted stage prefix like "'@stage_name'".

    Raises:
        ValueError: If the path is not properly quoted with single quotes or is not a Snowflake stage path.
    """
    # Validate that the path is quoted
    if not (path.startswith("'") and path.endswith("'")):
        exception = ValueError(
            f"Path must be quoted with single quotes, got: {path}. "
            f"Expected format: \"'@stage_name/path/to/file.csv'\""
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception

    # Remove quotes to parse
    clean_path = path.strip("'")

    # Validate it's a Snowflake stage path
    if not clean_path.startswith("@"):
        exception = ValueError(
            f"Path must be a Snowflake stage path starting with @, got: {path}. "
            f"Expected format: \"'@stage_name/path/to/file.csv'\""
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception

    # Extract stage name (everything before the first /)
    parts = clean_path.split("/")
    stage = parts[0]
    return f"'{stage}'"


def paths_share_same_stage(paths: list[str]) -> tuple[bool, str | None]:
    """
    Check if all quoted Snowflake stage paths share the same stage prefix.

    Args:
        paths: List of quoted stage paths like ["'@stage/file1.csv'", "'@stage/file2.csv'"]

    Returns:
        A tuple of (all_same_stage, quoted_stage_prefix).
        If all paths share the same stage, returns (True, "'@stage'").
        Otherwise, returns (False, None).
    """
    if not paths:
        return False, None

    first_stage = extract_stage_from_path(paths[0])

    for path in paths[1:]:
        stage = extract_stage_from_path(path)
        if stage != first_stage:
            return False, None

    return True, first_stage


def extract_relative_file_path(path: str, stage: str) -> str:
    """
    Extract the relative file path from a quoted Snowflake stage path.

    Args:
        path: A quoted stage path like "'@stage_name/path/to/file.csv'"
        stage: The quoted stage prefix like "'@stage_name'"

    Returns:
        The relative path after the stage, e.g., 'path/to/file.csv'
    """
    # Handle quoted paths and stages
    clean_path = path.strip("'")
    clean_stage = stage.strip("'")

    # Remove the stage prefix and leading slash
    if clean_path.startswith(clean_stage):
        relative_path = clean_path[len(clean_stage) :]
        # Remove leading slash if present
        if relative_path.startswith("/"):
            relative_path = relative_path[1:]
        return relative_path

    return clean_path


def exponential_backoff(
    func: Callable | None = None,
    max_retry_count: int = 3,
    initial_retry_delay_ms: int = 50,
    exponential_backoff_base: int = 2,
) -> Callable:
    if func is None:
        return functools.partial(
            exponential_backoff,
            max_retry_count=max_retry_count,
            initial_retry_delay_ms=initial_retry_delay_ms,
            exponential_backoff_base=exponential_backoff_base,
        )

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        error = None
        for retry_count in range(max_retry_count):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error = e

                delay_ms = (
                    exponential_backoff_base**retry_count * initial_retry_delay_ms
                )
                time.sleep(delay_ms / 1000.0)
                logger.debug(
                    f"Function '{func.__name__}' failed with {error.__repr__()}, retry count: {retry_count}, retrying ..."
                )
        error = SnowparkClientException(
            message=f"failed to run '{func.__name__}', got {error.__repr__()}"
        )
        logger.debug(
            f"Function '{func.__name__}' failed with {error.__repr__()}, exceed max retry time"
        )

        return error

    return wrapper


def _load_file_with_copy_into(
    reader: "snowpark.DataFrameReader",
    session: "snowpark.Session",
    target: str,
    stage_file_paths: list[str],
    stage: str,
    schema: "snowpark.types.StructType",
    file_format_options: dict[str, Any],
    file_format: Literal["csv", "json"],
) -> None:
    """
    Load multiple files from the same stage using COPY INTO with FILES parameter.

    Supports CSV and JSON file formats for parallel execution.

    Args:
        reader: The DataFrameReader with configured options.
        session: The Snowpark session.
        target: The name of the temporary table to load the data into.
        stage_file_paths: List of full stage paths like ['@stage/file1.csv', '@stage/file2.csv'] to load.
        stage: The common stage name like '@stage_name'.
        schema: The StructType schema for the table.
        file_format_options: File format options for the file type.
        file_format: The file format type, either "csv" or "json".

    TODO: SNOW-3002469 copy_into_table does not enable INCLUDE_METADATA even though add_filename_metadata_to_reader
        has been called before.
    """
    # Extract just the file paths relative to the stage for the FILES parameter
    relative_files = [
        extract_relative_file_path(path, stage) for path in stage_file_paths
    ]

    logger.debug(
        f"Using COPY INTO for parallel {file_format.upper()} loading: "
        f"{len(relative_files)} files from {stage}"
    )

    # Pre-create the target table if it doesn't exist.
    #
    # Why this is necessary:
    # Snowpark's copy_into_table() can only auto-create tables for CSV format (without
    # transformations). For JSON and other semi-structured formats, Snowpark cannot
    # determine column names from the data alone and raises:
    #   SnowparkDataframeReaderException: "Cannot create the target table ... because
    #   Snowpark cannot determine the column names to use."
    #
    # This is a Snowpark Python client-side limitation, not a Snowflake SQL limitation.
    # By pre-creating the table with our known schema, we bypass this restriction.
    #
    # See: snowflake/snowpark/_internal/analyzer/snowflake_plan.py::copy_into_table()
    try:
        session.table(target).schema  # Check if table exists
    except Exception:
        # Table doesn't exist - create an empty table with the expected schema
        logger.debug(
            f"Pre-creating temporary table '{target}' with schema for COPY INTO"
        )
        session.create_dataframe(data=[], schema=schema).write.save_as_table(
            target, table_type="temporary"
        )

    # Get the appropriate reader method based on format
    schema_reader = reader.schema(schema)
    if file_format == "csv":
        source_df = schema_reader.csv(stage)
    elif file_format == "json":
        source_df = schema_reader.json(stage)
    else:
        raise ValueError(f"Unsupported file format for COPY INTO: {file_format}")

    # Build copy options - JSON requires MATCH_BY_COLUMN_NAME to load into multi-column tables
    copy_options: dict[str, Any] = {"force": True}
    if file_format == "json":
        copy_options["MATCH_BY_COLUMN_NAME"] = "CASE_INSENSITIVE"

    # Use Snowpark's copy_into_table API with the files parameter for parallel loading
    source_df.copy_into_table(
        target,
        files=relative_files,
        format_type_options=file_format_options,
        **copy_options,
    )
