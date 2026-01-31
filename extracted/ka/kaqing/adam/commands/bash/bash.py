from adam.commands import extract_trailing_options
from adam.commands.bash import bash
from adam.commands.command import Command
from adam.commands.devices.devices import Devices
from adam.repl_state import ReplState, RequiredState
from adam.utils_context import Context

class Bash(Command):
    COMMAND = 'bash'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Bash, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return Bash.COMMAND

    def required(self):
        return [RequiredState.CLUSTER_OR_POD, RequiredState.APP_APP, ReplState.P]

    def run(self, cmd: str, s0: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, s0)

        with self.validate(args, s0) as (args, s1):
            with extract_trailing_options(args, '&') as (args, background):
                with bash(s0, s1) as exec:
                    return exec(args, Context.new(cmd, background=background))

    def completion(self, state: ReplState):
        return super().completion(state, {c : {'&': None} for c in ['ls', 'cat', 'head']}, pods=Devices.of(state).pods(state, '-'))

    def help(self, state: ReplState):
        return super().help(state, 'run bash on Cassandra nodes', args='[bash-commands] [&]')