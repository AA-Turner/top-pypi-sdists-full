# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

import json
import re
from typing import Optional, Tuple

import click
from click import Context

from tinybird.datafile.common import get_name_version
from tinybird.tb.client import AuthNoTokenException, TinyB
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.common import echo_safe_humanfriendly_tables_format_smart_table, wait_job
from tinybird.tb.modules.exceptions import CLIPipeException
from tinybird.tb.modules.feedback_manager import FeedbackManager


@cli.group()
@click.pass_context
def copy(ctx):
    """Copy pipe commands."""


@copy.command(name="ls")
@click.option("--match", default=None, help="Retrieve any resourcing matching the pattern. eg --match _test")
@click.option(
    "--format",
    "format_",
    type=click.Choice(["json"], case_sensitive=False),
    default=None,
    help="Force a type of the output",
)
@click.pass_context
def copy_ls(ctx: Context, match: str, format_: str):
    """List copy pipes"""

    client: TinyB = ctx.ensure_object(dict)["client"]
    pipes = client.pipes(dependencies=False, node_attrs="name", attrs="name,updated_at,type")
    copies = [p for p in pipes if p.get("type") == "copy"]
    copies = sorted(copies, key=lambda p: p["updated_at"])
    columns = ["name", "updated at", "nodes"]
    table_human_readable = []
    table_machine_readable = []
    pattern = re.compile(match) if match else None
    for t in copies:
        tk = get_name_version(t["name"])
        if pattern and not pattern.search(tk["name"]):
            continue
        table_human_readable.append((tk["name"], t["updated_at"][:-7], len(t["nodes"])))
        table_machine_readable.append(
            {
                "name": tk["name"],
                "updated at": t["updated_at"][:-7],
                "nodes": len(t["nodes"]),
            }
        )

    if not format_:
        click.echo(FeedbackManager.info_pipes())
        echo_safe_humanfriendly_tables_format_smart_table(table_human_readable, column_names=columns)
        click.echo("\n")
    elif format_ == "json":
        click.echo(json.dumps({"pipes": table_machine_readable}, indent=2))
    else:
        raise CLIPipeException(FeedbackManager.error_pipe_ls_type())


@copy.command(name="run", short_help="Run an on-demand copy job")
@click.argument("pipe_name_or_id")
@click.option("--wait", is_flag=True, default=False, help="Wait for the copy job to finish")
@click.option(
    "--mode", type=click.Choice(["append", "replace"], case_sensitive=True), default=None, help="Copy strategy"
)
@click.option(
    "--param",
    nargs=1,
    type=str,
    multiple=True,
    default=None,
    help="Key and value of the params you want the Copy pipe to be called with. For example: tb pipe copy run <my_copy_pipe> --param foo=bar",
)
@click.pass_context
def copy_run(ctx: click.Context, pipe_name_or_id: str, wait: bool, mode: str, param: Optional[Tuple[str]]):
    """Run an on-demand copy pipe"""

    params = dict(key_value.split("=") for key_value in param) if param else {}
    click.echo(FeedbackManager.highlight(message=f"\n» Running on-demand copy '{pipe_name_or_id}'"))
    client: TinyB = ctx.ensure_object(dict)["client"]

    try:
        response = client.pipe_run(pipe_name_or_id, "copy", params, mode)
        job_id = response["job"]["job_id"]
        job_url = response["job"]["job_url"]
        target_datasource_id = response["tags"]["copy_target_datasource"]
        target_datasource = client.get_datasource(target_datasource_id)
        target_datasource_name = target_datasource["name"]
        click.echo(FeedbackManager.gray(message="Job URL: ") + FeedbackManager.info(message=f"{job_url}"))
        click.echo(FeedbackManager.success(message=f"✓ Copy to '{target_datasource_name}' job created"))

        if wait:
            click.echo("\n")
            wait_job(client, job_id, job_url, FeedbackManager.highlight(message="» Copying data"))
            click.echo(FeedbackManager.success(message=f"✓ Data copied to '{target_datasource_name}'"))

    except AuthNoTokenException:
        raise
    except Exception as e:
        raise CLIPipeException(FeedbackManager.error_creating_copy_job(error=e))
