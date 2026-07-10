#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
import contextlib
import dataclasses
import functools
import json
import re

from pyspark.errors.exceptions.connect import AnalysisException

from snowflake import snowpark
from snowflake.snowpark import Column, Session
from snowflake.snowpark._internal.analyzer.analyzer_utils import (
    create_file_format_statement,
    unquote_if_quoted,
)
from snowflake.snowpark._internal.utils import ttl_cache
from snowflake.snowpark.functions import col, date_trunc, equal_null, lit
from snowflake.snowpark.types import StructType
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.utils.identifiers import FQN, spark_to_sf_single_id
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
)

_MINUS_AT_THE_BEGINNING_REGEX = re.compile(r"^-")
_TTL_CACHE_EXIPRATION_TIME_SECONDS = 15


def cached_file_format(
    session: Session, file_format: str, format_type_options: dict[str, str]
) -> str:
    """
    Cache and return a file format name based on the given options.
    """

    function_name = _MINUS_AT_THE_BEGINNING_REGEX.sub(
        "1", str(hash(frozenset(format_type_options.items())))
    )
    file_format_name = f"__SNOWPARK_CONNECT_FILE_FORMAT__{file_format}_{function_name}"
    if file_format_name in session._file_formats:
        return file_format_name

    session.sql(
        create_file_format_statement(
            file_format_name,
            file_format,
            format_type_options,
            temp=True,
            if_not_exist=True,
            use_scoped_temp_objects=False,
            is_generated=True,
        )
    ).collect()

    session._file_formats.add(file_format_name)
    return file_format_name


@functools.cache
def file_format(
    session: Session, compression: str, record_delimiter: str = None
) -> str:
    """
    Create a temporary file format for reading text files in Snowpark Connect.
    """
    if record_delimiter is None:
        record_delimiter_sql = "NONE"
        identifier_delimiter = "NONE"
    else:
        # Convert delimiter to hex format (\xHH for each byte) for robustness
        # This handles special characters, multibyte chars, and control characters safely
        identifier_delimiter = record_delimiter.encode("utf-8").hex()
        record_delimiter_sql = "".join(
            f"\\x{b:02x}" for b in record_delimiter.encode("utf-8")
        )

    file_format_name = f"IDENTIFIER('__SNOWPARK_CONNECT_TEXT_FILE_FORMAT__{compression}_{identifier_delimiter}')"
    session.sql(
        f"""
    CREATE TEMPORARY FILE FORMAT IF NOT EXISTS  {file_format_name}
    RECORD_DELIMITER = '{record_delimiter_sql}'
    FIELD_DELIMITER = 'NONE'
    EMPTY_FIELD_AS_NULL = FALSE
    COMPRESSION = '{compression}'"""
    ).collect()

    return file_format_name


# caches table type with a time-to-live (TTL) expiration
@ttl_cache(ttl_seconds=_TTL_CACHE_EXIPRATION_TIME_SECONDS)
def get_table_type(
    snowpark_table_name: str,
    snowpark_session: Session,
) -> str:
    fqn = FQN.from_string(snowpark_table_name)
    with contextlib.suppress(Exception):
        if fqn.database is not None:
            return snowpark_session.catalog.getTable(
                table_name=fqn.name, schema=fqn.schema, database=fqn.database
            ).table_type
        elif fqn.schema is not None:
            return snowpark_session.catalog.getTable(
                table_name=fqn.name, schema=fqn.schema
            ).table_type
        else:
            return snowpark_session.catalog.getTable(table_name=fqn.name).table_type
    return "TABLE"


@dataclasses.dataclass
class PartitionField:
    name: str
    transform: str
    source_id: int

    @property
    def position(self) -> int:
        """
        0-indexed column position
        """
        return self.source_id - 1


@dataclasses.dataclass
class PartitionSpec:
    fields: list[PartitionField]

    def uses_transform(self) -> bool:
        """
        Returns True if any partition field uses a transform.
        """
        return any(f.transform != "identity" for f in self.fields)

    def columns(self) -> list[str]:
        return [f.name for f in self.fields]

    def partition_column_positions(self) -> list[int]:
        return [f.position for f in self.fields]


