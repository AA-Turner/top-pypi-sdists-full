"""Tests for env var validation in artifact_collector.py."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.retro_spec.artifact_collector import (
    _get_diff_budget,
    _get_file_diff_max,
)


class TestGetDiffBudget:
    """Tests for _get_diff_budget."""

    def test_returns_default_when_env_not_set(self) -> None:
        """Test default value is returned when env var is absent."""
        with patch.dict("os.environ", {}, clear=True):
            assert _get_diff_budget() == 80_000

    def test_returns_value_from_env(self) -> None:
        """Test that valid positive integer from env is used."""
        with patch.dict("os.environ", {"AGDT_RETRO_SPEC_DIFF_BUDGET": "50000"}):
            assert _get_diff_budget() == 50000

    def test_warns_and_defaults_on_invalid_value(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test warning on non-integer env value."""
        with patch.dict("os.environ", {"AGDT_RETRO_SPEC_DIFF_BUDGET": "abc"}):
            assert _get_diff_budget() == 80_000
        assert "Invalid AGDT_RETRO_SPEC_DIFF_BUDGET" in capsys.readouterr().err

    def test_warns_and_defaults_on_zero(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that zero is treated as invalid."""
        with patch.dict("os.environ", {"AGDT_RETRO_SPEC_DIFF_BUDGET": "0"}):
            assert _get_diff_budget() == 80_000
        assert "Invalid" in capsys.readouterr().err

    def test_warns_and_defaults_on_negative(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that negative is treated as invalid."""
        with patch.dict("os.environ", {"AGDT_RETRO_SPEC_DIFF_BUDGET": "-5"}):
            assert _get_diff_budget() == 80_000


class TestGetFileDiffMax:
    """Tests for _get_file_diff_max."""

    def test_returns_default_when_env_not_set(self) -> None:
        """Test default value is returned when env var is absent."""
        with patch.dict("os.environ", {}, clear=True):
            assert _get_file_diff_max() == 4000

    def test_returns_value_from_env(self) -> None:
        """Test that valid positive integer from env is used."""
        with patch.dict("os.environ", {"AGDT_RETRO_SPEC_FILE_DIFF_MAX": "2000"}):
            assert _get_file_diff_max() == 2000

    def test_warns_and_defaults_on_invalid_value(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test warning on non-integer env value."""
        with patch.dict("os.environ", {"AGDT_RETRO_SPEC_FILE_DIFF_MAX": "xyz"}):
            assert _get_file_diff_max() == 4000
        assert "Invalid AGDT_RETRO_SPEC_FILE_DIFF_MAX" in capsys.readouterr().err

    def test_warns_and_defaults_on_zero(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that zero is treated as invalid."""
        with patch.dict("os.environ", {"AGDT_RETRO_SPEC_FILE_DIFF_MAX": "0"}):
            assert _get_file_diff_max() == 4000
