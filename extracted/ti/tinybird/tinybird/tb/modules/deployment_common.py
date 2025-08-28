import json
import logging
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

import click
import requests

from tinybird.tb.client import TinyB
from tinybird.tb.modules.common import (
    echo_safe_humanfriendly_tables_format_smart_table,
    get_display_cloud_host,
    sys_exit,
)
from tinybird.tb.modules.feedback_manager import FeedbackManager, bcolors
from tinybird.tb.modules.project import Project


# TODO(eclbg): This should eventually end up in client.py, but we're not using it here yet.
def api_fetch(url: str, headers: dict, max_retries: int = 3, backoff_factor: float = 0.5) -> dict:
    retries = 0
    while retries <= max_retries:
        try:
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                logging.debug(json.dumps(r.json(), indent=2))
                return r.json()
            else:
                raise Exception(f"Request failed with status code {r.status_code}")
        except Exception:
            retries += 1
            if retries > max_retries:
                break

            wait_time = backoff_factor * (2 ** (retries - 1))
            time.sleep(wait_time)

    # Try to parse and print the error from the response
    try:
        result = r.json()
        error = result.get("error")
        logging.debug(json.dumps(result, indent=2))
        click.echo(FeedbackManager.error(message=f"Error: {error}"))
        sys_exit("deployment_error", error)
    except Exception:
        message = "Error parsing response from API"
        click.echo(FeedbackManager.error(message=message))
        sys_exit("deployment_error", message)

    return {}


def api_post(
    url: str,
    headers: dict,
    files: Optional[list] = None,
    params: Optional[dict] = None,
) -> dict:
    r = requests.post(url, headers=headers, files=files, params=params)
    if r.status_code < 300:
        logging.debug(json.dumps(r.json(), indent=2))
        return r.json()

    # Try to parse and print the error from the response
    try:
        result = r.json()
        logging.debug(json.dumps(result, indent=2))
        error = result.get("error")
        if error:
            click.echo(FeedbackManager.error(message=f"Error: {error}"))
            sys_exit("deployment_error", error)
        return result
    except Exception:
        message = "Error parsing response from API"
        click.echo(FeedbackManager.error(message=message))
        sys_exit("deployment_error", message)

    return {}


# TODO(eclbg): This logic should be in the server, and there should be a dedicated endpoint for promoting a deployment
# potato
def promote_deployment(host: Optional[str], headers: dict, wait: bool, ingest_hint: Optional[bool] = True) -> None:
    TINYBIRD_API_URL = f"{host}/v1/deployments"
    result = api_fetch(TINYBIRD_API_URL, headers)

    deployments = result.get("deployments")
    if not deployments:
        message = "No deployments found"
        click.echo(FeedbackManager.error(message=message))
        sys_exit("deployment_error", message)
        return

    if len(deployments) < 2:
        message = "Only one deployment found"
        click.echo(FeedbackManager.error(message=message))
        sys_exit("deployment_error", message)
        return

    last_deployment, candidate_deployment = deployments[0], deployments[1]

    if candidate_deployment.get("status") != "data_ready":
        click.echo(FeedbackManager.error(message="Current deployment is not ready"))
        deploy_errors = candidate_deployment.get("errors", [])
        for deploy_error in deploy_errors:
            click.echo(FeedbackManager.error(message=f"* {deploy_error}"))
        sys_exit("deployment_error", "Current deployment is not ready: " + str(deploy_errors))
        return

    if candidate_deployment.get("live"):
        click.echo(FeedbackManager.error(message="Candidate deployment is already live"))
    else:
        TINYBIRD_API_URL = f"{host}/v1/deployments/{candidate_deployment.get('id')}/set-live"
        result = api_post(TINYBIRD_API_URL, headers=headers)

    click.echo(FeedbackManager.highlight(message="» Removing old deployment"))

    TINYBIRD_API_URL = f"{host}/v1/deployments/{last_deployment.get('id')}"
    r = requests.delete(TINYBIRD_API_URL, headers=headers)
    result = r.json()
    logging.debug(json.dumps(result, indent=2))
    if result.get("error"):
        click.echo(FeedbackManager.error(message=result.get("error")))
        sys_exit("deployment_error", result.get("error", "Unknown error"))
    click.echo(FeedbackManager.info(message="✓ Old deployment removed"))

    click.echo(FeedbackManager.highlight(message="» Waiting for deployment to be promoted..."))

    if wait:
        while True:
            TINYBIRD_API_URL = f"{host}/v1/deployments/{last_deployment.get('id')}"
            result = api_fetch(TINYBIRD_API_URL, headers=headers)

            last_deployment = result.get("deployment")
            if not last_deployment:
                click.echo(FeedbackManager.error(message="Error parsing deployment from response"))
                sys_exit("deployment_error", "Error parsing deployment from response")

            if last_deployment and last_deployment.get("status") == "deleted":
                click.echo(FeedbackManager.success(message=f"✓ Deployment #{candidate_deployment.get('id')} is live!"))
                break

            time.sleep(5)
    if last_deployment.get("id") == "0" and ingest_hint:
        # This is the first deployment, so we prompt the user to ingest data
        click.echo(
            FeedbackManager.info(
                message="A deployment with no data is useless. Learn how to ingest at https://www.tinybird.co/docs/forward/get-data-in"
            )
        )


