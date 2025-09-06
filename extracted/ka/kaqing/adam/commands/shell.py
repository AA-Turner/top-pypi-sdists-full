import os

from adam.commands.command import Command
from adam.repl_state import ReplState

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

    def run(self, cmd: str, s0: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, s0)

        _, args = self.apply_state(args, s0)

        os.system('QING_DROPPED=true bash')

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, _: ReplState):
        return f'{Shell.COMMAND}\t drop down to shell'