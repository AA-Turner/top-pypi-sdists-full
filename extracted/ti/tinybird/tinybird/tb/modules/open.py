import webbrowser

import click
from click import Context

from tinybird.tb.config import get_display_cloud_host
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.exceptions import CLIException
from tinybird.tb.modules.feedback_manager import FeedbackManager, get_cli_name


@cli.command()
@click.option(
    "--workspace",
    help="Set the workspace you want to open. If unset, your current workspace will be used.",
)
@click.pass_context
def open(ctx: Context, workspace: str):
    """Open workspace in the browser."""

    config = ctx.ensure_object(dict)["config"]
    client = ctx.ensure_object(dict)["client"]
    branch = ctx.ensure_object(dict)["branch"]

    is_local = "localhost" in client.host

    if not workspace:
        workspace = config.get("name")

    if not workspace:
        raise CLIException(
            FeedbackManager.error(
                message=f"No workspace found. Run '{get_cli_name()} login' first or pass a workspace using the --workspace parameter"
            )
        )

    if is_local:
        url_host = get_display_cloud_host(config["host"])
        click.echo(FeedbackManager.highlight(message=f"» Opening local workspace {workspace} in the browser"))
        auth_url = f"{url_host}/{workspace}~local~{workspace}"
    elif branch:
        url_host = get_display_cloud_host(client.host)
        click.echo(
            FeedbackManager.highlight(message=f"» Opening branch {branch} of workspace {workspace} in the browser")
        )
        auth_url = f"{url_host}/{workspace}~{branch}"
    else:
        url_host = get_display_cloud_host(client.host)
        click.echo(FeedbackManager.highlight(message=f"» Opening workspace {workspace} in the browser"))
        auth_url = f"{url_host}/{workspace}"

    webbrowser.open(auth_url)
