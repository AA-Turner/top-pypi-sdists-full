from prompt_toolkit.completion import WordCompleter

from adam.commands.command import Command
from adam.repl_state import ReplState
from adam.utils_job.job import Job
from adam.utils_job.job_completer import job_completer
from adam.utils_job.utils_job_results import show_last_results

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
            with self.context(args) as (args, ctx):
                show_last_results(state, args, ctx=ctx)

                return state

    def completion(self, state: ReplState):
        return super().completion(state, job_completer())

    def help(self, state: ReplState):
        return super().help(state, 'show results of last background job', args='[job_id]')