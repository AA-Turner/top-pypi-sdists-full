#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import copy

import pandas
import pyspark.sql.connect.proto.relations_pb2 as relation_proto

from snowflake import snowpark
from snowflake.snowpark import functions as snowpark_fn
from snowflake.snowpark._internal.analyzer import analyzer_utils
from snowflake.snowpark.functions import col
from snowflake.snowpark.types import (
    DateType,
    StringType,
    StructField,
    StructType,
    YearMonthIntervalType,
)
from snowflake.snowpark_connect.column_name_handler import set_schema_getter
from snowflake.snowpark_connect.config import global_config
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.relation.map_relation import map_relation
from snowflake.snowpark_connect.relation.read.metadata_utils import (
    without_hidden_columns,
)


def map_show_string(rel: relation_proto.Relation) -> pandas.DataFrame:
    """
    Generate the string representation of the input dataframe.

    We return a pandas DataFrame object here because the `show_string` relation
    message creates a string. The client expects this string to be packed into an Arrow
    Buffer object as a single cell.
    """
    input_df_container: DataFrameContainer = map_relation(rel.show_string.input)

    if input_df_container.has_zero_columns():
        # SNOW-3242008: Use known_row_count when available to avoid a Snowflake query.
        row_count = (
            input_df_container.known_row_count
            if input_df_container.known_row_count is not None
            else input_df_container.dataframe.count()
        )
        num_rows = min(rel.show_string.num_rows, row_count)
        show_string = _generate_empty_show_string(num_rows, rel.show_string.vertical)
        return pandas.DataFrame({"show_string": [show_string]})

    filtered_container = without_hidden_columns(input_df_container)
    display_spark_columns = filtered_container.column_map.get_spark_columns()

    # SNOW-3242008: For cached DDL results (e.g., "Statement executed successfully.")
    # generate the show string directly from the Arrow table instead of executing
    # a VALUES query against Snowflake.
    cached_table = input_df_container.cached_local_relation_arrow_table
    if cached_table is not None:
        show_string = _format_cached_ddl_result(
            cached_table, display_spark_columns, rel.show_string
        )
        return pandas.DataFrame({"show_string": [show_string]})

    display_df = filtered_container.dataframe
    input_df = _handle_datetype_columns(display_df)
    show_string = input_df._show_string_spark(
        num_rows=rel.show_string.num_rows,
        truncate=rel.show_string.truncate,
        vertical=rel.show_string.vertical,
        _spark_column_names=display_spark_columns,
        _spark_session_tz=global_config.spark_sql_session_timeZone,
    )
    return pandas.DataFrame({"show_string": [show_string]})


def map_repr_html(rel: relation_proto.Relation) -> pandas.DataFrame:
    """
    Generate the html string representation of the input dataframe.
    """
    input_df_container: DataFrameContainer = map_relation(rel.html_string.input)

    filtered_container = without_hidden_columns(input_df_container)
    input_df = filtered_container.dataframe
    input_panda = input_df.toPandas()
    input_panda.rename(
        columns={
            analyzer_utils.unquote_if_quoted(
                filtered_container.column_map.get_snowpark_columns()[i]
            ): filtered_container.column_map.get_spark_columns()[i]
            for i in range(len(input_panda.columns))
        },
        inplace=True,
    )
    html_string = input_panda.to_html(
        index=False,
        max_rows=rel.html_string.num_rows,
    )
    return pandas.DataFrame({"html_string": [html_string]})


