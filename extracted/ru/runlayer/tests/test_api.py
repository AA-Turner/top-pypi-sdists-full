"""Tests for RunlayerClient API methods."""

from unittest.mock import MagicMock, patch

import httpx

from runlayer_cli.api import RunlayerClient


def _mock_response(status_code: int, json_data: dict | None = None) -> MagicMock:
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status_code
    if json_data is not None:
        resp.json.return_value = json_data
    resp.raise_for_status = MagicMock()
    return resp


class TestSubmitMcpWatchScan:
    def _make_client(self) -> RunlayerClient:
        return RunlayerClient(hostname="https://example.com", secret="test-key")

    def test_returns_json_on_success(self):
        expected = {
            "servers_processed": 5,
            "shadow_servers_found": 2,
            "managed_servers_matched": 1,
        }
        mock_post = MagicMock(return_value=_mock_response(200, expected))

        with patch("httpx.Client") as mock_httpx:
            mock_httpx.return_value.__enter__ = MagicMock(
                return_value=MagicMock(post=mock_post)
            )
            mock_httpx.return_value.__exit__ = MagicMock(return_value=False)

            result = self._make_client().submit_mcp_watch_scan({"device_id": "test"})
            assert result == expected
            mock_post.assert_called_once()

    def test_falls_back_to_mcp_watch_on_404(self):
        expected = {
            "servers_processed": 3,
            "shadow_servers_found": 1,
            "managed_servers_matched": 0,
        }
        mock_post = MagicMock(
            side_effect=[_mock_response(404), _mock_response(200, expected)]
        )

        with patch("httpx.Client") as mock_httpx:
            mock_httpx.return_value.__enter__ = MagicMock(
                return_value=MagicMock(post=mock_post)
            )
            mock_httpx.return_value.__exit__ = MagicMock(return_value=False)

            result = self._make_client().submit_mcp_watch_scan({"device_id": "test"})
            assert result == expected
            assert mock_post.call_count == 2
            assert "/ai-watch/scan" in mock_post.call_args_list[0][0][0]
            assert "/mcp-watch/scan" in mock_post.call_args_list[1][0][0]

    def test_returns_unsupported_when_both_paths_404(self):
        mock_post = MagicMock(side_effect=[_mock_response(404), _mock_response(404)])

        with patch("httpx.Client") as mock_httpx:
            mock_httpx.return_value.__enter__ = MagicMock(
                return_value=MagicMock(post=mock_post)
            )
            mock_httpx.return_value.__exit__ = MagicMock(return_value=False)

            result = self._make_client().submit_mcp_watch_scan({"device_id": "test"})
            assert result == {"unsupported": True}
            assert mock_post.call_count == 2


def test_get_skill_file_uses_extended_timeout() -> None:
    client = RunlayerClient(hostname="https://example.com", secret="test-key")
    response = _mock_response(
        200,
        {
            "id": "file-1",
            "skill_id": "skill-1",
            "title": "SKILL.md",
            "content": "body",
        },
    )

    with patch("httpx.Client") as mock_httpx:
        mock_httpx.return_value.__enter__ = MagicMock(
            return_value=MagicMock(get=MagicMock(return_value=response))
        )
        mock_httpx.return_value.__exit__ = MagicMock(return_value=False)

        client.get_skill_file("skill-1", "file-1")

    assert mock_httpx.call_args.kwargs["timeout"] == 30.0


def test_list_skills_uses_extended_timeout() -> None:
    client = RunlayerClient(hostname="https://example.com", secret="test-key")
    response = _mock_response(200, {"data": [], "count": 0})

    with patch("httpx.Client") as mock_httpx:
        mock_httpx.return_value.__enter__ = MagicMock(
            return_value=MagicMock(get=MagicMock(return_value=response))
        )
        mock_httpx.return_value.__exit__ = MagicMock(return_value=False)

        client.list_skills("myorg/repo")

    assert mock_httpx.call_args.kwargs["timeout"] == 30.0


