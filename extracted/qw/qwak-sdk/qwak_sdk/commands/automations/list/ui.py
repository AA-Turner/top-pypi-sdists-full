import click

from qwak_sdk.commands.automations.list._logic import (
    execute_list_automations,
    execute_list_json_automations,
)
from qwak_sdk.inner.tools.cli_tools import QwakCommand


@click.command(
    "list",
    help="List all automations",
    cls=QwakCommand,
)
@click.option("--json-format", is_flag=True, type=bool)
def list_automations(json_format: bool, **kwargs):
    if json_format:
        click.echo(execute_list_json_automations())

    else:
        click.echo(execute_list_automations())
