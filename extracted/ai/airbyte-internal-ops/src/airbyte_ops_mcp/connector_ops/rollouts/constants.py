# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Constants for autopilot rollout orchestration."""

from __future__ import annotations

# Strategy step sizes (percentage increment per advancement cycle)
# Values must match the `AutopilotConfigStrategy` enum in airbyte-connector-models.
_FAST_SPEED = 100
_SLOW_SPEED = 5

STRATEGY_STEP_MAP: dict[str, int] = {
    "fast": _FAST_SPEED,
    "default": _FAST_SPEED,
    "slow": _SLOW_SPEED,
}

# Tier promotion sequence
TIER_ORDER: list[str] = ["TIER_2", "TIER_1", "ALL"]
