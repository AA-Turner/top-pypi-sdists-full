import json
from unittest.mock import MagicMock, patch

import httpx
from typer.testing import CliRunner

from runlayer_cli.api import RunlayerClient
from runlayer_cli.commands.logs import (
    TYPE_SHORTCUTS,
    _expand_type,
    _format_details,
    _format_resource,
    _status_style,
)
from runlayer_cli.main import app
from runlayer_cli.symbols import FAIL, OK, WARN

runner = CliRunner()


class TestExpandType:
    def test_shortcut_expands(self):
        result = _expand_type("auth")
        assert "auth_success" in result
        assert "auth_failed" in result
        assert "proxy_oauth_token_issued" in result

    def test_raw_passthrough(self):
        assert _expand_type("tool_call_success") == "tool_call_success"

    def test_mixed_shortcut_and_raw(self):
        result = _expand_type("auth,tool_call_success")
        assert "auth_success" in result
        assert "tool_call_success" in result

    def test_multiple_shortcuts(self):
        result = _expand_type("auth,tools")
        assert "auth_success" in result
        assert "tool_call_success" in result

    def test_whitespace_stripped(self):
        result = _expand_type("auth , tools")
        assert "auth_success" in result
        assert "tool_call_success" in result

    def test_all_shortcuts_defined(self):
        for shortcut in TYPE_SHORTCUTS:
            result = _expand_type(shortcut)
            assert len(result) > len(shortcut)


class TestStatusStyle:
    def test_failure_types(self):
        assert _status_style("auth_failed") == (FAIL, "red")
        assert _status_style("tool_call_failure") == (FAIL, "red")
        assert _status_style("client_token_refresh_failure") == (FAIL, "red")

    def test_warning_types(self):
        assert _status_style("security_violation") == (WARN, "yellow")
        assert _status_style("shadow_mcp_detected") == (WARN, "yellow")

    def test_success_types(self):
        assert _status_style("auth_success") == (OK, "green")
        assert _status_style("tool_call_success") == (OK, "green")
        assert _status_style("oauth_connected") == (OK, "green")

    def test_unknown_defaults_to_ok(self):
        assert _status_style("some_unknown_event") == (OK, "green")


class TestFormatDetails:
    def test_empty_details(self):
        assert _format_details("auth_success", {}) == ""

    def test_auth_success(self):
        result = _format_details(
            "auth_success", {"auth_method": "api_key", "client_name": "Runlayer CLI"}
        )
        assert "api_key" in result
        assert "Runlayer CLI" in result

    def test_auth_failed(self):
        result = _format_details("auth_failed", {"reason": "Invalid API key"})
        assert result == "Invalid API key"

    def test_proxy_oauth_token_issued(self):
        result = _format_details(
            "proxy_oauth_token_issued",
            {"grant_type": "refresh_token", "client_name": "Claude Code"},
        )
        assert "refresh_token grant" in result
        assert "client: Claude Code" in result

    def test_proxy_oauth_authorization_failed(self):
        result = _format_details(
            "proxy_oauth_authorization_failed", {"error_reason": "Invalid redirect_uri"}
        )
        assert result == "Invalid redirect_uri"

    def test_client_token_refresh_failure(self):
        result = _format_details(
            "client_token_refresh_failure", {"error_reason": "refresh token revoked"}
        )
        assert result == "refresh token revoked"

    def test_security_violation(self):
        result = _format_details(
            "security_violation", {"violation_reason": "suspicious content"}
        )
        assert result == "suspicious content"

    def test_tool_call(self):
        result = _format_details(
            "tool_call_success", {"resource_name": "read_file"}
        )
        assert result == "read_file"

    def test_default_shows_key_value_pairs(self):
        result = _format_details(
            "some_event",
            {
                "event_type": "some_event",
                "subject_id": "123",
                "custom_field": "value1",
                "another_field": "value2",
            },
        )
        assert "custom_field=value1" in result
        assert "another_field=value2" in result
        # Skipped internal fields should not appear
        assert "event_type" not in result
        assert "subject_id" not in result

    def test_default_limits_to_three_fields(self):
        result = _format_details(
            "some_event",
            {"a": "1", "b": "2", "c": "3", "d": "4"},
        )
        assert result.count("=") == 3

    def test_default_skips_none_and_complex(self):
        result = _format_details(
            "some_event",
            {"field": None, "nested": {"a": 1}, "items": [1, 2], "visible": "yes"},
        )
        assert "visible=yes" in result
        assert "field" not in result
        assert "nested" not in result
        assert "items" not in result


