import click

from adam.commands.deploy.undeploy_frontend import UndeployFrontend
from adam.commands.deploy.undeploy_pg_agent import UndeployPgAgent
from adam.commands.deploy.undeploy_pod import UndeployPod
from adam.commands.intermediate_command import IntermediateCommand

class Undeploy(IntermediateCommand):
    COMMAND = 'undeploy'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Undeploy, cls).__new__(cls)

        return cls.instance

    def command(self):
        return Undeploy.COMMAND

    def cmd_list(self):
        return [UndeployFrontend(), UndeployPod(), UndeployPgAgent()]

class UndeployCommandHelper(click.Command):
    def get_help(self, ctx: click.Context):
        IntermediateCommand.intermediate_help(super().get_help(ctx), Undeploy.COMMAND, Undeploy().cmd_list())