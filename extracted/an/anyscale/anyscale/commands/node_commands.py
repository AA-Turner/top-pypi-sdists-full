"""`anyscale node list`, `anyscale node get` and `anyscale node gpus`.

The `node` group holds the per-node views of a cluster: `list` and `get` over the
cluster dashboard's node endpoints, `gpus` over the per-node DCGM endpoint. All check
read permission on the cluster. The cluster is named by exactly one of --cluster-id,
--workspace-id, --job-id or --service-id (see `gpu_commands`).

Output is the model as the API returned it, in every format: text is the model as YAML
(like `anyscale job status`), table is one row per GPU with a column per field, json and
yaml are the model. Field names and values are not rewritten.

The group is `hidden=True` for now: it runs when typed, but is left out of `anyscale
--help`, the committed doc spec and the reference docs. Removing the flag (and the
matching one on the GPUs module in `_private/docgen/__main__.py`) publishes it.
"""

from dataclasses import fields
from typing import List, Optional, Tuple

import click

import anyscale
from anyscale.commands.doc_metadata import CommandExample
from anyscale.commands.gpu_commands import (
    beta_metadata,
    GPU_COLUMNS,
    option_output,
    option_resource,
    option_time,
    print_text,
    resource_ids,
    table_row,
)
from anyscale.commands.output_format import OutputFormat, print_output
from anyscale.commands.time_flags import parse_timestamp
from anyscale.commands.util import AnyscaleCommand
from anyscale.gpus.models import NodeGpus
from anyscale.node._private.node_sdk import DEFAULT_MAX_ITEMS
from anyscale.node.models import Node, NodeList, NodeStatus


# Table columns of `node get`: every field of the model, under its API name, in order.
NODE_COLUMNS: List[str] = [field.name for field in fields(Node)]


@click.group("node", help="Inspect the nodes of a cluster.", hidden=True)
def node_cli() -> None:
    pass


@beta_metadata(
    CommandExample(
        description="Every GPU on a node of a job with its DCGM telemetry, right now.",
        command="anyscale node gpus --job-id <job-id> --node-id <node-id>",
    ),
    CommandExample(
        description="The same node during an incident, found by its cluster.",
        command=(
            "anyscale node gpus --cluster-id <cluster-id> --node-id <node-id> "
            "--time 2026-09-01T13:45:00Z"
        ),
    ),
    CommandExample(
        description="One row per GPU of a workspace node.",
        command=("anyscale node gpus --workspace-id <workspace-id> --node-id <node-id> -o table"),
    ),
)
@node_cli.command(name="gpus", cls=AnyscaleCommand, short_help="List the GPUs of a node.")
@option_resource
@click.option("--node-id", required=True, help="ID of the node, e.g. nod_abc123.")
@option_time
@option_output
def gpus(  # noqa: PLR0913
    cluster_id: Optional[str],
    workspace_id: Optional[str],
    job_id: Optional[str],
    service_id: Optional[str],
    node_id: str,
    time: Optional[str],
    output_format: str,
) -> None:
    """List the GPUs of a node of a cluster, workspace, job or service with their DCGM
    telemetry, sorted by index.

    The backend looks back over the cluster's lifetime (up to seven days), so a node that
    is already terminated or dead still lists its GPUs, as OFFLINE with their last-known
    telemetry.
    """
    ids = resource_ids(cluster_id, workspace_id, job_id, service_id)
    node = anyscale.gpus.node_gpus(node_id, **ids, time=parse_timestamp(time, "--time"))
    _print_node(node, output_format)


# --- get -------------------------------------------------------------------------------------


@beta_metadata(
    CommandExample(
        description="State, IPs, instance type, resources and labels of a node of a job.",
        command="anyscale node get --id <node-id> --job-id <job-id>",
    ),
    CommandExample(
        description="The node as an earlier Ray session saw it, found by its cluster.",
        command=(
            "anyscale node get --id <node-id> --cluster-id <cluster-id> "
            "--ray-session session_2026-09-01_13-45-00_123456_1"
        ),
    ),
    CommandExample(
        description="JSON for scripts, for a node of a workspace.",
        command="anyscale node get --id <node-id> --workspace-id <workspace-id> -o json",
    ),
)
@node_cli.command(name="get", cls=AnyscaleCommand, short_help="Get one node of a cluster.")
@click.option(
    "--id",
    "--node-id",
    "node_id",
    required=True,
    help="Ray node ID (hex) of the node, as `anyscale node gpus` and the Nodes tab use it.",
)
@option_resource
@click.option(
    "--ray-session",
    default=None,
    help="Name of the Ray session to read the node from. Defaults to the newest of the "
    "cluster's recent sessions that has the node.",
)
@option_output
def get(  # noqa: PLR0913
    node_id: str,
    cluster_id: Optional[str],
    workspace_id: Optional[str],
    job_id: Optional[str],
    service_id: Optional[str],
    ray_session: Optional[str],
    output_format: str,
) -> None:
    """Get one node of a cluster, workspace, job or service: its state, IPs, instance
    type, Ray resources and labels.

    A node that already died still resolves, with its end time and status DEAD. A node
    the cluster never had, or a cluster that is not ready yet, is an error.
    """
    ids = resource_ids(cluster_id, workspace_id, job_id, service_id)
    node = anyscale.node.get(node_id, **ids, ray_session=ray_session)
    _print_one_node(node, output_format)


