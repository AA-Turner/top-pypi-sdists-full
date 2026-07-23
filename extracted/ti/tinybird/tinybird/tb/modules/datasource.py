# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

import json
import os
import re
import time
import uuid
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import click
import humanfriendly
import requests
from click import Context

from tinybird.datafile.common import get_name_version
from tinybird.prompts import quarantine_prompt
from tinybird.tb.client import (
    AuthException,
    AuthNoTokenException,
    DoesNotExistException,
    OperationCanNotBePerformed,
    TinyB,
)
from tinybird.tb.modules.build import process as build_project
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.common import (
    _analyze,
    analyze_file,
    echo_safe_humanfriendly_tables_format_smart_table,
    get_format_from_filename_or_url,
    normalize_datasource_name,
    push_data,
    wait_job,
)
from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.connection_dynamodb import connection_create_dynamodb, validate_dynamodb_table
from tinybird.tb.modules.connection_kafka import (
    connection_create_kafka,
    echo_kafka_data,
    meta_to_datasource_datafile,
    select_connection,
    select_group_id,
    select_topic,
)
from tinybird.tb.modules.connection_s3 import (
    connection_create_s3,
    echo_s3_data,
    meta_to_s3_datasource_datafile,
    select_bucket_uri,
    select_sample_file_uri,
    select_schedule,
)
from tinybird.tb.modules.create import (
    generate_gcs_connection_file_with_secrets,
)
from tinybird.tb.modules.datafile.fixture import persist_fixture
from tinybird.tb.modules.exceptions import CLIDatasourceException, CLIException
from tinybird.tb.modules.feedback_manager import FeedbackManager, get_cli_name
from tinybird.tb.modules.llm import LLM
from tinybird.tb.modules.llm_utils import extract_xml
from tinybird.tb.modules.project import Project
from tinybird.tb.modules.secret import save_secret_to_env_file
from tinybird.tb.modules.telemetry import add_telemetry_event

EXPERIMENTAL_FEATURE_USE_V1 = "use_v1"


def _echo_v1_import_jobs_queued(job_ids: list[str], operation: str) -> None:
    for job_id in job_ids:
        click.echo(FeedbackManager.success(message=f"✓ {operation} import job queued: {job_id}"))
        click.echo(FeedbackManager.gray(message=f"Check status: tb job details {job_id}"))


def _wait_for_v1_import_jobs(client: TinyB, job_ids: list[str], operation: str) -> None:
    for job_id in job_ids:
        try:
            wait_job(client, job_id, f"/v0/jobs/{job_id}", f"{operation} import")
        except CLIException:
            if _echo_v1_import_job_details(client, job_id):
                raise click.exceptions.Exit(1)
            raise
        click.echo(FeedbackManager.success(message=f"✓ {operation} import completed: {job_id}"))


def _echo_v1_import_job_details(client: TinyB, job_id: str) -> bool:
    try:
        job = client.job(job_id)
    except Exception:
        return False
    click.echo(FeedbackManager.info_job(job=job_id))
    echo_safe_humanfriendly_tables_format_smart_table([job.values()], column_names=job.keys())
    click.echo("\n")
    return True


def _dynamodb_key_schema_sort_key(key_schema: dict[str, str]) -> int:
    if key_schema.get("key_type") == "HASH":
        return 0
    if key_schema.get("key_type") == "RANGE":
        return 1
    return 2


def _dynamodb_attribute_type(attribute_name: str, validation_result: dict) -> str:
    attribute_type_by_name = {
        str(attribute.get("name")): attribute.get("type")
        for attribute in validation_result.get("attribute_definitions", [])
    }
    if attribute_type_by_name.get(attribute_name) == "N":
        return "Float64"
    return "String"


def _dynamodb_key_columns(validation_result: dict) -> list[str]:
    return [
        str(key_schema["attribute_name"])
        for key_schema in sorted(validation_result.get("key_schema", []), key=_dynamodb_key_schema_sort_key)
        if key_schema.get("attribute_name")
    ]


def create_terminal_box(content: str, new_content: Optional[str] = None, title: Optional[str] = None) -> str:
    lines = content.splitlines() or [""]
    if new_content:
        lines.extend(["", "Updated:", *new_content.splitlines()])

    max_line_width = max(len(line) for line in lines)
    if title:
        max_line_width = max(max_line_width, len(title))

    border = "+" + "-" * (max_line_width + 2) + "+"
    output: list[str] = [border]
    if title:
        output.append(f"| {title.ljust(max_line_width)} |")
        output.append(border)
    output.extend(f"| {line.ljust(max_line_width)} |" for line in lines)
    output.append(border)
    return "\n".join(output)


def _extract_connection_setting(content: str, key: str) -> Optional[str]:
    pattern = re.compile(rf"^{key}\s+(.+)$", re.MULTILINE)
    match = pattern.search(content)
    if not match:
        return None
    value = match.group(1).strip()
    return value.strip("\"'")


def _resolve_dynamodb_role_arn(connection_content: str, project: Project) -> Optional[str]:
    raw = _extract_connection_setting(connection_content, "DYNAMODB_ARN")
    if not raw:
        return None
    secret_match = re.search(r"tb_secret\(\s*[\"']([^\"']+)[\"']", raw)
    if secret_match:
        secret_name = secret_match.group(1)
        return project.get_secrets().get(secret_name)
    return raw or None


@cli.group()
@click.pass_context
def datasource(ctx):
    """Data source commands."""


@datasource.command(name="ls")
@click.option("--match", default=None, help="Retrieve any resources matching the pattern. For example, --match _test")
@click.option(
    "--format",
    "format_",
    type=click.Choice(["json"], case_sensitive=False),
    default=None,
    help="Force a type of the output",
)
@click.pass_context
def datasource_ls(ctx: Context, match: Optional[str], format_: str):
    """List data sources"""

    client: TinyB = ctx.ensure_object(dict)["client"]
    ds = client.datasources()
    columns = ["shared from", "name", "row_count", "size", "created at", "updated at", "connection"]
    table_human_readable = []
    table_machine_readable = []
    pattern = re.compile(match) if match else None

    for t in ds:
        stats = t.get("stats", None)
        if not stats:
            stats = t.get("statistics", {"bytes": ""})
            if not stats:
                stats = {"bytes": ""}

        tk = get_name_version(t["name"])
        if pattern and not pattern.search(tk["name"]):
            continue

        if "." in tk["name"]:
            shared_from, name = tk["name"].split(".")
        else:
            shared_from, name = "", tk["name"]

        table_human_readable.append(
            (
                shared_from,
                name,
                humanfriendly.format_number(stats.get("row_count")) if stats.get("row_count", None) else "-",
                humanfriendly.format_size(int(stats.get("bytes", 0))) if stats.get("bytes", None) else "-",
                t["created_at"][:-7],
                t["updated_at"][:-7],
                t.get("service", ""),
            )
        )
        table_machine_readable.append(
            {
                "shared from": shared_from,
                "name": name,
                "row_count": stats.get("row_count", None) or "-",
                "size": stats.get("bytes", None) or "-",
                "created at": t["created_at"][:-7],
                "updated at": t["updated_at"][:-7],
                "connection": t.get("service", ""),
            }
        )

    if not format_:
        click.echo(FeedbackManager.info_datasources())
        echo_safe_humanfriendly_tables_format_smart_table(table_human_readable, column_names=columns)
        click.echo("\n")
    elif format_ == "json":
        click.echo(json.dumps({"datasources": table_machine_readable}, indent=2))
    else:
        raise CLIDatasourceException(FeedbackManager.error_datasource_ls_type())


