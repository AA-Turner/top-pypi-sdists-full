""" mcli run Entrypoint """
import argparse
import logging
import os
import textwrap
from http import HTTPStatus
from typing import List, Optional

from mcli.api.exceptions import MAPIException, cli_error_handler
from mcli.api.model.run import Run, RunConfig
from mcli.api.runs import create_run, update_run
from mcli.api.runs.api_get_run_logs import follow_run_logs
from mcli.api.runs.api_get_runs import get_run
from mcli.api.runs.api_start_run import start_run
from mcli.api.runs.api_watch_run import EpilogSpinner as CloudEpilogSpinner
from mcli.api.runs.api_watch_run import wait_for_run_status
from mcli.utils import utils_completers
from mcli.utils.utils_cli import comma_separated, configure_bool_arg
from mcli.utils.utils_epilog import CommonLog
from mcli.utils.utils_interactive import query_yes_no
from mcli.utils.utils_logging import INFO, OK, WARN
from mcli.utils.utils_run_status import RunStatus
from mcli.utils.utils_spinner import console_status

logger = logging.getLogger(__name__)


def print_help(**kwargs) -> int:
    del kwargs
    mock_parser = argparse.ArgumentParser()
    _configure_parser(mock_parser)
    mock_parser.print_help()
    return 1


def follow_run(run: Run) -> int:
    last_status: Optional[RunStatus] = None

    with CloudEpilogSpinner(run, RunStatus.RUNNING) as watcher:
        run = watcher.follow()
        last_status = run.status

    # pull the latest details (not just the status)
    run = run.refresh()

    # Wait timed out
    common_log = CommonLog(logger)
    if last_status is None:
        common_log.log_timeout()
        return 0
    elif last_status in {RunStatus.FAILED, RunStatus.TERMINATING}:
        common_log.log_run_terminated(run)
        return 1
    elif last_status.before(RunStatus.RUNNING):
        common_log.log_unknown_did_not_start()
        logger.debug(last_status)
        return 1

    logger.info(f'{OK} Run [cyan]{run.name}[/] started')
    logger.info(f'{INFO} Following run logs. Press Ctrl+C to quit.\n')

    end = ''
    for line in follow_run_logs(run, rank=0):
        print(line, end=end)
    if not end:
        print('')

    wait_for_run_status(run, status=RunStatus.COMPLETED, timeout=10)

    return 0


def finish_run(run: Run, follow: bool, restarted: bool = False) -> int:
    if not follow:
        log_cmd = f'mcli logs {run.name}'
        message = f"""
        {OK} Run [cyan]{run.name}[/] {'re' if restarted else ''}submitted.

        To see the run\'s status, use:

        [bold]mcli get runs[/]

        To see the run\'s logs, use:

        [bold]{log_cmd}[/]
        """
        logger.info(textwrap.dedent(message).strip())
        return 0
    else:
        return follow_run(run)


@cli_error_handler('mcli run')
# pylint: disable-next=too-many-statements
def run_entrypoint(
    file: Optional[str] = None,
    restart_run: Optional[str] = None,
    clone: Optional[str] = None,
    follow: bool = True,
    override_cluster: Optional[str] = None,
    override_gpu_type: Optional[str] = None,
    override_gpu_num: Optional[int] = None,
    override_nodes: Optional[int] = None,
    override_node_names: Optional[List[str]] = None,
    override_instance: Optional[str] = None,
    override_image: Optional[str] = None,
    override_name: Optional[str] = None,
    override_priority: Optional[str] = None,
    override_preemptible: Optional[bool] = None,
    override_max_retries: Optional[int] = None,
    override_max_duration: Optional[float] = None,
    **kwargs,
) -> int:
    del kwargs

    runs_to_modify = sum([file is not None, clone is not None, restart_run is not None])
    if runs_to_modify != 1:
        print_help()
        raise MAPIException(HTTPStatus.BAD_REQUEST, "Must specify a file, a run to clone, or a run to restart.")
    if file:
        run_config = RunConfig.from_file(path=file)

    elif clone:
        run = get_run(clone)
        if run.submitted_config is None:
            raise MAPIException(HTTPStatus.NOT_FOUND, f"Could not retrieve configuration from run {clone}")
        run_config = run.submitted_config
    elif restart_run:
        configs = any([
            override_cluster is not None,
            override_gpu_type is not None,
            override_gpu_num is not None,
            override_instance is not None,
            override_image is not None,
            override_name is not None,
            override_nodes is not None,
            override_max_duration is not None,
        ])
        if configs:
            logger.info(f'{WARN} New configurations will be ignored when restarting a run.')
            restart_to_clone = query_yes_no(f'Would you like to clone {restart_run} with these configurations instead?')
            if not restart_to_clone:
                return 0
            run = get_run(restart_run)
            if run.submitted_config is None:
                raise MAPIException(HTTPStatus.NOT_FOUND, f"Could not retrieve configuration from run {restart_run}")
            run_config = run.submitted_config
        else:
            scheduling_config = any([
                override_priority is not None, override_preemptible is not None, override_max_retries is not None,
                override_max_duration is not None
            ])
            if scheduling_config:
                update_string = ''
                if override_preemptible is not None:
                    update_string += f" Set preemptible to {override_preemptible}."
                if override_priority is not None:
                    update_string += f" Set priority to {override_priority}."
                if override_max_retries is not None:
                    update_string += f" Set max_retries to {override_max_retries}."
                if override_max_duration is not None:
                    update_string += f"Set max-duration to ${override_max_duration} hours."
                update_run(restart_run,
                           preemptible=override_preemptible,
                           priority=override_priority,
                           max_retries=override_max_retries,
                           max_duration=override_max_duration)
                logger.info(f'{OK} Updated {restart_run}.{update_string}')
            with console_status('Restarting run...'):
                run = start_run(restart_run, timeout=None)

            return finish_run(run, follow, restarted=True)
    else:
        return print_help()

    if os.environ.get('DOGEMODE', None) == 'ON':
        logger.info(
            textwrap.dedent("""
        ------------------------------------------------------
        Let's run this run
        ------------------------------------------------------
        """))

    # command line overrides
    # only supports basic format for now and not structured params
    if override_cluster is not None:
        run_config.compute['cluster'] = override_cluster

    if override_gpu_type is not None:
        run_config.compute['gpu_type'] = override_gpu_type

    if override_gpu_num is not None:
        run_config.compute['gpus'] = override_gpu_num

    if override_image is not None:
        run_config.image = override_image

    if override_name is not None:
        run_config.name = override_name

    if override_priority is not None:
        run_config.scheduling['priority'] = override_priority

    if override_preemptible is not None:
        run_config.scheduling['preemptible'] = override_preemptible

    if override_max_retries is not None:
        run_config.scheduling['max_retries'] = override_max_retries

    if override_max_duration is not None:
        run_config.scheduling["max_duration"] = override_max_duration

    if override_instance is not None:
        run_config.compute['instance'] = override_instance

    if override_nodes is not None:
        run_config.compute['nodes'] = override_nodes

    if override_node_names is not None:
        run_config.compute['node_names'] = override_node_names

    with console_status('Submitting run...'):
        run = create_run(run=run_config, timeout=None)

    return finish_run(run, follow)


