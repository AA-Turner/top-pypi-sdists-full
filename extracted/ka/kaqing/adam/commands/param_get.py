from adam.commands.command import Command
from adam.config import Config
from adam.repl_state import ReplState
from adam.utils import lines_to_tabular, log, log2

class GetParam(Command):
    COMMAND = 'get'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(GetParam, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return GetParam.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)

        if len(args) < 1:
            lines = [f'{key}\t{Config().get(key, None)}' for key in Config().keys()]
            log(lines_to_tabular(lines, separator='\t'))

            return state

        key = args[0]
        if v := Config().get(key, None):
            log(v)
        else:
            log2(f'{key} is not set.')

        return v if v else state

    def completion(self, _: ReplState):
        return {GetParam.COMMAND: {key: None for key in Config().keys()}}

    def help(self, _: ReplState):
        return f"{GetParam.COMMAND} <key>\t shows a Kaqing parameter"