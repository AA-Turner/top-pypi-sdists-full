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
        if state.pod:
            return {Exit.COMMAND: None}

        return {}

    def help(self, _: ReplState):
        return f'{Exit.COMMAND}\t exit kaqing <Ctrl-D>'