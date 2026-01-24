from adam.commands import extract_options
from adam.commands.command import Command
from adam.utils_k8s.pods import Pods
from adam.utils_k8s.statefulsets import StatefulSets
from adam.repl_state import ReplState, RequiredState
from adam.utils import log2

class RestartCluster(Command):
    COMMAND = 'restart cluster'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(RestartCluster, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return RestartCluster.COMMAND

    def required(self):
        return RequiredState.CLUSTER

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with extract_options(args, '--force') as (args, forced):
                if not forced:
                    log2('Please add --force for restarting all nodes in a cluster.')

                    return 'force-needed'

                log2(f'Restarting all pods from {state.sts}...')
                for pod_name in StatefulSets.pod_names(state.sts, state.namespace):
                    Pods.delete(pod_name, state.namespace)

                return state

    def completion(self, state: ReplState):
        return super().completion(state, {'--force': None})

    def help(self, state: ReplState):
        return super().help(state, 'restart all the nodes in the cluster', args='--force')