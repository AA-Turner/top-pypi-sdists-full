"""
schema_profiler_duckdb.py
=========================

Compute DataAssetFieldProfiles directly with DuckDB/Arrow.
No pandas dependency, no copies; works on DuckDB relations
or Arrow tables that you already produce in schema_detection.py.
"""

from __future__ import annotations

from typing import Dict, Mapping, Union

import duckdb
import pyarrow as pa
from loguru import logger

from gable.cli.helpers.data_asset_s3.duckdb_connection import get_resilient_duckdb
from gable.cli.helpers.data_asset_s3.path_pattern_manager import (
    UUID_REGEX_V1,
    UUID_REGEX_V3,
    UUID_REGEX_V4,
    UUID_REGEX_V5,
)
from gable.openapi import (
    DataAssetFieldProfile,
    DataAssetFieldProfileBoolean,
    DataAssetFieldProfileList,
    DataAssetFieldProfileNumber,
    DataAssetFieldProfileOther,
    DataAssetFieldProfileString,
    DataAssetFieldProfileTemporal,
    DataAssetFieldProfileUnion,
    DataAssetFieldProfileUUID,
    DataAssetFieldsToProfilesMapping,
    S3SamplingParameters,
)


# ────────────────────────────────────────────────────────────────────────────
#  PUBLIC ENTRY
# ────────────────────────────────────────────────────────────────────────────
def get_data_asset_field_profiles_for_data_asset(
    recap_schema: dict,
    file_to_obj: Mapping[str, pa.Table],
    event_name: str,
    sampling_params: S3SamplingParameters,
) -> DataAssetFieldsToProfilesMapping | None:
    """
    Build { column_name -> DataAssetFieldProfile } using DuckDB aggregates,
    no pandas required.
    """
    logger.debug(f"[Profiler] computing profiles for {event_name}")

    if not file_to_obj:
        logger.warning(f"[Profiler] No sample data for {event_name}")
        return None

    # ------------------------------------------------------------------ #
    # 1 · Register every sample once (Arrow table) in a fresh connection
    # ------------------------------------------------------------------ #
    resilient_duckdb = get_resilient_duckdb()
    view_names: list[str] = []

    try:
        for idx, (_, obj) in enumerate(file_to_obj.items()):
            view = f"sample_view_{idx}"
            if isinstance(obj, pa.Table):
                resilient_duckdb.register(view, obj)
            else:
                raise TypeError("Expected Arrow table")
            view_names.append(view)  # ← append once

        union_sql = " UNION ALL ".join(f"SELECT * FROM {v}" for v in view_names)
        merged_rel = resilient_duckdb.query(union_sql)

        # ------------------------------------------------------------------ #
        # 2 · Map fully-qualified column names → schema fragments
        # ------------------------------------------------------------------ #
        column_schema: Dict[str, dict] = {}
        _populate_column_schemas(recap_schema, column_schema)

        # ------------------------------------------------------------------ #
        # 3 · Profile column-by-column
        # ------------------------------------------------------------------ #
        profiles: Dict[str, DataAssetFieldProfile] = {}

        for col, schema in column_schema.items():
            if col not in merged_rel.columns:
                logger.warning(f"[Profiler] Column {col} missing in sample; skipping")
                continue
            try:
                profiles[col] = _profile_column(
                    resilient_duckdb.connection,
                    merged_rel,
                    col,
                    schema,
                    sampling_params,
                    list(file_to_obj.keys()),  # Pass actual file names
                )
            except Exception as e:
                logger.error(f"[Profiler] Error profiling {col}: {e}")

        return DataAssetFieldsToProfilesMapping(root=profiles)
    except Exception as e:
        raise Exception(f"[Profiler] Error profiling {event_name}: {e}")


# ────────────────────────────────────────────────────────────────────────────
#  HELPERS
# ────────────────────────────────────────────────────────────────────────────
def _populate_column_schemas(schema: dict, out: dict, prefix: str = ""):
    for field in schema["fields"]:
        name = prefix + field["name"]
        # TODO: Implement nested field profiling in future iteration if needed
        # if field["type"] == "struct":
        #     _populate_column_schemas(field, out, name + ".")
        # else:
        out[name] = field


