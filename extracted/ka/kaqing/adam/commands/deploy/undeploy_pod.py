from adam.commands.command import Command
from adam.commands.deploy.deploy_utils import undeploy_frontend
from adam.config import Config
from adam.utils import ing
from adam.utils_k8s.config_maps import ConfigMaps
from adam.utils_k8s.deployment import Deployments
from adam.utils_k8s.pods import Pods
from adam.utils_k8s.service_accounts import ServiceAccounts
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

        with self.validate(args, state) as (args, state):
            label_selector = Config().get('pod.label-selector', 'run=ops')
            with ing('Deleting service account'):
                ServiceAccounts.delete(state.namespace, label_selector=label_selector)
            with ing('Deleting config map'): ConfigMaps.delete_with_selector(state.namespace, label_selector)
            with ing('Deleting deployment'): Deployments.delete_with_selector(state.namespace, label_selector, grace_period_seconds=0)
            with ing('Deleting pod'): Pods.delete_with_selector(state.namespace, label_selector, grace_period_seconds=0)
            undeploy_frontend(state.namespace, label_selector)

            return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'undeploy Ops pod')