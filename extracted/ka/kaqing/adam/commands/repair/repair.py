import click

from adam.commands.intermediate_command import IntermediateCommand
from .repair_run import RepairRun
from .repair_scan import RepairScan
from .repair_stop import RepairStop
from .repair_log import RepairLog

class Repair(IntermediateCommand):
    COMMAND = 'repair'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Repair, cls).__new__(cls)

        return cls.instance

    def command(self):
        return Repair.COMMAND

    def cmd_list(self):
        return [RepairRun(), RepairScan(), RepairStop(), RepairLog()]

class RepairCommandHelper(click.Command):
    def get_help(self, ctx: click.Context):
        IntermediateCommand.intermediate_help(super().get_help(ctx), Repair.COMMAND, Repair().cmd_list(), show_cluster_help=True)