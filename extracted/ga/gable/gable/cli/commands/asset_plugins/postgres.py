import functools
from typing import Callable, List, Mapping, TypedDict, Union

import click
from gable.api.client import GableAPIClient
from gable.cli.commands.asset_plugins.baseclass import (
    AssetPluginAbstract,
    ExtractedAsset,
)
from gable.cli.helpers.data_asset import get_db_schema_contents, recap_type_to_dict
from gable.cli.helpers.emoji import EMOJI
from gable.openapi import GableSchemaField, SourceType, StructuredDataAssetResourceName

PostgresConfig = TypedDict(
    "PostgresConfig",
    {
        "host": str,
        "port": int,
        "db": str,
        "schema": str,
        "table": str | None,
        "proxy_host": str,
        "proxy_port": int,
        "proxy_db": str,
        "proxy_schema": str,
        "proxy_user": str,
        "proxy_password": str,
    },
)


class PostgresAssetPlugin(AssetPluginAbstract):
    def source_type(self) -> SourceType:
        return SourceType.postgres

    def click_options_decorator(self) -> Callable:
        def decorator(func):
            @click.option(
                "--host",
                "-h",
                type=str,
                required=True,
                help="""The host name of the production database, for example 'service-one.xxxxxxxxxxxx.us-east-1.rds.amazonaws.com'.
                Despite not needing to connect to the production database, the host is still needed to generate the unique resource 
                name for the real database tables (data assets).
                """,
            )
            @click.option(
                "--port",
                "-p",
                type=int,
                required=True,
                help="""The port of the production database. Despite not needing to connect to the production database, the port is 
                still needed to generate the unique resource name for the real database tables (data assets).
            """,
            )
            @click.option(
                "--db",
                type=str,
                required=True,
                help="""The name of the production database. Despite not needing to connect to the production database, the database 
                name is still needed to generate the unique resource name for the real database tables (data assets).
                
                Database naming convention frequently includes the environment (production/development/test/staging) in the 
                database name, so this value may not match the name of the database in the proxy database instance. If this is 
                the case, you can set the --proxy-db value to the name of the database in the proxy instance, but we'll use the 
                value of --db to generate the unique resource name for the data asset.
                
                For example, if your production database is 'prod_service_one', but your test database is 'test_service_one', 
                you would set --db to 'prod_service_one' and --proxy-db to 'test_service_one'.""",
            )
            @click.option(
                "--schema",
                "-s",
                type=str,
                required=True,
                help=f"""The schema of the production database containing the table(s) to include. Despite not needing to connect to 
                the production database, the schema is still needed to generate the unique resource name for the real database tables
                (data assets).
                
                Database naming convention frequently includes the environment (production/development/test/staging) in the 
                schema name, so this value may not match the name of the schema in the proxy database instance. If this is 
                the case, you can set the --proxy-schema value to the name of the schema in the proxy instance, but we'll use the 
                value of --schema to generate the unique resource name for the data asset.
                
                For example, if your production schema is 'production', but your test database is 'test', 
                you would set --schema to 'production' and --proxy-schema to 'test'.""",
            )
            @click.option(
                "--table",
                "--tables",
                "-t",
                type=str,
                default=None,
                required=False,
                help=f"""A comma delimited list of the table(s) to include. If no table(s) are specified, all tables within the provided schema will be included.

                Table names in the proxy database instance must match the table names in the production database instance, even if
                the database or schema names are different.""",
            )
            @click.option(
                "--proxy-host",
                "-ph",
                type=str,
                required=True,
                help=f"""The host string of the database instance that serves as the proxy for the production database. This is the 
                database that Gable will connect to when including tables in the CI/CD workflow. 
                """,
            )
            @click.option(
                "--proxy-port",
                "-pp",
                type=int,
                required=True,
                help=f"""The port of the database instance that serves as the proxy for the production database. This is the 
                database that Gable will connect to when including tables in the CI/CD workflow. 
                """,
            )
            @click.option(
                "--proxy-db",
                "-pdb",
                type=str,
                required=False,
                help="""Only needed if the name of the database in the proxy instance is different than the name of the
                production database. If not specified, the value of --db will be used to generate the unique resource name for 
                the data asset. 
                
                For example, if your production database is 'prod_service_one', but your test database is 'test_service_one', 
                you would set --db to 'prod_service_one' and --proxy-db to 'test_service_one'.
                """,
            )
            @click.option(
                "--proxy-schema",
                "-ps",
                type=str,
                required=False,
                help="""Only needed if the name of the schema in the proxy instance is different than the name of the schema in the
                production database. If not specified, the value of --schema will be used to generate the unique resource name for 
                the data asset. 
                
                For example, if your production schema is 'production', but your test database is 'test', you would set --schema to
                'production' and --proxy-schema to 'test'.
                """,
            )
            @click.option(
                "--proxy-user",
                "-pu",
                type=str,
                required=True,
                help=f"""The user that will be used to connect to the proxy database instance that serves as the proxy for the production 
                database. This is the database that Gable will connect to when including tables in the CI/CD workflow. 
                """,
            )
            @click.option(
                "--proxy-password",
                "-ppw",
                type=str,
                default=None,
                required=False,
                help=f"""If specified, the password that will be used to connect to the proxy database instance that serves as the proxy for 
                the production database. This is the database that Gable will connect to when including tables in the CI/CD workflow. 
                """,
            )
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def click_options_keys(self) -> set[str]:
        return set(PostgresConfig.__annotations__.keys())

    def pre_validation(self, config: Mapping) -> None:
        """Validation for the asset plugin's inputs before asset extraction. This is intended
        for validity checks that cannot be done with click's validation and occurs after that validation.
        Should raise a click error like UsageError or MissingParameter.
        """

    def extract_assets(
        self, client: GableAPIClient, config: Mapping
    ) -> List[ExtractedAsset]:
        """Extract assets from the source."""
        from recap.converters.postgresql import PostgresqlConverter

        tables: Union[list[str], None] = (
            [t.strip() for t in config["table"].split(",")] if config["table"] else None
        )
        proxy_db = config["proxy_db"] if config["proxy_db"] else config["db"]
        proxy_schema = (
            config["proxy_schema"] if config["proxy_schema"] else config["schema"]
        )

        try:
            from gable.cli.readers.postgres import create_postgres_connection

            connection = create_postgres_connection(
                config["proxy_user"],
                config["proxy_password"],
                proxy_db,
                config["proxy_host"],
                config["proxy_port"],
            )
        except ImportError:
            raise ImportError(
                "The psycopg2 library is not installed. Run `pip install 'gable[postgres]'` to install it."
            )
        schema_contents = get_db_schema_contents(
            self.source_type(),
            connection,
            proxy_schema,
            tables=tables,
        )
        source_name = f"{config['host']}:{config['port']}"
        extracted_assets: list[ExtractedAsset] = []
        POSTGRES_CONVERTER = PostgresqlConverter(enforce_array_dimensions=True)
        fields_by_table = {}
        for field in schema_contents:
            table_name = field["TABLE_NAME"]
            fields_by_table.setdefault(table_name, [])
            fields_by_table[table_name].append(field)
        for table_name, fields in fields_by_table.items():
            fields.sort(key=lambda x: x["ORDINAL_POSITION"])
            recap_fields = []
            for field in fields:
                schema_recap_type = POSTGRES_CONVERTER.to_recap([field]).fields.pop()
                recap_fields.append(recap_type_to_dict(schema_recap_type))

            extracted_assets.append(
                ExtractedAsset(
                    darn=StructuredDataAssetResourceName(
                        source_type=self.source_type(),
                        data_source=source_name,
                        path=f"{config['db']}.{config['schema']}.{table_name}",
                    ),
                    dataProfileMapping=None,
                    fields=[
                        GableSchemaField.parse_obj(recap_field)
                        for recap_field in recap_fields
                    ],
                )
            )
        return extracted_assets

    def checked_when_registered(self) -> bool:
        """Whether the asset plugin should be checked when registered."""
        return False
