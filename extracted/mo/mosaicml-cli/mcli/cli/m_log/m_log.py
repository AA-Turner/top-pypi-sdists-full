"""mcli logs entrypoint"""
from __future__ import annotations

import argparse
import logging
import os
import sys
import warnings
from functools import partial
from http import HTTPStatus
from typing import List, Optional, Tuple, Union

from mcli.api.exceptions import MAPIException
from mcli.api.inference_deployments.api_get_inference_deployment_logs import get_inference_deployment_logs
from mcli.api.model.inference_deployment import InferenceDeployment
from mcli.api.model.run import Run
from mcli.api.runs.api_get_run_logs import follow_run_logs, get_run_logs
from mcli.api.runs.api_watch_run import EpilogSpinner as CloudEpilogSpinner
from mcli.cli.common.deployment_filters import get_deployments_with_filters
from mcli.cli.common.run_filters import get_runs_with_filters
from mcli.utils import utils_completers
from mcli.utils.utils_logging import FAIL, INFO, err_console
from mcli.utils.utils_model import SubmissionType
from mcli.utils.utils_run_status import RunStatus

logger = logging.getLogger(__name__)

# pylint: disable-next=invalid-name
RUN_LOG_EXAMPLES = """

Examples:

# View the current logs of an ongoing run
> mcli logs run-1234

# By default, if you don't specify the run name the logs for the latest run will be retrieved
> mcli logs

# View the logs of a specific node in a multi-node run
> mcli logs multinode-run-1234 --rank 1 # note: --rank will be deprecated in a future release
OR
> mcli logs multinode-run-1234 --node 1
OR
> mcli logs multinode-run-1234 --node-rank 1

# View the logs of a specific GPU in a run. Note: GPU rank logs are only available for runs using Composer and/or LLM Foundry.
> mcli logs multinode-run-1234 --node 1 --gpu 1
OR
> mcli logs multinode-run-1234 --global-gpu-rank 9

# Follow the logs for an ongoing run
> mcli logs run-1234 --follow

# View the logs for a failed run
> mcli logs run-1234 --failed

# View the logs for the run's first initial resumption
> mcli logs run-1234 --resumption 0

# View the logs for the run's previous resumption
> mcli logs run-1234 --prev

# View the exception for the first GPU that failed for a run
> mcli logs run-1234 --first-exception
"""

# pylint: disable-next=invalid-name
DEPLOYMENT_LOG_EXAMPLES = """

Examples:

# View the current logs of an ongoing deployment
> mcli get deployment logs deploy-1234

# By default, the logs for the latest deployment will be retrieved
> mcli get deployment logs

# View the logs of a specific restart in a deployment
> mcli get deployment logs deploy-1234 --restart 5

# View the logs for a failed deployment
> mcli get deployment logs deploy-1234 --failed
"""


