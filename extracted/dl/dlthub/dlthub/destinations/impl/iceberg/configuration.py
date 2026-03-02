import os
import dataclasses
from typing import Any, Dict, Optional, Final, Literal, ClassVar, Type, Union

from dlt.common.configuration import configspec, resolve_type
from dlt.common.configuration.exceptions import ConfigurationValueError
from dlt.common.configuration.specs.base_configuration import (
    CredentialsConfiguration,
    BaseConfiguration,
)
from dlt.common.configuration.specs.aws_credentials import AwsCredentials
from dlt.common.destination.client import DestinationClientDwhConfiguration
from dlt.common.storages.configuration import FilesystemConfiguration
from dlt.common.typing import TSecretStrValue
from dlt.common.storages.configuration import WithLocalFiles

from dlt.sources.credentials import ConnectionStringCredentials


@dataclasses.dataclass
class MetastoreProperties:
    properties: Optional[Dict[str, Any]] = None
    """Properties passed to pyiceberg Metastore constructor"""


@configspec(init=False)
class IcebergSqlCatalogCredentials(ConnectionStringCredentials, MetastoreProperties):
    pass


@configspec(init=False)
class AwsRESTCatalogCredentials(AwsCredentials, MetastoreProperties):
    uri: str = None
    warehouse: Optional[str] = None
    # TODO: add config validation


@configspec(init=False)
class AwsGlueCatalogCredentials(AwsCredentials, MetastoreProperties):
    # TODO: add config validation
    pass


@configspec
class IcebergRESTCatalogCredentials(CredentialsConfiguration, MetastoreProperties):
    uri: str = None
    credential: Optional[TSecretStrValue] = None
    headers: Optional[Dict[str, str]] = None
    warehouse: Optional[str] = None
    """Select warehouse by name ie. on Lakekeeper"""

    # TODO: it seems that pyiceberg understand many more properties ie.
    # "token" - initial bearer token
    # "ssl" Dict - ssl bundle
    def __str__(self) -> str:
        return f"{self.uri}@{self.warehouse}" if self.warehouse else self.uri


IcebergCredentials = Union[
    IcebergSqlCatalogCredentials,
    IcebergRESTCatalogCredentials,
    AwsRESTCatalogCredentials,
    AwsGlueCatalogCredentials,
]
CatalogType = Literal["rest", "sql", "glue", "glue-rest", "s3tables-rest"]


@configspec
class CatalogCapabilities(BaseConfiguration):
    """Settings that are different for each catalog type"""

    max_identifier_length: int = 255
    """applies to destination caps, varies per catalog (255 is for sql catalog)"""

    register_new_tables: bool = False
    """Attempts to register new table before it is created if location specified in `filesystem`
       using `table_metadata_layout`
    """
    table_metadata_layout: str = "metadata"
    """Used to search for newest metadata when registering tables, requires filesystem"""

    table_location_layout: Optional[str] = None
    """Allows to override default table location when creating table in the catalog.
       You can use {dataset_name} as dataset name / namespace placeholder or {table_name}
       as table name placeholder.
       Behavior is catalog specific. Sql catalogs we tested need full location to be provided,
       REST catalogs allow to provide location as long as it belongs to location prefix
       configured in warehouse (bucket + path)
    """

    duckdb_attach_catalog: bool = False
    """Tells if catalog can be attached as Iceberg Catalog to duckdb"""


@configspec
class SqlCatalogCapabilities(CatalogCapabilities):
    register_new_tables: bool = True
    # for SQL catalog table layout must be present
    table_location_layout: str = "{dataset_name}/{table_name}"


@configspec
class AWSGlueCatalogCapabilities(CatalogCapabilities):
    register_new_tables: bool = True
    table_location_layout: str = "{dataset_name}/{table_name}"


@configspec
class AWSRESTCatalogCapabilities(CatalogCapabilities):
    duckdb_attach_catalog: bool = True
    # table_location_layout: str = "{dataset_name}/{table_name}"


