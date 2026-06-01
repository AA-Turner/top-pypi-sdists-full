"""Tests for SharedWebSocket — the shared event gateway connection."""

import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import websockets
import websockets.frames

from smplkit._ws import SharedWebSocket, _BACKOFF_SCHEDULE


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_ws(*, app_base_url="https://app.smplkit.com", api_key="sk_test"):
    return SharedWebSocket(app_base_url=app_base_url, api_key=api_key)


# ===================================================================
# 1. URL construction
# ===================================================================


class TestBuildWsUrl:
    def test_https_to_wss(self):
        ws = _make_ws(app_base_url="https://app.smplkit.com", api_key="sk_key")
        url = ws._build_ws_url()
        assert url == "wss://app.smplkit.com/api/ws/v1/events?api_key=sk_key"

    def test_http_to_ws(self):
        ws = _make_ws(app_base_url="http://localhost:8080", api_key="sk_dev")
        url = ws._build_ws_url()
        assert url == "ws://localhost:8080/api/ws/v1/events?api_key=sk_dev"

    def test_trailing_slash_stripped(self):
        ws = _make_ws(app_base_url="https://app.smplkit.com/", api_key="sk_test")
        url = ws._build_ws_url()
        assert url == "wss://app.smplkit.com/api/ws/v1/events?api_key=sk_test"

    def test_bare_url_gets_wss_prefix(self):
        ws = _make_ws(app_base_url="app.smplkit.com", api_key="sk_bare")
        url = ws._build_ws_url()
        assert url == "wss://app.smplkit.com/api/ws/v1/events?api_key=sk_bare"


# ===================================================================
# 2. Listener registration and dispatch
# ===================================================================


class TestListenerRegistration:
    def test_on_registers_listener(self):
        ws = _make_ws()
        cb = MagicMock()
        ws.on("config_changed", cb)

        ws._dispatch("config_changed", {"config_id": "abc"})
        cb.assert_called_once_with({"config_id": "abc"})

    def test_multiple_listeners_for_same_event(self):
        ws = _make_ws()
        cb1 = MagicMock()
        cb2 = MagicMock()
        ws.on("config_changed", cb1)
        ws.on("config_changed", cb2)

        ws._dispatch("config_changed", {"config_id": "abc"})
        cb1.assert_called_once()
        cb2.assert_called_once()

    def test_different_events_dispatch_independently(self):
        ws = _make_ws()
        config_cb = MagicMock()
        flag_cb = MagicMock()
        ws.on("config_changed", config_cb)
        ws.on("flag_changed", flag_cb)

        ws._dispatch("config_changed", {"config_id": "abc"})
        config_cb.assert_called_once()
        flag_cb.assert_not_called()

        ws._dispatch("flag_changed", {"id": "my-flag"})
        flag_cb.assert_called_once()

    def test_off_removes_listener(self):
        ws = _make_ws()
        cb = MagicMock()
        ws.on("config_changed", cb)
        ws.off("config_changed", cb)

        ws._dispatch("config_changed", {"config_id": "abc"})
        cb.assert_not_called()

    def test_off_nonexistent_listener_is_noop(self):
        ws = _make_ws()
        cb = MagicMock()
        ws.off("config_changed", cb)  # Should not raise

    def test_listener_exception_is_caught(self):
        ws = _make_ws()
        bad_cb = MagicMock(side_effect=ValueError("boom"))
        good_cb = MagicMock()
        ws.on("config_changed", bad_cb)
        ws.on("config_changed", good_cb)

        ws._dispatch("config_changed", {"config_id": "abc"})
        bad_cb.assert_called_once()
        good_cb.assert_called_once()


# ===================================================================
# 3. Connection status
# ===================================================================


class TestConnectionStatus:
    def test_initial_status(self):
        ws = _make_ws()
        assert ws.connection_status == "disconnected"


# ===================================================================
# 4. Backoff schedule
# ===================================================================


class TestBackoffSchedule:
    def test_schedule_values(self):
        assert _BACKOFF_SCHEDULE == [1, 2, 4, 8, 16, 32, 60]


# ===================================================================
# 5. Connect flow
# ===================================================================


