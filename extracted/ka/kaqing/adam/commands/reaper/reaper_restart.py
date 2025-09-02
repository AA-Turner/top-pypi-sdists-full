from adam.commands.command import Command
from adam.k8s_utils.pods import Pods
from .reaper_session import ReaperSession
from adam.repl_state import ReplState, RequiredState

class ReaperRestart(Command):
    COMMAND = 'reaper restart'
    reaper_login = None

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

        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        if not(reaper := ReaperSession.create(state)):
            return state

        Pods.delete(reaper.pod, state.namespace)

        return state

    def completion(self, state: ReplState):
        if state.sts:
            return super().completion(state)

        return {}

    def help(self, _: ReplState):
        return f'{ReaperRestart.COMMAND}\t restart reaper'