class TestFormatResource:
    def test_resource_info_name(self):
        log = {"resource_info": {"name": "my-server"}}
        assert _format_resource(log) == "my-server"

    def test_details_server_name(self):
        log = {"details": {"server_name": "other-server"}}
        assert _format_resource(log) == "other-server"

    def test_details_resource_name(self):
        log = {"details": {"resource_name": "my-tool"}}
        assert _format_resource(log) == "my-tool"

    def test_fallback_dash(self):
        log = {}
        assert _format_resource(log) == "\u2014"

    def test_details_server_name_preferred_over_resource_info(self):
        log = {
            "resource_info": {"name": "from-info"},
            "details": {"server_name": "from-details"},
        }
        assert _format_resource(log) == "from-details"

    def test_empty_resource_info_falls_through(self):
        log = {"resource_info": {"name": None}, "details": {"server_name": "fallback"}}
        assert _format_resource(log) == "fallback"


def _mock_response(status_code: int, json_data: dict | None = None) -> MagicMock:
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status_code
    if json_data is not None:
        resp.json.return_value = json_data
    resp.raise_for_status = MagicMock()
    return resp


class TestGetAuditLogs:
    def _make_client(self) -> RunlayerClient:
        return RunlayerClient(hostname="https://example.com", secret="test-key")

    def test_passes_params(self):
        expected = {"data": [], "count": 0, "chart_bins": []}
        mock_get = MagicMock(return_value=_mock_response(200, expected))

        with patch("httpx.Client") as mock_httpx:
            mock_httpx.return_value.__enter__ = MagicMock(
                return_value=MagicMock(get=mock_get)
            )
            mock_httpx.return_value.__exit__ = MagicMock(return_value=False)

            result = self._make_client().get_audit_logs(
                action_type="auth_success",
                server_id="abc-123",
                limit=10,
            )
            assert result == expected

            call_args = mock_get.call_args
            params = call_args[1].get("params") or call_args.kwargs.get("params")
            assert params["action_type"] == "auth_success"
            assert params["server_id"] == "abc-123"
            assert params["limit"] == 10

    def test_omits_none_params(self):
        expected = {"data": [], "count": 0, "chart_bins": []}
        mock_get = MagicMock(return_value=_mock_response(200, expected))

        with patch("httpx.Client") as mock_httpx:
            mock_httpx.return_value.__enter__ = MagicMock(
                return_value=MagicMock(get=mock_get)
            )
            mock_httpx.return_value.__exit__ = MagicMock(return_value=False)

            self._make_client().get_audit_logs()

            call_args = mock_get.call_args
            params = call_args[1].get("params") or call_args.kwargs.get("params")
            assert "action_type" not in params
            assert "server_id" not in params
            assert params["limit"] == 50


SAMPLE_API_RESPONSE = {
    "data": [
        {
            "timestamp": "2026-03-25T14:30:05Z",
            "action_type": "auth_success",
            "resource_info": {"name": "my-server"},
            "actor_info": {"email": "user@example.com", "name": "Test User"},
            "details": {"auth_method": "api_key", "client_name": "Runlayer CLI"},
        },
        {
            "timestamp": "2026-03-25T14:25:12Z",
            "action_type": "auth_failed",
            "resource_info": None,
            "actor_info": None,
            "details": {"reason": "Invalid API key"},
        },
    ],
    "count": 2,
    "chart_bins": [],
}


