from adam.commands.command import Command
from adam.commands.deploy.deploy_utils import undeploy_frontend
from adam.config import Config
from adam.repl_state import ReplState, RequiredState

class UndeployFrontend(Command):
    COMMAND = 'undeploy frontend'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(UndeployFrontend, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return UndeployFrontend.COMMAND

    def required(self):
        return RequiredState.NAMESPACE

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        label_selector = Config().get('pod.label-selector', 'run=ops')
        undeploy_frontend(state.namespace, label_selector)

        return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, _: ReplState):
        return f'{UndeployFrontend.COMMAND}\t undeploy Web frontend'