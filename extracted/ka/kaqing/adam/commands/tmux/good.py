import click

from adam.commands.tmux.good_morning import GoodMorning
from adam.commands.tmux.good_night import GoodNight
from adam.commands.intermediate_command import IntermediateCommand

class Good(IntermediateCommand):
    COMMAND = 'good'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Good, cls).__new__(cls)

        return cls.instance

    def command(self):
        return Good.COMMAND

    def cmd_list(self):
        return [GoodMorning(), GoodNight()]

class GoodCommandHelper(click.Command):
    def get_help(self, ctx: click.Context):
        IntermediateCommand.intermediate_help(super().get_help(ctx), Good.COMMAND, Good().cmd_list(), show_cluster_help=True)