"""Tests for validate_run_id()."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.execution.run_id import validate_run_id


class TestValidateRunId:
    """Tests for validate_run_id()."""

    def test_strips_and_returns_valid_run_id(self) -> None:
        """Whitespace is stripped from a valid run identifier."""
        assert validate_run_id("  run-123  ") == "run-123"

    @pytest.mark.parametrize("run_id", ["", "   "])
    def test_rejects_empty_run_id(self, run_id: str) -> None:
        """Empty or whitespace-only run IDs are rejected."""
        with pytest.raises(ValueError, match="non-empty run identifier"):
            validate_run_id(run_id)

    @pytest.mark.parametrize("run_id", ["../escape", r"..\\escape", "/tmp/escape", "C:\\temp\\escape", ".."])
    def test_rejects_path_like_run_id(self, run_id: str) -> None:
        """Path-like run IDs are rejected."""
        with pytest.raises(ValueError, match="not a file path"):
            validate_run_id(run_id)
