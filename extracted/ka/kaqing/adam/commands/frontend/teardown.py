import click

from adam.commands.command import Command
from adam.commands.command_helpers import ClusterCommandHelper
from adam.commands.frontend.teardown_frontend import TearDownFrontend
from .setup_frontend import SetupFrontend
from adam.repl_state import ReplState
from adam.utils import lines_to_tabular, log, log2

class TearDown(Command):
    COMMAND = 'teardown'
    reaper_login = None

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(TearDown, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return TearDown.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)

        if state.in_repl:
            log(lines_to_tabular([c.help(ReplState()) for c in TearDown.cmd_list()], separator=':'))

            return 'command-missing'
        else:
            # head with the Chain of Responsibility pattern
            cmds = Command.chain(TearDown.cmd_list())
            if not cmds.run(cmd, state):
                log2('* Command is missing.')
                Command.display_help()

    def cmd_list():
        return [TearDownFrontend()]

    def completion(self, state: ReplState):
        if state.sts:
            return super().completion(state)

        return {}

    def help(self, _: ReplState):
        return None

class TearDownCommandHelper(click.Command):
    def get_help(self, ctx: click.Context):
        log(super().get_help(ctx))
        log()
        log('Sub-Commands:')

        log(lines_to_tabular([c.help(ReplState()).replace(f'{TearDown.COMMAND} ', '  ', 1) for c in TearDown.cmd_list()], separator=':'))