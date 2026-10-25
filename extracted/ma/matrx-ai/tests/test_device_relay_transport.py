"""A device_chat call streams through the relay's ``/stream`` contract, and every failure is typed.

L5 design REVISION 1, R3 (client side), R4, R5. The fake relay is an ``httpx.MockTransport``
bound through the host seam (``configure_device_relay(http_transport=...)``); it replays the REAL
recorded llama-server b9076 ``--jinja`` Qwen3.5-2B get_weather tool-call SSE from matrx-desktop
``test/fixtures/models/llama-b9076-tool-call.sse`` (copied to ``fixtures/device/``).

* G3  — the envelope, bearer, protocol header and forced ``stream``/``include_usage``; the real
        recorded stream parses into ``ToolCallContent(get_weather {"city": "Paris"})``, and a
        usage chunk becomes ``TokenUsage(api="device_chat")``.
* G4  — every relay answer maps to its typed device error, ``is_retryable=False``, plain words.
* G5  — device-served usage costs 0.0 with no pricing-miss alarm.
* G10 — a stream error after tool-call bytes is typed ``stream_dropped`` and sent ONCE
        (the loop-level half is in ``client_host/test_device_chat_loop.py``).

What each is FOR: replace ``RelayStreamTransport`` with the SDK's own transport and G3 dials
``device.invalid``; drop the ``[DONE]`` check and the cut stream "succeeds"; drop
``_OWNS_EVERY_FAILURE`` and a hop break reads as a retryable ``connection_error``; drop the
``device_served`` branch and G5 screams a pricing miss.
"""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import httpx
import pytest

from matrx_ai.config.served_via import ServedVia

FIXTURE = Path(__file__).parent / "fixtures" / "device" / "llama-b9076-tool-call.sse"
RECORDED = FIXTURE.read_bytes()
DEVICE = "6f1c2a7e-3b9d-4c1e-8f0a-2d4b6c8e0a13"
MODEL_ID = "2c4e6a80-9b1d-4f3e-8a5c-7e9f1b3d5a70"
MODEL_KEY = "qwen3.5-2b"
RELAY = "https://relay.test"
PERSON_TOKEN = "person-jwt"
TOOL_CALL_ID = "yRqVDjUOpU1DrYs62eJ03nRJHt0JY9EX"
#: The terminal usage chunk llama-server adds under stream_options.include_usage (the recorded
#: fixture was captured without it; this chunk is the OpenAI-spec shape, appended by the test).
USAGE_CHUNK = (
    b'data: {"choices":[],"created":1792634414,"id":"chatcmpl-DgY5VSYJEsPTpaygVNV1JmwvCuM21MSB",'
    b'"model":"Qwen3.5-2B-Q4_K_M.gguf","object":"chat.completion.chunk",'
    b'"usage":{"completion_tokens":65,"prompt_tokens":291,"total_tokens":356}}\n\n'
)
DONE = b"data: [DONE]\n\n"
WITH_USAGE = RECORDED.replace(DONE, USAGE_CHUNK + DONE)
assert WITH_USAGE != RECORDED, "the fixture's terminal [DONE] moved"


class _Chunked(httpx.AsyncByteStream):
    """Bytes in small pieces (a boundary can split ``data: [DONE]``), optionally breaking."""

    def __init__(self, data: bytes, *, size: int = 777, break_after: int | None = None) -> None:
        self._data, self._size, self._break = data, size, break_after

    async def __aiter__(self):
        for at in range(0, len(self._data), self._size):
            if self._break is not None and at >= self._break:
                raise httpx.ReadError("connection reset by relay")
            yield self._data[at : at + self._size]


