# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tools for GitHub workflow and Docker operations.

This module provides MCP tools for checking GitHub Actions workflow status,
Docker image availability, and other related operations.

## MCP reference

.. include:: ../../../docs/mcp-generated/github_actions.md
    :start-line: 2
"""

from __future__ import annotations

__all__: list[str] = []

import re
from typing import Annotated

import requests
from fastmcp import FastMCP
from fastmcp_extensions import mcp_tool, register_mcp_tools
from pydantic import BaseModel, Field

from airbyte_ops_mcp.github_actions import (
    get_workflow_jobs,
    resolve_default_workflow_branch,
    trigger_workflow_dispatch,
)
from airbyte_ops_mcp.github_api import (
    GITHUB_API_BASE,
    get_pr_head_ref,
    resolve_ci_trigger_github_token,
)

DOCKERHUB_API_BASE = "https://hub.docker.com/v2"


class JobInfo(BaseModel):
    """Information about a single job in a workflow run."""

    job_id: int
    name: str
    status: str
    conclusion: str | None = None
    started_at: str | None = None
    completed_at: str | None = None


class WorkflowRunStatus(BaseModel):
    """Response model for check_ci_workflow_status MCP tool."""

    run_id: int
    status: str
    conclusion: str | None
    workflow_name: str
    head_branch: str
    head_sha: str
    html_url: str
    created_at: str
    updated_at: str
    run_started_at: str | None = None
    jobs_url: str
    jobs: list[JobInfo] = []


def _parse_workflow_url(url: str) -> tuple[str, str, int]:
    """Parse a GitHub Actions workflow run URL into components.

    Args:
        url: GitHub Actions workflow run URL
            (e.g., "https://github.com/owner/repo/actions/runs/12345")

    Returns:
        Tuple of (owner, repo, run_id)

    Raises:
        ValueError: If URL format is invalid.
    """
    pattern = r"https://github\.com/([^/]+)/([^/]+)/actions/runs/(\d+)"
    match = re.match(pattern, url)
    if not match:
        raise ValueError(
            f"Invalid workflow URL format: {url}. "
            "Expected format: https://github.com/owner/repo/actions/runs/12345"
        )
    return match.group(1), match.group(2), int(match.group(3))


def _get_workflow_run(
    owner: str,
    repo: str,
    run_id: int,
    token: str,
) -> dict:
    """Get workflow run details from GitHub API.

    Args:
        owner: Repository owner (e.g., "airbytehq")
        repo: Repository name (e.g., "airbyte")
        run_id: Workflow run ID
        token: GitHub API token

    Returns:
        Workflow run data dictionary.

    Raises:
        ValueError: If workflow run not found.
        requests.HTTPError: If API request fails.
    """
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/actions/runs/{run_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code == 404:
        raise ValueError(f"Workflow run {owner}/{repo}/actions/runs/{run_id} not found")
    response.raise_for_status()

    return response.json()


@mcp_tool(
    read_only=True,
    idempotent=True,
    open_world=True,
)
def check_ci_workflow_status(
    workflow_url: Annotated[
        str | None,
        Field(
            description="Full GitHub Actions workflow run URL (e.g., 'https://github.com/owner/repo/actions/runs/12345')"
        ),
    ] = None,
    owner: Annotated[
        str | None,
        Field(description="Repository owner (e.g., 'airbytehq')"),
    ] = None,
    repo: Annotated[
        str | None,
        Field(description="Repository name (e.g., 'airbyte')"),
    ] = None,
    run_id: Annotated[
        int | None,
        Field(description="Workflow run ID"),
    ] = None,
) -> WorkflowRunStatus:
    """Check the status of a GitHub Actions workflow run.

    You can provide either:
    - A full workflow URL (workflow_url parameter), OR
    - The component parts (owner, repo, run_id parameters)

    Returns the current status, conclusion, and other details about the workflow run.

    Uses the CI trigger token (GITHUB_CI_WORKFLOW_TRIGGER_PAT) so that
    workflow runs in private repositories are accessible.
    """
    # Guard: Validate input parameters
    if workflow_url:
        # Parse URL to get components
        owner, repo, run_id = _parse_workflow_url(workflow_url)
    elif owner and repo and run_id:
        # Use provided components
        pass
    else:
        raise ValueError(
            "Must provide either workflow_url OR all of (owner, repo, run_id)"
        )

    # Guard: Check for required token
    # Use the CI trigger token (same as trigger_ci_workflow) so that
    # private-repo workflow runs are accessible.
    token = resolve_ci_trigger_github_token()

    # Get workflow run details
    run_data = _get_workflow_run(owner, repo, run_id, token)

    # Get jobs for the workflow run, passing the same token
    workflow_jobs = get_workflow_jobs(owner, repo, run_id, token=token)

    # Convert dataclass objects to Pydantic models for the response
    jobs = [
        JobInfo(
            job_id=job.job_id,
            name=job.name,
            status=job.status,
            conclusion=job.conclusion,
            started_at=job.started_at,
            completed_at=job.completed_at,
        )
        for job in workflow_jobs
    ]

    return WorkflowRunStatus(
        run_id=run_data["id"],
        status=run_data["status"],
        conclusion=run_data["conclusion"],
        workflow_name=run_data["name"],
        head_branch=run_data["head_branch"],
        head_sha=run_data["head_sha"],
        html_url=run_data["html_url"],
        created_at=run_data["created_at"],
        updated_at=run_data["updated_at"],
        run_started_at=run_data.get("run_started_at"),
        jobs_url=run_data["jobs_url"],
        jobs=jobs,
    )


class TriggerCIWorkflowResult(BaseModel):
    """Response model for trigger_ci_workflow MCP tool."""

    success: bool
    message: str
    workflow_url: str
    run_id: int | None = None
    run_url: str | None = None


@mcp_tool(
    read_only=False,
    idempotent=False,
    open_world=True,
)
def trigger_ci_workflow(
    owner: Annotated[
        str,
        Field(description="Repository owner (e.g., 'airbytehq')"),
    ],
    repo: Annotated[
        str,
        Field(description="Repository name (e.g., 'airbyte')"),
    ],
    workflow_file: Annotated[
        str,
        Field(description="Workflow file name (e.g., 'connector-regression-test.yml')"),
    ],
    workflow_definition_ref: Annotated[
        str | None,
        Field(
            description="Branch name or PR number for the workflow definition to use. "
            "If a PR number (integer string) is provided, it resolves to the PR's head branch name. "
            "If a branch name is provided, it is used directly. "
            "Defaults to 'main' if not specified, "
            "or AIRBYTE_OPS_DEFAULT_WORKFLOW_BRANCH_OVERRIDE when set for local testing."
        ),
    ] = None,
    inputs: Annotated[
        dict[str, str] | None,
        Field(
            description="Workflow inputs as a dictionary of string key-value pairs. "
            "These are passed to the workflow_dispatch event."
        ),
    ] = None,
) -> TriggerCIWorkflowResult:
    """Trigger a GitHub Actions CI workflow via workflow_dispatch.

    This tool triggers a workflow in any GitHub repository that has workflow_dispatch
    enabled. It resolves PR numbers to branch names automatically since GitHub's
    workflow_dispatch API only accepts branch names, not refs/pull/{pr}/head format.

    Requires GITHUB_CI_WORKFLOW_TRIGGER_PAT or GITHUB_TOKEN environment variable
    with 'actions:write' permission.
    """
    # Guard: Check for required token
    token = resolve_ci_trigger_github_token()

    if workflow_definition_ref:
        if workflow_definition_ref.isdigit():
            pr_head_info = get_pr_head_ref(
                owner,
                repo,
                int(workflow_definition_ref),
                token,
            )
            resolved_ref = pr_head_info.ref
        else:
            resolved_ref = workflow_definition_ref
    else:
        resolved_ref = resolve_default_workflow_branch("main")

    # Trigger the workflow
    result = trigger_workflow_dispatch(
        owner=owner,
        repo=repo,
        workflow_file=workflow_file,
        ref=resolved_ref,
        inputs=inputs or {},
        token=token,
        find_run=True,
    )

    # Build response message
    if result.run_id:
        message = f"Successfully triggered workflow {workflow_file} on {owner}/{repo} (ref: {resolved_ref}). Run ID: {result.run_id}"
    else:
        message = f"Successfully triggered workflow {workflow_file} on {owner}/{repo} (ref: {resolved_ref}). Run ID not yet available."

    return TriggerCIWorkflowResult(
        success=True,
        message=message,
        workflow_url=result.workflow_url,
        run_id=result.run_id,
        run_url=result.run_url,
    )


class DockerImageInfo(BaseModel):
    """Response model for get_docker_image_info MCP tool."""

    exists: bool
    image: str
    tag: str
    full_name: str
    digest: str | None = None
    last_updated: str | None = None
    size_bytes: int | None = None
    architecture: str | None = None
    os: str | None = None


def _check_dockerhub_image(
    image: str,
    tag: str,
) -> dict | None:
    """Check if a Docker image tag exists on DockerHub.

    Args:
        image: Docker image name (e.g., "airbyte/source-github")
        tag: Image tag (e.g., "2.1.5-preview.abc1234")

    Returns:
        Tag data dictionary if found, None if not found.
    """
    # DockerHub API endpoint for tag info
    url = f"{DOCKERHUB_API_BASE}/repositories/{image}/tags/{tag}"

    response = requests.get(url, timeout=30)
    if response.status_code == 404:
        return None
    response.raise_for_status()

    return response.json()


@mcp_tool(
    read_only=True,
    idempotent=True,
    open_world=True,
)
def get_docker_image_info(
    image: Annotated[
        str,
        Field(description="Docker image name (e.g., 'airbyte/source-github')"),
    ],
    tag: Annotated[
        str,
        Field(description="Image tag (e.g., '2.1.5-preview.abc1234')"),
    ],
) -> DockerImageInfo:
    """Check if a Docker image exists on DockerHub.

    Returns information about the image if it exists, or indicates if it doesn't exist.
    This is useful for confirming that a pre-release connector was successfully published.
    """
    full_name = f"{image}:{tag}"
    tag_data = _check_dockerhub_image(image, tag)

    if not tag_data:
        return DockerImageInfo(
            exists=False,
            image=image,
            tag=tag,
            full_name=full_name,
        )

    # Extract image details from the first image in the list (if available)
    images = tag_data.get("images", [])
    first_image = images[0] if images else {}

    return DockerImageInfo(
        exists=True,
        image=image,
        tag=tag,
        full_name=full_name,
        digest=tag_data.get("digest"),
        last_updated=tag_data.get("last_updated"),
        size_bytes=first_image.get("size"),
        architecture=first_image.get("architecture"),
        os=first_image.get("os"),
    )


def register_github_actions_tools(app: FastMCP) -> None:
    """Register GitHub Actions tools with the FastMCP app.

    Args:
        app: FastMCP application instance
    """
    register_mcp_tools(app, mcp_module=__name__)
