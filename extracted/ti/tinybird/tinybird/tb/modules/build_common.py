import json
import logging
import time
from pathlib import Path
from typing import Optional
from urllib.parse import urlencode, urljoin

import click
import requests

from tinybird.tb.client import TinyB
from tinybird.tb.modules.common import push_data, sys_exit
from tinybird.tb.modules.datafile.fixture import FixtureExtension, get_fixture_dir, persist_fixture
from tinybird.tb.modules.dev_server import BuildStatus
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.project import Project
from tinybird.tb.modules.shell import print_table_formatted


def process(
    project: Project,
    tb_client: TinyB,
    watch: bool,
    file_changed: Optional[str] = None,
    diff: Optional[str] = None,
    silent: bool = False,
    build_status: Optional[BuildStatus] = None,
    exit_on_error: bool = True,
    load_fixtures: bool = True,
) -> Optional[str]:
    time_start = time.time()
    build_failed = False
    build_error: Optional[str] = None
    build_result: Optional[bool] = None
    if build_status:
        if build_status.building:
            return build_status.error
        else:
            build_status.building = True
    if file_changed and (file_changed.endswith(FixtureExtension.NDJSON) or file_changed.endswith(FixtureExtension.CSV)):
        rebuild_fixture(project, tb_client, file_changed)
        if build_status:
            build_status.building = False
            build_status.error = None
    elif file_changed and file_changed.endswith(".sql"):
        rebuild_fixture_sql(project, tb_client, file_changed)
        if build_status:
            build_status.building = False
            build_status.error = None
    elif file_changed and (file_changed.endswith(".env.local") or file_changed.endswith(".env")):
        if build_status:
            build_status.building = False
            build_status.error = None
    else:
        try:
            build_result = build_project(project, tb_client, silent, load_fixtures)
            if build_status:
                build_status.building = False
                build_status.error = None
        except click.ClickException as e:
            if not silent:
                click.echo(FeedbackManager.info(message=str(e)))
            build_error = str(e)
            build_failed = True
        try:
            if file_changed and not build_failed and not build_status:
                show_data(tb_client, file_changed, diff)
        except Exception:
            pass

    time_end = time.time()
    elapsed_time = time_end - time_start

    rebuild_str = "Rebuild" if watch and file_changed else "Build"
    if build_failed:
        if not silent:
            click.echo(FeedbackManager.error(message=f"✗ {rebuild_str} failed"))
            if not watch and exit_on_error:
                sys_exit("build_error", build_error or "Unknown error")
        build_error = build_error or "Unknown error"
        if build_status:
            build_status.error = build_error
            build_status.building = False
        return build_error
    else:
        if not silent:
            if build_result == False:  # noqa: E712
                click.echo(FeedbackManager.info(message="No changes. Build skipped."))
            else:
                click.echo(FeedbackManager.success(message=f"\n✓ {rebuild_str} completed in {elapsed_time:.1f}s"))

    return None


def rebuild_fixture(project: Project, tb_client: TinyB, fixture: str) -> None:
    try:
        fixture_path = Path(fixture)
        datasources_path = Path(project.folder) / "datasources"
        ds_name = fixture_path.stem

        if ds_name not in project.datasources:
            try:
                ds_name = "_".join(fixture_path.stem.split("_")[:-1])
            except Exception:
                pass

        ds_path = datasources_path / f"{ds_name}.datasource"

        if ds_path.exists():
            tb_client.datasource_truncate(ds_name)
            append_fixture(tb_client, ds_name, str(fixture_path))
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=e))


def rebuild_fixture_sql(project: Project, tb_client: TinyB, sql_file: str) -> Path:
    sql_path = Path(sql_file)
    datasource_name = sql_path.stem
    valid_extensions = [FixtureExtension.NDJSON, FixtureExtension.CSV]
    fixtures_path = get_fixture_dir(project.folder)
    current_fixture_path = next(
        (
            fixtures_path / f"{datasource_name}{extension}"
            for extension in valid_extensions
            if (fixtures_path / f"{datasource_name}{extension}").exists()
        ),
        None,
    )
    fixture_format = current_fixture_path.suffix.lstrip(".") if current_fixture_path else "ndjson"
    sql = sql_path.read_text()
    sql_format = "CSV" if fixture_format == "csv" else "JSON"
    result = tb_client.query(f"{sql} FORMAT {sql_format}")
    data = result.get("data", [])
    return persist_fixture(datasource_name, data, project.folder, format=fixture_format)


def append_fixture(
    tb_client: TinyB,
    datasource_name: str,
    url: str,
):
    # Append fixtures only if the datasource is empty
    data = tb_client._req(f"/v0/datasources/{datasource_name}")
    if data.get("statistics", {}).get("row_count", 0) > 0:
        return

    push_data(
        tb_client,
        datasource_name,
        url,
        mode="append",
        concurrency=1,
        silent=True,
    )


def show_data(tb_client: TinyB, filename: str, diff: Optional[str] = None):
    table_name = diff
    resource_path = Path(filename)
    resource_name = resource_path.stem

    pipeline = resource_name if filename.endswith(".pipe") else None

    if not table_name:
        table_name = resource_name

    sql = f"SELECT * FROM {table_name} FORMAT JSON"

    res = tb_client.query(sql, pipeline=pipeline)
    print_table_formatted(res, table_name)
    if Project.get_pipe_type(filename) == "endpoint":
        example_params = {
            "format": "json",
            "pipe": resource_name,
            "q": "",
            "token": tb_client.token,
        }
        endpoint_url = tb_client._req(f"/examples/query.http?{urlencode(example_params)}")
        if endpoint_url:
            endpoint_url = endpoint_url.replace("http://localhost:8001", tb_client.host)
            click.echo(FeedbackManager.gray(message="\nTest endpoint at ") + FeedbackManager.info(message=endpoint_url))


