import click

from .util import (
    console,
    click_group,
)


@click_group()
def deployment():
    pass


def add_command(cli_group):
    cli_group.add_command(deployment)



@deployment.command(name="list")
@click.option(
    "--pattern",
    "-p",
    help="Regular expression pattern to filter deployment names.",
    default=None,
)
def list_command(pattern):
    print("hello my pattern", pattern)
