from adam.commands.command import Command
from adam.config import Config
from adam.repl_state import ReplState
from adam.utils import log, log2

class SetParam(Command):
    COMMAND = 'set'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(SetParam, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return SetParam.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)

        if len(args) < 2:
            log2('set <key> <value>')

            return 'invalid args'

        key = args[0]
        value = args[1]
        Config().set(key, value)

        log(Config().get(key, None))

        return value

    def completion(self, _: ReplState):
        return {SetParam.COMMAND: {key: ({'true': None, 'false': None} if Config().get(key, None) in [True, False] else None) for key in Config().keys()}}

    def help(self, _: ReplState):
        return f"{SetParam.COMMAND} <key> <value>\t sets a Kaqing parameter to a different value"