def add_run_argparser(subparser: argparse._SubParsersAction, is_admin: bool = False) -> None:
    run_parser: argparse.ArgumentParser = subparser.add_parser(
        'run',
        aliases=['r'],
        help='Launch a run in the MosaicML platform',
    )
    run_parser.set_defaults(func=run_entrypoint)
    _configure_parser(run_parser, is_admin=is_admin)


def _configure_parser(parser: argparse.ArgumentParser, is_admin: bool = False):
    if not is_admin:
        parser.add_argument(
            '-f',
            '--file',
            dest='file',
            help='File from which to load arguments.',
        )

    restart_parser = parser.add_argument(
        '-r',
        '--restart',
        dest='restart_run',
        help='Previously stopped run to start again',
    )
    restart_parser.completer = utils_completers.RunNameCompleter()  # pyright: ignore

    clone_parser = parser.add_argument(
        '--clone',
        dest='clone',
        help='Copy the run config from an existing run',
    )
    clone_parser.completer = utils_completers.RunNameCompleter()  # pyright: ignore

    parser.add_argument(
        '--priority',
        dest='override_priority',
        help='Priority level at which runs should be submitted. For lower priority runs, '
        'use "low" or "lowest" '
        '(default Auto)',
    )
    configure_bool_arg(parser=parser,
                       field='preemptible',
                       variable_name='override_preemptible',
                       default=None,
                       true_description='Allows runs to be stopped and re-queued by higher priority jobs',
                       false_description='Disallows runs from being stopped and re-queued by higher priority jobs')

    parser.add_argument('--max_retries',
                        type=int,
                        dest='override_max_retries',
                        help='Optional override for max number of times a run should be retried')

    configure_bool_arg(
        parser=parser,
        field='follow',
        variable_name='follow',
        default=False,
        true_description='Follow the logs of an in-progress run.',
        false_description='Do not automatically try to follow the run\'s logs. This is the default behavior')

    parser.add_argument(
        '--image',
        dest='override_image',
        help='Optional override for docker image',
    )

    parser.add_argument(
        '--name',
        '--run-name',
        dest='override_name',
        help='Optional override for run name',
    )

    parser.add_argument('--max-duration',
                        type=float,
                        dest="override_max_duration",
                        help="Optional override for the max duration (in hours) of a run")

    configure_compute_overrides(parser)


def configure_compute_overrides(parser: argparse.ArgumentParser):
    cluster_arguments = parser.add_argument_group(
        'Compute settings',
        'These settings are used to determine the cluster and compute resources to use for your run',
    )

    cluster_parser = cluster_arguments.add_argument(
        '--cluster',
        '--platform',  # TODO: remove this alias
        dest='override_cluster',
        help='Optional override for MCLI cluster',
    )
    cluster_parser.completer = utils_completers.ClusterNameCompleter()  # pyright: ignore

    gpu_type_parser = cluster_arguments.add_argument(
        '--gpu-type',
        dest='override_gpu_type',
        help='Optional override for GPU type. Valid GPU type depend on'
        ' the cluster and GPU number requested',
    )
    gpu_type_parser.completer = utils_completers.GPUTypeCompleter()  # pyright: ignore

    cluster_arguments.add_argument(
        '--gpus',
        type=int,
        dest='override_gpu_num',
        help='Optional override for number of GPUs. Valid GPU numbers '
        'depend on the cluster and GPU type',
    )

    instance_parser = cluster_arguments.add_argument(
        '--instance',
        dest='override_instance',
        help='Optional override for instance type',
    )
    instance_parser.completer = utils_completers.InstanceNameCompleter()  # pyright: ignore

    cluster_arguments.add_argument(
        '--nodes',
        type=int,
        dest='override_nodes',
        help='Optional override for number of nodes. '
        'Valid node numbers depend on the cluster and instance type',
    )

    node_names_parser = cluster_arguments.add_argument(
        '--node-names',
        default=None,
        dest='override_node_names',
        type=comma_separated,
        help='Optional override for names of nodes to run on (comma-separated if multiple)',
    )
    node_names_parser.completer = utils_completers.NodeNameCompleter()  # pyright: ignore
