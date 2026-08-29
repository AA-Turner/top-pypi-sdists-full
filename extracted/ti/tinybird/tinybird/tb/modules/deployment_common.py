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
    echo_json,
    echo_safe_humanfriendly_tables_format_smart_table,
    get_display_cloud_host,
    sys_exit,
)
from tinybird.tb.modules.feedback_manager import FeedbackManager, bcolors
from tinybird.tb.modules.job_common import echo_job_url
from tinybird.tb.modules.project import Project


# TODO(eclbg): This should eventually end up in client.py, but we're not using it here yet.
def api_fetch(
    url: str,
    headers: dict,
    max_retries: int = 3,
    backoff_factor: float = 0.5,
    request_from: Optional[str] = None,
) -> dict:
    request_params = {"from": request_from} if request_from and "from=" not in url else None
    retries = 0
    while retries <= max_retries:
        try:
            r = requests.get(url, headers=headers, params=request_params)
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
    request_from: Optional[str] = None,
) -> dict:
    request_params = dict(params or {})
    if request_from and "from=" not in url:
        request_params.setdefault("from", request_from)

    r = requests.post(url, headers=headers, files=files, params=request_params)
    try:
        if r.status_code < 300:
            logging.debug(json.dumps(r.json(), indent=2))
            return r.json()
    except json.JSONDecodeError:
        message = "Error parsing response from API"
        click.echo(FeedbackManager.error(message=message))
        sys_exit("deployment_error", message)

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


def _get_migrate_to_forward_error_message(result: dict[str, Any]) -> str:
    error = result.get("error")
    if error:
        return str(error)

    deployment = result.get("deployment") or {}
    deployment_errors = deployment.get("errors") or []
    error_messages = [
        str(item.get("error")) for item in deployment_errors if isinstance(item, dict) and item.get("error")
    ]
    if error_messages:
        return "; ".join(error_messages)

    return "Migration to Tinybird Forward failed"


def _is_first_deployment_with_seed_live(host: Optional[str], headers: dict) -> bool:
    """Best-effort check for first real deployment when seed deployment (id=0) is still live."""
    try:
        return _get_current_live_deployment_id(host, headers) == "0"
    except Exception:
        logging.exception("Error checking for live seed deployment while deciding first-deployment hint")
        return False


def _list_deployments(host: Optional[str], headers: dict) -> list[dict]:
    """Fetch the current deployments. Raises if the lookup fails."""
    response = requests.get(f"{host}/v1/deployments", headers=headers)
    response.raise_for_status()

    result = response.json()
    logging.debug(json.dumps(result, indent=2))
    return result.get("deployments") or []


def _get_current_live_deployment_id(host: Optional[str], headers: dict) -> Optional[str]:
    deployments = _list_deployments(host, headers)
    if not deployments:
        return None

    live_deployment = next((deployment for deployment in deployments if deployment.get("live")), deployments[0])
    live_id = live_deployment.get("id")
    return str(live_id) if live_id is not None else None


def _get_lingering_old_deployment_id(host: Optional[str], headers: dict, new_deployment_id: str) -> Optional[str]:
    """Look up a still-active deployment other than `new_deployment_id`, if any."""
    deployments = _list_deployments(host, headers)
    other_deployment = next((d for d in deployments if str(d.get("id")) != new_deployment_id), None)
    return str(other_deployment["id"]) if other_deployment else None


def _wait_for_deployment_deletion(
    host: Optional[str],
    headers: dict,
    deployment_id: str,
    request_from: Optional[str] = None,
    poll_interval: int = 5,
) -> bool:  # whether the deployment has been deleted successfully
    url = f"{host}/v1/deployments/{deployment_id}"
    while True:
        result = api_fetch(url, headers, request_from=request_from)
        old_deployment = result.get("deployment")
        if not old_deployment or old_deployment.get("status") == "deleted":
            return True
        if old_deployment.get("status") == "failed":
            return False
        time.sleep(poll_interval)


