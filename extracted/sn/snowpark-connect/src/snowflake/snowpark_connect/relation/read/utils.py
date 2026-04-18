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
from snowflake.snowpark_connect.relation.read.metadata_utils import (
    METADATA_FILENAME_COLUMN,
)
from snowflake.snowpark_connect.utils.context import _normalize as _norm
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


def normalize_stage_path(path: str) -> str:
    """Strip surrounding single-quotes and any trailing slash from a stage path.

    Quoted stage paths like ``'@stage/dir/'`` become ``@stage/dir``.
    Unquoted paths are returned with only the trailing slash removed.
    """
    return path.strip("'").rstrip("/")


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


def _build_partition_column_transforms(
    partition_columns: list[str],
    partition_types: dict[str, snowpark.types.DataType],
    partition_file_col_names: list[str] | None = None,
) -> tuple[list[str], list[snowpark.Column]]:
    """Build target_columns and transformations for Hive-style partition columns only.

    Partition values are extracted from ``METADATA$FILENAME`` using
    ``SPLIT_PART(..., 'col=', 2)`` and cast to their inferred types via
    ``try_cast(permissive=True)``.

    Args:
        partition_columns: Ordered list of partition column names (user schema names).
        partition_types: Mapping of user column name → inferred DataType.
        partition_file_col_names: If provided, the actual directory segment names used
            in METADATA$FILENAME (e.g. ``['id']`` when user schema has ``['ID']``).
            When omitted, ``partition_columns`` names are used for SPLIT_PART matching.

    Returns ``(target_columns, transformations)`` for partition columns.
    """
    from snowflake.snowpark.functions import lit, nullif, split_part, sql_expr

    target_cols: list[str] = []
    transforms: list[snowpark.Column] = []

    metadata_col = sql_expr(METADATA_FILENAME_COLUMN)
    for i, col_name in enumerate(partition_columns):
        target_cols.append(analyzer_utils.quote_name_without_upper_casing(col_name))
        file_col_name = (
            partition_file_col_names[i] if partition_file_col_names else col_name
        )
        partition_val = nullif(
            split_part(
                split_part(metadata_col, lit(f"{file_col_name}="), lit(2)),
                lit("/"),
                lit(1),
            ),
            lit("__HIVE_DEFAULT_PARTITION__"),
        )
        transforms.append(
            partition_val.try_cast(partition_types[col_name], permissive=True)
        )

    return target_cols, transforms


