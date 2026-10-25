"""One agent turn on a person's own computer, through the REAL loop (L5 design R4, G6, G10).

The run resolves ``served_via`` to the one ``device_chat`` route, ``DeviceChat`` streams through
the relay transport to a fake relay (``httpx.MockTransport``), and the executor does the rest
exactly as for a cloud model:

* end to end — the device answers with the REAL recorded llama-server tool call
  (get_weather {"city": "Paris"}), the loop runs the server tool, the SECOND device call carries
  the tool result (role ``tool``, the device's own call id), and the answer streams out through
  the emitter;
* G10 — a stream that breaks after the tool call's bytes is surfaced typed (``stream_dropped``)
  and sent exactly ONCE: no retry, no reroute, the tool never runs, nothing else is dispatched;
* G6 — with ``store: false`` the same run writes nothing to the conversation store.

What each is FOR: re-enable the executor's same-model retry for device profiles and G10 sends
twice; drop the ``tool`` message from the second call and the end-to-end check fails.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any

import httpx
import pytest

from matrx_ai._ext import configure_ext

pytestmark = pytest.mark.usefixtures("client_host_sandbox")

from test_execute_with_store import FakeEmitter, InMemoryStore, StaticCatalog  # noqa: E402

FIXTURE = Path(__file__).parent.parent / "fixtures" / "device" / "llama-b9076-tool-call.sse"
RECORDED = FIXTURE.read_bytes()
DEVICE = "6f1c2a7e-3b9d-4c1e-8f0a-2d4b6c8e0a13"
MODEL_ID = str(uuid.uuid4())
TOOL = "get_weather"
TOOL_CALL_ID = "yRqVDjUOpU1DrYs62eJ03nRJHt0JY9EX"
ANSWER = "It is 18 °C and sunny in Paris."

_DEVICE_MODEL = {
    "id": MODEL_ID,
    "name": "qwen3.5-2b",
    "provider": "qwen",
    "metadata": {},
    "capabilities": {"input": ["text"], "output": ["text"], "features": ["function_calling"]},
}
WRITES = (
    "ensure_conversation_exists",
    "create_pending_user_request",
    "persist_completed_request",
    "log_tool_call_start",
    "log_tool_call_update",
)


def _answer_sse(text: str) -> bytes:
    """A llama-server text answer in the recorded stream's own shape, with include_usage."""
    rid, base = (
        "chatcmpl-device-answer",
        {"object": "chat.completion.chunk", "model": "Qwen3.5-2B-Q4_K_M.gguf"},
    )
    chunks = [
        {
            **base,
            "id": rid,
            "choices": [
                {"index": 0, "delta": {"role": "assistant", "content": None}, "finish_reason": None}
            ],
        },
        *[
            {
                **base,
                "id": rid,
                "choices": [{"index": 0, "delta": {"content": piece}, "finish_reason": None}],
            }
            for piece in (text[i : i + 6] for i in range(0, len(text), 6))
        ],
        {**base, "id": rid, "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}]},
        {
            **base,
            "id": rid,
            "choices": [],
            "usage": {"prompt_tokens": 340, "completion_tokens": 12, "total_tokens": 352},
        },
    ]
    return b"".join(f"data: {json.dumps(c)}\n\n".encode() for c in chunks) + b"data: [DONE]\n\n"


class _Body(httpx.AsyncByteStream):
    def __init__(self, data: bytes, break_after: int | None = None) -> None:
        self.data, self.break_after = data, break_after

    async def __aiter__(self):
        for at in range(0, len(self.data), 512):
            if self.break_after is not None and at >= self.break_after:
                raise httpx.RemoteProtocolError(
                    "peer closed connection without sending complete message body"
                )
            yield self.data[at : at + 512]


class FakeRelay:
    def __init__(self, *bodies: _Body) -> None:
        self.bodies = list(bodies)
        self.sent: list[dict[str, Any]] = []

    def handler(self, request: httpx.Request) -> httpx.Response:
        self.sent.append(json.loads(request.content))
        body = self.bodies.pop(0)
        return httpx.Response(200, headers={"content-type": "text/event-stream"}, stream=body)


class StreamingEmitter(FakeEmitter):
    def __init__(self) -> None:
        super().__init__()
        self.text: list[str] = []

    async def send_chunk(self, text: str) -> None:
        self.text.append(text)


@pytest.fixture
def weather_tool():
    from matrx_ai.tools.registry import ToolRegistry

    registry = ToolRegistry.get_instance()
    saved = (dict(registry._tools), dict(registry._tools_by_id), registry._loaded)
    ran: list[dict[str, Any]] = []

    async def _weather(args: dict[str, Any], ctx: Any) -> Any:
        from matrx_ai.tools.models import ToolResult

        ran.append(dict(args or {}))
        return ToolResult(
            success=True,
            tool_name=ctx.tool_name,
            output={"city": (args or {}).get("city"), "temperature_c": 18, "sky": "sunny"},
        )

    registry.register_local(
        TOOL,
        _weather,
        description="Get the current weather for a city",
        parameters={"city": {"type": "string", "description": "a city"}},
    )
    registry._loaded = True
    try:
        yield ran
    finally:
        registry._tools.clear()
        registry._tools.update(saved[0])
        registry._tools_by_id.clear()
        registry._tools_by_id.update(saved[1])
        registry._loaded = saved[2]


@pytest.fixture
def device(monkeypatch):
    from matrx_ai.catalog.device_placement import configure_device_placement
    from matrx_ai.providers.device.relay_transport import configure_device_relay

    placed: list[str] = []

    async def placement(served_via: Any, *, model_id: str) -> None:
        placed.append(model_id)
        return None

    def bind(*bodies: _Body) -> FakeRelay:
        fake = FakeRelay(*bodies)

        async def bearer(device_id: str, token: str) -> str:
            return f"bearer-{device_id}"

        configure_device_relay(
            url=lambda: "https://relay.test",
            bearer=bearer,
            http_transport=httpx.MockTransport(fake.handler),
        )
        return fake

    configure_device_placement(placement)
    yield bind
    configure_device_placement(None)
    configure_device_relay(url=None, bearer=None)


def _run_setup(*, store: bool, emitter: Any = None) -> tuple[InMemoryStore, StreamingEmitter]:
    from matrx_connect.context.app_context import AppContext, set_app_context

    conversation_store = InMemoryStore()
    configure_ext(
        conversation_store=conversation_store,
        model_catalog=StaticCatalog([_DEVICE_MODEL]),
        api_key_resolver=lambda name: "not-a-real-key",
    )
    emitter = emitter or StreamingEmitter()
    set_app_context(
        AppContext(
            emitter=emitter,
            user_id=str(uuid.uuid4()),
            request_id=str(uuid.uuid4()),
            conversation_id=str(uuid.uuid4()),
            store=store,
            token="person-jwt",
            source_app="client_host_tests",
            source_feature="test",
            metadata={},
        )
    )
    return conversation_store, emitter


def _config() -> Any:
    from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage

    return UnifiedConfig(
        model=MODEL_ID,
        served_via={"provider": "device", "app_instance_id": DEVICE, "local_model_id": MODEL_ID},
        tools=[TOOL],
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


@pytest.mark.asyncio
@pytest.mark.parametrize("store", [True, False])
async def test_one_device_turn_runs_a_server_tool_and_streams_the_answer(
    device, weather_tool, store
) -> None:
    from matrx_ai.orchestrator.executor import execute_ai_request

    relay = device(_Body(RECORDED), _Body(_answer_sse(ANSWER)))
    conversation_store, emitter = _run_setup(store=store)

    completed = await execute_ai_request(_config(), max_iterations=4)

    # The device's tool call ran on the server, once, with the device's arguments.
    assert weather_tool == [{"city": "Paris"}]
    assert len(relay.sent) == 2, f"{len(relay.sent)} device calls"
    for envelope in relay.sent:
        assert (envelope["cap"], envelope["op"]) == ("models", "llm.chat")
        assert envelope["params"]["model"] == "qwen3.5-2b"
        assert envelope["params"]["body"]["stream_options"] == {"include_usage": True}
    first, second = (e["params"]["body"]["messages"] for e in relay.sent)
    assert [t["function"]["name"] for t in relay.sent[0]["params"]["body"]["tools"]] == [TOOL]
    tool_messages = [m for m in second if m.get("role") == "tool"]
    assert len(tool_messages) == 1 and tool_messages[0]["tool_call_id"] == TOOL_CALL_ID
    assert "sunny" in json.dumps(tool_messages[0]["content"])
    assistant = [m for m in second if m.get("role") == "assistant"]
    assert assistant and assistant[-1]["tool_calls"][0]["id"] == TOOL_CALL_ID
    assert len(second) > len(first)

    # The answer streamed out through the emitter and ends the run.
    streamed = "".join(emitter.text)
    assert ANSWER in streamed
    last = list(completed.request.config.messages)[-1]
    assert last.role == "assistant"
    assert ANSWER in "".join(getattr(c, "text", "") or "" for c in last.content).strip()

    if store:
        # The same run with store on writes the gated rows (so G6 below can fail).
        for call in (
            "ensure_conversation_exists",
            "create_pending_user_request",
            "log_tool_call_start",
            "persist_completed_request",
        ):
            assert call in conversation_store.calls, f"stored device run never called {call}"
    else:
        # G6: store:false takes the executor's ephemeral branches for a device run exactly as
        # for a cloud one — no conversation gate, no pending request, no tool-call rows. The
        # CompletedRequest still reaches a CLIENT host's store (persistence.py delegates it
        # wholesale; that host owns store semantics); a server host's cx-row gate
        # (db/persistence.py ``_should_persist``) is provider-agnostic.
        written = [
            c for c in conversation_store.calls if c in WRITES and c != "persist_completed_request"
        ]
        assert written == [], f"store:false device run wrote {written}"


@pytest.mark.asyncio
async def test_g10_a_stream_that_breaks_after_tool_call_bytes_is_never_retried(
    device, weather_tool
) -> None:
    from matrx_ai.orchestrator.executor import execute_ai_request

    cut_at = RECORDED.index(b'"name":"get_weather"') + 600
    relay = device(_Body(RECORDED, break_after=cut_at), _Body(_answer_sse(ANSWER)))
    _run_setup(store=False)

    raised: BaseException | None = None
    completed = None
    try:
        completed = await execute_ai_request(_config(), max_iterations=4)
    except Exception as exc:  # noqa: BLE001 — the executor may raise or settle failed
        raised = exc

    assert len(relay.sent) == 1, "a device call that broke mid-answer was sent again"
    assert weather_tool == [], "a half-received tool call never runs"
    if raised is not None:
        info = getattr(raised, "error_info", None)
        assert getattr(info, "error_type", None) == "stream_dropped", repr(raised)
        assert info.is_retryable is False
    else:
        meta = completed.metadata or {}
        assert "stream_dropped" in json.dumps(meta, default=str), meta


# ── D3 / item 4: the error EVENT is typed; the person's state files nothing ───
class _ErrorEmitter(StreamingEmitter):
    def __init__(self) -> None:
        super().__init__()
        self.errors: list[dict[str, Any]] = []

    async def send_error(
        self,
        error_type: str,
        message: str,
        user_message: str | None = None,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.errors.append(
            {
                "error_type": error_type,
                "user_message": user_message,
                "code": code,
                "details": details,
            }
        )


def _relay_refusal(status: int, code: str) -> Any:
    return httpx.Response(
        status, json={"ok": False, "error": {"code": code, "message": "x", "retryable": False}}
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("scenario", "error_type", "reason", "files"),
    [
        ("offline", "device_offline", "DEVICE_OFFLINE", False),
        ("not_on_device", "model_not_on_device", "not_on_device", False),
        ("dropped", "stream_dropped", "body_broken", True),
    ],
)
async def test_the_error_event_carries_code_and_details_and_person_state_files_nothing(
    device, weather_tool, monkeypatch, scenario, error_type, reason, files
) -> None:
    from matrx_ai.catalog.device_placement import DevicePlacementRefusal, configure_device_placement
    from matrx_ai.orchestrator import executor
    from matrx_ai.orchestrator.executor import execute_ai_request

    filed: list[str] = []

    async def _capture(*args: Any, **kwargs: Any) -> None:
        info = kwargs.get("error_info") or next((a for a in args if hasattr(a, "error_type")), None)
        filed.append(str(getattr(info, "error_type", "?")))

    monkeypatch.setattr(executor, "_capture_terminal_provider_failure", _capture)
    relay = device(_Body(RECORDED, break_after=RECORDED.index(b'"name":"get_weather"') + 600))
    if scenario == "offline":
        relay.handler = lambda request: (
            relay.sent.append({}),
            _relay_refusal(503, "DEVICE_OFFLINE"),
        )[1]  # type: ignore[method-assign]
        from matrx_ai.providers.device.relay_transport import configure_device_relay

        async def bearer(device_id: str, token: str) -> str:
            return "b"

        configure_device_relay(
            url=lambda: "https://relay.test",
            bearer=bearer,
            http_transport=httpx.MockTransport(relay.handler),
        )
    if scenario == "not_on_device":

        async def refuse(served_via: Any, *, model_id: str) -> Any:
            return DevicePlacementRefusal(code="not_on_device", message="no file")

        configure_device_placement(refuse)
    emitter = _ErrorEmitter()
    _run_setup(store=False, emitter=emitter)

    try:
        await execute_ai_request(_config(), max_iterations=2)
    except Exception:  # noqa: BLE001 — some paths raise after emitting
        pass

    events = [e for e in emitter.errors if e["error_type"] == error_type]
    assert events, f"no {error_type} error event: {emitter.errors}"
    event = events[-1]
    assert event["code"] == error_type
    assert event["details"] and event["details"].get("code") == reason
    assert event["details"].get("provider") == "device"
    assert event["user_message"]
    assert (error_type in filed) is files, f"system_error capture: {filed}"


# ── store:false on the person's computer: NO side agent reaches a cloud model ──
@pytest.mark.asyncio
async def test_a_store_false_device_turn_dispatches_nothing_off_the_device(device, weather_tool, monkeypatch) -> None:
    from matrx_ai.orchestrator.executor import execute_ai_request
    from matrx_ai.providers.unified_client import UnifiedAIClient

    routes: list[str] = []
    real = UnifiedAIClient._dispatch_admitted

    async def spy(*args: Any, **kwargs: Any) -> Any:
        routes.append(str(getattr(kwargs.get("profile"), "route_kind", "?")))
        return await real(*args, **kwargs)

    monkeypatch.setattr(UnifiedAIClient, "_dispatch_admitted", staticmethod(spy))
    device(_Body(RECORDED), _Body(_answer_sse(ANSWER)))
    _run_setup(store=False)
    await execute_ai_request(_config(), max_iterations=4)
    assert routes and set(routes) == {"device"}, f"dispatches: {routes}"


@pytest.mark.asyncio
@pytest.mark.parametrize("store", [False, True])
async def test_the_diagram_repair_never_runs_for_a_store_false_device_turn(monkeypatch, store) -> None:
    """The visual-map repair child runs a cloud model (repair_model knob / bound agent)."""
    from types import SimpleNamespace

    from matrx_ai.orchestrator import visual_map_repair as vmr

    reached: list[str] = []
    monkeypatch.setattr(vmr, "_assistant_text_parts", lambda req, resp: reached.append("read") or [])
    request = SimpleNamespace(config=_config())
    ctx = SimpleNamespace(store=store, emitter=None)
    assert await vmr.visual_map_gate(request, None, ctx) == []
    assert (reached == []) is (not store), reached


def test_is_private_device_turn() -> None:
    from types import SimpleNamespace

    from matrx_ai.providers.device.route_guard import is_private_device_turn

    device_config = _config()
    assert is_private_device_turn(SimpleNamespace(store=False), device_config) is True
    assert is_private_device_turn(SimpleNamespace(store=True), device_config) is False
    assert is_private_device_turn(SimpleNamespace(store=False), SimpleNamespace(served_via=None)) is False


# ── an unsaved device turn adjusts no setting it did not change ──────────────
@pytest.mark.asyncio
@pytest.mark.parametrize("store", [False, True])
async def test_a_device_turn_announces_no_settings_adjustment_for_its_store_choice(
    device, weather_tool, monkeypatch, store
) -> None:
    """``store: false`` is the run's own unsaved choice. llama-server keeps nothing, so on the
    device route it is never a provider setting: dropping it changed nothing, and the person
    saw "Some settings were adjusted to fit qwen-3.5-2b" for it (L5 live walk, 2026-10-24)."""
    from matrx_ai.orchestrator.executor import execute_ai_request
    from matrx_ai.providers import outbound_params

    published: list[list[str]] = []
    real = outbound_params.publish_settings_adjustments

    def spy(adjustments, **kw):
        published.append([getattr(a, "key", "?") for a in adjustments])
        return real(adjustments, **kw)

    monkeypatch.setattr(outbound_params, "publish_settings_adjustments", spy)
    device(_Body(_answer_sse(ANSWER)))
    _run_setup(store=store)
    config = _config()
    config.tools = []
    config.store = store
    await execute_ai_request(config, max_iterations=1)
    assert all("store" not in keys for keys in published), f"adjusted: {published}"


# ── a cost-0 device turn is outside the AI usage limit ───────────────────────
@pytest.mark.asyncio
@pytest.mark.parametrize("state", ["near", "over"])
async def test_a_device_turn_is_never_gated_or_warned_by_the_usage_limit(
    device, weather_tool, monkeypatch, state
) -> None:
    """A person near (or over) their limit from cloud use still runs on their own computer: the
    device turn costs 0.0 (adds 0 points), is never refused, and shows no "You're close to your AI
    usage limit." (L5 live walk, 2026-10-24)."""
    from matrx_ai.orchestrator.executor import execute_ai_request
    from matrx_ai.providers import usage_gate

    told: list[str] = []
    monkeypatch.setattr(usage_gate, "_gated_person", lambda ctx: "person-1")
    monkeypatch.setattr(
        usage_gate, "_verdict_for",
        lambda uid: usage_gate.UsageVerdict(state=state, refuse=state == "over", enforced=True, usage={}),
    )

    async def _tell(ctx, verdict):
        told.append(verdict.state)

    monkeypatch.setattr(usage_gate, "_tell_near", _tell)
    relay = device(_Body(_answer_sse(ANSWER)))
    _run_setup(store=False)
    config = _config()
    config.tools = []
    completed = await execute_ai_request(config, max_iterations=1)
    assert len(relay.sent) == 1, "the device turn was refused by the usage limit"
    assert told == [], f"usage warning on a device turn: {told}"
    costs = [u.calculate_cost({}) for u in completed.iteration_usages() if u is not None] if hasattr(
        completed, "iteration_usages"
    ) else []
    assert all(c == 0.0 for c in costs), costs


# ── reasoning_effort on the device route is APPLIED as the template's own switch ─
@pytest.mark.asyncio
@pytest.mark.parametrize(("effort", "thinking"), [("none", False), ("high", True), (None, None)])
async def test_a_device_turns_reasoning_choice_reaches_llama_and_is_not_announced(
    device, weather_tool, monkeypatch, effort, thinking
) -> None:
    from matrx_ai.orchestrator.executor import execute_ai_request
    from matrx_ai.providers import outbound_params

    published: list[list[str]] = []
    real = outbound_params.publish_settings_adjustments

    def spy(adjustments, **kw):
        if kw.get("seam") == "chat":
            published.append([getattr(a, "key", "?") for a in adjustments])
        return real(adjustments, **kw)

    monkeypatch.setattr(outbound_params, "publish_settings_adjustments", spy)
    relay = device(_Body(_answer_sse(ANSWER)))
    _run_setup(store=True)
    config = _config()
    config.tools = []
    config.reasoning_effort = effort
    await execute_ai_request(config, max_iterations=1)
    body = relay.sent[0]["params"]["body"]
    if thinking is None:
        assert "chat_template_kwargs" not in body
    else:
        assert body["chat_template_kwargs"] == {"enable_thinking": thinking}
    assert "reasoning_effort" not in body
    assert all("reasoning_effort" not in keys for keys in published), published
