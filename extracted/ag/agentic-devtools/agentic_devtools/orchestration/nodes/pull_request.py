"""Pull request node: create PR on the appropriate platform.

Detects the platform (Azure DevOps vs GitHub) from the ``issue_provider``
state field and creates a draft pull request with appropriate metadata.
"""

from __future__ import annotations

import os
import re
import tempfile
from typing import Any

import requests as _requests

from agentic_devtools.cli.azure_devops.auth import get_auth_headers, get_pat
from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig
from agentic_devtools.cli.azure_devops.helpers import get_repository_id
from agentic_devtools.cli.subprocess_utils import run_safe
from agentic_devtools.orchestration.nodes._helpers import (
    detect_issue_provider,
    normalize_issue_key,
    utc_now,
)
from agentic_devtools.orchestration.state_schema import WorkOnIssueState


def pull_request_node(state: WorkOnIssueState) -> dict[str, Any]:
    """Create pull request on the appropriate platform.

    Uses ``issue_provider`` when it is ``"github"``/``"jira"``, otherwise derives
    the platform from ``issue_key`` (GitHub numeric/#N vs Jira PROJECT-N).
    Creates as draft by default. When ``dry_run`` is active, PR creation is
    simulated and the generated title is returned without invoking provider
    commands.

    Fails fast when ``issue_key`` is missing, blank, or not a string so a
    corrupted/resumed checkpoint cannot raise ``AttributeError`` inside
    ``detect_issue_provider()`` or ``normalize_issue_key()``, or silently
    build a PR title with an empty scope.
    """
    issue_key = state.get("issue_key", "")
    if not isinstance(issue_key, str) or not issue_key.strip():
        return {
            "step": "pull_request",
            "error": "issue_key is required and must be a non-empty string",
            "events": [
                {
                    "event": "pull_request_failed",
                    "timestamp": utc_now(),
                    "signals": {"error": "missing_issue_key"},
                }
            ],
        }
    raw_issue_provider = state.get("issue_provider")
    issue_provider = (
        raw_issue_provider
        if isinstance(raw_issue_provider, str) and raw_issue_provider in {"jira", "github"}
        else detect_issue_provider(issue_key)
    )
    normalized_key = normalize_issue_key(issue_key)
    if not normalized_key:
        return {
            "step": "pull_request",
            "error": "issue_key must normalize to a non-empty issue identifier",
            "events": [
                {
                    "event": "pull_request_failed",
                    "timestamp": utc_now(),
                    "signals": {"error": "invalid_issue_key"},
                }
            ],
        }
    plan = state.get("plan", "")
    issue_data = state.get("issue_data", {})

    # Gate on the commit result: a blocked commit (error set) must NOT open a PR.
    # A no-op commit (no_op=True, error=None) still proceeds per FR-008.
    commit_result = state.get("commit_result")
    commit_error = getattr(commit_result, "error", None)
    if commit_error is not None:
        return {
            "step": "pull_request",
            "error": f"Skipping PR creation: commit was blocked ({commit_error.message})",
            "events": [
                {
                    "event": "pull_request_skipped",
                    "timestamp": utc_now(),
                    "signals": {"reason": "commit_blocked", "category": commit_error.category},
                }
            ],
        }
    commit_sha = getattr(commit_result, "commit_sha", None)
    commit_title = getattr(commit_result, "commit_message_title", None)

    # Generate PR title from commit result (FR-011) or fall back to issue data.
    if isinstance(commit_title, str) and commit_title.strip():
        pr_title = commit_title
    else:
        pr_title = _generate_pr_title(normalized_key, issue_data)
    pr_description = _generate_pr_description(normalized_key, plan, issue_data)

    if state.get("dry_run") is True:
        return {
            "step": "pull_request",
            "error": None,
            "pr_created": True,
            "pr_url": "",
            "pr_title": pr_title,
            "dry_run_skipped": True,
            "events": [
                {
                    "event": "pull_request_completed",
                    "timestamp": utc_now(),
                    "signals": {
                        "pr_created": True,
                        "pr_url": "",
                        "action": "skipped_dry_run",
                    },
                }
            ],
        }

    # Resolve the source branch from state (populated by the setup node) — never
    # from a CWD-based git call: after the setup node creates a sibling worktree
    # the process CWD may still be the repository root, so get_current_branch()
    # would return the wrong branch.
    source_branch = _resolve_source_branch(state)
    if not source_branch:
        return {
            "step": "pull_request",
            "error": "Cannot create PR: source branch is not available from setup_result/source_branch state",
            "events": [
                {
                    "event": "pull_request_failed",
                    "timestamp": utc_now(),
                    "signals": {"error": "missing_source_branch"},
                }
            ],
        }

    # Create PR based on platform
    if issue_provider == "github":
        result = _create_github_pr(pr_title, pr_description, source_branch)
    else:
        result = _create_azure_devops_pr(pr_title, pr_description, source_branch)

    if result.get("error"):
        return {
            "step": "pull_request",
            "error": result["error"],
            "pr_title": pr_title,
            "events": [
                {
                    "event": "pull_request_failed",
                    "timestamp": utc_now(),
                    "signals": {"error": result["error"]},
                }
            ],
        }

    return {
        "step": "pull_request",
        "error": None,
        "pr_created": True,
        "pr_url": result.get("url", ""),
        "pr_title": pr_title,
        "events": [
            {
                "event": "pull_request_completed",
                "timestamp": utc_now(),
                "signals": {
                    "pr_created": True,
                    "pr_url": result.get("url", ""),
                    "source_branch": source_branch,
                    "commit_sha": commit_sha,
                    "commit_title": commit_title,
                },
            }
        ],
    }


