"""Tests for agentic_devtools.cli.jira.discovery.load_cached_instance_metadata."""

import json
from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.jira.discovery import load_cached_instance_metadata


def _valid_metadata() -> dict:
    return {
        "version": "10.3.17",
        "versionNumbers": [10, 3, 17],
        "deploymentType": "Server",
        "buildNumber": "1003017",
        "baseUrl": "https://jira.example.com",
        "discoveredUtc": "2024-06-01T12:00:00+00:00",
    }


class TestLoadCachedInstanceMetadata:
    """Tests for load_cached_instance_metadata."""

    def test_returns_valid_cached_data(self, tmp_path: Path) -> None:
        """Returns cached dict when file exists and schema is valid."""
        cache_file = tmp_path / ".agdt" / "cache" / "jira-discovery.json"
        cache_file.parent.mkdir(parents=True)
        cache_file.write_text(json.dumps(_valid_metadata()), encoding="utf-8")

        with patch(
            "agentic_devtools.cli.jira.discovery._get_git_repo_root",
            return_value=tmp_path,
        ):
            result = load_cached_instance_metadata()

        assert result == _valid_metadata()

    def test_returns_none_for_missing_file(self, tmp_path: Path) -> None:
        """Returns None when cache file does not exist."""
        with patch(
            "agentic_devtools.cli.jira.discovery._get_git_repo_root",
            return_value=tmp_path,
        ):
            result = load_cached_instance_metadata()

        assert result is None

    def test_returns_none_for_malformed_json(self, tmp_path: Path) -> None:
        """Returns None when cache file contains malformed JSON."""
        cache_file = tmp_path / ".agdt" / "cache" / "jira-discovery.json"
        cache_file.parent.mkdir(parents=True)
        cache_file.write_text("not valid json {{{", encoding="utf-8")

        with patch(
            "agentic_devtools.cli.jira.discovery._get_git_repo_root",
            return_value=tmp_path,
        ):
            result = load_cached_instance_metadata()

        assert result is None

    def test_returns_none_for_invalid_utf8(self, tmp_path: Path) -> None:
        """Returns None when cache file cannot be decoded as UTF-8."""
        cache_file = tmp_path / ".agdt" / "cache" / "jira-discovery.json"
        cache_file.parent.mkdir(parents=True)
        cache_file.write_bytes(b"\xff\xfe\xfa")

        with patch(
            "agentic_devtools.cli.jira.discovery._get_git_repo_root",
            return_value=tmp_path,
        ):
            result = load_cached_instance_metadata()

        assert result is None

    def test_returns_none_for_missing_schema_key(self, tmp_path: Path) -> None:
        """Returns None when a required key is missing from the cached data."""
        data = _valid_metadata()
        del data["deploymentType"]
        cache_file = tmp_path / ".agdt" / "cache" / "jira-discovery.json"
        cache_file.parent.mkdir(parents=True)
        cache_file.write_text(json.dumps(data), encoding="utf-8")

        with patch(
            "agentic_devtools.cli.jira.discovery._get_git_repo_root",
            return_value=tmp_path,
        ):
            result = load_cached_instance_metadata()

        assert result is None

    def test_returns_none_when_no_repo_root(self) -> None:
        """Returns None when git repo root is None."""
        with patch(
            "agentic_devtools.cli.jira.discovery._get_git_repo_root",
            return_value=None,
        ):
            result = load_cached_instance_metadata()

        assert result is None

    def test_returns_none_for_non_dict_json(self, tmp_path: Path) -> None:
        """Returns None when cache file contains JSON that is not a dict."""
        cache_file = tmp_path / ".agdt" / "cache" / "jira-discovery.json"
        cache_file.parent.mkdir(parents=True)
        cache_file.write_text(json.dumps([1, 2, 3]), encoding="utf-8")

        with patch(
            "agentic_devtools.cli.jira.discovery._get_git_repo_root",
            return_value=tmp_path,
        ):
            result = load_cached_instance_metadata()

        assert result is None
