#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
import json
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

import numpy
import pandas
import pyarrow as pa
import pyarrow.compute as pc
import pyspark.sql.connect.proto.relations_pb2 as relation_proto
from pyarrow import Table
from pyspark.sql.pandas.types import _dedup_names

from snowflake.snowpark import types as sf_types
from snowflake.snowpark._internal.utils import is_in_stored_procedure
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.type_mapping import (
    SnowparkToArrowEmptyTableMapper,
    SnowparkToArrowMapper,
    SnowparkToArrowTempSchemaMapper,
)
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
)


def is_streaming(rel: relation_proto.Relation) -> bool:
    """
    Check if the relation is a streaming relation.

    A streaming relation is a relation that is the result of a streaming
    operation. This is used to determine if the relation should be shown
    immediately or if it should be stored in the session state for later use.
    """
    """Check if the relation is a streaming relation."""
    try:
        match rel.WhichOneof("rel_type"):
            case "read":
                return rel.read.is_streaming is True
            case "project":
                return is_streaming(rel.project.input)
            case "filter":
                return is_streaming(rel.filter.input)
            case "join":
                return is_streaming(rel.join.left) or is_streaming(rel.join.right)
            case "set_op":
                return is_streaming(rel.set_op.input)
            case "sort":
                return is_streaming(rel.sort.input)
            case "limit":
                return is_streaming(rel.limit.input)
            case "aggregate":
                return is_streaming(rel.aggregate.input)
            case "sample":
                return is_streaming(rel.sample.input)
            case "offset":
                return is_streaming(rel.offset.input)
            case "deduplicate":
                return is_streaming(rel.deduplicate.input)
            case "subquery_alias":
                return is_streaming(rel.subquery_alias.input)
            case "repartition":
                return is_streaming(rel.repartition.input)
            case "to_df":
                return is_streaming(rel.to_df.input)
            case "with_columns_renamed":
                return is_streaming(rel.with_columns_renamed.input)
            case "show_string":
                return is_streaming(rel.show_string.input)
            case "drop":
                return is_streaming(rel.drop.input)
            case "tail":
                return is_streaming(rel.tail.input)
            case "with_columns":
                return is_streaming(rel.with_columns.input)
            case "hint":
                return is_streaming(rel.hint.input)
            case "unpivot":
                return is_streaming(rel.unpivot.input)
            case "to_schema":
                return is_streaming(rel.to_schema.input)
            case "repartition_by_expression":
                return is_streaming(rel.repartition_by_expression.input)
            case "map_partitions":
                return is_streaming(rel.map_partitions.input)
            case "collect_metrics":
                return is_streaming(rel.collect_metrics.input)
            case "parse":
                return is_streaming(rel.parse.input)
            case "group_map":
                return is_streaming(rel.group_map.input)
            case "co_group_map":
                return is_streaming(rel.co_group_map.input)
            case "with_watermark":
                return is_streaming(rel.with_watermark.input)
            case "apply_in_pandas_with_state":
                return is_streaming(rel.apply_in_pandas.input)
            case "html_string":
                return is_streaming(rel.html_string.input)
            case "cached_remote_relation":
                exception = SnowparkConnectNotImplementedError(
                    "Cached remote relation not implemented"
                )
                attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
                raise exception
            case "common_inline_user_defined_table_function":
                return is_streaming(rel.common_inline_user_defined_table_function.input)
            case "fill_na":
                return is_streaming(rel.fill_na.input)
            case "drop_na":
                return is_streaming(rel.drop_na.input)
            case "replace":
                return is_streaming(rel.replace.input)
            case "stat":
                return is_streaming(rel.stat.input)
            case "summary":
                return is_streaming(rel.summary.input)
            case "crosstab":
                return is_streaming(rel.crosstab.input)
            case "describe":
                return is_streaming(rel.describe.input)
            case "cov":
                return is_streaming(rel.cov.input)
            case "corr":
                return is_streaming(rel.corr.input)
            case "approx_quantile":
                return is_streaming(rel.approx_quantile.input)
            case "freq_items":
                return is_streaming(rel.freq_items.input)
            case "sample_by":
                return is_streaming(rel.sample_by.input)
            case _:
                return False
    except AttributeError:
        # This is a leaf node with no `input`.
        return False


