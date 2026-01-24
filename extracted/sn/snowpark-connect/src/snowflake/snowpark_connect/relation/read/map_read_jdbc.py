#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import jaydebeapi
import jpype
import pyspark.sql.connect.proto.relations_pb2 as relation_proto

from snowflake import snowpark
from snowflake.snowpark._internal.analyzer.analyzer_utils import unquote_if_quoted
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.relation.read.jdbc_read_dbapi import JdbcDataFrameReader
from snowflake.snowpark_connect.relation.read.utils import (
    Connection,
    rename_columns_as_snowflake_standard,
)
from snowflake.snowpark_connect.type_support import emulate_integral_types
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger


def create_connection(jdbc_options: dict[str, str]) -> Connection:
    url = jdbc_options.get("url", None)
    driver = jdbc_options.get("driver", None)
    if driver is None:
        driver = (
            jpype.java.sql.DriverManager.getDriver(url).getClass().getCanonicalName()
        )
    try:
        return jaydebeapi.connect(driver, url, jdbc_options)
    except Exception as e:
        jpype.detachThreadFromJVM()
        exception = Exception(f"Error connecting JDBC datasource: {e}")
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception


def close_connection(conn: Connection) -> None:
    if conn is not None:
        conn.close()
    # JVM main thread and SAS Server main thread creates deadlock.
    # jaydebeapi has connect method which calls jpype internally.
    # jpype start JVM if it's not started.
    # Then jpype attach the current thread to the JVM.
    # But jaydebeapi doesn't have any method to detach or shutdown the JVM.
    jpype.detachThreadFromJVM()


def map_read_jdbc(
    rel: relation_proto.Relation,
    session: snowpark.Session,
    options: dict[str, str],
) -> DataFrameContainer:
    """
    Read a table data or query data from a JDBC external datasource into a Snowpark DataFrame.
    """

    jdbc_options = options.copy()
    dbtable = options.get("dbtable", None)
    query = options.get("query", None)
    partition_column = options.get("partitionColumn", None)
    lower_bound = options.get("lowerBound", None)
    upper_bound = options.get("upperBound", None)
    num_partitions = options.get("numPartitions", None)
    predicates = rel.read.data_source.predicates

    logger.info(
        f"dbtable={dbtable},query={query},partition_column={partition_column},lower_bound={lower_bound},upper_bound={upper_bound},num_partitions={num_partitions}"
    )
    if num_partitions is not None:
        num_partitions = int(num_partitions)

    if dbtable is not None and len(dbtable) == 0:
        dbtable = None

    # Neo4j labels/relationship options are resolved to query later in jdbc_read_dbapi
    has_neo4j_options = "labels" in options or "relationship" in options
    if not dbtable and not query and not has_neo4j_options:
        exception = ValueError("Include dbtable or query is required option")
        attach_custom_error_code(exception, ErrorCodes.INSUFFICIENT_INPUT)
        raise exception

    if query is not None and dbtable is not None:
        exception = ValueError(
            "Not allowed to specify dbtable and query options at the same time"
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception

    if query is not None and partition_column is not None:
        exception = ValueError(
            "Not allowed to specify partitionColumn and query options at the same time"
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception

    try:
        df = JdbcDataFrameReader(session, jdbc_options).jdbc_read_dbapi(
            create_connection,
            close_connection,
            table=dbtable,
            query=query,
            column=partition_column,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            num_partitions=num_partitions,
            predicates=predicates,
        )
        true_names = list(map(lambda x: unquote_if_quoted(x), df.columns))
        renamed_df, snowpark_cols = rename_columns_as_snowflake_standard(
            df, rel.common.plan_id
        )
        return DataFrameContainer.create_with_column_mapping(
            dataframe=renamed_df,
            spark_column_names=true_names,
            snowpark_column_names=snowpark_cols,
            snowpark_column_types=[
                emulate_integral_types(f.datatype) for f in df.schema.fields
            ],
        )
    except Exception as e:
        exception = Exception(f"Error accessing JDBC datasource for read: {e}")
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception
