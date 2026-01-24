import os

from adam.commands import validate_args
from adam.commands.command import Command
from adam.repl_state import ReplState
from adam.utils import log2

class Shell(Command):
    COMMAND = ':sh'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Shell, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return Shell.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, _):
            with validate_args(args, state, at_least=0) as args_str:
                if args_str:
                    os.system(args_str)
                    log2()
                else:
                    os.system('QING_DROPPED=true bash')

            return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'drop down to shell')