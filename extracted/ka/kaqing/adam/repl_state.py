from copy import copy
from enum import Enum
import re
from typing import Callable

from adam.utils_context import Context
from adam.utils_k8s.app_clusters import AppClusters
from adam.utils_k8s.app_pods import AppPods
from adam.utils_k8s.cassandra_clusters import CassandraClusters
from adam.utils_k8s.cassandra_nodes import CassandraNodes
from adam.utils_k8s.kube_context import KubeContext
from adam.utils_k8s.secrets import Secrets
from adam.utils import display_help, log2, random_alphanumeric

class BashSession:
    def __init__(self, device: str = None):
        self.session_id = random_alphanumeric(6)
        self.device = device

    def pwd(self, state: 'ReplState'):
        command = f'cat /tmp/.qing-{self.session_id}'

        with device(state) as pods:
            return pods.exec(command, action='bash', ctx=Context.NULL)

class RequiredState(Enum):
    CLUSTER = 'cluster'
    POD = 'pod'
    CLUSTER_OR_POD = 'cluster_or_pod'
    NAMESPACE = 'namespace'
    PG_DATABASE = 'pg_database'
    APP_APP = 'app_app'
    EXPORT_DB = 'export_db'

class ReplState:
    A = 'a'
    C = 'c'
    L = 'l'
    P = 'p'
    X = 'x'

    ANY = [A, C, L, P, X]
    NON_L = [A, C, P, X]

    def __init__(self, device: str = None,
                 sts: str = None, pod: str = None, namespace: str = None, ns_sts: str = None,
                 pg_path: str = None,
                 app_env: str = None, app_app: str = None, app_pod: str = None,
                 in_repl = False, bash_session: BashSession = None, remote_dir = None):
        self.namespace = KubeContext.in_cluster_namespace()

        self.device = device
        self.sts = sts
        self.pod = pod
        self.pg_path = pg_path
        self.app_env = app_env
        self.app_app = app_app
        self.app_pod = app_pod
        if namespace:
            self.namespace = namespace
        self.in_repl = in_repl
        self.bash_session = bash_session
        self.remote_dir = remote_dir
        self.original_state: ReplState = None
        self.pod_targetted = False

        self.export_session: str = None

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

    def __str__(self):
        msg = ''
        if self.device == ReplState.P:
            msg = f'{ReplState.P}:'
            host, database = self.pg_host_n_database()
            if database:
                msg += database
            elif host:
                msg += host
        elif self.device == ReplState.A:
            msg = f'{ReplState.A}:'
            if self.app_env:
                msg += self.app_env
            if self.app_app:
                msg += f'/{self.app_app}'
            if self.app_pod:
                # azops88-c3-c3-k8sdeploy-appleader-001-79957cf5b6-9k4bw
                group = re.match(r".*?-.*?-.*?-.*?-(.*?-.*?)-.*", self.app_pod)
                msg += '/' + group[1]
        elif self.device == ReplState.L:
            msg = f'{ReplState.L}:'
        elif self.device == ReplState.X:
            msg = f'{ReplState.X}:'
            if self.export_session:
                msg += self.export_session
        else:
            msg = f'{ReplState.C}:'
            if self.pod:
                # cs-d0767a536f-cs-d0767a536f-default-sts-0
                group = re.match(r".*?-.*?-(.*)", self.pod)
                msg += group[1]
            elif self.sts:
                # cs-d0767a536f-cs-d0767a536f-default-sts
                group = re.match(r".*?-.*?-(.*)", self.sts)
                msg += group[1]

        return msg

    def apply_args(self, args: list[str], cmd: list[str] = None, resolve_pg = True, args_to_check = 6) -> tuple['ReplState', list[str]]:
        state = self

        new_args = []
        for index, arg in enumerate(args):
            if index < args_to_check:
                state = copy(state)

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

    def apply_device_arg(self, args: list[str], cmd: list[str] = None) -> tuple['ReplState', list[str]]:
        state = self

        new_args = []
        for index, arg in enumerate(args):
            if index < 6:
                state = copy(state)

                groups = re.match(r'^([a|c|l|p|x]):(.*)$', arg)
                if groups:
                    if groups[1] == 'p':
                        state.device = 'p'
                        state.pg_path = groups[2]
                    elif groups[1] == 'c':
                        state.device = 'c'
                        if path := groups[2]:
                            p_and_ns = path.split('@')
                            sts_and_pod = p_and_ns[0].split('/')
                            state.sts = sts_and_pod[0]
                            if len(sts_and_pod) > 1:
                                state.pod = sts_and_pod[1]
                            if len(p_and_ns) > 1:
                                state.namespace = p_and_ns[1]
                            elif ns := KubeContext.in_cluster_namespace():
                                state.namespace = ns
                    elif groups[1] == 'l':
                        state.device = 'l'
                    elif groups[1] == 'x':
                        state.device = 'x'
                    else:
                        state.device = 'a'
                        if path := groups[2]:
                            env_and_app = path.split('/')
                            state.app_env = env_and_app[0]
                            if len(env_and_app) > 1:
                                state.app_app = env_and_app[1]
                else:
                    new_args.append(arg)
            else:
                new_args.append(arg)

        if cmd:
            new_args = new_args[len(cmd):]

        return (state, new_args)

    def validate(self, required: list[RequiredState] = [], show_err = True):
        if not required:
            return True

        def default_err():
            if self.in_repl:
                log2(f'Not a valid command on {self.device}: drive.')
            else:
                log2('* on a wrong device.')
                log2()
                display_help()

        if type(required) is not list:
            valid, err = self._validate(required)
            if valid:
                return True

            if show_err:
                if err:
                    err()
                else:
                    default_err()

            return False

        devices = [r for r in required if r in [ReplState.L, ReplState.A, ReplState.C, ReplState.P, ReplState.X]]
        non_devices = [r for r in required if r not in [ReplState.L, ReplState.A, ReplState.C, ReplState.P, ReplState.X]]

        first_error: Callable = None
        for r in non_devices:
            valid, err = self._validate(r)
            if valid:
                return True

            if not first_error:
                first_error = err

        if devices:
            valid, err = self._validate_device(devices)
            if valid:
                return True

            if not first_error:
                first_error = err

        if show_err and first_error:
            if first_error:
                first_error()
            else:
                default_err()

        return False

    def _validate(self, required: RequiredState):
        if required == RequiredState.CLUSTER:
            if self.device != ReplState.C:
                return (False, None)

            if not self.namespace or not self.sts:
                def error():
                    if self.in_repl:
                        log2('cd to a Cassandra cluster first.')
                    else:
                        log2('* Cassandra cluster is missing.')
                        log2()
                        display_help()
                return (False, error)

        elif required == RequiredState.POD:
            if self.device != ReplState.C:
                return (False, None)

            if not self.namespace or not self.pod:
                def error():
                    if self.in_repl:
                        log2('cd to a pod first.')
                    else:
                        log2('* Pod is missing.')
                        log2()
                        display_help()
                return (False, error)

        elif required == RequiredState.CLUSTER_OR_POD:
            if self.device != ReplState.C:
                return (False, None)

            if not self.namespace or not self.sts and not self.pod:
                def error():
                    if self.in_repl:
                        log2('cd to a Cassandra cluster first.')
                    else:
                        log2('* Cassandra cluster or pod is missing.')
                        log2()
                        display_help()
                return (False, error)

        elif required == RequiredState.NAMESPACE:
            if self.device != ReplState.C:
                return (False, None)

            if not self.namespace:
                def error():
                    if self.in_repl:
                        log2('Namespace is required.')
                    else:
                        log2('* namespace is missing.')
                        log2()
                        display_help()
                return (False, error)

        elif required == RequiredState.PG_DATABASE:
            if self.device != ReplState.P:
                return (False, None)

            _, database = self.pg_host_n_database()
            if not database:
                def error():
                    if self.in_repl:
                        log2('cd to a database first.')
                    else:
                        log2('* database is missing.')
                        log2()
                        display_help()
                return (False, error)

        elif required == RequiredState.APP_APP:
            if self.device != ReplState.A:
                return (False, None)

            if not self.app_app:
                def error():
                    if self.in_repl:
                        log2('cd to an app first.')
                    else:
                        log2('* app is missing.')
                        log2()
                        display_help()
                return (False, error)

        elif required == RequiredState.EXPORT_DB:
            if self.device not in [ReplState.C, ReplState.X]:
                return (False, None)

            if not self.export_session:
                def error():
                    if self.in_repl:
                        if self.device == ReplState.C:
                            log2("Select an export database first with 'use' command.")
                        else:
                            log2('cd to an export database first.')
                    else:
                        log2('* export database is missing.')
                        log2()
                        display_help()
                return (False, error)

        elif required in [ReplState.L, ReplState.A, ReplState.C, ReplState.P, ReplState.X] and self.device != required:
            def error():
                if self.in_repl:
                    log2(f'Switch to {required}: first.')
                else:
                    log2('* on a wrong device.')
                    log2()
                    display_help()
            return (False, error)

        return (True, None)

    def _validate_device(self, devices: list[RequiredState]):
        if self.device not in devices:
            def error():
                if self.in_repl:
                    log2(f'Not a valid command on {self.device}: drive.')
                else:
                    log2('* on a wrong device.')
                    log2()
                    display_help()
            return (False, error)

        return (True, None)

    def user_pass(self, secret_path = 'cql.secret'):
        return Secrets.get_user_pass(self.pod if self.pod else self.sts, self.namespace, secret_path=secret_path)

    def enter_bash(self, bash_session: BashSession):
        self.push()

        self.bash_session = bash_session

    def exit_bash(self):
        self.pop()
        self.bash_session = None

    def push(self, pod_targetted=False):
        if not self.original_state:
            self.original_state = copy(self)
            self.pod_targetted = pod_targetted

    def pop(self):
        if o := self.original_state:
            self.device = o.device
            self.sts = o.sts
            self.pod = o.pod
            self.pg_path = o.pg_path
            self.app_env = o.app_env
            self.app_app = o.app_app
            self.app_pod = o.app_pod
            # self.export_session = o.export_session
            self.namespace = o.namespace

            self.original_state = None
            self.pod_targetted = False

    def pg_host_n_database(self):
        host = None
        database = None

        if self.pg_path:
            host_n_db = self.pg_path.split('/')
            host = host_n_db[0]
            if len(host_n_db) > 1:
                database = host_n_db[1]

        return host, database

    def with_no_pod(self):
        state1 = copy(self)
        state1.pod = None

        return state1

    def with_pod(self, pod: str):
        state1 = copy(self)
        state1.pod = pod

        return state1

    def with_namespace(self, namespace: str):
        state1 = copy(self)
        state1.namespace = namespace

        return state1

class DevicePodService:
    def __init__(self, handler: 'DeviceExecHandler'):
        self.handler = handler

    def exec(self, command: str, action='bash', ctx: Context = Context.NULL):
        state = self.handler.state

        rs = None
        if state.device == ReplState.A and state.app_app:
            if state.app_pod:
                rs = [AppPods.exec(state.app_pod, state.namespace, command, ctx=ctx)]
            else:
                pods = AppPods.pod_names(state.namespace, state.app_env, state.app_app)
                rs = AppClusters.exec(pods, state.namespace, command, ctx=ctx)
        elif state.pod:
            rs = [CassandraNodes.exec(state.pod, state.namespace, command, ctx=ctx)]
        elif state.sts:
            rs = CassandraClusters.exec(state.sts, state.namespace, command, action=action, ctx=ctx)
        # assume that pg-agent or ops pod is single pod

        dir = None
        if rs:
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

class DeviceExecHandler:
    def __init__(self, state: ReplState):
        self.state = state

    def __enter__(self):
        return DevicePodService(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

def device(state: ReplState):
    return DeviceExecHandler(state)