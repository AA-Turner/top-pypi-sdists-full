"""Implementation of mcli get runs"""
from __future__ import annotations

import argparse
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Generator, List, Optional, Union

from mcli import config
from mcli.api.exceptions import cli_error_handler
from mcli.api.model.cluster_details import ClusterUtilizationByRun
from mcli.api.model.run import Resumption, Run
from mcli.cli.common.run_filters import configure_submission_filter_argparser, get_runs_with_filters
from mcli.cli.m_get.display import MCLIDisplayItem, MCLIGetDisplay, OutputDisplay
from mcli.utils.utils_cli import comma_separated
from mcli.utils.utils_date import format_timestamp
from mcli.utils.utils_logging import WARN, seconds_to_str
from mcli.utils.utils_run_status import RunStatus

DEFAULT_DISPLAY_LIMIT = 50

logger = logging.getLogger(__name__)

GPUS_PER_NODE = 8


@dataclass
class RunDisplayItem(MCLIDisplayItem):
    """Display items for runs
    """
    PROGRESS = [
        "□□□□□□□□□□", "■□□□□□□□□□", "■■□□□□□□□□", "■■■□□□□□□□", "■■■■□□□□□□", "■■■■■□□□□□", "■■■■■■□□□□", "■■■■■■■□□□",
        "■■■■■■■■□□", "■■■■■■■■■□", "■■■■■■■■■■"
    ]

    @classmethod
    def get_eta(cls, resumption: Union[Resumption, ClusterUtilizationByRun], run: Union[Run, ClusterUtilizationByRun],
                current_date: datetime) -> int:
        start_time = cls.get_start_time(run)
        if not start_time:
            return 0

        possible_end_times: List[float] = []
        if resumption.estimated_end_time:
            possible_end_times.append((resumption.estimated_end_time - current_date).total_seconds())
        if run.max_duration_seconds:
            expiration_date = start_time + \
                timedelta(seconds=run.max_duration_seconds)
            possible_end_times.append((expiration_date - current_date).total_seconds())

        possible_end_times = [eta for eta in possible_end_times if eta > 0]
        if len(possible_end_times) == 0:
            return 0

        seconds_left = min(possible_end_times)
        return int(seconds_left)

    @classmethod
    def get_start_time(cls, run: Union[Run, ClusterUtilizationByRun]) -> datetime | None:
        start_time = None
        if isinstance(run, Run):
            start_time = run.started_at
        else:
            start_time = run.start_time
        return start_time

    @classmethod
    def _get_run_progress(cls, eta: datetime, start_time: datetime) -> str:
        total_time = (eta - start_time).total_seconds()
        current_time = datetime.now(timezone.utc)
        elapsed_time = (current_time - start_time).total_seconds()
        percentage = min(int((elapsed_time / total_time) * 100), 100)
        return f"{cls.PROGRESS[int(percentage / 10)]}({percentage}%)"

    @classmethod
    def can_calculate_eta(cls, resumption: Union[Resumption, ClusterUtilizationByRun],
                          run: Union[Run, ClusterUtilizationByRun]) -> bool:
        if not cls.get_start_time(run):
            return False
        if resumption.estimated_end_time and resumption.estimated_end_time > datetime.now(timezone.utc):
            return True
        return run.max_duration_seconds is not None

    @classmethod
    def from_run(
        cls,
        run: Run,
        metadata_keys: List[str],
        include_ids: bool = False,
        expanded: bool = False,
    ) -> List[MCLIDisplayItem]:
        run_rows = []
        run.resumptions.sort(key=lambda resumption: resumption.index)

        for resumption in run.resumptions[::-1]:
            index = resumption.index
            display_status = resumption.status.display_name
            execution_reason = resumption.reason

            endtime_label = "End Time"
            end_time = resumption.ended_at
            status = f"{display_status} ({execution_reason})" if execution_reason else display_status
            seconds_left = None

            if resumption.status == RunStatus.RUNNING and not resumption.ended_at and cls.can_calculate_eta(
                    resumption, run):

                if not run.started_at:
                    logger.error(
                        f"Resumption of run {run.name} could not be displayed. Please contact support to resolve.")
                    continue  # for type checking only

                endtime_label = "ETA"
                current_date = datetime.now(timezone.utc)
                seconds_left = cls.get_eta(resumption, run, current_date)

                eta = current_date + timedelta(seconds=seconds_left)
                status = f"Running {cls._get_run_progress(eta, run.started_at)}"

            metadata_values = {}
            if metadata_keys and run.metadata:
                metadata_values = {key.split('/')[-1]: run.metadata.get(key, '-') for key in metadata_keys}
            else:
                metadata_values = {key.split('/')[-1]: '-' for key in metadata_keys}

            run_rows.append(
                MCLIDisplayItem({
                    'name': run.display_name if index == len(run.resumptions) - 1 else '',
                    'ID': run.run_uid if include_ids and index == len(run.resumptions) - 1 else '',
                    'User': run.created_by if index == len(run.resumptions) - 1 else '',
                    'Cluster': run.cluster if index == len(run.resumptions) - 1 else '',
                    'Nodes': run.node_count if index == len(run.resumptions) - 1 else '',
                    'Instance': get_instance_name(run) if index == len(run.resumptions) - 1 else '',
                    'Resumption': index,
                    'Status': status,
                    'Start Time': format_timestamp(resumption.started_at),
                    endtime_label: seconds_to_str(seconds_left) if seconds_left else format_timestamp(end_time),
                    **metadata_values,
                }))
            # only show the most recent 3 resumptions by default
            if not expanded and index == len(run.resumptions) - 3:
                break
        return run_rows