def test_list_plugins_detailed_uses_extended_timeout() -> None:
    client = RunlayerClient(hostname="https://example.com", secret="test-key")
    response = _mock_response(200, {"data": [], "count": 0})

    with patch("httpx.Client") as mock_httpx:
        mock_httpx.return_value.__enter__ = MagicMock(
            return_value=MagicMock(get=MagicMock(return_value=response))
        )
        mock_httpx.return_value.__exit__ = MagicMock(return_value=False)

        client.list_plugins_detailed("myorg/repo")

    assert mock_httpx.call_args.kwargs["timeout"] == 30.0


def test_list_server_tools_uses_extended_timeout() -> None:
    client = RunlayerClient(hostname="https://example.com", secret="test-key")
    response = _mock_response(200, [])

    with patch("httpx.Client") as mock_httpx:
        mock_httpx.return_value.__enter__ = MagicMock(
            return_value=MagicMock(get=MagicMock(return_value=response))
        )
        mock_httpx.return_value.__exit__ = MagicMock(return_value=False)

        client.list_server_tools("server-1")

    assert mock_httpx.call_args.kwargs["timeout"] == 30.0


def test_list_plugins_detailed_retries_transient_timeout() -> None:
    client = RunlayerClient(hostname="https://example.com", secret="test-key")
    request = httpx.Request("GET", "https://example.com/api/v1/plugins")
    timeout_error = httpx.ReadTimeout("timed out", request=request)
    response = _mock_response(200, {"data": [], "count": 0})
    mock_get = MagicMock(side_effect=[timeout_error, response])

    with patch("httpx.Client") as mock_httpx, patch("time.sleep") as sleep_mock:
        mock_httpx.return_value.__enter__ = MagicMock(
            return_value=MagicMock(get=mock_get)
        )
        mock_httpx.return_value.__exit__ = MagicMock(return_value=False)

        result = client.list_plugins_detailed("myorg/repo")

    assert result == []
    assert mock_get.call_count == 2
    sleep_mock.assert_called_once()


def test_list_server_tools_retries_transient_timeout() -> None:
    client = RunlayerClient(hostname="https://example.com", secret="test-key")
    request = httpx.Request("GET", "https://example.com/api/v1/proxy/server-1/tools")
    timeout_error = httpx.ReadTimeout("timed out", request=request)
    response = _mock_response(200, [{"name": "search"}])
    mock_get = MagicMock(side_effect=[timeout_error, response])

    with patch("httpx.Client") as mock_httpx, patch("time.sleep") as sleep_mock:
        mock_httpx.return_value.__enter__ = MagicMock(
            return_value=MagicMock(get=mock_get)
        )
        mock_httpx.return_value.__exit__ = MagicMock(return_value=False)

        result = client.list_server_tools("server-1")

    assert [tool.name for tool in result] == ["search"]
    assert mock_get.call_count == 2
    sleep_mock.assert_called_once()


def test_resolve_server_target_uses_resolve_endpoint() -> None:
    client = RunlayerClient(hostname="https://example.com", secret="test-key")
    response = _mock_response(200, {"server_id": "server-1"})
    mock_get = MagicMock(return_value=response)

    with patch("httpx.Client") as mock_httpx:
        mock_httpx.return_value.__enter__ = MagicMock(
            return_value=MagicMock(get=mock_get)
        )
        mock_httpx.return_value.__exit__ = MagicMock(return_value=False)

        result = client.resolve_server_target("@runlayer/agent-terminal")

    assert result == "server-1"
    mock_get.assert_called_once_with(
        "https://example.com/api/v1/local/resolve",
        params={"target": "@runlayer/agent-terminal"},
    )


def test_resolve_server_target_accepts_server_details_shape() -> None:
    client = RunlayerClient(hostname="https://example.com", secret="test-key")
    response = _mock_response(200, {"id": "server-1"})

    with patch("httpx.Client") as mock_httpx:
        mock_httpx.return_value.__enter__ = MagicMock(
            return_value=MagicMock(get=MagicMock(return_value=response))
        )
        mock_httpx.return_value.__exit__ = MagicMock(return_value=False)

        result = client.resolve_server_target("@runlayer/agent-terminal")

    assert result == "server-1"
