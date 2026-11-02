"""Tests for AttemptCoordinate in speckit/phase0/comments.py."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from agentic_devtools.cli.speckit.phase0.comments import AttemptCoordinate


class TestAttemptCoordinate:
    """Tests for the AttemptCoordinate dataclass."""

    def test_preserves_coordinate_fields(self) -> None:
        coordinate = AttemptCoordinate(
            attempt_started_at="2026-01-01T00:00:00Z",
            workflow_run_id=123,
            workflow_run_attempt=2,
        )

        assert coordinate.attempt_started_at == "2026-01-01T00:00:00Z"
        assert coordinate.workflow_run_id == 123
        assert coordinate.workflow_run_attempt == 2

    def test_is_frozen(self) -> None:
        coordinate = AttemptCoordinate(
            attempt_started_at="2026-01-01T00:00:00Z",
            workflow_run_id=123,
            workflow_run_attempt=2,
        )

        with pytest.raises(FrozenInstanceError):
            coordinate.workflow_run_attempt = 3  # type: ignore[misc]
