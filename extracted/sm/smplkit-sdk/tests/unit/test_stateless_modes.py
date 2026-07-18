"""Stateless (serverless-ready) modes.

- ``AuditClient(buffered=False)`` / ``AsyncAuditClient(buffered=False)``:
  no event buffer, no worker thread; ``events.record`` performs one blocking
  (sync) / awaited (async) POST per call and raises typed errors on failure;
  ``flush``/``close`` are no-ops for the buffer.
- ``streaming=False`` on Config/Flags/Logging clients: the first live call
  (or ``install()``) still fetches once, but no WebSocket and no ad-hoc
  daemon threads are ever created; registration threshold flushes run
  inline; ``refresh()`` re-fetches on demand.
"""

from __future__ import annotations

import asyncio
from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from smplkit import (
    AsyncAuditClient,
    AsyncConfigClient,
    AsyncFlagsClient,
    AsyncLoggingClient,
    AuditClient,
    ConfigClient,
    FlagsClient,
    LoggingClient,
    PaymentRequiredError,
)

AUDIT_BASE = "https://audit.example.test"


def _event_resource() -> dict:
    return {
        "id": "00000000-0000-0000-0000-000000000001",
        "type": "event",
        "attributes": {
            "event_type": "invoice.created",
            "resource_type": "invoice",
            "resource_id": "inv-1",
            "occurred_at": "2026-05-06T12:00:00+00:00",
            "created_at": "2026-05-06T12:00:01+00:00",
            "actor_type": "API_KEY",
            "actor_id": None,
            "actor_label": "",
            "data": {},
            "idempotency_key": "auto",
        },
    }


# ---------------------------------------------------------------------------
# Audit: buffered=False (stateless)
# ---------------------------------------------------------------------------


class TestStatelessAuditSync:
    def _client(self, handler) -> AuditClient:
        client = AuditClient(api_key="sk_api_test", base_url=AUDIT_BASE, environment="prod", buffered=False)
        client._auth.set_httpx_client(httpx.Client(transport=httpx.MockTransport(handler), base_url=AUDIT_BASE))
        return client

    def test_no_buffer_is_created(self):
        client = AuditClient(api_key="sk_api_test", base_url=AUDIT_BASE, environment="prod", buffered=False)
        assert client.events._buffer is None
        client._close()  # buffer close is a no-op

    def test_record_performs_one_blocking_post(self):
        posts: list[str] = []

        def handler(req: httpx.Request) -> httpx.Response:
            posts.append(req.content.decode())
            return httpx.Response(201, json={"data": _event_resource()})

        client = self._client(handler)
        client.events.record("invoice.created", "invoice", "inv-1", category="billing")
        assert len(posts) == 1
        assert '"invoice.created"' in posts[0]
        # The configured environment still rides on the event body.
        assert '"environment":"prod"' in posts[0].replace(" ", "")
        client._close()

    def test_record_flush_args_ignored(self):
        posts: list[str] = []

        def handler(req: httpx.Request) -> httpx.Response:
            posts.append(req.content.decode())
            return httpx.Response(201, json={"data": _event_resource()})

        client = self._client(handler)
        # flush/flush_timeout are meaningless in stateless mode and ignored.
        client.events.record("invoice.created", "invoice", "inv-1", flush=True, flush_timeout=0.1)
        assert len(posts) == 1
        client._close()

    def test_record_sends_idempotency_key_header(self):
        headers: list[str | None] = []

        def handler(req: httpx.Request) -> httpx.Response:
            headers.append(req.headers.get("Idempotency-Key"))
            return httpx.Response(201, json={"data": _event_resource()})

        client = self._client(handler)
        client.events.record("invoice.created", "invoice", "inv-1", idempotency_key="idem-1")
        assert headers == ["idem-1"]
        client._close()

    def test_record_raises_typed_error_on_failure(self):
        def handler(req: httpx.Request) -> httpx.Response:
            return httpx.Response(402, json={"errors": [{"detail": "quota exceeded"}]})

        client = self._client(handler)
        with pytest.raises(PaymentRequiredError):
            client.events.record("invoice.created", "invoice", "inv-1")
        client._close()

    def test_flush_is_noop(self):
        client = AuditClient(api_key="sk_api_test", base_url=AUDIT_BASE, environment="prod", buffered=False)
        client.events.flush(timeout=0.1)  # must not raise, must not block
        client._close()

    def test_default_mode_still_buffers(self):
        client = AuditClient(api_key="sk_api_test", base_url=AUDIT_BASE, environment="prod")
        assert client.events._buffer is not None
        client._close()