# TODO(eclbg): This logic should be in the server, and there should be a dedicated endpoint for discarding a
# deployment
def discard_deployment(host: Optional[str], headers: dict, wait: bool) -> None:
    TINYBIRD_API_URL = f"{host}/v1/deployments"
    result = api_fetch(TINYBIRD_API_URL, headers=headers)

    deployments = result.get("deployments")
    if not deployments:
        click.echo(FeedbackManager.error(message="No deployments found"))
        return

    if len(deployments) < 2:
        click.echo(FeedbackManager.error(message="Only one deployment found"))
        return

    previous_deployment, current_deployment = deployments[0], deployments[1]

    if previous_deployment.get("status") != "data_ready":
        click.echo(FeedbackManager.error(message="Previous deployment is not ready"))
        deploy_errors = previous_deployment.get("errors", [])
        for deploy_error in deploy_errors:
            click.echo(FeedbackManager.error(message=f"* {deploy_error}"))
        return

    if previous_deployment.get("live"):
        click.echo(FeedbackManager.error(message="Previous deployment is already live"))
    else:
        click.echo(FeedbackManager.success(message="Promoting previous deployment"))

        TINYBIRD_API_URL = f"{host}/v1/deployments/{previous_deployment.get('id')}/set-live"
        result = api_post(TINYBIRD_API_URL, headers=headers)

    click.echo(FeedbackManager.success(message="Removing current deployment"))

    TINYBIRD_API_URL = f"{host}/v1/deployments/{current_deployment.get('id')}"
    r = requests.delete(TINYBIRD_API_URL, headers=headers)
    result = r.json()
    logging.debug(json.dumps(result, indent=2))
    if result.get("error"):
        click.echo(FeedbackManager.error(message=result.get("error")))
        sys_exit("deployment_error", result.get("error", "Unknown error"))

    click.echo(FeedbackManager.success(message="Discard process successfully started"))

    if wait:
        while True:
            TINYBIRD_API_URL = f"{host}/v1/deployments/{current_deployment.get('id')}"
            result = api_fetch(TINYBIRD_API_URL, headers)

            current_deployment = result.get("deployment")
            if current_deployment.get("status") == "deleted":
                click.echo(FeedbackManager.success(message="Discard process successfully completed"))
                break
            time.sleep(5)


