"""Helper functions for S3 operations."""
import os
import json
import requests
import click
from loguru import logger
from gable.cli.helpers.npm import get_installed_package_dir
from gable.cli.helpers.repo_interactions import get_git_repo_info
from typing import Tuple
from gable.openapi import (
    PostScaStartRunRequest,
    StaticAnalysisCodeMetadata,
    StaticAnalysisToolMetadata,
    StaticAnalysisToolConfig,
    ErrorResponse,
    S3PresignedUrl,
    StaticAnalysisPathsUploadRequest
)
from gable.api.client import GableAPIClient

def start_sca_run(client: GableAPIClient, project_root: str) -> Tuple[str, S3PresignedUrl]:
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
        logger.debug(f"No git repository found at project root {project_root}, using default values")
        git_info = {
            "gitRemoteOriginHTTPS": "unknown",
            "gitBranch": "unknown",
            "gitHash": "unknown",
        }

    package_name, package_version = get_sca_package_info()

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
            )
        )

    if not success or isinstance(response, ErrorResponse):
        raise click.ClickException(
            f"Error starting static code analysis run: {response.title} - {response.message}"
        )

    return response.runId, response.s3PresignedUrl

def get_sca_package_info() -> tuple[str, str]:
    """Get the name and version of the installed @gable-eng/sca package."""
    try:
        package_dir = get_installed_package_dir()
        package_json_path = os.path.join(package_dir, "package.json")
        with open(package_json_path, "r") as f:
            package_data = json.load(f)
            return (
                package_data.get("name", ""),
                package_data.get("version", "")
            )
    except Exception as e:
        logger.debug(f"Error getting SCA package info: {e}")
        return ("", "")

def upload_sca_results(run_id: str, presigned_url: S3PresignedUrl, results_dir: str) -> None:
    """Upload SCA results to S3 using the presigned URL.
    
    Args:
        presigned_url: The S3 presigned URL to upload to
        results_dir: The directory containing the SCA results file
    """
    try:
        logger.debug(f'Uploading results from {os.path.join(results_dir, "results.json")}')
        # Read the SCA results file - hardcoded to results.json right now
        with open(os.path.join(results_dir, "results.json"), "rb") as f:
            file_content = f.read()

        results_json = json.loads(file_content)
        results_json["run_id"] = run_id

        results = StaticAnalysisPathsUploadRequest.parse_obj(results_json)

        # Create form data
        files = {'file': ('results.json', results.json(by_alias=True, exclude_none=True).encode('utf-8'), 'application/octet-stream')}
        data = presigned_url.fields

        # Upload to S3 with the complete form data as the body
        response = requests.post(
            presigned_url.url,
            files=files,
            data=data
        )
        response.raise_for_status()
        logger.debug("Successfully uploaded SCA results to S3")
    except requests.exceptions.HTTPError as e:
        error_msg = f"S3 upload failed with HTTP error: {e.response.text}"
        raise click.ClickException(error_msg)