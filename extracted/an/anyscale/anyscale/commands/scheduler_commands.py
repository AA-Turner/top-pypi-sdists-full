from dataclasses import fields
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Sequence

import click

import anyscale
from anyscale.cli_logger import BlockLogger
from anyscale.commands import command_examples
from anyscale.commands.doc_metadata import (
    command_metadata,
    CommandExample,
    ReleaseStatus,
)
from anyscale.commands.gpu_commands import (
    option_output,
    OUTPUT_FORMATS,
    print_text,
    table_row,
)
from anyscale.commands.output_format import (
    OUTPUT_FLAG,
    OUTPUT_FLAG_LONG,
    OutputFormat,
    print_output,
)
from anyscale.commands.util import AnyscaleCommand
from anyscale.scheduler._private.scheduler_sdk import (
    DEFAULT_MAX_CONSUMERS,
    DEFAULT_MAX_QUEUES,
    DEFAULT_MAX_WORKLOADS,
    MAX_CONSUMERS,
    MAX_QUEUES,
    MAX_WORKLOADS,
)
from anyscale.scheduler.models import (
    CloudRollup,
    MarketBreakdown,
    MatchExpression,
    NodeCounts,
    Operator,
    QueueWorkload,
    QueueWorkloadList,
    ResourceFlavor,
    ResourceQueueStatus,
    ResourceQueueStatusPage,
    ResourceUsage,
    SchedulerConfig,
    SchedulerConfigVersion,
    SchedulerConfigVersionSummary,
    SchedulerOverview,
    SchedulerTotals,
    TopConsumer,
    TopologySummary,
    WorkloadCounts,
    WorkloadNodes,
    WorkloadState,
    WorkloadStatus,
)
from anyscale.util import validate_non_negative_arg


log = BlockLogger()


_CONFIRMATION_PHRASE = "change config"

_NO_CATCH_ALL_RULE_WARNING = (
    "No catch-all scheduling rule is configured (a rule with no selector "
    "matches every workload). Workloads that do not match any scheduling "
    "rule will be rejected and fail."
)


@click.group(
    "scheduler",
    help="Manage the Anyscale Global Resource Scheduler.",
)
def scheduler_cli() -> None:
    pass


@scheduler_cli.group("config", help="Manage scheduler configurations.")
def config_cli() -> None:
    pass


@command_metadata(
    status=ReleaseStatus.BETA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Apply a scheduler config from a YAML file.",
            command="anyscale scheduler config apply -f scheduler-config.yaml",
            output_raw=command_examples.SCHEDULER_CONFIG_APPLY_EXAMPLE,
        ),
    ],
)
@config_cli.command(
    name="apply",
    short_help="Apply a scheduler config, creating a new active version.",
    cls=AnyscaleCommand,
    is_beta=True,
)
@click.option(
    "-f",
    "--config-file",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    help="Path to a YAML file containing the scheduler config.",
)
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    default=False,
    help="Skip asking for confirmation.",
)
def apply(config_file: str, yes: bool) -> None:
    """Apply a scheduler config, creating a new active version.

    The previous active version becomes inactive but remains queryable with
    `config list` and `config get --version N`.
    """
    try:
        config = SchedulerConfig.from_yaml(config_file)
    except Exception as e:  # noqa: BLE001 - YAML parse / schema validation surfaces here
        raise click.ClickException(
            f"Failed to load scheduler config from '{config_file}': {e}"
        ) from None

    if _should_warn_no_catch_all_rule(config):
        log.warning(_NO_CATCH_ALL_RULE_WARNING)

    if not yes:
        _confirm_config_change("apply")

    try:
        with log.spinner("Applying scheduler config..."):
            version: int = anyscale.scheduler.apply_config(config=config)
    except (ValueError, RuntimeError) as e:
        raise click.ClickException(str(e)) from None

    log.info(f"Applied scheduler config (version {version}).")


