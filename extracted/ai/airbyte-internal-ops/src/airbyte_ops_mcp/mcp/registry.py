# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tools for connector registry operations.

This module provides MCP tools for interacting with the Airbyte connector registry
stored in Google Cloud Storage, including:
- Reading connector metadata and specs
- Listing connectors and versions
- Yanking connector versions (workflow-backed)

## MCP reference

.. include:: ../../../docs/mcp-generated/registry.md
    :start-line: 2
"""

from __future__ import annotations

__all__: list[str] = []

from typing import Annotated, Any

from fastmcp import FastMCP
from fastmcp_extensions import mcp_tool, register_mcp_tools
from pydantic import BaseModel, Field

from airbyte_ops_mcp.github_actions import trigger_workflow_dispatch
from airbyte_ops_mcp.github_api import resolve_ci_trigger_github_token
from airbyte_ops_mcp.registry import (
    PROD_METADATA_SERVICE_BUCKET_NAME,
    ConnectorListResult,
    RegistryEntryResult,
    VersionListResult,
)
from airbyte_ops_mcp.registry._enums import (
    ConnectorLanguage,
    ConnectorType,
    SupportLevel,
)
from airbyte_ops_mcp.registry.operations import (
    get_registry_entry,
    get_registry_spec,
    list_connector_versions,
    list_registry_connectors,
    list_registry_connectors_filtered,
)


class RegistrySpecResult(BaseModel):
    """Result of reading a connector spec from GCS."""

    connector_name: str = Field(description="The connector technical name")
    version: str = Field(description="The version that was read")
    bucket_name: str = Field(description="The GCS bucket name")
    gcs_path: str = Field(description="The GCS path that was read")
    spec: dict[str, Any] = Field(description="The connector spec dictionary")


@mcp_tool(
    read_only=True,
    idempotent=True,
    open_world=True,
)
def get_connector_registry_entry(
    connector_name: Annotated[
        str,
        "The connector name (e.g., 'source-faker', 'destination-postgres')",
    ],
    version: Annotated[
        str,
        "Version to read (e.g., 'latest', '1.2.3'). Defaults to 'latest'.",
    ] = "latest",
) -> RegistryEntryResult:
    """Read a connector's metadata from the GCS registry.

    Returns the full metadata.yaml content for a connector at the specified version.
    Requires GCS_CREDENTIALS environment variable to be set.
    """
    bucket_name = PROD_METADATA_SERVICE_BUCKET_NAME
    metadata = get_registry_entry(
        connector_name=connector_name,
        bucket_name=bucket_name,
        version=version,
    )
    gcs_path = f"metadata/airbyte/{connector_name}/{version}/metadata.yaml"
    return RegistryEntryResult(
        connector_name=connector_name,
        version=version,
        bucket_name=bucket_name,
        gcs_path=gcs_path,
        metadata=metadata,
    )


@mcp_tool(
    read_only=True,
    idempotent=True,
    open_world=True,
)
def get_connector_registry_spec(
    connector_name: Annotated[
        str,
        "The connector name (e.g., 'source-faker', 'destination-postgres')",
    ],
    version: Annotated[
        str,
        "Version to read (e.g., 'latest', '1.2.3'). Defaults to 'latest'.",
    ] = "latest",
) -> RegistrySpecResult:
    """Read a connector's spec from the GCS registry.

    Returns the spec.json content for a connector at the specified version.
    Requires GCS_CREDENTIALS environment variable to be set.
    """
    bucket_name = PROD_METADATA_SERVICE_BUCKET_NAME
    spec = get_registry_spec(
        connector_name=connector_name,
        bucket_name=bucket_name,
        version=version,
    )
    gcs_path = f"metadata/airbyte/{connector_name}/{version}/spec.json"
    return RegistrySpecResult(
        connector_name=connector_name,
        version=version,
        bucket_name=bucket_name,
        gcs_path=gcs_path,
        spec=spec,
    )


@mcp_tool(
    read_only=True,
    idempotent=True,
    open_world=True,
)
def list_connectors_in_registry(
    certified: Annotated[
        bool,
        "When `True`, return only certified connectors. Shorthand for `support_level='certified'`.",
    ] = False,
    support_level: Annotated[
        str,
        "Exact support level to match (e.g., `certified`, `community`, `archived`). Empty string means no filter.",
    ] = "",
    min_support_level: Annotated[
        str,
        "Minimum support level threshold (inclusive). Levels: `archived` < `community` < `certified`. Empty string means no filter.",
    ] = "",
    connector_type: Annotated[
        str,
        "Filter by connector type: `source` or `destination`. Empty string means no filter.",
    ] = "",
    language: Annotated[
        str,
        "Filter by implementation language (e.g., `python`, `java`, `manifest-only`). Empty string means no filter.",
    ] = "",
) -> ConnectorListResult:
    """List connectors in the GCS registry with optional filtering.

    When filters are applied, reads the compiled `cloud_registry.json` index
    for fast lookups. Without filters, falls back to scanning individual
    metadata blobs (captures all connectors including OSS-only).

    Requires GCS_CREDENTIALS environment variable to be set.
    """
    bucket_name = PROD_METADATA_SERVICE_BUCKET_NAME

    # Normalise empty strings to typed enums or `None` for downstream logic.
    eff_support_level: SupportLevel | None = (
        SupportLevel.parse(support_level) if support_level else None
    )
    eff_min_support_level: SupportLevel | None = (
        SupportLevel.parse(min_support_level) if min_support_level else None
    )
    eff_connector_type: ConnectorType | None = (
        ConnectorType.parse(connector_type) if connector_type else None
    )
    eff_language: ConnectorLanguage | None = (
        ConnectorLanguage.parse(language) if language else None
    )

    # `certified=True` is sugar for `support_level="certified"`.
    if certified:
        if eff_support_level and eff_support_level != SupportLevel.CERTIFIED:
            raise ValueError(
                "`certified=True` conflicts with `support_level="
                f"{eff_support_level!r}`. Use one or the other."
            )
        eff_support_level = SupportLevel.CERTIFIED

    has_filters = any(
        [eff_support_level, eff_min_support_level, eff_connector_type, eff_language]
    )

    if has_filters:
        connectors = list_registry_connectors_filtered(
            bucket_name=bucket_name,
            support_level=eff_support_level,
            min_support_level=eff_min_support_level,
            connector_type=eff_connector_type,
            language=eff_language,
        )
    else:
        connectors = list_registry_connectors(bucket_name=bucket_name)

    return ConnectorListResult(
        bucket_name=bucket_name,
        connector_count=len(connectors),
        connectors=connectors,
    )


@mcp_tool(
    read_only=True,
    idempotent=True,
    open_world=True,
)
def list_connector_versions_in_registry(
    connector_name: Annotated[
        str,
        "The connector name (e.g., 'source-faker', 'destination-postgres')",
    ],
) -> VersionListResult:
    """List all versions of a connector in the GCS registry.

    Returns all published versions for a connector (excluding 'latest' and 'release_candidate').
    Requires GCS_CREDENTIALS environment variable to be set.
    """
    bucket_name = PROD_METADATA_SERVICE_BUCKET_NAME
    versions = list_connector_versions(
        connector_name=connector_name,
        bucket_name=bucket_name,
    )
    return VersionListResult(
        connector_name=connector_name,
        bucket_name=bucket_name,
        version_count=len(versions),
        versions=versions,
    )


# =============================================================================
# Yank Workflow Configuration
# =============================================================================

YANK_WORKFLOW_REPO_OWNER = "airbytehq"
YANK_WORKFLOW_REPO_NAME = "airbyte-ops-mcp"
YANK_WORKFLOW_DEFAULT_BRANCH = "main"
YANK_WORKFLOW_FILE = "registry-yank.yml"


class YankConnectorVersionResponse(BaseModel):
    """Response from triggering a yank connector version workflow."""

    message: str = Field(description="Human-readable status message")
    workflow_url: str | None = Field(
        default=None,
        description="URL to view the GitHub Actions workflow file",
    )
    github_run_id: int | None = Field(
        default=None,
        description="GitHub Actions workflow run ID (use with check_ci_workflow_status)",
    )
    github_run_url: str | None = Field(
        default=None,
        description="Direct URL to the GitHub Actions workflow run",
    )


@mcp_tool(
    read_only=False,
    idempotent=False,
    open_world=True,
)
def yank_connector_version(
    connector_name: Annotated[
        str,
        "Connector name (e.g., 'source-faker', 'destination-postgres').",
    ],
    version: Annotated[
        str,
        "Version to yank (e.g., '1.2.3').",
    ],
    store: Annotated[
        str,
        "Store target (e.g., 'coral:dev', 'coral:prod').",
    ],
    reason: Annotated[
        str,
        "Reason for yanking this version.",
    ] = "",
    unyank: Annotated[
        bool,
        "Set to true to unyank (restore) the version instead of yanking it.",
    ] = False,
) -> YankConnectorVersionResponse:
    """Yank or unyank a connector version and recompile the registry via GitHub Actions.

    Triggers a workflow that marks the version as yanked (or unyanked) and then
    recompiles the registry to update indexes and latest pointers.

    Returns immediately with a workflow URL. Use check_ci_workflow_status to monitor
    progress.

    Requires GITHUB_CI_WORKFLOW_TRIGGER_PAT or GITHUB_TOKEN environment variable
    with 'actions:write' permission.
    """
    try:
        token = resolve_ci_trigger_github_token()
    except ValueError as e:
        return YankConnectorVersionResponse(
            message=str(e),
        )

    action = "Unyank" if unyank else "Yank"
    workflow_inputs: dict[str, str] = {
        "connector_name": connector_name,
        "version": version,
        "store": store,
        "unyank": str(unyank).lower(),
    }
    if reason:
        workflow_inputs["reason"] = reason

    dispatch_result = trigger_workflow_dispatch(
        owner=YANK_WORKFLOW_REPO_OWNER,
        repo=YANK_WORKFLOW_REPO_NAME,
        workflow_file=YANK_WORKFLOW_FILE,
        ref=YANK_WORKFLOW_DEFAULT_BRANCH,
        inputs=workflow_inputs,
        token=token,
    )

    view_url = dispatch_result.run_url or dispatch_result.workflow_url
    reason_info = f" (reason: {reason})" if reason else ""
    return YankConnectorVersionResponse(
        message=(
            f"{action} workflow triggered for {connector_name}@{version} "
            f"on {store}{reason_info}. View progress at: {view_url}"
        ),
        workflow_url=dispatch_result.workflow_url,
        github_run_id=dispatch_result.run_id,
        github_run_url=dispatch_result.run_url,
    )


def register_registry_tools(app: FastMCP) -> None:
    """Register registry tools with the FastMCP app."""
    register_mcp_tools(app, mcp_module=__name__)
