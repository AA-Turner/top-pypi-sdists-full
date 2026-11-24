"""THE STATIC SEAL NEVER TOUCHES THE SEND (owner's rule, ``common-docs/systems/agents/agent-harness/projects/prompt-blocks-static-seal/VISION.md``,
2026-11-13): a real request must never fail, slow meaningfully, or change because of this project.

Every send here is REAL: the provider's own translator builds the request (stamping the line), the
provider's own SDK client sends it, and the bytes are read where they leave — an httpx
``MockTransport`` for Anthropic, OpenAI Responses and chat completions, genai's last pre-transport
step for Google, a stubbed xAI chat (the request proto the stub would send). All inside a
conversation and an agent loop, so every observer runs.

The baseline is the same send with every observer patched to a no-op. Then each piece the seal
added is made to raise in turn — ``RuntimeError``, ``TypeError``, ``RecursionError``,
``MemoryError`` — and each send must complete with bytes IDENTICAL to the baseline. Hostile
inputs (NaN, an 8 MB body, 2000-deep schema nesting, non-string slot keys) behave exactly as they
would with the observers off (and the deep schema exactly as before P0.2's canonical order). The
inline hook is measured, not guessed.
"""

from __future__ import annotations

import asyncio
import copy
import json
import logging
import math
import statistics
import time
from collections.abc import Callable
from typing import Any

import pytest
from xai_sdk.proto import chat_pb2

from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.send_boundary import order_for_wire, reset_loop_state
from matrx_ai.orchestrator.execution_state import (
    ExecutionState,
    clear_execution_state,
    set_execution_state,
)
from matrx_ai.providers import final_outbound_snapshot as fos
from matrx_ai.providers import request_capture, residual_check
from matrx_ai.providers.outbound_capture import CallMeta, make_capture_http_client, set_call_meta
from matrx_ai.providers.sdk_drift import route_undeclared_params
from matrx_ai.testing.profile_factory import make_profile
from matrx_ai.tools import declaration_ledger


@pytest.fixture(autouse=True)
def _call_meta_never_leaks() -> Any:
    """Sync sends here stamp the provider call metadata (a ContextVar) on the test's own context;
    without this a later test in the same process inherits it (test_outbound_capture's fallback
    test read "anthropic" instead of "unknown")."""
    from matrx_ai.providers import outbound_capture

    token = outbound_capture._call_meta_var.set(None)
    yield
    outbound_capture._call_meta_var.reset(token)


@pytest.fixture(autouse=True)
def _seal_check_switched_on(monkeypatch):
    """These tests prove the check itself; production starts it off (knob seal_check_on = 0)."""
    from matrx_ai.providers import final_outbound_snapshot as _fos

    monkeypatch.setattr(_fos, "seal_check_on", lambda: True)


CONV = "33333333-4444-5555-6666-777777777777"
SYSTEM = "You are a careful assistant."
TEMPLATE = "Write the brief for this request:\n"
TYPED = "What should I post on Friday?"
MARK = "<live_date>It is now 09:00.</live_date>"
ERRORS = [RuntimeError, TypeError, RecursionError, MemoryError]

# shape -> (translator module, class, wire format, provider)
SHAPES: dict[str, tuple[str, str, str, str]] = {
    "anthropic": ("matrx_ai.providers.anthropic.translator", "AnthropicTranslator", "anthropic_chat", "anthropic"),
    "responses": ("matrx_ai.providers.openai.translator", "OpenAITranslator", "openai_responses", "openai"),
    "chat": ("matrx_ai.providers.generic_openai.translator", "GenericOpenAITranslator", "openai_chat", "openai"),
    "genai": ("matrx_ai.providers.google.translator", "GoogleTranslator", "google_chat", "google"),
    "xai": ("matrx_ai.providers.xai.translator", "XAITranslator", "xai_chat", "xai"),
}
FOS_SHAPE = {
    "anthropic": fos.SHAPE_ANTHROPIC,
    "responses": fos.SHAPE_RESPONSES,
    "chat": fos.SHAPE_CHAT,
    "genai": fos.SHAPE_GOOGLE,
    "xai": fos.SHAPE_XAI,
}
REPLIES: dict[str, dict[str, Any]] = {
    "anthropic": {
        "id": "msg_1",
        "type": "message",
        "role": "assistant",
        "model": "m",
        "content": [{"type": "text", "text": "ok"}],
        "stop_reason": "end_turn",
        "stop_sequence": None,
        "usage": {"input_tokens": 1, "output_tokens": 1},
    },
    "responses": {
        "id": "resp_1",
        "object": "response",
        "created_at": 0,
        "model": "m",
        "status": "completed",
        "output": [
            {
                "type": "message",
                "id": "m1",
                "role": "assistant",
                "status": "completed",
                "content": [{"type": "output_text", "text": "ok", "annotations": []}],
            }
        ],
        "parallel_tool_calls": False,
        "tool_choice": "auto",
        "tools": [],
    },
    "chat": {
        "id": "c1",
        "object": "chat.completion",
        "created": 0,
        "model": "m",
        "choices": [{"index": 0, "message": {"role": "assistant", "content": "ok"}, "finish_reason": "stop"}],
    },
    "genai": {"candidates": [{"content": {"role": "model", "parts": [{"text": "ok"}]}, "finishReason": "STOP"}]},
}
URLS = {
    "anthropic": "https://api.anthropic.com",
    "responses": "https://api.openai.com/v1",
    "chat": "https://api.openai.com/v1",
}


class _Ctx:
    """The run's AppContext: a saved conversation turn of an agent (never a side run)."""

    conversation_id = CONV
    request_id = "req-1"
    agent_id = "agent-1"
    ai_watch = False
    emitter = None
    store = True
    system_run = False

    def __init__(self) -> None:
        self.metadata: dict[str, Any] = {}


@pytest.fixture(autouse=True)
def _run(monkeypatch: pytest.MonkeyPatch) -> Any:
    """A conversation and an agent-loop context around every send; clean seal state."""
    fos.reset_for_tests()
    declaration_ledger.reset_for_tests()
    reset_loop_state(CONV)
    ctx = _Ctx()
    monkeypatch.setattr("matrx_connect.context.app_context.try_get_app_context", lambda: ctx)
    token = set_execution_state(ExecutionState())
    yield ctx
    clear_execution_state(token)
    fos.reset_for_tests()
    declaration_ledger.reset_for_tests()
    reset_loop_state(CONV)


# ---------------------------------------------------------------------------
# One real send per wire shape
# ---------------------------------------------------------------------------


def _authored(role: str, text: str) -> UnifiedMessage:
    message = UnifiedMessage(role=role, content=[TextContent(text=text)])
    message.metadata = {"cache_template": "stable"}
    return message


