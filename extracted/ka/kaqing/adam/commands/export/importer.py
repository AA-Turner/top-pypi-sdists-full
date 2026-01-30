from abc import abstractmethod

from adam.commands.export.utils_export import csv_dir, fs_exec, table_log_dir
from adam.config import Config
from adam.repl_state import ReplState
from adam.utils import ing
from adam.utils_context import Context

class Importer:
    @abstractmethod
    def prefix(self):
        pass

    @abstractmethod
    def import_from_csv(self, state: ReplState, from_session: str, keyspace: str, table: str, target_table: str, columns: str, multi_tables = True, create_db = False, log_file: str = None):
        pass

    @abstractmethod
    def import_from_local_csv(self,
                              state: ReplState,
                              keyspace: str,
                              table: str,
                              target_table: str,
                              columns: str,
                              csv_file: str,
                              multi_tables = True,
                              create_db = False):
        pass

    def move_to_done(self, state: ReplState, from_session: str, keyspace: str, target_table: str, ctx: Context = Context.NULL):
        dir = table_log_dir(state.pod, state.namespace)
        to_session = state.export_session
        log_file = f'{dir}/{from_session}_{keyspace}.{target_table}.log.pending_import'

        to = f'{dir}/{to_session}_{keyspace}.{target_table}.log.done'

        cmd = f'mv {log_file} {to}'
        fs_exec(state.pod, state.namespace, cmd, ctx=ctx)

        return to, to_session

    def prefix_adjusted_session(self, session: str):
        if not session.startswith(self.prefix()):
            return f'{self.prefix()}{session[1:]}'

        return session

    def remove_csv(self, state: ReplState, from_session: str, table: str, target_table: str, multi_tables = True, ctx: Context = Context.NULL):
        with ing(f'[{from_session}] Cleaning up temporary files', suppress_log=multi_tables, job_log=ctx.log_file):
            cmd = f'rm -rf {self.csv_file(from_session, table, target_table)}'
            fs_exec(state.pod, state.namespace, cmd, ctx=ctx)

    def db(self, session: str, keyspace: str):
        return f'{session}_{keyspace}'

    def csv_file(self, session: str, table: str, target_table: str):
        return f'{csv_dir()}/{session}_{target_table}/{table}.csv'

    def prefix_from_importer(importer: str = ''):
        if not importer:
            return ''

        prefix = 's'

        if importer == 'athena':
            prefix = 'e'
        elif importer == 'csv':
            prefix = 'c'

        return prefix

    def importer_from_session(session: str):
        if not session:
            return None

        importer = 'csv'

        if session.startswith('s'):
            importer = 'sqlite'
        elif session.startswith('e'):
            importer = 'athena'

        return importer