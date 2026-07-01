""" mcli stop Entrypoint """
import argparse
import logging
from typing import List, Optional

from mcli.api.exceptions import cli_error_handler
from mcli.api.inference_deployments.api_stop_inference_deployments import stop_inference_deployments
from mcli.api.runs.api_stop_runs import stop_runs
from mcli.cli.common.deployment_filters import get_deployments_with_filters
from mcli.cli.common.run_filters import configure_submission_filter_argparser, get_runs_with_filters
from mcli.cli.m_delete.delete import confirm_deployment_update, confirm_run_update
from mcli.utils.utils_logging import FAIL, OK, WARN
from mcli.utils.utils_run_status import RunStatus
from mcli.utils.utils_spinner import console_status

logger = logging.getLogger(__name__)


def stop_entrypoint(parser, **kwargs) -> int:
    del kwargs
    parser.print_help()
    return 0


def get_runs_to_stop(runs):
    stopped_runs = [r for r in runs if r.status.is_terminal()]

    # If there are runs that are already in a terminal state (stopped/completed/failed), log an error
    if len(stopped_runs) == 1:
        logger.error(f'{WARN} {stopped_runs[0].name} has already stopped or completed. '
                     f'Skipping stop request for this run')
    elif len(stopped_runs):
        logger.error(f'{WARN} {len(stopped_runs)} runs have already stopped or completed. '
                     f'Skipping stop request for these runs')

    return [r for r in runs if not r.status.is_terminal()]


@cli_error_handler('mcli stop run')
def stop_run(
    name_filter: Optional[List[str]] = None,
    cluster_filter: Optional[List[str]] = None,
    before_filter: Optional[str] = None,
    after_filter: Optional[str] = None,
    gpu_type_filter: Optional[List[str]] = None,
    gpu_num_filter: Optional[List[int]] = None,
    status_filter: Optional[List[RunStatus]] = None,
    stop_all: bool = False,
    latest: bool = False,
    force: bool = False,
    reason: Optional[str] = None,
    **kwargs,
) -> int:
    del kwargs

    runs = get_runs_with_filters(
        name_filter,
        cluster_filter,
        before_filter,
        after_filter,
        gpu_type_filter,
        gpu_num_filter,
        status_filter,
        latest,
        stop_all,
    )

    if not runs:
        extra = '' if stop_all else ' matching the specified criteria'
        logger.error(f'{WARN} No runs found{extra}.')
        return 1

    filtered_runs = get_runs_to_stop(runs)
    if len(filtered_runs) == 0:
        return 1

    if not force and not confirm_run_update(filtered_runs, 'stop'):
        logger.error(f'{FAIL} Canceling stop runs')
        return 1

    with console_status('Stopping runs...'):
        stop_runs(filtered_runs, reason=reason)

    logger.info(f'{OK} Stopped runs')
    return 0


@cli_error_handler('mcli stop deployment')
def stop_deployment(
    name_filter: Optional[List[str]] = None,
    old_name_filter: Optional[str] = None,
    cluster_filter: Optional[List[str]] = None,
    before_filter: Optional[str] = None,
    after_filter: Optional[str] = None,
    gpu_type_filter: Optional[List[str]] = None,
    gpu_num_filter: Optional[List[int]] = None,
    status_filter: Optional[List[str]] = None,
    force: bool = False,
    **kwargs,
):
    del kwargs

    if not name_filter and old_name_filter:
        name_filter = [old_name_filter]

    deployments = get_deployments_with_filters(
        name_filter,
        cluster_filter,
        before_filter,
        after_filter,
        gpu_type_filter,
        gpu_num_filter,
        status_filter,
    )

    if not deployments:

        logger.error(f'{WARN} No deployments found matching the specified criteria.')
        return 1
    if not force and not confirm_deployment_update(deployments, 'stop'):
        logger.error(f'{FAIL} Canceling stop deployments')
        return 1

    with console_status('Stopping deployments...'):
        stop_inference_deployments(deployments)

    logger.info(f'{OK} Stopped deployments')
    return 0


def add_stop_parser(subparser: argparse._SubParsersAction, is_admin: bool = False):
    """Add the parser for stop runs
    """

    stop_parser: argparse.ArgumentParser = subparser.add_parser(
        'stop',
        help='Stop objects created with mcli',
    )
    stop_parser.set_defaults(func=stop_entrypoint, parser=stop_parser)

    subparsers = stop_parser.add_subparsers(
        title='MCLI Objects',
        description='The table below shows the objects that you can stop',
        help='DESCRIPTION',
        metavar='OBJECT',
    )

    # Stop custom code runs
    stop_run_parser = subparsers.add_parser(
        'run',
        aliases=['runs'],
        help='Stop runs',
    )
    stop_run_parser.set_defaults(func=stop_run)

    stop_run_parser.add_argument(
        dest='name_filter',
        nargs='*',
        metavar='RUN',
        default=None,
        help='String or glob of the name(s) of the runs to stop',
    )

    if is_admin:
        stop_run_parser.add_argument('--reason', dest='reason', default=None, help='Reason for stopping the run')

    configure_submission_filter_argparser('stop', stop_run_parser)

    stop_run_parser.add_argument('-y',
                                 '--force',
                                 dest='force',
                                 action='store_true',
                                 help='Skip confirmation dialog before stopping runs')

    # Stop inference deployments
    stop_deployment_parser = subparsers.add_parser(
        'deployment',
        aliases=['deployments'],
        help='Stop deployments',
    )
    stop_deployment_parser.set_defaults(func=stop_deployment)

    stop_deployment_parser.add_argument(
        dest='name_filter',
        nargs='*',
        metavar='DEPLOYMENT',
        default=None,
        help='String or glob of the name(s) of the deployments to stop',
    )

    configure_submission_filter_argparser('stop', stop_deployment_parser)

    stop_deployment_parser.add_argument('-y',
                                        '--force',
                                        dest='force',
                                        action='store_true',
                                        help='Skip confirmation dialog before stopping deployments')

    return stop_parser
