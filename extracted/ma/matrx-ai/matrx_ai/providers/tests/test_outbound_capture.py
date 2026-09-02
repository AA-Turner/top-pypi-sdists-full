"""Tests for ``matrx_ai.providers.outbound_capture`` — wire-level
CONTEXT_ANALYSIS capture.

The hard guarantees we lock down here:

1. ``snapshot=False`` (the default): the request hook is a near-no-op —
   no emitter call, no body parsing, no payload allocation.
2. ``snapshot=True``: an outbound httpx request triggers exactly one
   ``send_context_analysis`` call carrying the literal wire bytes (URL,
   method, headers, parsed JSON body, byte size). Auth-bearing headers
   are redacted in the event but NOT on the on-wire request itself.
3. Concurrent async tasks see only their own ``CallMeta`` (ContextVar
   isolation).
4. Hook exceptions never break the outbound request.
"""

from __future__ import annotations

import asyncio
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from matrx_ai.providers.outbound_capture import (
    CallMeta,
    _outbound_request_hook,
    emit_explicit_context_analysis,
    get_call_meta,
    make_capture_http_client,
    set_call_meta,
    stamp_call_meta,
)
from matrx_connect.context.app_context import (
    AppContext,
    clear_app_context,
    set_app_context,
)
from matrx_connect.context.events import ContextAnalysisPayload


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_emitter() -> Any:
    """A MagicMock ``Emitter`` whose async methods return AsyncMock."""
    emitter = MagicMock()
    emitter.send_context_analysis = AsyncMock()
    return emitter


def _install_ctx(*, snapshot: bool, emitter: Any | None = None) -> AppContext:
    em = emitter if emitter is not None else _make_emitter()
    ctx = AppContext(
        emitter=em,
        user_id="test-user",
        request_id="req-abc",
        conversation_id="conv-xyz",
        snapshot=snapshot,
    )
    token = set_app_context(ctx)
    # Tests are responsible for resetting via the returned context — we use
    # a fixture below to handle teardown.
    _install_ctx._token = token  # type: ignore[attr-defined]
    return ctx


def _make_request(
    *,
    method: str = "POST",
    url: str = "https://api.openai.com/v1/responses",
    body: dict[str, Any] | bytes | str | None = None,
    headers: dict[str, str] | None = None,
) -> httpx.Request:
    if isinstance(body, dict):
        return httpx.Request(method, url, json=body, headers=headers or {})
    if isinstance(body, str):
        return httpx.Request(method, url, content=body.encode("utf-8"), headers=headers or {})
    if isinstance(body, bytes):
        return httpx.Request(method, url, content=body, headers=headers or {})
    return httpx.Request(method, url, headers=headers or {})


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _reset_ctx_between_tests():
    yield
    token = getattr(_install_ctx, "_token", None)
    if token is not None:
        try:
            clear_app_context(token)
        except Exception:
            pass
    _install_ctx._token = None  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# Fast-path: snapshot=False
# ---------------------------------------------------------------------------


async def test_hook_is_noop_when_no_app_context_is_set():
    # No AppContext at all → ContextVar.get() returns None → instant return.
    request = _make_request(body={"messages": [{"role": "user", "content": "hi"}]})
    await _outbound_request_hook(request)  # must not raise


async def test_hook_is_noop_when_snapshot_flag_is_false():
    emitter = _make_emitter()
    _install_ctx(snapshot=False, emitter=emitter)

    request = _make_request(body={"messages": [{"role": "user", "content": "hi"}]})
    await _outbound_request_hook(request)

    emitter.send_context_analysis.assert_not_called()


async def test_explicit_emit_is_noop_when_snapshot_flag_is_false():
    emitter = _make_emitter()
    _install_ctx(snapshot=False, emitter=emitter)

    await emit_explicit_context_analysis(
        provider="elevenlabs",
        method="POST",
        url="https://api.elevenlabs.io/v1/text-to-dialogue/stream",
        body={"inputs": []},
    )
    emitter.send_context_analysis.assert_not_called()


# ---------------------------------------------------------------------------
# Hot path: snapshot=True
# ---------------------------------------------------------------------------


