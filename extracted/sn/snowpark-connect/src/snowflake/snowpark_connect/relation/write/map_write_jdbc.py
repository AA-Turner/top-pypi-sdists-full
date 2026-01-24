#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from snowflake import snowpark
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.relation.read.map_read_jdbc import (
    close_connection,
    create_connection,
)
from snowflake.snowpark_connect.relation.write.jdbc_write_dbapi import (
    JdbcDataFrameWriter,
)
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger


def map_write_jdbc(
    container: DataFrameContainer,
    session: snowpark.Session,
    options: dict[str, str],
    write_mode: str,
) -> None:
    """
    Write a Snowpark DataFrame into table into a JDBC external datasource.
    Default write mode is ErrorIfExists.
    Uses Dataframe schema.
    """

    jdbc_options = options.copy()
    dbtable = options.get("dbtable", None)

    logger.info(f"dbtable={dbtable}, write_mode={write_mode}")

    if dbtable is not None and len(dbtable) == 0:
        dbtable = None

    if dbtable is None:
        exception = ValueError("Include dbtable is required option")
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception

    try:
        JdbcDataFrameWriter(session, jdbc_options).jdbc_write_dbapi(
            container,
            create_connection,
            close_connection,
            table=dbtable,
            write_mode=write_mode,
        )
    except Exception as e:
        exception = Exception(f"Error accessing JDBC datasource for write: {e}")
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception
