from contextlib import closing
from dataclasses import dataclass
import re

import snowflake.connector

from tinybird_cdk import (cloud, config, connector, errors, export, formats, schema,
                          logger, utils)


LOGIN_TIMEOUT_IN_SECONDS = 10

# Snowflake specific classes.
# This is an abstraction leak, for Snowflake specific methods.
@dataclass(frozen=True)
class Role:
    name: str
    value: str

@dataclass(frozen=True)
class Warehouse:
    name: str
    size: str

@dataclass(frozen=True)
class Integration:
    name: str
    type: str

# The `snowql` CLI for Snowflake understands a good deal of environment
# variables:
#
#     https://docs.snowflake.com/en/user-guide/snowsql-start.html
#
# However, the Python library does not. I have created an issue for this:
#
#     https://github.com/snowflakedb/snowflake-connector-python/issues/1085
#
# Meanwhile, we support a subset of variables with the standard names.
class Connector(connector.SQLConnector):
    # The default value for MAX_FILE_SIZE in COPY INTO is 16 MB. Exports may be
    # way larger, though, like 20 GB. Better set a larger value (1 GB).
    MAX_FILE_SIZE = 1024**3
    TIMESTAMP_FORMAT_TZ = 'YYYY-MM-DD HH24:MI:SS.FF3 TZHTZM'
    TIMESTAMP_FORMAT_NTZ = 'YYYY-MM-DD HH24:MI:SS.FF3'

    # https://docs.snowflake.com/en/sql-reference/sql/copy-into-location.html#type-csv
    FILE_FORMAT_FOR_CSV = "TYPE=CSV COMPRESSION=NONE FIELD_DELIMITER=',' RECORD_DELIMITER='\\n' ESCAPE_UNENCLOSED_FIELD=NONE FIELD_OPTIONALLY_ENCLOSED_BY='\"' BINARY_FORMAT=HEX NULL_IF=()"

    def __init__(self):
        super().__init__()

    # Helper to get a property from a Snowflake `describe` resultset
    def _get_property(self, object_properties, property_name):
        property = list(filter(lambda p: p['property'] == property_name, object_properties))
        if len(property):
            return property[0]['property_value']

    # Get available roles for the provided user.
    # Tinybird needs to present the user with a list of available roles to configure the connection in the UI.
    # These two methods (get_roles, get_warehouses) are only avaiable in the Snowflake Connector, this is effectively an abstraction leak
    # as the method is not part of the generic Connector's interface, and the CDK user will become coupled to a concrete Connector implementation.
    def get_roles(self):
        roles = []
        for role in list(self._query('show grants')):
            roles.append(Role(name=role['role'], value=role['role']))
        roles.sort(key=lambda role: role.name)
        return roles
        
    # Get available warehouses for the provided user
    # Same use cases as get_roles
    def get_warehouses(self):
        warehouses = []
        for warehouse in list(self._query('show warehouses')):
            warehouses.append(Warehouse(name=warehouse['name'], size=warehouse['size']))
        warehouses.sort(key=lambda warehouse: warehouse.name)
        return warehouses

    # Get available integrations for the provided user and role
    def get_integrations(self):
        integrations = []
        for integration in list(self._query('show integrations')):
            integrations.append(Integration(name=integration['name'], type=integration['type']))
        integrations.sort(key=lambda integration: integration.name)
        return integrations

    # Create or replace Snowflake integration and stage.
    # https://docs.snowflake.com/en/sql-reference/sql/create-storage-integration
    # https://docs.snowflake.com/en/sql-reference/sql/create-stage
    #
    # The CDK needs the stage to unload data to GCS, generate signed URLs and send them to Tinybird Analytics
    # This method is intended to be called during the Connection creation flow, to ensure these resources exist
    #
    # The provided Snowflake user needs 'create stage' and 'create integration' grants:
    #     grant create stage on schema cdk.cdk_test_suite to role r_cdk_test;
    #     grant create integration on account to role r_cdk_test;
    #
    # The 'allowed_location' parameter is the GCS path, including the bucket and the workspace-scoped folder.
    # For example: gcs://tinybird-cdk-production-europe-west3/689d9d2b-633b-4900-b6cd-4a8d1d36ac3c/
    #
    # Returns the stage name, and the service account Snowflake generates for the integration. Tinybird Analytics
    # has to grant this account access to the bucket.
    def create_stage(self, allowed_location, integration_name='tinybird_integration', custom_stage_name=None):

        # Recreating a storage integration (using CREATE OR REPLACE STORAGE INTEGRATION) breaks the association
        # between the storage integration and any stage that references it.
        #
        # This is because a stage links to a storage integration using a hidden ID rather than the name of
        # the storage integration.
        #
        # Behind the scenes, the CREATE OR REPLACE syntax drops the object and recreates it with a different hidden ID.
        # https://docs.snowflake.com/en/sql-reference/sql/create-storage-integration#usage-notes
        # 
        # That's why we're only creating the integration once
        # 
        # NOTE: Commented out, since we're requiring the user to create the integration on their end.
        #
        # self._query(f'''
        #     create storage integration if not exists "{integration_name}"
        #       type = external_stage
        #       storage_provider = 'GCS'
        #       enabled = true
        #       comment = 'Tinybird Snowflake Connector Integration'
        #       storage_allowed_locations = ('{allowed_location}')
        # ''')

        # Since the integration is only created once, we need to update the STORAGE_ALLOWED_LOCATIONS property
        # and append new workspace folder if they do not exist already.
        integration = self._query(f''' describe integration "{integration_name}" ''');
        allowed_locations = self._get_property(integration, 'STORAGE_ALLOWED_LOCATIONS').split(",")
        if allowed_location not in allowed_locations:
            allowed_locations.append(allowed_location)
            self._query(f'''
                alter storage integration if exists "{integration_name}" set
                    storage_allowed_locations = ({', '.join(f'"{l}"' for l in allowed_locations)});
            ''')

        # Create one stage per workspace, since every stage must include the allowed location URL with
        # its workpace id in the path.
        #
        # Replace "-" chars for "_", so we can avoid using quotes in Snowflake resources and complicate everything
        stage_name = custom_stage_name or self.get_default_stage_name()
        self._query(f'''
            create or replace stage {stage_name}
              url='{allowed_location}'
              file_format = (type = csv compression = none )
              storage_integration = "{integration_name}";
        ''')

        account = self._get_property(integration, 'STORAGE_GCP_SERVICE_ACCOUNT')

        return { "stage": stage_name, "gcp_account": account }

    def get_integration_query(self, allowed_location, integration_name='tinybird_integration'):
        if not (role := config.get('SF_ROLE')):
            raise errors.MissingConfiguration('sf_role')

        # Remove tabs
        return re.sub(r"( )+", " ",
                      f'''create storage integration if not exists "{integration_name}"
                      \ttype = external_stage
                      \tstorage_provider = 'GCS'
                      \tenabled = true
                      \tcomment = 'Tinybird Snowflake Connector Integration'
                      \tstorage_allowed_locations = ('{allowed_location}');

                      grant create stage on all schemas in database <your_database> to role {role};

                      grant ownership on integration "{integration_name}" to role {role};''')

    def get_default_stage_name(self):
        if not (database := config.get('SF_DATABASE')):
            raise errors.MissingConfiguration('database')
        if not (schema := config.get('SF_SCHEMA')):
            raise errors.MissingConfiguration('schema')
        if not (role := config.get('SF_ROLE')):
            raise errors.MissingConfiguration('role')
        if not (workspace_id := config.get('TB_WORKSPACE_ID')):
            raise errors.MissingConfiguration('workspace_id')

        return f'{database}.{schema}.tinybird_stage__{workspace_id.replace("-", "_")}__{role}'

    #
    # --- Scopes ----------------------------------------------------------------------------------
    #

    def get_scopes(self):
        return (
            connector.Scope(name='Databases', value='database'),
            connector.Scope(name='Schemas', value='schema'),
            connector.Scope(name='Tables', value='table')
        )

    def list_scope(self, parents={}):
        if 'database' in parents:
            if 'schema' in parents:
                return self._list_tables(parents['database'], parents['schema'])
            return self._list_schemas(parents['database'])
        return self._list_databases()

    def _list_databases(self):
        databases = []
        raw_databases = list(self._query('show databases'))

        # The 'show databases' sentece includes also default databases SNOWFLAKE and SNOWFLAKE_SAMPLE_DATA.
        # Apparently, there's no way to filter out those databases from the result set. So we'll filter them manually.
        filtered_databases = list(filter(lambda d: d['name'] not in ('SNOWFLAKE', 'SNOWFLAKE_SAMPLE_DATA'), raw_databases))

        for database in filtered_databases:
            databases.append(connector.Scope(name=database['name'], value=database['name']))
        databases.sort(key=lambda database: database.name)
        return databases

    def _list_schemas(self, database):
        schemas = []
        for schema in list(self._query(f'show schemas in database {database}')):
            schemas.append(connector.Scope(name=schema['name'], value=f'{schema["database_name"]}.{schema["name"]}'))
        schemas.sort(key=lambda schema: schema.name)
        return schemas

    def _list_tables(self, database, schema):
        tables = []

        # Tables
        for table in list(self._query(f'show tables in {database}.{schema}')):
            tables.append(connector.Table(
                name=table['name'], value=f'{table["database_name"]}.{table["schema_name"]}.{table["name"]}',
                num_rows=table['rows'], size=table['bytes']
            ))

        # Views
        for view in list(self._query(f'show views in {database}.{schema}')):
            tables.append(connector.Table(
                name=view['name'], value=f'{view["database_name"]}.{view["schema_name"]}.{view["name"]}'
            ))

        tables.sort(key=lambda table: table.name)
        return tables

    #
    # --- Schema Suggestion -----------------------------------------------------------------------
    #

    def suggest_schema(self, scopes):
        if not (database := scopes.get('database')):
            raise errors.MissingConfiguration('database')
        if not (sf_schema := scopes.get('schema')):
            raise errors.MissingConfiguration('schema')
        if not (table := scopes.get('table')):
            raise errors.MissingConfiguration('table')

        suggested_schema = schema.Schema(scopes, table)
        # In Snowflake, `desc[ribe] table` works for both tables and views.
        #   https://docs.snowflake.com/en/sql-reference/sql/desc-table#usage-notes
        snowflake_schema = self._query(f'describe table {database}.{sf_schema}.{table}')
        for field in snowflake_schema:
            suggested_schema.columns.append(self._column(field))

        return suggested_schema

    # https://docs.snowflake.com/en/sql-reference/intro-summary-data-types
    def _column(self, field):
        src_type = schema.Type(field['type'], field['null?'] == 'Y')
        remark = None

        if field['type'] == 'STRING':
            ch_type = schema.String(null=src_type.null)
        elif re.match("VARCHAR\\(\\d+\\)", field['type']):
            ch_type = schema.String(null=src_type.null)
        elif re.match("NUMBER\\(\\d+,0\\)", field['type']):
            ch_type = schema.Int64(null=src_type.null)
        elif re.match("NUMBER\\(\\d+,[1-9]+\\)", field['type']):
            ch_type = schema.Float64(null=src_type.null)
        elif field['type'] == 'FLOAT':
            ch_type = schema.Float64(null=src_type.null)
        elif re.match("TIMESTAMP_NTZ\\(\\d+\\)", field['type']):
            ch_type = schema.DateTime64(null=src_type.null)
            remark = 'The domain range in ClickHouse is smaller'
        elif field['type'] == 'DATE':
            ch_type = schema.Date32(null=src_type.null)
            remark = 'The domain range in ClickHouse is smaller'
        elif field['type'] == 'DATETIME':
            ch_type = schema.DateTime64(null=src_type.null)
            remark = 'The domain range in ClickHouse is smaller'
        else:
            ch_type = schema.String(null=src_type.null)
            remark = 'Imported as String'

        return schema.Column(name=field['name'], src_type=src_type, ch_type=ch_type, remark=remark)

    #
    # --- Ingestion Query -------------------------------------------------------------------------
    #

    def ingest_query(self, schema, column_names):
        projections = []
        for column in schema.columns:
            if column.name in column_names:
                if column.ch_type.base_name == 'String':
                    # We need to apply some special functions when casting some types to string.
                    if column.src_type.name == 'VARCHAR(16777216)':
                        # String, Text and Varchar Snowflake types.
                        projections.append(f'"{column.name}"')
                    elif column.src_type.name in ('GEOGRAPHY', 'GEOMETRY'):
                        projections.append(f'ST_ASTEXT("{column.name}") AS "{column.name}"')
                    elif column.src_type.name in ('VARIANT', 'ARRAY', 'OBJECT'):
                        projections.append(f'TO_JSON("{column.name}") AS "{column.name}"')
                    else:
                        # CAST(NULL AS STRING) as a fallback, what we want.
                        # https://docs.snowflake.com/en/sql-reference/functions/cast
                        projections.append(f'CAST("{column.name}" AS STRING) AS "{column.name}"')
                else:
                    projections.append(f'"{column.name}"')
        return 'SELECT ' + ', '.join(projections) + ' FROM ' + f"{schema.scopes['database']}.{schema.scopes['schema']}.{schema.scopes['table']}"

    #
    # --- Query -----------------------------------------------------------------------------------
    #

    def _query(self, sql):
        with closing(self._connection()) as connection:
            with closing(connection.cursor(snowflake.connector.DictCursor)) as cursor:
                cursor.execute('''
                  alter session set query_tag='tinybird_query'
                ''')
                cursor.execute(sql)
                return cursor.fetchall()

    #
    # --- Export ----------------------------------------------------------------------------------
    #

    def _export(self, query, fmt, row_limit):
        if not (sf_stage := config.get('SF_STAGE')):
            raise errors.MissingConfiguration('SF_STAGE')

        if fmt != formats.CSV:
            raise errors.UnsupportedFormatError(fmt)

        with closing(self._connection()) as connection:
            logger.info('Connected to Snowflake')
            with closing(connection.cursor()) as cursor:
                # We want to make sure timestamps reflect the data and can be imported.
                # See https://docs.snowflake.com/en/sql-reference/parameters.html.
                cursor.execute('''
                  ALTER SESSION SET
                    TIMESTAMP_OUTPUT_FORMAT     = 'YYYY-MM-DD HH24:MI:SS.FF3 TZHTZM',
                    TIMESTAMP_NTZ_OUTPUT_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF3',
                    TIMESTAMP_LTZ_OUTPUT_FORMAT = NULL,
                    TIMESTAMP_TZ_OUTPUT_FORMAT  = NULL,
                    query_tag                   = 'tinybird_unload'
                ''')
                cursor.execute('SELECT GET_STAGE_LOCATION(%s)', (f'@{sf_stage}',))
                location = cursor.fetchone()[0].rstrip('/')
                directory = f'tinybird/{utils.random_dirname()}'
                logger.info(f'Unloading to {location}/{directory}/')

                # Trailing "/part" to get file names like ".../part_1_2_0.csv".
                external_stage = f'@{sf_stage}/{directory}/part'

                # https://docs.snowflake.com/en/sql-reference/sql/copy-into-location.html
                sql = f'''
                    COPY INTO {external_stage} FROM ({query})
                      FILE_FORMAT = ({self.FILE_FORMAT_FOR_CSV})
                      MAX_FILE_SIZE = {self.MAX_FILE_SIZE}'''
                logger.debug(f'Executing SQL statement\n{sql}')
                cursor.execute(sql)

        parsed_url = cloud.parse_url(location)
        client = cloud.client_for(parsed_url.service)
        if parsed_url.key:
            directory = f'{parsed_url.key}/{directory}'
        return export.CloudDir(client, parsed_url.bucket, directory)

    def _connection(self):
        try:
            return snowflake.connector.connect(
                account=config.get('SF_ACCOUNT'),
                user=config.get('SF_USER'),
                password=config.get('SF_PWD'),
                role=config.get('SF_ROLE'),
                warehouse=config.get('SF_WAREHOUSE'),
                database=config.get('SF_DATABASE'),
                schema=config.get('SF_SCHEMA'),
                login_timeout=LOGIN_TIMEOUT_IN_SECONDS
            )
        except Exception as err:
            raise errors.SnowflakeConnectionError(str(err)) from err
