from typing import Optional

import click

from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.login_common import login


@cli.command("login", help="Authenticate using the browser.")
@click.option(
    "--host",
    type=str,
    default=None,
    help="Set custom host if it's different than https://api.europe-west2.gcp.tinybird.co. See https://www.tinybird.co/docs/api-reference/overview#regions-and-endpoints for the available list of regions.",
)
@click.option(
    "--auth-host",
    default="https://cloud.tinybird.co",
    help="Set the host to authenticate to. If unset, the default host will be used.",
)
@click.option(
    "--workspace",
    help="Set the workspace to authenticate to. If unset, the default workspace will be used.",
)
@click.option(
    "-i",
    "--interactive",
    is_flag=True,
    default=False,
    help="Show available regions and select where to authenticate to",
)
@click.option(
    "--method",
    type=click.Choice(["browser", "code"]),
    default="browser",
    help="Set the authentication method to use. Default: browser.",
)
def login_cmd(host: Optional[str], auth_host: str, workspace: str, interactive: bool, method: str):
    login(host, auth_host, workspace, interactive, method)
