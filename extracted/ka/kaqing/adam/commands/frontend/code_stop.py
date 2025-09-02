from adam.commands.command import Command
from adam.commands.frontend.code_utils import stop_user_codes
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

        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        _, dry = Command.extract_options(args, '--dry')
        stop_user_codes(state.namespace, dry)

        # if not args:
        #     log2('Please specify <port>.')
        #     return state

        # port = args[0]
        # name = f'ops-{port}'
        # user = os.getenv("USER")
        # label_selector=f'user={user}'
        # Ingresses.delete_ingresses(state.namespace, label_selector=label_selector)
        # Services.delete_services(state.namespace, label_selector=label_selector)

        # pattern = f'/c3/c3/ops/code/{user}/'
        # self.kill_process_by_pattern(pattern)

        return state

    def completion(self, state: ReplState):
        if state.namespace:
            return super().completion(state)

        return {}

    def help(self, _: ReplState):
        return f'{CodeStop.COMMAND}\t stop code server'