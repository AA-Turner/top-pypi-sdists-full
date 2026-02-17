from adam.commands.command import Command
from adam.utils_repl.repl_state import ReplState
from adam.utils_job.job import Job
from adam.utils_job.utils_job_results import show_last_results_for_node_schedules, show_last_results_with_local_log

class ShowNodeRestartSchedules(Command):
    COMMAND = 'show node restart schedules'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowNodeRestartSchedules, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowNodeRestartSchedules.COMMAND

    def aliases(self):
        return [':??']

    def run(self, cmd: str, state: ReplState):
        if not self.args(cmd):
            return super().run(cmd, state)

        with self.context() as (_, ctx):
            if job := Job.node_scheduler():
                show_last_results_with_local_log(state, job, ctx=ctx)
                show_last_results_for_node_schedules(state, job, ctx=ctx)

            return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'show node restart schedule status')