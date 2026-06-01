"""Basic tests for SDK client initialization."""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from smplkit import AsyncSmplClient, SmplClient
from smplkit._ws import SharedWebSocket


def test_smpl_client_init():
    client = SmplClient(api_key="sk_api_test", environment="test")
    assert client._api_key == "sk_api_test"


def test_smpl_client_has_config():
    client = SmplClient(api_key="sk_api_test", environment="test")
    assert hasattr(client, "config")


def test_async_smpl_client_init():
    client = AsyncSmplClient(api_key="sk_api_test", environment="test")
    assert client._api_key == "sk_api_test"


def test_async_smpl_client_has_config():
    client = AsyncSmplClient(api_key="sk_api_test", environment="test")
    assert hasattr(client, "config")


def test_smpl_client_default_import():
    """Verify the public import path works."""
    from smplkit import SmplClient as Client

    assert Client is not None


def test_async_smpl_client_default_import():
    """Verify the public import path works."""
    from smplkit import AsyncSmplClient as Client

    assert Client is not None


def test_smpl_client_context_manager():
    with SmplClient(api_key="sk_api_test", environment="test") as client:
        assert client._api_key == "sk_api_test"


def test_smpl_client_close():
    client = SmplClient(api_key="sk_api_test", environment="test")
    client.close()  # Should not raise


def test_async_smpl_client_context_manager():
    async def _run():
        async with AsyncSmplClient(api_key="sk_api_test", environment="test") as client:
            assert client._api_key == "sk_api_test"

    asyncio.run(_run())


def test_async_smpl_client_close():
    async def _run():
        client = AsyncSmplClient(api_key="sk_api_test", environment="test")
        await client.close()

    asyncio.run(_run())


def test_smpl_client_close_with_existing_client():
    """Exercise close() when an httpx.Client has been created."""
    client = SmplClient(api_key="sk_api_test", environment="test")
    # Force the lazy client to be created by accessing it
    http_client = client._http_client.get_httpx_client()
    assert http_client is not None
    client.close()
    assert client._http_client._client is None


def test_smpl_client_close_idempotent():
    """Closing twice should not raise."""
    client = SmplClient(api_key="sk_api_test", environment="test")
    client.close()
    client.close()


def test_async_smpl_client_close_with_existing_client():
    """Exercise async close() when an httpx.AsyncClient has been created."""

    async def _run():
        client = AsyncSmplClient(api_key="sk_api_test", environment="test")
        # Force the lazy async client to be created
        http_client = client._http_client.get_async_httpx_client()
        assert http_client is not None
        await client.close()
        assert client._http_client._async_client is None

    asyncio.run(_run())


def test_async_ensure_ws_creates_and_starts():
    client = AsyncSmplClient(api_key="sk_api_test", environment="test")
    with patch.object(SharedWebSocket, "start"):
        ws = client._ensure_ws()
        assert ws is not None
        assert client._ws_manager is ws
        ws.start.assert_called_once()


def test_async_ensure_ws_reuses_existing():
    client = AsyncSmplClient(api_key="sk_api_test", environment="test")
    with patch.object(SharedWebSocket, "start"):
        ws1 = client._ensure_ws()
        ws2 = client._ensure_ws()
        assert ws1 is ws2


def test_async_close_stops_ws_manager():
    async def _run():
        client = AsyncSmplClient(api_key="sk_api_test", environment="test")
        with patch.object(SharedWebSocket, "start"):
            ws = client._ensure_ws()
        with patch.object(ws, "stop"):
            await client.close()
            ws.stop.assert_called_once()
        assert client._ws_manager is None

    asyncio.run(_run())


def test_smpl_client_no_connect_method():
    """connect() has been removed from SmplClient."""
    client = SmplClient(api_key="sk_api_test", environment="test")
    assert not hasattr(client, "connect")


def test_wait_until_ready_returns_when_connected():
    client = SmplClient(api_key="sk_api_test", environment="test")
    with (
        patch.object(SharedWebSocket, "start"),
        patch.object(client.flags, "start"),
        patch.object(client.config, "start"),
    ):
        ws = client._ensure_ws()
        ws._connection_status = "connected"
        client.wait_until_ready(timeout=1.0)
        client.flags.start.assert_called_once()
        client.config.start.assert_called_once()


