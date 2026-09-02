"""Tests for agentic_devtools.cli.jira.discovery._write_cache."""

import json
from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.jira.discovery import _write_cache


def _valid_metadata() -> dict:
    return {
        "version": "10.3.17",
        "versionNumbers": [10, 3, 17],
        "deploymentType": "Server",
        "buildNumber": "1003017",
        "baseUrl": "https://jira.example.com",
        "discoveredUtc": "2024-06-01T12:00:00+00:00",
    }


class TestWriteCache:
    """Tests for _write_cache."""

    def test_writes_metadata_to_cache_file(self, tmp_path: Path) -> None:
        """Writes metadata JSON to the expected cache path."""
        with patch(
            "agentic_devtools.cli.jira.discovery._get_git_repo_root",
            return_value=tmp_path,
        ):
            _write_cache(_valid_metadata())

        cache_file = tmp_path / ".agdt" / "cache" / "jira-discovery.json"
        assert cache_file.exists()
        data = json.loads(cache_file.read_text(encoding="utf-8"))
        assert data == _valid_metadata()

    def test_creates_cache_directory_if_missing(self, tmp_path: Path) -> None:
        """Creates .agdt/cache/ directory if it does not exist."""
        assert not (tmp_path / ".agdt" / "cache").exists()

        with patch(
            "agentic_devtools.cli.jira.discovery._get_git_repo_root",
            return_value=tmp_path,
        ):
            _write_cache(_valid_metadata())

        assert (tmp_path / ".agdt" / "cache").is_dir()

    def test_permission_error_emits_warning(self, tmp_path: Path, capsys) -> None:
        """Permission error emits warning to stderr but does not raise."""
        with (
            patch(
                "agentic_devtools.cli.jira.discovery._get_git_repo_root",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.jira.discovery.tempfile.mkstemp",
                side_effect=PermissionError("permission denied"),
            ),
        ):
            _write_cache(_valid_metadata())  # Should not raise

        captured = capsys.readouterr()
        assert "Cache write failed" in captured.err

    def test_no_op_when_no_repo_root(self) -> None:
        """Does nothing when _get_cache_path returns None."""
        with patch(
            "agentic_devtools.cli.jira.discovery._get_git_repo_root",
            return_value=None,
        ):
            _write_cache(_valid_metadata())  # Should not raise

    def test_replace_failure_cleans_up_temp_file(self, tmp_path: Path, capsys) -> None:
        """When os.replace fails, the temp file is cleaned up and warning emitted."""
        with (
            patch(
                "agentic_devtools.cli.jira.discovery._get_git_repo_root",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.jira.discovery.os.replace",
                side_effect=OSError("replace failed"),
            ),
        ):
            _write_cache(_valid_metadata())  # Should not raise

        captured = capsys.readouterr()
        assert "Cache write failed" in captured.err
        # Temp file should have been cleaned up
        cache_dir = tmp_path / ".agdt" / "cache"
        remaining = list(cache_dir.glob("*.tmp"))
        assert remaining == []

    def test_replace_failure_with_unlink_failure(self, tmp_path: Path, capsys) -> None:
        """When both os.replace and os.unlink fail, warning is still emitted."""
        with (
            patch(
                "agentic_devtools.cli.jira.discovery._get_git_repo_root",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.jira.discovery.os.replace",
                side_effect=OSError("replace failed"),
            ),
            patch(
                "agentic_devtools.cli.jira.discovery.os.unlink",
                side_effect=OSError("unlink failed"),
            ),
        ):
            _write_cache(_valid_metadata())  # Should not raise

        captured = capsys.readouterr()
        assert "Cache write failed" in captured.err