@command_metadata(
    status=ReleaseStatus.BETA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Roll back to scheduler config version 2.",
            command="anyscale scheduler config rollback --version 2",
            output_raw=command_examples.SCHEDULER_CONFIG_ROLLBACK_EXAMPLE,
        ),
    ],
)
@config_cli.command(
    name="rollback",
    short_help="Roll back to a scheduler config version, creating a new active version.",
    cls=AnyscaleCommand,
    is_beta=True,
)
@click.option(
    "--version",
    "version",
    required=True,
    type=int,
    help="Version whose config is applied as the new active version.",
)
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    default=False,
    help="Skip asking for confirmation.",
)
def rollback(version: int, yes: bool) -> None:
    """Roll back to a scheduler config version, creating a new active version.

    The config of `--version N` is applied as a new version. Version N stays in
    history unchanged, so `config list` keeps every version and a rollback can
    itself be rolled back.
    """
    try:
        with log.spinner(_get_spinner_text(version)):
            source: SchedulerConfigVersion = anyscale.scheduler.get_config(version=version)
    except (ValueError, RuntimeError) as e:
        raise click.ClickException(str(e)) from None

    if _should_warn_no_catch_all_rule(source.config):
        log.warning(_NO_CATCH_ALL_RULE_WARNING)

    if not yes:
        _confirm_config_change("roll back")

    try:
        with log.spinner(f"Rolling back to scheduler config version {version}..."):
            new_version: int = anyscale.scheduler.rollback_config(version=version)
    except (ValueError, RuntimeError) as e:
        raise click.ClickException(str(e)) from None

    log.info(
        f"Rolled back to scheduler config version {version} (applied as version {new_version})."
    )


@command_metadata(
    status=ReleaseStatus.BETA,
    since="0.0.0",
    output_formats=[OutputFormat.YAML, OutputFormat.JSON],
    examples=[
        CommandExample(
            description="Get the active scheduler config.",
            command="anyscale scheduler config get",
            output_instance=lambda: SchedulerConfigVersion(
                version=3,
                is_active=True,
                created_at=datetime(2026, 4, 25, 10, 0, 0),
                creator_id="usr_abc123",
                config=SchedulerConfig(
                    resource_flavors=[
                        ResourceFlavor(
                            name="spot",
                            selector=[
                                MatchExpression(
                                    key="market-type",
                                    operator=Operator.IN,
                                    values=["SPOT"],
                                )
                            ],
                        )
                    ],
                ),
            ),
        ),
    ],
    output_schema=SchedulerConfigVersion,
)
@config_cli.command(
    name="get",
    short_help="Get the active scheduler config, or a specific version.",
    cls=AnyscaleCommand,
    is_beta=True,
)
@click.option(
    "--version",
    "version",
    required=False,
    default=None,
    type=int,
    help="Version to fetch. Omit to fetch the active config.",
)
@click.option(
    OUTPUT_FLAG,
    OUTPUT_FLAG_LONG,
    "output_format",
    type=click.Choice([OutputFormat.YAML.value, OutputFormat.JSON.value]),
    default=OutputFormat.YAML.value,
    show_default=True,
    help="Output format for the result.",
)
def get(version: Optional[int], output_format: str) -> None:
    """Get the active scheduler config, or a specific version."""
    try:
        with log.spinner(_get_spinner_text(version)):
            result: SchedulerConfigVersion = anyscale.scheduler.get_config(
                version=version,
            )
    except (ValueError, RuntimeError) as e:
        raise click.ClickException(str(e)) from None

    print_output(result, output_format)


