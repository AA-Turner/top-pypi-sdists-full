# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Internal helpers for autopilot rollout operations.

Includes registry lookups, rollout filtering, tier logic, and health gates.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timezone

from airbyte_connector_models.metadata.v0.connector_registry_v0 import (
    ConnectorRegistryV0ConnectorRegistryReleasesRolloutConfiguration as RolloutConfiguration,
)

from airbyte_ops_mcp.cloud_admin.registry_lookup import (
    _fetch_cloud_registry,
    resolve_canonical_name_to_definition_id,
)
from airbyte_ops_mcp.connector_ops.rollouts.constants import (
    MAX_SOAK_TIME,
    MIN_SOAK_TIME,
    ROLLOUT_FAILURE_COUNT_THRESHOLD,
    SOAKED_SIGNAL_COUNT_THRESHOLD,
    SOAKED_SIGNAL_PERCENT_THRESHOLD,
    RolloutStrategy,
    resolve_strategy,
)
from airbyte_ops_mcp.connector_ops.rollouts.models import ConnectorRolloutRecord
from airbyte_ops_mcp.prod_db_access.queries import (
    query_connections_by_connector,
    query_connections_by_destination_connector,
)
from airbyte_ops_mcp.tier_cache import enrich_rows_by_org, filter_rows_by_tier

logger = logging.getLogger(__name__)


def parse_db_timestamp(value: object) -> datetime | None:
    """Coerce a DB timestamp (str or `datetime`) into a timezone-aware `datetime`.

    Returns `None` when `value` is missing or cannot be parsed. Naive datetimes
    are assumed UTC and a trailing `Z` on ISO strings is normalized to
    `+00:00`. Fails closed (returns `None`) on an unparseable string rather than
    raising, so a malformed DB row can't crash reconciliation.
    """
    if value is None:
        return None
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            logger.warning("Could not parse DB timestamp: %r", value)
            return None
    if not isinstance(value, datetime):
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value


# ---------------------------------------------------------------------------
# Metadata / gate helpers
# ---------------------------------------------------------------------------


_ROLLOUT_CONFIG_KNOWN_FIELDS: set[str] = set(
    RolloutConfiguration.model_json_schema().get("properties", {}).keys()
) | set(RolloutConfiguration.model_fields.keys())


def _parse_rollout_config(raw: dict) -> RolloutConfiguration:
    """Parse a registry `rolloutConfiguration` dict, ignoring legacy fields.

    The compiled registry may contain fields (e.g. `advanceDelayMinutes`,
    `initialPercentage`, `maxPercentage`) that predate the current schema.
    We strip them rather than relaxing the model's `extra='forbid'`.
    """
    filtered = {k: v for k, v in raw.items() if k in _ROLLOUT_CONFIG_KNOWN_FIELDS}
    return RolloutConfiguration.model_validate(filtered)


def _extract_rollout_config(
    entry: dict,
    rc_version: str | None,
) -> dict:
    """Extract `rolloutConfiguration` from a registry entry.

    When `rc_version` is provided, looks in the RC-specific metadata first
    (at `releases.releaseCandidates[rc_version].releases.rolloutConfiguration`).
    Falls back to the top-level `releases.rolloutConfiguration`.
    """
    releases = entry.get("releases", {})
    if rc_version:
        rc_entry = releases.get("releaseCandidates", {}).get(rc_version, {})
        rc_raw = rc_entry.get("releases", {}).get("rolloutConfiguration")
        if rc_raw:
            return rc_raw
    return releases.get("rolloutConfiguration") or {}


def get_connector_rollout_config(
    actor_definition_id: str,
    rc_version: str | None = None,
) -> RolloutConfiguration:
    """Fetch the `rolloutConfiguration` from the compiled registry.

    When `rc_version` is provided, prefers the RC-specific rollout config
    from `releases.releaseCandidates[rc_version]` over the top-level config.
    Returns the parsed `RolloutConfiguration` model with defaults applied if
    the connector does not have explicit rollout configuration.
    """
    registry = _fetch_cloud_registry()
    normalized_id = actor_definition_id.strip().lower()

    for source in registry.get("sources", []):
        if source.get("sourceDefinitionId", "").lower() == normalized_id:
            raw = _extract_rollout_config(source, rc_version)
            return _parse_rollout_config(raw)

    for destination in registry.get("destinations", []):
        if destination.get("destinationDefinitionId", "").lower() == normalized_id:
            raw = _extract_rollout_config(destination, rc_version)
            return _parse_rollout_config(raw)

    return RolloutConfiguration()


