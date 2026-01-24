from adam.commands.command import Command
from adam.commands.reaper.utils_reaper import Reapers
from adam.utils_k8s.pods import Pods
from adam.repl_state import ReplState, RequiredState

class ReaperRestart(Command):
    COMMAND = 'reaper restart'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ReaperRestart, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ReaperRestart.COMMAND

    def required(self):
        return RequiredState.CLUSTER

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            if not (pod := Reapers.pod_name(state)):
                return state

            Pods.delete(pod, state.namespace)

            return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'restart reaper')