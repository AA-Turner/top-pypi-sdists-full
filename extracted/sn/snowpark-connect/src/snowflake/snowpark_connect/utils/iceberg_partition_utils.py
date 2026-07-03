#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""Parse ``WriteOperationV2.partitioning_columns`` (DataFrameWriterV2
``partitionedBy``) into Snowflake Iceberg ``PARTITION BY`` expressions.

This is the Connect-server side of the translation Spark performs JVM-side in
``SparkConnectPlanner``: the protobuf carries identity columns and transform
functions, and there is no PySpark Connect helper that reads them back, so SCOS
owns the parse. Kept separate from the table-readback ``PartitionSpec`` in
``io_utils.py`` (which models a table's *existing* layout) to avoid conflating
"what the user requested" with "what Snowflake reports" (SNOW-3310107).
"""
import dataclasses
from collections.abc import Iterable

import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto

from snowflake.snowpark._internal.analyzer.analyzer_utils import unquote_if_quoted
from snowflake.snowpark_connect.column_name_handler import ColumnNameMap
from snowflake.snowpark_connect.config import global_config
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.utils.identifiers import spark_to_sf_single_id
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
)

# Spark partition-transform function name (as it arrives in the proto) ->
# Snowflake Iceberg PARTITION BY keyword. `bucket` is handled separately
# because it also carries a bucket-count literal. See SNOW-3310107.
SPARK_TO_SF_PARTITION_TRANSFORM = {
    "years": "YEAR",
    "months": "MONTH",
    "days": "DAY",
    "hours": "HOUR",
}


@dataclasses.dataclass(frozen=True)
class V2PartitionSpec:
    """One ``partitionedBy`` entry: identity column or partition transform.

    ``transform`` is the Snowflake keyword (``YEAR``/``MONTH``/``DAY``/
    ``HOUR``/``BUCKET``) or ``None`` for an identity column. ``num_buckets``
    is set only for ``BUCKET``.
    """

    column: str
    transform: str | None = None
    num_buckets: int | None = None


def _partition_arg_column(expr: expressions_proto.Expression) -> str:
    """Pull the column name out of a transform argument expression.

    The argument must be a plain column reference. A complex expression like
    ``days(col("ts").cast("timestamp"))`` arrives as a different ``expr_type``
    oneof variant; reading ``unresolved_attribute`` on it would silently return
    the proto default (``""``) and emit a malformed transform such as ``DAY("")``.
    """
    which = expr.WhichOneof("expr_type")
    if which != "unresolved_attribute":
        exception = ValueError(
            "Expected a column reference in partition transform argument, "
            f"got {which!r}"
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception
    return expr.unresolved_attribute.unparsed_identifier


def _require_arg_count(
    fn: expressions_proto.Expression.UnresolvedFunction, expected: int
) -> None:
    """Reject a malformed partition transform proto with too few arguments.

    The argument access below would otherwise raise a bare ``IndexError``
    rather than the controlled, error-coded exception used everywhere else
    in this module.
    """
    if len(fn.arguments) < expected:
        exception = ValueError(
            f"Partition transform '{fn.function_name}' expects {expected} "
            f"argument(s), got {len(fn.arguments)}"
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception


def _partition_bucket_count(expr: expressions_proto.Expression) -> int:
    """Read the constant bucket count from ``bucket(n, col)``'s first argument.

    Iceberg's bucket transform requires a literal integer number of buckets.
    PySpark's ``bucket`` signature also accepts a ``Column`` (e.g.
    ``bucket(col("n"), "id")``), but such an expression has no fixed partition
    count — we reject it rather than silently reading the proto default (0).
    """
    if expr.WhichOneof("expr_type") == "literal":
        literal_type = expr.literal.WhichOneof("literal_type")
        if literal_type == "integer":
            return expr.literal.integer
        if literal_type == "long":
            return expr.literal.long
    exception = ValueError(
        "bucket() partition transform requires a constant integer number of " "buckets"
    )
    attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
    raise exception


def parse_v2_partition_specs(
    partitioning_columns: Iterable[expressions_proto.Expression],
) -> list[V2PartitionSpec]:
    """Parse ``WriteOperationV2.partitioning_columns`` into partition specs.

    Identity columns arrive as ``unresolved_attribute``; transforms
    (``years``/``months``/``days``/``hours``/``bucket``) arrive as
    ``unresolved_function``. Only valid for Iceberg targets — an unsupported
    transform raises rather than silently dropping it, since that would change
    the physical layout the user requested (SNOW-3310107).

    Note: the SQL DDL path (``map_sql._extract_identity_partition_columns``)
    *warns and drops* non-identity transforms instead of raising; the
    DataFrameWriterV2 path is intentionally strict because silently ignoring a
    ``partitionedBy`` would mislead the caller about the on-disk layout.
    """
    specs: list[V2PartitionSpec] = []
    for expr in partitioning_columns:
        which = expr.WhichOneof("expr_type")
        if which == "unresolved_attribute":
            specs.append(
                V2PartitionSpec(column=expr.unresolved_attribute.unparsed_identifier)
            )
        elif which == "unresolved_function":
            fn = expr.unresolved_function
            name = fn.function_name.lower()
            if name == "bucket":
                # arguments: [num_buckets literal, column]. A non-literal count
                # (e.g. bucket(col("n"), "id")) is NOT supported — Iceberg needs
                # a constant integer; _partition_bucket_count rejects it.
                _require_arg_count(fn, 2)
                specs.append(
                    V2PartitionSpec(
                        column=_partition_arg_column(fn.arguments[1]),
                        transform="BUCKET",
                        num_buckets=_partition_bucket_count(fn.arguments[0]),
                    )
                )
            elif name in SPARK_TO_SF_PARTITION_TRANSFORM:
                _require_arg_count(fn, 1)
                specs.append(
                    V2PartitionSpec(
                        column=_partition_arg_column(fn.arguments[0]),
                        transform=SPARK_TO_SF_PARTITION_TRANSFORM[name],
                    )
                )
            else:
                exception = SnowparkConnectNotImplementedError(
                    f"Unsupported partition transform '{fn.function_name}' "
                    "for Iceberg table"
                )
                attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
                raise exception
        else:
            exception = SnowparkConnectNotImplementedError(
                "Unsupported partitionedBy expression for Iceberg table"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
    return specs


def _resolve_partition_column(
    spec: V2PartitionSpec, column_map: ColumnNameMap, is_cld: bool
) -> str:
    """Resolve a spec's source column to its Snowpark column name.

    CLD targets always normalize through ``spark_to_sf_single_id`` (matching
    the unconditional column-list normalization in ``_create_cld_iceberg_table``);
    non-CLD targets gate that on ``spark.sql.caseSensitive`` (matching the
    iceberg_config path).
    """
    resolved = column_map.get_snowpark_column_names_from_spark_column_names(
        [spec.column]
    )
    sf_col = resolved[0] if resolved else spec.column
    if is_cld or not global_config.spark_sql_caseSensitive:
        sf_col = spark_to_sf_single_id(unquote_if_quoted(sf_col), is_column=True)
    return sf_col


def render_partition_transform(
    transform: str | None, num_buckets: int | None, col: str
) -> str:
    """Wrap an already-prepared column string in its partition transform.

    ``col`` is the caller's chosen rendering of the inner column — a resolved
    name for the non-CLD ``iceberg_config`` path, or a quoted identifier for the
    CLD ``CREATE ICEBERG TABLE`` DDL path. Identity specs (``transform is None``)
    return the column unchanged; ``BUCKET`` prepends its count. Shared by both
    render sites so the two cannot drift out of sync (SNOW-3310107).
    """
    if transform is None:
        return col
    if num_buckets is not None:
        return f"{transform}({num_buckets}, {col})"
    return f"{transform}({col})"


def build_iceberg_partition_exprs(
    partition_specs: list[V2PartitionSpec],
    column_map: ColumnNameMap,
    is_cld: bool,
) -> list[str]:
    """Render partition specs as Snowflake ``PARTITION BY`` expression strings.

    The inner column is resolved through the same identifier pipeline the rest
    of the write path uses, then wrapped in the transform keyword, e.g.
    ``DAY("TS")`` or ``BUCKET(42, "ID")``. Used for the non-CLD
    ``iceberg_config`` path, where Snowpark drops these strings into the DDL
    verbatim. The CLD ``CREATE ICEBERG TABLE`` path instead consumes
    :func:`resolve_v2_partition_specs`, because it re-quotes each element and
    would corrupt a pre-rendered transform string like ``DAY("TS")``.
    """
    return [
        render_partition_transform(
            spec.transform,
            spec.num_buckets,
            _resolve_partition_column(spec, column_map, is_cld),
        )
        for spec in partition_specs
    ]


def resolve_v2_partition_specs(
    partition_specs: list[V2PartitionSpec],
    column_map: ColumnNameMap,
    is_cld: bool,
) -> list[V2PartitionSpec]:
    """Return specs with ``column`` resolved to its Snowpark name, transform
    untouched.

    The CLD ``CREATE ICEBERG TABLE`` path quotes the resolved column itself
    (via the same pipeline it uses for the column list) and assembles the
    transform keyword around the already-quoted identifier. Passing structured
    specs rather than the pre-rendered strings from
    :func:`build_iceberg_partition_exprs` keeps the transform keyword from being
    swept into a quoted identifier (which produced broken DDL like
    ``PARTITION BY ("DAY(""TS"")")``) — SNOW-3310107.
    """
    return [
        dataclasses.replace(
            spec, column=_resolve_partition_column(spec, column_map, is_cld)
        )
        for spec in partition_specs
    ]
