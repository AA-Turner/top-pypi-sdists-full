import webbrowser

import click
from click import Context

from tinybird.tb.config import get_display_cloud_host
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.exceptions import CLIException
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.local_common import get_build_workspace_name


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
    env = ctx.ensure_object(dict)["env"]

    url_host = get_display_cloud_host(client.host)

    if not workspace:
        workspace = get_build_workspace_name(config.get("path")) if env == "build" else config.get("name")

    if not workspace:
        raise CLIException(
            FeedbackManager.error(
                message="No workspace found. Run 'tb login' first or pass a workspace using the --workspace parameter"
            )
        )

    click.echo(FeedbackManager.highlight(message=f"» Opening workspace {workspace} in the browser"))

    auth_url = f"{url_host}/{workspace}"
    webbrowser.open(auth_url)