class TestConnect:
    def test_connect_waits_for_connected_message(self):
        """_connect opens WS and waits for connected confirmation."""
        ws = _make_ws()

        mock_ws_conn = AsyncMock()
        connected_msg = json.dumps({"type": "connected"})
        mock_ws_conn.recv = AsyncMock(return_value=connected_msg)
        mock_ws_conn.send = AsyncMock()
        mock_ws_conn.close = AsyncMock()

        async def _run():
            with patch(
                "smplkit._ws.websockets.asyncio.client.connect", new_callable=AsyncMock, return_value=mock_ws_conn
            ):
                ws._closed = True  # Exit receive loop immediately
                await ws._connect()

        asyncio.run(_run())
        assert ws._connection_status == "connected"
        # No subscribe message should be sent
        mock_ws_conn.send.assert_not_called()

    def test_connect_error_response_raises(self):
        """_connect raises on error response."""
        ws = _make_ws()

        mock_ws_conn = AsyncMock()
        error_msg = json.dumps({"type": "error", "message": "Invalid API key"})
        mock_ws_conn.recv = AsyncMock(return_value=error_msg)

        async def _run():
            with patch(
                "smplkit._ws.websockets.asyncio.client.connect", new_callable=AsyncMock, return_value=mock_ws_conn
            ):
                with pytest.raises(RuntimeError, match="Connection error"):
                    await ws._connect()

        asyncio.run(_run())


# ===================================================================
# 6. Receive loop
# ===================================================================


class TestReceiveLoop:
    def test_dispatches_events(self):
        """Receive loop dispatches events based on the 'event' field."""
        ws = _make_ws()
        events_received = []
        ws.on("config_changed", lambda data: events_received.append(data))

        mock_ws_conn = AsyncMock()
        msg = json.dumps({"event": "config_changed", "config_id": "abc"})

        call_count = 0

        async def recv_side_effect():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return msg
            ws._closed = True
            raise websockets.ConnectionClosed(None, None)

        mock_ws_conn.recv = recv_side_effect
        ws._ws = mock_ws_conn

        asyncio.run(ws._receive_loop())
        assert len(events_received) == 1
        assert events_received[0]["config_id"] == "abc"

    def test_heartbeat_pong_response(self):
        """Receive loop responds to text 'ping' with 'pong'."""
        ws = _make_ws()

        mock_ws_conn = AsyncMock()
        mock_ws_conn.send = AsyncMock()

        call_count = 0

        async def recv_side_effect():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return "ping"
            ws._closed = True
            raise websockets.ConnectionClosed(None, None)

        mock_ws_conn.recv = recv_side_effect
        ws._ws = mock_ws_conn

        asyncio.run(ws._receive_loop())
        mock_ws_conn.send.assert_called_once_with("pong")

    def test_connection_closed_when_not_closed_triggers_reconnect(self):
        """ConnectionClosed triggers reconnect when not intentionally closed."""
        ws = _make_ws()

        mock_ws_conn = AsyncMock()
        exc = websockets.ConnectionClosed(websockets.frames.Close(1006, "abnormal"), None)
        mock_ws_conn.recv = AsyncMock(side_effect=exc)
        ws._ws = mock_ws_conn

        async def _run():
            with patch.object(ws, "_reconnect", new_callable=AsyncMock) as mock_reconnect:
                await ws._receive_loop()
                mock_reconnect.assert_called_once()

        asyncio.run(_run())
        assert ws._connection_status == "reconnecting"

    def test_connection_closed_when_closed_exits(self):
        """ConnectionClosed when _closed=True exits cleanly without reconnect."""
        ws = _make_ws()
        ws._closed = True

        mock_ws_conn = AsyncMock()
        mock_ws_conn.recv = AsyncMock(side_effect=websockets.ConnectionClosed(None, None))
        ws._ws = mock_ws_conn

        asyncio.run(ws._receive_loop())

    def test_unexpected_error_triggers_reconnect(self):
        """Unexpected error in receive loop triggers reconnect."""
        ws = _make_ws()

        mock_ws_conn = AsyncMock()
        mock_ws_conn.recv = AsyncMock(side_effect=RuntimeError("unexpected"))
        ws._ws = mock_ws_conn

        async def _run():
            with patch.object(ws, "_reconnect", new_callable=AsyncMock) as mock_reconnect:
                await ws._receive_loop()
                mock_reconnect.assert_called_once()

        asyncio.run(_run())
        assert ws._connection_status == "reconnecting"

    def test_unexpected_error_when_closed_exits(self):
        """Unexpected error when _closed=True exits without reconnect."""
        ws = _make_ws()

        mock_ws_conn = AsyncMock()

        async def recv_sets_closed():
            ws._closed = True
            raise RuntimeError("unexpected")

        mock_ws_conn.recv = recv_sets_closed
        ws._ws = mock_ws_conn

        with patch.object(ws, "_reconnect", new_callable=AsyncMock) as mock_reconnect:
            asyncio.run(ws._receive_loop())
            mock_reconnect.assert_not_called()


