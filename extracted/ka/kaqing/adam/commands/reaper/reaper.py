import click

from adam.commands.intermediate_command import IntermediateCommand
from .reaper_forward import ReaperForward
from .reaper_forward_stop import ReaperForwardStop
from .reaper_restart import ReaperRestart
from .reaper_run_abort import ReaperRunAbort
from .reaper_runs import ReaperRuns
from .reaper_runs_abort import ReaperRunsAbort
from .reaper_schedule_activate import ReaperScheduleActivate
from .reaper_schedule_start import ReaperScheduleStart
from .reaper_schedule_stop import ReaperScheduleStop
from .reaper_schedules import ReaperSchedules
from .reaper_status import ReaperStatus

class Reaper(IntermediateCommand):
    COMMAND = 'reaper'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Reaper, cls).__new__(cls)

        return cls.instance

    def command(self):
        return Reaper.COMMAND

    def cmd_list(self):
        return [ReaperSchedules(), ReaperScheduleStop(), ReaperScheduleActivate(), ReaperScheduleStart(),
                ReaperForwardStop(), ReaperForward(), ReaperRunAbort(), ReaperRunsAbort(), ReaperRestart(),
                ReaperRuns(), ReaperStatus()]

class ReaperCommandHelper(click.Command):
    def get_help(self, ctx: click.Context):
        IntermediateCommand.intermediate_help(super().get_help(ctx), Reaper.COMMAND, Reaper().cmd_list(), show_cluster_help=True)