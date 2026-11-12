"""`anyscale <resource> logs` for jobs, services, workspaces and clusters.

One implementation, four Click commands, over `GET /api/v2/logs/{entity_type}/{entity_id}/files`:
the backend resolves the resource to one cluster, checks read permission on its project
and lists the files that cluster wrote to the cloud bucket. Shared flags are declared once
as module-level decorators and stacked on each command; a flag that does not apply to a
resource is simply not stacked, so Click rejects it there with "No such option".

The group files (job_commands.py, service_commands.py, workspace_commands_v2.py,
cluster_commands.py) import this module and `add_command` the command that belongs to
them. Nothing here imports a group file, which keeps the import graph acyclic. The job
one is `anyscale job logs-v2`: `anyscale job logs` already exists as a GA command with a
different flag set (--name, --follow, a boolean --tail with --max-lines), so the new one
takes a versioned name until that command is retired.

All four are `hidden=True` for now: they run when typed, but are left out of the group
`--help` listings, the committed doc spec and the reference docs. Removing the flag (and
the matching one on the Log Files module in `_private/docgen/__main__.py`) publishes them.

Each run prints at most 1000 lines. When more exist, it ends with a `--page-token` line on
stderr, so stdout stays one valid JSON or YAML document.
"""

from datetime import datetime
from typing import Any, List, Optional

import click

import anyscale
from anyscale.commands.doc_metadata import (
    command_metadata,
    CommandExample,
    ReleaseStatus,
)
from anyscale.commands.output_format import OutputFormat, print_output
from anyscale.commands.time_flags import resolve_window
from anyscale.commands.util import AnyscaleCommand
from anyscale.logs.models import (
    LOG_FILE_TYPES,
    LogFileLine,
    LogFilesFilter,
    MAX_LINES_PER_PAGE,
    NODE_TYPES,
)


_OUTPUT_FORMATS = [OutputFormat.TEXT, OutputFormat.JSON, OutputFormat.YAML]
_DEFAULT_TAIL = 1000


# --- shared flags, declared once ------------------------------------------------------------

argument_glob = click.argument("glob", required=False, default=None)
option_log_type = click.option(
    "--log-type",
    type=click.Choice(LOG_FILE_TYPES, case_sensitive=False),
    default="application",
    show_default=True,
    help="Which files to read: the workload's own output (application), Ray's own files "
    "such as raylet, gcs_server and the autoscaler monitor (system), or all.",
)
option_ray_session = click.option(
    "--ray-session",
    default=None,
    help="Only files of this Ray session. Defaults to every session of the cluster.",
)
option_node_type = click.option(
    "--node-type",
    type=click.Choice(NODE_TYPES, case_sensitive=False),
    default=None,
    help="Only files of the head node or of the worker nodes. Defaults to both.",
)
option_node_ip = click.option(
    "--node-ip", default=None, help="Only files of the node with this IP."
)
option_instance_id = click.option(
    "--instance-id", default=None, help="Only files of this instance."
)
option_since = click.option(
    "--since",
    default=None,
    help="Only files written in the last <duration>, e.g. 30m, 2h or 1d. "
    "Cannot be combined with --start-time, --end-time or --page-token.",
)
option_start_time = click.option(
    "--start-time",
    default=None,
    help="Only files written at or after this time. ISO 8601, e.g. 2026-09-01T10:00:00Z.",
)
option_end_time = click.option(
    "--end-time",
    default=None,
    help="Only files written at or before this time. ISO 8601, e.g. 2026-09-01T11:00:00Z.",
)
option_tail = click.option(
    "--tail",
    type=click.IntRange(1, MAX_LINES_PER_PAGE),
    default=_DEFAULT_TAIL,
    show_default=True,
    help=f"How many lines to show, at most {MAX_LINES_PER_PAGE}. When more exist, the output "
    "ends with a --page-token for the rest. Not applied with --download.",
)
option_page_token = click.option(
    "--page-token",
    default=None,
    help="Show the lines after the last one of an earlier run. Use the token that run "
    "printed, with the same filters and --sort. Cannot be combined with --since or "
    "--download.",
)
option_sort = click.option(
    "--sort",
    type=click.Choice(["timestamp", "-timestamp"]),
    default="-timestamp",
    show_default=True,
    help="'-timestamp' reads the newest files first and prints the newest line first; "
    "'timestamp' starts at the oldest file, oldest line first. Not applied with --download.",
)
option_download = click.option(
    "-d",
    "--download",
    is_flag=True,
    default=False,
    help="Write every matching file to disk, mirroring the bucket layout, instead of printing.",
)
option_download_dir = click.option(
    "--download-dir",
    type=click.Path(file_okay=False),
    default=None,
    help="Directory to write files into. Defaults to the current directory. "
    "Only read with --download.",
)
option_output = click.option(
    "-o",
    "--output",
    "output_format",
    type=click.Choice([fmt.value for fmt in _OUTPUT_FORMATS]),
    default=OutputFormat.TEXT.value,
    show_default=True,
    help="Output format for the result.",
)

