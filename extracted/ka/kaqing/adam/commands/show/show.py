import click

from adam.commands.command import Command
from adam.commands.command_helpers import ClusterCommandHelper
from adam.commands.show.show_app_actions import ShowAppActions
from adam.commands.show.show_app_queues import ShowAppQueues
from adam.commands.show.show_login import ShowLogin
from .show_params import ShowParams
from .show_app_id import ShowAppId
from .show_cassandra_status import ShowCassandraStatus
from .show_cassandra_version import ShowCassandraVersion
from .show_commands import ShowKubectlCommands
from .show_processes import ShowProcesses
from .show_repairs import ShowRepairs
from .show_storage import ShowStorage
from .show_adam import ShowAdam
from adam.repl_state import ReplState
from adam.utils import lines_to_tabular, log, log2

class Show(Command):
    COMMAND = 'show'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Show, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return Show.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)

        if state.in_repl:
            log(lines_to_tabular([c.help(ReplState()) for c in Show.cmd_list()], separator='\t'))

            return 'command-missing'
        else:
            # head with the Chain of Responsibility pattern
            cmds = Command.chain(Show.cmd_list())
            if not cmds.run(cmd, state):
                log2('* Command is missing.')
                Command.display_help()

    def cmd_list():
        return [ShowAppActions(), ShowAppId(), ShowAppQueues(), ShowLogin(), ShowKubectlCommands(), ShowParams(), ShowProcesses(), ShowRepairs(),
                ShowStorage(), ShowAdam(), ShowCassandraStatus(), ShowCassandraVersion()]

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, _: ReplState):
        return f"{Show.COMMAND}\t show kubectl commands"

class ShowCommandHelper(click.Command):
    def get_help(self, ctx: click.Context):
        log(super().get_help(ctx))
        log()
        log('Catogories:')

        log(lines_to_tabular([c.help(ReplState()).replace(f'{Show.COMMAND} ', '  ', 1) for c in Show.cmd_list()], separator=':'))
        log()
        ClusterCommandHelper.cluster_help()