# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tools for the connector registry and monorepo catalog: registry reads/yank plus repo connector listing and version bumps.

## MCP reference

.. include:: ../../../docs/mcp-generated/connector_registry.md
    :start-line: 2
"""

from __future__ import annotations

__all__: list[str] = []

from typing import Annotated, Any, Literal

from fastmcp import FastMCP
from fastmcp_extensions import mcp_tool, register_mcp_tools
from pydantic import BaseModel, Field

from airbyte_ops_mcp.airbyte_repo.bump_version import bump_connector_version
from airbyte_ops_mcp.airbyte_repo.list_connectors import list_connectors
from airbyte_ops_mcp.airbyte_repo.utils import resolve_diff_range
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
    resolve_registry_store,
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
from airbyte_ops_mcp.registry.registry_store_base import get_registry


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


class YankedVersionEntry(BaseModel):
    """A single yanked connector version discovered from its marker file."""

    connector_name: str = Field(description="The connector technical name")
    version: str = Field(description="The yanked version tag")
    yanked_at: str = Field(description="When the version was yanked, if recorded")
    reason: str = Field(description="Reason recorded in the yank marker, if any")
    approval_url: str = Field(description="Approval evidence URL, if recorded")


class YankedVersionsResult(BaseModel):
    """Result of listing yanked connector versions in a registry store."""

    store: str = Field(description="The store target that was read")
    bucket_name: str = Field(description="The resolved GCS bucket name")
    count: int = Field(description="Number of yanked versions found")
    yanked_versions: list[YankedVersionEntry] = Field(
        description="Yanked versions, sorted by connector name then version"
    )


class YankDetailResult(BaseModel):
    """Active yank-marker detail for a single connector version."""

    connector_name: str = Field(description="The connector technical name")
    version: str = Field(description="The version that was checked")
    store: str = Field(description="The store target that was read")
    bucket_name: str = Field(description="The resolved GCS bucket name")
    yanked: bool = Field(
        description="True when an active `version-yank.yml` marker exists"
    )
    yanked_at: str = Field(description="When the version was yanked, if recorded")
    reason: str = Field(description="Reason recorded in the yank marker, if any")
    approval_url: str = Field(description="Approval evidence URL, if recorded")


@mcp_tool(
    read_only=True,
    idempotent=True,
    open_world=True,
)
def list_yanked_connector_versions(
    store: Annotated[
        str,
        "Store target to read (e.g. 'coral:prod', 'coral:dev'). Defaults to 'coral:prod'.",
    ] = "coral:prod",
) -> YankedVersionsResult:
    """List every yanked connector version in a registry store.

    Returns one entry per active `version-yank.yml` marker, sorted by connector
    name then version, with each marker's `yanked_at`, `reason`, and
    `approval_url` populated. Historical `version-unyanked-*.yml` audit markers
    are ignored — only live markers count.

    Requires GCS_CREDENTIALS environment variable to be set.
    """
    registry = get_registry(resolve_registry_store(store=store))
    yanked = registry.list_yanked_versions()
    return YankedVersionsResult(
        store=store,
        bucket_name=registry.bucket_name,
        count=len(yanked),
        yanked_versions=[
            YankedVersionEntry(
                connector_name=item.connector_name,
                version=item.version,
                yanked_at=item.yanked_at,
                reason=item.reason,
                approval_url=item.approval_url,
            )
            for item in yanked
        ],
    )


@mcp_tool(
    read_only=True,
    idempotent=True,
    open_world=True,
)
def get_connector_version_yank_detail(
    connector_name: Annotated[
        str,
        "The connector name (e.g., 'source-faker', 'destination-postgres').",
    ],
    version: Annotated[
        str,
        "Version to inspect (e.g., '1.2.3').",
    ],
    store: Annotated[
        str,
        "Store target to read (e.g. 'coral:prod', 'coral:dev'). Defaults to 'coral:prod'.",
    ] = "coral:prod",
) -> YankDetailResult:
    """Read the active yank marker for a single connector version.

    Returns `yanked=True` with the marker's `yanked_at`, `reason`, and
    `approval_url` when the version currently has an active `version-yank.yml`
    marker, or `yanked=False` with empty fields when it is not yanked.
    Historical `version-unyanked-*.yml` audit markers are ignored.

    Requires GCS_CREDENTIALS environment variable to be set.
    """
    registry = get_registry(resolve_registry_store(store=store))
    marker = registry.get_yank_marker(connector_name=connector_name, version=version)
    return YankDetailResult(
        connector_name=connector_name,
        version=version,
        store=store,
        bucket_name=registry.bucket_name,
        yanked=marker is not None,
        yanked_at=marker.yanked_at if marker else "",
        reason=marker.reason if marker else "",
        approval_url=marker.approval_url if marker else "",
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
    requires_client_filesystem=True,
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
    requires_client_filesystem=True,
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


def register_connector_registry_tools(app: FastMCP) -> None:
    """Register connector_registry tools with the FastMCP app."""
    register_mcp_tools(app, mcp_module=__name__)
