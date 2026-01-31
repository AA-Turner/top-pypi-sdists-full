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
from adam.utils_repl.set_completer import SetCompleter

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
            with extract_trailing_options(args, '&') as (args, background):
                with extract_options(args, '--force') as (args, forced):
                    with validate_args(args, state, name='pod name'):
                        # restart nodes allow comma separator
                        safe_args = []
                        for arg in args:
                            for a in arg.split(','):
                                if a:
                                    safe_args.append(a)
                        args = safe_args

                        if background:
                            # start with foreground, it become background if the node restart thread is not yet runnig during scheduling
                            ctx = Context.new(cmd=cmd, show_out=True)

                            for pod in args:
                                NodeRestarter.schedule(state, pod, ctx)
                        else:
                            ctx = Context.new(cmd=cmd, show_out=True, background=background)
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
        return super().completion(state, lambda: SetCompleter(StatefulSets.pod_names(state.sts, state.namespace), options={'--force': {'&': None}, '&': None}))
        # return super().completion(state, lambda: {p: {'--force': {'&': None}, '&': None} for p in StatefulSets.pod_names(state.sts, state.namespace)})

    def help(self, state: ReplState):
        return super().help(state, 'restart Cassandra nodes  --force do not check node dependency', args='<pod-name>,... [--force] [&]')