"""`anyscale <resource> events` for jobs, services, workspaces and clusters.

One implementation, four Click commands. Shared flags are declared once as module-level
decorators and stacked on each command; a flag that does not apply to a resource is simply
not stacked, so Click rejects it there with "No such option".

The group files (job_commands.py, service_commands.py, workspace_commands_v2.py,
cluster_commands.py) import this module and `add_command` the command that belongs to
them. Nothing here imports a group file, which keeps the import graph acyclic.

All four are `hidden=True` for now: they run when typed, but are left out of the group
`--help` listings, the committed doc spec and the reference docs. Removing the flag
(and the matching one on the Events module in `_private/docgen/__main__.py`) publishes
them.
"""

from typing import Any, Dict, List, Optional, Tuple

import click

import anyscale
from anyscale.commands.doc_metadata import (
    command_metadata,
    CommandExample,
    ReleaseStatus,
)
from anyscale.commands.output_format import OutputFormat, print_output
from anyscale.commands.time_flags import format_timestamp, resolve_window
from anyscale.commands.util import AnyscaleCommand
from anyscale.events.models import Event, EventsFilter, LEVELS, SOURCES_BY_ENTITY


_OUTPUT_FORMATS = [OutputFormat.TEXT, OutputFormat.JSON, OutputFormat.YAML, OutputFormat.TABLE]
_TABLE_COLUMNS = ["created_at", "level", "source", "message"]


# --- shared flags, declared once ------------------------------------------------------------


def option_source(entity: str):
    # The accepted values differ per resource, so this one is built per command.
    return click.option(
        "--source",
        multiple=True,
        type=click.Choice(SOURCES_BY_ENTITY[entity], case_sensitive=False),
        help="Only show events from these subsystems. Repeat the flag for several.",
    )


