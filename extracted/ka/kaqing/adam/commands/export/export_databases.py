import os
import boto3

from adam.commands.export.export_sessions import ExportSessions
from adam.commands.export.importer import Importer
from adam.config import Config
from adam.repl_state import ReplState
from adam.utils import debug, log_timing, ing, log_exc
from adam.utils_tabulize import tabulize
from adam.utils_athena import Athena
from adam.utils_context import Context
from adam.utils_sqlite import SQLite

LIKE = 'e%_%'

class ExportDatabases:
    def run_query(query: str, database: str, ctx: Context = Context.NULL) -> int:
        cnt: int = 0

        ctx.log2(query)

        # log_file = None
        if database.startswith('s'):
            cnt0 = SQLite.run_query(query, database=database, ctx=ctx)
            cnt += cnt0
        else:
            cnt0 = Athena.run_query(query, database=database, ctx=ctx)
            cnt += cnt0

        return cnt

    def sessions_from_dbs(dbs: list[str]):

        sessions = set()

        for db in dbs:
            sessions.add(db.split('_')[0])

        return list(sessions)

    def drop_export_dbs(db: str = None):
        dbs: list[str] = []

        if not db or db.startswith('s'):
            dbs.extend(ExportDatabases.drop_sqlite_dbs(db))
        if not db or db.startswith('e'):
            dbs.extend(ExportDatabases.drop_athena_dbs(db))

        return dbs

    def drop_sqlite_dbs(db: str = None):
        dbs = SQLite.database_names(db)
        if dbs:
            with ing(f'Droping {len(dbs)} SQLite databases'):
                with log_exc():
                    for db in dbs:
                        file_path = f'{SQLite.local_db_dir()}/{db}'
                        try:
                            os.remove(file_path)
                        except OSError as e:
                            pass

        return dbs

    def drop_athena_dbs(db: str = None):
        dbs = Athena.database_names(f'{db}_%' if db else LIKE)
        if dbs:
            with ing(f'Droping {len(dbs)} Athena databases'):
                for db in dbs:
                    query = f'DROP DATABASE {db} CASCADE'
                    debug(query)
                    Athena.query(query)

        with ing(f'Deleting s3 folder: export'):
            with log_exc():
                if not db:
                    db = ''

                s3 = boto3.resource('s3')
                bucket = s3.Bucket(Config().get('export.bucket', 'c3.ops--qing'))
                bucket.objects.filter(Prefix=f'export/{db}').delete()

        return dbs

    def show_database(database: str, ctx: Context = Context.NULL):
        if not database:
            return

        ExportDatabases.clear_cache()

        keyspaces = {}
        for table in ExportDatabases.table_names(database):
            keyspace = table.split('.')[0]
            if keyspace in keyspaces:
                keyspaces[keyspace] += 1
            else:
                keyspaces[keyspace] = 1

        tabulize(keyspaces.items(),
                 lambda a: f'{a[0]},{a[1]}',
                 header='SCHEMA,# of TABLES',
                 separator=',',
                 ctx=ctx.copy(show_out=True))

    def database_names():
        return ExportDatabases.copy_database_names() + ExportDatabases.export_database_names()

    def copy_database_names():
        return list({n.split('_')[0] for n in SQLite.database_names()})

    def export_database_names():
        with log_timing('ExportDatabases.Athena.database_names'):
            return list({n.split('_')[0] for n in Athena.database_names(LIKE)})

    def database_names_with_keyspace_cnt(importer: str = None):
        r = {}

        names = []
        if not importer:
            names = SQLite.database_names() + Athena.database_names(LIKE)
        elif importer == 'athena':
            names = Athena.database_names(LIKE)
        else:
            names = SQLite.database_names()

        for n in names:
            tokens = n.split('_')
            name = tokens[0]
            keyspace = None
            if len(tokens) > 1:
                keyspace = tokens[1].replace('.db', '')

            if keyspace == 'root':
                continue

            if name in r:
                r[name] += 1
            else:
                r[name] = 1

        return r

    def table_names(session: str):
        tables = []

        for session in ExportDatabases._session_database_names(session):
            if session.startswith('s'):
                for table in SQLite.table_names(database=session):
                    tables.append(f'{SQLite.keyspace(session)}.{table}')
            else:
                for table in Athena.table_names(database=session, function='export'):
                    tables.append(f'{session}.{table}')

        return tables

    def _session_database_names(db: str):
        eprefix = db
        if '_' in db:
            eprefix = db.split('_')[0]

        if db.startswith('s'):
            return SQLite.database_names(prefix=f'{eprefix}_')
        else:
            return Athena.database_names(like=f'{eprefix}_%')

    def drop_databases(sts: str, pod: str, namespace: str, database: str = None):
        importer = None
        if database:
            importer = Importer.importer_from_session(database)

        sessions_done = ExportSessions.export_session_names(sts, pod, namespace, importer=importer, export_state='done')
        sessions = ExportDatabases.sessions_from_dbs(ExportDatabases.drop_export_dbs(database))
        if sessions_done and sessions:
            intersects = list(set(sessions_done) & set(sessions))
            with ing(f'Cleaning up {len(intersects)} completed sessions'):
                ExportSessions.clean_up_sessions(sts, pod, namespace, list(intersects))
                ExportSessions.clear_export_session_cache()

    def clear_cache(database: str = None):
        if not database or database.startswith('s'):
            SQLite.clear_cache()
        if not database or database.startswith('e'):
            Athena.clear_cache()

    def show_databases(importer: str = None, ctx: Context = Context.NULL):
        lines = [f'{k}\t{v}' for k, v in ExportDatabases.database_names_with_keyspace_cnt(importer).items()]
        tabulize(lines,
                 header='NAME\tKEYSPACES',
                 separator='\t',
                 ctx=ctx.copy(show_out=True))

class ExportDatabaseService:
    def __init__(self, handler: 'ExportDatabaseHandler'):
        self.handler = handler

    def sql(self, query: str, database: str = None, ctx: Context = Context.NULL):
        if not database:
            database = self.handler.state.export_session

        ExportDatabases.run_query(query, database, ctx=ctx)

    def drop(self, database: str):
        state = self.handler.state

        ExportDatabases.drop_databases(state.sts, state.pod, state.namespace, database)
        ExportDatabases.clear_cache(database)
        if state.export_session == database:
            state.export_session = None

    def drop_all(self):
        state = self.handler.state

        ExportDatabases.drop_databases(state.sts, state.pod, state.namespace)
        ExportDatabases.clear_cache()

        state.export_session = None

    def show_databases(self, importer: str = None, ctx: Context = Context.NULL):
        ExportDatabases.show_databases(importer, ctx=ctx)

    def show_database(self, database: str = None, ctx: Context = Context.NULL):
        if not database:
            database = self.handler.state.export_session

        ExportDatabases.show_database(database, ctx=ctx)

class ExportDatabaseHandler:
    def __init__(self, state: ReplState = None):
        self.state = state

    def __enter__(self):
        return ExportDatabaseService(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

def export_db(state: ReplState = None):
    return ExportDatabaseHandler(state)