class MCLIRunDisplay(MCLIGetDisplay):
    """Display manager for runs
    """

    def __init__(
        self,
        models: List[Run],
        metadata_keys: List[str],
        include_ids: bool = False,
        include_users: bool = True,
        include_cluster: bool = True,
        expanded: bool = False,
    ):
        self.models = sorted(models, key=lambda x: x.created_at, reverse=True)
        self.include_ids = include_ids
        self.include_users = include_users
        self.include_cluster = include_cluster
        self.include_resumptions = any(len(m.resumptions) > 1 for m in self.models)
        self.expanded = expanded
        self.metadata_keys = metadata_keys

    def __iter__(self) -> Generator[MCLIDisplayItem, None, None]:
        for model in self.models:
            items = RunDisplayItem.from_run(model,
                                            include_ids=self.include_ids,
                                            expanded=self.expanded,
                                            metadata_keys=self.metadata_keys)
            for item in items:
                if not self.include_resumptions:
                    item.__setattr__('Resumption', None)
                if not self.include_ids:
                    item.__setattr__('ID', None)
                if not self.include_users:
                    item.__setattr__('User', None)
                if not self.include_cluster:
                    item.__setattr__('Cluster', None)
                yield item


def get_instance_name(run: Run) -> str:
    """Get the run's instance name

    We'll try to create a human-readable name based on the gpu number and type (ie 8x v100),
    if possible.

    Args:
        run (Run): a Run

    Returns:
        str: The instance name
    """

    gpu_type = run.gpu_type

    # Convert 'None' to 'cpu'
    if gpu_type.lower() == 'none':
        gpu_type = 'cpu'

    if gpu_type != 'cpu':
        gpus = int(run.gpus / run.node_count) if run.node_count > 0 else run.gpus

        # Prefer the gpu type as a description, if available
        return f"{gpus}x {gpu_type.lower()}"
    else:
        # Otherwise just use "cpu", which is the default value
        return gpu_type


