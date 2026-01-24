from adam.commands import validate_args
from adam.commands.command import Command
from adam.commands.devices.devices import Devices
from adam.repl_state import ReplState, RequiredState

class Tail(Command):
    COMMAND = 'tail'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Tail, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return Tail.COMMAND

    def required(self):
        return [RequiredState.CLUSTER_OR_POD, RequiredState.APP_APP, ReplState.P]

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with validate_args(args, state, name='file') as args:
                return Devices.of(state).bash(state, state, ['tail', '-n', '10', args])

    def completion(self, state: ReplState):
        return super().completion(state, lambda: {f: None for f in Devices.of(state).files(state)}, pods=Devices.of(state).pods(state, '-'), auto='jit')

    def help(self, state: ReplState):
        return super().help(state, 'run tail command on the pod', args='<file>')