class FakeRelay:
    """The relay's /stream: records every request; answers what the test scripted."""

    def __init__(self, *answers: Any) -> None:
        self.answers = list(answers)
        self.requests: list[httpx.Request] = []

    def handler(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        answer = self.answers.pop(0) if len(self.answers) > 1 else self.answers[0]
        return answer() if callable(answer) else answer

    @property
    def bodies(self) -> list[dict[str, Any]]:
        return [json.loads(r.content) for r in self.requests]


def sse(data: bytes, **kw: Any) -> Any:
    return lambda: httpx.Response(
        200,
        headers={
            "content-type": "text/event-stream",
            "x-matrx-stream-result": json.dumps(
                {"model": MODEL_KEY, "content_type": "text/event-stream"}
            ),
        },
        stream=_Chunked(data, **kw),
    )


def refusal(status: int, code: str, message: str, reason: str | None = None) -> Any:
    error: dict[str, Any] = {"code": code, "message": message, "retryable": False}
    if reason:
        error["data"] = {"reason": reason}
    return lambda: httpx.Response(status, json={"ok": False, "error": error})


def sse_error_block(code: str, message: str) -> bytes:
    payload = {"error": {"type": "device_stream_error", "code": code, "message": message}}
    return f"event: error\ndata: {json.dumps(payload)}\n\n".encode()


@pytest.fixture
def relay():
    from matrx_ai.providers.device.relay_transport import configure_device_relay

    bearers: list[tuple[str, str]] = []

    def bind(*answers: Any) -> FakeRelay:
        fake = FakeRelay(*answers)

        async def bearer(device_id: str, token: str) -> str:
            bearers.append((device_id, token))
            return f"bearer-for-{device_id}"

        configure_device_relay(
            url=lambda: RELAY, bearer=bearer, http_transport=httpx.MockTransport(fake.handler)
        )
        fake.bearers = bearers  # type: ignore[attr-defined]
        return fake

    yield bind
    configure_device_relay(url=None, bearer=None)


@pytest.fixture
def ambient():
    from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

    class Emitter:
        def __init__(self) -> None:
            self.chunks: list[str] = []

        async def send_chunk(self, text: str) -> None:
            self.chunks.append(text)

        def __getattr__(self, name: str):
            async def _noop(*a: Any, **k: Any) -> None:
                return None

            return _noop

    emitter = Emitter()
    bound = set_app_context(
        AppContext(
            emitter=emitter, user_id="u-1", request_id="r-1", token=PERSON_TOKEN, metadata={}
        )
    )
    yield emitter
    clear_app_context(bound)


def _profile(**kw: Any) -> Any:
    from matrx_ai.catalog.host_catalog import _fallback_controls
    from matrx_ai.testing.profile_factory import make_profile

    base = make_profile(
        model_name="qwen3.5-2b",
        wire_format="device_chat",
        vendor="device",
        provider_model_id=kw.pop("provider_model_id", MODEL_KEY),
        controls=_fallback_controls("generic_openai_chat"),
        capabilities={"input": ["text"], "output": ["text"], "features": ["function_calling"]},
    )
    served_via = kw.pop(
        "served_via",
        ServedVia.model_validate(
            {"provider": "device", "app_instance_id": DEVICE, "local_model_id": MODEL_ID}
        ),
    )
    return base.model_copy(
        update={"route_kind": "device", "served_via": served_via, "model_id": MODEL_ID, **kw}
    )


def _config(stream: bool = True) -> Any:
    from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage

    return UnifiedConfig(
        model=MODEL_ID,
        stream=stream,
        messages=MessageList(
            _messages=[
                UnifiedMessage(
                    role="user",
                    content=[
                        TextContent(text="What is the weather in Paris? Use the get_weather tool.")
                    ],
                )
            ]
        ),
    )


async def _run(stream: bool = True, **profile_kw: Any) -> Any:
    from matrx_ai.providers.device import DeviceChat

    return await DeviceChat().execute(_config(stream), _profile(**profile_kw))


# ── G3 ───────────────────────────────────────────────────────────────────────
@pytest.mark.asyncio
@pytest.mark.parametrize("stream", [True, False])
async def test_g3_the_relay_envelope_bearer_and_forced_streaming(relay, ambient, stream) -> None:
    fake = relay(sse(WITH_USAGE))
    await _run(stream=stream)

    assert len(fake.requests) == 1
    sent = fake.requests[0]
    assert str(sent.url) == f"{RELAY}/v1/devices/{DEVICE}/stream"
    assert sent.method == "POST"
    assert sent.headers["authorization"] == f"Bearer bearer-for-{DEVICE}"
    assert sent.headers["x-matrx-protocol-version"] == "1.76"
    assert fake.bearers == [(DEVICE, PERSON_TOKEN)], "the bearer comes from the PERSON's token"
    envelope = fake.bodies[0]
    assert set(envelope) == {"cap", "op", "params", "first_byte_timeout_ms", "idle_timeout_ms"}
    assert (envelope["cap"], envelope["op"]) == ("models", "llm.chat")
    assert envelope["first_byte_timeout_ms"] == 300_000 and envelope["idle_timeout_ms"] == 120_000
    params = envelope["params"]
    assert set(params) == {"model", "body", "start_if_stopped"}
    assert params["model"] == MODEL_KEY and params["start_if_stopped"] is True
    assert params["body"]["stream"] is True, "a device run is always streamed"
    assert params["body"]["stream_options"] == {"include_usage": True}
    assert params["body"]["messages"][-1]["role"] == "user"


@pytest.mark.asyncio
async def test_g3_the_real_recorded_tool_call_stream_parses(relay, ambient) -> None:
    from matrx_ai.config import ThinkingContent, ToolCallContent

    relay(sse(WITH_USAGE))
    response = await _run()

    content = response.messages[0].content
    calls = [c for c in content if isinstance(c, ToolCallContent)]
    assert len(calls) == 1
    assert (calls[0].id, calls[0].name, calls[0].arguments) == (
        TOOL_CALL_ID,
        "get_weather",
        {"city": "Paris"},
    )
    assert any(isinstance(c, ThinkingContent) for c in content), "reasoning_content kept"
    assert str(response.finish_reason).lower().endswith("tool_calls")
    usage = response.usage
    assert (usage.input_tokens, usage.output_tokens) == (291, 65)
    assert usage.api == "device_chat"
    assert usage.metadata["device_served"] is True
    assert usage.metadata["served_via"] == {"provider": "device", "app_instance_id": DEVICE}
    assert "".join(ambient.chunks).startswith("<reasoning>"), "the answer streamed to the emitter"


@pytest.mark.asyncio
async def test_g3_the_recorded_stream_without_usage_is_loud_never_invented(
    relay, ambient, monkeypatch
) -> None:
    from matrx_ai.providers.generic_openai import generic_openai_api

    titles: list[str] = []
    real = generic_openai_api.vcprint
    monkeypatch.setattr(
        generic_openai_api,
        "vcprint",
        lambda data=None, title="", *a, **k: (
            titles.append(str(title)),
            real(data, title, *a, **k),
        ),
    )
    relay(sse(RECORDED))
    response = await _run()
    assert response.usage is None, "no usage chunk → no invented token counts"
    assert any("STREAM USAGE MISSING" in t for t in titles)


@pytest.mark.asyncio
async def test_g3_no_target_or_no_relay_sends_nothing(relay, ambient) -> None:
    from matrx_ai.providers.device import DeviceChat
    from matrx_ai.providers.device.errors import DeviceInvalidRequestError, DeviceOfflineError
    from matrx_ai.providers.device.relay_transport import configure_device_relay

    fake = relay(sse(WITH_USAGE))
    with pytest.raises(DeviceInvalidRequestError):
        await DeviceChat().execute(
            _config(), SimpleNamespace(route_kind="offering", served_via=None)
        )
    with pytest.raises(DeviceInvalidRequestError):  # an own file: the key is minted on the device
        await DeviceChat().execute(
            _config(),
            _profile(
                served_via=ServedVia.model_validate(
                    {
                        "provider": "device",
                        "app_instance_id": DEVICE,
                        "local_model_id": "9d2e4f60-1a3b-4c5d-8e7f-0a1b2c3d4e5f",
                    }
                )
            ),
        )
    assert fake.requests == []
    configure_device_relay(url=None, bearer=None)
    with pytest.raises(DeviceOfflineError) as raised:
        await _run()
    assert raised.value.error_info.details["reason"] == "relay_not_wired"


# ── G4 ───────────────────────────────────────────────────────────────────────
CASES = [
    (refusal(503, "DEVICE_OFFLINE", "device is offline"), "device_offline"),
    (refusal(504, "TIMEOUT", "no answer within 300000 ms"), "device_timeout"),
    (
        refusal(
            404,
            "NOT_FOUND",
            "qwen3.5-2b is not running on this computer. Start it in Models › This computer.",
            "model_not_running",
        ),
        "model_not_running",
    ),
    (
        refusal(
            502,
            "RESOURCE_GONE",
            "The model server on this computer did not answer.",
            "model_server_unreachable",
        ),
        "model_not_running",
    ),
    (refusal(409, "RESOURCE_BUSY", "llama-3 runs on this computer, not qwen3.5-2b."), "model_busy"),
    (
        refusal(400, "INVALID_PARAMS", "The model server refused the request: tools unsupported"),
        "device_invalid_request",
    ),
    (refusal(401, "AUTH_EXPIRED", "token expired"), "auth_expired"),
    (refusal(403, "AUTH_FORBIDDEN", "not this device's owner"), "device_access_denied"),
    (refusal(502, "INTERNAL", "boom"), "device_failed"),
    (
        sse(
            RECORDED.split(b'"tool_calls"')[0].rsplit(b"data: ", 1)[0]
            + sse_error_block("INTERNAL", "the device ended the stream (error)")
        ),
        "stream_dropped",
    ),
    (sse(RECORDED.replace(DONE, b"")), "stream_dropped"),
    (sse(RECORDED, break_after=4000), "stream_dropped"),
]


@pytest.mark.asyncio
@pytest.mark.parametrize(("answer", "error_type"), CASES)
async def test_g4_every_relay_answer_is_one_typed_device_error(
    relay, ambient, answer, error_type
) -> None:
    from matrx_ai.providers.device.classify import USER_MESSAGES
    from matrx_ai.providers.device.errors import DEVICE_ERROR_TYPES, DeviceRouteError

    fake = relay(answer)
    with pytest.raises(DeviceRouteError) as raised:
        await _run()
    info = raised.value.error_info
    assert info.error_type == error_type
    assert info.error_type in DEVICE_ERROR_TYPES
    assert info.is_retryable is False
    assert info.error_type not in ("server_error", "overloaded", "rate_limit", "connection_error")
    assert info.user_message and info.user_message.strip()[-1] in ".?!"
    assert info.user_message in USER_MESSAGES.values() or error_type in (
        "model_not_running",
        "model_busy",
    )
    assert len(fake.requests) == 1, "a device call is sent once"


@pytest.mark.asyncio
async def test_g4_the_shared_classifier_types_a_device_failure_too() -> None:
    import openai

    from matrx_ai.providers.errors import _PROVIDER_CLASSIFIERS, classify_provider_error

    assert "device" in _PROVIDER_CLASSIFIERS
    request = httpx.Request("POST", "https://device.invalid/v1/chat/completions")
    # A hop break the shared pass would read as a retryable connection error.
    info = classify_provider_error("device", httpx.ConnectError("refused", request=request))
    assert (info.error_type, info.is_retryable) == ("device_offline", False)
    wrapped = openai.APIConnectionError(request=request)
    info = classify_provider_error("device", wrapped)
    assert (info.error_type, info.is_retryable) == ("device_offline", False)
    status = openai.APIStatusError(
        "Error code: 409",
        response=httpx.Response(409, request=request),
        body={
            "ok": False,
            "error": {"code": "RESOURCE_BUSY", "message": "llama-3 runs here", "retryable": False},
        },
    )
    info = classify_provider_error("device", status)
    assert (info.error_type, info.is_retryable, info.user_message) == (
        "model_busy",
        False,
        "llama-3 runs here",
    )


# ── G10 ──────────────────────────────────────────────────────────────────────
@pytest.mark.asyncio
async def test_g10_an_error_after_tool_call_bytes_is_typed_and_sent_once(relay, ambient) -> None:
    from matrx_ai.providers.device.errors import DeviceStreamDroppedError
    from matrx_ai.providers.device.route_guard import may_retry_provider_error

    cut = RECORDED.split(b'"finish_reason":"tool_calls"')[0].rsplit(b"data: ", 1)[0]
    assert b'"name":"get_weather"' in cut, "the tool call's bytes were sent before the error"
    fake = relay(sse(cut + sse_error_block("TIMEOUT", "the device sent nothing for 120000 ms")))
    with pytest.raises(DeviceStreamDroppedError) as raised:
        await _run()
    assert raised.value.error_info.details["relay_code"] == "TIMEOUT"
    assert may_retry_provider_error(_profile(), raised.value.error_info) is False
    assert len(fake.requests) == 1


# ── G5 ───────────────────────────────────────────────────────────────────────
def test_g5_device_served_usage_costs_zero_with_no_pricing_miss(capsys) -> None:
    from matrx_ai.config import usage_config
    from matrx_ai.config.usage_config import TokenUsage

    usage = TokenUsage(
        input_tokens=291,
        output_tokens=65,
        matrx_model_name="qwen3.5-2b",
        api="device_chat",
        metadata={"device_served": True},
    )
    usage.offering_id = f"device:{DEVICE}"
    misses: list[tuple[str, str]] = []
    original = usage_config._pricing_miss
    usage_config._pricing_miss = lambda m, a: misses.append((m, a))  # type: ignore[assignment]
    try:
        assert usage.calculate_cost({}) == 0.0
        assert usage.calculate_catalog_cost({}) == 0.0
    finally:
        usage_config._pricing_miss = original  # type: ignore[assignment]
    assert misses == [], "a device-served call has no price to miss"
    out = capsys.readouterr().out
    assert out.count("device-served") == 1
    # The same usage NOT device-served is a real, loud miss (the guard can fail).
    cloud = TokenUsage(input_tokens=1, output_tokens=1, matrx_model_name="qwen3.5-2b", api="groq")
    usage_config._pricing_miss = lambda m, a: misses.append((m, a))  # type: ignore[assignment]
    try:
        cloud.calculate_cost({})
    finally:
        usage_config._pricing_miss = original  # type: ignore[assignment]
    assert misses == [("qwen3.5-2b", "groq")]


# ── a person's own uncatalogued file: the device's own key rides the envelope ──
OWN_FILE = "9d2e4f60-1a3b-4c5d-8e7f-0a1b2c3d4e5f"
OWN_KEY = "own-my-finetune-3fa9c2d1"


@pytest.mark.asyncio
async def test_an_own_file_runs_under_the_key_its_computer_minted(relay, ambient) -> None:
    from matrx_ai.catalog import device_placement
    from matrx_ai.catalog.resolve import resolve_call_profile
    from matrx_ai.db.ai_models.ai_model_manager import ai_model_manager_instance
    from matrx_ai.providers.device import DeviceChat

    sv = ServedVia.model_validate(
        {"provider": "device", "app_instance_id": DEVICE, "local_model_id": OWN_FILE}
    )

    async def check(_sv: Any, *, model_id: str) -> Any:
        return device_placement.DeviceOwnFile(
            file_id=OWN_FILE, name="my-finetune.gguf", metadata={}, model_key=OWN_KEY
        )

    async def no_model(_ref: str) -> Any:
        return None

    original = ai_model_manager_instance.load_model
    ai_model_manager_instance.load_model = no_model  # type: ignore[method-assign]
    device_placement.configure_device_placement(check)
    try:
        profile = await resolve_call_profile(OWN_FILE, served_via=sv)
    finally:
        device_placement.configure_device_placement(None)
        ai_model_manager_instance.load_model = original  # type: ignore[method-assign]
    assert profile.provider_model_id == OWN_KEY
    assert profile.offering_metadata["device_facts"]["model_key"] == {
        "value": OWN_KEY, "source": "device_reported"
    }
    fake = relay(sse(WITH_USAGE))
    await DeviceChat().execute(_config(), profile)
    assert fake.bodies[0]["params"]["model"] == OWN_KEY


@pytest.mark.asyncio
async def test_an_own_file_with_no_minted_key_is_refused_never_guessed(relay, ambient) -> None:
    from matrx_ai.providers.device import DeviceChat
    from matrx_ai.providers.device.errors import DeviceInvalidRequestError

    fake = relay(sse(WITH_USAGE))
    own = ServedVia.model_validate(
        {"provider": "device", "app_instance_id": DEVICE, "local_model_id": OWN_FILE}
    )
    with pytest.raises(DeviceInvalidRequestError):
        await DeviceChat().execute(_config(), _profile(
            served_via=own, provider_model_id=OWN_FILE, model_id=OWN_FILE,
            offering_metadata={"device_facts": {"source": "device_model_file"}},
        ))
    assert fake.requests == []


@pytest.mark.asyncio
async def test_an_own_file_with_a_catalog_dropped_run_key_is_sent_as_published(relay, ambient) -> None:
    """A download the catalog later dropped runs under its folder run key (no `own-` prefix)."""
    from matrx_ai.providers.device import DeviceChat

    fake = relay(sse(WITH_USAGE))
    own = ServedVia.model_validate(
        {"provider": "device", "app_instance_id": DEVICE, "local_model_id": OWN_FILE}
    )
    await DeviceChat().execute(_config(), _profile(
        served_via=own, provider_model_id="qwen3.5-2b-q4_k_m", model_id=OWN_FILE,
        offering_metadata={"device_facts": {
            "source": "device_model_file",
            "model_key": {"value": "qwen3.5-2b-q4_k_m", "source": "device_reported"},
        }},
    ))
    assert fake.bodies[0]["params"]["model"] == "qwen3.5-2b-q4_k_m"


# ── model_busy carries the chat the device names ─────────────────────────────
@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("message", "data", "expected"),
    [
        ("", {"reason": "busy_with_another_chat", "chat_title": "Trip to Lisbon"},
         "Your computer is busy with another chat (Trip to Lisbon)."),
        ("Matrx 2 is answering “Trip to Lisbon” on this computer. Try again when it finishes.",
         {"reason": "busy_with_another_chat", "chat_title": "Trip to Lisbon"},
         "Matrx 2 is answering “Trip to Lisbon” on this computer. Try again when it finishes."),
        ("", {"reason": "busy_with_another_chat"}, "Your computer is busy with another chat right now."),
    ],
)
async def test_model_busy_says_which_chat_the_computer_is_busy_with(relay, ambient, message, data, expected) -> None:
    from matrx_ai.providers.device.errors import ModelBusyError

    error = {"code": "RESOURCE_BUSY", "message": message, "retryable": False, "data": data}
    relay(lambda: httpx.Response(409, json={"ok": False, "error": error}))
    with pytest.raises(ModelBusyError) as raised:
        await _run()
    info = raised.value.error_info
    assert info.user_message == expected
    assert info.details["reason"] == "busy_with_another_chat"
    assert info.details["code"] == "busy_with_another_chat"
    assert info.details["busy_with"] == data.get("chat_title")