async def test_hook_emits_exactly_once_with_wire_bytes_when_snapshot_enabled():
    emitter = _make_emitter()
    _install_ctx(snapshot=True, emitter=emitter)
    set_call_meta(
        CallMeta(
            provider="openai",
            model="gpt-5-test",
            iteration=3,
            is_streaming=True,
            attempt=1,
        )
    )

    request_body = {
        "model": "gpt-5",
        "messages": [{"role": "user", "content": "hello"}],
        "stream": True,
    }
    request = _make_request(
        method="POST",
        url="https://api.openai.com/v1/responses",
        body=request_body,
        headers={"Authorization": "Bearer sk-secret-abcdef"},
    )

    await _outbound_request_hook(request)

    assert emitter.send_context_analysis.call_count == 1
    payload: ContextAnalysisPayload = emitter.send_context_analysis.call_args.args[0]
    assert isinstance(payload, ContextAnalysisPayload)

    assert payload.provider == "openai"
    assert payload.model == "gpt-5-test"
    assert payload.iteration == 3
    assert payload.is_streaming is True
    assert payload.method == "POST"
    assert payload.url == "https://api.openai.com/v1/responses"

    # Body was JSON-decoded faithfully.
    assert payload.body == request_body
    assert payload.body_raw is None
    assert payload.body_size_bytes == len(request.content)

    # Auth header redacted in the EVENT...
    assert payload.headers["authorization"] == "<redacted>"
    # ...but NOT in the actual on-wire request.
    assert request.headers["authorization"] == "Bearer sk-secret-abcdef"

    # Conversation/request IDs from AppContext flow through.
    assert payload.conversation_id == "conv-xyz"
    assert payload.request_id == "req-abc"


async def test_hook_handles_non_json_body_via_body_raw():
    emitter = _make_emitter()
    _install_ctx(snapshot=True, emitter=emitter)
    set_call_meta(CallMeta(provider="openai"))

    request = _make_request(
        method="POST",
        url="https://api.openai.com/v1/audio/speech",
        body=b"\x00\x01\x02\x03not-json",
    )

    await _outbound_request_hook(request)

    payload: ContextAnalysisPayload = emitter.send_context_analysis.call_args.args[0]
    assert payload.body is None
    assert payload.body_raw is not None
    assert "not-json" in payload.body_raw
    assert payload.body_size_bytes == len(b"\x00\x01\x02\x03not-json")


async def test_hook_handles_empty_body():
    emitter = _make_emitter()
    _install_ctx(snapshot=True, emitter=emitter)
    set_call_meta(CallMeta(provider="openai"))

    request = _make_request(method="GET", url="https://api.openai.com/v1/models")

    await _outbound_request_hook(request)

    payload: ContextAnalysisPayload = emitter.send_context_analysis.call_args.args[0]
    assert payload.body is None
    assert payload.body_raw is None
    assert payload.body_size_bytes == 0
    assert payload.method == "GET"


async def test_hook_uses_fallback_meta_when_set_call_meta_was_skipped():
    emitter = _make_emitter()
    _install_ctx(snapshot=True, emitter=emitter)
    # Deliberately do NOT call set_call_meta — simulate a provider that
    # forgot to stamp metadata. We still want an event, just decorated
    # with the fallback.

    request = _make_request(body={"x": 1})
    await _outbound_request_hook(request)

    payload: ContextAnalysisPayload = emitter.send_context_analysis.call_args.args[0]
    assert payload.provider == "unknown"
    assert payload.model is None
    assert payload.iteration is None


async def test_hook_swallows_emitter_exceptions_so_request_succeeds():
    emitter = _make_emitter()
    emitter.send_context_analysis.side_effect = RuntimeError("emit boom")
    _install_ctx(snapshot=True, emitter=emitter)
    set_call_meta(CallMeta(provider="openai"))

    request = _make_request(body={"x": 1})
    # MUST NOT raise — capture failures cannot break the live request.
    await _outbound_request_hook(request)


# ---------------------------------------------------------------------------
# Header redaction set
# ---------------------------------------------------------------------------


async def test_all_known_auth_headers_are_redacted():
    emitter = _make_emitter()
    _install_ctx(snapshot=True, emitter=emitter)
    set_call_meta(CallMeta(provider="generic"))

    request = _make_request(
        body={"x": 1},
        headers={
            "Authorization": "Bearer xxx",
            "X-API-Key": "ant-key-yyy",
            "X-Goog-Api-Key": "goog-zzz",
            "Anthropic-Api-Key": "ant-www",
            "Content-Type": "application/json",  # NOT redacted
        },
    )

    await _outbound_request_hook(request)
    payload: ContextAnalysisPayload = emitter.send_context_analysis.call_args.args[0]

    headers = {k.lower(): v for k, v in payload.headers.items()}
    assert headers["authorization"] == "<redacted>"
    assert headers["x-api-key"] == "<redacted>"
    assert headers["x-goog-api-key"] == "<redacted>"
    assert headers["anthropic-api-key"] == "<redacted>"
    assert headers["content-type"] == "application/json"


# ---------------------------------------------------------------------------
# Concurrency: ContextVar isolation
# ---------------------------------------------------------------------------


