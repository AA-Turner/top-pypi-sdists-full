"""Standalone (non-wired) construction + lifecycle for the fused logging client.

These exercise the paths a ``LoggingClient(api_key=..., ...)`` takes when it is
NOT wired into a ``SmplClient``: it builds and owns its own logging + app
transports, opens and owns its own WebSocket on ``install()``, and tears down
only what it owns on ``close()`` / ``aclose()``.
"""

from __future__ import annotations

import asyncio
from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock, patch

from smplkit import AsyncLoggingClient, LoggingClient


def _ok_response(parsed=None, status=HTTPStatus.OK):
    resp = MagicMock()
    resp.status_code = status
    resp.content = b""
    resp.parsed = parsed
    return resp


def _empty_list_parsed():
    parsed = MagicMock()
    parsed.data = []
    return parsed


# ---------------------------------------------------------------------------
# Sync standalone
# ---------------------------------------------------------------------------


class TestStandaloneConstruction:
    def test_builds_own_transports(self):
        client = LoggingClient(api_key="sk_test", base_domain="example.test", environment="prod")
        assert client._owns_transport is True
        assert client._parent is None
        assert client._environment == "prod"
        # Standalone has no parent to inherit a service from.
        assert client._service is None
        assert client._app_base_url == "https://app.example.test"
        assert client._logging_base_url == "https://logging.example.test"
        # The two management sub-clients share the client's discovery buffer.
        assert client.loggers._buffer is client._buffer
        client.close()

    def test_base_url_override_used_directly(self):
        client = LoggingClient(api_key="sk_test", base_url="http://logging.localhost", base_domain="example.test")
        assert client._logging_base_url == "http://logging.localhost"
        client.close()

    def test_standalone_api_key_resolved_from_token(self, monkeypatch):
        # api_key omitted → resolved from the ambient config. Provide it via the
        # env var so the test does not depend on a developer's ~/.smplkit.
        monkeypatch.setenv("SMPLKIT_API_KEY", "sk_ambient")
        client = LoggingClient(base_url="http://logging.localhost", base_domain="example.test")
        assert client._standalone_api_key is not None
        client.close()

    @patch("smplkit.logging.clients.list_log_groups.sync_detailed")
    @patch("smplkit.logging.clients.list_loggers.sync_detailed")
    @patch("smplkit.logging.clients.bulk_register_loggers.sync_detailed")
    @patch("smplkit.logging.clients._auto_load_adapters")
    def test_install_opens_own_ws(self, mock_auto_load, mock_bulk, mock_loggers, mock_groups):
        mock_auto_load.return_value = []
        mock_bulk.return_value = _ok_response()
        mock_loggers.return_value = _ok_response(_empty_list_parsed())
        mock_groups.return_value = _ok_response(_empty_list_parsed())

        client = LoggingClient(api_key="sk_test", base_domain="example.test")
        fake_ws = MagicMock()
        with patch("smplkit.logging.clients.SharedWebSocket", return_value=fake_ws) as ws_cls:
            client.install()
        ws_cls.assert_called_once()
        assert client._owns_ws is True
        assert client._ws_manager is fake_ws
        fake_ws.start.assert_called_once()
        client.close()
        fake_ws.stop.assert_called_once()

    def test_close_tears_down_owned_transports(self):
        client = LoggingClient(api_key="sk_test", base_domain="example.test")
        logging_inner = MagicMock()
        app_inner = MagicMock()
        client._logging_http._client = logging_inner
        client._app_http_standalone._client = app_inner
        client.close()
        logging_inner.close.assert_called_once()
        app_inner.close.assert_called_once()
        assert client._logging_http._client is None
        assert client._app_http_standalone._client is None

    def test_close_when_no_transports_materialized(self):
        client = LoggingClient(api_key="sk_test", base_domain="example.test")
        # _client starts None on a fresh transport; close() must be a no-op.
        assert client._logging_http._client is None
        client.close()  # should not raise

    def test_context_manager(self):
        with LoggingClient(api_key="sk_test", base_domain="example.test") as client:
            assert isinstance(client, LoggingClient)

    def test_loggers_flush_sync_alias(self):
        client = LoggingClient(api_key="sk_test", base_domain="example.test")
        with patch.object(client.loggers, "flush") as mock_flush:
            client.loggers.flush_sync()
        mock_flush.assert_called_once()
        client.close()


