#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from typing import Callable

from pyspark import Row

import snowflake.snowpark
from snowflake import snowpark
from snowflake.snowpark import DataFrameWriter
from snowflake.snowpark.dataframe import DataFrame
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.relation.read import jdbc_read_dbapi
from snowflake.snowpark_connect.relation.read.jdbc_read_dbapi import JdbcDialect
from snowflake.snowpark_connect.relation.read.utils import Connection
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger

DEFAULT_INSERT_BATCH_SIZE = 100


class JdbcDataFrameWriter(DataFrameWriter):
    """
    Derived Snowflake DataFrameReader class, so we can reuse methods.
    This class read data from a JDBC datasource and creates Snowpark Dataframe.
    """

    def __init__(
        self,
        session: "snowflake.snowpark.session.Session",
        jdbc_options: dict[str, str],
    ) -> None:
        super().__init__(session)
        self.session = session
        self.jdbc_options = jdbc_options
        jdbc_read_dbapi.register_all_supported_jdbc_dialect()

    def jdbc_write_dbapi(
        self,
        container: DataFrameContainer,
        create_connection: Callable[[dict[str, str]], "Connection"],
        close_connection: Callable[[Connection], None],
        table: str,
        write_mode: str,
    ) -> None:
        """
        Write a Snowpark Dataframe data into table of a JDBC datasource.
        """

        input_df = container.dataframe
        conn = create_connection(self.jdbc_options)
        try:
            url = self.jdbc_options.get("url", None)
            jdbc_dialect = jdbc_read_dbapi.get_jdbc_dialect(url)

            table_exist = self._does_table_exist(conn, table, jdbc_dialect)
            insert_query = self._generate_insert_query(
                container,
                table,
                jdbc_dialect,
            )

            match write_mode:
                case "append":
                    if not table_exist:
                        self._create_table(conn, table, container, jdbc_dialect)
                case "errorifexists":
                    if table_exist:
                        exception = ValueError(
                            "table is already exist and write mode is ERROR_IF_EXISTS"
                        )
                        attach_custom_error_code(
                            exception, ErrorCodes.INVALID_OPERATION
                        )
                        raise exception
                    else:
                        self._create_table(conn, table, container, jdbc_dialect)
                case "overwrite":
                    if table_exist:
                        self._drop_table(conn, table, jdbc_dialect)
                    self._create_table(conn, table, container, jdbc_dialect)
                case "ignore":
                    if table_exist:
                        # With Ignore write mode, if table already exists, the save operation is expected
                        # to not save the contents of the DataFrame and to not change the existing data.
                        return
                    else:
                        self._create_table(conn, table, container, jdbc_dialect)
                case _:
                    exception = ValueError(f"Invalid write mode value{write_mode}")
                    attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                    raise exception

            task_insert_into_data_source_with_retry(
                input_df,
                create_connection,
                self.jdbc_options,
                close_connection,
                insert_query,
            )
        finally:
            close_connection(conn)

    def _generate_insert_query(
        self, container: DataFrameContainer, table: str, jdbc_dialect: JdbcDialect
    ) -> str:
        """
        Generates INSERT statement with placeholders using dialect.
        :param container: Snowpark dataframe container
        :param table: JDBC datasource table name (or node label for Neo4j)
        :param jdbc_dialect: JDBC dialect for generating the query
        :return: INSERT SQL/Cypher statement
        """
        true_names = container.column_map.get_spark_columns()
        placeholders = ["?"] * len(true_names)
        return jdbc_dialect.get_insert_statement(table, true_names, placeholders)

    def _does_table_exist(
        self, conn: Connection, table: str, jdbc_dialect: JdbcDialect
    ) -> bool:
        """
        Check if a table/node label exists using dialect.
        :param conn: A Python DBAPI connection over JDBC connection
        :param table: JDBC datasource table name (or node label for Neo4j)
        :param jdbc_dialect: JDBC dialect for generating the query
        :return: True if table exists otherwise False
        """
        sql = jdbc_dialect.get_table_exists_query(table)
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
            table_exist = True
        except Exception:
            table_exist = False

        return table_exist

    def _drop_table(
        self, conn: Connection, table: str, jdbc_dialect: JdbcDialect
    ) -> None:
        """
        Drop a JDBC datasource table or delete Neo4j nodes.

        :param conn: A Python DBAPI connection over JDBC connection
        :param table: JDBC datasource table name (or node label for Neo4j)
        :param jdbc_dialect: JDBC dialect for generating the query
        :return: None
        """
        sql = jdbc_dialect.get_drop_table_statement(table)
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
        except Exception as e:
            logger.error(f"failed to drop table {table} from the data source {e}")
            attach_custom_error_code(e, ErrorCodes.INTERNAL_ERROR)
            raise e

    def _create_table(
        self,
        conn: Connection,
        table: str,
        container,
        jdbc_dialect: JdbcDialect,
    ) -> None:
        """
        Create a table in the JDBC Datasource or prepare for node creation in Neo4j.
        Pyspark by default adds double quotes to the column names to make it case sensitive.
        We will mimic the same behavior here.

        :param conn: A Python DBAPI connection over JDBC connection
        :param table: JDBC datasource table name (or node label for Neo4j)
        :param container: Snowpark dataframe container
        :param jdbc_dialect: JDBC specific dialect
        :return: None
        """
        input_df = container.dataframe
        fields = input_df.schema.fields
        column_map = container.column_map

        # Build list of (column_name, sql_type) tuples
        columns_with_types = []
        for field in fields:
            name = column_map.get_spark_column_name_from_snowpark_column_name(
                field.name
            )
            type_name = convert_sp_to_sql_type(field.datatype, jdbc_dialect)
            if not field.nullable:
                type_name += " NOT NULL"
            columns_with_types.append((name, type_name))

        sql = jdbc_dialect.get_create_table_statement(table, columns_with_types)

        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
        except Exception as e:
            logger.error(f"failed to create a table {table} from the data source {e}")
            attach_custom_error_code(e, ErrorCodes.INTERNAL_ERROR)
            raise e


