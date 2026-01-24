from datetime import datetime
import time
import traceback

from adam.commands.command import InvalidArgumentsException
from adam.commands.cql.utils_cql import cassandra_table_names, run_cql, table_spec
from adam.commands.export.export_databases import export_db
from adam.commands.export.export_exec_result import ExportExecResult
from adam.commands.export.export_sessions import ExportSessions
from adam.commands.export.importer import Importer
from adam.commands.export.importer_athena import AthenaImporter
from adam.commands.export.importer_sqlite import SqliteImporter
from adam.commands.export.utils_export import ExportSpec, ExportTableStatus, ExportTableSpec, ImportSpec, csv_dir, fs_exec, state_with_pod, table_log_dir
from adam.config import Config
from adam.repl_session import ReplSession
from adam.repl_state import ReplState
from adam.utils import debug, log, log_to_pods, offload, parallelize, log2, ing, log_exc
from adam.utils_async_job import AsyncJobs
from adam.utils_k8s.cassandra_nodes import CassandraNodes
from adam.utils_k8s.pod_files import PodFiles

class Exporter:
    def export_tables(args: list[str], state: ReplState, export_only: bool = False, max_workers = 0) -> ExportExecResult:
        if export_only:
            log2('export-only for testing')

        spec: ExportSpec = None
        with log_exc(True):
            spec = Exporter.export_spec(' '.join(args), state)

            r = Exporter._export_tables(spec, state, max_workers=max_workers, export_state='init')
            if not r:
                return r

            return Exporter._export_tables(spec, state, export_only, max_workers, 'pending_export')

        return None

    def export_spec(spec_str: str, state: ReplState):
        spec: ExportSpec = ExportSpec.parse_specs(spec_str)

        session = state.export_session
        if session:
            if spec.importer:
                importer_from_session = Importer.importer_from_session(session)
                if spec.importer != importer_from_session:
                    if spec.importer == 'csv':
                        prefix = Importer.prefix_from_importer(spec.importer)
                        session = f'{prefix}{session[1:]}'
                    else:
                        raise Exception(f"You're currently using {importer_from_session} export database. You cannot export tables with {spec.importer} type database.")
            else:
                spec.importer = Importer.importer_from_session(session)

            if spec.importer == 'athena' and not AthenaImporter.ping():
                raise Exception('Credentials for Athena is not present.')
        else:
            if not spec.importer:
                spec.importer = Config().get('export.default-importer', 'sqlite')

            prefix = Importer.prefix_from_importer(spec.importer)
            session = f'{prefix}{datetime.now().strftime("%Y%m%d%H%M%S")[3:]}'

            if spec.importer == 'athena' and not AthenaImporter.ping():
                raise Exception('Credentials for Athena is not present.')

            if spec.importer != 'csv':
                state.export_session = session

        spec.session = session

        return spec

    def import_session(spec_str: str, state: ReplState, max_workers = 0) -> ExportExecResult:
        import_spec: ImportSpec = None
        with log_exc(True):
            import_spec = Exporter.import_spec(spec_str, state)
            tables, status_in_whole = ExportTableStatus.from_session(state.sts, state.pod, state.namespace, import_spec.session)
            if status_in_whole == 'done':
                log2(f'The session has been completely done - no more csv files are found.')
                return ExportExecResult(spec=ExportSpec(None, None, importer=import_spec.importer, tables=[]))

            spec = ExportSpec(None, None, importer=import_spec.importer, tables=[ExportTableSpec.from_status(table) for table in tables], session=import_spec.session)

            return Exporter._export_tables(spec, state, max_workers=max_workers, export_state = 'import')

        return None

    def import_local_csv_files(spec_str: str, state: ReplState, max_workers = 0) -> tuple[list[str], ExportSpec]:
        spec: ImportSpec = None
        with log_exc(True):
            spec = Exporter.import_spec(spec_str, state, files=True)
            if not spec.table_name:
                log2(f"Use 'as <database-name>.<table-name>'.")
                raise InvalidArgumentsException()

            d_t = spec.table_name.split('.')
            if len(d_t) != 2:
                log2(f'Need <database-name>.<table-name> format for target table.')
                raise InvalidArgumentsException()

            database = d_t[0]
            table = d_t[1]
            im = AthenaImporter() if spec.importer == 'athena' else SqliteImporter()

            with parallelize(spec.files, max_workers, msg='Importing|Imported {size} csv files') as exec:
                return exec.map(lambda f: im.import_from_local_csv(state, database, table, f, len(spec.files) > 1, True)), spec

        return [], None

    def import_spec(spec_str: str, state: ReplState, files = False):
        spec: ImportSpec = ImportSpec.parse_specs(spec_str, files=files)

        session = state.export_session
        if session:
            if spec.importer:
                importer = Importer.importer_from_session(state.export_session)
                if spec.importer != importer:
                    raise Exception(f"You're currently using {importer} export database. You cannot import to {spec.importer} type database.")
            else:
                spec.importer = Importer.importer_from_session(state.export_session)
                if not spec.importer:
                    spec.importer = Config().get('export.default-importer', 'sqlite')

            if spec.importer == 'athena' and not AthenaImporter.ping():
                raise Exception('Credentials for Athena is not present.')
        else:
            if not spec.importer:
                spec.importer = Importer.importer_from_session(spec.session)

            if not spec.importer or spec.importer == 'csv':
                spec.importer = Config().get('export.default-importer', 'sqlite')

            if spec.importer == 'athena' and not AthenaImporter.ping():
                raise Exception('Credentials for Athena is not present.')

            prefix = Importer.prefix_from_importer(spec.importer)
            if spec.session:
                state.export_session = f'{prefix}{spec.session[1:]}'
            else:
                state.export_session = f'{prefix}{datetime.now().strftime("%Y%m%d%H%M%S")[3:]}'

        return spec

    def _export_tables(spec: ExportSpec, state: ReplState, export_only = False, max_workers = 0, export_state = None) -> ExportExecResult:
        if not spec.keyspace:
            spec.keyspace = f'{state.namespace}_db'

        if not spec.tables:
            spec.tables = [ExportTableSpec.parse(t) for t in cassandra_table_names(state, keyspace=spec.keyspace)]

        if not max_workers:
            max_workers = Config().action_workers(f'export.{spec.importer}', 8)

        if export_state == 'init':
            CassandraNodes.exec(state.pod, state.namespace, f'rm -rf {csv_dir()}/{spec.session}_*', show_out=Config().is_debug(), shell='bash')

        job_id = None
        job_log = None
        if export_state != 'init':
            job_id = AsyncJobs.new_id()
            job_log = AsyncJobs.local_log_file(f'export {spec.specs_str}', job_id, extra={'session': spec.session})
            ReplSession().append_history(f':cat {job_log}')

        action = f'[{spec.session}] Triggering export of'
        if export_state == 'init':
            action = f'[{spec.session}] Preparing|Prepared'
        elif export_state == 'import':
            action = f'[{spec.session}] Importing|Imported'
        msg = action + ' {size} Cassandra tables'
        pod = state.pod
        with parallelize(spec.tables, max_workers, msg=msg, collect=export_state == 'init', name='exporter') as exec:
            statuses = exec.map(lambda table: Exporter.export_table(table,
                                                                state.with_pod(pod),
                                                                spec.session,
                                                                spec.importer,
                                                                export_only,
                                                                len(spec.tables) > 1,
                                                                consistency=spec.consistency,
                                                                export_state=export_state,
                                                                job_log=None if export_state == 'init' else job_log))
            return ExportExecResult(log_file=job_log, job_id=job_id, spec=spec, statuses=statuses)

    def export_table(spec: ExportTableSpec,
                     state: ReplState,
                     session: str,
                     importer: str,
                     export_only = False,
                     multi_tables = True,
                     consistency: str = None,
                     export_state=None,
                     job_log: str = None):
        status: ExportTableStatus = None

        table, target_table, columns = Exporter.resove_table_n_columns(spec, state, include_ks_in_target=False, importer=importer)

        log_file = f'{table_log_dir(state.pod, state.namespace)}/{session}_{spec.keyspace}.{target_table}.log'
        create_db = not state.export_session

        if export_state == 'init':
            Exporter.create_table_log(spec, state, session, table, target_table)
            return 'table_log_created'
        else:
            try:
                if export_state == 'pending_export':
                    Exporter.export_to_csv(spec, state, session, table, target_table, columns, multi_tables=multi_tables, consistency=consistency, job_log=job_log)

                log_files: list[str] = PodFiles.find_files(state.pod, 'cassandra', state.namespace, f'{log_file}*', remote=log_to_pods())
                if not log_files:
                    return None

                log_file = log_files[0]

                status = ExportTableStatus.from_log_file(state.pod, state.namespace, session, log_file)

                with offload(name='exporter') as exec:
                    ctx = ExportTableContext(spec, state, session, importer, export_only, multi_tables, table, target_table, columns, create_db, log_file, status, job_log)
                    exec.submit(lambda: Exporter.export_loop(ctx))
            except:
                traceback.print_exc()

            return status

    def export_loop(ctx: 'ExportTableContext'):
        try:
            while ctx.status.status != 'done':
                if ctx.status.status == 'export_in_pregress':
                    debug('Exporting to CSV is still in progess, sleeping for 1 sec...')
                    time.sleep(1)
                elif ctx.status.status == 'exported':
                    ctx.log_file = Exporter.rename_to_pending_import(ctx.spec, ctx.state, ctx.session, ctx.target_table)
                    ExportSessions.clear_export_session_cache()
                    if ctx.importer == 'csv' or ctx.export_only:
                        return 'pending_import'
                elif ctx.status.status == 'pending_import':
                    ctx.log_file, ctx.session = Exporter.import_from_csv(ctx.spec,
                                                                         ctx.state,
                                                                         ctx.session,
                                                                         ctx.importer,
                                                                         ctx.table,
                                                                         ctx.target_table,
                                                                         ctx.columns,
                                                                         multi_tables=ctx.multi_tables,
                                                                         create_db=ctx.create_db,
                                                                         job_log=ctx.f)

                ctx.status = ExportTableStatus.from_log_file(ctx.state.pod, ctx.state.namespace, ctx.session, ctx.log_file)

            return ctx.status.status
        except:
            traceback.print_exc()

    def create_table_log(spec: ExportTableSpec, state: ReplState, session: str, table: str, target_table: str):
        dir = table_log_dir(state.pod, state.namespace)
        log_file = f'{dir}/{session}_{spec.keyspace}.{target_table}.log'

        cmd = f'rm -f {log_file}* && mkdir -p {dir} && touch {log_file}'
        fs_exec(state.pod, state.namespace, cmd, show_out=Config().is_debug())

        return table

    def export_to_csv(spec: ExportTableSpec,
                      state: ReplState,
                      session: str,
                      table: str,
                      target_table: str,
                      columns: str,
                      multi_tables = True,
                      consistency: str = None,
                      job_log: str = None):
        db = f'{session}_{target_table}'

        CassandraNodes.exec(state.pod, state.namespace, f'mkdir -p {csv_dir()}/{db}', show_out=Config().is_debug(), shell='bash')
        csv_file = f'{csv_dir()}/{db}/{table}.csv'
        table_log_file = f'{table_log_dir(state.pod, state.namespace)}/{session}_{spec.keyspace}.{target_table}.log'

        suppress_ing_log = Config().is_debug() or multi_tables
        queries = []
        if consistency:
            queries.append(f'CONSISTENCY {consistency}')
        queries.append(f"COPY {spec.keyspace}.{table}({columns}) TO '{csv_file}' WITH HEADER = TRUE")

        with ing(f'[{session}] Triggering dump of table {spec.keyspace}.{table}{f" with consistency {consistency}" if consistency else ""}',
                 suppress_log=suppress_ing_log,
                 job_log = job_log):
            run_cql(state, ';'.join(queries), show_out=Config().is_debug(), backgrounded=True, log_file=table_log_file, history=False)

        return table_log_file

    def rename_to_pending_import(spec: ExportTableSpec, state: ReplState, session: str, target_table: str):
        log_file = f'{table_log_dir(state.pod, state.namespace)}/{session}_{spec.keyspace}.{target_table}.log'
        to = f'{log_file}.pending_import'

        cmd =f'mv {log_file} {to}'
        fs_exec(state.pod, state.namespace, cmd, show_out=Config().is_debug())

        return to

    def import_from_csv(spec: ExportTableSpec,
                        state: ReplState,
                        session: str,
                        importer: str,
                        table: str,
                        target_table: str,
                        columns: str,
                        multi_tables = True,
                        create_db = False,
                        job_log: str = None):
        im = AthenaImporter() if importer == 'athena' else SqliteImporter()
        return im.import_from_csv(state, session if session else state.export_session, spec.keyspace, table, target_table, columns, multi_tables, create_db, job_log=job_log)

    def resove_table_n_columns(spec: ExportTableSpec, state: ReplState, include_ks_in_target = False, importer = 'sqlite'):
        table = spec.table
        columns = spec.columns
        if not columns:
            columns = Config().get(f'export.{importer}.columns', f'<keys>')

        keyspaced_table = f'{spec.keyspace}.{spec.table}'
        if columns == '<keys>':
            columns = ','.join(table_spec(state, keyspaced_table, on_any=True).keys())
        elif columns == '<row-key>':
            columns = table_spec(state, keyspaced_table, on_any=True).row_key()
        elif columns == '*':
            columns = ','.join([c.name for c in table_spec(state, keyspaced_table, on_any=True).columns])

        if not columns:
            log2(f'ERROR: Empty columns on {table}.')
            return table, None, None

        target_table = spec.target_table if spec.target_table else table
        if not include_ks_in_target and '.' in target_table:
            target_table = target_table.split('.')[-1]

        return table, target_table, columns

