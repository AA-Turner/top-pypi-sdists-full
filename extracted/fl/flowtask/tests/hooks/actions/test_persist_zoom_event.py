"""Tests for PersistZoomEvent and ZoomWebHook.on_shutdown (FEAT-018)."""
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from flowtask.hooks.actions.zoom_event import PersistZoomEvent
from flowtask.hooks.types.zoom import ZoomWebHook


SAMPLE_SMS_PAYLOAD = {
    "event": "phone.sms_received",
    "event_ts": 1714900000000,
    "payload": {
        "account_id": "ACC-001",
        "object": {"session_id": "sess-001", "message_id": "msg-001"},
    },
}

SAMPLE_GENERIC_PAYLOAD = {
    "event": "phone.callee_answered",
    "event_ts": 1714900001000,
    "payload": {"account_id": "ACC-001"},
}


# ── Fixtures ────────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def reset_class_pool():
    """Reset class-level pool state between tests."""
    PersistZoomEvent._pool = None
    PersistZoomEvent._pool_lock = None
    yield
    PersistZoomEvent._pool = None
    PersistZoomEvent._pool_lock = None


@pytest.fixture
def mock_pool():
    pool = MagicMock()
    pool.connect = AsyncMock()
    pool.wait_close = AsyncMock()
    mock_conn = AsyncMock()
    mock_conn.fetch_one = AsyncMock(return_value={"id": 42})
    cm = MagicMock()
    cm.__aenter__ = AsyncMock(return_value=mock_conn)
    cm.__aexit__ = AsyncMock(return_value=False)
    pool.acquire = MagicMock(return_value=cm)
    return pool, mock_conn


@pytest.fixture
def action():
    return PersistZoomEvent()


# ── open() tests ────────────────────────────────────────────────────────────────

class TestPersistZoomEventOpen:

    async def test_open_creates_pool_once(self, action, mock_pool):
        """open() called 10× concurrently creates pool exactly once."""
        pool, _ = mock_pool
        with patch("flowtask.hooks.actions.zoom_event.AsyncPool", return_value=pool):
            await asyncio.gather(*[action.open() for _ in range(10)])
        pool.connect.assert_called_once()
        assert PersistZoomEvent._pool is pool

    async def test_open_reads_pool_size(self, mock_pool):
        """open() passes self.pool_size as max_size to AsyncPool."""
        pool, _ = mock_pool
        action = PersistZoomEvent(pool_size=10)
        with patch("flowtask.hooks.actions.zoom_event.AsyncPool", return_value=pool) as MockPool:
            await action.open()
        call_kwargs = MockPool.call_args[1]
        assert call_kwargs["max_size"] == 10

    async def test_open_default_pool_size_is_5(self, action, mock_pool):
        """Default pool_size is 5."""
        pool, _ = mock_pool
        with patch("flowtask.hooks.actions.zoom_event.AsyncPool", return_value=pool) as MockPool:
            await action.open()
        call_kwargs = MockPool.call_args[1]
        assert call_kwargs["max_size"] == 5

    async def test_open_idempotent_second_call_noop(self, action, mock_pool):
        """Calling open() twice only creates pool once."""
        pool, _ = mock_pool
        with patch("flowtask.hooks.actions.zoom_event.AsyncPool", return_value=pool):
            await action.open()
            await action.open()
        pool.connect.assert_called_once()


# ── close() tests ───────────────────────────────────────────────────────────────

class TestPersistZoomEventClose:

    async def test_close_calls_wait_close_and_resets(self, action, mock_pool):
        """close() calls pool.wait_close() and resets _pool to None."""
        pool, _ = mock_pool
        PersistZoomEvent._pool = pool
        await action.close()
        pool.wait_close.assert_called_once()
        assert PersistZoomEvent._pool is None

    async def test_close_noop_when_no_pool(self, action):
        """close() is a no-op when pool is None — must not raise."""
        PersistZoomEvent._pool = None
        await action.close()


# ── run() tests ─────────────────────────────────────────────────────────────────

