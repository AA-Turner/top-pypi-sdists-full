"""Tests for compute_next_action in speckit/phase0/observability.py (FR-010)."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.speckit.phase0.observability import compute_next_action


class TestComputeNextAction:
    """Tests for the compute_next_action function."""

    def test_succeeded_is_none(self) -> None:
        result = compute_next_action(
            final_outcome="succeeded",
            last_stage="pull_request",
            artifact_branch="b",
            artifact_path="p",
            commit_sha="s",
        )
        assert result == "none"

    def test_skipped_is_none(self) -> None:
        result = compute_next_action(
            final_outcome="skipped", last_stage=None, artifact_branch=None, artifact_path=None, commit_sha=None
        )
        assert result == "none"

    def test_blocked_requires_manual_intervention(self) -> None:
        result = compute_next_action(
            final_outcome="blocked",
            last_stage="validation",
            artifact_branch=None,
            artifact_path=None,
            commit_sha=None,
        )
        assert result == "manual-intervention-required"

    def test_failed_delegates_to_resumability(self) -> None:
        result = compute_next_action(
            final_outcome="failed",
            last_stage="commit",
            artifact_branch="b",
            artifact_path="p",
            commit_sha=None,
        )
        assert result == "resume-safe:commit"

    def test_partial_delegates_to_resumability(self) -> None:
        result = compute_next_action(
            final_outcome="partial",
            last_stage="pull_request",
            artifact_branch=None,
            artifact_path=None,
            commit_sha=None,
        )
        assert result == "retry-safe:from-start"

    def test_raises_for_in_progress_outcome(self) -> None:
        with pytest.raises(ValueError):
            compute_next_action(
                final_outcome="in_progress",
                last_stage="validation",
                artifact_branch=None,
                artifact_path=None,
                commit_sha=None,
            )
