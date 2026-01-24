import os

from adam.commands.command import Command
from adam.repl_state import ReplState
from adam.utils import log2
from adam.utils_local import local_qing_dir

class LsLocal(Command):
    COMMAND = ':ls'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(LsLocal, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return LsLocal.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            if args:
                os.system(f'ls {args}')
            else:
                os.system(f'ls {local_qing_dir()}')
            log2()

            return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'list files on local system', args='[dir]')