import os

import aiohttp
import httpx
import pytest

from openreward import AsyncOpenReward
from openreward.api.sandboxes.types import (SandboxSettings)
from openreward.environments import Environment, tool, ToolOutput
from openreward.environments.server import Server
from openreward.environments.types import (Blocks, JSONObject, TextBlock)


class SandboxEnv(Environment):
    """Minimal env that starts/stops a sandbox using provided settings."""

    def __init__(self, task_spec: JSONObject, secrets: dict[str, str] = {}, settings: SandboxSettings | None = None) -> None:
        super().__init__(task_spec, secrets=secrets)
        self._client = AsyncOpenReward()
        self.sandbox = self._client.sandbox(settings)

    async def setup(self):
        await self.sandbox.start()

    async def teardown(self):
        await self.sandbox.stop()

    def get_prompt(self) -> Blocks:
        return [TextBlock(text="test")]

    @classmethod
    def list_splits(cls) -> list[str]:
        return ["train"]

    @classmethod
    def list_tasks(cls, split: str) -> list[JSONObject]:
        return [{}]

    @tool
    async def submit(self) -> ToolOutput:
        return ToolOutput(blocks=[TextBlock(text="done")], reward=1.0, finished=True)


class FailingEnv(Environment):
    """Env whose list_tasks always raises, used to trigger unhandled exceptions."""

    def get_prompt(self) -> Blocks:
        return [TextBlock(text="test")]

    @classmethod
    def list_splits(cls) -> list[str]:
        return ["train"]

    @classmethod
    def list_tasks(cls, split: str) -> list[JSONObject]:
        raise RuntimeError("something broke internally")

    @tool
    async def submit(self) -> ToolOutput:
        return ToolOutput(blocks=[TextBlock(text="done")], reward=1.0, finished=True)


def _make_server(return_errors: str) -> Server:
    """Build a Server with FailingEnv and the given return_errors mode."""
    return Server([FailingEnv], return_errors=return_errors)


async def _trigger_error(app) -> httpx.Response:
    """Hit the tasks endpoint which raises RuntimeError in FailingEnv."""
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        return await client.post("/failingenv/tasks", json={"split": "train"})

@pytest.mark.asyncio
async def test_return_errors_none():
    """With return_errors='none', 500 responses should be opaque."""
    server = _make_server("none")
    resp = await _trigger_error(server.app)

    assert resp.status_code == 500
    body = resp.json()
    assert body["detail"] == "Internal Server Error"
    assert "RuntimeError" not in body["detail"]
    assert "something broke" not in body["detail"]


@pytest.mark.asyncio
async def test_return_errors_exception():
    """With return_errors='exception', 500 responses should include the exception string."""
    server = _make_server("exception")
    resp = await _trigger_error(server.app)

    assert resp.status_code == 500
    body = resp.json()
    assert "RuntimeError" in body["detail"]
    assert "something broke internally" in body["detail"]
    # Should not contain a full traceback
    assert "Traceback" not in body["detail"]


@pytest.mark.asyncio
async def test_return_errors_stacktrace():
    """With return_errors='stacktrace', 500 responses should include the full traceback."""
    server = _make_server("stacktrace")
    resp = await _trigger_error(server.app)

    assert resp.status_code == 500
    body = resp.json()
    assert "Traceback (most recent call last)" in body["detail"]
    assert "RuntimeError: something broke internally" in body["detail"]

async def _start_stop(settings: SandboxSettings):
    env = SandboxEnv(task_spec={}, settings=settings)
    try:
        await env.setup()
    finally:
        await env.teardown()


@pytest.mark.asyncio
async def test_nonexistent_environment():
    """Sandbox referencing a nonexistent OpenReward environment should fail with a clear message."""
    with pytest.raises(aiohttp.ClientResponseError) as exc_info:
        await _start_stop(SandboxSettings(
            environment="GeneralReasoning/idontexist",
            image="python:3.11-slim",
            machine_size="1:2",
        ))
    assert exc_info.value.status == 404
    assert "idontexist" in exc_info.value.message
    assert "GeneralReasoning" in exc_info.value.message


# TODO: This currently hangs indefinitely.
# @pytest.mark.asyncio
# async def test_nonexistent_image():
#     """Sandbox referencing a nonexistent container image should fail with a clear message."""
#     with pytest.raises(RuntimeError) as exc_info:
#         await _start_stop(SandboxSettings(
#             environment="GeneralReasoning/test-env",
#             image="generalreasoning/idontexist:latest",
#             machine_size="1:2",
#         ))
#     assert "idontexist" in str(exc_info.value)
#     assert "ErrImagePull" in str(exc_info.value)


@pytest.mark.asyncio
async def test_missing_api_key():
    """Sandbox creation without an API key should fail with a clear auth message."""
    key = os.environ.pop("OPENREWARD_API_KEY", None)
    try:
        with pytest.raises(Exception) as exc_info:
            await _start_stop(SandboxSettings(
                environment="GeneralReasoning/test-env",
                image="python:3.11-slim",
                machine_size="1:2",
            ))
        assert "Authentication Failed" in str(exc_info.value)
    finally:
        if key is not None:
            os.environ["OPENREWARD_API_KEY"] = key


