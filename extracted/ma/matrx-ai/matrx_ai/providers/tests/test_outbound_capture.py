"""Tests for ``matrx_ai.providers.outbound_capture`` — wire-level
CONTEXT_ANALYSIS capture.

SUTs: ``_outbound_request_hook`` (driven through the real
``make_capture_http_client`` + httpx transport, and through the real OpenAI
SDK), ``emit_explicit_context_analysis``, ``stamp_call_meta``. Doubles: the
network (``httpx.MockTransport``) and the stream sink (the emitter — what it
receives IS the contract).

Owned contract, and the break each group names:
1. ``snapshot`` off → nothing is emitted (a leak of payloads into the stream).
2. ``snapshot`` on → exactly one event carrying the literal request: body bytes
   decoded faithfully against a committed provider payload captured from the
   real OpenAI SDK (``fixtures/openai_responses_request.json``), non-JSON and
   non-object roots preserved, size = wire bytes, per-call metadata intact.
3. Every credential-bearing header is redacted in the EVENT and untouched on
   the WIRE (dropping one name from the set leaks a secret into the stream;
   redacting the request in place breaks the provider call).
4. Concurrent tasks see only their own ``CallMeta``.
5. A capture failure never breaks the outbound request.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import httpx
import openai
import pytest
from matrx_connect.context.app_context import (
    AppContext,
    clear_app_context,
    set_app_context,
)
from matrx_connect.context.events import ContextAnalysisPayload

from matrx_ai.providers.outbound_capture import (
    CallMeta,
    _call_meta_var,
    _outbound_request_hook,
    emit_explicit_context_analysis,
    get_call_meta,
    make_capture_http_client,
    set_call_meta,
    stamp_call_meta,
)

# Captured 2026-09-10 from openai 2.54.0's own serialization of a
# ``client.responses.create(...)`` call (instructions, multi-turn input, a
# strict function tool, reasoning, metadata) through the capture client.
_CAPTURED_OPENAI_REQUEST = Path(__file__).parent / "fixtures" / "openai_responses_request.json"

# The security contract, stated independently of the SUT's constant: these
# header names carry credentials or identifying tokens and must never reach
# the CONTEXT_ANALYSIS stream.
_CREDENTIAL_HEADERS = frozenset(
    {
        "authorization",
        "x-api-key",
        "x-goog-api-key",
        "x-goog-api-client",
        "proxy-authorization",
        "anthropic-api-key",
        "openai-organization",
        "openai-project",
        "cookie",
    }
)


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


def _only_payload(emitter: Any) -> ContextAnalysisPayload:
    assert emitter.send_context_analysis.await_count == 1
    payload = emitter.send_context_analysis.await_args.args[0]
    assert isinstance(payload, ContextAnalysisPayload)
    return payload


class _Wire:
    """The network: records exactly what left the process."""

    def __init__(self) -> None:
        self.requests: list[httpx.Request] = []

    def transport(self, response: httpx.Response | None = None) -> httpx.MockTransport:
        def _handle(request: httpx.Request) -> httpx.Response:
            self.requests.append(request)
            return response if response is not None else httpx.Response(200, json={"ok": True})

        return httpx.MockTransport(_handle)


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
            attempt=2,
        )
    )

    request_body = {
        "model": "gpt-5",
        "messages": [{"role": "user", "content": "hello"}],
        "stream": True,
    }
    request = _make_request(
        method="POST",
        url="https://api.openai.com/v1/responses?api-version=2025-01-01",
        body=request_body,
        headers={"Authorization": "Bearer sk-secret-abcdef"},
    )

    await _outbound_request_hook(request)

    payload = _only_payload(emitter)
    assert payload.provider == "openai"
    assert payload.model == "gpt-5-test"
    assert payload.iteration == 3
    assert payload.is_streaming is True
    assert payload.attempt == 2
    assert payload.method == "POST"
    assert payload.url == "https://api.openai.com/v1/responses?api-version=2025-01-01"

    assert payload.body == {
        "model": "gpt-5",
        "messages": [{"role": "user", "content": "hello"}],
        "stream": True,
    }
    assert payload.body_raw is None
    assert payload.body_size_bytes == len(request.content)

    # Auth header redacted in the EVENT...
    assert payload.headers["authorization"] == "<redacted>"
    # ...but NOT in the actual on-wire request.
    assert request.headers["authorization"] == "Bearer sk-secret-abcdef"

    assert payload.conversation_id == "conv-xyz"
    assert payload.request_id == "req-abc"


async def test_captured_provider_payload_is_recorded_byte_faithfully():
    """The committed payload goes out through the real capture client; the
    event must carry it exactly and size it by the bytes that hit the wire."""
    captured = json.loads(_CAPTURED_OPENAI_REQUEST.read_text())
    wire_bytes = json.dumps(captured, ensure_ascii=False).encode("utf-8")

    emitter = _make_emitter()
    _install_ctx(snapshot=True, emitter=emitter)
    set_call_meta(CallMeta(provider="openai", model="gpt-5", iteration=1))

    wire = _Wire()
    async with make_capture_http_client(transport=wire.transport()) as client:
        resp = await client.post(
            "https://api.openai.com/v1/responses",
            content=wire_bytes,
            headers={"Content-Type": "application/json"},
        )
    assert resp.status_code == 200

    payload = _only_payload(emitter)
    assert payload.body == json.loads(_CAPTURED_OPENAI_REQUEST.read_text())
    assert payload.body_raw is None
    assert payload.body_size_bytes == len(wire.requests[0].content) == len(wire_bytes)


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

    payload = _only_payload(emitter)
    assert payload.body is None
    assert payload.body_raw == "\x00\x01\x02\x03not-json"
    assert payload.body_size_bytes == 12


async def test_non_object_json_root_is_wrapped_not_dropped():
    emitter = _make_emitter()
    _install_ctx(snapshot=True, emitter=emitter)
    set_call_meta(CallMeta(provider="together"))

    request = _make_request(body=b'[{"role": "user", "content": "batch item"}]')
    await _outbound_request_hook(request)

    payload = _only_payload(emitter)
    assert payload.body == {"__non_dict_root__": [{"role": "user", "content": "batch item"}]}
    assert payload.body_raw is None


async def test_hook_handles_empty_body():
    emitter = _make_emitter()
    _install_ctx(snapshot=True, emitter=emitter)
    set_call_meta(CallMeta(provider="openai"))

    request = _make_request(method="GET", url="https://api.openai.com/v1/models")

    await _outbound_request_hook(request)

    payload = _only_payload(emitter)
    assert payload.body is None
    assert payload.body_raw is None
    assert payload.body_size_bytes == 0
    assert payload.method == "GET"


async def test_hook_uses_fallback_meta_when_set_call_meta_was_skipped():
    emitter = _make_emitter()
    _install_ctx(snapshot=True, emitter=emitter)
    # Deliberately do NOT call set_call_meta — a provider that forgot to stamp
    # metadata still produces an event, decorated with the fallback.

    request = _make_request(body={"x": 1})
    await _outbound_request_hook(request)

    payload = _only_payload(emitter)
    assert payload.provider == "unknown"
    assert payload.model is None
    assert payload.iteration is None
    assert payload.attempt == 1


async def test_capture_failure_never_breaks_the_outbound_request():
    emitter = _make_emitter()
    emitter.send_context_analysis.side_effect = RuntimeError("emit boom")
    _install_ctx(snapshot=True, emitter=emitter)
    set_call_meta(CallMeta(provider="openai"))

    wire = _Wire()
    async with make_capture_http_client(transport=wire.transport()) as client:
        resp = await client.post("https://api.openai.com/v1/responses", json={"x": 1})

    assert resp.status_code == 200
    assert [json.loads(r.content) for r in wire.requests] == [{"x": 1}]
    assert emitter.send_context_analysis.await_count == 1


# ---------------------------------------------------------------------------
# Header redaction — through the real OpenAI SDK
# ---------------------------------------------------------------------------


async def test_every_credential_header_is_redacted_in_the_event_and_untouched_on_the_wire():
    emitter = _make_emitter()
    _install_ctx(snapshot=True, emitter=emitter)
    set_call_meta(CallMeta(provider="openai", model="gpt-5", iteration=1))

    secrets_on_wire = {
        "authorization": "Bearer sk-live-not-real",
        "openai-organization": "org-live-not-real",
        "openai-project": "proj-live-not-real",
        "cookie": "session=live-cookie",
        "proxy-authorization": "Basic cHJveHk6c2VjcmV0",
        "x-goog-api-client": "gl-python/3.13 grpc/1.0 auth/token-bearing",
        "x-api-key": "ant-key-live",
        "x-goog-api-key": "goog-key-live",
        "anthropic-api-key": "ant-live",
    }
    wire = _Wire()
    sdk = openai.AsyncOpenAI(
        api_key="sk-live-not-real",
        organization="org-live-not-real",
        project="proj-live-not-real",
        max_retries=0,
        default_headers={
            "Cookie": "session=live-cookie",
            "Proxy-Authorization": "Basic cHJveHk6c2VjcmV0",
            "X-Goog-Api-Client": "gl-python/3.13 grpc/1.0 auth/token-bearing",
            "X-API-Key": "ant-key-live",
            "X-Goog-Api-Key": "goog-key-live",
            "Anthropic-Api-Key": "ant-live",
        },
        http_client=make_capture_http_client(
            sdk=openai,
            transport=wire.transport(
                httpx.Response(400, json={"error": {"message": "stop", "type": "invalid_request_error"}})
            ),
        ),
    )
    with pytest.raises(openai.BadRequestError):
        await sdk.responses.create(model="gpt-5", input="Plan the upgrade.")

    assert len(wire.requests) == 1
    on_wire = dict(wire.requests[0].headers.items())
    payload = _only_payload(emitter)

    # The wire request is untouched: every secret reached the provider as sent.
    assert {k: on_wire[k] for k in secrets_on_wire} == secrets_on_wire
    # The event carries every wire header — credentials redacted, the rest verbatim.
    assert payload.headers == {
        k: ("<redacted>" if k in _CREDENTIAL_HEADERS else v) for k, v in on_wire.items()
    }
    assert {k for k, v in payload.headers.items() if v == "<redacted>"} == set(secrets_on_wire)
    # And the body is what the SDK serialized onto the wire.
    assert payload.body == {"model": "gpt-5", "input": "Plan the upgrade."}
    assert payload.body_size_bytes == len(wire.requests[0].content)


# ---------------------------------------------------------------------------
# emit_explicit_context_analysis — non-httpx provider call sites
# ---------------------------------------------------------------------------


async def test_explicit_emit_redacts_credentials_in_caller_header_case_and_sizes_the_body():
    emitter = _make_emitter()
    _install_ctx(snapshot=True, emitter=emitter)
    set_call_meta(CallMeta(provider="elevenlabs", model="eleven_v3", iteration=2))

    await emit_explicit_context_analysis(
        provider="elevenlabs",
        method="POST",
        url="https://api.elevenlabs.io/v1/text-to-dialogue/stream",
        headers={
            "Authorization": "Bearer el-secret",
            "Cookie": "sid=el",
            "Content-Type": "application/json",
        },
        body={"inputs": [{"text": "hi"}]},
        is_streaming=True,
        model="caller-fallback-model",
        attempt=3,
    )

    payload = _only_payload(emitter)
    assert payload.headers == {
        "Authorization": "<redacted>",
        "Cookie": "<redacted>",
        "Content-Type": "application/json",
    }
    assert payload.body == {"inputs": [{"text": "hi"}]}
    # len('{"inputs": [{"text": "hi"}]}') — the JSON the provider receives.
    assert payload.body_size_bytes == 28
    assert payload.model == "eleven_v3"  # stamped call meta wins over the caller hint
    assert payload.iteration == 2
    assert payload.is_streaming is True
    assert payload.attempt == 3
    assert payload.conversation_id == "conv-xyz"


async def test_explicit_emit_without_call_meta_uses_caller_model_and_utf8_raw_size():
    emitter = _make_emitter()
    _install_ctx(snapshot=True, emitter=emitter)
    token = _call_meta_var.set(None)  # no provider stamped CallMeta for this call
    try:
        await emit_explicit_context_analysis(
            provider="google",
            method="POST",
            url="https://generativelanguage.googleapis.com/v1beta/models/gemini:streamGenerateContent",
            body_raw="café",
            model="gemini-2.5-pro",
        )
    finally:
        _call_meta_var.reset(token)

    payload = _only_payload(emitter)
    assert payload.provider == "google"
    assert payload.model == "gemini-2.5-pro"
    assert payload.iteration is None
    assert payload.body is None
    assert payload.body_raw == "café"
    assert payload.body_size_bytes == 5  # 'café' is 5 UTF-8 bytes
    assert payload.is_streaming is False


# ---------------------------------------------------------------------------
# Concurrency: ContextVar isolation
# ---------------------------------------------------------------------------


async def test_concurrent_tasks_see_their_own_call_meta():
    emitter = _make_emitter()
    _install_ctx(snapshot=True, emitter=emitter)

    a_stamped = asyncio.Event()
    b_stamped = asyncio.Event()

    async def task_a():
        set_call_meta(CallMeta(provider="openai", model="m-a", iteration=1))
        a_stamped.set()
        # Emit only AFTER task b has stamped its own meta: a shared (non-
        # ContextVar) slot would now hold b's values.
        await asyncio.wait_for(b_stamped.wait(), timeout=5)
        await _outbound_request_hook(_make_request(body={"task": "a"}))

    async def task_b():
        await asyncio.wait_for(a_stamped.wait(), timeout=5)
        set_call_meta(CallMeta(provider="anthropic", model="m-b", iteration=99))
        b_stamped.set()
        await _outbound_request_hook(_make_request(body={"task": "b"}))

    await asyncio.gather(task_a(), task_b())

    payloads = [c.args[0] for c in emitter.send_context_analysis.await_args_list]
    by_task = {p.body["task"]: (p.provider, p.model, p.iteration) for p in payloads}
    assert by_task == {"a": ("openai", "m-a", 1), "b": ("anthropic", "m-b", 99)}


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
        stamp_call_meta(provider="openai", model="gpt-5", is_streaming=True, attempt=2)
        assert get_call_meta() == CallMeta(
            provider="openai", model="gpt-5", iteration=7, is_streaming=True, attempt=2
        )
    finally:
        clear_execution_state(token)


async def test_stamp_call_meta_works_without_execution_state():
    # Outside an executor — iteration is None but no exception is raised.
    stamp_call_meta(provider="standalone", model="x")
    assert get_call_meta() == CallMeta(provider="standalone", model="x", iteration=None)


# ---------------------------------------------------------------------------
# make_capture_http_client
# ---------------------------------------------------------------------------


async def test_make_capture_http_client_installs_request_hook_only_once():
    client = make_capture_http_client(event_hooks={"request": [_outbound_request_hook]})
    request_hooks = client.event_hooks.get("request", [])
    assert request_hooks.count(_outbound_request_hook) == 1


async def test_make_capture_http_client_does_not_clobber_caller_hooks():
    extra = AsyncMock()
    client = make_capture_http_client(event_hooks={"request": [extra]})
    assert client.event_hooks.get("request", []) == [extra, _outbound_request_hook]
