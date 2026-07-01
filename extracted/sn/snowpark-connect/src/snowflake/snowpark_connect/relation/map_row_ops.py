#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
import math

import pandas
import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto
import pyspark.sql.connect.proto.relations_pb2 as relation_proto
from pyspark.errors.exceptions.base import AnalysisException, IllegalArgumentException

import snowflake.snowpark_connect.relation.utils as utils
from snowflake import snowpark
from snowflake.snowpark import functions as snowpark_fn
from snowflake.snowpark.functions import (
    col,
    expr as snowpark_expr,
    iff,
    is_null,
    lit,
    object_construct_keep_null,
    to_binary,
)
from snowflake.snowpark.types import (
    ArrayType,
    BinaryType,
    BooleanType,
    ByteType,
    DecimalType,
    DoubleType,
    FloatType,
    IntegerType,
    LongType,
    NullType,
    ShortType,
    StringType,
    StructField,
    StructType,
    _IntegralType,
)
from snowflake.snowpark_connect.column_name_handler import (
    ColumnNameMap,
    set_schema_getter,
    union_restorable_name,
)
from snowflake.snowpark_connect.config import global_config
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.expression.literal import get_literal_field_and_name
from snowflake.snowpark_connect.expression.map_expression import (
    map_single_column_expression,
)
from snowflake.snowpark_connect.expression.map_unresolved_function import (
    _find_common_type,
)
from snowflake.snowpark_connect.expression.typer import ExpressionTyper
from snowflake.snowpark_connect.relation.map_relation import map_relation
from snowflake.snowpark_connect.relation.read.metadata_utils import (
    METADATA_FILENAME_COLUMN,
    without_hidden_columns,
    without_internal_columns,
)
from snowflake.snowpark_connect.typed_column import FieldType
from snowflake.snowpark_connect.utils.identifiers import (
    split_fully_qualified_spark_name,
)
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
)


def cast_columns(
    df_container: DataFrameContainer,
    target_field_types: list[FieldType],
    column_map: ColumnNameMap,
):
    df_schema = get_schema_from_result(df_container)
    df_datatypes = [f.datatype for f in df_schema.fields]
    target_datatypes = [t.datatype for t in target_field_types]

    if df_datatypes == target_datatypes:
        # Types match but nullable may differ — return a new container with
        # updated cached_schema_getter. Do NOT call set_schema_getter or
        # _apply_cached_schema_getter on the shared DataFrame: the original
        # container may be cached and reused in other operations.
        schema = DataFrameContainer._create_schema_from_types(
            column_map.get_snowpark_columns(), target_field_types
        )
        if schema is None:
            return df_container
        new_container = DataFrameContainer(
            dataframe=df_container.dataframe,
            column_map=column_map,
            table_name=df_container.table_name,
            alias=df_container.alias,
            partition_hint=df_container.partition_hint,
            dataframe_hint=df_container.dataframe_hint,
            can_be_cached=df_container.can_be_cached,
            can_be_materialized=df_container.can_be_materialized,
            aggregate_metadata=df_container._aggregate_metadata,
        )
        # Assign directly — do NOT pass through the constructor, which calls
        # _apply_cached_schema_getter and would mutate the shared DataFrame.
        new_container.cached_schema_getter = lambda s=schema: s
        return new_container

    df: snowpark.DataFrame = df_container.dataframe
    new_columns = []
    for i, field in enumerate(df_schema.fields):
        col_name = field.name
        current_type = field.datatype
        target_type = target_datatypes[i]
        new_columns.append(
            _cast_column_if_needed(df, col_name, current_type, target_type)
        )

    new_df = df.select(new_columns)
    return DataFrameContainer.create_with_column_mapping(
        dataframe=new_df,
        spark_column_names=column_map.get_spark_columns(),
        snowpark_column_names=column_map.get_snowpark_columns(),
        snowpark_column_types=target_field_types,
        column_metadata=column_map.column_metadata,
        parent_column_name_map=column_map,
    )


def get_schema_from_result(
    result: DataFrameContainer,
) -> StructType:
    """
    Get schema from a DataFrameContainer, using cached schema if available to avoid extra queries.
    """
    if (
        hasattr(result, "cached_schema_getter")
        and result.cached_schema_getter is not None
    ):
        return result.cached_schema_getter()
    else:
        return result.dataframe.schema


def _cast_column_if_needed(
    df: snowpark.DataFrame,
    col_name: str,
    current_type: snowpark.types.DataType,
    target_type: snowpark.types.DataType,
) -> snowpark.Column:
    """
    Cast a column to target type if needed, handling special cases like StringType to BinaryType.

    Returns the column expression (cast if types differ, unchanged otherwise).
    """
    if isinstance(current_type, StringType) and isinstance(target_type, BinaryType):
        return to_binary(df[col_name], "utf-8").alias(col_name)
    elif isinstance(current_type, NullType) and current_type != target_type:
        from snowflake.snowpark._internal.type_utils import convert_sp_to_sf_type

        sf_type_str = convert_sp_to_sf_type(target_type)
        return snowpark_expr(f"NULL :: {sf_type_str}").alias(col_name)
    elif current_type != target_type:
        return df[col_name].cast(target_type).alias(col_name)
    else:
        return df[col_name]


def _needs_reshape(source: StructType, target: StructType) -> bool:
    return {f.name for f in source.fields} != {f.name for f in target.fields}


