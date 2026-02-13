import os

from adam.commands.command import Command
from adam.repl_state import ReplState

class GoodMorning(Command):
    COMMAND = 'good morning'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(GoodMorning, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return GoodMorning.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not self.args(cmd):
            return super().run(cmd, state)

        if user := os.getenv('USER'):
            os.system(f'tmux attach -t {user}')

        return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'bring Kaqing into foreground')