def _contract() -> dict:
    """The pinned device-model contract, read from the package both sides test against."""
    import json
    from pathlib import Path

    path = Path(__file__).resolve().parents[3] / "apps" / "shared" / "desktop-protocol" / "fixtures" / "device-model-contract.json"
    return json.loads(path.read_text())



@pytest.mark.asyncio
async def test_the_pinned_busy_error_names_its_chat_and_nothing_else_does(relay, ambient) -> None:
    from matrx_ai.providers.device.errors import ModelBusyError

    pinned = _contract()["busy_error"]
    relay(lambda: httpx.Response(409, json={"ok": False, "error": {**pinned, "message": ""}}))
    with pytest.raises(ModelBusyError) as raised:
        await _run()
    info = raised.value.error_info
    assert info.details["reason"] == pinned["data"]["reason"] == "busy_with_another_chat"
    assert info.details["busy_with"] == pinned["data"]["chat_title"]
    assert pinned["data"]["chat_title"] in info.user_message
    # A name the contract does not pin is not read.
    relay(lambda: httpx.Response(409, json={"ok": False, "error": {"code": "RESOURCE_BUSY", "message": "", "retryable": True, "data": {"reason": "busy_with_another_chat", "chat_name": "Guessed"}}}))
    with pytest.raises(ModelBusyError) as guessed:
        await _run()
    assert guessed.value.error_info.details["busy_with"] is None


