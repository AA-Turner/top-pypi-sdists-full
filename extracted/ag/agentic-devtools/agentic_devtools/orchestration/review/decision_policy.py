"""Review decision policy — threshold-based approve/request-changes logic.

Satisfies FR-006: evaluates aggregated review findings against configurable
severity thresholds to produce an autonomous approve or request-changes
decision.

Configuration is loaded from ``.github/agdt-config.json`` under
``review.decision-policy``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal


@dataclass
class ReviewDecisionPolicy:
    """Configurable threshold policy for autonomous review decisions.

    Attributes:
        max_high_severity: Maximum number of high-severity findings before
            requesting changes.  Default ``0`` means any high-severity
            finding triggers request-changes.
        max_medium_severity: Maximum medium-severity findings.  ``None``
            means unlimited (no threshold).
        max_low_severity: Maximum low-severity findings.  ``None`` means
            unlimited.
    """

    max_high_severity: int | None = 0
    max_medium_severity: int | None = None
    max_low_severity: int | None = None

    @classmethod
    def from_config(cls, config: dict[str, Any] | None) -> ReviewDecisionPolicy:
        """Construct a policy from a config dict.

        Missing keys are treated as defaults (not as ``0``).  An absent
        or ``None``-valued ``config`` produces the default policy.

        Args:
            config: Parsed ``review.decision-policy`` section from
                ``.github/agdt-config.json``.

        Returns:
            A ``ReviewDecisionPolicy`` with the specified or default values.
        """
        if not config or not isinstance(config, dict):
            return cls()

        def _get_threshold(key: str, default: int | None) -> int | None:
            if key not in config:
                return default
            val = config[key]
            if val is None:
                return None
            # bool is a subclass of int, so reject it explicitly and fall back
            # to the documented default/unlimited behavior instead.
            if isinstance(val, int) and not isinstance(val, bool):
                return val if val >= 0 else default
            if isinstance(val, str):
                try:
                    parsed = int(val.strip())
                except ValueError:
                    return default
                return parsed if parsed >= 0 else default
            return default

        return cls(
            max_high_severity=_get_threshold("max-high-severity", 0),
            max_medium_severity=_get_threshold("max-medium-severity", None),
            max_low_severity=_get_threshold("max-low-severity", None),
        )


def evaluate_decision(
    policy: ReviewDecisionPolicy,
    high_count: int,
    medium_count: int,
    low_count: int,
) -> Literal["approve", "request-changes"]:
    """Evaluate findings against the decision policy.

    Args:
        policy: The threshold policy to apply.
        high_count: Number of high-severity findings.
        medium_count: Number of medium-severity findings.
        low_count: Number of low-severity findings.

    Returns:
        ``"approve"`` if all thresholds are met, ``"request-changes"``
        if any threshold is exceeded.
    """
    if policy.max_high_severity is not None and high_count > policy.max_high_severity:
        return "request-changes"

    if policy.max_medium_severity is not None and medium_count > policy.max_medium_severity:
        return "request-changes"

    if policy.max_low_severity is not None and low_count > policy.max_low_severity:
        return "request-changes"

    return "approve"
