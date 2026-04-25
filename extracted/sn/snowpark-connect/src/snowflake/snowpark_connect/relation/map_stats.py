#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import ast
import decimal

import pandas
import pyspark.sql.connect.proto.relations_pb2 as relation_proto
from pyspark.errors.exceptions.base import AnalysisException, IllegalArgumentException
from pyspark.sql.types import StructField

import snowflake.snowpark.functions as fn
import snowflake.snowpark.types as snowpark_types
from snowflake import snowpark
from snowflake.snowpark.exceptions import SnowparkSQLException
from snowflake.snowpark.types import _FractionalType, _IntegralType
from snowflake.snowpark_connect.config import get_boolean_session_config_param
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.relation.map_relation import map_relation
from snowflake.snowpark_connect.utils.session import get_or_create_snowpark_session


def map_corr(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Find the correlation of two columns in the input DataFrame.

    Returns a pandas DataFrame because the correlation of two columns produces
    a scalar value.
    """
    input_container = map_relation(rel.corr.input)
    input_df = input_container.dataframe

    col1 = input_container.column_map.get_snowpark_column_name_from_spark_column_name(
        rel.corr.col1
    )
    col2 = input_container.column_map.get_snowpark_column_name_from_spark_column_name(
        rel.corr.col2
    )
    # TODO: Handle method, Snowpark does not support this yet.
    # if rel.corr.HasField("method"):
    #     method = rel.corr.method
    # else:
    #     method = "pearson"
    result: float = input_df.corr(col1, col2)
    return pandas.DataFrame({"corr": [result]})


def map_cov(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Find the covariance of two columns in the input DataFrame.

    Returns a pandas DataFrame because the covariance of two columns produces
    a scalar value.
    """
    input_container = map_relation(rel.cov.input)
    input_df = input_container.dataframe

    col1 = input_container.column_map.get_snowpark_column_name_from_spark_column_name(
        rel.cov.col1
    )
    col2 = input_container.column_map.get_snowpark_column_name_from_spark_column_name(
        rel.cov.col2
    )

    col1_type = next(
        field.datatype for field in input_df.schema.fields if field.name == col1
    )
    col2_type = next(
        field.datatype for field in input_df.schema.fields if field.name == col2
    )
    _check_numeric_column(col_name=rel.cov.col1, col_type=col1_type)
    _check_numeric_column(col_name=rel.cov.col2, col_type=col2_type)

    result: float = input_df.cov(col1, col2)
    return pandas.DataFrame({"cov": [result]})


def map_approx_quantile(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Find one or more approximate quantiles in the input DataFrame.

    Returns a pandas DataFrame because the approximate quantile produces a
    list of scalar values.
    """
    input_container = map_relation(rel.approx_quantile.input)
    input_df = input_container.dataframe

    snowflake_compatible = get_boolean_session_config_param(
        "snowpark.connect.enable_snowflake_extension_behavior"
    )

    if not snowflake_compatible:
        # When Snowflake extension behavior is disabled, validate that all requested columns exist
        requested_spark_cols = list(rel.approx_quantile.cols)
        available_spark_cols = input_container.column_map.get_spark_columns()

        for col_name in requested_spark_cols:
            if col_name not in available_spark_cols:
                # Find suggestions for the unresolved column
                suggestions = [c for c in available_spark_cols if c != col_name]
                suggestion_text = (
                    f" Did you mean one of the following? [`{'`, `'.join(suggestions)}`]."
                    if suggestions
                    else ""
                )

                exception = AnalysisException(
                    f"[UNRESOLVED_COLUMN.WITH_SUGGESTION] A column or function parameter with name `{col_name}` cannot be resolved.{suggestion_text}"
                )
                attach_custom_error_code(exception, ErrorCodes.COLUMN_NOT_FOUND)
                raise exception

    cols = input_container.column_map.get_snowpark_column_names_from_spark_column_names(
        list(rel.approx_quantile.cols)
    )
    quantile = list(rel.approx_quantile.probabilities)
    # TODO: Handle relative_error, Snowpark does not support this yet.
    result: list[float] = input_df.approxQuantile(cols, quantile)
    # Wrap result in list here to pack the result into a single cell
    return pandas.DataFrame({"approx_quantile": [result]})


def _format_describe_value(
    value: object,
    stat_name: str,
    original_col_type: snowpark_types.DataType | None,
) -> str | None:
    """Format a describe/summary statistic value to match Spark's Cast(Type, StringType).

    Spark always returns StringType columns from describe/summary. The string formatting
    depends on the statistic type and the original column type:
    - count: always formatted as integer (Long -> "5")
    - mean/stddev: always formatted as float (Double -> "3.0", preserves .0)
    - min/max: formatted according to original column type
      (Int -> "1", Double -> "45000.0", String -> "Alice")
    """
    if value is None:
        return None

    if isinstance(value, (int, float, decimal.Decimal)):
        numeric = float(value)
        if stat_name == "count":
            return str(int(numeric))
        elif stat_name in ("min", "max") and isinstance(
            original_col_type, _IntegralType
        ):
            return str(int(numeric))
        elif stat_name in ("mean", "stddev") or stat_name.endswith("%"):
            return str(numeric)
        elif isinstance(original_col_type, _FractionalType):
            return str(numeric)
        elif isinstance(value, (int, decimal.Decimal)) and not isinstance(
            original_col_type, _FractionalType
        ):
            return str(int(numeric))
        else:
            return str(numeric)

    if isinstance(value, str):
        if stat_name in ("mean", "stddev") or stat_name.endswith("%"):
            try:
                return str(float(value))
            except (ValueError, TypeError):
                return value
        if stat_name in ("min", "max") and isinstance(
            original_col_type, _FractionalType
        ):
            try:
                return str(float(value))
            except (ValueError, TypeError):
                return value

    return str(value)


def _format_stats_rows(
    rows: list,
    col_names: list[str],
    original_types: dict[str, snowpark_types.DataType],
) -> dict[str, list[str | None]]:
    """Format collected describe/summary rows into string values keyed by stat name."""
    col_index = {name: i for i, name in enumerate(col_names)}
    result: dict[str, list[str | None]] = {}
    for row in rows:
        stat_name = row[0]
        string_row: list[str | None] = [stat_name]
        for col_name in col_names[1:]:
            value = row[col_index[col_name]]
            string_row.append(
                _format_describe_value(value, stat_name, original_types.get(col_name))
            )
        result[stat_name] = string_row
    return result


def map_describe(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Computes basic statistics for numeric columns, which includes count, mean, stddev, min, and max.
    If no columns are provided, this function computes statistics for all numerical or string columns.
    Non-numeric and non-string columns will be ignored.

    Returns a new DataFrame that provides basic statistics for the given DataFrame
    """
    input_container = map_relation(rel.describe.input)
    input_df = input_container.dataframe

    session = get_or_create_snowpark_session()
    spark_cols = (
        list(rel.describe.cols)
        if rel.describe.cols
        else input_container.column_map.get_spark_columns()
    )
    cols = [
        input_container.column_map.get_snowpark_column_name_from_spark_column_name(
            column
        )
        for column in spark_cols
    ]

    statistics = ["count", "mean", "stddev", "min", "max"]
    # TODO: there's a bug in Snowpark where strings can either all cast to numbers and then
    # stddev and mean will be computed correctly, try_cast will need to be used in snowpark when
    # strings_include_math_stats=True, this is the workaround for now
    try:
        desc_df = input_df.describe(cols, strings_include_math_stats=True)
        df_rows = desc_df.collect()
    except SnowparkSQLException as e:
        if "Numeric value" not in str(e) or "is not recognized" not in str(e):
            raise
        desc_df = input_df.describe(cols, strings_include_math_stats=False)
        df_rows = desc_df.collect()

    ordered_rows = []
    for stat in statistics:
        for row in df_rows:
            if stat == row.SUMMARY:
                ordered_rows.append(row)

    desc_columns = desc_df.columns
    original_types = {
        field.name: field.datatype
        for field in input_df.schema.fields
        if field.name in desc_columns
    }

    formatted = _format_stats_rows(ordered_rows, desc_columns, original_types)
    string_data = [formatted[stat] for stat in statistics if stat in formatted]

    schema = snowpark_types.StructType(
        [
            snowpark_types.StructField(name, snowpark_types.StringType())
            for name in desc_columns
        ]
    )
    ordered_desc_df = session.create_dataframe(string_data, schema)
    return _build_column_map_helper_container(ordered_desc_df, input_container)


# TODO: track missing Snowpark feature
def map_summary(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Computes specified statistics for numeric or string columns. Available statistics are: count, mean, stddev, min,
    max, arbitrary approximate percentiles specified as a percentage (e.g., 75%), count_distinct, and
    approx_count_distinct. If no statistics are given, this function computes count, mean, stddev, min, approximate
    quartiles (percentiles at 25%, 50%, and 75%), and max.

    Returns a new DataFrame that provides specified statistics for the given DataFrame.
    """
    session = get_or_create_snowpark_session()
    result = map_relation(rel.summary.input)
    input_container: DataFrameContainer = result
    input_df = input_container.dataframe

    numeric_and_string_spark_cols = [
        column
        for field, column in zip(
            input_df.schema.fields, input_container.column_map.get_spark_columns()
        )
        if isinstance(
            field.datatype, (snowpark_types._NumericType, snowpark_types.StringType)
        )
    ]

    # this is intentional to trigger ambigous column name is two columns of same name are provided
    numeric_and_string_snowpark_cols = [
        input_container.column_map.get_snowpark_column_name_from_spark_column_name(
            column
        )
        for column in numeric_and_string_spark_cols
    ]

    # Select only those columns
    input_df = input_df.select(*numeric_and_string_snowpark_cols)

    original_types = {field.name: field.datatype for field in input_df.schema.fields}

    # Collect raw describe stats and format in Python to preserve precision
    desc_df: snowpark.DataFrame = input_df.describe([])
    desc_col_names = desc_df.columns
    desc_rows = desc_df.collect()

    formatted_stats = _format_stats_rows(desc_rows, desc_col_names, original_types)

    if rel.summary.statistics:
        statistics = list(rel.summary.statistics)
    else:
        # default statistics
        statistics = ["count", "mean", "stddev", "min", "25%", "50%", "75%", "max"]

    quantiles = []
    percentages = []

    for stat in statistics:
        if stat[-1] == "%":
            quantiles.append(int(stat[:-1]) / 100)
            percentages.append(stat)
        elif stat == "count_distinct":
            count_distinct_values = [
                fn.count_distinct(column) for column in input_df.columns
            ]
            count_distinct_rows = input_df.select(*count_distinct_values).collect()
            formatted_stats["count_distinct"] = ["count_distinct"] + [
                str(value)
                for row in count_distinct_rows
                for value in row.as_dict().values()
            ]
        elif stat == "approx_count_distinct":
            approx_count_distinct_list_values = [
                fn.approx_count_distinct(column) for column in input_df.columns
            ]
            approx_count_distinct_df_rows = input_df.select(
                *approx_count_distinct_list_values
            ).collect()
            values = [
                str(value)
                for row in approx_count_distinct_df_rows
                for value in row.as_dict().values()
            ]
            values.insert(0, "approx_count_distinct")
            formatted_stats["approx_count_distinct"] = values

    if len(quantiles) > 0:
        eligible_columns = []
        for i, col in enumerate(input_df.columns):
            if not isinstance(
                input_df.schema.fields[i].datatype, snowpark_types.StringType
            ):
                eligible_columns.append(col)
        approx_quantile_values = input_df.approx_quantile(
            eligible_columns, percentile=quantiles
        )

        numeric_index = iter(approx_quantile_values)
        per_col_quantiles = []
        for col in input_df.columns:
            col_type = original_types.get(col)
            if col in eligible_columns:
                col_values = next(numeric_index)
                if isinstance(col_type, _IntegralType):
                    per_col_quantiles.append(
                        [str(int(v)) if v is not None else None for v in col_values]
                    )
                else:
                    per_col_quantiles.append(
                        [str(v) if v is not None else None for v in col_values]
                    )
            else:
                per_col_quantiles.append([None] * len(quantiles))

        for j, percentage in enumerate(percentages):
            row = [percentage]
            for col_quantiles in per_col_quantiles:
                row.append(col_quantiles[j])
            formatted_stats[percentage] = row

    # Build result in the requested order; stats from describe() (count, mean, stddev,
    # min, max) are always present, others (percentiles, count_distinct,
    # approx_count_distinct) are populated above only when requested.
    string_data = []
    for stat in statistics:
        if stat in formatted_stats:
            string_data.append(formatted_stats[stat])
        elif stat not in ("count", "mean", "stddev", "min", "max"):
            continue
        else:
            raise ValueError(f"Expected statistic '{stat}' was not computed")

    schema = snowpark_types.StructType(
        [
            snowpark_types.StructField(name, snowpark_types.StringType())
            for name in desc_col_names
        ]
    )
    ordered_summary_df = session.create_dataframe(string_data, schema)

    spark_col_names = ["summary"]
    spark_col_names.extend(numeric_and_string_spark_cols)

    return DataFrameContainer.create_with_column_mapping(
        dataframe=ordered_summary_df,
        spark_column_names=spark_col_names,
        snowpark_column_names=ordered_summary_df.columns,
    )


def map_freq_items(rel: relation_proto.Relation) -> DataFrameContainer:
    """
    Returns an approximation of the most frequent values in the input, along with their approximate frequencies.
    """
    input_container = map_relation(rel.freq_items.input)
    input_df = input_container.dataframe

    session = get_or_create_snowpark_session()
    support = rel.freq_items.support
    spark_col_names = []
    cols = input_container.column_map.get_snowpark_column_names_from_spark_column_names(
        list(rel.freq_items.cols)
    )

    # handle empty DataFrame case
    row_count = input_df.count()

    for sp_col_name in cols:
        spark_col_names.append(
            f"{input_container.column_map.get_spark_column_name_from_snowpark_column_name(sp_col_name)}_freqItems"
        )

    if row_count == 0:
        # If DataFrame is empty, return empty arrays for each column
        empty_values = [[] for _ in cols]
        approx_top_k_df = session.createDataFrame([empty_values], spark_col_names)
        return DataFrameContainer.create_with_column_mapping(
            dataframe=approx_top_k_df,
            spark_column_names=spark_col_names,
            snowpark_column_names=spark_col_names,
        )

    approx_top_k_df = input_df.select(
        *[
            fn.function("approx_top_k")(fn.col(col), round(row_count / support))
            for col in cols
        ]
    )
    approx_top_k_df_rows = approx_top_k_df.collect()
    approx_top_k_values = [
        ast.literal_eval(value)
        for row in approx_top_k_df_rows
        for value in row.as_dict().values()
    ]
    filtered_values = [
        [
            entry[0]
            for entry in value
            if entry[1] >= support * sum(count for _, count in value)
        ]
        for value in approx_top_k_values
    ]

    approx_top_k_df = session.createDataFrame([filtered_values], spark_col_names)

    return DataFrameContainer.create_with_column_mapping(
        dataframe=approx_top_k_df,
        spark_column_names=spark_col_names,
        snowpark_column_names=spark_col_names,
    )


def _build_column_map_helper_container(
    desc_df: snowpark.DataFrame,
    input_container: DataFrameContainer,
) -> DataFrameContainer:
    """Container version of _build_column_map_helper."""
    spark_col_names = ["summary"]
    for i, sp_col_name in enumerate(desc_df.columns):
        if i != 0:
            spark_col_names.append(
                input_container.column_map.get_spark_column_name_from_snowpark_column_name(
                    sp_col_name
                )
            )

    return DataFrameContainer.create_with_column_mapping(
        dataframe=desc_df,
        spark_column_names=spark_col_names,
        snowpark_column_names=desc_df.columns,
    )


def _check_numeric_column(col_name: str, col_type: StructField) -> None:
    """Checks if a column type is a Snowpark NumericType and raises an exception if not."""
    if not isinstance(col_type, snowpark_types._NumericType):
        raise IllegalArgumentException(
            f"Column '{col_name}' must be of numeric type for covariance calculation, "
            f"but got {col_type}"
        )