def get_registry_default_version(actor_definition_id: str) -> str | None:
    """Return the connector's current default `dockerImageTag` from the registry.

    This is the GA version that a finalized rollout must have flipped the
    default to. Returns `None` if the connector is not found in the compiled
    registry. Used by auto-promote to confirm that a `finalizing` rollout's GA
    version is actually live before closing the row.
    """
    registry = _fetch_cloud_registry()
    normalized_id = actor_definition_id.strip().lower()

    for source in registry.get("sources", []):
        if source.get("sourceDefinitionId", "").lower() == normalized_id:
            return source.get("dockerImageTag")

    for destination in registry.get("destinations", []):
        if destination.get("destinationDefinitionId", "").lower() == normalized_id:
            return destination.get("dockerImageTag")

    return None


def get_registry_release_candidates(actor_definition_id: str) -> list[str] | None:
    """Return the connector's advertised release-candidate versions from the registry.

    Reads `releases.releaseCandidates` (a version-keyed map) from the compiled
    Cloud registry and returns its keys — the versions the platform is allowed to
    progressively roll out. An empty list means the connector was found but
    currently advertises no release candidate, so any active rollout is obsolete.
    Returns `None` when the connector is not found in the registry (unknown), so
    callers can fail closed rather than treating it as "no candidate".
    """
    registry = _fetch_cloud_registry()
    normalized_id = actor_definition_id.strip().lower()

    for source in registry.get("sources", []):
        if source.get("sourceDefinitionId", "").lower() == normalized_id:
            raw = source.get("releases", {}).get("releaseCandidates") or {}
            return list(raw.keys())

    for destination in registry.get("destinations", []):
        if destination.get("destinationDefinitionId", "").lower() == normalized_id:
            raw = destination.get("releases", {}).get("releaseCandidates") or {}
            return list(raw.keys())

    return None


def get_unsafe_downgrades(actor_definition_id: str) -> list[str]:
    """Fetch the `unsafeDowngrades` map keys from the compiled registry.

    Returns a list of version strings that are unsafe to downgrade from.
    """
    registry = _fetch_cloud_registry()
    normalized_id = actor_definition_id.strip().lower()

    for source in registry.get("sources", []):
        if source.get("sourceDefinitionId", "").lower() == normalized_id:
            raw = source.get("releases", {}).get("unsafeDowngrades") or {}
            return list(raw.keys())

    for destination in registry.get("destinations", []):
        if destination.get("destinationDefinitionId", "").lower() == normalized_id:
            raw = destination.get("releases", {}).get("unsafeDowngrades") or {}
            return list(raw.keys())

    return []


# ---------------------------------------------------------------------------
# Rollout filtering
# ---------------------------------------------------------------------------


def filter_rollouts_by_connector(
    rollouts: list[ConnectorRolloutRecord],
    connector: str | None,
) -> list[ConnectorRolloutRecord]:
    """Filter rollouts to a specific connector if `--connector` was provided."""
    if connector is None:
        return rollouts

    definition_id = resolve_canonical_name_to_definition_id(connector)
    return [
        r for r in rollouts if r.actor_definition_id.lower() == definition_id.lower()
    ]


# ---------------------------------------------------------------------------
# Health gate
# ---------------------------------------------------------------------------


@dataclass
class HealthGateResult:
    """Result of a health gate evaluation."""

    passed: bool
    reason: str
    soak_elapsed_seconds: float = 0.0
    actors_with_successful_syncs: int = 0
    signal_percent: float = 0.0
    failure_count: int = 0
    should_rollback: bool = False