@command_metadata(
    status=ReleaseStatus.BETA,
    since="0.0.0",
    output_formats=[OutputFormat.TABLE, OutputFormat.JSON, OutputFormat.YAML],
    examples=[
        CommandExample(
            description="List scheduler config versions.",
            command="anyscale scheduler config list",
            output_instance=lambda: [
                SchedulerConfigVersionSummary(
                    version=3,
                    created_at=datetime(2026, 4, 25, 10, 0, 0),
                    creator_id="usr_abc123",
                ),
                SchedulerConfigVersionSummary(
                    version=2,
                    created_at=datetime(2026, 4, 20, 8, 30, 0),
                    creator_id="usr_abc123",
                ),
            ],
        ),
    ],
    output_schema=SchedulerConfigVersionSummary,
)
@config_cli.command(
    name="list",
    short_help="List scheduler config versions, newest first.",
    cls=AnyscaleCommand,
    is_beta=True,
)
@click.option(
    "--max-items",
    required=False,
    default=10,
    type=int,
    show_default=True,
    callback=validate_non_negative_arg,
    help="Maximum number of versions to return.",
)
@click.option(
    OUTPUT_FLAG,
    OUTPUT_FLAG_LONG,
    "output_format",
    type=click.Choice(
        [OutputFormat.TABLE.value, OutputFormat.JSON.value, OutputFormat.YAML.value]
    ),
    default=OutputFormat.TABLE.value,
    show_default=True,
    help="Output format for the result.",
)
def list_versions(
    max_items: int,
    output_format: str,
) -> None:  # noqa: A001
    """List scheduler config versions, newest first.

    Use `config get --version N` to fetch the full config for a version.
    """
    try:
        with log.spinner("Fetching scheduler config versions..."):
            results: List[SchedulerConfigVersionSummary] = anyscale.scheduler.list_config_versions(
                max_items=max_items,
            )
    except (ValueError, RuntimeError) as e:
        raise click.ClickException(str(e)) from None

    if not results and output_format == OutputFormat.TABLE.value:
        log.info("No scheduler config versions found.")
        return

    print_output(results, output_format)


# ---- queues (live state) ----
#
# Read-only views of what the scheduler is doing right now, the data behind the console's
# Utilization tab. Output is the model as the API returned it, in every format: text is
# the model as YAML, table is one row per item with a column per field, json and yaml are
# the model. Field names and values are not rewritten.

# Table columns: every field of the model, under its API name, in the API's order.
QUEUE_COLUMNS: List[str] = [field.name for field in fields(ResourceQueueStatus)]
WORKLOAD_COLUMNS: List[str] = [field.name for field in fields(QueueWorkload)]
OVERVIEW_COLUMNS: List[str] = [field.name for field in fields(SchedulerOverview)]
CONSUMER_COLUMNS: List[str] = [field.name for field in fields(TopConsumer)]

_WORKLOAD_ID_FLAGS = "--cluster-id, --workspace-id, --job-id or --service-id"


def _example_queue() -> ResourceQueueStatus:
    return ResourceQueueStatus(
        queue_id="6f1c2a9e-0d3b-4c57-9a41-2b8e7d5f3c10",
        queue="research",
        cohort="ml",
        workloads=WorkloadCounts(running=3, pending=2),
        nodes=NodeCounts(running=12, admitted=2, pending=6),
        quota=[
            ResourceUsage(
                flavor="ondemand",
                resource="gpu",
                used=14.0,
                ceiling=16.0,
                headroom=2.0,
                utilization=0.875,
            )
        ],
        market=MarketBreakdown(spot=0, on_demand=14, unspecified=0),
    )


def _example_workload() -> QueueWorkload:
    return QueueWorkload(
        cluster_id="ses_abc123",
        name="train-llm",
        type="workspace",
        project="default",
        priority=100,
        nodes=WorkloadNodes(requested=4, admitted=0, running=0, pending=4),
        flavors=["ondemand"],
        cloud_id="cld_abc123",
        created_at=datetime(2026, 11, 12, 10, 0, 0, tzinfo=timezone.utc),
        status=WorkloadStatus.QUEUED,
        plan_id="0b9d5c1e-7a42-4f0e-8c3d-5e6f7a8b9c0d",
        queue_position=1,
        requested_resources={"gpu": 4.0},
        url="/cld_abc123/default/workspaces/expwrk_abc123",
    )


def _example_overview() -> SchedulerOverview:
    nodes = NodeCounts(running=40, admitted=4, pending=10)
    workloads = WorkloadCounts(running=9, pending=3)
    market = MarketBreakdown(spot=20, on_demand=24, unspecified=0)
    return SchedulerOverview(
        totals=SchedulerTotals(
            nodes=nodes, active_workloads=12, workloads=workloads, market=market
        ),
        utilization=[
            ResourceUsage(
                flavor="ondemand",
                resource="gpu",
                used=24.0,
                ceiling=32.0,
                headroom=8.0,
                utilization=0.75,
            )
        ],
        clouds=[
            CloudRollup(cloud_id="cld_abc123", nodes=nodes, workloads=workloads, market=market)
        ],
        topology=TopologySummary(
            active_queues=2,
            active_flavors=2,
            active_rules=3,
            active_cohorts=1,
            config_version=3,
            config_updated_at=datetime(2026, 11, 1, 8, 30, 0, tzinfo=timezone.utc),
        ),
    )


