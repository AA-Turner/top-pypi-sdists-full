#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import re

import pandas
import pyspark.sql.connect.proto.catalog_pb2 as catalog_proto

from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.relation.catalogs import CATALOGS
from snowflake.snowpark_connect.relation.catalogs.utils import (
    CURRENT_CATALOG_NAME,
    get_current_catalog,
    set_current_catalog,
)
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
)


def map_catalog(
    rel: catalog_proto.Catalog,
) -> DataFrameContainer | pandas.DataFrame:
    match rel.WhichOneof("cat_type"):
        # Database related APIs
        case "current_database":
            return get_current_catalog().currentDatabase()
        case "database_exists":
            return get_current_catalog().databaseExists(
                rel.database_exists.db_name,
            )
        case "get_database":
            return get_current_catalog().getDatabase(
                rel.get_database.db_name,
            )
        case "list_databases":
            return get_current_catalog().listDatabases(
                (
                    rel.list_databases.pattern
                    if rel.list_databases.HasField("pattern")
                    else None
                ),
            )
        case "set_current_database":
            return get_current_catalog().setCurrentDatabase(
                rel.set_current_database.db_name,
            )
        # Table related APIs
        case "get_table":
            return get_current_catalog().getTable(rel.get_table.table_name)
        case "list_tables":
            return get_current_catalog().listTables(
                (
                    rel.list_tables.db_name
                    if rel.list_tables.HasField("db_name")
                    else None
                ),
                (
                    rel.list_tables.pattern
                    if rel.list_tables.HasField("pattern")
                    else None
                ),
            )
        case "list_catalogs":
            if (
                rel.list_catalogs.HasField("pattern")
                and rel.list_catalogs.pattern == ""
            ):
                return pandas.DataFrame([])
            # Handle None pattern by treating it as matching all catalogs
            pattern_str = (
                rel.list_catalogs.pattern
                if rel.list_catalogs.pattern is not None
                else ".*"
            )
            pattern = re.compile(pattern_str)
            return pandas.DataFrame(
                [
                    (name, cat.description)
                    for name, cat in CATALOGS.items()
                    if pattern.match(name) is not None
                ]
            )
        case "current_catalog":
            return pandas.DataFrame({"current_catalog": [CURRENT_CATALOG_NAME]})
        case "set_current_catalog":
            set_current_catalog(rel.set_current_catalog.catalog_name)
            return pandas.DataFrame()
        case "table_exists":
            return get_current_catalog().tableExists(
                rel.table_exists.table_name,
                (
                    rel.table_exists.db_name
                    if rel.table_exists.HasField("db_name")
                    else None
                ),
            )
        # Column related APIs
        case "list_columns":
            return get_current_catalog().listColumns(
                rel.list_columns.table_name,
                (
                    rel.list_columns.db_name
                    if rel.list_columns.HasField("db_name")
                    else None
                ),
            )
        # View related APIs
        case "drop_global_temp_view":
            return get_current_catalog().dropGlobalTempView(
                rel.drop_global_temp_view.view_name
            )
        case "drop_temp_view":
            return get_current_catalog().dropTempView(rel.drop_temp_view.view_name)
        case "recover_partitions":
            # This is a no-op operation in SAS as Snowpark doesn't have the concept of partitions.
            # All the data in the dataframe will be treated as a single partition, and this will not
            # have any side effects.
            logger.warning("recover_partitions is triggered with no-op")
            return pandas.DataFrame()
        # Table related APIs
        case "create_table":
            return get_current_catalog().createTable(
                rel.create_table.table_name,
                rel.create_table.path,
                rel.create_table.source,
                rel.create_table.schema,
                rel.create_table.description,
                **rel.create_table.options,
            )
        # Caching related APIs
        case "cache_table":
            return get_current_catalog().cacheTable(
                rel.cache_table.table_name,
                rel.cache_table.storage_level,
            )
        case "clear_cache":
            return get_current_catalog().clearCache()
        case "is_cached":
            return get_current_catalog().isCached(rel.is_cached.table_name)
        case "refresh_by_path":
            return get_current_catalog().refreshByPath(rel.refresh_by_path.path)
        case "refresh_table":
            return get_current_catalog().refreshTable(rel.refresh_table.table_name)
        case "uncache_table":
            return get_current_catalog().uncacheTable(rel.uncache_table.table_name)
        case other:
            # TODO: list_function implementation is blocked on SNOW-1787268
            exception = SnowparkConnectNotImplementedError(f"Other Relation {other}")
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
