from adam.commands import extract_options
from adam.commands.command import Command
from adam.utils_cassandra.node_restartability import NodeRestartability
from adam.utils_cassandra.node_restart_scheduler import NodeRestartScheduler
from adam.utils_cassandra.node_restart_schedules import NodeRestartSchedules
from adam.utils_k8s.pods import Pods
from adam.utils_k8s.statefulsets import StatefulSets
from adam.repl_state import ReplState, RequiredState
from adam.utils_color import Color
from adam.utils_log import log2

class RestartCluster(Command):
    COMMAND = 'restart cassandra cluster'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(RestartCluster, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return RestartCluster.COMMAND

    def required(self):
        return RequiredState.CLUSTER

    def backgrounable(self):
        return True

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with self.context(args) as (args, ctx):
                with extract_options(args, '--force') as (args, forced):
                    log2(f'Restarting all pods from {state.sts}...')

                    pods = StatefulSets.pod_names(state.sts, state.namespace)
                    if ctx.background:
                        # start with foreground, it become background if the node restart thread is not yet runnig during scheduling
                        for pod_name in pods:
                            NodeRestartScheduler.schedule(state, pod_name, ctx.copy(background=False))
                    else:
                        if not forced:
                            for pod_name in pods:
                                ctx.log(f'[{pod_name}] Checking...')
                                node: NodeRestartability = NodeRestartability.probe(state,
                                                                                    pod_name,
                                                                                    in_restartings=NodeRestartSchedules.restartings(ctx=ctx),
                                                                                    ctx=ctx.copy(show_out=False))
                                if not node.restartable():
                                    node.log(ctx=ctx.copy(text_color=Color.gray))
                                    ctx.log2('Please add --force for restarting pods unsafely.')

                                    return 'force-needed'

                        for pod_name in pods:
                            ctx.log(f'[{pod_name}] Restarting...')
                            Pods.delete(pod_name, state.namespace)
                            ctx.log(f'[{pod_name}] OK')

                    return state

    def completion(self, state: ReplState):
        return super().completion(state, {'--force': None})

    def help(self, state: ReplState):
        return super().help(state, 'restart all nodes in cluster', args='--force')