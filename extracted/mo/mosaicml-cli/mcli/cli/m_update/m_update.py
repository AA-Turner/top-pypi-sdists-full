""" mcli update Entrypoint """
import argparse
import datetime
import logging
from http import HTTPStatus
from typing import Optional

from mcli.api.exceptions import MAPIException, MCLIException, cli_error_handler
from mcli.api.inference_deployments.api_update_inference_deployments import update_inference_deployment
from mcli.api.model.run import Run
from mcli.api.runs.api_get_runs import get_run
from mcli.api.runs.api_update_run import update_run
from mcli.utils import utils_completers
from mcli.utils.utils_cli import configure_bool_arg
from mcli.utils.utils_logging import OK, seconds_to_str
from mcli.utils.utils_run_status import RunStatus

logger = logging.getLogger(__name__)

# pylint: disable-next=invalid-name
UPDATE_RUN_EXAMPLE = """
Example:

# Update a run
> mcli update run example-run --priority high --max-retries 4 --no-preemptible
"""

UPDATE_DEPLOYMENT_EXAMPLE = """
Example:

# Update a deployment
> mcli update deployment mpt30b-deployment --image new_image_name --replicas 4
"""


def update_entrypoint(parser, **kwargs) -> int:
    del kwargs
    parser.print_help()
    return 0


def get_expiration_date(run_start_time: datetime.datetime, max_duration: int) -> str:
    formatter = "%m/%d/%y at %I:%M%p"
    tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    expiration_time = (run_start_time + datetime.timedelta(seconds=max_duration)).astimezone(tz)
    return expiration_time.strftime(formatter)


def check_max_duration(run: Run, new_max_duration: int) -> str:
    """
    This function takes in a run, and a new max_duration_seconds value for that run. If the 
    new duration will cause the run to automatically expire, it will warn the user and ask
    for confirmation before they can continue.
    """
    if run.status.after(RunStatus.RUNNING):
        logger.error(f"Run {'is' if run.status == RunStatus.TERMINATING else 'has'} "
                     f"already {str(run.status).lower()}, cannot update max duration.")
        return ""

    new_max_string = seconds_to_str(new_max_duration)
    if not run.started_at:
        return f"{run.name} will now expire in {new_max_string}.\n"

    # Give all times the same tz so they can be compared
    tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    current_time = datetime.datetime.now().astimezone(tz)
    run_start_time = run.started_at.astimezone(tz)

    seconds_elapsed = (current_time - run_start_time).total_seconds()
    if new_max_duration <= seconds_elapsed:
        # If a provided max duration will make a run stop instantly, warn the user and ask for confirmation.
        raise MCLIException(
            f"Setting your max duration to {new_max_string} will cause your run to terminate immediately."
            f" If you want to stop your run, please use [cyan]mcli stop run[/].")

    return f"{run.name} will now expire on {get_expiration_date(run_start_time, new_max_duration)}.\n"


@cli_error_handler('mcli update run')
def _update_run(
    run_name: str,
    priority: Optional[str] = None,
    preemptible: Optional[bool] = None,
    max_retries: Optional[int] = None,
    max_duration: Optional[float] = None,
    **kwargs,
) -> int:
    del kwargs
    update_fields = any(
        [preemptible is not None, priority is not None, max_retries is not None, max_duration is not None])
    if not update_fields:
        raise MAPIException(HTTPStatus.BAD_REQUEST, "Must specify preemptible, priority, or max_retries to update")
    update_string = ""
    if preemptible is not None:
        update_string += f"Set preemptible to {preemptible}.\n"
    if priority is not None:
        update_string += f"Set priority to {priority}.\n"
    if max_retries is not None:
        update_string += f"Set max_retries to {max_retries}.\n"

    if max_duration is not None:
        # Make a get_run call to check the max duration of the user's run
        run = get_run(run_name, include_details=False)
        update = check_max_duration(run, new_max_duration=int(3600 * max_duration))
        if not update:
            return 0  # If the user cancelled their update, return.
        update_string += update

    update_run(run_name, preemptible=preemptible, priority=priority, max_retries=max_retries, max_duration=max_duration)

    logger.info(f'{OK} Updated {run_name}.\n{update_string}')
    return 0