def test_wait_until_ready_raises_on_timeout():
    import pytest as _pytest

    from smplkit import TimeoutError as SmplTimeoutError

    client = SmplClient(api_key="sk_api_test", environment="test")
    with (
        patch.object(SharedWebSocket, "start"),
        patch.object(client.flags, "start"),
        patch.object(client.config, "start"),
    ):
        ws = client._ensure_ws()
        ws._connection_status = "disconnected"
        with _pytest.raises(SmplTimeoutError, match="websocket did not connect"):
            client.wait_until_ready(timeout=0.1)


def test_async_wait_until_ready_returns_when_connected():
    async def _run():
        client = AsyncSmplClient(api_key="sk_api_test", environment="test")
        with (
            patch.object(SharedWebSocket, "start"),
            patch.object(client.flags, "start", new=AsyncMock()),
            patch.object(client.config, "start", new=AsyncMock()),
        ):
            ws = client._ensure_ws()
            ws._connection_status = "connected"
            await client.wait_until_ready(timeout=1.0)
            client.flags.start.assert_awaited_once()
            client.config.start.assert_awaited_once()

    asyncio.run(_run())


def test_async_wait_until_ready_raises_on_timeout():
    import pytest as _pytest

    from smplkit import TimeoutError as SmplTimeoutError

    async def _run():
        client = AsyncSmplClient(api_key="sk_api_test", environment="test")
        with (
            patch.object(SharedWebSocket, "start"),
            patch.object(client.flags, "start", new=AsyncMock()),
            patch.object(client.config, "start", new=AsyncMock()),
        ):
            ws = client._ensure_ws()
            ws._connection_status = "disconnected"
            with _pytest.raises(SmplTimeoutError, match="websocket did not connect"):
                await client.wait_until_ready(timeout=0.1)

    asyncio.run(_run())


def test_async_smpl_client_no_connect_method():
    """connect() has been removed from AsyncSmplClient."""
    client = AsyncSmplClient(api_key="sk_api_test", environment="test")
    assert not hasattr(client, "connect")


@patch("smplkit.client.gen_bulk_register_contexts.sync_detailed")
def test_service_context_registered_on_init(mock_bulk):
    """Environment and service contexts are registered during __init__ (fire-and-forget)."""
    mock_bulk.return_value = MagicMock()

    client = SmplClient(api_key="sk_api_test", environment="test", service="my-svc")
    client._init_thread.join(timeout=2.0)

    mock_bulk.assert_called_once()
    _, kwargs = mock_bulk.call_args
    body = kwargs["body"]
    assert len(body.contexts) == 2
    assert body.contexts[0].type_ == "environment"
    assert body.contexts[0].key == "test"
    assert body.contexts[1].type_ == "service"
    assert body.contexts[1].key == "my-svc"
    assert client._api_key == "sk_api_test"


@patch("smplkit.client.gen_bulk_register_contexts.sync_detailed")
def test_service_registration_failure_on_init_is_swallowed(mock_bulk):
    """Init succeeds even if service registration fails."""
    mock_bulk.side_effect = Exception("network error")

    client = SmplClient(api_key="sk_api_test", environment="test", service="my-svc")
    client._init_thread.join(timeout=2.0)
    assert client._api_key == "sk_api_test"


@patch("smplkit.client.gen_bulk_register_contexts.sync_detailed")
def test_async_service_context_registered_on_init(mock_bulk):
    """AsyncSmplClient also registers environment and service contexts via background thread."""
    mock_bulk.return_value = MagicMock()

    client = AsyncSmplClient(api_key="sk_api_test", environment="test", service="my-svc")
    client._init_thread.join(timeout=2.0)

    mock_bulk.assert_called_once()
    _, kwargs = mock_bulk.call_args
    body = kwargs["body"]
    assert len(body.contexts) == 2
    assert body.contexts[0].type_ == "environment"
    assert body.contexts[0].key == "test"
    assert body.contexts[1].type_ == "service"
    assert body.contexts[1].key == "my-svc"
    assert client._api_key == "sk_api_test"


@patch("smplkit.client.gen_bulk_register_contexts.sync_detailed")
def test_async_service_registration_failure_on_init_is_swallowed(mock_bulk):
    """AsyncSmplClient init succeeds even if service registration fails."""
    mock_bulk.side_effect = Exception("network error")

    client = AsyncSmplClient(api_key="sk_api_test", environment="test", service="my-svc")
    client._init_thread.join(timeout=2.0)
    assert client._api_key == "sk_api_test"


