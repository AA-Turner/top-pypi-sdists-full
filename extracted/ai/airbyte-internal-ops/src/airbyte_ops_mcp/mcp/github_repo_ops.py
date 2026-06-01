# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tools for GitHub repository operations.

This module exposes repository operations as MCP tools for AI agents to use.
These are thin wrappers around capability functions in airbyte_repo module.

## MCP reference

.. include:: ../../../docs/mcp-generated/github_repo_ops.md
    :start-line: 2
"""

from __future__ import annotations

__all__: list[str] = []

from typing import Annotated, Literal

from fastmcp import FastMCP
from fastmcp_extensions import mcp_tool, register_mcp_tools
from pydantic import BaseModel

from airbyte_ops_mcp.airbyte_repo.bump_version import bump_connector_version
from airbyte_ops_mcp.airbyte_repo.list_connectors import list_connectors
from airbyte_ops_mcp.airbyte_repo.utils import resolve_diff_range


class ConnectorListResponse(BaseModel):
    """Response model for list_connectors MCP tool."""

    connectors: list[str]
    count: int


class BumpVersionResponse(BaseModel):
    """Response model for bump_connector_version MCP tool."""

    connector: str
    previous_version: str
    new_version: str
    files_modified: list[str]
    dry_run: bool


@mcp_tool(
    read_only=True,
    idempotent=True,
    open_world=False,
)
def list_connectors_in_repo(
    repo_path: Annotated[str, "Absolute path to the Airbyte monorepo"],
    certified: Annotated[
        bool | None,
        "Filter by certification: True=certified only, False=non-certified only, None=all",
    ] = None,
    modified: Annotated[
        bool | None,
        "Filter by modification: True=modified only, False=not-modified only, None=all",
    ] = None,
    language_filter: Annotated[
        set[str] | None,
        "Set of languages to include (python, java, low-code, manifest-only)",
    ] = None,
    language_exclude: Annotated[
        set[str] | None,
        "Set of languages to exclude (mutually exclusive with language_filter)",
    ] = None,
    connector_type: Annotated[
        Literal["source", "destination"] | None,
        "Filter by connector type: 'source' or 'destination', None=all",
    ] = None,
    connector_subtype: Annotated[
        Literal["api", "database", "file", "custom"] | None,
        "Filter by connector subtype: 'api', 'database', 'file', 'custom', None=all",
    ] = None,
    pr_num_or_url: Annotated[
        str | None,
        "PR number (e.g., '123'), GitHub URL, or None to auto-detect from GITHUB_REF environment variable",
    ] = None,
    gh_token: Annotated[
        str | None,
        "GitHub API token. When provided together with pr_num_or_url, the GitHub API is used "
        "to detect modified files instead of local git diff (avoids shallow-clone issues).",
    ] = None,
) -> ConnectorListResponse:
    """List connectors in the Airbyte monorepo with flexible filtering.

    Filters can be combined to narrow results. PR context (if provided or auto-detected)
    determines the git diff range for modification detection.
    """
    # Resolve PR info to base_ref and head_ref (MCP-specific: supports PR URL/number input)
    base_ref, head_ref, pr_number, pr_owner, pr_repo = resolve_diff_range(pr_num_or_url)

    # Delegate to capability function
    result = list_connectors(
        repo_path=repo_path,
        certified=certified,
        modified=modified,
        language_filter=language_filter,
        language_exclude=language_exclude,
        connector_type=connector_type,
        connector_subtype=connector_subtype,
        base_ref=base_ref,
        head_ref=head_ref,
        pr_number=pr_number,
        pr_owner=pr_owner,
        pr_repo=pr_repo,
        gh_token=gh_token,
    )

    return ConnectorListResponse(
        connectors=result.connectors,
        count=result.count,
    )


@mcp_tool(
    read_only=False,
    idempotent=False,
    open_world=False,
)
def bump_version_in_repo(
    repo_path: Annotated[str, "Absolute path to the Airbyte monorepo"],
    connector_name: Annotated[str, "Connector technical name (e.g., 'source-github')"],
    bump_type: Annotated[
        Literal[
            "patch",
            "minor",
            "major",
            "patch_rc",
            "minor_rc",
            "major_rc",
            "rc",
            "promote",
        ]
        | None,
        "Version bump type. Standard: 'patch', 'minor', 'major'. "
        "RC: 'patch_rc', 'minor_rc', 'major_rc' (create RC for next version), "
        "'rc' (smart default: minor_rc if not RC, else bump RC number). "
        "'promote' (strip RC suffix to finalize release).",
    ] = None,
    new_version: Annotated[
        str | None,
        "Explicit new version (overrides bump_type if provided)",
    ] = None,
    changelog_message: Annotated[
        str | None,
        "Message to add to changelog (optional)",
    ] = None,
    pr_number: Annotated[
        int | None,
        "PR number for changelog entry (optional)",
    ] = None,
    dry_run: Annotated[
        bool,
        "If True, show what would be changed without modifying files",
    ] = False,
) -> BumpVersionResponse:
    """Bump a connector's version across all relevant files.

    Updates version in metadata.yaml (always), pyproject.toml (if exists),
    and documentation changelog (if changelog_message provided).

    Either bump_type or new_version must be provided.

    RC bump types (patch_rc, minor_rc, major_rc) only work on non-RC versions.
    If the version is already an RC, use 'rc' to bump the RC number or 'promote' to finalize.
    """
    # Delegate to capability function (validation happens there)
    result = bump_connector_version(
        repo_path=repo_path,
        connector_name=connector_name,
        bump_type=bump_type,
        new_version=new_version,
        changelog_message=changelog_message,
        pr_number=pr_number,
        dry_run=dry_run,
    )

    return BumpVersionResponse(
        connector=result.connector,
        previous_version=result.previous_version,
        new_version=result.new_version,
        files_modified=result.files_modified,
        dry_run=result.dry_run,
    )


def register_github_repo_ops_tools(app: FastMCP) -> None:
    """Register GitHub repository operation tools with the FastMCP app.

    Args:
        app: FastMCP application instance
    """
    register_mcp_tools(app, mcp_module=__name__)