def create_deployment(
    project: Project,
    client: TinyB,
    config: Dict[str, Any],
    wait: bool,
    auto: bool,
    verbose: bool = False,
    check: Optional[bool] = None,
    allow_destructive_operations: Optional[bool] = None,
    ingest_hint: Optional[bool] = True,
) -> None:
    # TODO: This code is duplicated in build_server.py
    # Should be refactored to be shared
    MULTIPART_BOUNDARY_DATA_PROJECT = "data_project://"
    DATAFILE_TYPE_TO_CONTENT_TYPE = {
        ".datasource": "text/plain",
        ".pipe": "text/plain",
        ".connection": "text/plain",
    }

    TINYBIRD_API_URL = f"{client.host}/v1/deploy"
    TINYBIRD_API_KEY = client.token

    if project.has_deeper_level():
        click.echo(
            FeedbackManager.warning(
                message="\nYour project contains directories nested deeper than the default scan depth (max_depth=3). "
                "Files in these deeper directories will not be processed. "
                "To include all nested directories, run `tb --max-depth <depth> <cmd>` with a higher depth value."
            )
        )

    files = [
        ("context://", ("cli-version", "1.0.0", "text/plain")),
    ]
    for file_path in project.get_project_files():
        relative_path = Path(file_path).relative_to(project.path).as_posix()
        with open(file_path, "rb") as fd:
            content_type = DATAFILE_TYPE_TO_CONTENT_TYPE.get(Path(file_path).suffix, "application/unknown")
            files.append((MULTIPART_BOUNDARY_DATA_PROJECT, (relative_path, fd.read().decode("utf-8"), content_type)))

    deployment = None
    try:
        HEADERS = {"Authorization": f"Bearer {TINYBIRD_API_KEY}"}
        params = {}
        if check:
            click.echo(FeedbackManager.highlight(message="\n» Validating deployment...\n"))
            params["check"] = "true"
        if allow_destructive_operations:
            params["allow_destructive_operations"] = "true"

        result = api_post(TINYBIRD_API_URL, headers=HEADERS, files=files, params=params)

        print_changes(result, project)

        deployment = result.get("deployment", {})
        feedback = deployment.get("feedback", [])
        for f in feedback:
            if f.get("level", "").upper() == "ERROR":
                feedback_func = FeedbackManager.error
                feedback_icon = ""
            elif f.get("level", "").upper() == "WARNING":
                feedback_func = FeedbackManager.warning
                feedback_icon = "△ "
            elif verbose and f.get("level", "").upper() == "INFO":
                feedback_func = FeedbackManager.info
                feedback_icon = ""
            else:
                feedback_func = None
            resource = f.get("resource")
            resource_bit = f"{resource}: " if resource else ""
            if feedback_func is not None:
                click.echo(feedback_func(message=f"{feedback_icon}{f.get('level')}: {resource_bit}{f.get('message')}"))

        deploy_errors = deployment.get("errors")
        for deploy_error in deploy_errors:
            if deploy_error.get("filename", None):
                click.echo(
                    FeedbackManager.error(message=f"{deploy_error.get('filename')}\n\n{deploy_error.get('error')}")
                )
            else:
                click.echo(FeedbackManager.error(message=f"{deploy_error.get('error')}"))
        click.echo("")  # For spacing

        status = result.get("result")
        if check:
            if status == "success":
                click.echo(FeedbackManager.success(message="\n✓ Deployment is valid"))
                sys.exit(0)
            elif status == "no_changes":
                sys.exit(0)

            click.echo(FeedbackManager.error(message="\n✗ Deployment is not valid"))
            sys_exit(
                "deployment_error",
                f"Deployment is not valid: {str(deployment.get('errors') + deployment.get('feedback', []))}",
            )

        status = result.get("result")
        if status == "success":
            host = get_display_cloud_host(client.host)
            click.echo(
                FeedbackManager.info(message="Deployment URL: ")
                + f"{bcolors.UNDERLINE}{host}/{config.get('name')}/deployments/{deployment.get('id')}{bcolors.ENDC}"
            )

            if wait:
                click.echo(FeedbackManager.info(message="\n* Deployment submitted"))
            else:
                click.echo(FeedbackManager.success(message="\n✓ Deployment submitted successfully"))
        elif status == "no_changes":
            click.echo(FeedbackManager.warning(message="△ Not deploying. No changes."))
            sys.exit(0)
        elif status == "failed":
            click.echo(FeedbackManager.error(message="Deployment failed"))
            sys_exit(
                "deployment_error",
                f"Deployment failed. Errors: {str(deployment.get('errors') + deployment.get('feedback', []))}",
            )
        else:
            click.echo(FeedbackManager.error(message=f"Unknown deployment result {status}"))
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=e))

        if not deployment and not check:
            sys_exit("deployment_error", "Deployment failed")

    if deployment and wait and not check:
        click.echo(FeedbackManager.highlight(message="» Waiting for deployment to be ready..."))
        while True:
            url = f"{client.host}/v1/deployments/{deployment.get('id')}"
            res = api_fetch(url, HEADERS)
            deployment = res.get("deployment")
            if not deployment:
                click.echo(FeedbackManager.error(message="Error parsing deployment from response"))
                sys_exit("deployment_error", "Error parsing deployment from response")
            if deployment.get("status") == "failed":
                click.echo(FeedbackManager.error(message="Deployment failed"))
                deploy_errors = deployment.get("errors")
                for deploy_error in deploy_errors:
                    click.echo(FeedbackManager.error(message=f"* {deploy_error}"))

                if auto:
                    click.echo(FeedbackManager.error(message="Rolling back deployment"))
                    discard_deployment(client.host, HEADERS, wait=wait)
                sys_exit(
                    "deployment_error",
                    f"Deployment failed. Errors: {str(deployment.get('errors') + deployment.get('feedback', []))}",
                )

            if deployment.get("status") == "data_ready":
                break

            if deployment.get("status") in ["deleting", "deleted"]:
                click.echo(FeedbackManager.error(message="Deployment was deleted by another process"))
                sys_exit("deployment_error", "Deployment was deleted by another process")

            time.sleep(5)

        click.echo(FeedbackManager.info(message="✓ Deployment is ready"))

        if auto:
            promote_deployment(client.host, HEADERS, wait=wait, ingest_hint=ingest_hint)