class TestStatelessAuditAsync:
    def _client(self, handler) -> AsyncAuditClient:
        client = AsyncAuditClient(api_key="sk_api_test", base_url=AUDIT_BASE, environment="prod", buffered=False)
        client._auth.set_async_httpx_client(
            httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url=AUDIT_BASE)
        )
        return client

    def test_no_buffer_is_created(self):
        client = AsyncAuditClient(api_key="sk_api_test", base_url=AUDIT_BASE, environment="prod", buffered=False)
        assert client.events._buffer is None

    def test_record_performs_one_awaited_post(self):
        posts: list[str] = []

        def handler(req: httpx.Request) -> httpx.Response:
            posts.append(req.content.decode())
            return httpx.Response(201, json={"data": _event_resource()})

        async def _run():
            client = self._client(handler)
            # flush args are ignored in stateless mode.
            await client.events.record("invoice.created", "invoice", "inv-1", flush=True)
            await client.events.record("invoice.created", "invoice", "inv-2", idempotency_key="idem-2")
            await client.events.flush(timeout=0.1)  # no-op
            await client._close()

        asyncio.run(_run())
        assert len(posts) == 2

    def test_record_raises_typed_error_on_failure(self):
        def handler(req: httpx.Request) -> httpx.Response:
            return httpx.Response(402, json={"errors": [{"detail": "quota exceeded"}]})

        async def _run():
            client = self._client(handler)
            with pytest.raises(PaymentRequiredError):
                await client.events.record("invoice.created", "invoice", "inv-1")
            await client._close()

        asyncio.run(_run())


# ---------------------------------------------------------------------------
# Shared mock helpers for the streaming=False suites
# ---------------------------------------------------------------------------


def _ok_response(parsed=None, content: bytes = b"", status=HTTPStatus.OK):
    resp = MagicMock()
    resp.status_code = status
    resp.content = content
    resp.parsed = parsed
    return resp


# ---------------------------------------------------------------------------
# Config: streaming=False
# ---------------------------------------------------------------------------


class TestStatelessConfigSync:
    @patch("smplkit.config.clients.list_configs.sync_detailed")
    def test_first_live_call_fetches_without_websocket(self, mock_list):
        mock_list.return_value = _ok_response()
        client = ConfigClient(api_key="sk_test", base_domain="example.test", streaming=False)
        with patch("smplkit.config.clients.SharedWebSocket") as ws_cls:
            value = client.get_value("billing", "max_seats", default=50)
        assert value == 50
        assert client._connected is True
        assert client._ws_manager is None
        ws_cls.assert_not_called()
        mock_list.assert_called()
        client.close()

    @patch("smplkit.config.clients.list_configs.sync_detailed")
    def test_refresh_refetches_on_demand(self, mock_list):
        mock_list.return_value = _ok_response()
        client = ConfigClient(api_key="sk_test", base_domain="example.test", streaming=False)
        client.refresh()
        first = mock_list.call_count
        client.refresh()
        assert mock_list.call_count > first
        assert client._ws_manager is None
        client.close()

    def test_threshold_flush_runs_inline(self):
        client = ConfigClient(api_key="sk_test", base_domain="example.test", streaming=False)
        with (
            patch("smplkit.config.clients._CONFIG_BATCH_FLUSH_SIZE", 1),
            patch.object(client, "flush") as mock_flush,
            patch("smplkit.config.clients.threading") as mock_threading,
        ):
            client.register_config("billing", service=None, environment=None)
            client.register_config_item("billing", "max_seats", "NUMBER", 50)
        assert mock_flush.call_count == 2
        mock_threading.Thread.assert_not_called()
        client.close()