@datasource.command(name="append")
@click.argument("datasource_name", required=False)
@click.argument("data", required=False)
@click.option("--url", type=str, help="URL to append data from")
@click.option("--file", type=str, help="Local file to append data from")
@click.option("--events", type=str, help="Events to append data from")
@click.option(
    "--experimental",
    type=click.Choice([EXPERIMENTAL_FEATURE_USE_V1]),
    multiple=True,
    help="Enable an experimental feature. May be specified multiple times.",
)
@click.option("--concurrency", help="How many files to submit concurrently", default=1, hidden=True)
@click.option("--wait", is_flag=True, default=False, help="Wait for a v1 import job to finish.")
@click.pass_context
def datasource_append(
    ctx: Context,
    datasource_name: str,
    data: Optional[str],
    url: str,
    file: str,
    events: str,
    experimental: tuple[str, ...],
    concurrency: int,
    wait: bool,
):
    """
    Appends data to an existing data source from URL, local file  or a connector

    - Events API: `tb datasource append [datasource_name] --events '{"a":"b, "c":"d"}'`\n
    - Local File: `tb datasource append [datasource_name] --file /path/to/local/file`\n
    - Remote URL: `tb datasource append [datasource_name] --url https://url_to_csv`\n
    - Kafka, S3 and GCS: https://www.tinybird.co/docs/forward/get-data-in/connectors\n

    More info: https://www.tinybird.co/docs/forward/get-data-in
    """
    env: str = ctx.ensure_object(dict)["env"]
    client: TinyB = ctx.obj["client"]
    project: Project = ctx.ensure_object(dict)["project"]
    use_v1 = EXPERIMENTAL_FEATURE_USE_V1 in experimental
    if wait and not use_v1:
        raise CLIDatasourceException("--wait requires --experimental=use_v1.")

    # If data is passed as argument, we detect if it's a JSON object, a URL or a file
    if data:
        VALID_EXTENSIONS = [
            "csv",
            "csv.gz",
            "ndjson",
            "ndjson.gz",
            "jsonl",
            "jsonl.gz",
            "json",
            "json.gz",
            "parquet",
            "parquet.gz",
        ]
        is_file_or_url = data and (data.startswith("http") or any(data.endswith(f".{ext}") for ext in VALID_EXTENSIONS))
        if is_file_or_url:
            try:
                if urlparse(data).scheme in ("http", "https"):
                    url = data
            except Exception:
                pass

            if not url:
                file = data
        else:
            events = data

    # If data is not passed as argument, we use the data from the options
    if not data:
        data = file or url or events

    if env == "local":
        tip = f"Did you build your project? Run `{get_cli_name()} build` first."
    else:
        tip = f"Did you deploy your project? Run `{get_cli_name()} --cloud deploy` first."

    datasources = client.datasources()
    if not datasources:
        raise CLIDatasourceException(FeedbackManager.error(message=f"No data sources found. {tip}"))

    if datasource_name and datasource_name not in [ds["name"] for ds in datasources]:
        raise CLIDatasourceException(FeedbackManager.error(message=f"Datasource {datasource_name} not found. {tip}"))

    if not datasource_name:
        datasource_index = -1

        click.echo(FeedbackManager.info(message="\n? Which data source do you want to ingest data into?"))
        while datasource_index == -1:
            for index, datasource in enumerate(datasources):
                click.echo(f"  [{index + 1}] {datasource['name']}")
            click.echo(
                FeedbackManager.gray(
                    message=f"Tip: Run {get_cli_name()} datasource append [datasource_name] to skip this step."
                )
            )

            datasource_index = click.prompt("\nSelect option", default=1)

            if datasource_index == 0:
                click.echo(FeedbackManager.warning(message="Datasource type selection cancelled by user"))
                return None

            try:
                datasource_name = datasources[int(datasource_index) - 1]["name"]
            except Exception:
                datasource_index = -1

    if not datasource_name:
        raise CLIDatasourceException(FeedbackManager.error_datasource_name())

    if not data:
        data_index = -1
        options = (
            "Events API",
            "Local File",
            "Remote URL",
        )
        click.echo(FeedbackManager.info(message="\n? How do you want to ingest data?"))
        while data_index == -1:
            for index, option in enumerate(options):
                click.echo(f"  [{index + 1}] {option}")
            click.echo(
                FeedbackManager.gray(
                    message=f"Tip: Run {get_cli_name()} datasource append [datasource_name] --events | --file | --url to skip this step"
                )
            )

            data_index = click.prompt("\nSelect option", default=1)

            if data_index == 0:
                click.echo(FeedbackManager.warning(message="Data selection cancelled by user"))
                return None

            try:
                data_index = int(data_index)
            except Exception:
                data_index = -1

        if data_index == 1:
            events = click.prompt("Events data")
        elif data_index == 2:
            data = click.prompt("Path to local file")
        elif data_index == 3:
            data = click.prompt("URL to remote file")
        else:
            raise CLIDatasourceException(FeedbackManager.error(message="Invalid ingestion option"))

    if events:
        if use_v1:
            raise CLIDatasourceException("--experimental=use_v1 only supports local files.")
        click.echo(FeedbackManager.highlight(message=f"\n» Sending events to {datasource_name}"))
        events_params = {"name": datasource_name}
        request_from = getattr(client, "request_from", None)
        if request_from:
            events_params["from"] = request_from
        response = requests.post(
            f"{client.host}/v0/events",
            headers={"Authorization": f"Bearer {client.token}"},
            params=events_params,
            data=events,
        )

        try:
            res = response.json()
        except Exception:
            raise CLIDatasourceException(FeedbackManager.error(message=response.text))

        successful_rows = res["successful_rows"]
        quarantined_rows = res["quarantined_rows"]
        if successful_rows > 0:
            click.echo(
                FeedbackManager.success(
                    message=f"✓ {successful_rows} row{'' if successful_rows == 1 else 's'} appended!"
                )
            )
        if quarantined_rows > 0:
            click.echo(
                FeedbackManager.error(
                    message=f"✗ {quarantined_rows} row{'' if quarantined_rows == 1 else 's'} went to quarantine"
                )
            )
            analyze_quarantine(datasource_name, project, client)
            return
    else:
        click.echo(FeedbackManager.highlight(message=f"\n» Appending data to {datasource_name}"))
        try:
            job_ids = push_data(
                client,
                datasource_name,
                data,
                mode="append",
                concurrency=concurrency,
                silent=True,
                use_v1=use_v1,
            )
        except Exception as e:
            is_quarantined = "quarantine" in str(e)
            click.echo(FeedbackManager.error(message="✗ " + str(e)))
            if is_quarantined:
                analyze_quarantine(datasource_name, project, client)
                return
            else:
                raise e
        if use_v1:
            _echo_v1_import_jobs_queued(job_ids or [], "Append")
            if wait:
                _wait_for_v1_import_jobs(client, job_ids or [], "Append")
        else:
            click.echo(FeedbackManager.success(message="✓ Rows appended!"))


@datasource.command(name="replace")
@click.argument("datasource_name", required=True)
@click.argument("url", nargs=-1, required=True)
@click.option("--sql-condition", default=None, help="SQL WHERE condition to replace data", hidden=True)
@click.option("--skip-incompatible-partition-key", is_flag=True, default=False, hidden=True)
@click.option("--wait", is_flag=True, default=False, help="Wait for a v1 import job to finish.")
@click.option(
    "--experimental",
    type=click.Choice([EXPERIMENTAL_FEATURE_USE_V1]),
    multiple=True,
    help="Enable an experimental feature. May be specified multiple times.",
)
@click.pass_context
def datasource_replace(
    ctx: Context,
    datasource_name,
    url,
    sql_condition,
    skip_incompatible_partition_key,
    experimental: tuple[str, ...],
    wait: bool,
):
    """
    Replaces the data in a data source from a URL, local file or a connector

    - Replace from URL `tb datasource replace [datasource_name] https://url_to_csv --sql-condition "country='ES'"`

    - Replace from local file `tb datasource replace [datasource_name] /path/to/local/file --sql-condition "country='ES'"`
    """

    replace_options = set()
    if skip_incompatible_partition_key:
        replace_options.add("skip_incompatible_partition_key")
    client: TinyB = ctx.obj["client"]
    use_v1 = EXPERIMENTAL_FEATURE_USE_V1 in experimental
    if wait and not use_v1:
        raise CLIDatasourceException("--wait requires --experimental=use_v1.")
    job_ids = push_data(
        client,
        datasource_name,
        url,
        mode="replace",
        sql_condition=sql_condition,
        replace_options=replace_options,
        use_v1=use_v1,
    )
    if use_v1:
        _echo_v1_import_jobs_queued(job_ids or [], "Replace")
        if wait:
            _wait_for_v1_import_jobs(client, job_ids or [], "Replace")


@datasource.command(name="analyze")
@click.argument("url_or_file")
@click.pass_context
def datasource_analyze(ctx, url_or_file):
    """Analyze a URL or a file before creating a new data source"""
    client = ctx.obj["client"]

    def _table(title, columns, data):
        row_format = "{:<25}" * len(columns)
        click.echo(FeedbackManager.info_datasource_title(title=title))
        click.echo(FeedbackManager.info_datasource_row(row=row_format.format(*columns)))
        for t in data:
            click.echo(FeedbackManager.info_datasource_row(row=row_format.format(*[str(element) for element in t])))

    analysis, _ = _analyze(url_or_file, client, format=get_format_from_filename_or_url(url_or_file))

    columns = ("name", "type", "nullable")
    if "columns" in analysis["analysis"]:
        _table(
            "columns",
            columns,
            [
                (t["name"], t["recommended_type"], "false" if t["present_pct"] == 1 else "true")
                for t in analysis["analysis"]["columns"]
            ],
        )

    click.echo(FeedbackManager.info_datasource_title(title="SQL Schema"))
    click.echo(analysis["analysis"]["schema"])

    values = []

    if "dialect" in analysis:
        for x in analysis["dialect"].items():
            if x[1] == " ":
                values.append((x[0], '" "'))
            elif type(x[1]) == str and ("\n" in x[1] or "\r" in x[1]):  # noqa: E721
                values.append((x[0], x[1].replace("\n", "\\n").replace("\r", "\\r")))
            else:
                values.append(x)

        _table("dialect", ("name", "value"), values)


