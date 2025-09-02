from adam.commands.command import Command
from adam.commands.frontend.code_utils import start_user_code, stop_user_codes
from adam.repl_state import ReplState, RequiredState
from adam.utils import log2

class CodeStart(Command):
    COMMAND = 'code start'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(CodeStart, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return CodeStart.COMMAND

    def required(self):
        return RequiredState.NAMESPACE

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        log2('This will support c3/c3 only for demo.')

        stop_user_codes(state.namespace)
        try:
            start_user_code(state.namespace)
        finally:
            stop_user_codes(state.namespace)

        return state

    def completion(self, state: ReplState):
        if state.namespace:
            return super().completion(state)

        return {}

    def help(self, _: ReplState):
        return f'{CodeStart.COMMAND}\t start code server'