def check_health_gate(
    rollout: ConnectorRolloutRecord,
    sync_info: dict,
    strategy: str | RolloutStrategy,
) -> HealthGateResult:
    """Evaluate health gate for a rollout at 100%.

    Uses a 5-threshold model:

    1. **MIN_SOAK_TIME** - Never promote before this elapsed time.
    2. **MAX_SOAK_TIME** - If signal data is not collected by this time,
       promote anyway (force progression).
    3. **ROLLOUT_FAILURE_COUNT_THRESHOLD** - If this many failures are
       observed, trigger pause/rollback.
    4. **SOAKED_SIGNAL_COUNT_THRESHOLD** - Minimum number of actors with
       successful syncs (success signal, unrelated to failures).
    5. **SOAKED_SIGNAL_PERCENT_THRESHOLD** - Minimum fraction of pinned
       actors with successful syncs.

    Gates 4 and 5 both must pass (AND) for the signal to be considered
    sufficient. If signal is insufficient but MAX_SOAK_TIME is exceeded,
    we promote regardless.

    Args:
        rollout: The rollout record (must be at 100%).
        sync_info: Response dict from `get_actor_sync_info`.
        strategy: Autopilot strategy key or `RolloutStrategy` enum value.

    Returns:
        `HealthGateResult` with `passed=True` if promotion is allowed,
        `passed=False` otherwise. `should_rollback=True` if the failure
        threshold was hit.
    """
    strategy_key = resolve_strategy(strategy)

    # --- Compute elapsed time ---
    updated_at = rollout.updated_at
    if updated_at is None:
        return HealthGateResult(
            passed=False,
            reason="Cannot evaluate soak time: rollout has no updated_at timestamp",
        )

    if isinstance(updated_at, str):
        # Handle trailing Z (ISO 8601 UTC marker) for broad compatibility.
        updated_at = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
    if updated_at.tzinfo is None:
        updated_at = updated_at.replace(tzinfo=timezone.utc)

    now = datetime.now(tz=timezone.utc)
    elapsed_seconds = (now - updated_at).total_seconds()

    # --- Extract sync data (tolerant of camelCase and snake_case keys) ---
    data = sync_info.get("data", sync_info)
    selection_info = (
        data.get("actorSelectionInfo") or data.get("actor_selection_info") or {}
    )
    num_pinned = (
        selection_info.get("numPinnedToConnectorRollout")
        or selection_info.get("num_pinned_to_connector_rollout")
        or 0
    )
    syncs_map = data.get("syncs", {})

    actors_with_successful_syncs = sum(
        1
        for actor_stats in syncs_map.values()
        if (actor_stats.get("numSucceeded") or actor_stats.get("num_succeeded") or 0)
        > 0
    )
    total_failed = sum(
        (actor_stats.get("numFailed") or actor_stats.get("num_failed") or 0)
        for actor_stats in syncs_map.values()
    )
    signal_percent = (
        actors_with_successful_syncs / num_pinned if num_pinned > 0 else 0.0
    )

    # --- Gate: failure threshold (checked first, independent of timing) ---
    failure_threshold = ROLLOUT_FAILURE_COUNT_THRESHOLD[strategy_key]
    if total_failed >= failure_threshold:
        return HealthGateResult(
            passed=False,
            should_rollback=True,
            reason=(
                f"Failure threshold hit: {total_failed} failures "
                f"(threshold={failure_threshold}). Pause/rollback recommended."
            ),
            soak_elapsed_seconds=elapsed_seconds,
            actors_with_successful_syncs=actors_with_successful_syncs,
            signal_percent=signal_percent,
            failure_count=total_failed,
        )

    # --- Gate: MIN_SOAK_TIME (never promote before this) ---
    min_soak = MIN_SOAK_TIME[strategy_key]
    if elapsed_seconds < min_soak:
        remaining = min_soak - elapsed_seconds
        return HealthGateResult(
            passed=False,
            reason=(
                f"Min soak time not met: {elapsed_seconds:.0f}s elapsed, "
                f"{min_soak}s required ({remaining:.0f}s remaining)"
            ),
            soak_elapsed_seconds=elapsed_seconds,
            actors_with_successful_syncs=actors_with_successful_syncs,
            signal_percent=signal_percent,
            failure_count=total_failed,
        )

    # --- Gate: MAX_SOAK_TIME (force progression if exceeded) ---
    max_soak = MAX_SOAK_TIME[strategy_key]
    if elapsed_seconds >= max_soak:
        return HealthGateResult(
            passed=True,
            reason=(
                f"Max soak time exceeded ({elapsed_seconds:.0f}s >= {max_soak}s): "
                f"progressing regardless of signal. "
                f"Signal: {actors_with_successful_syncs} actors, "
                f"{signal_percent:.1%} coverage"
            ),
            soak_elapsed_seconds=elapsed_seconds,
            actors_with_successful_syncs=actors_with_successful_syncs,
            signal_percent=signal_percent,
            failure_count=total_failed,
        )

    # --- Gates: signal count AND signal percent (both must pass) ---
    count_threshold = SOAKED_SIGNAL_COUNT_THRESHOLD[strategy_key]
    percent_threshold = SOAKED_SIGNAL_PERCENT_THRESHOLD[strategy_key]

    count_met = actors_with_successful_syncs >= count_threshold
    percent_met = signal_percent >= percent_threshold

    if count_met and percent_met:
        return HealthGateResult(
            passed=True,
            reason=(
                f"Signal thresholds met: "
                f"{actors_with_successful_syncs} actors (>= {count_threshold}), "
                f"{signal_percent:.1%} coverage (>= {percent_threshold:.0%}). "
                f"Soak: {elapsed_seconds:.0f}s, failures: {total_failed}"
            ),
            soak_elapsed_seconds=elapsed_seconds,
            actors_with_successful_syncs=actors_with_successful_syncs,
            signal_percent=signal_percent,
            failure_count=total_failed,
        )

    # Not enough signal yet, still within max soak window
    missing_parts = []
    if not count_met:
        missing_parts.append(f"count={actors_with_successful_syncs}/{count_threshold}")
    if not percent_met:
        missing_parts.append(f"percent={signal_percent:.1%}/{percent_threshold:.0%}")

    return HealthGateResult(
        passed=False,
        reason=(
            f"Insufficient signal: {', '.join(missing_parts)}. "
            f"Soak: {elapsed_seconds:.0f}s/{max_soak}s, failures: {total_failed}"
        ),
        soak_elapsed_seconds=elapsed_seconds,
        actors_with_successful_syncs=actors_with_successful_syncs,
        signal_percent=signal_percent,
        failure_count=total_failed,
    )