def _print_one_node(node: Node, output_format: str) -> None:
    if output_format == OutputFormat.TEXT.value:
        print_text(node)
        return
    if output_format == OutputFormat.TABLE.value:
        print_output([table_row(node)], output_format, NODE_COLUMNS)
        return
    print_output(node, output_format)


# --- list ------------------------------------------------------------------------------------


@beta_metadata(
    CommandExample(
        description="The first 10 nodes of a job, newest Ray session first.",
        command="anyscale node list --job-id <job-id>",
    ),
    CommandExample(
        description="Dead nodes of a service only, up to 200, for a post-mortem.",
        command="anyscale node list --service-id <service-id> --state dead --max-items 200",
    ),
    CommandExample(
        description="Nodes of one instance type in an earlier Ray session, found by cluster.",
        command=(
            "anyscale node list --cluster-id <cluster-id> --filter g5.xlarge "
            "--ray-session session_2026-09-01_13-45-00_123456_1"
        ),
    ),
)
@node_cli.command(name="list", cls=AnyscaleCommand, short_help="List the nodes of a cluster.")
@option_resource
@click.option(
    "--ray-session",
    default=None,
    help="Name of a Ray session: list only its nodes. Defaults to the nodes of the "
    "cluster's recent sessions, newest session first.",
)
@click.option(
    "--filter",
    "--text-filter",
    "text_filter",
    default=None,
    help="Case-insensitive substring to match in the node ID, name, IP, labels or "
    "resources. No regex.",
)
@click.option(
    "--state",
    "states",
    multiple=True,
    type=click.Choice([state.value for state in NodeStatus], case_sensitive=False),
    help="Only nodes in this state. Repeat for several, e.g. --state alive --state pending.",
)
@click.option(
    "--max-items",
    type=click.IntRange(min=1),
    default=DEFAULT_MAX_ITEMS,
    show_default=True,
    help="How many nodes to return at most.",
)
@option_output
def list_nodes(  # noqa: PLR0913
    cluster_id: Optional[str],
    workspace_id: Optional[str],
    job_id: Optional[str],
    service_id: Optional[str],
    ray_session: Optional[str],
    text_filter: Optional[str],
    states: Tuple[str, ...],
    max_items: int,
    output_format: str,
) -> None:
    """List the nodes of a cluster, workspace, job or service with their state, IPs,
    instance type, resources and labels, newest Ray session first.

    Dead nodes stay listed, with their end time. When more nodes match than --max-items,
    the output says so on stderr and `total` carries the full count.
    """
    ids = resource_ids(cluster_id, workspace_id, job_id, service_id)
    page = anyscale.node.list(
        **ids,
        ray_session=ray_session,
        text_filter=text_filter,
        states=[state.upper() for state in states] or None,
        max_items=max_items,
    )
    _print_node_list(page, output_format)


def _print_node_list(page: NodeList, output_format: str) -> None:
    if output_format == OutputFormat.TEXT.value:
        print_text(page)
    elif output_format == OutputFormat.TABLE.value:
        print_output([table_row(node) for node in page.results], output_format, NODE_COLUMNS)
    else:
        print_output(page, output_format)
    if page.total > len(page.results):
        # stderr, so json / yaml on stdout stay parseable.
        click.echo(
            f"Showing {len(page.results)} of {page.total} nodes. Use --max-items to see more.",
            err=True,
        )


# --- gpus ------------------------------------------------------------------------------------


def _print_node(node: NodeGpus, output_format: str) -> None:
    if output_format == OutputFormat.TEXT.value:
        print_text(node)
        return
    if output_format == OutputFormat.TABLE.value:
        print_output([table_row(gpu) for gpu in node.gpus], output_format, GPU_COLUMNS)
        return
    print_output(node, output_format)


__all__: List[str] = ["NODE_COLUMNS", "get", "gpus", "list_nodes", "node_cli"]