def _example_consumer() -> TopConsumer:
    return TopConsumer(
        cluster_id="ses_abc123",
        name="train-llm",
        project="default",
        nodes=8,
        duration_seconds=5400,
        url="/cld_abc123/default/workspaces/expwrk_abc123",
    )


def _queue_metadata(output_schema: Any, *examples: CommandExample):
    return command_metadata(
        status=ReleaseStatus.BETA,
        since="0.0.0",
        output_formats=OUTPUT_FORMATS,
        examples=list(examples),
        output_schema=output_schema,
    )


def _print_result(
    result: Any, rows: Sequence[Any], columns: List[str], output_format: str
) -> None:
    """Write a command's result to stdout in the chosen format.

    text is the model as YAML and json / yaml are the model: all three print `result`.
    table prints one row per item of `rows`, one column per name in `columns`.

    print_output has no renderer for text, which is why text goes through print_text.
    """
    if output_format == OutputFormat.TEXT.value:
        print_text(result)
    elif output_format == OutputFormat.TABLE.value:
        print_output([table_row(row) for row in rows], output_format, columns)
    else:
        print_output(result, output_format)


@scheduler_cli.group("queue", help="Inspect the live state of resource queues.")
def queue_cli() -> None:
    pass


@_queue_metadata(
    ResourceQueueStatusPage,
    CommandExample(
        description="The active queues with their workloads, nodes and quota use.",
        command="anyscale scheduler queue list",
        output_instance=lambda: ResourceQueueStatusPage(results=[_example_queue()]),
    ),
    CommandExample(
        description="One row per queue.",
        command="anyscale scheduler queue list -o table",
    ),
    CommandExample(
        description="The next page, after a run that printed a page token.",
        command="anyscale scheduler queue list --max-items 20 --page-token <token>",
    ),
)
@queue_cli.command(
    name="list",
    short_help="List resource queues with their live state.",
    cls=AnyscaleCommand,
    is_beta=True,
)
@click.option(
    "--max-items",
    type=click.IntRange(min=1, max=MAX_QUEUES),
    default=DEFAULT_MAX_QUEUES,
    show_default=True,
    help="Maximum number of queues to return. When more queues exist, the output ends "
    "with a --page-token for the rest.",
)
@click.option(
    "--page-token",
    default=None,
    help="Token printed by an earlier run, to continue after its last queue.",
)
@option_output
def list_queues(max_items: int, page_token: Optional[str], output_format: str) -> None:
    """List the active resource queues with their live state.

    Each queue shows its running and pending workloads, its running, admitted and pending
    nodes, and its quota use per flavor and resource. To see how the queues are defined,
    run `anyscale scheduler config get`.
    """
    try:
        page: ResourceQueueStatusPage = anyscale.scheduler.list_queues(
            max_items=max_items, page_token=page_token
        )
    except (ValueError, RuntimeError) as e:
        raise click.ClickException(str(e)) from None

    _print_result(page, page.results, QUEUE_COLUMNS, output_format)
    if page.next_page_token is not None:
        # stderr, so json / yaml on stdout stay parseable.
        click.echo(
            f"More queues exist. To see the next page, run again with "
            f"--page-token '{page.next_page_token}'",
            err=True,
        )


@_queue_metadata(
    ResourceQueueStatus,
    CommandExample(
        description="Workloads, nodes and quota use of one queue.",
        command="anyscale scheduler queue get --name research",
        output_instance=_example_queue,
    ),
    CommandExample(
        description="JSON for scripts.",
        command="anyscale scheduler queue get -n research -o json",
    ),
)
@queue_cli.command(
    name="get",
    short_help="Get the live state of a resource queue.",
    cls=AnyscaleCommand,
    is_beta=True,
)
@click.option(
    "--name",
    "-n",
    required=True,
    help="Name of the resource queue, as in the scheduler config.",
)
@option_output
def get_queue(name: str, output_format: str) -> None:
    """Get the live state of one active resource queue.

    Shows its running and pending workloads, its running, admitted and pending nodes, and
    its quota use per flavor and resource. A queue that is not in the active scheduler
    config is an error.
    """
    try:
        queue: ResourceQueueStatus = anyscale.scheduler.get_queue(name)
    except (ValueError, RuntimeError) as e:
        raise click.ClickException(str(e)) from None

    _print_result(queue, [queue], QUEUE_COLUMNS, output_format)