# ---------------------------------------------------------------------------
# Actor eligibility
# ---------------------------------------------------------------------------


def count_eligible_or_pinned_actors(sync_info: dict) -> int:
    """Return the number of actors eligible for pinning (or already pinned).

    Extracts `numActorsEligibleOrAlreadyPinned` from a `get_actor_sync_info`
    response, tolerant of both camelCase (raw platform response) and
    snake_case keys.

    A value of `0` means the rollout's tier has **no actors to pin**. This is
    the zero-eligible-actor condition: `TIER_1` / `TIER_0` are named strategic
    accounts, so a connector with no customers in that tier can never pin
    anyone there. Progressing such a rollout to a target percentage `> 0`
    makes the platform throw `ConnectorRolloutNotEnoughActorsProblem`
    server-side (before the `IN_PROGRESS` write), and the surrounding
    `@Transactional` rolls back, leaving the rollout silently frozen at
    `workflow_started` with no recorded error. Callers should check this
    before progressing and skip/handle the empty tier instead of wedging.
    """
    data = sync_info.get("data", sync_info)
    selection_info = (
        data.get("actorSelectionInfo") or data.get("actor_selection_info") or {}
    )
    return int(
        selection_info.get("numActorsEligibleOrAlreadyPinned")
        or selection_info.get("num_actors_eligible_or_already_pinned")
        or 0
    )


# ---------------------------------------------------------------------------
# Pre-flight eligibility estimate
# ---------------------------------------------------------------------------

