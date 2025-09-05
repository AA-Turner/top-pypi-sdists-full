from kubernetes import client

from adam.commands.command import Command
from adam.commands.deploy.deploy_utils import deploy_frontend, gen_labels
from adam.config import Config
from adam.k8s_utils.ingresses import Ingresses
from adam.k8s_utils.kube_context import KubeContext
from adam.k8s_utils.pods import Pods
from adam.k8s_utils.service_accounts import ServiceAccounts
from adam.k8s_utils.services import Services
from adam.repl_state import ReplState, RequiredState
from adam.utils import log2

class DeployPod(Command):
    COMMAND = 'deploy pod'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(DeployPod, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return DeployPod.COMMAND

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

        sa_name = Config().get('pod.sa.name', 'ops')
        sa_proto = Config().get('pod.sa.proto', 'c3')
        additional_cluster_roles = Config().get('pod.sa.additional-cluster-roles', 'c3aiops-k8ssandra-operator').split(',')
        label_selector = Config().get('pod.label-selector', 'run=ops')
        labels = gen_labels(label_selector)
        ServiceAccounts.replicate(sa_name, state.namespace, sa_proto, labels=labels, add_cluster_roles=additional_cluster_roles)

        pod_name = Config().get('pod.name', 'ops')
        image = Config().get('pod.image', 'seanahnsf/kaqing')
        security_context = client.V1SecurityContext(
            capabilities=client.V1Capabilities(
                add=["SYS_PTRACE"]
            )
        )
        Pods.create(state.namespace, pod_name, image, env={'NAMESPACE': state.namespace}, container_security_context=security_context, labels=labels, sa_name=sa_name)

        uri = deploy_frontend(pod_name, state.namespace, label_selector)

        Pods.wait_for_running(state.namespace, pod_name, msg=f'Ops pod is starting up; it will be available at {uri}.')

        return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, _: ReplState):
        return f'{DeployPod.COMMAND}\t deploy pod'