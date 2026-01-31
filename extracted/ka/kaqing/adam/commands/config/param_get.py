from adam.commands import validate_args
from adam.commands.command import Command
from adam.config import Config
from adam.repl_state import ReplState
from adam.utils import log, log2
from adam.utils_tabulize import tabulize
from adam.utils_context import Context

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

        with self.validate(args, state) as (args, state):
            def msg():
                tabulize(Config().keys(),
                         lambda key: f'{key}\t{Config().get(key, None)}',
                         separator='\t',
                         ctx=self.context())

            with validate_args(args, state, msg=msg) as key:
                if v := Config().get(key, None):
                    log(v)
                else:
                    log2(f'{key} is not set.')

                return v if v else state

    def completion(self, _: ReplState):
        return {GetParam.COMMAND: {key: None for key in Config().keys()}}

    def help(self, state: ReplState):
        return super().help(state, "shows a Kaqing system parameter's value", args='<key>')