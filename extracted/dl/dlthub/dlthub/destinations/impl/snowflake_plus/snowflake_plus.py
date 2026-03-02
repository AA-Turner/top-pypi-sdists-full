from typing import Sequence, List, cast, Dict, Any

from dlt.common.schema import TColumnSchema
from dlt.common.destination.client import PreparedTableSchema
from dlt.destinations.impl.snowflake.snowflake import SnowflakeClient
from dlt.destinations.exceptions import InvalidPlaceholderCallback

from dlthub.destinations.impl.snowflake_plus.configuration import SnowflakePlusClientConfiguration
from dlthub.destinations.impl.snowflake_plus.exceptions import MissingPlaceholderException


class SnowflakePlusClient(SnowflakeClient):
    def prepare_load_table(self, table_name: str) -> PreparedTableSchema:
        load_table = super().prepare_load_table(table_name)
        config = cast(SnowflakePlusClientConfiguration, self.config)
        if config.iceberg_mode == "all" or (
            config.iceberg_mode == "data_tables" and table_name not in self.schema.dlt_table_names()
        ):
            load_table["table_format"] = "iceberg"
        return load_table

    def _is_iceberg_table(self, table: PreparedTableSchema) -> bool:
        return table.get("table_format") == "iceberg"

    def _make_create_table(self, qualified_name: str, table: PreparedTableSchema) -> str:
        if not self._is_iceberg_table(table):
            return super()._make_create_table(qualified_name, table)

        not_exists_clause = " "
        if (
            table["name"] in self.schema.dlt_table_names()
            and self.capabilities.supports_create_table_if_not_exists
        ):
            not_exists_clause = " IF NOT EXISTS "
        return f"CREATE ICEBERG TABLE{not_exists_clause}{qualified_name}"

    def _format_base_location(
        self,
        base_location_template: str,
        dataset_name: str,
        table_name: str,
        extra_placeholders: Dict[str, Any] = None,
    ) -> str:
        format_kwargs = {
            "dataset_name": dataset_name,
            "table_name": table_name,
        }
        if extra_placeholders:
            for key, value in extra_placeholders.items():
                if callable(value):
                    try:
                        format_kwargs[key] = value(dataset_name, table_name)
                    except TypeError as exc:
                        raise InvalidPlaceholderCallback(key) from exc
                else:
                    format_kwargs[key] = value

        try:
            return base_location_template.format(**format_kwargs)
        except KeyError as exc:
            missing_placeholder = exc.args[0]
            raise MissingPlaceholderException(missing_placeholder, base_location_template) from exc

    def _get_table_update_sql(
        self,
        table_name: str,
        new_columns: Sequence[TColumnSchema],
        generate_alter: bool,
        separate_alters: bool = False,
    ) -> List[str]:
        table = self.prepare_load_table(table_name)

        if not self._is_iceberg_table(table):
            return super()._get_table_update_sql(table_name, new_columns, generate_alter)

        if not generate_alter:
            sql = super()._get_table_update_sql(table_name, new_columns, generate_alter)

            config = cast(SnowflakePlusClientConfiguration, self.config)

            iceberg_sql = []
            iceberg_sql.append(f"CATALOG = '{config.catalog}'")
            iceberg_sql.append(f"EXTERNAL_VOLUME = '{config.external_volume}'")

            if config.base_location is not None:
                base_location = self._format_base_location(
                    config.base_location,
                    dataset_name=self.sql_client.dataset_name,
                    table_name=table_name,
                    extra_placeholders=config.extra_placeholders,
                )
                iceberg_sql.append(f"BASE_LOCATION = '{base_location}'")

            if config.catalog_sync:
                iceberg_sql.append(f"CATALOG_SYNC = '{config.catalog_sync}'")

            sql[0] = sql[0] + "\n" + "\n".join(iceberg_sql)
        else:
            sql = []
            qualified_name = self.sql_client.make_qualified_table_name(table_name)
            add_column_statements = self._make_add_column_sql(new_columns, table)
            column_sql = ",\n".join(add_column_statements)
            sql.append(f"ALTER ICEBERG TABLE {qualified_name}\n {column_sql}")
            constraints_sql = self._get_constraints_sql(table_name, new_columns, generate_alter)
            if constraints_sql:
                sql.append(constraints_sql)

        return sql
