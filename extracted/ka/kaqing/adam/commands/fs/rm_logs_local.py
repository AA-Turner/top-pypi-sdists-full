import os

from adam.commands.command import Command
from adam.repl_state import ReplState
from adam.utils import log2, log_dir

class RmLogsLocal(Command):
    COMMAND = ':rm logs'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(RmLogsLocal, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return RmLogsLocal.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            cmd = f'rm -rf {log_dir()}/*'
            log2(cmd, text_color='gray')
            os.system(cmd)
            log2()

            return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, f'remove all qing log files under {log_dir()}')