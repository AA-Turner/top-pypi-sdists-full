# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tools for connector version lifecycle: cloud version overrides, progressive rollouts, and pre-release publishing.

## MCP reference

.. include:: ../../../docs/mcp-generated/connector_versions.md
    :start-line: 2
"""

# NOTE: We intentionally do NOT use `from __future__ import annotations` here.
# FastMCP has issues resolving forward references when PEP 563 deferred annotations
# are used. See: https://github.com/jlowin/fastmcp/issues/905
# Python 3.12+ supports modern type hint syntax natively, so this is not needed.

__all__: list[str] = []

import base64
import logging
from dataclasses import dataclass
from enum import StrEnum
from typing import Annotated, Literal

import requests
import yaml
from airbyte import constants
from airbyte.exceptions import PyAirbyteInputError
from fastmcp import Context, FastMCP
from fastmcp_extensions import get_mcp_config, mcp_tool, register_mcp_tools
from pydantic import BaseModel, Field

from airbyte_ops_mcp.airbyte_repo.bump_version import strip_prerelease_suffix
from airbyte_ops_mcp.approval_resolution import (
    ApprovalStatus,
    check_approval_status,
)
from airbyte_ops_mcp.cloud_admin import api_client
from airbyte_ops_mcp.cloud_admin.auth import (
    CloudAuthError,
    require_internal_admin_flag_only,
)
from airbyte_ops_mcp.cloud_admin.models import (
    ConnectorRolloutFinalizeResult,
    ConnectorRolloutProgressResult,
    ConnectorRolloutStartResult,
    ConnectorVersionInfo,
    OrganizationVersionOverrideResult,
    VersionOverrideOperationResult,
    WorkspaceVersionOverrideResult,
)
from airbyte_ops_mcp.cloud_admin.version_overrides import (
    VersionOverrideTarget,
    get_connector_version_info,
    set_version_override,
)
from airbyte_ops_mcp.connector_ops.rollouts._helpers import (
    count_eligible_or_pinned_actors,
)
from airbyte_ops_mcp.constants import ServerConfigKey, WorkspaceAliasEnum
from airbyte_ops_mcp.github_actions import trigger_workflow_dispatch
from airbyte_ops_mcp.github_api import (
    GITHUB_API_BASE,
    get_pr_head_ref,
    resolve_ci_trigger_github_token,
)
from airbyte_ops_mcp.mcp.cloud_auth import resolve_cloud_auth
from airbyte_ops_mcp.tier_cache import TierFilter, resolve_workspace

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class _ResolvedCloudAuth:
    """Resolved authentication for Airbyte Cloud API calls.

    Either bearer_token OR (client_id AND client_secret) will be set, not both.
    """

    bearer_token: str | None = None
    client_id: str | None = None
    client_secret: str | None = None


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
        auth=resolve_cloud_auth(ctx),
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
                "Required tier filter: 'TIER_0', 'TIER_1', 'TIER_2', 'UNKNOWN', or 'ALL'. "
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

    ws_resolution = resolve_workspace(
        workspace_id=resolved_workspace_id,
        allow_degraded=True,
    )
    if not ws_resolution.organization_id:
        return VersionOverrideOperationResult(
            success=False,
            message="Could not resolve organization for workspace.",
            connector_id=actor_id,
            connector_type=actor_type,
        )

    result = set_version_override(
        auth=resolve_cloud_auth(ctx),
        target=VersionOverrideTarget(
            scope="actor",
            organization_id=ws_resolution.organization_id,
            workspace_id=resolved_workspace_id,
            actor_id=actor_id,
            connector_type=actor_type,
        ),
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
    assert isinstance(result, VersionOverrideOperationResult)
    return result


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
                "Required tier filter: 'TIER_0', 'TIER_1', 'TIER_2', 'UNKNOWN', or 'ALL'. "
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

    ws_resolution = resolve_workspace(
        workspace_id=resolved_workspace_id,
        allow_degraded=True,
    )
    if not ws_resolution.organization_id:
        return WorkspaceVersionOverrideResult(
            success=False,
            message="Could not resolve organization for workspace.",
            workspace_id=resolved_workspace_id,
            connector_name=connector_name,
            connector_type=connector_type,
        )

    result = set_version_override(
        auth=resolve_cloud_auth(ctx),
        target=VersionOverrideTarget(
            scope="workspace",
            organization_id=ws_resolution.organization_id,
            workspace_id=resolved_workspace_id,
            connector_name=connector_name,
            connector_type=connector_type,
        ),
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
    assert isinstance(result, WorkspaceVersionOverrideResult)
    return result


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
                "Required tier filter: 'TIER_0', 'TIER_1', 'TIER_2', 'UNKNOWN', or 'ALL'. "
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
    result = set_version_override(
        auth=resolve_cloud_auth(ctx),
        target=VersionOverrideTarget(
            scope="organization",
            organization_id=organization_id,
            connector_name=connector_name,
            connector_type=connector_type,
        ),
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
    assert isinstance(result, OrganizationVersionOverrideResult)
    return result


def _resolve_cloud_auth(ctx: Context) -> _ResolvedCloudAuth:
    """Resolve authentication credentials for Airbyte Cloud API.

    Credentials are resolved in priority order:
    1. Bearer token (Authorization header or AIRBYTE_CLOUD_BEARER_TOKEN env var)
    2. Client credentials (X-Airbyte-Cloud-Client-Id/Secret headers or env vars)

    Args:
        ctx: FastMCP Context object from the current tool invocation.

    Returns:
        `_ResolvedCloudAuth` with either bearer_token or client credentials set.

    Raises:
        CloudAuthError: If credentials cannot be resolved from headers or env vars.
    """
    # Try bearer token first (preferred, but not required)
    bearer_token = get_mcp_config(ctx, ServerConfigKey.BEARER_TOKEN)
    if bearer_token:
        return _ResolvedCloudAuth(bearer_token=bearer_token)

    # Fall back to client credentials
    try:
        client_id = get_mcp_config(ctx, ServerConfigKey.CLIENT_ID)
        client_secret = get_mcp_config(ctx, ServerConfigKey.CLIENT_SECRET)
        return _ResolvedCloudAuth(
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
    destructive=True,
    idempotent=False,
    open_world=True,
)
def start_connector_rollout(
    docker_repository: Annotated[
        str,
        Field(description="The docker repository (e.g., 'airbyte/source-pokeapi')"),
    ],
    docker_image_tag: Annotated[
        str,
        Field(description="The docker image tag (e.g., '0.3.48-rc.1')"),
    ],
    actor_definition_id: Annotated[
        str,
        Field(description="The actor definition ID (UUID)"),
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
    admin_user_email_override: Annotated[
        str | None,
        Field(
            description="Direct admin email override for webapp-initiated actions. "
            "When the Ops Webapp env var is set, this bypasses the approval URL "
            "requirement. Ignored in agent/cron environments.",
            default=None,
        ),
    ],
    rollout_strategy: Annotated[
        Literal["manual", "automated", "overridden"],
        Field(
            description="The rollout strategy: "
            "'manual' for manual control of rollout progression, "
            "'automated' for automatic progression based on metrics, "
            "'overridden' for special cases where normal rules are bypassed.",
            default="manual",
        ),
    ],
    initial_rollout_pct: Annotated[
        int | None,
        Field(
            description="Initial/step percentage for rollout progression (0-100). "
            "For automated rollouts, this is the percentage increment per step. "
            "For example, 25 means the rollout will advance by 25% each step. "
            "Default is 25% if not specified.",
            default=None,
        ),
    ],
    final_target_rollout_pct: Annotated[
        int | None,
        Field(
            description="Maximum percentage of actors to pin (0-100). "
            "The rollout will not exceed this percentage. "
            "For example, 50 means at most 50% of actors will be pinned to the RC. "
            "Default is 50% if not specified.",
            default=None,
        ),
    ],
    customer_tier: Annotated[
        Literal["TIER_0", "TIER_1", "TIER_2", "ALL"] | None,
        Field(
            description="The customer tier to target for this rollout. "
            "Each tier represents a different group of customers: "
            "'TIER_0' for the highest-priority customers, "
            "'TIER_1' for mid-tier customers, "
            "'TIER_2' for the broadest customer group (default if not specified), "
            "'ALL' to target all customer tiers. "
            "When not specified, the platform defaults to TIER_2 only.",
            default=None,
        ),
    ],
    *,
    ctx: Context,
) -> ConnectorRolloutStartResult:
    """Start or configure a connector rollout workflow.

    This tool configures and starts a connector rollout workflow. It can be called
    multiple times while the rollout is in INITIALIZED state to update the configuration
    (strategy, percentages). Once the Temporal workflow starts and the state transitions
    to WORKFLOW_STARTED, the configuration is locked and cannot be changed.

    **Behavior:**
    - If rollout is INITIALIZED: Updates configuration and starts the workflow
    - If rollout is already started: Returns an error (configuration is locked)

    **Configuration Parameters:**
    - rollout_strategy: 'manual' (default), 'automated', or 'overridden'
    - initial_rollout_pct: Step size for progression (default: 25%)
    - final_target_rollout_pct: Maximum percentage to pin (default: 50%)
    - customer_tier: Customer tier to target - 'TIER_0', 'TIER_1', 'TIER_2', or 'ALL' (default: TIER_2)

    **Admin-only operation** - Requires:
    - AIRBYTE_INTERNAL_ADMIN_FLAG=airbyte.io environment variable
    - `approval_comment_url` (Slack approval record URL from `escalate_to_human`),
      OR `admin_user_email_override` when running inside the Ops Webapp.
    """
    # Validate admin access (check env var flag)
    try:
        require_internal_admin_flag_only()
    except CloudAuthError as e:
        return ConnectorRolloutStartResult(
            success=False,
            message=f"Admin authentication failed: {e}",
            docker_repository=docker_repository,
            docker_image_tag=docker_image_tag,
            actor_definition_id=actor_definition_id,
        )

    # Resolve admin email: webapp bypass or external approval URL
    approval = check_approval_status(
        approval_comment_url=approval_comment_url,
        user_email=admin_user_email_override,
    )
    if approval.status != ApprovalStatus.APPROVED:
        return ConnectorRolloutStartResult(
            success=False,
            message=approval.reason or "Approval check failed",
            docker_repository=docker_repository,
            docker_image_tag=docker_image_tag,
            actor_definition_id=actor_definition_id,
        )
    admin_user_email = approval.admin_email

    # Resolve auth credentials
    try:
        auth = _resolve_cloud_auth(ctx)
    except CloudAuthError as e:
        return ConnectorRolloutStartResult(
            success=False,
            message=f"Failed to resolve credentials: {e}",
            docker_repository=docker_repository,
            docker_image_tag=docker_image_tag,
            actor_definition_id=actor_definition_id,
        )

    # Get user ID from admin email
    try:
        user_id = api_client.get_user_id_by_email(
            email=admin_user_email,
            config_api_root=constants.CLOUD_CONFIG_API_ROOT,
            client_id=auth.client_id,
            client_secret=auth.client_secret,
            bearer_token=auth.bearer_token,
        )
    except PyAirbyteInputError as e:
        return ConnectorRolloutStartResult(
            success=False,
            message=f"Failed to get user ID for admin email '{admin_user_email}': {e}",
            docker_repository=docker_repository,
            docker_image_tag=docker_image_tag,
            actor_definition_id=actor_definition_id,
        )

    # Call the API to start the rollout
    try:
        api_client.start_connector_rollout(
            docker_repository=docker_repository,
            docker_image_tag=docker_image_tag,
            actor_definition_id=actor_definition_id,
            updated_by=user_id,
            rollout_strategy=rollout_strategy,
            config_api_root=constants.CLOUD_CONFIG_API_ROOT,
            initial_rollout_pct=initial_rollout_pct,
            final_target_rollout_pct=final_target_rollout_pct,
            customer_tier=customer_tier,
            client_id=auth.client_id,
            client_secret=auth.client_secret,
            bearer_token=auth.bearer_token,
        )

        # Build message with configuration details
        config_details = []
        if initial_rollout_pct is not None:
            config_details.append(f"initial_rollout_pct={initial_rollout_pct}%")
        if final_target_rollout_pct is not None:
            config_details.append(
                f"final_target_rollout_pct={final_target_rollout_pct}%"
            )
        if customer_tier is not None:
            config_details.append(f"customer_tier={customer_tier}")
        config_str = (
            f" Configuration: {', '.join(config_details)}." if config_details else ""
        )

        return ConnectorRolloutStartResult(
            success=True,
            message=f"Successfully started rollout workflow for "
            f"{docker_repository}:{docker_image_tag}. "
            f"The rollout state has transitioned from INITIALIZED to WORKFLOW_STARTED."
            f"{config_str}",
            docker_repository=docker_repository,
            docker_image_tag=docker_image_tag,
            actor_definition_id=actor_definition_id,
            rollout_strategy=rollout_strategy,
        )

    except PyAirbyteInputError as e:
        return ConnectorRolloutStartResult(
            success=False,
            message=str(e),
            docker_repository=docker_repository,
            docker_image_tag=docker_image_tag,
            actor_definition_id=actor_definition_id,
        )


@mcp_tool(
    destructive=True,
    idempotent=False,
    open_world=True,
)
def progress_connector_rollout(
    docker_repository: Annotated[
        str,
        Field(description="The docker repository (e.g., 'airbyte/source-pokeapi')"),
    ],
    docker_image_tag: Annotated[
        str,
        Field(description="The docker image tag (e.g., '0.3.48-rc.1')"),
    ],
    actor_definition_id: Annotated[
        str,
        Field(description="The actor definition ID (UUID)"),
    ],
    rollout_id: Annotated[
        str,
        Field(
            description="The rollout ID (UUID). Can be found from query_prod_connector_rollouts."
        ),
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
    admin_user_email_override: Annotated[
        str | None,
        Field(
            description="Direct admin email override for webapp-initiated actions. "
            "When the Ops Webapp env var is set, this bypasses the approval URL "
            "requirement. Ignored in agent/cron environments.",
            default=None,
        ),
    ],
    target_percentage: Annotated[
        int | None,
        Field(
            description="Target percentage of actors to pin to the RC (1-100). "
            "Either target_percentage or actor_ids must be provided.",
            default=None,
        ),
    ] = None,
    actor_ids: Annotated[
        list[str] | None,
        Field(
            description="Specific actor IDs to pin to the RC. "
            "Either target_percentage or actor_ids must be provided.",
            default=None,
        ),
    ] = None,
    *,
    ctx: Context,
) -> ConnectorRolloutProgressResult:
    """Progress a connector rollout by pinning actors to the RC version.

    This tool progresses a connector rollout by either:
    - Setting a target percentage of actors to pin to the RC version
    - Specifying specific actor IDs to pin

    **Admin-only operation** - Requires:
    - AIRBYTE_INTERNAL_ADMIN_FLAG=airbyte.io environment variable
    - `approval_comment_url` (Slack approval record URL from `escalate_to_human`),
      OR `admin_user_email_override` when running inside the Ops Webapp.
    """
    # Validate admin access (check env var flag)
    try:
        require_internal_admin_flag_only()
    except CloudAuthError as e:
        return ConnectorRolloutProgressResult(
            success=False,
            message=f"Admin authentication failed: {e}",
            rollout_id=rollout_id,
            docker_repository=docker_repository,
            docker_image_tag=docker_image_tag,
        )

    # Validate that at least one of target_percentage or actor_ids is provided
    if target_percentage is None and actor_ids is None:
        return ConnectorRolloutProgressResult(
            success=False,
            message="Either target_percentage or actor_ids must be provided",
            rollout_id=rollout_id,
            docker_repository=docker_repository,
            docker_image_tag=docker_image_tag,
        )

    # Resolve admin email: webapp bypass or external approval URL
    approval = check_approval_status(
        approval_comment_url=approval_comment_url,
        user_email=admin_user_email_override,
    )
    if approval.status != ApprovalStatus.APPROVED:
        return ConnectorRolloutProgressResult(
            success=False,
            message=approval.reason or "Approval check failed",
            rollout_id=rollout_id,
            docker_repository=docker_repository,
            docker_image_tag=docker_image_tag,
        )
    admin_user_email = approval.admin_email

    # Resolve auth credentials
    try:
        auth = _resolve_cloud_auth(ctx)
    except CloudAuthError as e:
        return ConnectorRolloutProgressResult(
            success=False,
            message=f"Failed to resolve credentials: {e}",
            rollout_id=rollout_id,
            docker_repository=docker_repository,
            docker_image_tag=docker_image_tag,
        )

    # Get user ID from admin email
    try:
        user_id = api_client.get_user_id_by_email(
            email=admin_user_email,
            config_api_root=constants.CLOUD_CONFIG_API_ROOT,
            client_id=auth.client_id,
            client_secret=auth.client_secret,
            bearer_token=auth.bearer_token,
        )
    except PyAirbyteInputError as e:
        return ConnectorRolloutProgressResult(
            success=False,
            message=f"Failed to get user ID for admin email '{admin_user_email}': {e}",
            rollout_id=rollout_id,
            docker_repository=docker_repository,
            docker_image_tag=docker_image_tag,
        )

    # Guard: a percentage-based progression toward a tier with zero eligible
    # actors will throw `ConnectorRolloutNotEnoughActorsProblem` server-side
    # and silently wedge the rollout at `workflow_started` (the throw happens
    # before the `IN_PROGRESS` write and the `@Transactional` rolls back).
    # Detect this up front and return an actionable error instead. Skipped when
    # pinning specific `actor_ids` (the caller chose the actors explicitly).
    if target_percentage is not None and target_percentage > 0 and not actor_ids:
        try:
            sync_info = api_client.get_actor_sync_info(
                rollout_id=rollout_id,
                config_api_root=constants.CLOUD_CONFIG_API_ROOT,
                client_id=auth.client_id,
                client_secret=auth.client_secret,
                bearer_token=auth.bearer_token,
            )
        except (PyAirbyteInputError, requests.exceptions.RequestException):
            # If eligibility can't be fetched (bad input or a network-level
            # failure), fall through and let the progress call surface the
            # underlying error rather than crashing the pre-check.
            sync_info = None
        if sync_info is not None and count_eligible_or_pinned_actors(sync_info) == 0:
            return ConnectorRolloutProgressResult(
                success=False,
                message=(
                    "Zero eligible actors: this rollout's tier has no actors to "
                    "pin, so progressing to "
                    f"target_percentage={target_percentage}% would throw "
                    "ConnectorRolloutNotEnoughActorsProblem server-side and "
                    "silently wedge the rollout at 'workflow_started'. "
                    "TIER_1/TIER_0 are named strategic accounts; a connector "
                    "with no customers in this tier can never pin anyone here. "
                    "Do not progress this tier. If the last non-empty tier is "
                    "healthy at 100%, cancel this empty rollout "
                    "(retain_pins_on_cancellation=true) and finalize the healthy "
                    "rollout as 'succeeded' to promote to GA. See the "
                    "'Rollout stuck at workflow_started with zero eligible "
                    "actors' troubleshooting guide in docs/progressive-rollouts.md."
                ),
                rollout_id=rollout_id,
                docker_repository=docker_repository,
                docker_image_tag=docker_image_tag,
            )

    # Call the API to progress the rollout
    try:
        api_client.progress_connector_rollout(
            docker_repository=docker_repository,
            docker_image_tag=docker_image_tag,
            actor_definition_id=actor_definition_id,
            rollout_id=rollout_id,
            updated_by=user_id,
            config_api_root=constants.CLOUD_CONFIG_API_ROOT,
            target_percentage=target_percentage,
            actor_ids=actor_ids,
            client_id=auth.client_id,
            client_secret=auth.client_secret,
            bearer_token=auth.bearer_token,
        )

        progress_msg = (
            f"target_percentage={target_percentage}%"
            if target_percentage
            else f"{len(actor_ids) if actor_ids else 0} specific actors"
        )
        return ConnectorRolloutProgressResult(
            success=True,
            message=f"Successfully progressed rollout for "
            f"{docker_repository}:{docker_image_tag} to {progress_msg}.",
            rollout_id=rollout_id,
            docker_repository=docker_repository,
            docker_image_tag=docker_image_tag,
            target_percentage=target_percentage,
        )

    except PyAirbyteInputError as e:
        return ConnectorRolloutProgressResult(
            success=False,
            message=str(e),
            rollout_id=rollout_id,
            docker_repository=docker_repository,
            docker_image_tag=docker_image_tag,
        )


@mcp_tool(
    destructive=True,
    idempotent=False,
    open_world=True,
)
def finalize_connector_rollout(
    docker_repository: Annotated[
        str,
        Field(
            description="The docker repository (e.g., 'airbyte/source-youtube-analytics')"
        ),
    ],
    docker_image_tag: Annotated[
        str,
        Field(description="The docker image tag (e.g., '1.2.0-rc.2')"),
    ],
    actor_definition_id: Annotated[
        str,
        Field(description="The actor definition ID (UUID)"),
    ],
    rollout_id: Annotated[
        str,
        Field(
            description="The rollout ID (UUID). Can be found in the 'pin_origin' field "
            "of rollout data from query_prod_actors_by_pinned_connector_version."
        ),
    ],
    state: Annotated[
        Literal["succeeded", "failed_rolled_back", "canceled"],
        Field(
            description="The final state for the rollout: "
            "'succeeded' promotes the RC to GA (default version for all users), "
            "'failed_rolled_back' rolls back the RC, "
            "'canceled' cancels the rollout without promotion or rollback."
        ),
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
    admin_user_email_override: Annotated[
        str | None,
        Field(
            description="Direct admin email override for webapp-initiated actions. "
            "When the Ops Webapp env var is set, this bypasses the approval URL "
            "requirement. Ignored in agent/cron environments.",
            default=None,
        ),
    ],
    error_msg: Annotated[
        str | None,
        Field(
            description="Optional error message for failed/canceled states.",
            default=None,
        ),
    ] = None,
    failed_reason: Annotated[
        str | None,
        Field(
            description="Optional failure reason for failed/canceled states.",
            default=None,
        ),
    ] = None,
    retain_pins_on_cancellation: Annotated[
        bool | None,
        Field(
            description="If True, retain version pins when canceling. "
            "Only applicable when state is 'canceled'.",
            default=None,
        ),
    ] = None,
    *,
    ctx: Context,
) -> ConnectorRolloutFinalizeResult:
    """Finalize a connector rollout by promoting, rolling back, or canceling.

    This tool allows admins to finalize connector rollouts that are in progress.
    Use this after monitoring a rollout and determining it is ready for finalization.

    **IMPORTANT: Finalization is asynchronous.** This tool sends a finalization
    request to the platform API, which transitions the rollout to `finalizing`
    state and triggers a Temporal workflow. The actual promotion (PR creation,
    connector publish, registry update) or rollback (GCS cleanup, registry
    recompile) happens asynchronously via the `finalize_rollout.yml` GitHub
    Actions workflow. A successful response from this tool means the request
    was accepted — NOT that the promotion/rollback is complete.

    After calling this tool, you MUST verify:
    1. The `finalize_rollout.yml` workflow ran successfully in GitHub Actions
    2. For promotions: a merged PR exists (e.g., `chore: finalize promote for <connector>`)
    3. The rollout state transitioned to its terminal state (`succeeded`,
       `failed_rolled_back`, or `canceled`) via `query_prod_connector_rollouts`

    **Admin-only operation** - Requires:
    - AIRBYTE_INTERNAL_ADMIN_FLAG=airbyte.io environment variable
    - `approval_comment_url` (Slack approval record URL from `escalate_to_human`),
      OR `admin_user_email_override` when running inside the Ops Webapp.
    """
    # Validate admin access (check env var flag)
    try:
        require_internal_admin_flag_only()
    except CloudAuthError as e:
        return ConnectorRolloutFinalizeResult(
            success=False,
            message=f"Admin authentication failed: {e}",
            rollout_id=rollout_id,
            docker_repository=docker_repository,
            docker_image_tag=docker_image_tag,
        )

    # Resolve admin email: webapp bypass or external approval URL
    approval = check_approval_status(
        approval_comment_url=approval_comment_url,
        user_email=admin_user_email_override,
    )
    if approval.status != ApprovalStatus.APPROVED:
        return ConnectorRolloutFinalizeResult(
            success=False,
            message=approval.reason or "Approval check failed",
            rollout_id=rollout_id,
            docker_repository=docker_repository,
            docker_image_tag=docker_image_tag,
        )
    admin_user_email = approval.admin_email

    # Resolve auth credentials
    try:
        auth = _resolve_cloud_auth(ctx)
    except CloudAuthError as e:
        return ConnectorRolloutFinalizeResult(
            success=False,
            message=f"Failed to resolve credentials: {e}",
            rollout_id=rollout_id,
            docker_repository=docker_repository,
            docker_image_tag=docker_image_tag,
        )

    # Get user ID from admin email
    try:
        user_id = api_client.get_user_id_by_email(
            email=admin_user_email,
            config_api_root=constants.CLOUD_CONFIG_API_ROOT,
            client_id=auth.client_id,
            client_secret=auth.client_secret,
            bearer_token=auth.bearer_token,
        )
    except PyAirbyteInputError as e:
        return ConnectorRolloutFinalizeResult(
            success=False,
            message=f"Failed to get user ID for admin email '{admin_user_email}': {e}",
            rollout_id=rollout_id,
            docker_repository=docker_repository,
            docker_image_tag=docker_image_tag,
        )

    # Call the API to finalize the rollout
    try:
        api_client.finalize_connector_rollout(
            docker_repository=docker_repository,
            docker_image_tag=docker_image_tag,
            actor_definition_id=actor_definition_id,
            rollout_id=rollout_id,
            updated_by=user_id,
            state=state,
            config_api_root=constants.CLOUD_CONFIG_API_ROOT,
            client_id=auth.client_id,
            client_secret=auth.client_secret,
            bearer_token=auth.bearer_token,
            error_msg=error_msg,
            failed_reason=failed_reason,
            retain_pins_on_cancellation=retain_pins_on_cancellation,
        )

        state_descriptions = {
            "succeeded": (
                "GA promotion has been initiated (state: finalizing). "
                "The actual promotion (PR creation, publish, registry update) "
                "happens asynchronously via the finalize_rollout.yml GitHub Actions workflow. "
                "You MUST verify the workflow completes successfully and the rollout "
                "transitions to 'succeeded' state before reporting completion. "
                "Check: (1) GitHub Actions for a 'Finalize Progressive Rollout' workflow run, "
                "(2) a merged promotion PR, and "
                "(3) query_prod_connector_rollouts to confirm state is 'succeeded'."
            ),
            "failed_rolled_back": (
                "rollback has been initiated (state: finalizing). "
                "The rollback happens asynchronously via the finalize_rollout.yml workflow. "
                "Verify the workflow completes and the rollout transitions to "
                "'failed_rolled_back' state."
            ),
            "canceled": "canceled",
        }
        state_desc = state_descriptions.get(state, state)

        return ConnectorRolloutFinalizeResult(
            success=True,
            message=f"Finalization request accepted for {docker_repository}:{docker_image_tag}: "
            f"{state_desc}",
            rollout_id=rollout_id,
            docker_repository=docker_repository,
            docker_image_tag=docker_image_tag,
            state=state,
        )

    except PyAirbyteInputError as e:
        return ConnectorRolloutFinalizeResult(
            success=False,
            message=str(e),
            rollout_id=rollout_id,
            docker_repository=docker_repository,
            docker_image_tag=docker_image_tag,
        )


class RolloutActorSelectionInfo(BaseModel):
    """Actor selection info for a connector rollout."""

    num_actors: int = Field(description="Total actors using this connector")
    num_pinned_to_connector_rollout: int = Field(
        description="Actors specifically pinned to this rollout"
    )
    num_actors_eligible_or_already_pinned: int = Field(
        description="Actors eligible for pinning or already pinned"
    )


class RolloutActorSyncStats(BaseModel):
    """Per-actor sync stats for a rollout (only syncs using the RC version)."""

    actor_id: str = Field(description="Actor UUID")
    num_connections: int = Field(description="Number of connections using this actor")
    num_succeeded: int = Field(
        description="Number of successful syncs using the RC version"
    )
    num_failed: int = Field(description="Number of failed syncs using the RC version")


class RolloutMonitoringResult(BaseModel):
    """Complete monitoring result for a rollout from the platform API.

    This uses the platform API's /get_actor_sync_info endpoint which filters
    sync stats to only include syncs that actually used the RC version
    associated with the rollout.
    """

    rollout_id: str = Field(description="Rollout UUID")
    actor_selection_info: RolloutActorSelectionInfo = Field(
        description="Actor selection info for the rollout"
    )
    actor_sync_stats: list[RolloutActorSyncStats] = Field(
        description="Per-actor sync stats for actors pinned to the rollout"
    )


@mcp_tool(
    read_only=True,
    idempotent=True,
)
def query_prod_rollout_monitoring_stats(
    rollout_id: Annotated[
        str,
        Field(description="Rollout UUID to get monitoring stats for"),
    ],
    *,
    ctx: Context,
) -> RolloutMonitoringResult:
    """Get monitoring stats for a connector rollout.

    Returns actor selection info and per-actor sync stats for actors
    participating in the rollout. This uses the platform API's
    /get_actor_sync_info endpoint which filters sync stats to only include
    syncs that actually used the RC version associated with the rollout.

    This is more accurate than SQL-based approaches which count all syncs
    regardless of which connector version was used.
    """
    auth = _resolve_cloud_auth(ctx)

    response = api_client.get_actor_sync_info(
        rollout_id=rollout_id,
        config_api_root=constants.CLOUD_CONFIG_API_ROOT,
        client_id=auth.client_id,
        client_secret=auth.client_secret,
        bearer_token=auth.bearer_token,
    )

    data = response.get("data", {})
    actor_selection_info_data = data.get("actor_selection_info", {})
    syncs_data = data.get("syncs", {})

    actor_selection_info = RolloutActorSelectionInfo(
        num_actors=actor_selection_info_data.get("num_actors", 0),
        num_pinned_to_connector_rollout=actor_selection_info_data.get(
            "num_pinned_to_connector_rollout", 0
        ),
        num_actors_eligible_or_already_pinned=actor_selection_info_data.get(
            "num_actors_eligible_or_already_pinned", 0
        ),
    )

    actor_sync_stats = [
        RolloutActorSyncStats(
            actor_id=actor_id,
            num_connections=sync_info.get("num_connections", 0),
            num_succeeded=sync_info.get("num_succeeded", 0),
            num_failed=sync_info.get("num_failed", 0),
        )
        for actor_id, sync_info in syncs_data.items()
    ]

    return RolloutMonitoringResult(
        rollout_id=rollout_id,
        actor_selection_info=actor_selection_info,
        actor_sync_stats=actor_sync_stats,
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

ENTERPRISE_REPO_NAME = ConnectorRepo.AIRBYTE_ENTERPRISE

ENTERPRISE_DEFAULT_BRANCH = "main"

ENTERPRISE_PRERELEASE_WORKFLOW_FILE = "publish_enterprise_connectors.yml"

PRERELEASE_TOKEN_ENV_VARS = [
    "GITHUB_CONNECTOR_PUBLISHING_PAT",
    "GITHUB_CI_WORKFLOW_TRIGGER_PAT",
    "GITHUB_TOKEN",
]

PRERELEASE_TAG_PREFIX = "preview"

PRERELEASE_SHA_LENGTH = 7


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


def register_connector_version_tools(app: FastMCP) -> None:
    """Register connector_versions tools with the FastMCP app."""
    register_mcp_tools(app, mcp_module=__name__)
