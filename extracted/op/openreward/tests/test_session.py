"""Tests for the unified _session module."""
import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp
import pytest

from openreward.api._session.http import (
    HeartbeatTimeoutError,
    MaxRetriesError,
    _parse_sse_events,
    request_retryable,
    resumable_sse,
)
from openreward.api._session.session import BaseAsyncSession, SessionTerminatedError


def _make_sse_bytes(events: list[tuple[str, str]]) -> bytes:
    """Build raw SSE byte payload from (event, data) pairs."""
    lines = []
    for event, data in events:
        lines.append(f"event: {event}")
        lines.append(f"data: {data}")
        lines.append("")  # blank line terminates event
    return "\n".join(lines).encode()


class FakeContent:
    """Simulates aiohttp response.content as an async line iterator."""

    def __init__(self, raw: bytes):
        self._lines = raw.split(b"\n")

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self._lines:
            raise StopAsyncIteration
        return self._lines.pop(0) + b"\n"


class FakeResponse:
    """Minimal fake aiohttp response for SSE tests."""

    def __init__(self, raw: bytes, status: int = 200):
        self.content = FakeContent(raw)
        self.status = status
        self.ok = status < 400
        self.headers = {}
        self.request_info = MagicMock()
        self.history = ()

    async def text(self):
        return ""

    async def json(self):
        return {}

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        pass


@pytest.mark.asyncio
async def test_parse_sse_events():
    raw = _make_sse_bytes([
        ("task_id", "abc123"),
        ("chunk", '{"partial":'),
        ("end", '"done"}'),
    ])
    resp = FakeResponse(raw)
    events = []
    async for event, data in _parse_sse_events(resp):
        events.append((event, data))
    assert events == [
        ("task_id", "abc123"),
        ("chunk", '{"partial":'),
        ("end", '"done"}'),
    ]


@pytest.mark.asyncio
async def test_resumable_sse_empty_end_data():
    """SSE with empty 'end' data should return None instead of crashing."""
    raw = _make_sse_bytes([
        ("task_id", "sid-001"),
        ("end", ""),
    ])

    call_count = 0
    def fake_post(path, **kwargs):
        nonlocal call_count
        call_count += 1
        return FakeResponse(raw)

    client = MagicMock()
    client.post = MagicMock(side_effect=fake_post)

    result = await resumable_sse(
        client, "/create_session", token="tok",
        max_retries=0, timeout=5,
    )
    assert result is None


@pytest.mark.asyncio
async def test_resumable_sse_captures_task_id_via_on_event():
    """Verify on_event callback receives task_id events."""
    raw = _make_sse_bytes([
        ("task_id", "sid-xyz"),
        ("end", '{"sid": "sid-xyz"}'),
    ])

    def fake_post(path, **kwargs):
        return FakeResponse(raw)

    client = MagicMock()
    client.post = MagicMock(side_effect=fake_post)

    captured = []
    result = await resumable_sse(
        client, "/create", token="tok",
        max_retries=0, timeout=5,
        on_event=lambda e, d: captured.append((e, d)),
    )
    assert result == {"sid": "sid-xyz"}
    assert ("task_id", "sid-xyz") in captured


@pytest.mark.asyncio
async def test_resumable_sse_retry_on_intermediary_5xx():
    """Verify retry on intermediary 5xx (502/503/504) — these typically
    come from load balancers / ingress controllers when the upstream is
    momentarily unavailable."""
    raw_ok = _make_sse_bytes([
        ("task_id", "s1"),
        ("end", '{"ok": true}'),
    ])

    for transient_status in (502, 503, 504):
        attempt = 0
        def fake_post(path, _status=transient_status, **kwargs):
            nonlocal attempt
            attempt += 1
            if attempt == 1:
                return FakeResponse(b"", status=_status)
            return FakeResponse(raw_ok)

        client = MagicMock()
        client.post = MagicMock(side_effect=fake_post)

        result = await resumable_sse(
            client, "/test", token="tok",
            max_retries=3, timeout=10, backoff_base=0.01,
        )
        assert result == {"ok": True}, f"status {transient_status} should retry"
        assert attempt == 2


