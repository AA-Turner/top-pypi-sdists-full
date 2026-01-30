from adam.commands.bash.bash_completer import BashCompleter
from adam.commands.command import Command, InvalidStateException
from adam.commands.commands_utils import show_pods, show_rollout
from adam.commands.cql.utils_cql import cassandra, cassandra_table_names
from adam.commands.devices.device import Device
from adam.config import Config
from adam.repl_state import ReplState
from adam.utils import tabulize, log, log2, wait_log
from adam.utils_context import Context
from adam.utils_k8s.cassandra_clusters import CassandraClusters
from adam.utils_k8s.custom_resources import CustomResources
from adam.utils_k8s.kube_context import KubeContext
from adam.utils_k8s.statefulsets import StatefulSets

class DeviceCass(Command, Device):
    COMMAND = f'{ReplState.C}:'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(DeviceCass, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return DeviceCass.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not self.args(cmd):
            return super().run(cmd, state)

        state.device = ReplState.C

        return state

    def pod(self, state: ReplState) -> str:
        return state.pod

    def pod_names(self, state: ReplState) -> list[str]:
        return StatefulSets.pod_names(state.sts, state.namespace)

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'move to Cassandra Operations device')

    def default_container(self, _: ReplState) -> str:
        return 'cassandra'

    def ls(self, cmd: str, state: ReplState):
        if state.pod:
            return self.bash(state, state, cmd.split(' '))
        elif state.sts and state.namespace:
            show_pods(StatefulSets.pods(state.sts, state.namespace), state.namespace, show_namespace=not KubeContext.in_cluster_namespace())
            show_rollout(state.sts, state.namespace)
        else:
            self.show_statefulsets()

    def ls_completion(self, cmd: str, state: ReplState, default: dict = {}):
        if state.sts:
            return super().completion(state) | {f'@{p}': {'ls': None} for p in self.pod_names(state)}
        else:
            return {cmd: {n: None for n in StatefulSets.list_sts_names()}}

    def show_statefulsets(self):
        ss = StatefulSets.list_sts_names()
        if len(ss) == 0:
            log2('No Cassandra clusters found.')
            return

        app_ids = CustomResources.get_app_ids()
        list = []
        for s in ss:
            cr_name = CustomResources.get_cr_name(s)
            app_id = 'Unknown'
            if cr_name in app_ids:
                app_id = app_ids[cr_name]
            list.append(f"{s} {app_id}")

        header = 'STATEFULSET_NAME@NAMESPACE APP_ID'
        if KubeContext.in_cluster_namespace():
            header = 'STATEFULSET_NAME APP_ID'
        tabulize(list, header=header)

    def cd(self, dir: str, state: ReplState):
        if dir == '':
            state.sts = None
            state.pod = None
        elif dir == '..':
            if state.pod:
                state.pod = None
            else:
                state.sts = None
        else:
            if not state.sts:
                ss_and_ns = dir.split('@')
                state.sts = ss_and_ns[0]
                if len(ss_and_ns) > 1:
                    state.namespace = ss_and_ns[1]
            elif not state.pod:
                p, _ = KubeContext.is_pod_name(dir)
                if p:
                    state.pod = p
                else:
                    names = CassandraClusters.pod_names_by_host_id(state.sts, state.namespace)
                    if dir in names:
                        state.pod = names[dir]
                    else:
                        state.pod = dir

    def cd_completion(self, cmd: str, state: ReplState, default: dict = {}):
        if state.pod:
            return {cmd: {'..': None}}
        elif state.sts:
            return {cmd: {'..': None} | {p: None for p in self.pod_names(state)}}
        else:
            return {cmd: {p: None for p in StatefulSets.list_sts_names()}}

    def pwd(self, state: ReplState):
        words = []

        if state.sts:
            words.append(f'sts/{state.sts}')
        if state.pod:
            words.append(f'pod/{state.pod}')

        return '\t'.join([f'{ReplState.C}:>'] + (words if words else ['/']))

    def try_fallback_action(self, chain: Command, state: ReplState, cmd: str):
        if state.sts:
            return True, chain.run(f'cql {cmd}', state)

        return False, None

    def enter(self, state: ReplState):
        auto_enter = Config().get('repl.c.auto-enter', 'cluster')
        if auto_enter and auto_enter in ['cluster', 'first-pod']:
            sts = StatefulSets.list_sts_name_and_ns()
            if not sts:
                log2("No Cassandra clusters found.")
            elif not state.sts and len(sts) == 1:
                cluster = sts[0]
                state.sts = cluster[0]
                state.namespace = cluster[1]
                if auto_enter == 'first-pod':
                    state.pod = f'{state.sts}-0'
                if KubeContext().in_cluster_namespace:
                    wait_log(f'Moving to the only Cassandra cluster: {state.sts}...')
                else:
                    wait_log(f'Moving to the only Cassandra cluster: {state.sts}@{state.namespace}...')

    def show_tables(self, state: ReplState):
        tabulize(cassandra_table_names(state), separator=',')

    def show_table_preview(self, state: ReplState, table: str, rows: int, ctx: Context = Context.NULL):
        with cassandra(state) as pods:
            pods.cql(f'select * from {table} limit {rows}', use_single_quotes=True, on_any=True, ctx=ctx.copy(show_out=True))

    def bash_target_changed(self, s0: ReplState, s1: ReplState):
        return s0.sts != s1.sts or s0.pod != s1.pod

    def exec_no_dir(self, command: str, state: ReplState, ctx: Context = Context.NULL):
        with cassandra(state) as pods:
            return pods.exec(command, action='bash', shell='bash', ctx=ctx.copy(show_out=True, show_verbose=True))

    def exec_with_dir(self, command: str, session_just_created: bool, state: ReplState, ctx: Context = Context.NULL):
        with cassandra(state) as pods:
            return pods.exec(command, action='bash', shell='bash', ctx=ctx.copy(show_out=not session_just_created, show_verbose=not session_just_created))

    def bash_completion(self, cmd: str, state: ReplState, default: dict = {}):
        completions = {cmd: BashCompleter(lambda: [])}

        if state.sts and state.namespace:
            completions |= {f'@{p}': {cmd: BashCompleter(lambda: [])} for p in self.pod_names(state)}

        return completions

