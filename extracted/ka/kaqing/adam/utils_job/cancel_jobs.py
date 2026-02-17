from adam.commands import validate_args
from adam.commands.command import Command
from adam.utils_repl.repl_state import ReplState, RequiredState
from adam.utils import datetime_sec_precision
from adam.utils_job.job_scheduler import JobScheduler
from adam.utils_job.job_schedules import JobSchedules
from adam.utils_job.job_status import JobStatus
from adam.utils_repl.set_completer import SetCompleter
from adam.utils_tabulize import tabulize

class CancelJobs(Command):
    COMMAND = 'cancel jobs'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(CancelJobs, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return CancelJobs.COMMAND

    def required(self):
        return RequiredState.CLUSTER

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state, apply=False) as (args, state):
            with self.context(args) as (_, ctx):
                with validate_args(args, state, name='job id'):
                    job_ids = self.comma_separated_args(args)

                    canceled: list[JobStatus] = list(JobScheduler.cancel_jobs(state, job_ids).values())
                    canceled = sorted(canceled, key=lambda s: s.job_id())

                    ctx.log('Canceled jobs:')
                    tabulize(canceled,
                            fn=lambda s: f'{s.job_id()}\t{datetime_sec_precision(s.ts)}',
                            header='JOB\tSCHEDULED/COMPLETED',
                            separator='\t',
                            ctx=ctx)

                    return state

    def completion(self, state: ReplState):
        return super().completion(state, lambda: SetCompleter(JobSchedules.pending().keys()))

    def help(self, state: ReplState):
        return super().help(state, 'cancel scheduled jobs', args='<job-id>,...')