class ExportTableContext:
    def __init__(self, spec: ExportTableSpec, state: ReplState, session: str, importer: str, export_only = False, multi_tables = True, table: str = None, target_table: str = None, columns: str = None, create_db = False, log_file: str = None, status: ExportTableStatus = None, f: str = None):
        self.spec = spec
        self.state = state
        self.session = session
        self.importer = importer
        self.export_only = export_only
        self.multi_tables = multi_tables
        self.table = table
        self.target_table = target_table
        self.columns = columns
        self.create_db = create_db
        self.log_file = log_file
        self.status = status
        self.f = f

class ExportService:
    def __init__(self, handler: 'ExporterHandler'):
        self.handler = handler

    def export(self, args: list[str], export_only=False) -> ExportExecResult:
        with state_with_pod(self.handler.state) as state:
            # --export-only for testing only
            r: ExportExecResult = Exporter.export_tables(args, state, export_only=export_only)
            if not r or not r.statuses:
                return r

            ExportSessions.clear_export_session_cache()

            return r

    def import_session(self, spec_str: str):
        state = self.handler.state

        r: ExportExecResult = Exporter.import_session(spec_str, state)
        if not r or not r.statuses:
            return r

        ExportSessions.clear_export_session_cache()

        log()
        with export_db(state) as dbs:
            dbs.show_database()

        return r

    def import_files(self, spec_str: str):
        state = self.handler.state

        tables, _ = Exporter.import_local_csv_files(spec_str, state)
        if tables:
            ExportSessions.clear_export_session_cache()

            log()
            with export_db(state) as dbs:
                dbs.show_database()

        return state

class ExporterHandler:
    def __init__(self, state: ReplState):
        self.state = state

    def __enter__(self):
        return ExportService(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

def export(state: ReplState):
    return ExporterHandler(state)