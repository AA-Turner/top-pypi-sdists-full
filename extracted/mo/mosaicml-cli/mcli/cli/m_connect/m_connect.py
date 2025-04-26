""" mcli connect Entrypoint """

import argparse
import logging
from typing import Optional, Union

from mcli.api.exceptions import MintException, cli_error_handler
from mcli.api.mint import shell
from mcli.api.model.run import Run, RunStatus, RunType
from mcli.api.runs.api_get_runs import get_run, get_runs
from mcli.api.runs.api_watch_run import EpilogSpinner as CloudEpilogSpinner
from mcli.cli.m_get.runs import get_instance_name
from mcli.models.common import ObjectList
from mcli.utils.utils_date import format_timestamp
from mcli.utils.utils_epilog import CommonLog
from mcli.utils.utils_interactive import choose_one
from mcli.utils.utils_logging import FAIL

logger = logging.getLogger(__name__)


def wait_for_run(run: Run) -> bool:
    last_status: Optional[RunStatus] = None
    with CloudEpilogSpinner(run, RunStatus.RUNNING) as watcher:
        run = watcher.follow()
        last_status = run.status

    run = run.refresh()

    common_log = CommonLog(logger)
    if last_status is None:
        common_log.log_timeout()
        return False
    elif last_status == RunStatus.RUNNING:
        common_log.log_run_interactive_starting(run.name)
        return True
    elif last_status in {RunStatus.FAILED, RunStatus.TERMINATING}:
        common_log.log_run_terminated(run)
        return False
    elif last_status.after(RunStatus.RUNNING):
        # TODO: Log image pull failures more cleanly
        common_log.log_connect_run_terminating(last_status.display_name)
        return False

    common_log.log_unknown_did_not_start()
    logger.debug(last_status)
    return False


def get_runs_to_connect_to(limit: Optional[int] = 10):
    return get_runs(
        statuses=[
            RunStatus.STARTING,
            RunStatus.RUNNING,
        ],
        limit=limit,
        run_types=[RunType.INTERACTIVE],
    )


@cli_error_handler("mcli connect")
def connect_entrypoint(
    name: Optional[str] = None,
    rank: int = 0,
    latest: bool = False,
    command: Optional[str] = None,
    container: Optional[str] = None,
    tmux: Optional[bool] = None,
    runs: Optional[ObjectList[Run]] = None,
    **kwargs,
):
    del kwargs

    if name:
        run = get_run(name)
    elif latest:
        runs = get_runs_to_connect_to(limit=1)
        if not runs:
            logger.error(f"{FAIL} No running runs available to connect to")
            return 1
        run = runs[0]
    else:
        # If a user doesn't specify a run name, get all starting and running runs
        # When runs are passed in, don't perform another query
        available_runs = runs or get_runs_to_connect_to()
        if not available_runs:
            logger.error(f"{FAIL} No running runs available to connect to")
            return 1
        elif len(available_runs) == 1:
            # Only one run, connect to this one automatically
            run = available_runs[0]
        else:
            # Multiple options for runs to connect to...
            sorted_runs = sorted(available_runs, key=lambda x: x.created_at, reverse=True)

            def name_formatter(r: Run):
                if r.started_at:
                    time_started = f"Started at {format_timestamp(r.started_at)}"
                else:
                    time_started = "Not yet started"

                instance_name = get_instance_name(r)
                if instance_name == "cpu":
                    gpu_info = "cpu"
                else:
                    gpu_info = f"{instance_name} x {r.node_count} node(s)"

                return f"{r.name} | {time_started} | {r.cluster} | {gpu_info}"

            run = choose_one(
                "Which run would you like to connect to?",
                options=sorted_runs,
                formatter=name_formatter,
            )

    # Wait for the run to be ready
    ready = wait_for_run(run)
    if not ready:
        return 1

    # Get the command and connect to the shell
    if tmux:
        command = get_tmux_command()

    try:
        mint_shell = shell.MintShell(run.name, rank=rank)
        mint_shell.connect(command=command, container=container)
    except MintException as e:
        logger.error(f"{FAIL} {e}")
        return 1
    return 0


def get_tmux_command() -> str:
    # set the command to a tmux entrypoint
    # Check if tmux already exists
    # command -v tmux >/dev/null 2>&1: Check if tmux already exists
    # apt update && apt install -yq tmux: If not, quietly install. Assumes debian-based systems with apt
    install_command = "command -v tmux >/dev/null 2>&1 || (apt update && apt install -yq tmux)"

    # new-session: Create a session
    # -A: Attach if one exists (for auto-reconnect)
    # -s main: Name the session ("main") for clarity
    # -D: Disconnect other clients (from previous connections)
    session_command = "tmux new-session -A -s main -D"
    return f'/bin/bash -c "({install_command}) && {session_command}"'


def configure_connection_argparser(parser: Union[argparse.ArgumentParser, "argparse._ArgumentGroup"]):
    parser.add_argument(
        "--rank",
        metavar="N",
        default=0,
        type=int,
        help="Connect to the specified node rank within the run",
    )

    parser.add_argument(
        "--container",
        default=None,
        type=str,
        help="Container to connect to, by default the MAIN container is used",
    )

    command_grp = parser.add_mutually_exclusive_group()
    command_grp.add_argument(
        "--command",
        help="The command to execute in the run. By default you will be dropped into a bash shell",
    )
    command_grp.add_argument(
        "--tmux",
        action="store_true",
        help="Use tmux as the entrypoint for your run so your session is robust to disconnects",
    )


class RunConnectorCompleter:

    def __init__(self, limit: Optional[int] = None):
        self.limit = limit

    def __call__(self, **kwargs):
        return get_runs_to_connect_to(limit=self.limit)


def configure_argparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument(
        "name",
        metavar="RUN",
        default=None,
        nargs="?",
        help="Run name",
    ).completer = RunConnectorCompleter()  # pyright: ignore

    parser.add_argument(
        "-l",
        "--latest",
        action="store_true",
        dest="latest",
        default=False,
        help="Connect to the latest run",
    )

    configure_connection_argparser(parser)

    parser.set_defaults(func=connect_entrypoint)
    return parser


def add_connect_argparser(subparser: argparse._SubParsersAction,) -> argparse.ArgumentParser:
    """Adds the get parser to a subparser

    Args:
        subparser: the Subparser to add the Get parser to
    """
    examples = """

Examples:

# Connect to an existing run
> mcli connect my-run-1234
    """

    connect_parser: argparse.ArgumentParser = subparser.add_parser(
        "connect",
        help="Create an interactive session that's connected to a run",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=examples,
    )

    get_parser = configure_argparser(parser=connect_parser)
    return get_parser