def _get_deployment_job(client: TinyB, deployment_id: Optional[Union[str, int]]) -> Optional[Dict[str, Any]]:
    if deployment_id is None:
        return None

    try:
        deployment_id = str(deployment_id)
        jobs = client.jobs()
        return next(
            (job for job in jobs if job.get("kind") == "deployment" and str(job.get("deployment_id")) == deployment_id),
            None,
        )
    except Exception:
        return None


def migrate_to_forward_workspace(client: TinyB, output: str = "human", dry_run: bool = False) -> None:
    headers = {"Authorization": f"Bearer {client.token}"}
    params = {"dry_run": dry_run}
    result = api_post(f"{client.host}/v1/migrate-to-forward", headers=headers, params=params)

    if result.get("result") != "success":
        error_message = _get_migrate_to_forward_error_message(result)
        if output == "json":
            echo_json(result)
        else:
            click.echo(FeedbackManager.error(message=error_message))
        sys_exit("deployment_error", error_message)

    if dry_run:
        return

    if output == "json":
        echo_json(result)
        return

    click.echo(FeedbackManager.success(message="✓ Workspace migrated to Tinybird Forward"))


def _should_show_migrate_to_forward_hint(client: TinyB, env: Optional[str]) -> bool:
    if env != "cloud":
        return False

    try:
        client.workspace_info(version="v1")
        return False
    except Exception:
        pass

    try:
        workspace_info = client.workspace_info(version="v0")
    except Exception:
        logging.exception("Error reading workspace info while deciding migrate-to-forward hint")
        return False

    return not workspace_info.get("is_forward", False) and not workspace_info.get("is_branch", False)


# TODO(eclbg): This logic should be in the server, and there should be a dedicated endpoint for promoting a deployment
def promote_deployment(
    host: Optional[str],
    headers: dict,
    wait: bool,
    ingest_hint: Optional[bool] = True,
    request_from: Optional[str] = None,
) -> None:
    TINYBIRD_API_DEPLOYMENTS_BASE_URL = f"{host}/v1/deployments"
    result = api_fetch(TINYBIRD_API_DEPLOYMENTS_BASE_URL, headers, request_from=request_from)

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
        tb_api_set_live_url = f"{TINYBIRD_API_DEPLOYMENTS_BASE_URL}/{candidate_deployment.get('id')}/set-live"
        click.echo(FeedbackManager.highlight(message="» Waiting for deployment to be promoted..."))
        result = api_post(tb_api_set_live_url, headers=headers, request_from=request_from)
        click.echo(FeedbackManager.info(message="✓ Deployment promoted"))

    last_deployment_id = last_deployment.get("id")
    tb_api_last_deployment_url = f"{TINYBIRD_API_DEPLOYMENTS_BASE_URL}/{last_deployment_id}"
    request_params = {"from": request_from} if request_from and "from=" not in tb_api_last_deployment_url else None
    r = requests.delete(tb_api_last_deployment_url, headers=headers, params=request_params)

    result = r.json()
    logging.debug(json.dumps(result, indent=2))
    if result.get("error"):
        click.echo(FeedbackManager.error(message=result.get("error")))
        sys_exit("deployment_error", result.get("error", "Unknown error"))

    is_first_deployment = not (int(last_deployment_id) > 0)

    if not is_first_deployment:
        if not wait:
            click.echo(
                FeedbackManager.highlight(message="» Old deployment removal dispatched. Not waiting for deletion.")
            )
        else:
            click.echo(FeedbackManager.highlight(message="» Removing old deployment..."))

    if wait:
        while True:
            result = api_fetch(tb_api_last_deployment_url, headers=headers, request_from=request_from)

            last_deployment = result.get("deployment")
            if not last_deployment:
                click.echo(FeedbackManager.error(message="Error parsing deployment from response"))
                sys_exit("deployment_error", "Error parsing deployment from response")

            if last_deployment and last_deployment.get("status") == "deleted":
                if not is_first_deployment:
                    click.echo(FeedbackManager.info(message="✓ Old deployment removed"))
                click.echo(FeedbackManager.success(message=f"✓ Deployment #{candidate_deployment.get('id')} is live!"))
                break

            time.sleep(5)
    if is_first_deployment and ingest_hint and len(candidate_deployment.get("new_data_connector_ids", [])) == 0:
        # This is the first deployment, so we prompt the user to ingest data
        click.echo(
            FeedbackManager.info(
                message="Need help ingesting your data? Learn how at https://www.tinybird.co/docs/forward/get-data-in"
            )
        )


