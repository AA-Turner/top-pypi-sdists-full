# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tools for GitHub operations: CI workflow triggering/status, Docker image info, and issue/PR subscriptions.

## MCP reference

.. include:: ../../../docs/mcp-generated/github_ops.md
    :start-line: 2
"""

from __future__ import annotations

__all__: list[str] = []

import logging
import os
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


logger = logging.getLogger(__name__)

SUBSCRIPTION_API_URL_ENV = "SUBSCRIPTION_API_URL"

SUBSCRIPTION_API_TOKEN_ENV = "SUBSCRIPTION_API_BEARER_TOKEN"


def _get_api_url() -> str:
    """Get the subscription API base URL."""
    url = os.environ.get(SUBSCRIPTION_API_URL_ENV)
    if not url:
        raise ValueError(
            f"{SUBSCRIPTION_API_URL_ENV} environment variable is not set. "
            "Cannot reach the GitHub subscriptions backend."
        )
    return url.rstrip("/")


def _get_api_token() -> str:
    """Get the subscription API bearer token."""
    token = os.environ.get(SUBSCRIPTION_API_TOKEN_ENV)
    if not token:
        raise ValueError(
            f"{SUBSCRIPTION_API_TOKEN_ENV} environment variable is not set. "
            "Cannot authenticate to the GitHub subscriptions backend."
        )
    return token


def _api_headers() -> dict[str, str]:
    """Build headers for API requests."""
    return {
        "Authorization": f"Bearer {_get_api_token()}",
        "Content-Type": "application/json",
    }


class SubscribeResponse(BaseModel):
    """Response from the subscribe_to_github_issue tool."""

    success: bool = Field(
        description="Whether the subscription was created successfully"
    )
    message: str = Field(description="Human-readable status message")
    subscription_id: str | None = Field(
        default=None,
        description="ID of the created or updated subscription",
    )
    github_url: str | None = Field(
        default=None,
        description="GitHub URL being watched",
    )
    expires_at: str | None = Field(
        default=None,
        description="When the subscription expires (ISO 8601)",
    )


class UnsubscribeResponse(BaseModel):
    """Response from the unsubscribe_from_github_issue tool."""

    success: bool = Field(description="Whether the unsubscribe was successful")
    message: str = Field(description="Human-readable status message")
    deleted_count: int = Field(
        default=0,
        description="Number of subscriptions removed",
    )


class ListSubscriptionsResponse(BaseModel):
    """Response from the list_github_subscriptions tool."""

    success: bool = Field(description="Whether the listing was successful")
    message: str = Field(description="Human-readable status message")
    subscriptions: list[dict[str, str]] = Field(
        default_factory=list,
        description="List of active subscriptions with id, github_url, expires_at",
    )


@mcp_tool(
    read_only=False,
    idempotent=True,
    open_world=True,
)
def subscribe_to_github_issue(
    github_url: Annotated[
        str,
        "The GitHub issue or PR URL to subscribe to. "
        "Examples: https://github.com/airbytehq/airbyte/issues/123 "
        "or https://github.com/airbytehq/airbyte/pull/456",
    ],
    agent_session_url: Annotated[
        str,
        "Your Devin session URL so notifications can be delivered back to "
        "your session. Use the session URL from your system prompt.",
    ],
    watch_events: Annotated[
        list[str] | None,
        "Optional list of event types to watch. Valid values: "
        "'comment', 'close', 'merge', 'reopen', 'label', 'synchronize', "
        "'ready_for_review', 'assigned'. Defaults to all events if not specified.",
    ] = None,
    ttl_hours: Annotated[
        int,
        "Number of hours until the subscription expires. Default is 240 (10 days).",
    ] = 240,
    slack_users_cc: Annotated[
        str | None,
        "Optional comma-delimited list of Slack user tags to CC on "
        "notifications. Example: '<@U12345>, <@U67890>'.",
    ] = None,
) -> SubscribeResponse:
    """Subscribe to notifications on a GitHub issue or pull request.

    Creates a subscription that will deliver real-time notifications back
    to your Devin session when activity occurs on the specified GitHub
    issue or PR. Notifications are triggered by GitHub webhooks and
    delivered within seconds.

    If you are already subscribed to the same issue/PR, the subscription
    is updated (TTL extended, watch events merged).

    Use this tool when you need to monitor a GitHub issue or PR for
    changes, new comments, merges, closures, or other activity.
    """
    try:
        api_url = _get_api_url()
        body: dict[str, str | list[str] | int | None] = {
            "github_url": github_url,
            "session_url": agent_session_url,
            "ttl_hours": ttl_hours,
        }
        if watch_events:
            body["watch_events"] = watch_events
        if slack_users_cc:
            body["slack_users_cc"] = slack_users_cc

        response = requests.post(
            f"{api_url}/subscriptions",
            json=body,
            headers=_api_headers(),
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        return SubscribeResponse(
            success=True,
            message=(
                f"Subscribed to {github_url}. "
                f"You will receive notifications in this session until "
                f"{data.get('expires_at', 'expiry unknown')}."
            ),
            subscription_id=data.get("id"),
            github_url=github_url,
            expires_at=data.get("expires_at"),
        )

    except ValueError as e:
        return SubscribeResponse(
            success=False,
            message=f"Configuration error: {e}",
        )
    except requests.RequestException as e:
        logger.exception("Failed to create subscription")
        return SubscribeResponse(
            success=False,
            message=f"Failed to create subscription: {e}",
        )


@mcp_tool(
    read_only=False,
    idempotent=True,
    open_world=True,
)
def unsubscribe_from_github_issue(
    agent_session_url: Annotated[
        str,
        "Your Devin session URL. Use the session URL from your system prompt.",
    ],
    github_url: Annotated[
        str | None,
        "The GitHub issue or PR URL to unsubscribe from. "
        "If not provided, all subscriptions for this session are removed.",
    ] = None,
    subscription_id: Annotated[
        str | None,
        "Optional specific subscription ID to remove. "
        "Use this if you know the exact subscription to cancel.",
    ] = None,
) -> UnsubscribeResponse:
    """Unsubscribe from notifications on a GitHub issue or pull request.

    Removes an active subscription so you will no longer receive
    notifications for the specified issue/PR.

    You can unsubscribe by:
    - Providing a specific subscription_id
    - Providing a github_url + session_url to unsubscribe from that specific issue/PR
    - Providing only session_url to unsubscribe from all issues/PRs
    """
    try:
        api_url = _get_api_url()

        if subscription_id:
            # Delete by ID
            response = requests.delete(
                f"{api_url}/subscriptions/{subscription_id}",
                headers=_api_headers(),
                timeout=10,
            )
        else:
            # Delete by match
            params: dict[str, str] = {"session_url": agent_session_url}
            if github_url:
                params["github_url"] = github_url
            response = requests.delete(
                f"{api_url}/subscriptions",
                params=params,
                headers=_api_headers(),
                timeout=10,
            )

        response.raise_for_status()
        data = response.json()
        count = data.get("deleted_count", 0)

        return UnsubscribeResponse(
            success=True,
            message=f"Removed {count} subscription(s).",
            deleted_count=count,
        )

    except ValueError as e:
        return UnsubscribeResponse(
            success=False,
            message=f"Configuration error: {e}",
        )
    except requests.RequestException as e:
        logger.exception("Failed to unsubscribe")
        return UnsubscribeResponse(
            success=False,
            message=f"Failed to unsubscribe: {e}",
        )


@mcp_tool(
    read_only=True,
    idempotent=True,
    open_world=True,
)
def list_github_subscriptions(
    agent_session_url: Annotated[
        str,
        "Your Devin session URL. Use the session URL from your system prompt.",
    ],
) -> ListSubscriptionsResponse:
    """List all active GitHub issue/PR subscriptions for this session.

    Returns the list of GitHub issues and PRs that this session is
    currently subscribed to, along with their expiry times.
    """
    try:
        api_url = _get_api_url()

        response = requests.get(
            f"{api_url}/subscriptions",
            params={"session_url": agent_session_url},
            headers=_api_headers(),
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        subs = [
            {
                "id": s["id"],
                "github_url": s["github_url"],
                "watch_events": ", ".join(s.get("watch_events", [])),
                "expires_at": s.get("expires_at", "unknown"),
            }
            for s in data
        ]

        if not subs:
            return ListSubscriptionsResponse(
                success=True,
                message="No active subscriptions for this session.",
                subscriptions=[],
            )

        return ListSubscriptionsResponse(
            success=True,
            message=f"Found {len(subs)} active subscription(s).",
            subscriptions=subs,
        )

    except ValueError as e:
        return ListSubscriptionsResponse(
            success=False,
            message=f"Configuration error: {e}",
        )
    except requests.RequestException as e:
        logger.exception("Failed to list subscriptions")
        return ListSubscriptionsResponse(
            success=False,
            message=f"Failed to list subscriptions: {e}",
        )


def register_github_ops_tools(app: FastMCP) -> None:
    """Register github_ops tools with the FastMCP app."""
    register_mcp_tools(app, mcp_module=__name__)
