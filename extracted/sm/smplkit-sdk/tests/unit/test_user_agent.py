"""Default User-Agent injection across every transport path.

The platform sits behind a WAF that rejects requests carrying no
User-Agent, so the SDK stamps ``smplkit-sdk-python/<version>`` on every
outbound HTTP request and on the WebSocket handshake — unless the caller
already supplied a User-Agent (matched case-insensitively) through an
``extra_headers`` surface, in which case the caller's value wins.
"""

from __future__ import annotations

import asyncio
import json
import time
from unittest.mock import AsyncMock, MagicMock, patch

import smplkit
from smplkit import (
    AccountClient,
    AsyncAccountClient,
    AsyncLoggingClient,
    AuditClient,
    ConfigClient,
    FlagsClient,
    JobsClient,
    LoggingClient,
    PlatformClient,
    SmplClient,
)
from smplkit._config import ResolvedClientConfig
from smplkit._transport import SDK_USER_AGENT, build_service_transports, with_default_user_agent
from smplkit._ws import SharedWebSocket


def _cfg(extra_headers: dict[str, str] | None = None) -> ResolvedClientConfig:
    return ResolvedClientConfig(
        api_key="sk_test",
        base_domain="example.test",
        scheme="https",
        debug=False,
        extra_headers=extra_headers,
    )


# ===================================================================
# 1. The constant and the helper
# ===================================================================


class TestUserAgentConstant:
    def test_format_is_sdk_name_slash_version(self):
        assert SDK_USER_AGENT.startswith("smplkit-sdk-python/")
        assert SDK_USER_AGENT == f"smplkit-sdk-python/{smplkit.__version__}"

    def test_version_part_is_the_resolved_version(self):
        assert SDK_USER_AGENT.split("/", 1)[1] == smplkit.__version__

    def test_falls_back_to_zero_version_without_version_module(self):
        """Source-tree runs without a build get smplkit-sdk-python/0.0.0."""
        import importlib
        import sys

        original_transport = sys.modules["smplkit._transport"]
        original_version = sys.modules.get("smplkit._version")
        sys.modules["smplkit._version"] = None  # type: ignore[assignment]
        sys.modules.pop("smplkit._transport")
        try:
            importlib.invalidate_caches()
            import smplkit._transport as fresh_transport

            assert fresh_transport.SDK_USER_AGENT == "smplkit-sdk-python/0.0.0"
        finally:
            sys.modules["smplkit._transport"] = original_transport
            if original_version is not None:
                sys.modules["smplkit._version"] = original_version
            else:
                sys.modules.pop("smplkit._version", None)


class TestWithDefaultUserAgent:
    def test_adds_default_when_absent(self):
        assert with_default_user_agent(None) == {"User-Agent": SDK_USER_AGENT}
        assert with_default_user_agent({}) == {"User-Agent": SDK_USER_AGENT}
        merged = with_default_user_agent({"X-Test": "v"})
        assert merged == {"X-Test": "v", "User-Agent": SDK_USER_AGENT}

    def test_does_not_mutate_the_input(self):
        original = {"X-Test": "v"}
        with_default_user_agent(original)
        assert original == {"X-Test": "v"}

    def test_caller_user_agent_wins_exact_case(self):
        headers = {"User-Agent": "acme-integration/9.9"}
        assert with_default_user_agent(headers) == {"User-Agent": "acme-integration/9.9"}

    def test_caller_user_agent_wins_alternate_casing(self):
        for name in ("user-agent", "USER-AGENT", "uSeR-aGeNt"):
            merged = with_default_user_agent({name: "acme-integration/9.9"})
            assert merged == {name: "acme-integration/9.9"}
            assert "User-Agent" not in merged


# ===================================================================
# 2. Wired transports (build_service_transports → SmplClient)
# ===================================================================


