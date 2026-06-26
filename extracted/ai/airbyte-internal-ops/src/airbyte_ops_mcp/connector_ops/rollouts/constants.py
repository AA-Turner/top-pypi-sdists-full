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


# Tier promotion sequence
TIER_ORDER: list[CustomerTier] = [
    CustomerTier.TIER_2,
    CustomerTier.TIER_1,
    CustomerTier.ALL,
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
