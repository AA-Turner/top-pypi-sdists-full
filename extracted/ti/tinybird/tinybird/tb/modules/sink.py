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
def sink(ctx):
    """Sink pipe commands."""


@sink.command(name="ls")
@click.option("--match", default=None, help="Retrieve any resourcing matching the pattern. eg --match _test")
@click.option(
    "--format",
    "format_",
    type=click.Choice(["json"], case_sensitive=False),
    default=None,
    help="Force a type of the output",
)
@click.pass_context
def sink_ls(ctx: Context, match: str, format_: str):
    """List sink pipes"""

    client: TinyB = ctx.ensure_object(dict)["client"]
    pipes = client.pipes(dependencies=False, node_attrs="name", attrs="name,updated_at,type")
    sinks = [p for p in pipes if p.get("type") == "sink"]
    sinks = sorted(sinks, key=lambda p: p["updated_at"])
    columns = ["name", "updated at", "nodes"]
    table_human_readable = []
    table_machine_readable = []
    pattern = re.compile(match) if match else None
    for t in sinks:
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


@sink.command(name="run", short_help="Run an on-demand sink job")
@click.argument("pipe_name_or_id")
@click.option("--wait", is_flag=True, default=False, help="Wait for the sink job to finish")
@click.option(
    "--mode", type=click.Choice(["append", "replace"], case_sensitive=True), default=None, help="Sink strategy"
)
@click.option(
    "--param",
    nargs=1,
    type=str,
    multiple=True,
    default=None,
    help="Key and value of the params you want the Sink pipe to be called with. For example: tb pipe sink run <my_sink_pipe> --param foo=bar",
)
@click.pass_context
def sink_run(ctx: click.Context, pipe_name_or_id: str, wait: bool, mode: str, param: Optional[Tuple[str]]):
    """Run a sink pipe"""

    params = dict(key_value.split("=") for key_value in param) if param else {}
    click.echo(FeedbackManager.highlight(message=f"\n» Running sink '{pipe_name_or_id}'"))
    client: TinyB = ctx.ensure_object(dict)["client"]

    try:
        response = client.pipe_run(pipe_name_or_id, "sink", params, mode)
        job_id = response["job"]["id"]
        job_url = response["job"]["job_url"]
        click.echo(FeedbackManager.gray(message="Job URL: ") + FeedbackManager.info(message=f"{job_url}"))
        click.echo(FeedbackManager.success(message="✓ Sink job created"))

        if wait:
            click.echo("\n")
            wait_job(client, job_id, job_url, FeedbackManager.highlight(message="» Exporting data"))
            click.echo(FeedbackManager.success(message="✓ Data exported"))

    except AuthNoTokenException:
        raise
    except Exception as e:
        raise CLIPipeException(FeedbackManager.error_creating_sink_job(error=e))
