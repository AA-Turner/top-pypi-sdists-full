import json
import logging
import re
import time
from copy import deepcopy
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlencode, urljoin

import click
import requests

from tinybird.datafile.parse_datasource import parse_datasource
from tinybird.tb.client import TinyB
from tinybird.tb.modules.common import push_data, sys_exit
from tinybird.tb.modules.datafile.fixture import FixtureExtension, get_fixture_dir, persist_fixture
from tinybird.tb.modules.deployment_common import api_fetch
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.local_common import get_local_tokens
from tinybird.tb.modules.project import Project
from tinybird.tb.modules.query_output import print_table_formatted


def process(
    project: Project,
    tb_client: TinyB,
    watch: bool,
    config: dict[str, Any],
    file_changed: Optional[str] = None,
    diff: Optional[str] = None,
    silent: bool = False,
    exit_on_error: bool = True,
    load_fixtures: bool = True,
    project_with_vendors: Optional[Project] = None,
    is_branch: bool = False,
    with_connections: bool = False,
    use_deployment_api: bool = False,
) -> Optional[str]:
    time_start = time.time()

    # Build vendored workspaces before build
    if not project_with_vendors and not is_branch:
        build_vendored_workspaces(project=project, tb_client=tb_client, config=config)

    # Ensure SHARED_WITH workspaces exist before build
    if not is_branch:
        build_shared_with_workspaces(project=project, tb_client=tb_client, config=config)

    build_failed = False
    build_error: Optional[str] = None
    build_result: Optional[bool] = None

    if file_changed and file_changed.endswith((FixtureExtension.NDJSON, FixtureExtension.CSV)):
        rebuild_fixture(project, tb_client, file_changed)

    elif file_changed and file_changed.endswith(".sql"):
        rebuild_fixture_sql(project, tb_client, file_changed)

    elif file_changed and file_changed.endswith((".env.local", ".env")):
        pass
    else:
        try:
            build_result = build_project(
                project,
                tb_client,
                silent,
                load_fixtures,
                project_with_vendors=project_with_vendors,
                with_connections=with_connections,
                use_deployment_api=use_deployment_api,
            )

        except click.ClickException as e:
            if not silent:
                click.echo(FeedbackManager.info(message=str(e)))
            build_error = str(e)
            build_failed = True
        try:
            if file_changed and not build_failed:
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

        return build_error

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
    project: Project,
    tb_client: TinyB,
    silent: bool = False,
    load_fixtures: bool = True,
    project_with_vendors: Optional[Project] = None,
    with_connections: bool = False,
    use_deployment_api: bool = False,
) -> Optional[bool]:
    build_url = "/v1/build"
    if with_connections:
        build_url = f"{build_url}?with_connections=true"
    TINYBIRD_API_URL = urljoin(tb_client.host, build_url)
    logging.debug(TINYBIRD_API_URL)
    TINYBIRD_API_KEY = tb_client.token
    request_from = getattr(tb_client, "request_from", None)
    error: Optional[str] = None

    try:
        if use_deployment_api:
            return build_project_with_deploy_api(
                project=project,
                tb_client=tb_client,
                silent=silent,
                load_fixtures=load_fixtures,
                project_with_vendors=project_with_vendors,
            )

        files, project_files = get_build_request_files(project, project_with_vendors)

        if not project_files:
            return False

        HEADERS = {"Authorization": f"Bearer {TINYBIRD_API_KEY}"}
        params = {"from": request_from} if request_from else None
        r = requests.post(TINYBIRD_API_URL, files=files, headers=HEADERS, params=params)
        try:
            result = r.json()
        except Exception as e:
            logging.debug(e, exc_info=True)
            click.echo(FeedbackManager.error(message="Couldn't parse response from server"))
            sys_exit("build_error", str(e))

        logging.debug(json.dumps(result, indent=2))

        build_result = result.get("result")
        if build_result == "success":
            build = result.get("build") or {}
            changes = get_build_changes(build)
            if not has_build_changes(changes):
                return False
            echo_build_changes(project, changes, silent)
            if load_fixtures:
                append_project_fixtures(project, tb_client, project_files)
            echo_build_feedback(build.get("feedback", []))
            if with_connections:
                echo_dynamodb_local_backfill_feedback(build)
            return True
        elif build_result == "failed":
            error = format_build_errors(result.get("errors", []))
        else:
            error = f"Unknown build result. Error: {result.get('error')}"
    except click.ClickException:
        raise
    except Exception as e:
        error = str(e)

    if error:
        raise click.ClickException(error)

    return False


