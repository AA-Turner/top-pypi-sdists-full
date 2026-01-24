from adam.commands import extract_options, validate_args
from adam.commands.command import Command
from adam.utils_k8s.pods import Pods
from adam.utils_k8s.statefulsets import StatefulSets
from adam.repl_state import ReplState, RequiredState
from adam.utils import log2

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
            with extract_options(args, '--force') as (args, forced):
                with validate_args(args, state, name='pod name'):
                    if not forced:
                        log2('Please add --force for restarting nodes.')

                        return 'force-needed'

                    for arg in args:
                        Pods.delete(arg, state.namespace)

                    return state

    def completion(self, state: ReplState):
        return super().completion(state, lambda: {p: {'--force': None} for p in StatefulSets.pod_names(state.sts, state.namespace)})

    def help(self, state: ReplState):
        return super().help(state, 'restart Cassandra nodes', args='<pod-name>... --force')