def get_partition_spec(table_name: str, session: Session) -> PartitionSpec | None:
    """
    Retrieves basic partition specs (list of fields with transforms) for the given table.
    """
    fqn = FQN.from_string(table_name)
    table_schema = ".".join(
        [part for part in [fqn.database, fqn.schema] if part is not None]
    )
    unquoted_table_name = unquote_if_quoted(fqn.name)

    # "show" is the only way to get partition specs
    if table_schema:
        show_query = (
            f"show iceberg tables like '{unquoted_table_name}' in schema {table_schema}"
        )
    else:
        show_query = f"show iceberg tables like '{unquoted_table_name}'"

    rows = session.sql(show_query).collect()

    # there should be only one table in the result, otherwise something's wrong
    if len(rows) != 1:
        exception = AnalysisException(
            f"[TABLE_NOT_FOUND] Could not find Iceberg table '{table_name}'"
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception

    spec_id = rows[0]["current_partition_spec_id"]
    if spec_id is None:
        return None

    partition_specs = [
        spec
        for spec in json.loads(rows[0]["partition_specs"])
        if spec["spec-id"] == spec_id
    ]
    if not partition_specs:
        return None

    if len(partition_specs) != 1:
        exception = AnalysisException(
            f"[TABLE_NOT_FOUND] Could not find partition spec for Iceberg table '{table_name}'"
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception

    fields = [
        PartitionField(f["name"], f["transform"], f["source-id"])
        for f in partition_specs[0]["fields"]
    ]
    return PartitionSpec(fields)


def get_overwrite_condition(
    distinct_partitions_df: snowpark.DataFrame,
    partition_column_names: list[str],
) -> Column | None:
    """
    Produces a (snowpark) column that can be used as an overwrite_condition when writing data to a table.
    """
    distinct_partitions = distinct_partitions_df.collect()
    if not distinct_partitions:
        return None

    or_conditions = []
    for row in distinct_partitions:
        and_conditions = []
        for partition_col, value in zip(partition_column_names, row):
            sf_col_name = spark_to_sf_single_id(
                unquote_if_quoted(partition_col), is_column=True
            )
            # partition values can be NULL, so we need to compare them with equal_null
            and_conditions.append(equal_null(col(sf_col_name), lit(value)))
        if and_conditions:
            combined_and = functools.reduce(lambda a, b: a & b, and_conditions)
            or_conditions.append(combined_and)

    if or_conditions:
        combined_or = functools.reduce(lambda a, b: a | b, or_conditions)
        return combined_or

    # no partitions in the input data
    return None


# Iceberg partition transforms supported in the dynamic-overwrite predicate, keyed on
# the transform string exactly as it appears in Iceberg table metadata
# (``PartitionField.transform``): singular time units. ``bucket[N]`` / ``truncate[W]``
# are bracketed and intentionally absent — the gate rejects them until implemented.
_DATE_TRUNC_UNIT_BY_TRANSFORM = {
    "year": "YEAR",
    "month": "MONTH",
    "day": "DAY",
    "hour": "HOUR",
}
SUPPORTED_OVERWRITE_TRANSFORMS = frozenset({"identity"}) | frozenset(
    _DATE_TRUNC_UNIT_BY_TRANSFORM
)


def overwrite_transform_supported(transform: str) -> bool:
    return transform in SUPPORTED_OVERWRITE_TRANSFORMS


def reject_unsupported_overwrite_transform(transform: str) -> None:
    """Gate: reject any transform SCOS cannot match correctly in the overwrite
    predicate, rather than silently producing wrong results / data loss."""
    if not overwrite_transform_supported(transform):
        exception = SnowparkConnectNotImplementedError(
            f"Iceberg partition overwrite is not supported for the '{transform}' "
            "transform"
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception


def apply_overwrite_partition_transform(column: Column, transform: str) -> Column:
    """Apply the Iceberg partition transform ``T(col)`` for the overwrite predicate.

    Keyed on the Iceberg-metadata transform name (``identity``/``year``/``month``/
    ``day``/``hour``). Applied on *both* sides of the predicate so the comparison is on
    the transformed partition value, not the raw value. Intended to be shared with the
    SQL ``INSERT OVERWRITE`` path (``map_sql.py``) in a follow-up; callers must gate
    unsupported transforms via ``reject_unsupported_overwrite_transform`` first.

    The table is partitioned by Snowflake's ``DAY``/``MONTH``/... DDL transform, so the
    predicate matches it with the equivalent ``DATE_TRUNC`` evaluated in the same
    (session) context Snowflake used to assign the partitions — NOT normalized to UTC.
    Both sides use the same expression, so rows are grouped consistently with the
    table's own partitioning.
    """
    if transform == "identity":
        return column
    unit = _DATE_TRUNC_UNIT_BY_TRANSFORM.get(transform)
    if unit is not None:
        return date_trunc(unit, column)
    reject_unsupported_overwrite_transform(transform)


def get_transform_overwrite_condition(
    input_df: snowpark.DataFrame,
    table_partition_spec: "PartitionSpec",
    column_map,
    table_schema: StructType,
) -> Column | None:
    """Build the dynamic-overwrite delete predicate for an Iceberg table that has a
    persisted partition spec, honoring non-identity transforms.

    Identity-only specs delegate to ``get_overwrite_condition`` (unchanged behavior).
    For transforms, each partition field's source column is resolved by NAME: its
    ``source_id``/``position`` is an ordinal into the *table* schema (the partition
    field's own name differs from the source column for transforms), so we read the
    source name from ``table_schema`` and match it to the input by name — order- and
    projection-independent, matching Spark's name-based ``overwritePartitions`` and the
    identity branch. The transform is applied on both the input side (to collect
    distinct transformed keys) and the predicate side. Unsupported transforms (bucket,
    truncate, void, unknown) are rejected by the gate.
    """
    # Gate first, so an unsupported transform errors regardless of input contents.
    for field in table_partition_spec.fields:
        reject_unsupported_overwrite_transform(field.transform)

    if not table_partition_spec.uses_transform():
        # Identity: preserve the existing name-based behavior exactly.
        names = column_map.get_snowpark_column_names_from_spark_column_names(
            table_partition_spec.columns()
        )
        distinct_partitions_df = input_df.select(*names).distinct()
        return get_overwrite_condition(distinct_partitions_df, names)

    # ``source_id``/``position`` indexes the TABLE schema (where source-ids are
    # defined), NOT the input DataFrame. Read each source column name from the table
    # schema and resolve it against the input by name, so an input whose columns are
    # reordered/projected still targets the correct partition (indexing the input by
    # table ordinal would build the predicate against the wrong column -> data loss).
    #
    # Resolve one field at a time and require exactly one match: the resolver is a
    # flat-map that silently skips unresolvable names and expands ambiguous ones, so a
    # single batched call could return a list that no longer lines up 1:1 with
    # ``fields`` -- pairing a transform with the wrong column and deleting the wrong
    # partitions. Per-field resolution keeps ``snowpark_names[i]`` aligned with
    # ``fields[i]`` and turns any skip/expand into a hard error instead of silent loss.
    snowpark_names = []
    for field in table_partition_spec.fields:
        source_name = unquote_if_quoted(table_schema.fields[field.position].name)
        resolved = column_map.get_snowpark_column_names_from_spark_column_names(
            [source_name]
        )
        if len(resolved) != 1:
            exception = ValueError(
                f"Iceberg partition source column {source_name!r} resolved to "
                f"{len(resolved)} input columns; expected exactly 1"
            )
            attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
            raise exception
        snowpark_names.append(resolved[0])
    # (snowpark_col_name, transform) per partition field.
    descriptors = [
        (snowpark_names[i], field.transform)
        for i, field in enumerate(table_partition_spec.fields)
    ]

    input_exprs = [
        apply_overwrite_partition_transform(col(name), transform).alias(
            f"__owp_key_{i}"
        )
        for i, (name, transform) in enumerate(descriptors)
    ]
    distinct_partitions = input_df.select(*input_exprs).distinct().collect()
    if not distinct_partitions:
        return None

    or_conditions = []
    for row in distinct_partitions:
        and_conditions = []
        for (name, transform), value in zip(descriptors, row):
            sf_col_name = spark_to_sf_single_id(unquote_if_quoted(name), is_column=True)
            target = apply_overwrite_partition_transform(col(sf_col_name), transform)
            and_conditions.append(equal_null(target, lit(value)))
        or_conditions.append(functools.reduce(lambda a, b: a & b, and_conditions))

    return functools.reduce(lambda a, b: a | b, or_conditions)
