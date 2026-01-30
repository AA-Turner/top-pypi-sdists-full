from adam.commands import extract_options
from adam.commands.command import Command
from adam.utils_cassandra.cassandra import Cassandra
from adam.utils_cassandra.node_restartable import NodeRestartable
from adam.utils_cassandra.node_restarter import NodeRestarter
from adam.utils_context import Context
from adam.utils_k8s.pods import Pods
from adam.utils_k8s.statefulsets import StatefulSets
from adam.repl_state import ReplState, RequiredState
from adam.utils import Color, log2

class RestartCluster(Command):
    COMMAND = 'restart cluster'

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

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with extract_options(args, '--force') as (args, forced):
                ctx = Context.new(show_out=True)

                log2(f'Restarting all pods from {state.sts}...')
                for pod_name in StatefulSets.pod_names(state.sts, state.namespace):
                    if forced:
                        ctx.log(f'[{pod_name}] Restarting...')
                    else:
                        ctx.log(f'[{pod_name}] Checking...')
                        node: NodeRestartable = Cassandra.restartable(state, pod_name, in_restartings=NodeRestarter.restartings(ctx=ctx), ctx=ctx.copy(show_out=False))
                        if not node.restartable():
                            node.log(ctx=ctx.copy(text_color=Color.gray))
                            ctx.log2('Please add --force for restarting pod unsafely.')

                            return 'force-needed'

                    Pods.delete(pod_name, state.namespace)
                    ctx.log(f'[{pod_name}] OK')

                return state

    def completion(self, state: ReplState):
        return super().completion(state, {'--force': None})

    def help(self, state: ReplState):
        return super().help(state, 'restart all the nodes in the cluster', args='--force')