@datasource.command(name="truncate")
@click.argument("datasource_name", required=True)
@click.option("--yes", is_flag=True, default=False, help="Do not ask for confirmation")
@click.option(
    "--cascade", is_flag=True, default=False, help="Truncate dependent DS attached in cascade to the given DS"
)
@click.pass_context
def datasource_truncate(ctx, datasource_name, yes, cascade):
    """Truncate a data source"""

    client = ctx.obj["client"]
    if yes or click.confirm(FeedbackManager.warning_confirm_truncate_datasource(datasource=datasource_name)):
        try:
            client.datasource_truncate(datasource_name)
        except AuthNoTokenException:
            raise
        except DoesNotExistException:
            raise CLIDatasourceException(FeedbackManager.error_datasource_does_not_exist(datasource=datasource_name))
        except Exception as e:
            raise CLIDatasourceException(FeedbackManager.error_exception(error=e))

        click.echo(FeedbackManager.success_truncate_datasource(datasource=datasource_name))

        if cascade:
            try:
                ds_cascade_dependencies = client.datasource_dependencies(
                    no_deps=False,
                    match=None,
                    pipe=None,
                    datasource=datasource_name,
                    check_for_partial_replace=True,
                    recursive=False,
                )
            except Exception as e:
                raise CLIDatasourceException(FeedbackManager.error_exception(error=e))

            cascade_dependent_ds = list(ds_cascade_dependencies.get("dependencies", {}).keys()) + list(
                ds_cascade_dependencies.get("incompatible_datasources", {}).keys()
            )
            for cascade_ds in cascade_dependent_ds:
                if yes or click.confirm(FeedbackManager.warning_confirm_truncate_datasource(datasource=cascade_ds)):
                    try:
                        client.datasource_truncate(cascade_ds)
                    except DoesNotExistException:
                        raise CLIDatasourceException(
                            FeedbackManager.error_datasource_does_not_exist(datasource=datasource_name)
                        )
                    except Exception as e:
                        raise CLIDatasourceException(FeedbackManager.error_exception(error=e))
                    click.echo(FeedbackManager.success_truncate_datasource(datasource=cascade_ds))
    else:
        click.echo(FeedbackManager.info(message="Operation cancelled by user"))


@datasource.command(name="stop")
@click.argument("datasource_name", required=True)
@click.pass_context
def datasource_stop(ctx: Context, datasource_name: str) -> None:
    """Stop Kafka ingestion for a datasource.

    This command is only available for Kafka-connected datasources in forward branches
    or tinybird local environments. Once stopped, no new data will be ingested from
    the Kafka topic until the datasource is started again.

    Example: tb datasource stop my_kafka_datasource
    """
    client: TinyB = ctx.obj["client"]
    try:
        client.datasource_stop(datasource_name)
    except AuthNoTokenException:
        raise
    except DoesNotExistException:
        raise CLIDatasourceException(FeedbackManager.error_datasource_does_not_exist(datasource=datasource_name))
    except AuthException as e:
        raise CLIDatasourceException(FeedbackManager.error_exception(error=e))
    except OperationCanNotBePerformed as e:
        raise CLIDatasourceException(FeedbackManager.error_exception(error=e))
    except Exception as e:
        raise CLIDatasourceException(FeedbackManager.error_exception(error=e))

    click.echo(FeedbackManager.success_stop_datasource(datasource=datasource_name))


@datasource.command(name="start")
@click.argument("datasource_name", required=True)
@click.pass_context
def datasource_start(ctx: Context, datasource_name: str) -> None:
    """Start Kafka ingestion for a datasource.

    This command is only available for Kafka-connected datasources in forward branches
    or tinybird local environments. Once started, data will be ingested from the Kafka
    topic, resuming from the last committed offset.

    Example: tb datasource start my_kafka_datasource
    """
    client: TinyB = ctx.obj["client"]
    try:
        client.datasource_start(datasource_name)
    except AuthNoTokenException:
        raise
    except DoesNotExistException:
        raise CLIDatasourceException(FeedbackManager.error_datasource_does_not_exist(datasource=datasource_name))
    except AuthException as e:
        raise CLIDatasourceException(FeedbackManager.error_exception(error=e))
    except OperationCanNotBePerformed as e:
        raise CLIDatasourceException(FeedbackManager.error_exception(error=e))
    except Exception as e:
        raise CLIDatasourceException(FeedbackManager.error_exception(error=e))

    click.echo(FeedbackManager.success_start_datasource(datasource=datasource_name))


@datasource.command(name="delete")
@click.argument("datasource_name")
@click.option("--sql-condition", default=None, help="SQL WHERE condition to remove rows", hidden=True, required=True)
@click.option("--yes", is_flag=True, default=False, help="Do not ask for confirmation")
@click.option(
    "--wait/--no-wait",
    default=None,
    help="Wait for the delete to finish. Defaults to true with --lightweight-delete (sync request), "
    "false otherwise (returns a job id).",
)
@click.option("--dry-run", is_flag=True, default=False, help="Run the command without deleting anything")
@click.option(
    "--lightweight-delete",
    "lightweight",
    is_flag=True,
    default=False,
    help="Use ClickHouse lightweight DELETE. Defaults to waiting inline and returning rows_affected; "
    "pass --no-wait to enqueue a job instead. Not compatible with --dry-run.",
)
@click.option(
    "--partition",
    default=None,
    help="Restrict the lightweight delete to a single partition expression. Only valid with --lightweight-delete.",
)
@click.option(
    "--projection-mode",
    type=click.Choice(["throw", "drop", "rebuild"]),
    default=None,
    help="How ClickHouse should handle table projections when running the lightweight DELETE. "
    "throw: fail the DELETE if the table has any projection defined (ClickHouse default). "
    "drop: drop the affected projections so the DELETE can proceed; they will need to be recreated. "
    "rebuild: rebuild the affected projections after the DELETE finishes. "
    "Only valid with --lightweight-delete.",
)
@click.pass_context
def datasource_delete_rows(
    ctx, datasource_name, sql_condition, yes, wait, dry_run, lightweight, partition, projection_mode
):
    """
    Delete rows from a datasource

    - Delete rows with SQL condition: `tb datasource delete [datasource_name] --sql-condition "country='ES'"`

    - Delete rows with SQL condition and wait for the job to finish: `tb datasource delete [datasource_name] --sql-condition "country='ES'" --wait`

    - Use ClickHouse lightweight DELETE (synchronous, no job): `tb datasource delete [datasource_name] --sql-condition "country='ES'" --lightweight-delete`

    - Use ClickHouse lightweight DELETE and return immediately with a job id: `tb datasource delete [datasource_name] --sql-condition "country='ES'" --lightweight-delete --no-wait`
    """

    client: TinyB = ctx.ensure_object(dict)["client"]
    if lightweight and dry_run:
        raise CLIDatasourceException(
            FeedbackManager.error_exception(error="--lightweight-delete is not compatible with --dry-run")
        )
    if (partition or projection_mode) and not lightweight:
        raise CLIDatasourceException(
            FeedbackManager.error_exception(error="--partition and --projection-mode require --lightweight-delete")
        )
    # Lightweight delete is sync by default (the endpoint blocks and returns
    # rows_affected); the classic /v0/ delete is async by default (returns a
    # job id). The tri-state --wait/--no-wait lets users override either.
    if wait is None:
        wait = lightweight
    if (
        dry_run
        or yes
        or click.confirm(
            FeedbackManager.warning_confirm_delete_rows_datasource(
                datasource=datasource_name, delete_condition=sql_condition
            )
        )
    ):
        try:
            res = client.datasource_delete_rows(
                datasource_name,
                sql_condition,
                dry_run,
                lightweight=lightweight,
                wait=wait,
                partition=partition,
                projection_mode=projection_mode,
            )
            if dry_run:
                click.echo(
                    FeedbackManager.success_dry_run_delete_rows_datasource(
                        rows=res["rows_to_be_deleted"], datasource=datasource_name, delete_condition=sql_condition
                    )
                )
                return
            # Lightweight sync path returns rows_affected directly, no job involved.
            if lightweight and wait:
                mutation = res.get("mutation") or {}
                click.echo(
                    FeedbackManager.success_lightweight_delete_rows_datasource(
                        datasource=datasource_name,
                        delete_condition=sql_condition,
                        rows_affected=res.get("rows_affected", 0),
                        partitions_scanned=mutation.get("partitions_scanned", 0),
                        partitions_done=mutation.get("partitions_done", 0),
                        partitions_in_progress=mutation.get("partitions_in_progress", 0),
                    )
                )
                return
            job_id = res["job_id"]
            job_url = res["job_url"]
            click.echo(FeedbackManager.info_datasource_delete_rows_job_url(url=job_url))
            if wait and not lightweight:
                progress_symbols = ["-", "\\", "|", "/"]
                progress_str = "Waiting for the job to finish"
                # TODO: Use click.echo instead of print and see if the behavior is the same
                print(f"\n{progress_str}", end="")  # noqa: T201

                def progress_line(n):
                    print(f"\r{progress_str} {progress_symbols[n % len(progress_symbols)]}", end="")  # noqa: T201

                i = 0
                while True:
                    try:
                        res = client._req(f"v0/jobs/{job_id}")
                    except Exception:
                        raise CLIDatasourceException(FeedbackManager.error_job_status(url=job_url))
                    if res["status"] == "done":
                        print("\n")  # noqa: T201
                        click.echo(
                            FeedbackManager.success_delete_rows_datasource(
                                datasource=datasource_name, delete_condition=sql_condition
                            )
                        )
                        break
                    elif res["status"] == "error":
                        print("\n")  # noqa: T201
                        raise CLIDatasourceException(FeedbackManager.error_exception(error=res["error"]))
                    time.sleep(1)
                    i += 1
                    progress_line(i)

        except AuthNoTokenException:
            raise
        except DoesNotExistException:
            raise CLIDatasourceException(FeedbackManager.error_datasource_does_not_exist(datasource=datasource_name))
        except Exception as e:
            raise CLIDatasourceException(FeedbackManager.error_exception(error=e))