def test_the_envelope_carries_the_conversations_title_as_pinned_and_only_when_there_is_one() -> None:
    from matrx_ai.providers.device.device_api import real_conversation_title
    from matrx_ai.providers.device.relay_transport import DeviceCallTarget, relay_stream_envelope

    pinned = _contract()["chat_request"]["params"]
    titled = DeviceCallTarget(device_id="d", model_key=pinned["model"], token="t", chat_title=pinned["chat_title"])
    params = relay_stream_envelope(titled, pinned["body"])["params"]
    assert params["chat_title"] == pinned["chat_title"]
    assert set(params) == set(pinned)  # exactly the pinned names, nothing else
    untitled = DeviceCallTarget(device_id="d", model_key=pinned["model"], token="t")
    assert "chat_title" not in relay_stream_envelope(untitled, pinned["body"])["params"]
    # A placeholder is not a title: it is never sent.
    assert real_conversation_title("Auto: Brand discovery") is None
    assert real_conversation_title("  ") is None
    assert real_conversation_title("Trip planning") == "Trip planning"


# ── chat_title only reaches a device that declares protocol 1.92+ ────────────
@pytest.mark.parametrize(
    ("version", "expected"),
    [("1.92", True), ("1.93", True), ("1.100", True), ("2.0", True), ("1.91", False), ("1.9", False), ("", False), (None, False), ("x.y", False), ("1.92.1", False)],
)
def test_only_a_well_formed_1_92_or_newer_counts(version, expected) -> None:
    from matrx_ai.providers.device.relay_transport import CHAT_TITLE_SINCE, version_at_least

    assert version_at_least(version, CHAT_TITLE_SINCE) is expected


