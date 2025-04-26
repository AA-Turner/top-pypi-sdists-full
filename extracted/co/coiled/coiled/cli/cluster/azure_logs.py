import click
from rich import print

import coiled

from .. import curl
from ..utils import CONTEXT_SETTINGS
from .better_logs import format_log_event
from .utils import find_cluster


@click.command(
    context_settings=CONTEXT_SETTINGS,
)
@click.option(
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
def show_azure_logs(workspace, cluster):
    with coiled.Cloud(workspace) as cloud:
        cluster_info = find_cluster(cloud, cluster or "")
        cluster_id = cluster_info["id"]
        cluster_name = cluster_info["name"]

        print(f"=== Logs for {cluster_name} ({cluster_id}) ===\n")

        print_azure_log_pages(pull_azure_logs(cloud, cluster_id))


def pull_azure_logs(cloud, cluster_id: int):
    url = f"{cloud.server}/api/v2/logs/cluster/{cluster_id}/init"
    response = curl.sync_request(cloud=cloud, url=url, method="get", data={}, json_output=True)

    if response.get("error"):
        print(response["error"])
        return []

    token = response.get("back", response.get("next"))
    lines = []

    while token:
        url = f"{cloud.server}/api/v2/logs/cluster/{cluster_id}/page/"
        response = curl.sync_request(
            cloud=cloud,
            url=url,
            method="post",
            data={"encoded_session": token},
            json=True,
            json_output=True,
        )
        lines.extend(response["lines"])
        token = response.get("back", response.get("next"))

    return sorted(lines, key=lambda line: line["timestamp"])


def print_azure_log_pages(lines):
    for line in lines:
        print(
            format_log_event(
                line, instances={}, pretty=True, show_label=True, show_timestamp=True, show_all_timestamps=False
            )
        )
