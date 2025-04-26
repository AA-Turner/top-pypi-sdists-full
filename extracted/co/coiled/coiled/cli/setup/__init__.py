import asyncio

import click

from ..utils import CONTEXT_SETTINGS
from .amp import aws_amp_setup
from .aws import aws_setup
from .azure import azure_setup
from .entry import do_setup_wizard, setup_wizard
from .gcp import gcp_setup
from .prometheus import get_prometheus_read_creds


@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.pass_context
def setup(ctx):
    """Setup Coiled with cloud provider"""
    # `coiled setup` by itself should invoke wizard
    if ctx.invoked_subcommand is None:
        asyncio.run(do_setup_wizard())


setup.add_command(setup_wizard, "wizard")
setup.add_command(aws_setup, "aws")
setup.add_command(gcp_setup, "gcp")
setup.add_command(azure_setup, "azure")

setup.add_command(aws_amp_setup, "amp")
setup.add_command(get_prometheus_read_creds, "prometheus-datasource")