def test_the_first_user_message_names_a_chat_with_no_title() -> None:
    from types import SimpleNamespace as NS

    from matrx_ai.providers.device.device_api import first_user_preview

    assert first_user_preview([NS(role="system", content="be nice"), NS(role="user", content="  Plan a   trip\nto Lisbon  ")]) == "Plan a trip to Lisbon"
    long = "Plan a really long trip around the whole of Portugal with stops in every small coastal village we can find please"
    preview = first_user_preview([NS(role="user", content=long)])
    assert preview is not None and preview.endswith("…") and len(preview) <= 61 and long.startswith(preview[:-1].rstrip())
    assert first_user_preview([NS(role="assistant", content="hi")]) is None
    assert first_user_preview([NS(role="user", content="   ")]) is None
    assert first_user_preview(None) is None


@pytest.mark.asyncio
@pytest.mark.parametrize(("declared", "sent"), [("1.92", True), ("1.95", True), ("1.91", False), (None, False)])
async def test_chat_title_is_sent_only_to_a_device_that_declares_1_92(relay, ambient, declared, sent) -> None:
    from matrx_ai.providers.device import relay_transport

    fake = relay(sse(WITH_USAGE))

    async def peer_version(device_id: str, token: str) -> str | None:
        return declared

    relay_transport._seam.peer_version = peer_version
    await _run()
    params = fake.bodies[0]["params"]
    assert ("chat_title" in params) is sent
    if sent:  # no stored title in a unit test: the first user message names the chat, never a generic label
        assert params["chat_title"] and params["chat_title"].lower() != "untitled"