class TestPersistZoomEventRun:

    async def test_run_inserts_row_returns_id(self, action, mock_pool):
        """run() with valid payload returns the inserted row id."""
        pool, _ = mock_pool
        with patch("flowtask.hooks.actions.zoom_event.AsyncPool", return_value=pool):
            result = await action.run(hook=None, payload=SAMPLE_SMS_PAYLOAD)
        assert result == 42

    async def test_run_deduplication_returns_none(self, action, mock_pool):
        """run() returns None when ON CONFLICT DO NOTHING fires (no row returned)."""
        pool, mock_conn = mock_pool
        mock_conn.fetch_one.return_value = None
        with patch("flowtask.hooks.actions.zoom_event.AsyncPool", return_value=pool):
            result = await action.run(hook=None, payload=SAMPLE_SMS_PAYLOAD)
        assert result is None

    async def test_run_missing_payload_returns_none(self, action, mock_pool):
        """run() with payload=None logs warning and returns None without DB call."""
        pool, mock_conn = mock_pool
        with patch("flowtask.hooks.actions.zoom_event.AsyncPool", return_value=pool):
            result = await action.run(hook=None, payload=None)
        assert result is None
        mock_conn.fetch_one.assert_not_called()

    async def test_run_calls_open_lazily(self, action, mock_pool):
        """run() initialises pool on first call (lazy self-init)."""
        pool, _ = mock_pool
        assert PersistZoomEvent._pool is None
        with patch("flowtask.hooks.actions.zoom_event.AsyncPool", return_value=pool):
            await action.run(hook=None, payload=SAMPLE_GENERIC_PAYLOAD)
        assert PersistZoomEvent._pool is pool

    async def test_run_uses_pattern_c(self, action, mock_pool):
        """run() uses async with pool.acquire() as conn: — Pattern C, not bare await."""
        pool, _ = mock_pool
        with patch("flowtask.hooks.actions.zoom_event.AsyncPool", return_value=pool):
            await action.run(hook=None, payload=SAMPLE_SMS_PAYLOAD)
        # acquire() must be called as a CM (MagicMock, not awaited)
        pool.acquire.assert_called_once()

    async def test_run_no_json_dumps(self, action, mock_pool):
        """run() passes dict directly — no json.dumps() wrapping."""
        pool, mock_conn = mock_pool
        with patch("flowtask.hooks.actions.zoom_event.AsyncPool", return_value=pool):
            await action.run(hook=None, payload=SAMPLE_SMS_PAYLOAD, headers={})
        # The last two args to fetch_one are dicts (headers + payload)
        args = mock_conn.fetch_one.call_args[0]
        assert isinstance(args[-1], dict), "payload must be passed as dict, not string"
        assert isinstance(args[-2], dict), "headers must be passed as dict, not string"


# ── ZoomWebHook.on_shutdown tests ───────────────────────────────────────────────

class TestZoomWebHookOnShutdown:

    async def test_on_shutdown_calls_close_on_all_actions(self, mock_pool):
        """on_shutdown iterates _actions and calls close() on each."""
        pool, _ = mock_pool
        PersistZoomEvent._pool = pool

        action1 = PersistZoomEvent()
        action2 = PersistZoomEvent()

        hook = ZoomWebHook.__new__(ZoomWebHook)
        hook._actions = [action1, action2]
        hook._logger = MagicMock()
        hook.trigger_id = "test-zoom"

        await hook.on_shutdown(app=None)

        # Class-level pool — closed exactly once (not once per action)
        pool.wait_close.assert_called_once()
        assert PersistZoomEvent._pool is None

    async def test_on_shutdown_handles_close_error(self):
        """on_shutdown continues even if one action.close() raises."""
        failing_action = MagicMock()
        failing_action.close = AsyncMock(side_effect=RuntimeError("boom"))

        hook = ZoomWebHook.__new__(ZoomWebHook)
        hook._actions = [failing_action]
        hook._logger = MagicMock()
        hook.trigger_id = "test-zoom"

        await hook.on_shutdown(app=None)  # must not raise
        failing_action.close.assert_called_once()


# ── Integration test (requires live DB + navigator.zoom_events_raw) ─────────────

@pytest.mark.integration
class TestPersistZoomEventBurst:

    async def test_burst_no_interface_error(self):
        """10 concurrent run() calls produce no InterfaceError."""
        action = PersistZoomEvent()
        results = await asyncio.gather(
            *[
                action.run(
                    hook=None,
                    payload={
                        **SAMPLE_SMS_PAYLOAD,
                        "payload": {
                            "account_id": "ACC-001",
                            "object": {"session_id": f"sess-{i}", "message_id": f"msg-{i}"},
                        },
                    },
                )
                for i in range(10)
            ],
            return_exceptions=True,
        )
        for r in results:
            assert not isinstance(r, Exception), f"Unexpected error: {r}"
            assert r is None or isinstance(r, int)
        await action.close()
