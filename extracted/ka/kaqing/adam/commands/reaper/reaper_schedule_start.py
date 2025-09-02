import requests

from adam.commands.command import Command
from .reaper_session import ReaperSession
from adam.repl_state import ReplState, RequiredState
from adam.utils import log2

class ReaperScheduleStart(Command):
    COMMAND = 'reaper start schedule'
    reaper_login = None

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ReaperScheduleStart, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ReaperScheduleStart.COMMAND

    def required(self):
        return RequiredState.CLUSTER

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        if not args:
            log2('Specify schedule to activate.')

            return state

        schedule_id = args[0]
        if not(reaper := ReaperSession.create(state)):
            return schedule_id

        self.start_schedule(state, reaper, schedule_id)

        return schedule_id

    def start_schedule(self, state: ReplState, reaper: ReaperSession, schedule_id: str):
        def body(uri: str, headers: dict[str, str]):
            return requests.post(uri, headers=headers)

        reaper.port_forwarded(state, f'repair_schedule/start/{schedule_id}', body, method='POST')
        reaper.show_schedule(state, schedule_id)

    def completion(self, state: ReplState):
        if state.sts:
            leaf = {id: None for id in ReaperSession.cached_schedule_ids(state)}

            return super().completion(state, leaf)

        return {}

    def help(self, _: ReplState):
        return f'{ReaperScheduleStart.COMMAND} <schedule-id>\t start reaper runs for schedule'