class TestStatelessConfigAsync:
    @patch("smplkit.config.clients.list_configs.asyncio_detailed", new_callable=AsyncMock)
    def test_first_live_call_fetches_without_websocket(self, mock_list):
        mock_list.return_value = _ok_response()

        async def _run():
            client = AsyncConfigClient(api_key="sk_test", base_domain="example.test", streaming=False)
            with patch("smplkit.config.clients.SharedWebSocket") as ws_cls:
                value = await client.get_value("billing", "max_seats", default=50)
            assert value == 50
            assert client._connected is True
            assert client._ws_manager is None
            ws_cls.assert_not_called()
            await client.close()

        asyncio.run(_run())

    def test_threshold_flush_runs_inline(self):
        client = AsyncConfigClient(api_key="sk_test", base_domain="example.test", streaming=False)
        with (
            patch("smplkit.config.clients._CONFIG_BATCH_FLUSH_SIZE", 1),
            patch.object(client, "flush_sync") as mock_flush,
            patch("smplkit.config.clients.threading") as mock_threading,
        ):
            client.register_config("billing", service=None, environment=None)
            client.register_config_item("billing", "max_seats", "NUMBER", 50)
        assert mock_flush.call_count == 2
        mock_threading.Thread.assert_not_called()


# ---------------------------------------------------------------------------
# Flags: streaming=False
# ---------------------------------------------------------------------------


class TestStatelessFlagsSync:
    @patch("smplkit.flags.clients.list_flags.sync_detailed")
    def test_evaluation_works_without_websocket(self, mock_list):
        mock_list.return_value = _ok_response(content=b'{"data": []}')
        client = FlagsClient(api_key="sk_test", base_domain="example.test", streaming=False)
        with patch("smplkit.flags.clients.SharedWebSocket") as ws_cls:
            handle = client.boolean_flag("beta", default=True)
            assert handle.get() is True
        assert client._connected is True
        assert client._ws_manager is None
        assert client._ws_subscribed is False
        ws_cls.assert_not_called()
        client.close()

    @patch("smplkit.flags.clients.list_flags.sync_detailed")
    def test_refresh_refetches_on_demand(self, mock_list):
        mock_list.return_value = _ok_response(content=b'{"data": []}')
        client = FlagsClient(api_key="sk_test", base_domain="example.test", streaming=False)
        client.refresh()
        first = mock_list.call_count
        client.refresh()
        assert mock_list.call_count > first
        assert client._ws_manager is None
        client.close()

    def test_threshold_flush_runs_inline(self):
        from smplkit.flags.types import FlagDeclaration

        client = FlagsClient(api_key="sk_test", base_domain="example.test", streaming=False)
        with (
            patch("smplkit.flags.clients._FLAG_BATCH_FLUSH_SIZE", 1),
            patch.object(client, "flush") as mock_flush,
            patch("smplkit.flags.clients.threading") as mock_threading,
        ):
            client.register(FlagDeclaration(id="beta", type="BOOLEAN", default=False))
        mock_flush.assert_called_once()
        mock_threading.Thread.assert_not_called()
        client.close()


class TestStatelessFlagsAsync:
    @patch("smplkit.flags.clients.list_flags.asyncio_detailed", new_callable=AsyncMock)
    def test_refresh_connects_without_websocket(self, mock_list):
        mock_list.return_value = _ok_response(content=b'{"data": []}')

        async def _run():
            client = AsyncFlagsClient(api_key="sk_test", base_domain="example.test", streaming=False)
            with patch("smplkit.flags.clients.SharedWebSocket") as ws_cls:
                await client.refresh()
                handle = client.boolean_flag("beta", default=True)
                assert handle.get() is True
            assert client._connected is True
            assert client._ws_manager is None
            assert client._ws_subscribed is False
            ws_cls.assert_not_called()
            await client.aclose()

        asyncio.run(_run())

    def test_threshold_flush_runs_inline(self):
        from smplkit.flags.types import FlagDeclaration

        client = AsyncFlagsClient(api_key="sk_test", base_domain="example.test", streaming=False)
        with (
            patch("smplkit.flags.clients._FLAG_BATCH_FLUSH_SIZE", 1),
            patch.object(client, "flush_sync") as mock_flush,
            patch("smplkit.flags.clients.threading") as mock_threading,
        ):
            client.register(FlagDeclaration(id="beta", type="BOOLEAN", default=False))
        mock_flush.assert_called_once()
        mock_threading.Thread.assert_not_called()