def build_project_with_deploy_api(
    project: Project,
    tb_client: TinyB,
    silent: bool = False,
    load_fixtures: bool = True,
    project_with_vendors: Optional[Project] = None,
) -> Optional[bool]:
    deploy_url = urljoin(tb_client.host, "/v1/deploy")
    logging.debug(deploy_url)
    request_from = getattr(tb_client, "request_from", None)
    files, project_files = get_build_request_files(project, project_with_vendors)

    if not project_files:
        return False

    headers = {"Authorization": f"Bearer {tb_client.token}"}
    params: dict[str, str] = {"auto_promote": "true"}
    if request_from:
        params["from"] = request_from

    response = requests.post(deploy_url, files=files, headers=headers, params=params)
    try:
        result = response.json()
    except Exception as e:
        logging.debug(e, exc_info=True)
        click.echo(FeedbackManager.error(message="Couldn't parse response from server"))
        sys_exit("build_error", str(e))

    logging.debug(json.dumps(result, indent=2))

    build_result = result.get("result")
    deployment = result.get("deployment") or {}
    if build_result == "no_changes":
        return False
    if build_result != "success":
        deployment_errors = deployment.get("errors", []) if deployment else result.get("errors", [])
        raise click.ClickException(result.get("error") or format_build_errors(deployment_errors))
    if not deployment:
        raise click.ClickException("Couldn't parse deployment response from server")

    deployment = wait_for_build_deployment_to_be_live(
        tb_client=tb_client,
        headers=headers,
        deployment=deployment,
        request_from=request_from,
        silent=silent,
    )
    changes = get_build_changes(deployment)
    if not has_build_changes(changes):
        return False

    echo_build_changes(project, changes, silent)
    if load_fixtures:
        append_project_fixtures(project, tb_client, project_files)
    echo_build_feedback(deployment.get("feedback", []))
    return True


def get_build_request_files(
    project: Project,
    project_with_vendors: Optional[Project] = None,
) -> tuple[list[tuple[str, tuple[str, str, str]]], list[str]]:
    multipart_boundary_data_project = "data_project://"
    datafile_type_to_content_type = {
        ".datasource": "text/plain",
        ".pipe": "text/plain",
        ".connection": "text/plain",
    }
    files: list[tuple[str, tuple[str, str, str]]] = [
        ("context://", ("cli-version", "1.0.0", "text/plain")),
    ]
    project_path = project.path
    project_files = project.get_project_files()

    for file_path in project_files:
        relative_path = Path(file_path).relative_to(project_path).as_posix()
        with open(file_path, "rb") as fd:
            content_type = datafile_type_to_content_type.get(Path(file_path).suffix, "application/unknown")
            content = fd.read().decode("utf-8")
            if project_with_vendors:
                # Replace SHARED_WITH targets when building vendored workspaces against the main project.
                content = replace_shared_with(content, [project_with_vendors.workspace_name])

            files.append((multipart_boundary_data_project, (relative_path, content, content_type)))

    return files, project_files


def wait_for_build_deployment_to_be_live(
    tb_client: TinyB,
    headers: dict[str, str],
    deployment: dict[str, Any],
    request_from: Optional[str],
    silent: bool,
) -> dict[str, Any]:
    if not silent:
        click.echo(FeedbackManager.highlight(message="» Waiting for deployment to be ready..."))

    poll_interval = 5
    times_seen_failed = 0
    while True:
        url = f"{tb_client.host}/v1/deployments/{deployment.get('id')}"
        result = api_fetch(url, headers, request_from=request_from)
        deployment = result.get("deployment", {})
        if not deployment:
            raise click.ClickException("Error parsing deployment from response")

        status = deployment.get("status")
        if status == "failed":
            times_seen_failed += 1
            if times_seen_failed > 60:
                raise click.ClickException("Deployment failed and wasn't deleted automatically")
            time.sleep(poll_interval)
            continue

        if status in ("deleting", "deleted"):
            errors = deployment.get("errors", [])
            raise click.ClickException(f"Deployment deleted after failure. Errors: {errors}")

        if deployment.get("live"):
            return deployment

        time.sleep(poll_interval)