def _task_insert_into_data_source(
    conn: Connection,
    insert_query: str,
    batch_rows: list[Row] = None,
    total_columns: int = 0,
) -> None:
    """

    :param conn: A Python DBAPI connection over JDBC connection
    :param insert_query: INSERT SQL statement
    :param batch_rows: List of rows
    :param total_columns: Total columns in the Dataframe
    :return: None
    """
    cursor = conn.cursor()
    auto_commit = conn.jconn.getAutoCommit()
    try:
        if auto_commit:
            conn.jconn.setAutoCommit(False)
        for row in batch_rows:
            parameter_values = [row[i] for i in range(0, total_columns)]
            cursor.execute(insert_query, parameter_values)
        conn.commit()
    except Exception as e:
        logger.debug(f"failed to insert into data source  {e}")
        conn.rollback()
        attach_custom_error_code(e, ErrorCodes.INTERNAL_ERROR)
        raise e
    finally:
        cursor.close()
        if auto_commit:
            conn.jconn.setAutoCommit(auto_commit)


def task_insert_into_data_source_with_retry(
    input_df: DataFrame,
    create_connection: Callable[[dict[str, str]], "Connection"],
    jdbc_options: dict[str, str],
    close_connection: Callable[[Connection], None],
    insert_query: str,
) -> None:
    """
    INSERT into JDBC datasource table.

    :param input_df:  Snowpark dataframe to save
    :param create_connection: JDBC create connection callaback
    :param jdbc_options: JDBC driver options
    :param close_connection: JDBC close connetcion callback
    :param insert_query: INSERT SQL
    :return:
    """
    conn = create_connection(jdbc_options)
    try:
        total_columns = len(input_df.columns)
        rows = input_df.to_local_iterator(case_sensitive=False)
        batch_size = DEFAULT_INSERT_BATCH_SIZE

        batch_rows = []
        batch_row_index = 0
        for row in rows:
            if batch_row_index + 1 == batch_size:
                _task_insert_into_data_source(
                    conn,
                    insert_query,
                    batch_rows,
                    total_columns,
                )
                batch_rows = []
                batch_row_index = 0
            else:
                batch_rows.append(row)
                batch_row_index += 1

        if batch_row_index > 0:
            # Last batch
            _task_insert_into_data_source(
                conn,
                insert_query,
                batch_rows,
                total_columns,
            )
    except Exception as e:
        logger.debug(f"failed to insert into data source  {e}")
        attach_custom_error_code(e, ErrorCodes.INTERNAL_ERROR)
        raise e
    finally:
        close_connection(conn)


def convert_sp_to_sql_type(
    datatype: snowpark.types.DataType,
    jdbc_dialect: JdbcDialect,
) -> str:
    """
    Convert Snowpark data type to a external datasource data type
    :param datatype: Snowpark datatype
    :param jdbc_dialect: JDBC specific dialect
    :return: String name of the SQL type.
    """

    # Snowflake and SQLServer have different max sizes of the varchar
    max_varchar_size = jdbc_dialect.get_max_varchar_length()

    match type(datatype):
        case snowpark.types.BinaryType:
            return "BINARY"
        case snowpark.types.BooleanType:
            return "BOOLEAN"
        case snowpark.types.ByteType:
            return "BYTEINT"
        case snowpark.types.DateType:
            return "DATE"
        case snowpark.types.DecimalType:
            return f"NUMBER({datatype.precision}, {datatype.scale})"
        case snowpark.types.DoubleType:
            return jdbc_dialect.get_double_type_name()
        case snowpark.types.FloatType:
            return "FLOAT"
        case snowpark.types.IntegerType:
            return "INT"
        case snowpark.types.LongType:
            return "INT"
        case snowpark.types.NullType:
            return "VARCHAR"
        case snowpark.types.ShortType:
            return "SMALLINT"
        # We regard NullType as String, which is required when creating
        # a dataframe from local data with all None values
        case snowpark.types.StringType:
            if datatype.length:
                if datatype.length > max_varchar_size:
                    size = max_varchar_size
                else:
                    size = datatype.length
                return f"VARCHAR({size})"
            return "VARCHAR"
        case snowpark.types.TimeType:
            return "TIME"
        case snowpark.types.TimestampType:
            match datatype.tz:
                case snowpark.types.TimestampTimeZone.NTZ:
                    return "TIMESTAMP_NTZ"
                case snowpark.types.TimestampTimeZone.LTZ:
                    return "TIMESTAMP_LTZ"
                case snowpark.types.TimestampTimeZone.TZ:
                    return "TIMESTAMP_TZ"
                case _:
                    return "TIMESTAMP"
        case _:
            exception = TypeError(
                f"Unsupported data type: {datatype.__class__.__name__}"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_TYPE)
            raise exception
