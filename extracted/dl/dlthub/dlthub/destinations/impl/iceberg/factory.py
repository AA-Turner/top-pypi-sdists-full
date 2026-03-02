from typing import Any, Dict, Optional, Type, TYPE_CHECKING, Union

from dlt.common.destination import DestinationCapabilitiesContext, Destination
from dlt.common.normalizers import NamingConvention

from dlthub.common.license.decorators import require_license
from dlthub.destinations.impl.iceberg.configuration import (
    CatalogType,
    IcebergClientConfiguration,
    MetastoreProperties,
    FilesystemConfiguration,
)


if TYPE_CHECKING:
    from dlthub.destinations.impl.iceberg.iceberg import PyIcebergJobClient


class iceberg(Destination[IcebergClientConfiguration, "PyIcebergJobClient"]):
    spec = IcebergClientConfiguration

    def _raw_capabilities(self) -> DestinationCapabilitiesContext:
        caps = DestinationCapabilitiesContext.generic_capabilities()
        caps.preferred_loader_file_format = "parquet"
        caps.supported_loader_file_formats = ["parquet", "reference"]
        caps.preferred_table_format = "iceberg"
        caps.supported_table_formats = ["iceberg"]
        caps.loader_file_format_selector = None
        caps.merge_strategies_selector = None
        caps.supported_merge_strategies = ["delete-insert", "upsert"]

        caps.max_identifier_length = 200
        caps.max_column_identifier_length = 200

        # note: query and string length are generic (like for parquet)
        caps.supports_ddl_transactions = True

        caps.supported_replace_strategies = ["truncate-and-insert"]
        caps.has_case_sensitive_identifiers = True
        caps.recommended_file_size = 128_000_000
        caps.supports_nested_types = True
        caps.sqlglot_dialect = "duckdb"

        return caps

    @classmethod
    def adjust_capabilities(
        cls,
        caps: DestinationCapabilitiesContext,
        config: IcebergClientConfiguration,
        naming: Optional[NamingConvention],
    ) -> DestinationCapabilitiesContext:
        # copy identifier length from the catalog
        caps.max_identifier_length = config.capabilities.max_identifier_length
        caps.max_column_identifier_length = config.capabilities.max_identifier_length

        return super().adjust_capabilities(caps, config, naming)

    @property
    def client_class(self) -> Type["PyIcebergJobClient"]:
        from dlthub.destinations.impl.iceberg.iceberg import PyIcebergJobClient

        return PyIcebergJobClient

    @require_license("dlthub.destinations.iceberg")
    def __init__(
        self,
        catalog_type: CatalogType = None,
        credentials: Union[MetastoreProperties, Dict[str, Any]] = None,
        filesystem: Union[FilesystemConfiguration, Dict[str, Any]] = None,
        destination_name: Optional[str] = None,
        environment: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            catalog_type=catalog_type,
            credentials=credentials,
            filesystem=filesystem,
            destination_name=destination_name,
            environment=environment,
            **kwargs,
        )


iceberg.register()
