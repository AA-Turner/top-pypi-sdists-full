#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import pyspark.sql.connect.proto.relations_pb2 as relation_proto
from pyspark.errors.exceptions.base import AnalysisException

from snowflake import snowpark
from snowflake.snowpark._internal.analyzer.analyzer_utils import (
    quote_name_without_upper_casing,
    unquote_if_quoted,
)
from snowflake.snowpark.exceptions import SnowparkSQLException
from snowflake.snowpark.types import StructField, StructType
from snowflake.snowpark_connect.column_name_handler import (
    ColumnNameMap,
    make_column_names_snowpark_compatible,
)
from snowflake.snowpark_connect.column_qualifier import ColumnQualifier
from snowflake.snowpark_connect.config import auto_uppercase_non_column_identifiers
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.relation.read.utils import (
    rename_columns_as_snowflake_standard,
)
from snowflake.snowpark_connect.type_support import emulate_integral_types
from snowflake.snowpark_connect.utils.context import get_processed_views
from snowflake.snowpark_connect.utils.identifiers import (
    split_fully_qualified_spark_name,
)
from snowflake.snowpark_connect.utils.session import _get_current_snowpark_session
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
)
from snowflake.snowpark_connect.utils.temporary_view_helper import get_temp_view


def post_process_df(
    df: snowpark.DataFrame, plan_id: int, source_table_name: str = None
) -> DataFrameContainer:
    try:
        true_names = list(map(lambda x: unquote_if_quoted(x), df.columns))
        renamed_df, snowpark_column_names = rename_columns_as_snowflake_standard(
            df, plan_id
        )
        name_parts = split_fully_qualified_spark_name(source_table_name)

        # If table name is not fully qualified (only has table name, no database),
        # add current schema name to qualifiers so columns can be referenced with database prefix
        # Note: In Spark, "database" corresponds to Snowflake "schema"
        if source_table_name and len(name_parts) == 1:
            session = _get_current_snowpark_session()
            current_schema = session.get_current_schema()
            if current_schema:
                name_parts = [unquote_if_quoted(current_schema)] + name_parts

        return DataFrameContainer.create_with_column_mapping(
            dataframe=renamed_df,
            spark_column_names=true_names,
            snowpark_column_names=snowpark_column_names,
            snowpark_column_types=[
                emulate_integral_types(f.datatype) for f in df.schema.fields
            ],
            column_qualifiers=[{ColumnQualifier(tuple(name_parts))} for _ in true_names]
            if source_table_name
            else None,
        )
    except SnowparkSQLException as e:
        # Check if this is a table/view not found error
        # Snowflake error codes: 002003 (42S02) - Object does not exist or not authorized
        if hasattr(e, "sql_error_code") and e.sql_error_code == 2003:
            exception = AnalysisException(
                f"[TABLE_OR_VIEW_NOT_FOUND] The table or view cannot be found. {source_table_name}"
            )
            attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
            raise exception from None  # Suppress original exception to reduce message size
        # Re-raise if it's not a table not found error
        raise


def _get_temporary_view(
    temp_view: DataFrameContainer, table_name: str, plan_id: int
) -> DataFrameContainer:
    if temp_view.has_zero_columns():
        return DataFrameContainer.create_with_column_mapping(
            dataframe=temp_view.dataframe.select("__DUMMY"),
            spark_column_names=["__DUMMY"],
            snowpark_column_names=["__DUMMY"],
            column_is_hidden=[True],
        )

    fields_names = [field.name for field in temp_view.dataframe.schema.fields]
    fields_types = [field.datatype for field in temp_view.dataframe.schema.fields]

    snowpark_column_names = make_column_names_snowpark_compatible(
        temp_view.column_map.get_spark_columns(), plan_id
    )
    # Rename columns in dataframe to prevent conflicting names during joins
    renamed_df = temp_view.dataframe.select(
        *(
            temp_view.dataframe.col(orig).alias(alias)
            for orig, alias in zip(fields_names, snowpark_column_names)
        )
    )
    # do not flatten initial rename when reading table
    # TODO: remove once SNOW-2203826 is done
    if renamed_df._select_statement is not None:
        renamed_df._select_statement.flatten_disabled = True

    new_column_map = ColumnNameMap(
        spark_column_names=temp_view.column_map.get_spark_columns(),
        snowpark_column_names=snowpark_column_names,
        column_metadata=temp_view.column_map.column_metadata,
        column_qualifiers=[
            {ColumnQualifier(tuple(split_fully_qualified_spark_name(table_name)))}
            for _ in range(len(temp_view.column_map.get_spark_columns()))
        ],
        parent_column_name_map=temp_view.column_map.get_parent_column_name_map(),
    )

    schema = StructType(
        [
            StructField(name, type, _is_column=False)
            for name, type in zip(snowpark_column_names, fields_types)
        ]
    )
    return DataFrameContainer(
        dataframe=renamed_df,
        column_map=new_column_map,
        table_name=temp_view.table_name,
        alias=temp_view.alias,
        partition_hint=temp_view.partition_hint,
        cached_schema_getter=lambda: schema,
    )


def get_table_from_name(
    table_name: str, session: snowpark.Session, plan_id: int
) -> DataFrameContainer:
    """Get table from name returning a container."""

    # Verify if recursive view read is not attempted
    if table_name in get_processed_views():
        exception = AnalysisException(
            f"[RECURSIVE_VIEW] Recursive view `{table_name}` detected (cycle: `{table_name}` -> `{table_name}`)"
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
        raise exception

    snowpark_name = ".".join(
        quote_name_without_upper_casing(part)
        for part in split_fully_qualified_spark_name(table_name)
    )

    temp_view = get_temp_view(snowpark_name)
    if temp_view:
        return _get_temporary_view(temp_view, table_name, plan_id)

    if auto_uppercase_non_column_identifiers():
        snowpark_name = snowpark_name.upper()

    df = session.read.table(snowpark_name)
    return post_process_df(df, plan_id, table_name)


def get_table_from_query(
    query: str, session: snowpark.Session, plan_id: int
) -> snowpark.DataFrame:
    df = session.sql(query)
    return post_process_df(df, plan_id)


def map_read_table(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Read a table into a Snowpark DataFrame.
    """
    session: snowpark.Session = _get_current_snowpark_session()
    if rel.read.HasField("named_table"):
        table_identifier = rel.read.named_table.unparsed_identifier
    elif (
        rel.read.data_source.HasField("format")
        and rel.read.data_source.format.lower() == "iceberg"
    ):
        if len(rel.read.data_source.paths) != 1:
            exception = SnowparkConnectNotImplementedError(
                f"Unexpected paths: {rel.read.data_source.paths}"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
        table_identifier = rel.read.data_source.paths[0]
    else:
        exception = ValueError("The relation must have a table identifier.")
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception
    return get_table_from_name(table_identifier, session, rel.common.plan_id)
