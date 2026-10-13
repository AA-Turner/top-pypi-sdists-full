"""Capture mode returns EXACTLY what each provider adapter would send — and sends nothing.

The Model view (agent builder) shows the request a run would send. It is only
honest if, for every provider adapter, the captured request is byte-for-byte
the request the provider receives on a real call. Each test runs the SAME
adapter twice on the same input:

1. normally, through a recording transport (the "wire") that answers 400 —
   so we hold the exact bytes the SDK put on the wire, and
2. in capture mode — where the transport must NOT be reached, and the captured
   ``body_text`` must equal those bytes.

Break the capture hook (``outbound_capture._outbound_request_hook``), the genai
wrapper (``install_genai_capture``) or the xAI branch and these go red.
"""

from __future__ import annotations

import json
from contextlib import asynccontextmanager
from typing import Any

import anthropic as anthropic_sdk
import cerebras.cloud.sdk as cerebras_sdk
import groq as groq_sdk
import httpx
import openai as openai_sdk
import pytest
import together as together_sdk
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_connect.emitters import SilentEmitter

from matrx_ai.config import TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.providers.outbound_capture import make_capture_http_client, resolve_sdk_httpx
from matrx_ai.providers.request_capture import (
    REDACTED,
    ProviderRequestCaptured,
    capturing_provider_request,
    is_capturing,
)
from matrx_ai.testing.profile_factory import make_profile

SECRET = "sk-test-SECRET-never-returned-0123456789"
SYSTEM = "You help Dana Whitfield plan a trip.\n\n  Keep answers short.\t(tab)"
USER = "Where should I go in May?\n\n   Two lines,\ttabbed.  "


def _profile(model: str, wire_format: str) -> Any:
    from matrx_ai.catalog.controls import ControlRule

    key = "max_output_tokens" if wire_format.startswith("google") else "max_tokens"
    return make_profile(
        model_name=model,
        wire_format=wire_format,
        rules={"max_output_tokens": ControlRule.model_validate({"provider_key": key})},
    )


def _config(model: str, *, stream: bool) -> UnifiedConfig:
    return UnifiedConfig(
        model=model,
        stream=stream,
        max_output_tokens=1024,
        system_instruction=SYSTEM,
        messages=[UnifiedMessage(role="user", content=[TextContent(text=USER)])],
    )


class _Wire:
    """A transport that records every request and answers 400 (so no parser runs)."""

    def __init__(self, sdk: Any) -> None:
        self.requests: list[Any] = []
        self._flavor = resolve_sdk_httpx(sdk)

    def transport(self) -> Any:
        def handler(request: Any) -> Any:
            if str(request.url).endswith("/tcp_warming"):  # Cerebras SDK constructor warm-up, not a call
                return self._flavor.Response(200, text="ok")
            self.requests.append(request)
            return self._flavor.Response(400, json={"error": {"type": "invalid_request_error", "message": "recorded"}})

        return self._flavor.MockTransport(handler)


@pytest.fixture
def app_context():
    token = set_app_context(AppContext(emitter=SilentEmitter()))
    yield
    clear_app_context(token)


@pytest.fixture(autouse=True)
def _no_keys(monkeypatch):
    monkeypatch.setattr("matrx_ai.providers.keys.resolve_api_key", lambda *a, **kw: SECRET)


def _anthropic(wire: _Wire):
    from matrx_ai.providers.anthropic.anthropic_api import AnthropicChat

    chat = AnthropicChat()
    chat.client = anthropic_sdk.AsyncAnthropic(
        api_key=SECRET,
        max_retries=0,
        http_client=make_capture_http_client(sdk=anthropic_sdk, transport=wire.transport()),
    )
    return chat


def _openai(wire: _Wire):
    from matrx_ai.providers.openai.openai_api import OpenAIChat

    chat = OpenAIChat()
    chat.client = openai_sdk.AsyncOpenAI(
        api_key=SECRET,
        max_retries=0,
        http_client=make_capture_http_client(sdk=openai_sdk, transport=wire.transport()),
    )
    return chat


def _groq(wire: _Wire):
    from matrx_ai.providers.groq.groq_api import GroqChat

    chat = GroqChat()
    chat.client = groq_sdk.AsyncGroq(
        api_key=SECRET,
        max_retries=0,
        http_client=make_capture_http_client(sdk=groq_sdk, transport=wire.transport()),
    )
    return chat


def _cerebras(wire: _Wire):
    from matrx_ai.providers.cerebras.cerebras_api import CerebrasChat

    chat = CerebrasChat()
    chat.client = cerebras_sdk.AsyncCerebras(
        api_key=SECRET,
        max_retries=0,
        warm_tcp_connection=False,
        http_client=make_capture_http_client(sdk=cerebras_sdk, transport=wire.transport()),
    )
    return chat


def _together(wire: _Wire):
    from matrx_ai.providers.together.together_api import TogetherChat

    chat = TogetherChat()
    chat.client = together_sdk.AsyncTogether(
        api_key=SECRET,
        max_retries=0,
        http_client=make_capture_http_client(sdk=together_sdk, transport=wire.transport()),
    )
    return chat


