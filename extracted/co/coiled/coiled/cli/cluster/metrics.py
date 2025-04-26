from typing import Optional

import click

import coiled

from ..utils import CONTEXT_SETTINGS
from .utils import find_cluster


@click.command(
    context_settings=CONTEXT_SETTINGS,
)
@click.option(
    "--account",
    "--workspace",
    default=None,
    help="Coiled workspace (uses default workspace if not specified)."
    " Note: --account is deprecated, please use --workspace instead.",
)
@click.option(
    "--cluster",
    default=None,
    help="Cluster for which to show logs, default is most recent",
)
def foo(
    account: Optional[str],
    cluster: Optional[str],
):
    with coiled.Cloud(account=account) as cloud:
        find_cluster(cloud, cluster or "")