def _get_run_logs(
    run: Run,
    follow: bool,
    node_rank: Optional[int],
    local_gpu_rank: Optional[int],
    global_gpu_rank: Optional[int],
    first_exception: bool,
    failed: bool,
    resumption: Optional[int],
    prev: bool,
    tail: Optional[int],
    container: Optional[str] = None,
) -> Tuple[Optional[str], int]:
    if prev:
        if run.resumption_count == 1:
            logger.error(f'{FAIL} Cannot get previous resumption because the run has only executed once.')
            return '', 1
        resumption = run.resumption_count - 2
    elif resumption is None:
        resumption = run.resumption_count - 1
    elif resumption >= run.resumption_count or resumption < 0:
        logger.error(f'{FAIL} Run only has {run.resumption_count} resumptions. '\
            f'Resumption must be non-negative and <= {run.resumption_count-1}.')
        return '', 1
    chosen_resumption = sorted(run.resumptions, key=lambda x: x.index)[resumption]
    # should return reason in resumption; we must get from lifecycle for now
    lifecycle = sorted(run.lifecycle, key=lambda x: x.resumption_index)[resumption]
    is_specific_rank_requested = node_rank is not None or local_gpu_rank is not None or global_gpu_rank is not None

    # failed and first exception are mutually exclusive
    if failed and first_exception:
        logger.error(f'{FAIL} Cannot use both --failed and --first-exception.')
        return '', 1

    if chosen_resumption.status == RunStatus.FAILED and not failed and not is_specific_rank_requested:
        if lifecycle.reason and lifecycle.reason == "FailedImagePull":
            suggestion = f'Try `mcli describe run {run.name}` and double-check that your image name is correct.'
            logger.info(
                f'{INFO} Run {run.name} has failed during image pull, so there are likely no logs. {suggestion}')
            return '', 0
        else:
            err_message = f'({lifecycle.reason})' if lifecycle.reason else ''
            if not first_exception:
                logger.info(
                    f'{INFO} Run {run.name} has failed. {err_message} Defaulting to show the first failed node rank.')
        failed = True

    # follow and first exception are mutually exclusive
    if follow and first_exception:
        logger.error(f'{FAIL} Cannot use both --follow and --first-exception.')
        return '', 1

    # will only go through the following if statements if chosen_resumption is the current one
    if follow and chosen_resumption.status.before(RunStatus.RUNNING):
        with CloudEpilogSpinner(run, RunStatus.RUNNING) as watcher:
            run = watcher.follow()

    elif chosen_resumption.status.before(RunStatus.QUEUED, inclusive=True):
        # Pod still waiting to be scheduled. Return
        logger.error(f'{FAIL} Run {run.name} has not been scheduled')
        return '', 1
    elif chosen_resumption.status.before(RunStatus.RUNNING):
        # Pod still not running, probably because follow==False
        logger.error(f'{FAIL} Run has not yet started. You can check the status with `mcli get runs` '
                     'and try again later.')
        return '', 1

    last_line: Optional[str] = None
    end: str = ''
    if follow:
        for line in follow_run_logs(run,
                                    resumption=resumption,
                                    tail=tail,
                                    container=container,
                                    node_rank=node_rank,
                                    local_gpu_rank=local_gpu_rank,
                                    global_gpu_rank=global_gpu_rank):
            print(line, end=end)
            if line:
                last_line = line
        return last_line, int(0)
    else:
        log_lines = get_run_logs(run,
                                 failed=failed,
                                 resumption=resumption,
                                 tail=tail,
                                 container=container,
                                 node_rank=node_rank,
                                 first_exception=first_exception,
                                 local_gpu_rank=local_gpu_rank,
                                 global_gpu_rank=global_gpu_rank)
        for line in log_lines:
            # When using progress bars we randomly get newlines added. By default,
            # kubernetes does not return empty lines when streaming, which is
            # replicated in `follow_run_logs`. We'll do that here for parity
            if line:
                last_line = line
                print(line, end='')
        return last_line, int(0)


def _get_deployment_logs(deploy: InferenceDeployment, follow: bool, restart: Optional[int], failed: bool,
                         tail: Optional[int]) -> Tuple[Optional[str], int]:
    log_lines = get_inference_deployment_logs(deploy, restart=restart, failed=failed, follow=follow, tail=tail)
    last_line: Optional[str] = None
    for line in log_lines:
        # When using progress bars we randomly get newlines added. By default,
        # kubernetes does not return empty lines when streaming, which is
        # replicated in `follow_run_logs`. We'll do that here for parity
        if line:
            last_line = line
            print(line, end='')
    return last_line, 0


def get_with_filters(submission_type: SubmissionType,
                     name: Optional[str] = None,
                     latest: bool = False) -> Union[List[Run], List[InferenceDeployment]]:
    name_filter = [name] if name else None
    if submission_type is SubmissionType.TRAINING:
        return get_runs_with_filters(name_filter=name_filter, latest=latest, include_details=True, include_deleted=True)
    else:
        return get_deployments_with_filters(name_filter=name_filter)