# --- resource-specific flags, stacked only where they apply -------------------------------

option_run = click.option(
    "--run", default=None, help="Name or ID of one job run. Defaults to the latest run."
)
option_version = click.option(
    "--version",
    default=None,
    help="Name or ID of one service version. Defaults to the primary version.",
)


# The Click group each resource's command hangs under, as the user types it.
_GROUP_NAMES = {
    "job": "job",
    "service": "service",
    "workspace": "workspace_v2",
    "cluster": "cluster",
}

# The command's name under its group. Jobs get a versioned name: `anyscale job logs` is
# taken by the GA command.
_COMMAND_NAMES = {
    "job": "logs-v2",
    "service": "logs",
    "workspace": "logs",
    "cluster": "logs",
}


def _metadata(entity: str):
    invocation = f"anyscale {_GROUP_NAMES[entity]} {_COMMAND_NAMES[entity]} --id <{entity}-id>"
    return command_metadata(
        status=ReleaseStatus.BETA,
        since="0.0.0",
        output_formats=_OUTPUT_FORMATS,
        examples=[
            CommandExample(
                description=f"Print the last 1000 lines of a {entity}'s application logs.",
                command=invocation,
            ),
            CommandExample(
                description="Only the raylet files of the head node, from the last 30 minutes.",
                command=f"{invocation} --log-type system --node-type head --since 30m 'raylet*'",
            ),
            CommandExample(
                description="Download every file to a directory.",
                command=f"{invocation} --log-type all --download --download-dir ./logs",
            ),
            CommandExample(
                description="The next page, after a run that printed a page token.",
                command=f"{invocation} --page-token <token>",
            ),
        ],
    )


_HELP_GLOB = "An optional GLOB keeps only the files whose bucket path matches it, e.g. 'raylet*'."


# --- the four commands -----------------------------------------------------------------------


@_metadata("job")
@click.command(
    name="logs-v2", cls=AnyscaleCommand, short_help="Read log files of a job.", hidden=True
)
@click.option("--job-id", "--id", "id", required=True, help="ID of the job.")
@argument_glob
@option_log_type
@option_run
@option_ray_session
@option_node_type
@option_node_ip
@option_instance_id
@option_since
@option_start_time
@option_end_time
@option_tail
@option_page_token
@option_sort
@option_download
@option_download_dir
@option_output
def job_logs(id: str, **kwargs: Any) -> None:  # noqa: A002
    """Read the log files of a job's latest run, or of the run named by --run.

    Prints the job's output (its stdout and stderr) by default, like `anyscale job logs`.
    A GLOB or a node flag reads other files of the run's cluster instead. The GLOB keeps
    only the files whose bucket path matches it, e.g. 'raylet*'.
    """
    _run("job", id, **kwargs)


@_metadata("service")
@click.command(
    name="logs", cls=AnyscaleCommand, short_help="Read log files of a service.", hidden=True
)
@click.option("--service-id", "--id", "id", required=True, help="ID of the service.")
@argument_glob
@option_log_type
@option_version
@option_ray_session
@option_node_type
@option_node_ip
@option_instance_id
@option_since
@option_start_time
@option_end_time
@option_tail
@option_page_token
@option_sort
@option_download
@option_download_dir
@option_output
def service_logs(id: str, **kwargs: Any) -> None:  # noqa: A002
    """Read the log files of a service's primary version, or of the version named by --version.

    An optional GLOB keeps only the files whose bucket path matches it, e.g. 'raylet*'.
    """
    _run("service", id, **kwargs)


@_metadata("workspace")
@click.command(
    name="logs", cls=AnyscaleCommand, short_help="Read log files of a workspace.", hidden=True
)
@click.option("--workspace-id", "--id", "id", required=True, help="ID of the workspace.")
@argument_glob
@option_log_type
@option_ray_session
@option_node_type
@option_node_ip
@option_instance_id
@option_since
@option_start_time
@option_end_time
@option_tail
@option_page_token
@option_sort
@option_download
@option_download_dir
@option_output
def workspace_logs(id: str, **kwargs: Any) -> None:  # noqa: A002
    """Read the log files of a workspace's cluster.

    An optional GLOB keeps only the files whose bucket path matches it, e.g. 'raylet*'.
    """
    _run("workspace", id, **kwargs)


