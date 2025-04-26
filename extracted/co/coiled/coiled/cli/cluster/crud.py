from typing import Optional

import click

import coiled

from ..utils import CONTEXT_SETTINGS
from .utils import find_cluster


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("cluster", default="", required=False)
@click.option(
    "--account",
    "--workspace",
    default=None,
    help="Coiled workspace (uses default workspace if not specified)."
    " Note: --account is deprecated, please use --workspace instead.",
)
def stop(
    cluster: str,
    account: Optional[str],
):
    with coiled.Cloud(account=account) as cloud:
        cluster_info = find_cluster(cloud, cluster)
        print(
            f"Requesting stop for {cluster_info['name']} ({cluster_info['id']}), "
            f"current state is {cluster_info['current_state']['state']}"
        )
        cluster_id = cluster_info["id"]
        cloud.delete_cluster(cluster_id, account, reason="User requested stop via CLI")
