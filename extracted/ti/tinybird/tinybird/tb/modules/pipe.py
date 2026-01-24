# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

import json
import re

import click
from click import Context

from tinybird.datafile.common import get_name_version
from tinybird.tb.client import TinyB
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.common import (
    echo_safe_humanfriendly_tables_format_smart_table,
)
from tinybird.tb.modules.exceptions import CLIPipeException
from tinybird.tb.modules.feedback_manager import FeedbackManager


@cli.group(hidden=False)
@click.pass_context
def pipe(ctx):
    """Pipe commands."""


@pipe.command(name="ls")
@click.option("--match", default=None, help="Retrieve any resourcing matching the pattern. For example, --match _test")
@click.option(
    "--format",
    "format_",
    type=click.Choice(["json"], case_sensitive=False),
    default=None,
    help="Force a type of the output",
)
@click.pass_context
def pipe_ls(ctx: Context, match: str, format_: str):
    """List pipes"""

    client: TinyB = ctx.ensure_object(dict)["client"]
    pipes = client.pipes(dependencies=False, node_attrs="name", attrs="name,updated_at,type")
    pipes = sorted(pipes, key=lambda p: p["updated_at"])

    columns = ["name", "published date", "nodes", "type"]
    table_human_readable = []
    table_machine_readable = []
    pattern = re.compile(match) if match else None
    for t in pipes:
        tk = get_name_version(t["name"])
        if pattern and not pattern.search(tk["name"]):
            continue
        table_human_readable.append((tk["name"], t["updated_at"][:-7], len(t["nodes"]), t["type"]))
        table_machine_readable.append(
            {
                "name": tk["name"],
                "published date": t["updated_at"][:-7],
                "nodes": len(t["nodes"]),
                "type": t["type"],
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
