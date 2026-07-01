"""Implementation of mcli describe deployment"""
import logging
from typing import Dict, Generator, List, Optional

from rich import print as rprint
from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table

from mcli.api.exceptions import MAPIException
from mcli.api.inference_deployments.api_get_inference_deployments import get_inference_deployment
from mcli.api.model.inference_deployment import InferenceDeployment, InferenceDeploymentReplica
from mcli.cli.m_get.display import MCLIDisplayItem, MCLIGetDisplay, OutputDisplay, create_vertical_display_table
from mcli.cli.m_get.inference_deployments import K8S_REPLICA_HASH_LENGTH
from mcli.utils.utils_date import format_timestamp
from mcli.utils.utils_logging import FAIL, FormatString, format_string

logger = logging.getLogger(__name__)


# Displays
class MCLIDescribeDeploymentMetadataDisplay(MCLIGetDisplay):
    """ Vertical table view of inference deployment metadata """

    def __init__(self, models: List[InferenceDeployment]):
        self.models = sorted(models, key=lambda x: x.created_at, reverse=True)

    @property
    def index_label(self) -> str:
        return ""

    def create_custom_table(self, data: List[Dict[str, str]]) -> Optional[Table]:
        return create_vertical_display_table(data=data[0])

    def __iter__(self) -> Generator[MCLIDisplayItem, None, None]:
        for model in self.models:
            config = model.config
            item = MCLIDisplayItem({
                'Inference Deployment Name': model.name,
                'Address': model.public_dns,
                'Image': config.image,
                'Cluster': config.cluster,
                'GPU Num': config.gpu_num,
                'GPU Type': config.gpu_type,
                'Replicas': config.replicas,
                'Metadata': config.metadata,
                'Current Release': model.current_version
            })
            yield item


class MCLIReplicaDisplay():
    """ Panel view of replica details """

    def __init__(self, model: InferenceDeployment):
        self.model = model

    def print(self):
        # Build the visual panels for Replica details
        panels = []
        for ind in range(self.model.config.replicas):
            replica = self.model.replicas[ind] if self.model.replicas else None
            panels.append(create_replica_panel(replica))
        rprint(Columns(panels))
        print()


def format_restarts(replica: Optional[InferenceDeploymentReplica]) -> str:
    if not replica:
        return 'Not started yet'
    elif replica.latest_restart_count > 0:
        return (f'{replica.latest_restart_count} restarts, '
                f'Last restart at {format_timestamp(replica.latest_restart_time)}')
    else:
        return f'Started at {format_timestamp(replica.latest_restart_time)}'


def create_replica_panel(replica: Optional[InferenceDeploymentReplica] = None) -> Panel:
    """ Creates a panel for replica details """
    panel_string = replica.status.lower().capitalize() if replica else 'Pending'
    name = f"[bold]Replica Name: [/bold]{replica.name[-K8S_REPLICA_HASH_LENGTH:] if replica else ''}\n"
    restarts = f"Restarts: {replica.latest_restart_count if replica else 0}"
    last_restart = format_restarts(replica)
    return Panel(f"{name}\n\n{restarts}\n{last_restart}", expand=True, width=40, title=panel_string)


def describe_deploy(deployment_name: str, output: OutputDisplay = OutputDisplay.TABLE, **kwargs):
    """
    Fetches more details of a Inference Deployment
    """
    del kwargs

    try:
        deployment = get_inference_deployment(deployment_name)
    except MAPIException as e:
        logger.error(f'{FAIL} {e}')
        return 1

    # Deployment metadata section
    print(format_string('Inference Deployment Metadata', FormatString.BOLD))
    metadata_display = MCLIDescribeDeploymentMetadataDisplay([deployment])
    metadata_display.print(output)
    print()

    #Replica details section
    print(format_string('Replica Details', FormatString.BOLD))
    replica_display = MCLIReplicaDisplay(deployment)
    replica_display.print()
    print()

    # Deployment original input section
    print(format_string('Submitted YAML', FormatString.BOLD))
    print(deployment.submitted_config)