# A tier with exactly this many predicted-eligible actors is treated as empty:
# there is nobody to pin, so a rollout to that tier is a no-op ("nothing to do")
# rather than something we should start or advance.
ELIGIBILITY_SKIP_AT_OR_BELOW = 0

# A tier with more than `ELIGIBILITY_SKIP_AT_OR_BELOW` but at most this many
# predicted-eligible actors is still rolled out, but the sample is too small to
# produce a statistically meaningful health signal, so autopilot warns.
ELIGIBILITY_WARN_AT_OR_BELOW = 3


@dataclass
class TierEligibilityEstimate:
    """A local, pre-flight prediction of how many actors a tier would pin.

    Derived from production connections plus the org tier cache, so it can be
    computed **before** a rollout is started or progressed — unlike the
    platform's `numActorsEligibleOrAlreadyPinned`, which only exists once a
    rollout record has been created.

    `disposition` is one of:

    - `skip`: exactly `0` eligible actors — the tier is empty, so starting or
      advancing a rollout there is a no-op. Callers should treat this as a valid
      "nothing to do" signal, not an error.
    - `warn`: `1..ELIGIBILITY_WARN_AT_OR_BELOW` eligible actors — proceed, but
      the sample is too small for a meaningful health gate, so surface a warning.
    - `normal`: more than `ELIGIBILITY_WARN_AT_OR_BELOW` — proceed normally.

    The ops tier lists can drift slightly from the platform's, so this estimate
    decides *intent*; callers still confirm against the platform's actual count
    before an irreversible step (see `count_eligible_or_pinned_actors`).
    """

    tier: str
    eligible_actor_count: int
    disposition: str
    reason: str


def _classify_eligibility(tier: str, count: int) -> TierEligibilityEstimate:
    """Map an eligible-actor `count` to a `TierEligibilityEstimate`."""
    if count <= ELIGIBILITY_SKIP_AT_OR_BELOW:
        disposition = "skip"
        reason = f"{tier} has 0 predicted-eligible actors (empty tier — nothing to do)"
    elif count <= ELIGIBILITY_WARN_AT_OR_BELOW:
        disposition = "warn"
        reason = (
            f"{tier} has only {count} predicted-eligible "
            f"actor{'s' if count != 1 else ''} "
            f"(<= {ELIGIBILITY_WARN_AT_OR_BELOW}); health signal will be weak"
        )
    else:
        disposition = "normal"
        reason = f"{tier} has {count} predicted-eligible actors"
    return TierEligibilityEstimate(
        tier=tier,
        eligible_actor_count=count,
        disposition=disposition,
        reason=reason,
    )


def estimate_tier_eligible_actors(
    actor_definition_id: str,
    docker_repository: str,
    tier: str,
) -> TierEligibilityEstimate:
    """Predict how many actors a rollout to `tier` would be eligible to pin.

    Counts distinct, unpinned actors with an active sync schedule for
    `actor_definition_id`, enriches them with the org tier cache, filters to
    `tier`, and classifies the result via `_classify_eligibility`.

    `docker_repository` (e.g. `airbyte/source-faker` or
    `airbyte/destination-bigquery`) selects the source vs destination query and
    the actor-id column used for the distinct count.
    """
    is_destination = "/destination-" in f"/{docker_repository.split('/')[-1]}"
    if is_destination:
        rows = query_connections_by_destination_connector(
            connector_definition_id=actor_definition_id,
            limit=None,
            exclude_pinned=True,
            enabled_schedules_only=True,
        )
        actor_id_key = "destination_id"
    else:
        rows = query_connections_by_connector(
            connector_definition_id=actor_definition_id,
            limit=None,
            exclude_pinned=True,
            enabled_schedules_only=True,
        )
        actor_id_key = "source_id"

    enrich_rows_by_org(rows)
    in_tier = filter_rows_by_tier(rows, tier)
    distinct_actors = {str(r.get(actor_id_key)) for r in in_tier if r.get(actor_id_key)}
    return _classify_eligibility(tier, len(distinct_actors))
