import functools
import re

from adam.utils_cassandra import cassandra_exec
from adam.utils_context import NULL
from adam.utils_k8s.secrets import Secrets
from adam.utils_k8s.pod_exec_result import PodExecResult
from adam.repl_state import ReplState
from adam.utils_log import log2, log_timing, wait_log
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
        log2('No pod is available on describe keyspaces')
        return []

    return parse_cql_desc_keyspaces(r.stdout if state.pod else r[0].stdout)

def cassandra_table_names(state: ReplState, keyspace = None):
    return [f'{k}.{t}' for k, ts in cassandra_tables(state, on_any=True).items() for t in ts if not keyspace or keyspace == '*' or k == keyspace]

@functools.lru_cache()
def cassandra_tables(state: ReplState, on_any=False) -> dict[str, list[str]]:
    r: list[PodExecResult] = run_cql(state, 'describe tables', on_any=on_any)
    if not r:
        log2('No pod is available on describe tables')
        return {}

    if isinstance(r, list):
        r = r[0]

    return parse_cql_desc_tables(r.stdout)

@functools.lru_cache()
def table_spec(state: ReplState, table: str, on_any=False) -> 'TableSpec':
    r: list[PodExecResult] = run_cql(state, f'describe table {table}', on_any=on_any)
    if not r:
        log2('No pod is available on describe table ABC')
        return None

    if isinstance(r, list):
        r = r[0]

    return parse_cql_desc_table(r.stdout)

def run_cql(state: ReplState,
            cql: str,
            opts: list = [],
            use_single_quotes = False,
            on_any = False,
            no_color = False,
            ctx = NULL) -> list[PodExecResult]:
    command = None
    with log_timing('k8s.secrets.get_user_pass'):
        user, pw = Secrets.get_user_pass(state.sts if state.sts else state.pod, state.namespace, secret_path='cql.secret')
        if no_color:
            command = f'echo "{cql}; exit" | cqlsh --no-color -u {user} -p {pw}'
        else:
            if use_single_quotes:
                command = f"cqlsh -u {user} -p {pw} {' '.join(opts)} -e '{cql}'"
            else:
                command = f'cqlsh -u {user} -p {pw} {" ".join(opts)} -e "{cql}"'

    with log_timing(cql):
        return cassandra_exec.cassandra_exec(state, state.pod, command, action='cql', on_any=on_any, ctx=ctx)

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