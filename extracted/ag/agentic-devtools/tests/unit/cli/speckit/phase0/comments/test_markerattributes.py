"""Tests for MarkerAttributes in speckit/phase0/comments.py."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from agentic_devtools.cli.speckit.phase0.comments import MarkerAttributes


class TestMarkerAttributes:
    """Tests for the MarkerAttributes dataclass."""

    def test_preserves_parsed_marker_fields(self) -> None:
        marker = MarkerAttributes(
            schema_version="1.0",
            chain_operation_id="gh-event:delivery-1",
            operation_id="gh-event:delivery-1",
            run_id="gh:owner/repo:1:1",
            issue_id="owner/repo#1",
            attempt_started_at="2026-01-01T00:00:00Z",
        )

        assert marker.schema_version == "1.0"
        assert marker.chain_operation_id == "gh-event:delivery-1"
        assert marker.operation_id == "gh-event:delivery-1"
        assert marker.run_id == "gh:owner/repo:1:1"
        assert marker.issue_id == "owner/repo#1"
        assert marker.attempt_started_at == "2026-01-01T00:00:00Z"

    def test_is_frozen(self) -> None:
        marker = MarkerAttributes(
            schema_version="1.0",
            chain_operation_id="gh-event:delivery-1",
            operation_id="gh-event:delivery-1",
            run_id="gh:owner/repo:1:1",
            issue_id="owner/repo#1",
            attempt_started_at="2026-01-01T00:00:00Z",
        )

        with pytest.raises(FrozenInstanceError):
            marker.issue_id = "owner/repo#2"  # type: ignore[misc]
