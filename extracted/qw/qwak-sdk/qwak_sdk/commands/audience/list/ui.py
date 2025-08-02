import click

from qwak_sdk.commands._logic.tools import list_of_messages_to_json_str
from qwak_sdk.commands.audience.audience_api_dump import (
    audience_entries_to_pretty_string,
)
from qwak_sdk.commands.audience.list.logic import list_audience
from qwak_sdk.exceptions import QwakCommandException, QwakResourceNotFound
from qwak_sdk.inner.tools.cli_tools import QwakCommand


@click.command("list", cls=QwakCommand)
@click.option("--json-format", is_flag=True, type=bool)
def list_audience_command(json_format: bool, **kwargs):
    try:
        audience_entries = list_audience()
        if json_format:
            click.echo(list_of_messages_to_json_str(audience_entries))
        else:
            click.echo("Getting audiences")
            click.echo(
                audience_entries_to_pretty_string(audience_entries=audience_entries)
            )
    except (QwakCommandException, QwakResourceNotFound) as e:
        click.echo(f"Failed to list audiences, Error: {e}")
        exit(1)