@datasource.command(
    name="data",
    context_settings=dict(
        allow_extra_args=True,
        ignore_unknown_options=True,
    ),
)
@click.argument("datasource")
@click.option("--limit", type=int, default=5, help="Limit the number of rows to return")
@click.pass_context
def datasource_data(ctx: Context, datasource: str, limit: int):
    """Print data returned by an endpoint

    Syntax: tb datasource data <datasource_name>
    """

    client: TinyB = ctx.ensure_object(dict)["client"]
    try:
        res = client.query(f"SELECT * FROM {datasource} LIMIT {limit} FORMAT JSON")
    except AuthNoTokenException:
        raise
    except Exception as e:
        raise CLIDatasourceException(FeedbackManager.error_exception(error=str(e)))

    if not res["data"]:
        click.echo(FeedbackManager.info_no_rows())
    else:
        echo_safe_humanfriendly_tables_format_smart_table(
            data=[d.values() for d in res["data"]], column_names=res["data"][0].keys()
        )


@datasource.command(name="export")
@click.argument("datasource")
@click.option(
    "--format",
    "format_",
    type=click.Choice(["csv", "ndjson"], case_sensitive=False),
    default="ndjson",
    help="Output format (csv or ndjson)",
)
@click.option("--rows", type=int, default=100, help="Number of rows to export (default: 100)")
@click.option("--where", type=str, default=None, help="Condition to filter data")
@click.option("--target", type=str, help="Target file path (default: datasource_name.{format})")
@click.pass_context
def datasource_export(
    ctx: Context,
    datasource: str,
    format_: str,
    rows: int,
    where: Optional[str],
    target: Optional[str],
):
    """Export data from a datasource to a file in CSV or NDJSON format

    Example usage:
    - Export all rows as CSV: tb datasource export my_datasource
    - Export 1000 rows as NDJSON: tb datasource export my_datasource --format ndjson --rows 1000
    - Export to specific file: tb datasource export my_datasource --target ./data/export.csv
    """
    client: TinyB = ctx.ensure_object(dict)["client"]
    project: Project = ctx.ensure_object(dict)["project"]

    # Build query with optional row limit
    query = f"SELECT * FROM {datasource} WHERE {where or 1} LIMIT {rows}"

    click.echo(FeedbackManager.highlight(message=f"\n» Exporting {datasource}"))

    try:
        if format_ == "csv":
            query += " FORMAT CSVWithNames"
        else:
            query += " FORMAT JSONEachRow"

        res = client.query(query)

        target_path = persist_fixture(datasource, res, project.folder, format=format_, target=target)
        file_size = os.path.getsize(target_path)

        click.echo(
            FeedbackManager.success(
                message=f"✓ Exported data to {str(target_path).replace(project.folder, '')} ({humanfriendly.format_size(file_size)})"
            )
        )

    except Exception as e:
        raise CLIDatasourceException(FeedbackManager.error(message=str(e)))


@datasource.command(name="sync")
@click.argument("datasource_name")
@click.option("--yes", is_flag=True, default=False, help="Do not ask for confirmation")
@click.pass_context
def datasource_sync(ctx: Context, datasource_name: str, yes: bool):
    """Sync from a GCS or S3 connection defined in .datasource file"""

    try:
        client: TinyB = ctx.obj["client"]
        ds = client.get_datasource(datasource_name)

        warning_message = FeedbackManager.warning_datasource_sync_bucket(datasource=datasource_name)

        if yes or click.confirm(warning_message):
            client.datasource_sync(ds["id"])
            click.echo(FeedbackManager.success_sync_datasource(datasource=datasource_name))
    except AuthNoTokenException:
        raise
    except Exception as e:
        raise CLIDatasourceException(FeedbackManager.error_syncing_datasource(datasource=datasource_name, error=str(e)))


@datasource.command(name="sample")
@click.argument("datasource_name")
@click.option(
    "--max-files",
    default=1,
    type=int,
    help="Maximum number of files to import (default 1, max 10)",
)
@click.option(
    "--wait",
    is_flag=True,
    default=False,
    help="Wait for the import job to finish",
)
@click.option(
    "--rows",
    default=None,
    type=int,
    help="For DynamoDB, the maximum number of rows to scan and import (default 1500; mutually exclusive with --max-bytes)",
)
@click.option(
    "--max-bytes",
    default=None,
    type=str,
    help="For DynamoDB, the maximum approximate JSONEachRow bytes to import, e.g. 500MB (capped at 10GB by default; mutually exclusive with --rows)",
)
@click.option(
    "--full-export",
    is_flag=True,
    default=False,
    help="For DynamoDB, trigger a full PITR export instead of a bounded sample (mutually exclusive with --rows and --max-bytes)",
)
@click.pass_context
def datasource_sample(
    ctx: Context,
    datasource_name: str,
    max_files: int,
    wait: bool,
    rows: Optional[int],
    max_bytes: Optional[str],
    full_export: bool,
) -> None:
    """Import sample data from a datasource connected to S3, GCS, or DynamoDB.

    For S3 and GCS, this imports a limited number of files from the bucket URI
    pattern. For DynamoDB, this scans and imports a bounded sample limited by
    either --rows or --max-bytes (defaulting to 1500 rows), or --full-export to
    trigger a PITR export of the whole table.

    By default, returns immediately with job info. Use --wait to block until complete.

    Examples:
        tb --branch=my_branch datasource sample my_s3_ds
        tb --branch=my_branch datasource sample my_s3_ds --max-files 3 --wait
        tb --branch=my_branch datasource sample my_dynamodb_ds --wait
        tb --branch=my_branch datasource sample my_dynamodb_ds --rows 100000 --wait
        tb --branch=my_branch datasource sample my_dynamodb_ds --max-bytes 1GB --wait
        tb --branch=my_branch datasource sample my_dynamodb_ds --full-export --wait
    """
    from tinybird.tb.modules.common import wait_job
    from tinybird.tb.modules.job_common import echo_job_url

    try:
        client: TinyB = ctx.obj["client"]
        config = ctx.obj.get("config", {})

        if rows is not None and max_bytes is not None:
            raise CLIDatasourceException(
                FeedbackManager.error(message="--rows and --max-bytes are mutually exclusive; pass only one.")
            )

        if full_export and (rows is not None or max_bytes is not None):
            raise CLIDatasourceException(
                FeedbackManager.error(message="--full-export cannot be combined with --rows or --max-bytes.")
            )

        if full_export:
            click.echo(
                FeedbackManager.warning(
                    message=(
                        "DynamoDB full export samples will import the whole table. "
                        "Use --rows or --max-bytes without --full-export for a bounded sample."
                    )
                )
            )

        click.echo(FeedbackManager.info(message=f"Starting sample import for {datasource_name}..."))

        # Start the job
        result = client.datasource_sample(
            datasource_name, max_files=max_files, rows=rows, max_bytes=max_bytes, full_export=full_export
        )

        job_id = result.get("job_id") or result.get("id")
        if not job_id:
            raise CLIDatasourceException(
                FeedbackManager.error_sample_import_datasource(
                    datasource=datasource_name, error="No job ID returned from server"
                )
            )
        job_url = result.get("job_url", f"/v0/jobs/{job_id}")

        # Show job URL
        echo_job_url(client.token, client.host, config.get("name", ""), job_url)

        if not wait:
            # Return immediately with job info
            click.echo(FeedbackManager.success(message=f"Job started: {job_id}"))
            click.echo(FeedbackManager.gray(message=f"Check status: tb job get {job_id}"))
            return

        # Wait for job completion using existing wait_job utility
        # wait_job raises CLIException on failure, so we only reach here on success
        job_result = wait_job(client, job_id, job_url, "Importing sample")

        stats = job_result.get("stats", {})
        found_files = stats.get("found_files", max_files)
        click.echo(
            FeedbackManager.success_sample_import_datasource(
                datasource=datasource_name,
                file=f"{found_files} file(s)",
                rows="see job details",
                size="see job details",
            )
        )

    except AuthNoTokenException:
        raise
    except CLIDatasourceException:
        raise
    except Exception as e:
        raise CLIDatasourceException(
            FeedbackManager.error_sample_import_datasource(datasource=datasource_name, error=str(e))
        )


