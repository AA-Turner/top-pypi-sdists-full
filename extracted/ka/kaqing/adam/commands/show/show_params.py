from adam.commands.command import Command
from adam.config import Config
from adam.repl_state import ReplState
from adam.utils import lines_to_tabular, log

class ShowParams(Command):
    COMMAND = 'show params'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowParams, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowParams.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not self.args(cmd):
            return super().run(cmd, state)

        lines = [f'{key}\t{Config().get(key, None)}' for key in Config().keys()]
        log(lines_to_tabular(lines, separator='\t'))

        return lines

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, _: ReplState):
        return f"{ShowParams.COMMAND}\t show Kaqing parameters"