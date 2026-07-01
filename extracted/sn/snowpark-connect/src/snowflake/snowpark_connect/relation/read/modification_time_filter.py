#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
"""Spark ``modifiedBefore`` / ``modifiedAfter`` read options (SNOW-3295605 / GAP-045).

Spark batch reads can filter source files by last-modification time. SCOS
implements this by listing stage files, applying the time bounds, and passing
explicit file paths to the existing format readers (avoiding broad COPY INTO
prefix scans that would include out-of-range files).
"""
from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any, NamedTuple, NoReturn
from zoneinfo import ZoneInfo

import pyspark.sql.connect.proto.relations_pb2 as relation_proto
from pyspark.errors.exceptions.base import AnalysisException

from snowflake import snowpark
from snowflake.snowpark.types import StructType
from snowflake.snowpark_connect.config import global_config
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.relation.io_utils import (
    convert_file_prefix_path,
    is_cloud_path,
)
from snowflake.snowpark_connect.relation.read.path_anchoring import (
    PathClassification,
    spark_glob_to_snowflake_regex,
)
from snowflake.snowpark_connect.relation.read.utils import (
    CLOUD_LIST_SCHEME_PARTS,
    cloud_list_path_to_relative,
    get_spark_column_names_from_snowpark_columns,
    rename_columns_as_snowflake_standard,
)
from snowflake.snowpark_connect.type_support import emulate_integral_types
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger

_MODIFIED_BEFORE_KEY = "modifiedbefore"
_MODIFIED_AFTER_KEY = "modifiedafter"
_TIMEZONE_KEY = "timezone"
_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"


def _raise_analysis_error(
    message: str,
    cause: BaseException | None = None,
    error_code: ErrorCodes = ErrorCodes.INVALID_FUNCTION_ARGUMENT,
) -> NoReturn:
    exception = AnalysisException(message)
    attach_custom_error_code(exception, error_code)
    if cause is not None:
        raise exception from cause
    raise exception


class ModifiedTimeFilters(NamedTuple):
    """Resolved modification-time bounds for a read-options dict."""

    modified_before: datetime | None
    modified_after: datetime | None
    timezone: str
    is_active: bool


def consume_modified_time_filters(
    options: dict[str, Any],
    session: snowpark.Session,
) -> ModifiedTimeFilters:
    """Pop ``modifiedBefore`` / ``modifiedAfter`` and parse bounds.

    ``timeZone`` is peeked (not removed) so it can still flow to format readers
    for data timestamp parsing and unsupported-option warnings when no bound is
    set. Mutates ``options`` in place so bound keys never leak to COPY INTO.
    Returns ``is_active=False`` when neither bound is set.
    """
    before_raw: str | None = None
    after_raw: str | None = None
    keys_to_pop = [
        k
        for k in list(options.keys())
        if k.lower() in (_MODIFIED_BEFORE_KEY, _MODIFIED_AFTER_KEY)
    ]
    for key in keys_to_pop:
        lowered = key.lower()
        value = options.pop(key)
        if value is None:
            continue
        if lowered == _MODIFIED_BEFORE_KEY:
            before_raw = str(value)
        elif lowered == _MODIFIED_AFTER_KEY:
            after_raw = str(value)

    if before_raw is None and after_raw is None:
        return ModifiedTimeFilters(None, None, "", False)

    tz_raw = _peek_timezone_option(options)
    tz_name = _resolve_timezone(tz_raw, session)
    modified_before = (
        _parse_modified_timestamp(before_raw, tz_name) if before_raw else None
    )
    modified_after = (
        _parse_modified_timestamp(after_raw, tz_name) if after_raw else None
    )
    return ModifiedTimeFilters(modified_before, modified_after, tz_name, is_active=True)