def _is_agg_function_with_single_row_result(rel: relation_proto.Relation) -> bool:
    """
    Detect a Spark Connect relation corresponding to a global aggregate.

    A Spark Connect `aggregate` relation with *no* grouping expressions corresponds to a global
    aggregation (e.g. `df.agg(...)` / `df.groupBy().agg(...)`). This always produces exactly one
    output row (even if the input is empty), regardless of the specific aggregate functions used.
    """
    try:
        if rel.WhichOneof("rel_type") != "aggregate":
            return False

        agg = rel.aggregate
        if len(agg.grouping_expressions) != 0:
            return False

        # an "aggregate" with no aggregate expressions is not meaningful.
        return len(agg.aggregate_expressions) > 0
    except Exception:
        # if we can't prove it is a global aggregate, keep the default path.
        return False


def pandas_to_arrow_batches_bytes(pandas_df: pandas.DataFrame) -> bytes:
    """
    Serialize a pandas DataFrame as Pyarrow encoded bytes.
    """
    # Pyarrow doesn't support duplicate column names, so we need to deduplicate them.
    # It is important that the schema is passed in whatever message we send back to the
    # client, otherwise the names will not be correct.
    pandas_df.columns = _dedup_names(pandas_df.columns)
    sink = pa.BufferOutputStream()
    batch = pa.RecordBatch.from_pandas(pandas_df, schema=None)
    with pa.ipc.new_stream(sink, batch.schema) as writer:
        writer.write_batch(batch)
    return sink.getvalue().to_pybytes()


_SNOWFLAKE_TIMESTAMP_FORMATS = (
    "%Y-%m-%d %H:%M:%S.%f %z",
    "%Y-%m-%d %H:%M:%S %z",
    "%Y-%m-%d %H:%M:%S.%f",
    "%Y-%m-%d %H:%M:%S",
)


def _parse_snowflake_timestamp(text: str) -> datetime:
    """Parse Snowflake's JSON rendering of a timestamp.

    ``TIMESTAMP_NTZ`` values carry no offset and parse to a naive datetime;
    ``TIMESTAMP_LTZ``/``TIMESTAMP_TZ`` values carry a numeric offset and parse to
    a tz-aware datetime, so the instant is preserved when pyarrow stores it as
    the target's UTC-based timestamp type.
    """
    text = text.strip()
    for fmt in _SNOWFLAKE_TIMESTAMP_FORMATS:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    raise ValueError(f"unrecognized timestamp format: {text!r}")


def _json_to_arrow_value(value: object, pa_type: pa.DataType) -> object:
    """Convert a JSON-decoded value into one pyarrow can build with ``pa_type``.

    Element scalars that Snowflake serializes as text (timestamps, dates, binary)
    or as JSON numbers that need exact precision (decimals) are converted to the
    matching Python object; nested list/struct/map values recurse; ``None`` passes
    through. Any format we do not recognize raises, and the caller keeps the
    original string column (never-regress).
    """
    if value is None:
        return None
    if pa.types.is_list(pa_type) or pa.types.is_large_list(pa_type):
        return [_json_to_arrow_value(item, pa_type.value_type) for item in value]
    if pa.types.is_struct(pa_type):
        by_lower_name = {str(k).lower(): v for k, v in value.items()}
        return {
            field.name: _json_to_arrow_value(
                by_lower_name.get(field.name.lower()), field.type
            )
            for field in pa_type
        }
    if pa.types.is_map(pa_type):
        return {k: _json_to_arrow_value(v, pa_type.item_type) for k, v in value.items()}
    if pa.types.is_decimal(pa_type):
        return value if isinstance(value, Decimal) else Decimal(str(value))
    if pa.types.is_timestamp(pa_type):
        return _parse_snowflake_timestamp(value)
    if pa.types.is_date(pa_type):
        return date.fromisoformat(value)
    if pa.types.is_binary(pa_type) or pa.types.is_large_binary(pa_type):
        return bytes.fromhex(value)
    if pa.types.is_floating(pa_type):
        return float(value)
    return value


