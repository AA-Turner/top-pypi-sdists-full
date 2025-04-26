""" MCLI Run Filters """
import argparse
import fnmatch
import functools
import logging
from typing import Dict, List, Optional, Tuple

from mcli.api.exceptions import MCLIException
from mcli.api.model.run import Run
from mcli.api.runs.api_get_runs import get_runs
from mcli.utils import utils_completers
from mcli.utils.utils_cli import comma_separated, date_time_parse
from mcli.utils.utils_model import SubmissionType
from mcli.utils.utils_run_status import RunStatus
from mcli.utils.utils_spinner import console_status
from mcli.utils.utils_string_functions import is_glob

logger = logging.getLogger(__name__)


def configure_submission_filter_argparser(action: str,
                                          parser: argparse.ArgumentParser,
                                          include_all: bool = True,
                                          submission_type: SubmissionType = SubmissionType.TRAINING) -> None:
    cluster_parser = parser.add_argument(
        '-c',
        '--cluster',
        '-p',
        '--platform',
        dest='cluster_filter',
        metavar='CLUSTER',
        type=comma_separated,
        default=None,
        help=f'{action.capitalize()} {submission_type.value}s on the specified cluster(s). If no other arguments are '
        f'provided, will {action} all {submission_type.value}s on the specified cluster(s). Multiple clusters '
        'should be specified using a comma-separated list, e.g. "cluster1,cluster2"',
    )
    cluster_parser.completer = utils_completers.ClusterNameCompleter()  # pyright: ignore

    parser.add_argument(
        '--before',
        dest='before_filter',
        metavar='DATE/TIME',
        nargs='?',
        type=date_time_parse,
        help=f'{action.capitalize()} {submission_type.value}s created before specific time. Datetimes must be '
        'surrounded by \'\'. e.g 2023-01-01 or 01-13-2023 or 12:30:23.4 or \'01-13-2023 19:20:21.9\'',
    )
    parser.add_argument(
        '--after',
        dest='after_filter',
        metavar='DATE/TIME',
        nargs='?',
        type=date_time_parse,
        help=f'{action.capitalize()} {submission_type.value}s created after specific time. Datetimes must be '
        'surrounded by \'\'. e.g 2023-01-01 or 01-13-2023 or 12:30:23.4 or \'01-13-2023 19:20:21.9\'',
    )
    gpu_type_parser = parser.add_argument(
        '-t',
        '--gpu-type',
        dest='gpu_type_filter',
        metavar='GPU',
        default=None,
        type=comma_separated,
        help=f'{action.capitalize()} {submission_type.value}s with specific GPU type. '
        'Multiple types should be specified using a comma-separated list, e.g. "a100_40gb,v100_16gb"',
    )
    gpu_type_parser.completer = utils_completers.GPUTypeCompleter()  # pyright: ignore

    parser.add_argument(
        '-n',
        '--gpu-num',
        dest='gpu_num_filter',
        metavar='# GPUs',
        default=None,
        type=functools.partial(comma_separated, fun=int),
        help=f'{action.capitalize()} {submission_type.value}s with specific number of GPUs. '
        'Multiple values should be specified using a comma-separated list, e.g. "1,8"',
    )

    def status(value: str):
        if submission_type is SubmissionType.TRAINING:
            res = comma_separated(value, RunStatus.from_string)
            if res == [RunStatus.UNKNOWN] and value != [RunStatus.UNKNOWN.value]:
                raise TypeError(f'Unknown value {value}')
            return res
        else:
            res = comma_separated(value)
            return res

    status_parser = parser.add_argument(
        '-s',
        '--status',
        dest='status_filter',
        default=None,
        metavar='STATUS',
        type=status,
        help=f'{action.capitalize()} {submission_type.value}s with the specified statuses (choices: '
        f'{", ".join(SubmissionType.get_status_options(submission_type))}). Multiple statuses should be specified '
        'using a comma-separated list, e.g. "failed,pending"',
    )
    if submission_type is SubmissionType.TRAINING:
        status_parser.completer = utils_completers.RunStatusCompleter()  # pyright: ignore
    else:
        status_parser.completer = utils_completers.DeploymentStatusCompleter()  # pyright: ignore

    if submission_type is SubmissionType.TRAINING:
        parser.add_argument(
            '-l',
            '--latest',
            action='store_true',
            dest='latest',
            default=False,
            help=f'Connect to the latest {submission_type.value}',
        )

    if include_all:
        parser.add_argument(
            '-a',
            '--all',
            dest=f'{action}_all',
            action='store_true',
            help=f'{action} all {submission_type.value}s',
        )


def _split_glob_filters(filters: List[str]) -> Tuple[List[str], List[str]]:
    """Split a list of filters into glob-containing and non-glob-containing filters
    """

    globbers: List[str] = []
    non_globbers: Optional[List[str]] = []
    for f in filters:
        if is_glob(f):
            globbers.append(f)
        else:
            non_globbers.append(f)

    return globbers, non_globbers


def get_runs_with_filters(
    name_filter: Optional[List[str]] = None,
    cluster_filter: Optional[List[str]] = None,
    before_filter: Optional[str] = None,
    after_filter: Optional[str] = None,
    gpu_type_filter: Optional[List[str]] = None,
    gpu_num_filter: Optional[List[int]] = None,
    status_filter: Optional[List[RunStatus]] = None,
    latest: bool = False,
    action_all: Optional[bool] = None,
    user_filter: Optional[List[str]] = None,
    limit: Optional[int] = None,
    all_users: bool = False,
    include_details: bool = False,
    include_deleted: bool = False,
) -> List[Run]:

    filter_used = any([
        name_filter,
        before_filter,
        after_filter,
        cluster_filter,
        gpu_type_filter,
        gpu_num_filter,
        status_filter,
        latest,
        user_filter,
    ])
    if not filter_used:
        if action_all is False:
            raise MCLIException('Must specify at least one filter or --all')

    if not name_filter:
        # Accept all that pass other filters
        name_filter = []

    # Use get_runs only for the non-glob names provided
    glob_filters, run_names = _split_glob_filters(name_filter)

    # If we're getting the latest run, we only need to get one
    if latest:
        limit = 1

    with console_status('Retrieving requested runs...'):
        runs = get_runs(
            runs=(run_names or None) if not glob_filters else None,
            cluster_names=cluster_filter,
            user_emails=user_filter,
            before=before_filter,
            after=after_filter,
            gpu_types=gpu_type_filter,
            gpu_nums=gpu_num_filter,
            statuses=status_filter,
            timeout=None,
            limit=limit,
            all_users=all_users,
            include_details=include_details,
            include_deleted=include_deleted,
        )

    if glob_filters:
        found_runs: Dict[str, Run] = {r.name: r for r in runs}

        # Any globs will be handled by additional client-side filtering
        filtered = set()
        for pattern in glob_filters:
            for match in fnmatch.filter(found_runs, pattern):
                filtered.add(match)

        expected_names = set(run_names)
        for run_name in found_runs:
            if run_name in expected_names:
                filtered.add(run_name)

        return [found_runs[r] for r in filtered]

    return list(runs)
