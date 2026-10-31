"""`anyscale metrics names|query|query-range`.

Three commands over the backend's PromQL endpoints. Each takes exactly one resource id
(cluster, workspace, job or service); the backend resolves it, checks read permission,
and restricts the query to that resource, so nothing here filters client-side.

The group is `hidden=True` for now: it runs when typed, but is left out of `anyscale
--help`, the committed doc spec and the reference docs. Removing the flag (and the
matching one on the Metrics module in `_private/docgen/__main__.py`) publishes it.
"""

from datetime import datetime
import math
from typing import Any, Dict, List, Optional, Tuple

import click

import anyscale
from anyscale.commands.doc_metadata import (
    command_metadata,
    CommandExample,
    ReleaseStatus,
)
from anyscale.commands.output_format import OutputFormat, print_output
from anyscale.commands.time_flags import (
    format_timestamp,
    parse_duration,
    parse_timestamp,
    resolve_window,
)
from anyscale.commands.util import AnyscaleCommand
from anyscale.metrics.models import MetricSeries, MetricsResource


_OUTPUT_FORMATS = [OutputFormat.TEXT, OutputFormat.JSON, OutputFormat.YAML, OutputFormat.TABLE]
_NAME_COLUMNS = ["name"]
_SERIES_COLUMNS = ["timestamp", "metric", "value"]

_RESOURCE_FLAGS = "--cluster-id, --workspace-id, --job-id or --service-id"


@click.group(
    "metrics",
    help="Query Ray metrics of a cluster, workspace, job or service.",
    hidden=True,
)
def metrics_cli() -> None:
    pass


# --- shared flags, declared once ------------------------------------------------------------

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
option_since = click.option(
    "--since",
    default=None,
    help="Use the last <duration> as the window, e.g. 30m, 2h or 1d. "
    "Cannot be combined with --start-time or --end-time.",
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
) -> MetricsResource:
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
        return MetricsResource(resource_type=resource_type, resource_id=resource_id)
    except (TypeError, ValueError) as e:
        raise click.UsageError(str(e)) from None


def _metadata(*examples: CommandExample):
    return command_metadata(
        status=ReleaseStatus.BETA,
        since="0.0.0",
        output_formats=_OUTPUT_FORMATS,
        examples=list(examples),
    )


# --- names -----------------------------------------------------------------------------------


@_metadata(
    CommandExample(
        description="List every metric a cluster has data for.",
        command="anyscale metrics names --cluster-id <cluster-id>",
    ),
    CommandExample(
        description="Only metrics with data in a window.",
        command=(
            "anyscale metrics names --cluster-id <cluster-id> "
            "--start-time 2026-09-01T00:00:00Z --end-time 2026-09-02T00:00:00Z"
        ),
    ),
    CommandExample(
        description="Structured output for scripts.",
        command="anyscale metrics names --job-id <job-id> -o json",
    ),
)
@metrics_cli.command(
    name="names", cls=AnyscaleCommand, short_help="List metric names of a resource."
)
@option_cluster_id
@option_workspace_id
@option_job_id
@option_service_id
@option_start_time
@option_end_time
@option_output
def names(  # noqa: PLR0913
    cluster_id: Optional[str],
    workspace_id: Optional[str],
    job_id: Optional[str],
    service_id: Optional[str],
    start_time: Optional[str],
    end_time: Optional[str],
    output_format: str,
) -> None:
    """List the metric names that have data for a cluster, workspace, job or service.

    This is the discovery step before writing a PromQL query. Without --start-time and
    --end-time the whole retention window (90 days) is searched.
    """
    resource = _resource(cluster_id, workspace_id, job_id, service_id)
    start = parse_timestamp(start_time, "--start-time")
    end = parse_timestamp(end_time, "--end-time")
    if start is not None and end is not None and end <= start:
        raise click.UsageError("--end-time must be after --start-time.")

    metric_names = anyscale.metrics.names(resource, start=start, end=end)

    if output_format == OutputFormat.TEXT.value:
        for name in metric_names:
            click.echo(name)
    elif output_format == OutputFormat.TABLE.value:
        print_output([{"name": name} for name in metric_names], output_format, _NAME_COLUMNS)
    else:
        print_output(metric_names, output_format)


# --- query -----------------------------------------------------------------------------------


@_metadata(
    CommandExample(
        description="Current CPU utilization of every node of a cluster.",
        command="anyscale metrics query 'ray_node_cpu_utilization' --cluster-id <cluster-id>",
    ),
    CommandExample(
        description="One number: total CPU utilization across the cluster, as of a moment.",
        command=(
            "anyscale metrics query 'sum(ray_node_cpu_utilization)' "
            "--cluster-id <cluster-id> --time 2026-09-01T14:00:00Z"
        ),
    ),
    CommandExample(
        description="Structured output for scripts.",
        command="anyscale metrics query 'ray_node_mem_used' --workspace-id <workspace-id> -o json",
    ),
)
@metrics_cli.command(
    name="query", cls=AnyscaleCommand, short_help="Evaluate a PromQL query at one moment."
)
@click.argument("query")
@option_cluster_id
@option_workspace_id
@option_job_id
@option_service_id
@click.option(
    "--time",
    default=None,
    help="Evaluate the query as of this moment. ISO 8601, e.g. 2026-09-01T14:00:00Z. "
    "Defaults to now.",
)
@option_output
def query(  # noqa: PLR0913
    query: str,  # noqa: A002
    cluster_id: Optional[str],
    workspace_id: Optional[str],
    job_id: Optional[str],
    service_id: Optional[str],
    time: Optional[str],
    output_format: str,
) -> None:
    """Evaluate a PromQL expression at one moment for a cluster, workspace, job or service.

    QUERY is the PromQL expression, e.g. 'sum(ray_node_cpu_utilization)'. Quote it so the
    shell leaves it alone. The backend restricts it to the named resource, so a selector
    that names another resource is rejected.
    """
    resource = _resource(cluster_id, workspace_id, job_id, service_id)
    series = anyscale.metrics.query(query, resource, time=parse_timestamp(time, "--time"))
    _print_series(series, output_format)


