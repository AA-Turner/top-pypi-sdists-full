"""Freshness evaluation for Phase 0 configuration-discovery metadata (spec #1812).

Implements FR-007, FR-007a, and FR-007b: Phase 0 configuration metadata (the
project-level ``issue_types_metadata`` entry produced by property discovery)
carries a ``lastRefreshed`` timestamp. When that timestamp is older than a
configurable threshold, Phase 0 emits an informational staleness warning
without blocking the run or affecting its outcome (FR-008).
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import Literal

__all__ = [
    "DEFAULT_STALENESS_THRESHOLD_DAYS",
    "FreshnessStatus",
    "resolve_staleness_threshold_days",
    "parse_last_refreshed",
    "evaluate_freshness",
    "render_freshness_for_humans",
]

DEFAULT_STALENESS_THRESHOLD_DAYS = 30

FreshnessStatus = Literal["fresh", "stale", "unknown-freshness", "not-evaluated"]

_SECONDS_PER_DAY = 86_400
_DATE_ONLY_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}")


def resolve_staleness_threshold_days(issue_management_config: dict | None) -> int:
    """Resolve ``issueManagement.stalenessThresholdDays`` with defaulting (FR-007).

    Args:
        issue_management_config: The ``issueManagement`` configuration mapping
            (or ``None``/empty when absent).

    Returns:
        The configured threshold in days, defaulting to
        :data:`DEFAULT_STALENESS_THRESHOLD_DAYS` (30) when the setting is
        absent or is not an ``int``/``float`` value convertible to an integer
        number of days. Non-positive values are returned as-is (they disable
        the threshold comparison per FR-007) rather than being replaced by the
        default, since ``<= 0`` is itself meaningful configuration.
    """
    if not isinstance(issue_management_config, dict) or not issue_management_config:
        return DEFAULT_STALENESS_THRESHOLD_DAYS

    raw = issue_management_config.get("stalenessThresholdDays", DEFAULT_STALENESS_THRESHOLD_DAYS)
    if isinstance(raw, bool):
        return DEFAULT_STALENESS_THRESHOLD_DAYS
    if isinstance(raw, int):
        return raw
    if isinstance(raw, float) and raw.is_integer():
        return int(raw)
    return DEFAULT_STALENESS_THRESHOLD_DAYS


def parse_last_refreshed(value: object, *, now: datetime) -> datetime | None:
    """Parse a ``lastRefreshed`` value into a UTC datetime, or ``None`` if invalid.

    A value is considered invalid (returns ``None``) when it is absent, is not
    a string, is not a valid ISO 8601 timestamp, or represents an instant in
    the future relative to *now* (FR-007b).

    Args:
        value: The raw ``lastRefreshed`` value from project metadata.
        now: The current UTC run-start instant to compare against for
            future-dated detection.

    Returns:
        A timezone-aware UTC :class:`datetime`, or ``None`` when the value is
        missing, malformed, or future-dated.
    """
    if not isinstance(value, str) or not value:
        return None

    if _DATE_ONLY_PATTERN.fullmatch(value) is not None:
        return None

    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=UTC)
        else:
            parsed = parsed.astimezone(UTC)
    except (ValueError, OverflowError):
        return None

    now_utc = now if now.tzinfo is not None else now.replace(tzinfo=UTC)
    if parsed > now_utc:
        return None

    return parsed


def evaluate_freshness(
    *,
    project_metadata_exists: bool,
    last_refreshed: object,
    threshold_days: int,
    run_started_at: datetime,
) -> FreshnessStatus:
    """Evaluate the FR-007/FR-007a/FR-007b freshness status for a Phase 0 run.

    Args:
        project_metadata_exists: Whether a project-level ``issue_types_metadata``
            entry exists for the relevant project identifier. When ``False``,
            this is treated as the FR-007a first-run case.
        last_refreshed: The raw ``lastRefreshed`` value from that metadata entry
            (ignored when *project_metadata_exists* is ``False``).
        threshold_days: The resolved ``issueManagement.stalenessThresholdDays``
            value (see :func:`resolve_staleness_threshold_days`).
        run_started_at: The UTC run-start instant used to compute age and
            detect future-dated timestamps.

    Returns:
        One of ``"fresh"``, ``"stale"``, ``"unknown-freshness"``, or
        ``"not-evaluated"``.
    """
    if not project_metadata_exists:
        # FR-007a: no prior discovery record for the project — always suppressed.
        return "not-evaluated"

    parsed = parse_last_refreshed(last_refreshed, now=run_started_at)
    if parsed is None:
        # FR-007b: absent, malformed, or future-dated timestamp.
        return "unknown-freshness"

    if threshold_days <= 0:
        # FR-007: non-positive threshold disables the comparison entirely,
        # but only once FR-007a/FR-007b have been ruled out above.
        return "not-evaluated"

    run_started_at_utc = run_started_at if run_started_at.tzinfo is not None else run_started_at.replace(tzinfo=UTC)
    age_seconds = (run_started_at_utc - parsed).total_seconds()
    threshold_seconds = threshold_days * _SECONDS_PER_DAY
    return "stale" if age_seconds > threshold_seconds else "fresh"


def render_freshness_for_humans(status: FreshnessStatus) -> str:
    """Render a :data:`FreshnessStatus` value for human-facing surfaces (FR-003/FR-004).

    The only difference from the JSON enum is that ``"not-evaluated"`` renders
    as the two-word ``"not evaluated"``.
    """
    return "not evaluated" if status == "not-evaluated" else status
