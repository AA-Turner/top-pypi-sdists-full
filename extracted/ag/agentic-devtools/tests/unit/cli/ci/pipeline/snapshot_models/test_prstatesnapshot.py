"""Tests for PRStateSnapshot."""

from dataclasses import FrozenInstanceError
from inspect import signature

import pytest

from agentic_devtools.cli.ci.pipeline import PRStateSnapshot as PipelinePRStateSnapshot
from agentic_devtools.cli.ci.pipeline import build_pr_state_snapshot
from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot


class TestPRStateSnapshot:
    """Tests for PRStateSnapshot construction."""

    def test_default_construction(self) -> None:
        snapshot = PRStateSnapshot()
        assert snapshot.pr_number == 0
        assert snapshot.head_sha == ""
        assert snapshot.commit_count == 1
        assert snapshot.ci_status == "unknown"
        assert snapshot.active_session is False
        assert snapshot.is_draft is False
        assert snapshot.has_changes is False
        assert snapshot.head_author_login == ""

    def test_custom_construction(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=42,
            head_sha="abc123",
            commit_count=3,
            ci_status="passing",
            is_draft=True,
            labels=["ai-auto-merge-allowed"],
        )
        assert snapshot.pr_number == 42
        assert snapshot.head_sha == "abc123"
        assert snapshot.commit_count == 3
        assert snapshot.ci_status == "passing"
        assert snapshot.is_draft is True
        assert "ai-auto-merge-allowed" in snapshot.labels

    def test_preserves_existing_positional_arguments(self) -> None:
        snapshot = PRStateSnapshot(42, "abc123", "main", "base-sha", "feature", 3, "passing")
        assert snapshot.pr_number == 42
        assert snapshot.pr_id is None
        assert snapshot.head_sha == "abc123"
        assert snapshot.base_branch == "main"
        assert snapshot.base_sha == "base-sha"
        assert snapshot.head_branch == "feature"
        assert snapshot.commit_count == 3
        assert snapshot.ci_status == "passing"

    def test_pipeline_exports_preserve_snapshot_identity_and_builder_signature(self) -> None:
        assert PipelinePRStateSnapshot is PRStateSnapshot
        parameters = signature(build_pr_state_snapshot).parameters
        assert tuple(parameters) == ("provider", "pr_number", "actionable_check_names", "promote_findings")
        assert parameters["actionable_check_names"].default is None
        assert parameters["promote_findings"].default is True

    def test_frozen(self) -> None:
        """PRStateSnapshot should be immutable."""
        snapshot = PRStateSnapshot(pr_number=1)
        with pytest.raises(FrozenInstanceError):
            snapshot.pr_number = 2  # type: ignore[misc]
