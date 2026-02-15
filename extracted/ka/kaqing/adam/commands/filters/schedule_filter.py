from functools import partial
from typing import Callable

from adam.commands.command_filter import CommandFilter
from adam.repl_state import ReplState
from adam.utils_context import Context
from adam.utils_job.job_scheduler import JobScheduler
from adam.utils_job.job_status import JobStatus
from adam.utils_log import log2

class ScheduleFilter(CommandFilter):
    def command(self) -> str:
        return 'schedule'

    def process(self, state: ReplState, cmd: str) -> tuple[Callable[[], None], str]:
        if (pre := f'{self.command()} ') and cmd.startswith(pre):
            cmd = cmd[len(pre):]

            return partial(ScheduleFilter.callback, state, cmd), cmd

        return None, cmd

    def callback(state: ReplState, cmd: str, result: JobStatus):
        if not isinstance(result, JobStatus):
            log2('Scheduling is ignored as command is not schedulable.')

            return

        JobScheduler.schedule(state, cmd, result, ctx=Context.new(show_out=True, job_id=result.job_id()))

    def help(self, state: ReplState) -> str:
        return super().help(state, 'schedule command that is automatically retried until succeeded', command='schedule <command>...')