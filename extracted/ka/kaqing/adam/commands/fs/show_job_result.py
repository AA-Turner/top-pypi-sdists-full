from adam.commands.fs.utils_fs import show_last_results, show_last_local_results
from adam.commands.command import Command
from adam.repl_state import ReplState
from adam.utils import log_to_pods
from adam.utils_async_job import AsyncJobs
from adam.utils_context import Context

class ShowJobResults(Command):
    COMMAND = 'show job result'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowJobResults, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowJobResults.COMMAND

    def aliases(self):
        return [':?']

    def run(self, cmd: str, state: ReplState):
        if not (args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            if log_to_pods():
                show_last_results(state, args, ctx=self.context())
            else:
                show_last_local_results(state, ctx=self.context())

            return state

    def completion(self, state: ReplState):
        return super().completion(state, lambda: {j: None for j in reversed(sorted(AsyncJobs.commands().keys()))}, auto='jit')

    def help(self, state: ReplState):
        return super().help(state, 'show results of last background job', args='[job_id]')