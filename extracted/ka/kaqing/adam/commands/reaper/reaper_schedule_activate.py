from adam.commands import validate_args
from adam.commands.command import Command
from adam.commands.reaper.utils_reaper import Reapers, reaper
from adam.repl_state import ReplState, RequiredState

import nest_asyncio
nest_asyncio.apply()

import asyncio

class ReaperScheduleActivate(Command):
    COMMAND = 'reaper activate schedule'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ReaperScheduleActivate, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ReaperScheduleActivate.COMMAND

    def required(self):
        return RequiredState.CLUSTER

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with validate_args(args, state, name='schedule') as schedule_id:
                with reaper(state) as http:
                    http.put(f'repair_schedule/{schedule_id}?state=ACTIVE')
                    Reapers.show_schedule(state, schedule_id)

                return schedule_id

    def completion(self, state: ReplState):
        return super().completion(state, lambda: {id: None for id in Reapers.cached_schedule_ids(state)}, auto_key='reaper.schedules')

    def help(self, state: ReplState):
        return super().help(state, 'resume reaper schedule', args='<schedule-id>')