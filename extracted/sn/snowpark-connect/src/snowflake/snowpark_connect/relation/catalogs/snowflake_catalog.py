#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import re
import typing

import pandas
import pyspark.sql.connect.proto.common_pb2 as common_proto
import pyspark.sql.connect.proto.types_pb2 as types_proto
from pyspark.errors.exceptions.base import AnalysisException

from snowflake.snowpark._internal.analyzer.analyzer_utils import (
    quote_name_without_upper_casing,
    unquote_if_quoted,
)
from snowflake.snowpark.exceptions import SnowparkSQLException
from snowflake.snowpark.functions import lit
from snowflake.snowpark.types import BooleanType, StringType
from snowflake.snowpark_connect.column_qualifier import ColumnQualifier
from snowflake.snowpark_connect.config import global_config
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import (
    SCHEMA_NOT_FOUND_ERROR_CLASS,
    TABLE_OR_VIEW_NOT_FOUND_ERROR_CLASS,
    attach_custom_error_code,
)
from snowflake.snowpark_connect.error.exceptions import MissingDatabase, MissingSchema
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
    is_temp_view_in_snowflake,
    unregister_snowflake_temp_view,
)
from snowflake.snowpark_connect.utils.udf_cache import cached_udf


def _normalize_identifier(identifier: str | None) -> str | None:
    if identifier is None:
        return None
    return (
        identifier.upper() if not global_config.spark_sql_caseSensitive else identifier
    )


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

        session = get_or_create_snowpark_session()
        if sf_database:
            sf_database_q = sf_quote(sf_database)
        else:
            sf_database_q = session.catalog.get_current_database()
            if sf_database_q is None:
                raise MissingDatabase()

        try:
            rows = session.sql(f"SHOW SCHEMAS IN DATABASE {sf_database_q}").collect()
        except SnowparkSQLException as e:
            # 2003 = "Object does not exist"; 2043 = "Object does not exist, or
            # operation cannot be performed" (raised when the database is missing).
            if hasattr(e, "sql_error_code") and e.sql_error_code in (2003, 2043):
                return pandas.DataFrame([])
            raise

        normalized_pat = _normalize_identifier(sf_schema)

        names: list[str] = list()
        catalogs: list[str] = list()
        descriptions: list[str | None] = list()
        locationUris: list[str] = list()
        for r in rows:
            name = unquote_if_quoted(r["name"])
            if name == "INFORMATION_SCHEMA" and global_config._get_config_setting(
                "spark.Catalog.databaseFilterInformationSchema"
            ):
                continue
            if normalized_pat and not re.match(normalized_pat, name):
                continue
            names.append(name)
            catalogs.append(self.name)
            descriptions.append(r["comment"] if r["comment"] else None)
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

        row = self._show_schema_metadata(sf_database, sf_schema)
        if row is None:
            exception = AnalysisException(
                error_class=SCHEMA_NOT_FOUND_ERROR_CLASS,
                message_parameters={"schemaName": spark_dbName},
            )
            raise exception

        name = unquote_if_quoted(row["name"])
        return pandas.DataFrame(
            {
                "name": [name],
                "catalog": [self.name],
                "description": [row["comment"] if row["comment"] else None],
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
        except AnalysisException as ex:
            if ex.error_class == SCHEMA_NOT_FOUND_ERROR_CLASS:
                exists = False
            else:
                raise
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
        # Snowflake-backed temp views surface through SHOW VIEWS like any other
        # view; their leaf names let us relabel those rows as TEMPORARY rather
        # than the default PERMANENT, matching getTable.
        snowflake_backed_temp_view_leaf_names = {
            unquote_if_quoted(FQN.from_string(name).name).lower()
            for name in (
                set(get_temp_view_normalized_names(include_created_in_snowflake=True))
                - set(get_temp_view_normalized_names())
            )
        }

        for o in tables:
            names.append(unquote_if_quoted(o[1]))
            catalogs.append(self.name)
            namespaces.append([unquote_if_quoted(o[3])])
            descriptions.append(o[5] if o[5] else None)
            table_types.append("PERMANENT" if o[4] == "TABLE" else o[4])
            is_temporaries.append(o[4] == "TEMPORARY")
        for o in views:
            view_name = unquote_if_quoted(o[1])
            is_temp = view_name.lower() in snowflake_backed_temp_view_leaf_names
            names.append(view_name)
            catalogs.append(self.name)
            namespaces.append([unquote_if_quoted(o[4])])
            descriptions.append(o[6] if o[6] else None)
            table_types.append("TEMPORARY" if is_temp else "PERMANENT")
            is_temporaries.append(is_temp)

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

            def python_regex_filter(pattern: str, input: str) -> bool:
                return bool(re.match(pattern, input))

            namespace_hash = f"{abs(hash((database, schema))):X}"
            python_regex_filter.__name__ = f"python_regex_filter_{namespace_hash}"
            regex_filter_udf = cached_udf(
                python_regex_filter,
                input_types=[StringType(), StringType()],
                return_type=BooleanType(),
            )

            df = df.filter(regex_filter_udf(lit(pattern), df['"name"']))

        return df.collect()

    def getTable(
        self,
        spark_tableName: str,
    ) -> pandas.DataFrame:
        """Listing a single table/view with provided name that's accessible in Snowflake.

        Uses ``SHOW OBJECTS LIKE`` through the SQL execution path instead of the
        REST v2 API (``sp_catalog.get_table``), which is unreliable under
        concurrent CI workloads (intermittent 400 Bad Request).
        """

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

        catalog, sf_database, sf_schema, table_name = _process_multi_layer_identifier(
            spark_tableName
        )
        if catalog is not None and self != catalog:
            exception = SnowparkConnectNotImplementedError(
                "Calling into another catalog is not currently supported"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception

        row = self._show_object_metadata(sf_database, sf_schema, table_name)
        if row is None:
            exception = AnalysisException(
                error_class=TABLE_OR_VIEW_NOT_FOUND_ERROR_CLASS,
                message_parameters={"relationName": spark_tableName},
            )
            attach_custom_error_code(exception, ErrorCodes.TABLE_NOT_FOUND)
            raise exception

        kind = row["kind"]
        # The REST `Table.kind` only ever surfaced 'PERMANENT' or 'TEMPORARY'.
        # `SHOW OBJECTS` exposes more granular kinds (e.g. 'TEMP VIEW',
        # 'EXTERNAL TABLE', 'MATERIALIZED VIEW', 'TRANSIENT TABLE',
        # 'ICEBERG TABLE', 'DYNAMIC TABLE', ...). Collapse everything that is
        # not explicitly temporary back to 'PERMANENT' to preserve the prior
        # public catalog API contract.
        is_temporary = kind in ("TEMPORARY", "TEMP VIEW")
        table_type = "TEMPORARY" if is_temporary else "PERMANENT"
        return pandas.DataFrame(
            {
                "name": [unquote_if_quoted(row["name"])],
                "catalog": [self.name],
                "namespace": [[unquote_if_quoted(row["schema_name"])]],
                "description": [row["comment"] if row["comment"] else None],
                "tableType": [table_type],
                "isTemporary": [is_temporary],
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
            self._verify_table_exists(table_mli)
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
        else:
            sf_database = None
            sf_schema = spark_dbName
            sf_table = spark_tableName

        parts = []
        if sf_database:
            parts.append(sf_quote(sf_database))
        if sf_schema:
            parts.append(sf_quote(sf_schema))
        parts.append(sf_quote(sf_table))
        fqn = ".".join(parts)

        session = get_or_create_snowpark_session()
        try:
            describe_rows = session.sql(f"DESCRIBE TABLE {fqn}").collect()
        except SnowparkSQLException as e:
            if hasattr(e, "sql_error_code") and e.sql_error_code in (2003, 2043):
                exception = AnalysisException(
                    error_class=TABLE_OR_VIEW_NOT_FOUND_ERROR_CLASS,
                    message_parameters={"relationName": spark_tableName},
                )
                attach_custom_error_code(exception, ErrorCodes.TABLE_NOT_FOUND)
                raise exception
            raise

        # Only emit rows that describe actual columns (DESCRIBE TABLE on a
        # table with a virtual column would also include `kind='VIRTUAL_COLUMN'`,
        # which list_columns surfaces too, so we keep all column-style rows).
        column_rows = [
            r for r in describe_rows if r["kind"] in (None, "COLUMN", "VIRTUAL_COLUMN")
        ]

        names: list[str] = list()
        descriptions: list[str | None] = list()
        data_types: list[str] = list()
        nullables: list[bool] = list()
        is_partitions: list[bool] = list()
        is_buckets: list[bool] = list()
        for r in column_rows:
            names.append(unquote_if_quoted(r["name"]))
            descriptions.append(r["comment"] if r["comment"] else None)
            data_types.append(r["type"])
            nullables.append(r["null?"] == "Y")
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
            cache_name = (
                f"{spark_to_sf_single_id_with_unquoting(schema)}."
                f"{spark_to_sf_single_id_with_unquoting(spark_view_name)}"
            )
            snowflake_name = f"{sf_quote(schema)}.{sf_quote(spark_view_name)}"
            result = unregister_snowflake_temp_view(
                session, cache_name, snowflake_name, if_exists=True
            )
            if not result:
                drop_result = session.sql(
                    "drop view if exists identifier(?)",
                    params=[snowflake_name],
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
            simplified_name = spark_to_sf_single_id_with_unquoting(spark_view_name)
            result = unregister_snowflake_temp_view(
                session, simplified_name, sf_quote(spark_view_name), if_exists=True
            )
            if not result and is_temp_view_in_snowflake(simplified_name):
                # A temp view created via CREATE TEMP VIEW ... USING bypasses the
                # cache, so it must be dropped directly from Snowflake.
                try:
                    drop_result = session.sql(
                        "drop view if exists identifier(?)",
                        params=[sf_quote(spark_view_name)],
                    ).collect()
                    result = (
                        len(drop_result) == 1
                        and "successfully dropped" in drop_result[0]["status"]
                    )
                except SnowparkSQLException as e:
                    if "not specified type 'VIEW'" in str(e):
                        result = False
                    else:
                        raise

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

        sf_table_name = ".".join(sf_quote(p) for p in table_name_parts)
        empty_df = session.createDataFrame([], sp_schema)
        empty_df.write.save_as_table(sf_table_name)

        if description:
            escaped_desc = description.replace("\\", "\\\\").replace("'", "''")
            session.sql(
                f"COMMENT ON TABLE {sf_table_name} IS '{escaped_desc}'"
            ).collect()

        return DataFrameContainer.create_with_column_mapping(
            dataframe=session.table(sf_table_name),
            spark_column_names=columns,
            snowpark_column_names=columns,
            snowpark_column_types=column_types,
            column_qualifiers=qualifiers,
        )

    def _show_object_metadata(
        self,
        sf_database: str | None,
        sf_schema: str | None,
        table_name: str,
    ) -> typing.Mapping[str, typing.Any] | None:
        """Fetch a single object's metadata via ``SHOW OBJECTS LIKE``.

        Returns the matching ``Row`` (as a mapping) when the object exists, or
        ``None`` when it does not (including when the parent database/schema does
        not exist).

        Uses the SQL execution path instead of the REST v2 API
        (``sp_catalog.get_table``) which is unreliable under concurrent CI
        workloads (intermittent 400 Bad Request).
        """
        session = get_or_create_snowpark_session()

        # When the caller supplies a database/schema we normalize + quote it
        # (matching the rest of the catalog code). For the current
        # database/schema we use the value Snowpark already returns
        # quoted/case-preserved — running it through `sf_quote` would
        # uppercase mixed-case identifiers (e.g. `"default"` -> `"DEFAULT"`)
        # and break lookups against schemas created via Spark Connect.
        if sf_database:
            sf_database_q = sf_quote(sf_database)
        else:
            sf_database_q = session.catalog.get_current_database()
            if sf_database_q is None:
                raise MissingDatabase()

        if sf_schema:
            sf_schema_q = sf_quote(sf_schema)
        else:
            sf_schema_q = session.catalog.get_current_schema()
            if sf_schema_q is None:
                raise MissingSchema()

        normalized_name = _normalize_identifier(table_name)
        # SHOW LIKE treats `_` and `%` as wildcards; escape them (and any
        # backslashes / single quotes) so the pattern matches `table_name` exactly.
        escaped_pattern = (
            normalized_name.replace("\\", "\\\\")
            .replace("%", "\\%")
            .replace("_", "\\_")
            .replace("'", "''")
        )

        try:
            rows = session.sql(
                f"SHOW OBJECTS LIKE '{escaped_pattern}' "
                f"IN SCHEMA {sf_database_q}.{sf_schema_q}"
            ).collect()
        except SnowparkSQLException as e:
            # 2003 = "Object does not exist"; 2043 = "Object does not exist, or
            # operation cannot be performed" (raised when the parent database
            # or schema is missing).
            if hasattr(e, "sql_error_code") and e.sql_error_code in (2003, 2043):
                return None
            raise

        # SHOW LIKE matches case-insensitively; defensively filter for an exact
        # name match so we never return a different object.
        for r in rows:
            if r["name"] == normalized_name:
                return r
        return None

    def _show_schema_metadata(
        self,
        sf_database: str | None,
        sf_schema: str,
    ) -> typing.Mapping[str, typing.Any] | None:
        """Fetch a single schema's metadata via ``SHOW SCHEMAS LIKE``.

        Returns the matching ``Row`` (as a mapping) when the schema exists, or
        ``None`` when it does not (including when the parent database does
        not exist).

        Uses the SQL execution path instead of the REST v2 API
        (``sp_catalog.get_schema``) which is unreliable under concurrent CI
        workloads (intermittent 400 Bad Request).
        """
        session = get_or_create_snowpark_session()

        # When the caller supplies a database we normalize + quote it (matching
        # the rest of the catalog code). For the current database we use the
        # value Snowpark already returns quoted/case-preserved — running it
        # through `sf_quote` would uppercase mixed-case identifiers
        # (e.g. `"default"` -> `"DEFAULT"`) and break lookups against
        # databases created via Spark Connect.
        if sf_database:
            sf_database_q = sf_quote(sf_database)
        else:
            sf_database_q = session.catalog.get_current_database()
            if sf_database_q is None:
                raise MissingDatabase()

        normalized_name = _normalize_identifier(sf_schema)
        # SHOW LIKE treats `_` and `%` as wildcards; escape them (and any
        # backslashes / single quotes) so the pattern matches `sf_schema` exactly.
        escaped_pattern = (
            normalized_name.replace("\\", "\\\\")
            .replace("%", "\\%")
            .replace("_", "\\_")
            .replace("'", "''")
        )

        try:
            rows = session.sql(
                f"SHOW SCHEMAS LIKE '{escaped_pattern}' IN DATABASE {sf_database_q}"
            ).collect()
        except SnowparkSQLException as e:
            # 2003 = "Object does not exist"; 2043 = "Object does not exist, or
            # operation cannot be performed" (raised when the parent database
            # is missing).
            if hasattr(e, "sql_error_code") and e.sql_error_code in (2003, 2043):
                return None
            raise

        # SHOW LIKE matches case-insensitively; defensively filter for an exact
        # name match so we never return a different schema.
        for r in rows:
            if r["name"] == normalized_name:
                return r
        return None

    def _verify_table_exists(self, spark_tableName: str) -> None:
        """Verify a table/view exists, raising AnalysisException if not.

        Uses DESCRIBE TABLE through the SQL execution path instead of the
        REST v2 API (sp_catalog.get_table), which is unreliable under
        concurrent CI workloads (intermittent 400 Bad Request).
        """
        spark_table_name_parts = [
            quote_name_without_upper_casing(part)
            for part in split_fully_qualified_spark_name(spark_tableName)
        ]
        spark_view_name = ".".join(spark_table_name_parts)
        if get_temp_view(spark_view_name):
            return

        catalog, sf_database, sf_schema, table_name = _process_multi_layer_identifier(
            spark_tableName
        )
        if catalog is not None and self != catalog:
            exception = SnowparkConnectNotImplementedError(
                "Calling into another catalog is not currently supported"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception

        parts = []
        if sf_database:
            parts.append(sf_quote(sf_database))
        if sf_schema:
            parts.append(sf_quote(sf_schema))
        parts.append(sf_quote(table_name))
        fqn = ".".join(parts)

        session = get_or_create_snowpark_session()
        try:
            session.sql(f"DESCRIBE TABLE {fqn}").collect()
        except SnowparkSQLException as e:
            if hasattr(e, "sql_error_code") and e.sql_error_code == 2003:
                exception = AnalysisException(
                    error_class=TABLE_OR_VIEW_NOT_FOUND_ERROR_CLASS,
                    message_parameters={"relationName": spark_tableName},
                )
                attach_custom_error_code(exception, ErrorCodes.TABLE_NOT_FOUND)
                raise exception
            raise

    def isCached(self, spark_tableName: str) -> pandas.DataFrame:
        """Whether a table is cached by us locally.

        Check whether a table exists and then delegate to the local cache.
        """
        self._verify_table_exists(spark_tableName)
        return super().isCached(spark_tableName)

    def cacheTable(
        self,
        spark_tableName: str,
        storageLevel: common_proto.StorageLevel | None = None,
    ) -> pandas.DataFrame:
        """Cache a table, or view locally.

        Check whether a table exists and then delegate to the local cache.
        """
        self._verify_table_exists(spark_tableName)
        return super().cacheTable(spark_tableName, storageLevel)

    def uncacheTable(self, spark_tableName: str) -> pandas.DataFrame:
        """Uncache a table, or view locally.

        Check whether a table exists and then delegate to the local cache.
        """
        self._verify_table_exists(spark_tableName)
        return super().uncacheTable(spark_tableName)

    def refreshTable(self, spark_tableName: str) -> pandas.DataFrame:
        """Refresh a table, or view locally.

        Check whether a table exists and then delegate to the local cache.
        """
        self._verify_table_exists(spark_tableName)
        return super().refreshTable(spark_tableName)