# ─────────────────────────────────────────────────────────────────────
# Client-side exception taxonomy
# ─────────────────────────────────────────────────────────────────────

import asyncio
from unittest.mock import MagicMock, patch

from openreward.api._session.http import _RemoteSSEError, resumable_sse
from openreward.api.environments.client import AsyncEnvironment, AsyncSession, Task
from openreward.api.errors import (
    SessionTerminatedError,
    ToolCallError,
    ToolFailed,
)


def _make_sse_bytes(events: list[tuple[str, str]]) -> bytes:
    lines = []
    for event, data in events:
        lines.append(f"event: {event}")
        lines.append(f"data: {data}")
        lines.append("")
    return "\n".join(lines).encode()


class _FakeContent:
    def __init__(self, raw: bytes):
        self._lines = raw.split(b"\n")

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self._lines:
            raise StopAsyncIteration
        return self._lines.pop(0) + b"\n"


class _FakeResp:
    def __init__(self, raw: bytes, status: int = 200):
        self.content = _FakeContent(raw)
        self.status = status
        self.ok = status < 400
        self.headers = {}
        self.request_info = MagicMock()
        self.history = ()

    async def text(self):
        return "" if self.ok else "session not found"

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        pass


@pytest.mark.asyncio
async def test_resumable_sse_410_with_sid_raises_session_terminated():
    """410 Gone on a session-bearing request is the unambiguous "session
    deleted" signal — surface as SessionTerminatedError."""
    client = MagicMock()
    client.post = MagicMock(return_value=_FakeResp(b"", status=410))

    with pytest.raises(SessionTerminatedError) as exc_info:
        await resumable_sse(
            client, "/foo/call", token="tok", sid="sid-123",
            max_retries=0, timeout=5, backoff_base=0.01,
        )
    assert exc_info.value.sid == "sid-123"
    assert "410" in str(exc_info.value)


@pytest.mark.asyncio
async def test_resumable_sse_410_without_sid_keeps_client_response_error():
    """Without an sid the 410 isn't session-bearing — should propagate as ClientResponseError."""
    client = MagicMock()
    client.post = MagicMock(return_value=_FakeResp(b"", status=410))

    with pytest.raises(aiohttp.ClientResponseError):
        await resumable_sse(
            client, "/create_session", token="tok",
            max_retries=0, timeout=5, backoff_base=0.01,
        )


@pytest.mark.asyncio
async def test_resumable_sse_404_with_sid_does_not_kill_session():
    """404 is ambiguous (wrong path / unknown env / missing session) —
    must propagate as plain ClientResponseError so the caller can decide."""
    client = MagicMock()
    client.post = MagicMock(return_value=_FakeResp(b"", status=404))

    with pytest.raises(aiohttp.ClientResponseError) as exc_info:
        await resumable_sse(
            client, "/foo/call", token="tok", sid="sid-x",
            max_retries=0, timeout=5, backoff_base=0.01,
        )
    assert exc_info.value.status == 404


@pytest.mark.asyncio
async def test_resumable_sse_sse_error_event_raises_remote_sse_error():
    """An SSE `error` event should surface as the typed _RemoteSSEError sentinel."""
    raw = _make_sse_bytes([
        ("task_id", "t-1"),
        ("error", "ValueError: boom"),
    ])
    client = MagicMock()
    client.post = MagicMock(return_value=_FakeResp(raw))

    with pytest.raises(_RemoteSSEError) as exc_info:
        await resumable_sse(
            client, "/foo/call", token="tok", sid="sid-1",
            max_retries=0, timeout=5, backoff_base=0.01,
        )
    assert "boom" in str(exc_info.value)
    # Sentinel still subclasses RuntimeError for back-compat with sandbox helpers.
    assert isinstance(exc_info.value, RuntimeError)


# ── AsyncSession.call_tool ──────────────────────────────────────────


def _build_session(sid: str = "sid-test") -> AsyncSession:
    """Construct an AsyncSession bypassing the network setup it normally does."""
    client = MagicMock()
    client._base_url = "http://test"
    client.closed = False
    env = AsyncEnvironment(
        namespace=None, name="env", variant=None,
        client=client, api_key="key",
    )
    session = AsyncSession(env, task=Task(
        server_name="env",
        environment_name="env",
        task_spec={},
        namespace=None,
    ))
    session.sid = sid
    return session


@pytest.mark.asyncio
async def test_call_tool_translates_remote_sse_error_to_tool_failed():
    """User @tool raising → SSE error event → AsyncSession surfaces ToolFailed."""
    session = _build_session()

    async def fake_resumable_sse(*args, **kwargs):
        raise _RemoteSSEError("ValueError: boom")

    with patch(
        "openreward.api.environments.client.resumable_sse",
        side_effect=fake_resumable_sse,
    ):
        with pytest.raises(ToolFailed) as exc_info:
            await session.call_tool("submit", {})

    assert "boom" in str(exc_info.value)