@cli_error_handler('mcli get runs')
def cli_get_runs(
    name_filter: Optional[List[str]] = None,
    cluster_filter: Optional[List[str]] = None,
    before_filter: Optional[str] = None,
    after_filter: Optional[str] = None,
    gpu_type_filter: Optional[List[str]] = None,
    gpu_num_filter: Optional[List[int]] = None,
    status_filter: Optional[List[RunStatus]] = None,
    output: OutputDisplay = OutputDisplay.TABLE,
    include_ids: bool = False,
    latest: bool = False,
    user_filter: Optional[List[str]] = None,
    limit: Optional[int] = DEFAULT_DISPLAY_LIMIT,
    expanded: bool = False,
    metadata: Optional[List[str]] = None,
    include_deleted: bool = False,
    all_users: bool = False,
    **kwargs,
) -> int:
    """Get a table of ongoing and completed runs
    """
    del kwargs
    runs = get_runs_with_filters(
        name_filter=name_filter,
        cluster_filter=cluster_filter,
        before_filter=before_filter,
        after_filter=after_filter,
        gpu_type_filter=gpu_type_filter,
        gpu_num_filter=gpu_num_filter,
        status_filter=status_filter,
        latest=latest,
        user_filter=user_filter,
        limit=limit,
        all_users=all_users,
        include_details=metadata is not None,
        include_deleted=include_deleted,
    )

    include_users = all_users or (user_filter is not None and len(user_filter) > 1)
    include_cluster = cluster_filter is None or len(cluster_filter) != 1
    display = MCLIRunDisplay(runs,
                             include_ids=include_ids,
                             include_users=include_users,
                             include_cluster=include_cluster,
                             expanded=expanded,
                             metadata_keys=metadata if metadata else [])
    display.print(output)

    if len(runs) == DEFAULT_DISPLAY_LIMIT:
        logger.warning(f'{WARN} Run view shows only the last {DEFAULT_DISPLAY_LIMIT} runs and may be truncated. '
                       'Use --limit to increase the number of runs displayed.')
    return 0


def get_runs_argparser(subparsers: argparse._SubParsersAction):
    """Configures the ``mcli get runs`` argparser
    """

    run_examples: str = """Examples:
    $ mcli get runs

    NAME                         CLUSTER    GPU_TYPE      GPU_NUM      CREATED_TIME     USER               STATUS
    run-foo                      c-1        g0-type       8            05/06/22 1:58pm  abc@gmail.com      Completed
    run-bar                      c-2        g0-type       1            05/06/22 1:57pm  abc@gmail.com      Completed

    $ mcli get runs --user xyz@gmail.com
    NAME                         CLUSTER    GPU_TYPE      GPU_NUM      CREATED_TIME     USER               STATUS
    run-xyz-1                    c-1        g0-type       8            05/06/22 1:58pm  xyz@gmail.com      Completed
    run-xyz-2                    c-2        g0-type       1            05/06/22 1:57pm  xyz@gmail.com      Completed
    """
    runs_parser = subparsers.add_parser('runs',
                                        aliases=['run'],
                                        help='Get information on all of your existing runs across all clusters.',
                                        epilog=run_examples,
                                        formatter_class=argparse.RawDescriptionHelpFormatter)

    runs_parser.add_argument(
        dest='name_filter',
        nargs='*',  # Note: This will not work yet for `mcli get run logs <run>`. See deployments
        metavar='RUN',
        default=None,
        help='String or glob of the name(s) of the runs to get',
    )

    configure_submission_filter_argparser('get', runs_parser, include_all=False)
    runs_parser.set_defaults(func=cli_get_runs)

    runs_parser.add_argument(
        '--include-deleted',
        action='store_true',
        dest='include_deleted',
        default=config.ADMIN_MODE,  # Show all runs by default if admin
        help='Include runs that have been deleted')

    runs_parser.add_argument('--ids',
                             action='store_true',
                             dest='include_ids',
                             default=config.ADMIN_MODE,
                             help='Include the run ids in the output')

    def user(value: str):
        return comma_separated(value)

    user_group = runs_parser.add_mutually_exclusive_group()

    user_group.add_argument(
        '-u',
        '--user',
        dest='user_filter',
        default=None,
        metavar='User',
        type=user,
        help='Fetch the runs created by a user in your organization with their email address. '
        'Multiple users should be specified using a comma-separated list, '
        'e.g. "alice@gmail.com,bob@gmail.com"',
    )

    user_group.add_argument(
        '--all-users',
        action='store_true',
        help='Fetch the runs created by all users in your organization',
    )

    def limit(value: str) -> Optional[int]:
        if value.lower() == 'none':
            return None

        return int(value)

    runs_parser.add_argument(
        '--limit',
        help='Maximum number of runs to return. Runs will be sorted by creation time. '
        f'Default: {DEFAULT_DISPLAY_LIMIT}',
        default=DEFAULT_DISPLAY_LIMIT,
        type=limit,
    )

    runs_parser.add_argument('--expanded',
                             action='store_true',
                             dest='expanded',
                             help='Include all resumptions in the output, rather than the latest 3')

    runs_parser.add_argument("-m",
                             "--metadata",
                             action="append",
                             help="Metadata to display in the list. Multiple keys can be specified.")

    return runs_parser