def expand_paths_for_modification_time_filter(
    paths: list[str],
    session: snowpark.Session,
    mod_filters: ModifiedTimeFilters,
    *,
    read_format: str,
    is_recursive: bool,
    clean_source_paths: list[str],
    path_classifications: list[PathClassification],
    options: dict[str, Any],
) -> list[str]:
    """LIST under each stage path, filter by mtime, return explicit file paths."""
    glob_filter = _get_path_glob_filter(options)
    glob_regex = (
        re.compile(spark_glob_to_snowflake_regex(glob_filter)) if glob_filter else None
    )
    result: list[str] = []
    for stage_path, source_path, classification in zip(
        paths, clean_source_paths, path_classifications
    ):
        result.extend(
            _expand_single_path(
                stage_path,
                source_path,
                session,
                mod_filters,
                read_format=read_format,
                is_recursive=is_recursive,
                classification=classification,
                glob_regex=glob_regex,
            )
        )
    return result


def empty_file_read_result(
    read_format: str,
    rel: relation_proto.Relation,
    schema: StructType | None,
    session: snowpark.Session,
) -> DataFrameContainer:
    """Return an empty DataFrame when modification-time filtering matches no files."""
    effective_schema = schema if schema is not None else StructType([])
    if not effective_schema.fields:
        format_label = read_format.upper()
        _raise_analysis_error(
            f"Unable to infer schema for {format_label}. It must be specified manually."
        )

    df = session.create_dataframe([], schema=effective_schema)
    spark_column_names = get_spark_column_names_from_snowpark_columns(
        [f.name for f in effective_schema.fields]
    )
    renamed_df, snowpark_column_names = rename_columns_as_snowflake_standard(
        df, rel.common.plan_id
    )
    return DataFrameContainer.create_with_column_mapping(
        dataframe=renamed_df,
        spark_column_names=spark_column_names,
        snowpark_column_names=snowpark_column_names,
        snowpark_column_types=[
            emulate_integral_types(f.datatype) for f in effective_schema.fields
        ],
    )


def _resolve_timezone(tz_raw: str | None, session: snowpark.Session) -> str:
    if tz_raw:
        return tz_raw
    session_tz = global_config.spark_sql_session_timeZone
    if session_tz:
        return str(session_tz)
    try:
        return str(session.get_current_timezone())
    except Exception as exc:
        logger.debug("Could not resolve session timezone: %s; defaulting to UTC", exc)
        return "UTC"


def _peek_timezone_option(options: dict[str, Any]) -> str | None:
    for key, value in options.items():
        if key.lower() == _TIMEZONE_KEY and value is not None:
            return str(value)
    return None


def _parse_modified_timestamp(value: str, tz_name: str) -> datetime:
    stripped = value.strip()
    # fromisoformat() accepts "Z" only in Python 3.11+; normalize for 3.10 compat.
    if stripped.endswith("Z"):
        stripped = stripped[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(stripped)
    except ValueError:
        try:
            parsed = datetime.strptime(stripped, _TIMESTAMP_FORMAT)
        except ValueError as exc:
            _raise_analysis_error(
                f"Invalid modification time filter timestamp '{value}'. "
                "Expected ISO-like format (e.g. 2020-06-01, "
                f"2020-06-01 13:00:00, or {_TIMESTAMP_FORMAT}).",
                cause=exc,
            )
    try:
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=ZoneInfo(tz_name))
        return parsed
    except Exception as exc:
        _raise_analysis_error(
            f"Invalid timeZone '{tz_name}' for modification time filter.",
            cause=exc,
        )


def _get_path_glob_filter(options: dict[str, Any]) -> str | None:
    for key in ("pathGlobFilter", "pathglobfilter"):
        value = options.get(key)
        if value:
            return str(value)
    return None


def _unquote_stage_path(stage_path: str) -> str:
    return stage_path.strip("'\"").rstrip("/")