class TestWiredTransports:
    def test_all_five_service_transports_carry_default_ua(self):
        t = build_service_transports(_cfg())
        for http in (t.app_http, t.config_http, t.flags_http, t.logging_http, t.jobs_http):
            assert http._headers["User-Agent"] == SDK_USER_AGENT
        # The jobs JSON:API Accept header still rides alongside.
        assert t.jobs_http._headers["Accept"] == "application/vnd.api+json"

    def test_httpx_client_sends_the_default_ua(self):
        """httpx applies client default headers to every request — assert at that level."""
        t = build_service_transports(_cfg())
        try:
            assert t.app_http.get_httpx_client().headers["user-agent"] == SDK_USER_AGENT
        finally:
            t.close()

    def test_caller_ua_wins_any_casing_down_to_httpx(self):
        t = build_service_transports(_cfg(extra_headers={"user-agent": "acme-integration/9.9"}))
        try:
            for http in (t.app_http, t.config_http, t.flags_http, t.logging_http, t.jobs_http):
                assert "User-Agent" not in http._headers
                assert http._headers["user-agent"] == "acme-integration/9.9"
            assert t.app_http.get_httpx_client().headers["user-agent"] == "acme-integration/9.9"
        finally:
            t.close()

    def test_smpl_client_stamps_every_surface(self):
        client = SmplClient(api_key="sk_api_test", environment="test", service="svc")
        for http in (
            client._app_http,
            client._http_client,  # config
            client.flags._flags_http,
            client.logging._logging_http,
            client._transports.jobs_http,
            client.audit._auth,
        ):
            assert http._headers["User-Agent"] == SDK_USER_AGENT
        assert client.account.settings._headers["User-Agent"] == SDK_USER_AGENT

    def test_smpl_client_caller_ua_wins_on_every_surface(self):
        client = SmplClient(
            api_key="sk_api_test",
            environment="test",
            service="svc",
            extra_headers={"user-agent": "acme-integration/9.9"},
        )
        for http in (
            client._app_http,
            client._http_client,  # config
            client.flags._flags_http,
            client.logging._logging_http,
            client._transports.jobs_http,
            client.audit._auth,
        ):
            assert "User-Agent" not in http._headers
            assert http._headers["user-agent"] == "acme-integration/9.9"
        assert "User-Agent" not in client.account.settings._headers
        assert client.account.settings._headers["user-agent"] == "acme-integration/9.9"


# ===================================================================
# 3. Standalone sub-clients
# ===================================================================


class TestStandaloneClients:
    def test_config_client(self):
        client = ConfigClient(api_key="sk_test", base_domain="example.test")
        assert client._http._headers["User-Agent"] == SDK_USER_AGENT

    def test_flags_client_both_transports(self):
        client = FlagsClient(api_key="sk_test", base_domain="example.test")
        assert client._flags_http._headers["User-Agent"] == SDK_USER_AGENT
        assert client._app_http_standalone._headers["User-Agent"] == SDK_USER_AGENT

    def test_logging_client_both_transports(self):
        client = LoggingClient(api_key="sk_test", base_domain="example.test")
        assert client._logging_http._headers["User-Agent"] == SDK_USER_AGENT
        assert client._app_http_standalone._headers["User-Agent"] == SDK_USER_AGENT

    def test_audit_client(self):
        client = AuditClient(api_key="sk_test", base_url="https://audit.example.test", environment="test")
        assert client._auth._headers["User-Agent"] == SDK_USER_AGENT
        assert client._auth._headers["Accept"] == "application/vnd.api+json"

    def test_jobs_client(self):
        client = JobsClient(api_key="sk_test", base_domain="example.test")
        assert client._auth._headers["User-Agent"] == SDK_USER_AGENT

    def test_platform_client(self):
        client = PlatformClient(api_key="sk_test", base_domain="example.test")
        assert client._app_http._headers["User-Agent"] == SDK_USER_AGENT

    def test_account_client_sync_and_async(self):
        client = AccountClient(api_key="sk_test", base_domain="example.test")
        assert client.settings._headers["User-Agent"] == SDK_USER_AGENT
        aclient = AsyncAccountClient(api_key="sk_test", base_domain="example.test")
        assert aclient.settings._headers["User-Agent"] == SDK_USER_AGENT

    def test_standalone_caller_ua_wins_alternate_casing(self):
        audit = AuditClient(
            api_key="sk_test",
            base_url="https://audit.example.test",
            environment="test",
            extra_headers={"user-agent": "acme-integration/9.9"},
        )
        assert "User-Agent" not in audit._auth._headers
        assert audit._auth._headers["user-agent"] == "acme-integration/9.9"

        account = AccountClient(
            api_key="sk_test",
            base_domain="example.test",
            extra_headers={"USER-AGENT": "acme-integration/9.9"},
        )
        assert "User-Agent" not in account.settings._headers
        assert account.settings._headers["USER-AGENT"] == "acme-integration/9.9"


