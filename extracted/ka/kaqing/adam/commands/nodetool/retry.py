from adam.commands import validate_args
from adam.commands.command import Command
from adam.commands.nodetool.nodetool import NodeTool
from adam.repl_state import ReplState
from adam.utils_job.job import Job
from adam.utils_job.job_completer import job_completer
from adam.utils_job.utils_job_results import find_failed_pods

class Retry(Command):
    COMMAND = 'retry'

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

                    # failed = StatefulSets.pod_names(state.sts, state.namespace)[1:]
                    failed = find_failed_pods(state, job, ctx=ctx)
                    NodeTool().retry(job.command, state, failed=failed, ctx=ctx.copy(job_id=job_id, cmd=job.command))

                    return state

    def completion(self, state: ReplState):
        return super().completion(state, job_completer())

    def help(self, state: ReplState):
        return super().help(state, 'retry nodetool command', args='[job_id]')