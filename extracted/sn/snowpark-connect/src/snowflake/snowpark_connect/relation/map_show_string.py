#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import copy

import pandas
import pyspark.sql.connect.proto.relations_pb2 as relation_proto

from snowflake import snowpark
from snowflake.snowpark._internal.analyzer import analyzer_utils
from snowflake.snowpark.functions import col
from snowflake.snowpark.types import DateType, StringType, StructField, StructType
from snowflake.snowpark_connect.column_name_handler import set_schema_getter
from snowflake.snowpark_connect.config import global_config
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.relation.map_relation import map_relation
from snowflake.snowpark_connect.relation.read.metadata_utils import (
    without_internal_columns,
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
        # special case for 0-column dataframes
        num_rows = min(rel.show_string.num_rows, input_df_container.dataframe.count())
        show_string = _generate_empty_show_string(num_rows, rel.show_string.vertical)
        return pandas.DataFrame({"show_string": [show_string]})

    filtered_container = without_internal_columns(input_df_container)
    display_df = filtered_container.dataframe
    display_spark_columns = filtered_container.column_map.get_spark_columns()

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

    filtered_container = without_internal_columns(input_df_container)
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


def _handle_datetype_columns(input_df: snowpark.DataFrame) -> snowpark.DataFrame:
    """
    Maps DateType columns to strings it aims to allow showing the dates which are out of range of datetime.datetime.
    """
    new_column_mapping = []
    new_fields = []
    transformation_required = False
    for field in input_df.schema:
        if isinstance(field.datatype, DateType):
            transformation_required = True
            new_column_mapping.append(col(field.name).cast(StringType()))
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
