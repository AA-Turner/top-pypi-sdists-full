# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

from typing import Tuple

import click
from click import Context

from tinybird.tb.client import DoesNotExistException, TinyB
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.common import echo_safe_humanfriendly_tables_format_smart_table
from tinybird.tb.modules.exceptions import CLIException
from tinybird.tb.modules.feedback_manager import FeedbackManager


@cli.group()
@click.pass_context
def job(ctx: Context) -> None:
    """Jobs commands."""


@job.command(name="ls")
@click.option(
    "-s",
    "--status",
    help="Show only jobs with this status",
    type=click.Choice(["waiting", "working", "done", "error", "cancelling", "cancelled"], case_sensitive=False),
    multiple=True,
    default=None,
)
@click.option(
    "-k",
    "--kind",
    help="Show only jobs of this kind",
    multiple=True,
    default=None,
)
@click.pass_context
def jobs_ls(ctx: Context, status: Tuple[str, ...], kind: Tuple[str, ...]) -> None:
    """List jobs, up to 100"""
    client: TinyB = ctx.ensure_object(dict)["client"]
    jobs = client.jobs(status=status, kind=kind)
    columns = ["id", "kind", "status", "created at", "updated at", "job url"]
    click.echo(FeedbackManager.info_jobs())
    table = []
    for j in jobs:
        table.append([j[c.replace(" ", "_")] for c in columns])
    echo_safe_humanfriendly_tables_format_smart_table(table, column_names=columns)
    click.echo("\n")


@job.command(name="details")
@click.argument("job_id")
@click.pass_context
def job_details(ctx: Context, job_id: str) -> None:
    """Get details for any job created in the last 48h"""
    client: TinyB = ctx.ensure_object(dict)["client"]
    job = client.job(job_id)
    columns = []
    click.echo(FeedbackManager.info_job(job=job_id))
    table = []
    columns = job.keys()
    table = [job.values()]
    echo_safe_humanfriendly_tables_format_smart_table(table, column_names=columns)
    click.echo("\n")


@job.command(name="cancel")
@click.argument("job_id")
@click.pass_context
def job_cancel(ctx: Context, job_id: str) -> None:
    """Try to cancel a job"""
    client = ctx.ensure_object(dict)["client"]

    try:
        result = client.job_cancel(job_id)
    except DoesNotExistException:
        raise CLIException(FeedbackManager.error_job_does_not_exist(job_id=job_id))
    except Exception as e:
        raise CLIException(FeedbackManager.error_exception(error=e))
    else:
        current_job_status = result["status"]
        if current_job_status == "cancelling":
            click.echo(FeedbackManager.success_job_cancellation_cancelling(job_id=job_id))
        elif current_job_status == "cancelled":
            click.echo(FeedbackManager.success_job_cancellation_cancelled(job_id=job_id))
        else:
            raise CLIException(FeedbackManager.error_job_cancelled_but_status_unknown(job_id=job_id))
    click.echo("\n")