option_level = click.option(
    "--level",
    multiple=True,
    type=click.Choice(LEVELS, case_sensitive=False),
    help="Only show events at these levels. Repeat the flag for several.",
)
option_message_contains = click.option(
    "--message-contains",
    default=None,
    help="Only show events whose message contains this text (case-sensitive).",
)
option_since = click.option(
    "--since",
    default=None,
    help="Only show events from the last <duration>, e.g. 30m, 2h or 1d. "
    "Cannot be combined with --start-time or --end-time.",
)
option_start_time = click.option(
    "--start-time",
    default=None,
    help="Only show events after this time (exclusive). ISO 8601, e.g. 2026-09-01T10:00:00Z.",
)
option_end_time = click.option(
    "--end-time",
    default=None,
    help="Only show events before this time (exclusive). ISO 8601, e.g. 2026-09-01T11:00:00Z.",
)
option_sort = click.option(
    "--sort",
    type=click.Choice(["timestamp", "-timestamp"]),
    default="-timestamp",
    show_default=True,
    help="Sort order: 'timestamp' for oldest first, '-timestamp' for newest first.",
)
option_max_items = click.option(
    "--max-items",
    type=int,
    default=100,
    show_default=True,
    help="Stop after this many events.",
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

option_verbose = click.option(
    "--verbose",
    is_flag=True,
    default=False,
    help="Show full event bodies instead of truncated ones.",
)
option_instance_id = click.option(
    "--instance-id",
    default=None,
    help="Only show events from this instance.",
)
option_node_ip = click.option(
    "--node-ip",
    default=None,
    help="Only show events from the node with this IP.",
)
option_resource_bundles = click.option(
    "--resource-bundles",
    multiple=True,
    help="Only show autoscaler events relevant to these resource bundles. Each value is a "
    "JSON object, e.g. '{\"GPU\": 1}'. Repeat the flag for several.",
)


def _metadata(entity: str):
    return command_metadata(
        status=ReleaseStatus.BETA,
        since="0.0.0",
        output_formats=_OUTPUT_FORMATS,
        examples=[
            CommandExample(
                description=f"Show the most recent events of a {entity}.",
                command=f"anyscale {_GROUP_NAMES[entity]} events --id <{entity}-id>",
            ),
            CommandExample(
                description="Only errors and warnings from the last 30 minutes.",
                command=(
                    f"anyscale {_GROUP_NAMES[entity]} events --id <{entity}-id> "
                    "--level error --level warning --since 30m"
                ),
            ),
            CommandExample(
                description="Structured output for scripts.",
                command=f"anyscale {_GROUP_NAMES[entity]} events --id <{entity}-id> -o json",
            ),
        ],
    )


# The Click group each resource's command hangs under, as the user types it.
_GROUP_NAMES = {
    "job": "job",
    "service": "service",
    "workspace": "workspace_v2",
    "cluster": "cluster",
}


# --- the four commands -----------------------------------------------------------------------


@_metadata("job")
@click.command(name="events", cls=AnyscaleCommand, short_help="List events of a job.", hidden=True)
@click.option("--job-id", "--id", "id", required=True, help="ID of the job.")
@option_source("job")
@option_level
@option_message_contains
@option_since
@option_start_time
@option_end_time
@option_sort
@option_max_items
@option_output
def job_events(id: str, **kwargs: Any) -> None:  # noqa: A002
    """List events of a job: state changes, cluster lifecycle and failures."""
    _run("job", id, **kwargs)


@_metadata("service")
@click.command(
    name="events", cls=AnyscaleCommand, short_help="List events of a service.", hidden=True
)
@click.option("--service-id", "--id", "id", required=True, help="ID of the service.")
@option_source("service")
@option_level
@option_message_contains
@option_since
@option_start_time
@option_end_time
@option_sort
@option_max_items
@option_output
@option_verbose
def service_events(id: str, **kwargs: Any) -> None:  # noqa: A002
    """List events of a service: rollouts, versions, load balancer and cluster activity."""
    _run("service", id, **kwargs)


@_metadata("workspace")
@click.command(
    name="events", cls=AnyscaleCommand, short_help="List events of a workspace.", hidden=True
)
@click.option("--workspace-id", "--id", "id", required=True, help="ID of the workspace.")
@option_source("workspace")
@option_level
@option_message_contains
@option_since
@option_start_time
@option_end_time
@option_sort
@option_max_items
@option_output
def workspace_events(id: str, **kwargs: Any) -> None:  # noqa: A002
    """List events of a workspace: start, stop, snapshots and cluster activity."""
    _run("workspace", id, **kwargs)


@_metadata("cluster")
@click.command(
    name="events", cls=AnyscaleCommand, short_help="List events of a cluster.", hidden=True
)
@click.option("--cluster-id", "--id", "id", required=True, help="ID of the cluster.")
@option_source("cluster")
@option_level
@option_message_contains
@option_since
@option_start_time
@option_end_time
@option_sort
@option_max_items
@option_output
@option_instance_id
@option_node_ip
@option_resource_bundles
def cluster_events(id: str, **kwargs: Any) -> None:  # noqa: A002
    """List events of a cluster: autoscaler decisions, node lifecycle, OS and idle termination."""
    _run("cluster", id, **kwargs)


# --- shared implementation ---------------------------------------------------------------


def _run(  # noqa: PLR0913
    entity: str,
    entity_id: str,
    *,
    source: Tuple[str, ...],
    level: Tuple[str, ...],
    message_contains: Optional[str],
    since: Optional[str],
    start_time: Optional[str],
    end_time: Optional[str],
    sort: str,
    max_items: int,
    output_format: str,
    verbose: bool = False,
    instance_id: Optional[str] = None,
    node_ip: Optional[str] = None,
    resource_bundles: Tuple[str, ...] = (),
) -> None:
    start, end = resolve_window(since, start_time, end_time)

    try:
        events_filter = EventsFilter(
            entity_type=entity,
            entity_id=entity_id,
            # Click already restricted the values; upper-case them so the wire sees the
            # canonical spelling whatever the user typed. None means "all", never [].
            source=[value.upper() for value in source] or None,
            level=[value.upper() for value in level] or None,
            message_contains=message_contains,
            start_time=start,
            end_time=end,
            ascending=(sort == "timestamp"),
            max_items=max_items,
            verbose=verbose,
            instance_id=instance_id,
            node_ip=node_ip,
            resource_bundles=list(resource_bundles) or None,
        )
    except (TypeError, ValueError) as e:
        raise click.UsageError(str(e)) from None

    events = anyscale.events.list(events_filter)

    if output_format == OutputFormat.TEXT.value:
        for event in events:
            click.echo(_format_text_line(event))
    else:
        print_output([_to_row(event) for event in events], output_format, _TABLE_COLUMNS)


def _format_text_line(event: Event) -> str:
    # One event per line: timestamp, then fixed-width level and source, then the message.
    return (
        f"{format_timestamp(event.created_at)}  {event.level:<8} {event.source:<18} "
        f"{event.message or ''}"
    ).rstrip()


def _to_row(event: Event) -> Dict[str, Any]:
    row = event.to_dict()
    row["created_at"] = format_timestamp(event.created_at)
    return row


__all__: List[str] = ["cluster_events", "job_events", "service_events", "workspace_events"]