def _year_month_interval_to_spark_display(
    column: snowpark.Column, datatype: YearMonthIntervalType
) -> snowpark.Column:
    """Build a Snowflake SQL expression that renders a YearMonthIntervalType
    column as the Spark display string (e.g. ``INTERVAL '4-0' YEAR TO MONTH``).

    Computing the components ourselves bypasses the connector / Snowpark display
    formatter, which changed its representation of ``INTERVAL YEAR`` /
    ``INTERVAL MONTH`` in snowflake-connector-python 4.3+ and breaks
    ``YearMonthIntervalType`` formatting downstream.
    """
    # DATE_PART returns signed components on negative intervals, so the simple
    # multiply-and-add yields the correct signed total months (verified against
    # Snowflake: e.g. INTERVAL '-1-6' YEAR TO MONTH -> year=-1, month=-6).
    total_months = snowpark_fn.call_function(
        "date_part", snowpark_fn.sql_expr("year"), column
    ) * 12 + snowpark_fn.call_function(
        "date_part", snowpark_fn.sql_expr("month"), column
    )

    abs_months = snowpark_fn.abs(total_months)
    sign = snowpark_fn.iff(total_months < 0, snowpark_fn.lit("-"), snowpark_fn.lit(""))
    years_part = snowpark_fn.floor(abs_months / 12).cast(StringType())
    months_part = (abs_months % 12).cast(StringType())
    abs_months_str = abs_months.cast(StringType())

    start_field = getattr(datatype, "start_field", YearMonthIntervalType.YEAR)
    end_field = getattr(datatype, "end_field", YearMonthIntervalType.MONTH)

    if (
        start_field == YearMonthIntervalType.YEAR
        and end_field == YearMonthIntervalType.YEAR
    ):
        body = snowpark_fn.concat(sign, years_part)
        suffix = "' YEAR"
    elif (
        start_field == YearMonthIntervalType.MONTH
        and end_field == YearMonthIntervalType.MONTH
    ):
        body = snowpark_fn.concat(sign, abs_months_str)
        suffix = "' MONTH"
    else:
        body = snowpark_fn.concat(sign, years_part, snowpark_fn.lit("-"), months_part)
        suffix = "' YEAR TO MONTH"

    return snowpark_fn.concat(
        snowpark_fn.lit("INTERVAL '"), body, snowpark_fn.lit(suffix)
    )


def _handle_datetype_columns(input_df: snowpark.DataFrame) -> snowpark.DataFrame:
    """
    Maps DateType and YearMonthIntervalType columns to strings.

    For ``DateType`` this allows showing dates outside of
    ``datetime.datetime``'s range. For ``YearMonthIntervalType`` this builds
    the Spark display string in Snowflake so the show output is independent of
    ``snowflake-connector-python`` / Snowpark formatter changes (the connector
    4.3+ representation of bare ``INTERVAL YEAR`` / ``INTERVAL MONTH`` is
    misinterpreted by Snowpark's display formatter for ``YearMonthIntervalType``
    fields).
    """
    new_column_mapping = []
    new_fields = []
    transformation_required = False
    for field in input_df.schema:
        if isinstance(field.datatype, DateType):
            transformation_required = True
            new_column_mapping.append(col(field.name).cast(StringType()))
            new_fields.append(StructField(field.name, StringType()))
        elif isinstance(field.datatype, YearMonthIntervalType):
            transformation_required = True
            new_column_mapping.append(
                _year_month_interval_to_spark_display(
                    col(field.name), field.datatype
                ).alias(field.name)
            )
            new_fields.append(StructField(field.name, StringType()))
        else:
            new_column_mapping.append(col(field.name))
            new_fields.append(field)

    if not transformation_required:
        return input_df

    transformed_df = input_df.select(new_column_mapping)
    set_schema_getter(transformed_df, lambda: StructType(new_fields))
    transformed_df._column_map = copy.deepcopy(input_df._column_map)

    return transformed_df


def _format_cached_ddl_result(
    cached_table, spark_columns: list[str], show_params
) -> str:
    """SNOW-3242008: Format show string for a cached DDL result (1 row, 1 col, string).

    Replicates the formatting logic from Snowpark's _show_string_spark for this
    specific case to avoid an unnecessary Snowflake round trip.
    """
    col_name = spark_columns[0]
    raw = cached_table.column(0)[0].as_py()
    value = "NULL" if raw is None else str(raw)

    truncate = show_params.truncate
    if truncate > 0 and len(value) > truncate:
        value = value[: truncate - 3] + "..." if truncate >= 4 else value[:truncate]

    minimum_col_width = 3
    col_width = max(minimum_col_width, len(col_name), len(value))

    if not show_params.vertical:
        pad = str.rjust if truncate > 0 else str.ljust
        sep = f"+{'-' * col_width}+\n"
        return (
            f"{sep}|{pad(col_name, col_width)}|\n{sep}|{pad(value, col_width)}|\n{sep}"
        )
    else:
        field_width = max(minimum_col_width, len(col_name))
        data_width = max(minimum_col_width, len(value))
        row_header = "-RECORD 0".ljust(field_width + data_width + 5, "-")
        return f"{row_header}\n {col_name.ljust(field_width)} | {value.ljust(data_width)}\n"


def _generate_empty_show_string(
    num_rows: int,
    vertical: bool,
) -> str:
    if vertical:
        return (
            "\n".join([f"-RECORD {i}" for i in range(num_rows)]) + "\n"
            if num_rows > 0
            else ""
        )
    else:
        top_line = "++\n"
        header_line = "||\n"
        separator_line = "++\n"
        data_lines = "".join(["||\n" for _ in range(num_rows)])
        return f"{top_line}{header_line}{top_line}{data_lines}{separator_line}"