def _expand_single_path(
    stage_path: str,
    source_path: str,
    session: snowpark.Session,
    mod_filters: ModifiedTimeFilters,
    *,
    read_format: str,
    is_recursive: bool,
    classification: PathClassification,
    glob_regex: re.Pattern | None,
) -> list[str]:
    unquoted_stage = _unquote_stage_path(stage_path)
    max_slashes = unquoted_stage.count("/") if not is_recursive else None

    local_file = convert_file_prefix_path(source_path.rstrip("/"))
    if (
        not is_cloud_path(source_path)
        and classification.kind == "file"
        and os.path.isfile(local_file)
    ):
        mtime = os.path.getmtime(local_file)
        if _passes_mtime_filter(mtime, mod_filters) and _passes_file_filters(
            os.path.basename(local_file),
            os.path.basename(local_file),
            read_format,
            glob_regex,
            max_slashes,
        ):
            return [_quoted_listed_path(unquoted_stage)]
        return []

    listed = _list_files_with_mtime(session, stage_path)
    matched: list[str] = []
    for full_name, relative_path, list_mtime in listed:
        if not _passes_file_filters(
            relative_path,
            os.path.basename(relative_path),
            read_format,
            glob_regex,
            max_slashes,
        ):
            continue
        mtime = _resolve_file_mtime(
            source_path, full_name, stage_path, relative_path, list_mtime
        )
        if _passes_mtime_filter(mtime, mod_filters):
            matched.append(_quoted_listed_path(full_name))
    return matched


def _list_files_with_mtime(
    session: snowpark.Session,
    stage_path: str,
) -> list[tuple[str, str, float]]:
    """Return ``(full_listed_name, stage_relative_path, list_mtime_epoch)`` tuples."""
    unquoted = stage_path.strip("'\"")
    cleaned = _escape_sql_single_quoted_string(unquoted)
    results: list[tuple[str, str, float]] = []
    try:
        rows = session.sql(f"LIST '{cleaned}'").collect()
    except Exception as exc:
        _raise_analysis_error(
            f"Failed to list files at '{cleaned}' while applying "
            f"modification time filter: {exc}",
            cause=exc,
            error_code=ErrorCodes.INTERNAL_ERROR,
        )

    stage_name_no_at = cleaned.lstrip("@")
    stage_prefix = stage_name_no_at.split("/")[0].lower()
    for row in rows:
        full_name = row[0]
        if full_name is None:
            continue
        if full_name.endswith("_SUCCESS"):
            continue
        relative = _stage_relative_path(full_name, stage_prefix)
        list_mtime = _row_mtime_to_epoch(row)
        results.append((full_name, relative, list_mtime))
    return results


def _stage_relative_path(full_name: str, stage_prefix: str) -> str:
    """Strip cloud / stage prefix so glob + depth filters run on relative paths."""
    cloud_relative = cloud_list_path_to_relative(full_name)
    if cloud_relative is not None:
        return cloud_relative
    name = full_name.lstrip("@")
    lowered = name.lower()
    prefix = stage_prefix.lower()
    if lowered.startswith(prefix + "/"):
        return name[len(prefix) + 1 :]
    if "/" in name:
        parts = name.split("/")[1:]
        return "/".join(parts)
    return name


def _row_mtime_to_epoch(row: Any) -> float:
    file_name = row[0] if len(row) > 0 else "<unknown>"
    try:
        return _value_to_epoch(row[3], file_name)
    except IndexError as exc:
        _raise_analysis_error(
            "LIST result row is missing modification-time column.",
            cause=exc,
            error_code=ErrorCodes.INTERNAL_ERROR,
        )


