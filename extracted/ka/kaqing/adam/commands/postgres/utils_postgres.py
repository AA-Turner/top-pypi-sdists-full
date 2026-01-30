import functools

from adam.commands.postgres.postgres_databases import PostgresDatabases, pg_path
from adam.config import Config
from adam.repl_state import ReplState
from adam.utils import ExecResult, log2, wait_log
from adam.utils_context import Context
from adam.utils_k8s.pods import Pods

TestPG = [False]

def direct_dirs(state: ReplState) -> list[str]:
    with pg_path(state) as (host, database):
        if database:
            return ['..']
        elif host:
            return ['..'] + pg_database_names(state)
        else:
            return PostgresDatabases.host_names(state.namespace)

def pg_database_names(state: ReplState):
    # cache on pg_path
    return _pg_database_names(state, state.pg_path)

@functools.lru_cache()
def _pg_database_names(state: ReplState, pg_path: str):
    if TestPG[0]:
        return ['azops88_c3ai_c3']

    wait_log('Inspecting Postgres Databases...')

    return [db['name'] for db in PostgresDatabases.databases(state, default_owner=True)]

def pg_table_names(state: ReplState):
    # cache on pg_path
    return _pg_table_names(state, state.pg_path)

@functools.lru_cache()
def _pg_table_names(state: ReplState, pg_path: str):
    if TestPG[0]:
        return ['C3_2_XYZ1']

    wait_log('Inspecting Postgres Database...')
    return [table['name'] for table in PostgresDatabases.tables(state, default_schema=True)]

class PostgresPodService:
    def __init__(self, handler: 'PostgresExecHandler'):
        self.handler = handler

    def exec(self, command: str, ctx: Context = Context.NULL):
        state = self.handler.state

        pod, container = PostgresDatabases.pod_and_container(state.namespace)
        if not pod:
            log2('Cannot locate postgres agent or ops pod.')
            return state

        r = Pods.exec(pod, container, state.namespace, command, ctx=ctx)

        if r and ctx.show_out and not ctx.debug:
            ctx.log(r.command, verbose=True)

            if r.stdout:
                ctx.log(r.stdout)
            if r.stderr:
                ctx.log2(r.stderr)

        return r

    def sql(self, args: list[str], ctx: Context = Context.NULL) -> ExecResult:
        state = self.handler.state

        query = args
        if isinstance(args, list):
            query = ' '.join(args)

        return PostgresDatabases.run_sql(state, query, ctx=ctx)

class PostgresExecHandler:
    def __init__(self, state: ReplState, backgrounded=False):
        self.state = state
        self.backgrounded = backgrounded

    def __enter__(self):
        return PostgresPodService(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

def postgres(state: ReplState, backgrounded=False):
    return PostgresExecHandler(state, backgrounded=backgrounded)