def get_build_changes(result: dict[str, Any]) -> dict[str, list[str]]:
    return {
        "new_datasources": result.get("new_datasource_names", []),
        "changed_datasources": result.get("changed_datasource_names", []),
        "deleted_datasources": result.get("deleted_datasource_names", []),
        "new_pipes": result.get("new_pipe_names", []),
        "changed_pipes": result.get("changed_pipe_names", []),
        "deleted_pipes": result.get("deleted_pipe_names", []),
        "new_connections": result.get("new_data_connector_names", []),
        "changed_connections": result.get("changed_data_connector_names", []),
        "deleted_connections": result.get("deleted_data_connector_names", []),
    }


def has_build_changes(changes: dict[str, list[str]]) -> bool:
    return any(changes.values())


def echo_build_changes(project: Project, changes: dict[str, list[str]], silent: bool) -> None:
    if silent:
        return

    echo_changes(project, changes["new_datasources"], ".datasource", "created")
    echo_changes(project, changes["changed_datasources"], ".datasource", "changed")
    echo_changes(project, changes["deleted_datasources"], ".datasource", "deleted")
    echo_changes(project, changes["new_pipes"], ".pipe", "created")
    echo_changes(project, changes["changed_pipes"], ".pipe", "changed")
    echo_changes(project, changes["deleted_pipes"], ".pipe", "deleted")
    echo_changes(project, changes["new_connections"], ".connection", "created")
    echo_changes(project, changes["changed_connections"], ".connection", "changed")
    echo_changes(project, changes["deleted_connections"], ".connection", "deleted")


def append_project_fixtures(
    project: Project,
    tb_client: TinyB,
    project_files: list[str],
) -> None:
    ds_name = ""
    try:
        for filename in project_files:
            if not filename.endswith(".datasource"):
                continue

            ds_name = Path(filename).stem
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


def echo_build_feedback(feedback: list[dict[str, Any]]) -> None:
    for item in feedback:
        click.echo(
            FeedbackManager.warning(message=f"△ {item.get('level')}: {item.get('resource')}: {item.get('message')}")
        )


def echo_dynamodb_local_backfill_feedback(build: dict[str, Any]) -> None:
    datasources_by_id = {datasource.get("id"): datasource.get("name") for datasource in build.get("datasources", [])}
    for data_linker in build.get("data_linkers", []):
        if data_linker.get("service") != "dynamodb":
            continue

        settings = data_linker.get("settings") or {}
        export_arn = settings.get("initial_export_arn")
        if not export_arn:
            continue

        datasource_name = datasources_by_id.get(data_linker.get("datasource_id")) or "unknown"
        click.echo(
            FeedbackManager.warning(
                message=(
                    f"△ DynamoDB initial export backfill started for datasource '{datasource_name}'. "
                    "AWS exports can stay in progress for several minutes; Tinybird Local will keep retrying "
                    f"the import until AWS marks the export as completed. Export ARN: {export_arn}."
                )
            )
        )


def format_build_errors(build_errors: list[dict[str, Any]]) -> str:
    full_error_msg = ""
    for build_error in build_errors:
        filename_bit = build_error.get("filename", build_error.get("resource", ""))
        error_bit = build_error.get("error") or build_error.get("message") or ""
        error_msg = ((filename_bit + "\n") if filename_bit else "") + error_bit
        full_error_msg += error_msg + "\n\n"
    return full_error_msg.strip("\n") or "Unknown build error"


def echo_changes(project: Project, changes: list[str], extension: str, status: str):
    resource_type_by_extension = {
        ".datasource": "datasource",
        ".pipe": "pipe",
        ".connection": "connection",
    }
    for resource in changes:
        resource_type = resource_type_by_extension.get(extension)
        path_str = project.get_resource_path(resource, resource_type) if resource_type else ""
        if not path_str:
            path_str = resource + extension
        if path_str:
            click.echo(FeedbackManager.info(message=f"✓ {path_str} {status}"))


def find_workspace_or_create(user_client: TinyB, workspace_name: str) -> Optional[str]:
    # Get a client scoped to the vendored workspace using the user token
    ws_token = None
    org_id = None
    try:
        # Fetch org id and workspaces with tokens
        info = user_client.user_workspaces_with_organization(version="v1")
        org_id = info.get("organization_id")
        workspaces = info.get("workspaces", [])
        found = next((w for w in workspaces if w.get("name") == workspace_name), None)
        if found:
            ws_token = found.get("token")
        # If still not found, try the generic listing
        if not ws_token:
            workspaces_full = user_client.user_workspaces_and_branches(version="v1")
            created_ws = next(
                (w for w in workspaces_full.get("workspaces", []) if w.get("name") == workspace_name), None
            )
            if created_ws:
                ws_token = created_ws.get("token")
    except Exception:
        ws_token = None

    # If workspace doesn't exist, try to create it and fetch its token
    if not ws_token:
        try:
            user_client.create_workspace(workspace_name, assign_to_organization_id=org_id, version="v1")
            # Fetch token for newly created workspace
            info_after = user_client.user_workspaces_and_branches(version="v1")
            created = next((w for w in info_after.get("workspaces", []) if w.get("name") == workspace_name), None)
            ws_token = created.get("token") if created else None
        except Exception as e:
            click.echo(
                FeedbackManager.warning(
                    message=(f"Skipping vendored workspace '{workspace_name}': unable to create or resolve token ({e})")
                )
            )

    return ws_token


