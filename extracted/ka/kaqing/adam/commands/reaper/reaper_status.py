import re
from typing import List, cast
from kubernetes import client

from adam.commands.command import Command
from adam.commands.commands_utils import show_pods
from .reaper_session import ReaperSession
from adam.repl_state import ReplState, RequiredState
from adam.utils import lines_to_tabular, log, log2

class ReaperStatus(Command):
    COMMAND = 'reaper status'
    reaper_login = None

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ReaperStatus, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ReaperStatus.COMMAND

    def required(self):
        return RequiredState.CLUSTER

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        if not(reaper := ReaperSession.create(state)):
            return state

        pods = self.list_pods(state.sts, state.namespace)

        show_pods(pods, state.namespace, show_host_id=False)

        return state

    def list_pods(self, sts_name: str, namespace: str) -> List[client.V1Pod]:
        v1 = client.CoreV1Api()

        # cs-9834d85c68-cs-9834d85c68-default-sts-0
        # k8ssandra.io/reaper: cs-d0767a536f-cs-d0767a536f-reaper
        groups = re.match(r'(.*?-.*?-.*?-.*?)-.*', sts_name)
        label_selector = f'k8ssandra.io/reaper={groups[1]}-reaper'

        return cast(List[client.V1Pod], v1.list_namespaced_pod(namespace, label_selector=label_selector).items)

    def completion(self, state: ReplState):
        if state.sts:
            return super().completion(state)

        return {}

    def help(self, _: ReplState):
        return f'{ReaperStatus.COMMAND}\t show reaper status'