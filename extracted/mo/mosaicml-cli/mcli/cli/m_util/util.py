""" mcli util helpers """

import logging
from datetime import datetime, timezone
from http import HTTPStatus
from typing import Any, Dict, Generator, List, Optional, Union

import yaml
from rich.style import Style
from rich.table import Table

from mcli.api.cluster import get_clusters
from mcli.api.exceptions import MAPIErrorMessages, MAPIException, MCLIException, cli_error_handler
from mcli.api.model.cluster_details import ClusterDetails, ClusterUtilizationByDeployment, ClusterUtilizationByRun
from mcli.cli.m_get.display import MCLIDisplayItem, MCLIGetDisplay, OutputDisplay
from mcli.cli.m_get.runs import RunDisplayItem
from mcli.utils.utils_logging import print_timedelta, seconds_to_str
from mcli.utils.utils_model import SubmissionType

logger = logging.getLogger(__name__)


def get_row_color(node: dict) -> Optional[str]:
    """Get the row color using the serialized NodeInfo data
    """
    gpus_used = int(node.get("gpus_used", 0))
    gpus_available = int(node.get("gpus_available", 0))

    if gpus_used == 0 and gpus_available == 0:
        return "bright_black"  # gray

    if gpus_available == 0:
        return "red"

    if gpus_available > 0:
        return "green"

    return None


class SubmissionUtilizationDisplay(MCLIGetDisplay):
    """Display information about the node for submissions
    """

    @property
    def index_label(self) -> str:
        if self.num_clusters == 1:
            if self.submission_type is SubmissionType.INFERENCE:
                return "deployment_name"
            else:
                return "run_name" if self.is_active else "pos"
        else:
            return "name"

    def __init__(self,
                 clusters: List[ClusterDetails],
                 is_active=True,
                 preemptible: Optional[bool] = None,
                 submission_type: SubmissionType = SubmissionType.TRAINING):
        self.clusters = clusters
        self.num_clusters = len({i.name for i in clusters})
        self.is_active = is_active
        self.preemptible = preemptible
        self.submission_type = submission_type

    def format_active_submission_name(self, r: Union[ClusterUtilizationByRun, ClusterUtilizationByDeployment]) -> str:
        return f'[cyan]{r.display_name}[/]'

    def format_pending_submission_name(self, r: Union[ClusterUtilizationByRun, ClusterUtilizationByDeployment]) -> str:
        return f'[yellow]{r.display_name}[/]'

    def format_priority(self, priority: Optional[str]) -> str:
        if not priority or priority == 'DEFAULT':
            return 'medium'
        return priority.lower()

    def get_list(self) -> List[Dict[str, Any]]:
        items = super().get_list()
        if not self.is_active:
            # Pending submissions should have the index included
            return items
        # Remove 'pos' from active submissions
        for item in items:
            item.pop('pos', None)
        return items

    def _check_for_eta(self) -> bool:
        for cluster in self.clusters:
            assert cluster.utilization
            submissions = cluster.utilization.get_submissions(self.submission_type, self.is_active, self.preemptible)
            for submission in submissions:
                if isinstance(submission, ClusterUtilizationByRun) and RunDisplayItem.can_calculate_eta(
                        submission, submission):
                    return True

        return False

    def __iter__(self) -> Generator[MCLIDisplayItem, None, None]:
        # if there are no estimated time stamps on this cluster, don't show the ETA column at all.
        has_estimated_timestamp = self._check_for_eta()
        for cluster in self.clusters:
            assert cluster.utilization
            submissions = cluster.utilization.get_submissions(self.submission_type, self.is_active, self.preemptible)

            for i, by_user in enumerate(submissions):
                cluster_name = cluster.name
                if self.num_clusters == 1:
                    # Exclude cluster name from table completely when there's only one cluster
                    cluster_name = None
                elif i > 0:
                    # Skip cluster name if it was the same as the previous
                    cluster_name = ''

                if self.is_active:
                    name = self.format_active_submission_name(by_user)
                else:
                    name = self.format_pending_submission_name(by_user)

                if self.submission_type is SubmissionType.TRAINING:
                    # A priority value may not exist, so default it
                    priority = self.format_priority(by_user.scheduling.get('priority', None))

                    mcli_display_item_init = {
                        "pos": i + 1,
                        "name": cluster_name,
                        "run_name": name,
                        "user": by_user.user,
                        "age": print_timedelta(datetime.now(timezone.utc) - by_user.created_at),
                        "gpus": by_user.gpu_num,
                        "priority": priority
                    }

                    # we already know that this is a ClusterUtilizationByRun since the submission type
                    # is TRAINING. this simply avoids a pyright error
                    if isinstance(by_user, ClusterUtilizationByDeployment):
                        raise MCLIException("ETA and reason can only be used on training runs.")
                    # Add reason only for queued runs where reason is known
                    if not self.is_active:
                        mcli_display_item_init["reason"] = by_user.reason if by_user.reason else ''

                    if has_estimated_timestamp and RunDisplayItem.can_calculate_eta(by_user, by_user):
                        eta = RunDisplayItem.get_eta(by_user, by_user, datetime.now(timezone.utc))
                        if RunDisplayItem.can_calculate_eta(by_user, by_user) and eta:
                            mcli_display_item_init["ETA"] = seconds_to_str(eta)
                        else:
                            mcli_display_item_init["ETA"] = '-'

                    yield MCLIDisplayItem(mcli_display_item_init)
                else:
                    yield MCLIDisplayItem({
                        "name": cluster_name,
                        "deployment_name": name,
                        "user": by_user.user,
                        "age": print_timedelta(datetime.now(timezone.utc) - by_user.created_at),
                        "gpus": by_user.gpu_num,
                    })


