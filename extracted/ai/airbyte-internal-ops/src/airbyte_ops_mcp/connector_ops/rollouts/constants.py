# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Constants for autopilot rollout orchestration."""

from __future__ import annotations

from enum import StrEnum


class RolloutStrategy(StrEnum):
    """Canonical autopilot rollout strategies."""

    FAST = "fast"
    SLOW = "slow"


# Alias input value — resolves to FAST at decision points.
STRATEGY_DEFAULT = "default"


def resolve_strategy(raw: str) -> RolloutStrategy:
    """Resolve a raw strategy value to one of the two canonical strategies.

    `"default"` is an alias for `RolloutStrategy.FAST`. Any other unknown
    value raises `ValueError` rather than falling back silently.
    """
    if raw == STRATEGY_DEFAULT:
        return RolloutStrategy.FAST
    try:
        return RolloutStrategy(raw)
    except ValueError:
        msg = f"Unknown autopilot strategy: {raw!r}. Must be 'fast', 'slow', or 'default'."
        raise ValueError(msg) from None


# Strategy step sizes (percentage increment per advancement cycle)
# Values must match the `AutopilotConfigStrategy` enum in airbyte-connector-models.
_FAST_SPEED = 100
_SLOW_SPEED = 5

STRATEGY_STEP_MAP: dict[RolloutStrategy, int] = {
    RolloutStrategy.FAST: _FAST_SPEED,
    RolloutStrategy.SLOW: _SLOW_SPEED,
}


class CustomerTier(StrEnum):
    """Customer tier levels for progressive rollout targeting."""

    TIER_0 = "TIER_0"
    TIER_1 = "TIER_1"
    TIER_2 = "TIER_2"
    ALL = "ALL"

    @property
    def label(self) -> str:
        """Human-readable display label (e.g. `"Tier 2"`, `"All"`)."""
        if self == CustomerTier.ALL:
            return "All"
        return self.value.replace("_", " ").title()


# Tier promotion sequence. Each stage is an explicit customer cohort, ending at
# `TIER_0` (the highest-priority customers). "Everyone by default" is not a
# rollout stage — it is the GA promotion that follows the final tier.
TIER_ORDER: list[CustomerTier] = [
    CustomerTier.TIER_2,
    CustomerTier.TIER_1,
    CustomerTier.TIER_0,
]

# ---------------------------------------------------------------------------
# Health gate thresholds
# ---------------------------------------------------------------------------

# Minimum elapsed seconds before promotion is ever considered.
MIN_SOAK_TIME: dict[RolloutStrategy, int] = {
    RolloutStrategy.FAST: 4 * 3600,  # 4 hours
    RolloutStrategy.SLOW: 28 * 3600,  # 28 hours
}

# Maximum elapsed seconds; if data is not collected by this time, progress anyway.
MAX_SOAK_TIME: dict[RolloutStrategy, int] = {
    RolloutStrategy.FAST: 24 * 3600,  # 24 hours
    RolloutStrategy.SLOW: 28 * 3600,  # 28 hours
}

# Minimum number of actors with successful syncs required to consider the
# rollout "soaked" (sufficient signal collected).
SOAKED_SIGNAL_COUNT_THRESHOLD: dict[RolloutStrategy, int] = {
    RolloutStrategy.FAST: 5,
    RolloutStrategy.SLOW: 100,
}

# Minimum fraction of pinned actors with successful syncs required to
# consider the rollout "soaked".
SOAKED_SIGNAL_PERCENT_THRESHOLD: dict[RolloutStrategy, float] = {
    RolloutStrategy.FAST: 0.10,  # 10%
    RolloutStrategy.SLOW: 0.50,  # 50%
}

# Number of failures that triggers a pause/rollback decision.
ROLLOUT_FAILURE_COUNT_THRESHOLD: dict[RolloutStrategy, int] = {
    RolloutStrategy.FAST: 1,
    RolloutStrategy.SLOW: 1,
}

# ---------------------------------------------------------------------------
# Finalize reconciliation
# ---------------------------------------------------------------------------

# Minutes a rollout may sit in `finalizing` before auto-promote treats it as
# stuck and reconciles it. A healthy finalize (fresh Temporal run confirming
# the GA default) closes well within this window; anything longer indicates the
# finalize Temporal run died before recording the terminal transition.
FINALIZING_GRACE_MINUTES = 20

# A workflow-started rollout that has not changed for this long requires
# operator review instead of another automatic recovery attempt.
WORKFLOW_STARTED_STALE_MINUTES = 60

# Recorded by `auto-triage-failed` when it pauses a rollout after the health
# gate recommends rollback. This is intentionally an outcome marker, not a
# health re-check performed while evaluating sibling rollouts.
FAILURE_THRESHOLD_EXCEEDED_MARKER = "Failure threshold exceeded:"

# Recorded when AutoPilot creates and immediately cancels an empty next-tier
# rollout while promoting the current tier.
NO_OP_EMPTY_TIER_MARKER = "[No-op.] Nothing to do"