# --- query-range -----------------------------------------------------------------------------


@_metadata(
    CommandExample(
        description="Memory used by every node over the last two hours, one point per minute.",
        command=(
            "anyscale metrics query-range 'ray_node_mem_used' --cluster-id <cluster-id> "
            "--since 2h --step 1m"
        ),
    ),
    CommandExample(
        description="An explicit window.",
        command=(
            "anyscale metrics query-range 'ray_node_cpu_utilization' --job-id <job-id> "
            "--start-time 2026-09-01T00:00:00Z --end-time 2026-09-01T06:00:00Z --step 5m"
        ),
    ),
    CommandExample(
        description="Structured output for plotting.",
        command=(
            "anyscale metrics query-range 'ray_node_mem_used' --cluster-id <cluster-id> "
            "--since 1h -o json"
        ),
    ),
)
@metrics_cli.command(
    name="query-range",
    cls=AnyscaleCommand,
    short_help="Evaluate a PromQL query across a time window.",
)
@click.argument("query")
@option_cluster_id
@option_workspace_id
@option_job_id
@option_service_id
@option_since
@option_start_time
@option_end_time
@click.option(
    "--step",
    default=None,
    help="Distance between points: a number followed by s, m, h or d, e.g. 15s or 5m. "
    "Default: the larger of 15s and the window divided by 1000, so the result never has "
    "more than 1000 points per series.",
)
@option_output
def query_range(  # noqa: PLR0913
    query: str,  # noqa: A002
    cluster_id: Optional[str],
    workspace_id: Optional[str],
    job_id: Optional[str],
    service_id: Optional[str],
    since: Optional[str],
    start_time: Optional[str],
    end_time: Optional[str],
    step: Optional[str],
    output_format: str,
) -> None:
    """Evaluate a PromQL expression at every step across a time window.

    QUERY is the PromQL expression, e.g. 'ray_node_mem_used'. Quote it so the shell leaves
    it alone. Give the window as either --since, or both --start-time and --end-time. The
    backend restricts the query to the named resource.

    Without --step the distance between points grows with the window (the larger of 15s
    and the window divided by 1000), so a long window never hits the server's limit on
    points per series.
    """
    resource = _resource(cluster_id, workspace_id, job_id, service_id)
    start, end = _required_window(since, start_time, end_time)
    if step is not None:
        # Validate the grammar here; the value itself is sent as typed, Prometheus reads it.
        parse_duration(step, "--step")
    series = anyscale.metrics.query_range(query, resource, start=start, end=end, step=step)
    _print_series(series, output_format, is_range=True)


# --- shared implementation ---------------------------------------------------------------


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


def _print_series(
    series: List[MetricSeries], output_format: str, *, is_range: bool = False
) -> None:
    # The text layout follows the command, not the sample count: a range query that
    # happens to return one point per series still prints as a block.
    if output_format == OutputFormat.TEXT.value:
        for item in series:
            if not is_range:
                # Instant query: one line per series.
                sample = item.samples[0]
                click.echo(
                    f"{format_timestamp(sample.timestamp)}  {_selector(item)}  "
                    f"{_format_value(sample.value)}"
                )
            else:
                # Range query: the series once, then one indented line per point.
                click.echo(_selector(item))
                for sample in item.samples:
                    click.echo(
                        f"  {format_timestamp(sample.timestamp)}  {_format_value(sample.value)}"
                    )
        return

    if output_format == OutputFormat.TABLE.value:
        rows: List[Dict[str, Any]] = [
            {
                "timestamp": format_timestamp(sample.timestamp),
                "metric": _selector(item),
                "value": _format_value(sample.value),
            }
            for item in series
            for sample in item.samples
        ]
        print_output(rows, output_format, _SERIES_COLUMNS)
        return

    plain = [item.to_dict() for item in series]
    for item in plain:
        for sample in item["samples"]:
            sample["value"] = _prometheus_value(sample["value"])
    print_output(plain, output_format)


def _prometheus_value(value: float) -> Any:
    # JSON has no NaN or Inf; write them the way Prometheus does.
    if math.isnan(value):
        return "NaN"
    if math.isinf(value):
        return "+Inf" if value > 0 else "-Inf"
    return value


def _selector(series: MetricSeries) -> str:
    """``name{label="value",...}`` as Prometheus would print the series."""
    name = series.labels.get("__name__", "")
    labels = ",".join(
        f'{key}="{value}"' for key, value in sorted(series.labels.items()) if key != "__name__"
    )
    if labels:
        return f"{name}{{{labels}}}"
    return name or "{}"


def _format_value(value: float) -> str:
    # Whole numbers print without a trailing .0 (2277806080, not 2277806080.0); anything
    # else, NaN and Inf included, prints the way Python does.
    if value == value and abs(value) != float("inf") and value == int(value):  # noqa: PLR0124
        return str(int(value))
    return repr(value)


__all__: List[str] = ["metrics_cli", "names", "query", "query_range"]
