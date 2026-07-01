# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Command implementations for the AutoPilot progressive rollout system.

Each function queries prod DB for relevant rollouts, applies metadata gates
from the compiled registry, and executes actions via the Cloud Config API.
"""

from __future__ import annotations

import logging
import os
from collections import defaultdict
from typing import Literal

from airbyte import constants
from airbyte_connector_models.metadata.v0.connector_registry_v0 import (
    ConnectorRegistryV0ConnectorRegistryReleasesRolloutConfigurationAutopilotConfig as AutopilotConfig,
)
from airbyte_connector_models.metadata.v0.connector_registry_v0 import (
    ConnectorRegistryV0ConnectorRegistryReleasesRolloutConfigurationDefaultRolloutMode as RolloutMode,
)
from packaging.version import Version

from airbyte_ops_mcp.cloud_admin import api_client
from airbyte_ops_mcp.cloud_admin.auth import get_admin_user_id
from airbyte_ops_mcp.cloud_admin.version_overrides import ResolvedCloudAuth
from airbyte_ops_mcp.connector_ops.rollouts._helpers import (
    HealthGateResult,
    check_health_gate,
    filter_rollouts_by_connector,
    get_connector_rollout_config,
    get_unsafe_downgrades,
)
from airbyte_ops_mcp.connector_ops.rollouts.constants import (
    STRATEGY_DEFAULT,
    STRATEGY_STEP_MAP,
    TIER_ORDER,
    CustomerTier,
    resolve_strategy,
)
from airbyte_ops_mcp.connector_ops.rollouts.models import (
    AutopilotAction,
    AutopilotResult,
    ConnectorRolloutRecord,
)
from airbyte_ops_mcp.prod_db_access.queries import query_connector_rollouts
from airbyte_ops_mcp.slack_posting import send_hitl_notification

logger = logging.getLogger(__name__)

_AUTOPILOT_ESCALATION_TARGET = "@aaronsteers"


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
                    tier=rollout.tier,
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
                    tier=rollout.tier,
                )
            )
            continue

        raw_strategy = (
            autopilot_config.strategy.value
            if autopilot_config.strategy
            else STRATEGY_DEFAULT
        )
        try:
            strategy = resolve_strategy(raw_strategy)
        except ValueError as e:
            result.errors.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="start",
                    success=False,
                    message=str(e),
                    tier=rollout.tier,
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
                    tier=rollout.tier,
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
                    tier=rollout.tier,
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
                    tier=rollout.tier,
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
                    tier=rollout.tier,
                )
            )

    logger.info("auto-start: %s", result.summary)
    return result


# States that auto-advance should handle: in_progress for normal advancement,
# workflow_started for recovery (Phase 2 of a prior tier promotion failed before
# setting the initial percentage).
_ADVANCE_STATES = ["in_progress", "workflow_started"]


def run_auto_advance(
    *,
    auth: ResolvedCloudAuth,
    connector: str | None = None,
    dry_run: bool = False,
) -> AutopilotResult:
    """Advance rollouts within their current tier.

    Handles two cases:
    - `in_progress` rollouts: normal percentage advancement, health-gated.
    - `workflow_started` rollouts: recovery from a failed tier promotion
      where `start_connector_rollout` succeeded but the subsequent
      `progress_connector_rollout` call failed.  These are advanced to
      their initial percentage *without* a health gate check (there is no
      sync data yet).
    """
    result = AutopilotResult(command="auto-advance", dry_run=dry_run)

    raw_rows = query_connector_rollouts(active_only=True, limit=None)
    rollouts = [ConnectorRolloutRecord.from_db_row(r) for r in raw_rows]
    rollouts = filter_rollouts_by_connector(rollouts, connector)
    advanceable = [r for r in rollouts if r.state in _ADVANCE_STATES]

    if not advanceable:
        logger.info("auto-advance: No advanceable rollouts found.")
        return result

    user_id = get_admin_user_id(
        client_id=auth.client_id,
        client_secret=auth.client_secret,
        bearer_token=auth.bearer_token,
    )

    for rollout in advanceable:
        rc_version = rollout.rc_docker_image_tag or "unknown"
        is_recovery = rollout.state == "workflow_started"

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
                    tier=rollout.tier,
                )
            )
            continue

        current_pct = rollout.current_target_rollout_pct or 0
        final_pct = rollout.final_target_rollout_pct or 100

        if current_pct >= final_pct and not is_recovery:
            result.skipped.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="advance",
                    success=False,
                    message=f"Skipped: already at target ({current_pct}% >= {final_pct}%)",
                    tier=rollout.tier,
                )
            )
            continue

        autopilot_config = rollout_config.autopilot_config or AutopilotConfig()
        raw_strategy = (
            autopilot_config.strategy.value
            if autopilot_config.strategy
            else STRATEGY_DEFAULT
        )
        try:
            strategy = resolve_strategy(raw_strategy)
        except ValueError as e:
            result.errors.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="advance",
                    success=False,
                    message=str(e),
                    tier=rollout.tier,
                )
            )
            continue
        step_pct = STRATEGY_STEP_MAP[strategy]
        next_pct = min(current_pct + step_pct, final_pct)

        # --- Health gate: skip for workflow_started recovery (no sync data) ---
        if is_recovery:
            logger.info(
                "auto-advance: Recovering workflow_started rollout %s (%s, %s) "
                "— restarting workflow and advancing to %d%%",
                rollout.connector_name,
                rollout.rollout_id,
                rollout.tier,
                next_pct,
            )
        else:
            try:
                sync_info = api_client.get_actor_sync_info(
                    rollout_id=rollout.rollout_id,
                    config_api_root=constants.CLOUD_CONFIG_API_ROOT,
                    client_id=auth.client_id,
                    client_secret=auth.client_secret,
                    bearer_token=auth.bearer_token,
                )
            except Exception as e:
                logger.warning(
                    "auto-advance: Failed to fetch sync info for health gate "
                    "(rollout=%s): %s — skipping advancement as precaution",
                    rollout.rollout_id,
                    e,
                )
                result.errors.append(
                    AutopilotAction(
                        rollout_id=rollout.rollout_id,
                        actor_definition_id=rollout.actor_definition_id,
                        connector_name=rollout.connector_name,
                        rc_version=rc_version,
                        action="advance",
                        success=False,
                        message=f"Failed to fetch sync info for health gate: {e}",
                        tier=rollout.tier,
                    )
                )
                continue

            gate = check_health_gate(rollout, sync_info, strategy)
            if gate.should_rollback:
                logger.warning(
                    "auto-advance: Failure threshold hit for %s (rollout=%s): %s",
                    rollout.connector_name,
                    rollout.rollout_id,
                    gate.reason,
                )
                result.skipped.append(
                    AutopilotAction(
                        rollout_id=rollout.rollout_id,
                        actor_definition_id=rollout.actor_definition_id,
                        connector_name=rollout.connector_name,
                        rc_version=rc_version,
                        action="advance",
                        success=False,
                        message=(f"Skipped: failure threshold hit — {gate.reason}"),
                        tier=rollout.tier,
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
                    action="advance",
                    success=True,
                    message=f"Would advance {current_pct}% -> {next_pct}% (strategy={strategy})",
                    tier=rollout.tier,
                )
            )
            continue

        # For workflow_started recovery, restart the Temporal workflow via
        # manual_start before calling progress.  The platform uses
        # WORKFLOW_ID_CONFLICT_POLICY_TERMINATE_EXISTING, so this safely
        # terminates any stale workflow and starts a fresh one.
        if is_recovery:
            try:
                api_client.start_connector_rollout(
                    docker_repository=rollout.rc_docker_repository or "",
                    docker_image_tag=rc_version,
                    actor_definition_id=rollout.actor_definition_id,
                    updated_by=user_id,
                    rollout_strategy="manual",
                    config_api_root=constants.CLOUD_CONFIG_API_ROOT,
                    client_id=auth.client_id,
                    client_secret=auth.client_secret,
                    bearer_token=auth.bearer_token,
                    customer_tier=rollout.tier,
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
                        message=f"Failed to restart workflow for recovery: {e}",
                        tier=rollout.tier,
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
                    tier=rollout.tier,
                )
            )
        else:
            action_label = (
                f"Recovered workflow_started: restarted workflow and set to {next_pct}%"
                if is_recovery
                else f"Advanced {current_pct}% -> {next_pct}% (strategy={strategy})"
            )
            result.actions.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="advance",
                    success=True,
                    message=action_label,
                    tier=rollout.tier,
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

    Behaviour by tier:
    - **Non-ALL tiers** (e.g. TIER_2, TIER_1): After the health gate passes,
      starts a new concurrent rollout for the next tier via `manual_start`
      followed by `manual_rollout` at the strategy step percentage.
    - **ALL tier**: After the health gate passes, finalizes the rollout as
      succeeded (promotes to GA).

    Health gate algorithm (5-threshold model):
    1. If failures >= `ROLLOUT_FAILURE_COUNT_THRESHOLD`, recommend rollback.
    2. If elapsed < `MIN_SOAK_TIME`, wait (never promote before this).
    3. If elapsed >= `MAX_SOAK_TIME`, force progression regardless of signal.
    4. Otherwise, require both `SOAKED_SIGNAL_COUNT_THRESHOLD` (actor count)
       and `SOAKED_SIGNAL_PERCENT_THRESHOLD` (% of pinned) to pass.
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
                    tier=rollout.tier,
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
                    tier=rollout.tier,
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
                    tier=rollout.tier,
                )
            )
            continue

        raw_strategy = (
            autopilot_config.strategy.value
            if autopilot_config.strategy
            else STRATEGY_DEFAULT
        )
        try:
            strategy_key = resolve_strategy(raw_strategy)
        except ValueError as e:
            result.errors.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="promote",
                    success=False,
                    message=str(e),
                    tier=rollout.tier,
                )
            )
            continue
        current_tier = rollout.tier

        # --- Health gate: fetch sync info and evaluate ---
        try:
            sync_info = api_client.get_actor_sync_info(
                rollout_id=rollout.rollout_id,
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
                    message=f"Failed to fetch sync info for health gate: {e}",
                    tier=rollout.tier,
                )
            )
            continue

        gate = check_health_gate(rollout, sync_info, strategy_key)
        if not gate.passed:
            result.skipped.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="promote",
                    success=False,
                    message=f"Health gate not passed: {gate.reason}",
                    tier=rollout.tier,
                )
            )
            continue

        logger.info(
            "auto-promote: Health gate passed for %s (%s): %s",
            rollout.connector_name,
            rollout.rollout_id,
            gate.reason,
        )

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
                        message=(
                            f"Would finalize as succeeded (promote to GA). "
                            f"Health: {gate.reason}"
                        ),
                        tier=rollout.tier,
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
                        tier=rollout.tier,
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
                        tier=rollout.tier,
                    )
                )
        else:
            # --- Tier progression: start a new rollout for the next tier ---
            tier_idx = (
                TIER_ORDER.index(CustomerTier(current_tier))
                if current_tier in [t.value for t in TIER_ORDER]
                else len(TIER_ORDER) - 1
            )
            next_t = (
                TIER_ORDER[tier_idx + 1]
                if tier_idx + 1 < len(TIER_ORDER)
                else CustomerTier.ALL
            )
            step_pct = STRATEGY_STEP_MAP[strategy_key]

            # Deduplication guard: skip if a rollout for the next tier already
            # exists in ANY active state (not just in_progress).  A prior
            # promotion attempt may have created a rollout that is stuck in
            # workflow_started; auto-advance will recover it.
            next_tier_exists = any(
                r.tier == next_t
                and r.actor_definition_id == rollout.actor_definition_id
                and r.rc_docker_image_tag == rc_version
                for r in rollouts
                if r.rollout_id != rollout.rollout_id
            )
            if next_tier_exists:
                result.skipped.append(
                    AutopilotAction(
                        rollout_id=rollout.rollout_id,
                        actor_definition_id=rollout.actor_definition_id,
                        connector_name=rollout.connector_name,
                        rc_version=rc_version,
                        action="promote",
                        success=False,
                        message=(
                            f"Skipped: {next_t} rollout already exists "
                            f"for {rollout.connector_name} {rc_version}"
                        ),
                        tier=rollout.tier,
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
                        action="promote",
                        success=True,
                        message=(
                            f"Would promote {current_tier} -> {next_t} "
                            f"(start new rollout at {step_pct}%). "
                            f"Health: {gate.reason}"
                        ),
                        tier=rollout.tier,
                    )
                )
                continue

            # Phase 1: Start a new rollout for the next tier. The platform
            # creates a distinct rollout record tagged by tier, so both
            # the current and new rollouts coexist as IN_PROGRESS.
            try:
                start_resp = api_client.start_connector_rollout(
                    docker_repository=rollout.rc_docker_repository or "",
                    docker_image_tag=rc_version,
                    actor_definition_id=rollout.actor_definition_id,
                    updated_by=user_id,
                    rollout_strategy="manual",
                    config_api_root=constants.CLOUD_CONFIG_API_ROOT,
                    client_id=auth.client_id,
                    client_secret=auth.client_secret,
                    bearer_token=auth.bearer_token,
                    customer_tier=next_t.value,
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
                        message=(f"Failed to start {next_t} rollout: {e}"),
                        tier=rollout.tier,
                    )
                )
                continue

            new_rollout_id = start_resp.get("id") or start_resp.get("rollout_id")
            if not new_rollout_id:
                result.errors.append(
                    AutopilotAction(
                        rollout_id=rollout.rollout_id,
                        actor_definition_id=rollout.actor_definition_id,
                        connector_name=rollout.connector_name,
                        rc_version=rc_version,
                        action="promote",
                        success=False,
                        message=(
                            f"Started {next_t} rollout but response "
                            f"missing rollout ID: {start_resp}"
                        ),
                        tier=rollout.tier,
                    )
                )
                continue

            # Phase 2: Advance the new rollout to the strategy step percentage.
            try:
                api_client.progress_connector_rollout(
                    docker_repository=rollout.rc_docker_repository or "",
                    docker_image_tag=rc_version,
                    actor_definition_id=rollout.actor_definition_id,
                    rollout_id=new_rollout_id,
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
                        rollout_id=new_rollout_id,
                        actor_definition_id=rollout.actor_definition_id,
                        connector_name=rollout.connector_name,
                        rc_version=rc_version,
                        action="promote",
                        success=False,
                        message=(
                            f"Started {next_t} rollout ({new_rollout_id}) but "
                            f"failed to set initial percentage: {e}"
                        ),
                        tier=next_t.value,
                    )
                )
            else:
                logger.info(
                    "auto-promote: Promoted %s -> %s for %s (new rollout %s at %d%%)",
                    current_tier,
                    next_t,
                    rollout.connector_name,
                    new_rollout_id,
                    step_pct,
                )
                result.actions.append(
                    AutopilotAction(
                        rollout_id=new_rollout_id,
                        actor_definition_id=rollout.actor_definition_id,
                        connector_name=rollout.connector_name,
                        rc_version=rc_version,
                        action="promote",
                        success=True,
                        message=(
                            f"Promoted {current_tier} -> {next_t}: "
                            f"started new rollout {new_rollout_id} at {step_pct}%"
                        ),
                        tier=next_t.value,
                    )
                )

    logger.info("auto-promote: %s", result.summary)
    return result


def _build_ci_run_url() -> str:
    """Build the GitHub Actions run URL from standard CI env vars.

    Falls back to a generic repo URL if vars are missing.
    """
    server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    repo = os.environ.get("GITHUB_REPOSITORY", "airbytehq/airbyte-ops-mcp")
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    if run_id:
        return f"{server}/{repo}/actions/runs/{run_id}"
    return f"{server}/{repo}"


def _send_failure_threshold_hitl(
    rollout: ConnectorRolloutRecord,
    rc_version: str,
    gate: HealthGateResult,
) -> bool:
    """Send HITL notification for a rollout that hit the failure threshold.

    Uses direct Slack API call via `send_hitl_notification()` with roster-based
    person resolution. Requires `SLACK_BOT_TOKEN_HITL` env var.

    Returns `True` if the notification was sent successfully, `False` otherwise.
    Failures are logged but not raised.
    """
    message = (
        f"🚨 *Rollout paused (failure threshold)*\n\n"
        f"Connector: `{rollout.connector_name}`\n"
        f"Version: `{rc_version}`\n"
        f"Rollout ID: `{rollout.rollout_id}`\n"
        f"Tier: `{rollout.tier or 'unknown'}`\n"
        f"Current %: {rollout.current_target_rollout_pct or 0}%\n\n"
        f"Reason: {gate.reason}\n"
        f"Failures observed: {gate.failure_count}\n\n"
        f"Action required: review sync failures and decide whether to "
        f"rollback or resume the rollout."
    )
    try:
        send_hitl_notification(
            target_person=_AUTOPILOT_ESCALATION_TARGET,
            message=message,
            agent_session_url=_build_ci_run_url(),
            connector_name=rollout.connector_name,
            header_emoji="🚨",
            header_label="Rollout Failure Threshold",
        )
    except Exception as exc:
        logger.warning(
            "auto-triage-failed: Failed to send HITL notification for %s: %s",
            rollout.connector_name,
            exc,
        )
        return False
    return True


def run_auto_triage_failed(
    *,
    auth: ResolvedCloudAuth,
    connector: str | None = None,
    dry_run: bool = False,
) -> AutopilotResult:
    """Triage failed rollouts and detect failure thresholds on active rollouts.

    Two responsibilities:

    1. **Existing failures** (errored/paused): Log all, check unpin eligibility
       per `unsafeDowngrades`. Actor-level unpinning not yet implemented.
    2. **Failure threshold detection** (`in_progress` and `workflow_started`
       autopilot rollouts): Calls `check_health_gate` on active rollouts. If
       failure count >= threshold, cancels the rollout (retaining pins) and
       sends an HITL notification.  Cancellation prevents duplicate
       notifications on subsequent cron runs. Auto-advance and auto-promote
       independently skip on the same gate as defense-in-depth.
    """
    result = AutopilotResult(command="auto-triage-failed", dry_run=dry_run)

    raw_rows = query_connector_rollouts(active_only=True, limit=None)
    rollouts = [ConnectorRolloutRecord.from_db_row(r) for r in raw_rows]
    rollouts = filter_rollouts_by_connector(rollouts, connector)

    user_id = get_admin_user_id(
        client_id=auth.client_id,
        client_secret=auth.client_secret,
        bearer_token=auth.bearer_token,
    )

    # --- Part 1: Check active rollouts for failure threshold ---
    # Include workflow_started so that stuck rollouts are also triaged.
    active_for_triage = [
        r for r in rollouts if r.state in ["in_progress", "workflow_started"]
    ]
    for rollout in active_for_triage:
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
                    action="triage",
                    success=False,
                    message="Skipped: defaultRolloutMode is not 'autopilot'",
                    tier=rollout.tier,
                )
            )
            continue

        autopilot_config = rollout_config.autopilot_config or AutopilotConfig()
        raw_strategy = (
            autopilot_config.strategy.value
            if autopilot_config.strategy
            else STRATEGY_DEFAULT
        )
        try:
            strategy = resolve_strategy(raw_strategy)
        except ValueError as e:
            result.errors.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="triage",
                    success=False,
                    message=str(e),
                    tier=rollout.tier,
                )
            )
            continue

        try:
            sync_info = api_client.get_actor_sync_info(
                rollout_id=rollout.rollout_id,
                config_api_root=constants.CLOUD_CONFIG_API_ROOT,
                client_id=auth.client_id,
                client_secret=auth.client_secret,
                bearer_token=auth.bearer_token,
            )
        except Exception as e:
            logger.warning(
                "auto-triage-failed: Failed to fetch sync info for %s (rollout=%s): %s",
                rollout.connector_name,
                rollout.rollout_id,
                e,
            )
            result.errors.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="triage",
                    success=False,
                    message=f"Failed to fetch sync info: {e}",
                    tier=rollout.tier,
                )
            )
            continue

        gate = check_health_gate(rollout, sync_info, strategy)
        if not gate.should_rollback:
            continue

        logger.warning(
            "auto-triage-failed: Failure threshold hit for %s %s (rollout=%s): %s",
            rollout.connector_name,
            rc_version,
            rollout.rollout_id,
            gate.reason,
        )

        if dry_run:
            result.actions.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="triage",
                    success=True,
                    message=(
                        f"Would cancel rollout and send HITL notification "
                        f"(failure threshold): {gate.reason}"
                    ),
                    tier=rollout.tier,
                )
            )
            continue

        # Cancel the rollout (retain pins) to prevent re-notification on next run
        try:
            api_client.finalize_connector_rollout(
                docker_repository=rollout.rc_docker_repository or "",
                docker_image_tag=rc_version,
                actor_definition_id=rollout.actor_definition_id,
                rollout_id=rollout.rollout_id,
                updated_by=user_id,
                state="canceled",
                config_api_root=constants.CLOUD_CONFIG_API_ROOT,
                client_id=auth.client_id,
                client_secret=auth.client_secret,
                bearer_token=auth.bearer_token,
                error_msg=f"Failure threshold exceeded: {gate.reason}",
                retain_pins_on_cancellation=True,
            )
        except Exception as e:
            logger.warning(
                "auto-triage-failed: Failed to cancel rollout %s: %s",
                rollout.rollout_id,
                e,
            )
            result.errors.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="triage",
                    success=False,
                    message=f"Failed to cancel rollout: {e}",
                    tier=rollout.tier,
                )
            )
            continue

        sent = _send_failure_threshold_hitl(rollout, rc_version, gate)
        result.actions.append(
            AutopilotAction(
                rollout_id=rollout.rollout_id,
                actor_definition_id=rollout.actor_definition_id,
                connector_name=rollout.connector_name,
                rc_version=rc_version,
                action="triage",
                success=sent,
                message=(
                    f"Rollout canceled (retain pins) and HITL notification "
                    f"{'sent' if sent else 'FAILED'}: {gate.reason}"
                ),
                tier=rollout.tier,
            )
        )

    # --- Part 2: Triage already-failed rollouts (errored/paused) ---
    failed = [r for r in rollouts if r.state in ["errored", "paused"]]

    if not failed and not active_for_triage:
        logger.info("auto-triage-failed: No rollouts to triage.")
        return result

    for rollout in failed:
        rc_version = rollout.rc_docker_image_tag or "unknown"

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
                    tier=rollout.tier,
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
                    tier=rollout.tier,
                )
            )
            continue

        # TODO: Implement actor-level unpinning for failing connections.
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
                tier=rollout.tier,
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
                    tier=rollout.tier,
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
                    tier=rollout.tier,
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
                    tier=rollout.tier,
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
                    tier=rollout.tier,
                )
            )

    logger.info("auto-rollback-failed: %s", result.summary)
    return result


# ---------------------------------------------------------------------------
# Auto-supersede: cancel older rollouts when a newer RC exists
# ---------------------------------------------------------------------------

_SUPERSEDE_ELIGIBLE_STATES = frozenset(
    [
        "initialized",
        "workflow_started",
        "in_progress",
        "paused",
    ]
)
"""Rollout states eligible for supersession (non-terminal, non-errored)."""


def _parse_rc_version(tag: str | None) -> Version | None:
    """Parse an RC docker image tag into a `Version`, returning `None` on failure."""
    if not tag:
        return None
    try:
        return Version(tag)
    except ValueError:
        return None


def run_auto_supersede(
    *,
    auth: ResolvedCloudAuth,
    connector: str | None = None,
    dry_run: bool = False,
) -> AutopilotResult:
    """Cancel older rollouts when a newer RC rollout exists for the same connector.

    When a connector has multiple active rollouts at different RC versions,
    the older rollouts are superseded: canceled with `retain_pins_on_cancellation=True`
    so that pinned actors remain on the old version until the new rollout
    progressively advances to include them.

    The new rollout is left untouched (it will be started by `run_auto_start`).
    """
    result = AutopilotResult(command="auto-supersede", dry_run=dry_run)

    raw_rows = query_connector_rollouts(active_only=True, limit=None)
    rollouts = [ConnectorRolloutRecord.from_db_row(r) for r in raw_rows]
    rollouts = filter_rollouts_by_connector(rollouts, connector)

    # Only consider rollouts in states eligible for supersession
    eligible = [r for r in rollouts if r.state in _SUPERSEDE_ELIGIBLE_STATES]

    if not eligible:
        logger.info("auto-supersede: No eligible rollouts found.")
        return result

    # Group by actor_definition_id
    by_connector: dict[str, list[ConnectorRolloutRecord]] = defaultdict(list)
    for rollout in eligible:
        by_connector[rollout.actor_definition_id].append(rollout)

    # Find connectors with multiple active rollouts at different versions
    to_supersede: list[ConnectorRolloutRecord] = []
    for _actor_def_id, connector_rollouts in by_connector.items():
        # Parse and sort by version (highest first)
        versioned: list[tuple[Version, ConnectorRolloutRecord]] = []
        for r in connector_rollouts:
            parsed = _parse_rc_version(r.rc_docker_image_tag)
            if parsed is not None:
                versioned.append((parsed, r))

        if len(versioned) <= 1:
            continue

        versioned.sort(reverse=True, key=lambda x: x[0])
        highest_version = versioned[0][0]
        # Only supersede rollouts at strictly lower versions
        for ver, older_rollout in versioned[1:]:
            if ver < highest_version:
                to_supersede.append(older_rollout)

    if not to_supersede:
        logger.info("auto-supersede: No superseded rollouts detected.")
        return result

    user_id = get_admin_user_id(
        client_id=auth.client_id,
        client_secret=auth.client_secret,
        bearer_token=auth.bearer_token,
    )

    for rollout in to_supersede:
        rc_version = rollout.rc_docker_image_tag or "unknown"

        # Gate: only auto-supersede rollouts with autopilot mode enabled
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
                    action="supersede",
                    success=False,
                    message="Skipped: defaultRolloutMode is not 'autopilot'",
                    tier=rollout.tier,
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
                    action="supersede",
                    success=True,
                    message=(
                        f"Would cancel superseded rollout (retain pins) "
                        f"for {rollout.connector_name}@{rc_version}"
                    ),
                    tier=rollout.tier,
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
                state="canceled",
                config_api_root=constants.CLOUD_CONFIG_API_ROOT,
                client_id=auth.client_id,
                client_secret=auth.client_secret,
                bearer_token=auth.bearer_token,
                error_msg=(
                    "AutoPilot auto-supersede: newer RC version published; "
                    "retaining pins for progressive migration"
                ),
                failed_reason="superseded_by_newer_rc",
                retain_pins_on_cancellation=True,
            )
        except Exception as e:
            result.errors.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="supersede",
                    success=False,
                    message=f"Failed to supersede: {e}",
                    tier=rollout.tier,
                )
            )
        else:
            result.actions.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="supersede",
                    success=True,
                    message=(
                        f"Canceled superseded rollout (pins retained) "
                        f"for {rollout.connector_name}@{rc_version}"
                    ),
                    tier=rollout.tier,
                )
            )

    logger.info("auto-supersede: %s", result.summary)
    return result
