import click
from click.core import Context as ClickContext
from gable.cli.client import GableAPIClient
from gable.cli.helpers.shell_output import shell_linkify
from gable.cli.options import global_options


@click.command()
@global_options()
@click.pass_context
def ui(ctx: ClickContext):
    """Opens the Gable UI in a web browser"""
    client: GableAPIClient = ctx.obj.client
    url = client.ui_endpoint
    print(f"Opening Gable UI in default web browser: {shell_linkify(url, url)}")
    click.launch(url)
