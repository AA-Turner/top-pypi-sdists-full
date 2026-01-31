import functools
import re
from typing import Union

from adam.commands.command import Command
from adam.commands.commands_utils import show_table
from adam.utils_context import Context
from adam.utils_k8s.cassandra_clusters import CassandraClusters
from adam.utils_k8s.cassandra_nodes import CassandraNodes
from adam.utils_k8s.secrets import Secrets
from adam.utils_k8s.pod_exec_result import PodExecResult
from adam.repl_state import ReplState
from adam.utils import log2, log_timing, offload, wait_log
from adam.utils_k8s.statefulsets import StatefulSets

def cd_dirs(state: ReplState) -> list[str]:
    if state.pod:
        return [".."]
    elif state.sts:
        return [".."] + StatefulSets.pod_names(state.sts, state.namespace)
    else:
        return StatefulSets.list_sts_names()

@functools.lru_cache()
def cassandra_keyspaces(state: ReplState, on_any=True):
    if state.pod:
        wait_log(f'Inspecting Cassandra Keyspaces on {state.pod}...')
    else:
        wait_log(f'Inspecting Cassandra Keyspaces...')

    r: list[PodExecResult] = run_cql(state, 'describe keyspaces', on_any=on_any)
    if not r:
        log2('No pod is available')
        return []

    return parse_cql_desc_keyspaces(r.stdout if state.pod else r[0].stdout)

def cassandra_table_names(state: ReplState, keyspace = None):
    return [f'{k}.{t}' for k, ts in cassandra_tables(state, on_any=True).items() for t in ts if not keyspace or keyspace == '*' or k == keyspace]

@functools.lru_cache()
def cassandra_tables(state: ReplState, on_any=False) -> dict[str, list[str]]:
    r: list[PodExecResult] = run_cql(state, 'describe tables', on_any=on_any)
    if not r:
        log2('No pod is available')
        return {}

    if isinstance(r, list):
        r = r[0]

    return parse_cql_desc_tables(r.stdout)

@functools.lru_cache()
def table_spec(state: ReplState, table: str, on_any=False) -> 'TableSpec':
    r: list[PodExecResult] = run_cql(state, f'describe table {table}', on_any=on_any)
    if not r:
        log2('No pod is available')
        return None

    if isinstance(r, list):
        r = r[0]

    return parse_cql_desc_table(r.stdout)

def run_cql(state: ReplState,
            cql: str,
            opts: list = [],
            use_single_quotes = False,
            on_any = False,
            ctx: Context = Context.NULL) -> list[PodExecResult]:
    # ctx.log2(cql) alter tables double outs

    command = None
    with log_timing('Secrets.get_user_pass'):
        user, pw = Secrets.get_user_pass(state.sts if state.sts else state.pod, state.namespace, secret_path='cql.secret')
        if use_single_quotes:
            command = f"cqlsh -u {user} -p {pw} {' '.join(opts)} -e '{cql}'"
        else:
            command = f'cqlsh -u {user} -p {pw} {" ".join(opts)} -e "{cql}"'

    with log_timing(cql):
        with cassandra(state) as pods:
            # return pods.exec(command, action='cql', on_any=on_any, ctx=ctx.copy(text_color='gray' if not ctx or ctx.background else None))
            return pods.exec(command, action='cql', on_any=on_any, ctx=ctx)

def parse_cql_desc_tables(out: str):
    # Keyspace data_endpoint_auth
    # ---------------------------
    # "token"

    # Keyspace reaper_db
    # ------------------
    # repair_run                     schema_migration
    # repair_run_by_cluster          schema_migration_leader

    # Keyspace system
    tables_by_keyspace: dict[str, list[str]] = {}
    keyspace = None
    state = 's0'
    for line in out.split('\n'):
        if state == 's0':
            groups = re.match(r'^Keyspace (.*)$', line)
            if groups:
                keyspace = groups[1].strip(' \r')
                state = 's1'
        elif state == 's1':
            if line.startswith('---'):
                state = 's2'
        elif state == 's2':
            if not line.strip(' \r'):
                state = 's0'
            else:
                for table in line.split(' '):
                    if t := table.strip(' \r'):
                        if not keyspace in tables_by_keyspace:
                            tables_by_keyspace[keyspace] = []
                        tables_by_keyspace[keyspace].append(t)

    return tables_by_keyspace

def parse_cql_desc_keyspaces(out: str) -> list[str]:
    #
    # Warning: Cannot create directory at `/home/cassandra/.cassandra`. Command history will not be saved. Please check what was the environment property CQL_HISTORY set to.
    #
    #
    # Warning: Using a password on the command line interface can be insecure.
    # Recommendation: use the credentials file to securely provide the password.
    #
    #
    # azops88_db  system_auth         system_traces
    # reaper_db   system_distributed  system_views
    # system      system_schema       system_virtual_schema
    #
    kses = []
    for line in out.split('\n'):
        line = line.strip(' \r')
        if not line:
            continue
        if line.startswith('Warning:'):
            continue
        if line.startswith('Recommendation:'):
            continue

        for ks in line.split(' '):
            if s := ks.strip(' \r\t'):
                kses.append(s)

    return kses

class ColumnSpec:
    def __init__(self, name: str, type: str, key_index = -1):
        self.name = name
        self.type = type
        self.key_index = key_index

    def __eq__(self, other):
        if not isinstance(other, ColumnSpec):
            return NotImplemented

        return self.name == other.name and self.type == other.type and self.key_index == other.key_index

class TableSpec:
    def __init__(self, columns: list[ColumnSpec]):
        self.columns = columns

    def row_key(self):
        for c in self.columns:
            if c.key_index == 0:
                return c.name

    def keys(self):
        return [c.name for c in self.columns if c.key_index > -1]

