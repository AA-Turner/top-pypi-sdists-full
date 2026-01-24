import click

from adam.commands.command import Command
from adam.commands.intermediate_command import IntermediateCommand
from .medusa_backup import MedusaBackup
from .medusa_restore import MedusaRestore
from .medusa_show_backupjobs import MedusaShowBackupJobs
from .medusa_show_restorejobs import MedusaShowRestoreJobs

class Medusa(IntermediateCommand):
    COMMAND = 'medusa'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Medusa, cls).__new__(cls)

        return cls.instance

    def command(self):
        return Medusa.COMMAND

    def cmd_list(self):
        return [MedusaBackup(), MedusaRestore(), MedusaShowBackupJobs(), MedusaShowRestoreJobs()]

class MedusaCommandHelper(click.Command):
    def get_help(self, ctx: click.Context):
        IntermediateCommand.intermediate_help(super().get_help(ctx), Medusa.COMMAND, Medusa().cmd_list(), show_cluster_help=True)