def _is_structured_sp_eligible(sp_type: sf_types.DataType) -> bool:
    """Return True if this column type can arrive as a JSON string in an
    EXECUTE AS OWNER stored procedure and should be deserialized."""
    if isinstance(sp_type, sf_types.ArrayType):
        return sp_type.structured and sp_type.element_type is not None
    if isinstance(sp_type, sf_types.MapType):
        return sp_type.structured
    if isinstance(sp_type, sf_types.StructType):
        return sp_type.structured and len(sp_type.fields) > 0
    return False


def _deserialize_structured_string_columns(
    table: pa.Table, snowpark_schema: sf_types.StructType
) -> pa.Table:
    """Rebuild structured columns the server returned as JSON strings in SPs.

    SNOW-3746128: inside an ``EXECUTE AS OWNER`` stored procedure the
    ``ENABLE_STRUCTURED_TYPES_IN_SNOWPARK_CONNECT_RESPONSE`` parameter resolves
    from the owner's *account-level* value — it is not in the owner's-rights
    parameter allowlist, and SCOS cannot set it there (``ALTER SESSION`` is
    skipped/blocked). When it is off the server does not emit structured-type
    metadata, so the connector delivers structured ``ArrayType``, ``MapType``,
    and ``StructType`` columns as prettified JSON text.

    TODO(SNOW-3746128): the cleaner long-term fix is platform-side — allow
    ``ENABLE_STRUCTURED_TYPES_IN_SNOWPARK_CONNECT_RESPONSE`` to be honored from a
    user-level (or owner's-rights-inherited) setting so an EXECUTE AS OWNER
    procedure can opt in without an account-wide change. If that lands, this
    client-side deserialization can be retired.

    This runs only inside a stored procedure and only for columns whose Snowpark
    schema is a structured complex type (ArrayType/MapType/StructType) but whose
    Arrow column actually came back as a string — the exact mismatch that occurs
    when the parameter is off. It is a no-op everywhere else.

    If a cell fails to parse or an element value cannot be reconstructed for the
    target type, the original string column is kept — behavior is never worse
    than before the fix.
    """
    if not is_in_stored_procedure():
        return table

    fields = snowpark_schema.fields
    mapper = SnowparkToArrowEmptyTableMapper()
    for i in range(min(len(fields), table.num_columns)):
        sp_type = fields[i].datatype
        if not _is_structured_sp_eligible(sp_type):
            continue
        column = table.column(i)
        if not pa.types.is_string(column.type):
            continue
        field_name = table.schema.field(i).name
        try:
            target_type = mapper.map(sp_type, pa.null())
            parsed = [
                _json_to_arrow_value(
                    json.loads(value, parse_float=Decimal), target_type
                )
                if value is not None
                else None
                for value in column.to_pylist()
            ]
            rebuilt = pa.array(parsed, type=target_type)
        except Exception as exc:  # never regress: keep the original string column
            logger.debug(
                "SNOW-3746128: keeping column %s as string; could not deserialize "
                "structured array (%s)",
                field_name,
                exc,
            )
            continue
        table = table.set_column(i, pa.field(field_name, target_type), rebuilt)
    return table


