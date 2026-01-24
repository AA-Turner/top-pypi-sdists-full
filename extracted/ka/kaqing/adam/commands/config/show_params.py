from adam.commands.command import Command
from adam.config import Config
from adam.repl_state import ReplState
from adam.utils import tabulize

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

        return tabulize(Config().keys(), lambda k: f'{k}\t{Config().get(k, None)}', separator='\t')

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'show Kaqing system parameters')