# ===================================================================
# 7. Reconnection
# ===================================================================


class TestReconnect:
    def test_respects_closed_flag(self):
        ws = _make_ws()
        ws._closed = True
        asyncio.run(ws._reconnect())

    def test_succeeds_after_retry(self):
        ws = _make_ws()
        attempt = 0

        async def connect_side_effect():
            nonlocal attempt
            attempt += 1
            if attempt < 2:
                raise OSError("Connection refused")

        async def _run():
            with patch.object(ws, "_connect", new_callable=AsyncMock, side_effect=connect_side_effect):
                with patch("smplkit._ws._BACKOFF_SCHEDULE", [0.01, 0.01]):
                    await ws._reconnect()

        asyncio.run(_run())
        assert attempt >= 2

    def test_exits_when_closed_during_sleep(self):
        ws = _make_ws()

        original_sleep = asyncio.sleep

        async def close_during_sleep(delay):
            ws._closed = True
            await original_sleep(0)

        async def _run():
            with patch.object(ws, "_connect", new_callable=AsyncMock, side_effect=OSError("refused")):
                with patch("smplkit._ws._BACKOFF_SCHEDULE", [0.01]):
                    with patch("asyncio.sleep", side_effect=close_during_sleep):
                        await ws._reconnect()

        asyncio.run(_run())
        assert ws._closed is True


# ===================================================================
# 8. Thread entry
# ===================================================================


class TestWsThreadEntry:
    def test_creates_event_loop(self):
        ws = _make_ws()
        ws._closed = True

        with patch.object(ws, "_ws_main", new_callable=AsyncMock):
            ws._ws_thread_entry()

        assert ws._ws_loop is not None
        assert ws._ws_loop.is_closed()

    def test_exception_in_ws_main_is_caught(self):
        ws = _make_ws()

        async def boom():
            raise RuntimeError("boom")

        with patch.object(ws, "_ws_main", side_effect=boom):
            ws._ws_thread_entry()

        assert ws._ws_loop is not None
        assert ws._ws_loop.is_closed()


# ===================================================================
# 9. Lifecycle (start / stop)
# ===================================================================


class TestLifecycle:
    def test_start_creates_daemon_thread(self):
        ws = _make_ws()

        with patch.object(ws, "_ws_thread_entry"):
            ws.start()

        assert ws._ws_thread is not None
        assert ws._ws_thread.daemon is True
        assert ws._ws_thread.name == "smplkit-shared-ws"

    def test_stop_sets_closed(self):
        ws = _make_ws()
        ws.stop()
        assert ws._closed is True
        assert ws.connection_status == "disconnected"

    def test_stop_joins_thread(self):
        ws = _make_ws()
        mock_thread = MagicMock()
        mock_thread.is_alive.return_value = True
        ws._ws_thread = mock_thread

        ws.stop()
        mock_thread.join.assert_called_once_with(timeout=2.0)

    def test_stop_closes_ws_connection(self):
        ws = _make_ws()
        mock_ws_conn = AsyncMock()
        loop = asyncio.new_event_loop()
        import threading

        thread = threading.Thread(target=loop.run_forever, daemon=True)
        thread.start()
        ws._ws = mock_ws_conn
        ws._ws_loop = loop

        ws.stop()
        # Give the coroutine time to execute on the loop
        import time

        time.sleep(0.1)
        loop.call_soon_threadsafe(loop.stop)
        thread.join(timeout=2)
        loop.close()
        mock_ws_conn.close.assert_awaited_once()

    def test_stop_ws_close_exception_swallowed(self):
        ws = _make_ws()
        mock_ws_conn = AsyncMock()
        mock_ws_conn.close.side_effect = RuntimeError("close failed")
        loop = asyncio.new_event_loop()
        import threading

        thread = threading.Thread(target=loop.run_forever, daemon=True)
        thread.start()
        ws._ws = mock_ws_conn
        ws._ws_loop = loop

        ws.stop()  # Should not raise
        import time

        time.sleep(0.1)
        loop.call_soon_threadsafe(loop.stop)
        thread.join(timeout=2)
        loop.close()


