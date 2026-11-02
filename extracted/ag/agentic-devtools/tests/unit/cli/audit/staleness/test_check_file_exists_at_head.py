"""Tests for staleness detection."""

from pathlib import Path

import pytest

from agentic_devtools.cli.audit.models import ReviewObservation
from agentic_devtools.cli.audit.staleness import check_file_exists_at_head, detect_stale_comments


class TestCheckFileExistsAtHead:
    """Tests for check_file_exists_at_head()."""

    def test_existing_file(self, tmp_path: Path) -> None:
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "main.py").write_text("code")
        assert check_file_exists_at_head("src/main.py", str(tmp_path)) is True

    def test_nonexistent_file(self, tmp_path: Path) -> None:
        assert check_file_exists_at_head("src/deleted.py", str(tmp_path)) is False

    def test_empty_path(self, tmp_path: Path) -> None:
        assert check_file_exists_at_head("", str(tmp_path)) is False

    def test_leading_slash_normalized(self, tmp_path: Path) -> None:
        (tmp_path / "file.py").write_text("code")
        assert check_file_exists_at_head("/file.py", str(tmp_path)) is True

    def test_backslashes_normalized(self, tmp_path: Path) -> None:
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "main.py").write_text("code")
        assert check_file_exists_at_head(r"src\main.py", str(tmp_path)) is True

    def test_dotdot_path_is_rejected(self, tmp_path: Path) -> None:
        outside = tmp_path.parent / "outside.py"
        outside.write_text("code")
        assert check_file_exists_at_head("../outside.py", str(tmp_path)) is False

    def test_absolute_path_is_rejected(self, tmp_path: Path) -> None:
        absolute = tmp_path / "outside.py"
        absolute.write_text("code")
        assert check_file_exists_at_head(str(absolute), str(tmp_path)) is False

    def test_windows_absolute_path_is_rejected(self, tmp_path: Path) -> None:
        assert check_file_exists_at_head(r"C:\temp\outside.py", str(tmp_path)) is False

    def test_symlink_escape_path_is_rejected(self, tmp_path: Path) -> None:
        outside_dir = tmp_path.parent / "outside-dir"
        outside_dir.mkdir(exist_ok=True)
        (outside_dir / "secret.py").write_text("code")
        try:
            (tmp_path / "linked").symlink_to(outside_dir, target_is_directory=True)
        except OSError as error:
            pytest.skip(f"Symlink creation not supported in this environment: {error}")
        assert check_file_exists_at_head("linked/secret.py", str(tmp_path)) is False


class TestDetectStaleComments:
    """Tests for detect_stale_comments() marking observations with deleted files."""

    def test_marks_stale_when_file_deleted(self, tmp_path: Path) -> None:
        obs = [
            ReviewObservation(
                file_path="deleted.py",
                line=5,
                body="Fix this",
                diff_hunk="",
                resolved=False,
                reviewer="bot",
                primary_category="other",
            ),
        ]
        result = detect_stale_comments(obs, str(tmp_path))
        assert result[0].is_stale is True

    def test_keeps_fresh_when_file_exists(self, tmp_path: Path) -> None:
        (tmp_path / "existing.py").write_text("code")
        obs = [
            ReviewObservation(
                file_path="existing.py",
                line=5,
                body="Fix this",
                diff_hunk="",
                resolved=False,
                reviewer="bot",
                primary_category="other",
            ),
        ]
        result = detect_stale_comments(obs, str(tmp_path))
        assert result[0].is_stale is False

    def test_empty_file_path_not_stale(self, tmp_path: Path) -> None:
        """Observations with empty file_path (PR-level) should not be marked stale."""
        obs = [
            ReviewObservation(
                file_path="",
                line=None,
                body="General comment",
                diff_hunk="",
                resolved=False,
                reviewer="bot",
                primary_category="other",
            ),
        ]
        result = detect_stale_comments(obs, str(tmp_path))
        assert result[0].is_stale is False

    def test_mixed_observations(self, tmp_path: Path) -> None:
        (tmp_path / "exists.py").write_text("code")
        obs = [
            ReviewObservation(
                file_path="exists.py",
                line=1,
                body="ok",
                diff_hunk="",
                resolved=False,
                reviewer="a",
                primary_category="other",
            ),
            ReviewObservation(
                file_path="deleted.py",
                line=2,
                body="gone",
                diff_hunk="",
                resolved=False,
                reviewer="b",
                primary_category="other",
            ),
        ]
        result = detect_stale_comments(obs, str(tmp_path))
        assert result[0].is_stale is False
        assert result[1].is_stale is True

    def test_stale_observation_preserves_pr_number(self, tmp_path: Path) -> None:
        """pr_number is carried over when an observation is marked stale."""
        obs = [
            ReviewObservation(
                file_path="deleted.py",
                line=1,
                body="gone",
                diff_hunk="",
                resolved=False,
                reviewer="bot",
                primary_category="other",
                pr_number=42,
            ),
        ]
        result = detect_stale_comments(obs, str(tmp_path))
        assert result[0].is_stale is True
        assert result[0].pr_number == 42