def _tool_schema() -> dict[str, Any]:
    return {"type": "object", "properties": {"q": {"type": "string", "description": "What to look up."}}, "required": ["q"]}


def _config(*, typed: str = TYPED, schema: dict[str, Any] | None = None, slots: dict[Any, str] | None = None) -> UnifiedConfig:
    config = UnifiedConfig(
        model="m",
        messages=[],
        custom_tools=[{"name": "lookup", "description": "Look something up.", "input_schema": schema or _tool_schema()}],
    )
    config.messages = MessageList(_messages=[_authored("user", TEMPLATE), _authored("assistant", "Understood.")])
    config.system_instruction = SYSTEM
    config.stream = False
    config.messages.append_or_extend_user_input(typed)
    for slot, text in (slots or {"live_date": MARK}).items():
        config.messages.attach_turn_context(text, slot=slot)
    return config


def _build(shape: str, config: UnifiedConfig) -> Any:
    import importlib

    module, cls, wire_format, _provider = SHAPES[shape]
    profile = make_profile(model_name="m", wire_format=wire_format)
    prep = order_for_wire(config, profile)
    translator = getattr(importlib.import_module(module), cls)()
    return translator.build_request(prep.wire_config if prep.wire_config is not None else config, profile)


async def _sdk_send(shape: str, request: Any, seen: list[bytes]) -> None:
    import anthropic
    import openai

    from matrx_ai.providers.outbound_capture import resolve_sdk_httpx

    sdk = anthropic if shape == "anthropic" else openai
    flavor = resolve_sdk_httpx(sdk)  # the httpx flavor the SDK itself is built on

    def handler(http_request: Any) -> Any:
        seen.append(http_request.content)
        return flavor.Response(200, json=REPLIES[shape])

    http = make_capture_http_client(sdk=sdk, transport=flavor.MockTransport(handler))
    if shape == "anthropic":
        request = {"max_tokens": 64, **request}  # the API class sets it from the model's limit
        client = anthropic.AsyncAnthropic(api_key="test", base_url=URLS[shape], http_client=http, max_retries=0)
        await client.messages.create(**route_undeclared_params(client.messages.create, request, provider="anthropic"))
    elif shape == "responses":
        client = openai.AsyncOpenAI(api_key="test", base_url=URLS[shape], http_client=http, max_retries=0)
        await client.responses.create(**route_undeclared_params(client.responses.create, request, provider="openai"))
    else:
        client = openai.AsyncOpenAI(api_key="test", base_url=URLS[shape], http_client=http, max_retries=0)
        create = client.chat.completions.create
        await create(**route_undeclared_params(create, request, provider="openai"))
    await http.aclose()


async def _genai_send(request: Any, seen: list[bytes], monkeypatch: pytest.MonkeyPatch) -> None:
    from google import genai
    from google.genai import _api_client

    async def transport(self: Any, http_request: Any, stream: bool = False, **_kw: Any) -> Any:
        data = http_request.data
        seen.append(data if isinstance(data, bytes) else json.dumps(data).encode("utf-8"))
        return _api_client.HttpResponse({}, response_stream=[json.dumps(REPLIES["genai"])])

    monkeypatch.setattr(_api_client.BaseApiClient, "_async_request_once", transport)
    monkeypatch.setattr(request_capture, "_GENAI_INSTALLED", False)
    request_capture.install_genai_capture()  # THE patched last pre-transport step, over the recorder
    client = genai.Client(api_key="test")
    generate = client.aio.models.generate_content
    await generate(**route_undeclared_params(generate, request, provider="google"))


async def _xai_send(config: UnifiedConfig, seen: list[bytes], monkeypatch: pytest.MonkeyPatch) -> None:
    """The REAL ``XAIChat.execute`` (translator, call meta, the observer's call site) over a stubbed
    xai_sdk client: ``chat.create`` builds the request proto; the bytes the stub would send are read
    where the SDK would send them."""
    from matrx_ai.providers.xai import xai_api

    class _StubChat:
        def __init__(self, **kwargs: Any) -> None:
            self._proto = chat_pb2.GetCompletionsRequest(model=str(kwargs.get("model") or "m"))
            for message in kwargs.get("messages") or []:
                self._proto.messages.append(message)
            for tool in kwargs.get("tools") or []:
                self._proto.tools.append(tool)
            self._stub = object()

    class _Chats:
        def create(self, **kwargs: Any) -> _StubChat:
            return _StubChat(**kwargs)

    class _Client:
        chat = _Chats()

    class _XAI(xai_api.XAIChat):
        client = _Client()  # type: ignore[assignment]

        async def _execute_non_streaming(self, chat: Any, *_a: Any, **_k: Any) -> Any:
            seen.append(chat._proto.SerializeToString(deterministic=True))
            return "sent"

    ctx = _Ctx()
    monkeypatch.setattr("matrx_ai.context.app_context.get_app_context", lambda: ctx)
    profile = make_profile(model_name="m", wire_format=SHAPES["xai"][2])
    prep = order_for_wire(config, profile)
    result = await _XAI().execute(prep.wire_config if prep.wire_config is not None else config, profile)
    assert result == "sent"


def _send(shape: str, monkeypatch: pytest.MonkeyPatch, config: UnifiedConfig | None = None) -> tuple[str, Any]:
    """One real send: ``("ok", transport bytes)`` or ``("raised", exception type)``."""
    seen: list[bytes] = []

    async def run() -> None:
        set_call_meta(CallMeta(provider=SHAPES[shape][3], model="m"))
        if shape == "xai":
            await _xai_send(config or _config(), seen, monkeypatch)
            await fos.wait_for_pending()
            return
        request = _build(shape, config or _config())
        if shape == "genai":
            await _genai_send(request, seen, monkeypatch)
        else:
            await _sdk_send(shape, request, seen)
        await fos.wait_for_pending()

    try:
        asyncio.run(run())
    except BaseException as exc:  # noqa: BLE001 — the outcome is compared, whatever it is
        return "raised", type(exc)
    return "ok", seen


def _observers_off(monkeypatch: pytest.MonkeyPatch) -> None:
    """The baseline: every observer is a no-op (nothing the seal added can touch the send)."""
    monkeypatch.setattr(fos.SealLocator, "before", lambda *_a, **_k: None)
    monkeypatch.setattr(fos.SealLocator, "finish", lambda *_a, **_k: None)
    monkeypatch.setattr(fos, "observe_wire_body", lambda **_k: None)
    monkeypatch.setattr(fos, "observe_xai_request", lambda *_a, **_k: None)
    monkeypatch.setattr(residual_check, "note_wire_source", lambda *_a, **_k: None)


