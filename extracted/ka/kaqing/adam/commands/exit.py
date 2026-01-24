from adam.commands.command import Command
from adam.repl_state import ReplState

class Exit(Command):
    COMMAND = 'exit'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Exit, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return Exit.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not self.args(cmd):
            return super().run(cmd, state)

        exit()

    def completion(self, state: ReplState):
        return {Exit.COMMAND: None}

    def help(self, state: ReplState):
        return super().help(state, 'exit kaqing  <Ctrl-D>')