# pylint: disable-next=too-many-statements
def get_logs(
    submission_type: SubmissionType,
    submission_name: Optional[str] = None,
    node_rank: Optional[int] = None,
    local_gpu_rank: Optional[int] = None,
    global_gpu_rank: Optional[int] = None,
    first_exception: bool = False,
    restart: Optional[int] = None,
    follow: bool = False,
    failed: bool = False,
    resumption: Optional[int] = None,
    prev: bool = False,
    tail: Optional[int] = None,
    container: Optional[str] = None,
    **kwargs,
) -> int:
    del kwargs

    if tail is not None and tail < 0:
        logger.error(f'{FAIL} --tail must be non-negative')
        return 1

    try:
        submission_type_str = submission_type.value.lower()
        with err_console.status(f'Getting {submission_type_str} details...') as spinner:
            if submission_name is None:
                spinner.update(f'No {submission_type_str} name provided. Finding latest {submission_type_str}'
                               f'...')
                submissions = get_with_filters(submission_type, submission_name, latest=True)
                if not submissions:
                    raise MAPIException(status=HTTPStatus.NOT_FOUND, message=f'No {submission_type_str} found')
                logger.info(
                    f'{INFO} No {submission_type_str} name provided. Displaying log of latest {submission_type_str}: '
                    f'[cyan]{submissions[0].name}[/]')
            else:
                submissions = get_with_filters(submission_type, submission_name, latest=True)
                if not submissions:
                    raise MAPIException(status=HTTPStatus.NOT_FOUND,
                                        message=f'Could not find {submission_type_str}: [red]{submission_name}[/]')

        submission = submissions[0]

        last_line: Optional[str] = None
        # Have to check type to satisfy pyright
        if isinstance(submission, Run):
            last_line, err = _get_run_logs(submission, follow, node_rank, local_gpu_rank, global_gpu_rank,
                                           first_exception, failed, resumption, prev, tail, container)
            if err == 1:
                return 1
        elif isinstance(submission, InferenceDeployment):
            last_line, err = _get_deployment_logs(submission, follow, restart, failed, tail)
            if err == 1:
                return 1

        # Progress bars are weird. Let's add a final newline so that if the printing
        # ends on an incompleted progress bar, it isn't erased. Skip this for more precise tailing.
        if last_line and tail is None:
            print('', file=sys.stderr)
    except MAPIException as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except RuntimeError as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except BrokenPipeError:
        # This is raised when output is piped to programs like `head`
        # Error handling taken from this example in the python docs:
        # https://docs.python.org/3/library/signal.html#note-on-sigpipe
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())

        return 1

    return 0


def configure_deployments_argparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.set_defaults(func=partial(get_logs, SubmissionType.INFERENCE))

    submission_parser = parser.add_argument(
        'submission_name',
        metavar='DEPLOYMENT',
        help='The name of the inference deployment to fetch logs for.',
    )
    submission_parser.completer = utils_completers.DeploymentNameCompleter()  # pyright: ignore

    restart_grp = parser.add_mutually_exclusive_group()
    restart_grp.add_argument(
        '--restart',
        type=int,
        default=None,
        help='Which restart to fetch logs for. If not provided, will fetch logs of most recent restart')
    restart_grp.add_argument('--failed',
                             action='store_true',
                             dest='failed',
                             default=False,
                             help='Get the logs of the latest failed deployment')
    follow_grp = parser.add_mutually_exclusive_group()
    follow_grp.add_argument('--no-follow',
                            action='store_false',
                            dest='follow',
                            default=False,
                            help='Do not follow the logs of an in-progress deployment. '
                            'Simply print any existing logs and exit. This is the default behavior.')
    follow_grp.add_argument('-f',
                            '--follow',
                            action='store_true',
                            dest='follow',
                            default=False,
                            help='Follow the logs of an in-progress deployment.')

    return parser


