from adam.commands.command import Command
from adam.utils_repl.repl_state import ReplState
from adam.utils_job.job import Job
from adam.utils_job.utils_job_results import show_last_results_for_job_schedules, show_last_results_with_local_log

class ShowJobSchedules(Command):
    COMMAND = 'show job schedules'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowJobSchedules, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowJobSchedules.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not self.args(cmd):
            return super().run(cmd, state)

        with self.context() as (_, ctx):
            if job := Job.job_scheduler():
                show_last_results_with_local_log(state, job, ctx=ctx)
                show_last_results_for_job_schedules(state, job, ctx=ctx)

            return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'show status of scheduled jobs')