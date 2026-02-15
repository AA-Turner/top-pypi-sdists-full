from adam.commands import validate_args
from adam.commands.command import Command
from adam.repl_state import ReplState
from adam.utils_job.job import Job
from adam.utils_job.job_completer import job_completer

class Retry(Command):
    COMMAND = 'retry'

    run_command: callable = None

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Retry, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return Retry.COMMAND

    def aliases(self):
        return [':!']

    def run(self, cmd: str, state: ReplState):
        if not (args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with validate_args(args, state, name='job id') as job_id:
                with self.context(args) as (args, ctx):
                    if ctx.debug:
                        ctx.show_out=True

                    job = Job.job(job_id)
                    if not job:
                        ctx.log2('Job not found.')
                        return state

                    if not job.raw_command:
                        ctx.log2('Cannot find raw command for job.')
                        return state

                    self.run_command(state, job.raw_command, job=job)

                    return state

    def completion(self, state: ReplState):
        return super().completion(state, job_completer())

    def help(self, state: ReplState):
        return super().help(state, 'retry command', args='[job_id]')