async def test_concurrent_tasks_see_their_own_call_meta():
    emitter = _make_emitter()
    _install_ctx(snapshot=True, emitter=emitter)

    captured: dict[str, ContextAnalysisPayload | None] = {"a": None, "b": None}

    async def task_a():
        set_call_meta(CallMeta(provider="openai", model="m-a", iteration=1))
        await asyncio.sleep(0.01)
        em_a = MagicMock()
        em_a.send_context_analysis = AsyncMock()
        # Local emitter override for this task's context — but the real
        # path uses the shared emitter. We instead verify by inspecting
        # what the SHARED emitter received for this task's request.
        request = _make_request(body={"task": "a"})
        await _outbound_request_hook(request)
        # Find the most-recent call args.
        captured["a"] = emitter.send_context_analysis.call_args.args[0]

    async def task_b():
        set_call_meta(CallMeta(provider="anthropic", model="m-b", iteration=99))
        await asyncio.sleep(0.005)
        request = _make_request(body={"task": "b"})
        await _outbound_request_hook(request)
        captured["b"] = emitter.send_context_analysis.call_args.args[0]

    # Run both — each is its own asyncio Task → forked ContextVar view.
    await asyncio.gather(task_a(), task_b())

    # Both tasks emitted (we just need both to have produced a payload that
    # matches their own metadata, regardless of which one happens to be the
    # most-recent overall call_args).
    assert emitter.send_context_analysis.call_count == 2
    payloads = [c.args[0] for c in emitter.send_context_analysis.call_args_list]

    by_task = {p.body["task"]: p for p in payloads}
    assert by_task["a"].provider == "openai"
    assert by_task["a"].model == "m-a"
    assert by_task["a"].iteration == 1
    assert by_task["b"].provider == "anthropic"
    assert by_task["b"].model == "m-b"
    assert by_task["b"].iteration == 99


# ---------------------------------------------------------------------------
# stamp_call_meta + ExecutionState integration
# ---------------------------------------------------------------------------


async def test_stamp_call_meta_reads_iteration_from_execution_state():
    from matrx_ai.orchestrator.execution_state import (
        ExecutionState,
        clear_execution_state,
        set_execution_state,
    )

    state = ExecutionState()
    state.iteration = 7
    token = set_execution_state(state)
    try:
        stamp_call_meta(provider="openai", model="gpt-5", is_streaming=True)
        meta = get_call_meta()
        assert meta is not None
        assert meta.provider == "openai"
        assert meta.model == "gpt-5"
        assert meta.iteration == 7
        assert meta.is_streaming is True
    finally:
        clear_execution_state(token)


async def test_stamp_call_meta_works_without_execution_state():
    # Outside an executor — iteration is None but no exception is raised.
    stamp_call_meta(provider="standalone", model="x")
    meta = get_call_meta()
    assert meta is not None
    assert meta.iteration is None


# ---------------------------------------------------------------------------
# make_capture_http_client — factory smoke test
# ---------------------------------------------------------------------------


async def test_make_capture_http_client_installs_request_hook_only_once():
    client = make_capture_http_client()
    request_hooks = client.event_hooks.get("request", [])
    assert _outbound_request_hook in request_hooks
    assert request_hooks.count(_outbound_request_hook) == 1


async def test_make_capture_http_client_does_not_clobber_caller_hooks():
    extra = AsyncMock()
    client = make_capture_http_client(event_hooks={"request": [extra]})
    request_hooks = client.event_hooks.get("request", [])
    assert extra in request_hooks
    assert _outbound_request_hook in request_hooks


async def test_capture_http_client_drives_the_hook_end_to_end():
    """Full integration: build a real httpx.AsyncClient with our hook,
    point it at httpx's MockTransport so we don't hit the network, and
    assert the hook fires with the actual on-wire request."""

    emitter = _make_emitter()
    _install_ctx(snapshot=True, emitter=emitter)
    set_call_meta(
        CallMeta(provider="openai", model="gpt-5", iteration=2, is_streaming=False)
    )

    seen_bodies: list[bytes] = []

    def _handle(request: httpx.Request) -> httpx.Response:
        seen_bodies.append(request.content)
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(_handle)
    async with make_capture_http_client(transport=transport) as client:
        resp = await client.post(
            "https://api.openai.com/v1/responses",
            json={"model": "gpt-5", "stream": False, "messages": [{"role": "user", "content": "hi"}]},
            headers={"Authorization": "Bearer sk-test"},
        )
        assert resp.status_code == 200

    # Hook fired exactly once.
    assert emitter.send_context_analysis.call_count == 1
    payload: ContextAnalysisPayload = emitter.send_context_analysis.call_args.args[0]
    assert payload.body == {
        "model": "gpt-5",
        "stream": False,
        "messages": [{"role": "user", "content": "hi"}],
    }
    assert payload.headers["authorization"] == "<redacted>"
    assert payload.body_size_bytes == len(seen_bodies[0])