class ClusterDisplay(MCLIGetDisplay):
    """Display information about the node
    """

    def __init__(self, clusters: List[ClusterDetails]):
        self.clusters = sorted(clusters)
        self.num_clusters = len({i.name for i in clusters})

    def __iter__(self) -> Generator[MCLIDisplayItem, None, None]:
        for cluster in self.clusters:
            assert cluster.utilization
            cluster_name = cluster.name
            valid_instances_displayed = 0
            for inst in cluster.utilization.cluster_instance_utils:
                if inst.instance.gpu_type == "None":
                    continue
                if valid_instances_displayed > 0:
                    cluster_name = ''
                valid_instances_displayed += 1
                yield MCLIDisplayItem({
                    "name": cluster_name,
                    "instance_name": inst.instance.name,
                    "node_info": str(inst.instance.gpus) + "x" + inst.instance.gpu_type,
                    "gpus_available": inst.gpus_available,
                    "gpus_used": inst.gpus_used,
                    "gpus_total": inst.gpus_total,
                })

    def to_table(self, items: List[Dict[str, Any]]) -> Table:
        """Overrides MCLIGetDisplay.to_table to have custom node colors by row using rich style
        """

        def _to_str(obj: Any) -> str:
            return yaml.safe_dump(obj, default_flow_style=None).strip() if not isinstance(obj, str) else obj

        column_names = [key for key, val in items[0].items() if val and key != 'name']

        data_table = Table(box=None, pad_edge=False)
        data_table.add_column('NAME', justify='left', no_wrap=True)

        for column_name in column_names:
            data_table.add_column(column_name.upper())

        for item in items:
            row_args = {}
            data_row = tuple(_to_str(item[key]) for key in column_names)
            color = get_row_color(item)
            if color is not None:
                row_args["style"] = Style(color=color)
            data_table.add_row(item['name'], *data_row, **row_args)

        return data_table


@cli_error_handler('mcli util')
def get_util(clusters: Optional[List[str]] = None,
             hide_users: bool = False,
             training: bool = False,
             inference: bool = False,
             include_all: bool = False,
             **kwargs) -> int:

    submission_type_filter = None
    if training:
        submission_type_filter = SubmissionType.TRAINING
    elif inference:
        submission_type_filter = SubmissionType.INFERENCE

    if not clusters and not inference and not training:
        # The default "mcli util" is to show only training clusters
        # If a user specifies inference clusters or a cluster by name, then don't apply this filter
        submission_type_filter = SubmissionType.TRAINING

    del kwargs
    try:
        c = get_clusters(
            clusters=clusters,
            include_utilization=True,
            include_all=include_all,
            submission_type_filter=submission_type_filter,
        )
    except MAPIException as e:
        if e.status == HTTPStatus.NOT_FOUND:
            e.message = MAPIErrorMessages.NOT_FOUND_CLUSTER.value
        raise e

    if len(c) == 0:
        raise MAPIException(HTTPStatus.NOT_FOUND, f'No clusters found with name(s): {clusters}')

    if submission_type_filter is None:
        submission_types_list = [SubmissionType.TRAINING]
    else:
        submission_types_list = [submission_type_filter]

    for i, submission_type in enumerate(submission_types_list):
        submission_cluster = [cluster for cluster in c if submission_type in cluster.submission_types]
        if len(submission_cluster) == 0:
            continue
        agg = ''
        if len({cluster.name for cluster in submission_cluster}) > 1:
            agg = ' by Cluster'

        print(f'{submission_type.name.capitalize()} Instances{agg}:')
        cluster_display = ClusterDisplay(submission_cluster)
        cluster_display.print(OutputDisplay.TABLE)

        if not hide_users:
            print(f'\nActive Non-Preemptible {submission_type.value}s{agg}:')
            active_display = SubmissionUtilizationDisplay(submission_cluster,
                                                          submission_type=submission_type,
                                                          is_active=True,
                                                          preemptible=False)
            active_display.print(OutputDisplay.TABLE)

            print(f'\nActive Preemptible {submission_type.value}s{agg}:')
            active_display = SubmissionUtilizationDisplay(submission_cluster,
                                                          submission_type=submission_type,
                                                          is_active=True,
                                                          preemptible=True)
            active_display.print(OutputDisplay.TABLE)

            print(f'\nQueued {submission_type.value}s{agg}:')
            queued_display = SubmissionUtilizationDisplay(submission_cluster,
                                                          submission_type=submission_type,
                                                          is_active=False)
            queued_display.print(OutputDisplay.TABLE)

        if i < len(submission_types_list) - 1:
            print("\n")
    return 0