def _moonshot(wire: _Wire):
    from matrx_ai.providers.moonshot.moonshot_api import MoonshotChat

    chat = MoonshotChat()
    chat.client = openai_sdk.AsyncOpenAI(
        api_key=SECRET,
        max_retries=0,
        base_url="https://api.moonshot.ai/v1",
        http_client=make_capture_http_client(sdk=openai_sdk, transport=wire.transport()),
    )
    return chat


HTTPX_ADAPTERS = [
    pytest.param(_anthropic, anthropic_sdk, "anthropic_chat", "claude-haiku-5-5", id="anthropic"),
    pytest.param(_openai, openai_sdk, "openai_responses", "gpt-5-nano", id="openai-responses"),
    pytest.param(_openai, openai_sdk, "openai_chat", "gpt-4.1-mini", id="openai-chat"),
    pytest.param(_groq, groq_sdk, "groq_chat", "llama-3.1-8b-instant", id="groq"),
    pytest.param(_cerebras, cerebras_sdk, "cerebras_chat", "llama3.1-8b", id="cerebras"),
    pytest.param(_together, together_sdk, "together_chat", "meta-llama/Llama-3-8b-chat-hf", id="together"),
    pytest.param(_moonshot, openai_sdk, "moonshot_chat", "kimi-k2", id="moonshot-generic-openai"),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("stream", [False, True])
@pytest.mark.parametrize(("build", "sdk", "wire_format", "model"), HTTPX_ADAPTERS)
async def test_capture_is_the_exact_wire_request_and_nothing_is_sent(
    app_context, build, sdk, wire_format, model, stream
):
    profile = _profile(model, wire_format)

    # 1 — the real send, recorded at the transport.
    wire = _Wire(sdk)
    chat = build(wire)
    with pytest.raises(Exception) as failure:  # noqa: B017 — the recording wire answers 400
        await chat.execute(_config(model, stream=stream), profile)
    assert len(wire.requests) == 1, f"the adapter must send exactly one request: {failure.value!r}"
    sent = wire.requests[0]

    # 2 — the same input, captured: the wire is never reached.
    capture_wire = _Wire(sdk)
    chat = build(capture_wire)
    with capturing_provider_request(), pytest.raises(ProviderRequestCaptured) as stop:
        await chat.execute(_config(model, stream=stream), profile)
    assert capture_wire.requests == [], "capture mode SENT the request"

    captured = stop.value.request
    assert captured["body_text"].encode("utf-8") == sent.content, "captured body differs from the wire"
    assert captured["body"] == json.loads(sent.content)
    assert captured["method"] == sent.method
    assert captured["url"] == str(sent.url)
    assert captured["transport"] == "https"
    # The text the person typed and the system text reach the wire untouched.
    assert json.dumps(USER)[1:-1] in captured["body_text"]
    # Secrets never come back.
    assert SECRET not in json.dumps(captured)
    secret_headers = {k.lower() for k, v in sent.headers.items() if SECRET in v}
    assert secret_headers, "the SDK did not send the key at all — the redaction check proves nothing"
    for name in secret_headers:
        assert {k.lower(): v for k, v in captured["headers"].items()}[name] == REDACTED
    assert not is_capturing()


@pytest.mark.asyncio
@pytest.mark.parametrize("stream", [False, True])
async def test_google_capture_is_what_genai_puts_on_the_wire(app_context, monkeypatch, stream):
    from google import genai

    from matrx_ai.providers.google.google_api import GoogleChat

    recorded: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        recorded.append(request)
        return httpx.Response(400, json={"error": {"code": 400, "message": "recorded", "status": "INVALID_ARGUMENT"}})

    def client_on(transport_records: list) -> Any:
        return genai.Client(
            api_key=SECRET,
            http_options=genai.types.HttpOptions(httpx_async_client=httpx.AsyncClient(transport=httpx.MockTransport(handler))),
        )

    model = "gemini-3.1-flash-lite"
    profile = _profile(model, "google_chat")
    chat = GoogleChat()
    chat.client = client_on(recorded)
    with pytest.raises(Exception) as failure:  # noqa: B017
        await chat.execute(_config(model, stream=stream), profile)
    assert len(recorded) == 1, repr(failure.value)
    sent = recorded[0]

    chat = GoogleChat()
    chat.client = client_on(recorded)
    with capturing_provider_request(), pytest.raises(ProviderRequestCaptured) as stop:
        await chat.execute(_config(model, stream=stream), profile)
    assert len(recorded) == 1, "capture mode SENT the request"
    captured = stop.value.request
    assert captured["body_text"].encode("utf-8") == sent.content
    assert captured["url"] == str(sent.url)
    assert captured["provider"] == "google"
    assert SECRET not in json.dumps(captured)
    assert captured["headers"]["x-goog-api-key"] == REDACTED


@pytest.mark.asyncio
@pytest.mark.parametrize("stream", [False, True])
async def test_xai_capture_is_the_request_proto_the_stub_sends(app_context, monkeypatch, stream):
    import grpc
    import xai_sdk
    from google.protobuf.json_format import MessageToDict
    from xai_sdk.proto import chat_pb2, chat_pb2_grpc

    from matrx_ai.providers.xai.xai_api import XAIChat

    received: list[Any] = []

    class ChatService(chat_pb2_grpc.ChatServicer):
        async def GetCompletion(self, request, context):
            received.append(request)
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "recorded")

        async def GetCompletionChunk(self, request, context):
            received.append(request)
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "recorded")
            yield  # pragma: no cover

    server = grpc.aio.server()
    chat_pb2_grpc.add_ChatServicer_to_server(ChatService(), server)
    port = server.add_insecure_port("127.0.0.1:0")
    await server.start()
    real_client = xai_sdk.AsyncClient
    monkeypatch.setattr(
        xai_sdk,
        "AsyncClient",
        lambda api_key: real_client(api_key=api_key, api_host=f"127.0.0.1:{port}", use_insecure_channel=True, timeout=5),
    )
    model = "grok-build-0.1"
    profile = _profile(model, "xai_chat")
    try:
        from matrx_ai.providers.keys import prepare_provider_clients

        provider = XAIChat()
        await prepare_provider_clients(provider)
        with pytest.raises(Exception) as failure:  # noqa: B017
            await provider.execute(_config(model, stream=stream), profile)
        assert len(received) == 1, repr(failure.value)
        sent = MessageToDict(received[0], preserving_proto_field_name=True)

        with capturing_provider_request(), pytest.raises(ProviderRequestCaptured) as stop:
            await provider.execute(_config(model, stream=stream), profile)
        assert len(received) == 1, "capture mode SENT the request"
        captured = stop.value.request
        assert captured["transport"] == "grpc"
        assert captured["body"] == sent
        assert json.loads(captured["body_text"]) == sent
        assert captured["url"].endswith("GetCompletionChunk" if stream else "GetCompletion")
    finally:
        await server.stop(None)


