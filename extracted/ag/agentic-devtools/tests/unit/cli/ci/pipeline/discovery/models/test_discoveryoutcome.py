"""Tests for DiscoveryOutcome enum."""

from __future__ import annotations

from agentic_devtools.cli.ci.pipeline.discovery.models import DiscoveryOutcome


class TestDiscoveryOutcome:
    """Tests for DiscoveryOutcome enum values."""

    def test_success_value(self) -> None:
        assert DiscoveryOutcome.SUCCESS.value == "success"

    def test_empty_value(self) -> None:
        assert DiscoveryOutcome.EMPTY.value == "empty"

    def test_error_value(self) -> None:
        assert DiscoveryOutcome.ERROR.value == "error"

    def test_anchored_no_replacement_value(self) -> None:
        assert DiscoveryOutcome.ANCHORED_NO_REPLACEMENT.value == "anchored_no_replacement"
