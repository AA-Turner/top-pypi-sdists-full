import os
import boto3

from adam.commands.export.export_databases import export_db
from adam.commands.export.importer import Importer
from adam.config import Config
from adam.repl_state import ReplState
from adam.utils import GeneratorStream, bytes_generator_from_file, debug, log2, ing
from adam.utils_athena import Athena
from adam.utils_context import Context
from adam.utils_k8s.pod_files import PodFiles
from adam.utils_k8s.pods import Pods

class AthenaImporter(Importer):
    def ping():
        session = boto3.session.Session()
        credentials = session.get_credentials()

        return credentials is not None

    def prefix(self):
        return 'e'

    def import_from_csv(self,
                        state: ReplState,
                        from_session: str,
                        keyspace: str,
                        table: str,
                        target_table: str,
                        columns: str,
                        multi_tables = True,
                        create_db = False,
                        ctx: Context = Context.NULL):
        csv_file = self.csv_file(from_session, table, target_table)
        pod = state.pod
        namespace = state.namespace
        to_session = state.export_session
        database = self.db(to_session, keyspace)

        succeeded = False
        try:
            bucket = Config().get('export.bucket', 'c3.ops--qing')

            with ing(f'[{to_session}] Uploading to S3', suppress_log=multi_tables):
                bytes = PodFiles.read_file(pod, 'cassandra', namespace, csv_file)

                s3 = boto3.client('s3')
                s3.upload_fileobj(GeneratorStream(bytes), bucket, f'export/{database}/{keyspace}/{target_table}/{table}.csv')

            self.create_schema(to_session, bucket, database, keyspace, table, columns, multi_tables, create_db)

            to, _ = self.move_to_done(state, from_session, keyspace, target_table)

            succeeded = True

            return to, to_session
        finally:
            if succeeded:
                self.remove_csv(state, from_session, table, target_table, multi_tables, ctx=ctx)
                Athena.clear_cache()

                if multi_tables:
                    ctx.log2(f'[{to_session}] {keyspace}.{target_table} OK')
                else:
                    with export_db(state) as dbs:
                        dbs.sql(f'select * from {keyspace}.{target_table} limit 10', ctx=ctx)

    def import_from_local_csv(self, state: ReplState,
                        keyspace: str, table: str, csv_file: str, multi_tables = True, create_db = False):
        to_session = state.export_session
        database = self.db(to_session, keyspace)

        succeeded = False
        try:
            columns = None
            with open(csv_file, 'r') as f:
                columns = f.readline()

            bucket = Config().get('export.bucket', 'c3.ops--qing')

            with ing(f'[{to_session}] Uploading to S3', suppress_log=multi_tables):
                bytes = bytes_generator_from_file(csv_file)

                s3 = boto3.client('s3')
                s3.upload_fileobj(GeneratorStream(bytes), bucket, f'export/{database}/{keyspace}/{table}/{os.path.basename(csv_file)}')

            self.create_schema(to_session, bucket, database, keyspace, table, columns, multi_tables, create_db)

            succeeded = True

            return csv_file, to_session
        finally:
            if succeeded:
                Athena.clear_cache()

                if not multi_tables:
                    with export_db(state) as dbs:
                        dbs.sql(f'select * from {database}.{table} limit 10')

    def create_schema(self, to_session: str, bucket: str, database: str, keyspace: str, table: str, columns: list[str], multi_tables: bool, create_db = False):
        msg: str = None
        if create_db:
            msg = f"[{to_session}] Creating database {database}"
        else:
            msg = f"[{to_session}] Creating table {table}"

        with ing(msg, suppress_log=multi_tables):
            query = f'CREATE DATABASE IF NOT EXISTS {database};'
            debug(query)
            Athena.query(query, 'default')

            query = f'DROP TABLE IF EXISTS {table};'
            debug(query)
            Athena.query(query, database)

            athena_columns = ', '.join([f'{c} string' for c in columns.split(',')])
            query = f'CREATE EXTERNAL TABLE IF NOT EXISTS {table}(\n' + \
                    f'    {athena_columns})\n' + \
                        "ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'\n" + \
                        'WITH SERDEPROPERTIES (\n' + \
                        '    "separatorChar" = ",",\n' + \
                        '    "quoteChar"     = "\\"")\n' + \
                    f"LOCATION 's3://{bucket}/export/{database}/{keyspace}/{table}'\n" + \
                        'TBLPROPERTIES ("skip.header.line.count"="1");'
            debug(query)
            try:
                Athena.query(query, database)
            except Exception as e:
                log2(f'*** Failed query:\n{query}')
                raise e