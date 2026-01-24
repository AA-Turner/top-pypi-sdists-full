import platform
import sys
from typing import Optional

import click

from tinybird.tb.config import CURRENT_VERSION
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.login_common import login
from tinybird.tb.modules.telemetry import add_telemetry_event


@cli.command("login", help="Authenticate using the browser.")
@click.option(
    "--host",
    type=str,
    default=None,
    help="Set the API host to authenticate to. See https://www.tinybird.co/docs/api-reference#regions-and-endpoints for the available list of regions.",
)
@click.option(
    "--auth-host",
    default="https://cloud.tinybird.co",
    help="Set the auth host to authenticate to. If unset, the default host will be used.",
    hidden=True,
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
    # we send a telemetry event manually so we have user and workspace info available
    add_telemetry_event(
        "system_info",
        platform=platform.platform(),
        system=platform.system(),
        arch=platform.machine(),
        processor=platform.processor(),
        python_runtime=platform.python_implementation(),
        python_version=platform.python_version(),
        is_ci=False,
        ci_product=None,
        cli_version=CURRENT_VERSION,
        cli_args=sys.argv[1:] if len(sys.argv) > 1 else [],
    )
