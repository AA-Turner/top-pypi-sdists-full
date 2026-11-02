"""Configuration constants for the reconciliation engine.

All values are overridable via environment variables.
"""

from __future__ import annotations

import os


def _safe_csv(env_var: str, default: tuple[str, ...]) -> tuple[str, ...]:
    """Return comma-delimited values from *env_var* or *default*.

    Empty items are removed and surrounding whitespace is stripped.
    """
    raw = os.environ.get(env_var)
    if raw is None:
        return default
    values = tuple(item.strip() for item in raw.split(",") if item.strip())
    return values or default


def _safe_int(env_var: str, default: int, min_value: int = 1) -> int:
    """Return the integer value of *env_var*, falling back to *default*."""
    raw = os.environ.get(env_var)
    if raw is None:
        return default
    try:
        value = int(raw)
    except ValueError:
        return default
    return value if value >= min_value else default


def _safe_bool(env_var: str, default: bool) -> bool:
    """Return the boolean value of *env_var*, falling back to *default*."""
    raw = os.environ.get(env_var)
    if raw is None:
        return default
    lower = raw.lower()
    if lower in {"1", "true", "yes"}:
        return True
    if lower in {"0", "false", "no"}:
        return False
    return default


MAX_RUN_ATTEMPTS: int = _safe_int("AGDT_MAX_RUN_ATTEMPTS", 3)
RECONCILIATION_WINDOW_HOURS: int = _safe_int(
    "AGDT_RECONCILIATION_WINDOW_HOURS",
    24,
)
RETRIABLE_CONCLUSIONS: frozenset[str] = frozenset({"cancelled", "failure", "timed_out", "startup_failure"})

# Finite limits (FR-013)
MAX_RETRY_ATTEMPTS: int = _safe_int("AGDT_MAX_RETRY_ATTEMPTS", 3)
MAX_RECOVERY_ATTEMPTS: int = _safe_int("AGDT_MAX_RECOVERY_ATTEMPTS", 5)
MAX_PAGINATION_PAGES_PER_RUN: int = _safe_int(
    "AGDT_MAX_PAGINATION_PAGES_PER_RUN",
    20,
)
MAX_LEASE_RECLAIMS_PER_CYCLE: int = _safe_int(
    "AGDT_MAX_LEASE_RECLAIMS_PER_CYCLE",
    10,
)
MAX_LEASE_RECLAIM_CYCLES: int = _safe_int("AGDT_MAX_LEASE_RECLAIM_CYCLES", 3)
MAX_PROVIDER_FAILURE_DURATION: int = _safe_int(
    "AGDT_MAX_PROVIDER_FAILURE_DURATION",
    3600,
)
MAX_STATE_SIZE_BYTES: int = _safe_int("AGDT_MAX_STATE_SIZE_BYTES", 1_048_576)
MAX_STATE_AGE_SECONDS: int = _safe_int("AGDT_MAX_STATE_AGE_SECONDS", 86_400)

# Schedule intervals
RECONCILIATION_SCHEDULE_INTERVAL_MINUTES: int = _safe_int(
    "AGDT_RECONCILIATION_SCHEDULE_INTERVAL_MINUTES",
    5,
)
DUE_PROBE_WAKEUP_INTERVAL_MINUTES: int = _safe_int(
    "AGDT_DUE_PROBE_WAKEUP_INTERVAL_MINUTES",
    2,
)

# Feature flags
ENABLE_RECONCILIATION: bool = _safe_bool("AGDT_ENABLE_RECONCILIATION", True)
ENABLE_DUE_PROBE_WAKEUP: bool = _safe_bool("AGDT_ENABLE_DUE_PROBE_WAKEUP", True)

# Trusted observation and durable work-state configuration
TRUSTED_OBSERVATION_FRESHNESS_MINUTES: int = _safe_int(
    "AGDT_TRUSTED_OBSERVATION_FRESHNESS_MINUTES",
    30,
)
TRUSTED_OBSERVATION_TARGET_MINUTES: int = _safe_int(
    "AGDT_TRUSTED_OBSERVATION_TARGET_MINUTES",
    25,
)
TRUSTED_RECONCILIATION_INTERVAL_MINUTES: int = _safe_int(
    "AGDT_TRUSTED_RECONCILIATION_INTERVAL_MINUTES",
    20,
)
TRUSTED_RECONCILIATION_SCOPE: tuple[str, ...] = _safe_csv(
    "AGDT_TRUSTED_RECONCILIATION_SCOPE",
    (),
)
TRUSTED_RECONCILIATION_TARGET_BRANCHES: tuple[str, ...] = _safe_csv(
    "AGDT_TRUSTED_RECONCILIATION_TARGET_BRANCHES",
    ("main",),
)
TRUSTED_RECONCILIATION_CANDIDATE_FILTER: str = (
    os.environ.get(
        "AGDT_TRUSTED_RECONCILIATION_CANDIDATE_FILTER",
        "target_branch_match",
    ).strip()
    or "target_branch_match"
)
TRUSTED_RECONCILIATION_ROLLOUT_ENABLED: bool = _safe_bool(
    "AGDT_TRUSTED_RECONCILIATION_ROLLOUT_ENABLED",
    False,
)