# ===================================================================
# 4. WebSocket handshake
# ===================================================================


class TestWebSocketHandshake:
    def test_handshake_sends_the_sdk_user_agent(self):
        """The WS upgrade carries the same (renamed) UA as the HTTP transports."""
        ws = SharedWebSocket(app_base_url="https://app.example.test", api_key="sk_test")

        mock_ws_conn = AsyncMock()
        mock_ws_conn.recv = AsyncMock(return_value=json.dumps({"type": "connected"}))

        async def _run():
            with patch(
                "smplkit._ws.websockets.asyncio.client.connect", new_callable=AsyncMock, return_value=mock_ws_conn
            ) as mock_connect:
                ws._closed = True  # Exit receive loop immediately
                await ws._connect()
            return mock_connect

        mock_connect = asyncio.run(_run())
        headers = mock_connect.call_args.kwargs["additional_headers"]
        assert headers == {"User-Agent": SDK_USER_AGENT}
        # Locks in the smplkit-python-sdk → smplkit-sdk-python rename.
        assert headers["User-Agent"].startswith("smplkit-sdk-python/")


# ===================================================================
# 5. Async logging WS refresh — loop-scoped transport rebuilds
# ===================================================================


def _wait_for_call(mock_obj, timeout: float = 2.0) -> None:
    deadline = time.monotonic() + timeout
    while mock_obj.call_args is None:
        if time.monotonic() >= deadline:
            raise AssertionError("mocked AuthenticatedClient was never constructed")
        time.sleep(0.01)


class TestAsyncLoggingRefreshTransports:
    """AsyncLoggingClient rebuilds a fresh AuthenticatedClient per WS event
    (loop-scoped); those rebuilds must mirror the User-Agent decision."""

    def _wired_client(self) -> AsyncLoggingClient:
        parent = MagicMock()
        parent._api_key = "sk_test"
        parent._environment = "test"
        parent._service = None
        transport = MagicMock()
        transport._base_url = "http://logging:8003"
        return AsyncLoggingClient(parent=parent, transport=transport, metrics=None)

    @patch("smplkit.logging.clients.AuthenticatedClient")
    def test_loggers_changed_refresh_client_carries_default_ua(self, mock_ac_cls):
        client = self._wired_client()
        client._handle_loggers_changed({})
        _wait_for_call(mock_ac_cls)
        headers = mock_ac_cls.call_args.kwargs["headers"]
        assert headers["User-Agent"] == SDK_USER_AGENT

    @patch("smplkit.logging.clients.AuthenticatedClient")
    def test_run_ws_handler_client_carries_default_ua(self, mock_ac_cls):
        client = self._wired_client()

        async def _noop(key, http, pre):
            return None

        client._run_ws_handler(_noop, "some-logger", {})
        _wait_for_call(mock_ac_cls)
        headers = mock_ac_cls.call_args.kwargs["headers"]
        assert headers["User-Agent"] == SDK_USER_AGENT

    def test_refresh_client_inherits_caller_ua(self):
        """A caller-supplied User-Agent rides the rebuilds too — no default."""
        # Construct BEFORE patching so the real standalone transport (with the
        # caller's headers) is built; only the per-event rebuild is mocked.
        client = AsyncLoggingClient(
            api_key="sk_test",
            base_domain="example.test",
            extra_headers={"user-agent": "acme-integration/9.9"},
        )
        with patch("smplkit.logging.clients.AuthenticatedClient") as mock_ac_cls:
            client._handle_loggers_changed({})
            _wait_for_call(mock_ac_cls)
            headers = mock_ac_cls.call_args.kwargs["headers"]
        assert "User-Agent" not in headers
        assert headers["user-agent"] == "acme-integration/9.9"