def _profile_column(
    con: duckdb.DuckDBPyConnection,  # kept for regex BOOL_AND call
    rel: duckdb.DuckDBPyRelation,
    col: str,
    schema: dict,
    params: S3SamplingParameters,
    sampled_files: list[str],
) -> DataAssetFieldProfile:
    col_q = f'"{col}"'  # always quote identifiers

    total_rows_row = rel.aggregate("COUNT(*)").fetchone()
    total_rows = total_rows_row[0] if total_rows_row is not None else 0
    null_cnt_row = rel.aggregate(f"COUNT(*) - COUNT({col_q})").fetchone()
    null_cnt = null_cnt_row[0] if null_cnt_row is not None else 0

    nullable = total_rows == 0 or null_cnt > 0

    try:
        col_type = rel.to_arrow_table().column(col).type
    except Exception:
        col_type = schema["type"]

    # ─────────────────────────────  BOOLEAN  ──────────────────────────────
    if is_boolean_type(col_type):
        true_cnt_row = rel.aggregate(f"SUM({col_q} = 'true')").fetchone()
        true_cnt = true_cnt_row[0] if true_cnt_row is not None else 0
        false_cnt_row = rel.aggregate(f"SUM({col_q} = 'false')").fetchone()
        false_cnt = false_cnt_row[0] if false_cnt_row is not None else 0
        profile = DataAssetFieldProfileBoolean(
            profileType="boolean",
            sampledRecordsCount=total_rows,
            nullable=nullable,
            nullCount=null_cnt,
            trueCount=true_cnt or 0,
            falseCount=false_cnt or 0,
            sampledFiles=sampled_files,
            samplingParameters=params,
        )

    # ─────────────────────────────  NUMERIC / TEMPORAL  ───────────────────
    elif is_numeric_type(col_type):
        min_v_row = rel.aggregate(f"MIN({col_q})").fetchone()
        min_v = min_v_row[0] if min_v_row is not None else None
        max_v_row = rel.aggregate(f"MAX({col_q})").fetchone()
        max_v = max_v_row[0] if max_v_row is not None else None

        if _schema_is_date(schema):
            profile = DataAssetFieldProfileTemporal(
                profileType="temporal",
                sampledRecordsCount=total_rows,
                nullable=nullable,
                nullCount=null_cnt,
                min=min_v,  # type: ignore
                max=max_v,  # type: ignore
                format="",
                sampledFiles=sampled_files,
                samplingParameters=params,
            )
        else:
            uniq_row = rel.aggregate(f"COUNT(DISTINCT {col_q})").fetchone()
            uniq = uniq_row[0] if uniq_row is not None else 0

            profile = DataAssetFieldProfileNumber(
                profileType="number",
                sampledRecordsCount=total_rows,
                nullable=nullable,
                nullCount=null_cnt,
                uniqueCount=uniq,  # type: ignore
                min=min_v,  # type: ignore
                max=max_v,  # type: ignore
                sampledFiles=sampled_files,
                samplingParameters=params,
            )

    # ─────────────────────────────  STRING  ───────────────────────────────
    elif is_string_type(col_type):
        uniq_row = rel.aggregate(f"COUNT(DISTINCT {col_q})").fetchone()
        uniq = uniq_row[0] if uniq_row is not None else 0
        empty_cnt_row = rel.aggregate(f"SUM({col_q} = '')").fetchone()
        empty_cnt = empty_cnt_row[0] if empty_cnt_row is not None else 0
        max_len_row = rel.aggregate(f"MAX(LENGTH({col_q}))").fetchone()
        max_len = max_len_row[0] if max_len_row is not None else None
        min_len_row = rel.aggregate(f"MIN(LENGTH({col_q}))").fetchone()
        min_len = min_len_row[0] if min_len_row is not None else None

        # UUID-v4 check – use relation aggregate instead of SELECT … FROM (rel)
        is_v4_row = rel.aggregate(
            f"BOOL_AND(REGEXP_MATCHES({col_q}, '^{UUID_REGEX_V4}$'))"
        ).fetchone()
        is_v4 = is_v4_row[0] if is_v4_row is not None else False

        if is_v4:
            profile = DataAssetFieldProfileUUID(
                profileType="uuid",
                sampledRecordsCount=total_rows,
                nullable=nullable,
                nullCount=null_cnt,
                uuidVersion=4,
                emptyCount=empty_cnt or 0,
                uniqueCount=uniq,  # type: ignore
                maxLength=max_len,  # type: ignore
                minLength=min_len,  # type: ignore
                sampledFiles=sampled_files,
                samplingParameters=params,
            )
        else:
            profile = DataAssetFieldProfileString(
                profileType="string",
                sampledRecordsCount=total_rows,
                nullable=nullable,
                nullCount=null_cnt,
                emptyCount=empty_cnt or 0,
                uniqueCount=uniq,  # type: ignore
                maxLength=max_len,  # type: ignore
                minLength=min_len,  # type: ignore
                sampledFiles=sampled_files,
                samplingParameters=params,
            )

    # ─────────────────────────────  LIST  ─────────────────────────────────
    elif is_list_type(col_type):
        max_len_row = rel.aggregate(f"MAX(ARRAY_LENGTH({col_q}))").fetchone()
        max_len = max_len_row[0] if max_len_row is not None else None
        min_len_row = rel.aggregate(f"MIN(ARRAY_LENGTH({col_q}))").fetchone()
        min_len = min_len_row[0] if min_len_row is not None else None

        profile = DataAssetFieldProfileList(
            profileType="list",
            sampledRecordsCount=total_rows,
            nullable=nullable,
            nullCount=null_cnt,
            maxLength=max_len,  # type: ignore
            minLength=min_len,  # type: ignore
            sampledFiles=sampled_files,
            samplingParameters=params,
        )

    # ─────────────────────────────  UNION / OTHER  ────────────────────────
    elif is_union_type(col_type):
        profile = DataAssetFieldProfileUnion(
            profileType="union",
            sampledRecordsCount=total_rows,
            nullable=nullable,
            profiles=[],  # recursion can be added later
            sampledFiles=sampled_files,
            samplingParameters=params,
        )
    else:
        profile = DataAssetFieldProfileOther(
            profileType="other",
            sampledRecordsCount=total_rows,
            nullable=nullable,
            nullCount=null_cnt,
            sampledFiles=sampled_files,
            samplingParameters=params,
        )

    return DataAssetFieldProfile(root=profile)


