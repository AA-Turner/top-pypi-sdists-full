from adam.commands.fs.utils_fs import show_last_results_for_background_jobs
from adam.commands.command import Command
from adam.repl_state import ReplState
from adam.utils_async_job import AsyncJobs
from adam.utils_context import Context

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

        if cmd_info := AsyncJobs.show_restarts_command():
            show_last_results_for_background_jobs(state, cmd_info, ctx=Context.new(show_out=True))

        return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'show status of background jobs')