from typing import Optional, Literal

from dlt.common.configuration import configspec
from dlt.destinations.impl.filesystem.typing import TExtraPlaceholders
from dlt.destinations.impl.snowflake.configuration import SnowflakeClientConfiguration

DEFAULT_BASE_LOCATION_TEMPLATE = "{dataset_name}/{table_name}"


IcebergMode = Literal["none", "data_tables", "all"]


@configspec
class SnowflakePlusClientConfiguration(SnowflakeClientConfiguration):
    external_volume: str = None
    catalog: str = "SNOWFLAKE"
    base_location: Optional[str] = DEFAULT_BASE_LOCATION_TEMPLATE
    extra_placeholders: Optional[TExtraPlaceholders] = None
    catalog_sync: Optional[str] = None
    iceberg_mode: Optional[IcebergMode] = "none"
