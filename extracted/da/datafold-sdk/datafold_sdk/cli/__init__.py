import logging
import os
from typing import Any

import click

from datafold_sdk.cli import diff, dbt, alerts, ci, context, monitors
from datafold_sdk.cli.context import CliContext
from datafold_sdk.cli.context import DATAFOLD_HOST, DATAFOLD_API_KEY, DATAFOLD_APIKEY
from datafold_sdk.versions import start_fetching_versions, check_newer_version
from datafold_sdk.version import __version__


from datafold_sdk import sdk_log

FORMAT = '%(asctime)-15s:%(levelname)s:%(module)s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

logger = logging.getLogger(__file__)
logger.addHandler(sdk_log.SDKLogHandler())

@click.group()
@click.option('--host',
              default="https://app.datafold.com",
              help="Set the host for Dedicated Cloud deployments of Datafold. For multi-tenant SaaS deployments, the host value does not need to be set. You can also store an environment variable, DATAFOLD_HOST")
@click.pass_context
def manager(ctx, host: str, **kwargs):
    """DATAFOLD CLI\n
       Please visit us 🙏 for detailed documentation:
       https://docs.datafold.com/reference/cloud/datafold-sdk"""

    api_key = os.environ.get(DATAFOLD_API_KEY) or os.environ.get(DATAFOLD_APIKEY)
    if not api_key:
        raise ValueError(f"The {DATAFOLD_API_KEY} environment variable is not set")

    override_host = os.environ.get(DATAFOLD_HOST)
    if override_host is not None:
        logger.info(f"Overriding host {host} to {override_host}")
        host = override_host

    start_fetching_versions()
    ctx.obj = CliContext(host=host, api_key=api_key)


@manager.result_callback()
def check_latest_version(result: None, **_: Any) -> None:
    check_newer_version()
    return result


@manager.command()
@click.pass_context
def version(ctx):
    """Displays Datafold CLI version."""
    print(__version__)


manager.add_command(diff.manager, "diff")
manager.add_command(dbt.manager, "dbt")
manager.add_command(alerts.manager, "queries")
manager.add_command(ci.manager, "ci")
manager.add_command(monitors.manager, "monitors")
