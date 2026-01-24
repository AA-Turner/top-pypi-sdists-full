#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import re
import typing

import pandas
import pyspark.sql.connect.proto.common_pb2 as common_proto
import pyspark.sql.connect.proto.types_pb2 as types_proto
from pyspark.errors.exceptions.base import AnalysisException
from pyspark.sql.connect.client.core import Retrying
from snowflake.core.exceptions import APIError, NotFoundError
from snowflake.core.schema import Schema
from snowflake.core.table import Table, TableColumn

from snowflake.snowpark._internal.analyzer.analyzer_utils import (
    quote_name_without_upper_casing,
    unquote_if_quoted,
)
from snowflake.snowpark.functions import lit
from snowflake.snowpark.types import BooleanType, StringType
from snowflake.snowpark_connect.column_qualifier import ColumnQualifier
from snowflake.snowpark_connect.config import (
    auto_uppercase_non_column_identifiers,
    global_config,
)
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import (
    TABLE_OR_VIEW_NOT_FOUND_ERROR_CLASS,
    attach_custom_error_code,
)
from snowflake.snowpark_connect.error.exceptions import MaxRetryExceeded
from snowflake.snowpark_connect.relation.catalogs.abstract_spark_catalog import (
    AbstractSparkCatalog,
    _get_current_snowflake_schema,
    _process_multi_layer_database,
    _process_multi_layer_identifier,
)
from snowflake.snowpark_connect.type_mapping import proto_to_snowpark_type
from snowflake.snowpark_connect.utils.identifiers import (
    FQN,
    spark_to_sf_single_id_with_unquoting,
    split_fully_qualified_spark_name,
)
from snowflake.snowpark_connect.utils.session import get_or_create_snowpark_session
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
)
from snowflake.snowpark_connect.utils.temporary_view_helper import (
    get_temp_view,
    get_temp_view_normalized_names,
    unregister_temp_view,
)
from snowflake.snowpark_connect.utils.udf_cache import cached_udf


def _is_retryable_api_error(e: Exception) -> bool:
    """
    Determine if an APIError should be retried.

    Only retry on server errors, rate limiting, and transient network issues.
    Don't retry on client errors like authentication, authorization, or validation failures.
    """
    if not isinstance(e, APIError):
        return False

    # Check if the error has a status_code attribute
    if hasattr(e, "status_code"):
        # Retry on server errors (5xx), rate limiting (429), and some client errors (400)
        # 400 can be transient in some cases (like the original error trace shows)
        return e.status_code in [400, 429, 500, 502, 503, 504]

    # For APIErrors without explicit status codes, check the message
    error_msg = str(e).lower()
    retryable_patterns = [
        "timeout",
        "connection",
        "network",
        "unavailable",
        "temporary",
        "rate limit",
        "throttle",
    ]

    return any(pattern in error_msg for pattern in retryable_patterns)


def _normalize_identifier(identifier: str | None) -> str | None:
    if identifier is None:
        return None
    return identifier.upper() if auto_uppercase_non_column_identifiers() else identifier


def sf_quote(name: str | None) -> str | None:
    if name is None:
        return None
    return quote_name_without_upper_casing(_normalize_identifier(name))


