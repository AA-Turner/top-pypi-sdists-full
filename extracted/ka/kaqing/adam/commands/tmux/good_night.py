import os

from adam.commands.command import Command
from adam.utils_repl.repl_state import ReplState

class GoodNight(Command):
    COMMAND = 'good night'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(GoodNight, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return GoodNight.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not self.args(cmd):
            return super().run(cmd, state)

        if user := os.getenv('USER'):
            os.system(f'tmux detach -s {user}')

        return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'run Kaqing in background over night')