# ---------------------------------------------------------------------------
# Logging: streaming=False
# ---------------------------------------------------------------------------


class TestStatelessLoggingSync:
    @patch("smplkit.logging.clients.list_log_groups.sync_detailed")
    @patch("smplkit.logging.clients.list_loggers.sync_detailed")
    @patch("smplkit.logging.clients._auto_load_adapters")
    def test_install_fetches_and_applies_without_websocket(self, mock_adapters, mock_loggers, mock_groups):
        mock_adapters.return_value = []
        mock_loggers.return_value = _ok_response()
        mock_groups.return_value = _ok_response()
        client = LoggingClient(api_key="sk_test", base_domain="example.test", streaming=False)
        with patch("smplkit.logging.clients.SharedWebSocket") as ws_cls:
            client.install()
        assert client._connected is True
        assert client._ws_manager is None
        assert client._owns_ws is False
        ws_cls.assert_not_called()
        mock_loggers.assert_called()

        # The NotInstalledError gate stays: on_change works only after install.
        @client.on_change
        def _listener(event):  # pragma: no cover - never fired here
            pass

        # refresh() re-fetches on demand.
        first = mock_loggers.call_count
        client.refresh()
        assert mock_loggers.call_count > first
        client.close()

    def test_uninstalled_gate_still_raises(self):
        from smplkit.errors import NotInstalledError

        client = LoggingClient(api_key="sk_test", base_domain="example.test", streaming=False)
        with pytest.raises(NotInstalledError):
            client.refresh()
        client.close()

    def test_threshold_flush_runs_inline(self):
        from smplkit import LogLevel
        from smplkit.logging.sources import LoggerSource

        client = LoggingClient(api_key="sk_test", base_domain="example.test", streaming=False)
        with (
            patch("smplkit.logging.clients._LOGGER_BATCH_FLUSH_SIZE", 1),
            patch.object(client.loggers, "flush") as mock_flush,
            patch("smplkit.logging.clients.threading") as mock_threading,
        ):
            client.loggers.register(LoggerSource(name="app.db", resolved_level=LogLevel.INFO))
        mock_flush.assert_called_once()
        mock_threading.Thread.assert_not_called()
        client.close()


class TestStatelessLoggingAsync:
    @patch("smplkit.logging.clients.list_log_groups.asyncio_detailed", new_callable=AsyncMock)
    @patch("smplkit.logging.clients.list_loggers.asyncio_detailed", new_callable=AsyncMock)
    @patch("smplkit.logging.clients._auto_load_adapters")
    def test_install_fetches_and_applies_without_websocket(self, mock_adapters, mock_loggers, mock_groups):
        mock_adapters.return_value = []
        mock_loggers.return_value = _ok_response()
        mock_groups.return_value = _ok_response()

        async def _run():
            client = AsyncLoggingClient(api_key="sk_test", base_domain="example.test", streaming=False)
            with patch("smplkit.logging.clients.SharedWebSocket") as ws_cls:
                await client.install()
            assert client._connected is True
            assert client._ws_manager is None
            ws_cls.assert_not_called()
            # refresh() re-fetches on demand.
            first = mock_loggers.call_count
            await client.refresh()
            assert mock_loggers.call_count > first
            await client.aclose()

        asyncio.run(_run())

    def test_threshold_flush_runs_inline(self):
        from smplkit import LogLevel
        from smplkit.logging.sources import LoggerSource

        client = AsyncLoggingClient(api_key="sk_test", base_domain="example.test", streaming=False)
        with (
            patch("smplkit.logging.clients._LOGGER_BATCH_FLUSH_SIZE", 1),
            patch.object(client.loggers, "flush_sync") as mock_flush,
            patch("smplkit.logging.clients.threading") as mock_threading,
        ):
            client.loggers.register(LoggerSource(name="app.db", resolved_level=LogLevel.INFO))
        mock_flush.assert_called_once()
        mock_threading.Thread.assert_not_called()