@pytest.mark.asyncio
async def test_env_server_client_does_not_retry_500():
    """env-server policy: 500 means an unhandled exception in user code
    caught by ErrorHandlingMiddleware — retrying re-executes the same
    code path. Must propagate immediately."""
    from openreward.api._session.http import set_retry_policy

    def fake_post(path, **kwargs):
        return FakeResponse(b"", status=500)

    client = MagicMock()
    client.post = MagicMock(side_effect=fake_post)
    set_retry_policy(client, "env-server")

    with pytest.raises(aiohttp.ClientResponseError) as exc_info:
        await resumable_sse(
            client, "/test", token="tok",
            max_retries=5, timeout=10, backoff_base=0.01,
        )
    assert exc_info.value.status == 500


@pytest.mark.asyncio
async def test_api_client_retries_500():
    """api policy: 500 might be a transient downstream blip. Retries
    until max_retries, then raises MaxRetriesError."""
    attempts = 0
    def fake_post(path, **kwargs):
        nonlocal attempts
        attempts += 1
        return FakeResponse(b"", status=500)

    client = MagicMock()
    client.post = MagicMock(side_effect=fake_post)
    # No set_retry_policy call → defaults to "api".

    with pytest.raises(MaxRetriesError):
        await resumable_sse(
            client, "/test", token="tok",
            max_retries=2, timeout=10, backoff_base=0.01,
        )
    assert attempts >= 3  # initial + 2 retries


@pytest.mark.asyncio
async def test_resumable_sse_max_retries_exceeded():
    """Verify MaxRetriesError raised after exceeding retries."""
    def fake_post(path, **kwargs):
        return FakeResponse(b"", status=502)

    client = MagicMock()
    client.post = MagicMock(side_effect=fake_post)

    with pytest.raises(MaxRetriesError):
        await resumable_sse(
            client, "/test", token="tok",
            max_retries=2, timeout=10, backoff_base=0.01,
        )


@pytest.mark.asyncio
async def test_session_terminated_error():
    err = SessionTerminatedError("pod gone", sid="abc", kind="sandbox")
    assert err.sid == "abc"
    assert err.reason == "pod gone"
    assert err.kind == "sandbox"
    assert "abc" in str(err)
    assert "sandbox session terminated" in str(err)


@pytest.mark.asyncio
async def test_base_session_lifecycle():
    """Mock SSE creation returning SID, verify ping started and /delete called on exit."""
    raw = _make_sse_bytes([
        ("task_id", "sid-lifecycle"),
        ("end", '{"sid": "sid-lifecycle"}'),
    ])

    def fake_post(path, **kwargs):
        return FakeResponse(raw)

    client = MagicMock()
    client.post = MagicMock(side_effect=fake_post)
    client.closed = False
    client._base_url = "http://test"

    delete_calls = []

    async def mock_request(client, method, path, expect_json, token, **kw):
        if path == "/delete_session":
            delete_calls.append(kw.get("sid"))
            return None
        return None

    async def mock_run_ping(self_, **kw):
        await asyncio.sleep(1000)

    with patch("openreward.api._session.session.resumable_sse") as mock_sse, \
         patch("openreward.api._session.session.request_retryable", side_effect=mock_request), \
         patch.object(BaseAsyncSession, "_run_ping", mock_run_ping):

        async def sse_side_effect(*args, **kwargs):
            on_event = kwargs.get("on_event", lambda e, d: None)
            on_event("task_id", "sid-lifecycle")
            return {"sid": "sid-lifecycle"}
        mock_sse.side_effect = sse_side_effect

        session = BaseAsyncSession(
            base_url="http://test",
            api_key="key",
            creation_endpoint="/create_sandbox",
            creation_payload={"foo": "bar"},
            client=client,
        )
        session._session_kind = "sandbox"

        async with session:
            assert session.sid == "sid-lifecycle"
            assert session._ping_task is not None

        assert session._ping_task is None
        assert "sid-lifecycle" in delete_calls


