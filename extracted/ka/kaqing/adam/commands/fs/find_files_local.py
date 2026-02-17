import os

from adam.commands.command import Command
from adam.directories import Directories
from adam.utils_repl.repl_state import ReplState
from adam.utils_log import log2

class FindLocalFiles(Command):
    COMMAND = ':find file'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(FindLocalFiles, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return FindLocalFiles.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            cmd = 'find'

            if not args:
                cmd = f'find {Directories.local_q_dir()}'
            elif len(args) == 1:
                cmd = f"find {Directories.local_q_dir()} -name '{args[0]}'"
            else:
                new_args = [f"'{arg}'" if '*' in arg else arg for arg in args]
                cmd = 'find ' + ' '.join(new_args)

            log2(cmd, text_color='gray')
            os.system(cmd)

            return state

    def completion(self, state: ReplState):
        return super().completion(state, {
            '*.csv': None,
            '*.db': None,
            '*': None
        })

    def help(self, state: ReplState):
        return super().help(state, 'find files from local machine', args='[linux-find-arguments]')