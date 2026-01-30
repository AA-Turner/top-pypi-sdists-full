from typing import TextIO
import pandas

from adam.commands.export.export_databases import export_db
from adam.commands.export.importer import Importer
from adam.repl_state import ReplState
from adam.utils import GeneratorStream, bytes_generator_from_file, ing, log2
from adam.utils_context import Context
from adam.utils_k8s.pod_files import PodFiles
from adam.utils_k8s.pods import Pods
from adam.utils_sqlite import SQLite, sqlite

class SqliteImporter(Importer):
    def prefix(self):
        return 's'

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

        succeeded = False
        try:
            with ing(f'[{to_session}] Uploading to Sqlite', suppress_log=multi_tables, job_log=ctx.log_file):
                # create a connection to single keyspace
                with sqlite(to_session, keyspace) as conn:
                    bytes = PodFiles.read_file(pod, 'cassandra', namespace, csv_file)
                    df = pandas.read_csv(GeneratorStream(bytes))
                    df.to_sql(target_table, conn, index=False, if_exists='replace')

            to, _ = self.move_to_done(state, from_session, keyspace, target_table)

            succeeded = True

            return to, to_session
        finally:
            if succeeded:
                self.remove_csv(state, from_session, table, target_table, multi_tables, ctx=ctx)
                SQLite.clear_cache()

                if multi_tables:
                    ctx.log2(f'[{to_session}] {keyspace}.{target_table} OK')
                else:
                    # test
                    with export_db(state) as dbs:
                        dbs.sql(f'select * from {keyspace}.{target_table} limit 10', ctx=ctx)

    def import_from_local_csv(self, state: ReplState,
                        keyspace: str, table: str, csv_file: str, multi_tables = True, create_db = False):
        to_session = state.export_session

        succeeded = False
        try:
            with ing(f'[{to_session}] Uploading to Sqlite', suppress_log=multi_tables):
                # create a connection to single keyspace
                with sqlite(to_session, keyspace) as conn:
                    bytes = bytes_generator_from_file(csv_file)
                    df = pandas.read_csv(GeneratorStream(bytes))
                    df.to_sql(table, conn, index=False, if_exists='replace')

            succeeded = True

            return csv_file, to_session
        finally:
            if succeeded:
                SQLite.clear_cache()

                if not multi_tables:
                    with export_db(state) as dbs:
                        dbs.sql(f'select * from {keyspace}.{table} limit 10')