def discard_deployment(host: Optional[str], headers: dict, wait: bool, request_from: Optional[str] = None) -> None:
    TINYBIRD_API_URL = f"{host}/v1/deployments"
    result = api_fetch(TINYBIRD_API_URL, headers=headers, request_from=request_from)

    deployments = result.get("deployments")
    if not deployments:
        click.echo(FeedbackManager.error(message="No deployments found"))
        return

    if len(deployments) < 2:
        click.echo(FeedbackManager.error(message="Only one deployment found. Cannot discard the only deployment."))
        return

    current_deployment, deployment_to_discard = deployments[0], deployments[1]

    # NOTE(eclbg): we never get here. We wrote this code when we though we'd enable promoting back and forth between
    # staging and live, but the current CLI commands don't allow getting in that state
    if current_deployment.get("status") != "data_ready":
        click.echo(FeedbackManager.error(message="Previous deployment is not ready"))
        deploy_errors = current_deployment.get("errors", [])
        for deploy_error in deploy_errors:
            click.echo(FeedbackManager.error(message=f"* {deploy_error}"))
        return

    to_discard_status = deployment_to_discard.get("status")
    verb = "Canceling" if to_discard_status in {"calculating", "creating_schema", "schema_ready"} else "Removing"
    click.echo(FeedbackManager.success(message=f"{verb} deployment {deployment_to_discard['id']}"))

    TINYBIRD_API_URL = f"{host}/v1/deployments/{deployment_to_discard.get('id')}"
    request_params = {"from": request_from} if request_from and "from=" not in TINYBIRD_API_URL else None
    r = requests.delete(TINYBIRD_API_URL, headers=headers, params=request_params)
    result = r.json()
    logging.debug(json.dumps(result, indent=2))
    if result.get("error"):
        click.echo(FeedbackManager.error(message=result.get("error")))
        sys_exit("deployment_error", result.get("error", "Unknown error"))

    deployment_to_discard = deployments[1]
    click.echo(FeedbackManager.success(message="Discard process successfully started"))

    if wait:
        while True:
            TINYBIRD_API_URL = f"{host}/v1/deployments/{deployment_to_discard.get('id')}"
            result = api_fetch(TINYBIRD_API_URL, headers, request_from=request_from)

            deployment_to_discard = result.get("deployment")
            if deployment_to_discard and deployment_to_discard.get("status") == "deleted":
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
    show_migrate_to_forward_hint: bool = True,
    output: Optional[str] = "human",
    env: Optional[str] = "cloud",
    return_check_result: bool = False,
    validate_forward_workspace: bool = True,
    is_classic_migration: bool = False,
) -> Optional[Dict[str, Any]]:
    # TODO: This code is duplicated in build_server.py
    # Should be refactored to be shared
    MULTIPART_BOUNDARY_DATA_PROJECT = "data_project://"
    MULTIPART_BOUNDARY_DATA_PROJECT_VENDORED = "data_project_vendored://"
    DATAFILE_TYPE_TO_CONTENT_TYPE = {
        ".datasource": "text/plain",
        ".pipe": "text/plain",
        ".connection": "text/plain",
    }

    TINYBIRD_API_DEPLOY_ENDPOINT_URL = f"{client.host}/v1/deploy"
    TINYBIRD_API_KEY = client.token

    if project.has_deeper_level():
        click.echo(
            FeedbackManager.warning(
                message=f"\nYour project contains directories nested deeper than the used scan depth (max_depth={project.max_depth}). "
                "Files in these deeper directories will not be processed. "
                f"If you have tinybird files in directories deeper than {project.max_depth} levels, you can use "
                "`tb --max-depth <depth> <cmd>` with a higher depth value. "
                "Otherwise you can ignore this warning."
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
    for file_path in project.get_vendored_files():
        relative_path = Path(file_path).relative_to(project.path).as_posix()
        with open(file_path, "rb") as fd:
            content_type = DATAFILE_TYPE_TO_CONTENT_TYPE.get(Path(file_path).suffix, "application/unknown")
            files.append(
                (MULTIPART_BOUNDARY_DATA_PROJECT_VENDORED, (relative_path, fd.read().decode("utf-8"), content_type))
            )

    deployment_job: Optional[Dict[str, Any]] = None
    deployment_request_sent = False
    deployment = {}
    HEADERS = {"Authorization": f"Bearer {TINYBIRD_API_KEY}"}
    request_from = getattr(client, "request_from", None)
    try:
        params = {}
        if check:
            click.echo(FeedbackManager.highlight(message="\n» Validating deployment...\n"))
            params["check"] = "true"
        elif auto:
            params["auto_promote"] = "true"
        if allow_destructive_operations:
            params["allow_destructive_operations"] = "true"
        if not validate_forward_workspace:
            params["validate_forward_workspace"] = "false"
        if is_classic_migration:
            params["is_classic_migration"] = "true"

        deployment_request_sent = True
        result = api_post(
            TINYBIRD_API_DEPLOY_ENDPOINT_URL, headers=HEADERS, files=files, params=params, request_from=request_from
        )

        print_changes(result, project, output)

        deployment = result.get("deployment", {})
        if not deployment:
            click.echo(FeedbackManager.error_exception(error="Failed to parse response from API"))
            sys_exit("deployment_error", "Failed to parse deployment from API response")

        if output == "json" and check:
            echo_json(deployment, indent=8)

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
            if status in {"success", "no_changes"}:
                if status == "success":
                    click.echo(FeedbackManager.success(message="\n✓ Deployment is valid"))

                if (
                    output == "human"
                    and show_migrate_to_forward_hint
                    and _should_show_migrate_to_forward_hint(client, env)
                ):
                    click.echo(
                        FeedbackManager.info(
                            message=(
                                "You can now migrate this Tinybird Classic workspace to Forward "
                                "with `tb migrate-to-forward`."
                            )
                        )
                    )

                if return_check_result:
                    return {"status": status, "deployment": deployment}

                sys.exit(0)

            click.echo(FeedbackManager.error(message="\n✗ Deployment is not valid"))
            sys_exit(
                "deployment_error",
                f"Deployment is not valid: {str(deployment.get('errors') + deployment.get('feedback', []))}",
            )

        host = get_display_cloud_host(client.host)
        if status in ["success", "failed"]:
            click.echo(
                FeedbackManager.gray(message="Deployment URL: ")
                + f"{bcolors.UNDERLINE}{host}/{config.get('name')}/deployments/{deployment.get('id')}{bcolors.ENDC}"
            )
            deployment_job = _get_deployment_job(client, deployment.get("id"))
            if deployment_job:
                echo_job_url(
                    token=client.token,
                    host=client.host,
                    workspace_name=config.get("name") or "",
                    job_url=deployment_job.get("job_url") or "",
                )

        if status == "success":
            autopromote_frag = (
                " It will be auto-promoted when ready." if auto else " It won't be auto-promoted when ready."
            )
            if wait:
                message = "\n* Deployment submitted." + autopromote_frag
                click.echo(FeedbackManager.info(message=message))
            else:
                message = "\n✓ Deployment submitted successfully." + autopromote_frag
                click.echo(FeedbackManager.success(message=message))
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

        if check:
            sys_exit("deployment_error", "Deployment check failed")

        if not deployment:
            sys_exit("deployment_error", "Deployment failed")
    except KeyboardInterrupt:
        if deployment_request_sent and not check:
            click.echo(
                FeedbackManager.warning(
                    message=f"\nDeployment request might have reached the server. Check with `tb --{env} deployment ls`. You can cancel an ongoing deployment with `tb --{env} deployment discard`."
                )
            )
        raise click.Abort()

    if not wait:
        if output == "json" and deployment:
            echo_json(deployment, 8)
        sys.exit(0)

    click.echo(FeedbackManager.highlight(message="» Waiting for deployment to be ready..."))
    waiting_auto_promote = False
    is_first_deployment = str(deployment.get("id")) == "1"
    times_seen_failed = 0
    poll_interval = 5
    try:
        while True:
            url = f"{client.host}/v1/deployments/{deployment.get('id')}"
            res = api_fetch(url, HEADERS, request_from=request_from)
            deployment = res.get("deployment", {})
            if not deployment:
                click.echo(FeedbackManager.error(message="Error parsing deployment from response"))
                sys_exit("deployment_error", "Error parsing deployment from response")
                return None

            status = deployment.get("status")
            errors = deployment.get("errors")
            feedback = deployment.get("feedback")

            if status == "failed":
                times_seen_failed += 1
                # See if it's stuck in failed, otherwise just wait until we see deleting or deleted
                if times_seen_failed > 60:  # 5s * 60 = 5mins
                    message = (
                        "Deployment failed to create and didn't start deleting automatically after 5 minutes. "
                        "You might need to delete it manually in the UI."
                    )
                    click.echo(FeedbackManager.warning(message=message))
                    sys_exit("deployment_error", "Deployment failed and wasn't deleted automatically")
                time.sleep(poll_interval)
                continue

            if status == "data_ready":
                if auto and not deployment.get("live"):
                    if not waiting_auto_promote:
                        click.echo(FeedbackManager.info(message="✓ Deployment is ready"))
                        click.echo(FeedbackManager.highlight(message="» Waiting for deployment to be promoted..."))
                        if not is_first_deployment:
                            is_first_deployment = _is_first_deployment_with_seed_live(client.host, HEADERS)
                        waiting_auto_promote = True
                    time.sleep(poll_interval)
                    continue
                break

            if status in ["deleting", "deleted"]:
                errors = deployment.get("errors")
                if errors:
                    verb = "is being" if status == "deleting" else "was"
                    click.echo(
                        FeedbackManager.error(
                            message=f"Deployment failed and {verb} deleted automatically. Deployment errors:"
                        )
                    )
                    for error in errors:
                        click.echo(FeedbackManager.error(message=f"* {error}"))
                sys_exit(
                    "deployment_error",
                    f"Deployment deleted after failure. Errors: {str(errors + (feedback or []))}",
                )

            time.sleep(poll_interval)

    except KeyboardInterrupt:
        should_cancel = True
        try:
            prompt = "\nYour deployment is in progress. Do you want to cancel the deployment? If not, it will continue even after exiting this command"
            should_cancel = click.confirm(FeedbackManager.warning(message=prompt), default=True, show_default=True)
        except (KeyboardInterrupt, click.Abort):
            # A second Ctrl+C is interpreted as confirming cancellation.
            pass

        if not should_cancel:
            click.echo(FeedbackManager.info(message="Deployment not canceled. Exiting"))
            sys.exit(0)

        click.echo(FeedbackManager.warning(message="Canceling deployment"))
        cancel_url = f"{client.host}/v1/deployments/{deployment.get('id')}"
        r = requests.delete(cancel_url, headers=HEADERS)
        result = r.json()
        logging.debug(json.dumps(result, indent=2))
        if result.get("error"):
            click.echo(FeedbackManager.error(message="Failed to cancel deployment: " + result.get("error")))
            sys_exit("deployment_error", result.get("error", "Unknown error"))

        click.echo(FeedbackManager.success(message="Deployment canceled. It will be deleted evenutally."))

        raise click.Abort()

    # We get here when wait is True, after we've finished polling
    if auto:
        if not waiting_auto_promote:
            click.echo(FeedbackManager.info(message="✓ Deployment is ready"))
            click.echo(FeedbackManager.highlight(message="» Waiting for deployment to be promoted..."))
        click.echo(FeedbackManager.info(message="✓ Deployment promoted"))
        click.echo(FeedbackManager.success(message=f"✓ Deployment #{deployment.get('id')} is live!"))

        old_deployment_id: Optional[str] = None
        try:
            old_deployment_id = _get_lingering_old_deployment_id(client.host, HEADERS, str(deployment.get("id")))
        except Exception:
            click.echo(
                FeedbackManager.warning(
                    message="Could not confirm if there's a previous deployment to remove. "
                    f"If a follow-up `tb deploy` reports one already in progress, check `tb --{env} deployment ls`."
                )
            )

        if old_deployment_id:
            click.echo(FeedbackManager.highlight(message="» Removing old deployment..."))
            try:
                deleted = _wait_for_deployment_deletion(
                    client.host, HEADERS, old_deployment_id, request_from=request_from
                )
            except KeyboardInterrupt:
                click.echo(
                    FeedbackManager.warning(
                        message=f"\nDeployment is live, but the old deployment is still being removed. "
                        f"Check its status with `tb --{env} deployment ls`."
                    )
                )
                raise click.Abort()
            if deleted:
                click.echo(FeedbackManager.info(message="✓ Old deployment removed"))
            else:
                click.echo(
                    FeedbackManager.warning(
                        message="Deployment is live, but the old deployment failed to be removed. "
                        f"Check its status with `tb --{env} deployment ls`."
                    )
                )

        if ingest_hint and len(deployment.get("new_data_connector_ids", [])) == 0 and is_first_deployment:
            click.echo(
                FeedbackManager.info(
                    message="Need help ingesting your data? Learn how at https://www.tinybird.co/docs/forward/get-data-in"
                )
            )
    else:
        click.echo(FeedbackManager.info(message="✓ Deployment is ready"))

    # Output JSON at the appropriate time based on the execution path
    if output == "json" and deployment:
        echo_json(deployment, 8)

    return None


def _build_data_movement_message(kind: str, source_mv_name: Optional[str]) -> str:
    if kind == "backfill_with_mv_queries":
        return f"Using Materialized Pipe {source_mv_name or ''}"
    elif kind == "backfill_with_forward_query":
        return "From live deployment using Forward Query"
    else:
        return ""


def print_changes(result: dict, project: Project, output: Optional[str] = "human") -> None:
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

    resources.extend(
        ["new", ds, "datasource", project.get_resource_path(ds, "datasource")]
        for ds in deployment.get("new_datasource_names", [])
    )

    for p in deployment.get("new_pipe_names", []):
        path = project.get_resource_path(p, "pipe")
        pipe_type = project.get_pipe_type(path)
        resources.append(["new", p, pipe_type, path])

    resources.extend(
        ["new", dc, "connection", project.get_resource_path(dc, "connection")]
        for dc in deployment.get("new_data_connector_names", [])
    )

    resources.extend(
        ["modified", ds, "datasource", project.get_resource_path(ds, "datasource")]
        for ds in deployment.get("changed_datasource_names", [])
    )

    for p in deployment.get("changed_pipe_names", []):
        path = project.get_resource_path(p, "pipe")
        pipe_type = project.get_pipe_type(path)
        resources.append(["modified", p, pipe_type, path])

    resources.extend(
        ["modified", dc, "connection", project.get_resource_path(dc, "connection")]
        for dc in deployment.get("changed_data_connector_names", [])
    )

    resources.extend(
        ["modified", ds, "datasource", project.get_resource_path(ds, "datasource")]
        for ds in deployment.get("disconnected_data_source_names", [])
    )

    resources.extend(
        ["deleted", ds, "datasource", project.get_resource_path(ds, "datasource")]
        for ds in deployment.get("deleted_datasource_names", [])
    )

    for p in deployment.get("deleted_pipe_names", []):
        path = project.get_resource_path(p, "pipe")
        pipe_type = project.get_pipe_type(path)
        resources.append(["deleted", p, pipe_type, path])

    resources.extend(
        ["deleted", dc, "connection", project.get_resource_path(dc, "connection")]
        for dc in deployment.get("deleted_data_connector_names", [])
    )

    for token_change in deployment.get("token_changes", []):
        token_name = token_change.get("token_name")
        change_type = token_change.get("change_type")
        permission_changes = token_change.get("permission_changes", {})
        added_perms = [
            f"{perm['resource_name']}.{perm['resource_type']}:{perm['permission']}"
            for perm in permission_changes.get("added_permissions", [])
        ]
        removed_perms = [
            f"{perm['resource_name']}.{perm['resource_type']}:{perm['permission']}"
            for perm in permission_changes.get("removed_permissions", [])
        ]

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