class TestLogsCommand:
    @patch("runlayer_cli.commands.logs.resolve_credentials")
    @patch("runlayer_cli.commands.logs.RunlayerClient")
    def test_json_output(self, mock_client_cls, mock_resolve):
        mock_resolve.return_value = {"host": "https://example.com", "secret": "key"}
        mock_client_cls.return_value.get_audit_logs.return_value = SAMPLE_API_RESPONSE

        result = runner.invoke(app, ["logs", "--json", "--start", "2026-03-24T00:00:00Z"])
        assert result.exit_code == 0
        parsed = json.loads(result.stdout)
        assert len(parsed) == 2
        assert parsed[0]["action_type"] == "auth_success"

    @patch("runlayer_cli.commands.logs.resolve_credentials")
    @patch("runlayer_cli.commands.logs.RunlayerClient")
    def test_table_output(self, mock_client_cls, mock_resolve):
        mock_resolve.return_value = {"host": "https://example.com", "secret": "key"}
        mock_client_cls.return_value.get_audit_logs.return_value = SAMPLE_API_RESPONSE

        result = runner.invoke(app, ["logs", "--start", "2026-03-24T00:00:00Z"])
        assert result.exit_code == 0
        output = result.output
        assert "Audit Logs" in output
        assert "2 total" in output

    @patch("runlayer_cli.commands.logs.resolve_credentials")
    @patch("runlayer_cli.commands.logs.RunlayerClient")
    def test_empty_results(self, mock_client_cls, mock_resolve):
        mock_resolve.return_value = {"host": "https://example.com", "secret": "key"}
        mock_client_cls.return_value.get_audit_logs.return_value = {
            "data": [],
            "count": 0,
            "chart_bins": [],
        }

        result = runner.invoke(app, ["logs"])
        assert result.exit_code == 0
        assert "No events found" in result.output

    @patch("runlayer_cli.commands.logs.resolve_credentials")
    @patch("runlayer_cli.commands.logs.RunlayerClient")
    def test_type_shortcut_passed_to_api(self, mock_client_cls, mock_resolve):
        mock_resolve.return_value = {"host": "https://example.com", "secret": "key"}
        mock_client_cls.return_value.get_audit_logs.return_value = {
            "data": [],
            "count": 0,
            "chart_bins": [],
        }

        runner.invoke(app, ["logs", "-t", "auth"])

        call_kwargs = mock_client_cls.return_value.get_audit_logs.call_args[1]
        assert "auth_success" in call_kwargs["action_type"]
        assert "auth_failed" in call_kwargs["action_type"]

    @patch("runlayer_cli.commands.logs.resolve_credentials")
    @patch("runlayer_cli.commands.logs.RunlayerClient")
    def test_api_error_exits_1(self, mock_client_cls, mock_resolve):
        mock_resolve.return_value = {"host": "https://example.com", "secret": "key"}
        mock_client_cls.return_value.get_audit_logs.side_effect = httpx.HTTPStatusError(
            "Unauthorized", request=MagicMock(), response=MagicMock(status_code=401)
        )

        result = runner.invoke(app, ["logs"])
        assert result.exit_code == 1
        assert "Error" in result.output

    @patch("runlayer_cli.commands.logs.resolve_credentials")
    @patch("runlayer_cli.commands.logs.RunlayerClient")
    def test_limit_capped_at_2000(self, mock_client_cls, mock_resolve):
        mock_resolve.return_value = {"host": "https://example.com", "secret": "key"}
        mock_client_cls.return_value.get_audit_logs.return_value = {
            "data": [],
            "count": 0,
            "chart_bins": [],
        }

        runner.invoke(app, ["logs", "-n", "5000"])

        call_kwargs = mock_client_cls.return_value.get_audit_logs.call_args[1]
        assert call_kwargs["limit"] == 2000

    @patch("runlayer_cli.commands.logs.resolve_credentials")
    @patch("runlayer_cli.commands.logs.RunlayerClient")
    def test_more_events_hint(self, mock_client_cls, mock_resolve):
        mock_resolve.return_value = {"host": "https://example.com", "secret": "key"}
        mock_client_cls.return_value.get_audit_logs.return_value = {
            "data": [SAMPLE_API_RESPONSE["data"][0]],
            "count": 100,
            "chart_bins": [],
        }

        result = runner.invoke(app, ["logs"])
        assert result.exit_code == 0
        assert "99 more events" in result.output

    @patch("runlayer_cli.commands.logs.resolve_credentials")
    @patch("runlayer_cli.commands.logs.RunlayerClient")
    def test_user_id_passed_to_api(self, mock_client_cls, mock_resolve):
        mock_resolve.return_value = {"host": "https://example.com", "secret": "key"}
        mock_client_cls.return_value.get_audit_logs.return_value = {
            "data": [],
            "count": 0,
            "chart_bins": [],
        }

        runner.invoke(app, ["logs", "--user-id", "abc-123"])

        call_kwargs = mock_client_cls.return_value.get_audit_logs.call_args[1]
        assert call_kwargs["user_id"] == "abc-123"

    @patch("runlayer_cli.commands.logs.resolve_credentials")
    @patch("runlayer_cli.commands.logs.RunlayerClient")
    def test_default_scopes_to_own_logs(self, mock_client_cls, mock_resolve):
        mock_resolve.return_value = {"host": "https://example.com", "secret": "key"}
        mock_client_cls.return_value.get_current_user.return_value = {"id": "user-123"}
        mock_client_cls.return_value.get_audit_logs.return_value = {
            "data": [],
            "count": 0,
            "chart_bins": [],
        }

        runner.invoke(app, ["logs"])

        call_kwargs = mock_client_cls.return_value.get_audit_logs.call_args[1]
        assert call_kwargs["actor_id"] == "user-123"

    @patch("runlayer_cli.commands.logs.resolve_credentials")
    @patch("runlayer_cli.commands.logs.RunlayerClient")
    def test_all_flag_skips_actor_scoping(self, mock_client_cls, mock_resolve):
        mock_resolve.return_value = {"host": "https://example.com", "secret": "key"}
        mock_client_cls.return_value.get_audit_logs.return_value = {
            "data": [],
            "count": 0,
            "chart_bins": [],
        }

        runner.invoke(app, ["logs", "--all"])

        mock_client_cls.return_value.get_current_user.assert_not_called()
        call_kwargs = mock_client_cls.return_value.get_audit_logs.call_args[1]
        assert call_kwargs["actor_id"] is None
