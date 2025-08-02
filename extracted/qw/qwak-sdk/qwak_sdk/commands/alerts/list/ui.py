import click

from qwak_sdk.commands.alerts.list._logic import (
    execute_json_format_list_channels,
    execute_list_channels,
)
from qwak_sdk.inner.tools.cli_tools import QwakCommand


@click.command("list", cls=QwakCommand, help="List all alerts system channels.")
@click.option("--json-format", is_flag=True, type=bool)
def list_channels(json_format, **kwargs):
    if json_format:
        print(execute_json_format_list_channels())

    else:
        print(execute_list_channels())
