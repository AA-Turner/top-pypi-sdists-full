from adam.commands import extract_options, extract_trailing_options, validate_args
from adam.commands.command import Command
from adam.utils_cassandra.cassandra import Cassandra
from adam.utils_cassandra.node_restartable import NodeRestartable
from adam.utils_cassandra.node_restarter import NodeRestarter
from adam.utils_context import Context
from adam.utils_k8s.pods import Pods
from adam.utils_k8s.statefulsets import StatefulSets
from adam.repl_state import ReplState, RequiredState
from adam.utils import Color

class RestartNodes(Command):
    COMMAND = 'restart nodes'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(RestartNodes, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return RestartNodes.COMMAND

    def required(self):
        return RequiredState.CLUSTER

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state, apply=False) as (args, state):
            with extract_trailing_options(args, '&') as (args, backgrounded):
                with extract_options(args, '--force') as (args, forced):
                    with validate_args(args, state, name='pod name'):
                        if backgrounded:
                            # start with foreground, it become background if the node restart thread is not yet runnig during scheduling
                            ctx = Context.new(cmd=cmd, show_out=True)

                            for pod in args:
                                NodeRestarter.schedule(state, pod, ctx)
                        else:
                            ctx = Context.new(cmd=cmd, show_out=True, backgrounded=backgrounded)
                            for arg in args:
                                if forced:
                                    ctx.log(f'[{arg}] Restarting...')
                                else:
                                    ctx.log(f'[{arg}] Checking...')

                                    node: NodeRestartable = Cassandra.restartable(state, arg, in_restartings=NodeRestarter.restartings(ctx=ctx), ctx=ctx.copy(show_out=False))
                                    if not node.restartable():
                                        node.log(ctx=ctx.copy(text_color=Color.gray))
                                        ctx.log2('Please add --force for restarting pod unsafely.')

                                        return 'force-needed'

                                Pods.delete(arg, state.namespace)

                        return state

    def completion(self, state: ReplState):
        return super().completion(state, lambda: {p: {'--force': {'&': None}, '&': None} for p in StatefulSets.pod_names(state.sts, state.namespace)})

    def help(self, state: ReplState):
        return super().help(state, 'restart Cassandra nodes  --force do not check node dependency', args='<pod-name>... [--force] [&]')