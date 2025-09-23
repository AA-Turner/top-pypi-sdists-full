from adam.commands.command import Command
from adam.commands.deploy.deploy_utils import undeploy_frontend, deleting
from adam.config import Config
from adam.k8s_utils.config_maps import ConfigMaps
from adam.k8s_utils.deployment import Deployments
from adam.k8s_utils.pods import Pods
from adam.k8s_utils.service_accounts import ServiceAccounts
from adam.repl_state import ReplState, RequiredState

class UndeployPod(Command):
    COMMAND = 'undeploy pod'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(UndeployPod, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return UndeployPod.COMMAND

    def required(self):
        return RequiredState.NAMESPACE

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        label_selector = Config().get('pod.label-selector', 'run=ops')
        deleting('service account', lambda: ServiceAccounts.delete(state.namespace, label_selector=label_selector))
        deleting('config map', lambda: ConfigMaps.delete_with_selector(state.namespace, label_selector))
        deleting('deployment', lambda: Deployments.delete_with_selector(state.namespace, label_selector, grace_period_seconds=0))
        deleting('pod', lambda: Pods.delete_with_selector(state.namespace, label_selector, grace_period_seconds=0))
        undeploy_frontend(state.namespace, label_selector)

        return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, _: ReplState):
        return f'{UndeployPod.COMMAND}\t undeploy Ops pod'