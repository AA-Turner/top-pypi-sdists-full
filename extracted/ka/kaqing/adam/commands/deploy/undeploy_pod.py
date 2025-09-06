from adam.app_session import AppSession
from adam.commands.command import Command
from adam.commands.deploy.deploy_utils import deploy_frontend, undeploy_frontend
from adam.config import Config
from adam.k8s_utils.ingresses import Ingresses
from adam.k8s_utils.kube_context import KubeContext
from adam.k8s_utils.pods import Pods
from adam.k8s_utils.service_accounts import ServiceAccounts
from adam.k8s_utils.services import Services
from adam.repl_state import ReplState, RequiredState
from adam.utils import log2

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

        if KubeContext.in_cluster():
            log2('This is doable only from outside of the Kubernetes cluster.')
            return state

        label_selector = Config().get('pod.label-selector', 'run=ops')
        undeploy_frontend(state.namespace, label_selector)
        Pods.delete_with_selector(state.namespace, label_selector, grace_period_seconds=0)
        ServiceAccounts.delete(state.namespace, label_selector=label_selector)

        return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, _: ReplState):
        return f'{UndeployPod.COMMAND}\t undeploy pod'