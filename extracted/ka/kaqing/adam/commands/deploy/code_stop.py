from adam.commands.command import Command
from adam.commands.deploy.code_utils import stop_user_codes
from adam.repl_state import ReplState, RequiredState

class CodeStop(Command):
    COMMAND = 'code stop'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(CodeStop, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return CodeStop.COMMAND

    def required(self):
        return RequiredState.NAMESPACE

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            _, dry = Command.extract_options(args, '--dry')
            stop_user_codes(state.namespace, dry)

            return state

    def completion(self, state: ReplState):
        if state.namespace:
            return super().completion(state)

        return {}

    def help(self, state: ReplState):
        return super().help(state, 'stop code server')