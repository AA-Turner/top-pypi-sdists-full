import functools
from typing import Union

from adam.commands.postgres.postgres_databases import PostgresDatabases, pg_path
from adam.repl_state import ReplState
from adam.utils import ExecResult
from adam.utils_color import Color
from adam.utils_context import NULL
from adam.utils_k8s.pod_exec_result import PodExecResult
from adam.utils_k8s.pods import Pods
from adam.utils_log import log2, wait_log

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

    def exec(self, command: str, ctx = NULL) -> Union[PodExecResult, ReplState]:
        state = self.handler.state

        pod, container = PostgresDatabases.pod_and_container(state.namespace)
        if not pod:
            ctx.log2('Cannot locate postgres agent or ops pod.')
            return state

        r = Pods.exec(pod, container, state.namespace, command, ctx=ctx)

        if r and ctx.show_out and not ctx.debug:
            ctx.log(r.command, text_color=Color.gray)

            if r.stdout:
                ctx.log(r.stdout)
            if r.stderr:
                ctx.log2(r.stderr)

        return r

    def sql(self, args: list[str], ctx = NULL) -> ExecResult:
        state = self.handler.state

        query = args
        if isinstance(args, list):
            query = ' '.join(args)

        return PostgresDatabases.run_sql(state, query, ctx=ctx)

class PostgresExecHandler:
    def __init__(self, state: ReplState, background=False):
        self.state = state
        self.background = background

    def __enter__(self):
        return PostgresPodService(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

def postgres(state: ReplState, background=False):
    return PostgresExecHandler(state, background=background)

# alias to postgres
def ops(state: ReplState, background=False):
    return PostgresExecHandler(state, background=background)