def _load_file_with_copy_into(
    reader: "snowpark.DataFrameReader",
    session: "snowpark.Session",
    target: str,
    stage_file_paths: list[str],
    stage: str,
    schema: "snowpark.types.StructType",
    file_format_options: dict[str, Any],
    file_format: Literal["csv", "json", "parquet"],
    on_error: str | None = None,
    partition_columns: list[str] | None = None,
    partition_types: dict[str, snowpark.types.DataType] | None = None,
    partition_file_col_names: list[str] | None = None,
    needs_metadata: bool = False,
    target_columns: list[str] | None = None,
    transformations: list[Any] | None = None,
    table_already_exists: bool = False,
) -> List[Any]:
    """Load files from a stage using COPY INTO.

    Supports CSV, JSON, and Parquet file formats for parallel execution.
    When *partition_columns* is provided, uses COPY INTO with transformations
    to extract partition values from ``METADATA$FILENAME`` and data columns
    via positional (CSV) or path-based (JSON/Parquet ``$1:field``) references.

    When *needs_metadata* is ``True``, ``METADATA$FILENAME`` is included in
    the target table so that ``input_file_name()`` can resolve it later.
    For JSON without transformations this uses ``INCLUDE_METADATA``; when
    transformations are already active (e.g. partition extraction) an extra
    ``METADATA$FILENAME`` transformation is appended instead.

    Args:
        reader: The DataFrameReader with configured options.
        session: The Snowpark session.
        target: The name of the temporary table to load the data into.
        stage_file_paths: List of full stage paths to load. Pass an empty
            list when loading from a single file (stage param is the full path).
        stage: The common stage name like '@stage_name', or full path for
            single-file loads.
        schema: The StructType schema for the table.
        file_format_options: File format options for the file type.
        file_format: The file format type: "csv", "json", or "parquet".
        on_error: Optional ON_ERROR strategy (e.g. "CONTINUE").
        partition_columns: Ordered list of Hive partition column names.
        partition_types: Mapping of partition column name -> inferred DataType.
        partition_file_col_names: Actual METADATA$FILENAME segment names
            for SPLIT_PART matching (when case differs from user schema names).
            Only used for Parquet.
        needs_metadata: When True, include ``METADATA$FILENAME`` in the target
            table to support ``input_file_name()``.
        target_columns: Pre-built list of target column names for COPY INTO.
            When provided together with *transformations*, these are used
            directly instead of building them from partition logic.
        transformations: Pre-built list of Snowpark Column transformations
            for COPY INTO.  When provided, these are used as the base set
            of transformations; partition and metadata transforms are appended
            on top if needed.
        table_already_exists: When True, skip the table existence check — the
            caller has already pre-created the table.  Saves 1 round-trip per
            COPY INTO call (useful when loading multiple stage groups in a loop).

    Returns:
        The result rows from the COPY INTO command.
    """
    from snowflake.snowpark.functions import sql_expr
    from snowflake.snowpark.types import StringType, StructField, StructType

    relative_files = [
        extract_relative_file_path(path, stage) for path in stage_file_paths
    ]

    has_partitions = bool(partition_columns)
    logger.debug(
        f"Using COPY INTO for parallel {file_format.upper()} loading: "
        f"{len(relative_files)} files from {stage}"
        f"{' (with partition transform)' if has_partitions else ''}"
        f"{' (with metadata)' if needs_metadata else ''}"
    )

    loading_schema = schema
    copy_target_columns = target_columns
    copy_transformations = transformations

    if has_partitions:
        part_cols, part_transforms = _build_partition_column_transforms(
            partition_columns, partition_types, partition_file_col_names
        )
        partition_name_set = {
            _norm(analyzer_utils.unquote_if_quoted(c)) for c in partition_columns
        }
        partition_fields = [
            StructField(
                analyzer_utils.quote_name_without_upper_casing(col),
                partition_types[col],
                nullable=True,
            )
            for col in partition_columns
        ]
        data_fields = [
            f
            for f in schema.fields
            if _norm(analyzer_utils.unquote_if_quoted(f.name)) not in partition_name_set
        ]
        loading_schema = StructType(data_fields + partition_fields)
        copy_target_columns = [
            c
            for c in copy_target_columns
            if _norm(analyzer_utils.unquote_if_quoted(c)) not in partition_name_set
        ]
        copy_transformations = [
            t
            for t, c in zip(copy_transformations, target_columns)
            if _norm(analyzer_utils.unquote_if_quoted(c)) not in partition_name_set
        ]
        copy_target_columns = copy_target_columns + part_cols
        copy_transformations = copy_transformations + part_transforms

    if needs_metadata:
        metadata_field = StructField(
            METADATA_FILENAME_COLUMN, StringType(), nullable=True
        )
        loading_schema = StructType(list(loading_schema.fields) + [metadata_field])
        if copy_transformations is not None:
            copy_target_columns = copy_target_columns + [METADATA_FILENAME_COLUMN]
            copy_transformations = copy_transformations + [
                sql_expr(METADATA_FILENAME_COLUMN)
            ]

    if not table_already_exists:
        # Pre-create the target table if it doesn't exist.
        # Snowpark's copy_into_table() can only auto-create tables for CSV
        # without transformations.  For JSON/Parquet and semi-structured formats
        # Snowpark cannot determine column names and raises
        # SnowparkDataframeReaderException.  Pre-creating bypasses this.
        try:
            session.table(target).schema
        except Exception:
            logger.debug(
                f"Pre-creating temporary table '{target}' with schema for COPY INTO"
            )
            session.create_dataframe(
                data=[], schema=loading_schema
            ).write.save_as_table(target, table_type="temporary")

    # Parquet passes loading_schema (with partition cols filtered out) to the
    # reader so Snowpark generates the correct COPY INTO column list.
    # CSV/JSON use the original schema.
    reader_schema = loading_schema if file_format == "parquet" else schema
    schema_reader = reader.schema(reader_schema)
    if file_format == "csv":
        source_df = schema_reader.csv(stage)
    elif file_format == "json":
        source_df = schema_reader.json(stage)
    elif file_format == "parquet":
        source_df = schema_reader.parquet(stage)
    else:
        raise ValueError(f"Unsupported file format for COPY INTO: {file_format}")

    copy_options: dict[str, Any] = {"force": True}
    if on_error is not None:
        copy_options["ON_ERROR"] = on_error

    return source_df.copy_into_table(
        target,
        files=relative_files,
        target_columns=copy_target_columns,
        transformations=copy_transformations,
        format_type_options=file_format_options,
        **copy_options,
    )