@pytest.mark.asyncio
async def test_a_device_status_that_cannot_be_read_sends_no_title_and_the_chat_still_runs(relay, ambient) -> None:
    from matrx_ai.providers.device import relay_transport

    fake = relay(sse(WITH_USAGE))

    async def broken(device_id: str, token: str) -> str | None:
        raise RuntimeError("relay status down")

    relay_transport._seam.peer_version = broken
    await _run()
    assert "chat_title" not in fake.bodies[0]["params"]


# ── llama-server's context refusal is typed, with its own token counts ───────
LLAMA_400 = json.loads((FIXTURE.parent / "llama-400-exceed-context.json").read_text())


def _device_refusal_of(llama_body: dict[str, Any]) -> dict[str, Any]:
    """What the device answers for llama's 400 (core/capabilities/python/llm-chat.ts llamaRefusal:
    INVALID_PARAMS, "The model server refused the request: <llama's message>")."""
    message = f"The model server refused the request: {llama_body['error']['message']}"
    return {"code": "INVALID_PARAMS", "message": message[:300], "retryable": False}


@pytest.mark.asyncio
@pytest.mark.parametrize("phase", ["before_response", "sse_error"])
async def test_a_context_window_too_small_is_typed_with_its_token_counts(relay, ambient, phase) -> None:
    from matrx_ai.providers.device.errors import DeviceContextTooSmallError
    from matrx_ai.providers.device.route_guard import may_retry_provider_error

    refusal_body = _device_refusal_of(LLAMA_400)
    if phase == "before_response":
        fake = relay(lambda: httpx.Response(400, json={"ok": False, "error": refusal_body}))
    else:
        fake = relay(sse(sse_error_block(refusal_body["code"], refusal_body["message"])))
    with pytest.raises(DeviceContextTooSmallError) as raised:
        await _run()
    info = raised.value.error_info
    assert info.error_type == "device_context_too_small"
    assert info.is_retryable is False
    assert info.details["needed_tokens"] == 9851 and info.details["window_tokens"] == 4096
    assert info.user_message == (
        "This chat needs about 9851 tokens; your computer runs this model with a "
        "4096-token window. Raise it in Matrx 2 › Models › This computer › Options… › Context window."
    )
    assert may_retry_provider_error(_profile(), info) is False
    assert len(fake.requests) == 1, "sent once, never moved"
