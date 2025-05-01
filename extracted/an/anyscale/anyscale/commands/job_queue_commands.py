from typing import List

import click

from anyscale.client.openapi_client.models.job_queue_sort_directive import (
    JobQueueSortDirective,
)
from anyscale.client.openapi_client.models.job_queue_sort_field import JobQueueSortField
from anyscale.client.openapi_client.models.sort_order import SortOrder
from anyscale.commands import command_examples
from anyscale.commands.util import AnyscaleCommand
from anyscale.controllers.job_controller import JobController, JobQueueView
from anyscale.util import validate_non_negative_arg


@click.group(
    "job-queues", help="Interact with production job queues running on Anyscale."
)
def job_queue_cli() -> None:
    pass


def parse_sort_fields(
    param: str, sort_fields: List[str],
) -> List[JobQueueSortDirective]:
    sort_directives = []

    for field_str in sort_fields:
        descending = field_str.startswith("-")
        raw_field = field_str.lstrip("-").upper()

        if raw_field not in JobQueueSortField.allowable_values:
            raise click.UsageError(
                f"{param} must be one of {', '.join([v.lower() for v in JobQueueSortField.allowable_values])}"
            )

        sort_directives.append(
            JobQueueSortDirective(
                sort_field=raw_field,
                sort_order=SortOrder.DESC if descending else SortOrder.ASC,
            )
        )

    return sort_directives


@job_queue_cli.command(
    name="list",
    short_help="List job queues.",
    cls=AnyscaleCommand,
    example=command_examples.JOB_QUEUE_LIST,
)
@click.option(
    "--include-all-users",
    is_flag=True,
    default=False,
    help="Include job queues not created by current user.",
)
@click.option(
    "--view",
    type=click.Choice([v.name.lower() for v in JobQueueView], case_sensitive=False),
    default=JobQueueView.DEFAULT.name,
    help="Select which view to display.",
    callback=lambda _, __, value: JobQueueView[value.upper()],
)
@click.option(
    "--page",
    default=100,
    type=int,
    help="Page size (default 100).",
    callback=validate_non_negative_arg,
)
@click.option(
    "--max-items",
    required=False,
    type=int,
    help="Max items to show in list (only valid in interactive mode).",
    callback=lambda ctx, param, value: validate_non_negative_arg(ctx, param, value)
    if value
    else None,
)
@click.option(
    "--sort",
    "sorting_directives",
    multiple=True,
    default=[JobQueueSortField.CREATED_AT],
    help=f"""
        Sort by column(s). Prefix column with - to sort in descending order.
        Supported columns: {', '.join([v.lower() for v in JobQueueSortField.allowable_values])}.
    """,
    callback=lambda _, __, value: parse_sort_fields("sort", list(value)),
)
@click.option(
    "--interactive/--no-interactive",
    default=True,
    help="--no-interactive disables the default interactive mode.",
)
def list_job_queues(
    include_all_users: bool,
    view: JobQueueView,
    page: int,
    max_items: int,
    sorting_directives: List[JobQueueSortDirective],
    interactive: bool,
):
    if max_items is not None and interactive:
        raise click.UsageError("--max-items can only be used in non interactive mode.")
    job_controller = JobController()
    job_controller.list_job_queues(
        max_items=max_items,
        page_size=page,
        include_all_users=include_all_users,
        view=view,
        sorting_directives=sorting_directives,
        interactive=interactive,
    )


@job_queue_cli.command(
    name="update",
    short_help="Update job queue.",
    cls=AnyscaleCommand,
    example=command_examples.JOB_QUEUE_UPDATE,
)
@click.option(
    "--id", "job_queue_id", required=False, default=None, help="ID of the job queue."
)
@click.option(
    "--name",
    "job_queue_name",
    required=False,
    default=None,
    help="Name of the job queue.",
)
@click.option(
    "--max-concurrency",
    required=False,
    default=None,
    help="Maximum concurrency of the job queue",
)
@click.option(
    "--idle-timeout-s",
    required=False,
    default=None,
    help="Idle timeout of the job queue",
)
def update_job_queue(
    job_queue_id: str, job_queue_name: str, max_concurrency: int, idle_timeout_s: int
):
    if job_queue_id is None and job_queue_name is None:
        raise click.ClickException("ID or name of job queue is required")
    job_controller = JobController()
    job_controller.update_job_queue(
        job_queue_id=job_queue_id,
        job_queue_name=job_queue_name,
        max_concurrency=max_concurrency,
        idle_timeout_s=idle_timeout_s,
    )


@job_queue_cli.command(
    name="info",
    short_help="Info of a job queue.",
    cls=AnyscaleCommand,
    example=command_examples.JOB_QUEUE_INFO,
)
@click.option(
    "--id", "job_queue_id", required=True, default=None, help="ID of the job."
)
def get_job_queue(job_queue_id: str):
    job_controller = JobController()
    job_controller.get_job_queue(job_queue_id=job_queue_id)
