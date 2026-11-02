"""Tests for pipeline_lock_path."""

from unittest.mock import patch

from agentic_devtools.cli.azure_devops.pr_review_pipeline_lock import (
    PIPELINE_LOCK_FILENAME,
    pipeline_lock_path,
)

_MODULE = "agentic_devtools.cli.azure_devops.pr_review_pipeline_lock"


class TestPipelineLockPath:
    def test_sits_beside_review_state(self, tmp_path):
        state_file = tmp_path / "reviews" / "review-state.json"
        with patch(f"{_MODULE}.get_review_state_file_path", return_value=state_file):
            result = pipeline_lock_path(42)
        assert result == tmp_path / "reviews" / f"{PIPELINE_LOCK_FILENAME}.42.lock"

    def test_scopes_lock_file_by_pr_id(self, tmp_path):
        state_file = tmp_path / "reviews" / "review-state.json"
        with patch(f"{_MODULE}.get_review_state_file_path", return_value=state_file):
            assert pipeline_lock_path(7) != pipeline_lock_path(8)
