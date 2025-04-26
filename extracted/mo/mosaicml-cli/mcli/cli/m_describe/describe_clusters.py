"""Implementation of mcli describe cluster"""
from __future__ import annotations

import logging
from http import HTTPStatus
from typing import Dict, Generator, List, Optional

from rich import print as rprint
from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table

from mcli.api.cluster.api_get_clusters import get_clusters
from mcli.api.exceptions import MAPIException, cli_error_handler
from mcli.api.model.cluster_details import ClusterDetails, Instance
from mcli.cli.m_get.display import MCLIDisplayItem, MCLIGetDisplay, OutputDisplay, create_vertical_display_table
from mcli.models.common import ObjectList
from mcli.utils.utils_logging import FormatString, format_string

logger = logging.getLogger(__name__)


class MCLIDescribeClusterDetailsDisplay(MCLIGetDisplay):
    """ Vertical table view of cluster details """

    def __init__(self, models: ObjectList[ClusterDetails]):
        self.models = models

    @property
    def index_label(self) -> str:
        return ""

    def create_custom_table(self, data: List[Dict[str, str]]) -> Optional[Table]:
        return create_vertical_display_table(data=data[0])

    def __iter__(self) -> Generator[MCLIDisplayItem, None, None]:
        for model in self.models:
            item = MCLIDisplayItem({
                'Name':
                    model.name,
                'ID':
                    model.id,
                'Allowed Submission Types':
                    ', '.join([type.name.lower().capitalize() for type in model.submission_types]),
                'Cloud Provider':
                    model.provider,
                'Is Multitenant':
                    model.is_multitenant,
                'Priority and Preemption Enabled':
                    model.scheduler_enabled,
                'Multinode Training Enabled':
                    model.allow_multinode,
                'Fractional Training Enabled':
                    model.allow_fractional,
                'Reservation Type':
                    model.reservation_type or 'Unspecified',
            })
            yield item


class MCLIInstanceDisplay():
    """ Panel view of instance details """

    def __init__(self, model: List[Instance]):
        self.model = model

    def print(self):
        # Build the visual panels for Instance details
        all_columns = []
        curr_columns = []
        count = 0
        total_gpus = sum(instance.gpus * instance.nodes for instance in self.model)
        total_nodes = sum(instance.nodes for instance in self.model)
        print(f'Total Nodes: {total_nodes}')
        print(f'Total GPUs: {total_gpus}')

        for instance in self.model:
            if count % 3 == 0 and count != 0:
                all_columns.append(Columns(curr_columns))
                curr_columns = [create_instance_panel(instance)]
            else:
                curr_columns.append(create_instance_panel(instance))
            count += 1
        all_columns.append(Columns(curr_columns))

        for col in all_columns:
            rprint(col)
            print()


def create_instance_panel(instance: Instance) -> Panel:
    """ Creates a panel for instance details """
    if len(instance.name) > 20:
        instance.name = instance.name[:17] + "..."
    instance_details = f"[bold]Instance Name: [/bold]{instance.name}\n[bold]GPU Type: [/bold]{instance.gpu_type}"
    gpu_string = f"GPUs: {instance.gpus*instance.nodes}"
    nodes = instance.nodes
    node_string = f"Nodes: {nodes}"
    per_node = "\n\n\n"
    gpus_per_node = f"GPUs: {instance.gpus}"
    cpus_per_node = f"CPUs: {instance.cpus if instance.cpus is not None else 0}"
    storage_per_node = f"Storage: {instance.storage}"
    memory_per_node = f"RAM: {instance.memory}"
    per_node = f"[bold]Per Node: [/bold]\n{gpus_per_node}\n{cpus_per_node}\n{storage_per_node}\n{memory_per_node}"
    return Panel(f"{instance_details}\n\n{node_string}\n{gpu_string}\n\n{per_node}", expand=True, width=40)


class MCLIInstanceNodeDisplay(MCLIGetDisplay):
    """Display manager for nodes
    """

    def __init__(self, models: List[Instance]):
        self.models = models

    @property
    def index_label(self) -> str:
        return "Name"

    def __iter__(self) -> Generator[MCLIDisplayItem, None, None]:
        for model in self.models:
            for node in model.node_details:
                item = MCLIDisplayItem({
                    'Name': node.name,
                    'Instance': model.name,
                    'Status': 'Alive' if node.is_alive else 'Dead',
                    'Schedulable': node.is_schedulable,
                })
                yield item


@cli_error_handler("mcli describe cluster")
def describe_cluster(cluster_name: str | None, output: OutputDisplay = OutputDisplay.TABLE, **kwargs):
    """
    Fetches more details of a Cluster
    """
    del kwargs

    cluster = get_clusters()
    if cluster_name is None and len(cluster) > 1:
        raise MAPIException(
            HTTPStatus.BAD_REQUEST,
            f'Multiple clusters found. Please specify one of the following: {", ".join([c.name for c in cluster])}',
        )

    if cluster_name is not None:
        cluster = get_clusters(clusters=[cluster_name])

    if not cluster:
        raise MAPIException(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            f'Cluster {cluster_name} not found.',
        )

    # Cluster details section
    print(format_string('Cluster Details', FormatString.BOLD))
    cluster_details_display = MCLIDescribeClusterDetailsDisplay(cluster)
    cluster_details_display.print(output)
    print()

    # Instance details section
    instances = cluster[0].cluster_instances
    instance_display = MCLIInstanceDisplay(instances)
    instance_display.print()
    print()

    # Node details section
    print(format_string('Node Details', FormatString.BOLD))
    display = MCLIInstanceNodeDisplay(instances)
    display.print(output)