@patch("smplkit.client.gen_bulk_register_contexts.asyncio_detailed")
def test_async_register_service_context_success(mock_bulk):
    """The async _register_service_context method works end to end."""
    mock_bulk.return_value = MagicMock()

    client = AsyncSmplClient(api_key="sk_api_test", environment="test", service="my-svc")
    # Wait for the sync background thread (from __init__) to finish first
    client._init_thread.join(timeout=2.0)

    asyncio.run(client._register_service_context())
    mock_bulk.assert_called_once()
    _, kwargs = mock_bulk.call_args
    body = kwargs["body"]
    assert len(body.contexts) == 2
    assert body.contexts[0].type_ == "environment"
    assert body.contexts[0].key == "test"
    assert body.contexts[1].type_ == "service"
    assert body.contexts[1].key == "my-svc"


@patch("smplkit.client.gen_bulk_register_contexts.asyncio_detailed")
def test_async_register_service_context_failure_swallowed(mock_bulk):
    """The async _register_service_context swallows exceptions."""
    mock_bulk.side_effect = Exception("network error")

    client = AsyncSmplClient(api_key="sk_api_test", environment="test", service="my-svc")
    client._init_thread.join(timeout=2.0)

    # Should not raise
    asyncio.run(client._register_service_context())


# ---------------------------------------------------------------------------
# base_domain / scheme tests
# ---------------------------------------------------------------------------


def test_smpl_client_default_urls():
    """Default URLs are production smplkit.com with https."""
    client = SmplClient(api_key="sk_api_test", environment="test")
    assert client._http_client._base_url == "https://config.smplkit.com"
    assert client._app_base_url == "https://app.smplkit.com"
    assert client.flags._flags_http._base_url == "https://flags.smplkit.com"
    assert client.manage._app_http._base_url == "https://app.smplkit.com"
    assert client.logging._logging_http._base_url == "https://logging.smplkit.com"


def test_smpl_client_custom_base_domain():
    """Custom base_domain overrides all service URLs."""
    client = SmplClient(
        api_key="sk_api_test",
        environment="test",
        base_domain="localhost",
        scheme="http",
    )
    assert client._http_client._base_url == "http://config.localhost"
    assert client._app_base_url == "http://app.localhost"
    assert client.flags._flags_http._base_url == "http://flags.localhost"
    assert client.manage._app_http._base_url == "http://app.localhost"
    assert client.logging._logging_http._base_url == "http://logging.localhost"


def test_smpl_client_custom_domain_ws_url():
    """_ensure_ws uses the computed app URL."""
    client = SmplClient(
        api_key="sk_api_test",
        environment="test",
        base_domain="localhost",
        scheme="http",
    )
    with patch.object(SharedWebSocket, "start"):
        ws = client._ensure_ws()
    assert ws._app_base_url == "http://app.localhost"


def test_async_smpl_client_default_urls():
    """AsyncSmplClient default URLs are production smplkit.com with https."""
    client = AsyncSmplClient(api_key="sk_api_test", environment="test")
    assert client._http_client._base_url == "https://config.smplkit.com"
    assert client._app_base_url == "https://app.smplkit.com"
    assert client.flags._flags_http._base_url == "https://flags.smplkit.com"
    assert client.logging._logging_http._base_url == "https://logging.smplkit.com"


def test_async_smpl_client_custom_base_domain():
    """AsyncSmplClient custom base_domain overrides all service URLs."""
    client = AsyncSmplClient(
        api_key="sk_api_test",
        environment="test",
        base_domain="localhost",
        scheme="http",
    )
    assert client._http_client._base_url == "http://config.localhost"
    assert client._app_base_url == "http://app.localhost"
    assert client.flags._flags_http._base_url == "http://flags.localhost"
    assert client.manage._app_http._base_url == "http://app.localhost"
    assert client.logging._logging_http._base_url == "http://logging.localhost"


def test_async_smpl_client_custom_domain_ws_url():
    """AsyncSmplClient _ensure_ws uses the computed app URL."""
    client = AsyncSmplClient(
        api_key="sk_api_test",
        environment="test",
        base_domain="localhost",
        scheme="http",
    )
    with patch.object(SharedWebSocket, "start"):
        ws = client._ensure_ws()
    assert ws._app_base_url == "http://app.localhost"


