import functools

from adam.commands.command import Command
from adam.commands.cql_utils import parse_cql_desc_tables, run_cql
from adam.commands.postgres.postgres_session import PostgresSession
from adam.config import Config
from adam.pod_exec_result import PodExecResult
from adam.repl_state import ReplState, RequiredState
from adam.utils import lines_to_tabular, log, log2

class PreviewTable(Command):
    COMMAND = 'preview'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(PreviewTable, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return PreviewTable.COMMAND

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        if state.device == ReplState.P:
            if not self.validate_state(state, RequiredState.PG_DATABASE):
                return state
        else:
            if not self.validate_state(state):
                return state

        if not args:
            def show_tables():
                if state.device == ReplState.P:
                    pg = PostgresSession(state.namespace, state.pg_path)
                    lines = [db["name"] for db in pg.tables() if db["schema"] == PostgresSession.default_schema()]
                    log(lines_to_tabular(lines, separator=','))
                else:
                    run_cql(state, f'describe tables', show_out=True)

            if state.in_repl:
                log2('Table is required.')
                log2()
                log2('Tables:')
                show_tables()
            else:
                log2('* Table is missing.')
                show_tables()

                Command.display_help()

            return 'command-missing'

        table = args[0]

        rows = Config().get('preview.rows', 10)
        if state.device == ReplState.P:
            PostgresSession(state.namespace, state.pg_path).run_sql(f'select * from {table} limit {rows}')
        else:
            run_cql(state, f'select * from {table} limit {rows}', show_out=True, use_single_quotes=True)

        return state

    def completion(self, state: ReplState):
        if state.device == ReplState.P:
            if tables := PreviewTable.pg_tables(state.namespace, state.pg_path):
                return {PreviewTable.COMMAND: {db["name"]: None for db in tables if db["schema"] == PostgresSession.default_schema()}}
        else:
            if state.pod:
                tables = PreviewTable.cql_tables(state)
                return {PreviewTable.COMMAND: {f'{k}.{t}': None for k, ts in tables.items() for t in ts}}

        return {}

    def help(self, _: ReplState):
        return f'{PreviewTable.COMMAND} TABLE\t preview table'

    @functools.lru_cache()
    def cql_tables(state: ReplState):
        r: PodExecResult =  run_cql(state, 'describe tables', show_out=False)
        return parse_cql_desc_tables(r.stdout)

    @functools.lru_cache()
    def pg_tables(ns: str, pg_path: str):
        pg = PostgresSession(ns, pg_path)
        if pg.db:
            return pg.tables()

        return None
