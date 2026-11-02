"""Default policy constants.

These constants define the sensible defaults for all policy fields when no
configuration file is present or when a field is not explicitly overridden.
"""

from __future__ import annotations

DEFAULT_MAX_HIGH_SEVERITY: int = 0
"""Any high-severity finding blocks approval."""

DEFAULT_MAX_MEDIUM_SEVERITY: int = 3
"""More than 3 medium-severity findings block approval."""

DEFAULT_CONFIDENCE_MINIMUM: float = 0.7
"""Minimum confidence score for autonomous decision-making."""

DEFAULT_ESCALATION_TRIGGERS: tuple[str, ...] = ()
"""Escalation trigger patterns (empty by default)."""

DEFAULT_RETRY_BUDGET: int = 3
"""Maximum retry attempts before stopping."""

DEFAULT_MAX_TOKENS: int = 500000
"""Maximum token consumption before halting."""

DEFAULT_MAX_WALL_CLOCK_MINUTES: int = 60
"""Maximum wall-clock minutes before halting."""

DEFAULT_BLOCKED_AFTER_MINUTES: int = 30
"""Minutes without progress before declaring blocked."""

DEFAULT_COVERAGE_THRESHOLD: int = 100
"""Minimum test coverage percentage required."""