def _baseline(shape: str, config_factory: Callable[[], UnifiedConfig] = _config) -> tuple[str, Any]:
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("matrx_connect.context.app_context.try_get_app_context", lambda: _Ctx())
        _observers_off(mp)
        outcome = _send(shape, mp, config_factory())
    fos.reset_for_tests()
    declaration_ledger.reset_for_tests()
    reset_loop_state(CONV)
    return outcome


def _raiser(error: type[BaseException]) -> Callable[..., Any]:
    def boom(*_a: Any, **_k: Any) -> Any:
        raise error("injected by the guard")

    return boom


# ---------------------------------------------------------------------------
# The observed send equals the observer-free send, observers on
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("shape", list(SHAPES))
def test_an_observed_send_is_byte_identical_to_an_unobserved_one(shape: str, monkeypatch: pytest.MonkeyPatch) -> None:
    base = _baseline(shape)
    assert base[0] == "ok" and base[1], f"{shape}: the baseline send itself failed: {base}"
    observed = _send(shape, monkeypatch)
    assert observed == base
    assert fos.take_seal_records(CONV), f"{shape}: the observer never ran — this guard would prove nothing"


# ---------------------------------------------------------------------------
# Each piece raising in turn
# ---------------------------------------------------------------------------

#: name -> how to make it raise (monkeypatch, error, shape) — every piece the seal added on the path.
PIECES: dict[str, Callable[[pytest.MonkeyPatch, type[BaseException], str], None]] = {
    "_target_for": lambda mp, e, s: mp.setattr(fos, "_target_for", _raiser(e)),
    "locator before": lambda mp, e, s: mp.setattr(fos, "_content_len", _raiser(e)),
    "locator finish": lambda mp, e, s: mp.setattr(fos.SealLocator, "_resolve", _raiser(e)),
    "locator stamp": lambda mp, e, s: mp.setattr(fos.SealLocator, "_stamp", _raiser(e)),
    "_send_identity": lambda mp, e, s: mp.setattr(fos, "_send_identity", _raiser(e)),
    "_fingerprint": lambda mp, e, s: (
        mp.setattr(fos, "_fingerprint", _raiser(e)),
        mp.setattr(fos, "_fingerprint_xai", _raiser(e), raising=False),
    ),
    "segments": lambda mp, e, s: (
        mp.setattr(fos, "segments_xai", _raiser(e))
        if s == "xai"
        else mp.setitem(fos._PARSERS, FOS_SHAPE[s], _raiser(e))
    ),
    "check_and_remember": lambda mp, e, s: mp.setattr(fos, "check_and_remember", _raiser(e)),
    "_store": lambda mp, e, s: mp.setattr(fos, "_store", _raiser(e)),
    "dispatcher": lambda mp, e, s: mp.setattr(fos, "_ensure_dispatcher", _raiser(e)),
    "worker process": lambda mp, e, s: mp.setattr(fos, "_run_in_worker", _raiser(e)),
    "worker answers an error": lambda mp, e, s: mp.setattr(fos, "_run_in_worker", lambda _p: {"error": e.__name__}),
    "worker answers garbage": lambda mp, e, s: mp.setattr(fos, "_run_in_worker", lambda _p: {"fidelity": 1}),
    "observe_xai_request": lambda mp, e, s: mp.setattr(fos, "observe_xai_request", _raiser(e)),
    "observe_wire_body": lambda mp, e, s: mp.setattr(fos, "observe_wire_body", _raiser(e)),
    "canonical_json": lambda mp, e, s: mp.setattr(declaration_ledger, "canonical_json", _raiser(e)),
    # The residual check (P1a): its source note on the send path, its knob, and the check itself.
    "note_wire_source": lambda mp, e, s: mp.setattr(residual_check, "note_wire_source", _raiser(e)),
    "residual knob": lambda mp, e, s: mp.setattr(residual_check, "residual_check_enabled", _raiser(e)),
    "platform_patterns": lambda mp, e, s: mp.setattr(residual_check, "platform_patterns", _raiser(e)),
    "report_residual": lambda mp, e, s: mp.setattr(residual_check, "report_residual", _raiser(e)),
    "residual known_texts": lambda mp, e, s: mp.setattr(residual_check, "known_texts", _raiser(e)),
}


_BASELINES: dict[str, tuple[str, Any]] = {}


def _cached_baseline(shape: str) -> tuple[str, Any]:
    if shape not in _BASELINES:
        _BASELINES[shape] = _baseline(shape)
    return _BASELINES[shape]


@pytest.mark.parametrize("error", ERRORS, ids=lambda e: e.__name__)
@pytest.mark.parametrize("piece", list(PIECES))
@pytest.mark.parametrize("shape", list(SHAPES))
def test_any_seal_piece_raising_leaves_the_send_byte_identical(
    shape: str, piece: str, error: type[BaseException], monkeypatch: pytest.MonkeyPatch
) -> None:
    base = _cached_baseline(shape)
    assert base[0] == "ok", base
    PIECES[piece](monkeypatch, error, shape)
    assert _send(shape, monkeypatch) == base, f"{shape}: {piece} raising {error.__name__} changed the send"


@pytest.mark.parametrize("error", ERRORS, ids=lambda e: e.__name__)
def test_a_failing_seal_record_never_costs_the_turn_its_other_conversation_fields(
    error: type[BaseException], monkeypatch: pytest.MonkeyPatch
) -> None:
    """``take_seal_records`` / ``merged_seal_state`` raising inside ``_refresh_cache_state``: the
    turn's other cache facts and its context breakdown still reach the conversation update."""
    from matrx_ai.db import persistence

    written: list[dict[str, Any]] = []

    class _Conversation:
        async def load_conversation_by_id(self, _cid: str) -> Any:
            class _Row:
                cache_state = {"cumulative_trimmable_chars": 5}

            return _Row()

    class _Cxm:
        conversation = _Conversation()

    monkeypatch.setattr(persistence, "_cxm", lambda: _Cxm())
    monkeypatch.setattr(persistence, "_get_live_coordinator", lambda: object())
    monkeypatch.setattr(persistence, "_queue_conversation_update", lambda _cid, **fields: written.append(fields))
    monkeypatch.setattr(
        "matrx_ai.config.send_boundary.take_context_breakdown", lambda _cid: {"sections": ["system"]}
    )
    for target in ("take_seal_records", "merged_seal_state"):
        written.clear()
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(fos, target, _raiser(error))
            asyncio.run(
                persistence._refresh_cache_state(CONV, [{"provider": "anthropic", "ai_model": "m"}], None)
            )
        assert written, f"{target} raising {error.__name__} lost the conversation update"
        state = written[0]["cache_state"]
        assert state["last_model"] == "m" and state["last_provider"] == "anthropic" and state["last_response_at"]
        assert state["cumulative_trimmable_chars"] == 5
        assert written[0]["last_context_breakdown"] == {"sections": ["system"]}