def _schema_is_date(schema: dict) -> bool:
    return schema["type"] == "int" and schema.get("logical") in ("Timestamp", "Date")


def is_boolean_type(type: Union[str, pa.DataType]) -> bool:
    if isinstance(type, pa.DataType):
        return pa.types.is_boolean(type)
    if hasattr(type, "arrow_type"):
        type = type.arrow_type  # type: ignore
        return pa.types.is_boolean(type)
    if type == "bool" or type == "boolean":
        return True

    return False


def is_numeric_type(type: Union[str, pa.DataType]) -> bool:
    """
    Check if type is numeric using multiple strategies.

    Args:
        type: Either a string representation or type object

    Returns:
        bool: True if the type is numeric
    """
    # If it's a PyArrow type, use built-in methods
    if isinstance(type, pa.DataType):
        return (
            pa.types.is_integer(type)
            or pa.types.is_floating(type)
            or pa.types.is_decimal(type)
        )

    # If it has an arrow_type attribute, use that
    if hasattr(type, "arrow_type"):
        type = type.arrow_type  # type: ignore
        return (
            pa.types.is_integer(type)
            or pa.types.is_floating(type)
            or pa.types.is_decimal(type)
        )

    # Fall back to string-based checking
    type_str = str(type).upper()

    # Comprehensive numeric type patterns
    numeric_patterns = ["INT", "FLOAT", "DOUBLE", "REAL", "DECIMAL", "NUMERIC"]

    # Check for exact matches first
    exact_numeric_types = {
        "TINYINT",
        "SMALLINT",
        "INTEGER",
        "BIGINT",
        "INT",
        "INT8",
        "INT16",
        "INT32",
        "INT64",
        "UTINYINT",
        "USMALLINT",
        "UINTEGER",
        "UBIGINT",
        "UINT8",
        "UINT16",
        "UINT32",
        "UINT64",
        "FLOAT",
        "DOUBLE",
        "FLOAT32",
        "FLOAT64",
        "REAL",
        "DECIMAL",
        "NUMERIC",
    }

    if type_str in exact_numeric_types:
        return True

    # Check for parameterized types
    if type_str.startswith(("DECIMAL(", "NUMERIC(")):
        return True

    # Check for pattern matches
    return any(pattern in type_str for pattern in numeric_patterns)


def is_string_type(type: Union[str, pa.DataType]) -> bool:
    """
    Check if type is string using multiple strategies.

    Args:
        type: Either a string representation or type object

    Returns:
        bool: True if the type is string
    """
    if isinstance(type, pa.DataType):
        return pa.types.is_string(type)
    if hasattr(type, "arrow_type"):
        type = type.arrow_type  # type: ignore
        return pa.types.is_string(type)

    if type == "string":
        return True

    return False


def is_list_type(type: Union[str, pa.DataType]) -> bool:
    if isinstance(type, pa.DataType):
        return pa.types.is_list(type)
    if hasattr(type, "arrow_type"):
        type = type.arrow_type  # type: ignore
        return pa.types.is_list(type)
    if type == "list":
        return True

    return False


def is_union_type(type: Union[str, pa.DataType]) -> bool:
    if isinstance(type, pa.DataType):
        return pa.types.is_union(type)
    if hasattr(type, "arrow_type"):
        type = type.arrow_type  # type: ignore
        return pa.types.is_union(type)
    if type == "union":
        return True

    return False
