"""`anyscale task aggregate`, plus the flags and rendering `anyscale actor aggregate` shares.

The data comes from the observability API on the cloud's system cluster, the way the
console's Tasks and Actors tabs read it: the command describes the system workload for
the cluster's cloud (starting the system cluster unless --no-start-cluster), signs in to
the service, and reads the aggregates. See `_private/workload/observability_api.py`. The
describe call needs a user token: a cluster CLI token (inside a workspace) is not allowed
to start a system cluster.

Output is the model as the API returned it, in every format: text is the model as YAML
(like `anyscale job status`), table is one row per group with the group's fields and its
`metrics` fields side by side, json and yaml are the model. Field names are not rewritten.

The group is `hidden=True` for now: it runs when typed, but is left out of `anyscale
--help`, the committed doc spec and the reference docs. Removing the flag (and the
matching one on the Tasks module in `_private/docgen/__main__.py`) publishes it.
"""

from dataclasses import fields
from typing import Any, Callable, List, Optional, Tuple, Type

import click

import anyscale
from anyscale.commands.doc_metadata import CommandExample
from anyscale.commands.gpu_commands import (
    beta_metadata,
    option_output,
    option_resource,
    print_text,
    resource_ids,
    table_row,
)
from anyscale.commands.output_format import OutputFormat, print_output
from anyscale.commands.util import AnyscaleCommand
from anyscale.task._private.task_sdk import DEFAULT_MAX_ITEMS
from anyscale.task.models import (
    TaskAggregateBy,
    TaskAggregateMetrics,
    TaskExceptionAggregate,
    TaskFunctionAggregate,
    TaskJobAggregate,
)


@click.group("task", help="Inspect the Ray tasks of a cluster.", hidden=True)
def task_cli() -> None:
    pass


# --- shared flags and helpers, used by `anyscale actor aggregate` too ----------------------


def option_by(choices: List[str], help_text: str) -> Callable:
    """`--by`: the grouping, as the design names it (hyphens; the SDK takes underscores)."""
    return click.option(
        "--by",
        "by",
        required=True,
        type=click.Choice(choices, case_sensitive=False),
        help=help_text,
    )


option_ray_session = click.option(
    "--ray-session",
    default=None,
    help="Name of a Ray session: only its tasks or actors. Defaults to every recent "
    "session of the cluster.",
)
option_max_items = click.option(
    "--max-items",
    type=click.IntRange(min=1),
    default=DEFAULT_MAX_ITEMS,
    show_default=True,
    help="How many groups to return at most.",
)
option_start_cluster = click.option(
    "--start-cluster/--no-start-cluster",
    "start_cluster",
    default=True,
    show_default=True,
    help="Start the cloud's system cluster when it is not running, waiting up to ten "
    "minutes for it (a cold start takes a few). With --no-start-cluster, a system cluster "
    "that is not running is an error instead.",
)


def group_columns(group_type: Type[Any], metrics_type: Type[Any]) -> List[str]:
    """Table columns of one grouping: the group's own fields, then its metrics fields."""
    return [
        *[field.name for field in fields(group_type) if field.name != "metrics"],
        *[field.name for field in fields(metrics_type)],
    ]


def group_row(group: Any) -> Any:
    """One table row: the group's fields and its `metrics` fields side by side."""
    row = table_row(group)
    metrics = row.pop("metrics", None)
    return {**row, **table_row(group.metrics)} if metrics is not None else row


def print_groups(page: Any, output_format: str, columns: List[str]) -> None:
    """Render the aggregates, then the API's stale-data note and the page size on stderr."""
    if output_format == OutputFormat.TEXT.value:
        print_text(page)
    elif output_format == OutputFormat.TABLE.value:
        print_output([group_row(group) for group in page.results], output_format, columns)
    else:
        print_output(page, output_format)
    # stderr, so json / yaml on stdout stay parseable.
    if page.warning:
        click.echo(page.warning, err=True)
    if page.total > len(page.results):
        click.echo(
            f"Showing {len(page.results)} of {page.total} groups. Use --max-items to see more.",
            err=True,
        )


# --- aggregate -------------------------------------------------------------------------------

_TASK_GROUP_TYPES = {
    TaskAggregateBy.FUNCTION: TaskFunctionAggregate,
    TaskAggregateBy.JOB: TaskJobAggregate,
    TaskAggregateBy.EXCEPTION: TaskExceptionAggregate,
}
TASK_COLUMNS: Tuple[Tuple[TaskAggregateBy, List[str]], ...] = tuple(
    (by, group_columns(group_type, TaskAggregateMetrics))
    for by, group_type in _TASK_GROUP_TYPES.items()
)


@beta_metadata(
    CommandExample(
        description="Which exceptions are failing the tasks of a job, with counts.",
        command="anyscale task aggregate --by exception --job-id <job-id>",
    ),
    CommandExample(
        description="Every function of a cluster with its counts and timings, one row each.",
        command="anyscale task aggregate --by function --cluster-id <cluster-id> -o table",
    ),
    CommandExample(
        description="Tasks per Ray job of a workspace, without waking a stopped system cluster.",
        command=(
            "anyscale task aggregate --by job --workspace-id <workspace-id> --no-start-cluster"
        ),
    ),
)
@task_cli.command(
    name="aggregate", cls=AnyscaleCommand, short_help="Group the tasks of a cluster."
)
@option_by(
    ["function", "job", "exception"],
    "Group the tasks by Ray function (and task type), by Ray job, or by the exception "
    "type that failed them.",
)
@option_resource
@option_ray_session
@option_max_items
@option_start_cluster
@option_output
def aggregate(  # noqa: PLR0913
    by: str,
    cluster_id: Optional[str],
    workspace_id: Optional[str],
    job_id: Optional[str],
    service_id: Optional[str],
    ray_session: Optional[str],
    max_items: int,
    start_cluster: bool,
    output_format: str,
) -> None:
    """Group the Ray tasks of a cluster, workspace, job or service by function, job or
    exception, with counts and timings per group.

    The data is read from the cloud's system cluster, as the console's Tasks tab does, so
    a cold system cluster is started first and the command waits for it. Needs a user
    token: a cluster CLI token cannot start a system cluster.
    """
    ids = resource_ids(cluster_id, workspace_id, job_id, service_id)
    page = anyscale.task.aggregate(
        by=by,
        **ids,
        ray_session=ray_session,
        max_items=max_items,
        start_cluster=start_cluster,
    )
    print_groups(page, output_format, dict(TASK_COLUMNS)[page.by])


__all__: List[str] = [
    "TASK_COLUMNS",
    "aggregate",
    "group_columns",
    "group_row",
    "option_by",
    "option_max_items",
    "option_ray_session",
    "option_start_cluster",
    "print_groups",
    "task_cli",
]
