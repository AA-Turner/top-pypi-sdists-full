import json
import re

import click

from tinybird.datafile.common import PipeTypes, get_name_version
from tinybird.tb.client import TinyB
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.common import (
    echo_safe_humanfriendly_tables_format_smart_table,
    wait_job,
)
from tinybird.tb.modules.exceptions import CLIPipeException
from tinybird.tb.modules.feedback_manager import FeedbackManager


@cli.group()
@click.pass_context
def materialization(ctx):
    """Materialization commands."""


@materialization.command(name="ls")
@click.option("--match", default=None, help="Retrieve any resourcing matching the pattern. For example, --match _test")
@click.option(
    "--format",
    "format_",
    type=click.Choice(["json"], case_sensitive=False),
    default=None,
    help="Force a type of the output",
)
@click.pass_context
def materialization_ls(ctx: click.Context, match: str, format_: str):
    """List materializations"""

    client: TinyB = ctx.ensure_object(dict)["client"]
    pipes = client.pipes(dependencies=True, node_attrs="name,materialized", attrs="name,updated_at,endpoint,type")
    materializations = [p for p in pipes if p.get("type") == PipeTypes.MATERIALIZED]
    materializations = sorted(materializations, key=lambda p: p["updated_at"])
    datasources = client.datasources()
    columns = ["name", "updated at", "nodes", "target datasource"]
    table_human_readable = []
    table_machine_readable = []
    pattern = re.compile(match) if match else None
    for t in materializations:
        tk = get_name_version(t["name"])
        if pattern and not pattern.search(tk["name"]):
            continue
        target_datasource_id = next((n["materialized"] for n in t["nodes"] if n.get("materialized")), None)
        target_datasource = next((d for d in datasources if d["id"] == target_datasource_id), None)
        target_datasource_name = target_datasource.get("name", "") if target_datasource else ""
        table_human_readable.append((tk["name"], t["updated_at"][:-7], len(t["nodes"]), target_datasource_name))
        table_machine_readable.append(
            {
                "name": tk["name"],
                "updated at": t["updated_at"][:-7],
                "nodes": len(t["nodes"]),
                "target datasource": target_datasource_name,
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


@materialization.command(name="populate")
@click.argument("pipe_name")
@click.option("--node", type=str, help="Name of the materialized node.", default=None, required=False)
@click.option(
    "--sql-condition",
    type=str,
    default=None,
    help="Populate with a SQL condition to be applied to the trigger data source of the materialized view. For instance, `--sql-condition='date == toYYYYMM(now())'` it'll populate taking all the rows from the trigger data source which `date` is the current month. Use it together with --populate. --sql-condition is not taken into account if the --subset param is present. Including in the ``sql_condition`` any column present in the data source ``engine_sorting_key`` will make the populate job process less data.",
)
@click.option(
    "--truncate", is_flag=True, default=False, help="Truncates the materialized data source before populating it."
)
@click.option(
    "--wait",
    is_flag=True,
    default=False,
    help="Waits for populate jobs to finish, showing a progress bar. Disabled by default.",
)
@click.option(
    "--on-demand-compute",
    is_flag=True,
    default=False,
    help="Use on-demand compute instances for the populate job.",
)
@click.pass_context
def pipe_populate(
    ctx: click.Context,
    pipe_name: str,
    node: str,
    sql_condition: str,
    truncate: bool,
    wait: bool,
    on_demand_compute: bool,
):
    """Populate the result of a Materialized Node into the target materialized view"""

    click.echo(
        "Populating a materialized view on-demand is not supported yet. You can backfill data sources via Deployments."
    )
    return

    cl: TinyB = ctx.ensure_object(dict)["client"]

    pipe = cl.pipe(pipe_name)

    if pipe["type"] != PipeTypes.MATERIALIZED:
        raise CLIPipeException(FeedbackManager.error_pipe_not_materialized(pipe=pipe_name))

    if not node:
        materialized_ids = [pipe_node["id"] for pipe_node in pipe["nodes"] if pipe_node.get("materialized") is not None]

        if not materialized_ids:
            raise CLIPipeException(FeedbackManager.error_populate_no_materialized_in_pipe(pipe=pipe_name))

        elif len(materialized_ids) > 1:
            raise CLIPipeException(FeedbackManager.error_populate_several_materialized_in_pipe(pipe=pipe_name))

        node = materialized_ids[0]

    response = cl.populate_node(
        pipe_name, node, populate_condition=sql_condition, truncate=truncate, on_demand_compute=on_demand_compute
    )
    if "job" not in response:
        raise CLIPipeException(response)

    job_id = response["job"]["id"]
    job_url = response["job"]["job_url"]
    if sql_condition:
        click.echo(FeedbackManager.info_populate_condition_job_url(url=job_url, populate_condition=sql_condition))
    else:
        click.echo(FeedbackManager.info_populate_job_url(url=job_url))
    if wait:
        wait_job(cl, job_id, job_url, "Populating")
