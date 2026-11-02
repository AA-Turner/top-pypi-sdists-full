"""Tests for the pipeline_lock context manager."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.azure_devops.pr_review_pipeline_lock import pipeline_lock, pipeline_lock_path
from agentic_devtools.file_locking import FileLockError, locked_file

_MODULE = "agentic_devtools.cli.azure_devops.pr_review_pipeline_lock"


class TestPipelineLock:
    def test_acquires_and_releases(self, tmp_path):
        state_file = tmp_path / "reviews" / "review-state.json"
        with patch(f"{_MODULE}.get_review_state_file_path", return_value=state_file):
            with pipeline_lock(7) as handle:
                assert handle is not None
            # Lock released — a second acquisition succeeds.
            with pipeline_lock(7):
                pass

    def test_second_acquisition_raises_when_held(self, tmp_path):
        state_file = tmp_path / "reviews" / "review-state.json"
        with patch(f"{_MODULE}.get_review_state_file_path", return_value=state_file):
            lock_path = pipeline_lock_path(7)
            with locked_file(lock_path, mode="r+", exclusive=True, timeout=5.0):
                with pytest.raises(FileLockError):
                    with pipeline_lock(7, timeout=0.1):
                        pass

    def test_different_pr_ids_do_not_contend(self, tmp_path):
        state_file = tmp_path / "reviews" / "review-state.json"
        with patch(f"{_MODULE}.get_review_state_file_path", return_value=state_file):
            with pipeline_lock(7):
                with pipeline_lock(8):
                    pass
