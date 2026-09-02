"""Tests for agentic_devtools.cli.jira.discovery._fetch_server_info."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.jira.discovery import _fetch_server_info
from agentic_devtools.tools.jira import JiraConfig


def _server_response() -> dict:
    return {
        "version": "10.3.17",
        "versionNumbers": [10, 3, 17],
        "deploymentType": "Server",
        "buildNumber": "1003017",
        "baseUrl": "https://jira.example.com",
    }


class TestFetchServerInfo:
    """Tests for _fetch_server_info."""

    def test_returns_normalized_dict_on_success(self) -> None:
        """Returns a 6-key dict when the SDK call succeeds."""
        mock_client = MagicMock()
        mock_client.get.return_value = _server_response()

        with patch(
            "agentic_devtools.cli.jira.sdk.build_jira_client",
            return_value=mock_client,
        ):
            result = _fetch_server_info()

        assert result is not None
        assert result["version"] == "10.3.17"
        assert result["versionNumbers"] == [10, 3, 17]
        assert result["deploymentType"] == "Server"
        assert result["buildNumber"] == "1003017"
        assert result["baseUrl"] == "https://jira.example.com"
        assert "discoveredUtc" in result

    def test_cloud_response(self) -> None:
        """Returns Cloud deployment type correctly."""
        response = _server_response()
        response["deploymentType"] = "Cloud"
        mock_client = MagicMock()
        mock_client.get.return_value = response

        with patch(
            "agentic_devtools.cli.jira.sdk.build_jira_client",
            return_value=mock_client,
        ):
            result = _fetch_server_info()

        assert result is not None
        assert result["deploymentType"] == "Cloud"

    def test_data_center_reports_server(self) -> None:
        """Data Center instances report deploymentType as 'Server'."""
        response = _server_response()
        response["deploymentType"] = "Server"
        mock_client = MagicMock()
        mock_client.get.return_value = response

        with patch(
            "agentic_devtools.cli.jira.sdk.build_jira_client",
            return_value=mock_client,
        ):
            result = _fetch_server_info()

        assert result is not None
        assert result["deploymentType"] == "Server"

    def test_missing_build_number_normalized_to_none(self) -> None:
        """Missing buildNumber in response is normalized to None."""
        response = _server_response()
        del response["buildNumber"]
        mock_client = MagicMock()
        mock_client.get.return_value = response

        with patch(
            "agentic_devtools.cli.jira.sdk.build_jira_client",
            return_value=mock_client,
        ):
            result = _fetch_server_info()

        assert result is not None
        assert result["buildNumber"] is None

    def test_returns_none_on_import_error(self) -> None:
        """Returns None when atlassian-python-api is not installed."""
        import builtins

        _real_import = builtins.__import__

        def _block_sdk_import(name, *args, **kwargs):
            if name == "agentic_devtools.cli.jira.sdk":
                raise ImportError("simulated missing sdk")
            return _real_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=_block_sdk_import):
            result = _fetch_server_info()

        assert result is None

    def test_returns_none_on_connection_error(self) -> None:
        """Returns None on connection error."""
        mock_client = MagicMock()
        mock_client.get.side_effect = ConnectionError("refused")

        with patch(
            "agentic_devtools.cli.jira.sdk.build_jira_client",
            return_value=mock_client,
        ):
            result = _fetch_server_info()

        assert result is None

    def test_returns_none_on_http_401(self) -> None:
        """Returns None when SDK raises on 401."""
        mock_client = MagicMock()
        mock_client.get.side_effect = Exception("HTTP 401 Unauthorized")

        with patch(
            "agentic_devtools.cli.jira.sdk.build_jira_client",
            return_value=mock_client,
        ):
            result = _fetch_server_info()

        assert result is None

    def test_returns_none_on_non_dict_response(self) -> None:
        """Returns None when response is not a dict."""
        mock_client = MagicMock()
        mock_client.get.return_value = "not a dict"

        with patch(
            "agentic_devtools.cli.jira.sdk.build_jira_client",
            return_value=mock_client,
        ):
            result = _fetch_server_info()

        assert result is None

    def test_returns_none_on_missing_required_fields(self) -> None:
        """Returns None when required fields (version, baseUrl, etc.) are missing."""
        mock_client = MagicMock()
        mock_client.get.return_value = {"buildNumber": "123"}

        with patch(
            "agentic_devtools.cli.jira.sdk.build_jira_client",
            return_value=mock_client,
        ):
            result = _fetch_server_info()

        assert result is None

    def test_config_is_forwarded_to_build_jira_client(self) -> None:
        """When config is provided, it is forwarded to build_jira_client."""
        mock_client = MagicMock()
        mock_client.get.return_value = _server_response()
        cfg = JiraConfig(
            base_url="https://jira.example.com",
            headers={"Authorization": "******"},
            ssl_verify=True,
        )

        with patch(
            "agentic_devtools.cli.jira.sdk.build_jira_client",
            return_value=mock_client,
        ) as mock_build:
            result = _fetch_server_info(config=cfg)

        mock_build.assert_called_once_with(config=cfg)
        assert result is not None
        assert result["version"] == "10.3.17"
