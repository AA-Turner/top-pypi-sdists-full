"""Tests for resolve_staleness_threshold_days in speckit/phase0/freshness.py (FR-007)."""

from __future__ import annotations

from agentic_devtools.cli.speckit.phase0.freshness import resolve_staleness_threshold_days


class TestResolveStalenessThresholdDays:
    """Tests for the resolve_staleness_threshold_days function."""

    def test_defaults_when_config_absent(self) -> None:
        assert resolve_staleness_threshold_days(None) == 30

    def test_defaults_when_key_absent(self) -> None:
        assert resolve_staleness_threshold_days({}) == 30

    def test_returns_configured_positive_value(self) -> None:
        assert resolve_staleness_threshold_days({"stalenessThresholdDays": 7}) == 7

    def test_non_positive_value_is_preserved_not_defaulted(self) -> None:
        assert resolve_staleness_threshold_days({"stalenessThresholdDays": 0}) == 0
        assert resolve_staleness_threshold_days({"stalenessThresholdDays": -1}) == -1

    def test_integer_valued_float_is_coerced(self) -> None:
        assert resolve_staleness_threshold_days({"stalenessThresholdDays": 14.0}) == 14

    def test_invalid_value_falls_back_to_default(self) -> None:
        assert resolve_staleness_threshold_days({"stalenessThresholdDays": "thirty"}) == 30
        assert resolve_staleness_threshold_days({"stalenessThresholdDays": 14.5}) == 30
        assert resolve_staleness_threshold_days({"stalenessThresholdDays": True}) == 30
