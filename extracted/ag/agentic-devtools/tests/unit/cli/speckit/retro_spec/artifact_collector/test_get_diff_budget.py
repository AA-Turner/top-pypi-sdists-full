"""Tests for get_diff_budget in retro_spec/artifact_collector.py."""

from __future__ import annotations

from unittest.mock import patch

from agentic_devtools.cli.speckit.retro_spec.artifact_collector import get_diff_budget


class TestGetDiffBudget:
    """Tests for the public get_diff_budget wrapper."""

    def test_returns_default_when_env_not_set(self) -> None:
        """Returns the default budget when the env var is absent."""
        with patch.dict("os.environ", {}, clear=True):
            assert get_diff_budget() == 80_000

    def test_delegates_to_private_budget_resolution(self) -> None:
        """Public helper delegates to the same budget parsing logic as the private function."""
        with patch.dict("os.environ", {"AGDT_RETRO_SPEC_DIFF_BUDGET": "1234"}):
            assert get_diff_budget() == 1234