def arrow_table_to_arrow_bytes(
    table: pa.Table, snowpark_schema: sf_types.StructType, spark_columns: list
) -> bytes:
    """
    Serialize a pyarrow.table as Pyarrow encoded bytes according to provided snowpark schema.
    """
    assert table.num_rows > 0, "Table must have at least one row"

    table = _deserialize_structured_string_columns(table, snowpark_schema)

    pa_schema_temp = pa.schema(
        SnowparkToArrowTempSchemaMapper().map_schema(
            snowpark_schema, pa.struct(table.schema)
        )
    )

    pa_schema_final = pa.schema(
        SnowparkToArrowMapper().map_schema(snowpark_schema, pa.struct(table.schema))
    )

    table = _cast_arrow_table(table, pa_schema_final, spark_columns, pa_schema_temp)
    # note that we don't need to track the original column name, since this helper function only needs to generate arrow
    # data bytes. When the arrow bytes are returned to spark connect client, an explicit schema would be passed along,
    # which contains expected column name. E.g.,
    #   return [
    #         proto_base.ExecutePlanResponse(
    #             session_id=request.session_id,
    #             operation_id=get_or_generate(operation_id),
    #             arrow_batch=proto_base.ExecutePlanResponse.ArrowBatch(
    #                 row_count=row_count,
    #                 data=arrow_bytes, # arrow bytes generated by this helper function
    #             ),
    #             schema=schema,    # schema containing correct column name
    #         ),
    #   ]
    sink = pa.BufferOutputStream()
    with pa.ipc.new_stream(sink, table.schema) as writer:
        writer.write_table(table)
    arrow_bytes = sink.getvalue().to_pybytes()
    return arrow_bytes


def _safe_cast_timestamp_columns(table: Table, target_pa_schema: pa.Schema) -> None:
    """Validate that columns being cast to a timestamp type don't overflow int64.

    The Snowflake connector may return numeric types (decimal128, int64) for
    timestamp results. The main cast uses safe=False to allow Spark-style integer
    overflow wrapping, but timestamp overflows should raise — matching Spark's
    ArithmeticException behavior. We do this by attempting a safe=True cast on
    just the timestamp columns and letting ArrowInvalid propagate.
    """
    for i, target_field in enumerate(target_pa_schema):
        if not pa.types.is_timestamp(target_field.type):
            continue
        src_type = table.schema.field(i).type
        if pa.types.is_timestamp(src_type):
            continue
        table.column(i).cast(target_field.type, safe=True)


def _has_only_inherited_nulls(parent: pa.Array, child: pa.Array) -> bool:
    """True when *child* has nulls but ALL of them sit at positions where
    *parent* is also null — i.e. the child nulls are Arrow physical
    artefacts from the struct's flat storage layout, not real user-supplied
    data.

    Arrow stores structs as a validity bitmap + parallel child arrays.
    When the struct is null at a position (validity=false), the child
    array at that index contains undefined/garbage data that may appear
    as null.  These "inherited" nulls are harmless — no code ever reads
    them.

    Returns False when any child null appears at a position where the
    parent struct is non-null (validity=true), meaning the user provided
    a struct with a genuinely missing field value.
    """
    if child.null_count == 0:
        return False
    if parent.null_count == 0:
        return False
    parent_valid = pc.is_valid(parent)
    child_null = pc.is_null(child)
    return not pc.any(pc.and_(parent_valid, child_null)).as_py()


def _pa_type_relaxed_for_nulls(
    arr: pa.Array,
    pa_type: pa.DataType,
    parent: pa.Array | None = None,
) -> pa.DataType:
    """Return *pa_type* with field nullability widened to True only for
    struct children whose nulls are inherited from a null parent struct
    (Arrow physical artefacts from flat child-array storage).

    Children with "real" nulls — where the parent struct exists
    (validity=true) but the child value is null — keep their declared
    nullability so that genuine non-nullable constraint violations
    propagate as errors downstream.
    """
    if pa.types.is_struct(pa_type) and pa.types.is_struct(arr.type):
        if pa_type.num_fields != arr.type.num_fields:
            return pa_type
        return pa.struct(
            [
                pa.field(
                    pa_type.field(i).name,
                    _pa_type_relaxed_for_nulls(
                        arr.field(i), pa_type.field(i).type, parent=arr
                    ),
                    nullable=(
                        pa_type.field(i).nullable
                        or _has_only_inherited_nulls(arr, arr.field(i))
                    ),
                )
                for i in range(pa_type.num_fields)
            ]
        )
    # Array/Map nullability is never relaxed — only recurse for inner element
    # types to handle nested structs within list/map values.
    if pa.types.is_list(pa_type) and pa.types.is_list(arr.type):
        vf = pa_type.value_field
        values = arr.values
        return pa.list_(
            pa.field(
                vf.name,
                _pa_type_relaxed_for_nulls(values, vf.type, parent=arr),
                nullable=vf.nullable,
            )
        )
    if pa.types.is_map(pa_type) and pa.types.is_map(arr.type):
        kf = pa_type.key_field
        itf = pa_type.item_field
        entries = arr.values
        keys = entries.field(0)
        items = entries.field(1)
        return pa.map_(
            pa.field(
                kf.name,
                _pa_type_relaxed_for_nulls(keys, kf.type, parent=arr),
                nullable=kf.nullable,
            ),
            pa.field(
                itf.name,
                _pa_type_relaxed_for_nulls(items, itf.type, parent=arr),
                nullable=itf.nullable,
            ),
        )
    return pa_type


