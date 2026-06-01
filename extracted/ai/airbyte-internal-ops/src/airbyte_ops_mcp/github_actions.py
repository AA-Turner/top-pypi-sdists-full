# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""GitHub Actions API utilities.

This module provides utilities for interacting with GitHub Actions workflows,
including workflow dispatch, run discovery, and job status. These utilities
are used by MCP tools but are not MCP-specific.

For general GitHub API utilities (authentication, PR info, file contents),
see the github_api module.
"""

from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass
from datetime import datetime, timedelta

import requests

from airbyte_ops_mcp.github_api import (
    GITHUB_API_BASE,
    resolve_ci_trigger_github_token,
)

logger = logging.getLogger(__name__)

DEFAULT_WORKFLOW_BRANCH_OVERRIDE_ENV = "AIRBYTE_OPS_DEFAULT_WORKFLOW_BRANCH_OVERRIDE"


def resolve_default_workflow_branch(default_branch: str) -> str:
    """Return the default workflow branch, honoring the local testing override."""
    override = os.getenv(DEFAULT_WORKFLOW_BRANCH_OVERRIDE_ENV, "").strip()
    if override:
        logger.warning(
            "Using %s=%r instead of default workflow branch %r.",
            DEFAULT_WORKFLOW_BRANCH_OVERRIDE_ENV,
            override,
            default_branch,
        )
        return override
    return default_branch


@dataclass
class WorkflowDispatchResult:
    """Result of triggering a workflow dispatch."""

    workflow_url: str
    """URL to the workflow file (e.g., .../actions/workflows/my-workflow.yml)"""

    run_id: int | None = None
    """GitHub Actions run ID, if discovered"""

    run_url: str | None = None
    """Direct URL to the workflow run, if discovered"""


@dataclass
class WorkflowJobInfo:
    """Information about a single job in a workflow run."""

    job_id: int
    """GitHub job ID (use with git_ci_job_logs to retrieve logs)"""

    name: str
    """Job name as defined in the workflow"""

    status: str
    """Job status: queued, in_progress, completed"""

    conclusion: str | None = None
    """Job conclusion: success, failure, cancelled, skipped (only set when completed)"""

    started_at: str | None = None
    """ISO 8601 timestamp when the job started"""

    completed_at: str | None = None
    """ISO 8601 timestamp when the job completed"""


def get_workflow_jobs(
    owner: str,
    repo: str,
    run_id: int,
    token: str | None = None,
) -> list[WorkflowJobInfo]:
    """Get jobs for a workflow run from GitHub API.

    Args:
        owner: Repository owner (e.g., "airbytehq")
        repo: Repository name (e.g., "airbyte")
        run_id: Workflow run ID
        token: GitHub API token. If `None`, resolved via
            `resolve_ci_trigger_github_token` (which prefers
            `GITHUB_CI_WORKFLOW_TRIGGER_PAT`) so that private-repo
            workflow runs are accessible even when the default token
            lacks permission.

    Returns:
        List of WorkflowJobInfo objects for each job in the workflow run.

    Raises:
        ValueError: If no GitHub token is found.
        requests.HTTPError: If API request fails.
    """
    if token is None:
        token = resolve_ci_trigger_github_token()

    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/actions/runs/{run_id}/jobs"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    jobs_data = response.json()
    return [
        WorkflowJobInfo(
            job_id=job["id"],
            name=job["name"],
            status=job["status"],
            conclusion=job.get("conclusion"),
            started_at=job.get("started_at"),
            completed_at=job.get("completed_at"),
        )
        for job in jobs_data.get("jobs", [])
    ]


def find_workflow_run(
    owner: str,
    repo: str,
    workflow_file: str,
    ref: str,
    token: str,
    created_after: datetime,
    max_wait_seconds: float = 5.0,
) -> tuple[int, str] | None:
    """Find a workflow run that was created after a given time.

    This is used to find the run that was just triggered via workflow_dispatch.
    Polls for up to max_wait_seconds to handle GitHub API eventual consistency.

    Args:
        owner: Repository owner
        repo: Repository name
        workflow_file: Workflow file name
        ref: Git ref the workflow was triggered on
        token: GitHub API token
        created_after: Only consider runs created after this time
        max_wait_seconds: Maximum time to wait for run to appear (default 5 seconds)

    Returns:
        Tuple of (run_id, run_url) if found, None otherwise.
    """
    url = (
        f"{GITHUB_API_BASE}/repos/{owner}/{repo}/actions/workflows/{workflow_file}/runs"
    )
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    params = {
        "branch": ref,
        "event": "workflow_dispatch",
        "per_page": 5,
    }

    # Add a small buffer to handle timestamp precision differences between
    # local time and GitHub's created_at (which has second resolution)
    search_after = created_after - timedelta(seconds=2)

    deadline = time.monotonic() + max_wait_seconds
    attempt = 0

    while time.monotonic() < deadline:
        if attempt > 0:
            time.sleep(1.0)
        attempt += 1

        response = requests.get(url, headers=headers, params=params, timeout=30)
        if not response.ok:
            continue

        data = response.json()
        runs = data.get("workflow_runs", [])

        for run in runs:
            run_created_at = datetime.fromisoformat(
                run["created_at"].replace("Z", "+00:00")
            )
            if run_created_at >= search_after:
                return run["id"], run["html_url"]

    return None


def trigger_workflow_dispatch(
    owner: str,
    repo: str,
    workflow_file: str,
    ref: str,
    inputs: dict,
    token: str,
    find_run: bool = True,
    max_wait_seconds: float = 5.0,
) -> WorkflowDispatchResult:
    """Trigger a GitHub Actions workflow via workflow_dispatch.

    Args:
        owner: Repository owner (e.g., "airbytehq")
        repo: Repository name (e.g., "airbyte-ops-mcp")
        workflow_file: Workflow file name (e.g., "connector-regression-test.yml")
        ref: Git ref to run the workflow on (branch name)
        inputs: Workflow inputs dictionary
        token: GitHub API token
        find_run: Whether to attempt to find the run after dispatch (default True)
        max_wait_seconds: Maximum time to wait for run discovery (default 5 seconds)

    Returns:
        WorkflowDispatchResult with workflow URL and optionally run ID/URL.

    Raises:
        requests.HTTPError: If API request fails.
    """
    dispatch_time = datetime.now(tz=datetime.now().astimezone().tzinfo)

    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/actions/workflows/{workflow_file}/dispatches"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    payload = {
        "ref": ref,
        "inputs": inputs,
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()

    workflow_url = (
        f"https://github.com/{owner}/{repo}/actions/workflows/{workflow_file}"
    )

    if not find_run:
        return WorkflowDispatchResult(workflow_url=workflow_url)

    # Best-effort lookup of the run that was just triggered
    run_info = find_workflow_run(
        owner, repo, workflow_file, ref, token, dispatch_time, max_wait_seconds
    )
    if run_info:
        run_id, run_url = run_info
        return WorkflowDispatchResult(
            workflow_url=workflow_url,
            run_id=run_id,
            run_url=run_url,
        )

    return WorkflowDispatchResult(workflow_url=workflow_url)


@dataclass
class WorkflowRunStatus:
    """Status of a completed (or timed-out) workflow run."""

    run_id: int
    """GitHub Actions run ID."""

    status: str
    """Run status: queued, in_progress, completed."""

    conclusion: str | None = None
    """Run conclusion: success, failure, cancelled, etc. Only set when completed."""

    run_url: str | None = None
    """Direct URL to the workflow run."""

    jobs: list[WorkflowJobInfo] | None = None
    """Job-level details (populated on failure for diagnostics)."""

    @property
    def succeeded(self) -> bool:
        """Return True if the run completed successfully."""
        return self.status == "completed" and self.conclusion == "success"

    @property
    def failed(self) -> bool:
        """Return True if the run completed with a non-success conclusion."""
        return self.status == "completed" and self.conclusion not in (
            "success",
            None,
        )


def wait_for_workflow_completion(
    owner: str,
    repo: str,
    run_id: int,
    token: str,
    poll_interval_seconds: float = 5.0,
    max_wait_seconds: float = 120.0,
) -> WorkflowRunStatus:
    """Poll a workflow run until it completes or the timeout is reached.

    Args:
        owner: Repository owner (e.g., "airbytehq")
        repo: Repository name (e.g., "airbyte-ops-mcp")
        run_id: GitHub Actions workflow run ID to monitor
        token: GitHub API token
        poll_interval_seconds: Seconds between polling attempts (default 5)
        max_wait_seconds: Maximum total seconds to wait (default 120)

    Returns:
        WorkflowRunStatus with the final status. If the run failed,
        job-level details are included for diagnostics.
    """
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/actions/runs/{run_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    deadline = time.monotonic() + max_wait_seconds
    last_status = "unknown"
    last_conclusion: str | None = None
    run_url: str | None = None

    while time.monotonic() < deadline:
        response = requests.get(url, headers=headers, timeout=30)
        if response.ok:
            data = response.json()
            last_status = data.get("status", "unknown")
            last_conclusion = data.get("conclusion")
            run_url = data.get("html_url")

            if last_status == "completed":
                jobs: list[WorkflowJobInfo] | None = None
                if last_conclusion != "success":
                    # Fetch job details for failure diagnostics
                    try:
                        jobs = get_workflow_jobs(owner, repo, run_id)
                    except Exception:
                        logger.warning(
                            "Failed to fetch job details for run %s",
                            run_id,
                            exc_info=True,
                        )
                return WorkflowRunStatus(
                    run_id=run_id,
                    status=last_status,
                    conclusion=last_conclusion,
                    run_url=run_url,
                    jobs=jobs,
                )

        time.sleep(poll_interval_seconds)

    # Timed out — return whatever we last saw
    return WorkflowRunStatus(
        run_id=run_id,
        status=last_status,
        conclusion=last_conclusion,
        run_url=run_url,
    )


def download_job_logs(
    owner: str,
    repo: str,
    job_id: int,
    token: str,
) -> str:
    """Download raw logs for a GitHub Actions job.

    Args:
        owner: Repository owner (e.g., "airbytehq")
        repo: Repository name (e.g., "airbyte-ops-mcp")
        job_id: GitHub Actions job ID
        token: GitHub API token

    Returns:
        Raw log text for the job.

    Raises:
        requests.HTTPError: If API request fails.
    """
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/actions/jobs/{job_id}/logs"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    response = requests.get(url, headers=headers, timeout=60, allow_redirects=True)
    response.raise_for_status()
    return response.text
