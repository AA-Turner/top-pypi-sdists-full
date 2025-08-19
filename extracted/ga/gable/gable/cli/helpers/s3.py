"""Helper functions for S3 operations."""

import json
import os
import time
from typing import Tuple

import click
import requests
from loguru import logger

from gable.api.client import GableAPIClient
from gable.cli.helpers.npm import get_installed_package_dir
from gable.cli.helpers.repo_interactions import get_git_repo_info, get_pr_link
from gable.openapi import (
    Action1,
    ErrorResponse,
    OutputFormat,
    PostScaStartRunRequest,
    S3PresignedUrl,
    StaticAnalysisCodeMetadata,
    StaticAnalysisPathsUploadRequest,
    StaticAnalysisToolConfig,
    StaticAnalysisToolMetadata,
)


def start_sca_run(
    client: GableAPIClient,
    project_root: str,
    action: str,
    output: str | None,
    include_unchanged_assets: bool | None,
) -> Tuple[str, S3PresignedUrl]:
    """Call the SCA start run API to get the S3 presigned URL to upload the SCA results

    Args:
        client: The Gable API client
        project_root: The root directory of the project to analyze

    Returns:
        A tuple of (run_id, presigned_url)

    Raises:
        ClickException: If the API call was not successful
    """
    try:
        git_info = get_git_repo_info(project_root)
    except click.ClickException:
        logger.debug(
            f"No git repository found at project root {project_root}, using default values"
        )
        git_info = {
            "gitRemoteOriginHTTPS": "unknown",
            "gitBranch": "unknown",
            "gitHash": "unknown",
        }

    package_name, package_version = get_sca_package_info()
    action_name = Action1.check if action == "check" else Action1.register
    include = True if include_unchanged_assets else False
    output_f = None
    if action_name == "check":
        if output == "markdown":
            output_f = OutputFormat.markdown
        elif output == "text":
            output_f = OutputFormat.text
        else:
            output_f = OutputFormat.json
    # Call the SCA start run API to get the S3 presigned URL to upload the SCA results
    response, success, _status_code = client.post_sca_start_run(
        PostScaStartRunRequest(
            code_info=StaticAnalysisCodeMetadata(
                repo_uri=git_info["gitRemoteOriginHTTPS"],
                repo_branch=git_info["gitBranch"],
                repo_commit=git_info["gitHash"],
                project_root=project_root,
            ),
            sca_info=StaticAnalysisToolMetadata(
                name=package_name,
                version=package_version,
                config=StaticAnalysisToolConfig(
                    ingress_signatures=[],
                    egress_signatures=[],
                ),
            ),
            action=action_name,
            pr_link=get_pr_link(),
            output_format=output_f,
            include_unchanged_assets=include,
        )
    )

    if not success or isinstance(response, ErrorResponse):
        raise click.ClickException(
            f"Error starting static code analysis run: {response.title} - {response.message}"  # type: ignore
        )

    return response.runId, response.s3PresignedUrl  # type: ignore


def get_sca_package_info() -> tuple[str, str]:
    """Get the name and version of the installed @gable-eng/sca package."""
    try:
        package_dir = get_installed_package_dir()
        package_json_path = os.path.join(package_dir, "package.json")
        with open(package_json_path, "r") as f:
            package_data = json.load(f)
            return (package_data.get("name", ""), package_data.get("version", ""))
    except Exception as e:
        logger.debug(f"Error getting SCA package info: {e}")
        return ("", "")


def poll_sca_job_status(
    api_client: GableAPIClient,
    job_id: str,
    timeout_seconds: float = 300,
    interval_seconds: float = 5,
) -> dict:
    """
    Poll the job status until it completes successfully or fails, or until timeout.

    Parameters:
        api_client (GableAPIClient): Client used to fetch job status.
        job_id (str): The ID of the job to check.
        timeout_seconds (float): Max seconds to poll before timing out.
        interval_seconds (float): Seconds to wait between polling attempts.

    Returns:
        dict: The final status response from the API.

    Raises:
        click.ClickException: If the job fails or polling times out.
    """
    start_time = time.time()
    logger.debug(f"Polling job status for job_id: {job_id}")
    poll_until_complete = False if timeout_seconds <= 0 else True
    while True:
        elapsed_time = time.time() - start_time

        if poll_until_complete and elapsed_time > timeout_seconds:
            raise click.ClickException(
                f"Timed out after {timeout_seconds}s waiting for job ID: {job_id}"
            )
        try:
            response, success, _ = api_client.get_sca_run_status(job_id)
        except requests.RequestException as error:
            click.echo(f"[retrying] Error polling job status: {error}", err=True)
            logger.error("Error polling job status: %s, retrying…", error)
            time.sleep(interval_seconds)
            continue
        if not success or isinstance(response, ErrorResponse):
            error_msg = (
                f"Error polling job status for job ID {job_id}: " f"{response.message}"
            )
            logger.error(error_msg)
            raise click.ClickException(error_msg)
        status_data = response.dict()
        job_status = status_data.get("status", "").lower()
        message = status_data.get("message", "")
        click.echo(
            f"[{int(elapsed_time)}s] Status for Job with ID {job_id}: {job_status}"
        )
        click.echo(f"{message}")
        if not poll_until_complete:
            return status_data

        if job_status == "success":
            return status_data

        if job_status == "error":
            error_msg = status_data.get("message", "No error message provided.")
            raise click.ClickException(
                f"Job failed with status '{job_status}': {error_msg}"
            )

        time.sleep(interval_seconds)


def upload_sca_results(
    run_id: str, presigned_url: S3PresignedUrl, results_dir: str
) -> None:
    """Upload SCA results to S3 using the presigned URL.

    Args:
        presigned_url: The S3 presigned URL to upload to
        results_dir: The directory containing the SCA results file
    """
    try:
        logger.debug(
            f'Uploading results from {os.path.join(results_dir, "results.json")}'
        )
        # Read the SCA results file - hardcoded to results.json right now
        with open(os.path.join(results_dir, "results.json"), "rb") as f:
            file_content = f.read()

        results_json = json.loads(file_content)
        results_json["run_id"] = run_id
        results = StaticAnalysisPathsUploadRequest.parse_obj(results_json)

        # Create form data
        files = {
            "file": (
                "results.json",
                results.json(by_alias=True, exclude_none=True).encode("utf-8"),
                "application/octet-stream",
            )
        }
        data = presigned_url.fields
        # Upload to S3 with the complete form data as the body
        response = requests.post(presigned_url.url, files=files, data=data)
        response.raise_for_status()
        logger.debug("Successfully uploaded SCA results to S3")
    except requests.exceptions.HTTPError as e:
        error_msg = f"S3 upload failed with HTTP error: {e.response.text}"
        raise click.ClickException(error_msg)
