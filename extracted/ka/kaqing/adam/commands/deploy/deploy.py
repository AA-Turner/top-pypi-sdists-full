import click

from adam.commands.deploy.deploy_pg_agent import DeployPgAgent
from adam.commands.deploy.deploy_pod import DeployPod
from adam.commands.intermediate_command import IntermediateCommand
from .deploy_frontend import DeployFrontend

class Deploy(IntermediateCommand):
    COMMAND = 'deploy'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Deploy, cls).__new__(cls)

        return cls.instance

    def command(self):
        return Deploy.COMMAND

    def cmd_list(self):
        return [DeployFrontend(), DeployPod(), DeployPgAgent()]

class DeployCommandHelper(click.Command):
    def get_help(self, ctx: click.Context):
        IntermediateCommand.intermediate_help(super().get_help(ctx), Deploy.COMMAND, Deploy().cmd_list())