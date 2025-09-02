import click

from adam.commands.command import Command
from adam.commands.command_helpers import ClusterCommandHelper
from .repair_run import RepairRun
from .repair_scan import RepairScan
from .repair_stop import RepairStop
from .repair_log import RepairLog
from adam.repl_state import ReplState, RequiredState
from adam.utils import lines_to_tabular, log, log2

class Repair(Command):
    COMMAND = 'repair'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Repair, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return Repair.COMMAND

    def required(self):
        return RequiredState.CLUSTER

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        if state.in_repl:
            log(lines_to_tabular([c.help(ReplState()) for c in Repair.cmd_list()], separator='\t'))

            return 'command-missing'
        else:
            # head with the Chain of Responsibility pattern
            cmds = Command.chain(Repair.cmd_list())
            if not cmds.run(cmd, state):
                log2('* Command is missing.')
                Command.display_help()

    def cmd_list():
        return [RepairRun(), RepairScan(), RepairStop(), RepairLog()]

    def completion(self, state: ReplState):
        if state.sts:
            return super().completion(state)
        return {}

    def help(self, _: ReplState):
        return None

class RepairCommandHelper(click.Command):
    def get_help(self, ctx: click.Context):
        log(super().get_help(ctx))
        log()
        log('Sub-Commands:')

        log(lines_to_tabular([c.help(ReplState()).replace(f'{Repair.COMMAND} ', '  ', 1) for c in Repair.cmd_list()], separator='\t'))
        log()
        ClusterCommandHelper.cluster_help()