#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import functools
import re
import time
from collections.abc import Callable
from typing import (  # noqa: F401
    TYPE_CHECKING,
    Any,
    Dict,
    Generator,
    Iterator,
    List,
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

STATEMENT_PARAMS_DATA_SOURCE = "SNOWPARK_PYTHON_DATASOURCE"
DATA_SOURCE_DBAPI_SIGNATURE = "DataFrameReader.dbapi"
DATA_SOURCE_SQL_COMMENT = (
    f"/* Python:snowflake.snowpark.{DATA_SOURCE_DBAPI_SIGNATURE} */"
)

INDEXED_COLUMN_NAME_PATTERN = re.compile(r"(^\"c)(\d+)(\"$)")


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
