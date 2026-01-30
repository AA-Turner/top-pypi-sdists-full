import sys
import os

from adam.utils import tabulize

current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.append(grandparent_dir)

from version import __version__
from adam.commands.command import Command
from adam.repl_state import ReplState

class ShowAdam(Command):
    COMMAND = 'show adam'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowAdam, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowAdam.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not self.args(cmd):
            return super().run(cmd, state)

        package = os.path.dirname(os.path.abspath(__file__))
        package = package.split('/adam/')[0] + '/adam'
        tabulize([
            f'version\t{__version__}',
            f'source\t{package}'
        ], separator='\t', err=True)

        return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'show kaqing version')