@pytest.mark.asyncio
async def test_call_tool_marks_session_dead_after_410():
    """A 410 mid-call should both raise SessionTerminatedError AND poison
    the local handle so subsequent calls short-circuit without going to
    the network. Closes the symmetry gap with the ToolFailed path."""
    session = _build_session()

    async def fake_resumable_sse(*args, **kwargs):
        raise SessionTerminatedError(
            "server returned 410: gone",
            sid=session.sid,
        )

    with patch(
        "openreward.api.environments.client.resumable_sse",
        side_effect=fake_resumable_sse,
    ):
        with pytest.raises(SessionTerminatedError):
            await session.call_tool("submit", {})

        # Second call must not touch the network.
        with pytest.raises(SessionTerminatedError):
            await session.call_tool("submit", {})

    # Local handle is now poisoned.
    assert session._dead_exception is not None
    assert session._dead.is_set()


@pytest.mark.asyncio
async def test_call_tool_marks_session_dead_after_tool_failed():
    """After a single ToolFailed, the next call_tool must raise SessionTerminatedError.

    This is the core invariant: tools own their retries, so any tool
    exception terminates the session and the caller cannot keep going on
    the same handle.
    """
    session = _build_session()

    async def fake_resumable_sse(*args, **kwargs):
        raise _RemoteSSEError("KeyError: 'x'")

    with patch(
        "openreward.api.environments.client.resumable_sse",
        side_effect=fake_resumable_sse,
    ):
        with pytest.raises(ToolFailed):
            await session.call_tool("submit", {})

        # Second call must short-circuit with SessionTerminatedError — the SDK
        # never retries past a tool failure.
        with pytest.raises(SessionTerminatedError):
            await session.call_tool("submit", {})


@pytest.mark.asyncio
async def test_call_tool_bad_input_shape_raises_invalid_tool_call():
    """Pre-flight input checks raise ToolCallError(reason='bad_input_shape')."""
    session = _build_session()

    with pytest.raises(ToolCallError) as exc_info:
        await session.call_tool("submit", "not a dict")  # type: ignore[arg-type]
    assert exc_info.value.reason == "bad_input_shape"

    with pytest.raises(ToolCallError) as exc_info:
        await session.call_tool("submit", {1: "x"})  # type: ignore[dict-item]
    assert exc_info.value.reason == "bad_input_shape"


@pytest.mark.asyncio
async def test_call_tool_run_tool_error_with_reason_raises_invalid_tool_call():
    """Server returns RunToolError with a `reason` field — client surfaces it verbatim."""
    session = _build_session()

    async def fake_resumable_sse(*args, **kwargs):
        return {
            "ok": False,
            "reason": "input_validation",
            "error": "Tool input validation error: [{...}]",
        }

    with patch(
        "openreward.api.environments.client.resumable_sse",
        side_effect=fake_resumable_sse,
    ):
        with pytest.raises(ToolCallError) as exc_info:
            await session.call_tool("submit", {})

    assert exc_info.value.reason == "input_validation"


@pytest.mark.asyncio
async def test_call_tool_eagerly_tears_down_server_session_on_tool_failed():
    """When a ToolFailed marks the session dead, the SDK should fire
    `_pre_delete` (POST /delete) without waiting for __aexit__, so the
    server doesn't keep the session running until the 900s reaper."""
    session = _build_session()

    pre_delete_calls = 0

    async def fake_pre_delete():
        nonlocal pre_delete_calls
        pre_delete_calls += 1

    async def fake_resumable_sse(*args, **kwargs):
        raise _RemoteSSEError("BOOM")

    with patch.object(session, "_pre_delete", fake_pre_delete), \
         patch(
             "openreward.api.environments.client.resumable_sse",
             side_effect=fake_resumable_sse,
         ):
        with pytest.raises(ToolFailed):
            await session.call_tool("submit", {})

        # _pre_delete is fire-and-forget; yield to let it run.
        await asyncio.sleep(0)
        await asyncio.sleep(0)

    assert pre_delete_calls == 1


@pytest.mark.asyncio
async def test_call_tool_run_tool_error_legacy_server_infers_reason():
    """Server predates the `reason` field — client infers from the message prefix."""
    session = _build_session()

    cases = [
        ("Tool name collision: 'foo' is defined in both...", "name_collision"),
        ("Tool input validation error: [{...}]", "input_validation"),
        ("'submit' is not a valid tool", "not_found"),
    ]

    for error_msg, expected in cases:
        async def fake_resumable_sse(*args, _msg=error_msg, **kwargs):
            return {"ok": False, "error": _msg}

        with patch(
            "openreward.api.environments.client.resumable_sse",
            side_effect=fake_resumable_sse,
        ):
            with pytest.raises(ToolCallError) as exc_info:
                await session.call_tool("submit", {})
        assert exc_info.value.reason == expected, f"for message {error_msg!r}"
