from adam.commands import validate_args
from adam.commands.command import Command
from adam.config import Config
from adam.repl_state import ReplState

class DebugTimings(Command):
    COMMAND = 'debug timings'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(DebugTimings, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return DebugTimings.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with validate_args(args, state, name='on, off or file') as args:
                Config().set('debugs.timings', args)

                return state

    def completion(self, state: ReplState):
        return super().completion(state, {f: None for f in ['on', 'off', 'file']})

    def help(self, state: ReplState):
        return super().help(state, 'turn timing debug on or off', args='on|off|file')