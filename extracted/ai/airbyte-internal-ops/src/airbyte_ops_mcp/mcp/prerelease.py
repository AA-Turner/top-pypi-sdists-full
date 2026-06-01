# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tools for triggering connector pre-release workflows.

This module provides MCP tools for triggering the publish-connectors-prerelease
workflow in the airbytehq/airbyte repository (for OSS connectors) or the
publish_enterprise_connectors workflow in airbytehq/airbyte-enterprise
(for enterprise connectors) via GitHub's workflow dispatch API.

## MCP reference

.. include:: ../../../docs/mcp-generated/prerelease.md
    :start-line: 2
"""

from __future__ import annotations

__all__: list[str] = []

import base64
from enum import StrEnum
from typing import Annotated, Literal

import requests
import yaml
from fastmcp import FastMCP
from fastmcp_extensions import mcp_tool, register_mcp_tools
from pydantic import BaseModel, Field

from airbyte_ops_mcp.airbyte_repo.bump_version import strip_prerelease_suffix
from airbyte_ops_mcp.github_actions import trigger_workflow_dispatch
from airbyte_ops_mcp.github_api import (
    GITHUB_API_BASE,
    get_pr_head_ref,
    resolve_ci_trigger_github_token,
)


class ConnectorRepo(StrEnum):
    """Repository where connector code is located."""

    AIRBYTE = "airbyte"
    AIRBYTE_ENTERPRISE = "airbyte-enterprise"


DEFAULT_REPO_OWNER = "airbytehq"
DEFAULT_REPO_NAME = ConnectorRepo.AIRBYTE
DEFAULT_BRANCH = "master"
PRERELEASE_WORKFLOW_FILE = "publish-connectors-prerelease-command.yml"
CONNECTOR_PATH_PREFIX = "airbyte-integrations/connectors"

# Enterprise repository constants
ENTERPRISE_REPO_NAME = ConnectorRepo.AIRBYTE_ENTERPRISE
ENTERPRISE_DEFAULT_BRANCH = "main"
ENTERPRISE_PRERELEASE_WORKFLOW_FILE = "publish_enterprise_connectors.yml"

# Token env vars for prerelease publishing (in order of preference)
PRERELEASE_TOKEN_ENV_VARS = [
    "GITHUB_CONNECTOR_PUBLISHING_PAT",
    "GITHUB_CI_WORKFLOW_TRIGGER_PAT",
    "GITHUB_TOKEN",
]

# =============================================================================
# Pre-release Version Tag Constants
# =============================================================================

PRERELEASE_TAG_PREFIX = "preview"
"""The prefix used for pre-release version tags (e.g., '1.2.3-preview.abcde12')."""

PRERELEASE_SHA_LENGTH = 7
"""The number of characters from the git SHA to include in pre-release tags."""


def compute_prerelease_docker_image_tag(base_version: str, sha: str) -> str:
    """Compute the pre-release docker image tag.

    This is the SINGLE SOURCE OF TRUTH for pre-release version format.
    All other code should receive this value as a parameter, not recompute it.

    The format is: {base_version}-preview.{short_sha}

    Where:
        - base_version: The base version from metadata.yaml (e.g., "1.2.3"),
          which may already contain a pre-release suffix (e.g., "2.23.16-rc.1").
          Any existing pre-release suffix is stripped before applying the preview tag.
        - short_sha: The first 7 characters of the git commit SHA

    Examples:
        >>> compute_prerelease_docker_image_tag("1.2.3", "abcdef1234567890")
        '1.2.3-preview.abcdef1'
        >>> compute_prerelease_docker_image_tag("0.1.0", "1234567")
        '0.1.0-preview.1234567'
        >>> compute_prerelease_docker_image_tag("2.23.16-rc.1", "abcdef1234567890")
        '2.23.16-preview.abcdef1'

    Args:
        base_version: The base version from metadata.yaml (e.g., "1.2.3" or "2.23.16-rc.1")
        sha: The full git commit SHA (or at least 7 characters)

    Returns:
        Pre-release version tag (e.g., "1.2.3-preview.abcde12")
    """
    short_sha = sha[:PRERELEASE_SHA_LENGTH]
    clean_version = strip_prerelease_suffix(base_version)
    return f"{clean_version}-{PRERELEASE_TAG_PREFIX}.{short_sha}"


class PrereleaseWorkflowResult(BaseModel):
    """Response model for publish_connector_to_airbyte_registry MCP tool."""

    success: bool
    message: str
    workflow_url: str | None = None
    connector_name: str | None = None
    pr_number: int | None = None
    docker_image: str | None = None
    docker_image_tag: str | None = None


def _get_connector_metadata(
    owner: str,
    repo: str,
    connector_name: str,
    ref: str,
    token: str,
) -> dict | None:
    """Fetch and parse connector metadata.yaml from the repository.

    Args:
        owner: Repository owner (e.g., "airbytehq")
        repo: Repository name (e.g., "airbyte")
        connector_name: Connector name (e.g., "source-github")
        ref: Git ref to fetch from (branch name or SHA)
        token: GitHub API token

    Returns:
        Parsed metadata dictionary, or None if not found.
    """
    metadata_path = f"{CONNECTOR_PATH_PREFIX}/{connector_name}/metadata.yaml"
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/contents/{metadata_path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    params = {"ref": ref}

    response = requests.get(url, headers=headers, params=params, timeout=30)

    # Guard: Return None if metadata file not found
    if response.status_code == 404:
        return None

    response.raise_for_status()

    content_data = response.json()

    # Guard: Return None if content is not base64 encoded
    if content_data.get("encoding") != "base64":
        return None

    content = base64.b64decode(content_data["content"]).decode("utf-8")
    return yaml.safe_load(content)


@mcp_tool(
    read_only=False,
    destructive=False,
    idempotent=False,
    open_world=True,
)
def publish_connector_to_airbyte_registry(
    connector_name: Annotated[
        str,
        Field(
            description="The connector name to publish (e.g., 'source-github', 'destination-postgres')"
        ),
    ],
    pr_number: Annotated[
        int,
        Field(description="The pull request number containing the connector changes"),
    ],
    repo: Annotated[
        ConnectorRepo,
        Field(
            default=ConnectorRepo.AIRBYTE,
            description="Repository where the connector PR is located. "
            "Use 'airbyte' for OSS connectors (default) or 'airbyte-enterprise' for enterprise connectors.",
        ),
    ],
    prerelease: Annotated[
        Literal[True],
        Field(
            default=True,
            description="Must be True. Only prerelease publishing is supported at this time.",
        ),
    ],
) -> PrereleaseWorkflowResult:
    """Publish a connector to the Airbyte registry.

    Currently only supports pre-release publishing. This tool triggers the
    publish-connectors-prerelease workflow in the airbytehq/airbyte repository
    (for OSS connectors) or the publish_enterprise_connectors workflow in
    airbytehq/airbyte-enterprise (for enterprise connectors), which publishes
    a pre-release version of the specified connector from the PR branch.

    Pre-release versions are tagged with the format: {version}-preview.{7-char-git-sha}
    These versions are available for version pinning via the scoped_configuration API.

    Requires GITHUB_CONNECTOR_PUBLISHING_PAT or GITHUB_TOKEN environment variable
    with 'actions:write' permission.
    """
    # Guard: Only prerelease publishing is supported
    if prerelease is not True:
        raise NotImplementedError(
            "Non-prerelease publishing is not implemented yet. Set prerelease=True."
        )

    # Guard: Check for required token
    token = resolve_ci_trigger_github_token(PRERELEASE_TOKEN_ENV_VARS)

    # Determine repo-specific settings
    is_enterprise = repo == ConnectorRepo.AIRBYTE_ENTERPRISE
    target_repo_name = ENTERPRISE_REPO_NAME if is_enterprise else DEFAULT_REPO_NAME
    target_branch = ENTERPRISE_DEFAULT_BRANCH if is_enterprise else DEFAULT_BRANCH
    target_workflow = (
        ENTERPRISE_PRERELEASE_WORKFLOW_FILE
        if is_enterprise
        else PRERELEASE_WORKFLOW_FILE
    )

    # Get the PR's head SHA for computing the docker image tag
    # Note: We no longer pass gitref to the workflow - it derives the ref from PR number
    head_info = get_pr_head_ref(DEFAULT_REPO_OWNER, target_repo_name, pr_number, token)

    # Prepare workflow inputs
    workflow_inputs = {
        "repo": f"{DEFAULT_REPO_OWNER}/{target_repo_name}",
        "pr": str(pr_number),
        "connector": connector_name,
    }

    # Trigger the workflow on the configured default branch.
    # The workflow will checkout the PR branch via inputs.gitref
    dispatch_result = trigger_workflow_dispatch(
        owner=DEFAULT_REPO_OWNER,
        repo=target_repo_name,
        workflow_file=target_workflow,
        ref=target_branch,
        inputs=workflow_inputs,
        token=token,
        find_run=True,
    )
    # Use the specific run URL if found, otherwise fall back to the workflow URL
    workflow_url = dispatch_result.run_url or dispatch_result.workflow_url

    # Try to compute docker_image and docker_image_tag from connector metadata
    docker_image: str | None = None
    docker_image_tag: str | None = None
    metadata = _get_connector_metadata(
        DEFAULT_REPO_OWNER,
        target_repo_name,
        connector_name,
        head_info.sha,
        token,
    )
    if metadata and "data" in metadata:
        data = metadata["data"]
        docker_image = data.get("dockerRepository")
        base_version = data.get("dockerImageTag")
        if base_version:
            docker_image_tag = compute_prerelease_docker_image_tag(
                base_version, head_info.sha
            )

    repo_info = f" from {repo}" if is_enterprise else ""
    return PrereleaseWorkflowResult(
        success=True,
        message=f"Successfully triggered pre-release workflow for {connector_name}{repo_info} from PR #{pr_number}",
        workflow_url=workflow_url,
        connector_name=connector_name,
        pr_number=pr_number,
        docker_image=docker_image,
        docker_image_tag=docker_image_tag,
    )


def register_prerelease_tools(app: FastMCP) -> None:
    """Register pre-release workflow tools with the FastMCP app.

    Args:
        app: FastMCP application instance
    """
    register_mcp_tools(app, mcp_module=__name__)
