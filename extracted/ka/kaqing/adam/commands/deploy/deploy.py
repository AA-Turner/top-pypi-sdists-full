import click

from adam.commands.command import Command
from adam.commands.deploy.deploy_pg_agent import DeployPgAgent
from adam.commands.deploy.deploy_pod import DeployPod
from .deploy_frontend import DeployFrontend
from adam.repl_state import ReplState
from adam.utils import lines_to_tabular, log, log2

class Deploy(Command):
    COMMAND = 'deploy'
    reaper_login = None

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Deploy, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return Deploy.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)

        if state.in_repl:
            log(lines_to_tabular([c.help(ReplState()) for c in Deploy.cmd_list()], separator='\t'))

            return 'command-missing'
        else:
            # head with the Chain of Responsibility pattern
            cmds = Command.chain(Deploy.cmd_list())
            if not cmds.run(cmd, state):
                log2('* Command is missing.')
                Command.display_help()

    def cmd_list():
        return [DeployFrontend(), DeployPod(), DeployPgAgent()]

    def completion(self, state: ReplState):
        if state.sts:
            return super().completion(state)

        return {}

    def help(self, _: ReplState):
        return None

class DeployCommandHelper(click.Command):
    def get_help(self, ctx: click.Context):
        log(super().get_help(ctx))
        log()
        log('Sub-Commands:')

        log(lines_to_tabular([c.help(ReplState()).replace(f'{Deploy.COMMAND} ', '  ', 1) for c in Deploy.cmd_list()], separator='\t'))