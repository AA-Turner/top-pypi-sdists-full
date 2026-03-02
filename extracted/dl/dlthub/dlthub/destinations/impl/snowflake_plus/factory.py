import typing as t

from dlt.common.schema.typing import TColumnSchema
from dlt.common.configuration import resolve_configuration, known_sections
from dlt.common.destination import DestinationCapabilitiesContext
from dlt.common.destination.reference import TDestinationConfig
from dlt.common.destination.typing import PreparedTableSchema
from dlt.common.exceptions import TerminalValueError
from dlt.common.destination.configuration import CsvFormatConfiguration

from dlt.destinations.impl.snowflake.factory import snowflake, SnowflakeTypeMapper
from dlt.destinations.impl.snowflake.configuration import SnowflakeCredentials
from dlthub.common.license.decorators import require_license
from dlthub.destinations.impl.snowflake_plus.configuration import SnowflakePlusClientConfiguration
from dlt.destinations.impl.filesystem.typing import TExtraPlaceholders
from dlthub.destinations.impl.snowflake_plus.configuration import IcebergMode

if t.TYPE_CHECKING:
    from dlthub.destinations.impl.snowflake_plus.snowflake_plus import SnowflakePlusClient


class SnowflakePlusTypeMapper(SnowflakeTypeMapper):
    dbt_to_sct = {
        # Snowflake
        "varchar": "text",
        "float": "double",
        "boolean": "bool",
        "date": "date",
        "timestamp_tz": "timestamp",
        "binary": "binary",
        "variant": "json",
        "time": "time",
        # Iceberg
        "double": "double",
        "timestamp": "timestamp",
        "timestamptz": "timestamp",
        "decimal": "decimal",
        "tinyint": "bigint",
        "smallint": "bigint",
        "int": "bigint",
        "long": "bigint",
        "string": "text",
    }

    sct_to_iceberg_unbound_dbt = {
        "json": "string",
        "text": "string",
        "double": "double",
        "bool": "boolean",
        "date": "date",
        "timestamp": "timestamp",
        "bigint": "bigint",
        "binary": "binary",
        "time": "string",
    }

    def to_destination_type(self, column: TColumnSchema, table: PreparedTableSchema) -> str:
        if table.get("table_format") == "iceberg":
            if column["data_type"] == "double":
                return "double"
            elif column["data_type"] == "text":
                return "string"
            elif column["data_type"] == "json":
                return "string"
            elif column["data_type"] in ("decimal", "wei"):
                precision_tup = self.precision_tuple_or_default(column["data_type"], column)
                if precision_tup:
                    return "decimal(%i,%i)" % precision_tup
                else:
                    return "decimal"
            else:
                return super().to_destination_type(column, table)
        else:
            return super().to_destination_type(column, table)

    def to_db_datetime_type(
        self,
        column: TColumnSchema,
        table: PreparedTableSchema = None,
    ) -> str:
        if table.get("table_format") == "iceberg":
            return "timestamp"
        else:
            return super().to_db_datetime_type(column, table)

    def to_db_time_type(self, column: TColumnSchema, table: PreparedTableSchema = None) -> str:
        if table.get("table_format") == "iceberg":
            return "time"
        else:
            return super().to_db_time_type(column, table)

    def to_db_integer_type(self, column: TColumnSchema, table: PreparedTableSchema = None) -> str:
        if table.get("table_format") != "iceberg":
            return super().to_db_integer_type(column, table)

        precision = column.get("precision")
        if precision is None:
            return "long"
        if precision <= 8:
            return "int"
        elif precision <= 16:
            return "int"
        elif precision <= 32:
            return "int"
        elif precision <= 64:
            return "long"
        raise TerminalValueError(
            f"bigint with {precision} bits precision cannot be mapped into an Iceberg integer type"
        )


class snowflake_plus(snowflake):
    spec = SnowflakePlusClientConfiguration

    CONFIG_SECTION = "snowflake"

    def _raw_capabilities(self) -> DestinationCapabilitiesContext:
        caps = super()._raw_capabilities()
        caps.type_mapper = SnowflakePlusTypeMapper
        return caps

    @property
    def client_class(self) -> t.Type["SnowflakePlusClient"]:
        from dlthub.destinations.impl.snowflake_plus.snowflake_plus import SnowflakePlusClient

        return SnowflakePlusClient

    @require_license("dlthub.destinations.snowflake_plus")
    def __init__(
        self,
        credentials: t.Union[SnowflakeCredentials, t.Dict[str, t.Any], str] = None,
        stage_name: t.Optional[str] = None,
        keep_staged_files: bool = True,
        csv_format: t.Optional[CsvFormatConfiguration] = None,
        query_tag: t.Optional[str] = None,
        create_indexes: bool = False,
        destination_name: t.Optional[str] = None,
        environment: t.Optional[str] = None,
        external_volume: t.Optional[str] = None,
        catalog: t.Optional[str] = None,
        base_location: t.Optional[str] = None,
        extra_placeholders: t.Optional[TExtraPlaceholders] = None,
        catalog_sync: t.Optional[str] = None,
        iceberg_mode: t.Optional[IcebergMode] = None,
        **kwargs: t.Any,
    ) -> None:
        """Configure the Snowflake Plus destination to use in a pipeline.

        All arguments provided here supersede other configuration sources such as environment
        variables and dlt config files.

        Args:
            credentials: Credentials to connect to the snowflake database. Can be an instance
                of `SnowflakeCredentials` or a connection string in the format
                `snowflake://user:password@host:port/database`
            stage_name: Name of an existing stage to use for loading data. Default uses implicit
                stage per table
            keep_staged_files: Whether to delete or keep staged files after loading
            csv_format: Optional csv format configuration
            query_tag: A tag with placeholders to tag sessions executing jobs
            create_indexes: Whether UNIQUE or PRIMARY KEY constrains should be created
            external_volume: Name of the external volume to use for Iceberg tables
            catalog: Name of the catalog to use for Iceberg tables
            base_location: Template for the base location of Iceberg tables
            extra_placeholders: Additional placeholders to use in the base_location template
            catalog_sync: Catalog sync setting for Iceberg tables
            iceberg_mode: Mode to determine which tables should be created as Iceberg tables.
                `none`: No Iceberg tables are created
                `data_tables`: Only data tables are created, dlt system tables are created
                    as Snowflake tables
                `all`: All tables are created as Iceberg tables
        """
        super().__init__(
            credentials=credentials,
            stage_name=stage_name,
            keep_staged_files=keep_staged_files,
            csv_format=csv_format,
            query_tag=query_tag,
            create_indexes=create_indexes,
            destination_name=destination_name,
            environment=environment,
            external_volume=external_volume,
            catalog=catalog,
            base_location=base_location,
            extra_placeholders=extra_placeholders,
            catalog_sync=catalog_sync,
            iceberg_mode=iceberg_mode,
            **kwargs,
        )

    def configuration(
        self, initial_config: TDestinationConfig, accept_partial: bool = False
    ) -> t.Union[TDestinationConfig, SnowflakePlusClientConfiguration]:
        config = resolve_configuration(
            initial_config or self.spec(),
            sections=(known_sections.DESTINATION, self.CONFIG_SECTION),
            explicit_value=self.config_params,
            accept_partial=accept_partial,
        )
        return config


snowflake_plus.register()