def _build_struct_reshape_sql(
    var: str, source_type: StructType, target_type: StructType
) -> str:
    """Build a SQL expression string that reshapes a struct variable to target_type.
    Used both directly (via OBJECT_CONSTRUCT_KEEP_NULL) and inside TRANSFORM lambdas."""
    source_map = {f.name: f for f in source_type.fields}
    parts: list[str] = []
    for tf in target_type.fields:
        sf = source_map.get(tf.name)
        if sf is None:
            parts.append(f"'{tf.name}', NULL")
        elif (
            isinstance(sf.datatype, StructType)
            and isinstance(tf.datatype, StructType)
            and _needs_reshape(sf.datatype, tf.datatype)
        ):
            nested = _build_struct_reshape_sql(
                f'{var}:"{tf.name}"', sf.datatype, tf.datatype
            )
            parts.append(f"'{tf.name}', {nested}")
        elif (
            isinstance(sf.datatype, ArrayType)
            and isinstance(tf.datatype, ArrayType)
            and isinstance(sf.datatype.element_type, StructType)
            and isinstance(tf.datatype.element_type, StructType)
            and _needs_reshape(sf.datatype.element_type, tf.datatype.element_type)
        ):
            inner = _build_array_struct_reshape_sql(
                f'{var}:"{tf.name}"', sf.datatype, tf.datatype
            )
            parts.append(f"'{tf.name}', {inner}")
        else:
            parts.append(f"'{tf.name}', {var}:\"{tf.name}\"")
    return f"object_construct_keep_null({', '.join(parts)})"


def _build_array_struct_reshape_sql(
    var: str, source_type: ArrayType, target_type: ArrayType
) -> str:
    """Build a TRANSFORM(..., el -> ...) SQL expression for array-of-struct reshaping."""
    inner_sql = _build_struct_reshape_sql(
        "el", source_type.element_type, target_type.element_type
    )
    return f"transform({var}, el -> {inner_sql})"


def _build_struct_reshape_expr(
    col_expr: snowpark.Column,
    source_type: StructType,
    target_type: StructType,
) -> snowpark.Column:
    """Build a column expression that reshapes a struct column to match target_type,
    filling missing fields with NULL and recursing into nested structs/arrays."""
    kv_pairs: list[snowpark.Column] = []
    source_map = {f.name: f for f in source_type.fields}
    for tf in target_type.fields:
        kv_pairs.append(lit(tf.name))
        sf = source_map.get(tf.name)
        if sf is None:
            kv_pairs.append(lit(None).cast(tf.datatype))
        elif (
            isinstance(sf.datatype, StructType)
            and isinstance(tf.datatype, StructType)
            and _needs_reshape(sf.datatype, tf.datatype)
        ):
            kv_pairs.append(
                _build_struct_reshape_expr(col_expr[tf.name], sf.datatype, tf.datatype)
            )
        elif (
            isinstance(sf.datatype, ArrayType)
            and isinstance(tf.datatype, ArrayType)
            and isinstance(sf.datatype.element_type, StructType)
            and isinstance(tf.datatype.element_type, StructType)
            and _needs_reshape(sf.datatype.element_type, tf.datatype.element_type)
        ):
            reshape_sql = _build_array_struct_reshape_sql(
                f'"{tf.name}"', sf.datatype, tf.datatype
            )
            kv_pairs.append(snowpark_fn.sql_expr(reshape_sql))
        else:
            kv_pairs.append(col_expr[tf.name])

    reshaped = object_construct_keep_null(*kv_pairs).cast(target_type)
    return iff(is_null(col_expr), lit(None).cast(target_type), reshaped)


def _reshape_df_columns_by_name(
    df: snowpark.DataFrame,
    type_map: dict[str, snowpark.types.DataType],
) -> snowpark.DataFrame:
    """Cast DataFrame columns per type_map. For struct/array-of-struct columns whose
    field sets differ, reshapes via OBJECT_CONSTRUCT_KEEP_NULL / TRANSFORM."""
    if not type_map:
        return df

    new_fields: list[StructField] = []
    select_cols = []
    for field in df.schema.fields:
        target_type = type_map.get(field.name)
        current_type = field.datatype
        if (
            target_type is not None
            and isinstance(target_type, StructType)
            and isinstance(current_type, StructType)
            and _needs_reshape(current_type, target_type)
        ):
            select_cols.append(
                _build_struct_reshape_expr(
                    df[field.name], current_type, target_type
                ).alias(field.name)
            )
            new_fields.append(StructField(field.name, target_type, field.nullable))
        elif (
            target_type is not None
            and isinstance(target_type, ArrayType)
            and isinstance(current_type, ArrayType)
            and isinstance(target_type.element_type, StructType)
            and isinstance(current_type.element_type, StructType)
            and _needs_reshape(current_type.element_type, target_type.element_type)
        ):
            reshape_sql = _build_array_struct_reshape_sql(
                f'"{field.name}"', current_type, target_type
            )
            select_cols.append(
                snowpark_fn.sql_expr(reshape_sql).cast(target_type).alias(field.name)
            )
            new_fields.append(StructField(field.name, target_type, field.nullable))
        elif target_type is not None:
            select_cols.append(
                _cast_column_if_needed(df, field.name, current_type, target_type)
            )
            new_fields.append(StructField(field.name, target_type, field.nullable))
        else:
            select_cols.append(df[field.name])
            new_fields.append(field)

    new_df = df.select(select_cols)
    set_schema_getter(new_df, lambda: StructType(new_fields))
    return new_df


