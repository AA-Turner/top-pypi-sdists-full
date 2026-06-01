# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tools for connector release block operations.

These tools trigger the `block-release.yml` GitHub Actions workflow in the
airbyte monorepo to create or remove `block-release.yaml` marker files.
The workflow handles branching, PR creation, and force-merge automatically.
"""

from __future__ import annotations

from typing import Annotated
from urllib.parse import quote

import requests
import yaml
from fastmcp import FastMCP
from fastmcp_extensions import mcp_tool, register_mcp_tools
from pydantic import BaseModel, Field

from airbyte_ops_mcp.github_actions import (
    resolve_default_workflow_branch,
    trigger_workflow_dispatch,
)
from airbyte_ops_mcp.github_api import (
    GITHUB_API_BASE,
    get_file_contents_at_ref,
    resolve_ci_trigger_github_token,
)

AIRBYTE_REPO_OWNER = "airbytehq"
AIRBYTE_REPO_NAME = "airbyte"
BLOCK_RELEASE_WORKFLOW_FILE = "block-release.yml"
DEFAULT_REF = "master"


class BlockConnectorReleaseResult(BaseModel):
    """Result of triggering a release block workflow."""

    success: bool = Field(description="Whether the workflow dispatch succeeded")
    message: str = Field(description="Human-readable result message")
    workflow_url: str = Field(description="URL to the workflow")
    run_id: int | None = Field(
        default=None, description="Workflow run ID, if discovered"
    )
    run_url: str | None = Field(default=None, description="URL to the workflow run")


class UnblockConnectorReleaseResult(BaseModel):
    """Result of triggering a release unblock workflow."""

    success: bool = Field(description="Whether the workflow dispatch succeeded")
    message: str = Field(description="Human-readable result message")
    workflow_url: str = Field(description="URL to the workflow")
    run_id: int | None = Field(
        default=None, description="Workflow run ID, if discovered"
    )
    run_url: str | None = Field(default=None, description="URL to the workflow run")


class ListBlockedConnectorsResult(BaseModel):
    """Result of listing blocked connectors via the GitHub API."""

    blocked_connectors: list[dict] = Field(
        default_factory=list,
        description="List of blocked connectors with optional block metadata",
    )
    count: int = Field(default=0, description="Number of blocked connectors")


@mcp_tool(
    read_only=False,
    idempotent=False,
    open_world=True,
)
def block_connector_release(
    connector_name: Annotated[
        str,
        Field(
            description="Connector technical name (e.g., `source-faker`, `destination-postgres`)"
        ),
    ],
    reason: Annotated[
        str,
        Field(description="Human-readable reason for blocking the release"),
    ],
    yanked_version: Annotated[
        str | None,
        Field(description="Version that was yanked (for reference)"),
    ] = None,
    blocked_by: Annotated[
        str | None,
        Field(description="Email or identifier of the person requesting the block"),
    ] = None,
) -> BlockConnectorReleaseResult:
    """Block a connector from being released by creating a `block-release.yaml` marker.

    Triggers the `block-release.yml` workflow in the airbyte monorepo, which
    creates a marker file, opens a PR, and force-merges it to master. While the
    marker exists, the publish pipeline will skip the connector with a warning.

    Use this after yanking a connector version to prevent CI from accidentally
    re-publishing the broken code.
    """
    token = resolve_ci_trigger_github_token()

    inputs: dict[str, str] = {
        "connector-name": connector_name,
        "action": "block",
        "reason": reason,
    }
    if yanked_version:
        inputs["yanked-version"] = yanked_version
    if blocked_by:
        inputs["blocked-by"] = blocked_by

    result = trigger_workflow_dispatch(
        owner=AIRBYTE_REPO_OWNER,
        repo=AIRBYTE_REPO_NAME,
        workflow_file=BLOCK_RELEASE_WORKFLOW_FILE,
        ref=resolve_default_workflow_branch(DEFAULT_REF),
        inputs=inputs,
        token=token,
        find_run=True,
    )

    if result.run_id:
        message = (
            f"Successfully triggered release block for {connector_name}. "
            f"Run ID: {result.run_id}"
        )
    else:
        message = (
            f"Successfully triggered release block for {connector_name}. "
            "Run ID not yet available."
        )

    return BlockConnectorReleaseResult(
        success=True,
        message=message,
        workflow_url=result.workflow_url,
        run_id=result.run_id,
        run_url=result.run_url,
    )


@mcp_tool(
    read_only=False,
    idempotent=False,
    open_world=True,
)
def unblock_connector_release(
    connector_name: Annotated[
        str,
        Field(
            description="Connector technical name (e.g., `source-faker`, `destination-postgres`)"
        ),
    ],
) -> UnblockConnectorReleaseResult:
    """Remove a release block for a connector by deleting its `block-release.yaml` marker.

    Triggers the `block-release.yml` workflow with action=unblock, which removes
    the marker file, opens a PR, and force-merges it to master. After this, the
    connector can be published normally again.
    """
    token = resolve_ci_trigger_github_token()

    result = trigger_workflow_dispatch(
        owner=AIRBYTE_REPO_OWNER,
        repo=AIRBYTE_REPO_NAME,
        workflow_file=BLOCK_RELEASE_WORKFLOW_FILE,
        ref=resolve_default_workflow_branch(DEFAULT_REF),
        inputs={
            "connector-name": connector_name,
            "action": "unblock",
        },
        token=token,
        find_run=True,
    )

    if result.run_id:
        message = (
            f"Successfully triggered release unblock for {connector_name}. "
            f"Run ID: {result.run_id}"
        )
    else:
        message = (
            f"Successfully triggered release unblock for {connector_name}. "
            "Run ID not yet available."
        )

    return UnblockConnectorReleaseResult(
        success=True,
        message=message,
        workflow_url=result.workflow_url,
        run_id=result.run_id,
        run_url=result.run_url,
    )


@mcp_tool(
    read_only=True,
    idempotent=True,
    open_world=True,
)
def list_blocked_connector_releases(
    connector_name: Annotated[
        str | None,
        Field(
            description="Optional connector name to check. If not provided, scans all connectors."
        ),
    ] = None,
    include_details: Annotated[
        bool,
        Field(
            description="Whether to fetch and parse each marker file for reason and metadata."
        ),
    ] = True,
) -> ListBlockedConnectorsResult:
    """List connectors that are currently blocked from release.

    Searches the airbyte monorepo for `block-release.yaml` marker files using
    the GitHub API. Returns a list of blocked connectors, with marker metadata
    when `include_details` is `True`.
    """

    token = resolve_ci_trigger_github_token()
    ref = resolve_default_workflow_branch(DEFAULT_REF)
    blocked: list[dict] = []

    if connector_name:
        blocked = _check_single_connector_block(connector_name, token, ref)
    else:
        blocked = _search_all_blocked_connectors(token, ref, include_details)

    return ListBlockedConnectorsResult(
        blocked_connectors=blocked,
        count=len(blocked),
    )


def _check_single_connector_block(
    connector_name: str,
    token: str,
    ref: str,
) -> list[dict]:
    """Check if a single connector has a release block."""
    path = f"airbyte-integrations/connectors/{connector_name}/block-release.yaml"
    content = get_file_contents_at_ref(
        owner=AIRBYTE_REPO_OWNER,
        repo=AIRBYTE_REPO_NAME,
        path=path,
        ref=ref,
        token=token,
    )
    if content is None:
        return []

    return _parse_block_marker_content(connector_name, content)


def _parse_block_marker_content(connector_name: str, content: str) -> list[dict]:
    """Parse a `block-release.yaml` marker into the MCP response shape."""
    try:
        block_file_data = yaml.safe_load(content)
        if isinstance(block_file_data, dict):
            return [
                {
                    "connector_name": connector_name,
                    "reason": block_file_data.get("reason", "(no reason provided)"),
                    "yanked_version": block_file_data.get("yanked_version"),
                    "blocked_at": block_file_data.get("blocked_at"),
                    "blocked_by": block_file_data.get("blocked_by"),
                }
            ]
    except yaml.YAMLError:
        return [
            {"connector_name": connector_name, "reason": "(unable to parse marker)"}
        ]

    return [
        {
            "connector_name": connector_name,
            "reason": "(invalid block-release.yaml format)",
        }
    ]


def _search_all_blocked_connectors(
    token: str,
    ref: str,
    include_details: bool,
) -> list[dict]:
    """Search the repo for all `block-release.yaml` files at the requested ref."""
    tree_ref = quote(ref, safe="")
    url = (
        f"{GITHUB_API_BASE}/repos/{AIRBYTE_REPO_OWNER}/{AIRBYTE_REPO_NAME}"
        f"/git/trees/{tree_ref}"
    )
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    response = requests.get(
        url,
        headers=headers,
        params={"recursive": "1"},
        timeout=30,
    )
    response.raise_for_status()

    tree = response.json().get("tree", [])
    blocked: list[dict] = []

    for item in tree:
        file_path = item.get("path", "")
        if not file_path.endswith("/block-release.yaml"):
            continue

        parts = file_path.split("/")
        if (
            len(parts) == 4
            and parts[0] == "airbyte-integrations"
            and parts[1] == "connectors"
        ):
            connector_name = parts[2]
            if not include_details:
                blocked.append({"connector_name": connector_name})
                continue

            content = get_file_contents_at_ref(
                owner=AIRBYTE_REPO_OWNER,
                repo=AIRBYTE_REPO_NAME,
                path=file_path,
                ref=ref,
                token=token,
            )
            if content is not None:
                blocked.extend(_parse_block_marker_content(connector_name, content))

    return blocked


def register_release_block_tools(app: FastMCP) -> None:
    """Register release block tools with the FastMCP app."""
    register_mcp_tools(app, mcp_module=__name__)
