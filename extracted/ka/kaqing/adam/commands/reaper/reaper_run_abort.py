from adam.commands import validate_args
from adam.commands.command import Command
from adam.commands.reaper.utils_reaper import reaper
from adam.repl_state import ReplState, RequiredState
from adam.utils import log2

class ReaperRunAbort(Command):
    COMMAND = 'reaper abort run'

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

        with self.validate(args, state) as (args, state):
            with validate_args(args, state, name='run id') as run_id:
                with reaper(state) as http:
                    http.put(f'repair_run/{run_id}/state/ABORTED')

                return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'abort reaper run', args='<run-id>')