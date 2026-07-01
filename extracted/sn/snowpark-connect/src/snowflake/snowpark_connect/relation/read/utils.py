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
from snowflake.snowpark._internal.analyzer.analyzer_utils import unquote_if_quoted
from snowflake.snowpark.exceptions import SnowparkClientException
from snowflake.snowpark.types import StringType as _SnowparkStringType
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

_METADATA_CORRUPT_RECORD_KEY = '"METADATA$CORRUPT_RECORD"'

# Cloud URI schemes as they appear in Snowflake ``LIST`` output, mapped to the
# number of ``/``-delimited leading components to drop (scheme + bucket, plus
# the container for Azure) to recover a stage-relative path.
CLOUD_LIST_SCHEME_PARTS: dict[str, int] = {
    "s3://": 3,
    "s3a://": 3,
    "azure://": 4,
    "gs://": 3,
    "gcs://": 3,
}


def cloud_list_path_to_relative(listed_path: str) -> str | None:
    """Convert a cloud-rooted ``LIST`` path into a stage-relative path.

    Snowflake's ``LIST`` returns rows rooted at the backing cloud location
    (``s3://bucket/...``, ``gcs://bucket/...``,
    ``azure://account.host/container/...``). This drops the scheme + bucket
    (+ container for Azure) so callers get a path relative to the stage root
    (e.g. ``dir/file.parquet``). Returns ``None`` when the path is not a
    recognized cloud URI — i.e. a stage-name-rooted path the caller must handle
    itself.
    """
    for prefix, skip_parts in CLOUD_LIST_SCHEME_PARTS.items():
        if listed_path.startswith(prefix):
            return "/".join(listed_path.split("/")[skip_parts:])
    return None


def ensure_corrupt_record_metadata_allowed() -> None:
    """Allow ``METADATA$CORRUPT_RECORD`` in Snowpark's INCLUDE_METADATA allowlist.

    Snowpark's client-side validation in ``DataFrame.copy_into_table`` consults
    ``snowflake.snowpark.column.METADATA_COLUMN_TYPES`` to decide which
    ``METADATA$*`` functions are projectable via ``INCLUDE_METADATA``. The
    allowlist does not yet include ``METADATA$CORRUPT_RECORD`` even though the
    Snowflake server supports it, so we install it here.

    Called from the CSV ``_corrupt_record`` code path (lazy on purpose). If a
    future ``snowpark-python`` release renames or removes the symbol, the
    resulting ``ImportError`` / ``AttributeError`` surfaces at the
    ``_corrupt_record`` user feature-use site with a clean stack instead of a
    silent startup degradation. Idempotent via ``dict.setdefault`` (atomic
    under the GIL, no extra locking required).

    TODO(SNOW-3443841): Move this allowlist extension upstream into
    snowpark-python so SAS does not have to patch it at all.
    """
    from snowflake.snowpark import column as _snowpark_column

    _snowpark_column.METADATA_COLUMN_TYPES.setdefault(
        _METADATA_CORRUPT_RECORD_KEY, _SnowparkStringType()
    )


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


def normalized_file_source_column_merge_key(name: str) -> str:
    """Return a comparison key for merging column names across file reads.

    Strips Snowflake/Snowpark identifier quoting, then applies the same
    case-folding as ``snowflake.snowpark_connect.utils.context._normalize``
    (``spark.sql.caseSensitive``).

    Shared by CSV ``mergeSchema`` union logic and JSON inferred-schema
    case-insensitive field deduplication so both paths stay consistent.
    """
    return _norm(unquote_if_quoted(name))


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


