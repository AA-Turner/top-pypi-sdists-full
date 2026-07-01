#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import zlib

from pyspark.sql import DataFrame, SparkSession

SQL_PASS_THROUGH_MARKER = "PRIVATE-SNOWFLAKE-SQL"


def calculate_checksum(data: str) -> str:
    checksum = zlib.crc32(data.encode("utf-8"))
    return format(checksum, "08X")


class SnowflakeSession:
    """
    Provides a wrapper around SparkSession to enable Snowflake SQL pass-through functionality.
    Also provides helper methods to switch to different database, schema, role, warehouse, etc.
    """

    def __init__(self, spark_session: SparkSession) -> None:
        self.spark_session = spark_session

    def sql(self, sql_stmt: str) -> DataFrame:
        """
        Execute Snowflake specific SQL directly against Snowflake.
        """
        checksum = calculate_checksum(sql_stmt)
        return self.spark_session.sql(
            f"{SQL_PASS_THROUGH_MARKER} {checksum} {sql_stmt}"
        )

    def use_database(self, database: str, preserve_case: bool = False) -> DataFrame:
        """
        Switch to the database specified by `database`.
        """
        if preserve_case:
            database = f'"{database}"'
        return self.sql(f"USE DATABASE {database}")

    def use_schema(self, schema: str, preserve_case: bool = False) -> DataFrame:
        """
        Switch to the schema specified by `schema`.
        """
        if preserve_case:
            schema = f'"{schema}"'
        return self.sql(f"USE SCHEMA {schema}")

    def use_role(self, role: str, preserve_case: bool = False) -> DataFrame:
        """
        Switch to the role specified by `role`.
        """
        if preserve_case:
            role = f'"{role}"'
        return self.sql(f"USE ROLE {role}")

    def use_warehouse(self, warehouse: str, preserve_case: bool = False) -> DataFrame:
        """
        Switch to the warehouse specified by `warehouse`.
        """
        if preserve_case:
            warehouse = f'"{warehouse}"'
        return self.sql(f"USE WAREHOUSE {warehouse}")
