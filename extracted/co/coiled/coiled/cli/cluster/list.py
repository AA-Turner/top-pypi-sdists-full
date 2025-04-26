import click
from rich.console import Console
from rich.table import Table

import coiled

from ...utils import get_details_url
from ..utils import CONTEXT_SETTINGS

console = Console()


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--workspace", default=None, required=False, help="Coiled workspace (uses default workspace if not specified)."
)
@click.option(
    "--just-mine",
    default=False,
    is_flag=True,
    help="Show only my clusters",
)
@click.option(
    "--max-pages",
    default=1,
    type=int,
    help="Maximum number of pages to show (where each page is 100 clusters)",
)
def list_clusters(workspace: str, just_mine: bool, max_pages: int):
    """List the Coiled clusters in a workspace"""
    with coiled.Cloud(workspace=workspace) as cloud:
        clusters = cloud.list_clusters(
            workspace=workspace,
            just_mine=just_mine,
            max_pages=max_pages,
        )
        table = Table(title="Clusters")
        table.add_column("Name", style="cyan")
        table.add_column("Updated", style="magenta")
        table.add_column("Link", style="magenta")
        table.add_column("Status", style="green")
        for cluster_details in clusters:
            table.add_row(
                cluster_details["name"],
                cluster_details["updated"],
                get_details_url(cloud.server, workspace or cloud.default_workspace, cluster_details["id"]),
                cluster_details["current_state"].get("state") or "unknown",
            )
        console.print(table)
