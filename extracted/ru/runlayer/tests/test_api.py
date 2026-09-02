"""Tests for RunlayerClient API methods."""

from unittest.mock import MagicMock, patch

import httpx
import pytest

from runlayer_cli.aiwatch_config_cache import SyncedAIWatchConfig
from runlayer_cli.api import RunlayerClient
from runlayer_cli.models_mcp import LocalCapabilities


def _mock_response(status_code: int, json_data: dict | None = None) -> MagicMock:
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status_code
    if json_data is not None:
        resp.json.return_value = json_data
    resp.raise_for_status = MagicMock()
    return resp


class TestUpdateCapabilities:
    def _make_client(self) -> RunlayerClient:
        return RunlayerClient(hostname="https://example.com", secret="test-key")

    def test_sends_server_version_and_checks_response(self):
        response = _mock_response(200)
        mock_post = MagicMock(return_value=response)
        capabilities = LocalCapabilities(
            tools={},
            resources={},
            prompts={},
            synced_at="2026-07-29T12:00:00Z",
        )

        with patch("httpx.Client") as mock_httpx:
            mock_httpx.return_value.__enter__ = MagicMock(
                return_value=MagicMock(post=mock_post)
            )
            mock_httpx.return_value.__exit__ = MagicMock(return_value=False)

            result = self._make_client().update_capabilities(
                "server-123", capabilities, server_version=7
            )

        assert result is response
        assert mock_post.call_args.kwargs["params"] == {"server_version": 7}
        response.raise_for_status.assert_called_once()

    def test_omits_server_version_for_older_backends(self):
        response = _mock_response(200)
        mock_post = MagicMock(return_value=response)
        capabilities = LocalCapabilities(
            tools={},
            resources={},
            prompts={},
            synced_at="2026-07-29T12:00:00Z",
        )

        with patch("httpx.Client") as mock_httpx:
            mock_httpx.return_value.__enter__ = MagicMock(
                return_value=MagicMock(post=mock_post)
            )
            mock_httpx.return_value.__exit__ = MagicMock(return_value=False)

            self._make_client().update_capabilities("server-123", capabilities)

        assert mock_post.call_args.kwargs["params"] is None


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


class TestBatchArtifactLookup:
    def _make_client(self) -> RunlayerClient:
        return RunlayerClient(hostname="https://example.com", secret="test-key")

    @pytest.mark.parametrize(
        ("method_name", "path"),
        [
            ("submit_skill_fingerprints", "skills/lookup-batch"),
            ("submit_plugin_fingerprints", "plugins/lookup-batch"),
        ],
    )
    def test_returns_batch_results(self, method_name: str, path: str):
        expected = {
            "results": [{"identifier": "known", "known": True, "has_content": True}]
        }
        mock_post = MagicMock(return_value=_mock_response(200, expected))

        with patch("httpx.Client") as mock_httpx:
            mock_httpx.return_value.__enter__ = MagicMock(
                return_value=MagicMock(post=mock_post)
            )
            mock_httpx.return_value.__exit__ = MagicMock(return_value=False)

            result = getattr(self._make_client(), method_name)(["known"])

        assert result == expected
        assert path in mock_post.call_args.args[0]
        assert mock_post.call_args.kwargs["json"] == {"identifiers": ["known"]}

    @pytest.mark.parametrize(
        "method_name",
        ["submit_skill_fingerprints", "submit_plugin_fingerprints"],
    )
    def test_returns_unsupported_when_both_batch_paths_404(self, method_name: str):
        mock_post = MagicMock(side_effect=[_mock_response(404), _mock_response(404)])

        with patch("httpx.Client") as mock_httpx:
            mock_httpx.return_value.__enter__ = MagicMock(
                return_value=MagicMock(post=mock_post)
            )
            mock_httpx.return_value.__exit__ = MagicMock(return_value=False)

            result = getattr(self._make_client(), method_name)(["unknown"])

        assert result == {"unsupported": True}
        assert mock_post.call_count == 2


class TestArtifactSubmit:
    def _make_client(self) -> RunlayerClient:
        return RunlayerClient(hostname="https://example.com", secret="test-key")

    @pytest.mark.parametrize(
        ("method_name", "payload"),
        [
            ("submit_skill", {"identifier": "skill"}),
            ("submit_plugin", {"identifier": "plugin"}),
        ],
    )
    def test_returns_unsupported_when_both_submit_paths_404(
        self,
        method_name: str,
        payload: dict[str, str],
    ) -> None:
        mock_post = MagicMock(side_effect=[_mock_response(404), _mock_response(404)])

        with patch("httpx.Client") as mock_httpx:
            mock_httpx.return_value.__enter__ = MagicMock(
                return_value=MagicMock(post=mock_post)
            )
            mock_httpx.return_value.__exit__ = MagicMock(return_value=False)

            result = getattr(self._make_client(), method_name)(payload)

        assert result == {"unsupported": True}
        assert mock_post.call_count == 2


