import functools
import re

from adam.k8s_utils.cassandra_clusters import CassandraClusters
from adam.k8s_utils.cassandra_nodes import CassandraNodes
from adam.k8s_utils.secrets import Secrets
from adam.pod_exec_result import PodExecResult
from adam.repl_state import ReplState
from adam.utils import log2

@functools.lru_cache()
def keyspaces(sts: str, namespace: str):
    user, pw = Secrets.get_user_pass(sts, namespace, secret_path='cql.secret')
    command = f'cqlsh -u {user} -p {pw} -e "describe keyspaces"'

    r: list[PodExecResult] = CassandraClusters.exec(sts, namespace, command, show_out=False, action='cql', on_any=True)
    if not r:
        log2('No pod is available')
        return []

    return parse_cql_desc_keyspaces(r[0].stdout)

def run_cql(state: ReplState, cql: str, opts: list = [], show_out = False, use_single_quotes = False, on_any = False):
    user, pw = Secrets.get_user_pass(state.sts if state.sts else state.pod, state.namespace, secret_path='cql.secret')
    if use_single_quotes:
        command = f"cqlsh -u {user} -p {pw} {' '.join(opts)} -e '{cql}'"
    else:
        command = f'cqlsh -u {user} -p {pw} {" ".join(opts)} -e "{cql}"'

    if state.pod:
        return CassandraNodes.exec(state.pod, state.namespace, command, show_out=show_out)
    else:
        return CassandraClusters.exec(state.sts, state.namespace, command, show_out=show_out, action='cql', on_any=on_any)

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