def _relax_pa_schema_for_nulls(table: Table, schema: pa.Schema) -> pa.Schema:
    """Return *schema* with nested field nullability widened wherever the
    corresponding data carries nulls inherited from a null parent struct.

    Top-level column nullability is never changed — a null in a non-nullable
    top-level column is a genuine data error that should propagate.  Only
    nested struct/list/map children are relaxed, because Arrow's physical
    layout can place null slots in child buffers under a null parent even
    when the child field is declared non-nullable.
    """
    relaxed = []
    for i in range(len(schema)):
        col = table.column(i).combine_chunks()
        field = schema.field(i)
        relaxed.append(
            pa.field(
                field.name,
                _pa_type_relaxed_for_nulls(col, field.type),
                nullable=field.nullable,
            )
        )
    return pa.schema(relaxed)


def _offsets_with_validity(arr: pa.Array) -> pa.Array:
    """Return a list/map offsets array that also encodes the parent validity.

    ``MapArray.from_arrays`` / ``ListArray.from_arrays`` reproduce a null slot
    when the corresponding entry in the offsets array is null. ``arr.offsets``
    itself carries no validity, so we splice the parent null mask back in.
    """
    offsets = arr.offsets
    if arr.null_count == 0:
        return offsets
    valid = pc.is_valid(arr).to_pylist()
    mask = [not v for v in valid] + [False]  # last offset is always valid
    return pa.array(offsets.to_pylist(), type=offsets.type, mask=mask)


def _safe_cast_array(arr: pa.Array | pa.ChunkedArray, target: pa.DataType):
    """Cast an arrow array to ``target``, avoiding a pyarrow 14.0.x crash.

    pyarrow 14.0.x aborts (native SIGABRT) when ``cast`` changes the key type of
    a map whose value is a nested type (e.g. ``map<decimal128, list<double>>`` →
    ``map<int64, list<double>>``). We sidestep the buggy cast kernel by rebuilding
    map/list/struct arrays from their recursively-cast child arrays. Primitive
    types fall through to the normal ``cast``.
    """
    if isinstance(arr, pa.ChunkedArray):
        if arr.num_chunks == 0:
            return arr.cast(target, safe=False)
        return pa.chunked_array(
            [_safe_cast_array(chunk, target) for chunk in arr.chunks], type=target
        )
    if arr.type.equals(target):
        return arr
    if pa.types.is_map(target) and pa.types.is_map(arr.type):
        keys = _safe_cast_array(arr.keys, target.key_type)
        items = _safe_cast_array(arr.items, target.item_type)
        return pa.MapArray.from_arrays(_offsets_with_validity(arr), keys, items)
    if (pa.types.is_list(target) or pa.types.is_large_list(target)) and (
        pa.types.is_list(arr.type) or pa.types.is_large_list(arr.type)
    ):
        values = _safe_cast_array(arr.values, target.value_type)
        return pa.ListArray.from_arrays(_offsets_with_validity(arr), values)
    if pa.types.is_struct(target) and pa.types.is_struct(arr.type):
        fields = [
            _safe_cast_array(arr.field(i), target.field(i).type)
            for i in range(target.num_fields)
        ]
        names = [target.field(i).name for i in range(target.num_fields)]
        mask = pc.is_null(arr) if arr.null_count else None
        return pa.StructArray.from_arrays(fields, names=names, mask=mask)
    return arr.cast(target, safe=False)


