import re

from adam.k8s_utils.cassandra_clusters import CassandraClusters
from adam.k8s_utils.cassandra_nodes import CassandraNodes
from adam.k8s_utils.secrets import Secrets
from adam.repl_state import ReplState

def run_cql(state: ReplState, cql: str, opts: list = [], show_out = False, use_single_quotes = False):
    user, pw = Secrets.get_user_pass(state.sts if state.sts else state.pod, state.namespace, secret_path='cql.secret')
    if use_single_quotes:
        command = f"cqlsh -u {user} -p {pw} {' '.join(opts)} -e '{cql}'"
    else:
        command = f'cqlsh -u {user} -p {pw} {" ".join(opts)} -e "{cql}"'

    if state.pod:
        return CassandraNodes.exec(state.pod, state.namespace, command, show_out=show_out)
    else:
        return CassandraClusters.exec(state.sts, state.namespace, command, action='cql')

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