class TestWiredCloseNoOp:
    def test_wired_close_leaves_borrowed_transport(self):
        from smplkit import SmplClient

        client = SmplClient(api_key="sk_test", base_domain="example.test")
        sentinel = MagicMock()
        client.logging._logging_http._client = sentinel
        client.logging._close()  # wired: owns neither transport nor ws
        assert client.logging._logging_http._client is sentinel
        client.close()


# ---------------------------------------------------------------------------
# Async standalone
# ---------------------------------------------------------------------------


class TestStandaloneAsyncConstruction:
    def test_builds_own_transports(self):
        client = AsyncLoggingClient(api_key="sk_test", base_domain="example.test", environment="prod")
        assert client._owns_transport is True
        assert client._parent is None
        assert client._environment == "prod"
        assert client._app_base_url == "https://app.example.test"
        assert client.loggers._buffer is client._buffer
        asyncio.run(client.aclose())

    def test_base_url_override_used_directly(self):
        client = AsyncLoggingClient(api_key="sk_test", base_url="http://logging.localhost", base_domain="example.test")
        assert client._logging_base_url == "http://logging.localhost"
        asyncio.run(client.aclose())

    def test_standalone_api_key_resolved_from_token(self, monkeypatch):
        monkeypatch.setenv("SMPLKIT_API_KEY", "sk_ambient")
        client = AsyncLoggingClient(base_url="http://logging.localhost", base_domain="example.test")
        assert client._standalone_api_key is not None
        asyncio.run(client.aclose())

    def test_install_opens_own_ws(self):
        async def _run():
            client = AsyncLoggingClient(api_key="sk_test", base_domain="example.test")
            fake_ws = MagicMock()
            with (
                patch("smplkit.logging.clients.SharedWebSocket", return_value=fake_ws) as ws_cls,
                patch("smplkit.logging.clients._auto_load_adapters", return_value=[]),
                patch.object(client, "_flush_bulk_async", new_callable=AsyncMock),
                patch.object(client, "_fetch_and_apply", new_callable=AsyncMock),
            ):
                await client.install()
            ws_cls.assert_called_once()
            assert client._owns_ws is True
            assert client._connected is True
            await client.aclose()
            fake_ws.stop.assert_called_once()

        asyncio.run(_run())

    def test_aclose_tears_down_owned_async_transports(self):
        async def _run():
            client = AsyncLoggingClient(api_key="sk_test", base_domain="example.test")
            logging_ac = AsyncMock()
            logging_ac.aclose = AsyncMock()
            app_ac = AsyncMock()
            app_ac.aclose = AsyncMock()
            client._logging_http._async_client = logging_ac
            client._app_http_standalone._async_client = app_ac
            await client.aclose()
            logging_ac.aclose.assert_awaited_once()
            app_ac.aclose.assert_awaited_once()
            assert client._logging_http._async_client is None
            assert client._app_http_standalone._async_client is None

        asyncio.run(_run())

    def test_aclose_also_tears_down_owned_sync_clients(self):
        """aclose() first runs _close(), which tears down any owned sync clients."""

        async def _run():
            client = AsyncLoggingClient(api_key="sk_test", base_domain="example.test")
            logging_sync = MagicMock()
            app_sync = MagicMock()
            client._logging_http._client = logging_sync
            client._app_http_standalone._client = app_sync
            await client.aclose()
            logging_sync.close.assert_called_once()
            app_sync.close.assert_called_once()
            assert client._logging_http._client is None
            assert client._app_http_standalone._client is None

        asyncio.run(_run())

    def test_aclose_when_no_async_transports_materialized(self):
        async def _run():
            client = AsyncLoggingClient(api_key="sk_test", base_domain="example.test")
            assert client._logging_http._async_client is None
            await client.aclose()  # should not raise

        asyncio.run(_run())

    def test_async_context_manager(self):
        async def _run():
            async with AsyncLoggingClient(api_key="sk_test", base_domain="example.test") as client:
                assert isinstance(client, AsyncLoggingClient)

        asyncio.run(_run())


class TestAsyncWiredCloseNoOp:
    def test_wired_close_leaves_borrowed_transport(self):
        from smplkit import AsyncSmplClient

        client = AsyncSmplClient(api_key="sk_test", base_domain="example.test")
        sentinel = MagicMock()
        client.logging._logging_http._client = sentinel
        client.logging._close()  # wired: owns neither transport nor ws
        assert client.logging._logging_http._client is sentinel
        asyncio.run(client.close())
