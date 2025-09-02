import requests

from adam.commands.command import Command
from .reaper_session import ReaperSession
from adam.repl_state import ReplState, RequiredState
from adam.utils import log2

class ReaperRunAbort(Command):
    COMMAND = 'reaper abort run'
    reaper_login = None

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ReaperRunAbort, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ReaperRunAbort.COMMAND

    def required(self):
        return RequiredState.CLUSTER

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        if not args:
            if state.in_repl:
                log2('Specify run id to abort.')
            else:
                Command.display_help()

            return state

        if not(reaper := ReaperSession.create(state)):
            return state

        self.stop_run(state, reaper, args[0])

        return state

    def stop_run(self, state: ReplState, reaper: ReaperSession, run_id: str):
        def body(uri: str, headers: dict[str, str]):
            return requests.put(uri, headers=headers)

        # PAUSED, RUNNING, ABORTED
        # PUT /repair_run/{id}/state/{state}
        reaper.port_forwarded(state, f'repair_run/{run_id}/state/ABORTED', body, method='PUT')

    def completion(self, state: ReplState):
        if state.sts:
            return super().completion(state)

        return {}

    def help(self, _: ReplState):
        return f'{ReaperRunAbort.COMMAND} <run-id>\t abort reaper run'