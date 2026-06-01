# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tools for cloud connector version management.

This module exposes the connector version-override operations as MCP tools.
The tools are thin presentation-layer wrappers: they resolve auth from the
incoming `fastmcp.Context` and forward to the core
`airbyte_ops_mcp.cloud_admin.version_overrides` module which both the MCP
and CLI surfaces share.

## MCP reference

.. include:: ../../../docs/mcp-generated/cloud_connector_versions.md
    :start-line: 2
"""

# NOTE: We intentionally do NOT use `from __future__ import annotations` here.
# FastMCP has issues resolving forward references when PEP 563 deferred annotations
# are used. See: https://github.com/jlowin/fastmcp/issues/905
# Python 3.12+ supports modern type hint syntax natively, so this is not needed.

__all__: list[str] = []

import logging
from typing import Annotated, Literal

from fastmcp import Context, FastMCP
from fastmcp_extensions import get_mcp_config, mcp_tool, register_mcp_tools
from pydantic import Field

from airbyte_ops_mcp.cloud_admin.auth import CloudAuthError
from airbyte_ops_mcp.cloud_admin.models import (
    ConnectorVersionInfo,
    OrganizationVersionOverrideResult,
    VersionOverrideOperationResult,
    WorkspaceVersionOverrideResult,
)
from airbyte_ops_mcp.cloud_admin.version_overrides import (
    ResolvedCloudAuth,
    get_connector_version_info,
    set_actor_version_override,
    set_organization_version_override,
    set_workspace_version_override,
)
from airbyte_ops_mcp.constants import ServerConfigKey, WorkspaceAliasEnum
from airbyte_ops_mcp.tier_cache import TierFilter

logger = logging.getLogger(__name__)


def _resolve_cloud_auth(ctx: Context) -> ResolvedCloudAuth:
    """Resolve authentication credentials for Airbyte Cloud API from `ctx`.

    Credentials are resolved in priority order:

    1. Bearer token (`Authorization` header or `AIRBYTE_CLOUD_BEARER_TOKEN` env var)
    2. Client credentials (`X-Airbyte-Cloud-Client-Id`/`Secret` headers or env vars)

    Raises `CloudAuthError` if credentials cannot be resolved.
    """
    bearer_token = get_mcp_config(ctx, ServerConfigKey.BEARER_TOKEN)
    if bearer_token:
        return ResolvedCloudAuth(bearer_token=bearer_token)

    try:
        client_id = get_mcp_config(ctx, ServerConfigKey.CLIENT_ID)
        client_secret = get_mcp_config(ctx, ServerConfigKey.CLIENT_SECRET)
        return ResolvedCloudAuth(
            client_id=client_id,
            client_secret=client_secret,
        )
    except ValueError as e:
        raise CloudAuthError(
            f"Failed to resolve credentials. Ensure credentials are provided "
            f"via Authorization header (Bearer token), "
            f"HTTP headers (X-Airbyte-Cloud-Client-Id, X-Airbyte-Cloud-Client-Secret), "
            f"or environment variables. Error: {e}"
        ) from e


@mcp_tool(
    read_only=True,
    idempotent=True,
    open_world=True,
)
def get_cloud_connector_version(
    workspace_id: Annotated[
        str | WorkspaceAliasEnum,
        Field(
            description="The Airbyte Cloud workspace ID (UUID) or alias. "
            "Accepts '@devin-ai-sandbox' as an alias for the Devin AI sandbox workspace."
        ),
    ],
    actor_id: Annotated[
        str, "The ID of the deployed connector (source or destination)"
    ],
    actor_type: Annotated[
        Literal["source", "destination"],
        "The type of connector (source or destination)",
    ],
    config_api_root: Annotated[
        str | None,
        Field(
            description="Optional API root URL override for the Config API. "
            "Defaults to Airbyte Cloud (https://cloud.airbyte.com/api/v1). "
            "Use this to target local or self-hosted deployments.",
            default=None,
        ),
    ] = None,
    *,
    ctx: Context,
) -> ConnectorVersionInfo:
    """Get the current version information for a deployed connector.

    Returns version details including the current version string and whether
    an override (pin) is applied.

    Authentication credentials are resolved in priority order:

    1. Bearer token (Authorization header or AIRBYTE_CLOUD_BEARER_TOKEN env var)
    2. HTTP headers: X-Airbyte-Cloud-Client-Id, X-Airbyte-Cloud-Client-Secret
    3. Environment variables: AIRBYTE_CLOUD_CLIENT_ID, AIRBYTE_CLOUD_CLIENT_SECRET
    """
    resolved_workspace_id = WorkspaceAliasEnum.resolve(workspace_id)
    assert resolved_workspace_id is not None  # workspace_id is required

    return get_connector_version_info(
        auth=_resolve_cloud_auth(ctx),
        workspace_id=resolved_workspace_id,
        actor_id=actor_id,
        actor_type=actor_type,
        config_api_root=config_api_root,
    )


@mcp_tool(
    destructive=True,
    idempotent=False,
    open_world=True,
)
def set_cloud_connector_version_override(
    workspace_id: Annotated[
        str | WorkspaceAliasEnum,
        Field(
            description="The Airbyte Cloud workspace ID (UUID) or alias. "
            "Accepts '@devin-ai-sandbox' as an alias for the Devin AI sandbox workspace."
        ),
    ],
    actor_id: Annotated[
        str, "The ID of the deployed connector (source or destination)"
    ],
    actor_type: Annotated[
        Literal["source", "destination"],
        "The type of connector (source or destination)",
    ],
    approval_comment_url: Annotated[
        str | None,
        Field(
            description="URL to the Slack approval record. Obtain this by calling the "
            "`escalate_to_human` tool with `approval_requested=True`; the backend delivers "
            "the approval record URL when a human clicks Approve. "
            "Format: https://<workspace>.slack.com/archives/... "
            "The admin email is automatically resolved from the approver's identity "
            "via the team roster.",
            default=None,
        ),
    ],
    version: Annotated[
        str | None,
        Field(
            description="The semver version string to pin to (e.g., '0.1.0'). "
            "Must be None if unset is True.",
            default=None,
        ),
    ],
    unset: Annotated[
        bool,
        Field(
            description="If True, removes any existing version override. "
            "Cannot be True if version is provided.",
            default=False,
        ),
    ],
    override_reason: Annotated[
        str | None,
        Field(
            description="Required when setting a version. "
            "Explanation for the override (min 10 characters).",
            default=None,
        ),
    ],
    override_reason_reference_url: Annotated[
        str | None,
        Field(
            description="Optional URL with more context (e.g., issue link).",
            default=None,
        ),
    ],
    issue_url: Annotated[
        str | None,
        Field(
            description="URL to the GitHub issue providing context for this operation. "
            "Must be a valid GitHub URL (https://github.com/...). Required for authorization.",
            default=None,
        ),
    ],
    ai_agent_session_url: Annotated[
        str | None,
        Field(
            description="URL to the AI agent session driving this operation, if applicable. "
            "Provides additional auditability for AI-driven operations.",
            default=None,
        ),
    ] = None,
    force: Annotated[
        bool,
        Field(
            description="If `True`, allow overwriting an existing version pin. "
            "Existing pins may have been set by rollouts, breaking-change migrations, "
            "or other operators. Defaults to `False`. NOTE: `force=True` only "
            "bypasses the existing-pin check — major-version crossings are always "
            "blocked and cannot be overridden.",
            default=False,
        ),
    ] = False,
    config_api_root: Annotated[
        str | None,
        Field(
            description="Optional API root URL override for the Config API. "
            "Defaults to Airbyte Cloud (https://cloud.airbyte.com/api/v1). "
            "Use this to target local or self-hosted deployments.",
            default=None,
        ),
    ] = None,
    customer_tier_filter: Annotated[
        TierFilter,
        Field(
            description=(
                "Required tier filter: 'TIER_0', 'TIER_1', 'TIER_2', or 'ALL'. "
                "The operation will be rejected if the actual customer tier does not match. "
                "Use 'ALL' to proceed regardless of tier (a warning is shown for sensitive tiers)."
            ),
        ),
    ] = "TIER_2",
    *,
    ctx: Context,
) -> VersionOverrideOperationResult:
    """Set or clear a version override for a deployed connector.

    **Admin-only operation** - Requires:

    - AIRBYTE_INTERNAL_ADMIN_FLAG=airbyte.io environment variable
    - issue_url parameter (GitHub issue URL for context)
    - approval_comment_url (Slack approval record URL from `escalate_to_human`)

    The admin user email is automatically derived from the Slack approval record,
    resolving the approver's @airbyte.io email via the team roster.

    You must specify EXACTLY ONE of `version` OR `unset=True`, but not both.
    When setting a version, `override_reason` is required.

    The `customer_tier_filter` parameter gates the operation: the call fails if
    the actual tier of the workspace's organization does not match.  Use `ALL`
    to bypass the check (a warning is still emitted for sensitive tiers).

    Business rules enforced:

    - Dev versions (-dev): Only creator can unpin their own dev version override
    - Production versions: Require strong justification mentioning customer/support/investigation
    - Release candidates (-rc): Any admin can pin/unpin RC versions

    Authentication credentials are resolved in priority order:

    1. Bearer token (Authorization header or AIRBYTE_CLOUD_BEARER_TOKEN env var)
    2. HTTP headers: X-Airbyte-Cloud-Client-Id, X-Airbyte-Cloud-Client-Secret
    3. Environment variables: AIRBYTE_CLOUD_CLIENT_ID, AIRBYTE_CLOUD_CLIENT_SECRET
    """
    resolved_workspace_id = WorkspaceAliasEnum.resolve(workspace_id)
    assert resolved_workspace_id is not None  # workspace_id is required

    return set_actor_version_override(
        auth=_resolve_cloud_auth(ctx),
        workspace_id=resolved_workspace_id,
        actor_id=actor_id,
        actor_type=actor_type,
        approval_comment_url=approval_comment_url,
        version=version,
        unset=unset,
        override_reason=override_reason,
        override_reason_reference_url=override_reason_reference_url,
        issue_url=issue_url,
        ai_agent_session_url=ai_agent_session_url,
        customer_tier_filter=customer_tier_filter,
        force=force,
        config_api_root=config_api_root,
    )


@mcp_tool(
    destructive=True,
    idempotent=False,
    open_world=True,
)
def set_workspace_connector_version_override(
    workspace_id: Annotated[
        str | WorkspaceAliasEnum,
        Field(
            description="The Airbyte Cloud workspace ID (UUID) or alias. "
            "Accepts '@devin-ai-sandbox' as an alias for the Devin AI sandbox workspace."
        ),
    ],
    connector_name: Annotated[
        str,
        Field(
            description="The connector name (e.g., 'source-github', 'destination-bigquery')."
        ),
    ],
    connector_type: Annotated[
        Literal["source", "destination"],
        "The type of connector (source or destination)",
    ],
    approval_comment_url: Annotated[
        str | None,
        Field(
            description="URL to the Slack approval record. Obtain this by calling the "
            "`escalate_to_human` tool with `approval_requested=True`; the backend delivers "
            "the approval record URL when a human clicks Approve. "
            "Format: https://<workspace>.slack.com/archives/... "
            "The admin email is automatically resolved from the approver's identity "
            "via the team roster.",
            default=None,
        ),
    ],
    version: Annotated[
        str | None,
        Field(
            description="The semver version string to pin to (e.g., '0.1.0'). "
            "Must be None if unset is True.",
            default=None,
        ),
    ],
    unset: Annotated[
        bool,
        Field(
            description="If True, removes any existing version override. "
            "Cannot be True if version is provided.",
            default=False,
        ),
    ],
    override_reason: Annotated[
        str | None,
        Field(
            description="Required when setting a version. "
            "Explanation for the override (min 10 characters).",
            default=None,
        ),
    ],
    override_reason_reference_url: Annotated[
        str | None,
        Field(
            description="Optional URL with more context (e.g., issue link).",
            default=None,
        ),
    ],
    issue_url: Annotated[
        str | None,
        Field(
            description="URL to the GitHub issue providing context for this operation. "
            "Must be a valid GitHub URL (https://github.com/...). Required for authorization.",
            default=None,
        ),
    ],
    ai_agent_session_url: Annotated[
        str | None,
        Field(
            description="URL to the AI agent session driving this operation, if applicable. "
            "Provides additional auditability for AI-driven operations.",
            default=None,
        ),
    ] = None,
    force: Annotated[
        bool,
        Field(
            description="If `True`, allow overwriting an existing version pin. "
            "Existing pins may have been set by rollouts, breaking-change migrations, "
            "or other operators. Defaults to `False`. NOTE: `force=True` only "
            "bypasses the existing-pin check — major-version crossings are always "
            "blocked and cannot be overridden.",
            default=False,
        ),
    ] = False,
    config_api_root: Annotated[
        str | None,
        Field(
            description="Optional API root URL override for the Config API. "
            "Defaults to Airbyte Cloud (https://cloud.airbyte.com/api/v1). "
            "Use this to target local or self-hosted deployments.",
            default=None,
        ),
    ] = None,
    customer_tier_filter: Annotated[
        TierFilter,
        Field(
            description=(
                "Required tier filter: 'TIER_0', 'TIER_1', 'TIER_2', or 'ALL'. "
                "The operation will be rejected if the actual customer tier does not match. "
                "Use 'ALL' to proceed regardless of tier (a warning is shown for sensitive tiers)."
            ),
        ),
    ] = "TIER_2",
    *,
    ctx: Context,
) -> WorkspaceVersionOverrideResult:
    """Set or clear a workspace-level version override for a connector type.

    This pins ALL instances of a connector type within a workspace to a specific version.
    For example, pinning 'source-github' at workspace level means all GitHub sources
    in that workspace will use the pinned version.

    **Admin-only operation** - Requires:

    - AIRBYTE_INTERNAL_ADMIN_FLAG=airbyte.io environment variable
    - issue_url parameter (GitHub issue URL for context)
    - approval_comment_url (Slack approval record URL from `escalate_to_human`)

    You must specify EXACTLY ONE of `version` OR `unset=True`, but not both.
    When setting a version, `override_reason` is required.

    The `customer_tier_filter` parameter gates the operation: the call fails if
    the actual tier of the workspace's organization does not match.  Use `ALL`
    to bypass the check (a warning is still emitted for sensitive tiers).
    """
    resolved_workspace_id = WorkspaceAliasEnum.resolve(workspace_id)
    assert resolved_workspace_id is not None  # workspace_id is required

    return set_workspace_version_override(
        auth=_resolve_cloud_auth(ctx),
        workspace_id=resolved_workspace_id,
        connector_name=connector_name,
        connector_type=connector_type,
        approval_comment_url=approval_comment_url,
        version=version,
        unset=unset,
        override_reason=override_reason,
        override_reason_reference_url=override_reason_reference_url,
        issue_url=issue_url,
        ai_agent_session_url=ai_agent_session_url,
        customer_tier_filter=customer_tier_filter,
        force=force,
        config_api_root=config_api_root,
    )


@mcp_tool(
    destructive=True,
    idempotent=False,
    open_world=True,
)
def set_organization_connector_version_override(
    organization_id: Annotated[
        str,
        Field(description="The Airbyte Cloud organization ID."),
    ],
    connector_name: Annotated[
        str,
        Field(
            description="The connector name (e.g., 'source-github', 'destination-bigquery')."
        ),
    ],
    connector_type: Annotated[
        Literal["source", "destination"],
        "The type of connector (source or destination)",
    ],
    approval_comment_url: Annotated[
        str | None,
        Field(
            description="URL to the Slack approval record. Obtain this by calling the "
            "`escalate_to_human` tool with `approval_requested=True`; the backend delivers "
            "the approval record URL when a human clicks Approve. "
            "Format: https://<workspace>.slack.com/archives/... "
            "The admin email is automatically resolved from the approver's identity "
            "via the team roster.",
            default=None,
        ),
    ],
    version: Annotated[
        str | None,
        Field(
            description="The semver version string to pin to (e.g., '0.1.0'). "
            "Must be None if unset is True.",
            default=None,
        ),
    ],
    unset: Annotated[
        bool,
        Field(
            description="If True, removes any existing version override. "
            "Cannot be True if version is provided.",
            default=False,
        ),
    ],
    override_reason: Annotated[
        str | None,
        Field(
            description="Required when setting a version. "
            "Explanation for the override (min 10 characters).",
            default=None,
        ),
    ],
    override_reason_reference_url: Annotated[
        str | None,
        Field(
            description="Optional URL with more context (e.g., issue link).",
            default=None,
        ),
    ],
    issue_url: Annotated[
        str | None,
        Field(
            description="URL to the GitHub issue providing context for this operation. "
            "Must be a valid GitHub URL (https://github.com/...). Required for authorization.",
            default=None,
        ),
    ],
    ai_agent_session_url: Annotated[
        str | None,
        Field(
            description="URL to the AI agent session driving this operation, if applicable. "
            "Provides additional auditability for AI-driven operations.",
            default=None,
        ),
    ] = None,
    force: Annotated[
        bool,
        Field(
            description="If `True`, allow overwriting an existing version pin. "
            "Existing pins may have been set by rollouts, breaking-change migrations, "
            "or other operators. Defaults to `False`. NOTE: `force=True` only "
            "bypasses the existing-pin check — major-version crossings are always "
            "blocked and cannot be overridden.",
            default=False,
        ),
    ] = False,
    config_api_root: Annotated[
        str | None,
        Field(
            description="Optional API root URL override for the Config API. "
            "Defaults to Airbyte Cloud (https://cloud.airbyte.com/api/v1). "
            "Use this to target local or self-hosted deployments.",
            default=None,
        ),
    ] = None,
    customer_tier_filter: Annotated[
        TierFilter,
        Field(
            description=(
                "Required tier filter: 'TIER_0', 'TIER_1', 'TIER_2', or 'ALL'. "
                "The operation will be rejected if the actual customer tier does not match. "
                "Use 'ALL' to proceed regardless of tier (a warning is shown for sensitive tiers)."
            ),
        ),
    ] = "TIER_2",
    *,
    ctx: Context,
) -> OrganizationVersionOverrideResult:
    """Set or clear an organization-level version override for a connector type.

    This pins ALL instances of a connector type across an entire organization to a
    specific version. For example, pinning 'source-github' at organization level means
    all GitHub sources in all workspaces within that organization will use the pinned version.

    **Admin-only operation** - Requires:

    - AIRBYTE_INTERNAL_ADMIN_FLAG=airbyte.io environment variable
    - issue_url parameter (GitHub issue URL for context)
    - approval_comment_url (Slack approval record URL from `escalate_to_human`)

    You must specify EXACTLY ONE of `version` OR `unset=True`, but not both.
    When setting a version, `override_reason` is required.

    The `customer_tier_filter` parameter gates the operation: the call fails if
    the actual tier of the organization does not match.  Use `ALL` to bypass
    the check (a warning is still emitted for sensitive tiers).
    """
    return set_organization_version_override(
        auth=_resolve_cloud_auth(ctx),
        organization_id=organization_id,
        connector_name=connector_name,
        connector_type=connector_type,
        approval_comment_url=approval_comment_url,
        version=version,
        unset=unset,
        override_reason=override_reason,
        override_reason_reference_url=override_reason_reference_url,
        issue_url=issue_url,
        ai_agent_session_url=ai_agent_session_url,
        customer_tier_filter=customer_tier_filter,
        force=force,
        config_api_root=config_api_root,
    )


def register_cloud_connector_version_tools(app: FastMCP) -> None:
    """Register cloud connector version management tools with the FastMCP app."""
    register_mcp_tools(app, mcp_module=__name__)