def configure_runs_argparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.set_defaults(func=partial(get_logs, SubmissionType.TRAINING))
    submimssion_name_parser = parser.add_argument(
        'submission_name',
        metavar='RUN',
        nargs='?',
        help='The name of the run. If not provided, will return the logs of the latest run',
    )
    submimssion_name_parser.completer = utils_completers.RunNameCompleter()  # pyright: ignore

    resumption_grp = parser.add_mutually_exclusive_group()
    resumption_grp.add_argument(
        '--resumption',
        type=int,
        default=None,
        metavar='N',
        dest='resumption',
        help='Resumption (0-indexed) of the run logs that you\'d like to view. '
        'The default without the flag is the latest resumption.',
    )
    resumption_grp.add_argument('--prev',
                                action='store_true',
                                help='Get the logs of the previous resumption of the run.')

    class DeprecatedAction(argparse.Action):

        def __call__(self, parser, namespace, values, option_string=None):
            warnings.warn("--rank is deprecated and will be removed in a future release. Please use --node instead.")
            setattr(namespace, self.dest, values)

    node_rank_grp = parser.add_mutually_exclusive_group()
    node_rank_grp.add_argument(
        '--rank',  # TODO: --rank should be deprecated
        type=int,
        action=DeprecatedAction,
        dest='node_rank',
        default=None,
        metavar='N',
        help='(Deprecated) Node rank for multi-node run logs. Use --node instead.')
    node_rank_grp.add_argument('--node-rank',
                               '--node',
                               type=int,
                               dest='node_rank',
                               default=None,
                               metavar='N',
                               help='Node rank for multi-node run logs. 0-indexed.')
    node_rank_grp.add_argument('--failed',
                               action='store_true',
                               dest='failed',
                               default=False,
                               help='Get the logs of the first failed node rank in a multi-node run.')

    # GPU related flags, not mutually exclusive with node-rank but with each other
    gpu_rank_grp = parser.add_mutually_exclusive_group()
    gpu_rank_grp.add_argument(
        '--local-gpu-rank',
        '--gpu',
        type=int,
        dest='local_gpu_rank',
        metavar='N',
        help='Local GPU rank # on default lowest rank or specified node rank when combined with --node. 0-indexed.')
    gpu_rank_grp.add_argument('--global-gpu-rank',
                              type=int,
                              dest='global_gpu_rank',
                              metavar='N',
                              help='Global GPU rank # across all nodes. 0-indexed.')

    first_exception_grp = parser.add_mutually_exclusive_group()
    first_exception_grp.add_argument('--error',
                                     '--first-exception',
                                     action='store_true',
                                     dest='first_exception',
                                     default=False,
                                     help='Get the first exception that is thrown on a failed run. \
        You can also specify node rank to see the errors for the first gpu that failed \
        on a node or node + GPU rank / global GPU rank to see the errors surfaced on a specific GPU.')

    parser.add_argument(
        '--container',
        '-c',
        type=str.upper,
        default=None,  # rely on mapi defaults
        metavar='CONTAINER',
        help='Container name to fetch logs for. If not provided, will fetch logs of the main container',
        choices=['MAIN', 'MODEL'],
    )

    follow_grp = parser.add_mutually_exclusive_group()
    follow_grp.add_argument('--no-follow',
                            action='store_false',
                            dest='follow',
                            default=False,
                            help='Do not follow the logs of an in-progress run. '
                            'Simply print any existing logs and exit. This is the default behavior.')
    follow_grp.add_argument('-f',
                            '--follow',
                            action='store_true',
                            dest='follow',
                            default=False,
                            help='Follow the logs of an in-progress run.')

    return parser


def add_log_parser(subparser: argparse._SubParsersAction, submission_type: SubmissionType):
    """Add the parser for retrieving submission logs
    """

    log_parser: argparse.ArgumentParser = subparser.add_parser(
        'logs',
        aliases=['log'],
        help=f'View the logs from a specific {submission_type.value.lower()}',
        description=f'View the logs of an ongoing, completed or failed {submission_type.value.lower()}',
        epilog=RUN_LOG_EXAMPLES if submission_type is SubmissionType.TRAINING else DEPLOYMENT_LOG_EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    log_parser = configure_runs_argparser(
        log_parser) if submission_type is SubmissionType.TRAINING else configure_deployments_argparser(log_parser)

    log_parser.add_argument('-t',
                            '--tail',
                            metavar='N',
                            type=int,
                            help='Number of lines to show from the end of the log.')

    return log_parser