def _resolve_source_branch(state: WorkOnIssueState) -> str:
    """Resolve the PR source branch from graph state (never from process CWD).

    Prefers the explicit ``source_branch`` field, then ``setup_result.branch_name``.
    Returns an empty string when neither is available.
    """
    source_branch = state.get("source_branch")
    if isinstance(source_branch, str) and source_branch.strip():
        return source_branch.strip()
    setup_result = state.get("setup_result")
    branch_name = getattr(setup_result, "branch_name", None)
    if isinstance(branch_name, str) and branch_name.strip():
        return branch_name.strip()
    return ""


def _create_github_pr(title: str, description: str, source_branch: str) -> dict[str, Any]:
    """Create a GitHub PR by invoking the ``gh`` CLI directly.

    Uses a temporary body file to avoid OS argument-length limits and writes no
    state values — all parameters are passed explicitly on the command line.
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as tf:
        tf.write(description or "")
        tmp_body_path = tf.name

    try:
        cmd = [
            "gh",
            "pr",
            "create",
            "--title",
            title,
            "--body-file",
            tmp_body_path,
            "--base",
            "main",
            "--head",
            source_branch,
            "--draft",
        ]
        try:
            result = run_safe(cmd, capture_output=True, text=True, shell=False)
        except OSError as exc:
            return {"error": f"GitHub CLI ('gh') could not be started: {exc}"}
    finally:
        try:
            os.unlink(tmp_body_path)
        except OSError:
            pass

    if result.returncode != 0:
        return {"error": f"GitHub PR creation failed: {result.stderr.strip()}"}

    # gh pr create prints the PR URL on success.
    url = ""
    for line in result.stdout.splitlines():
        match = re.search(r"https://github\.com/\S+/pull/\d+", line)
        if match:
            url = match.group(0)
            break

    return {"url": url}


def _create_azure_devops_pr(title: str, description: str, source_branch: str) -> dict[str, Any]:
    """Create an Azure DevOps PR via the REST API directly.

    Reads organisation/project/repository coordinates from state (via
    :class:`~agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig`)
    and posts a draft PR to the ADO Git REST endpoint.  No ``agdt-*``
    subprocesses are spawned and no state values are mutated.
    """
    config = AzureDevOpsConfig.from_state()

    try:
        repo_id = get_repository_id(config.organization, config.project, config.repository)
    except Exception as exc:
        return {"error": f"Failed to resolve ADO repository ID: {exc}"}

    try:
        pat = get_pat()
    except OSError as exc:
        return {"error": f"Azure DevOps PAT not available: {exc}"}

    headers = get_auth_headers(pat)
    headers["Content-Type"] = "application/json"

    pr_url = config.build_api_url(repo_id, "pullrequests")
    payload: dict[str, Any] = {
        "title": title,
        "description": description or "",
        "sourceRefName": f"refs/heads/{source_branch}",
        "targetRefName": "refs/heads/main",
        "isDraft": True,
    }

    try:
        response = _requests.post(pr_url, headers=headers, json=payload, timeout=60)
    except Exception as exc:
        return {"error": f"Azure DevOps PR creation request failed: {exc}"}

    if not response.ok:
        return {"error": f"Azure DevOps PR creation failed (HTTP {response.status_code}): {response.text}"}

    try:
        data = response.json()
    except Exception as exc:
        return {"error": f"Azure DevOps PR creation returned non-JSON response: {exc}"}
    if not isinstance(data, dict):
        return {"error": f"Azure DevOps PR creation returned unexpected response type: {type(data).__name__}"}
    pr_id = data.get("pullRequestId")
    if pr_id is None:
        return {"error": "Azure DevOps PR creation returned success but response is missing a valid pullRequestId"}
    # The REST response 'url' field is the API URL, not the HTML PR link.
    # Construct the human-readable web URL from the resolved coordinates.
    html_url = ""
    if config.organization:
        html_url = f"{config.organization.rstrip('/')}/{config.project}/_git/{config.repository}/pullrequest/{pr_id}"

    return {"url": html_url}


def _generate_pr_title(issue_key: str, issue_data: Any) -> str:
    """Generate PR title from issue data."""
    summary = ""
    if isinstance(issue_data, dict):
        raw_summary = issue_data.get("summary", "")
        if isinstance(raw_summary, str):
            summary = raw_summary

    if not summary:
        summary = "autonomous implementation"

    normalized = issue_key.lstrip("#")
    if normalized.isdigit():
        scope = f"#{normalized}"
    else:
        scope = normalized

    title = f"feat({scope}): {summary}"
    if len(title) > 72:
        title = title[:69] + "..."
    return title


def _generate_pr_description(issue_key: str, plan: str, issue_data: Any) -> str:
    """Generate PR description."""
    summary = ""
    if isinstance(issue_data, dict):
        raw_summary = issue_data.get("summary", "")
        if isinstance(raw_summary, str):
            summary = raw_summary

    if not isinstance(plan, str):
        plan = ""

    description_parts = [
        f"## Summary\n\nAutonomous implementation for issue {issue_key}.",
    ]

    if summary:
        description_parts.append(f"\n**Issue**: {summary}")

    if plan:
        plan_preview = plan[:500]
        description_parts.append(f"\n## Implementation Plan\n\n{plan_preview}")

    description_parts.append("\n---\n*Generated by LangChain work-on-issue workflow*")
    return "\n".join(description_parts)
