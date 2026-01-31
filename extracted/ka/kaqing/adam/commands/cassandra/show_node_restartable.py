from adam.commands import extract_options, extract_trailing_options, validate_args
from adam.commands.command import Command
from adam.commands.devices.devices import Devices
from adam.repl_state import ReplState, RequiredState
from adam.utils_cassandra.cassandra import Cassandra
from adam.utils_cassandra.node_restartable import NodeRestartable
from adam.utils_cassandra.node_restarter import NodeRestarter
from adam.utils_context import Context
from adam.utils_k8s.statefulsets import StatefulSets

class ShowNodeRestartable(Command):
    COMMAND = 'show node restartable'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowNodeRestartable, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowNodeRestartable.COMMAND

    def required(self):
        return RequiredState.CLUSTER

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state, apply=False) as (args, state):
            with extract_trailing_options(args, '&') as (args, background):
                with extract_options(args, ['-s', '--show']) as (args, verbose):
                    with validate_args(args, state, name='Pod Name'):
                        pod = args[0]

                        ctx: Context = Context.new(cmd=cmd, show_out=True, show_verbose=verbose, background=background)
                        node: NodeRestartable = Cassandra.restartable(state, pod, in_restartings=NodeRestarter.restartings(ctx=ctx), ctx=ctx)

                        node.log(ctx)

                        return state

    def completion(self, state: ReplState):
        return super().completion(state, lambda: {p: {'-s': {'&': None}, '&': None} for p in StatefulSets.pod_names(state.sts, state.namespace)})

    def help(self, state: ReplState):
        return super().help(state, 'check if node is restartable  -s show processing details', args='[-s] [&]')