@_queue_metadata(
    QueueWorkloadList,
    CommandExample(
        description="What is waiting in a queue, next to be admitted first.",
        command="anyscale scheduler queue workloads --name research --state pending",
        output_instance=lambda: QueueWorkloadList(results=[_example_workload()], total=1),
    ),
    CommandExample(
        description="Where one job is in that line.",
        command=(
            "anyscale scheduler queue workloads -n research --state pending --job-id <job-id>"
        ),
    ),
    CommandExample(
        description="The workloads that hold capacity, one row each.",
        command="anyscale scheduler queue workloads -n research --state running -o table",
    ),
)
@queue_cli.command(
    name="workloads",
    short_help="List the pending or running workloads of a resource queue.",
    cls=AnyscaleCommand,
    is_beta=True,
)
@click.option(
    "--name",
    "-n",
    required=True,
    help="Name of the resource queue, as in the scheduler config.",
)
@click.option(
    "--state",
    required=True,
    type=click.Choice([state.value for state in WorkloadState], case_sensitive=False),
    help="Which workloads to list: pending (waiting for admission) or running (holding capacity).",
)
@click.option(
    "--max-items",
    type=click.IntRange(min=1, max=MAX_WORKLOADS),
    default=DEFAULT_MAX_WORKLOADS,
    show_default=True,
    help="Maximum number of workloads to return.",
)
@click.option(
    "--cluster-id",
    default=None,
    help=f"Only the workload on this cluster, e.g. ses_abc123. At most one of "
    f"{_WORKLOAD_ID_FLAGS} can be given.",
)
@click.option(
    "--workspace-id",
    default=None,
    help="Only this workspace, e.g. expwrk_abc123. Matches the workspace's cluster.",
)
@click.option(
    "--job-id",
    default=None,
    help="Only this job, e.g. prodjob_abc123. Matches the cluster of the job's latest run.",
)
@click.option(
    "--service-id",
    default=None,
    help="Only this service, e.g. service2_abc123. Matches the cluster of the service's "
    "primary version.",
)
@option_output
def list_queue_workloads(  # noqa: PLR0913
    name: str,
    state: str,
    max_items: int,
    cluster_id: Optional[str],
    workspace_id: Optional[str],
    job_id: Optional[str],
    service_id: Optional[str],
    output_format: str,
) -> None:
    """List the pending or running workloads of a resource queue.

    The pending list is in admission order: `queue_position` 1 is next. It has one row
    per queued request, so a cluster with several queued requests is listed several
    times. The running list has one row per cluster.

    The scheduler identifies a workload by its cluster. To find one workspace, job or
    service, pass its ID and only its rows are returned. When more workloads match than
    --max-items, the output says so on stderr and `total` carries the full count.
    """
    ids: Dict[str, str] = {
        key: value
        for key, value in {
            "cluster_id": cluster_id,
            "workspace_id": workspace_id,
            "job_id": job_id,
            "service_id": service_id,
        }.items()
        if value is not None
    }
    if len(ids) > 1:
        raise click.UsageError(f"At most one of {_WORKLOAD_ID_FLAGS} can be given.")
    # An empty ID (`--job-id "$JOB"` with JOB unset) is an error, not "no filter".
    for key, value in ids.items():
        if not value.strip():
            raise click.UsageError(f"--{key.replace('_', '-')} cannot be empty.")

    try:
        page: QueueWorkloadList = anyscale.scheduler.list_queue_workloads(
            name, state=state, max_items=max_items, **ids
        )
    except (ValueError, RuntimeError) as e:
        raise click.ClickException(str(e)) from None

    _print_result(page, page.results, WORKLOAD_COLUMNS, output_format)
    # A cut list needs no note here: the SDK warns "Showing N of T ..." on stderr.