# ===================================================================
# 9b. _ws_main / _ws_thread_entry edge cases
# ===================================================================


class TestWsMain:
    def test_ws_main_connect_succeeds(self):
        ws = _make_ws()

        async def _run():
            with patch.object(ws, "_connect", new_callable=AsyncMock) as mock_connect:
                await ws._ws_main()
                mock_connect.assert_awaited_once()

        asyncio.run(_run())

    def test_ws_main_connect_fails_triggers_reconnect(self):
        ws = _make_ws()

        async def _run():
            with (
                patch.object(ws, "_connect", new_callable=AsyncMock, side_effect=RuntimeError("fail")),
                patch.object(ws, "_reconnect", new_callable=AsyncMock) as mock_reconnect,
            ):
                await ws._ws_main()
                mock_reconnect.assert_awaited_once()

        asyncio.run(_run())


class TestWsThreadEntryPendingTasks:
    def test_cancels_pending_tasks(self):
        ws = _make_ws()

        async def _main_with_pending():
            async def _lingering():
                await asyncio.sleep(999)

            asyncio.ensure_future(_lingering())
            # Return immediately — the lingering task stays pending
            return

        with patch.object(ws, "_ws_main", side_effect=_main_with_pending):
            ws._ws_thread_entry()

        assert ws._ws_loop is not None
        assert ws._ws_loop.is_closed()


# ===================================================================
# 10. Multi-product event routing
# ===================================================================


class TestMultiProductRouting:
    def test_config_and_flags_receive_their_own_events(self):
        """Config and flags listeners receive only their own events."""
        ws = _make_ws()

        config_events = []
        flag_events = []

        ws.on("config_changed", lambda data: config_events.append(data))
        ws.on("flag_changed", lambda data: flag_events.append(data))

        ws._dispatch("config_changed", {"config_id": "cfg-001"})
        ws._dispatch("flag_changed", {"id": "my-flag"})

        assert len(config_events) == 1
        assert config_events[0]["config_id"] == "cfg-001"
        assert len(flag_events) == 1
        assert flag_events[0]["id"] == "my-flag"

    def test_multiple_config_listeners(self):
        """Multiple config runtimes can listen for config_changed."""
        ws = _make_ws()

        rt1_events = []
        rt2_events = []

        ws.on("config_changed", lambda data: rt1_events.append(data))
        ws.on("config_changed", lambda data: rt2_events.append(data))

        ws._dispatch("config_changed", {"config_id": "cfg-001"})

        assert len(rt1_events) == 1
        assert len(rt2_events) == 1


# ===================================================================
# 11. Lazy initialization from client
# ===================================================================


class TestLazyInit:
    def test_ws_manager_none_until_ensure_ws(self):
        from smplkit.client import SmplClient

        client = SmplClient(api_key="sk_test", environment="test")
        assert client._ws_manager is None

    def test_ensure_ws_creates_and_starts(self):
        from smplkit.client import SmplClient

        client = SmplClient(api_key="sk_test", environment="test")
        with patch.object(SharedWebSocket, "start"):
            ws = client._ensure_ws()
            assert ws is not None
            assert client._ws_manager is ws
            ws.start.assert_called_once()

    def test_ensure_ws_reuses_existing(self):
        from smplkit.client import SmplClient

        client = SmplClient(api_key="sk_test", environment="test")
        with patch.object(SharedWebSocket, "start"):
            ws1 = client._ensure_ws()
            ws2 = client._ensure_ws()
            assert ws1 is ws2

    def test_close_stops_ws_manager(self):
        from smplkit.client import SmplClient

        client = SmplClient(api_key="sk_test", environment="test")
        with patch.object(SharedWebSocket, "start"):
            ws = client._ensure_ws()
        with patch.object(ws, "stop"):
            client.close()
            ws.stop.assert_called_once()
        assert client._ws_manager is None

    def test_close_without_ws_is_fine(self):
        from smplkit.client import SmplClient

        client = SmplClient(api_key="sk_test", environment="test")
        client.close()  # Should not raise


