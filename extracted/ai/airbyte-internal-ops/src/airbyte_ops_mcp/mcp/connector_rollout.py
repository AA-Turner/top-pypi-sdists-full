# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tools for connector rollout management.

This module provides MCP tools for managing connector rollouts in Airbyte Cloud,
including finalizing (promoting, rolling back, or canceling) rollouts.

## MCP reference

.. include:: ../../../docs/mcp-generated/connector_rollout.md
    :start-line: 2
"""

# NOTE: We intentionally do NOT use `from __future__ import annotations` here.
# FastMCP has issues resolving forward references when PEP 563 deferred annotations
# are used. See: https://github.com/jlowin/fastmcp/issues/905
# Python 3.12+ supports modern type hint syntax natively, so this is not needed.

__all__: list[str] = []

from dataclasses import dataclass
from typing import Annotated, Literal

from airbyte import constants
from airbyte.exceptions import PyAirbyteInputError
from fastmcp import Context, FastMCP
from fastmcp_extensions import get_mcp_config, mcp_tool, register_mcp_tools
from pydantic import BaseModel, Field

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
)
from airbyte_ops_mcp.constants import ServerConfigKey


@dataclass(frozen=True)
class _ResolvedCloudAuth:
    """Resolved authentication for Airbyte Cloud API calls.

    Either bearer_token OR (client_id AND client_secret) will be set, not both.
    """

    bearer_token: str | None = None
    client_id: str | None = None
    client_secret: str | None = None


def _resolve_cloud_auth(ctx: Context) -> _ResolvedCloudAuth:
    """Resolve authentication credentials for Airbyte Cloud API.

    Credentials are resolved in priority order:
    1. Bearer token (Authorization header or AIRBYTE_CLOUD_BEARER_TOKEN env var)
    2. Client credentials (X-Airbyte-Cloud-Client-Id/Secret headers or env vars)

    Args:
        ctx: FastMCP Context object from the current tool invocation.

    Returns:
        _ResolvedCloudAuth with either bearer_token or client credentials set.

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


def register_connector_rollout_tools(app: FastMCP) -> None:
    """Register connector rollout tools with the FastMCP app.

    Args:
        app: FastMCP application instance
    """
    register_mcp_tools(app)
