import duckdb
from urllib.parse import urlparse
from typing import Dict, Optional
from datetime import datetime  # noqa: TID251

from dlt.common import logger
from dlt.common.destination.typing import PreparedTableSchema
from dlt.common.storages.fsspec_filesystem import fsspec_from_config

from dlt.destinations.sql_client import raise_database_error
from dlt.destinations.impl.filesystem.sql_client import WithTableScanners
from dlt.destinations.impl.duckdb.configuration import DuckDbCredentials
from dlt.sources.credentials import (
    AwsCredentials,
    AzureCredentials,
    AzureServicePrincipalCredentials,
)

from dlthub.destinations.impl.iceberg.iceberg import PyIcebergJobClient, IcebergTable


class IcebergSqlClient(WithTableScanners):
    def __init__(
        self,
        remote_client: PyIcebergJobClient,
        dataset_name: str = None,
        cache_db: DuckDbCredentials = None,
        persist_secrets: bool = False,
    ) -> None:
        super().__init__(remote_client, dataset_name, cache_db, persist_secrets)
        self.remote_client: PyIcebergJobClient = remote_client
        self._catalog = remote_client._catalog
        self.filesystem_config = remote_client.config.filesystem
        self.use_filesystem_auth = (
            self.filesystem_config is not None
            and self.filesystem_config.credentials is not None
            and self.filesystem_config.credentials.is_resolved()
        )
        if (
            self.remote_client.config.is_aws_rest_catalog
            and self.remote_client.config.capabilities.duckdb_attach_catalog
        ):
            self.database_name = self._catalog.name

    def catalog_name(self, quote: bool = True, casefold: bool = True) -> Optional[str]:
        if not self.database_name:
            return None

        if casefold:
            database_name = self.capabilities.casefold_identifier(self.database_name)
        else:
            database_name = self.database_name
        if quote:
            database_name = self.capabilities.escape_identifier(database_name)
        return database_name

    def can_create_view(self, table_schema: PreparedTableSchema) -> bool:
        return True

    def should_replace_view(self, view_name: str, table_schema: PreparedTableSchema) -> bool:
        # always refresh abfss via filesystem config or when refresh is requested
        # TODO: better data refresh! we could compare existing metadata snapshot with the one in
        #  catalog and only replace view when it changes
        return (
            self.use_filesystem_auth
            and self.filesystem_config.protocol == "abfss"
            or self.remote_client.config.always_refresh_views
        )

    def create_views_for_tables(self, tables: Dict[str, str]) -> None:
        if (
            self.remote_client.config.is_aws_rest_catalog
            and self.remote_client.config.capabilities.duckdb_attach_catalog
        ):
            return
        super().create_views_for_tables(tables)

    @raise_database_error
    def create_view(self, view_name: str, table_schema: PreparedTableSchema) -> None:
        if (
            self.remote_client.config.is_aws_rest_catalog
            and self.remote_client.config.capabilities.duckdb_attach_catalog
        ):
            return None

        # get snapshot and io from catalog
        table_name = table_schema["name"]
        iceberg_table = self.remote_client.load_open_table("iceberg", table_name)
        # NOTE: two operations below do not need data access and are just Table props in pyiceberg
        last_metadata_file = iceberg_table.metadata_location
        table_location = iceberg_table.location()

        if not self.use_filesystem_auth:
            # TODO: vended credentials may
            #  have expiration time so it makes sense to store expiry time and do
            #  should_replace_view
            if self._register_file_io_secret(iceberg_table):
                logger.info(
                    f"Successfully registered duckdb secret for table location {table_location}"
                )
            elif self._register_filesystem_for_table(iceberg_table):
                logger.warning(
                    "Catalog vended credentials in a form that cannot be persisted as duckdb "
                    "secret. Transformation engine like dbt that connects to duckdb separately "
                    "won't be able to use this credentials. A few fixes are available:"
                    "1. define `filesystem` config field with your data location and credentials "
                    "to override catalog credentials in duckdb 2. use STS credentials vending on"
                    " s3 3. add missing FileIO credentials to "
                    "`destination.iceberg.credentials.properties` ie `s3.region=...` when s3 "
                    "region is missing. "
                    f"The requested table location was {table_location}"
                )
                logger.info(
                    "Successfully registered fsspec filesystem for table location "
                    f"{iceberg_table.location()}"
                )
            else:
                logger.warning(
                    "Pyiceberg instantiated Arrow filesystem which cannot be used with duckdb. "
                    f"The requested table location was {table_location}. "
                    "Creating views will most probably fail."
                )
        else:
            logger.info(
                "Credentials in `filesystem` configuration were used for secrets for table "
                f"location {table_location}"
            )

        if ".gz." in last_metadata_file:
            compression = ", metadata_compression_codec = 'gzip'"
        else:
            compression = ""

        from_statement = f"iceberg_scan('{last_metadata_file}'{compression}, union_by_name=true)"

        # create view
        view_name = self.make_qualified_table_name(view_name)
        columns = [
            self.escape_column_name(c) for c in self.schema.get_table_columns(table_name).keys()
        ]
        create_table_sql_base = (
            f"CREATE OR REPLACE VIEW {view_name} AS SELECT {', '.join(columns)} "
            f"FROM {from_statement}"
        )
        self._conn.execute(create_table_sql_base)

    def _register_file_io_secret(self, iceberg_table: IcebergTable) -> bool:
        """Register FileIO as duckdb secret if possible"""
        properties = iceberg_table.io.properties
        # check credential types that we can convert into duckdb secrets
        aws_credentials = AwsCredentials.from_pyiceberg_fileio_config(properties)
        if aws_credentials.is_resolved():
            if not aws_credentials.region_name:
                logger.warning(
                    "s3.region is missing in FileIO properties and credentials for the table "
                    "cannot be used directly with duckdb."
                )
                return False
            self.create_secret(
                iceberg_table.location(),
                aws_credentials,
                persist_secrets=self.persist_secrets,
            )
            return True
        azure_credentials = AzureCredentials.from_pyiceberg_fileio_config(properties)
        if azure_credentials.is_resolved():
            if not azure_credentials.azure_storage_account_key:
                logger.warning(
                    "adls.account-key is missing in FileIO properties and credentials for the "
                    "table cannot be used directly with duckdb."
                )
                return False
            self.create_secret(
                iceberg_table.location(),
                azure_credentials,
                persist_secrets=self.persist_secrets,
            )
            return True
        azure_tenant_credentials = AzureServicePrincipalCredentials.from_pyiceberg_fileio_config(
            properties
        )
        if azure_tenant_credentials.is_resolved():
            self.create_secret(
                iceberg_table.location(),
                azure_tenant_credentials,
                persist_secrets=self.persist_secrets,
            )
            return True
        # none of the gcp credentials can be converted from file io to duckdb
        return False

    def _register_filesystem_for_table(self, iceberg_table: IcebergTable) -> bool:
        """Tries to register FileIO in `iceberg_table` as fsspec filesystem in duckdb"""
        from pyiceberg.io.fsspec import FsspecFileIO

        uri = urlparse(iceberg_table.metadata.location)
        properties = iceberg_table.io.properties

        if not isinstance(iceberg_table.io, FsspecFileIO):
            # if not fsspec then try to create own instance
            fs = FsspecFileIO(properties).get_fs(uri.scheme)
            # pyiceberg does not set expiry which leads to credentials immediately invalid
            if uri.scheme in ["gs", "gcs"]:
                fs.credentials.credentials.expiry = datetime.fromtimestamp(
                    int(properties.get("gcs.oauth2.token-expires-at")) / 1000
                )
        else:
            fs = iceberg_table.io.get_fs(uri.scheme)

        self._register_filesystem(fs, uri.scheme)
        return True

    def _attach_iceberg_extension(self) -> None:
        # 1. expose AWS creds to DuckDB
        self.create_secret(
            "s3://",
            self.remote_client.config.credentials,  # type: ignore
            persist_secrets=self.persist_secrets,
        )
        # 3. attach the catalog only once
        already = self._conn.execute(
            f"SELECT COUNT(*)>0 FROM duckdb_databases() "
            f"WHERE database_name = '{self.catalog_name()}'"
        ).fetchone()[0]
        if not already:
            warehouse = self.remote_client.config.credentials.warehouse  # type: ignore
            with self.remote_client._clock_iceberg(
                f"duckdb attach catalog: {warehouse} {self.remote_client.config.catalog_type}"
            ):
                if self.remote_client.config.catalog_type == "s3tables-rest":
                    ## s3tables-rest catalog
                    self._conn.execute(
                        f"""ATTACH '{warehouse}' AS {self.catalog_name()}
                        (TYPE iceberg, ENDPOINT_TYPE s3_tables)"""
                    )
                else:
                    ## glue-rest catalog
                    self._conn.execute(
                        f"""ATTACH '{warehouse}' AS {self.catalog_name()}
                        (TYPE iceberg, ENDPOINT_TYPE glue)"""
                    )

        # 4. use catalog
        with self.remote_client._clock_iceberg(
            f"duckdb use catalog namespace: {self.fully_qualified_dataset_name()}"
        ):
            self._conn.sql(f"USE {self.fully_qualified_dataset_name()}")

    # def execute_query(self, query, *args, **kwargs):
    #     with self.remote_client._clock_iceberg(f"duckdb {query}"):
    #         return super().execute_query(query, *args, **kwargs)

    def open_connection(self) -> duckdb.DuckDBPyConnection:
        with self.credentials.conn_pool._conn_lock:
            first_connection = self.credentials.conn_pool.never_borrowed

            if (
                self.remote_client.config.is_aws_rest_catalog
                and self.remote_client.config.capabilities.duckdb_attach_catalog
            ):
                # Skips WithTableScanners open_connect - dataset creation not required for S3 Tables
                super(WithTableScanners, self).open_connection()
            else:
                super().open_connection()

        if first_connection and self.filesystem_config and self.filesystem_config.is_resolved():
            # NOTE: hopefully duckdb will implement REST catalog connection working with all
            #   main bucket. see create_view to see how we deal with vended credentials.
            #   Current best option (performance) is to pass credentials via filesystem or use STS
            if self.filesystem_config.protocol != "file":
                # create single authentication for the whole client if filesystem is specified
                # if self.filesystem_config.protocol in ["abfss"]:
                #     from packaging.version import Version
                #     if Version(duckdb.__version__) > Version("1.2.1"):
                #         logger.warning(
                #             "Iceberg scanning is broken in duckdb v. above 1.2.1. Falling back to"
                #             " fsspec which degrades performance."
                #         )
                #         self._register_filesystem(
                #             fsspec_from_config(self.filesystem_config)[0], "abfss"
                #         )

                if not self.create_secret(
                    self.filesystem_config.bucket_url,
                    self.filesystem_config.credentials,
                    persist_secrets=self.persist_secrets,
                ):
                    # native google storage implementation is not supported..
                    if self.filesystem_config.protocol in ["gs", "gcs"]:
                        logger.warning(
                            "For gs/gcs access via duckdb please use the gs/gcs s3 compatibility"
                            "layer if possible (not supported when using `iceberg` table format). "
                            "Falling back to fsspec which degrades scanning performance."
                        )
                        self._register_filesystem(
                            fsspec_from_config(self.filesystem_config)[0], "gcs"
                        )

        if (
            first_connection
            and self.remote_client.config.is_aws_rest_catalog
            and self.remote_client.config.capabilities.duckdb_attach_catalog
        ):
            self._attach_iceberg_extension()

        # provides a speed-up when parquet files are requested several times without closing the
        # connection
        self._conn.sql("SET parquet_metadata_cache=true;SET enable_http_metadata_cache=true")

        return self._conn