# ===================================================================
# 12. No subscribe message
# ===================================================================


class TestNoSubscribe:
    def test_no_subscribe_message_sent(self):
        """The shared WS protocol does not send any subscribe message."""
        ws = _make_ws()

        mock_ws_conn = AsyncMock()
        connected_msg = json.dumps({"type": "connected"})
        mock_ws_conn.recv = AsyncMock(return_value=connected_msg)
        mock_ws_conn.send = AsyncMock()
        mock_ws_conn.close = AsyncMock()

        async def _run():
            with patch(
                "smplkit._ws.websockets.asyncio.client.connect", new_callable=AsyncMock, return_value=mock_ws_conn
            ):
                ws._closed = True
                await ws._connect()

        asyncio.run(_run())
        # No subscribe or any other message should be sent
        mock_ws_conn.send.assert_not_called()


# ===================================================================
# Metrics instrumentation
# ===================================================================


class TestWebSocketMetrics:
    def test_connect_records_gauge(self):
        """_connect records platform.websocket_connections=1 on success."""
        metrics = MagicMock()
        ws = SharedWebSocket(app_base_url="https://app.smplkit.com", api_key="sk_test", metrics=metrics)

        mock_ws_conn = AsyncMock()
        connected_msg = json.dumps({"type": "connected"})
        mock_ws_conn.recv = AsyncMock(return_value=connected_msg)

        async def _run():
            with patch(
                "smplkit._ws.websockets.asyncio.client.connect", new_callable=AsyncMock, return_value=mock_ws_conn
            ):
                ws._closed = True
                await ws._connect()

        asyncio.run(_run())
        metrics.record_gauge.assert_called_once_with("platform.websocket_connections", 1, unit="connections")

    def test_connection_closed_records_gauge_zero(self):
        """ConnectionClosed records platform.websocket_connections=0."""
        metrics = MagicMock()
        ws = SharedWebSocket(app_base_url="https://app.smplkit.com", api_key="sk_test", metrics=metrics)

        mock_ws_conn = AsyncMock()
        exc = websockets.ConnectionClosed(websockets.frames.Close(1006, "abnormal"), None)
        mock_ws_conn.recv = AsyncMock(side_effect=exc)
        ws._ws = mock_ws_conn

        async def _run():
            with patch.object(ws, "_reconnect", new_callable=AsyncMock):
                await ws._receive_loop()

        asyncio.run(_run())
        metrics.record_gauge.assert_called_with("platform.websocket_connections", 0, unit="connections")

    def test_unexpected_error_records_gauge_zero(self):
        """Unexpected error records platform.websocket_connections=0."""
        metrics = MagicMock()
        ws = SharedWebSocket(app_base_url="https://app.smplkit.com", api_key="sk_test", metrics=metrics)

        mock_ws_conn = AsyncMock()
        mock_ws_conn.recv = AsyncMock(side_effect=RuntimeError("unexpected"))
        ws._ws = mock_ws_conn

        async def _run():
            with patch.object(ws, "_reconnect", new_callable=AsyncMock):
                await ws._receive_loop()

        asyncio.run(_run())
        metrics.record_gauge.assert_called_with("platform.websocket_connections", 0, unit="connections")


# ===================================================================
# 5. Dispatch: unmatched event debug
# ===================================================================


class TestDispatchUnmatchedEvent:
    def test_unmatched_event_does_not_call_any_callback(self):
        """Dispatching an unknown event silently no-ops (no registered handlers)."""
        ws = _make_ws()
        cb = MagicMock()
        ws.on("flag_changed", cb)

        ws._dispatch("logger_updated", {"id": "abc"})  # not registered
        cb.assert_not_called()

    def test_matched_event_calls_callback(self):
        """Dispatching a known event calls the registered callback."""
        ws = _make_ws()
        cb = MagicMock()
        ws.on("logger_changed", cb)

        ws._dispatch("logger_changed", {"id": "abc"})
        cb.assert_called_once_with({"id": "abc"})
