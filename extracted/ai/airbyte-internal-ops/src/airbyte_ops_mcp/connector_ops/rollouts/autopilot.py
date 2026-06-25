# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Command implementations for the AutoPilot progressive rollout system.

Each function queries prod DB for relevant rollouts, applies metadata gates
from the compiled registry, and executes actions via the Cloud Config API.
"""

from __future__ import annotations

import logging
from typing import Literal

from airbyte import constants
from airbyte_connector_models.metadata.v0.connector_registry_v0 import (
    ConnectorRegistryV0ConnectorRegistryReleasesRolloutConfigurationAutopilotConfig as AutopilotConfig,
)
from airbyte_connector_models.metadata.v0.connector_registry_v0 import (
    ConnectorRegistryV0ConnectorRegistryReleasesRolloutConfigurationDefaultRolloutMode as RolloutMode,
)

from airbyte_ops_mcp.cloud_admin import api_client
from airbyte_ops_mcp.cloud_admin.auth import get_admin_user_id
from airbyte_ops_mcp.cloud_admin.version_overrides import ResolvedCloudAuth
from airbyte_ops_mcp.connector_ops.rollouts._helpers import (
    filter_rollouts_by_connector,
    get_connector_rollout_config,
    get_unsafe_downgrades,
)
from airbyte_ops_mcp.connector_ops.rollouts.constants import (
    STRATEGY_STEP_MAP,
    TIER_ORDER,
)
from airbyte_ops_mcp.connector_ops.rollouts.models import (
    AutopilotAction,
    AutopilotResult,
    ConnectorRolloutRecord,
)
from airbyte_ops_mcp.prod_db_access.queries import query_connector_rollouts

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Command implementations
# ---------------------------------------------------------------------------


def run_auto_start(
    *,
    auth: ResolvedCloudAuth,
    connector: str | None = None,
    dry_run: bool = False,
) -> AutopilotResult:
    """Start INITIALIZED rollouts that have autopilot auto-start enabled.

    Gate: `autopilotConfig.autoStart == true` (defaults to true when
    `defaultRolloutMode: autopilot`).
    """
    result = AutopilotResult(command="auto-start", dry_run=dry_run)

    raw_rows = query_connector_rollouts(active_only=True, limit=None)
    rollouts = [ConnectorRolloutRecord.from_db_row(r) for r in raw_rows]
    rollouts = filter_rollouts_by_connector(rollouts, connector)
    initialized = [r for r in rollouts if r.state in ["initialized"]]

    if not initialized:
        logger.info("auto-start: No INITIALIZED rollouts found.")
        return result

    user_id = get_admin_user_id(
        client_id=auth.client_id,
        client_secret=auth.client_secret,
        bearer_token=auth.bearer_token,
    )

    for rollout in initialized:
        rc_version = rollout.rc_docker_image_tag or "unknown"

        # Gate: check autopilot config
        rollout_config = get_connector_rollout_config(
            rollout.actor_definition_id, rc_version=rc_version
        )
        if rollout_config.default_rollout_mode != RolloutMode.autopilot:
            result.skipped.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="start",
                    success=False,
                    message="Skipped: defaultRolloutMode is not 'autopilot'",
                )
            )
            continue

        autopilot_config = rollout_config.autopilot_config or AutopilotConfig()
        if not autopilot_config.auto_start:
            result.skipped.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="start",
                    success=False,
                    message="Skipped: autopilotConfig.autoStart is false",
                )
            )
            continue

        strategy = (
            autopilot_config.strategy.value if autopilot_config.strategy else "default"
        )
        if strategy not in STRATEGY_STEP_MAP:
            result.errors.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="start",
                    success=False,
                    message=f"Unknown strategy '{strategy}' (expected one of {sorted(STRATEGY_STEP_MAP)})",
                )
            )
            continue

        step_pct = STRATEGY_STEP_MAP[strategy]
        rollout_strategy: Literal["manual", "automated", "overridden"] = "manual"

        if dry_run:
            result.actions.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="start",
                    success=True,
                    message=f"Would start rollout (strategy={strategy}, step_pct={step_pct}%)",
                )
            )
            continue

        # Two-phase start: first transition INITIALIZED -> IN_PROGRESS via
        # manual_start (no percentage params — all pacing is ours), then
        # immediately advance to the first step percentage via manual_rollout.
        try:
            start_resp = api_client.start_connector_rollout(
                docker_repository=rollout.rc_docker_repository or "",
                docker_image_tag=rc_version,
                actor_definition_id=rollout.actor_definition_id,
                updated_by=user_id,
                rollout_strategy=rollout_strategy,
                config_api_root=constants.CLOUD_CONFIG_API_ROOT,
                client_id=auth.client_id,
                client_secret=auth.client_secret,
                bearer_token=auth.bearer_token,
                customer_tier="TIER_2",
            )
        except Exception as e:
            result.errors.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="start",
                    success=False,
                    message=f"Failed to start: {e}",
                )
            )
            continue

        # Extract the rollout ID from the start response for the progress call.
        started_rollout_id = (
            start_resp.get("id") or start_resp.get("rollout_id") or rollout.rollout_id
        )

        try:
            api_client.progress_connector_rollout(
                docker_repository=rollout.rc_docker_repository or "",
                docker_image_tag=rc_version,
                actor_definition_id=rollout.actor_definition_id,
                rollout_id=started_rollout_id,
                updated_by=user_id,
                target_percentage=step_pct,
                config_api_root=constants.CLOUD_CONFIG_API_ROOT,
                client_id=auth.client_id,
                client_secret=auth.client_secret,
                bearer_token=auth.bearer_token,
            )
        except Exception as e:
            result.errors.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="start",
                    success=False,
                    message=f"Started but failed to set initial percentage: {e}",
                )
            )
        else:
            result.actions.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="start",
                    success=True,
                    message=f"Started rollout and set to {step_pct}% (strategy={strategy})",
                )
            )

    logger.info("auto-start: %s", result.summary)
    return result


def run_auto_advance(
    *,
    auth: ResolvedCloudAuth,
    connector: str | None = None,
    dry_run: bool = False,
) -> AutopilotResult:
    """Advance IN_PROGRESS rollouts within their current tier.

    No gate: runs for all IN_PROGRESS autopilot rollouts. Advances the
    rollout percentage based on strategy pacing within the current tier.
    """
    result = AutopilotResult(command="auto-advance", dry_run=dry_run)

    raw_rows = query_connector_rollouts(active_only=True, limit=None)
    rollouts = [ConnectorRolloutRecord.from_db_row(r) for r in raw_rows]
    rollouts = filter_rollouts_by_connector(rollouts, connector)
    in_progress = [r for r in rollouts if r.state in ["in_progress"]]

    if not in_progress:
        logger.info("auto-advance: No IN_PROGRESS rollouts found.")
        return result

    user_id = get_admin_user_id(
        client_id=auth.client_id,
        client_secret=auth.client_secret,
        bearer_token=auth.bearer_token,
    )

    for rollout in in_progress:
        rc_version = rollout.rc_docker_image_tag or "unknown"

        rollout_config = get_connector_rollout_config(
            rollout.actor_definition_id, rc_version=rc_version
        )
        if rollout_config.default_rollout_mode != RolloutMode.autopilot:
            result.skipped.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="advance",
                    success=False,
                    message="Skipped: defaultRolloutMode is not 'autopilot'",
                )
            )
            continue

        current_pct = rollout.current_target_rollout_pct or 0
        final_pct = rollout.final_target_rollout_pct or 100

        if current_pct >= final_pct:
            result.skipped.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="advance",
                    success=False,
                    message=f"Skipped: already at target ({current_pct}% >= {final_pct}%)",
                )
            )
            continue

        autopilot_config = rollout_config.autopilot_config or AutopilotConfig()
        strategy = (
            autopilot_config.strategy.value if autopilot_config.strategy else "default"
        )
        if strategy not in STRATEGY_STEP_MAP:
            result.errors.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="advance",
                    success=False,
                    message=f"Unknown strategy '{strategy}' (expected one of {sorted(STRATEGY_STEP_MAP)})",
                )
            )
            continue
        step_pct = STRATEGY_STEP_MAP[strategy]
        next_pct = min(current_pct + step_pct, final_pct)

        if dry_run:
            result.actions.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="advance",
                    success=True,
                    message=f"Would advance {current_pct}% -> {next_pct}% (strategy={strategy})",
                )
            )
            continue

        try:
            api_client.progress_connector_rollout(
                docker_repository=rollout.rc_docker_repository or "",
                docker_image_tag=rc_version,
                actor_definition_id=rollout.actor_definition_id,
                rollout_id=rollout.rollout_id,
                updated_by=user_id,
                target_percentage=next_pct,
                config_api_root=constants.CLOUD_CONFIG_API_ROOT,
                client_id=auth.client_id,
                client_secret=auth.client_secret,
                bearer_token=auth.bearer_token,
            )
        except Exception as e:
            result.errors.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="advance",
                    success=False,
                    message=f"Failed to advance: {e}",
                )
            )
        else:
            result.actions.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="advance",
                    success=True,
                    message=f"Advanced {current_pct}% -> {next_pct}% (strategy={strategy})",
                )
            )

    logger.info("auto-advance: %s", result.summary)
    return result


def run_auto_promote(
    *,
    auth: ResolvedCloudAuth,
    connector: str | None = None,
    dry_run: bool = False,
) -> AutopilotResult:
    """Promote rollouts when at 100% of current tier.

    Gate: `autopilotConfig.autoPromoteStages == true`.
    Currently finalizes rollouts at ALL tier as succeeded (GA promotion).
    Cross-tier promotion (TIER_2 -> TIER_1 -> ALL) is not yet implemented;
    non-ALL tiers are logged and skipped.
    """
    result = AutopilotResult(command="auto-promote", dry_run=dry_run)

    raw_rows = query_connector_rollouts(active_only=True, limit=None)
    rollouts = [ConnectorRolloutRecord.from_db_row(r) for r in raw_rows]
    rollouts = filter_rollouts_by_connector(rollouts, connector)
    in_progress = [r for r in rollouts if r.state in ["in_progress"]]

    if not in_progress:
        logger.info("auto-promote: No IN_PROGRESS rollouts found.")
        return result

    user_id = get_admin_user_id(
        client_id=auth.client_id,
        client_secret=auth.client_secret,
        bearer_token=auth.bearer_token,
    )

    for rollout in in_progress:
        rc_version = rollout.rc_docker_image_tag or "unknown"

        rollout_config = get_connector_rollout_config(
            rollout.actor_definition_id, rc_version=rc_version
        )
        if rollout_config.default_rollout_mode != RolloutMode.autopilot:
            result.skipped.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="promote",
                    success=False,
                    message="Skipped: defaultRolloutMode is not 'autopilot'",
                )
            )
            continue

        autopilot_config = rollout_config.autopilot_config or AutopilotConfig()
        if not autopilot_config.auto_promote_stages:
            result.skipped.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="promote",
                    success=False,
                    message="Skipped: autopilotConfig.autoPromoteStages is false",
                )
            )
            continue

        current_pct = rollout.current_target_rollout_pct or 0
        final_pct = rollout.final_target_rollout_pct or 100
        if current_pct < final_pct:
            result.skipped.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="promote",
                    success=False,
                    message=f"Skipped: not at target pct ({current_pct}% < {final_pct}%)",
                )
            )
            continue

        current_tier = rollout.tier

        if current_tier == "ALL":
            if dry_run:
                result.actions.append(
                    AutopilotAction(
                        rollout_id=rollout.rollout_id,
                        actor_definition_id=rollout.actor_definition_id,
                        connector_name=rollout.connector_name,
                        rc_version=rc_version,
                        action="promote",
                        success=True,
                        message="Would finalize as succeeded (promote to GA)",
                    )
                )
                continue

            try:
                api_client.finalize_connector_rollout(
                    docker_repository=rollout.rc_docker_repository or "",
                    docker_image_tag=rc_version,
                    actor_definition_id=rollout.actor_definition_id,
                    rollout_id=rollout.rollout_id,
                    updated_by=user_id,
                    state="succeeded",
                    config_api_root=constants.CLOUD_CONFIG_API_ROOT,
                    client_id=auth.client_id,
                    client_secret=auth.client_secret,
                    bearer_token=auth.bearer_token,
                )
            except Exception as e:
                result.errors.append(
                    AutopilotAction(
                        rollout_id=rollout.rollout_id,
                        actor_definition_id=rollout.actor_definition_id,
                        connector_name=rollout.connector_name,
                        rc_version=rc_version,
                        action="promote",
                        success=False,
                        message=f"Failed to finalize: {e}",
                    )
                )
            else:
                result.actions.append(
                    AutopilotAction(
                        rollout_id=rollout.rollout_id,
                        actor_definition_id=rollout.actor_definition_id,
                        connector_name=rollout.connector_name,
                        rc_version=rc_version,
                        action="promote",
                        success=True,
                        message="Finalized as succeeded (promoted to GA)",
                    )
                )
        else:
            tier_idx = (
                TIER_ORDER.index(current_tier)
                if current_tier in TIER_ORDER
                else len(TIER_ORDER) - 1
            )
            next_t = (
                TIER_ORDER[tier_idx + 1] if tier_idx + 1 < len(TIER_ORDER) else "ALL"
            )
            if dry_run:
                result.actions.append(
                    AutopilotAction(
                        rollout_id=rollout.rollout_id,
                        actor_definition_id=rollout.actor_definition_id,
                        connector_name=rollout.connector_name,
                        rc_version=rc_version,
                        action="promote",
                        success=True,
                        message=f"Would promote {current_tier} -> {next_t}",
                    )
                )
                continue

            # TODO: The platform API for re-starting a rollout at a new tier
            # is not yet a single endpoint. This would require calling
            # start_connector_rollout with a new customer_tier filter.
            logger.info(
                "auto-promote: Would promote rollout %s from %s to %s",
                rollout.rollout_id,
                current_tier,
                next_t,
            )
            result.skipped.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="promote",
                    success=False,
                    message=f"Skipped: tier promotion API not yet available ({current_tier} -> {next_t})",
                )
            )

    logger.info("auto-promote: %s", result.summary)
    return result


def run_auto_triage_failed(
    *,
    auth: ResolvedCloudAuth,
    connector: str | None = None,
    dry_run: bool = False,
) -> AutopilotResult:
    """Triage failed rollouts: log all, check unpin eligibility.

    No gate: always runs. Finds rollouts in `errored` or `paused` state
    and logs them. Checks safe-to-downgrade eligibility per `unsafeDowngrades`.
    Actor-level unpinning is not yet implemented.
    """
    result = AutopilotResult(command="auto-triage-failed", dry_run=dry_run)

    raw_rows = query_connector_rollouts(active_only=True, limit=None)
    rollouts = [ConnectorRolloutRecord.from_db_row(r) for r in raw_rows]
    rollouts = filter_rollouts_by_connector(rollouts, connector)
    failed = [r for r in rollouts if r.state in ["errored", "paused"]]

    if not failed:
        logger.info("auto-triage-failed: No errored/paused rollouts found.")
        return result

    for rollout in failed:
        rc_version = rollout.rc_docker_image_tag or "unknown"

        # Always log the failure
        logger.warning(
            "auto-triage-failed: %s %s (rollout=%s) state=%s error=%s reason=%s paused=%s",
            rollout.connector_name,
            rc_version,
            rollout.rollout_id,
            rollout.state,
            rollout.error_msg or "no error message",
            rollout.failed_reason or "unknown",
            rollout.paused_reason or "none",
        )

        # Check if safe to unpin (version not in unsafeDowngrades)
        unsafe_versions = get_unsafe_downgrades(rollout.actor_definition_id)
        if rc_version in unsafe_versions:
            result.skipped.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="triage",
                    success=False,
                    message=f"Cannot unpin: {rc_version} is in unsafeDowngrades",
                )
            )
            continue

        if dry_run:
            result.actions.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="triage",
                    success=True,
                    message=f"Would unpin failing actors (state={rollout.state})",
                )
            )
            continue

        # TODO: Implement actor-level unpinning for failing connections.
        # This requires querying pinned actors and clearing their pins individually.
        logger.info(
            "auto-triage-failed: Would unpin failing actors for rollout %s (not yet implemented)",
            rollout.rollout_id,
        )
        result.skipped.append(
            AutopilotAction(
                rollout_id=rollout.rollout_id,
                actor_definition_id=rollout.actor_definition_id,
                connector_name=rollout.connector_name,
                rc_version=rc_version,
                action="triage",
                success=False,
                message=f"Skipped: actor unpin API not yet implemented (state={rollout.state})",
            )
        )

    logger.info("auto-triage-failed: %s", result.summary)
    return result


def run_auto_rollback_failed(
    *,
    auth: ResolvedCloudAuth,
    connector: str | None = None,
    dry_run: bool = False,
) -> AutopilotResult:
    """Full rollback/cancel of failed rollouts when safe to downgrade.

    Gate: version NOT in `unsafeDowngrades`. Calls
    `finalize_connector_rollout(state="failed_rolled_back")` to cancel
    the entire rollout and roll back all pinned actors to GA.
    """
    result = AutopilotResult(command="auto-rollback-failed", dry_run=dry_run)

    raw_rows = query_connector_rollouts(active_only=True, limit=None)
    rollouts = [ConnectorRolloutRecord.from_db_row(r) for r in raw_rows]
    rollouts = filter_rollouts_by_connector(rollouts, connector)
    failed = [r for r in rollouts if r.state in ["errored"]]

    if not failed:
        logger.info("auto-rollback-failed: No errored rollouts found.")
        return result

    user_id = get_admin_user_id(
        client_id=auth.client_id,
        client_secret=auth.client_secret,
        bearer_token=auth.bearer_token,
    )

    for rollout in failed:
        rc_version = rollout.rc_docker_image_tag or "unknown"

        # Gate: check unsafeDowngrades
        unsafe_versions = get_unsafe_downgrades(rollout.actor_definition_id)
        if rc_version in unsafe_versions:
            result.skipped.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="rollback",
                    success=False,
                    message=f"Skipped: {rc_version} is in unsafeDowngrades (cannot safely rollback)",
                )
            )
            continue

        if dry_run:
            result.actions.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="rollback",
                    success=True,
                    message="Would finalize as failed_rolled_back",
                )
            )
            continue

        try:
            api_client.finalize_connector_rollout(
                docker_repository=rollout.rc_docker_repository or "",
                docker_image_tag=rc_version,
                actor_definition_id=rollout.actor_definition_id,
                rollout_id=rollout.rollout_id,
                updated_by=user_id,
                state="failed_rolled_back",
                config_api_root=constants.CLOUD_CONFIG_API_ROOT,
                client_id=auth.client_id,
                client_secret=auth.client_secret,
                bearer_token=auth.bearer_token,
                error_msg="AutoPilot auto-rollback: rollout failed and version is safe to downgrade",
                failed_reason="autopilot_auto_rollback",
            )
        except Exception as e:
            result.errors.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="rollback",
                    success=False,
                    message=f"Failed to rollback: {e}",
                )
            )
        else:
            result.actions.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="rollback",
                    success=True,
                    message="Finalized as failed_rolled_back",
                )
            )

    logger.info("auto-rollback-failed: %s", result.summary)
    return result