def _target_has_map(pa_type: pa.DataType) -> bool:
    """True if ``pa_type`` is, or nests, a map type."""
    if pa.types.is_map(pa_type):
        return True
    if pa.types.is_list(pa_type) or pa.types.is_large_list(pa_type):
        return _target_has_map(pa_type.value_type)
    if pa.types.is_struct(pa_type):
        return any(
            _target_has_map(pa_type.field(i).type) for i in range(pa_type.num_fields)
        )
    return False


def _safe_cast_table(table: Table, target_pa_schema: pa.Schema) -> Table:
    """Cast a table to ``target_pa_schema`` avoiding the pyarrow 14.0.x map-cast crash.

    Only map-bearing columns take the manual rebuild path; every other column
    keeps the standard ``cast`` behaviour so non-map results are unaffected.
    """

    import numpy

    if not numpy.__version__.startswith("14."):
        return table.cast(target_pa_schema, safe=False)

    if not any(_target_has_map(field.type) for field in target_pa_schema):
        return table.cast(target_pa_schema, safe=False)
    columns = [
        _safe_cast_array(table.column(i), target_pa_schema.field(i).type)
        for i in range(table.num_columns)
    ]
    return pa.Table.from_arrays(columns, schema=target_pa_schema)


def _cast_arrow_table(
    table: Table,
    target_pa_schema: pa.Schema,
    spark_columns: list,
    temp_pa_schema: Optional[pa.Schema] = None,
) -> Table:
    # 1. rename column names to 0,1,2, etc. to avoid unmatching names due to undesired factors like quotes.
    # 2. casting is required here because sometimes arrow table does use expected data type. E.g., for LongType,
    #       pyarrow table uses decimal128(38,0), which converts to Decimal instead of Long on client side.
    table = table.rename_columns([str(i) for i in range(table.num_columns)])

    if temp_pa_schema is not None and not temp_pa_schema.equals(target_pa_schema):
        # cast to temp_pa_schema is necessary for cases when i.e. the pyarrow table has int64,
        # but the snowpark schema is Decimal128(p, s) with p <= 18.
        table = _safe_cast_table(table, temp_pa_schema)

    # Cast non-timestamp columns with safe=False (Spark allows integer overflow
    # wrapping, so we must not reject decimal128 → int64 overflows here).
    # For timestamp columns, use safe=True to catch values that overflow int64
    # microseconds — matching Spark's ArithmeticException on timestamp overflow.
    _safe_cast_timestamp_columns(table, target_pa_schema)
    table = _safe_cast_table(table, target_pa_schema)
    table = table.rename_columns(spark_columns)
    return table


def pandas_empty_table_to_arrow_bytes(
    pandas_df: pandas.DataFrame,
    snowpark_schema: sf_types.StructType,
    spark_columns: list,
) -> bytes:
    """
    Serialize an empty pandas DataFrame as Pyarrow encoded bytes according to provided snowpark schema and spark columns.
    """
    pandas_df.columns = _dedup_names(pandas_df.columns)
    table = pa.Table.from_pandas(pandas_df)
    pa_schema = pa.schema(
        SnowparkToArrowEmptyTableMapper().map_schema(
            snowpark_schema, pa.struct(table.schema)
        )
    )
    table = _cast_arrow_table(table, pa_schema, spark_columns)

    if numpy.__version__.startswith("14."):
        # _cast_arrow_table restores the (possibly duplicate) spark column names, so
        # dedup again before to_pandas — pyarrow <15 raises "Found non-unique column
        # index" on duplicate labels. pandas_to_arrow_batches_bytes re-dedups and the
        # client relies on the explicit response schema, so these names are throwaway.
        table = table.rename_columns(_dedup_names(table.column_names))
    return pandas_to_arrow_batches_bytes(table.to_pandas())