class SnowflakeCatalog(AbstractSparkCatalog):
    def __init__(self) -> None:
        super().__init__(name="spark_catalog", description=None)

    def listDatabases(
        self,
        pattern: str | None = None,
    ) -> pandas.DataFrame:
        """List all databases accessible in Snowflake with an optional name to filter by."""

        if pattern == "":
            return pandas.DataFrame([])

        # This pattern is case-sensitive while our SAS implementation is not
        catalog, sf_database, sf_schema = _process_multi_layer_database(pattern)
        sf_schema = sf_schema.replace("*", ".*")
        if catalog is not None and self != catalog:
            exception = SnowparkConnectNotImplementedError(
                "Calling into another catalog is not currently supported"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
        sp_catalog = get_or_create_snowpark_session().catalog

        dbs: list[Schema] | None = None
        for attempt in Retrying(
            max_retries=5,
            initial_backoff=100,  # 100ms
            max_backoff=5000,  # 5 s
            backoff_multiplier=2.0,
            jitter=100,
            min_jitter_threshold=200,
            can_retry=_is_retryable_api_error,
        ):
            with attempt:
                dbs = sp_catalog.list_schemas(
                    database=sf_quote(sf_database),
                    pattern=_normalize_identifier(sf_schema),
                )
        if dbs is None:
            raise MaxRetryExceeded(
                f"Failed to fetch databases {f'with pattern {pattern} ' if pattern is not None else ''}after all retry attempts",
                custom_error_code=ErrorCodes.INTERNAL_ERROR,
            )
        names: list[str] = list()
        catalogs: list[str] = list()
        descriptions: list[str | None] = list()
        locationUris: list[str] = list()
        for db in dbs:
            name = unquote_if_quoted(db.name)
            if name == "INFORMATION_SCHEMA" and global_config._get_config_setting(
                "spark.Catalog.databaseFilterInformationSchema"
            ):
                continue
            names.append(name)
            catalogs.append(self.name)
            descriptions.append(db.comment)
            locationUris.append(f"snowflake://{name}")
        return pandas.DataFrame(
            {
                "name": names,
                "catalog": catalogs,
                "description": descriptions,
                "locationUri": locationUris,
            }
        )

    def getDatabase(
        self,
        spark_dbName: str,
    ) -> pandas.DataFrame:
        """Listing a single database that's accessible in Snowflake."""
        catalog, sf_database, sf_schema = _process_multi_layer_database(spark_dbName)
        if catalog is not None and self != catalog:
            exception = SnowparkConnectNotImplementedError(
                "Calling into another catalog is not currently supported"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
        sp_catalog = get_or_create_snowpark_session().catalog

        db: Schema | None = None
        for attempt in Retrying(
            max_retries=5,
            initial_backoff=100,  # 100ms
            max_backoff=5000,  # 5 s
            backoff_multiplier=2.0,
            jitter=100,
            min_jitter_threshold=200,
            can_retry=_is_retryable_api_error,
        ):
            with attempt:
                db = sp_catalog.get_schema(
                    schema=sf_quote(sf_schema), database=sf_quote(sf_database)
                )
        if db is None:
            raise MaxRetryExceeded(
                f"Failed to fetch database {spark_dbName} after all retry attempts",
                custom_error_code=ErrorCodes.INTERNAL_ERROR,
            )

        name = unquote_if_quoted(db.name)
        return pandas.DataFrame(
            {
                "name": [name],
                "catalog": [self.name],
                "description": [db.comment],
                "locationUri": [f"snowflake://{name}"],
            }
        )

    def databaseExists(
        self,
        spark_dbName: str,
    ) -> pandas.DataFrame:
        """Whether a database with provided name exists in Snowflake."""
        try:
            self.getDatabase(spark_dbName)
            exists = True
        except NotFoundError:
            exists = False
        return pandas.DataFrame({"exists": [exists]})

    def _get_temp_view_prefixes(self, spark_dbName: str | None) -> list[str]:
        if spark_dbName is None:
            return []
        return [
            quote_name_without_upper_casing(part)
            for part in split_fully_qualified_spark_name(spark_dbName)
        ]

    def _list_temp_views(
        self,
        spark_dbName: str | None = None,
        pattern: str | None = None,
    ) -> typing.Tuple[
        list[str | None],
        list[list[str | None]],
        list[str],
        list[str | None],
        list[str | None],
        list[bool],
    ]:
        catalogs: list[str | None] = list()
        namespaces: list[list[str | None]] = list()
        names: list[str] = list()
        descriptions: list[str | None] = list()
        table_types: list[str | None] = list()
        is_temporaries: list[bool] = list()

        temp_views_prefix = ".".join(self._get_temp_view_prefixes(spark_dbName))
        normalized_spark_dbName = (
            temp_views_prefix.lower()
            if global_config.spark_sql_caseSensitive
            else temp_views_prefix
        )
        normalized_global_temp_database_name = (
            quote_name_without_upper_casing(
                global_config.spark_sql_globalTempDatabase.lower()
            )
            if global_config.spark_sql_caseSensitive
            else quote_name_without_upper_casing(
                global_config.spark_sql_globalTempDatabase
            )
        )

        temp_views = get_temp_view_normalized_names()
        null_safe_pattern = pattern if pattern is not None else ""

        for temp_view in temp_views:
            normalized_temp_view = (
                temp_view.lower()
                if global_config.spark_sql_caseSensitive
                else temp_view
            )
            fqn = FQN.from_string(temp_view)
            normalized_schema = (
                fqn.schema.lower()
                if fqn.schema is not None and global_config.spark_sql_caseSensitive
                else fqn.schema
            )

            is_global_view = normalized_global_temp_database_name == normalized_schema
            is_local_temp_view = fqn.schema is None
            # Temporary views are always shown if they match the pattern
            matches_prefix = (
                normalized_spark_dbName == normalized_schema or is_local_temp_view
            )
            if matches_prefix and bool(
                re.match(null_safe_pattern, normalized_temp_view)
            ):
                names.append(unquote_if_quoted(fqn.name))
                catalogs.append(None)
                namespaces.append(
                    [global_config.spark_sql_globalTempDatabase]
                    if is_global_view
                    else []
                )
                descriptions.append(None)
                table_types.append("TEMPORARY")
                is_temporaries.append(True)
        return (
            catalogs,
            namespaces,
            names,
            descriptions,
            table_types,
            is_temporaries,
        )

    def listTables(
        self,
        spark_dbName: str | None = None,
        pattern: str | None = None,
    ) -> pandas.DataFrame:
        """Listing all tables/views accessible in Snowflake, optionally filterable on database, schema, and a pattern for the table names."""
        if spark_dbName is not None:
            catalog, sf_database, sf_schema = _process_multi_layer_database(
                spark_dbName
            )
            if catalog is not None and self != catalog:
                exception = SnowparkConnectNotImplementedError(
                    "Calling into another catalog is not currently supported"
                )
                attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
                raise exception
        else:
            catalog = sf_database = sf_schema = None

        tables = self._list_objects(
            object_name="TABLES",
            database=sf_quote(sf_database),
            schema=sf_quote(sf_schema),
            pattern=_normalize_identifier(pattern),
        )
        views = self._list_objects(
            object_name="VIEWS",
            database=sf_quote(sf_database),
            schema=sf_quote(sf_schema),
            pattern=_normalize_identifier(pattern),
        )
        catalogs: list[str | None] = list()
        namespaces: list[list[str | None]] = list()
        names: list[str] = list()
        descriptions: list[str | None] = list()
        table_types: list[str | None] = list()
        is_temporaries: list[bool] = list()
        for o in tables:
            names.append(unquote_if_quoted(o[1]))
            catalogs.append(self.name)
            namespaces.append([unquote_if_quoted(o[3])])
            descriptions.append(o[5] if o[5] else None)
            table_types.append("PERMANENT" if o[4] == "TABLE" else o[4])
            is_temporaries.append(o[4] == "TEMPORARY")
        for o in views:
            names.append(unquote_if_quoted(o[1]))
            catalogs.append(self.name)
            namespaces.append([unquote_if_quoted(o[4])])
            descriptions.append(o[6] if o[6] else None)
            table_types.append("PERMANENT")
            is_temporaries.append(False)

        (
            non_materialized_catalogs,
            non_materialized_namespaces,
            non_materialized_names,
            non_materialized_descriptions,
            non_materialized_table_types,
            non_materialized_is_temporaries,
        ) = self._list_temp_views(spark_dbName, pattern)
        catalogs.extend(non_materialized_catalogs)
        namespaces.extend(non_materialized_namespaces)
        names.extend(non_materialized_names)
        descriptions.extend(non_materialized_descriptions)
        table_types.extend(non_materialized_table_types)
        is_temporaries.extend(non_materialized_is_temporaries)

        return pandas.DataFrame(
            {
                "name": names,
                "catalog": catalogs,
                "namespace": namespaces,
                "description": descriptions,
                "tableType": table_types,
                "isTemporary": is_temporaries,
            }
        )

    def _list_objects(
        self,
        *,
        object_name: str,
        database: typing.Optional[str],
        schema: typing.Optional[str],
        pattern: typing.Optional[str] = None,
    ):
        session = get_or_create_snowpark_session()
        if not database:
            database = session.catalog.get_current_database()
        if not schema:
            schema = session.catalog.get_current_schema()
        df = get_or_create_snowpark_session().sql(
            f"SHOW {object_name} IN {database}.{schema}"
        )
        if pattern:

            @cached_udf(
                input_types=[StringType(), StringType()], return_type=BooleanType()
            )
            def python_regex_filter(pattern: str, input: str) -> bool:
                return bool(re.match(pattern, input))

            df = df.filter(python_regex_filter(lit(pattern), df['"name"']))

        return df.collect()

    def getTable(
        self,
        spark_tableName: str,
    ) -> pandas.DataFrame:
        """Listing a single table/view with provided name that's accessible in Snowflake."""

        def _get_temp_view():
            spark_table_name_parts = [
                quote_name_without_upper_casing(part)
                for part in split_fully_qualified_spark_name(spark_tableName)
            ]
            spark_view_name = ".".join(spark_table_name_parts)
            temp_view = get_temp_view(spark_view_name)
            if temp_view:
                return pandas.DataFrame(
                    {
                        "name": [unquote_if_quoted(spark_table_name_parts[-1])],
                        "catalog": [None],
                        "namespace": [
                            [unquote_if_quoted(spark_table_name_parts[-2])]
                            if len(spark_table_name_parts) > 1
                            else []
                        ],
                        "description": [None],
                        "tableType": ["TEMPORARY"],
                        "isTemporary": [True],
                    }
                )
            return None

        # Attempt to get the view from the non materialized views first
        temp_view = _get_temp_view()
        if temp_view is not None:
            return temp_view

        sp_catalog = get_or_create_snowpark_session().catalog
        catalog, sf_database, sf_schema, table_name = _process_multi_layer_identifier(
            spark_tableName
        )
        if catalog is not None and self != catalog:
            exception = SnowparkConnectNotImplementedError(
                "Calling into another catalog is not currently supported"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception

        table: Table | None = None
        try:
            for attempt in Retrying(
                max_retries=5,
                initial_backoff=100,  # 100ms
                max_backoff=5000,  # 5 s
                backoff_multiplier=2.0,
                jitter=100,
                min_jitter_threshold=200,
                can_retry=_is_retryable_api_error,
            ):
                with attempt:
                    table = sp_catalog.get_table(
                        database=sf_quote(sf_database),
                        schema=sf_quote(sf_schema),
                        table_name=sf_quote(table_name),
                    )
        except NotFoundError:
            exception = AnalysisException(
                error_class=TABLE_OR_VIEW_NOT_FOUND_ERROR_CLASS,
                message_parameters={"relationName": spark_tableName},
            )
            attach_custom_error_code(exception, ErrorCodes.TABLE_NOT_FOUND)
            raise exception

        if table is None:
            raise MaxRetryExceeded(
                f"Failed to fetch table {spark_tableName} after all retry attempts",
                custom_error_code=ErrorCodes.INTERNAL_ERROR,
            )

        return pandas.DataFrame(
            {
                "name": [unquote_if_quoted(table.name)],
                "catalog": [self.name],
                "namespace": [[unquote_if_quoted(table.schema_name)]],
                "description": [table.comment],
                "tableType": [table.kind],
                "isTemporary": [table.kind == "TEMPORARY"],
            }
        )

    def tableExists(
        self,
        spark_tableName: str,
        spark_dbName: str | None,
    ) -> pandas.DataFrame:
        """Whether a table/view with provided name exists in Snowflake, optionally filterable with dbName.
        If no database is specified, first try to treat tableName as a multi-layer-namespace identifier
        (or fully qualified name), then try tableName as a normal table name in the current database if necessary.
        Argument dbName is not actually implemented yet while we figure out how to map databases from Spark to Snowflake.
        """
        table_mli = spark_tableName
        if spark_dbName:
            table_mli = f"{spark_dbName}.{table_mli}"

        try:
            self.getTable(table_mli)
            exists = True
        except AnalysisException as ex:
            if ex.error_class == TABLE_OR_VIEW_NOT_FOUND_ERROR_CLASS:
                exists = False
        return pandas.DataFrame({"exists": [exists]})

    def _list_temp_view_columns(
        self,
        spark_tableName: str,
        spark_dbName: typing.Optional[str] = None,
    ):
        spark_view_name_parts = [
            quote_name_without_upper_casing(part)
            for part in split_fully_qualified_spark_name(spark_tableName)
        ]
        spark_view_name_parts = (
            self._get_temp_view_prefixes(spark_dbName) + spark_view_name_parts
        )
        spark_view_name = ".".join(spark_view_name_parts)
        temp_view = get_temp_view(spark_view_name)

        if not temp_view:
            return None

        return self._list_columns_from_dataframe_container(temp_view)

    def _list_columns_from_dataframe_container(
        self, container: DataFrameContainer
    ) -> pandas.DataFrame:
        names: list[str] = list()
        descriptions: list[str | None] = list()
        data_types: list[str] = list()
        nullables: list[bool] = list()
        is_partitions: list[bool] = list()
        is_buckets: list[bool] = list()

        for field, spark_column in zip(
            container.dataframe.schema.fields,
            container.column_map.get_spark_columns(),
        ):
            names.append(spark_column)
            descriptions.append(None)
            data_types.append(field.datatype.simpleString())
            nullables.append(field.nullable)
            is_partitions.append(False)
            is_buckets.append(False)

        return pandas.DataFrame(
            {
                "name": names,
                "description": descriptions,
                "dataType": data_types,
                "nullable": nullables,
                "isPartition": is_partitions,
                "isBucket": is_buckets,
            }
        )

    def listColumns(
        self,
        spark_tableName: str,
        spark_dbName: typing.Optional[str] = None,
    ) -> pandas.DataFrame:
        """List all columns in a table/view, optionally database name filter can be provided."""

        temp_view_columns = self._list_temp_view_columns(spark_tableName, spark_dbName)
        if temp_view_columns is not None:
            return temp_view_columns

        sp_catalog = get_or_create_snowpark_session().catalog
        columns: list[TableColumn] | None = None
        if spark_dbName is None:
            catalog, sf_database, sf_schema, sf_table = _process_multi_layer_identifier(
                spark_tableName
            )
            if catalog is not None and self != catalog:
                exception = SnowparkConnectNotImplementedError(
                    "Calling into another catalog is not currently supported"
                )
                attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
                raise exception
            for attempt in Retrying(
                max_retries=5,
                initial_backoff=100,  # 100ms
                max_backoff=5000,  # 5 s
                backoff_multiplier=2.0,
                jitter=100,
                min_jitter_threshold=200,
                can_retry=_is_retryable_api_error,
            ):
                with attempt:
                    columns = sp_catalog.list_columns(
                        database=sf_quote(sf_database),
                        schema=sf_quote(sf_schema),
                        table_name=sf_quote(sf_table),
                    )
        else:
            for attempt in Retrying(
                max_retries=5,
                initial_backoff=100,  # 100ms
                max_backoff=5000,  # 5 s
                backoff_multiplier=2.0,
                jitter=100,
                min_jitter_threshold=200,
                can_retry=_is_retryable_api_error,
            ):
                with attempt:
                    columns = sp_catalog.list_columns(
                        schema=sf_quote(spark_dbName),
                        table_name=sf_quote(spark_tableName),
                    )
        if columns is None:
            raise MaxRetryExceeded(
                f"Failed to fetch columns of {spark_tableName} after all retry attempts",
                custom_error_code=ErrorCodes.INTERNAL_ERROR,
            )
        names: list[str] = list()
        descriptions: list[str | None] = list()
        data_types: list[str] = list()
        nullables: list[bool] = list()
        is_partitions: list[bool] = list()
        is_buckets: list[bool] = list()
        for column in columns:
            names.append(unquote_if_quoted(column.name))
            descriptions.append(column.comment)
            data_types.append(column.datatype)
            nullables.append(bool(column.nullable))
            is_partitions.append(False)
            is_buckets.append(False)

        return pandas.DataFrame(
            {
                "name": names,
                "description": descriptions,
                "dataType": data_types,
                "nullable": nullables,
                "isPartition": is_partitions,
                "isBucket": is_buckets,
            }
        )

    def currentDatabase(self) -> pandas.DataFrame:
        """Get the currently used database's name."""
        db_name = _get_current_snowflake_schema()
        assert db_name is not None, "current database could not be confirmed"
        return pandas.DataFrame({"current_database": [unquote_if_quoted(db_name)]})

    def setCurrentDatabase(
        self,
        spark_dbName: str,
    ) -> pandas.DataFrame:
        """Set the currently used database's name."""
        sp_catalog = get_or_create_snowpark_session().catalog
        sp_catalog.setCurrentSchema(sf_quote(spark_dbName))
        return pandas.DataFrame({"current_database": [spark_dbName]})

    def dropGlobalTempView(
        self,
        spark_view_name: str,
    ) -> DataFrameContainer:
        session = get_or_create_snowpark_session()
        schema = global_config.spark_sql_globalTempDatabase
        result = False
        if spark_view_name:
            result = unregister_temp_view(
                f"{spark_to_sf_single_id_with_unquoting(schema)}.{spark_to_sf_single_id_with_unquoting(spark_view_name)}"
            )

        if not result:
            drop_result = session.sql(
                "drop view if exists identifier(?)",
                params=[f"{sf_quote(schema)}.{sf_quote(spark_view_name)}"],
            ).collect()
            result = (
                len(drop_result) == 1
                and "successfully dropped" in drop_result[0]["status"]
            )
        columns = ["value"]
        result_df = session.createDataFrame([result], schema=columns)
        return DataFrameContainer.create_with_column_mapping(
            dataframe=result_df,
            spark_column_names=columns,
            snowpark_column_names=columns,
            snowpark_column_types=[BooleanType()],
        )

    def dropTempView(
        self,
        spark_view_name: str,
    ) -> DataFrameContainer:
        """Drop the current temporary view."""
        session = get_or_create_snowpark_session()
        columns = ["value"]
        result = False
        if spark_view_name:
            result = unregister_temp_view(
                spark_to_sf_single_id_with_unquoting(spark_view_name)
            )
        if not result:
            drop_result = session.sql(
                "drop view if exists identifier(?)",
                params=[sf_quote(spark_view_name)],
            ).collect()
            result = (
                len(drop_result) == 1
                and "successfully dropped" in drop_result[0]["status"]
            )

        result_df = session.createDataFrame([result], schema=columns)
        return DataFrameContainer.create_with_column_mapping(
            dataframe=result_df,
            spark_column_names=columns,
            snowpark_column_names=columns,
            snowpark_column_types=[BooleanType()],
        )

    def createTable(
        self,
        tableName: str,
        path: str,
        source: str,
        schema: types_proto.DataType,
        description: str,
        **options: typing.Any,
    ) -> DataFrameContainer:
        """Create either an external, or a managed table.

        If path is supplied in which the data for this table exists. When path is specified, an external table is
        created from the data at the given path. Otherwise a managed table is created.

        In case a managed table is being created, schema is required.
        """
        # TODO: support fully-qualified tableName
        if source == "":
            source = global_config.get("spark.sql.sources.default")
        if source not in ("csv", "json", "avro", "parquet", "orc", "xml"):
            exception = SnowparkConnectNotImplementedError(
                f"Source '{source}' is not currently supported by Catalog.createTable. "
                "Maybe default value through 'spark.sql.sources.default' should be set."
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
        if path != "":
            # External table creation is not supported currently.
            exception = SnowparkConnectNotImplementedError(
                "External table creation is not supported currently."
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception

        session = get_or_create_snowpark_session()
        # Managed table
        if schema.ByteSize() == 0:
            exception = SnowparkConnectNotImplementedError(
                f"Unable to infer schema for {source.upper()}. It must be specified manually.",
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
        sp_schema = proto_to_snowpark_type(schema)
        columns = [c.name for c in schema.struct.fields]
        table_name_parts = split_fully_qualified_spark_name(tableName)
        qualifiers: list[set[ColumnQualifier]] = [
            {ColumnQualifier(tuple(table_name_parts))} for _ in columns
        ]
        column_types = [f.datatype for f in sp_schema.fields]
        return DataFrameContainer.create_with_column_mapping(
            dataframe=session.createDataFrame([], sp_schema),
            spark_column_names=columns,
            snowpark_column_names=columns,
            snowpark_column_types=column_types,
            column_qualifiers=qualifiers,
        )

    def isCached(self, spark_tableName: str) -> pandas.DataFrame:
        """Whether a table is cached by us locally.

        Check whether a table exists and then delegate to the local cache.
        """
        self.getTable(spark_tableName)
        return super().isCached(spark_tableName)

    def cacheTable(
        self,
        spark_tableName: str,
        storageLevel: common_proto.StorageLevel | None = None,
    ) -> pandas.DataFrame:
        """Cache a table, or view locally.

        Check whether a table exists and then delegate to the local cache.
        """
        self.getTable(spark_tableName)
        return super().cacheTable(spark_tableName, storageLevel)

    def uncacheTable(self, spark_tableName: str) -> pandas.DataFrame:
        """Uncache a table, or view locally.

        Check whether a table exists and then delegate to the local cache.
        """
        self.getTable(spark_tableName)
        return super().uncacheTable(spark_tableName)

    def refreshTable(self, spark_tableName: str) -> pandas.DataFrame:
        """Refresh a table, or view locally.

        Check whether a table exists and then delegate to the local cache.
        """
        self.getTable(spark_tableName)
        return super().refreshTable(spark_tableName)