@_metadata("cluster")
@click.command(
    name="logs", cls=AnyscaleCommand, short_help="Read log files of a cluster.", hidden=True
)
@click.option("--cluster-id", "--id", "id", required=True, help="ID of the cluster.")
@argument_glob
@option_log_type
@option_ray_session
@option_node_type
@option_node_ip
@option_instance_id
@option_since
@option_start_time
@option_end_time
@option_tail
@option_page_token
@option_sort
@option_download
@option_download_dir
@option_output
def cluster_logs(id: str, **kwargs: Any) -> None:  # noqa: A002
    """Read the log files of a cluster.

    An optional GLOB keeps only the files whose bucket path matches it, e.g. 'raylet*'.
    """
    _run("cluster", id, **kwargs)


# --- shared implementation ---------------------------------------------------------------


def _run(  # noqa: PLR0913
    entity: str,
    entity_id: str,
    *,
    glob: Optional[str],
    log_type: str,
    ray_session: Optional[str],
    node_type: Optional[str],
    node_ip: Optional[str],
    instance_id: Optional[str],
    since: Optional[str],
    start_time: Optional[str],
    end_time: Optional[str],
    tail: int,
    sort: str,
    download: bool,
    download_dir: Optional[str],
    page_token: Optional[str],
    output_format: str,
    run: Optional[str] = None,
    version: Optional[str] = None,
) -> None:
    if since is not None and page_token is not None:
        # The token is a position in the earlier run's window. --since would re-resolve
        # that window against a later "now" and skip lines.
        raise click.UsageError(
            "--since cannot be combined with --page-token. Use the --start-time and "
            "--end-time that the earlier run printed."
        )
    if download and page_token is not None:
        raise click.UsageError(
            "--page-token cannot be combined with --download, which writes every matching file."
        )
    start, end = resolve_window(since, start_time, end_time)

    try:
        files_filter = LogFilesFilter(
            entity_type=entity,
            entity_id=entity_id,
            # Click already restricted the values; lower-case them so the wire sees the
            # canonical spelling whatever the user typed.
            log_type=log_type.lower(),
            job_run=run,
            service_version=version,
            ray_session=ray_session,
            node_type=node_type.lower() if node_type else None,
            node_ip=node_ip,
            instance_id=instance_id,
            glob=glob,
            start_time=start,
            end_time=end,
            # A download takes every file of the window, whatever the sort; printing
            # reads the newest chunks backwards unless asked for the oldest first.
            latest=(not download and sort == "-timestamp"),
        )
    except (TypeError, ValueError) as e:
        raise click.UsageError(str(e)) from None

    if download:
        target = anyscale.logs.download(files_filter, download_dir=download_dir)
        if output_format != OutputFormat.TEXT.value:
            print_output({"download_dir": target}, output_format)
        return

    try:
        page = anyscale.logs.read_page(files_filter, max_lines=tail, page_token=page_token)
    except ValueError as e:
        if page_token is None:
            raise
        # A token that is malformed, from another --sort, or no longer in the listing.
        raise click.UsageError(f"Invalid --page-token: {e}") from None

    if output_format == OutputFormat.TEXT.value:
        if not page.lines:
            click.echo("No log files matched.", err=True)
        for line in page.lines:
            click.echo(line.line)
    else:
        print_output([_to_row(line) for line in page.lines], output_format)

    if page.next_page_token is not None:
        # stderr, so json / yaml on stdout stay parseable.
        click.echo(_next_page_hint(page.next_page_token, since, start, end), err=True)


def _next_page_hint(
    token: str, since: Optional[str], start: Optional[datetime], end: Optional[datetime]
) -> str:
    hint = f"--page-token '{token}'"
    if since is not None and start is not None and end is not None:
        # Pin the window --since resolved, at full precision, so the token's position
        # still lines up on the next run.
        hint = (
            f"--start-time '{start.isoformat()}' --end-time '{end.isoformat()}' "
            f"in place of --since, and {hint}"
        )
    return f"More lines exist. To see them, run the same command with {hint}."


def _to_row(line: LogFileLine) -> dict:
    # Every record carries the same keys, so a reader can rely on them.
    return line.to_dict(exclude_none=False)


__all__: List[str] = ["cluster_logs", "job_logs", "service_logs", "workspace_logs"]