def test_smpl_client_debug_enables_logger():
    """debug=True sets the smplkit logger to DEBUG level."""
    import logging

    smplkit_logger = logging.getLogger("smplkit")
    original_level = smplkit_logger.level
    try:
        smplkit_logger.setLevel(logging.WARNING)  # reset to non-DEBUG
        SmplClient(api_key="sk_api_test", environment="test", debug=True)
        assert smplkit_logger.level == logging.DEBUG
    finally:
        smplkit_logger.setLevel(original_level)


def test_async_smpl_client_debug_enables_logger():
    """debug=True sets the smplkit logger to DEBUG level for AsyncSmplClient."""
    import logging

    smplkit_logger = logging.getLogger("smplkit")
    original_level = smplkit_logger.level
    try:
        smplkit_logger.setLevel(logging.WARNING)  # reset to non-DEBUG
        AsyncSmplClient(api_key="sk_api_test", environment="test", debug=True)
        assert smplkit_logger.level == logging.DEBUG
    finally:
        smplkit_logger.setLevel(original_level)


def test_async_logging_client_stores_logging_base_url():
    """AsyncLoggingClient stores logging_base_url for WS refresh thread."""
    client = AsyncSmplClient(
        api_key="sk_api_test",
        environment="test",
        base_domain="localhost",
        scheme="http",
    )
    assert client.logging._logging_base_url == "http://logging.localhost"


# ---------------------------------------------------------------------------
# set_context — per-request context management via contextvars
# ---------------------------------------------------------------------------


def test_set_context_stashes_into_contextvar():
    from smplkit import Context
    from smplkit._context import get_context

    client = SmplClient(api_key="sk_api_test", environment="test")
    client.set_context([Context("user", "u-1", plan="enterprise")])
    stashed = get_context()
    assert len(stashed) == 1
    assert stashed[0].type == "user"
    assert stashed[0].key == "u-1"


def test_set_context_with_block_reverts_on_exit():
    from smplkit import Context
    from smplkit._context import get_context

    client = SmplClient(api_key="sk_api_test", environment="test")
    client.set_context([Context("user", "outer")])
    with client.set_context([Context("user", "inner")]):
        assert get_context()[0].key == "inner"
    assert get_context()[0].key == "outer"


def test_set_context_nested_with_blocks_lifo():
    from smplkit import Context
    from smplkit._context import get_context

    client = SmplClient(api_key="sk_api_test", environment="test")
    client.set_context([Context("user", "outer")])
    with client.set_context([Context("user", "middle")]):
        with client.set_context([Context("user", "inner")]):
            assert get_context()[0].key == "inner"
        assert get_context()[0].key == "middle"
    assert get_context()[0].key == "outer"


def test_set_context_async_with_block_reverts_on_exit():
    from smplkit import Context
    from smplkit._context import get_context

    async def _run():
        client = AsyncSmplClient(api_key="sk_api_test", environment="test")
        client.set_context([Context("user", "outer")])
        async with client.set_context([Context("user", "inner")]):
            assert get_context()[0].key == "inner"
        assert get_context()[0].key == "outer"

    asyncio.run(_run())


def test_async_set_context_stashes_into_contextvar():
    from smplkit import Context
    from smplkit._context import get_context

    client = AsyncSmplClient(api_key="sk_api_test", environment="test")
    client.set_context([Context("account", "acme", region="us")])
    stashed = get_context()
    assert stashed[0].type == "account"
    assert stashed[0].key == "acme"


def test_get_context_default_is_empty():
    from smplkit._context import _request_context, get_context

    # reset to default to defend against test ordering
    _request_context.set([])
    assert get_context() == []


# ---------------------------------------------------------------------------
# set_context — eager registration
# ---------------------------------------------------------------------------


def test_set_context_eagerly_registers():
    """``set_context([...])`` queues contexts for bulk registration."""
    from smplkit import Context

    client = SmplClient(api_key="sk_api_test", environment="test")
    try:
        client.set_context([Context("user", "u-1", plan="enterprise")])
        assert client.manage.contexts._buffer.pending_count >= 1
    finally:
        client.close()


def test_set_context_empty_does_not_register():
    """Empty context list is a no-op for registration."""
    from smplkit import Context  # noqa: F401  -- ensure side-effect-free import

    client = SmplClient(api_key="sk_api_test", environment="test")
    try:
        # Service context registration runs in a daemon thread; the local
        # registration buffer is unrelated to that.  An empty set_context
        # must not push anything.
        before = client.manage.contexts._buffer.pending_count
        client.set_context([])
        after = client.manage.contexts._buffer.pending_count
        assert after == before
    finally:
        client.close()