def _coerce_set_op_types(
    left_df: DataFrameContainer,
    right_df: DataFrameContainer,
    operation_name: str,
) -> tuple[DataFrameContainer, DataFrameContainer]:
    """
    Coerce types for set operations (UNION, INTERSECT, EXCEPT).

    Validates column counts match and casts both sides to common types when needed.

    Returns updated (left_result, right_result).
    """
    left_fields = get_schema_from_result(left_df).fields
    right_fields = get_schema_from_result(right_df).fields
    left_dtypes = [f.datatype for f in left_fields]
    right_dtypes = [f.datatype for f in right_fields]

    if len(left_dtypes) != len(right_dtypes):
        exception = AnalysisException(
            f"{operation_name}: the number of columns must match"
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
        raise exception

    # Compute merged nullable per set operation semantics
    # EXCEPT: rows come from left only → left nullable
    # INTERSECT: rows that appear in both → nullable = left AND right
    # UNION: rows from either side → nullable = left OR right
    op = operation_name.upper()
    target_nullables = []
    for lf, rf in zip(left_fields, right_fields):
        if op == "EXCEPT":
            target_nullables.append(lf.nullable)
        elif op == "INTERSECT":
            target_nullables.append(lf.nullable and rf.nullable)
        else:  # UNION
            target_nullables.append(lf.nullable or rf.nullable)

    if left_dtypes != right_dtypes:
        target_dtypes = []
        for left_type, right_type in zip(left_dtypes, right_dtypes):
            try:
                target_dtypes.append(
                    _find_common_type(
                        [left_type, right_type],
                        narrow_string=global_config.spark_sql_ansi_enabled,
                    )
                )
            except AnalysisException as exception:
                if "DATATYPE_MISMATCH.DATA_DIFF_TYPES" in exception.message:
                    exception = AnalysisException(
                        f"""[INCOMPATIBLE_COLUMN_TYPE] {operation_name} can only be performed on tables with compatible column types. "{str(left_type)}" type which is not compatible with "{str(right_type)}". """
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
    else:
        target_dtypes = left_dtypes

    target_field_types = [
        FieldType(dt, nullable) for dt, nullable in zip(target_dtypes, target_nullables)
    ]

    left_df = cast_columns(
        left_df,
        target_field_types,
        left_df.column_map,
    )
    right_df = cast_columns(
        right_df,
        target_field_types,
        right_df.column_map,
    )

    return left_df, right_df


def map_deduplicate(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Deduplicate a DataFrame based on a Relation's deduplicate.

    The deduplicate is a list of columns that is applied to the DataFrame.
    """
    input_container = without_internal_columns(map_relation(rel.deduplicate.input))
    input_df = input_container.dataframe

    if (
        rel.deduplicate.HasField("within_watermark")
        and rel.deduplicate.within_watermark
    ):
        exception = AnalysisException(
            "dropDuplicatesWithinWatermark is not supported with batch DataFrames/DataSets"
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    # Spark's Deduplicate is a UnaryNode that dedups on the user-visible output
    # and propagates `metadataOutput` (i.e. qualifier-access-only columns)
    # unchanged. Mirror that here: dedup on the visible snowpark columns only,
    # but keep QAO shadows in the column map so plan-id-qualified references
    # downstream (e.g. `df.distinct().select(df_left["x"])`) still resolve.
    #
    # Perf shortcut: snowpark's `drop_duplicates(*subset)` renders to
    # `row_number() OVER (...) AS "<random>"` SQL with a fresh random alias on
    # every call (see `generate_random_alphanumeric()` in snowpark), defeating
    # the SQL-string-keyed describe-query cache. The no-args form delegates
    # to `self.distinct()` which renders to a deterministic `GROUP BY ...`
    # SQL that does cache. When the subset we'd pass equals every physical
    # column of `input_df`, the two forms are semantically identical, so
    # prefer the no-args form for cache locality.
    all_snowpark_columns_in_current_projection = {
        c.snowpark_name for c in input_container.column_map.columns
    }
    if (
        rel.deduplicate.HasField("all_columns_as_keys")
        and rel.deduplicate.all_columns_as_keys
    ):
        subset_snowpark_columns = input_container.column_map.get_snowpark_columns()
    else:
        subset_snowpark_columns = input_container.column_map.get_snowpark_column_names_from_spark_column_names(
            list(rel.deduplicate.column_names)
        )

    if set(subset_snowpark_columns) == all_snowpark_columns_in_current_projection:
        result: snowpark.DataFrame = input_df.drop_duplicates()
    else:
        result: snowpark.DataFrame = input_df.drop_duplicates(*subset_snowpark_columns)

    return DataFrameContainer(
        result,
        input_container.column_map,
        input_container.table_name,
        input_container.alias,
        cached_schema_getter=lambda: input_df.schema,
    )


def map_dropna(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Drop NA values from the input DataFrame.
    """
    input_container = map_relation(rel.drop_na.input)
    input_df = input_container.dataframe

    if rel.drop_na.HasField("min_non_nulls"):
        thresh = rel.drop_na.min_non_nulls
        how = "all"
    else:
        thresh = None
        how = "any"
    if len(rel.drop_na.cols) > 0:
        columns: list[str] = []
        nested_columns: list[str] = []
        for c in rel.drop_na.cols:
            # Check if column has nested path (e.g., "c1.c1-1")
            try:
                col_parts = c.split(".")
                base_col = col_parts[0]
                snowpark_col = input_container.column_map.get_snowpark_column_name_from_spark_column_name(
                    base_col
                )
                if len(col_parts) > 1:
                    # For nested columns, build SQL expression for filtering
                    # Snowflake uses bracket notation for nested field access
                    nested_path = "".join(f"['{p}']" for p in col_parts[1:])
                    nested_columns.append(f"{snowpark_col}{nested_path}")
                else:
                    columns.append(snowpark_col)
            except Exception:
                available_cols = input_container.column_map.get_spark_columns()
                exception = AnalysisException(
                    f"[UNRESOLVED_COLUMN.WITH_SUGGESTION] A column or function parameter with name `{c}` cannot be resolved. "
                    f"Did you mean one of the following? [{', '.join(f'`{col}`' for col in available_cols)}]."
                )
                attach_custom_error_code(exception, ErrorCodes.COLUMN_NOT_FOUND)
                raise exception

        result: snowpark.DataFrame = input_df

        def _is_null_or_nan(col_expr: str) -> str:
            return f"({col_expr} IS NULL OR {col_expr}::VARCHAR = 'NaN')"

        # When thresh is specified with nested columns, we need to combine all columns
        # in a single threshold check
        if thresh is not None and nested_columns:
            all_columns = columns + nested_columns
            # Count non-null AND non-NaN values (Spark treats NaN as null for dropna)
            non_null_exprs = [
                f"CASE WHEN NOT {_is_null_or_nan(col_name)} THEN 1 ELSE 0 END"
                for col_name in all_columns
            ]
            sum_non_null_expr = " + ".join(non_null_exprs)
            threshold_condition = f"({sum_non_null_expr}) >= {thresh}"
            result = result.filter(snowpark_expr(threshold_condition))
        else:
            # Handle regular columns with Snowpark's dropna
            if columns:
                result = result.dropna(how=how, subset=columns, thresh=thresh)

            # Handle nested columns with filter expressions
            # Note: Spark treats NaN as null for dropna, so we filter both NULL and NaN
            if nested_columns:
                if how == "any":
                    # For "any", drop rows where ANY of the nested columns is NULL or NaN
                    result = result.filter(
                        snowpark_expr(
                            " AND ".join(
                                f"NOT {_is_null_or_nan(nested_col)}"
                                for nested_col in nested_columns
                            )
                        )
                    )
                else:
                    # For "all", drop rows where ALL of the nested columns are NULL or NaN
                    all_null_or_nan_condition = " AND ".join(
                        _is_null_or_nan(nc) for nc in nested_columns
                    )
                    result = result.filter(
                        snowpark_expr(f"NOT ({all_null_or_nan_condition})")
                    )
    elif input_container.has_hidden_columns():
        columns = input_container.column_map.get_snowpark_columns()
        result: snowpark.DataFrame = input_df.dropna(
            how=how, subset=columns, thresh=thresh
        )
    else:
        result: snowpark.DataFrame = input_df.dropna(how=how, thresh=thresh)

    return DataFrameContainer(
        result,
        input_container.column_map,
        input_container.table_name,
        input_container.alias,
        cached_schema_getter=lambda: input_df.schema,
    )


def map_fillna(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Fill NA values in the DataFrame.

    The `fill_value` is a scalar value that will be used to replace NaN values.
    """
    input_container = map_relation(rel.fill_na.input)
    input_df = input_container.dataframe
    schema_fields = {field.name: field for field in input_df.schema.fields}

    if len(rel.fill_na.cols) > 0:
        # Note: "*" in cols is NOT a wildcard but a literal column name reference.
        # In Spark, col("*") refers to a column named "*", not all columns.
        # If no column named "*" exists, fillna is a no-op for that column reference.
        spark_col_names = list(rel.fill_na.cols)

        # When a single fill value is provided alongside a list of column names, the
        # user called fillna(value, subset=[...]).  Spark validates that every column
        # in the subset actually exists in the schema and raises AnalysisException for
        # any missing top-level column (SNOW-3372862).
        #
        # When len(values) > 1 the user called fillna({"col": value, ...}) (dict mode).
        # In that mode Spark silently skips missing dict keys, so we preserve the
        # original ignore-and-continue behaviour for dict mode.
        #
        # Nested / fully-qualified paths (e.g. "struct_col.field") are not fully
        # validated in SCOS — missing nested fields are silently ignored regardless of
        # mode (tracked separately).
        is_subset_mode = len(rel.fill_na.values) == 1

        columns: list[str] = []
        valid_indices: list[int] = []
        for i, c in enumerate(spark_col_names):
            col_parts = split_fully_qualified_spark_name(c)
            base_col = col_parts[0]
            is_nested = len(col_parts) > 1
            try:
                col_name = input_container.column_map.get_snowpark_column_name_from_spark_column_name(
                    base_col
                )
                columns.append(col_name)
                valid_indices.append(i)
            except Exception:
                if c == "*":
                    # col("*") refers to a literal column named "*", not a wildcard.
                    # Spark silently ignores it when no such column exists.
                    continue
                if is_subset_mode and not is_nested:
                    # Top-level column missing in subset mode — raise immediately,
                    # matching Spark behaviour.
                    available_cols = input_container.column_map.get_spark_columns()
                    exception = AnalysisException(
                        f"[UNRESOLVED_COLUMN.WITH_SUGGESTION] A column or function parameter with name `{c}` cannot be resolved. "
                        f"Did you mean one of the following? [{', '.join(f'`{col}`' for col in available_cols)}]."
                    )
                    attach_custom_error_code(exception, ErrorCodes.COLUMN_NOT_FOUND)
                    raise exception
                # Otherwise (dict mode or nested path): silently skip the missing column.

        raw_values = [get_literal_field_and_name(v)[0] for v in rel.fill_na.values]
        if len(raw_values) == 1:
            # This happens when the client uses the `subset` parameter.
            values = raw_values * len(columns)
        else:
            # Filter values to only include those for existing columns
            values = [raw_values[i] for i in valid_indices]

        # If no valid columns found, return the input unchanged
        if not columns:
            return DataFrameContainer(
                input_df,
                input_container.column_map,
                input_container.table_name,
                input_container.alias,
                cached_schema_getter=lambda: input_df.schema,
            )

        assert len(columns) == len(
            values
        ), "FILLNA: number of columns and values must match"

        # Spark casts float fill values to int for integer columns; Snowpark doesn't
        converted_values = [
            int(val)
            if isinstance(val, float)
            and col_name in schema_fields
            and isinstance(schema_fields[col_name].datatype, _IntegralType)
            else val
            for col_name, val in zip(columns, values)
        ]

        result = input_df.fillna(
            dict(zip(columns, converted_values)), include_decimal=True
        )
    else:
        assert len(rel.fill_na.values) == 1
        proto_value: expressions_proto.Expression.Literal = rel.fill_na.values[0]
        fill_value = get_literal_field_and_name(proto_value)[0]

        has_hidden_columns = input_container.has_hidden_columns()
        visible_columns = [
            c.snowpark_name
            for c in input_container.column_map.columns
            if c.is_visible and c.snowpark_name != METADATA_FILENAME_COLUMN
        ]

        # Spark casts float fill values to int for integer columns; Snowpark doesn't
        if isinstance(fill_value, float):
            visible_columns_set = set(visible_columns)
            fill_value_dict: dict[str, float | int] = {
                field.name: int(fill_value)
                if isinstance(field.datatype, _IntegralType)
                else fill_value
                for field in input_df.schema.fields
                if field.name in visible_columns_set
            }
            result = input_df.fillna(fill_value_dict, include_decimal=True)
        elif has_hidden_columns or METADATA_FILENAME_COLUMN in schema_fields:
            result = input_df.fillna(
                fill_value, subset=visible_columns, include_decimal=True
            )
        else:
            result = input_df.fillna(fill_value, include_decimal=True)

    return DataFrameContainer(
        result,
        input_container.column_map,
        input_container.table_name,
        input_container.alias,
        cached_schema_getter=lambda: input_df.schema,
    )


def map_union(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Union two DataFrames together.

    The two DataFrames must have the same schema.
    """
    # todo: preserve metadata internal columns
    # Union also drops qualified-access-only metadata (USING-join source columns) —
    # they are not part of either input's user-visible schema. SNOW-2443454.
    left_result = without_hidden_columns(map_relation(rel.set_op.left_input))
    right_result = without_hidden_columns(map_relation(rel.set_op.right_input))
    left_df = left_result.dataframe
    right_df = right_result.dataframe
    allow_missing_columns = bool(rel.set_op.allow_missing_columns)

    if not rel.set_op.by_name:
        left_result, right_result = _coerce_set_op_types(
            left_result, right_result, "UNION"
        )
        left_df = left_result.dataframe
        right_df = right_result.dataframe

    if rel.set_op.by_name:
        # To use unionByName, we need to have the same column names.
        # We rename the columns back to their originals using the map
        left_column_map = left_result.column_map
        left_table_name = left_result.table_name
        right_column_map = right_result.column_map
        columns_to_restore: dict[str, tuple[str, str]] = {}

        original_right_schema = right_df.schema
        original_left_schema = left_df.schema

        right_renamed_fields = []
        for field in original_right_schema.fields:
            spark_name = (
                right_column_map.get_spark_column_name_from_snowpark_column_name(
                    field.name
                )
            )
            new_field_name = union_restorable_name(spark_name)
            columns_to_restore[new_field_name] = (
                spark_name,
                field.name,
            )
            right_renamed_fields.append(
                StructField(new_field_name, field.datatype, field.nullable)
            )
        if right_renamed_fields:
            right_df = right_df.select(
                [
                    col(field.name).alias(renamed.name)
                    for field, renamed in zip(
                        original_right_schema.fields, right_renamed_fields
                    )
                ]
            )
        set_schema_getter(right_df, lambda: StructType(right_renamed_fields))

        left_renamed_fields = []
        for field in original_left_schema.fields:
            spark_name = (
                left_column_map.get_spark_column_name_from_snowpark_column_name(
                    field.name
                )
            )
            new_field_name = union_restorable_name(spark_name)
            columns_to_restore[new_field_name] = (
                spark_name,
                field.name,
            )
            left_renamed_fields.append(
                StructField(new_field_name, field.datatype, field.nullable)
            )
        if left_renamed_fields:
            left_df = left_df.select(
                [
                    col(field.name).alias(renamed.name)
                    for field, renamed in zip(
                        original_left_schema.fields, left_renamed_fields
                    )
                ]
            )
        set_schema_getter(left_df, lambda: StructType(left_renamed_fields))

        left_type_map = {f.name: f.datatype for f in left_renamed_fields}
        right_type_map = {f.name: f.datatype for f in right_renamed_fields}
        shared_columns = set(left_type_map) & set(right_type_map)

        common_type_map = {}
        for col_name in shared_columns:
            if left_type_map[col_name] != right_type_map[col_name]:
                common_type_map[col_name] = _find_common_type(
                    [left_type_map[col_name], right_type_map[col_name]],
                    narrow_string=global_config.spark_sql_ansi_enabled,
                    merge_structs=allow_missing_columns,
                )

        left_df = _reshape_df_columns_by_name(left_df, common_type_map)
        right_df = _reshape_df_columns_by_name(right_df, common_type_map)
        result = _union_by_name_optimized(left_df, right_df, allow_missing_columns)

        spark_columns = []
        snowpark_columns = []
        select_exprs = []

        left_nullable_map = {f.name: f.nullable for f in left_renamed_fields}
        right_nullable_map = {f.name: f.nullable for f in right_renamed_fields}
        snowpark_column_types = [
            FieldType(
                f.datatype,
                left_nullable_map.get(f.name, True)
                or right_nullable_map.get(f.name, True),
            )
            for f in result.schema.fields
        ]

        for col_ in result.columns:
            spark_col_to_restore, snowpark_col_to_restore = columns_to_restore[
                union_restorable_name(col_)
            ]
            select_exprs.append(col(col_).alias(snowpark_col_to_restore))
            spark_columns.append(spark_col_to_restore)
            snowpark_columns.append(snowpark_col_to_restore)
        result = result.select(select_exprs)

        left_df_col_metadata = left_column_map.column_metadata or {}
        right_df_col_metadata = right_column_map.column_metadata or {}
        merged_column_metadata = left_df_col_metadata | right_df_col_metadata

        return DataFrameContainer.create_with_column_mapping(
            result,
            spark_column_names=spark_columns,
            snowpark_column_types=snowpark_column_types,
            snowpark_column_names=snowpark_columns,
            column_metadata=merged_column_metadata,
            table_name=left_table_name,
        )
    elif rel.set_op.is_all:
        result = left_df.unionAll(right_df)
        _left_schema = get_schema_from_result(left_result)
        _right_schema = get_schema_from_result(right_result)
        return DataFrameContainer(
            result,
            column_map=left_result.column_map,
            cached_schema_getter=lambda: StructType(
                [
                    StructField(
                        lf.name,
                        lf.datatype,
                        lf.nullable or rf.nullable,
                    )
                    for lf, rf in zip(_left_schema.fields, _right_schema.fields)
                ]
            ),
        )
    else:
        result = left_df.union(right_df)
        _left_schema = get_schema_from_result(left_result)
        _right_schema = get_schema_from_result(right_result)
        # union operation does not preserve column qualifiers
        return DataFrameContainer(
            result,
            column_map=left_result.column_map,
            cached_schema_getter=lambda: StructType(
                [
                    StructField(
                        lf.name,
                        lf.datatype,
                        lf.nullable or rf.nullable,
                    )
                    for lf, rf in zip(_left_schema.fields, _right_schema.fields)
                ]
            ),
        )


def map_intersect(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Return a new DataFrame containing rows in both DataFrames:

    1. If set_op.is_all is True, this method is implementing ```intersectAll```
        while preserving duplicates.

    2. If set_op.is_all is False, this method is implementing ```intersect```
        while removing duplicates.

    Examples
    --------
    >>> df1 = spark.createDataFrame([("a", 1), ("a", 1), ("a", 1), ("a", 2), ("b",  3), ("c", 4)], ["C1", "C2"]))
    >>> df2 = spark.createDataFrame([("a", 1), ("a", 1), ("b", 3)], ["C1", "C2"])
    >>> df1.intersect(df2).show()

    +---+---+
    | C1| C2|
    +---+---+
    |  a|  1|
    |  b|  3|
    +---+---+

    >>> df1.intersectAll(df2).show()

    +---+---+
    | C1| C2|
    +---+---+
    |  a|  1|
    |  a|  1|
    |  b|  3|
    +---+---+
    """
    # Intersect also drops qualified-access-only metadata (USING-join source columns) —
    # they are not part of either input's user-visible schema. SNOW-2443454.
    left_result = without_hidden_columns(map_relation(rel.set_op.left_input))
    right_result = without_hidden_columns(map_relation(rel.set_op.right_input))

    left_result, right_result = _coerce_set_op_types(
        left_result, right_result, "INTERSECT"
    )
    left_df = left_result.dataframe
    right_df = right_result.dataframe

    if rel.set_op.is_all:
        left_df_with_row_number = utils.get_df_with_partition_row_number(
            left_result, rel.set_op.left_input.common.plan_id, "left_row_number"
        )
        right_df_with_row_number = utils.get_df_with_partition_row_number(
            right_result, rel.set_op.right_input.common.plan_id, "right_row_number"
        )

        result: snowpark.DataFrame = left_df_with_row_number.intersect(
            right_df_with_row_number
        ).select(*left_result.column_map.get_snowpark_columns())
    else:
        result: snowpark.DataFrame = left_df.intersect(right_df)

    return DataFrameContainer(
        dataframe=result,
        column_map=left_result.column_map,
        table_name=left_result.table_name,
        cached_schema_getter=left_result.cached_schema_getter,
    )


def map_except(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Return a new DataFrame containing rows in the left DataFrame but not in the right DataFrame.

    1. If set_op.is_all is True, this method is implementing ```exceptAll```
        while preserving duplicates.

    2. If set_op.is_all is False, this method is implementing ```subtract```
        while removing duplicates.

    Examples
    --------
    >>> df1 = spark.createDataFrame([("a", 1), ("a", 1), ("a", 1), ("a", 2), ("b",  3), ("c", 4)], ["C1", "C2"]))
    >>> df2 = spark.createDataFrame([("a", 1), ("a", 1), ("b", 3)], ["C1", "C2"])
    >>> df1.subtract(df2).show()

    +---+---+
    | C1| C2|
    +---+---+
    |  a|  2|
    |  c|  4|
    +---+---+

    >>> df1.exceptAll(df2).show()

    +---+---+
    | C1| C2|
    +---+---+
    |  a|  1|
    |  a|  1|
    |  a|  2|
    |  c|  4|
    +---+---+
    """
    # Except also drops qualified-access-only metadata (USING-join source columns) —
    # they are not part of either input's user-visible schema. SNOW-2443454.
    left_result = without_hidden_columns(map_relation(rel.set_op.left_input))
    right_result = without_hidden_columns(map_relation(rel.set_op.right_input))

    left_result, right_result = _coerce_set_op_types(
        left_result, right_result, "EXCEPT"
    )
    left_df = left_result.dataframe
    right_df = right_result.dataframe

    if rel.set_op.is_all:
        # Snowflake except removes all duplicated rows. In order to handle the case,
        # we add a partition row number column to the df to make duplicated rows unique to
        # avoid the duplicated rows to be removed.
        # For example, with the following left_df and right_df
        # +---+---+                               +---+---+
        # | C1| C2|                               | C1| C2|
        # +---+---+                               +---+---+
        # |  a|  1|                               |  a|  1|
        # |  a|  1|                               |  a|  2|
        # |  a|  2|                               +---+---+
        # |  c|  4|
        # +---+---+
        # we will do
        # +---+---+------------+                    +---+---+------------+
        # | C1| C2| ROW_NUMBER |     EXCEPT         | C1| C2| ROW_NUMBER |
        # +---+---+------------+                    +---+---+------------+
        # |  a|  1|         0  |                    |  a|  1|         0  |
        # |  a|  1|         1  |                    |  a|  2|         0  |
        # |  a|  2|         0  |                    +---+---+------------+
        # |  c|  4|         0  |
        # +---+---+------------+
        # at the end we will do a select to exclude the row number column
        left_df_with_row_number = utils.get_df_with_partition_row_number(
            left_result, rel.set_op.left_input.common.plan_id, "left_row_number"
        )
        right_df_with_row_number = utils.get_df_with_partition_row_number(
            right_result, rel.set_op.right_input.common.plan_id, "right_row_number"
        )

        # Perform except use left_df_with_row_number and right_df_with_row_number,
        # and drop the row number column after except.
        result_df = left_df_with_row_number.except_(right_df_with_row_number).select(
            *left_result.column_map.get_snowpark_columns()
        )
    else:
        result_df = left_df.except_(right_df)

    # the result df keeps the column map of the original left_df
    # union operation does not preserve column qualifiers
    return DataFrameContainer(
        dataframe=result_df,
        column_map=left_result.column_map,
        table_name=left_result.table_name,
        cached_schema_getter=left_result.cached_schema_getter,
    )


def map_filter(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Filter a DataFrame based on a Relation's filter.

    The filter is a SQL expression that is applied to the DataFrame.
    Special-case plan shapes (distinct-over-project with missing references,
    subquery_alias inputs) are handled by resolution rules in map_relation
    before this fallback is reached.
    """
    input_container = map_relation(rel.filter.input)
    input_df = input_container.dataframe

    typer = ExpressionTyper(input_df)
    _, condition = map_single_column_expression(
        rel.filter.condition, input_container.column_map, typer
    )
    result = input_df.filter(condition.col)

    return DataFrameContainer(
        result,
        input_container.column_map,
        input_container.table_name,
        input_container.alias,
        cached_schema_getter=lambda: input_df.schema,
    )


def map_limit(
    rel: relation_proto.Relation,
) -> DataFrameContainer | pandas.DataFrame:
    """
    Limit a DataFrame based on a Relation's limit.

    The limit is an integer that is applied to the DataFrame.
    """

    input_container = without_internal_columns(map_relation(rel.limit.input))

    if isinstance(input_container, pandas.DataFrame):
        return input_container.head(rel.limit.limit)

    input_df = input_container.dataframe

    result: snowpark.DataFrame = input_df.limit(rel.limit.limit)

    return DataFrameContainer(
        result,
        column_map=input_container.column_map,
        table_name=input_container.table_name,
        alias=input_container.alias,
        cached_schema_getter=lambda: input_df.schema,
    )


def map_offset(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Offset a DataFrame based on a Relation's offset.

    The offset is an integer that is applied to the DataFrame.
    """
    input_container = without_internal_columns(map_relation(rel.offset.input))
    input_df = input_container.dataframe

    # TODO: This is a terrible way to have to do this, but Snowpark does not
    # support offset without limit.
    result: snowpark.DataFrame = input_df.limit(
        input_df.count(), offset=rel.offset.offset
    )

    return DataFrameContainer(
        result,
        column_map=input_container.column_map,
        table_name=input_container.table_name,
        alias=input_container.alias,
        cached_schema_getter=lambda: input_df.schema,
    )


def map_replace(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Replace values in the DataFrame.

    The `replace_map` is a dictionary of column names to a dictionary of
    values to replace. The values in the dictionary are the values to replace
    and the keys are the values to replace them with.
    """
    result = map_relation(rel.replace.input)
    input_df = result.dataframe
    ordered_columns = result.column_map.get_snowpark_columns(with_hidden=True)
    column_map = result.column_map
    table_name = result.table_name
    # note that seems like spark connect always send number values as double in rel.replace.replacements.
    to_replace = [
        get_literal_field_and_name(i.old_value)[0] for i in rel.replace.replacements
    ]
    values = [
        get_literal_field_and_name(i.new_value)[0] for i in rel.replace.replacements
    ]

    def _is_nan(value) -> bool:
        """Check if a value is NaN (Not a Number)."""
        return isinstance(value, float) and math.isnan(value)

    def _format_numeric_new_value(nv, col_datatype) -> str | None:
        """Format the new value for numeric columns. Returns None if should skip."""
        if nv is None:
            return "NULL"
        is_integer_column = isinstance(col_datatype, _IntegralType)
        if _is_nan(nv):
            # NaN is only representable for non-integer numeric types. For integer
            # columns, Spark casts NaN to 0.
            if is_integer_column:
                return "0"
            return "'NaN'::DOUBLE"
        if is_integer_column:
            try:
                nv_numeric = int(float(nv))
                return str(nv_numeric)
            except (TypeError, ValueError, OverflowError):
                return None
        else:
            return str(float(nv))

    # Snowpark doesn't support replacing floats with integers. We used column expressions instead of Snowpark function to achieve spark's compatibility.
    def replace_case_expr(col_name: str, old_vals: list, new_vals: list):
        """
        Generate a SQL CASE expression to replace values in a DataFrame column,
        matching PySpark's DataFrame.replace() behavior exactly.

        - Numeric columns:
            - Non-numeric replacement values are skipped.
            - Integer columns (IntegerType, LongType, ShortType, ByteType):
                - Replacement values are truncated to integers (e.g., 82.9 → 82).
            - Float/Double/Decimal columns:
                - Replacement values retain their original numeric precision.
            - Numeric comparisons are done using TO_DOUBLE() to allow matching
              integer and float equivalents (e.g., 80 matches 80.0).
            - NaN values are compared using IS_DOUBLE_NAN() function.
            - NULL values are compared using IS NULL.
        - Boolean columns:
            - Only boolean replacements are allowed; non-boolean replacements are skipped.
            - Boolean values are represented as TRUE/FALSE in SQL.
        - String columns:
            - Replacement values are enclosed in single quotes.
            - NULL values are represented as SQL NULL.
        - NULL values:
            - Represented explicitly as SQL NULL without quotes.
            - Compared using IS NULL, not = NULL.
        """
        col_datatype = next(
            field.datatype
            for field in result.dataframe.schema.fields
            if field.name == col_name
        )
        numeric_flag = isinstance(
            col_datatype,
            (
                IntegerType,
                LongType,
                FloatType,
                DoubleType,
                DecimalType,
                ShortType,
                ByteType,
            ),
        )
        bool_flag = isinstance(col_datatype, BooleanType)
        is_float_column = isinstance(col_datatype, (FloatType, DoubleType))

        case_expr = "CASE"
        for ov, nv in zip(old_vals, new_vals):
            if numeric_flag:
                if isinstance(ov, bool) or isinstance(ov, str):
                    # skip boolean/string replacements on numeric columns
                    continue

                # Skip NaN in old value for non-float columns (NaN only valid for float/double)
                if _is_nan(ov) and not is_float_column:
                    continue

                nv_expr = _format_numeric_new_value(nv, col_datatype)
                if nv_expr is None:
                    continue

                # Handle NULL in old value
                if ov is None:
                    case_expr += f" WHEN {col_name} IS NULL THEN {nv_expr}"
                # Handle NaN in old value (only for float/double columns)
                # In Snowflake, we detect NaN by casting to VARCHAR and comparing to 'NaN'
                elif _is_nan(ov):
                    case_expr += f" WHEN {col_name} IS NOT NULL AND {col_name}::VARCHAR = 'NaN' THEN {nv_expr}"
                else:
                    case_expr += (
                        f" WHEN TO_DOUBLE({col_name}) = {float(ov)} THEN {nv_expr}"
                    )

            elif bool_flag:
                if not isinstance(ov, bool):
                    continue
                nv_expr = str(nv).upper() if nv is not None else "NULL"
                case_expr += f" WHEN {col_name} IS NOT NULL AND {col_name} = {str(ov).upper()} THEN {nv_expr}"

            else:
                # If the column is a string type but either ov or nv is numeric, skip replacement.
                if isinstance(ov, (int, float, complex)) or isinstance(
                    nv, (int, float, complex)
                ):
                    continue
                nv_expr = f"'{nv}'" if nv is not None else "NULL"
                # Handle NULL in old value for string columns
                if ov is None:
                    case_expr += f" WHEN {col_name} IS NULL THEN {nv_expr}"
                else:
                    ov_expr = f"'{ov}'"
                    case_expr += f" WHEN {col_name} = {ov_expr} THEN {nv_expr}"
        if case_expr == "CASE":
            return col(col_name)
        else:
            case_expr += f" ELSE {col_name} END"
            return snowpark_expr(case_expr)

    if len(rel.replace.cols) > 0:
        columns: list[str] = [
            column_map.get_snowpark_column_name_from_spark_column_name(c)
            for c in rel.replace.cols
        ]
    else:
        columns: list[str] = [
            c.snowpark_name
            for c in result.column_map.columns
            if c.is_visible and c.snowpark_name != METADATA_FILENAME_COLUMN
        ]
    input_df = input_df.with_columns(
        columns, [replace_case_expr(c, to_replace, values) for c in columns]
    )

    result_df = input_df.select(*[col(c) for c in ordered_columns])
    original_schema = result.dataframe.schema

    return DataFrameContainer(
        result_df,
        column_map=column_map,
        table_name=table_name,
        cached_schema_getter=lambda: original_schema,
    )


def map_sample(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Sample a DataFrame based on a Relation's sample.
    """
    input_container = without_internal_columns(map_relation(rel.sample.input))
    input_df = input_container.dataframe

    frac = rel.sample.upper_bound - rel.sample.lower_bound
    if frac < 0 or frac > 1:
        exception = IllegalArgumentException("Sample fraction must be between 0 and 1")
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception
    # The seed argument is not supported here. There are a number of reasons that implementing
    # this will be complicated in Snowflake. Here is a list of complications:
    #
    # 1. Spark Connect always provides a seed, even if the user has not provided one. This seed
    #    is a randomly generated number, so we cannot detect if the user has provided a seed or not.
    # 2. Snowflake only supports seed on tables, not on views.
    # 3. Snowpark almost always creates a new view in the form of nested queries for every query.
    #
    # Given these three issues, users would be required to write their own temporary tables prior
    # to sampling, which is not a good user experience and has significant performance implications.
    # For these reasons, we choose to ignore the seed argument until we have a plan for how to solve
    # these issues.
    if rel.sample.with_replacement:
        # TODO: Use a random number generator with ROW_NUMBER and SELECT.
        exception = SnowparkConnectNotImplementedError(
            "Sample with replacement is not supported"
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception
    else:
        result: snowpark.DataFrame = input_df.sample(frac=frac)
        return DataFrameContainer(
            result,
            column_map=input_container.column_map,
            table_name=input_container.table_name,
            alias=input_container.alias,
            cached_schema_getter=lambda: input_df.schema,
        )


def map_tail(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Tail a DataFrame based on a Relation's tail.

    The tail is an integer that is applied to the DataFrame.
    """
    input_container = without_internal_columns(map_relation(rel.tail.input))
    input_df = input_container.dataframe

    num_rows = input_df.count()
    result: snowpark.DataFrame = input_df.limit(
        num_rows, offset=max(0, num_rows - rel.tail.limit)
    )

    return DataFrameContainer(
        result,
        column_map=input_container.column_map,
        table_name=input_container.table_name,
        alias=input_container.alias,
        cached_schema_getter=lambda: input_df.schema,
    )


def _union_by_name_optimized(
    left_df: snowpark.DataFrame,
    right_df: snowpark.DataFrame,
    allow_missing_columns: bool = False,
) -> snowpark.DataFrame:
    """
    This implementation is an optimized version of Snowpark's Dataframe::_union_by_name_internal.
    The only change is, that it avoids redundant schema queries that occur in the standard Snowpark,
    by reusing already-fetched/calculated schemas.
    """

    left_schema = left_df.schema
    right_schema = right_df.schema

    left_cols = {field.name for field in left_schema.fields}
    right_cols = {field.name for field in right_schema.fields}
    right_field_map = {field.name: field for field in right_schema.fields}

    missing_left = right_cols - left_cols
    missing_right = left_cols - right_cols

    def add_nulls(
        missing_cols: set[str], to_df: snowpark.DataFrame, from_df: snowpark.DataFrame
    ) -> snowpark.DataFrame:
        dt_map = {field.name: field.datatype for field in from_df.schema.fields}
        result = to_df.select(
            "*",
            *[lit(None).cast(dt_map[col]).alias(col) for col in missing_cols],
        )

        result_fields = []
        for field in to_df.schema.fields:
            result_fields.append(
                StructField(field.name, field.datatype, field.nullable)
            )
        for col_name in missing_cols:
            from_field = next(
                field for field in from_df.schema.fields if field.name == col_name
            )
            result_fields.append(
                StructField(col_name, from_field.datatype, from_field.nullable)
            )

        set_schema_getter(result, lambda: StructType(result_fields))

        return result

    if missing_left or missing_right:
        if allow_missing_columns:
            left = left_df
            right = right_df
            if missing_left:
                left = add_nulls(missing_left, left, right)
            if missing_right:
                right = add_nulls(missing_right, right, left)
            result = left._union_by_name_internal(right, is_all=True)

            result_fields = []
            for field in left_schema.fields:
                result_fields.append(
                    StructField(field.name, field.datatype, field.nullable)
                )
            for col_name in missing_left:
                right_field = right_field_map[col_name]
                result_fields.append(
                    StructField(col_name, right_field.datatype, right_field.nullable)
                )

            set_schema_getter(result, lambda: StructType(result_fields))
            return result
        else:
            parts = []
            for column in missing_left:
                parts.append(f"`{column}` is in the right hand side, but not the left")
            for column in missing_right:
                parts.append(f"`{column}` is in the left hand side, but not the right")
            exception = AnalysisException(
                f"Cannot union the DataFrames by column names. {'. '.join(parts)}."
            )
            attach_custom_error_code(exception, ErrorCodes.COLUMN_NOT_FOUND)
            raise exception

    result = left_df.unionAllByName(
        right_df, allow_missing_columns=allow_missing_columns
    )
    set_schema_getter(result, lambda: left_df.schema)
    return result
