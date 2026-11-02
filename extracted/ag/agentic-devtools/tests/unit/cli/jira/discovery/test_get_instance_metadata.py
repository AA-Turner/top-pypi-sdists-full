"""Tests for agentic_devtools.cli.jira.discovery.get_instance_metadata."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.jira.discovery import get_instance_metadata
from agentic_devtools.tools.jira import JiraConfig


def _server_response() -> dict:
    return {
        "version": "10.3.17",
        "versionNumbers": [10, 3, 17],
        "deploymentType": "Server",
        "buildNumber": "1003017",
        "baseUrl": "https://jira.example.com",
    }


def _valid_cache() -> dict:
    return {
        "version": "10.3.17",
        "versionNumbers": [10, 3, 17],
        "deploymentType": "Server",
        "buildNumber": "1003017",
        "baseUrl": "https://jira.example.com",
        "discoveredUtc": "2024-06-01T12:00:00+00:00",
    }


class TestGetInstanceMetadata:
    """Tests for get_instance_metadata."""

    def test_fresh_fetch_returns_metadata(self, tmp_path: Path) -> None:
        """Returns metadata dict on successful fresh fetch."""
        mock_client = MagicMock()
        mock_client.get.return_value = _server_response()

        with (
            patch(
                "agentic_devtools.cli.jira.discovery._get_git_repo_root",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.jira.sdk.build_jira_client",
                return_value=mock_client,
            ),
        ):
            result = get_instance_metadata()

        assert result is not None
        assert result["version"] == "10.3.17"
        assert result["deploymentType"] == "Server"

    def test_cache_hit_returns_cached_dict(self, tmp_path: Path) -> None:
        """Returns cached dict without calling SDK when cache is valid."""
        cache_file = tmp_path / ".agdt" / "cache" / "jira-discovery.json"
        cache_file.parent.mkdir(parents=True)
        cache_file.write_text(json.dumps(_valid_cache()), encoding="utf-8")

        with patch(
            "agentic_devtools.cli.jira.discovery._get_git_repo_root",
            return_value=tmp_path,
        ):
            result = get_instance_metadata()

        assert result == _valid_cache()

    def test_cache_hit_does_not_call_sdk(self, tmp_path: Path) -> None:
        """SDK .get() is not called when valid cache exists and force_refresh=False."""
        cache_file = tmp_path / ".agdt" / "cache" / "jira-discovery.json"
        cache_file.parent.mkdir(parents=True)
        cache_file.write_text(json.dumps(_valid_cache()), encoding="utf-8")

        mock_client = MagicMock()

        with (
            patch(
                "agentic_devtools.cli.jira.discovery._get_git_repo_root",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.jira.sdk.build_jira_client",
                return_value=mock_client,
            ),
        ):
            get_instance_metadata(force_refresh=False)

        mock_client.get.assert_not_called()

    def test_force_refresh_bypasses_cache(self, tmp_path: Path) -> None:
        """force_refresh=True bypasses cache and calls SDK."""
        cache_file = tmp_path / ".agdt" / "cache" / "jira-discovery.json"
        cache_file.parent.mkdir(parents=True)
        cache_file.write_text(json.dumps(_valid_cache()), encoding="utf-8")

        mock_client = MagicMock()
        mock_client.get.return_value = _server_response()

        with (
            patch(
                "agentic_devtools.cli.jira.discovery._get_git_repo_root",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.jira.sdk.build_jira_client",
                return_value=mock_client,
            ),
        ):
            result = get_instance_metadata(force_refresh=True)

        mock_client.get.assert_called_once()
        assert result is not None
        assert result["version"] == "10.3.17"

    def test_force_refresh_updates_cache(self, tmp_path: Path) -> None:
        """force_refresh=True writes new data to cache file."""
        cache_file = tmp_path / ".agdt" / "cache" / "jira-discovery.json"
        cache_file.parent.mkdir(parents=True)
        cache_file.write_text(json.dumps(_valid_cache()), encoding="utf-8")

        new_response = _server_response()
        new_response["version"] = "11.0.0"
        mock_client = MagicMock()
        mock_client.get.return_value = new_response

        with (
            patch(
                "agentic_devtools.cli.jira.discovery._get_git_repo_root",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.jira.sdk.build_jira_client",
                return_value=mock_client,
            ),
        ):
            result = get_instance_metadata(force_refresh=True)

        assert result is not None
        assert result["version"] == "11.0.0"
        updated = json.loads(cache_file.read_text(encoding="utf-8"))
        assert updated["version"] == "11.0.0"

    def test_returns_none_on_import_error(self, tmp_path: Path) -> None:
        """Returns None when SDK import fails."""
        with (
            patch(
                "agentic_devtools.cli.jira.discovery._get_git_repo_root",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.jira.sdk.build_jira_client",
                side_effect=ImportError("no module"),
            ),
        ):
            result = get_instance_metadata(force_refresh=True)

        assert result is None

    def test_returns_none_on_connection_error(self, tmp_path: Path) -> None:
        """Returns None on connection error without raising."""
        mock_client = MagicMock()
        mock_client.get.side_effect = ConnectionError("refused")

        with (
            patch(
                "agentic_devtools.cli.jira.discovery._get_git_repo_root",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.jira.sdk.build_jira_client",
                return_value=mock_client,
            ),
        ):
            result = get_instance_metadata(force_refresh=True)

        assert result is None

    def test_returns_none_on_http_401(self, tmp_path: Path) -> None:
        """Returns None on HTTP 401."""
        mock_client = MagicMock()
        mock_client.get.side_effect = Exception("HTTP 401 Unauthorized")

        with (
            patch(
                "agentic_devtools.cli.jira.discovery._get_git_repo_root",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.jira.sdk.build_jira_client",
                return_value=mock_client,
            ),
        ):
            result = get_instance_metadata(force_refresh=True)

        assert result is None

    def test_returns_none_on_json_decode_error(self, tmp_path: Path) -> None:
        """Returns None when SDK returns non-dict response."""
        mock_client = MagicMock()
        mock_client.get.return_value = "invalid"

        with (
            patch(
                "agentic_devtools.cli.jira.discovery._get_git_repo_root",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.jira.sdk.build_jira_client",
                return_value=mock_client,
            ),
        ):
            result = get_instance_metadata(force_refresh=True)

        assert result is None

    def test_returns_none_on_missing_required_fields(self, tmp_path: Path) -> None:
        """Returns None when required fields are missing from response."""
        mock_client = MagicMock()
        mock_client.get.return_value = {"buildNumber": "123"}

        with (
            patch(
                "agentic_devtools.cli.jira.discovery._get_git_repo_root",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.jira.sdk.build_jira_client",
                return_value=mock_client,
            ),
        ):
            result = get_instance_metadata(force_refresh=True)

        assert result is None

    def test_cache_write_failure_still_returns_metadata(self, tmp_path: Path) -> None:
        """Returns metadata even when cache write fails."""
        mock_client = MagicMock()
        mock_client.get.return_value = _server_response()

        with (
            patch(
                "agentic_devtools.cli.jira.discovery._get_git_repo_root",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.jira.sdk.build_jira_client",
                return_value=mock_client,
            ),
            patch(
                "agentic_devtools.cli.jira.discovery.tempfile.mkstemp",
                side_effect=PermissionError("denied"),
            ),
        ):
            result = get_instance_metadata(force_refresh=True)

        assert result is not None
        assert result["version"] == "10.3.17"

    def test_unexpected_exception_returns_none(self, tmp_path: Path) -> None:
        """Unexpected exception in the outer try block returns None without raising."""
        with (
            patch(
                "agentic_devtools.cli.jira.discovery._get_git_repo_root",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.jira.discovery.load_cached_instance_metadata",
                side_effect=RuntimeError("completely unexpected"),
            ),
        ):
            result = get_instance_metadata(force_refresh=False)

        assert result is None

    def test_config_forwarded_to_fetch_server_info(self, tmp_path: Path) -> None:
        """When config is provided it is forwarded to _fetch_server_info."""
        mock_client = MagicMock()
        mock_client.get.return_value = _server_response()
        cfg = JiraConfig(
            base_url="https://jira.example.com",
            headers={"Authorization": "******"},
            ssl_verify=True,
        )

        with (
            patch(
                "agentic_devtools.cli.jira.discovery._get_git_repo_root",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.jira.sdk.build_jira_client",
                return_value=mock_client,
            ) as mock_build,
        ):
            result = get_instance_metadata(force_refresh=True, config=cfg)

        mock_build.assert_called_once_with(config=cfg)
        assert result is not None
        assert result["version"] == "10.3.17"

    def test_config_ignored_on_cache_hit(self, tmp_path: Path) -> None:
        """Config is not forwarded to the SDK when the cache is used."""
        cache_file = tmp_path / ".agdt" / "cache" / "jira-discovery.json"
        cache_file.parent.mkdir(parents=True)
        cache_file.write_text(json.dumps(_valid_cache()), encoding="utf-8")
        cfg = JiraConfig(
            base_url="https://jira.example.com",
            headers={"Authorization": "******"},
            ssl_verify=True,
        )
        mock_client = MagicMock()

        with (
            patch(
                "agentic_devtools.cli.jira.discovery._get_git_repo_root",
                return_value=tmp_path,
            ),
            patch(
                "agentic_devtools.cli.jira.sdk.build_jira_client",
                return_value=mock_client,
            ),
        ):
            result = get_instance_metadata(force_refresh=False, config=cfg)

        mock_client.get.assert_not_called()
        assert result == _valid_cache()
