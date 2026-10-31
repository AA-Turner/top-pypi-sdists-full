"""`anyscale node gpus`.

The `node` group holds the per-node views of a cluster. Today that is `gpus`, over the
backend's per-node DCGM endpoint; the backend checks read permission on the cluster.

Output is the model as the API returned it, in every format: text is the model as YAML
(like `anyscale job status`), table is one row per GPU with a column per field, json and
yaml are the model. Field names and values are not rewritten.

The group is `hidden=True` for now: it runs when typed, but is left out of `anyscale
--help`, the committed doc spec and the reference docs. Removing the flag (and the
matching one on the GPUs module in `_private/docgen/__main__.py`) publishes it.
"""

from typing import List, Optional

import click

import anyscale
from anyscale.commands.doc_metadata import CommandExample
from anyscale.commands.gpu_commands import (
    beta_metadata,
    GPU_COLUMNS,
    option_cluster_id,
    option_output,
    option_time,
    print_text,
    table_row,
)
from anyscale.commands.output_format import OutputFormat, print_output
from anyscale.commands.time_flags import parse_timestamp
from anyscale.commands.util import AnyscaleCommand
from anyscale.gpus.models import NodeGpus


@click.group("node", help="Inspect the nodes of a cluster.", hidden=True)
def node_cli() -> None:
    pass


@beta_metadata(
    CommandExample(
        description="Every GPU on a node with its DCGM telemetry, right now.",
        command="anyscale node gpus --cluster-id <cluster-id> --node-id <node-id>",
    ),
    CommandExample(
        description="The same node during an incident.",
        command=(
            "anyscale node gpus --cluster-id <cluster-id> --node-id <node-id> "
            "--time 2026-09-01T13:45:00Z"
        ),
    ),
    CommandExample(
        description="One row per GPU.",
        command="anyscale node gpus --cluster-id <cluster-id> --node-id <node-id> -o table",
    ),
)
@node_cli.command(name="gpus", cls=AnyscaleCommand, short_help="List the GPUs of a node.")
@option_cluster_id
@click.option("--node-id", required=True, help="ID of the node, e.g. nod_abc123.")
@option_time
@option_output
def gpus(cluster_id: str, node_id: str, time: Optional[str], output_format: str) -> None:
    """List the GPUs of a node of a cluster with their DCGM telemetry, sorted by index.

    The backend looks back over the cluster's lifetime (up to seven days), so a node that
    is already terminated or dead still lists its GPUs, as OFFLINE with their last-known
    telemetry.
    """
    node = anyscale.gpus.node_gpus(cluster_id, node_id, time=parse_timestamp(time, "--time"))
    _print_node(node, output_format)


def _print_node(node: NodeGpus, output_format: str) -> None:
    if output_format == OutputFormat.TEXT.value:
        print_text(node)
        return
    if output_format == OutputFormat.TABLE.value:
        print_output([table_row(gpu) for gpu in node.gpus], output_format, GPU_COLUMNS)
        return
    print_output(node, output_format)


__all__: List[str] = ["gpus", "node_cli"]