class TestGetAIWatchConfig:
    config: SyncedAIWatchConfig = {
        "version": 1,
        "daemon_enabled": False,
        "remove_uv_tool": True,
        "mode": "protect",
        "sessions": True,
        "mcp_usage_metadata": False,
        "browser_mode": "enforce",
        "browser_sessions": False,
        "detect_processes": True,
        "detect_containers": False,
        "detect_disguised_skills": True,
        "artifact_lookup_cache": True,
        "project_depth": 12,
        "project_timeout": 90,
    }

    def _make_client(self) -> RunlayerClient:
        return RunlayerClient(hostname="https://example.com", secret="test-key")

    def test_returns_valid_config_with_bounded_timeout(self):
        mock_get = MagicMock(return_value=_mock_response(200, self.config))

        with patch("httpx.Client") as mock_httpx:
            mock_httpx.return_value.__enter__ = MagicMock(
                return_value=MagicMock(get=mock_get)
            )
            mock_httpx.return_value.__exit__ = MagicMock(return_value=False)

            result = self._make_client().get_aiwatch_config()

        assert result == self.config
        assert mock_httpx.call_args.kwargs["timeout"] == 10.0
        assert mock_get.call_args.args[0].endswith("/api/v1/ai-watch/config")

    def test_returns_none_when_endpoint_is_unsupported(self):
        mock_get = MagicMock(return_value=_mock_response(404))

        with patch("httpx.Client") as mock_httpx:
            mock_httpx.return_value.__enter__ = MagicMock(
                return_value=MagicMock(get=mock_get)
            )
            mock_httpx.return_value.__exit__ = MagicMock(return_value=False)

            assert self._make_client().get_aiwatch_config() is None

    def test_rejects_partial_config(self):
        mock_get = MagicMock(
            return_value=_mock_response(200, {"version": 1, "mode": "protect"})
        )

        with patch("httpx.Client") as mock_httpx:
            mock_httpx.return_value.__enter__ = MagicMock(
                return_value=MagicMock(get=mock_get)
            )
            mock_httpx.return_value.__exit__ = MagicMock(return_value=False)

            with pytest.raises(ValueError, match="invalid AI Watch config field"):
                self._make_client().get_aiwatch_config()


class TestSubmitAgents:
    def _make_client(self) -> RunlayerClient:
        return RunlayerClient(hostname="https://example.com", secret="test-key")

    def test_returns_json_on_success(self):
        expected = {"agents_processed": 2}
        mock_post = MagicMock(return_value=_mock_response(200, expected))

        with patch("httpx.Client") as mock_httpx:
            mock_httpx.return_value.__enter__ = MagicMock(
                return_value=MagicMock(post=mock_post)
            )
            mock_httpx.return_value.__exit__ = MagicMock(return_value=False)

            payload = {"device_id": "test", "agents": [{"framework_id": "langchain"}]}
            result = self._make_client().submit_agents(payload)

        assert result == expected
        mock_post.assert_called_once()
        assert mock_post.call_args.args[0].endswith("/api/v1/ai-watch/agents")
        assert mock_post.call_args.kwargs["json"] == payload

    def test_404_is_unsupported_no_fallback(self):
        # Agents is an ai-watch-only endpoint: a 404 is a single-shot
        # "unsupported" (no legacy mcp-watch path to retry).
        mock_post = MagicMock(return_value=_mock_response(404))

        with patch("httpx.Client") as mock_httpx:
            mock_httpx.return_value.__enter__ = MagicMock(
                return_value=MagicMock(post=mock_post)
            )
            mock_httpx.return_value.__exit__ = MagicMock(return_value=False)

            result = self._make_client().submit_agents({"device_id": "test"})

        assert result == {"unsupported": True}
        assert mock_post.call_count == 1


class TestTrackCommandEvents:
    def _make_client(self) -> RunlayerClient:
        return RunlayerClient(hostname="https://example.com", secret="test-key")

    def test_posts_events_with_bounded_timeout(self):
        mock_post = MagicMock(return_value=_mock_response(200, {"recorded": 1}))
        with patch("httpx.Client") as mock_httpx:
            mock_httpx.return_value.__enter__ = MagicMock(
                return_value=MagicMock(post=mock_post)
            )
            mock_httpx.return_value.__exit__ = MagicMock(return_value=False)
            result = self._make_client().track_command_events([{"command": "scan"}])
        assert result == {"recorded": 1}
        # Bounded timeout so command exit is never blocked on a slow backend.
        assert mock_httpx.call_args.kwargs["timeout"] == 2.0
        url = mock_post.call_args.args[0]
        assert url.endswith("/api/v1/telemetry/cli-command-events")
        assert mock_post.call_args.kwargs["json"] == {"events": [{"command": "scan"}]}

    def test_404_is_unsupported_no_op(self):
        mock_post = MagicMock(return_value=_mock_response(404))
        with patch("httpx.Client") as mock_httpx:
            mock_httpx.return_value.__enter__ = MagicMock(
                return_value=MagicMock(post=mock_post)
            )
            mock_httpx.return_value.__exit__ = MagicMock(return_value=False)
            result = self._make_client().track_command_events([{"command": "scan"}])
        assert result == {"unsupported": True}


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


def test_score_skill_sends_scan_id_header() -> None:
    client = RunlayerClient(hostname="https://example.com", secret="test-key")
    scan_id = "ci-scan-123"
    response = _mock_response(
        200,
        {
            "scan_id": scan_id,
            "skill_score": 0.1,
            "skill_risk_level": "Minimal",
            "classification": "UNKNOWN_SKILL",
            "files": [],
        },
    )
    mock_post = MagicMock(return_value=response)

    with patch("httpx.Client") as mock_httpx:
        mock_httpx.return_value.__enter__ = MagicMock(
            return_value=MagicMock(post=mock_post)
        )
        mock_httpx.return_value.__exit__ = MagicMock(return_value=False)

        result = client.score_skill(
            skill_name="review",
            files=[{"name": "SKILL.md", "content": "# Review"}],
            scan_id=scan_id,
        )

    assert result.scan_id == scan_id
    mock_post.assert_called_once_with(
        "https://example.com/api/v1/security/score/skill",
        json={
            "skill_name": "review",
            "files": [{"name": "SKILL.md", "content": "# Review"}],
        },
        headers={"x-runlayer-scan-id": scan_id},
    )
