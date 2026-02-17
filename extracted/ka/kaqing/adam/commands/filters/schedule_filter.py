from functools import partial
from typing import Callable

from adam.commands.command import Command
from adam.commands.command_filter import CommandFilter
from adam.utils_context import Context
from adam.utils_global import thread_local
from adam.utils_job.job_scheduler import JobScheduler
from adam.utils_job.job_status import JobStatus, NullJobStatus
from adam.utils_log import log2
from adam.utils_repl.repl_state import ReplState

class ScheduleFilter(CommandFilter):
    def command(self) -> str:
        return 'schedule'

    def process(self, state: ReplState, cmd: str) -> tuple[Callable[[], None], ReplState, str]:
        if (pre := f'{self.command()} ') and cmd.startswith(pre):
            cmd = cmd[len(pre):]

            thread_local.scheduled_command = cmd

            # scheduled job needs background
            if not cmd.endswith(' &'):
                cmd = cmd + ' &'

            return partial(ScheduleFilter.callback, state, cmd), state, cmd

        return None, state, cmd

    def applicable_commands(self, commands: list[Command]) -> list[Command]:
        return [c for c in commands if c.schedulable()]

    def callback(state: ReplState, cmd: str, result: JobStatus):
        if hasattr(thread_local, 'scheduled_command'):
            thread_local.scheduled_command = None

        if not isinstance(result, JobStatus):
            log2('Scheduling is ignored as command is not schedulable.')

            return

        if isinstance(result, NullJobStatus):
            # handled by its own scheduler, for example, NodeRestartScheduler
            return

        JobScheduler.schedule(state, cmd, result, ctx=Context.new(show_out=True, job_id=result.job_id()))

    def help(self, state: ReplState) -> str:
        return super().help(state, 'schedule command that is automatically retried until succeeded', command='schedule <command>...')