@cli_error_handler('mcli update deployment')
def _update_deployment(
    deployment_name: str,
    image: Optional[str] = None,
    replicas: Optional[int] = None,
    **kwargs,
) -> int:
    del kwargs
    update_deployment_data = {}
    update_fields = any([image is not None, replicas is not None])
    if not update_fields:
        raise MAPIException(HTTPStatus.BAD_REQUEST, "Must specify image or replicas to update")
    update_string = ""
    if image is not None:
        update_deployment_data['image'] = image
        update_string += f"Set image to {image}.\n"
    if replicas is not None:
        update_deployment_data['replicas'] = replicas
        update_string += f"Set replica count to {replicas}.\n"
    update_inference_deployment(deployment_name, update_deployment_data)

    logger.info(f'{OK} Updated {deployment_name}.\n{update_string}')
    return 0


def add_update_argparser(subparser: argparse._SubParsersAction) -> argparse.ArgumentParser:
    """Add the parser for update
    """
    update_parser: argparse.ArgumentParser = subparser.add_parser(
        'update',
        help='Update a training run or inference deployment',
    )
    return _configure_argparser(parser=update_parser)


def deployment_argparser(subparser: argparse._SubParsersAction) -> None:
    deployment_parser = subparser.add_parser('deployment',
                                             description='Update the config for deployments created with mcli. '
                                             'This command can be used to update the image or number of replicas.',
                                             help='Update the image or replicas for an inference deployment',
                                             formatter_class=argparse.RawDescriptionHelpFormatter,
                                             epilog=UPDATE_DEPLOYMENT_EXAMPLE)
    deployment_name_parser = deployment_parser.add_argument(
        'deployment_name',
        type=str,
        help='The name of the deployment',
    )
    # pyright: ignore
    deployment_name_parser.completer = utils_completers.DeploymentNameCompleter()
    deployment_parser.add_argument('--image', dest='image', help='Update deployment image file')
    deployment_parser.add_argument('--replicas', dest='replicas', type=int, help='Update deployment replica count')
    deployment_parser.set_defaults(func=_update_deployment)


def run_argparser(subparser: argparse._SubParsersAction) -> None:
    run_parser = subparser.add_parser(
        'run',
        description='Update the scheduling config for runs created with mcli. '
        'This command can be used to update the priority, preemptible, or max_retries.',
        help='Update the scheduling config of a run',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=UPDATE_RUN_EXAMPLE,
    )
    run_name_parser = run_parser.add_argument(
        'run_name',
        type=str,
        help='The name of the run',
    )
    run_name_parser.completer = utils_completers.RunNameCompleter()  # pyright: ignore
    run_parser.add_argument('--priority',
                            dest='priority',
                            help='Update run priority from the default `auto` to `low` or `lowest`')
    configure_bool_arg(parser=run_parser,
                       field='preemptible',
                       variable_name='preemptible',
                       true_description='Allows runs to be stopped and re-queued by higher priority jobs',
                       false_description='Disallows runs from being stopped and re-queued by higher priority jobs')
    run_parser.add_argument('--max-retries',
                            type=int,
                            dest='max_retries',
                            help='Update max number of times a run should be retried (default 0)')
    run_parser.add_argument(
        '--max-duration',
        type=float,
        dest='max_duration',
        help='Update the maximum time that a run should run for (in hours). If the run exceeds this '
        'duration, it will be stopped.')

    run_parser.set_defaults(func=_update_run)


def _configure_argparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    subparsers = parser.add_subparsers(title='MCLI Updates', help='DESCRIPTION', metavar='OBJECT')
    parser.set_defaults(func=update_entrypoint, parser=parser)
    run_argparser(subparsers)
    deployment_argparser(subparsers)
    return parser