def test_async_set_context_eagerly_registers():
    """``AsyncSmplClient.set_context([...])`` queues contexts for bulk registration."""
    from smplkit import Context

    async def _run():
        client = AsyncSmplClient(api_key="sk_api_test", environment="test")
        try:
            client.set_context([Context("account", "acme", region="us")])
            assert client.manage.contexts._buffer.pending_count >= 1
        finally:
            await client.close()

    asyncio.run(_run())


def test_async_set_context_empty_does_not_register():
    async def _run():
        client = AsyncSmplClient(api_key="sk_api_test", environment="test")
        try:
            before = client.manage.contexts._buffer.pending_count
            client.set_context([])
            after = client.manage.contexts._buffer.pending_count
            assert after == before
        finally:
            await client.close()

    asyncio.run(_run())


# ---------------------------------------------------------------------------
# Periodic flush timer — lifecycle
# ---------------------------------------------------------------------------


def test_smpl_client_init_starts_periodic_flush_timer():
    client = SmplClient(api_key="sk_api_test", environment="test")
    try:
        assert client._flush_timer is not None
        assert client._closed is False
    finally:
        client.close()


def test_smpl_client_close_cancels_timer_and_runs_final_flush():
    client = SmplClient(api_key="sk_api_test", environment="test")
    timer_before = client._flush_timer
    assert timer_before is not None
    with (
        patch.object(client.manage.contexts, "flush") as mock_ctx_flush,
        patch.object(client.manage.flags, "flush") as mock_flag_flush,
        patch.object(client.manage.loggers, "flush") as mock_log_flush,
    ):
        client.close()
    assert client._closed is True
    assert client._flush_timer is None
    mock_ctx_flush.assert_called_once()
    mock_flag_flush.assert_called_once()
    mock_log_flush.assert_called_once()


def test_async_smpl_client_init_starts_periodic_flush_timer():
    async def _run():
        client = AsyncSmplClient(api_key="sk_api_test", environment="test")
        try:
            assert client._flush_timer is not None
            assert client._closed is False
        finally:
            await client.close()

    asyncio.run(_run())


def test_async_smpl_client_close_cancels_timer_and_runs_final_flush():
    async def _run():
        client = AsyncSmplClient(api_key="sk_api_test", environment="test")
        assert client._flush_timer is not None
        with (
            patch.object(client.manage.contexts, "flush", new=AsyncMock()) as mock_ctx_flush,
            patch.object(client.manage.flags, "flush", new=AsyncMock()) as mock_flag_flush,
            patch.object(client.manage.loggers, "flush", new=AsyncMock()) as mock_log_flush,
        ):
            await client.close()
        assert client._closed is True
        assert client._flush_timer is None
        mock_ctx_flush.assert_awaited_once()
        mock_flag_flush.assert_awaited_once()
        mock_log_flush.assert_awaited_once()

    asyncio.run(_run())


def test_periodic_flush_tick_drains_buffers():
    """Firing the timer's callback drains all three buffers."""
    client = SmplClient(api_key="sk_api_test", environment="test")
    try:
        timer = client._flush_timer
        assert timer is not None
        timer.cancel()
        with (
            patch.object(client.manage.contexts, "flush") as mock_ctx_flush,
            patch.object(client.manage.flags, "flush") as mock_flag_flush,
            patch.object(client.manage.loggers, "flush") as mock_log_flush,
            patch.object(client, "_schedule_periodic_flush"),
        ):
            timer.function()
        mock_ctx_flush.assert_called_once()
        mock_flag_flush.assert_called_once()
        mock_log_flush.assert_called_once()
    finally:
        client._closed = True
        if client._flush_timer is not None:
            client._flush_timer.cancel()


def test_async_periodic_flush_tick_drains_buffers_via_sync_variants():
    """The async client's tick uses ``flush_sync`` so it can run on a thread."""

    async def _run():
        client = AsyncSmplClient(api_key="sk_api_test", environment="test")
        try:
            timer = client._flush_timer
            assert timer is not None
            timer.cancel()
            with (
                patch.object(client.manage.contexts, "flush_sync") as mock_ctx_flush,
                patch.object(client.manage.flags, "flush_sync") as mock_flag_flush,
                patch.object(client.manage.loggers, "flush_sync") as mock_log_flush,
                patch.object(client, "_schedule_periodic_flush"),
            ):
                timer.function()
            mock_ctx_flush.assert_called_once()
            mock_flag_flush.assert_called_once()
            mock_log_flush.assert_called_once()
        finally:
            client._closed = True
            if client._flush_timer is not None:
                client._flush_timer.cancel()
            await client.close()

    asyncio.run(_run())


