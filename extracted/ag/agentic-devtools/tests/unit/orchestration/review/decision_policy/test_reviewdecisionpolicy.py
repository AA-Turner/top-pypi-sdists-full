"""Tests for ReviewDecisionPolicy dataclass."""

from __future__ import annotations

from agentic_devtools.orchestration.review.decision_policy import ReviewDecisionPolicy


class TestReviewDecisionPolicy:
    """Tests for ReviewDecisionPolicy construction."""

    def test_default_values(self) -> None:
        """Default policy has max_high=0, unlimited medium/low."""
        policy = ReviewDecisionPolicy()
        assert policy.max_high_severity == 0
        assert policy.max_medium_severity is None
        assert policy.max_low_severity is None

    def test_from_config_empty_dict(self) -> None:
        """Empty config dict produces default policy."""
        policy = ReviewDecisionPolicy.from_config({})
        assert policy.max_high_severity == 0
        assert policy.max_medium_severity is None
        assert policy.max_low_severity is None

    def test_from_config_none(self) -> None:
        """None config produces default policy."""
        policy = ReviewDecisionPolicy.from_config(None)
        assert policy.max_high_severity == 0

    def test_from_config_explicit_values(self) -> None:
        """Explicit config values are used."""
        policy = ReviewDecisionPolicy.from_config(
            {
                "max-high-severity": 2,
                "max-medium-severity": 5,
                "max-low-severity": 10,
            }
        )
        assert policy.max_high_severity == 2
        assert policy.max_medium_severity == 5
        assert policy.max_low_severity == 10

    def test_from_config_null_means_unlimited(self) -> None:
        """Explicit null in config means unlimited (None)."""
        policy = ReviewDecisionPolicy.from_config(
            {
                "max-high-severity": None,
                "max-medium-severity": None,
                "max-low-severity": None,
            }
        )
        assert policy.max_high_severity is None
        assert policy.max_medium_severity is None
        assert policy.max_low_severity is None

    def test_from_config_missing_keys_use_defaults(self) -> None:
        """Missing keys use defaults, not 0."""
        policy = ReviewDecisionPolicy.from_config(
            {
                "max-high-severity": 1,
            }
        )
        assert policy.max_high_severity == 1
        assert policy.max_medium_severity is None
        assert policy.max_low_severity is None

    def test_from_config_non_dict(self) -> None:
        """Non-dict config produces default policy."""
        policy = ReviewDecisionPolicy.from_config("invalid")  # type: ignore[arg-type]
        assert policy.max_high_severity == 0

    def test_from_config_parses_numeric_strings(self) -> None:
        """Digit-only string thresholds are coerced to integers."""
        policy = ReviewDecisionPolicy.from_config(
            {
                "max-high-severity": " 3 ",
                "max-medium-severity": "4",
                "max-low-severity": "0",
            }
        )

        assert policy.max_high_severity == 3
        assert policy.max_medium_severity == 4
        assert policy.max_low_severity == 0

    def test_from_config_invalid_thresholds_fall_back_to_defaults(self) -> None:
        """Invalid threshold values keep their documented defaults."""
        policy = ReviewDecisionPolicy.from_config(
            {
                "max-high-severity": "three",
                "max-medium-severity": "",
                "max-low-severity": object(),
            }
        )

        assert policy.max_high_severity == 0
        assert policy.max_medium_severity is None
        assert policy.max_low_severity is None

    def test_from_config_negative_thresholds_fall_back_to_defaults(self) -> None:
        """Negative thresholds are rejected in favor of documented defaults."""
        policy = ReviewDecisionPolicy.from_config(
            {
                "max-high-severity": -1,
                "max-medium-severity": "-2",
                "max-low-severity": -3,
            }
        )

        assert policy.max_high_severity == 0
        assert policy.max_medium_severity is None
        assert policy.max_low_severity is None