@pytest.mark.asyncio
async def test_run_or_die_cancels_on_death():
    """Start a slow coro, mark session dead, verify SessionTerminatedError raised."""
    from openreward.api._session.ping import ErrorResponse

    async def mock_run_ping(self_, **kw):
        await asyncio.sleep(1000)

    with patch("openreward.api._session.session.resumable_sse") as mock_sse, \
         patch.object(BaseAsyncSession, "_run_ping", mock_run_ping):

        async def sse_side_effect(*args, **kwargs):
            on_event = kwargs.get("on_event", lambda e, d: None)
            on_event("task_id", "sid-die")
            return {"sid": "sid-die"}
        mock_sse.side_effect = sse_side_effect

        client = MagicMock()
        client.closed = False
        client._base_url = "http://test"

        session = BaseAsyncSession(
            base_url="http://test",
            api_key="key",
            creation_endpoint="/create",
            creation_payload={},
            client=client,
        )
        session._session_kind = "sandbox"

        with patch("openreward.api._session.session.request_retryable", new=AsyncMock(return_value=None)):
            await session.__aenter__()

        async def slow_task():
            await asyncio.sleep(100)

        # Mark dead after a short delay
        async def kill_later():
            await asyncio.sleep(0.05)
            session._mark_dead(ErrorResponse(type="error", message="pod gone"))

        asyncio.create_task(kill_later())

        with pytest.raises(SessionTerminatedError):
            await session._run_or_die(slow_task())

        with patch("openreward.api._session.session.request_retryable", new=AsyncMock(return_value=None)):
            await session.__aexit__(None, None, None)


@pytest.mark.asyncio
async def test_sandbox_inherits_base():
    """Verify AsyncSandboxesAPI uses /create endpoint and inherits from BaseAsyncSession."""
    from openreward.api.sandboxes.client import AsyncSandboxesAPI
    from openreward.api.sandboxes.types import SandboxSettings

    settings = SandboxSettings(
        environment="test",
        image="python:3.10",
        machine_size="1:1",
    )

    api = AsyncSandboxesAPI(
        base_url="http://test",
        api_key="key",
        settings=settings,
    )

    assert isinstance(api, BaseAsyncSession)
    assert api._creation_endpoint == "/create_sandbox"
    assert api._creation_payload == settings.model_dump()
    api.sid = "test-sid"
    assert api.sid == "test-sid"


# ----------------------------------------------------------------------
# _run_ping failure-tolerance tests
#
# Regression context: PR #1721 added try/except around the ping future
# that called _mark_dead on ANY exception. A single TimeoutError from
# an unreachable /ping endpoint was enough to permanently kill a session
# client-side, even though the server-side session was healthy and
# other paths (sandbox.run, /files/fetch) were still renewing TTL.
# These tests pin the new tolerance policy: only definitive
# SessionTerminatedError or N consecutive failures cause _mark_dead.
# ----------------------------------------------------------------------


def _make_session_with_ping_disabled():
    """Construct a BaseAsyncSession instance with no real network setup —
    ready to have _run_ping called directly with a mocked ping_thread."""
    client = MagicMock()
    client.closed = False
    client._base_url = "http://test"
    session = BaseAsyncSession(
        base_url="http://test",
        api_key="key",
        creation_endpoint="/create_sandbox",
        creation_payload={},
        client=client,
    )
    session._session_kind = "sandbox"
    session.sid = "test-sid"
    return session