def test_periodic_flush_tick_no_op_when_closed():
    """If the timer fires after ``close()`` set ``_closed``, the tick is a no-op."""
    client = SmplClient(api_key="sk_api_test", environment="test")
    timer = client._flush_timer
    assert timer is not None
    timer.cancel()
    client._closed = True
    with (
        patch.object(client.manage.contexts, "flush") as mock_ctx_flush,
        patch.object(client, "_schedule_periodic_flush") as mock_resched,
    ):
        timer.function()
    mock_ctx_flush.assert_not_called()
    mock_resched.assert_not_called()


def test_async_periodic_flush_tick_no_op_when_closed():
    async def _run():
        client = AsyncSmplClient(api_key="sk_api_test", environment="test")
        timer = client._flush_timer
        assert timer is not None
        timer.cancel()
        client._closed = True
        with (
            patch.object(client.manage.contexts, "flush_sync") as mock_ctx_flush,
            patch.object(client, "_schedule_periodic_flush") as mock_resched,
        ):
            timer.function()
        mock_ctx_flush.assert_not_called()
        mock_resched.assert_not_called()
        await client.close()

    asyncio.run(_run())


def test_periodic_flush_tick_swallows_flush_errors():
    """A flush exception during the tick logs a warning but doesn't raise."""
    client = SmplClient(api_key="sk_api_test", environment="test")
    timer = client._flush_timer
    assert timer is not None
    timer.cancel()
    with (
        patch.object(client.manage.contexts, "flush", side_effect=RuntimeError("boom")),
        patch.object(client, "_schedule_periodic_flush") as mock_resched,
    ):
        timer.function()
    # The loop catches and reschedules — verify reschedule still ran.
    mock_resched.assert_called_once()
    client._closed = True
    if client._flush_timer is not None:
        client._flush_timer.cancel()


def test_async_periodic_flush_tick_swallows_flush_errors():
    async def _run():
        client = AsyncSmplClient(api_key="sk_api_test", environment="test")
        timer = client._flush_timer
        assert timer is not None
        timer.cancel()
        with (
            patch.object(client.manage.contexts, "flush_sync", side_effect=RuntimeError("boom")),
            patch.object(client.manage.flags, "flush_sync"),
            patch.object(client.manage.loggers, "flush_sync"),
            patch.object(client, "_schedule_periodic_flush") as mock_resched,
        ):
            timer.function()
        mock_resched.assert_called_once()
        client._closed = True
        if client._flush_timer is not None:
            client._flush_timer.cancel()
        await client.close()

    asyncio.run(_run())


def test_final_flush_swallows_errors():
    """``_final_flush`` keeps draining each buffer even if one raises."""
    client = SmplClient(api_key="sk_api_test", environment="test")
    with (
        patch.object(client.manage.contexts, "flush", side_effect=RuntimeError("boom")),
        patch.object(client.manage.flags, "flush") as mock_flag,
        patch.object(client.manage.loggers, "flush") as mock_log,
    ):
        client._final_flush()
    mock_flag.assert_called_once()
    mock_log.assert_called_once()
    client._closed = True
    if client._flush_timer is not None:
        client._flush_timer.cancel()


def test_async_final_flush_swallows_errors():
    async def _run():
        client = AsyncSmplClient(api_key="sk_api_test", environment="test")
        with (
            patch.object(client.manage.contexts, "flush", new=AsyncMock(side_effect=RuntimeError("boom"))),
            patch.object(client.manage.flags, "flush", new=AsyncMock()) as mock_flag,
            patch.object(client.manage.loggers, "flush", new=AsyncMock()) as mock_log,
        ):
            await client._final_flush()
        mock_flag.assert_awaited_once()
        mock_log.assert_awaited_once()
        client._closed = True
        if client._flush_timer is not None:
            client._flush_timer.cancel()
        with (
            patch.object(client.manage.contexts, "flush", new=AsyncMock()),
            patch.object(client.manage.flags, "flush", new=AsyncMock()),
            patch.object(client.manage.loggers, "flush", new=AsyncMock()),
        ):
            await client.close()

    asyncio.run(_run())