@pytest.mark.parametrize("error", ERRORS, ids=lambda e: e.__name__)
def test_the_capture_keeps_its_record_when_the_line_cannot_be_read(
    error: type[BaseException], monkeypatch: pytest.MonkeyPatch
) -> None:
    """``current_seal_stamp`` raising in the capture's ``_finish``: the request is still captured."""
    monkeypatch.setattr(fos, "current_seal_stamp", _raiser(error))
    with request_capture.capturing_provider_request() as slot:
        try:
            request_capture.capture_wire_request(
                method="post", url="https://api.anthropic.com/v1/messages", headers={}, body=b'{"a":1}'
            )
        except request_capture.ProviderRequestCaptured:
            pass
    assert slot.captured is not None and slot.seal is None


def _import_and_call_sit_in_their_own_try(module: Any, name: str) -> bool:
    """Whether ``from ... import name`` and the call of ``name`` sit in a try of their OWN (only
    those statements) that catches ``Exception`` — so neither can stop the code around it."""
    import ast

    from matrx_utils.source_guard import stable_source

    for node in ast.walk(ast.parse(stable_source(module))):
        if not isinstance(node, ast.Try) or len(node.body) > 2:
            continue
        catches = any(
            h.type is None or (isinstance(h.type, ast.Name) and h.type.id in {"Exception", "BaseException"})
            for h in node.handlers
        )
        imported = any(
            isinstance(stmt, ast.ImportFrom) and any(a.name == name for a in stmt.names) for stmt in node.body
        )
        called = any(
            isinstance(stmt, ast.Expr)
            and isinstance(stmt.value, ast.Call)
            and isinstance(stmt.value.func, ast.Name)
            and stmt.value.func.id == name
            for stmt in node.body
        )
        if catches and imported and called:
            return True
    return False


def test_the_resolver_and_the_xai_client_guard_the_observer_import_and_call() -> None:
    """The two call sites outside this module: the resolver's row note and the xAI client's
    observer. An import that fails (a broken module, MemoryError) must not stop either."""
    from matrx_ai.agents import resolver
    from matrx_ai.providers.xai import xai_api

    assert _import_and_call_sit_in_their_own_try(resolver, "note_conversation_row_read")
    assert _import_and_call_sit_in_their_own_try(xai_api, "observe_xai_request")


@pytest.mark.parametrize("error", ERRORS, ids=lambda e: e.__name__)
def test_the_row_note_never_raises(error: type[BaseException]) -> None:
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(fos, "_LOCK", _RaisingLock(error))
        fos.note_conversation_row_read(CONV, known=False)


class _RaisingLock:
    def __init__(self, error: type[BaseException]) -> None:
        self.error = error

    def __enter__(self) -> Any:
        raise self.error("injected")

    def __exit__(self, *_a: Any) -> None:
        return None


@pytest.mark.parametrize("error", ERRORS, ids=lambda e: e.__name__)
def test_a_failing_wire_hydration_never_fails_the_send(error: type[BaseException], monkeypatch: pytest.MonkeyPatch) -> None:
    """The ledger's wire-text hydration raising: the send goes out as a fresh ledger would send it."""
    from matrx_ai.orchestrator import executor

    base = _cached_baseline("anthropic")
    _send("anthropic", monkeypatch)
    record = declaration_ledger.export_record(CONV)
    assert record
    declaration_ledger.reset_for_tests()
    fos.reset_for_tests()
    monkeypatch.setattr(declaration_ledger, "_declaration_of", _raiser(error))

    class _Holder:
        tool_declarations = record

    executor._hydrate_tool_ledger(CONV, _Holder())
    assert _send("anthropic", monkeypatch) == base


# ---------------------------------------------------------------------------
# Hostile inputs: exactly what the send does with the observers off
# ---------------------------------------------------------------------------

HOSTILE: dict[str, Callable[[], UnifiedConfig]] = {
    "NaN": lambda: _config(
        schema={"type": "object", "properties": {"x": {"type": "number", "default": math.nan}}},
        typed="nan " + str(math.nan),
    ),
    "8 MB body": lambda: _config(typed="x" * (8 * 1024 * 1024)),
    "non-string slot keys": lambda: _config(slots={"live_date": MARK, 7: "<seven>7</seven>", ("t",): "<t>t</t>"}),
}