def _value_to_epoch(value: Any, file_name: str = "<unknown>") -> float:
    if value is None:
        _raise_analysis_error(
            "LIST returned a NULL modification-time column while applying "
            f"modifiedBefore/modifiedAfter filter for file {file_name!r}.",
            error_code=ErrorCodes.INTERNAL_ERROR,
        )
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.timestamp()
    if isinstance(value, str):
        if not value:
            return _raise_unparseable_mtime(value, file_name)
        try:
            parsed = parsedate_to_datetime(value)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed.timestamp()
        except (TypeError, ValueError):
            pass
        for fmt in (
            "%a, %d %b %Y %H:%M:%S %Z",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S",
            _TIMESTAMP_FORMAT,
        ):
            try:
                parsed = datetime.strptime(value, fmt)
                if parsed.tzinfo is None:
                    parsed = parsed.replace(tzinfo=timezone.utc)
                return parsed.timestamp()
            except ValueError:
                continue
    return _raise_unparseable_mtime(value, file_name)


def _raise_unparseable_mtime(value: Any, file_name: str = "<unknown>") -> NoReturn:
    _raise_analysis_error(
        f"Cannot parse LIST modification-time value {value!r} "
        f"(type {type(value).__name__}) for file {file_name!r}.",
        error_code=ErrorCodes.INTERNAL_ERROR,
    )


def _resolve_file_mtime(
    source_path: str,
    full_name: str,
    stage_path: str,
    relative_path: str,
    list_mtime: float,
) -> float:
    local_path = _local_path_for_listed_file(source_path, stage_path, relative_path)
    if local_path is not None and os.path.isfile(local_path):
        return os.path.getmtime(local_path)
    return list_mtime


def _local_path_for_listed_file(
    source_path: str,
    stage_path: str,
    relative_path: str,
) -> str | None:
    if is_cloud_path(source_path):
        return None
    source = convert_file_prefix_path(source_path.rstrip("/"))
    if os.path.isfile(source):
        return source
    if os.path.isdir(source):
        rel = relative_path.lstrip("/")
        unquoted_stage = _unquote_stage_path(stage_path)
        stage_suffix = unquoted_stage.split("/", 1)[1] if "/" in unquoted_stage else ""
        if stage_suffix and rel.lower().startswith(stage_suffix.lower() + "/"):
            rel = rel[len(stage_suffix) + 1 :]
        elif stage_suffix and rel.lower() == stage_suffix.lower():
            return None
        return os.path.join(source, rel.replace("/", os.sep))
    return None


def _passes_mtime_filter(mtime_epoch: float, mod_filters: ModifiedTimeFilters) -> bool:
    if mod_filters.modified_before is not None:
        if mtime_epoch >= mod_filters.modified_before.timestamp():
            return False
    if mod_filters.modified_after is not None:
        if mtime_epoch <= mod_filters.modified_after.timestamp():
            return False
    return True


def _passes_file_filters(
    relative_path: str,
    basename: str,
    read_format: str,
    glob_regex: re.Pattern | None,
    max_slashes: int | None,
) -> bool:
    if basename.startswith("_") or basename.startswith("."):
        return False
    fmt = read_format.lower()
    # Parquet/XML readers only consume these extensions on the normal
    # directory-read path (_FORMATS_HONORING_PATH_GLOB_FILTER in path_anchoring).
    if fmt == "parquet" and not basename.lower().endswith(".parquet"):
        return False
    if fmt == "xml" and not basename.lower().endswith(".xml"):
        return False
    if max_slashes is not None and relative_path.count("/") > max_slashes:
        return False
    # Spark pathGlobFilter matches basename only; see PartitioningAwareFileIndex.
    if glob_regex is not None and glob_regex.fullmatch(basename) is None:
        return False
    return True


def _escape_sql_single_quoted_string(value: str) -> str:
    return value.replace("'", "''")


def _quoted_listed_path(name: str) -> str:
    escaped = _escape_sql_single_quoted_string(name)
    if name.startswith(tuple(CLOUD_LIST_SCHEME_PARTS)):
        return f"'{escaped}'"
    if not name.startswith("@"):
        name = f"@{name}"
        escaped = _escape_sql_single_quoted_string(name)
    return f"'{escaped}'"
