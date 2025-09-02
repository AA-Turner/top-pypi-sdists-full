import copy
from enum import Enum

from adam.commands.postgres.postgres_session import PostgresSession
from adam.k8s_utils.cassandra_clusters import CassandraClusters
from adam.k8s_utils.cassandra_nodes import CassandraNodes
from adam.k8s_utils.kube_context import KubeContext
from adam.k8s_utils.secrets import Secrets
from adam.utils import display_help, log2, random_alphanumeric

class BashSession:
    def __init__(self, device: str = None):
        self.session_id = random_alphanumeric(6)
        self.device = device

    def pwd(self, state: 'ReplState'):
        command = f'cat /tmp/.qing-{self.session_id}'

        if state.pod:
            rs = [CassandraNodes.exec(state.pod, state.namespace, command, show_out=False)]
        elif state.sts:
            rs = CassandraClusters.exec(state.sts, state.namespace, command, action='bash', show_out=False)

        dir = None
        for r in rs:
            if r.exit_code(): # if fails to read the session file, ignore
                continue

            dir0 = r.stdout.strip(' \r\n')
            if dir:
                if dir != dir0:
                    log2('Inconsitent working dir found across multiple pods.')
                    return None
            else:
                dir = dir0

        return dir

class RequiredState(Enum):
    CLUSTER = 'cluster'
    POD = 'pod'
    CLUSTER_OR_POD = 'cluster_or_pod'
    NAMESPACE = 'namespace'
    PG_DATABASE = 'pg_database'
    APP_APP = 'app_app'

class ReplState:
    A = 'a'
    C = 'c'
    P = 'p'

    def __init__(self, device: str = None,
                 sts: str = None, pod: str = None, namespace: str = None, ns_sts: str = None,
                 pg_path: str = None,
                 app_env: str = None, app_app: str = None,
                 in_repl = False, bash_session: BashSession = None, remote_dir = None):
        self.namespace = KubeContext.in_cluster_namespace()

        self.device = device
        self.sts = sts
        self.pod = pod
        self.pg_path = pg_path
        self.app_env = app_env
        self.app_app = app_app
        if namespace:
            self.namespace = namespace
        self.in_repl = in_repl
        self.bash_session = bash_session
        self.remote_dir = remote_dir
        self.wait_log_flag = False

        if ns_sts:
            nn = ns_sts.split('@')
            self.sts = nn[0]
            if len(nn) > 1:
                self.namespace = nn[1]

    # work for CliCommand.Values()
    def __eq__(self, other: 'ReplState'):
        return self.sts == other.sts and self.pod == other.pod

    def __hash__(self):
        return hash((self.sts, self.pod))

    def apply_args(self, args: list[str], cmd: list[str] = None, resolve_pg = True) -> tuple['ReplState', list[str]]:
        state = self

        new_args = []
        for index, arg in enumerate(args):
            if index < 6:
                state = copy.copy(state)

                s, n = KubeContext.is_sts_name(arg)
                if s:
                    if not state.sts:
                        state.sts = s
                    if n and not state.namespace:
                        state.namespace = n

                p, n = KubeContext.is_pod_name(arg)
                if p:
                    if not state.pod:
                        state.pod = p
                    if n and not state.namespace:
                        state.namespace = n

                pg = None
                if resolve_pg:
                    pg = KubeContext.is_pg_name(arg)
                    if pg and not state.pg_path:
                        state.pg_path = pg

                if not s and not p and not pg:
                    new_args.append(arg)
            else:
                new_args.append(arg)

        if cmd:
            new_args = new_args[len(cmd):]

        return (state, new_args)

    def validate(self, required: RequiredState = None, pg_required: RequiredState = None, app_required: RequiredState = None):
        if not pg_required and not app_required:
            if required == RequiredState.CLUSTER:
                if not self.namespace or not self.sts:
                    if self.in_repl:
                        log2('cd to a Cassandra cluster first.')
                    else:
                        log2('* Cassandra cluster is missing.')
                        log2()
                        display_help()

                    return False
            elif required == RequiredState.POD:
                if not self.namespace or not self.pod:
                    if self.in_repl:
                        log2('cd to a pod first.')
                    else:
                        log2('* Pod is missing.')
                        log2()
                        display_help()

                    return False
            elif required == RequiredState.CLUSTER_OR_POD:
                if not self.namespace or not self.sts and not self.pod:
                    if self.in_repl:
                        log2('cd to a Cassandra cluster first.')
                    else:
                        log2('* Cassandra cluster or pod is missing.')
                        log2()
                        display_help()

                    return False
            elif required == RequiredState.NAMESPACE:
                if not self.namespace:
                    if self.in_repl:
                        log2('Namespace is required.')
                    else:
                        log2('* namespace is missing.')
                        log2()
                        display_help()

                    return False

        if pg_required == RequiredState.PG_DATABASE:
            pg = PostgresSession(self.namespace, self.pg_path)
            if not pg.db:
                if self.in_repl:
                    log2('cd to a database first.')
                else:
                    log2('* database is missing.')
                    log2()
                    display_help()

                return False

        if app_required == RequiredState.APP_APP and not self.app_app:
            if self.in_repl:
                log2('cd to an app first.')
            else:
                log2('* app is missing.')
                log2()
                display_help()

            return False

        return True

    def user_pass(self, secret_path = 'cql.secret'):
        return Secrets.get_user_pass(self.pod if self.pod else self.sts, self.namespace, secret_path=secret_path)

    def enter_bash(self, bash_session: BashSession):
        self.bash_session = bash_session
        if self.device != ReplState.C:
            self.device = ReplState.C
            log2(f'Moved to {ReplState.C}: automatically. Will move back to {ReplState.P}: when you exit the bash session.')

    def exit_bash(self):
        if self.bash_session and self.bash_session.device:
            self.device = self.bash_session.device

        self.bash_session = None

    def wait_log(self, msg: str):
        if not self.wait_log_flag:
            log2(msg)
            self.wait_log_flag = True

    def clear_wait_log_flag(self):
        self.wait_log_flag = False