# ---------------------------------------------------------------------------
# flag.get(context=[...]) eagerly registers the explicit context
# ---------------------------------------------------------------------------


def test_flag_get_with_explicit_context_registers():
    """Sync ``flag.get(context=[...])`` queues the explicit context for registration."""
    from smplkit import Context

    client = SmplClient(api_key="sk_api_test", environment="test")
    try:
        flag = client.flags.boolean_flag("dark-mode", default=False)
        client.flags._connected = True  # short-circuit lazy connect
        client.flags._flag_store = {"dark-mode": {"id": "dark-mode", "default": False, "environments": {}}}
        before = client.manage.contexts._buffer.pending_count
        flag.get(context=[Context("user", "explicit-1", plan="pro")])
        assert client.manage.contexts._buffer.pending_count > before
    finally:
        client.close()


def test_async_flag_get_with_explicit_context_registers():
    """Async ``flag.get(context=[...])`` queues the explicit context for registration."""
    from smplkit import Context

    async def _run():
        client = AsyncSmplClient(api_key="sk_api_test", environment="test")
        try:
            flag = client.flags.boolean_flag("dark-mode", default=False)
            client.flags._connected = True
            client.flags._flag_store = {"dark-mode": {"id": "dark-mode", "default": False, "environments": {}}}
            before = client.manage.contexts._buffer.pending_count
            flag.get(context=[Context("user", "explicit-async", plan="pro")])
            assert client.manage.contexts._buffer.pending_count > before
        finally:
            with (
                patch.object(client.manage.contexts, "flush", new=AsyncMock()),
                patch.object(client.manage.flags, "flush", new=AsyncMock()),
                patch.object(client.manage.loggers, "flush", new=AsyncMock()),
            ):
                await client.close()

    asyncio.run(_run())


def test_flag_get_with_set_context_does_not_double_register():
    """When ``set_context`` already registered, ``flag.get()`` reads contextvar without re-registering."""
    from smplkit import Context

    client = SmplClient(api_key="sk_api_test", environment="test")
    try:
        flag = client.flags.boolean_flag("dark-mode", default=False)
        client.flags._connected = True
        client.flags._flag_store = {"dark-mode": {"id": "dark-mode", "default": False, "environments": {}}}
        client.set_context([Context("user", "u-set", plan="free")])
        baseline = client.manage.contexts._buffer.pending_count
        flag.get()
        assert client.manage.contexts._buffer.pending_count == baseline
    finally:
        client.close()


def test_smpl_client_extra_headers_flags() -> None:
    """extra_headers are stored on FlagsClient._flags_http and applied to every request."""
    client = SmplClient(api_key="sk_api_test", environment="test", service="svc", extra_headers={"X-Test": "v"})
    try:
        assert client.flags._flags_http._headers.get("X-Test") == "v"
    finally:
        client.close()


def test_smpl_client_extra_headers_logging() -> None:
    """extra_headers are stored on LoggingClient._logging_http and applied to every request."""
    client = SmplClient(api_key="sk_api_test", environment="test", service="svc", extra_headers={"X-Test": "v"})
    try:
        assert client.logging._logging_http._headers.get("X-Test") == "v"
    finally:
        client.close()


def test_smpl_client_extra_headers_audit() -> None:
    """extra_headers are stored on AuditClient._auth and applied to every request."""
    client = SmplClient(api_key="sk_api_test", environment="test", service="svc", extra_headers={"X-Test": "v"})
    try:
        assert client.audit._auth._headers.get("X-Test") == "v"
    finally:
        client.close()


def test_smpl_client_extra_headers_config() -> None:
    """extra_headers propagate to the config HTTP transport via the management client."""
    client = SmplClient(api_key="sk_api_test", environment="test", service="svc", extra_headers={"X-Test": "v"})
    try:
        assert client._http_client._headers.get("X-Test") == "v"
    finally:
        client.close()


def test_async_smpl_client_extra_headers_audit() -> None:
    """extra_headers propagate through AsyncSmplClient to AsyncAuditClient."""

    async def _run():
        client = AsyncSmplClient(
            api_key="sk_api_test", environment="test", service="svc", extra_headers={"X-Test": "v"}
        )
        try:
            assert client.audit._inner._auth._headers.get("X-Test") == "v"
        finally:
            await client.close()

    asyncio.run(_run())
