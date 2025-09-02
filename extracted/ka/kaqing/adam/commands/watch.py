import threading
import time
from kubernetes import client
from typing import List

from adam.commands.command import Command
from adam.commands.commands_utils import show_pods, show_rollout
from adam.config import Config
from adam.k8s_utils.statefulsets import StatefulSets
from adam.repl_state import ReplState, RequiredState
from adam.utils import convert_seconds, log2

class Watch(Command):
    COMMAND = 'watch'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Watch, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return Watch.COMMAND

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        pods = StatefulSets.pods(state.sts, state.namespace)
        if not pods:
            log2("No pods are found.")
            return state

        stop_event = threading.Event()
        thread = threading.Thread(target=self.loop, args=(stop_event, state.sts, pods, state.namespace), daemon=True)
        thread.start()

        try:
            log2(f"Press Ctrl+C to break.")

            time.sleep(Config().get('watch.timeout', 3600 * 1))
        except KeyboardInterrupt:
            pass

        log2("Stopping watch...")
        stop_event.set()
        thread.join()

        return state

    def loop(self, stop_flag: threading.Event, sts: str, pods: List[client.V1Pod], ns: str):
        show_pods(pods, ns)
        show_rollout(sts, ns)

        cnt = Config().get('watch.interval', 10)
        while not stop_flag.is_set():
            time.sleep(1)
            cnt -= 1

            if not cnt:
                show_pods(pods, ns)
                show_rollout(sts, ns)
                cnt = Config().get('watch.interval', 10)

    def completion(self, state: ReplState):
        if state.pod:
            return {}

        if not state.sts:
            return {Watch.COMMAND: {n: None for n in StatefulSets.list_sts_names()}}

        return {Watch.COMMAND: None}

    def help(self, _: ReplState):
        return f'{Watch.COMMAND}\t watch pod changes'