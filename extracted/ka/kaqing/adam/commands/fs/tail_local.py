import os

from adam.commands import validate_args
from adam.commands.command import Command
from adam.repl_state import ReplState, RequiredState
from adam.utils import log2
from adam.utils_local import find_local_files

class TailLocal(Command):
    COMMAND = ':tail'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(TailLocal, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return TailLocal.COMMAND

    def required(self):
        return [RequiredState.CLUSTER_OR_POD, RequiredState.APP_APP, ReplState.P, ReplState.X, ReplState.L]

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with validate_args(args, state, name='file') as args:
                cmd = f'tail -n 10 {args}'
                log2(cmd)
                log2()

                os.system(cmd)
                log2()

                return state

    def completion(self, state: ReplState):
        return super().completion(state, lambda: {n: None for n in find_local_files(file_type='f', max_depth=1)}, auto='jit')

    def help(self, state: ReplState):
        return super().help(state, 'run tail command on local file system', args='<file>')