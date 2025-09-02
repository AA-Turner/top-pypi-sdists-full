from adam.commands.command import Command
from adam.k8s_utils.ingresses import Ingresses
from adam.k8s_utils.services import Services
from adam.repl_state import ReplState, RequiredState

class TearDownFrontend(Command):
    COMMAND = 'teardown frontend'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(TearDownFrontend, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return TearDownFrontend.COMMAND

    def required(self):
        return RequiredState.NAMESPACE

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        name = 'ops'
        Ingresses.delete_ingress(name, state.namespace)
        Services.delete_service(name, state.namespace)

        return state

    def completion(self, _: ReplState):
        return {}

    def help(self, _: ReplState):
        return f'{TearDownFrontend.COMMAND}\t tear down frontend'