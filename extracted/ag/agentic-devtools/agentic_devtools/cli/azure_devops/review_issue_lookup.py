"""Resolve Azure DevOps pull-request and linked Jira issue details."""

import json
import os
import sys
from typing import Any

from ...state import get_value
from ..subprocess_utils import run_safe
from .auth import get_pat
from .config import AzureDevOpsConfig
from .helpers import verify_az_cli


def _get_jira_issue_key_from_state() -> str | None:
    """Get Jira issue key from state."""
    return get_value("jira.issue_key")


def _get_pull_request_id_from_state() -> int | None:
    """Get pull request ID from state."""
    value = get_value("pull_request_id")
    if value is not None:
        try:
            return int(value)
        except ValueError, TypeError:
            return None
    return None


def _get_linked_pull_request_from_jira(issue_key: str) -> int | None:
    """
    Fetch Jira issue and extract linked Azure DevOps pull request ID.

    This looks for remote links that point to Azure DevOps pull requests.

    Args:
        issue_key: Jira issue key (e.g., PROJECT-1234)

    Returns:
        Pull request ID if found, None otherwise
    """
    import re

    try:
        import requests as req_module
    except ImportError:
        print("Warning: 'requests' library required for Jira API calls", file=sys.stderr)
        return None

    # Import Jira config
    try:
        from ..jira.config import get_jira_base_url, get_jira_headers
        from ..jira.helpers import _get_ssl_verify
    except ImportError:
        print("Warning: Jira module not available", file=sys.stderr)
        return None

    base_url = get_jira_base_url()
    headers = get_jira_headers()
    ssl_verify = _get_ssl_verify()

    # First, get the issue with remote links
    issue_url = f"{base_url}/rest/api/2/issue/{issue_key}?fields=summary"

    try:
        response = req_module.get(issue_url, headers=headers, verify=ssl_verify, timeout=30)
        if response.status_code != 200:
            return None
    except Exception:
        return None

    # Get remote links for the issue
    remote_links_url = f"{base_url}/rest/api/2/issue/{issue_key}/remotelink"

    try:
        response = req_module.get(remote_links_url, headers=headers, verify=ssl_verify, timeout=30)
        if response.status_code == 200:
            remote_links = response.json()

            # Look for Azure DevOps PR links
            # Pattern: https://dev.azure.com/{org}/{project}/_git/{repo}/pullrequest/{id}
            pr_url_pattern = re.compile(r"pullrequest[s]?/(\d+)", re.IGNORECASE)

            for link in remote_links:
                link_url = link.get("object", {}).get("url", "")
                if "dev.azure.com" in link_url or "visualstudio.com" in link_url:
                    match = pr_url_pattern.search(link_url)
                    if match:
                        return int(match.group(1))
    except Exception:  # pragma: no cover
        pass

    return None


def _fetch_pull_request_basic_info(pull_request_id: int, config: AzureDevOpsConfig) -> dict[str, Any] | None:
    """
    Fetch basic pull request info using az CLI.

    Args:
        pull_request_id: PR ID to fetch
        config: Azure DevOps configuration

    Returns:
        PR data dict or None if failed
    """
    verify_az_cli()
    pat = get_pat()

    env = os.environ.copy()
    env["AZURE_DEVOPS_EXT_PAT"] = pat

    org_arg = (
        config.organization
        if config.organization.startswith("http")
        else f"https://dev.azure.com/{config.organization}"
    )

    result = run_safe(
        [
            "az",
            "repos",
            "pr",
            "show",
            "--id",
            str(pull_request_id),
            "--organization",
            org_arg,
            "--output",
            "json",
        ],
        capture_output=True,
        text=True,
        env=env,
    )

    if result.returncode != 0:
        return None

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def _fetch_and_display_jira_issue(issue_key: str) -> bool:
    """
    Fetch and display Jira issue details.

    Args:
        issue_key: Jira issue key

    Returns:
        True if successful, False otherwise
    """
    from ..workflows.base import _safe_print

    try:
        from ..jira.get_commands import get_issue
        from ..jira.state_helpers import set_jira_value

        # Set the issue key in state
        set_jira_value("issue_key", issue_key)

        # Call get_issue (this prints details and saves to temp file)
        get_issue()
        return True
    except SystemExit:
        # get_issue calls sys.exit(1) on failure - catch and continue
        _safe_print(
            f"Warning: Jira issue {issue_key} could not be fetched. Proceeding with PR review only.",
            file=sys.stderr,
        )
        return False
    except Exception as e:
        _safe_print(f"Warning: Failed to fetch Jira issue {issue_key}: {e}", file=sys.stderr)
        return False