@datasource.command(name="create")
@click.option("--name", type=str, help="Name of the data source")
@click.option("--blank", is_flag=True, default=False, help="Create a blank data source")
@click.option("--file", type=str, help="Create a data source from a local file")
@click.option("--url", type=str, help="Create a data source from a remote URL")
@click.option("--connection-name", type=str, help="Create a data source from a connection")
@click.option("--s3", is_flag=True, default=False, help="Create a data source from a S3 connection")
@click.option("--gcs", is_flag=True, default=False, help="Create a data source from a GCS connection")
@click.option("--kafka", is_flag=True, default=False, help="Create a data source from a Kafka connection")
@click.option("--dynamodb", is_flag=True, default=False, help="Create a data source from a DynamoDB connection")
@click.option("--kafka-topic", "kafka_topic_param", type=str, help="Kafka topic")
@click.option("--kafka-group-id", "kafka_group_id_param", type=str, help="Kafka group ID")
@click.option(
    "--kafka-auto-offset-reset",
    "kafka_auto_offset_reset_param",
    type=click.Choice(["latest", "earliest"], case_sensitive=False),
    help="Kafka auto offset reset",
)
@click.option("--s3-bucket-uri", "s3_bucket_uri_param", type=str, help="S3 bucket URI (e.g., s3://my-bucket/*.csv)")
@click.option("--s3-sample-file", "s3_sample_file_param", type=str, help="S3 sample file for schema inference")
@click.option(
    "--s3-schedule",
    "s3_schedule_param",
    type=click.Choice(["@auto", "@once"], case_sensitive=False),
    help="S3 import schedule (@auto for automatic ingestion, @once for on-demand)",
)
@click.option(
    "--s3-format",
    "s3_format_param",
    type=click.Choice(["csv", "ndjson", "parquet"], case_sensitive=False),
    help="S3 import format (default: auto-detected from file extension)",
)
@click.option("--dynamodb-table-arn", "dynamodb_table_arn_param", type=str, help="DynamoDB table ARN")
@click.option("--dynamodb-export-bucket", "dynamodb_export_bucket_param", type=str, help="S3 export bucket")
@click.option("--yes", is_flag=True, default=False, help="Do not ask for confirmation")
@click.pass_context
def datasource_create(
    ctx: Context,
    name: str,
    blank: bool,
    file: str,
    url: str,
    connection_name: Optional[str],
    s3: bool,
    gcs: bool,
    kafka: bool,
    dynamodb: bool,
    kafka_topic_param: str,
    kafka_group_id_param: str,
    kafka_auto_offset_reset_param: str,
    s3_bucket_uri_param: Optional[str],
    s3_sample_file_param: Optional[str],
    s3_schedule_param: Optional[str],
    s3_format_param: Optional[str],
    dynamodb_table_arn_param: Optional[str],
    dynamodb_export_bucket_param: Optional[str],
    yes: bool,
):
    wizard_data: dict[str, str | bool | float] = {
        "wizard": "datasource_create",
        "current_step": "start",
    }
    start_time = time.time()

    if name:
        wizard_data["datasource_name"] = name

    try:
        project: Project = ctx.ensure_object(dict)["project"]
        client: TinyB = ctx.ensure_object(dict)["client"]
        config = ctx.ensure_object(dict)["config"]
        env: str = ctx.ensure_object(dict)["env"]

        datasource_types = {
            "blank": ("Blank", "A data source with an example schema"),
            "local_file": ("Local file", "Use a local file to define the schema"),
            "remote_url": ("Remote URL", "Use a remote file to define the schema"),
            "s3": ("S3", "Connect your data source to S3. A S3 connection file is required."),
            "gcs": ("GCS", "Connect your data source to GCS. A GCS connection file is required."),
            "kafka": ("Kafka", "Connect your data source to a Kafka topic. A Kafka connection file is required."),
            "dynamodb": (
                "DynamoDB",
                "Connect your data source to a DynamoDB table. A DynamoDB connection file is required.",
            ),
        }
        datasource_type: Optional[str] = None
        connection_file: Optional[str] = None
        ds_content = """SCHEMA >
    `data` String `json:$`

ENGINE "MergeTree"
# ENGINE_SORTING_KEY "user_id, timestamp"
# ENGINE_TTL "timestamp + toIntervalDay(60)"
# Learn more at https://www.tinybird.co/docs/forward/dev-reference/datafiles/datasource-files
"""
        valid_extensions = [
            "csv",
            "csv.gz",
            "ndjson",
            "ndjson.gz",
            "jsonl",
            "jsonl.gz",
            "json",
            "json.gz",
            "parquet",
            "parquet.gz",
        ]

        if file:
            datasource_type = "local_file"
        elif url:
            datasource_type = "remote_url"
        elif blank:
            datasource_type = "blank"
        elif s3:
            datasource_type = "s3"
        elif gcs:
            datasource_type = "gcs"
        elif kafka:
            datasource_type = "kafka"
        elif dynamodb:
            datasource_type = "dynamodb"
        elif connection_name:
            # Determine type from local connection file
            connection_files = project.get_connection_files()
            connection_file = next((f for f in connection_files if f.endswith(f"{connection_name}.connection")), None)
            if connection_file:
                connection_content = Path(connection_file).read_text()
                if project.is_kafka_connection(connection_content):
                    datasource_type = "kafka"
                elif project.is_s3_connection(connection_content):
                    datasource_type = "s3"
                elif project.is_gcs_connection(connection_content):
                    datasource_type = "gcs"
                elif project.is_dynamodb_connection(connection_content):
                    datasource_type = "dynamodb"

        datasource_type_index = -1

        if datasource_type is None:
            wizard_data["current_step"] = "select_datasource_origin"
            click.echo(
                FeedbackManager.highlight(
                    message="? This command will create the schema (.datasource) for your data. Choose where from:"
                )
            )

            dt_keys = list(datasource_types.keys())
            while datasource_type_index == -1:
                for index, key in enumerate(dt_keys):
                    click.echo(
                        f"  [{index + 1}] {FeedbackManager.bold(message=datasource_types[key][0])}: {datasource_types[key][1]}"
                    )
                click.echo(FeedbackManager.gray(message="\nFiles can be either NDJSON, CSV or Parquet."))
                click.echo(
                    FeedbackManager.gray(
                        message=(
                            f"Tip: Run `{get_cli_name()} datasource create --file | --url | --connection` to skip this step."
                        )
                    )
                )
                datasource_type_index = click.prompt("\nSelect option", default=1)

                if datasource_type_index == 0:
                    click.echo(FeedbackManager.warning(message="Datasource type selection cancelled by user"))

                    wizard_data["exit_reason"] = "user_cancelled_type_selection"
                    wizard_data["duration_seconds"] = round(time.time() - start_time, 2)
                    add_telemetry_event("system_info", **wizard_data)
                    return None

                try:
                    datasource_type = dt_keys[int(datasource_type_index) - 1]
                except Exception:
                    datasource_type_index = -1

        if datasource_type:
            wizard_data["datasource_type"] = datasource_type

        if not datasource_type:
            click.echo(
                FeedbackManager.error(
                    message=f"Invalid option: {datasource_type_index}. Please select a valid option from the list above."
                )
            )

            wizard_data["exit_reason"] = "invalid_type_selection"
            wizard_data["duration_seconds"] = round(time.time() - start_time, 2)
            add_telemetry_event("system_info", **wizard_data)
            return

        connection_required = datasource_type in ("kafka", "s3", "gcs", "dynamodb")

        if connection_required:
            if env == "local":
                click.echo(FeedbackManager.gray(message="» Building project before continue..."))
                build_project(project=project, tb_client=client, watch=False, config=config, silent=True)
                click.echo(FeedbackManager.success(message="✓ Build completed!\n"))

            wizard_data["current_step"] = "select_connection"

            # For S3, include both s3 and s3_iamrole connections
            if datasource_type == "s3":
                connections = client.connections("s3") + client.connections("s3_iamrole")
            else:
                connections = client.connections(datasource_type)
            connection_type = datasource_types[datasource_type][0]
            new_connection_created = False
            # Only prompt to create a connection if connection_name was not provided via CLI
            if len(connections) == 0 and not connection_name:
                click.echo(FeedbackManager.info(message=f"No {connection_type} connections found."))
                if click.confirm(
                    FeedbackManager.highlight(
                        message=f"\n? Do you want to create a {connection_type} connection? [Y/n]"
                    ),
                    show_default=False,
                    default=True,
                ):
                    wizard_data["created_new_connection"] = True
                    if datasource_type == "kafka":
                        result = connection_create_kafka(ctx)
                        connection_name = result["name"]
                    elif datasource_type == "s3":
                        click.echo(FeedbackManager.gray(message="\n» Creating S3 connection..."))
                        result = connection_create_s3(ctx, access_type="read")
                        connection_name = result["name"]
                    elif datasource_type == "gcs":
                        click.echo(FeedbackManager.gray(message="\n» Creating .connection file..."))
                        default_connection_name = f"{datasource_type}_{generate_short_id()}"
                        gcs_connection_name: str = click.prompt(
                            FeedbackManager.highlight(message=f"? Connection name [{default_connection_name}]"),
                            show_default=False,
                            default=default_connection_name,
                        )
                        connection_name = gcs_connection_name
                        wizard_data["connection_name"] = gcs_connection_name
                        generate_gcs_connection_file_with_secrets(
                            gcs_connection_name,
                            service="gcs",
                            svc_account_creds="GCS_SERVICE_ACCOUNT_CREDENTIALS_JSON",
                            folder=project.folder,
                        )
                    elif datasource_type == "dynamodb":
                        result = connection_create_dynamodb(ctx)
                        if result.get("error"):
                            raise CLIDatasourceException(
                                FeedbackManager.error(message=f"DynamoDB connection creation failed: {result['error']}")
                            )
                        connection_name = result["name"]
                    new_connection_created = True
                    if env == "local" and new_connection_created:
                        click.echo(FeedbackManager.gray(message="\n» Building project to access the new connection..."))
                        build_project(project=project, tb_client=client, watch=False, config=config, silent=True)
                        click.echo(FeedbackManager.success(message="✓ Build completed!"))
                else:
                    click.echo(
                        FeedbackManager.info(
                            message=f"→ To continue, you need a connection. Run `{get_cli_name()} connection create {datasource_type}` to create one."
                        )
                    )
                    wizard_data["exit_reason"] = "user_declined_connection_creation"
                    wizard_data["duration_seconds"] = round(time.time() - start_time, 2)
                    add_telemetry_event("system_info", **wizard_data)
                    return

            # Only prompt for connection selection if connection_name wasn't provided via CLI
            if not connection_name:
                wizard_data["selected_connection_from_multiple"] = True
                connection = select_connection(None, datasource_type, connections, client)
                connection_id = connection["id"]
                connection_name = connection["name"]

        if datasource_type == "local_file":
            wizard_data["current_step"] = "file_input"
            if not file:
                click.echo(
                    FeedbackManager.gray(
                        message=f"\nPlease, enter a valid path to your file.\nThe schema of the new data source will be automatically detected based on the data of the file.\nValid extensions: {', '.join(valid_extensions)}"
                    )
                )
                file = click.prompt(FeedbackManager.highlight(message="? Path"))
                if file.startswith("~"):
                    file = os.path.expanduser(file)

            folder_path = project.path
            path = folder_path / file
            if not path.exists():
                path = Path(file)

            data_format = path.suffix.lstrip(".")
            ds_content = analyze_file(str(path), client, format=data_format)
            default_name = normalize_datasource_name(path.stem)
            wizard_data["current_step"] = "enter_name"
            click.echo(FeedbackManager.gray(message="\n» Creating .datasource file..."))
            name = name or click.prompt(
                FeedbackManager.highlight(message=f"? Data source name [{default_name}]"),
                default=default_name,
                show_default=False,
            )
            wizard_data["datasource_name"] = name

            if name == default_name:
                wizard_data["used_default_name"] = True

        if datasource_type == "remote_url":
            wizard_data["current_step"] = "file_input"
            if not url:
                click.echo(
                    FeedbackManager.gray(
                        message=f"\nPlease, enter a valid url to your file.\nThe schema of the new data source will be automatically detected based on the data of the file.\nValid extensions: {', '.join(valid_extensions)}"
                    )
                )
                url = click.prompt(FeedbackManager.highlight(message="? URL"))
            format = url.split(".")[-1]
            ds_content = analyze_file(url, client, format)
            default_name = normalize_datasource_name(Path(url).stem)
            wizard_data["current_step"] = "enter_name"
            click.echo(FeedbackManager.gray(message="\n» Creating .datasource file..."))
            name = name or click.prompt(
                FeedbackManager.highlight(message=f"? Data source name [{default_name}]"),
                default=default_name,
                show_default=False,
            )
            wizard_data["datasource_name"] = name

            if name == default_name:
                wizard_data["used_default_name"] = True

        if datasource_type not in ("remote_url", "local_file"):
            wizard_data["current_step"] = "enter_name"
            click.echo(FeedbackManager.gray(message="\n» Creating .datasource file..."))
            default_name = f"ds_{generate_short_id()}"
            name = name or click.prompt(
                FeedbackManager.highlight(message=f"? Data source name [{default_name}]"),
                default=default_name,
                show_default=False,
            )
            wizard_data["datasource_name"] = name

            if name == default_name:
                wizard_data["used_default_name"] = True

        if datasource_type == "kafka":
            assert connection_name is not None
            wizard_data["current_step"] = "kafka_configuration"
            connections = client.connections("kafka")
            kafka_connection_id: Optional[str] = next(
                (c["id"] for c in connections if c["name"] == connection_name), None
            )
            if not kafka_connection_id:
                raise CLIDatasourceException(
                    FeedbackManager.error(message=f"No Kafka connection found with name '{connection_name}'.")
                )

            # Kafka configuration values - preserve param values if provided
            kafka_topic: Optional[str] = None
            if kafka_topic_param:
                kafka_topic = kafka_topic_param
            else:
                kafka_topic = select_topic(None, kafka_connection_id, client)

            kafka_group_id = select_group_id(kafka_group_id_param, kafka_topic, kafka_connection_id, client)
            kafka_group_id_secret_name = f"KAFKA_GROUP_ID_LOCAL_{name}"
            kafka_group_id_secret_value = f"{kafka_group_id}_{generate_short_id()}"
            try:
                save_secret_to_env_file(
                    project=project,
                    name=kafka_group_id_secret_name,
                    value=kafka_group_id_secret_value,
                )
                client.create_secret(name=kafka_group_id_secret_name, value=kafka_group_id_secret_value)
            except Exception as e:
                raise CLIDatasourceException(FeedbackManager.error(message=str(e)))
            kafka_auto_offset_reset: Optional[str] = None
            if kafka_auto_offset_reset_param:
                kafka_auto_offset_reset = kafka_auto_offset_reset_param
            else:
                kafka_auto_offset_reset = select_auto_offset_reset()

            if connection_name and kafka_connection_id is None:
                raise CLIDatasourceException(
                    FeedbackManager.error(message=f"No Kafka connection found with name '{connection_name}'.")
                )

            confirmed = yes
            change_topic = False
            change_group_id = False
            change_connection = False
            change_auto_offset_reset = False

            # When --yes is passed, generate ds_content directly without the confirmation loop
            if confirmed:
                assert kafka_connection_id is not None
                assert connection_name is not None
                assert kafka_topic is not None
                assert kafka_group_id is not None
                assert kafka_auto_offset_reset is not None
                click.echo(FeedbackManager.gray(message="\n» Generating schema..."))
                response = client.kafka_preview_topic(kafka_connection_id, kafka_topic, kafka_group_id)
                meta = response.get("preview", {}).get("meta", [])
                ds_content = meta_to_datasource_datafile(
                    name,
                    meta,
                    connection_name,
                    kafka_topic,
                    kafka_group_id,
                    kafka_auto_offset_reset,
                )

            while not confirmed:
                # Select connection if not set or if user wants to change it
                if change_connection:
                    selected_connection = select_connection(kafka_connection_id, datasource_type, connections, client)
                    kafka_connection_id = selected_connection["id"]
                    connection_name = selected_connection["name"]
                    change_connection = False
                    change_topic = True

                assert kafka_connection_id is not None

                # Select topic if not set
                if change_topic:
                    kafka_topic = select_topic(None, kafka_connection_id, client)
                    change_topic = False
                    change_group_id = True

                # Select group ID if not set or if user wants to change it
                if change_group_id and kafka_connection_id is not None:
                    kafka_group_id = select_group_id(kafka_group_id, kafka_topic, kafka_connection_id, client)
                    kafka_group_id_secret_value = f"{kafka_group_id}_{generate_short_id()}"
                    try:
                        save_secret_to_env_file(
                            project=project,
                            name=kafka_group_id_secret_name,
                            value=kafka_group_id_secret_value,
                        )
                        client.create_secret(name=kafka_group_id_secret_name, value=kafka_group_id_secret_value)
                    except Exception as e:
                        raise CLIDatasourceException(FeedbackManager.error(message=str(e)))
                    change_group_id = False  # Reset flag

                # Select auto offset reset if not set or if user wants to change it
                if change_auto_offset_reset:
                    kafka_auto_offset_reset = select_auto_offset_reset(kafka_auto_offset_reset)
                    change_auto_offset_reset = False  # Reset flag

                # Show preview - at this point kafka_connection_id is guaranteed to be set
                assert kafka_connection_id is not None
                assert connection_name is not None
                assert kafka_topic is not None
                assert kafka_group_id is not None
                preview_result = echo_kafka_data(
                    kafka_connection_id, connection_name, kafka_topic, kafka_group_id, client
                )
                click.echo(FeedbackManager.highlight(message=f"\n» Previewing {name}.datasource"))
                meta = preview_result["meta"]
                ds_content = meta_to_datasource_datafile(
                    name,
                    meta,
                    connection_name,
                    kafka_topic,
                    kafka_group_id,
                    kafka_auto_offset_reset,
                )
                click.echo(create_terminal_box(ds_content, title=f"{name}.datasource"))

                # Confirmation step
                wizard_data["current_step"] = "kafka_confirmation"
                click.echo(FeedbackManager.highlight(message="\n? What would you like to do?"))
                click.echo("  [1] Create .datasource file with this configuration")
                click.echo("  [2] Edit connection")
                click.echo("  [3] Edit topic")
                click.echo("  [4] Edit group ID")
                click.echo("  [5] Edit auto offset reset")
                click.echo("  [6] Cancel")

                choice = click.prompt("\nSelect option", default=1, type=int)

                if choice == 1:
                    confirmed = True
                elif choice == 2:
                    change_connection = True
                elif choice == 3:
                    change_topic = True
                elif choice == 4:
                    change_group_id = True  # Set flag to re-prompt with current value as default
                elif choice == 5:
                    change_auto_offset_reset = True  # Set flag to re-prompt with current value as default
                elif choice == 6:
                    wizard_data["exit_reason"] = "user_cancelled_kafka_configuration"
                    wizard_data["duration_seconds"] = round(time.time() - start_time, 2)
                    add_telemetry_event("system_info", **wizard_data)
                    return None
                else:
                    click.echo(FeedbackManager.error(message="Invalid option. Please select 1-6."))

        if datasource_type == "s3":
            assert connection_name is not None
            wizard_data["current_step"] = "s3_configuration"
            s3_connections = client.connections("s3") + client.connections("s3_iamrole")
            s3_connection_id: Optional[str] = next(
                (c["id"] for c in s3_connections if c["name"] == connection_name), None
            )
            if not s3_connection_id:
                raise CLIDatasourceException(
                    FeedbackManager.error(message=f"No S3 connection found with name '{connection_name}'.")
                )

            # S3 configuration values - preserve param values if provided
            s3_bucket_uri: Optional[str] = None
            if s3_bucket_uri_param:
                s3_bucket_uri = s3_bucket_uri_param
            else:
                s3_bucket_uri = select_bucket_uri(None)

            s3_sample_file = select_sample_file_uri(s3_sample_file_param, s3_bucket_uri, s3_connection_id, client)
            s3_format: str = s3_format_param.lower() if s3_format_param else select_format_file(None)

            s3_schedule: Optional[str] = None
            if s3_schedule_param:
                s3_schedule = s3_schedule_param
            else:
                s3_schedule = select_schedule(None)

            confirmed = yes
            change_bucket = False
            change_sample_file = False
            change_connection = False
            change_schedule = False

            # When --yes is passed, generate ds_content directly without the confirmation loop
            if confirmed:
                assert s3_connection_id is not None
                assert connection_name is not None
                assert s3_bucket_uri is not None
                assert s3_sample_file is not None
                assert s3_schedule is not None
                assert s3_format is not None
                click.echo(FeedbackManager.gray(message="\n» Generating schema..."))
                response = client.preview_s3(s3_connection_id, s3_bucket_uri, s3_sample_file, None)
                meta = response.get("preview", {}).get("meta", [])
                ds_content = meta_to_s3_datasource_datafile(
                    meta, connection_name, s3_bucket_uri, s3_schedule, s3_format
                )

            while not confirmed:
                # Select connection if not set or if user wants to change it
                if change_connection:
                    selected_connection = select_connection(s3_connection_id, datasource_type, s3_connections, client)
                    s3_connection_id = selected_connection["id"]
                    connection_name = selected_connection["name"]
                    change_connection = False
                    change_bucket = True

                assert s3_connection_id is not None

                # Select bucket URI if not set or if user wants to change it
                if change_bucket:
                    s3_bucket_uri = select_bucket_uri(None)
                    change_bucket = False
                    change_sample_file = True

                # Select sample file if not set or if user wants to change it
                if change_sample_file and s3_connection_id is not None and s3_bucket_uri is not None:
                    s3_sample_file = select_sample_file_uri(None, s3_bucket_uri, s3_connection_id, client)
                    change_sample_file = False

                # Select schedule if user wants to change it
                if change_schedule:
                    s3_schedule = select_schedule(None)
                    change_schedule = False

                # Show preview - at this point s3_connection_id is guaranteed to be set
                assert s3_connection_id is not None
                assert connection_name is not None
                assert s3_bucket_uri is not None
                assert s3_sample_file is not None
                assert s3_schedule is not None
                preview_result = echo_s3_data(s3_connection_id, connection_name, s3_bucket_uri, s3_sample_file, client)
                click.echo(FeedbackManager.highlight(message=f"\n» Previewing {name}.datasource"))
                meta = preview_result["meta"]
                ds_content = meta_to_s3_datasource_datafile(
                    meta, connection_name, s3_bucket_uri, s3_schedule, s3_format
                )
                click.echo(create_terminal_box(ds_content, title=f"{name}.datasource"))

                # Confirmation step
                wizard_data["current_step"] = "s3_confirmation"
                click.echo(FeedbackManager.highlight(message="\n? What would you like to do?"))
                click.echo("  [1] Create .datasource file with this configuration")
                click.echo("  [2] Edit connection")
                click.echo("  [3] Edit bucket URI")
                click.echo("  [4] Edit sample file")
                click.echo("  [5] Edit schedule")
                click.echo("  [6] Cancel")

                choice = click.prompt("\nSelect option", default=1, type=int)

                if choice == 1:
                    confirmed = True
                elif choice == 2:
                    change_connection = True
                elif choice == 3:
                    change_bucket = True
                elif choice == 4:
                    change_sample_file = True
                elif choice == 5:
                    change_schedule = True
                elif choice == 6:
                    wizard_data["exit_reason"] = "user_cancelled_s3_configuration"
                    wizard_data["duration_seconds"] = round(time.time() - start_time, 2)
                    add_telemetry_event("system_info", **wizard_data)
                    return None
                else:
                    click.echo(FeedbackManager.error(message="Invalid option. Please select 1-6."))

        if datasource_type == "gcs":
            # Use connection_name from CLI if provided, otherwise look it up from selected connection_id
            gcs_conn_name: Optional[str] = connection_name
            if not gcs_conn_name:
                gcs_connections = client.connections("gcs")
                gcs_conn_name = next((c["name"] for c in gcs_connections if c["id"] == connection_id), None)
            ds_content += f"""
IMPORT_CONNECTION_NAME "{gcs_conn_name}"
IMPORT_BUCKET_URI "gs://my-bucket/*.csv"
IMPORT_SCHEDULE "@auto"
"""

        if datasource_type == "dynamodb":
            assert connection_name is not None
            wizard_data["current_step"] = "dynamodb_configuration"

            connection_files = project.get_dynamodb_connection_files()
            connection_file = next((f for f in connection_files if Path(f).stem == connection_name), None)
            if not connection_file:
                raise CLIDatasourceException(
                    FeedbackManager.error(message=f"No DynamoDB connection found with name '{connection_name}'.")
                )

            connection_content = Path(connection_file).read_text()
            connection_region = _extract_connection_setting(connection_content, "DYNAMODB_REGION")
            if not connection_region:
                raise CLIDatasourceException(
                    FeedbackManager.error(
                        message=f"Could not determine DYNAMODB_REGION from connection '{connection_name}'."
                    )
                )

            dynamodb_table_arn = dynamodb_table_arn_param
            if not dynamodb_table_arn:
                dynamodb_table_arn = click.prompt(
                    FeedbackManager.highlight(
                        message="? DynamoDB table ARN (e.g. arn:aws:dynamodb:us-east-1:123456789012:table/my-table)"
                    )
                )
            if not dynamodb_table_arn.startswith("arn:aws:dynamodb:"):
                raise CLIDatasourceException(
                    FeedbackManager.error(
                        message=f"Invalid table ARN: '{dynamodb_table_arn}'. Must start with 'arn:aws:dynamodb:'."
                    )
                )

            dynamodb_export_bucket = dynamodb_export_bucket_param
            if not dynamodb_export_bucket:
                dynamodb_export_bucket = click.prompt(
                    FeedbackManager.highlight(message="? S3 export bucket (e.g. my-exports-bucket)")
                )
            if dynamodb_export_bucket.startswith("s3://"):
                raise CLIDatasourceException(
                    FeedbackManager.error(
                        message=(
                            f"Invalid export bucket: '{dynamodb_export_bucket}'. Use the bucket name only, "
                            "without the 's3://' prefix."
                        )
                    )
                )

            connection_role_arn = _resolve_dynamodb_role_arn(connection_content, project)
            if not connection_role_arn:
                raise CLIDatasourceException(
                    FeedbackManager.error(
                        message=f"Could not determine the role ARN from connection '{connection_name}'."
                    )
                )

            click.echo(FeedbackManager.gray(message="\n» Validating DynamoDB table..."))
            validation_result = validate_dynamodb_table(
                client,
                dynamodb_table_arn,
                connection_region,
                connection_role_arn,
                fail_on_error=True,
                external_id_seed=connection_name,
            )
            assert validation_result is not None

            key_columns = _dynamodb_key_columns(validation_result)
            key_schema = "".join(
                f"    `{key_column}` {_dynamodb_attribute_type(key_column, validation_result)} `json:$.Item.{key_column}`,\n"
                for key_column in key_columns
            )
            sorting_key = ", ".join(key_columns)
            old_record_column = ""
            if validation_result.get("stream_view_type") == "NEW_AND_OLD_IMAGES":
                old_record_column = "    `_old_record` Nullable(String) `json:$.OldImage`,\n"

            ds_content = f"""DESCRIPTION >
    {name} - DynamoDB data source

SCHEMA >
{key_schema}    `_record` String `json:$.NewImage`,
{old_record_column}    `_timestamp` DateTime64(3) `json:$.ApproximateCreationDateTime`,
    `_event_name` LowCardinality(String) `json:$.eventName`,
    `_is_deleted` UInt8 `json:$._is_deleted`

ENGINE "ReplacingMergeTree"
ENGINE_SORTING_KEY {sorting_key}
ENGINE_VER _timestamp
ENGINE_IS_DELETED _is_deleted

IMPORT_CONNECTION_NAME '{connection_name}'
IMPORT_TABLE_ARN '{dynamodb_table_arn}'
IMPORT_EXPORT_BUCKET '{dynamodb_export_bucket}'
"""

        wizard_data["current_step"] = "create_datasource_file"

        datasources_path = project.path / "datasources"
        if not datasources_path.exists():
            datasources_path.mkdir()
        ds_file = datasources_path / f"{name}.datasource"
        if not ds_file.exists():
            ds_file.touch()
        ds_file.write_text(ds_content)
        click.echo("")
        click.echo(FeedbackManager.success(message=f"✓ /datasources/{name}.datasource created"))

        if datasource_type == "kafka":
            tip_message = f"""Next steps:
    - Run `{get_cli_name()} deploy` to consume from the topic in Tinybird Local.
    - Run `{get_cli_name()} --cloud deploy` to deploy the new resource to Tinybird Cloud."""
        else:
            tip_message = f"""Next steps:
    - Run `{get_cli_name()} --cloud deploy` to deploy the new resource to Tinybird Cloud."""

        click.echo(FeedbackManager.gray(message=tip_message))

        wizard_data["current_step"] = "completed"
        wizard_data["duration_seconds"] = round(time.time() - start_time, 2)
        add_telemetry_event("system_info", **wizard_data)
    except Exception as e:
        wizard_data["duration_seconds"] = round(time.time() - start_time, 2)

        current_exception: Optional[BaseException] = e
        while current_exception:
            if isinstance(current_exception, KeyboardInterrupt):
                wizard_data["exit_reason"] = "user_interrupted"
                add_telemetry_event("system_info", **wizard_data)
                raise
            current_exception = current_exception.__cause__ or current_exception.__context__

        wizard_data["error_message"] = str(e)
        add_telemetry_event("wizard_error", **wizard_data)
        raise CLIDatasourceException(FeedbackManager.error(message=str(e)))