def copy_stage_target(stage_name: str, stage_files: list[str]) -> tuple[str, list[str]]:
    """Return ``(stage, stage_file_paths)`` for :func:`_load_file_with_copy_into`.

    A single path uses the full quoted stage path with an empty ``files`` list
    (Snowflake resolves the prefix via ``PATTERN``). Multiple concrete files on
    one stage pass both the stage root and relative file paths. Multiple
    directory/glob scan prefixes (trailing ``/``) must not be passed as COPY
    ``files`` — Snowflake expects file paths there, not prefixes — so we scope
    ``PATTERN`` to the stage root instead.
    """
    if len(stage_files) == 1:
        return stage_files[0], []
    if all(path.strip("'").rstrip().endswith("/") for path in stage_files):
        return stage_name, []
    return stage_name, stage_files


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
    apply_positional_normalization: bool = True,
    skip_names: List[str] | None = None,
) -> List[str]:
    """Convert Snowpark column names to their Spark-facing equivalents.

    The only transformation is converting Snowflake's synthetic 1-indexed
    positional placeholders (``c1``, ``c2``, …) back to Spark's 0-indexed
    ``_cN`` form. Those placeholders are generated *only* when a file is read
    with neither a user-supplied schema nor a header row, so the decrement
    must never be applied to names the user (or a header) actually chose --
    a user column literally named ``c0`` would otherwise be mangled to
    ``_c-1`` (SNOW-3587964).

    Args:
        snowpark_column_names: The Snowpark/source column names.
        apply_positional_normalization: When ``False``, names are returned
            verbatim (only unquoted). Callers pass ``False`` whenever the
            names came from a user schema or a file header -- i.e. anything
            other than SCOS-generated positional placeholders.
        skip_names: Names that must never be normalized even when
            ``apply_positional_normalization`` is ``True`` (e.g. Hive
            partition columns, whose names come from the directory path and
            could coincidentally look like ``cN``).
    """
    skip_set = {_norm(unquote_if_quoted(n)) for n in (skip_names or [])}

    def _to_spark(c: str) -> str:
        if not apply_positional_normalization:
            return analyzer_utils.unquote_if_quoted(c)
        if _norm(unquote_if_quoted(c)) in skip_set:
            return analyzer_utils.unquote_if_quoted(c)
        return analyzer_utils.unquote_if_quoted(
            INDEXED_COLUMN_NAME_PATTERN.sub(subtract_one, c)
        )

    return [_to_spark(c) for c in snowpark_column_names]


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
    reader_schema_override: Optional["snowpark.types.StructType"] = None,
    table_already_exists: bool = False,
    corrupt_record_column: str | None = None,
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
        on_error: Optional ON_ERROR strategy (e.g. "CONTINUE", "PERMISSIVE").
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
        corrupt_record_column: When set (CSV only), append a nullable
            ``StringType`` column to ``loading_schema`` and add
            ``<col> => METADATA$CORRUPT_RECORD`` to ``INCLUDE_METADATA`` so
            COPY INTO populates it with the raw record bytes for malformed
            rows (NULL on good rows, matching Spark). Works for both
            PARSE_HEADER=TRUE and PARSE_HEADER=FALSE via SNOW-3348324
            (server parameter ``ENABLE_INCLUDE_METADATA_WITHOUT_MBCN_CSV``,
            on by default for SCOS sessions). One cosmetic D1 remains:
            METADATA$CORRUPT_RECORD includes the trailing line terminator
            that Spark trims.

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

    if corrupt_record_column is not None:
        # CSV only — caller is responsible for that precondition.
        # SNOW-3348324 (server PR snowflake-eng/snowflake#440411, parameter
        # ``ENABLE_INCLUDE_METADATA_WITHOUT_MBCN_CSV``, account-level
        # ``ENABLE_INCLUDE_METADATA_WITHOUT_MBCN_CSV_FOR_SCOS`` defaults to
        # ``Enable``) lifts the server-side constraint that INCLUDE_METADATA
        # required MATCH_BY_COLUMN_NAME for CSV. With the parameter on, the
        # server positionally loads file fields into the non-metadata columns
        # of the target table and resolves the INCLUDE_METADATA names by
        # column name — so the corrupt-record column works for both
        # PARSE_HEADER=TRUE (header→column-name match) and PARSE_HEADER=FALSE
        # (positional match) flavours below. ``MATCH_BY_COLUMN_NAME`` is
        # still emitted (as ``NONE`` on the no-header branch) because
        # snowpark-python's client-side validation rejects INCLUDE_METADATA
        # without it.
        # Quote the field name so the temp table preserves the user's exact
        # casing — INCLUDE_METADATA below references the quoted form, and
        # Snowpark would otherwise upper-case bare identifiers.
        loading_schema = StructType(
            list(loading_schema.fields)
            + [
                StructField(
                    analyzer_utils.quote_name_without_upper_casing(
                        corrupt_record_column
                    ),
                    StringType(),
                    nullable=True,
                )
            ]
        )
        if copy_transformations is not None:
            # Positional-transforms path: INCLUDE_METADATA is not used, so
            # populate the corrupt-record column by adding METADATA$CORRUPT_RECORD
            # as an explicit expression in the SELECT list, the same way
            # METADATA$FILENAME is handled for needs_metadata above.
            copy_target_columns = copy_target_columns + [
                analyzer_utils.quote_name_without_upper_casing(corrupt_record_column)
            ]
            copy_transformations = copy_transformations + [
                sql_expr("METADATA$CORRUPT_RECORD")
            ]

    if not table_already_exists:
        # Pre-create the target table.
        # Snowpark's copy_into_table() can only auto-create tables for CSV
        # without transformations.  For JSON/Parquet and semi-structured formats
        # Snowpark cannot determine column names and raises
        # SnowparkDataframeReaderException.  Pre-creating bypasses this.
        #
        # SNOW-3590917: the previous implementation gated the create on a
        # ``try: session.table(target).schema`` existence probe.  ``target``
        # is always a freshly-allocated ``SNOWPARK_TEMP_TABLE_<random>`` name
        # (every caller passes ``random_name_for_temp_object(TempObjectType.TABLE)``
        # or sets ``table_already_exists=True``), so the probe was a
        # guaranteed cache-miss describe round-trip (~200-300 ms) on every
        # CSV/JSON/Parquet read pipeline.  Issuing the create with
        # ``mode="ignore"`` lets Snowflake express the same intent
        # server-side as ``CREATE TEMPORARY TABLE IF NOT EXISTS ...``: zero
        # describe RTT in the common (target absent) case, and on the
        # theoretical name-collision case it silently keeps the existing
        # table — matching the pre-fix semantics rather than raising. The
        # temp table is dropped at session end either way.
        logger.debug(
            f"Pre-creating temporary table '{target}' with schema for COPY INTO"
        )
        # SNOW-3554289: CSV/JSON file sources can always contain
        # NULL values, so the COPY temp table must be fully nullable
        # to avoid spurious NOT NULL rejections under PERMISSIVE /
        # CONTINUE on malformed rows. Matches Spark's SPARK-35912
        # behaviour (the CSV / JSON readers silently convert
        # non-nullable user schemas to nullable). JSON also runs
        # ``_make_schema_nullable`` upstream in ``map_read_json``;
        # the coercion here is belt-and-suspenders so the temp
        # table is always created with the relaxed nullability
        # regardless of how the schema is built. Parquet is out
        # of scope -- nested struct fidelity matters there and the
        # existing ``snowpark.connect.io.validations.mode`` knob
        # already covers it. The user-visible schema is unchanged:
        # the caller preserves the original schema for the
        # post-load reshuffle / cast.
        creation_schema = (
            StructType(
                [
                    StructField(f.name, f.datatype, nullable=True)
                    for f in loading_schema.fields
                ]
            )
            if file_format in ("csv", "json")
            else loading_schema
        )
        session.create_dataframe(data=[], schema=creation_schema).write.save_as_table(
            target, table_type="temporary", mode="ignore"
        )

    # Parquet passes loading_schema (with partition cols filtered out) to the
    # reader so Snowpark generates the correct COPY INTO column list.
    # CSV/JSON use the original schema.
    reader_schema = reader_schema_override or (
        loading_schema if file_format == "parquet" else schema
    )
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

    # SNOW-3554289: under PERMISSIVE, Spark CSV silently truncates or
    # nullifies fields that exceed the target column width; Snowflake CSV
    # COPY defaults to ``TRUNCATECOLUMNS = FALSE`` and aborts the row with
    # "String '...' is too long". Setting ``TRUNCATECOLUMNS = TRUE`` aligns
    # the row-level outcome with Spark. Scoped to CSV: the option only
    # applies to character-typed COPY targets, JSON loads into a single
    # VARIANT column where truncation is a no-op, and Parquet is
    # intentionally out of scope.
    if on_error == "PERMISSIVE" and file_format == "csv":
        copy_options["TRUNCATECOLUMNS"] = True

    # CSV-specific INCLUDE_METADATA / MATCH_BY_COLUMN_NAME wiring (plain
    # COPY paths only -- partitioned Parquet/JSON take the transformations
    # branch and emit metadata via an explicit SELECT list).
    #
    # SNOW-3348324 (server parameter ``ENABLE_INCLUDE_METADATA_WITHOUT_MBCN_CSV``,
    # on by default for SCOS via ``..._FOR_SCOS``) lets the server populate
    # INCLUDE_METADATA columns by name while loading file data positionally
    # into the remaining columns, so the same path works for both
    # PARSE_HEADER=TRUE (header -> name match, MBCN=CASE_INSENSITIVE) and
    # PARSE_HEADER=FALSE (positional, MBCN=NONE). MATCH_BY_COLUMN_NAME must
    # always be set whenever INCLUDE_METADATA is emitted -- snowpark-python's
    # client-side validation rejects INCLUDE_METADATA without it. We also set
    # MBCN=CASE_INSENSITIVE for header=true CSV without INCLUDE_METADATA so
    # regular header-based column matching keeps working.
    if file_format == "csv" and copy_transformations is None:
        csv_parse_header = bool(file_format_options.get("PARSE_HEADER", False))
        include_metadata: dict[str, str] = {}
        if needs_metadata and not has_partitions:
            include_metadata[
                analyzer_utils.quote_name_without_upper_casing(METADATA_FILENAME_COLUMN)
            ] = "METADATA$FILENAME"
        if corrupt_record_column is not None:
            include_metadata[
                analyzer_utils.quote_name_without_upper_casing(corrupt_record_column)
            ] = "METADATA$CORRUPT_RECORD"
        if include_metadata:
            copy_options["INCLUDE_METADATA"] = include_metadata
        if csv_parse_header or include_metadata:
            copy_options["MATCH_BY_COLUMN_NAME"] = (
                "CASE_INSENSITIVE" if csv_parse_header else "NONE"
            )
    elif file_format == "csv" and copy_transformations is not None:
        # SNOW-3216131 sub-fix 2 positional path.  The SELECT's ``$N``
        # references already drive the file-to-target column mapping, so
        # name-based matching must be off.  Set ``MATCH_BY_COLUMN_NAME=NONE``
        # explicitly rather than relying on Snowflake's default — keeps the
        # contract consistent with the ``copy_transformations is None``
        # branch above and future-proofs against a default change.
        copy_options["MATCH_BY_COLUMN_NAME"] = "NONE"

    return source_df.copy_into_table(
        target,
        files=relative_files,
        target_columns=copy_target_columns,
        transformations=copy_transformations,
        format_type_options=file_format_options,
        **copy_options,
    )
