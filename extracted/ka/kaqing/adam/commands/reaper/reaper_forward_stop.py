from adam.commands.command import Command
from .reaper_session import ReaperSession
from adam.repl_state import ReplState, RequiredState
from adam.utils import log2

class ReaperForwardStop(Command):
    COMMAND = 'reaper forward stop'
    reaper_login = None

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ReaperForwardStop, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ReaperForwardStop.COMMAND

    def required(self):
        return RequiredState.CLUSTER

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        if not ReaperSession.create(state):
            return state

        ReaperSession.is_forwarding = False
        ReaperSession.stopping.set()
        log2("Stopped reaper forward session.")

        return state

    def completion(self, state: ReplState):
        if state.sts:
            return super().completion(state)

        return {}

    def help(self, _: ReplState):
        return f'{ReaperForwardStop.COMMAND}\t stop port-forward to reaper'