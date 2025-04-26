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
@click.option(
    "--private",
    default=False,
    is_flag=True,
    help="Use private IP address of scheduler (default is DNS hostname for public IP)",
)
@click.option(
    "--by-ip",
    default=False,
    is_flag=True,
    help="Use public IP address of scheduler directly, not using DNS hostname",
)
@click.option(
    "--worker",
    default=None,
    help="Connect to worker with specified name or private IP address (default is to connect to scheduler)",
)
def get_address(
    cluster: str,
    account: Optional[str],
    private: bool,
    by_ip: bool,
    worker: Optional[str],
):
    with coiled.Cloud(account=account) as cloud:
        cluster_info = find_cluster(cloud, cluster)
        cluster_id = cluster_info["id"]
        ssh_info = cloud.get_ssh_key(cluster_id=cluster_id, worker=worker)

    if private:
        scheduler_address = ssh_info["scheduler_private_address"]
    else:
        if by_ip:
            scheduler_address = ssh_info["scheduler_public_address"]
        else:
            scheduler_address = ssh_info["scheduler_hostname"] or ssh_info["scheduler_public_address"]

    print(ssh_info["worker_address"] or scheduler_address, end="")