def build_vendored_workspaces(project: Project, tb_client: TinyB, config: dict[str, Any]) -> None:
    """Build each vendored workspace under project.vendor_path if present.

    Directory structure expected: vendor/<workspace_name>/<data_project_inside>
    Each top-level directory under vendor is treated as a separate workspace
    whose project files will be built using that workspace's token.
    """
    try:
        vendor_root = Path(project.vendor_path)

        if not vendor_root.exists() or not vendor_root.is_dir():
            return

        tokens = get_local_tokens()
        user_token = tokens["user_token"]
        user_client = deepcopy(tb_client)
        user_client.token = user_token

        # Iterate over vendored workspace folders
        for ws_dir in sorted([p for p in vendor_root.iterdir() if p.is_dir()]):
            workspace_name = ws_dir.name
            ws_token = find_workspace_or_create(user_client, workspace_name)

            if not ws_token:
                click.echo(
                    FeedbackManager.warning(
                        message=f"Skipping vendored workspace '{workspace_name}': could not resolve token after creation"
                    )
                )
                continue

            # Build using a client scoped to the vendor workspace token
            vendor_client = deepcopy(tb_client)
            vendor_client.token = ws_token
            vendor_project = Project(folder=str(ws_dir), workspace_name=workspace_name, max_depth=project.max_depth)
            workspace_info = tb_client.workspace_info(version="v1")
            project.workspace_name = workspace_info.get("name", "")
            # Do not exit on error to allow main project to continue
            process(
                project=vendor_project,
                tb_client=vendor_client,
                watch=False,
                silent=True,
                exit_on_error=True,
                load_fixtures=True,
                config=config,
                project_with_vendors=project,
            )
    except Exception as e:
        # Never break the main build due to vendored build errors
        click.echo(FeedbackManager.error_exception(error=e))


def build_shared_with_workspaces(project: Project, tb_client: TinyB, config: dict[str, Any]) -> None:
    """Scan project for .datasource files and ensure SHARED_WITH workspaces exist."""

    try:
        # Gather SHARED_WITH workspace names from all .datasource files
        datasource_files = project.get_datasource_files()
        shared_ws_names = set()

        for filename in datasource_files:
            try:
                doc = parse_datasource(filename).datafile
                for ws_name in doc.shared_with or []:
                    shared_ws_names.add(ws_name)
            except Exception:
                # Ignore parse errors here; they'll be handled during the main process()
                continue

        if not shared_ws_names:
            return

        # Need a user token to list/create workspaces
        tokens = get_local_tokens()
        user_token = tokens.get("user_token")
        if not user_token:
            click.echo(FeedbackManager.info_skipping_shared_with_entry())
            return

        user_client = deepcopy(tb_client)
        user_client.token = user_token

        # Ensure each SHARED_WITH workspace exists
        for ws_name in sorted(shared_ws_names):
            find_workspace_or_create(user_client, ws_name)
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=e))


def replace_shared_with(text: str, new_workspaces: list[str]) -> str:
    replacement = ", ".join(new_workspaces)

    # 1) Formato multilinea:
    # SHARED_WITH >
    #     workspace1, workspace2
    #
    # Solo sustituimos la LÍNEA de workspaces (grupo 3), no usamos DOTALL.
    pat_multiline = re.compile(r"(?m)^(SHARED_WITH\s*>\s*)\n([ \t]*)([^\n]*)$")
    if pat_multiline.search(text):
        return pat_multiline.sub(lambda m: f"{m.group(1)}\n{m.group(2)}{replacement}", text)

    # 2) Formato inline:
    # SHARED_WITH workspace1, workspace2
    pat_inline = re.compile(r"(?m)^(SHARED_WITH\s+)([^\n]*)$")
    if pat_inline.search(text):
        return pat_inline.sub(lambda m: f"{m.group(1)}{replacement}", text)

    return text
