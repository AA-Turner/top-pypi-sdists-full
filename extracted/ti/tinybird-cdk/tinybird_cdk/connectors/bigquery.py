from google.cloud import bigquery

from tinybird_cdk import (connector, errors, export, formats, logger, schema,
                          utils)
from tinybird_cdk.cloud import gcp, gcs
from typing import Optional
import google.api_core.exceptions


# This connector expects the standard environment variable
#
#     GOOGLE_APPLICATION_CREDENTIALS
#
# to be set to a path to the JSON file with the application credentials you can
# obtain by following the steps explained in
#
#     https://cloud.google.com/docs/authentication/getting-started
#
# The GCS bucket used for exports is taken from the standard environment
# variable GCS_BUCKET.
class Connector(connector.SQLConnector):
    def __init__(self):
        super().__init__()
        self.bigquery = bigquery.Client(credentials=gcp.credentials(), project=gcp.project_id())
        self.client = gcs.Client()

    #
    # --- Scopes ----------------------------------------------------------------------------------
    #

    def get_scopes(self):
        return (
            connector.Scope(name='Projects', value='project'),
            connector.Scope(name='Datasets', value='dataset'),
            connector.Scope(name='Tables', value='table')
        )

    def list_scope(self, parents={}):
        if 'project' in parents:
            if 'dataset' in parents:
                return self._list_tables(parents['project'], parents['dataset'])
            return self._list_datasets(parents['project'])
        return self._list_projects()

    def _list_projects(self):
        projects = []
        for project in list(self.bigquery.list_projects()):
            projects.append(connector.Scope(name=project.friendly_name, value=project.project_id))
        projects.sort(key=lambda project: project.name)
        return projects

    def _list_datasets(self, project):
        datasets = []
        for dataset in list(self.bigquery.list_datasets(project=project)):
            datasets.append(connector.Scope(name=dataset.dataset_id, value=dataset.dataset_id))
        datasets.sort(key=lambda dataset: dataset.name)
        return datasets

    def _list_tables(self, project, dataset):
        tables = []
        for table in list(self.bigquery.list_tables(dataset=f'{project}.{dataset}')):
            table_info = self.bigquery.get_table(table.reference)
            tables.append(connector.Table(
                name=table.table_id, value=table.table_id, num_rows=table_info.num_rows, size=table_info.num_bytes
            ))
        tables.sort(key=lambda table: table.name)
        return tables

    #
    # --- Schema Suggestion -----------------------------------------------------------------------
    #

    # https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.table.Table.html#google.cloud.bigquery.table.Table
    # https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.schema.SchemaField.html#google.cloud.bigquery.schema.SchemaField
    # https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#TableFieldSchema.FIELDS.mode
    def suggest_schema(self, scopes):
        if not (project := scopes.get('project')):
            raise errors.MissingConfiguration('project')
        if not (dataset := scopes.get('dataset')):
            raise errors.MissingConfiguration('dataset')
        if not (table := scopes.get('table')):
            raise errors.MissingConfiguration('table')

        suggested_schema = schema.Schema(scopes, table)
        bigquery_schema = self.bigquery.get_table(table=f'{project}.{dataset}.{table}').schema
        for field in bigquery_schema:
            suggested_schema.columns.append(self._column(field))

        return suggested_schema

    # https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#TableFieldSchema.FIELDS.type
    def _column(self, field):
        # An ARRAY<INT64> comes as a field of type 'INTEGER' and mode 'REPEATED'.
        if field.mode == 'REPEATED':
            return self._array_column(field)

        src_type = schema.Type(field.field_type, field.mode == 'NULLABLE')
        remark = None

        if field.field_type == 'STRING':
            ch_type = schema.String(null=src_type.null)
        elif field.field_type == 'BYTES':
            ch_type = schema.String(null=src_type.null)
            remark = 'Binaries get Base64-encoded'
        elif field.field_type == 'INTEGER':
            ch_type = schema.Int64(null=src_type.null)
        elif field.field_type == 'FLOAT':
            ch_type = schema.Float64(null=src_type.null)
        elif field.field_type == 'TIMESTAMP':
            ch_type = schema.DateTime64(null=src_type.null)
            remark = 'The domain range in ClickHouse is smaller'
        elif field.field_type == 'DATE':
            ch_type = schema.Date32(null=src_type.null)
            remark = 'The domain range in ClickHouse is smaller'
        elif field.field_type == 'DATETIME':
            ch_type = schema.DateTime64(null=src_type.null)
            remark = 'The domain range in ClickHouse is smaller'
        else:
            ch_type = schema.String(null=src_type.null)
            remark = 'Imported as String'

        return schema.Column(name=field.name, src_type=src_type, ch_type=ch_type, remark=remark)

    def _array_column(self, field):
        src_type = schema.Type(f'ARRAY<{field.field_type}>', False)
        remark = None

        # BigQuery does not export ARRAY to CSV. We invoke TO_JSON() on the
        # field to bypass that restriction. That allow us to send arrays of
        # numbers, but the moment you have strings, quotes break the trick.
        # Therefore, we import any other type of array as String.
        if field.field_type == 'INTEGER':
            ch_type = schema.Array(schema.Int64(False))
        elif field.field_type == 'FLOAT':
            ch_type = schema.Array(schema.Float64(False))
        else:
            ch_type = schema.String(null=False)
            remark = 'Imported as String'

        return schema.Column(name=field.name, src_type=src_type, ch_type=ch_type, remark=remark)

    #
    # --- Ingestion Query -------------------------------------------------------------------------
    #

    def ingest_query(self, schema, column_names):
        projections = []
        for column in schema.columns:
            if column.name in column_names:
                quoted = f'`{column.name}`'
                if column.ch_type.base_name == 'String':
                    if column.src_type.name == 'STRING':
                        projections.append(quoted)
                    elif column.src_type.name == 'BYTES':
                        # TO_BASE64(NULL) is NULL, what we want.
                        projections.append(f'TO_BASE64({quoted}) AS {quoted}')
                    elif column.src_type.name.startswith('ARRAY'):
                        # Arrays can be inserted as NULL, but are read back as
                        # empty arrays. We do not need to check for NULL.
                        projections.append(f'TO_JSON({quoted}, stringify_wide_numbers=>FALSE) AS {quoted}')
                    elif column.src_type.name == 'JSON':
                        projections.append(quoted)
                    elif column.src_type.name == 'RECORD':
                        projections.append(f"IF({quoted} IS NULL, NULL, TO_JSON({quoted}, stringify_wide_numbers=>FALSE)) AS {quoted}")
                    elif column.src_type.name == 'GEOGRAPHY':
                        # ST_ASTEXT(NULL) is NULL, what we want.
                        projections.append(f'ST_ASTEXT({quoted}) AS {quoted}')
                    else:
                        # CAST(NULL AS STRING) is NULL, what we want.
                        # https://cloud.google.com/bigquery/docs/reference/standard-sql/conversion_functions#cast_as_string
                        projections.append(f'CAST({quoted} AS STRING) AS {quoted}')
                elif column.ch_type.name == 'Array(Int64)':
                   # Arrays can be inserted as NULL, but are read back as empty
                   # arrays. We do not need to check for NULL.
                    projections.append(f'TO_JSON({quoted}, stringify_wide_numbers=>FALSE) AS {quoted}')
                elif column.ch_type.name == 'Array(Float64)':
                    # Arrays can be inserted as NULL, but are read back as empty
                    # arrays. We do not need to check for NULL.
                    projections.append(f'TO_JSON({quoted}) AS {quoted}')
                elif column.src_type.name == 'DATETIME':
                    projections.append(f"FORMAT_DATETIME('%Y-%m-%d %H:%M:%E3S', {quoted}) AS {quoted}")
                elif column.src_type.name == 'TIMESTAMP':
                    projections.append(f"FORMAT_TIMESTAMP('%Y-%m-%d %H:%M:%E3S%z', {quoted}) AS {quoted}")
                else:
                    projections.append(quoted)

        return 'SELECT ' + ', '.join(projections) + ' FROM ' + f"`{schema.scopes['project']}.{schema.scopes['dataset']}.{schema.scopes['table']}`"

    #
    # --- Query -----------------------------------------------------------------------------------
    #

    def _query(self, sql):
        query_job = self.bigquery.query(sql)
        return [dict(row) for row in query_job.result()]

    #
    # --- Export ----------------------------------------------------------------------------------
    #

    # https://cloud.google.com/bigquery/docs/exporting-data
    # https://cloud.google.com/bigquery/docs/reference/standard-sql/other-statements#export_data_statement
    def _export(self, query, fmt, row_limit: Optional[int]):
        if fmt != formats.CSV:
            raise errors.UnsupportedFormatError(fmt)

        bucket = gcp.gcs_bucket()

        directory = utils.random_dirname()
        if folder := gcp.gcs_folder():
            directory = folder + '/' + directory

        uri = self.client.uri(bucket, f'{directory}/*.{fmt}')
        logger.info(f'Exporting to {uri}')
        export_query = f"EXPORT DATA OPTIONS (format='CSV', uri='{uri}') AS {query}"
        if row_limit is not None:
            export_query += f" LIMIT {row_limit}"
        self._run_query(export_query)

        return export.CloudDir(self.client, bucket, directory)
    
    def _run_query(self, query: str) -> None:
        try:
            query_job = self.bigquery.query(query)
            query_job.result() # Wait for job to complete.
        except (
            google.api_core.exceptions.BadRequest,
            google.api_core.exceptions.NotFound,
            google.api_core.exceptions.Forbidden,
        ) as err:
            raise errors.ExternalDatasourceError(str(err)) from err
        # Everything else bubbles up as is to be captured as an internal error
