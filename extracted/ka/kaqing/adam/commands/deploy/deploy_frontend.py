from adam.commands.command import Command
from adam.commands.deploy.deploy_utils import deploy_frontend
from adam.config import Config
from adam.repl_state import ReplState, RequiredState
from adam.utils import log2

class DeployFrontend(Command):
    COMMAND = 'deploy frontend'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(DeployFrontend, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return DeployFrontend.COMMAND

    def required(self):
        return RequiredState.NAMESPACE

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        log2('This will support c3/c3 only for demo.')

        pod_name = Config().get('pod.name', 'ops')
        label_selector = Config().get('pod.label-selector', 'run=ops')
        try:
            uri = deploy_frontend(pod_name, state.namespace, label_selector)
            log2(f'Ops pod is available at {uri}.')
        except Exception as e:
            if e.status == 409:
                log2(f"Error: '{pod_name}' already exists in namespace '{state.namespace}'.")
            else:
                log2(f"Error creating ingress or service: {e}")

        return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, _: ReplState):
        return f'{DeployFrontend.COMMAND}\t deploy Web frontend'