@pytest.mark.asyncio
async def test_run_ping_tolerates_transient_failures():
    """A handful of transient ping failures (below the consecutive-fails
    threshold) must NOT mark the session dead. Reproduces the
    env-marketmaker regression: TimeoutError from an unreachable /ping
    endpoint used to kill the session immediately on the first failure.
    """
    session = _make_session_with_ping_disabled()

    # 3 transient TimeoutErrors then a successful ping. Default threshold
    # is 5 — we should NEVER hit _mark_dead in this sequence.
    fail_count = {"n": 0}

    def fake_schedule(url, sid, api_key, sleep_time, deployment):
        loop = asyncio.get_event_loop()
        future = loop.create_future()
        if fail_count["n"] < 3:
            fail_count["n"] += 1
            future.set_exception(asyncio.TimeoutError())
        else:
            # Simulate a "ping returned cleanly" — counter resets in
            # the loop and we then cancel to end the test.
            future.set_result(None)
        return asyncio.run_coroutine_threadsafe(
            _resolved(future), loop,
        ) if False else _wrap_as_concurrent_future(future)

    # asyncio.wrap_future takes a concurrent.futures.Future, so wrap.
    import concurrent.futures as cf

    def _wrap_as_concurrent_future(asyncio_future):
        cfut = cf.Future()
        if asyncio_future.done():
            if asyncio_future.exception() is not None:
                cfut.set_exception(asyncio_future.exception())
            else:
                cfut.set_result(asyncio_future.result())
        else:
            asyncio_future.add_done_callback(
                lambda f: cfut.set_exception(f.exception())
                if f.exception() else cfut.set_result(f.result())
            )
        return cfut

    async def _resolved(future):
        return await future

    with patch(
        "openreward.api._session.session.ping_thread.schedule",
        side_effect=fake_schedule,
    ), patch(
        "openreward.api._session.session.asyncio.sleep",
        new=AsyncMock(return_value=None),  # don't actually wait between retries
    ):
        # Run for a bounded time — the loop runs forever in real life,
        # so cancel after a few iterations.
        task = asyncio.create_task(session._run_ping(
            url="http://test/ping",
            sid="test-sid",
            api_key=None,
            sleep_time=0,
            deployment=None,
            max_consecutive_failures=5,
        ))
        # Let the loop iterate enough to hit the 3 failures + 1 success.
        await asyncio.sleep(0.05)
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    # The session must NOT have been marked dead. Three transient
    # failures followed by a success must reset the counter.
    assert session._dead_exception is None, (
        f"Session was marked dead despite only 3 transient failures: "
        f"{session._dead_exception}"
    )


@pytest.mark.asyncio
async def test_run_ping_marks_dead_after_threshold_consecutive_failures():
    """After max_consecutive_failures (default 5) ping failures in a row
    with no success in between, the session SHOULD be marked dead — same
    as the original behaviour, just delayed past transient blips.
    """
    session = _make_session_with_ping_disabled()

    import concurrent.futures as cf

    def fake_schedule(url, sid, api_key, sleep_time, deployment):
        cfut = cf.Future()
        cfut.set_exception(asyncio.TimeoutError("simulated /ping unreachable"))
        return cfut

    with patch(
        "openreward.api._session.session.ping_thread.schedule",
        side_effect=fake_schedule,
    ), patch(
        "openreward.api._session.session.asyncio.sleep",
        new=AsyncMock(return_value=None),
    ):
        # max_consecutive_failures=3 to keep the test fast.
        await session._run_ping(
            url="http://test/ping",
            sid="test-sid",
            api_key=None,
            sleep_time=0,
            deployment=None,
            max_consecutive_failures=3,
        )

    # After 3 consecutive failures the session must be marked dead.
    assert session._dead_exception is not None
    assert "consecutive ping failures" in str(session._dead_exception)


@pytest.mark.asyncio
async def test_run_ping_marks_dead_immediately_on_session_terminated_error():
    """A definitive server-side SessionTerminatedError signal must mark
    the session dead immediately — not wait for the consecutive-failures
    threshold. This preserves the original 'session_not_found' behaviour.
    """
    session = _make_session_with_ping_disabled()

    import concurrent.futures as cf

    def fake_schedule(url, sid, api_key, sleep_time, deployment):
        cfut = cf.Future()
        cfut.set_exception(SessionTerminatedError(
            "session_not_found", sid="test-sid", kind="sandbox",
        ))
        return cfut

    with patch(
        "openreward.api._session.session.ping_thread.schedule",
        side_effect=fake_schedule,
    ), patch(
        "openreward.api._session.session.asyncio.sleep",
        new=AsyncMock(return_value=None),
    ):
        await session._run_ping(
            url="http://test/ping",
            sid="test-sid",
            api_key=None,
            sleep_time=0,
            deployment=None,
            max_consecutive_failures=5,  # high threshold; should bypass
        )

    # Should be marked dead immediately on the first failure because it's
    # a definitive SessionTerminatedError, not a transient TimeoutError.
    assert session._dead_exception is not None


