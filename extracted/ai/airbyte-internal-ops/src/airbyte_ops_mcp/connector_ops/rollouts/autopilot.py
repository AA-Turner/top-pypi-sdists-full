# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Command implementations for the AutoPilot progressive rollout system.

Each function queries prod DB for relevant rollouts, applies metadata gates
from the compiled registry, and executes actions via the Cloud Config API.
"""

from __future__ import annotations

import logging
import os
from collections import defaultdict
from datetime import datetime, timezone
from typing import Literal

import requests
import sqlalchemy.exc
from airbyte import constants
from airbyte.exceptions import PyAirbyteInputError
from airbyte_connector_models.metadata.v0.connector_registry_v0 import (
    ConnectorRegistryV0ConnectorRegistryReleasesRolloutConfigurationAutopilotConfig as AutopilotConfig,
)
from airbyte_connector_models.metadata.v0.connector_registry_v0 import (
    ConnectorRegistryV0ConnectorRegistryReleasesRolloutConfigurationDefaultRolloutMode as RolloutMode,
)
from packaging.version import InvalidVersion, Version

from airbyte_ops_mcp.cloud_admin import api_client
from airbyte_ops_mcp.cloud_admin.auth import get_admin_user_id
from airbyte_ops_mcp.cloud_admin.version_overrides import ResolvedCloudAuth
from airbyte_ops_mcp.connector_ops.rollouts._helpers import (
    HealthGateResult,
    TierEligibilityEstimate,
    check_health_gate,
    count_eligible_or_pinned_actors,
    estimate_tier_eligible_actors,
    filter_rollouts_by_connector,
    get_connector_rollout_config,
    get_registry_default_version,
    get_registry_release_candidates,
    get_unsafe_downgrades,
    parse_db_timestamp,
)
from airbyte_ops_mcp.connector_ops.rollouts.constants import (
    FINALIZING_GRACE_MINUTES,
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
# Shared guards
# ---------------------------------------------------------------------------


def _safe_estimate(
    *,
    actor_definition_id: str,
    docker_repository: str,
    tier: str,
    action: str,
) -> TierEligibilityEstimate:
    """Run `estimate_tier_eligible_actors`, tolerating prod-DB read failures.

    The pre-flight estimate is an optimization, not the authority.  If the
    estimate can't be computed — a bad input, a transient SQL error, or a tier
    cache that can't be loaded/refreshed (`RuntimeError` from
    `tier_cache._load_tier_cache` when BigQuery fails and no stale cache
    exists) — this logs and returns an "unavailable" estimate
    (`eligible_actor_count == -1`).  Non-recovery callers then fall through to
    the platform's authoritative actor count, and the `workflow_started`
    recovery guard skips rather than re-driving a tier it can't confirm.
    """
    try:
        return estimate_tier_eligible_actors(
            actor_definition_id=actor_definition_id,
            docker_repository=docker_repository,
            tier=tier,
        )
    except (PyAirbyteInputError, sqlalchemy.exc.SQLAlchemyError, RuntimeError) as e:
        logger.warning(
            "auto-%s: could not estimate eligibility for %s (%s): %s "
            "— returning an unavailable estimate; the normal in-progress path "
            "falls back to the platform actor count, while workflow_started "
            "recovery skips (no platform sync info yet)",
            action,
            actor_definition_id,
            tier,
            e,
        )
        return TierEligibilityEstimate(
            tier=tier,
            eligible_actor_count=-1,
            disposition="normal",
            reason="eligibility estimate unavailable",
        )


def _recovery_tier_action(
    estimate: TierEligibilityEstimate,
) -> Literal["complete", "skip", "proceed"]:
    """Decide how to handle a `workflow_started` rollout from its tier estimate.

    A `workflow_started` rollout has no platform sync info yet, so the local
    pre-flight estimate is the only eligibility signal available:

    - `complete`: the tier is confirmed empty (`disposition == "skip"` with a
      non-negative count).  Zero-of-zero eligible actors is *done*, not stuck —
      the caller finalizes the rollout as `succeeded` (promotes the RC to GA)
      instead of leaving it wedged.
    - `skip`: the estimate is unavailable (`eligible_actor_count < 0`).  We can't
      confirm the tier is empty or populated, so defer to a later cron cycle
      rather than re-drive a possibly-empty tier and wedge it again.
    - `proceed`: the tier has eligible actors — recover by restarting the
      workflow and advancing to the initial percentage.
    """
    if estimate.eligible_actor_count < 0:
        return "skip"
    if estimate.disposition == "skip":
        return "complete"
    return "proceed"


def _select_forward_tier(
    *,
    actor_definition_id: str,
    docker_repository: str,
    current_tier: str,
    action: str,
) -> tuple[
    Literal["start", "ga", "unavailable"],
    CustomerTier | None,
    TierEligibilityEstimate | None,
]:
    """Scan `TIER_ORDER` forward for the next tier that has eligible actors.

    Starting just after `current_tier`, this estimates each later tier in order
    and returns a decision for the first tier with a confirmed, non-empty
    estimate — skipping empty intermediate tiers rather than starting a rollout
    that would wedge at `workflow_started`:

    - `("start", tier, estimate)`: `tier` has eligible actors — start a rollout
      there.
    - `("ga", None, None)`: every later tier is confirmed empty, so no customer
      tier remains to roll out to — finalize the current tier to GA.
    - `("unavailable", tier, estimate)`: a candidate tier's estimate could not be
      computed; defer rather than risk skipping a populated tier or wedging an
      empty one.
    """
    order_values = [t.value for t in TIER_ORDER]
    if current_tier in order_values:
        start_idx = order_values.index(current_tier) + 1
    else:
        # A tier not in `TIER_ORDER` (e.g. a legacy `ALL` stage) has no later
        # cohort to roll out to; the only forward move is GA.
        start_idx = len(TIER_ORDER)

    for candidate in TIER_ORDER[start_idx:]:
        estimate = _safe_estimate(
            actor_definition_id=actor_definition_id,
            docker_repository=docker_repository,
            tier=candidate.value,
            action=action,
        )
        if estimate.eligible_actor_count < 0:
            return "unavailable", candidate, estimate
        if estimate.disposition == "skip":
            continue
        return "start", candidate, estimate

    return "ga", None, None


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

    # Track `(actor_definition_id, rc_version)` pairs already finalized to GA in
    # this pass. Finalizing any one of an RC's tier rollouts as `succeeded`
    # promotes the whole RC to GA, so a connector with several empty
    # `workflow_started` records must promote exactly once.
    finalized_rcs: set[tuple[str, str]] = set()

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
            # A `workflow_started` rollout has no sync info yet, so the local
            # pre-flight estimate is the only eligibility signal. It classifies
            # the tier as complete (confirmed empty — 0/0 is done), skip
            # (unavailable — can't confirm), or proceed (has actors — recover).
            estimate = _safe_estimate(
                actor_definition_id=rollout.actor_definition_id,
                docker_repository=rollout.rc_docker_repository or "",
                tier=rollout.tier,
                action="advance",
            )
            recovery_action = _recovery_tier_action(estimate)

            if recovery_action == "skip":
                logger.info(
                    "auto-advance: %s (%s, %s) — %s",
                    rollout.connector_name,
                    rollout.rollout_id,
                    rollout.tier,
                    estimate.reason,
                )
                result.skipped.append(
                    AutopilotAction(
                        rollout_id=rollout.rollout_id,
                        actor_definition_id=rollout.actor_definition_id,
                        connector_name=rollout.connector_name,
                        rc_version=rc_version,
                        action="advance",
                        success=False,
                        message=f"Skipped: {estimate.reason}",
                        tier=rollout.tier,
                    )
                )
                continue

            if recovery_action == "complete":
                # Zero-of-zero eligible actors is *done*, not stuck. Finalize the
                # empty `workflow_started` rollout as `succeeded` (promote the RC
                # to GA) so it stops wedging the queue.
                rc_key = (rollout.actor_definition_id, rc_version)
                if rc_key in finalized_rcs:
                    result.skipped.append(
                        AutopilotAction(
                            rollout_id=rollout.rollout_id,
                            actor_definition_id=rollout.actor_definition_id,
                            connector_name=rollout.connector_name,
                            rc_version=rc_version,
                            action="complete",
                            success=False,
                            message=(
                                "Skipped: RC already finalized to GA this pass "
                                "(sibling tier)"
                            ),
                            tier=rollout.tier,
                        )
                    )
                    continue

                if dry_run:
                    finalized_rcs.add(rc_key)
                    result.actions.append(
                        AutopilotAction(
                            rollout_id=rollout.rollout_id,
                            actor_definition_id=rollout.actor_definition_id,
                            connector_name=rollout.connector_name,
                            rc_version=rc_version,
                            action="complete",
                            success=True,
                            message=(
                                f"Would finalize empty tier as succeeded "
                                f"(0/0 complete → GA): {estimate.reason}"
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
                except (
                    PyAirbyteInputError,
                    requests.exceptions.RequestException,
                ) as e:
                    result.errors.append(
                        AutopilotAction(
                            rollout_id=rollout.rollout_id,
                            actor_definition_id=rollout.actor_definition_id,
                            connector_name=rollout.connector_name,
                            rc_version=rc_version,
                            action="complete",
                            success=False,
                            message=(
                                f"Empty tier (0 eligible actors) but failed to "
                                f"finalize as succeeded: {e}"
                            ),
                            tier=rollout.tier,
                        )
                    )
                else:
                    finalized_rcs.add(rc_key)
                    logger.info(
                        "auto-advance: finalized empty workflow_started rollout "
                        "%s (%s, %s) as succeeded (0/0 complete → GA)",
                        rollout.connector_name,
                        rollout.rollout_id,
                        rollout.tier,
                    )
                    result.actions.append(
                        AutopilotAction(
                            rollout_id=rollout.rollout_id,
                            actor_definition_id=rollout.actor_definition_id,
                            connector_name=rollout.connector_name,
                            rc_version=rc_version,
                            action="complete",
                            success=True,
                            message=(
                                "Empty tier (0 eligible actors): finalized as "
                                "succeeded (0/0 complete → promoted to GA)"
                            ),
                            tier=rollout.tier,
                        )
                    )
                continue

            if estimate.disposition == "warn":
                logger.warning(
                    "auto-advance: %s (%s, %s) — %s",
                    rollout.connector_name,
                    rollout.rollout_id,
                    rollout.tier,
                    estimate.reason,
                )
                result.warnings.append(
                    AutopilotAction(
                        rollout_id=rollout.rollout_id,
                        actor_definition_id=rollout.actor_definition_id,
                        connector_name=rollout.connector_name,
                        rc_version=rc_version,
                        action="advance",
                        success=True,
                        message=f"Proceeding despite low eligibility: {estimate.reason}",
                        tier=rollout.tier,
                    )
                )

            logger.info(
                "auto-advance: Recovering workflow_started rollout %s (%s, %s) "
                "— restarting workflow and advancing to %d%% (%s)",
                rollout.connector_name,
                rollout.rollout_id,
                rollout.tier,
                next_pct,
                estimate.reason,
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

            # Layer 2 backstop: confirm the platform actually has eligible or
            # pinned actors before progressing. The ops tier lists can drift
            # from the platform's actor selection; a zero here means progressing
            # would throw `ConnectorRolloutNotEnoughActorsProblem` and wedge the
            # rollout, so treat it as a valid "nothing to advance" and skip.
            if count_eligible_or_pinned_actors(sync_info) == 0:
                logger.info(
                    "auto-advance: %s (%s, %s) has 0 eligible or pinned actors "
                    "— skipping advancement (nothing to do)",
                    rollout.connector_name,
                    rollout.rollout_id,
                    rollout.tier,
                )
                result.skipped.append(
                    AutopilotAction(
                        rollout_id=rollout.rollout_id,
                        actor_definition_id=rollout.actor_definition_id,
                        connector_name=rollout.connector_name,
                        rc_version=rc_version,
                        action="advance",
                        success=False,
                        message=(
                            "Skipped: 0 eligible or pinned actors "
                            "(empty tier — nothing to advance)"
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
    in_progress = [r for r in rollouts if r.state == "in_progress"]
    finalizing = [r for r in rollouts if r.state == "finalizing"]

    if not in_progress and not finalizing:
        logger.info("auto-promote: No IN_PROGRESS or FINALIZING rollouts found.")
        return result

    user_id = get_admin_user_id(
        client_id=auth.client_id,
        client_secret=auth.client_secret,
        bearer_token=auth.bearer_token,
    )

    # Track `(actor_definition_id, rc_version)` pairs already finalized to GA in
    # this pass. Finalizing any one of an RC's tier rollouts as `succeeded`
    # promotes the whole RC to GA, so an RC with multiple coexisting in-progress
    # tier records must promote exactly once.
    finalized_rcs: set[tuple[str, str]] = set()

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

        rc_key = (rollout.actor_definition_id, rc_version)

        if current_tier == "ALL":
            if rc_key in finalized_rcs:
                result.skipped.append(
                    AutopilotAction(
                        rollout_id=rollout.rollout_id,
                        actor_definition_id=rollout.actor_definition_id,
                        connector_name=rollout.connector_name,
                        rc_version=rc_version,
                        action="promote",
                        success=False,
                        message=(
                            "Skipped: RC already finalized to GA this pass "
                            "(sibling tier)"
                        ),
                        tier=rollout.tier,
                    )
                )
                continue

            if dry_run:
                finalized_rcs.add(rc_key)
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
            except (PyAirbyteInputError, requests.exceptions.RequestException) as e:
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
                finalized_rcs.add(rc_key)
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
            # --- Tier progression: scan forward for the next tier with actors --
            # Rather than only considering the immediate next sequential tier,
            # scan `TIER_ORDER` forward and start the first later tier that has
            # eligible actors, skipping empty intermediate tiers (starting an
            # empty tier would throw `ConnectorRolloutNotEnoughActorsProblem` and
            # wedge it at `workflow_started`). If no later customer tier has
            # actors, the next eligible action is GA promotion — already gated
            # above by `autoPromoteStages`.
            step_pct = STRATEGY_STEP_MAP[strategy_key]
            kind, next_t, next_estimate = _select_forward_tier(
                actor_definition_id=rollout.actor_definition_id,
                docker_repository=rollout.rc_docker_repository or "",
                current_tier=current_tier,
                action="promote",
            )

            if kind == "unavailable":
                # A candidate tier's estimate couldn't be computed; defer rather
                # than risk skipping a populated tier or wedging an empty one.
                result.skipped.append(
                    AutopilotAction(
                        rollout_id=rollout.rollout_id,
                        actor_definition_id=rollout.actor_definition_id,
                        connector_name=rollout.connector_name,
                        rc_version=rc_version,
                        action="promote",
                        success=False,
                        message=(
                            f"Skipped: eligibility estimate unavailable for "
                            f"{next_t.value} — deferring promotion"
                        ),
                        tier=rollout.tier,
                    )
                )
                continue

            if kind == "ga":
                # No later customer tier has eligible actors — promote the
                # current, validated tier straight to GA.
                if rc_key in finalized_rcs:
                    result.skipped.append(
                        AutopilotAction(
                            rollout_id=rollout.rollout_id,
                            actor_definition_id=rollout.actor_definition_id,
                            connector_name=rollout.connector_name,
                            rc_version=rc_version,
                            action="promote",
                            success=False,
                            message=(
                                "Skipped: RC already finalized to GA this pass "
                                "(sibling tier)"
                            ),
                            tier=rollout.tier,
                        )
                    )
                    continue

                if dry_run:
                    finalized_rcs.add(rc_key)
                    result.actions.append(
                        AutopilotAction(
                            rollout_id=rollout.rollout_id,
                            actor_definition_id=rollout.actor_definition_id,
                            connector_name=rollout.connector_name,
                            rc_version=rc_version,
                            action="promote",
                            success=True,
                            message=(
                                f"Would finalize {current_tier} as GA (no later "
                                f"tier with eligible actors). Health: {gate.reason}"
                            ),
                            tier=rollout.tier,
                        )
                    )
                    continue

                logger.info(
                    "auto-promote: no later tier has actors for %s (%s); "
                    "finalizing current tier %s as GA",
                    rollout.connector_name,
                    rollout.rollout_id,
                    current_tier,
                )
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
                except (
                    PyAirbyteInputError,
                    requests.exceptions.RequestException,
                ) as e:
                    result.errors.append(
                        AutopilotAction(
                            rollout_id=rollout.rollout_id,
                            actor_definition_id=rollout.actor_definition_id,
                            connector_name=rollout.connector_name,
                            rc_version=rc_version,
                            action="promote",
                            success=False,
                            message=(
                                f"No later tier has actors but failed to "
                                f"finalize {current_tier} as GA: {e}"
                            ),
                            tier=rollout.tier,
                        )
                    )
                else:
                    finalized_rcs.add(rc_key)
                    result.actions.append(
                        AutopilotAction(
                            rollout_id=rollout.rollout_id,
                            actor_definition_id=rollout.actor_definition_id,
                            connector_name=rollout.connector_name,
                            rc_version=rc_version,
                            action="promote",
                            success=True,
                            message=(
                                f"No later tier has eligible actors; finalized "
                                f"{current_tier} as succeeded (promoted to GA)"
                            ),
                            tier=rollout.tier,
                        )
                    )
                continue

            # kind == "start": `next_t` has eligible actors.
            if next_estimate is not None and next_estimate.disposition == "warn":
                logger.warning(
                    "auto-promote: %s (%s) — next tier %s: %s",
                    rollout.connector_name,
                    rollout.rollout_id,
                    next_t,
                    next_estimate.reason,
                )
                result.warnings.append(
                    AutopilotAction(
                        rollout_id=rollout.rollout_id,
                        actor_definition_id=rollout.actor_definition_id,
                        connector_name=rollout.connector_name,
                        rc_version=rc_version,
                        action="promote",
                        success=True,
                        message=(
                            f"Proceeding to {next_t.value} despite low eligibility: "
                            f"{next_estimate.reason}"
                        ),
                        tier=next_t.value,
                    )
                )

            # Deduplication guard: skip if a rollout for the chosen tier already
            # exists in ANY active state (not just in_progress). A prior pass may
            # have started it; auto-advance will recover or complete it.
            next_tier_exists = any(
                r.tier == next_t.value
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
                            f"Skipped: {next_t.value} rollout already exists "
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
                            f"Would promote {current_tier} -> {next_t.value} "
                            f"(start new rollout at {step_pct}%). "
                            f"Health: {gate.reason}"
                        ),
                        tier=rollout.tier,
                    )
                )
                continue

            # Start a new rollout for the chosen tier. The platform creates a
            # distinct rollout record tagged by tier, so both the current and
            # new rollouts coexist as IN_PROGRESS.
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
                        message=(f"Failed to start {next_t.value} rollout: {e}"),
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
                            f"Started {next_t.value} rollout but response "
                            f"missing rollout ID: {start_resp}"
                        ),
                        tier=rollout.tier,
                    )
                )
                continue

            # Platform drift backstop: the forward scan already chose a tier
            # with a positive *local* estimate, but the platform's own actor
            # selection can differ. If the freshly-started tier actually has zero
            # eligible actors, progressing it would throw
            # `ConnectorRolloutNotEnoughActorsProblem` and wedge it at
            # `workflow_started`. Cancel the empty rollout (retaining pins) and
            # finalize the current, validated tier to GA instead.
            next_tier_eligible: int | None = None
            try:
                next_sync_info = api_client.get_actor_sync_info(
                    rollout_id=new_rollout_id,
                    config_api_root=constants.CLOUD_CONFIG_API_ROOT,
                    client_id=auth.client_id,
                    client_secret=auth.client_secret,
                    bearer_token=auth.bearer_token,
                )
                next_tier_eligible = count_eligible_or_pinned_actors(next_sync_info)
            except (PyAirbyteInputError, requests.exceptions.RequestException) as e:
                # If eligibility can't be determined (bad input or a network-level
                # failure), fall through to the normal progress path rather than
                # blocking promotion.
                logger.warning(
                    "auto-promote: could not fetch eligibility for new %s "
                    "rollout %s: %s",
                    next_t,
                    new_rollout_id,
                    e,
                )

            if next_tier_eligible == 0:
                logger.info(
                    "auto-promote: %s tier is empty for %s (0 eligible actors); "
                    "canceling empty rollout %s and promoting current tier %s "
                    "to GA",
                    next_t,
                    rollout.connector_name,
                    new_rollout_id,
                    current_tier,
                )
                cancel_failed = False
                try:
                    api_client.finalize_connector_rollout(
                        docker_repository=rollout.rc_docker_repository or "",
                        docker_image_tag=rc_version,
                        actor_definition_id=rollout.actor_definition_id,
                        rollout_id=new_rollout_id,
                        updated_by=user_id,
                        state="canceled",
                        retain_pins_on_cancellation=True,
                        config_api_root=constants.CLOUD_CONFIG_API_ROOT,
                        client_id=auth.client_id,
                        client_secret=auth.client_secret,
                        bearer_token=auth.bearer_token,
                    )
                except (
                    PyAirbyteInputError,
                    requests.exceptions.RequestException,
                ) as e:
                    cancel_failed = True
                    result.errors.append(
                        AutopilotAction(
                            rollout_id=new_rollout_id,
                            actor_definition_id=rollout.actor_definition_id,
                            connector_name=rollout.connector_name,
                            rc_version=rc_version,
                            action="promote",
                            success=False,
                            message=(
                                f"{next_t.value} tier is empty (0 eligible actors) but "
                                f"failed to cancel the empty rollout: {e}"
                            ),
                            tier=next_t.value,
                        )
                    )
                if cancel_failed:
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
                except (
                    PyAirbyteInputError,
                    requests.exceptions.RequestException,
                ) as e:
                    result.errors.append(
                        AutopilotAction(
                            rollout_id=rollout.rollout_id,
                            actor_definition_id=rollout.actor_definition_id,
                            connector_name=rollout.connector_name,
                            rc_version=rc_version,
                            action="promote",
                            success=False,
                            message=(
                                f"Canceled empty {next_t.value} rollout but failed to "
                                f"finalize current tier {current_tier} as GA: {e}"
                            ),
                            tier=rollout.tier,
                        )
                    )
                else:
                    finalized_rcs.add(rc_key)
                    result.actions.append(
                        AutopilotAction(
                            rollout_id=rollout.rollout_id,
                            actor_definition_id=rollout.actor_definition_id,
                            connector_name=rollout.connector_name,
                            rc_version=rc_version,
                            action="promote",
                            success=True,
                            message=(
                                f"Skipped empty {next_t.value} tier (0 eligible actors); "
                                f"canceled empty rollout {new_rollout_id} "
                                f"(pins retained) and finalized {current_tier} as "
                                f"succeeded (promoted to GA)"
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
                            f"Started {next_t.value} rollout ({new_rollout_id}) but "
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
                            f"Promoted {current_tier} -> {next_t.value}: "
                            f"started new rollout {new_rollout_id} at {step_pct}%"
                        ),
                        tier=next_t.value,
                    )
                )

    _reconcile_finalizing_rollouts(
        finalizing=finalizing,
        auth=auth,
        user_id=user_id,
        result=result,
        dry_run=dry_run,
    )

    logger.info("auto-promote: %s", result.summary)
    return result


def _reconcile_finalizing_rollouts(
    *,
    finalizing: list[ConnectorRolloutRecord],
    auth: ResolvedCloudAuth,
    user_id: str,
    result: AutopilotResult,
    dry_run: bool,
) -> None:
    """Reconcile rollouts stuck in `finalizing` as part of auto-promote.

    A finalize sets `finalizing`, dispatches the GitHub promote workflow, and
    waits (via a Temporal `verifyDefaultVersion` poll) for the registry default
    to flip to the GA version before recording the terminal transition. If that
    Temporal run dies, the row stays `finalizing` forever even after GA is live.

    For each rollout past `FINALIZING_GRACE_MINUTES`:

    - **GA is already the registry default** → re-finalize (`succeeded`). A
      fresh Temporal run sees the default already flipped and closes the row.
      This is the safe, idempotent auto-heal (the faker/pokeapi case).
    - **GA is not yet the default** → record a warning for human review rather
      than auto-dispatching the promote workflow from the cron. The GA flip
      hasn't happened, so re-finalizing risks superseding the rollout; the
      Webapp's Re-drive Finalize control drives that remediation deliberately.

    Rollouts within the grace window — or whose `updated_at` can't be parsed,
    so the elapsed time can't be confirmed — are left alone (still settling).
    """
    now = datetime.now(tz=timezone.utc)
    for rollout in finalizing:
        rc_version = rollout.rc_docker_image_tag or "unknown"
        updated_at = parse_db_timestamp(rollout.updated_at)
        if updated_at is None:
            # Fail closed: without a parseable timestamp we can't confirm the
            # rollout is past the grace window, and re-finalizing prematurely
            # could supersede a still-settling rollout. Flag for review instead.
            result.warnings.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="reconcile-finalizing",
                    success=False,
                    message=(
                        "Stuck finalizing but updated_at is missing/unparseable; "
                        "cannot confirm the grace window elapsed. Needs review."
                    ),
                    tier=rollout.tier,
                )
            )
            continue

        elapsed_min = (now - updated_at).total_seconds() / 60
        if elapsed_min < FINALIZING_GRACE_MINUTES:
            result.skipped.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="reconcile-finalizing",
                    success=False,
                    message=(
                        f"Skipped: finalizing for {elapsed_min:.0f}m "
                        f"(< {FINALIZING_GRACE_MINUTES}m grace)"
                    ),
                    tier=rollout.tier,
                )
            )
            continue

        try:
            ga_version = Version(rc_version).base_version
        except InvalidVersion:
            result.warnings.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="reconcile-finalizing",
                    success=False,
                    message=(
                        f"Stuck finalizing but the RC tag ({rc_version}) is not a "
                        f"parseable version; cannot verify the GA default. "
                        f"Needs review."
                    ),
                    tier=rollout.tier,
                )
            )
            continue
        try:
            registry_default = get_registry_default_version(rollout.actor_definition_id)
            ga_is_default = registry_default is not None and Version(
                registry_default
            ) == Version(ga_version)
        except (PyAirbyteInputError, InvalidVersion) as e:
            result.warnings.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="reconcile-finalizing",
                    success=False,
                    message=(
                        f"Stuck finalizing but could not resolve the registry "
                        f"default to verify GA {ga_version}: {e}. Needs review."
                    ),
                    tier=rollout.tier,
                )
            )
            continue

        if not ga_is_default:
            result.warnings.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="reconcile-finalizing",
                    success=False,
                    message=(
                        f"Stuck finalizing: GA {ga_version} is not the registry "
                        f"default (default={registry_default}). Needs review — "
                        f"re-drive the promote workflow via the Webapp"
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
                    action="reconcile-finalizing",
                    success=True,
                    message=(
                        f"Would re-finalize (GA {ga_version} already the registry "
                        f"default) to close the stuck finalizing row"
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
        except (PyAirbyteInputError, requests.exceptions.RequestException) as e:
            result.errors.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="reconcile-finalizing",
                    success=False,
                    message=(
                        f"GA {ga_version} is the registry default but re-finalize "
                        f"to close the stuck row failed: {e}"
                    ),
                    tier=rollout.tier,
                )
            )
        else:
            logger.info(
                "auto-promote: re-finalized stuck rollout %s (%s, GA %s already "
                "default) to close it",
                rollout.rollout_id,
                rollout.connector_name,
                ga_version,
            )
            result.actions.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="reconcile-finalizing",
                    success=True,
                    message=(
                        f"Re-finalized stuck finalizing rollout (GA {ga_version} "
                        f"already the registry default) to close it as succeeded"
                    ),
                    tier=rollout.tier,
                )
            )


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
# Auto-close: close rollouts that are no longer the connector's active candidate
# ---------------------------------------------------------------------------

_CLOSE_ELIGIBLE_STATES = frozenset(
    [
        "initialized",
        "workflow_started",
        "in_progress",
        "paused",
    ]
)
"""Rollout states eligible for closing (non-terminal, non-errored)."""


def _parse_rc_version(tag: str | None) -> Version | None:
    """Parse an RC docker image tag into a `Version`, returning `None` on failure."""
    if not tag:
        return None
    try:
        return Version(tag)
    except ValueError:
        return None


def _rc_is_already_ga(
    rollout: ConnectorRolloutRecord,
    default_versions: dict[str, str | None],
) -> bool:
    """Return whether the rollout's RC version is already the registry GA default.

    A rollout whose RC equals the connector's current registry default is
    redundant: the version is already generally available, so no progressive
    rollout is needed. `default_versions` caches one registry lookup per
    `actor_definition_id` across the run.
    """
    parsed_rc = _parse_rc_version(rollout.rc_docker_image_tag)
    if parsed_rc is None:
        return False
    adid = rollout.actor_definition_id
    if adid not in default_versions:
        try:
            default_versions[adid] = get_registry_default_version(adid)
        except (PyAirbyteInputError, InvalidVersion):
            default_versions[adid] = None
    default = default_versions[adid]
    if default is None:
        return False
    try:
        return Version(default) == Version(parsed_rc.base_version)
    except InvalidVersion:
        return False


def _parse_candidate_versions(candidates: list[str]) -> list[Version]:
    """Parse advertised candidate keys into `Version`s, dropping unparseable ones."""
    parsed: list[Version] = []
    for candidate in candidates:
        try:
            parsed.append(Version(candidate))
        except InvalidVersion:
            continue
    return parsed


def _rc_matches_highest_candidate(
    rollout: ConnectorRolloutRecord,
    candidates: list[str],
) -> bool:
    """Return whether the rollout's RC is the highest advertised release candidate.

    `candidates` is the connector's `releases.releaseCandidates` version list
    from the compiled registry. The highest-priority candidate is the max
    semver among them. Returns `False` when `candidates` is empty (nothing is
    advertised, so no RC can match) or when the RC / candidates are unparseable.

    Matching is prerelease-aware to avoid two failure modes: when the rollout tag
    carries an explicit prerelease suffix (e.g. `0.2.5-rc.2`), it must match the
    highest candidate *exactly*, so a newer prerelease of the same base
    (`0.2.5-rc.3`) correctly supersedes it; when the rollout tag has no suffix
    (e.g. `0.2.5`), base versions are compared so a registry key that carries a
    suffix (`0.2.5-rc.1`) still matches its own base and is not wrongly closed.
    """
    parsed_rc = _parse_rc_version(rollout.rc_docker_image_tag)
    if parsed_rc is None:
        return False
    parsed_candidates = _parse_candidate_versions(candidates)
    if not parsed_candidates:
        return False
    highest = max(parsed_candidates)
    if parsed_rc.pre is not None:
        return parsed_rc == highest
    return Version(parsed_rc.base_version) == Version(highest.base_version)


def run_auto_close(
    *,
    auth: ResolvedCloudAuth,
    connector: str | None = None,
    dry_run: bool = False,
) -> AutopilotResult:
    """Close rollouts a connector no longer needs, so only its active candidate remains.

    Three conditions close a rollout (all with `retain_pins_on_cancellation=True`,
    so pinned actors are left undisturbed — pin cleanup is a separate step and
    auto-close never removes pins):

    - **Case A — superseded by a newer RC** (`superseded_by_newer_rc`): when a
      connector has active rollouts at multiple RC versions, the lower versions
      are closed so only the newest RC keeps advancing.
    - **Case B — RC already GA** (`already_ga`): when a rollout's RC is already
      the connector's registry default version, the version is generally
      available and the rollout is closed. This clears the zombie rollout the
      platform re-creates for an already-promoted version.
    - **Else — not the highest advertised candidate** (`not_highest_candidate`):
      the registry-driven catch-all. If a rollout survives A and B but its RC is
      not the highest-priority candidate in the connector's compiled
      `releaseCandidates` (including the case where none is advertised), it is
      obsolete and closed. This absorbs race-condition leftovers.

    All three fail closed: when the registry can't be resolved for a connector,
    its rollout is left untouched. Only rollouts whose connector has
    `defaultRolloutMode == autopilot` are acted on.
    """
    result = AutopilotResult(command="auto-close", dry_run=dry_run)

    raw_rows = query_connector_rollouts(active_only=True, limit=None)
    rollouts = [ConnectorRolloutRecord.from_db_row(r) for r in raw_rows]
    rollouts = filter_rollouts_by_connector(rollouts, connector)

    # Only consider rollouts in states eligible for closing
    eligible = [r for r in rollouts if r.state in _CLOSE_ELIGIBLE_STATES]

    if not eligible:
        logger.info("auto-close: No eligible rollouts found.")
        return result

    # Group by actor_definition_id
    by_connector: dict[str, list[ConnectorRolloutRecord]] = defaultdict(list)
    for rollout in eligible:
        by_connector[rollout.actor_definition_id].append(rollout)

    # `(rollout, reason)` pairs; `reason` drives the log/close message.
    to_cancel: list[tuple[ConnectorRolloutRecord, str]] = []
    queued_ids: set[str] = set()

    # Case A: superseded by a newer active RC for the same connector.
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
                to_cancel.append((older_rollout, "newer_rc"))
                queued_ids.add(older_rollout.rollout_id)

    # Case B: RC already the registry GA default (rollout no longer needed).
    default_versions: dict[str, str | None] = {}
    for rollout in eligible:
        if rollout.rollout_id in queued_ids:
            continue
        if _rc_is_already_ga(rollout, default_versions):
            to_cancel.append((rollout, "already_ga"))
            queued_ids.add(rollout.rollout_id)

    # Else (catch-all): not the highest advertised release candidate. Fails
    # closed — an unresolved registry (`None`) or an unparseable RC tag leaves
    # the rollout untouched, since neither can be reasoned about safely.
    candidates_cache: dict[str, list[str] | None] = {}
    for rollout in eligible:
        if rollout.rollout_id in queued_ids:
            continue
        if _parse_rc_version(rollout.rc_docker_image_tag) is None:
            continue
        adid = rollout.actor_definition_id
        if adid not in candidates_cache:
            try:
                candidates_cache[adid] = get_registry_release_candidates(adid)
            except PyAirbyteInputError:
                candidates_cache[adid] = None
        candidates = candidates_cache[adid]
        if candidates is None:
            continue
        if candidates and not _parse_candidate_versions(candidates):
            # Candidates are advertised but none parse as semver: the highest
            # candidate can't be determined, so fail closed and leave it alone.
            # (An empty list is different — nothing is advertised, so close.)
            continue
        if not _rc_matches_highest_candidate(rollout, candidates):
            to_cancel.append((rollout, "not_highest_candidate"))
            queued_ids.add(rollout.rollout_id)

    if not to_cancel:
        logger.info("auto-close: No obsolete rollouts detected.")
        return result

    # Resolved lazily below (only when a real closure runs) so a dry run stays
    # preview-only and does not depend on admin auth.
    user_id: str | None = None

    for rollout, reason in to_cancel:
        rc_version = rollout.rc_docker_image_tag or "unknown"

        # Gate: only auto-close rollouts with autopilot mode enabled
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
                    action="close",
                    success=False,
                    message="Skipped: defaultRolloutMode is not 'autopilot'",
                    tier=rollout.tier,
                )
            )
            continue

        if reason == "already_ga":
            reason_msg = f"RC {rc_version} is already the registry GA default"
            failed_reason = "already_ga"
            error_msg = (
                "AutoPilot auto-close: RC already GA (registry default); "
                "closing obsolete rollout"
            )
        elif reason == "not_highest_candidate":
            reason_msg = (
                f"RC {rc_version} is not the highest advertised release "
                f"candidate for {rollout.connector_name}"
            )
            failed_reason = "not_highest_candidate"
            error_msg = (
                "AutoPilot auto-close: RC is not the highest registry release "
                "candidate; closing obsolete rollout"
            )
        else:
            reason_msg = (
                f"superseded: a newer RC exists for {rollout.connector_name}, "
                f"so this RC {rc_version} rollout is obsolete"
            )
            failed_reason = "superseded_by_newer_rc"
            error_msg = (
                "AutoPilot auto-close: newer RC version published; "
                "retaining pins for progressive migration"
            )

        if dry_run:
            result.actions.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="close",
                    success=True,
                    message=f"Would close obsolete rollout (retain pins): {reason_msg}",
                    tier=rollout.tier,
                )
            )
            continue

        if user_id is None:
            user_id = get_admin_user_id(
                client_id=auth.client_id,
                client_secret=auth.client_secret,
                bearer_token=auth.bearer_token,
            )

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
                error_msg=error_msg,
                failed_reason=failed_reason,
                retain_pins_on_cancellation=True,
            )
        except (PyAirbyteInputError, requests.exceptions.RequestException) as e:
            result.errors.append(
                AutopilotAction(
                    rollout_id=rollout.rollout_id,
                    actor_definition_id=rollout.actor_definition_id,
                    connector_name=rollout.connector_name,
                    rc_version=rc_version,
                    action="close",
                    success=False,
                    message=f"Failed to close obsolete rollout: {e}",
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
                    action="close",
                    success=True,
                    message=f"Closed obsolete rollout (pins retained): {reason_msg}",
                    tier=rollout.tier,
                )
            )

    logger.info("auto-close: %s", result.summary)
    return result