@_queue_metadata(
    SchedulerOverview,
    CommandExample(
        description="Node and workload totals, quota use, per-cloud totals and topology.",
        command="anyscale scheduler overview",
        output_instance=_example_overview,
    ),
    CommandExample(
        description="JSON for scripts.",
        command="anyscale scheduler overview -o json",
    ),
)
@scheduler_cli.command(
    name="overview",
    short_help="Get the organization-wide scheduler rollup.",
    cls=AnyscaleCommand,
    is_beta=True,
)
@option_output
def overview(output_format: str) -> None:
    """Get the organization-wide scheduler rollup.

    Shows node and workload totals, quota use per flavor and resource, the same totals
    per cloud, and how many queues, flavors, rules and cohorts the active scheduler
    config defines.
    """
    try:
        result: SchedulerOverview = anyscale.scheduler.get_overview()
    except (ValueError, RuntimeError) as e:
        raise click.ClickException(str(e)) from None

    _print_result(result, [result], OVERVIEW_COLUMNS, output_format)


@_queue_metadata(
    TopConsumer,
    CommandExample(
        description="The 10 clusters that hold the most nodes in the organization.",
        command="anyscale scheduler top-consumers",
        output_instance=lambda: [_example_consumer()],
    ),
    CommandExample(
        description="The top 5 of one queue, one row each.",
        command="anyscale scheduler top-consumers --queue research --max-items 5 -o table",
    ),
)
@scheduler_cli.command(
    name="top-consumers",
    short_help="List the clusters that hold the most nodes.",
    cls=AnyscaleCommand,
    is_beta=True,
)
@click.option(
    "--max-items",
    type=click.IntRange(min=1, max=MAX_CONSUMERS),
    default=DEFAULT_MAX_CONSUMERS,
    show_default=True,
    help="Maximum number of clusters to return.",
)
@click.option(
    "--queue",
    default=None,
    help="Name of a resource queue, to count only its clusters. Defaults to the whole "
    "organization.",
)
@option_output
def top_consumers(max_items: int, queue: Optional[str], output_format: str) -> None:
    """List the clusters that hold the most nodes, largest first.

    Counts the whole organization, or one resource queue with --queue. Each row carries
    the cluster ID, the workload's name and project, its node count and its approximate
    run time.
    """
    try:
        consumers: List[TopConsumer] = anyscale.scheduler.list_top_consumers(
            max_items=max_items, queue=queue
        )
    except (ValueError, RuntimeError) as e:
        raise click.ClickException(str(e)) from None

    _print_result(consumers, consumers, CONSUMER_COLUMNS, output_format)


# ---- helpers ----


def _confirm_config_change(action: str) -> None:
    """Gate an org-wide config change behind the typed confirmation phrase.

    `action` completes the sentence "You must type ... to <action>".
    """
    click.echo(
        "\nOnce applied, all workloads in your organization will be admitted, "
        "scheduled, run, or rejected according to this new configuration.\n",
        err=True,
    )
    typed = click.prompt(
        f'Type "{_CONFIRMATION_PHRASE}" to proceed, or press Ctrl+C to cancel',
        type=str,
        # Click re-prompts forever on a blank line unless a default is set.
        default="",
        show_default=False,
        err=True,
    )
    if typed.strip() != _CONFIRMATION_PHRASE:
        raise click.ClickException(
            f'You must type "{_CONFIRMATION_PHRASE}" to {action}. Nothing was applied.'
        )


def _should_warn_no_catch_all_rule(config: SchedulerConfig) -> bool:
    """Whether to warn that the config declares no catch-all scheduling rule.

    A rule with no selector matches every workload, so one anywhere in the list
    means nothing can go unmatched. A config declaring no rules at all admits
    everything, so there is nothing to warn about. Mirrors the console's
    condition.
    """
    rules = config.scheduling_rules
    if not rules:
        return False
    return all(r.selector for r in rules)


def _get_spinner_text(version: Optional[int]) -> str:
    return (
        f"Fetching scheduler config version {version}..."
        if version is not None
        else "Fetching active scheduler config..."
    )