def build_project(
    project: Project, tb_client: TinyB, silent: bool = False, load_fixtures: bool = True
) -> Optional[bool]:
    MULTIPART_BOUNDARY_DATA_PROJECT = "data_project://"
    DATAFILE_TYPE_TO_CONTENT_TYPE = {
        ".datasource": "text/plain",
        ".pipe": "text/plain",
        ".connection": "text/plain",
    }
    TINYBIRD_API_URL = urljoin(tb_client.host, "/v1/build")
    logging.debug(TINYBIRD_API_URL)
    TINYBIRD_API_KEY = tb_client.token
    error: Optional[str] = None
    try:
        files = [
            ("context://", ("cli-version", "1.0.0", "text/plain")),
        ]
        project_path = project.path
        project_files = project.get_project_files()

        if not project_files:
            return False

        for file_path in project_files:
            relative_path = Path(file_path).relative_to(project_path).as_posix()
            with open(file_path, "rb") as fd:
                content_type = DATAFILE_TYPE_TO_CONTENT_TYPE.get(Path(file_path).suffix, "application/unknown")
                files.append(
                    (MULTIPART_BOUNDARY_DATA_PROJECT, (relative_path, fd.read().decode("utf-8"), content_type))
                )
        HEADERS = {"Authorization": f"Bearer {TINYBIRD_API_KEY}"}

        r = requests.post(TINYBIRD_API_URL, files=files, headers=HEADERS)
        try:
            result = r.json()
        except Exception as e:
            logging.debug(e, exc_info=True)
            click.echo(FeedbackManager.error(message="Couldn't parse response from server"))
            sys_exit("build_error", str(e))

        logging.debug(json.dumps(result, indent=2))

        build_result = result.get("result")
        if build_result == "success":
            build = result.get("build")
            new_datasources = build.get("new_datasource_names", [])
            new_pipes = build.get("new_pipe_names", [])
            new_connections = build.get("new_data_connector_names", [])
            changed_datasources = build.get("changed_datasource_names", [])
            changed_pipes = build.get("changed_pipe_names", [])
            changed_connections = build.get("changed_data_connector_names", [])
            deleted_datasources = build.get("deleted_datasource_names", [])
            deleted_pipes = build.get("deleted_pipe_names", [])
            deleted_connections = build.get("deleted_data_connector_names", [])

            no_changes = (
                not new_datasources
                and not changed_datasources
                and not new_pipes
                and not changed_pipes
                and not new_connections
                and not changed_connections
                and not deleted_datasources
                and not deleted_pipes
                and not deleted_connections
            )
            if no_changes:
                return False
            else:
                if not silent:
                    echo_changes(project, new_datasources, ".datasource", "created")
                    echo_changes(project, changed_datasources, ".datasource", "changed")
                    echo_changes(project, deleted_datasources, ".datasource", "deleted")
                    echo_changes(project, new_pipes, ".pipe", "created")
                    echo_changes(project, changed_pipes, ".pipe", "changed")
                    echo_changes(project, deleted_pipes, ".pipe", "deleted")
                    echo_changes(project, new_connections, ".connection", "created")
                    echo_changes(project, changed_connections, ".connection", "changed")
                    echo_changes(project, deleted_connections, ".connection", "deleted")
            if load_fixtures:
                try:
                    for filename in project_files:
                        if filename.endswith(".datasource"):
                            ds_path = Path(filename)
                            ds_name = ds_path.stem
                            fixture_folder = get_fixture_dir(project.folder)
                            fixture_extensions = [FixtureExtension.NDJSON, FixtureExtension.CSV]
                            fixture_path = next(
                                (
                                    fixture_folder / f"{ds_name}{ext}"
                                    for ext in fixture_extensions
                                    if (fixture_folder / f"{ds_name}{ext}").exists()
                                ),
                                None,
                            )
                            if not fixture_path:
                                sql_path = fixture_folder / f"{ds_name}.sql"
                                if sql_path.exists():
                                    fixture_path = rebuild_fixture_sql(project, tb_client, str(sql_path))

                            if fixture_path:
                                append_fixture(tb_client, ds_name, str(fixture_path))

                except Exception as e:
                    click.echo(FeedbackManager.error_exception(error=f"Error appending fixtures for '{ds_name}': {e}"))

            feedback = build.get("feedback", [])
            for f in feedback:
                click.echo(
                    FeedbackManager.warning(message=f"△ {f.get('level')}: {f.get('resource')}: {f.get('message')}")
                )
        elif build_result == "failed":
            build_errors = result.get("errors")
            full_error_msg = ""
            for build_error in build_errors:
                filename_bit = build_error.get("filename", build_error.get("resource", ""))
                error_bit = build_error.get("error") or build_error.get("message") or ""
                error_msg = ((filename_bit + "\n") if filename_bit else "") + error_bit
                full_error_msg += error_msg + "\n\n"
            error = full_error_msg.strip("\n") or "Unknown build error"
        else:
            error = f"Unknown build result. Error: {result.get('error')}"
    except Exception as e:
        error = str(e)

    if error:
        raise click.ClickException(error)

    return build_result


def echo_changes(project: Project, changes: list[str], extension: str, status: str):
    for resource in changes:
        path_str = next(
            (p for p in project.get_project_files() if p.endswith(resource + extension)), resource + extension
        )
        if path_str:
            path_str = path_str.replace(f"{project.folder}/", "")
            click.echo(FeedbackManager.info(message=f"✓ {path_str} {status}"))
