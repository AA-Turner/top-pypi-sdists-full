"""Tests for DetectionResult."""

from agentic_devtools.cli.git.worktree import DetectionResult


class TestDetectionResult:
    """Tests for DetectionResult dataclass."""

    def test_defaults_path_and_branch_to_none(self):
        """DetectionResult defaults optional path and branch fields."""
        result = DetectionResult(status="not_found")

        assert result.status == "not_found"
        assert result.path is None
        assert result.branch is None

    def test_stores_resume_details(self):
        """DetectionResult stores resume path and branch values."""
        result = DetectionResult(status="resume", path="/repo/1900", branch="feature/1900/tests")

        assert result.path == "/repo/1900"
        assert result.branch == "feature/1900/tests"
