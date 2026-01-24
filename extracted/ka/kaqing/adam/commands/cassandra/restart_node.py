from adam.commands import extract_options
from adam.commands.command import Command
from adam.commands.devices.devices import Devices
from adam.utils_k8s.pods import Pods
from adam.repl_state import ReplState, RequiredState
from adam.utils import log2

class RestartNode(Command):
    COMMAND = 'restart node'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(RestartNode, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return RestartNode.COMMAND

    def required(self):
        return RequiredState.POD

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            if not state.pod:
                log2("'pod' is required")

                return 'pod-needed'

            with extract_options(args, '--force') as (args, forced):
                if not forced:
                    log2('Please add --force for restarting pod.')

                    return 'force-needed'

                log2(f'Restarting {state.pod}...')
                Pods.delete(state.pod, state.namespace)

                return state

    def completion(self, state: ReplState):
        return super().completion(state, {'--force': None}, pods=Devices.of(state).pods(state, '-'))

    def help(self, state: ReplState):
        return super().help(state, 'restart the node', args='--force')