@pytest.mark.asyncio
async def test_capture_unwinds_without_reports_findings_or_spend_gates(app_context, monkeypatch):
    """The dispatch seams a real failure takes are silent for a capture: nothing is filed."""
    from matrx_ai.providers.unified_client import UnifiedAIClient

    called: list[str] = []

    async def report(*a, **kw):
        called.append("report_dispatch_failure")

    async def flush(*a, **kw):
        called.append("flush_translation_findings")

    async def gate(*a, **kw):
        called.append("admit_paid_call")

    @asynccontextmanager
    async def admit(profile):
        yield

    monkeypatch.setattr("matrx_ai.providers.failure_report.report_dispatch_failure", report)
    monkeypatch.setattr("matrx_ai.providers.structured_output_findings.flush_translation_findings", flush)
    monkeypatch.setattr("matrx_ai.providers.usage_gate.admit_paid_call", gate)
    monkeypatch.setattr("matrx_ai.providers.admission.admit_provider_call", admit)

    wire = _Wire(anthropic_sdk)
    chat = _anthropic(wire)
    model = "claude-haiku-5-5"
    profile = _profile(model, "anthropic_chat")
    with capturing_provider_request(), pytest.raises(ProviderRequestCaptured):
        await UnifiedAIClient._dispatch_with_billing_net(
            lambda: chat.execute(_config(model, stream=True), profile),
            profile=profile,
            provider_client=chat,
        )
    assert wire.requests == []
    assert called == [], f"a capture reached a failure/finding/spend seam: {called}"

    # The same seams DO fire for a real failure — the doubles above are live.
    with pytest.raises(Exception):  # noqa: B017
        await UnifiedAIClient._dispatch_with_billing_net(
            lambda: chat.execute(_config(model, stream=True), profile),
            profile=profile,
            provider_client=chat,
        )
    assert "report_dispatch_failure" in called and "admit_paid_call" in called


@pytest.mark.asyncio
async def test_a_route_without_a_wire_capture_is_never_run(app_context, monkeypatch):
    """A route whose transport cannot stop (native decisions, media…) returns the request instead."""
    from matrx_ai.providers import unified_client

    profile = make_profile(model_name="sys-one", wire_format="typesafe_systemone")

    async def resolve(*a, **kw):
        return profile

    monkeypatch.setattr("matrx_ai.catalog.resolve.resolve_tts_call_profile", resolve)
    from matrx_ai.orchestrator.requests import AIMatrixRequest

    request = AIMatrixRequest(conversation_id="c", config=_config("sys-one", stream=False), request_id="r")
    with capturing_provider_request(), pytest.raises(ProviderRequestCaptured) as stop:
        await unified_client.UnifiedAIClient()._execute_dispatch(request)
    assert stop.value.request["transport"] == "uncaptured"
    assert json.dumps(USER)[1:-1] in json.dumps(stop.value.request["body"])
