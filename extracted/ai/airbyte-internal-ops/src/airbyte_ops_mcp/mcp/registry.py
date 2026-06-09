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

from airbyte_ops_mcp.approval_resolution import (
    ApprovalResolutionError,
    resolve_admin_email_from_approval,
)
from airbyte_ops_mcp.github_actions import trigger_workflow_dispatch
from airbyte_ops_mcp.github_api import resolve_ci_trigger_github_token
from airbyte_ops_mcp.human_in_the_loop import APPROVAL_REQUEST_SUMMARY_MAX_LENGTH
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
YANK_WORKFLOW_REPO_NAME = "airbyte"
YANK_WORKFLOW_DEFAULT_BRANCH = "master"
YANK_WORKFLOW_FILE = "version-yank-command.yml"


class YankConnectorVersionResponse(BaseModel):
    """Response from triggering a yank connector version workflow."""

    approval_required: bool = Field(
        default=False,
        description=(
            "Whether the operation still requires Slack/HITL approval before dispatch."
        ),
    )
    message: str = Field(description="Human-readable status message")
    approval_request_summary: str | None = Field(
        default=None,
        description=(
            "Short approval summary to pass to `escalate_to_human` when approval is required."
        ),
    )
    approval_request_message: str | None = Field(
        default=None,
        description=(
            "Detailed Slack message to pass to `escalate_to_human` when approval is required."
        ),
    )
    approved_by: str | None = Field(
        default=None,
        description="Resolved `@airbyte.io` email for the Slack approver.",
    )
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


def _format_yank_action(unyank: bool) -> str:
    """Return the registry action label for a yank tool call."""
    return "unyank" if unyank else "yank"


def _sanitize_approval_request_summary_text(value: str) -> str:
    """Return text safe for Slack approval request formatting."""
    return value.replace("`", "'")


def _build_yank_approval_request_summary(
    *,
    connector_name: str,
    version: str,
    store: str,
    reason: str,
    unyank: bool,
) -> str:
    """Build a Slack confirmation summary for registry yank approval."""
    action = _format_yank_action(unyank)
    sanitized_connector_name = _sanitize_approval_request_summary_text(connector_name)
    sanitized_version = _sanitize_approval_request_summary_text(version)
    sanitized_store = _sanitize_approval_request_summary_text(store)
    summary = (
        f"{action} {sanitized_connector_name}@{sanitized_version} in "
        f"{sanitized_store}; registry will be recompiled"
    )
    if reason:
        sanitized_reason = _sanitize_approval_request_summary_text(reason)
        summary = f"{summary}; reason: {sanitized_reason}"
    if len(summary) <= APPROVAL_REQUEST_SUMMARY_MAX_LENGTH:
        return summary
    return f"{summary[: APPROVAL_REQUEST_SUMMARY_MAX_LENGTH - 3].rstrip()}..."


def _build_yank_approval_request_message(
    *,
    connector_name: str,
    version: str,
    store: str,
    reason: str,
    unyank: bool,
) -> str:
    """Build the Slack message body for registry yank approval."""
    action = _format_yank_action(unyank)
    sanitized_connector_name = _sanitize_approval_request_summary_text(connector_name)
    sanitized_version = _sanitize_approval_request_summary_text(version)
    sanitized_store = _sanitize_approval_request_summary_text(store)
    reason_text = (
        _sanitize_approval_request_summary_text(reason) if reason else "(none provided)"
    )
    return (
        "Approval requested for an MCP registry connector-version operation.\n\n"
        f"- Action: `{action}`\n"
        f"- Connector: `{sanitized_connector_name}`\n"
        f"- Version: `{sanitized_version}`\n"
        f"- Store: `{sanitized_store}`\n"
        f"- Reason: {reason_text}\n"
        "- Consequence: after approval, the MCP tool will dispatch "
        "`airbyte/.github/workflows/version-yank-command.yml`; that workflow "
        "will update the yank marker and run `airbyte-ops registry store compile`, "
        "recompiling registry indexes and latest pointers.\n\n"
        "After Slack approval, copy the Slack approval record URL into "
        "`approval_comment_url` and call `yank_connector_version` again with "
        "the same connector name, version, store, reason, and unyank values."
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
    approval_comment_url: Annotated[
        str | None,
        Field(
            description=(
                "Slack approval record URL. Obtain this by calling "
                "`escalate_to_human` with `approval_requested=True` using the "
                "approval request details returned by this tool. The backend "
                "validates the approval record and resolves the approver's "
                "`@airbyte.io` email before dispatching the registry workflow."
            ),
            default=None,
        ),
    ] = None,
) -> YankConnectorVersionResponse:
    """Yank or unyank a connector version after Slack/HITL approval.

    This MCP tool requires approval for all stores, including dev/test stores,
    so the safety behavior is consistent and prod-impacting `coral:prod`
    requests cannot dispatch without approval.

    Without `approval_comment_url`, returns the exact approval request summary
    and Slack message to send via `escalate_to_human`; no GitHub Actions
    workflow is triggered. With an approved Slack record URL, validates the
    approver and then triggers a workflow that marks the version as yanked
    (or unyanked) and recompiles the registry to update indexes and latest
    pointers.

    Requires GITHUB_CI_WORKFLOW_TRIGGER_PAT or GITHUB_TOKEN environment variable
    with 'actions:write' permission.
    """
    action = _format_yank_action(unyank)
    action_title = action.capitalize()

    approval_request_summary = _build_yank_approval_request_summary(
        connector_name=connector_name,
        version=version,
        store=store,
        reason=reason,
        unyank=unyank,
    )
    approval_request_message = _build_yank_approval_request_message(
        connector_name=connector_name,
        version=version,
        store=store,
        reason=reason,
        unyank=unyank,
    )

    if not approval_comment_url:
        return YankConnectorVersionResponse(
            approval_required=True,
            message=(
                f"Slack/HITL approval is required before dispatching the {action} "
                f"workflow for {connector_name}@{version} on {store}. Call "
                "`escalate_to_human` with `approval_requested=True`, "
                "`request_type='approval'`, the returned "
                "`approval_request_summary`, and the returned "
                "`approval_request_message`. After approval, call this tool "
                "again with the Slack approval record URL as `approval_comment_url`."
            ),
            approval_request_summary=approval_request_summary,
            approval_request_message=approval_request_message,
        )

    try:
        approved_by = resolve_admin_email_from_approval(
            approval_comment_url=approval_comment_url,
        )
    except ApprovalResolutionError as e:
        return YankConnectorVersionResponse(
            approval_required=True,
            message=str(e),
            approval_request_summary=approval_request_summary,
            approval_request_message=approval_request_message,
        )

    try:
        token = resolve_ci_trigger_github_token()
    except ValueError as e:
        return YankConnectorVersionResponse(
            message=str(e),
            approved_by=approved_by,
        )

    workflow_inputs: dict[str, str] = {
        "connector-name": connector_name,
        "version": version,
        "store": store,
        "unyank": str(unyank).lower(),
        "approval-url": approval_comment_url,
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
            f"{action_title} workflow triggered for {connector_name}@{version} "
            f"on {store}{reason_info} after approval by {approved_by}. "
            f"View progress at: {view_url}"
        ),
        approved_by=approved_by,
        workflow_url=dispatch_result.workflow_url,
        github_run_id=dispatch_result.run_id,
        github_run_url=dispatch_result.run_url,
    )


def register_registry_tools(app: FastMCP) -> None:
    """Register registry tools with the FastMCP app."""
    register_mcp_tools(app, mcp_module=__name__)
