from adam.commands.command import Command
from adam.k8s_utils.pods import Pods
from adam.k8s_utils.statefulsets import StatefulSets
from adam.repl_state import ReplState, RequiredState
from adam.utils import log2

class Restart(Command):
    COMMAND = 'restart'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Restart, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return Restart.COMMAND

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        args, forced = Command.extract_options(args, '--force')
        if not args:
            if state.pod:
                log2(f'Restarting {state.pod}...')
                Pods.delete(state.pod, state.namespace)
            else:
                if not forced:
                    log2('Please add --force for restarting all nodes in a cluster.')
                    return 'force-needed'

                log2(f'Restarting all pods from {state.sts}...')
                for pod_name in StatefulSets.pod_names(state.sts, state.namespace):
                    Pods.delete(pod_name, state.namespace)
        else:
            for arg in args:
                Pods.delete(arg, state.namespace)

        return state

    def completion(self, state: ReplState):
        if state.pod:
            return {Restart.COMMAND: None}
        elif state.sts:
            return {Restart.COMMAND: {p: None for p in StatefulSets.pod_names(state.sts, state.namespace)}}

        return {}

    def help(self, _: ReplState):
        return f"{Restart.COMMAND} [<host-id>] [--force]\t restart the node you're in or all the nodes in the cluster"