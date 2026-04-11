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
from snowflake.snowpark._internal.error_message import SnowparkClientExceptionMessages
from snowflake.snowpark.functions import col, expr as snowpark_expr, lit, to_binary
from snowflake.snowpark.types import (
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
    without_internal_columns,
)
from snowflake.snowpark_connect.utils.identifiers import (
    split_fully_qualified_spark_name,
)
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
)


def cast_columns(
    df_container: DataFrameContainer,
    df_dtypes: list[snowpark.types.DataType],
    target_dtypes: list[snowpark.types.DataType],
    column_map: ColumnNameMap,
):
    df: snowpark.DataFrame = df_container.dataframe
    if df_dtypes == target_dtypes:
        return df_container
    # Use cached schema if available to avoid triggering extra queries
    if (
        hasattr(df_container, "cached_schema_getter")
        and df_container.cached_schema_getter is not None
    ):
        df_schema = df_container.cached_schema_getter()
    else:
        df_schema = df.schema  # Get current schema
    new_columns = []

    for i, field in enumerate(df_schema.fields):
        col_name = field.name
        current_type = field.datatype
        target_type = target_dtypes[i]
        new_columns.append(
            _cast_column_if_needed(df, col_name, current_type, target_type)
        )

    new_df = df.select(new_columns)
    return DataFrameContainer.create_with_column_mapping(
        dataframe=new_df,
        spark_column_names=column_map.get_spark_columns(),
        snowpark_column_names=column_map.get_snowpark_columns(),
        snowpark_column_types=target_dtypes,
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


def _cast_df_columns_by_name(
    df: snowpark.DataFrame,
    type_map: dict[str, snowpark.types.DataType],
) -> snowpark.DataFrame:
    """
    Cast DataFrame columns based on a name-to-type mapping.

    Returns new_df with updated types and set_schema_getter called to PatchedDataFrame.
    """
    if not type_map:
        return df

    new_fields: list[StructField] = []
    select_cols = []
    for field in df.schema.fields:
        target_type = type_map.get(field.name)
        current_type = field.datatype
        if target_type is not None:
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
    left_dtypes = [field.datatype for field in get_schema_from_result(left_df).fields]
    right_dtypes = [field.datatype for field in get_schema_from_result(right_df).fields]

    if left_dtypes != right_dtypes:
        if len(left_dtypes) != len(right_dtypes):
            exception = AnalysisException(
                f"{operation_name}: the number of columns must match"
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
            raise exception
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

        left_df = cast_columns(
            left_df,
            left_dtypes,
            target_dtypes,
            left_df.column_map,
        )
        right_df = cast_columns(
            right_df,
            right_dtypes,
            target_dtypes,
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

    if (
        rel.deduplicate.HasField("all_columns_as_keys")
        and rel.deduplicate.all_columns_as_keys
    ):
        result: snowpark.DataFrame = input_df.drop_duplicates()
    else:
        result: snowpark.DataFrame = input_df.drop_duplicates(
            *input_container.column_map.get_snowpark_column_names_from_spark_column_names(
                list(rel.deduplicate.column_names)
            )
        )

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
    elif any([c.is_hidden for c in input_container.column_map.columns]):
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

        # We don't validate the fully qualified spark name here as fillNa is no-op for structured type columns.
        # It only works for scalar type columns like float, int, string or bool.
        # Also, if a column doesn't exist, fillna silently ignores it (Spark behavior).
        columns: list[str] = []
        valid_indices: list[int] = []
        for i, c in enumerate(spark_col_names):
            try:
                col_name = input_container.column_map.get_snowpark_column_name_from_spark_column_name(
                    split_fully_qualified_spark_name(c)[0]
                )
                columns.append(col_name)
                valid_indices.append(i)
            except Exception:
                # Column doesn't exist, skip it (Spark behavior is to silently ignore)
                pass

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

        has_hidden_columns = any(
            c.is_hidden for c in input_container.column_map.columns
        )
        visible_columns = [
            c.snowpark_name
            for c in input_container.column_map.columns
            if not c.is_hidden and c.snowpark_name != METADATA_FILENAME_COLUMN
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
    left_result = without_internal_columns(map_relation(rel.set_op.left_input))
    right_result = without_internal_columns(map_relation(rel.set_op.right_input))
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
        right_renamed_fields = []
        for field in original_right_schema.fields:
            spark_name = (
                right_column_map.get_spark_column_name_from_snowpark_column_name(
                    field.name
                )
            )
            columns_to_restore[spark_name.upper()] = (spark_name, field.name)
            right_renamed_fields.append(
                StructField(spark_name, field.datatype, field.nullable)
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

        original_left_schema = left_df.schema
        left_renamed_fields = []
        for field in original_left_schema.fields:
            spark_name = (
                left_column_map.get_spark_column_name_from_snowpark_column_name(
                    field.name
                )
            )
            columns_to_restore[spark_name.upper()] = (spark_name, field.name)
            left_renamed_fields.append(
                StructField(spark_name, field.datatype, field.nullable)
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
                )

        left_df = _cast_df_columns_by_name(left_df, common_type_map)
        right_df = _cast_df_columns_by_name(right_df, common_type_map)
        result = _union_by_name_optimized(left_df, right_df, allow_missing_columns)

        spark_columns = []
        snowpark_columns = []

        snowpark_column_types = [f.datatype for f in result.schema.fields]
        select_exprs = []
        for col_ in result.columns:
            spark_col_to_restore, snowpark_col_to_restore = columns_to_restore[
                col_.upper()
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
        return DataFrameContainer(
            result,
            column_map=left_result.column_map,
            cached_schema_getter=lambda: left_df.schema,
        )
    else:
        result = left_df.union(right_df)
        # union operation does not preserve column qualifiers
        return DataFrameContainer(
            result,
            column_map=left_result.column_map,
            cached_schema_getter=lambda: left_df.schema,
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
    left_result = without_internal_columns(map_relation(rel.set_op.left_input))
    right_result = without_internal_columns(map_relation(rel.set_op.right_input))

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
        cached_schema_getter=lambda: left_df.schema,
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
    left_result = without_internal_columns(map_relation(rel.set_op.left_input))
    right_result = without_internal_columns(map_relation(rel.set_op.right_input))

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
        cached_schema_getter=lambda: left_df.schema,
    )


def map_filter(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Filter a DataFrame based on a Relation's filter.

    The filter is a SQL expression that is applied to the DataFrame.
    """
    input_container = map_relation(rel.filter.input)
    input_df = input_container.dataframe

    typer = ExpressionTyper(input_df)
    _, condition = map_single_column_expression(
        rel.filter.condition, input_container.column_map, typer
    )

    if rel.filter.input.WhichOneof("rel_type") == "subquery_alias":
        # map_subquery_alias does not actually wrap the DataFrame in an alias or subquery.
        # Apparently, there are cases (e.g., TpcdsQ53) where this is required, without it, we get
        # SQL compilation error.
        # To mitigate it, we are doing .select("*"), .alias() introduces additional describe queries
        result = input_df.select("*").filter(condition.col)
    else:
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
            if not c.is_hidden and c.snowpark_name != METADATA_FILENAME_COLUMN
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
            exception = (
                SnowparkClientExceptionMessages.DF_CANNOT_RESOLVE_COLUMN_NAME_AMONG(
                    missing_left, missing_right
                )
            )
            attach_custom_error_code(exception, ErrorCodes.COLUMN_NOT_FOUND)
            raise exception

    result = left_df.unionAllByName(
        right_df, allow_missing_columns=allow_missing_columns
    )
    set_schema_getter(result, lambda: left_df.schema)
    return result