@pytest.mark.parametrize("hostile", list(HOSTILE))
@pytest.mark.parametrize("shape", list(SHAPES))
def test_hostile_inputs_behave_exactly_as_with_the_observers_off(
    shape: str, hostile: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    base = _baseline(shape, HOSTILE[hostile])
    observed = _send(shape, monkeypatch, HOSTILE[hostile]())
    assert observed == base, f"{shape}: {hostile} changed the send ({observed[0]} vs {base[0]})"
    if hostile != "NaN":  # a NaN the SDK itself refuses to serialize is refused with or without us
        assert observed[0] == "ok", f"{shape}: {hostile} failed the send: {observed}"


def _deep_schema(depth: int) -> dict[str, Any]:
    schema: dict[str, Any] = {"type": "string"}
    for _ in range(depth):
        schema = {"type": "object", "properties": {"n": schema}}
    return schema


@pytest.mark.parametrize("shape", list(SHAPES))
def test_a_2000_deep_schema_behaves_exactly_as_before_the_canonical_order(
    shape: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Before P0.2 the ledger kept a plain copy of each declaration; with observers off and that
    copy, the outcome is the same as today's (whatever it is: sent, or refused before sending)."""
    factory = lambda: _config(schema=_deep_schema(2000))  # noqa: E731
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(declaration_ledger, "canonical_json", copy.deepcopy)
        mp.setattr(declaration_ledger, "canonical_tool_array", lambda decls, **_k: decls)
        before = _baseline(shape, factory)
    now = _send(shape, monkeypatch, factory())
    if before[0] == "raised":
        assert now == before
    else:
        assert now[0] == "ok" and [len(b) for b in now[1]] == [len(b) for b in before[1]]


# ---------------------------------------------------------------------------
# Latency: measured, never guessed
# ---------------------------------------------------------------------------


def _anthropic_body(size: int) -> bytes:
    filler = "y" * max(size - 2000, 0)
    return json.dumps(
        {
            "model": "m",
            "tools": [{"name": "lookup", "input_schema": _tool_schema()}],
            "system": [{"type": "text", "text": SYSTEM}],
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": TEMPLATE + filler}]},
                {"role": "assistant", "content": [{"type": "text", "text": "Understood."}]},
                {"role": "user", "content": [{"type": "text", "text": MARK}, {"type": "text", "text": TYPED}]},
            ],
        }
    ).encode()


def _realistic_body(messages: int = 240) -> bytes:
    """A body shaped like a long real conversation: ~250 KB, 240 messages of mixed lengths and
    roles, non-ASCII text (escaped by the SDK exactly as on the wire), tool calls and results."""
    words = ["planificación", "Überblick", "naïve", "東京の天気", "résumé", "Ελληνικά", "emoji 🚀", "plain words"]
    out: list[dict[str, Any]] = []
    for index in range(messages):
        text = " ".join(words[(index + k) % len(words)] for k in range(17 + (index * 37) % 52))
        role = "user" if index % 2 == 0 else "assistant"
        content: list[dict[str, Any]] = [{"type": "text", "text": f"[{index}] {text}"}]
        if role == "assistant" and index % 6 == 1:
            content.append({"type": "tool_use", "id": f"t{index}", "name": "lookup", "input": {"q": text[:80]}})
        out.append({"role": role, "content": content})
    return json.dumps(
        {"model": "m", "tools": [{"name": "lookup", "input_schema": _tool_schema()}], "system": SYSTEM, "messages": out}
    ).encode()


def _loop_side_cost(observe: Callable[[], Any], runs: int = 200) -> tuple[float, float, float]:
    """(median, p90, max) milliseconds the event loop spends in ``observe`` (the workers drain
    between runs, so each measurement is the hook's own cost, not a queue)."""
    timings: list[float] = []

    async def run() -> None:
        for _ in range(runs):
            began = time.perf_counter()
            assert observe() is None  # handed to the pool, never fingerprinted on the loop
            timings.append((time.perf_counter() - began) * 1000)
            await fos.wait_for_pending()

    asyncio.run(run())
    timings.sort()
    return statistics.median(timings), timings[int(len(timings) * 0.9)], timings[-1]


def test_the_event_loop_side_of_a_realistic_send_is_well_under_a_millisecond() -> None:
    body = _realistic_body()
    assert 200 * 1024 < len(body) < 256 * 1024  # under the retired inline limit: the case that cost 4 ms

    def observe() -> Any:
        set_call_meta(CallMeta(provider="anthropic", model="m"))
        fos.stamp_seal(fos.SealStamp(fos.SHAPE_ANTHROPIC, 230, None))
        return fos.observe_wire_body(url="https://api.anthropic.com/v1/messages", body=body)

    median, p90, worst = _loop_side_cost(observe)
    print(f"seal hook on the loop, {len(body) // 1024} KB / 240 messages: median {median:.3f} ms, p90 {p90:.3f} ms, max {worst:.3f} ms")
    assert median < 0.5, f"loop-side median {median:.3f} ms"
    assert fos.take_seal_records(CONV)  # and the worker did the fingerprint


def test_the_event_loop_side_of_a_genai_send_is_well_under_a_millisecond() -> None:
    contents = [
        {"role": "user" if i % 2 == 0 else "model", "parts": [{"text": json.loads(_realistic_body(1))["messages"][0]["content"][0]["text"]}]}
        for i in range(240)
    ]
    body = {"systemInstruction": {"parts": [{"text": SYSTEM}]}, "contents": contents}
    url = "https://generativelanguage.googleapis.com/v1beta/models/m:generateContent"

    def observe() -> Any:
        set_call_meta(CallMeta(provider="google", model="m"))
        fos.stamp_seal(fos.SealStamp(fos.SHAPE_GOOGLE, 230, None))
        return fos.observe_wire_body(url=url, body_obj=body, always_off_loop=True)

    median, p90, worst = _loop_side_cost(observe)
    print(f"seal hook on the loop, genai 240 contents: median {median:.3f} ms, p90 {p90:.3f} ms, max {worst:.3f} ms")
    assert median < 0.5, f"loop-side median {median:.3f} ms"


def test_an_xai_request_is_fingerprinted_off_the_loop(monkeypatch: pytest.MonkeyPatch) -> None:
    proto = chat_pb2.GetCompletionsRequest(model="m")
    for index in range(240):
        role = chat_pb2.MessageRole.ROLE_USER if index % 2 == 0 else chat_pb2.MessageRole.ROLE_ASSISTANT
        proto.messages.add(role=role).content.add(text=f"[{index}] " + "東京の天気 planificación " * 50)

    class _Chat:
        _proto = proto

    pids: list[int] = []
    real = fos._run_in_worker

    def spy(payload: Any) -> Any:
        result = real(payload)
        pids.append(result["pid"])
        return result

    monkeypatch.setattr(fos, "_run_in_worker", spy)

    def observe() -> Any:
        set_call_meta(CallMeta(provider="xai", model="m"))
        fos.stamp_seal(fos.SealStamp(fos.SHAPE_XAI, 230, None))
        return fos.observe_xai_request(_Chat())

    median, p90, worst = _loop_side_cost(observe)
    print(f"seal hook on the loop, xAI {proto.ByteSize() // 1024} KB / 240 messages: median {median:.3f} ms, p90 {p90:.3f} ms, max {worst:.3f} ms")
    assert median < 0.5, f"loop-side median {median:.3f} ms"
    import os

    assert pids and all(pid != os.getpid() for pid in pids)  # parsed in the worker process
    assert fos.take_seal_records(CONV)


# ---------------------------------------------------------------------------
# The bounds the audit asked for
# ---------------------------------------------------------------------------


def test_pending_jobs_are_capped_by_bytes_not_only_by_count(monkeypatch: pytest.MonkeyPatch) -> None:
    import threading

    gate = threading.Event()
    real = fos._run_in_worker

    def slow(payload: Any) -> Any:
        gate.wait(5)
        return real(payload)

    monkeypatch.setattr(fos, "_run_in_worker", slow)
    monkeypatch.setattr(fos, "seal_pending_max", lambda: 1000)
    monkeypatch.setattr(fos, "seal_pending_max_bytes", lambda: 3 * 1024 * 1024)
    body = _anthropic_body(1024 * 1024)

    async def run() -> tuple[int, int]:
        for _ in range(10):
            set_call_meta(CallMeta(provider="anthropic", model="m"))
            fos.stamp_seal(fos.SealStamp(fos.SHAPE_ANTHROPIC, 2, 1))
            fos.observe_wire_body(url="https://api.anthropic.com/v1/messages", body=body)
        held = (len(fos._PENDING), fos._PENDING_BYTES[0])
        gate.set()
        await fos.wait_for_pending()
        return held

    jobs, held_bytes = asyncio.run(run())
    assert jobs == (3 * 1024 * 1024) // len(body) < 10 and held_bytes <= 3 * 1024 * 1024
    assert fos._PENDING_BYTES[0] == 0  # released as each job ends


def test_chunk_digests_kept_per_segment_are_bounded() -> None:
    segment = fos.segment_of("system", b"a" * (10 * 1024 * 1024))
    assert len(segment.chunks) + len(segment.tail) <= fos._HEAD_CHUNKS + fos._TAIL_CHUNKS
    persisted = segment.as_list(with_chunks=False)
    assert len(persisted[3]) <= fos._PERSISTED_HEAD_CHUNKS and len(persisted[4]) <= fos._PERSISTED_TAIL_CHUNKS


@pytest.mark.parametrize("stored", [False, True], ids=["process memory", "cache_state"])
def test_a_tail_append_and_a_head_edit_are_located_to_a_chunk(stored: bool) -> None:
    """The live finding (2026-11-13): an edit appended at the END of a 26 KB system segment was
    reported "at byte unknown". Head and tail digests locate both ends."""
    text = bytes(range(32, 127)) * 300  # ~28 KB, every chunk distinct
    base = fos.segment_of("system", text)
    if stored:
        base = fos.Segment.from_list(base.as_list(with_chunks=False))
        assert base is not None
    appended = fos.segment_of("system", text + b" and one more rule.")
    low, high = fos._divergence(base, appended)
    last_chunk = (len(text) // fos.CHUNK_BYTES) * fos.CHUNK_BYTES
    assert high == last_chunk  # located to the chunk the append touched
    if not stored:
        assert low == high == last_chunk
    head = fos.segment_of("system", b"X" + text[1:])
    assert fos._divergence(base, head) == (0, 0)
    middle_at = 7 * fos.CHUNK_BYTES + 5
    middle = fos.segment_of("system", text[:middle_at] + b"#" + text[middle_at + 1 :])
    low, high = fos._divergence(base, middle)
    assert low <= 7 * fos.CHUNK_BYTES <= high


def test_the_event_loop_never_waits_for_a_busy_check_and_never_logs_under_the_lock(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    import logging
    import threading

    body = _anthropic_body(4096)

    def observe(request_id: str, *, changed: bool = False) -> Any:
        set_call_meta(CallMeta(provider="anthropic", model="m"))
        _Ctx.request_id = request_id
        fos.stamp_seal(fos.SealStamp(fos.SHAPE_ANTHROPIC, 2, 1))
        sent = body.replace(b"careful", b"CAREFUL") if changed else body
        return fos.observe_wire_body(url="https://api.anthropic.com/v1/messages", body=sent)

    # A worker holds the check and lets go only after 3 s: a loop that WAITED for it goes red
    # (elapsed ~3 s), never hangs.
    holding = threading.Event()

    def worker_holds_the_check() -> None:
        with fos._CHECK_LOCK:
            holding.set()
            time.sleep(3)

    holder = threading.Thread(target=worker_holds_the_check)
    holder.start()
    holding.wait(5)
    snapshot = fos.FinalOutboundSnapshot(
        provider="anthropic", model="m", conversation_id=CONV, request_id="req-busy", loop_round=0,
        fidelity="bytes", body_sha256="x", body_bytes=1, seal=fos.SealStamp(fos.SHAPE_ANTHROPIC, 1, None),
    )

    async def busy() -> tuple[list[str], float]:
        began = time.perf_counter()
        reported = fos.check_and_remember(snapshot)  # on the event-loop thread
        return reported, time.perf_counter() - began

    reported, elapsed = asyncio.run(busy())
    holder.join(10)
    assert elapsed < 0.05 and reported == []  # never waited; the check was skipped (said once)

    held: list[bool] = []

    class _Probe(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            if "static_seal_broken" in record.getMessage():
                held.append(fos._CHECK_LOCK.locked())

    probe = _Probe()
    logging.getLogger(fos.__name__).addHandler(probe)
    try:
        caplog.set_level(logging.WARNING)

        async def two() -> None:
            observe("req-1")
            await fos.wait_for_pending()
            observe("req-2", changed=True)
            await fos.wait_for_pending()

        asyncio.run(two())
        # And from a worker thread (blocking acquire): the report is logged after release too.
        thread = threading.Thread(target=lambda: observe("req-3"))
        thread.start()
        thread.join(5)
    finally:
        logging.getLogger(fos.__name__).removeHandler(probe)
    assert held and not any(held), "a seal report was logged while the check lock was held"


def test_a_genai_body_is_never_serialized_whole(monkeypatch: pytest.MonkeyPatch) -> None:
    """genai hands the observer the dict its transport dumps: only the segments above the line are
    serialized (a multi-MB inline image below it holds the GIL for nothing), no whole-body hash."""
    sizes: list[int] = []
    real_dumps = json.dumps

    class _Json:
        loads = staticmethod(json.loads)

        @staticmethod
        def dumps(*args: Any, **kwargs: Any) -> str:
            out = real_dumps(*args, **kwargs)
            sizes.append(len(out))
            return out

    monkeypatch.setattr(fos, "json", _Json)
    image = "A" * (6 * 1024 * 1024)
    body = {
        "systemInstruction": {"parts": [{"text": SYSTEM}]},
        "contents": [
            {"role": "user", "parts": [{"text": TEMPLATE}]},
            {"role": "user", "parts": [{"text": TYPED}, {"inlineData": {"mimeType": "image/png", "data": image}}]},
        ],
    }
    who = fos._Identity("google", "m", CONV, "req-1", 0, "agent-1", "loop")
    snapshot = fos._fingerprint(who, fos.SealStamp(fos.SHAPE_GOOGLE, 1, None), fos.SHAPE_GOOGLE, None, body, 1.0)
    assert snapshot is not None and snapshot.body_sha256 == "" and snapshot.parsed is False  # 6 MB > the parse line
    assert not sizes or max(sizes) < 64 * 1024
    small = {**body, "contents": [body["contents"][0], {"role": "user", "parts": [{"text": TYPED}]}]}
    sizes.clear()
    snapshot = fos._fingerprint(who, fos.SealStamp(fos.SHAPE_GOOGLE, 1, None), fos.SHAPE_GOOGLE, None, small, 2.0)
    assert snapshot is not None and snapshot.parsed and [s.label for s in snapshot.segments] == ["system", "message 0"]
    assert max(sizes) < 64 * 1024


def test_canonical_json_keeps_a_data_value_it_cannot_serialize_unchanged() -> None:
    """``const``/``enum``/``default``/``examples``/``example`` are the author's literal data: a value
    JSON cannot hold is kept as it was (copied), never turned into its ``str``; key order inside
    an ``example`` object is the author's."""
    from matrx_ai.config.canonical_order import canonical_json

    marker = frozenset({"a"})
    out = canonical_json({"type": "object", "default": {"when": marker}, "example": {"z": 1, "a": 2}})
    assert out["default"] == {"when": marker} and isinstance(out["default"]["when"], frozenset)
    assert list(out["example"]) == ["z", "a"]
    assert canonical_json(out) == out


def test_a_genai_job_is_charged_its_size_in_the_pending_cap(monkeypatch: pytest.MonkeyPatch) -> None:
    import threading

    gate = threading.Event()
    real = fos._run_in_worker
    monkeypatch.setattr(fos, "_run_in_worker", lambda p: (gate.wait(5), real(p))[1])
    text = "Ελληνικά " * 4000  # ~36 KB: under seal_genai_max_kb
    body = {"contents": [{"role": "user", "parts": [{"text": TYPED}, {"text": text}]}]}

    async def run() -> int:
        set_call_meta(CallMeta(provider="google", model="m"))
        fos.stamp_seal(fos.SealStamp(fos.SHAPE_GOOGLE, 0, None))
        fos.observe_wire_body(
            url="https://generativelanguage.googleapis.com/v1beta/models/m:generateContent", body_obj=body
        )
        held = fos._PENDING_BYTES[0]
        gate.set()
        await fos.wait_for_pending()
        return held

    assert asyncio.run(run()) >= len(text)


def test_a_big_genai_body_is_skipped_on_the_loop_and_said_once(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """Sending a dict to the worker process walks every node: above ``seal_genai_max_kb`` the job is
    skipped on the loop (said once), never queued."""
    import logging

    monkeypatch.setattr(fos, "_FAILED", set())
    caplog.set_level(logging.DEBUG, logger=fos.logger.name)
    image = "A" * (2 * 1024 * 1024)
    body = {"contents": [{"role": "user", "parts": [{"text": TYPED}, {"inlineData": {"mimeType": "image/png", "data": image}}]}]}

    async def run() -> int:
        set_call_meta(CallMeta(provider="google", model="m"))
        fos.stamp_seal(fos.SealStamp(fos.SHAPE_GOOGLE, 0, None))
        fos.observe_wire_body(
            url="https://generativelanguage.googleapis.com/v1beta/models/m:generateContent", body_obj=body
        )
        return len(fos._PENDING)

    assert asyncio.run(run()) == 0
    # An expected skip is announced ONCE as a skip at WARNING, never as an ERROR "failed" line
    # (live 2026-11-15: it read as OverflowError('more than 65536 bytes') and filed an app_log ERROR).
    mine = [r for r in caplog.records if "seal_genai_max_kb" in r.getMessage()]
    assert len(mine) == 1, [r.getMessage() for r in caplog.records]
    assert mine[0].levelno == logging.WARNING and "skipped" in mine[0].getMessage()
    assert "failed" not in mine[0].getMessage() and "OverflowError" not in mine[0].getMessage()
    assert not [r for r in caplog.records if r.levelno >= logging.ERROR and r.name == fos.logger.name]


# ---------------------------------------------------------------------------
# The residual check (PLAN §5.4, P1a): report-only, the subtraction in the worker process only
# ---------------------------------------------------------------------------

RESIDUAL_SHAPES = ["anthropic", "responses", "chat", "genai"]
PLANT = "Planted platform sentence that no registered block accounts for."


def _residual_reports(caplog: pytest.LogCaptureFixture) -> list[Any]:
    return [r for r in caplog.records if getattr(r, "kind", None) == residual_check.REPORT_KIND]


def _spy_residual(monkeypatch: pytest.MonkeyPatch) -> list[list[tuple[str, str]]]:
    """The residual each worker job computed (the subtraction runs in the worker process: its answer
    is read where the dispatcher receives it)."""
    ran: list[list[tuple[str, str]]] = []
    real = fos._run_in_worker

    def spy(payload: Any) -> Any:
        out = real(payload)
        if "known" in payload and isinstance(out, dict) and "residual" in out:
            ran.append([tuple(item) for item in out["residual"]])
        return out

    monkeypatch.setattr(fos, "_run_in_worker", spy)
    return ran


@pytest.mark.parametrize("shape", RESIDUAL_SHAPES)
def test_a_known_request_yields_no_residual_report(
    shape: str, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.WARNING)
    ran = _spy_residual(monkeypatch)
    assert _send(shape, monkeypatch)[0] == "ok"
    assert ran, f"{shape}: the residual check never ran — this guard would prove nothing"
    assert ran == [[]], ran
    assert not _residual_reports(caplog)


def _plant_in_person_turn(request: dict[str, Any], shape: str) -> None:
    """An unregistered sentence added on the wire after the translator rendered the send."""
    if shape == "responses":
        turns = [m for m in request["input"] if isinstance(m, dict) and m.get("role") == "user"]
    else:
        turns = [m for m in request["messages"] if isinstance(m, dict) and m.get("role") == "user"]
    turn = turns[-1]
    if isinstance(turn["content"], str):
        turn["content"] = f"{turn['content']}\n\n{PLANT}"
    else:
        kind = "input_text" if shape == "responses" else "text"
        turn["content"] = [*turn["content"], {"type": kind, "text": PLANT}]


@pytest.mark.parametrize("shape", ["anthropic", "responses", "chat"])
def test_a_planted_unregistered_addition_yields_exactly_one_report(
    shape: str, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.WARNING)
    ran = _spy_residual(monkeypatch)
    real_build = _build

    def planted_build(s: str, config: UnifiedConfig) -> Any:
        request = real_build(s, config)
        _plant_in_person_turn(request, s)
        return request

    monkeypatch.setitem(globals(), "_build", planted_build)
    # Two sends of the same conversation: one report (one per conversation per window).
    assert _send(shape, monkeypatch)[0] == "ok"
    assert _send(shape, monkeypatch)[0] == "ok"
    assert len(ran) == 2 and all(any(PLANT in text for _, text in r) for r in ran), ran
    reports = _residual_reports(caplog)
    assert len(reports) == 1, [r.getMessage() for r in reports]
    assert PLANT[:40] in reports[0].getMessage()


@pytest.mark.parametrize("piece", ["known_texts", "platform_patterns", "report_residual"])
@pytest.mark.parametrize("error", ERRORS, ids=lambda e: e.__name__)
@pytest.mark.parametrize("shape", RESIDUAL_SHAPES)
def test_an_exception_inside_the_residual_check_leaves_the_send_byte_identical(
    shape: str, error: type[BaseException], piece: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The server-side pieces raise here; the worker-side subtraction raising is an answer
    (``residual_error``), covered by ``test_static_seal_worker_process.py``."""
    base = _cached_baseline(shape)
    assert base[0] == "ok", base
    ran: list[int] = []

    def boom(*_a: Any, **_k: Any) -> Any:
        ran.append(1)
        raise error("injected inside the residual check")

    if piece == "report_residual":
        if shape == "genai":
            pytest.skip("the plant helper writes the httpx shapes; genai's reporter is the same code")
        real_build = _build

        def planted_build(s: str, config: UnifiedConfig) -> Any:
            request = real_build(s, config)
            _plant_in_person_turn(request, s)
            return request

        monkeypatch.setitem(globals(), "_build", planted_build)  # a residual, so the reporter is reached
        base = (base[0], None)
    monkeypatch.setattr(residual_check, piece, boom)
    outcome = _send(shape, monkeypatch)
    assert outcome[0] == "ok" and (base[1] is None or outcome == base)
    assert ran, f"{shape}: {piece} never ran — this guard would prove nothing"


def test_the_residual_check_never_runs_on_the_event_loop(monkeypatch: pytest.MonkeyPatch) -> None:
    """The subtraction runs in the worker process; its server side (known texts, the report) on the
    dispatcher thread — never the event loop."""
    import os
    import threading

    threads: list[str] = []
    pids: list[int] = []
    real_known = residual_check.known_texts
    real_run = fos._run_in_worker

    def spy_known(*args: Any, **kwargs: Any) -> Any:
        threads.append(threading.current_thread().name)
        return real_known(*args, **kwargs)

    def spy_run(payload: Any) -> Any:
        out = real_run(payload)
        if "known" in payload:
            pids.append(out["pid"])
        return out

    monkeypatch.setattr(residual_check, "known_texts", spy_known)
    monkeypatch.setattr(fos, "_run_in_worker", spy_run)
    assert _send("anthropic", monkeypatch)[0] == "ok"
    assert threads and all(name.startswith("static-seal") for name in threads), threads
    assert pids and all(pid != os.getpid() for pid in pids), pids


def test_the_knob_off_stops_the_residual_check(monkeypatch: pytest.MonkeyPatch) -> None:
    ran = _spy_residual(monkeypatch)
    monkeypatch.setattr(residual_check, "residual_check_enabled", lambda: False)
    assert _send("anthropic", monkeypatch)[0] == "ok"
    assert not ran


# --- the translator's source is recorded only for a send the residual check will read ---


def _source_after_note(provider: str = "anthropic") -> Any:
    residual_check.note_wire_source("config", ["message"], provider=provider)
    return residual_check._wire_source_var.get()


def test_the_source_is_recorded_for_a_checked_send() -> None:
    assert _source_after_note() == ("config", ["message"])


@pytest.mark.parametrize("why", ["seal off", "knob off", "xai", "no agent loop", "no conversation"])
def test_the_source_is_never_kept_for_a_send_that_is_not_checked(why: str, monkeypatch: pytest.MonkeyPatch) -> None:
    residual_check._wire_source_var.set(("stale config", ["stale"]))  # an earlier send's source
    provider = "anthropic"
    if why == "seal off":
        monkeypatch.setattr(fos, "seal_check_on", lambda: False)
    elif why == "knob off":
        monkeypatch.setattr(residual_check, "residual_check_enabled", lambda: False)
    elif why == "xai":
        provider = "xai"
    elif why == "no agent loop":
        monkeypatch.setattr(fos, "_in_agent_loop", lambda: False)
    else:
        monkeypatch.setattr(fos, "_app_context", lambda: None)
    assert _source_after_note(provider) is None


@pytest.mark.parametrize("error", ERRORS, ids=lambda e: e.__name__)
def test_noting_the_source_never_raises(error: type[BaseException], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(fos, "seal_check_on", _raiser(error))
    residual_check._wire_source_var.set(("stale config", ["stale"]))
    assert _source_after_note() is None


# --- the residual check never runs on the event loop or in the no-loop inline fallback ---


def _spy_check(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    import threading

    calls: list[str] = []
    monkeypatch.setattr(
        residual_check, "check_residual", lambda **_k: calls.append(threading.current_thread().name) or []
    )
    return calls


def test_the_residual_subtraction_runs_only_in_the_worker_process(monkeypatch: pytest.MonkeyPatch) -> None:
    """The seal's fingerprint left the server process (2026-11-13): the inline fingerprint takes no
    residual source at all, and a send on the loop hands the subtraction to the worker process."""
    import inspect
    import os

    assert "residual_source" not in inspect.signature(fos._fingerprint).parameters
    calls = _spy_check(monkeypatch)
    pids: list[int] = []
    real = fos._run_in_worker

    def spy(payload: Any) -> Any:
        out = real(payload)
        if "known" in payload and isinstance(out, dict) and "residual" in out:
            pids.append(out["pid"])
        return out

    monkeypatch.setattr(fos, "_run_in_worker", spy)
    assert _send("anthropic", monkeypatch)[0] == "ok"
    assert calls == []  # the in-process check is never called on the send path
    assert pids and all(pid != os.getpid() for pid in pids), "the worker never ran the residual — this guard would prove nothing"


def test_the_no_loop_inline_fallback_never_runs_the_residual_check(monkeypatch: pytest.MonkeyPatch) -> None:
    """``observe_wire_body`` with no running loop fingerprints inline: never with the residual check."""
    calls = _spy_check(monkeypatch)
    monkeypatch.setattr(residual_check, "_will_be_checked", lambda _p: True)
    residual_check.note_wire_source("config", [], provider="anthropic")
    set_call_meta(CallMeta(provider="anthropic", model="m"))
    fos.stamp_seal(fos.SealStamp(fos.SHAPE_ANTHROPIC, 0, under_sealed=True))
    body = json.dumps({"system": SYSTEM, "messages": [{"role": "user", "content": TYPED}]}).encode()
    snapshot = fos.observe_wire_body(url="https://api.anthropic.com/v1/messages", body=body)
    assert snapshot is not None, "the inline fallback never ran — this guard would prove nothing"
    assert calls == []


@pytest.mark.parametrize("shape", [s for s in SHAPES if s != "xai"])
def test_each_translator_names_its_provider_when_it_notes_the_source(shape: str, monkeypatch: pytest.MonkeyPatch) -> None:
    """``messages_for_wire`` forwards ``provider=`` to ``note_wire_source``: without it every send
    reads as provider "" and the xAI exclusion (proto bodies are never read) cannot apply."""
    seen: list[str] = []
    monkeypatch.setattr(
        residual_check, "note_wire_source", lambda _c, _m, *, provider="": seen.append(provider)
    )
    import importlib

    module, cls, _wire, _provider = SHAPES[shape]
    translator = getattr(importlib.import_module(module), cls)()
    expected = str(getattr(translator, "PROVIDER", "") or translator._provider_label())
    _build(shape, _config())
    assert expected and seen and all(p == expected for p in seen), (shape, expected, seen)