def _build_data_movement_message(kind: str, source_mv_name: Optional[str]) -> str:
    if kind == "backfill_with_mv_queries":
        return f"Using Materialized Pipe {source_mv_name or ''}"
    elif kind == "backfill_with_forward_query":
        return "From live deployment using Forward Query"
    else:
        return ""


def print_changes(result: dict, project: Project) -> None:
    deployment = result.get("deployment", {})
    resources_columns = ["status", "name", "type", "path"]
    resources: list[list[Union[str, None]]] = []
    tokens_columns = ["Change", "Token name", "Added permissions", "Removed permissions"]
    tokens: list[Tuple[str, str, str, str]] = []
    data_movements_columns = ["Datasource", "Backfill type"]
    data_movements = deployment.get("data_movements")
    if data_movements is not None:
        data_movements = [
            (
                dm.get("datasource_name"),
                _build_data_movement_message(dm.get("kind"), dm.get("source_mv_name")),
            )
            for dm in data_movements
        ]

    for ds in deployment.get("new_datasource_names", []):
        resources.append(["new", ds, "datasource", project.get_resource_path(ds, "datasource")])

    for p in deployment.get("new_pipe_names", []):
        path = project.get_resource_path(p, "pipe")
        pipe_type = project.get_pipe_type(path)
        resources.append(["new", p, pipe_type, path])

    for dc in deployment.get("new_data_connector_names", []):
        resources.append(["new", dc, "connection", project.get_resource_path(dc, "connection")])

    for ds in deployment.get("changed_datasource_names", []):
        resources.append(["modified", ds, "datasource", project.get_resource_path(ds, "datasource")])

    for p in deployment.get("changed_pipe_names", []):
        path = project.get_resource_path(p, "pipe")
        pipe_type = project.get_pipe_type(path)
        resources.append(["modified", p, pipe_type, path])

    for dc in deployment.get("changed_data_connector_names", []):
        resources.append(["modified", dc, "connection", project.get_resource_path(dc, "connection")])

    for ds in deployment.get("disconnected_data_source_names", []):
        resources.append(["modified", ds, "datasource", project.get_resource_path(ds, "datasource")])

    for ds in deployment.get("deleted_datasource_names", []):
        resources.append(["deleted", ds, "datasource", project.get_resource_path(ds, "datasource")])

    for p in deployment.get("deleted_pipe_names", []):
        path = project.get_resource_path(p, "pipe")
        pipe_type = project.get_pipe_type(path)
        resources.append(["deleted", p, pipe_type, path])

    for dc in deployment.get("deleted_data_connector_names", []):
        resources.append(["deleted", dc, "connection", project.get_resource_path(dc, "connection")])

    for token_change in deployment.get("token_changes", []):
        token_name = token_change.get("token_name")
        change_type = token_change.get("change_type")
        added_perms = []
        removed_perms = []
        permission_changes = token_change.get("permission_changes", {})
        for perm in permission_changes.get("added_permissions", []):
            added_perms.append(f"{perm['resource_name']}.{perm['resource_type']}:{perm['permission']}")
        for perm in permission_changes.get("removed_permissions", []):
            removed_perms.append(f"{perm['resource_name']}.{perm['resource_type']}:{perm['permission']}")

        tokens.append((change_type, token_name, "\n".join(added_perms), "\n".join(removed_perms)))

    if resources:
        click.echo(FeedbackManager.info(message="\n* Changes to be deployed:"))
        echo_safe_humanfriendly_tables_format_smart_table(resources, column_names=resources_columns)
    else:
        click.echo(FeedbackManager.gray(message="\n* No changes to be deployed"))
    if tokens:
        click.echo(FeedbackManager.info(message="\n* Changes in tokens to be deployed:"))
        echo_safe_humanfriendly_tables_format_smart_table(tokens, column_names=tokens_columns)
    else:
        click.echo(FeedbackManager.gray(message="* No changes in tokens to be deployed"))
    if data_movements is not None:
        if data_movements:
            click.echo(FeedbackManager.info(message="\n Data that will be copied with this deployment:"))
            echo_safe_humanfriendly_tables_format_smart_table(data_movements, column_names=data_movements_columns)
        else:
            click.echo(FeedbackManager.gray(message="* No data will be copied with this deployment"))
