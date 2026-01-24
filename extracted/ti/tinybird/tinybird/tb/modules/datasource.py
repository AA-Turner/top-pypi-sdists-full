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
from tinybird.tb.client import AuthNoTokenException, DoesNotExistException, TinyB
from tinybird.tb.modules.agent.utils import (
    create_terminal_box,
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
)
from tinybird.tb.modules.config import CLIConfig
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
    create_resources_from_prompt,
    generate_gcs_connection_file_with_secrets,
)
from tinybird.tb.modules.datafile.fixture import persist_fixture
from tinybird.tb.modules.exceptions import CLIDatasourceException
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.llm import LLM
from tinybird.tb.modules.llm_utils import extract_xml
from tinybird.tb.modules.project import Project
from tinybird.tb.modules.secret import save_secret_to_env_file
from tinybird.tb.modules.telemetry import add_telemetry_event


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
@click.option("--concurrency", help="How many files to submit concurrently", default=1, hidden=True)
@click.pass_context
def datasource_append(
    ctx: Context,
    datasource_name: str,
    data: Optional[str],
    url: str,
    file: str,
    events: str,
    concurrency: int,
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
        tip = "Did you build your project? Run `tb build` first."
    else:
        tip = "Did you deploy your project? Run `tb --cloud deploy` first."

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
                FeedbackManager.gray(message="Tip: Run tb datasource append [datasource_name] to skip this step.")
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
                    message="Tip: Run tb datasource append [datasource_name] --events | --file | --url to skip this step"
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
        click.echo(FeedbackManager.highlight(message=f"\n» Sending events to {datasource_name}"))
        response = requests.post(
            f"{client.host}/v0/events?name={datasource_name}",
            headers={"Authorization": f"Bearer {client.token}"},
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
            push_data(
                client,
                datasource_name,
                data,
                mode="append",
                concurrency=concurrency,
                silent=True,
            )
        except Exception as e:
            is_quarantined = "quarantine" in str(e)
            click.echo(FeedbackManager.error(message="✗ " + str(e)))
            if is_quarantined:
                analyze_quarantine(datasource_name, project, client)
                return
            else:
                raise e
        click.echo(FeedbackManager.success(message="✓ Rows appended!"))


@datasource.command(name="replace")
@click.argument("datasource_name", required=True)
@click.argument("url", nargs=-1, required=True)
@click.option("--sql-condition", default=None, help="SQL WHERE condition to replace data", hidden=True)
@click.option("--skip-incompatible-partition-key", is_flag=True, default=False, hidden=True)
@click.pass_context
def datasource_replace(
    ctx: Context,
    datasource_name,
    url,
    sql_condition,
    skip_incompatible_partition_key,
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
    push_data(
        client,
        datasource_name,
        url,
        mode="replace",
        sql_condition=sql_condition,
        replace_options=replace_options,
    )


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


@datasource.command(name="delete")
@click.argument("datasource_name")
@click.option("--sql-condition", default=None, help="SQL WHERE condition to remove rows", hidden=True, required=True)
@click.option("--yes", is_flag=True, default=False, help="Do not ask for confirmation")
@click.option("--wait", is_flag=True, default=False, help="Wait for delete job to finish, disabled by default")
@click.option("--dry-run", is_flag=True, default=False, help="Run the command without deleting anything")
@click.pass_context
def datasource_delete_rows(ctx, datasource_name, sql_condition, yes, wait, dry_run):
    """
    Delete rows from a datasource

    - Delete rows with SQL condition: `tb datasource delete [datasource_name] --sql-condition "country='ES'"`

    - Delete rows with SQL condition and wait for the job to finish: `tb datasource delete [datasource_name] --sql-condition "country='ES'" --wait`
    """

    client: TinyB = ctx.ensure_object(dict)["client"]
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
            res = client.datasource_delete_rows(datasource_name, sql_condition, dry_run)
            if dry_run:
                click.echo(
                    FeedbackManager.success_dry_run_delete_rows_datasource(
                        rows=res["rows_to_be_deleted"], datasource=datasource_name, delete_condition=sql_condition
                    )
                )
                return
            job_id = res["job_id"]
            job_url = res["job_url"]
            click.echo(FeedbackManager.info_datasource_delete_rows_job_url(url=job_url))
            if wait:
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


@datasource.command(name="create")
@click.option("--name", type=str, help="Name of the data source")
@click.option("--blank", is_flag=True, default=False, help="Create a blank data source")
@click.option("--file", type=str, help="Create a data source from a local file")
@click.option("--url", type=str, help="Create a data source from a remote URL")
@click.option("--prompt", type=str, help="Create a data source from a prompt")
@click.option("--connection-name", type=str, help="Create a data source from a connection")
@click.option("--s3", is_flag=True, default=False, help="Create a data source from a S3 connection")
@click.option("--gcs", is_flag=True, default=False, help="Create a data source from a GCS connection")
@click.option("--kafka", is_flag=True, default=False, help="Create a data source from a Kafka connection")
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
@click.option("--yes", is_flag=True, default=False, help="Do not ask for confirmation")
@click.pass_context
def datasource_create(
    ctx: Context,
    name: str,
    blank: bool,
    file: str,
    url: str,
    connection_name: Optional[str],
    prompt: str,
    s3: bool,
    gcs: bool,
    kafka: bool,
    kafka_topic_param: str,
    kafka_group_id_param: str,
    kafka_auto_offset_reset_param: str,
    s3_bucket_uri_param: Optional[str],
    s3_sample_file_param: Optional[str],
    s3_schedule_param: Optional[str],
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
            "prompt": ("Prompt", "Create a data source from a prompt"),
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
        elif prompt:
            datasource_type = "prompt"
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
                        message=("Tip: Run `tb datasource create --file | --url | --connection` to skip this step.")
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

        if datasource_type == "prompt":
            if not config.get("user_token"):
                raise Exception("This action requires authentication. Run 'tb login' first.")

            instructions = (
                "Create or update a Tinybird datasource (.datasource file) for this project. "
                "Do not generate mock data or append data; those steps will run later programmatically."
            )
            if not prompt:
                wizard_data["current_step"] = "enter_prompt"
                prompt = click.prompt(FeedbackManager.highlight(message="? Enter your prompt"))
            wizard_data["prompt"] = prompt

            if name:
                instructions += f" Name the datasource '{name}'."

            created_resources = create_resources_from_prompt(
                config,
                project,
                prompt,
                feature="tb_datasource_create",
                instructions=instructions,
            )
            if any(path.suffix == ".datasource" for path in created_resources):
                click.echo(FeedbackManager.success(message="✓ .datasource created!"))
            else:
                click.echo(
                    FeedbackManager.gray(
                        message="△ No new datasource file detected. Existing resources may have been updated instead."
                    )
                )

            wizard_data["current_step"] = "completed"
            wizard_data["duration_seconds"] = round(time.time() - start_time, 2)
            add_telemetry_event("system_info", **wizard_data)
            return

        connection_required = datasource_type in ("kafka", "s3", "gcs")

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
                    new_connection_created = True
                    if env == "local" and new_connection_created:
                        click.echo(FeedbackManager.gray(message="\n» Building project to access the new connection..."))
                        build_project(project=project, tb_client=client, watch=False, config=config, silent=True)
                        click.echo(FeedbackManager.success(message="✓ Build completed!"))
                else:
                    click.echo(
                        FeedbackManager.info(
                            message=f"→ To continue, you need a connection. Run `tb connection create {datasource_type}` to create one."
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
                click.echo(FeedbackManager.gray(message="\n» Generating schema..."))
                response = client.preview_s3(s3_connection_id, s3_bucket_uri, s3_sample_file, None)
                meta = response.get("preview", {}).get("meta", [])
                ds_content = meta_to_s3_datasource_datafile(meta, connection_name, s3_bucket_uri, s3_schedule)

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
                ds_content = meta_to_s3_datasource_datafile(meta, connection_name, s3_bucket_uri, s3_schedule)
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
            tip_message = """Next steps:
    - Run `tb deploy` to consume from the topic in Tinybird Local.
    - Run `tb --cloud deploy` to deploy the new resource to Tinybird Cloud."""
        else:
            tip_message = """Next steps:
    - Run `tb --cloud deploy` to deploy the new resource to Tinybird Cloud."""

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