def parse_cql_desc_table(out: str) -> TableSpec:
    # CREATE TABLE azops88_db.analyticscontainer_dfeevalhistory (
    #     id text,
    #     columnname text,
    #     version bigint static,
    #     contentb blob,
    #     contentbool boolean,
    #     contentn double,
    #     contents text,
    #     PRIMARY KEY (id, columnname)
    # ) WITH CLUSTERING ORDER BY (columnname ASC)
    #     AND additional_write_policy = '99p'
    #     AND bloom_filter_fp_chance = 0.1
    #     AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
    #     AND cdc = false
    #     AND comment = ''
    #     AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
    #     AND compression = {'chunk_length_in_kb': '16', 'class': 'org.apache.cassandra.io.compress.SnappyCompressor'}
    #     AND memtable = 'default'
    #     AND crc_check_chance = 1.0
    #     AND default_time_to_live = 0
    #     AND extensions = {}
    #     AND gc_grace_seconds = 3600
    #     AND max_index_interval = 2048
    #     AND memtable_flush_period_in_ms = 0
    #     AND min_index_interval = 128
    #     AND read_repair = 'BLOCKING'
    #     AND speculative_retry = '99p';
    pkeys = {}
    columns: list[ColumnSpec] = []

    state = 's0'
    for line in out.split('\n'):
        if state == 's0':
            if line.startswith('CREATE TABLE'):
                state = 's1'
        elif state == 's1':
            if line.startswith(')'):
                state = 's2'
                continue

            groups = re.match(r'^\s*PRIMARY KEY\s*\((.*)\).*$', line)
            if groups:
                pkeys = {n.strip(' '): i for i, n in enumerate(groups[1].strip(' \r').split(','))}
                continue

            #  single key column - name text PRIMARY KEY,
            groups = re.match(r'^\s*(\S*?)\s*(\S*?)\s*PRIMARY KEY,.*$', line)
            if groups:
                columns.append(ColumnSpec(groups[1], groups[2]))
                pkeys[groups[1]] = 0
            else:
                groups = re.match(r'^\s*(\S*?)\s*(\S*?),.*$', line)
                if groups:
                    columns.append(ColumnSpec(groups[1], groups[2]))
        elif state == 's2':
            pass

    for column in columns:
        if column.name in pkeys.keys():
            column.key_index = pkeys[column.name]

    return TableSpec(columns)

class CassandraPodService:
    def __init__(self, handler: 'CassandraExecHandler'):
        self.handler = handler

    def exec(self,
             command: str,
             action='bash',
             on_any = False,
             throw_err = False,
             shell = '/bin/sh',
             ctx: Context = Context.NULL) -> Union[PodExecResult, list[PodExecResult]]:
        state = self.handler.state
        pod = self.handler.pod

        if pod:
            return CassandraNodes.exec(pod,
                                       state.namespace,
                                       command,
                                       throw_err=throw_err,
                                       shell=shell,
                                       ctx=ctx)
        elif state.sts:
            return CassandraClusters.exec(state.sts,
                                          state.namespace,
                                          command,
                                          action=action,
                                          on_any=on_any,
                                          shell=shell,
                                          ctx=ctx)

        return []

    def cql(self, args: list[str], opts: list = [], use_single_quotes = False, on_any = False, ctx: Context = Context.NULL):
        state = self.handler.state
        query: str = args

        if isinstance(query, list):
            opts = []
            cqls = []
            for arg in args:
                if arg.startswith('--'):
                    opts.append(arg)
                elif arg != '-e':
                    cqls.append(arg)
            if not cqls:
                if self.state.in_repl:
                    log2('Please enter cql statement. e.g. select host_id from system.local')
                else:
                    log2('* CQL statement is missing.')
                    log2()
                    Command.display_help()

                return 'no-cql'

            query = ' '.join(cqls)
            # ctx = ctx.copy(show_out=True)

        return run_cql(state, query, opts=opts, use_single_quotes=use_single_quotes, on_any=on_any, ctx=ctx)

    def display_table(self, cols: str, header: str, ctx: Context = Context.NULL):
        if ctx.background:
            with offload(name='display-table') as exec:
                exec.submit(lambda: self._display_table(cols, header, ctx=ctx))
        else:
            self._display_table(cols, header, ctx=ctx)

    def _display_table(self, cols: str, header: str, ctx: Context = Context.NULL):
        state = self.handler.state

        if state.pod:
            show_table(state, [state.pod], cols, header, ctx)
        elif state.sts:
            pod_names = [pod.metadata.name for pod in StatefulSets.pods(state.sts, state.namespace)]
            show_table(state, pod_names, cols, header, ctx)

    def nodetool(self, args: str, status = False, ctx: Context = Context.NULL) -> Union[PodExecResult, list[PodExecResult]]:
        state = self.handler.state
        pod = self.handler.pod

        user, pw = state.user_pass()
        command = f"nodetool -u {user} -pw {pw} {args}"

        if pod:
            return CassandraNodes.exec(pod, state.namespace, command, ctx=ctx)
        else:
            return CassandraClusters.exec(state.sts, state.namespace, command, action='nodetool.status' if status else 'nodetool', ctx=ctx)

class CassandraExecHandler:
    def __init__(self, state: ReplState, pod: str = None):
        self.state = state
        self.pod = pod
        if not pod and state.pod:
            self.pod = state.pod

    def __enter__(self):
        return CassandraPodService(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

def cassandra(state: ReplState, pod: str=None):
    return CassandraExecHandler(state, pod=pod)