def generate_short_id():
    return str(uuid.uuid4())[:4]


def analyze_quarantine(datasource_name: str, project: Project, client: TinyB):
    config = CLIConfig.get_project_config()
    res = client.query(f"SELECT * FROM {datasource_name}_quarantine ORDER BY insertion_date DESC LIMIT 1 FORMAT JSON")
    quarantine_data = res["data"]
    error_message = json.dumps(res["data"])
    user_token = config.get_user_token()
    click.echo(FeedbackManager.gray(message=f"\n» Analyzing errors in {datasource_name}_quarantine..."))
    if user_token:
        try:
            llm = LLM(user_token=user_token, host=config.get_client().host)
            ds_filenames = project.get_datasource_files()
            datasource_definition = next(
                (Path(f).read_text() for f in ds_filenames if f.endswith(f"{datasource_name}.datasource")), ""
            )
            response_llm = llm.ask(
                system_prompt=quarantine_prompt(datasource_definition),
                prompt=f"The quarantine errors are:\n{json.dumps(quarantine_data)}",
                feature="tb_datasource_append_analyze_quarantine",
            )
            response = extract_xml(response_llm, "quarantine_errors")
            error_message += "\n" + response
            click.echo(response)
        except Exception:
            click.echo(FeedbackManager.error(message="There was an error analyzing the quarantine errors"))
    else:
        echo_safe_humanfriendly_tables_format_smart_table(
            data=[d.values() for d in res["data"]], column_names=res["data"][0].keys()
        )

    add_telemetry_event("datasource_error", error=f"quarantine_error: {error_message}")


def select_auto_offset_reset(current_value: Optional[str] = None) -> str:
    return click.prompt(
        FeedbackManager.highlight(message="? Auto offset reset"),
        type=click.Choice(["latest", "earliest"], case_sensitive=False),
        default=current_value or "latest",
        show_default=True,
    )


def select_format_file(current_value: Optional[str] = None) -> str:
    """Select file format for import operations.

    Args:
        current_value: Current format value to use as default

    Returns:
        Selected format string ("auto", "csv", "ndjson", or "parquet")
    """
    result = click.prompt(
        FeedbackManager.highlight(message="? Import format"),
        type=click.Choice(["Auto", "CSV", "NDJSON", "Parquet"], case_sensitive=False),
        default=current_value or "Auto",
        show_default=True,
    )
    return result.lower()