@configspec
class IcebergClientConfiguration(WithLocalFiles, DestinationClientDwhConfiguration):
    catalog_name: str = "pyiceberg"

    destination_type: Final[str] = dataclasses.field(  # type: ignore
        default="iceberg", init=False, repr=False, compare=False
    )

    CATALOG_CREDENTIALS: ClassVar[Dict[CatalogType, Any]] = {
        "sql": IcebergSqlCatalogCredentials,
        "rest": IcebergRESTCatalogCredentials,
        "glue": AwsGlueCatalogCredentials,
        "glue-rest": AwsRESTCatalogCredentials,
        "s3tables-rest": AwsRESTCatalogCredentials,
    }

    CATALOG_CAPABILITIES: ClassVar[Dict[CatalogType, Any]] = {
        "sql": SqlCatalogCapabilities,
        "glue": AWSGlueCatalogCapabilities,
        "glue-rest": AWSRESTCatalogCapabilities,
        "s3tables-rest": AWSRESTCatalogCapabilities,
    }

    CATALOG_FILESYSTEM: ClassVar[Dict[CatalogType, Any]] = {
        # sql catalog requires filesystem to resolve
        "sql": FilesystemConfiguration,
        "glue": FilesystemConfiguration,
    }

    catalog_type: CatalogType = None

    # catalog: CatalogConfiguration = None
    credentials: IcebergCredentials = None
    capabilities: CatalogCapabilities = None
    filesystem: Optional[FilesystemConfiguration] = None

    # TODO: possibly extract parts of those to CatalogConfiguration so we have setting per catalog
    # TODO: implement additional properties passed to when namespace or table are created
    namespace_properties: Optional[Dict[str, Any]] = None
    table_properties: Optional[Dict[str, Any]] = None

    # TODO: store dlt table schemas and schema properties in namespaces and table properties
    # dlt.table.schema = table schema
    # dlt.schema_name = schema_name
    # dlt.schema_name (namespace)
    # dlt.schema_hash (namespace)
    store_dlt_schema: bool = False
    """Stores dlt schema in table and namespace properties"""

    iceberg_write_batch_size: int = 0
    """Number of rows per batch when writing to Iceberg tables. Default is 0, which means that
    entire table is written at once."""

    # TODO: sql client settings may be moved to OSS and we may require it to be present in
    # DestinationClientDwhConfiguration if WithTableScanners interface is implemented by sql_client
    always_refresh_views: bool = False
    """Always refresh table scanner views be setting the newest table metadata"""

    def table_location_layout(self) -> Optional[str]:
        """Verifies and computes table layout based on catalog caps. May return None if both layout
        and bucket_url are not configured. In that case the catalog is fully responsible for
        locating tables.
        """

        table_location_layout = self.capabilities.table_location_layout
        is_relative_path = (
            table_location_layout
            and FilesystemConfiguration.is_local_path(table_location_layout)
            and not os.path.isabs(table_location_layout)
        )

        if self.filesystem and self.filesystem.bucket_url:
            if is_relative_path:
                table_location_layout = self.filesystem.pathlib.join(
                    self.filesystem.bucket_url, table_location_layout
                )
            elif table_location_layout:
                if not table_location_layout.startswith(self.filesystem.bucket_url):
                    raise ConfigurationValueError(
                        f"Both filesystem bucket_url and absolute table location layout were "
                        "provided and they refer to different locations. "
                        f"{table_location_layout} does not start with {self.filesystem.bucket_url}."
                    )
            else:
                table_location_layout = self.filesystem.bucket_url

            # pyiceberg cannot deal with windows absolute urls
            if self.filesystem.is_local_filesystem and os.name == "nt":
                table_location_layout = table_location_layout.replace("file:///", "file://")
        elif is_relative_path:
            raise ConfigurationValueError(
                "You must provide absolute table_location_layout "
                "(currently: {table_location_layout}) or filesystem config in order to "
                "compute location. "
            )
        return table_location_layout

    def on_resolved(self) -> None:
        if isinstance(self.credentials, ConnectionStringCredentials) and (
            self.filesystem is None or self.filesystem.is_partial()
        ):
            if self.filesystem is None:
                fs_msg = "No filesystem configuration was provided. "
            else:
                if not self.filesystem.bucket_url:
                    fs_msg = "No location (bucket_url) was provided. "
                else:
                    fs_msg = f"Location is to {self.filesystem.bucket_url}. "
                if not self.filesystem.credentials:
                    fs_msg + "Credentials were not provided."
                else:
                    fs_msg + "Credentials were provided but they are incomplete."
            raise ConfigurationValueError(
                "SQL Catalog requires a filesystem configuration to be present. Filesystem provides"
                f" required credentials and table location. {fs_msg}"
            )
        # if sqllite catalog is used, move it to data folder (WithLocalFiles)
        if self.catalog_type == "sql":
            assert isinstance(self.credentials, ConnectionStringCredentials)
            if self.credentials.drivername.startswith("sqlite"):
                if not os.path.isabs(self.credentials.database):
                    self.credentials.database = self.make_location(
                        self.credentials.database, "%s.db"
                    )
        if self.filesystem and self.filesystem.bucket_url:
            # relocate bucket_url
            if self.filesystem.is_local_filesystem:
                orig_bucket_url = self.filesystem.original_bucket_url()
                if not os.path.isabs(orig_bucket_url):
                    # convert to native path
                    relocated_path = self.make_location(orig_bucket_url, "%s")
                    self.filesystem.bucket_url = self.filesystem.make_file_url(relocated_path)

        # validate table root layout
        self.table_location_layout()

    @resolve_type("credentials")
    def resolve_credentials_type(self) -> Type[CredentialsConfiguration]:
        # use known credentials or empty credentials for unknown protocol
        return self.CATALOG_CREDENTIALS.get(self.catalog_type) or CredentialsConfiguration

    @resolve_type("capabilities")
    def resolve_capabilities_type(self) -> Type[CatalogCapabilities]:
        # use known credentials or empty credentials for unknown protocol
        return self.CATALOG_CAPABILITIES.get(self.catalog_type) or CatalogCapabilities

    @resolve_type("filesystem")
    def resolve_filesystem_type(self) -> Type[FilesystemConfiguration]:
        # use known credentials or empty credentials for unknown protocol
        return self.CATALOG_FILESYSTEM.get(self.catalog_type) or Optional[FilesystemConfiguration]  # type: ignore[return-value]

    @property
    def catalog_props(self) -> Dict[str, Any]:
        # always make shallow copy
        return dict(self.credentials.properties or {})

    @property
    def is_aws_rest_catalog(self) -> bool:
        """True when we're talking to an S3 Tables **REST** catalog."""
        return isinstance(self.credentials, AwsRESTCatalogCredentials)
