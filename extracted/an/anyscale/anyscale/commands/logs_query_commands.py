"""`anyscale logs query`.

Searches one resource's logs with a LogQL query over the backend's `/logs/query` route.
The command takes exactly one resource id (cluster, workspace, job or service); the
backend resolves it, checks read permission, and pins the query's stream selector to
that resource, so nothing here filters client-side.

The command is `hidden=True` for now: it runs when typed, but is left out of
`anyscale logs --help`, the committed doc spec and the reference docs. Removing the flag
(and the matching one on the Log Queries module in `_private/docgen/__main__.py`)
publishes it.
"""

from datetime import datetime, timezone
from typing import Optional, Tuple

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
from anyscale.logs._private.logs_sdk import DEFAULT_LIMIT, MAX_LIMIT
from anyscale.logs.models import LOG_TYPES, LogsResource


_OUTPUT_FORMATS = [OutputFormat.TEXT, OutputFormat.JSON, OutputFormat.YAML]

_RESOURCE_FLAGS = "--cluster-id, --workspace-id, --job-id or --service-id"

_NEWEST_FIRST = "-timestamp"
_OLDEST_FIRST = "timestamp"


# --- flags ---------------------------------------------------------------------------------

option_cluster_id = click.option(
    "--cluster-id",
    default=None,
    help=f"ID of the cluster. Exactly one of {_RESOURCE_FLAGS} is required.",
)
option_workspace_id = click.option(
    "--workspace-id",
    default=None,
    help=f"ID of the workspace. Exactly one of {_RESOURCE_FLAGS} is required.",
)
option_job_id = click.option(
    "--job-id",
    default=None,
    help=f"ID of the job. Exactly one of {_RESOURCE_FLAGS} is required.",
)
option_service_id = click.option(
    "--service-id",
    default=None,
    help=f"ID of the service. Exactly one of {_RESOURCE_FLAGS} is required.",
)
option_log_type = click.option(
    "--log-type",
    type=click.Choice(LOG_TYPES),
    default="application",
    show_default=True,
    help="Which lines to search: the workload's own output (application), or Ray's own "
    "files such as raylet and gcs (system), which are kept at WARNING and above only.",
)
option_since = click.option(
    "--since",
    default=None,
    help="Use the last <duration> as the window, e.g. 30m, 2h or 1d. "
    "Cannot be combined with --start-time or --end-time.",
)
option_start_time = click.option(
    "--start-time",
    default=None,
    help="Start of the time window. ISO 8601, e.g. 2026-09-01T10:00:00Z.",
)
option_end_time = click.option(
    "--end-time",
    default=None,
    help="End of the time window. ISO 8601, e.g. 2026-09-01T11:00:00Z.",
)
option_tail = click.option(
    "--tail",
    type=click.IntRange(1, MAX_LIMIT),
    default=DEFAULT_LIMIT,
    show_default=True,
    help=f"Maximum number of lines to return, up to {MAX_LIMIT}.",
)
option_sort = click.option(
    "--sort",
    type=click.Choice([_OLDEST_FIRST, _NEWEST_FIRST]),
    default=_NEWEST_FIRST,
    show_default=True,
    help="Which lines of the window to return and in what order: -timestamp the newest "
    "lines, newest first; timestamp the oldest lines, oldest first.",
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


def _resource(
    cluster_id: Optional[str],
    workspace_id: Optional[str],
    job_id: Optional[str],
    service_id: Optional[str],
) -> LogsResource:
    """The one resource the user named, or a usage error naming the four flags."""
    given = {
        kind: value
        for kind, value in {
            "cluster": cluster_id,
            "workspace": workspace_id,
            "job": job_id,
            "service": service_id,
        }.items()
        if value
    }
    if len(given) != 1:
        raise click.UsageError(f"Exactly one of {_RESOURCE_FLAGS} is required.")
    ((resource_type, resource_id),) = given.items()
    try:
        return LogsResource(resource_type=resource_type, resource_id=resource_id)
    except (TypeError, ValueError) as e:
        raise click.UsageError(str(e)) from None


def _required_window(
    since: Optional[str], start_time: Optional[str], end_time: Optional[str]
) -> Tuple[datetime, datetime]:
    start, end = resolve_window(since, start_time, end_time)
    if start is None or end is None:
        raise click.UsageError(
            "A time window is required: either --since, or both --start-time and --end-time."
        )
    if end <= start:
        raise click.UsageError("--end-time must be after --start-time.")
    return start, end


def _format_timestamp(value: datetime) -> str:
    """``2026-09-01T10:00:00.123Z``: UTC with milliseconds, since lines of one second
    are common."""
    utc = value.astimezone(timezone.utc) if value.tzinfo else value.replace(tzinfo=timezone.utc)
    return utc.strftime("%Y-%m-%dT%H:%M:%S.") + f"{utc.microsecond // 1000:03d}Z"


# --- query -----------------------------------------------------------------------------------


@command_metadata(
    status=ReleaseStatus.BETA,
    since="0.0.0",
    output_formats=_OUTPUT_FORMATS,
    examples=[
        CommandExample(
            description="The newest lines mentioning OOM in a job's last hour of logs.",
            command="anyscale logs query '{} |= \"OOM\"' --job-id <job-id> --since 1h",
        ),
        CommandExample(
            description="Ray's own raylet and gcs lines of a cluster over an explicit window.",
            command=(
                "anyscale logs query '{}' --cluster-id <cluster-id> --log-type system "
                "--start-time 2026-09-01T10:00:00Z --end-time 2026-09-01T11:00:00Z"
            ),
        ),
        CommandExample(
            description="The first 50 lines of a window, oldest first, as JSON.",
            command=(
                "anyscale logs query '{} |= \"error\"' --service-id <service-id> --since 2h "
                "--tail 50 --sort timestamp -o json"
            ),
        ),
    ],
)
@click.command(
    name="query",
    cls=AnyscaleCommand,
    short_help="Search the logs of a resource with LogQL.",
    hidden=True,
)
@click.argument("query")
@option_cluster_id
@option_workspace_id
@option_job_id
@option_service_id
@option_log_type
@option_since
@option_start_time
@option_end_time
@option_tail
@option_sort
@option_output
def query(  # noqa: PLR0913
    query: str,  # noqa: A002
    cluster_id: Optional[str],
    workspace_id: Optional[str],
    job_id: Optional[str],
    service_id: Optional[str],
    log_type: str,
    since: Optional[str],
    start_time: Optional[str],
    end_time: Optional[str],
    tail: int,
    sort: str,
    output_format: str,
) -> None:
    """Search the logs of a cluster, workspace, job or service with a LogQL query.

    QUERY is a LogQL log query, e.g. '{} |= "OOM"' or '{} | json | level="ERROR"'. Quote
    it so the shell leaves it alone. The backend pins its stream selector to the named
    resource, so a selector that names another resource is rejected. Give the window as
    either --since, or both --start-time and --end-time.

    By default the newest lines of the window come back, newest first, like tail. Use
    --sort timestamp for the oldest lines, oldest first.
    """
    resource = _resource(cluster_id, workspace_id, job_id, service_id)
    start, end = _required_window(since, start_time, end_time)

    lines = anyscale.logs.query(
        query,
        resource,
        start=start,
        end=end,
        log_type=log_type,
        limit=tail,
        newest_first=sort == _NEWEST_FIRST,
    )

    if output_format == OutputFormat.TEXT.value:
        for line in lines:
            click.echo(f"{_format_timestamp(line.timestamp)}  {line.message}")
        return
    print_output([line.to_dict() for line in lines], output_format)
