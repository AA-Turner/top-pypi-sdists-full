from adam.commands.command import Command
from adam.repl_state import ReplState
from adam.utils_job.job import Job
from adam.utils_context import Context
from adam.utils_job.utils_job_results import show_last_results_for_background_jobs, show_last_results_with_local_log

class ShowJobs(Command):
    COMMAND = 'show jobs'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowJobs, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowJobs.COMMAND

    def aliases(self):
        return [':??']

    def run(self, cmd: str, state: ReplState):
        if not self.args(cmd):
            return super().run(cmd, state)

        if job := Job.show_restarts_command():
            ctx = self.context()

            show_last_results_with_local_log(state, job, ctx=ctx)
            show_last_results_for_background_jobs(state, job, ctx=ctx)

        return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'show status of background jobs')