#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import typing
from abc import ABC, abstractmethod

import pandas
import pyspark.sql.connect.proto.common_pb2 as common_proto
import pyspark.sql.connect.proto.types_pb2 as types_proto

from snowflake.snowpark._internal.analyzer.analyzer_utils import unquote_if_quoted
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.error.exceptions import MissingDatabase, MissingSchema
from snowflake.snowpark_connect.utils.identifiers import (
    split_fully_qualified_spark_name,
)
from snowflake.snowpark_connect.utils.session import get_or_create_snowpark_session
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
)

Identifier = str | None


class AbstractSparkCatalog(ABC):
    def __init__(self, name: str, description: str | None) -> None:
        self.cache: set[tuple[str, str, str]] = set()
        self.name = name
        self.description = description

    @abstractmethod
    def createTable(
        self,
        tableName: str,
        path: str,
        source: str,
        schema: types_proto.DataType,
        description: str,
        **options: typing.Any,
    ) -> DataFrameContainer:
        exception = SnowparkConnectNotImplementedError("createTable is not implemented")
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    @abstractmethod
    def listDatabases(
        self,
        pattern: str | None = None,
    ) -> pandas.DataFrame:
        exception = SnowparkConnectNotImplementedError(
            "listDatabases is not implemented"
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    @abstractmethod
    def getDatabase(
        self,
        spark_dbName: str,
    ) -> pandas.DataFrame:
        exception = SnowparkConnectNotImplementedError("getDatabase is not implemented")
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    @abstractmethod
    def databaseExists(
        self,
        spark_dbName: str,
    ) -> pandas.DataFrame:
        exception = SnowparkConnectNotImplementedError(
            "databaseExists is not implemented"
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    @abstractmethod
    def listTables(
        self,
        spark_dbName: str | None = None,
        pattern: str | None = None,
    ) -> pandas.DataFrame:
        exception = SnowparkConnectNotImplementedError("listTables is not implemented")
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    @abstractmethod
    def getTable(
        self,
        spark_tableName: str,
    ) -> pandas.DataFrame:
        exception = SnowparkConnectNotImplementedError("getTable is not implemented")
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    @abstractmethod
    def tableExists(
        self,
        spark_tableName: str,
        spark_dbName: str | None,
    ) -> pandas.DataFrame:
        exception = SnowparkConnectNotImplementedError("tableExists is not implemented")
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    @abstractmethod
    def listColumns(
        self,
        spark_tableName: str,
        spark_dbName: str | None = None,
    ) -> pandas.DataFrame:
        exception = SnowparkConnectNotImplementedError("listColumns is not implemented")
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    @abstractmethod
    def currentDatabase(self) -> pandas.DataFrame:
        exception = SnowparkConnectNotImplementedError(
            "currentDatabase is not implemented"
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    @abstractmethod
    def setCurrentDatabase(
        self,
        spark_dbName: str,
    ) -> pandas.DataFrame:
        exception = SnowparkConnectNotImplementedError(
            "setCurrentDatabase is not implemented"
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    @abstractmethod
    def dropGlobalTempView(
        self,
        spark_view_name: str,
    ) -> DataFrameContainer:
        exception = SnowparkConnectNotImplementedError(
            "dropGlobalTempView is not implemented"
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    @abstractmethod
    def dropTempView(
        self,
        spark_view_name: str,
    ) -> DataFrameContainer:
        exception = SnowparkConnectNotImplementedError(
            "dropTempView is not implemented"
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    def cacheTable(
        self,
        spark_tableName: str,
        storageLevel: common_proto.StorageLevel | None = None,
    ) -> pandas.DataFrame:
        """Add a table, or view to our local cache to answer isCached queries.

        This operation doesn't actually do anything on the Snowflake side since caching is impossible server-side.
        """
        catalog, sf_database, sf_schema, sf_table = _process_multi_layer_identifier(
            spark_tableName
        )
        if catalog is not None and self != catalog:
            exception = SnowparkConnectNotImplementedError(
                "Calling into another catalog is not currently supported"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
        if sf_database is None:
            sf_database = _get_current_snowflake_database()
        if sf_schema is None:
            sf_schema = _get_current_snowflake_schema()
        self.cache.add(
            (
                sf_database,
                sf_schema,
                sf_table,
            )
        )
        return pandas.DataFrame()

    def clearCache(self) -> pandas.pandas.DataFrame:
        """Remove all tables and views from our local cache to answer isCached queries.

        This operation doesn't actually do anything on the Snowflake side since caching is impossible server-side.
        """
        self.cache = set()
        return pandas.DataFrame()

    def isCached(self, spark_tableName: str) -> pandas.DataFrame:
        """Whether we have cached a table, or view locally.

        This operation doesn't actually do anything on the Snowflake side since caching is impossible server-side.
        """
        catalog, sf_database, sf_schema, sf_table = _process_multi_layer_identifier(
            spark_tableName
        )
        if catalog is not None and self != catalog:
            exception = SnowparkConnectNotImplementedError(
                "Calling into another catalog is not currently supported"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
        if sf_database is None:
            sf_database = _get_current_snowflake_database()
        if sf_schema is None:
            sf_schema = _get_current_snowflake_schema()
        return pandas.DataFrame(
            {"cached": [(sf_database, sf_schema, sf_table) in self.cache]}
        )

    def refreshByPath(self, path: str) -> pandas.DataFrame:
        return pandas.DataFrame()

    def refreshTable(self, spark_tableName: str) -> pandas.DataFrame:
        return pandas.DataFrame()

    def uncacheTable(self, spark_tableName: str) -> pandas.DataFrame:
        """Remove a table, or view from our local cache to answer isCached queries.

        This operation doesn't actually do anything on the Snowflake side since caching is impossible server-side.
        """
        catalog, sf_database, sf_schema, sf_table = _process_multi_layer_identifier(
            spark_tableName
        )
        if catalog is not None and self != catalog:
            exception = SnowparkConnectNotImplementedError(
                "Calling into another catalog is not currently supported"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
        if sf_database is None:
            sf_database = _get_current_snowflake_database()
        if sf_schema is None:
            sf_schema = _get_current_snowflake_schema()
        self.cache.remove(
            (
                sf_database,
                sf_schema,
                sf_table,
            )
        )
        return pandas.DataFrame()


def _get_current_snowflake_database() -> str:
    """Return the current Snowflake database and throw a central exception if it cannot be determined."""
    session = get_or_create_snowpark_session()
    current_database = session.catalog.get_current_database()
    if current_database is None:
        raise MissingDatabase()
    return unquote_if_quoted(current_database)


def _get_current_snowflake_schema() -> str:
    """Return the current Snowflake schema and throw a central exception if it cannot be determined."""
    session = get_or_create_snowpark_session()
    current_schema = session.catalog.get_current_schema()
    if current_schema is None:
        raise MissingSchema()
    return unquote_if_quoted(current_schema)


def _process_multi_layer_database(
    spark_mli: str | None,
) -> typing.Tuple[AbstractSparkCatalog | None, Identifier, Identifier]:
    """This function transforms Spark database identifiers into their Snowflake parts.

    Possible formats are:
    - database_name
    - catalog_name.database_name
    """
    from . import CATALOGS

    match split_fully_qualified_spark_name(spark_mli):
        case [d]:
            return None, None, d
        case [c, d]:
            if c in CATALOGS:
                return CATALOGS[c], None, d
            else:
                return None, c, d
        case _:
            exception = ValueError(
                f"Unexpected database identifier format: {spark_mli}"
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
            raise exception


def _process_multi_layer_identifier(
    spark_mli: str | None,
) -> typing.Tuple[AbstractSparkCatalog | None, Identifier, Identifier, Identifier]:
    """This function transforms Spark table/view identifiers into their Snowflake parts.

    We map Spark databases to Snowflake schemas and Spark cataglogs might be interpreted as
    Snowflake database names if they are unknown catalogs.

    Possible formats are:
    - table_name
    - database_name.table_name
    - catalog_name.database_name.table_name
    """
    from . import CATALOGS

    snowflake_obj: Identifier = None
    snowflake_database: Identifier = None
    snowflake_schema: Identifier = None
    spark_catalog: AbstractSparkCatalog | None = None
    match split_fully_qualified_spark_name(spark_mli):
        case [o]:
            snowflake_obj = o
        case [s, o]:
            snowflake_schema, snowflake_obj = s, o
        case [d, s, t]:
            if d in CATALOGS:
                snowflake_schema, snowflake_obj = s, t
                spark_catalog = CATALOGS[d]
            else:
                snowflake_database, snowflake_schema, snowflake_obj = d, s, t
        case _:
            exception = ValueError(
                f"Unexpected table/view identifier format: {spark_mli}"
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
            raise exception
    return spark_catalog, snowflake_database, snowflake_schema, snowflake_obj
